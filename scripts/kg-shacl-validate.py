#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kg-shacl-validate.py
====================

KG SHACL/语义约束校验器（真约束版，替代原仅查 rdfs:label 的空壳校验）。

约束清单：
  C1 LABEL       (error)   所有带 rdf:type 的节点必须有非空 rdfs:label（pyshacl）
  C2 DANGLING    (error)   关系两端实体必须存在（jsonl 级 + ttl 级对象存在性）
  C3 CANONICAL   (error)   Standard/Protocol 实体名必须命中 canonical-names.yaml
                           登记（canonical/alias）或符合编号/版本模式
  C4 HISTORICAL  (error)   历史版本 Standard 不得冒充现行版：同族存在更新版本时，
                           必须有入向 EVOLVED_FROM 边或 context 中的版本语境标注
  C5 MULTI-DEF   (warning) Term 被 >5 个不同文件的 DEFINES 边连接（多定义告警，仅报告）
  I1 RANGE-DRIFT (info)    对象属性实际端点类型与本体声明 domain/range 的漂移（backlog）
  I2 DUP-VARIANT (info)    同族同版本/变体重复 Standard 实体（backlog，待重抽取归并）

退出码：任一 error 类约束（C1-C4）有命中 -> 1；仅 warning/info -> 0。

用法：
    python scripts/kg-shacl-validate.py
    python scripts/kg-shacl-validate.py --max-samples 20
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import yaml
from pyshacl import validate
from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, SH
from rdflib.namespace import XSD

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KG_DIR = PROJECT_ROOT / "struct" / "99-reference" / "knowledge-graph"
CANONICAL_YAML = PROJECT_ROOT / "struct" / "99-reference" / "tools" / "canonical-names.yaml"
REPORT_PATH = PROJECT_ROOT / "reports" / "kg-shacl-report.md"

BASE_URI = "https://github.com/AdaMartin18010/Architecture/kg/"
AR = Namespace(BASE_URI)
ARO = Namespace(BASE_URI + "ontology/")

OBJECT_PROPERTIES = [
    "defines", "references", "belongsTo", "providesPositiveExample",
    "providesNegativeExample", "mentions", "implementedBy", "relatedTo",
    "evolvedFrom",
]

# 本体声明的 domain/range（与 kg-builder.py PROPERTIES 同步，仅用于 I1 信息项）
DECLARED_ENDPOINTS = {
    "defines": ("File", {"Term"}),
    "references": ("File", {"File"}),
    "belongsTo": ("File", {"Topic"}),
    "providesPositiveExample": ("File", {"Term"}),
    "providesNegativeExample": ("File", {"Term"}),
    "mentions": ("File", {"Standard"}),
    "implementedBy": ("Entity", {"Tool"}),
    "relatedTo": ("Term", {"Entity"}),
    "evolvedFrom": ("Standard", {"Standard"}),
}
JSONL_REL_TO_PROP = {
    "DEFINES": "defines", "REFERENCES": "references", "BELONGS_TO": "belongsTo",
    "PROVIDES_POSITIVE_EXAMPLE": "providesPositiveExample",
    "PROVIDES_NEGATIVE_EXAMPLE": "providesNegativeExample",
    "MENTIONS": "mentions", "IMPLEMENTED_BY": "implementedBy",
    "RELATED_TO": "relatedTo", "EVOLVED_FROM": "evolvedFrom",
}

# C3 canonical 模式：未在 canonical-names.yaml 登记时，Standard/Protocol 名称
# 必须符合“组织 + 编号(+版本)”或公认版本线格式。
STD_PATTERNS = [
    r"^ISO/IEC/IEEE\s+\d+(-\d+)*(:\d{4})?$",
    r"^ISO/IEC\s+\d+(-\d+)*(:\d{4})?$",
    r"^ISO\s+\d+(-\d+)*(:\d{4})?$",
    r"^IEC(\s+(TS|TR))?\s+\d+(-\d+)*(:\d{4})?$",
    r"^IEEE(\s+Std)?\s+\d+(\.\d+)*(:\d{4})?$",
    r"^NIST\s+SP\s+800-\d+[A-Z]?$",
    r"^NIST\s+SSDF\s+\d+\.\d+$",
    r"^SLSA\s+\d+\.\d+$",
]
PROTO_PATTERNS = [
    r"^MCP\s+\d{4}-\d{2}-\d{2}(\s+RC)?$",
    r"^A2A\s+v?\d+\.\d+(\.\d+)?$",
]
STD_RES = [re.compile(p) for p in STD_PATTERNS]
PROTO_RES = [re.compile(p) for p in PROTO_PATTERNS]

VERSION_CONTEXT_RE = re.compile(
    r"历史|前身|上一代|旧版|已被.*取代|predecessor|superseded|historical|legacy",
    re.IGNORECASE,
)
MULTI_DEF_THRESHOLD = 5


# ---------------------------------------------------------------------------
# 数据加载
# ---------------------------------------------------------------------------

def load_entities(path: Path) -> Dict[str, dict]:
    out: Dict[str, dict] = {}
    with path.open(encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                o = json.loads(ln)
                out[o["id"]] = o
    return out


def load_relations(path: Path) -> List[dict]:
    out = []
    with path.open(encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                out.append(json.loads(ln))
    return out


def load_canonical_registry(path: Path) -> Set[str]:
    """canonical + aliases（小写）集合。"""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    names: Set[str] = set()
    for entry in data.get("standards", []) or []:
        canon = (entry.get("canonical") or "").strip()
        if canon:
            names.add(canon.lower())
        for a in entry.get("aliases", []) or []:
            if isinstance(a, str) and a.strip():
                names.add(a.strip().lower())
    return names


# ---------------------------------------------------------------------------
# C1/C2-ttl: pyshacl 真约束
# ---------------------------------------------------------------------------

def build_shacl_shapes() -> Graph:
    """label 非空 + 对象属性值必须是有类型的实体节点（dangling 存根即失败）。"""
    g = Graph()
    g.bind("sh", SH)
    g.bind("aro", ARO)
    g.bind("rdf", RDF)
    g.bind("rdfs", RDFS)

    # C1: 任何实体（带 ar:sourceFile）必须有非空 rdfs:label
    # 不用 targetSubjectsOf rdf:type：rdfs 推理会给字面量补 rdf:type 产生误报
    label_shape = URIRef(BASE_URI + "shapes/EntityLabelShape")
    ps = URIRef(BASE_URI + "shapes/EntityLabelProp")
    g.add((label_shape, RDF.type, SH.NodeShape))
    g.add((label_shape, SH.targetSubjectsOf, AR.sourceFile))
    g.add((label_shape, SH.property, ps))
    g.add((ps, SH.path, RDFS.label))
    g.add((ps, SH.minCount, Literal(1)))
    g.add((ps, SH.minLength, Literal(1)))

    # C2(ttl): 每个对象属性的值必须是有 rdf:type 的节点（dangling 存根无类型）
    for prop in OBJECT_PROPERTIES:
        ns = URIRef(BASE_URI + f"shapes/{prop}ObjectExistsShape")
        sparql = Literal(
            "PREFIX aro: <" + str(ARO) + ">\n"
            "SELECT $this ?value WHERE {\n"
            f"  $this aro:{prop} ?value .\n"
            "  FILTER NOT EXISTS { ?value a ?anyType }\n"
            "}",
            datatype=XSD.string,
        )
        g.add((ns, RDF.type, SH.NodeShape))
        g.add((ns, SH.targetSubjectsOf, ARO[prop]))
        g.add((ns, SH.sparql, URIRef(BASE_URI + f"shapes/{prop}ObjectExistsSparql")))
        qn = URIRef(BASE_URI + f"shapes/{prop}ObjectExistsSparql")
        g.add((qn, RDF.type, SH.SPARQLConstraint))
        g.add((qn, SH.select, sparql))
        g.add((qn, SH.message, Literal(f"aro:{prop} 的对象不是已定义实体（dangling）")))
    return g


def run_shacl(ttl_path: Path) -> Tuple[bool, Counter, List[Tuple[str, str]], str]:
    """返回 (conforms, 每约束命中数, 样例[(shape, focus)], pyshacl 文本)。"""
    data = Graph()
    data.parse(str(ttl_path), format="turtle")
    # 注意：必须用 inference="none"——pyshacl 在 rdfs 推理下 SPARQL 约束不响應，
    # 且数据图所有实体均显式带 rdf:type，无需推理。
    conforms, results_graph, results_text = validate(
        data, shacl_graph=build_shacl_shapes(), inference="none",
        abort_on_first=False, meta_shacl=False, debug=False,
    )
    counts: Counter = Counter()
    samples: List[Tuple[str, str]] = []
    for r in results_graph.subjects(RDF.type, SH.ValidationResult):
        shape = results_graph.value(r, SH.sourceShape)
        focus = results_graph.value(r, SH.focusNode)
        shape_name = str(shape).rsplit("/", 1)[-1] if shape else "unknown"
        counts[shape_name] += 1
        if len(samples) < 60:
            samples.append((shape_name, str(focus)))
    return conforms, counts, samples, results_text


# ---------------------------------------------------------------------------
# C2: jsonl 级 dangling
# ---------------------------------------------------------------------------

def check_dangling(entities: Dict[str, dict], relations: List[dict]):
    missing_src, missing_tgt = [], []
    for r in relations:
        if r["source_id"] not in entities:
            missing_src.append(r)
        if r["target_id"] not in entities:
            missing_tgt.append(r)
    return missing_src, missing_tgt


# ---------------------------------------------------------------------------
# C3: canonical 名称
# ---------------------------------------------------------------------------

def check_canonical(entities: Dict[str, dict], registry: Set[str]):
    violations = []
    for o in entities.values():
        t, name = o.get("type"), o.get("name", "")
        if t == "Standard":
            pats = STD_RES
        elif t == "Protocol":
            pats = PROTO_RES
        else:
            continue
        if name.lower() in registry:
            continue
        if any(p.match(name) for p in pats):
            continue
        violations.append(o)
    return violations


# ---------------------------------------------------------------------------
# C4: 历史版本不得冒充现行版
# ---------------------------------------------------------------------------

def parse_family_version(name: str) -> Optional[Tuple[str, Tuple[int, ...]]]:
    """提取 (族键, 版本元组)。无显式版本返回 None。

    注意：NIST SP 800-xxx 是文档编号（非版本），IEEE 802.x / IEC 62443-4-2
    中的点分/连字符编号同理，只有 `:YYYY` 或尾部 `x.y` 才算版本。
    """
    s = name.strip()
    # NIST SP 800-204 / 800-204A：纯文档编号，无版本概念
    if re.match(r"^NIST\s+SP\s+800-\d+[A-Z]?$", s):
        return None
    # ISO/IEC/IEEE 42010:2022 -> family "42010", ver (2022,)
    # IEC 62443-4-2:2019 -> family "62443-4-2", ver (2019,)
    # IEEE 802.1 -> family "802.1", 无版本 -> None
    m = re.match(r"^(?:ISO(?:/IEC(?:/IEEE)?)?|IEC|IEEE)(?:\s+(?:TS|TR|Std))?\s+(\d+(?:[.\-]\d+)*)(?::(\d{4}))?$", s)
    if m:
        return (m.group(1), (int(m.group(2)),)) if m.group(2) else None
    # SLSA 1.2 / NIST SSDF 1.1 / ArchiMate 3.2 / DMN 1.5 / BPMN 2.0 / A2A v1.0.0
    m = re.match(r"^([A-Za-z][A-Za-z0-9 ]*?)\s+v?(\d+(?:\.\d+)+)(?:\s+RC)?$", s)
    if m:
        fam = re.sub(r"[\s]+", "", m.group(1)).lower()
        ver = tuple(int(x) for x in m.group(2).split("."))
        return fam, ver
    return None


def _is_prefix(a: Tuple[int, ...], b: Tuple[int, ...]) -> bool:
    return len(a) < len(b) and b[: len(a)] == a


def check_historical(entities: Dict[str, dict], relations: List[dict]):
    evolved_targets = {r["target_id"] for r in relations if r["relation"] == "EVOLVED_FROM"}
    fam: Dict[str, List[Tuple[Tuple[int, ...], dict]]] = defaultdict(list)
    for o in entities.values():
        if o.get("type") != "Standard":
            continue
        pv = parse_family_version(o.get("name", ""))
        if pv:
            fam[pv[0]].append((pv[1], o))
    violations = []
    for f, members in fam.items():
        vers = sorted({v for v, _ in members})
        for ver, o in members:
            newer = [v for v in vers if v > ver and not _is_prefix(ver, v)]
            if not newer:
                continue
            if o["id"] in evolved_targets:
                continue
            if VERSION_CONTEXT_RE.search(o.get("context", "") or ""):
                continue
            violations.append((o, max(newer)))
    return violations


# ---------------------------------------------------------------------------
# C5: 多定义告警
# ---------------------------------------------------------------------------

def check_multi_def(entities: Dict[str, dict], relations: List[dict]):
    defines: Dict[str, Set[str]] = defaultdict(set)
    for r in relations:
        if r["relation"] == "DEFINES":
            defines[r["target_id"]].add(r["source_id"])
    out = []
    for tid, files in defines.items():
        if len(files) > MULTI_DEF_THRESHOLD:
            name = entities.get(tid, {}).get("name", tid)
            out.append((name, tid, sorted(files)))
    out.sort(key=lambda x: -len(x[2]))
    return out


# ---------------------------------------------------------------------------
# I1/I2: 信息项
# ---------------------------------------------------------------------------

def check_range_drift(entities: Dict[str, dict], relations: List[dict]):
    drift = []
    for r in relations:
        prop = JSONL_REL_TO_PROP.get(r["relation"])
        if not prop or prop not in DECLARED_ENDPOINTS:
            continue
        dom, rng = DECLARED_ENDPOINTS[prop]
        s, t = entities.get(r["source_id"]), entities.get(r["target_id"])
        if not s or not t:
            continue
        st, tt = s.get("type"), t.get("type")
        ok_dom = dom == "Entity" or st == dom
        ok_rng = "Entity" in rng or tt in rng
        if not (ok_dom and ok_rng):
            drift.append((prop, st, tt, r))
    return drift


def check_dup_variants(entities: Dict[str, dict]):
    fam: Dict[str, List[Tuple[Optional[Tuple[int, ...]], dict]]] = defaultdict(list)
    for o in entities.values():
        if o.get("type") != "Standard":
            continue
        pv = parse_family_version(o.get("name", ""))
        key = pv[0] if pv else o.get("name", "").lower()
        fam[key].append((pv[1] if pv else None, o))
    dups = []
    for f, members in fam.items():
        if len(members) > 1:
            dups.append((f, sorted(m[1]["name"] for m in members)))
    dups.sort()
    return dups


# ---------------------------------------------------------------------------
# 报告
# ---------------------------------------------------------------------------

def fmt_samples(items, n, fmt):
    lines = [fmt(x) for x in items[:n]]
    if len(items) > n:
        lines.append(f"- ... 还有 {len(items) - n} 条")
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description="KG SHACL/语义约束校验器")
    ap.add_argument("--entities", type=Path, default=KG_DIR / "kg-entities.jsonl")
    ap.add_argument("--relations", type=Path, default=KG_DIR / "kg-relations.jsonl")
    ap.add_argument("--ttl", type=Path, default=KG_DIR / "kg.ttl")
    ap.add_argument("--registry", type=Path, default=CANONICAL_YAML)
    ap.add_argument("--report", type=Path, default=REPORT_PATH)
    ap.add_argument("--max-samples", type=int, default=15)
    args = ap.parse_args()

    entities = load_entities(args.entities)
    relations = load_relations(args.relations)
    registry = load_canonical_registry(args.registry)

    conforms, shacl_counts, shacl_samples, shacl_text = run_shacl(args.ttl)
    missing_src, missing_tgt = check_dangling(entities, relations)
    canonical_viol = check_canonical(entities, registry)
    historical_viol = check_historical(entities, relations)
    multi_def = check_multi_def(entities, relations)
    drift = check_range_drift(entities, relations)
    dups = check_dup_variants(entities)

    errors = {
        "C1 LABEL (pyshacl)": sum(shacl_counts.values()),
        "C2 DANGLING (jsonl)": len(missing_src) + len(missing_tgt),
        "C3 CANONICAL": len(canonical_viol),
        "C4 HISTORICAL": len(historical_viol),
    }
    passed = all(v == 0 for v in errors.values())
    n = args.max_samples

    lines: List[str] = []
    lines += [
        "# KG SHACL 验证报告",
        "",
        f"> **验证时间**: {datetime.now(timezone.utc).isoformat()}",
        f"> **验证结果**: {'✅ 通过' if passed else '❌ 未通过'}",
        f"> **校验器**: `scripts/kg-shacl-validate.py`（pyshacl + 自研语义约束）",
        f"> **数据**: {len(entities)} 实体 / {len(relations)} 关系 / canonical 登记 {len(registry)} 名",
        "",
        "## 约束命中汇总",
        "",
        "| 约束 | 级别 | 命中数 |",
        "|------|------|--------|",
    ]
    for k, v in errors.items():
        lines.append(f"| {k} | error（触发 exit 1） | {v} |")
    lines.append(f"| C2 DANGLING (ttl, pyshacl 对象存在性) | error | {'0' if conforms or not shacl_counts else '见 C1 列'} |")
    lines.append(f"| C5 MULTI-DEF (>{MULTI_DEF_THRESHOLD} 文件 DEFINES 同一 Term) | warning（仅报告） | {len(multi_def)} |")
    lines.append(f"| I1 RANGE-DRIFT（端点类型 vs 本体声明） | info | {len(drift)} |")
    lines.append(f"| I2 DUP-VARIANT（同族重复 Standard） | info | {len(dups)} |")
    lines.append("")

    # C1
    lines += ["## C1 LABEL — rdfs:label 非空（pyshacl）", ""]
    if shacl_counts:
        for shape, c in shacl_counts.items():
            lines.append(f"- `{shape}`: {c} 命中")
        lines += fmt_samples(shacl_samples, n, lambda x: f"- `{x[0]}` ← {x[1]}")
    else:
        lines.append("- ✅ 无违例：所有实体节点均有非空 rdfs:label；对象属性端点均为已定义实体。")
    lines.append("")

    # C2
    lines += ["## C2 DANGLING — 关系两端实体存在", ""]
    if not missing_src and not missing_tgt:
        lines.append("- ✅ 无 dangling：所有关系 source_id / target_id 均存在于 kg-entities.jsonl。")
    else:
        by_rel = Counter(r["relation"] for r in missing_src + missing_tgt)
        for rel, c in by_rel.items():
            lines.append(f"- `{rel}`: {c} 条")
        lines += fmt_samples(
            [("源缺失", r) for r in missing_src] + [("目标缺失", r) for r in missing_tgt],
            n,
            lambda x: f"- [{x[0]}] `{x[1]['source_id']}` -{x[1]['relation']}-> `{x[1]['target_id']}`",
        )
    lines.append("")

    # C3
    lines += ["## C3 CANONICAL — Standard/Protocol 名称规范", ""]
    lines.append("规则：命中 `canonical-names.yaml` 登记（canonical/alias），或匹配编号/版本模式 "
                 "（`ISO/IEC \\d+(-\\d+)?:\\d{4}` 等）。")
    lines.append("")
    if not canonical_viol:
        lines.append("- ✅ 无违例。")
    else:
        lines += fmt_samples(
            canonical_viol, n,
            lambda o: f"- [{o['type']}] **{o['name']}** ← `{o.get('source_file','')}:{o.get('source_line','')}`",
        )
    lines.append("")

    # C4
    lines += ["## C4 HISTORICAL — 历史版本不得冒充现行版", ""]
    lines.append("规则：同族存在更新版本时，历史版本必须有入向 EVOLVED_FROM 边或 context 版本语境标注。")
    lines.append("")
    if not historical_viol:
        lines.append("- ✅ 无违例。")
    else:
        lines += fmt_samples(
            historical_viol, n,
            lambda x: f"- **{x[0]['name']}**（族内更新版本 {'.'.join(map(str, x[1]))} 存在，无 EVOLVED_FROM/版本语境）"
                      f" ← `{x[0].get('source_file','')}:{x[0].get('source_line','')}`",
        )
    lines.append("")

    # C5
    lines += [f"## C5 MULTI-DEF — 多定义告警（>{MULTI_DEF_THRESHOLD} 个文件 DEFINES，仅报告）", ""]
    if not multi_def:
        lines.append("- 无。")
    else:
        for name, tid, files in multi_def:
            lines.append(f"- **{name}**（`{tid}`）：{len(files)} 个文件")
            for fid in files[:8]:
                lines.append(f"  - `{entities.get(fid, {}).get('name', fid)}`")
            if len(files) > 8:
                lines.append(f"  - ... 还有 {len(files) - 8} 个文件")
    lines.append("")

    # Backlog
    lines += ["## Backlog（info，不影响退出码）", ""]
    lines.append("### I1 端点类型与本体声明漂移")
    if not drift:
        lines.append("- 无。")
    else:
        by = Counter((p, s, t) for p, s, t, _ in drift)
        for (p, s, t), c in by.most_common():
            lines.append(f"- `aro:{p}`: {s} → {t}（{c} 条）")
    lines.append("")
    lines.append("### I2 同族重复/变体 Standard（待重抽取归并或 canonical-names.yaml 补登别名）")
    if not dups:
        lines.append("- 无。")
    else:
        for f, names in dups:
            lines.append(f"- 族 `{f}`: {' / '.join(names)}")
    lines.append("")
    lines.append("### 已知语义限制")
    lines.append("- `evolvedFrom` 本体声明为 Standard→Standard；Protocol 版本线（MCP/A2A）暂无谱系边，"
                 "MCP 2025-03-26/2025-06-18、A2A v1.1/2.0 等版本关系待本体扩展后补全。")
    lines.append("")

    # Appendix
    lines += ["## 附录：pyshacl 原始输出", "", "```text", shacl_text.strip(), "```", ""]

    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(lines), encoding="utf-8")

    print(f"实体 {len(entities)} / 关系 {len(relations)} / 登记名 {len(registry)}")
    for k, v in errors.items():
        print(f"  {k}: {v}")
    print(f"  C5 MULTI-DEF (warning): {len(multi_def)}")
    print(f"  I1 RANGE-DRIFT: {len(drift)} / I2 DUP-VARIANT: {len(dups)}")
    print(f"报告: {args.report}")
    print("结果:", "PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
