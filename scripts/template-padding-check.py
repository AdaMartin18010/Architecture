#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模板 Padding 治理脚本

扫描 struct/ 下所有 Markdown 文件，检测末尾或正文中机械重复的
「补充说明 / 概念定义 / 示例 / 反例 / 权威来源 / 分析 / 参考文献 /
延伸阅读 / 附录」等模板块，统计其占总行数比例，并输出 Top 20
padding 占比最高的文件列表。

用法：
    python scripts/template-padding-check.py
    python scripts/template-padding-check.py --output reports/template-padding-report.md

退出码：
    0  正常完成（即使最高占比超过 30%，也仅打印 WARNING 而不失败）
"""

import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List


@dataclass
class PaddingRecord:
    path: str
    total_lines: int
    padding_lines: int
    ratio: float
    matched_sections: List[str] = field(default_factory=list)


# 被视为模板 Padding 的二级/三级/四级标题模式。
# 这些标题通常出现在文件末尾，机械重复「概念定义+示例+反例+权威来源」组合。
PADDING_HEADING_PATTERNS = [
    r"^(#{2,4})\s+补充说明",
    r"^(#{2,4})\s+概念定义\s*$",
    r"^(#{2,4})\s+示例\s*$",
    r"^(#{2,4})\s+反例\s*$",
    r"^(#{2,4})\s+权威来源\s*$",
    r"^(#{2,4})\s+分析\s*$",
    r"^(#{2,4})\s+参考文献\s*$",
    r"^(#{2,4})\s+延伸阅读\s*$",
    r"^(#{2,4})\s+附录\s*$",
]


def calculate_padding(lines: List[str]) -> tuple:
    """返回 (模板块行数, 命中的小节标题列表)。"""
    is_padding = [False] * len(lines)
    patterns = [re.compile(p) for p in PADDING_HEADING_PATTERNS]
    matched_sections: List[str] = []
    i = 0
    while i < len(lines):
        matched = False
        for p in patterns:
            m = p.match(lines[i])
            if m:
                level = len(m.group(1))
                title = lines[i].strip().lstrip("#").strip()
                matched_sections.append(title)
                is_padding[i] = True
                i += 1
                while i < len(lines):
                    m2 = re.match(r"^(#{1,6})\s", lines[i])
                    if m2 and len(m2.group(1)) <= level:
                        break
                    is_padding[i] = True
                    i += 1
                matched = True
                break
        if not matched:
            i += 1
    return sum(is_padding), matched_sections


def scan(root: Path) -> List[PaddingRecord]:
    records: List[PaddingRecord] = []
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root).as_posix()
        # 跳过模板、审计、工具说明自身，避免自我污染统计
        if any(
            p in rel
            for p in (
                "99-reference/templates/",
                "99-reference/audit/",
                "99-reference/tools/",
                "_HISTORICAL_",
                "plans-tasks/",
            )
        ):
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        total = len(lines)
        if total == 0:
            continue
        padding, sections = calculate_padding(lines)
        ratio = padding / total * 100
        records.append(
            PaddingRecord(
                path=rel,
                total_lines=total,
                padding_lines=padding,
                ratio=ratio,
                matched_sections=sections,
            )
        )
    records.sort(key=lambda r: r.ratio, reverse=True)
    return records


def generate_report(records: List[PaddingRecord], top_n: int = 20) -> str:
    lines = [
        "# Template Padding 治理报告",
        "",
        "> 生成命令：`python scripts/template-padding-check.py`",
        "",
        "## 统计概览",
        "",
        f"- 扫描文件数：{len(records)}",
        f"- 平均 Padding 占比：{sum(r.ratio for r in records) / len(records):.2f}%" if records else "- 平均 Padding 占比：0.00%",
        f"- 最高 Padding 占比：{records[0].ratio:.2f}%" if records else "- 最高 Padding 占比：0.00%",
        f"- 占比超过 30% 的文件数：{sum(1 for r in records if r.ratio > 30)}",
        "",
        f"## Top {top_n} Padding 占比文件",
        "",
        "| 排名 | 文件 | 总行数 | 模板块行数 | 占比 | 命中板块 |",
        "|---:|---|---:|---:|---:|---|",
    ]
    for idx, r in enumerate(records[:top_n], start=1):
        sections = "、".join(r.matched_sections[:4])
        if len(r.matched_sections) > 4:
            sections += "…"
        lines.append(
            f"| {idx} | `{r.path}` | {r.total_lines} | {r.padding_lines} | {r.ratio:.2f}% | {sections} |"
        )

    lines.extend(
        [
            "",
            "## 说明",
            "",
            "1. 「模板块」指机械重复的「补充说明 / 概念定义 / 示例 / 反例 / 权威来源 / 分析 / 参考文献 / 延伸阅读 / 附录」等小节。",
            "2. 占比 = 模板块行数 / 文件总行数 × 100%。",
            "3. 占比超过 30% 时建议审视：是否已在正文完整阐述后仍机械重复？是否可用交叉引用替代？",
            "4. 治理规则详见 [`struct/99-reference/templates/content-block-guideline.md`](../struct/99-reference/templates/content-block-guideline.md)。",
        ]
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="检测 Markdown 文件中的模板 Padding 占比")
    parser.add_argument(
        "--output",
        default="reports/template-padding-report.md",
        help="报告输出路径（默认：reports/template-padding-report.md）",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="Top N 文件数（默认：20）",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    struct_root = project_root / "struct"

    records = scan(struct_root)
    report = generate_report(records, top_n=args.top)

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = project_root / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    if records:
        top = records[0]
        print(f"扫描完成：{len(records)} 个文件，最高占比 {top.ratio:.2f}%（{top.path}）")
        print(f"报告已保存：{output_path}")
        if top.ratio > 30:
            print(
                f"WARNING: 最高模板 Padding 占比 {top.ratio:.2f}% 超过 30%，建议按治理规则精简。",
                file=sys.stderr,
            )
    else:
        print("扫描完成：未找到 Markdown 文件。")

    return 0


if __name__ == "__main__":
    sys.exit(main())
