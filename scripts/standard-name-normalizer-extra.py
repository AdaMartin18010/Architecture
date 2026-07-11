#!/usr/bin/env python3
"""
standard-name-normalizer-extra.py
=================================

对 canonical-names.yaml 中“明显安全”但标准脚本未覆盖的别名执行补充替换。

安全规则：
- 仅处理普通正文段落；跳过代码块、Mermaid、表格、标题、行内代码、Markdown 链接文本、URL。
- 仅替换不会造成版本/语义漂移的格式变体、缺少年份/前缀的写法。
- 高风险或歧义别名（MCP、SLSA、OPC UA、A2A、TOGAF、OWASP 等）不处理。
"""

import re
from pathlib import Path
from typing import List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 规则：正则模式 -> 替换文本
EXTRA_SAFE_REPLACEMENTS: List[Tuple[str, str]] = [
    # 格式变体 / 官方标题规范
    (r"TOGAF Standard, 10th Edition", "TOGAF Standard 10"),
    (r"TOGAF Standard 10th Edition", "TOGAF Standard 10"),
    (r"IEEE 1471-2000", "IEEE 1471:2000"),
    (r"ISA95", "ISA-95"),
    (r"SLSA v1\.0", "SLSA 1.0"),
    (r"SWEBOK v4", "SWEBOK V4"),
    (r"ArchiMate 4\.0 Specification", "ArchiMate 4.0"),
    # 注：不为 "ArchiMate 3.2 Specification" 去后缀——参考文献语境需保留官方题名

    # ISO/IEC 前缀缺失 + 年份补齐（低风险）
    (r"ISO 42010\b(?!:)", "ISO/IEC/IEEE 42010:2022"),
    (r"ISO 25010\b(?!:)", "ISO/IEC 25010:2023"),
    (r"ISO 26550\b(?!:)", "ISO/IEC 26550:2015"),
    (r"ISO 21838\b", "ISO/IEC 21838"),
    (r"ISO 5962\b", "ISO/IEC 5962"),
    (r"ISO 26565\b", "ISO/IEC 26565:2026"),
    (r"ISO 26566:2026", "ISO/IEC 26566:2026"),
    (r"ISO 30141\b(?!:)", "ISO/IEC 30141:2024"),
    (r"ISO/IEC 30141\b(?!:)", "ISO/IEC 30141:2024"),
    (r"ISO 33000\b", "ISO/IEC 33000"),
    (r"ISO/IEC 33004\b(?!:)", "ISO/IEC 33004:2022"),
    (r"ISO/IEC 33003\b(?!:)", "ISO/IEC 33003:2019"),
    (r"ISO/IEC 33020\b(?!:)", "ISO/IEC 33020:2019"),
    (r"ISO/IEC 33001\b(?!:)", "ISO/IEC 33001:2014"),
    (r"ISO/IEC 42001\b(?!:)", "ISO/IEC 42001:2023"),
    (r"ISO 42001\b(?!:)", "ISO/IEC 42001:2023"),
    (r"ISO/IEC 5230\b(?!:)", "ISO/IEC 5230:2024"),
    (r"ISO/IEC 25059\b(?!:)", "ISO/IEC 25059:2023"),
    (r"ISO/IEC 25011\b(?!:)", "ISO/IEC 25011:2017"),
    (r"ISO 15704\b", "ISO 15704:2019"),

    # 直接年份/组织补齐
    (r"ISO 25040:2024", "ISO/IEC 25040:2024"),
    (r"ISO 25040\b(?!:)", "ISO/IEC 25040:2024"),
    (r"ISO/IEC 25040\b(?!:)", "ISO/IEC 25040:2024"),
    (r"ISO/IEC 12207:2026", "ISO/IEC/IEEE 12207:2026"),
    (r"ISO 12207:2026", "ISO/IEC/IEEE 12207:2026"),
    (r"IEC 62443-4-2\b(?!:)", "IEC 62443-4-2:2019"),
    (r"IEEE 1012-2024", "ISO/IEC/IEEE 1012:2024"),
    (r"ISO/IEC 42020:2019", "ISO/IEC/IEEE 42020:2019"),
    (r"ISO/IEC 42020\b(?!:)", "ISO/IEC/IEEE 42020:2019"),

    # NIST 变体（仅无歧义补全；800-204A/800-204B 为独立真实文档，不归到 800-204）
    (r"NIST SP 800-161 Rev\. 1", "NIST SP 800-161"),
    (r"(?<!NIST )SSDF 1\.2\b", "NIST SSDF 1.2"),
    # 注：不做 BPMN 2.1->2.0——“没有官方 BPMN 2.1” 等否定语境会被颠倒语义
]


def protected_intervals(line: str) -> List[Tuple[int, int]]:
    """返回行内需要保护的区域：行内代码、Markdown 链接文本、URL 尖括号。"""
    intervals = []
    # 行内代码 `...`
    for m in re.finditer(r"`[^`]+`", line):
        intervals.append((m.start(), m.end()))
    # Markdown 链接文本 [text](url)
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line):
        intervals.append((m.start(1), m.end(1)))
    # URL <...>
    for m in re.finditer(r"<[^>]+>", line):
        intervals.append((m.start(), m.end()))
    return intervals


def apply_extra_fixes(file_path: Path) -> int:
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_code_block = False
    in_mermaid = False
    new_lines = []
    replacements = 0
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            in_mermaid = in_code_block and "mermaid" in stripped.lower()
            new_lines.append(line)
            continue
        if in_code_block or in_mermaid or stripped.startswith("|") or re.match(r"^#{1,6}\s+", stripped):
            new_lines.append(line)
            continue
        intervals = protected_intervals(line)
        new_line = line
        for pattern, repl in EXTRA_SAFE_REPLACEMENTS:
            def replacer(m: re.Match) -> str:
                s, e = m.start(), m.end()
                # 命中位于保护区则跳过
                for a, b in intervals:
                    if s >= a and e <= b:
                        return m.group(0)
                # 若原文紧接着已有“:年份”，避免制造重复年份（如 ISO 42010:2022）
                if re.match(r":\d", new_line[e:e + 2]):
                    return m.group(0)
                return repl
            new_line, count = re.subn(pattern, replacer, new_line)
            replacements += count
        new_lines.append(new_line)
    new_text = "\n".join(new_lines)
    if new_text != text:
        file_path.write_text(new_text, encoding="utf-8")
    return replacements


def main() -> int:
    md_files = sorted((PROJECT_ROOT / "struct").rglob("*.md"))
    total = 0
    for md_file in md_files:
        if "_ARCHIVE" in md_file.parts or "_HISTORICAL" in md_file.parts:
            continue
        total += apply_extra_fixes(md_file)
    print(f"额外安全替换完成: {total} 处")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
