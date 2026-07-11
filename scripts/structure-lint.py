#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目录结构 Lint（Structure Lint）

校验 struct/ 目录结构与文档描述的一致性：
1. 编号规则：每个主题目录（struct/NN-xxx）下的编号子目录（NN-xxx）
   - 编号无重复；
   - 编号无跳空（从 01 起连续；`NN-reserved` 类预留目录可占据其编号槽位，
     额外的跳空豁免可通过下方 CONFIG 的 ALLOWED_GAPS 配置）。
2. 目录树双向对齐：struct/README.md「实际文件夹结构导航」代码块中出现的
   每个 `NN-xxx` 目录必须在文件系统中存在；文件系统中实际存在的每个
   `NN-xxx` 目录（struct/ 下任意深度，排除 _ARCHIVE）也必须出现在树中。
3. 输出 Markdown 报告 reports/structure-lint.md；存在不一致时 exit 1。

用法：
    python scripts/structure-lint.py
    python scripts/structure-lint.py --report reports/structure-lint.md
    python scripts/structure-lint.py --no-report
"""

import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple
from collections import defaultdict


# ============================ CONFIG ============================
# 预留目录名模式（如 08-reserved）：允许占据编号槽位而不视为跳空
RESERVED_DIR_RE = re.compile(r"^\d{2}-reserved$")
# 跳空豁免：{主题目录名: {允许缺失的编号集合}}，用于历史保留空号
ALLOWED_GAPS: Dict[str, Set[int]] = {}
# 编号目录名模式
NUMBERED_DIR_RE = re.compile(r"^(\d{2})-[A-Za-z0-9_-]+$")
# 排除目录（不参与任何校验）
EXCLUDE_DIR_NAMES = {"_ARCHIVE"}
# 目录树来源文件（相对项目根）
TREE_SOURCE = "struct/README.md"
# ================================================================


@dataclass
class LintIssue:
    category: str   # duplicate-number / numbering-gap / tree-missing-on-fs / fs-missing-in-tree
    location: str
    detail: str


@dataclass
class LintResult:
    issues: List[LintIssue] = field(default_factory=list)
    checked_topics: int = 0
    checked_numbered_dirs: int = 0
    tree_entries: int = 0

    @property
    def ok(self) -> bool:
        return not self.issues

    def add(self, category: str, location: str, detail: str):
        self.issues.append(LintIssue(category, location, detail))


def scan_filesystem(struct_dir: Path) -> Tuple[Dict[str, List[Tuple[int, str]]], Set[str]]:
    """扫描文件系统。

    返回：
    - topic_map: {主题目录名: [(编号, 子目录名), ...]}（仅编号子目录）
    - all_numbered: struct/ 下所有编号目录的相对路径集合（排除 _ARCHIVE）
    """
    topic_map: Dict[str, List[Tuple[int, str]]] = {}
    all_numbered: Set[str] = set()

    for topic in sorted(struct_dir.iterdir()):
        if not topic.is_dir() or topic.name in EXCLUDE_DIR_NAMES:
            continue
        if not NUMBERED_DIR_RE.match(topic.name):
            continue
        all_numbered.add(topic.name)
        subs: List[Tuple[int, str]] = []
        for sub in sorted(topic.iterdir()):
            if sub.is_dir():
                m = NUMBERED_DIR_RE.match(sub.name)
                if m:
                    subs.append((int(m.group(1)), sub.name))
                    all_numbered.add(f"{topic.name}/{sub.name}")
        topic_map[topic.name] = subs
    return topic_map, all_numbered


def check_numbering(topic_map: Dict[str, List[Tuple[int, str]]], result: LintResult):
    """规则 ①：编号无重复、无跳空（预留目录与 ALLOWED_GAPS 豁免）。"""
    for topic, subs in topic_map.items():
        result.checked_topics += 1
        result.checked_numbered_dirs += len(subs)
        if not subs:
            continue

        # 重复编号
        by_num: Dict[int, List[str]] = defaultdict(list)
        for num, name in subs:
            by_num[num].append(name)
        for num, names in sorted(by_num.items()):
            if len(names) > 1:
                result.add(
                    "duplicate-number",
                    f"struct/{topic}",
                    f"编号 {num:02d} 重复: {', '.join(sorted(names))}",
                )

        # 跳空：所有编号目录（含 reserved）的编号并集必须覆盖 1..max
        present = set(by_num.keys())
        allowed = ALLOWED_GAPS.get(topic, set())
        for n in range(1, max(present) + 1):
            if n not in present and n not in allowed:
                reserved_note = "（若该编号为预留空号，请创建 NN-reserved 占位目录或在 ALLOWED_GAPS 中登记）"
                result.add(
                    "numbering-gap",
                    f"struct/{topic}",
                    f"编号 {n:02d} 跳空 {reserved_note}",
                )


def parse_readme_tree(readme_path: Path) -> Set[str]:
    """解析 README 中的目录树代码块，返回所有 NN-xxx 目录相对路径集合。"""
    text = readme_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    # 定位包含 "struct/" 的 ```text / ``` 代码块
    tree_lines: List[str] = []
    in_block = False
    block_has_struct = False
    current: List[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_block:
                in_block = True
                current = []
                block_has_struct = False
            else:
                if block_has_struct:
                    tree_lines = current
                    break
                in_block = False
            continue
        if in_block:
            current.append(line)
            if "struct/" in line:
                block_has_struct = True

    entries: Set[str] = set()
    stack: Dict[int, str] = {}
    entry_re = re.compile(r"^(?P<prefix>(?:│   |    )*)(?:├──|└──)\s+(?P<name>[^\s#/]+)(?P<dir>/?)")
    for line in tree_lines:
        m = entry_re.match(line)
        if not m:
            continue
        if not m.group("dir"):
            continue  # 仅目录条目（以 / 结尾）
        depth = len(m.group("prefix")) // 4
        name = m.group("name")
        stack[depth] = name
        # 清理更深层残留
        for d in [d for d in stack if d > depth]:
            del stack[d]
        if NUMBERED_DIR_RE.match(name):
            path = "/".join(stack[d] for d in sorted(stack) if d <= depth)
            # 仅保留 struct/ 下的相对路径（树根行 "struct/" 本身不匹配编号模式）
            entries.add(path)
    return entries


def check_tree_alignment(struct_dir: Path, readme_path: Path, result: LintResult):
    """规则 ②：README 目录树与文件系统双向对齐（仅 NN-xxx 目录）。"""
    tree_entries = parse_readme_tree(readme_path)
    result.tree_entries = len(tree_entries)
    _, fs_entries = scan_filesystem(struct_dir)

    for rel in sorted(tree_entries - fs_entries):
        result.add(
            "tree-missing-on-fs",
            f"struct/{rel}",
            "目录树中登记但文件系统不存在",
        )
    for rel in sorted(fs_entries - tree_entries):
        result.add(
            "fs-missing-in-tree",
            f"struct/{rel}",
            "文件系统存在但未在目录树中登记",
        )


def write_report(report_path: Path, result: LintResult, tree_source: str):
    report_path.parent.mkdir(parents=True, exist_ok=True)
    by_cat: Dict[str, int] = defaultdict(int)
    for issue in result.issues:
        by_cat[issue.category] += 1

    lines = [
        "# 目录结构 Lint 报告",
        "",
        "## 概览",
        "",
        f"- 校验主题目录数: **{result.checked_topics}**",
        f"- 校验编号子目录数: **{result.checked_numbered_dirs}**",
        f"- 目录树编号条目数: **{result.tree_entries}**（来源 `{tree_source}`）",
        f"- 问题总数: **{len(result.issues)}**",
        f"- 结论: {'✅ 通过' if result.ok else '❌ 未通过'}",
        "",
        "## 校验规则",
        "",
        "1. **编号无重复**：同一主题目录下不得存在两个相同编号的子目录。",
        "2. **编号无跳空**：编号须从 01 起连续；`NN-reserved` 预留目录可占据编号槽位，"
        "额外豁免见脚本 `ALLOWED_GAPS` 配置。",
        "3. **目录树双向对齐**：目录树中每个 `NN-xxx` 必须在文件系统存在；"
        "文件系统中每个 `NN-xxx` 目录（排除 `_ARCHIVE`）必须在目录树中登记。",
        "",
    ]
    if result.issues:
        lines.extend(["## 问题明细", ""])
        for cat in sorted(by_cat, key=lambda c: -by_cat[c]):
            lines.append(f"### {cat}（{by_cat[cat]} 项）")
            lines.append("")
            for issue in result.issues:
                if issue.category == cat:
                    lines.append(f"- `{issue.location}` — {issue.detail}")
            lines.append("")
    else:
        lines.extend(["## 问题明细", "", "✅ 未发现问题。", ""])

    report_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="struct/ 目录结构 Lint")
    parser.add_argument("--report", metavar="PATH", default="reports/structure-lint.md",
                        help="Markdown 报告输出路径（默认 reports/structure-lint.md）")
    parser.add_argument("--no-report", action="store_true", help="不输出报告文件")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    struct_dir = project_root / "struct"
    readme_path = project_root / TREE_SOURCE

    if not struct_dir.is_dir():
        print(f"错误: 未找到 struct/ 目录: {struct_dir}", file=sys.stderr)
        return 2
    if not readme_path.is_file():
        print(f"错误: 未找到目录树来源文件: {readme_path}", file=sys.stderr)
        return 2

    result = LintResult()
    topic_map, _ = scan_filesystem(struct_dir)
    check_numbering(topic_map, result)
    check_tree_alignment(struct_dir, readme_path, result)

    if not args.no_report:
        report_path = project_root / args.report
        write_report(report_path, result, TREE_SOURCE)
        print(f"报告已保存: {report_path}")

    if result.ok:
        print(f"structure-lint 通过: 主题 {result.checked_topics} 个，"
              f"编号子目录 {result.checked_numbered_dirs} 个，目录树条目 {result.tree_entries} 个，无问题")
        return 0
    print(f"structure-lint 未通过: {len(result.issues)} 个问题", file=sys.stderr)
    for issue in result.issues:
        print(f"  [{issue.category}] {issue.location} — {issue.detail}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
