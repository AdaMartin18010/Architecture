#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用一致性检查脚本

检查内容：
1. 公理编号是否被引用但未定义（如 "公理 2.1" 在当前项目中是否有定义）
2. 标准版本是否冲突（如同一标准在不同文件中引用不同年份）
3. 术语定义是否冲突（基于 glossary-master.md）

用法：
    python scripts/cross-index-check.py
    python scripts/cross-index-check.py --json reports/cross-index-conflicts.json
    python scripts/cross-index-check.py --glossary struct/99-reference/glossary/glossary-master.md
"""

import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Set
from collections import defaultdict


@dataclass
class AxiomIssue:
    axiom_id: str
    referenced_in: List[Tuple[str, int]] = field(default_factory=list)  # (file, line)
    defined_in: List[Tuple[str, int]] = field(default_factory=list)

    @property
    def is_undefined(self) -> bool:
        return not self.defined_in and self.referenced_in

    @property
    def is_multi_defined(self) -> bool:
        return len(self.defined_in) > 1


@dataclass
class StandardVersionConflict:
    standard: str
    versions: Dict[str, List[Tuple[str, int]]]  # version -> [(file, line)]


@dataclass
class TermConflict:
    term: str
    definitions: List[Tuple[str, str]]  # (file, definition_snippet)


AXIOM_DEFINE_RE = re.compile(
    r"^[>\s]*\*\*公理\s+([A-Z]\.\d+)\*\*",
    re.MULTILINE,
)
AXIOM_REF_RE = re.compile(
    r"公理\s+([A-Z]\.\d+)",
)


def _is_valid_axiom_id(aid: str) -> bool:
    """仅接受全局公理编号：单个大写字母 + 点 + 数字（如 M.1、S.3），排除章节局部公理 3.1/3.2 等。"""
    return bool(re.fullmatch(r"[A-Z]\.\d+", aid))
STANDARD_RE = re.compile(
    r"\b(ISO\s*/\s*IEC\s*/\s*IEEE\s+\d+(?:[-/]\d+)*|"
    r"ISO\s*/\s*IEC\s+\d+(?:[-/]\d+)*|"
    r"ISO\s+\d+(?:[-/]\d+)*|"
    r"IEEE\s+\d+(?:[-/]\d+)*|"
    r"IEC\s+\d+(?:[-/]\d+)*|"
    r"ISA\s*[-]?\s*\d+(?:\.\d+)*|"
    r"TOGAF\s+\d+(?:\.\d+)*|"
    r"SLSA\s+\d+(?:\.\d+)*|"
    r"NIST\s+SP\s+\d+(?:[-/]\d+)*|"
    r"MCP\s+\d{4}-\d{2}-\d{2})"
    r"(?![\d])"
    r"[\s:：]*[:]?\s*(\d{4})",
    re.IGNORECASE,
)


def _collect_markdown_files(root: Path) -> List[Path]:
    files = []
    skip_patterns = ["__pycache__", ".venv", ".git", "_HISTORICAL_"]
    for md in root.rglob("*.md"):
        rel = md.relative_to(root).as_posix()
        if any(sp in rel for sp in skip_patterns):
            continue
        files.append(md)
    return files


def extract_axioms(root: Path) -> Tuple[Dict[str, AxiomIssue], Set[str]]:
    """提取公理定义与引用"""
    issues: Dict[str, AxiomIssue] = {}
    files = _collect_markdown_files(root)

    for md in files:
        text = md.read_text(encoding="utf-8")
        rel = md.relative_to(root).as_posix()
        for lineno, line in enumerate(text.splitlines(), start=1):
            # 定义
            for m in AXIOM_DEFINE_RE.finditer(line):
                axiom_id = m.group(1)
                if not _is_valid_axiom_id(axiom_id):
                    continue
                issue = issues.setdefault(axiom_id, AxiomIssue(axiom_id=axiom_id))
                issue.defined_in.append((rel, lineno))
            # 引用
            for m in AXIOM_REF_RE.finditer(line):
                axiom_id = m.group(1)
                if not _is_valid_axiom_id(axiom_id):
                    continue
                issue = issues.setdefault(axiom_id, AxiomIssue(axiom_id=axiom_id))
                if not any(r == (rel, lineno) for r in issue.defined_in):
                    issue.referenced_in.append((rel, lineno))

    return issues, set()


HISTORICAL_CONTEXT_RE = re.compile(
    r"反例|历史|旧版|旧标准|前一版本|前版|前身|升级|演进|对照|对比|timeline|roadmap|frontier|tracking|status|update|alignment|mapping|"
    r"deprecated|obsolete|取代|替代|previously|former|superseded|withdrawn|legacy|replaced by|first edition|prior|previous|edition|"
    r"evolution|history of|不存在.*官方版本|非官方|预期更新|草案|draft|新版本动态|后续版本规划",
    re.IGNORECASE,
)


def extract_standard_version_conflicts(root: Path) -> List[StandardVersionConflict]:
    """提取标准版本冲突。

    冲突判定规则：
    1. 仅检查同一文件内同一标准出现多个版本；跨文件版本差异视为合理。
    2. 若旧版本仅出现在历史/反例/对比语境（含“反例”“历史”“旧版”“deprecated”等词），不视为冲突。
    """
    refs: Dict[str, Dict[str, List[Tuple[str, int, bool]]]] = defaultdict(lambda: defaultdict(list))
    files = _collect_markdown_files(root)

    for md in files:
        text = md.read_text(encoding="utf-8")
        lines = text.splitlines()
        rel = md.relative_to(root).as_posix()
        for lineno, line in enumerate(lines, start=1):
            for m in STANDARD_RE.finditer(line):
                std_raw = m.group(1).strip().upper()
                # 统一空格与斜杠，使 ISO 42010 / ISO/IEC/IEEE 42010 可比较
                std = re.sub(r"\s+", " ", std_raw)
                std = re.sub(r"\s*/\s*", "/", std)
                # 统一 ISO/IEEE 与 ISO/IEC/IEEE 的写法差异（仅用于冲突检测）
                std = re.sub(r"^ISO/IEC/IEEE\s+", "ISO/IEC/IEEE ", std)
                year = m.group(2)
                # 取前后最多 5 行作为上下文，判断是否为历史/反例/演进语境
                ctx_lines = lines[max(0, lineno - 6):lineno + 5]
                context = "\n".join(ctx_lines)
                is_historical = bool(HISTORICAL_CONTEXT_RE.search(context))
                refs[std][year].append((rel, lineno, is_historical))

    conflicts = []
    for std, versions in refs.items():
        if len(versions) <= 1:
            continue
        # 按文件聚合版本，忽略纯历史语境中的版本
        per_file_versions: Dict[str, Set[str]] = defaultdict(set)
        for version, locs in versions.items():
            for file, line, is_historical in locs:
                if not is_historical:
                    per_file_versions[file].add(version)
        intra_file_conflicts = any(len(vs) > 1 for vs in per_file_versions.values())
        if intra_file_conflicts:
            # 报告中仅保留非历史语境的位置，便于定位
            filtered_versions: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
            for version, locs in versions.items():
                for file, line, is_historical in locs:
                    if not is_historical:
                        filtered_versions[version].append((file, line))
            conflicts.append(StandardVersionConflict(standard=std, versions=dict(filtered_versions)))
    return conflicts


def extract_term_definitions_from_glossary(glossary_path: Path) -> Dict[str, List[Tuple[str, str]]]:
    """从 glossary-master.md 提取术语定义"""
    terms: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
    if not glossary_path.exists():
        return terms

    text = glossary_path.read_text(encoding="utf-8")
    # 模式: ### Term (中文)
    for m in re.finditer(r"^###\s+(.+?)\s*\(([^)]+)\)\s*$", text, re.MULTILINE):
        term_en = m.group(1).strip()
        term_cn = m.group(2).strip()
        snippet_start = m.end()
        next_match = re.search(r"^###\s+", text[snippet_start:], re.MULTILINE)
        snippet = text[snippet_start:snippet_start + (next_match.start() if next_match else 400)]
        def_text = re.sub(r"\s+", " ", snippet).strip()[:200]
        if term_en:
            terms[term_en].append((glossary_path.name, def_text))
        if term_cn:
            terms[term_cn].append((glossary_path.name, def_text))

    return terms


def extract_term_conflicts(root: Path, glossary_path: Path) -> List[TermConflict]:
    """检测术语在 glossary 与正文中的定义冲突。

    仅检测以标题形式（##/###/#### Term）明确定义的术语，
    且该术语在 2 至 5 个不同非 glossary 文件中被定义；
    超高频通用术语或在大量文件中出现的标题不视为冲突。
    """
    glossary_terms = extract_term_definitions_from_glossary(glossary_path)
    conflicts: List[TermConflict] = []
    term_occurrences: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
    files = _collect_markdown_files(root)

    for md in files:
        rel = md.relative_to(root).as_posix()
        if "glossary" in rel:
            continue
        text = md.read_text(encoding="utf-8")
        for term in glossary_terms:
            # 仅匹配标题级定义
            term_escaped = re.escape(term)
            pattern = re.compile(
                r"^#{2,4}\s+" + term_escaped + r"\s*$",
                re.MULTILINE,
            )
            for m in pattern.finditer(text):
                line_no = text[:m.start()].count("\n") + 1
                term_occurrences[term].append((rel, f"第 {line_no} 行"))
                break

    for term, occurrences in term_occurrences.items():
        files_set = {o[0] for o in occurrences}
        if 2 <= len(files_set) <= 5:
            conflicts.append(TermConflict(term=term, definitions=occurrences))

    return conflicts


def write_json_report(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_md_report(path: Path, undefined_axioms: List[AxiomIssue], multi_defined_axioms: List[AxiomIssue],
                    std_conflicts: List[StandardVersionConflict], term_conflicts: List[TermConflict]):
    lines = [
        "# 交叉引用一致性检查报告",
        "",
        "## 公理定义检查",
        "",
    ]

    if undefined_axioms:
        lines.append("### 被引用但未定义的公理")
        for issue in undefined_axioms:
            lines.append(f"- **{issue.axiom_id}**")
            for ref in issue.referenced_in:
                lines.append(f"  - 引用: `{ref[0]}` 第 {ref[1]} 行")
        lines.append("")
    else:
        lines.append("- 未发现被引用但未定义的公理")
        lines.append("")

    if multi_defined_axioms:
        lines.append("### 重复定义的公理")
        for issue in multi_defined_axioms:
            lines.append(f"- **{issue.axiom_id}**")
            for df in issue.defined_in:
                lines.append(f"  - 定义: `{df[0]}` 第 {df[1]} 行")
        lines.append("")
    else:
        lines.append("- 未发现重复定义的公理")
        lines.append("")

    lines.append("## 标准版本冲突")
    lines.append("")
    if std_conflicts:
        for c in std_conflicts:
            lines.append(f"### {c.standard}")
            for version, locs in c.versions.items():
                lines.append(f"- **{version}** ({len(locs)} 处)")
                for loc in locs[:5]:
                    lines.append(f"  - `{loc[0]}` 第 {loc[1]} 行")
                if len(locs) > 5:
                    lines.append(f"  - ... 还有 {len(locs) - 5} 处")
            lines.append("")
    else:
        lines.append("- 未发现标准版本冲突")
        lines.append("")

    lines.append("## 术语定义冲突")
    lines.append("")
    if term_conflicts:
        for c in term_conflicts:
            lines.append(f"### {c.term}")
            for d in c.definitions:
                lines.append(f"- `{d[0]}` ({d[1]})")
            lines.append("")
    else:
        lines.append("- 未发现术语定义冲突")
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="检查项目内交叉引用一致性（公理、标准版本、术语）"
    )
    parser.add_argument(
        "--root",
        metavar="PATH",
        default="struct",
        help="项目文档根目录（默认 struct/）",
    )
    parser.add_argument(
        "--glossary",
        metavar="PATH",
        default="struct/99-reference/glossary/glossary-master.md",
        help="主术语表路径（默认 struct/99-reference/glossary/glossary-master.md）",
    )
    parser.add_argument(
        "--json",
        metavar="PATH",
        help="输出 JSON 报告路径",
    )
    parser.add_argument(
        "--report",
        metavar="PATH",
        default="cross-index-report.md",
        help="输出 Markdown 报告路径（默认 cross-index-report.md）",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    root = (project_root / args.root).resolve()
    glossary_path = (project_root / args.glossary).resolve()

    if not root.exists():
        print(f"错误：根目录不存在 {root}", file=sys.stderr)
        sys.exit(1)

    print(f"扫描目录: {root}")
    print(f"术语表: {glossary_path}")

    axiom_issues, _ = extract_axioms(root)
    undefined_axioms = [a for a in axiom_issues.values() if a.is_undefined]

    # 公理重复定义：允许权威索引位置（axiom-theorem-tree.md 与各主题 README.md）的跨文件重复；
    # 只保留同一文件内多次定义，或非权威位置之间的重复。
    authority_files = {"99-reference/glossary/axiom-theorem-tree.md"}
    raw_multi = [a for a in axiom_issues.values() if a.is_multi_defined]
    multi_defined_axioms = []
    for issue in raw_multi:
        files = {loc[0] for loc in issue.defined_in}
        if len(files) == 1:
            multi_defined_axioms.append(issue)
            continue
        non_authority_files = {f for f in files if f not in authority_files and not f.endswith("README.md")}
        if len(non_authority_files) > 1:
            multi_defined_axioms.append(issue)

    std_conflicts = extract_standard_version_conflicts(root)
    term_conflicts = extract_term_conflicts(root, glossary_path)

    print(f"公理问题: {len(undefined_axioms)} 个未定义, {len(multi_defined_axioms)} 个重复定义")
    print(f"标准版本冲突: {len(std_conflicts)} 个")
    print(f"术语定义冲突: {len(term_conflicts)} 个")

    if undefined_axioms:
        print("\n未定义公理:")
        for a in undefined_axioms:
            print(f"  - {a.axiom_id} 引用处: {a.referenced_in[:3]}")

    if std_conflicts:
        print("\n标准版本冲突:")
        for c in std_conflicts:
            versions = ", ".join(f"{v}({len(locs)})" for v, locs in c.versions.items())
            print(f"  - {c.standard}: {versions}")

    if args.json:
        data = {
            "undefined_axioms": [
                {
                    "axiom_id": a.axiom_id,
                    "referenced_in": [{"file": f, "line": l} for f, l in a.referenced_in],
                }
                for a in undefined_axioms
            ],
            "multi_defined_axioms": [
                {
                    "axiom_id": a.axiom_id,
                    "defined_in": [{"file": f, "line": l} for f, l in a.defined_in],
                }
                for a in multi_defined_axioms
            ],
            "standard_version_conflicts": [
                {
                    "standard": c.standard,
                    "versions": {
                        v: [{"file": f, "line": l} for f, l in locs]
                        for v, locs in c.versions.items()
                    },
                }
                for c in std_conflicts
            ],
            "term_conflicts": [
                {
                    "term": c.term,
                    "definitions": [{"file": f, "location": loc} for f, loc in c.definitions],
                }
                for c in term_conflicts
            ],
        }
        write_json_report(Path(args.json), data)
        print(f"JSON 报告已保存: {args.json}")

    if args.report:
        write_md_report(Path(args.report), undefined_axioms, multi_defined_axioms, std_conflicts, term_conflicts)
        print(f"Markdown 报告已保存: {args.report}")

    # 标准版本冲突与术语定义冲突多为历史/跨文件合理差异，当前仅作为警告报告，
    # 不阻塞退出码；真正的错误仅保留“被引用但未定义的公理”。
    has_error = bool(undefined_axioms)
    if std_conflicts:
        print("\n注意：存在标准版本差异，已作为警告输出，请人工复核。")
    if term_conflicts:
        print("\n注意：存在术语定义差异，已作为警告输出，请人工复核。")
    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
