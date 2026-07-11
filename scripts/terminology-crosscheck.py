#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
术语双向交叉校验（terminology-crosscheck）

对两套术语库进行双向覆盖校验：
  - 集中术语表：struct/99-reference/glossary/glossary-master.md（中英双语词条）
  - 机器可读术语库：struct/99-reference/tools/terminology-db.yaml（英文标准定义）

校验内容：
  1. YAML 中的术语在 glossary 中缺失（按英文名匹配，允许别名映射表）
  2. glossary 词条在 YAML 中缺失对应英文术语
  3. 双侧都覆盖的术语：确认两侧定义文本均存在（不做语义比对）

输出：reports/terminology-crosscheck.md
退出码：恒为 0（报告型脚本，暂不作为硬门禁）

用法：
    python scripts/terminology-crosscheck.py
"""

import re
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    print("错误：需要 PyYAML（pip install pyyaml）", file=sys.stderr)
    sys.exit(0)  # 报告型脚本，不因缺依赖而失败

ROOT = Path(__file__).resolve().parent.parent
GLOSSARY = ROOT / "struct" / "99-reference" / "glossary" / "glossary-master.md"
YAML_DB = ROOT / "struct" / "99-reference" / "tools" / "terminology-db.yaml"
REPORT = ROOT / "reports" / "terminology-crosscheck.md"

# 两侧术语库的已知等价别名映射（双向生效）。
# 键值两侧可以是 YAML 术语名或 glossary 词条名，规范化（小写、去非字母数字）后比较。
ALIAS_EQUIVALENTS = [
    ("MCP", "Model Context Protocol"),
    ("Reusable Asset", "Asset"),
    ("Reuse", "Reusability"),
    ("Architecture Decision", "ADR"),
    ("Architecture Decision", "Architecture Rationale"),
    # TOGAF 中 Building Block 仅有 ABB/SBB 两种形态，glossary 以合并词条覆盖
    ("Building Block", "Architecture Building Block"),
    ("Building Block", "Solution Building Block"),
]


def normalize(name: str) -> str:
    """规范化术语名：小写 + 仅保留字母数字，用于宽松匹配。"""
    return re.sub(r"[^a-z0-9]", "", name.lower())


def split_english_names(heading: str):
    """从 glossary 词条标题中提取全部英文候选名。

    支持形式：
      Component (组件)                      -> ["Component"]
      EDA (Event-Driven Architecture, 事件驱动架构) -> ["EDA", "Event-Driven Architecture"]
      Architecture Decision / ADR (架构决策) -> ["Architecture Decision", "ADR"]
    """
    names = []
    m = re.match(r"^(.+?)\s*\(([^)]*)\)\s*$", heading)
    if m:
        head, paren = m.group(1), m.group(2)
    else:
        head, paren = heading, ""
    for part in re.split(r"[/,]", head):
        part = part.strip()
        if part and re.search(r"[A-Za-z]", part):
            names.append(part)
    for part in re.split(r"[,/]", paren):
        part = part.strip()
        # 括号内仅保留纯英文片段（排除中文译名）
        if part and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 \-+.]*", part):
            names.append(part)
    return names


def parse_glossary(path: Path):
    """解析 glossary-master.md，返回词条列表：
    [{heading, names(英文候选), has_definition(定义文本非空)}]
    """
    entries = []
    current = None
    for line in path.read_text(encoding="utf-8").splitlines():
        h2 = re.match(r"^##\s+(.+?)\s*$", line)
        if h2:
            section = h2.group(1)
            current = None  # 切换章节时收尾
            continue
        h3 = re.match(r"^###\s+(.+?)\s*$", line)
        if h3:
            heading = h3.group(1)
            # 词条标题须以英文字母/数字开头（排除附录中的中文小节，如"正向示例"）
            if re.match(r"^[A-Za-z0-9]", heading):
                current = {
                    "heading": heading,
                    "names": split_english_names(heading),
                    "has_definition": False,
                }
                entries.append(current)
            else:
                current = None
            continue
        if current is not None:
            m = re.match(r"^-\s*\*\*定义\*\*[:：]\s*(\S.*)$", line)
            if m:
                current["has_definition"] = True
    return entries


def parse_yaml_db(path: Path):
    """解析 terminology-db.yaml，返回术语列表：
    [{term, names(含英文别名), has_definition}]
    """
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    terms = []
    for term, info in (data.get("terms") or {}).items():
        names = [term]
        for alias in info.get("aliases") or []:
            # 仅保留英文别名用于跨库匹配
            if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 \-+.]*", str(alias).strip()):
                names.append(str(alias).strip())
        has_def = bool(info.get("definitions"))
        terms.append({"term": term, "names": names, "has_definition": has_def})
    return terms


def build_alias_graph():
    graph = {}
    for a, b in ALIAS_EQUIVALENTS:
        na, nb = normalize(a), normalize(b)
        graph.setdefault(na, set()).add(nb)
        graph.setdefault(nb, set()).add(na)
    return graph


def matches(names_a, names_b, alias_graph):
    """两组候选名是否存在匹配（含别名映射）。"""
    set_a = {normalize(n) for n in names_a}
    set_b = {normalize(n) for n in names_b}
    if set_a & set_b:
        return True
    expanded_a = set_a | {x for n in set_a for x in alias_graph.get(n, ())}
    return bool(expanded_a & set_b)


def main():
    if not GLOSSARY.exists() or not YAML_DB.exists():
        print(f"错误：找不到 {GLOSSARY} 或 {YAML_DB}", file=sys.stderr)
        sys.exit(0)

    glossary = parse_glossary(GLOSSARY)
    yaml_terms = parse_yaml_db(YAML_DB)
    alias_graph = build_alias_graph()

    covered = []          # 双侧已覆盖
    yaml_only = []        # YAML 有、glossary 缺失
    glossary_only = []    # glossary 有、YAML 缺失
    definition_issues = []  # 双侧覆盖但某侧定义文本缺失

    matched_glossary = set()
    for yt in yaml_terms:
        hit = None
        for i, ge in enumerate(glossary):
            if matches(yt["names"], ge["names"], alias_graph):
                hit = (i, ge)
                break
        if hit:
            i, ge = hit
            matched_glossary.add(i)
            covered.append((yt, ge))
            if not yt["has_definition"] or not ge["has_definition"]:
                definition_issues.append((yt, ge))
        else:
            yaml_only.append(yt)

    for i, ge in enumerate(glossary):
        if i not in matched_glossary:
            glossary_only.append(ge)

    # ---- 生成报告 ----
    lines = []
    lines.append("# 术语库双向交叉校验报告")
    lines.append("")
    lines.append(f"> 生成日期：{date.today().isoformat()}")
    lines.append(f"> 生成脚本：`scripts/terminology-crosscheck.py`（报告型，exit 0，暂不做硬门禁）")
    lines.append(f"> 数据源：`struct/99-reference/glossary/glossary-master.md`（{len(glossary)} 词条）、`struct/99-reference/tools/terminology-db.yaml`（{len(yaml_terms)} 术语）")
    lines.append("")
    lines.append("## 概要")
    lines.append("")
    lines.append("| 项目 | 数量 |")
    lines.append("|---|---|")
    lines.append(f"| 双侧已覆盖（定义文本均存在性确认） | {len(covered)} |")
    lines.append(f"| YAML 有、glossary 缺失 | {len(yaml_only)} |")
    lines.append(f"| glossary 有、YAML 缺失 | {len(glossary_only)} |")
    lines.append(f"| 双侧覆盖但定义文本缺失 | {len(definition_issues)} |")
    lines.append("")

    lines.append("## 1. 双侧已覆盖（仅确认两侧定义文本存在，不做语义比对）")
    lines.append("")
    if covered:
        lines.append("| YAML 术语 | glossary 词条 | YAML 定义 | glossary 定义 |")
        lines.append("|---|---|---|---|")
        for yt, ge in covered:
            yd = "✅" if yt["has_definition"] else "❌ 缺失"
            gd = "✅" if ge["has_definition"] else "❌ 缺失"
            lines.append(f"| {yt['term']} | {ge['heading']} | {yd} | {gd} |")
    else:
        lines.append("（无）")
    lines.append("")

    lines.append("## 2. YAML 中有、glossary 中缺失的术语")
    lines.append("")
    if yaml_only:
        for yt in yaml_only:
            srcs = "、".join((yt.get("names") or [])[:1])
            lines.append(f"- **{yt['term']}**")
    else:
        lines.append("（无）")
    lines.append("")

    lines.append("## 3. glossary 中有、YAML 中缺失对应英文术语的词条")
    lines.append("")
    if glossary_only:
        for ge in glossary_only:
            lines.append(f"- **{ge['heading']}**")
    else:
        lines.append("（无）")
    lines.append("")

    if definition_issues:
        lines.append("## 4. 双侧覆盖但定义文本缺失")
        lines.append("")
        for yt, ge in definition_issues:
            which = []
            if not yt["has_definition"]:
                which.append("YAML 缺定义")
            if not ge["has_definition"]:
                which.append("glossary 缺定义")
            lines.append(f"- **{yt['term']}** / {ge['heading']}：{'，'.join(which)}")
        lines.append("")

    lines.append("## 别名映射表")
    lines.append("")
    lines.append("以下已知等价对在匹配时视为同一术语（规范化后比较，双向生效）：")
    lines.append("")
    for a, b in ALIAS_EQUIVALENTS:
        lines.append(f"- `{a}` ↔ `{b}`")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("> 说明：本脚本仅做名称级覆盖校验与定义文本存在性确认，不做定义语义一致性比对；"
                 "缺失清单供人工补全参考，不影响 CI 门禁。")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"报告已生成：{REPORT}")
    print(f"  双侧已覆盖: {len(covered)}")
    print(f"  YAML 有、glossary 缺失: {len(yaml_only)}")
    print(f"  glossary 有、YAML 缺失: {len(glossary_only)}")
    print(f"  定义文本缺失: {len(definition_issues)}")
    sys.exit(0)


if __name__ == "__main__":
    main()
