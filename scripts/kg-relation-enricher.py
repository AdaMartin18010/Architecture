#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kg-relation-enricher.py
=======================

为知识图谱增量补充 ontology 已定义但抽取器此前未产出的语义关系：
  - evolvedFrom  (Standard/Protocol -> Standard/Protocol)：权威版本谱系（事实）
  - mentions     (File -> Standard/Term)：文件正文对权威标准/术语的引用
  - relatedTo    (Term -> Term)：glossary 词条"关系"段解析（可选）
  - implementedBy(Standard -> Tool)：标准 -> 实现/验证工具（可选，需 Tool 实体）

设计原则：
  - 增量、幂等：只追加 kg-relations.jsonl 中尚不存在的关系；
    现有 5 类关系（DEFINES/REFERENCES/BELONGS_TO/PROVIDES_POSITIVE/NEGATIVE_EXAMPLE）一字不动。
  - kg.ttl 不重写，仅在末尾追加新增三元组块，零回归风险。
  - 默认 --dry-run，仅打印统计与样例；--apply 才写文件。

用法：
    python scripts/kg-relation-enricher.py            # dry-run
    python scripts/kg-relation-enricher.py --apply    # 写入
"""

import argparse
import datetime
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KG_DIR = PROJECT_ROOT / "struct" / "99-reference" / "knowledge-graph"
STRUCT_DIR = PROJECT_ROOT / "struct"
CANONICAL_YAML = PROJECT_ROOT / "struct" / "99-reference" / "tools" / "canonical-names.yaml"
REPORT_FILE = PROJECT_ROOT / "reports" / "kg-extraction-report.md"

ENTITY_URI_PREFIX = "https://github.com/AdaMartin18010/Architecture/kg/entity/"

REL_TO_PREDICATE = {
    "EVOLVED_FROM": "aro:evolvedFrom",
    "MENTIONS": "aro:mentions",
    "RELATED_TO": "aro:relatedTo",
    "IMPLEMENTED_BY": "aro:implementedBy",
}

# 权威版本谱系：new 版本 evolvedFrom old 版本（事实，仅当两端实体均存在时生成）
# 端点类型可为 Standard 或 Protocol（本体已放宽，C6 EVOLVED-TYPE 约束）。
EVOLVED_FROM_PAIRS: List[Tuple[str, str]] = [
    ("ISO/IEC/IEEE 12207:2026", "ISO/IEC/IEEE 12207:2017"),
    ("ISO/IEC 25010:2023", "ISO/IEC 25010:2011"),
    ("ISO/IEC 25040:2024", "ISO/IEC 25040:2005"),
    ("SLSA 1.1", "SLSA 1.0"),
    ("SLSA 1.2", "SLSA 1.1"),
    ("SLSA 2.0", "SLSA 1.2"),
    ("SysML v2", "SysML v1"),
    ("DMN 1.6", "DMN 1.5"),
    ("ArchiMate 4.0", "ArchiMate 3.2"),
    ("ISO/IEC/IEEE 42010:2022", "ISO/IEC/IEEE 42010:2011"),
    ("ISO/IEC/IEEE 15288:2023", "ISO/IEC/IEEE 15288:2015"),
    ("NIST SSDF 1.2", "NIST SSDF 1.1"),
    ("ISO/IEC 30141:2024", "ISO/IEC 30141:2018"),
    ("ISO/IEC 5230:2024", "ISO/IEC 5230:2021"),
    # 协议版本线（来源：struct/12-ai-native-reuse/ 权威文档版本表）
    ("MCP 2025-03-26", "MCP 2024-11-05"),
    ("MCP 2025-06-18", "MCP 2025-03-26"),
    ("MCP 2025-11-25", "MCP 2025-06-18"),
    ("A2A v1.0.0", "A2A v0.3.0"),
    ("A2A v1.0.1", "A2A v1.0.0"),
]

# 历史版本 Standard 实体补全（KG 中缺失但 EVOLVED_FROM 谱系需要的旧版本实体）
NEW_HISTORICAL_STANDARDS: Dict[str, str] = {
    "ArchiMate 3.2": "ArchiMate 3.2 Specification (2022), predecessor of ArchiMate 4.0",
    "ISO/IEC/IEEE 42010:2011": "ISO/IEC/IEEE 42010:2011, predecessor of 42010:2022",
    "ISO/IEC/IEEE 15288:2015": "ISO/IEC/IEEE 15288:2015, predecessor of 15288:2023",
    "NIST SSDF 1.1": "NIST SP 800-218 Rev.1 (SSDF 1.1, 2022), predecessor of SSDF 1.2 (IPD)",
    "ISO/IEC 30141:2018": "ISO/IEC 30141:2018 (IoT RA), predecessor of 30141:2024",
}

# 历史版本 Protocol 实体补全（协议版本谱系旧版端点，来源见 context 中权威文档）
NEW_HISTORICAL_PROTOCOLS: Dict[str, str] = {
    "MCP 2024-11-05": "MCP 2024-11-05 初始发布（JSON-RPC 2.0、HTTP+SSE），predecessor of MCP 2025-03-26；"
                      "来源 struct/12-ai-native-reuse/01-mcp-protocol/mcp-2025-11-25-authoritative.md 版本表",
    "A2A v0.3.0": "A2A v0.3.0（2025-07-30：流式传输、Agent Card 能力协商），predecessor of A2A v1.0.0 GA；"
                  "来源 struct/12-ai-native-reuse/02-a2a-protocol/a2a-v1-deep-dive.md 版本时间线",
}


def load_entities() -> Tuple[Dict[str, dict], Dict[str, str]]:
    """返回 (id->entity, name(lower)->entity_id)。

    name 索引覆盖 Standard 与 Protocol（EVOLVED_FROM 端点类型）。
    """
    by_id: Dict[str, dict] = {}
    std_name_to_id: Dict[str, str] = {}
    with (KG_DIR / "kg-entities.jsonl").open(encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            o = json.loads(ln)
            by_id[o["id"]] = o
            if o.get("type") in ("Standard", "Protocol"):
                std_name_to_id[o["name"].lower()] = o["id"]
    return by_id, std_name_to_id


def load_existing_relations() -> Set[Tuple[str, str, str]]:
    seen: Set[Tuple[str, str, str]] = set()
    with (KG_DIR / "kg-relations.jsonl").open(encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            o = json.loads(ln)
            seen.add((o["source_id"], o["relation"], o["target_id"]))
    return seen


def load_standard_aliases() -> Dict[str, List[str]]:
    """canonical(lower) -> [aliases...]（仅含长度>=4 的别名，降低误匹配）。"""
    import yaml
    data = yaml.safe_load(CANONICAL_YAML.read_text(encoding="utf-8")) or {}
    out: Dict[str, List[str]] = {}
    for entry in data.get("standards", []) or []:
        canon = entry.get("canonical", "")
        aliases = []
        for a in entry.get("aliases", []) or []:
            if isinstance(a, str) and len(a) >= 4:
                aliases.append(a)
        out[canon.lower()] = aliases
    return out


def std_id(name: str, etype: str = "Standard") -> str:
    return etype + ":" + re.sub(r"[/ :.]", "_", name)


def ensure_historical_entities(by_id, std_name_to_id) -> List[dict]:
    """补全 EVOLVED_FROM 谱系所需的历史版本 Standard/Protocol 实体（幂等）。返回新增实体列表。"""
    added: List[dict] = []
    for etype, table in (("Standard", NEW_HISTORICAL_STANDARDS), ("Protocol", NEW_HISTORICAL_PROTOCOLS)):
        for name, ctx in table.items():
            if name.lower() in std_name_to_id:
                continue
            eid = std_id(name, etype)
            ent = {
                "id": eid, "name": name, "type": etype,
                "source_file": "struct/99-reference/tools/canonical-names.yaml",
                "source_line": 1, "context": ctx,
            }
            by_id[eid] = ent
            std_name_to_id[name.lower()] = eid
            added.append(ent)
    return added


def append_entities_jsonl(entities: List[dict]) -> None:
    if not entities:
        return
    with (KG_DIR / "kg-entities.jsonl").open("a", encoding="utf-8") as f:
        for e in entities:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


def append_entities_ttl(entities: List[dict]) -> int:
    if not entities:
        return 0
    lines = ["", "# === 历史版本 Standard 实体补全（kg-relation-enricher.py） ===",
             f"# 生成时间: {datetime.datetime.now().isoformat(timespec='seconds')}", ""]
    for e in entities:
        lines.append(f"{id_to_uri(e['id'])} a aro:{e['type']} ;")
        lines.append(f'    rdfs:label "{e["name"]}" ;')
        lines.append(f'    ar:sourceFile "{e["source_file"]}" ;')
        lines.append(f"    ar:sourceLine {e['source_line']} .")
        lines.append("")
    with (KG_DIR / "kg.ttl").open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return len(entities)


def build_evolved_from(by_id, std_name_to_id, seen) -> List[dict]:
    rels = []
    name_to_id = std_name_to_id
    for new_name, old_name in EVOLVED_FROM_PAIRS:
        sid = name_to_id.get(new_name.lower())
        tid = name_to_id.get(old_name.lower())
        if not sid or not tid:
            continue
        key = (sid, "EVOLVED_FROM", tid)
        if key in seen:
            continue
        rels.append({
            "source_id": sid, "relation": "EVOLVED_FROM", "target_id": tid,
            "source_file": "struct/99-reference/tools/canonical-names.yaml", "source_line": 1, "weight": 1.0,
        })
        seen.add(key)
    return rels


def _match_in_text(text: str, name: str) -> int:
    """返回 name 在 text 中首次出现的 1-based 行号，未命中返回 0。"""
    if not name:
        return 0
    # 含单词字符边界的用 \b，否则直接子串（含 / : 空格 的标准名）
    if re.match(r"^[A-Za-z0-9 .+-]+$", name) and " " not in name:
        pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(name) + r"(?![A-Za-z0-9])")
    else:
        pat = re.compile(re.escape(name))
    for i, line in enumerate(text.splitlines(), start=1):
        if pat.search(line):
            return i
    return 0


def build_mentions(by_id, std_name_to_id, aliases_map, seen) -> List[dict]:
    files = [
        o for o in by_id.values()
        if o.get("type") == "File" and not o.get("name", "").startswith(("./", "../"))
    ]
    standards = [o for o in by_id.values() if o.get("type") == "Standard"]
    # 预读文件正文
    file_text: Dict[str, str] = {}
    for fo in files:
        rel = fo.get("source_file", "")
        p = PROJECT_ROOT / rel
        if p.exists():
            try:
                file_text[fo["id"]] = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                file_text[fo["id"]] = ""
        else:
            file_text[fo["id"]] = ""

    rels = []
    for so in standards:
        names: Set[str] = {so["name"]}
        names.update(aliases_map.get(so["name"].lower(), []))
        # 过滤过短/易误配名称
        names = {n for n in names if len(n) >= 4}
        for fo in files:
            text = file_text.get(fo["id"], "")
            if not text:
                continue
            key = (fo["id"], "MENTIONS", so["id"])
            if key in seen:
                continue
            hit_line = 0
            for nm in names:
                hit_line = _match_in_text(text, nm)
                if hit_line:
                    break
            if hit_line:
                rels.append({
                    "source_id": fo["id"], "relation": "MENTIONS", "target_id": so["id"],
                    "source_file": fo.get("source_file", ""),
                    "source_line": hit_line, "weight": 1.0,
                })
                seen.add(key)
    return rels


GLOSSARY_FILE = STRUCT_DIR / "99-reference" / "glossary" / "glossary-master.md"

# 关系段前缀标签（抽取关联项时去除）
_REL_LABELS = ("方法", "标准", "上位", "下位", "实现", "对齐", "应用", "参见", "工具",
               "框架", "协议", "类似", "对比", "互补", "替代", "依赖", "组成")


def parse_glossary_relations(text: str) -> Dict[str, List[str]]:
    """解析 glossary-master.md：{词条英文主名 lower: [关联项原文...]}。"""
    out: Dict[str, List[str]] = {}
    # 按 ### 词条分块
    blocks = re.split(r"(?m)^### ", text)
    for blk in blocks[1:]:
        head_end = blk.find("\n")
        if head_end < 0:
            continue
        head = blk[:head_end].strip()
        en = re.split(r"\s*\(", head)[0].strip().lower()
        if not en:
            continue
        body = blk[head_end:]
        # 提取 “关系” 段：- **关系**: 到下一个 - ** 或 --- 或 ### 之间
        m = re.search(r"-\s*\*\*关系\*\*\s*[:：](.*?)(?=\n-\s*\*\*|\n---|\Z)", body, re.S)
        if not m:
            continue
        seg = m.group(1)
        items: List[str] = []
        for line in seg.splitlines():
            line = line.strip().lstrip("-").strip()
            if not line:
                continue
            # 去前缀标签
            for lab in _REL_LABELS:
                line = re.sub(rf"^{re.escape(lab)}\s*[:：]", "", line).strip()
            # 分割并列项
            for tok in re.split(r"[、，,;；/]", line):
                tok = tok.strip().strip("（）()《》\"'`").strip()
                if len(tok) >= 2:
                    items.append(tok)
        if items:
            out[en] = items
    return out


def build_related_to(by_id, seen) -> List[dict]:
    if not GLOSSARY_FILE.exists():
        return []
    relmap = parse_glossary_relations(GLOSSARY_FILE.read_text(encoding="utf-8", errors="ignore"))
    # 名称索引：Term/Standard/Protocol/Organization
    name_idx: Dict[str, str] = {}
    for o in by_id.values():
        if o.get("type") in ("Term", "Standard", "Protocol", "Organization"):
            name_idx.setdefault(o["name"].lower(), o["id"])
    rels = []
    for en, items in relmap.items():
        src_id = name_idx.get(en)
        # 源必须是 Term
        if not src_id or by_id[src_id].get("type") != "Term":
            continue
        for tok in items:
            tl = tok.lower()
            tgt_id = name_idx.get(tl)
            if not tgt_id:
                # 退而求其次：实体名被关联项包含（实体名>=4）或关联项包含实体名(>=4)
                for nm, eid in name_idx.items():
                    if len(nm) >= 4 and (nm in tl or tl in nm):
                        tgt_id = eid
                        break
            if not tgt_id or tgt_id == src_id:
                continue
            key = (src_id, "RELATED_TO", tgt_id)
            if key in seen:
                continue
            rels.append({
                "source_id": src_id, "relation": "RELATED_TO", "target_id": tgt_id,
                "source_file": "struct/99-reference/glossary/glossary-master.md",
                "source_line": 1, "weight": 1.0,
            })
            seen.add(key)
    return rels


# 形式化规约/策略工件 → 验证/执行工具映射（IMPLEMENTED_BY）
EXT_TOOL: Dict[str, str] = {
    ".tla": "TLC", ".als": "Alloy Analyzer", ".v": "Rocq",
    ".thy": "Isabelle/HOL", ".rego": "OPA",
}
RS_PREFIX_TOOL: Dict[str, str] = {
    "kani": "Kani", "miri": "Miri", "verus": "Verus", "prusti": "Prusti",
}
MD_DIR_TOOL: Dict[str, str] = {
    "05-spark-ada": "SPARK Pro", "06-b-method": "Atelier B",
}
NEW_TOOLS: Dict[str, str] = {
    "TLC": "TLA+ model checker",
    "Alloy Analyzer": "Alloy model finder",
    "Rocq": "Rocq (Coq) proof assistant",
    "Isabelle/HOL": "Isabelle/HOL theorem prover",
    "Kani": "Kani Rust Verifier",
    "Miri": "Miri UB detector for Rust",
    "Verus": "Verus verified Rust",
    "Prusti": "Prusti verifier for Rust",
    "OPA": "Open Policy Agent (Rego)",
    "SPARK Pro": "SPARK Pro (Ada) verification toolset",
    "Atelier B": "Atelier B / Rodin (B / Event-B)",
}


def tool_id(name: str) -> str:
    return "Tool:" + re.sub(r"[/ :.]", "_", name)


def spec_id(relpath: str) -> str:
    return "Specification:" + re.sub(r"[/\\.]", "_", relpath)


def ensure_tool_entities(by_id) -> List[dict]:
    added: List[dict] = []
    existing = {o["name"].lower() for o in by_id.values() if o.get("type") == "Tool"}
    for name, ctx in NEW_TOOLS.items():
        if name.lower() in existing:
            continue
        eid = tool_id(name)
        ent = {"id": eid, "name": name, "type": "Tool",
               "source_file": "struct/99-reference/tools/formal-verification-env/README.md",
               "source_line": 1, "context": ctx}
        by_id[eid] = ent
        added.append(ent)
        existing.add(name.lower())
    return added


def build_implemented_by(by_id, seen) -> Tuple[List[dict], List[dict]]:
    rels: List[dict] = []
    spec_entities: List[dict] = []
    artifact_exts = set(EXT_TOOL) | {".rs"}
    for path in sorted(STRUCT_DIR.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in artifact_exts:
            continue
        rel = path.relative_to(PROJECT_ROOT).as_posix()
        ext = path.suffix.lower()
        if ext == ".rs":
            stem = path.stem.lower()
            tool = next((t for p, t in RS_PREFIX_TOOL.items() if stem.startswith(p)), None)
        else:
            tool = EXT_TOOL.get(ext)
        if not tool:
            continue
        tid = tool_id(tool)
        if tid not in by_id:
            continue
        sid = spec_id(rel)
        if sid not in by_id:
            ent = {"id": sid, "name": rel, "type": "Specification",
                   "source_file": rel, "source_line": 1, "context": f"formal artifact implementedBy {tool}"}
            by_id[sid] = ent
            spec_entities.append(ent)
        key = (sid, "IMPLEMENTED_BY", tid)
        if key in seen:
            continue
        rels.append({"source_id": sid, "relation": "IMPLEMENTED_BY", "target_id": tid,
                     "source_file": rel, "source_line": 1, "weight": 1.0})
        seen.add(key)
    # md 文档级规约（SPARK / B Method 内联规约）→ 复用 File 实体
    for sub, tool in MD_DIR_TOOL.items():
        tid = tool_id(tool)
        if tid not in by_id:
            continue
        for fo in by_id.values():
            if fo.get("type") != "File" or fo.get("name", "").startswith(("./", "../")):
                continue
            sf = fo.get("source_file", "")
            if f"/07-formal-verification/{sub}/" not in ("/" + sf):
                continue
            key = (fo["id"], "IMPLEMENTED_BY", tid)
            if key in seen:
                continue
            rels.append({"source_id": fo["id"], "relation": "IMPLEMENTED_BY", "target_id": tid,
                         "source_file": sf, "source_line": 1, "weight": 1.0})
            seen.add(key)
    return rels, spec_entities


def id_to_uri(eid: str) -> str:
    return f"<{ENTITY_URI_PREFIX}{eid.replace(':', '_', 1)}>"


def append_ttl(relations: List[dict]) -> int:
    """在 kg.ttl 末尾追加新增三元组块。返回追加的语句数。"""
    if not relations:
        return 0
    lines = ["", "", "# === 语义关系增量补充（kg-relation-enricher.py） ===",
             f"# 生成时间: {datetime.datetime.now().isoformat(timespec='seconds')}", ""]
    by_src: Dict[str, Dict[str, List[str]]] = {}
    for r in relations:
        by_src.setdefault(r["source_id"], {}).setdefault(r["relation"], []).append(r["target_id"])
    n = 0
    for sid, relmap in by_src.items():
        for rel, tids in relmap.items():
            pred = REL_TO_PREDICATE[rel]
            objs = ",\n        ".join(id_to_uri(t) for t in tids)
            lines.append(f"{id_to_uri(sid)} {pred} {objs} .")
            n += 1
    with (KG_DIR / "kg.ttl").open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return n


def append_jsonl(relations: List[dict]) -> None:
    with (KG_DIR / "kg-relations.jsonl").open("a", encoding="utf-8") as f:
        for r in relations:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description="KG 语义关系增量补充（dry-run 默认）")
    ap.add_argument("--apply", action="store_true", help="实际写入 jsonl/ttl（默认仅 dry-run）")
    args = ap.parse_args()

    by_id, std_name_to_id = load_entities()
    seen = load_existing_relations()
    aliases_map = load_standard_aliases()

    new_entities = ensure_historical_entities(by_id, std_name_to_id)
    new_entities += ensure_tool_entities(by_id)

    evolved = build_evolved_from(by_id, std_name_to_id, seen)
    mentions = build_mentions(by_id, std_name_to_id, aliases_map, seen)
    related = build_related_to(by_id, seen)
    impl_rels, spec_entities = build_implemented_by(by_id, seen)
    new_entities += spec_entities
    new_rels = evolved + mentions + related + impl_rels

    by_rel: Dict[str, int] = {}
    for r in new_rels:
        by_rel[r["relation"]] = by_rel.get(r["relation"], 0) + 1

    print("=== KG 语义关系增量补充（dry-run） ===" if not args.apply else "=== KG 语义关系增量补充（apply） ===")
    print(f"现有关系去重集合: {len(seen)} 条")
    print(f"新增实体: {len(new_entities)} 个")
    _et: Dict[str, int] = {}
    for e in new_entities:
        _et[e["type"]] = _et.get(e["type"], 0) + 1
    for t, c in sorted(_et.items()):
        print(f"  {t}: +{c}")
    for e in new_entities[:12]:
        print(f"  + [{e['type']}] {e['name']}")
    print(f"新增关系总计: {len(new_rels)} 条")
    for rel, c in sorted(by_rel.items()):
        print(f"  {rel}: +{c}")
    print("\n样例（每类最多 3 条）：")
    shown: Dict[str, int] = {}
    for r in new_rels:
        if shown.get(r["relation"], 0) >= 3:
            continue
        shown[r["relation"]] = shown.get(r["relation"], 0) + 1
        s = by_id[r["source_id"]]["name"]
        t = by_id[r["target_id"]]["name"]
        print(f"  [{r['relation']}] {s}  ->  {t}  ({r['source_file']}:{r['source_line']})")

    if args.apply:
        append_entities_jsonl(new_entities)
        ne = append_entities_ttl(new_entities)
        append_jsonl(new_rels)
        n = append_ttl(new_rels)
        print(f"\n已追加 kg-entities.jsonl: +{len(new_entities)} 实体")
        print(f"已追加 kg-relations.jsonl: +{len(new_rels)} 行")
        print(f"已追加 kg.ttl: +{ne} 实体声明 + {n} 条谓词语句")
        print("提示：运行 `python scripts/health-check.py` 与 `python scripts/knowledge-cli.py stats` 复核。")
    else:
        print("\n（dry-run：未写入。加 --apply 落盘。）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
