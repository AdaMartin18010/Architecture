#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
standard-version-audit.py
=========================

只读审计：扫描 struct/ 正文，检测两类问题：

1. “标准族 + 版本号”引用中使用了 canonical-names.yaml 标记为 invalid
   （不存在/已废弃）的版本号（历史规则，命中仅告警，不影响退出码）。
2. “畸形版本串”——批量归一脚本重复叠加产生的损坏文本，例如
   ``A2A v1.0.0.0.0.0.0.0``、``ISO/IEC/IEEE 1517:2010-2010``。
   此类命中无合法语境，命中时脚本以非零码退出（回归门控）。

设计原则：
  - 只读、零改动：仅输出审计报告，绝不自动修改正文。
  - 跳过代码块、Mermaid、表格、标题、行内代码、Markdown 链接文本与 URL
    （畸形版本串规则额外扫描标题与表格——损坏文本常出现在标题中）。
  - 命中 invalid 版本记为“疑似硬错误”，需人工结合上下文确认（历史对照语境可能合法）。

退出码：
  - 0: 无畸形版本串命中（invalid 版本告警不影响退出码）。
  - 1: 存在畸形版本串命中。

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


# 畸形版本串模式：批量归一重复叠加产物的回归检测
# (正则, 说明) —— 命中即视为损坏文本，无合法语境
MALFORMED_PATTERNS: List[Tuple[str, str]] = [
    (r"\bv\d+\.\d+(?:\.\d+){2,}", "版本号段数 ≥4（如 v1.0.0.0，疑似重复归一叠加）"),
    (r"\b(20\d\d)[-:]\1\b", "同一年份重复叠加（如 1517:2010-2010）"),
    (r"\bv(\d+\.\d+(?:\.\d+)?)[,; ]\s*v\1\b", "版本号重复叠加（如 v1.0 v1.0）"),
]


def audit_malformed_file(path: Path) -> List[dict]:
    """扫描畸形版本串（批量归一叠加产物）。与 audit_file 不同：
    标题与表格也纳入扫描——损坏文本常出现在标题/对齐标准行中。"""
    hits = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    in_code = False
    for ln, line in enumerate(text.splitlines(), start=1):
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        iv = protected(line)
        for pat, note in MALFORMED_PATTERNS:
            for m in re.finditer(pat, line):
                a, b = m.start(), m.end()
                if any(a >= x and b <= y for x, y in iv):
                    continue
                hits.append({
                    "pattern": pat, "match": m.group(0), "note": note,
                    "file": path.relative_to(PROJECT_ROOT).as_posix(),
                    "line": ln, "context": s[:160],
                })
    return hits


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
    malformed_hits: List[dict] = []
    for md in sorted(STRUCT_DIR.rglob("*.md")):
        if "_ARCHIVE" in md.parts or "_HISTORICAL" in md.parts:
            continue
        all_hits.extend(audit_file(md))
        malformed_hits.extend(audit_malformed_file(md))

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

    lines += [
        "",
        "## 畸形版本串回归检测",
        "",
        "> 检测批量归一脚本重复叠加产生的损坏文本（版本号段数 ≥4、同一年份/版本号重复叠加）。",
        "> 此类命中无合法语境，命中时脚本以非零码退出。",
        "",
        f"- 畸形版本串命中: **{len(malformed_hits)}**",
        "",
    ]
    if not malformed_hits:
        lines.append("未发现畸形版本串。")
    else:
        lines.append("| 命中文本 | 规则说明 | 文件:行 | 上下文 |")
        lines.append("|----------|----------|---------|--------|")
        for h in malformed_hits:
            ctx = h["context"].replace("|", "\\|")
            lines.append(f"| `{h['match']}` | {h['note']} | {h['file']}:{h['line']} | {ctx} |")
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"疑似硬错误命中: {len(all_hits)}")
    for fam, c in sorted(by_fam.items()):
        print(f"  {fam}: {c}")
    print(f"畸形版本串命中: {len(malformed_hits)}")
    for h in malformed_hits:
        print(f"  {h['file']}:{h['line']}  {h['match']}  ({h['note']})")
    print(f"报告: {REPORT_FILE}")
    # 仅“畸形版本串”规则影响退出码（回归门控）；invalid 版本告警保持历史行为
    return 1 if malformed_hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
