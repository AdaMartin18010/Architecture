#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kg-relation-enricher.py
=======================

为知识图谱增量补充 ontology 已定义但抽取器此前未产出的语义关系：
  - evolvedFrom  (Standard -> Standard)：权威版本谱系（事实）
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
]

# 历史版本 Standard 实体补全（KG 中缺失但 EVOLVED_FROM 谱系需要的旧版本实体）
NEW_HISTORICAL_STANDARDS: Dict[str, str] = {
    "ArchiMate 3.2": "ArchiMate 3.2 Specification (2022), predecessor of ArchiMate 4.0",
    "ISO/IEC/IEEE 42010:2011": "ISO/IEC/IEEE 42010:2011, predecessor of 42010:2022",
    "ISO/IEC/IEEE 15288:2015": "ISO/IEC/IEEE 15288:2015, predecessor of 15288:2023",
    "NIST SSDF 1.1": "NIST SP 800-218 Rev.1 (SSDF 1.1, 2022), predecessor of SSDF 1.2 (IPD)",
    "ISO/IEC 30141:2018": "ISO/IEC 30141:2018 (IoT RA), predecessor of 30141:2024",
}


def load_entities() -> Tuple[Dict[str, dict], Dict[str, str]]:
    """返回 (id->entity, name(lower)->standard_id)。"""
    by_id: Dict[str, dict] = {}
    std_name_to_id: Dict[str, str] = {}
    with (KG_DIR / "kg-entities.jsonl").open(encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            o = json.loads(ln)
            by_id[o["id"]] = o
            if o.get("type") == "Standard":
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


def std_id(name: str) -> str:
    return "Standard:" + re.sub(r"[/ :.]", "_", name)


def ensure_historical_entities(by_id, std_name_to_id) -> List[dict]:
    """补全 EVOLVED_FROM 谱系所需的历史版本 Standard 实体（幂等）。返回新增实体列表。"""
    added: List[dict] = []
    for name, ctx in NEW_HISTORICAL_STANDARDS.items():
        if name.lower() in std_name_to_id:
            continue
        eid = std_id(name)
        ent = {
            "id": eid, "name": name, "type": "Standard",
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
        lines.append(f"{id_to_uri(e['id'])} a aro:Standard ;")
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

    evolved = build_evolved_from(by_id, std_name_to_id, seen)
    mentions = build_mentions(by_id, std_name_to_id, aliases_map, seen)
    related = build_related_to(by_id, seen)
    new_rels = evolved + mentions + related

    by_rel: Dict[str, int] = {}
    for r in new_rels:
        by_rel[r["relation"]] = by_rel.get(r["relation"], 0) + 1

    print("=== KG 语义关系增量补充（dry-run） ===" if not args.apply else "=== KG 语义关系增量补充（apply） ===")
    print(f"现有关系去重集合: {len(seen)} 条")
    print(f"新增历史版本实体: {len(new_entities)} 个")
    for e in new_entities:
        print(f"  + Standard: {e['name']}")
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
