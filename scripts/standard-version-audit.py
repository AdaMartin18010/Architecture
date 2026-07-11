#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
standard-version-audit.py
=========================

只读审计：扫描 struct/ 正文，检测“标准族 + 版本号”引用中是否使用了
canonical-names.yaml 标记为 invalid（不存在/已废弃）的版本号。

设计原则：
  - 只读、零改动：仅输出审计报告，绝不自动修改正文。
  - 跳过代码块、Mermaid、表格、标题、行内代码、Markdown 链接文本与 URL。
  - 命中 invalid 版本记为“疑似硬错误”，需人工结合上下文确认（历史对照语境可能合法）。

用法：
    python scripts/standard-version-audit.py
"""

import datetime
import re
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STRUCT_DIR = PROJECT_ROOT / "struct"
REPORT_FILE = PROJECT_ROOT / "reports" / "standard-version-audit.md"

# 族关键词 -> (匹配版本的正则, invalid 版本集合, 备注)
# 版本号形如 2023 / 4.0 / 1.2 / V4
FAMILIES: Dict[str, Tuple[str, set, str]] = {
    "ISO/IEC 25010":   (r"(?:ISO/IEC|ISO|IEC)?\s*25010\s*:?\s*(\d{4})", {"2024", "2025"}, "现行 2023；2011 为历史版"),
    "ISO/IEC/IEEE 42010": (r"(?:ISO/IEC/IEEE|ISO/IEC|ISO|IEC|IEEE)?\s*42010\s*:?\s*(\d{4})", set(), "现行 2022；2011 为历史版"),
    "ArchiMate":       (r"ArchiMate\s+(\d+\.\d+)", {"4.1", "4.2", "4.3", "5.0"}, "现行 4.0；3.2 为历史版；无 4.1/4.2/4.3/5.0"),
    "ISO/IEC 26550":   (r"(?:ISO/IEC|ISO|IEC)?\s*26550\s*:?\s*(\d{4})", {"2023", "2025"}, "现行 2015"),
    "ISO/IEC 26564":   (r"(?:ISO/IEC|ISO|IEC)?\s*26564\s*:?\s*(\d{4})", {"2025"}, "现行 2022"),
    "ISO/IEC 26565":   (r"(?:ISO/IEC|ISO|IEC)?\s*26565\s*:?\s*(\d{4})", {"2023", "2025"}, "现行 2026"),
    "IEC 62443-4-2":   (r"62443-4-2\s*:?\s*(\d{4})", {"2025"}, "现行 2019"),
}


def protected(line: str) -> List[Tuple[int, int]]:
    iv = []
    for m in re.finditer(r"`[^`]+`", line):
        iv.append((m.start(), m.end()))
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line):
        iv.append((m.start(1), m.end(1)))
        iv.append((m.start(2), m.end(2)))
    for m in re.finditer(r"<[^>]+>", line):
        iv.append((m.start(), m.end()))
    return iv


def audit_file(path: Path) -> List[dict]:
    hits = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    in_code = False
    for ln, line in enumerate(text.splitlines(), start=1):
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code or s.startswith("|") or re.match(r"^#{1,6}\s+", s):
            continue
        iv = protected(line)
        for fam, (pat, invalid, note) in FAMILIES.items():
            if not invalid:
                continue
            for m in re.finditer(pat, line):
                ver = m.group(1)
                if ver not in invalid:
                    continue
                a, b = m.start(), m.end()
                if any(a >= x and b <= y for x, y in iv):
                    continue
                hits.append({
                    "family": fam, "version": ver, "note": note,
                    "file": path.relative_to(PROJECT_ROOT).as_posix(),
                    "line": ln, "context": s[:160],
                })
    return hits


def main() -> int:
    all_hits: List[dict] = []
    for md in sorted(STRUCT_DIR.rglob("*.md")):
        if "_ARCHIVE" in md.parts or "_HISTORICAL" in md.parts:
            continue
        all_hits.extend(audit_file(md))

    by_fam: Dict[str, int] = {}
    for h in all_hits:
        by_fam[h["family"]] = by_fam.get(h["family"], 0) + 1

    lines = [
        "# 标准版本号硬错误审计（只读）",
        "",
        f"> 生成时间: {datetime.datetime.now().isoformat(timespec='seconds')}",
        "> 源: struct/ 正文 × canonical-names.yaml invalid_versions",
        "> 性质: 只读审计，不改动正文；命中为疑似不存在/已废弃版本号，需人工结合上下文确认。",
        "",
        "## 摘要",
        "",
        f"- 疑似命中总计: **{len(all_hits)}**",
        "",
        "| 标准族 | 疑似命中数 | 说明 |",
        "|--------|-----------|------|",
    ]
    for fam, (pat, invalid, note) in FAMILIES.items():
        if not invalid:
            continue
        lines.append(f"| {fam} | {by_fam.get(fam, 0)} | {note}（invalid={sorted(invalid)}）|")
    lines += ["", "## 明细", ""]
    if not all_hits:
        lines.append("未发现使用 invalid 版本号的正文引用（版本号维度已对齐）。")
    else:
        lines.append("| 标准族 | 命中版本 | 文件:行 | 上下文 |")
        lines.append("|--------|----------|---------|--------|")
        for h in all_hits:
            ctx = h["context"].replace("|", "\\|")
            lines.append(f"| {h['family']} | {h['version']} | {h['file']}:{h['line']} | {ctx} |")
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"疑似硬错误命中: {len(all_hits)}")
    for fam, c in sorted(by_fam.items()):
        print(f"  {fam}: {c}")
    print(f"报告: {REPORT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
