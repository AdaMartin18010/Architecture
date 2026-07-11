#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
standard-name-first-mention.py
==============================

标准名称归一 backlog 收口工具（保守策略）。

策略：
- Part A：对"纯前缀/年份补全、大小写变体、安全截断"类别名做全量替换（仅未保护正文行）。
- Part B：对高频简写族（TOGAF/SWEBOK/MCP/A2A/SLSA/EU CRA）执行"首次出现展开"：
  每个文件中，若该族的第一次未保护出现是裸简写，则展开为 canonical/全称形式；
  后续出现保留简写（符合 book-format-guide 6.4 版本标注规则）。

保护语境（不替换、不计入首次出现）：
- YAML frontmatter、代码块、Mermaid、表格行、标题行
- quiz 选项行（- A. / ✅ / ❌）
- 行内代码 span、Markdown 链接文本
- 含 http 的引用/链接行（仅跳过替换；其中的全称仍计为"已引入"）

用法：
    python scripts/standard-name-first-mention.py            # dry-run，打印计划修改
    python scripts/standard-name-first-mention.py --apply    # 实际写入
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 领地目录
SCOPE_DIRS = [
    "struct/01-meta-model-standards",
    "struct/02-business-architecture-reuse",
    "struct/03-application-architecture-reuse",
    "struct/04-component-architecture-reuse",
    "struct/06-cross-layer-governance",
    "struct/07-formal-verification",
    "struct/08-cognitive-architecture",
    "struct/09-value-quantification",
    "struct/99-reference",
]
SCOPE_FILES = ["struct/README.md", "struct/MASTER_PLAN.md"]

# 历史记录/审计快照文件：原则上不改
EXCLUDE_PATTERNS = [
    re.compile(r"CHANGELOG", re.I),
    re.compile(r"/audit/", re.I),
    re.compile(r"_HISTORICAL", re.I),
    re.compile(r"_ARCHIVE", re.I),
    re.compile(r"20\d\d-\d\d-\d\d"),          # 带日期的快照报告
    re.compile(r"20\d\d-q[1-4]", re.I),       # 季度快照
    re.compile(r"-report\.md$", re.I),        # tracker 类快照报告
    re.compile(r"gap-analysis", re.I),
    re.compile(r"fact-fix", re.I),
    re.compile(r"book-format-guide\.md$"),  # 格式规范本身，示例须保持字面
]

# ---------------------------------------------------------------- Part A
# 安全全量替换（正则 -> 替换文本）。仅作用于未保护正文行。
PART_A_RULES: List[Tuple[str, str, str]] = [
    (r"(?<![A-Za-z0-9\-/.])SWEBOK v4\b", "SWEBOK V4", "SWEBOK v4 大小写变体"),
    (r"(?<![A-Za-z0-9\-/.])ISA95\b", "ISA-95", "ISA95 缺连字符"),
    (r"(?<![A-Za-z0-9\-/.])SLSA v1\.0\b", "SLSA 1.0", "SLSA v1.0 变体"),
    (r"(?<![A-Za-z0-9\-/.])TOGAF Standard 10th Edition\b", "TOGAF Standard 10", "TOGAF Standard 10th Edition 格式变体"),
    (r"(?<![A-Za-z0-9\-/.])TOGAF 10\b", "TOGAF Standard 10", "TOGAF 10 版本简写"),
    (r"(?<![A-Za-z0-9\-/.])A2A v1\.0\b(?!\.)", "A2A v1.0.0", "A2A v1.0 版本简写"),
    (r"(?<![A-Za-z0-9\-/.])ArchiMate 4\.0 Specification\b", "ArchiMate 4.0", "ArchiMate 4.0 Specification 截断"),
    (r"(?<![A-Za-z0-9\-/.])ArchiMate 3\.2 Specification\b", "ArchiMate 3.2", "ArchiMate 3.2 Specification 截断"),
    (r"(?<![A-Za-z0-9\-/.])ISO 33000\b", "ISO/IEC 33000", "ISO 33000 缺 IEC"),
    (r"(?<![A-Za-z0-9\-/.])ISO 25040:2024\b", "ISO/IEC 25040:2024", "ISO 25040:2024 缺 IEC"),
    (r"(?<![A-Za-z0-9\-/.])ISO 25040\b(?!:)", "ISO/IEC 25040:2024", "ISO 25040 简写"),
    (r"(?<![A-Za-z0-9\-/.])ISO 30141\b(?!:)", "ISO/IEC 30141:2024", "ISO 30141 简写"),
    (r"(?<![A-Za-z0-9\-/.])ISO 21838\b(?![:\\-])", "ISO/IEC 21838", "ISO 21838 简写"),
    (r"(?<![A-Za-z0-9\-/.])ISO 42001\b(?!:)", "ISO/IEC 42001:2023", "ISO 42001 简写"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 42001\b(?!:)", "ISO/IEC 42001:2023", "ISO/IEC 42001 缺年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 5230\b(?!:)", "ISO/IEC 5230:2024", "ISO/IEC 5230 缺年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO 26565\b(?!:)", "ISO/IEC 26565:2026", "ISO 26565 简写"),
    (r"(?<![A-Za-z0-9\-/.])ISO 5962\b", "ISO/IEC 5962", "ISO 5962 缺 IEC"),
    (r"(?<![A-Za-z0-9\-/.])ISO 26566:2026\b", "ISO/IEC 26566:2026", "ISO 26566:2026 缺 IEC"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 42020\b(?!:)", "ISO/IEC/IEEE 42020:2019", "ISO/IEC 42020 缺 IEEE/年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO 12207:2026\b", "ISO/IEC/IEEE 12207:2026", "ISO 12207:2026 缺 IEC/IEEE"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 12207:2026\b", "ISO/IEC/IEEE 12207:2026", "ISO/IEC 12207:2026 缺 IEEE"),
    (r"(?<![A-Za-z0-9\-/.])IEC 62443-4-2\b(?!:)", "IEC 62443-4-2:2019", "IEC 62443-4-2 缺年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 33004\b(?!:)", "ISO/IEC 33004:2022", "ISO/IEC 33004 缺年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 33003\b(?!:)", "ISO/IEC 33003:2019", "ISO/IEC 33003 缺年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 33020\b(?!:)", "ISO/IEC 33020:2019", "ISO/IEC 33020 缺年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 25059\b(?!:)", "ISO/IEC 25059:2023", "ISO/IEC 25059 缺年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 25011\b(?!:)", "ISO/IEC 25011:2017", "ISO/IEC 25011 缺年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 33001\b(?!:)", "ISO/IEC 33001:2014", "ISO/IEC 33001 缺年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO 15704\b(?!:)", "ISO 15704:2019", "ISO 15704 缺年份"),
    (r"(?<![A-Za-z0-9\-/.])NIST SP 800-161 Rev\. 1\b", "NIST SP 800-161", "NIST SP 800-161 Rev. 1 精简"),
    (r"(?<![A-Za-z0-9\-/.])(?<!NIST )SSDF 1\.2\b", "NIST SSDF 1.2", "SSDF 1.2 缺 NIST 前缀"),
]
PART_A = [(re.compile(p), r, d) for p, r, d in PART_A_RULES]

# ---------------------------------------------------------------- Part B
# 首次出现展开族配置
FAMILIES = [
    {
        "name": "TOGAF",
        "replacement": "TOGAF Standard 10",
        "full_patterns": [
            r"TOGAF Standard 10\b", r"TOGAF Standard,\s*10th Edition", r"TOGAF®",
            r"TOGAF Standard 10th Edition", r"The Open Group Architecture Framework",
            r"TOGAF 10\b", r"TOGAF Standard, Version", r"TOGAF®? Standard, Version",
        ],
        "alias": r"TOGAF",
        "skip_follow": [
            r"\s+Standard", r"®", r"\s+10\b", r"\s+9\.", r"\s+Series", r"\s+Library",
            r"\s+Architecture Content", r"\s+-", r"\s+Version", r"\(", r"（", r"\s+ADM and",
        ],
    },
    {
        "name": "SWEBOK",
        "replacement": "SWEBOK V4",
        "full_patterns": [r"SWEBOK V4", r"SWEBOK v4", r"SWEBOK 4\b", r"SWEBOK Guide",
                          r"Software Engineering Body of Knowledge"],
        "alias": r"SWEBOK",
        "skip_follow": [r"\s+V4", r"\s+v4", r"\s+4\b", r"\s+Guide", r"\(", r"（"],
    },
    {
        "name": "MCP",
        "replacement": "MCP（Model Context Protocol）",
        "full_patterns": [r"MCP 2025-11-25", r"MCP 2026-07-28", r"MCP 2025-03-26",
                          r"Model Context Protocol", r"MCP 2026\b"],
        "alias": r"MCP",
        "skip_follow": [
            r"\s+2025", r"\s+2026", r"\s+Tool", r"\s+Server", r"\s+Client", r"\s+Registry",
            r"\s+Apps?\b", r"\s+Gateway", r"\s+Specification", r"\s+Spec\b", r"\s+Top",
            r"\s+Introduction", r"\s+Authorization", r"\s+Companion", r"\s+for\b",
            r"\s+Industrial", r"\s+Protocol", r"\s+协议", r"\s+版本", r"\.", r"\+",
            r"\(", r"（", r"-",
        ],
        "skip_precede": [r"OWASP\s+$"],
    },
    {
        "name": "A2A",
        "replacement": "A2A（Agent-to-Agent Protocol）",
        "full_patterns": [r"A2A v1", r"Agent-to-Agent", r"A2A（Agent-to-Agent"],
        "alias": r"A2A",
        "skip_follow": [r"\s+v1", r"\(", r"（", r"\+", r"-", r"\.", r"\s+Protocol",
                        r"\s+协议"],
    },
    {
        "name": "SLSA",
        "replacement": "SLSA 1.2",
        "full_patterns": [r"SLSA 1\.[012]\b", r"SLSA v1", r"Supply-chain Levels",
                          r"Supply Chain Levels"],
        "alias": r"SLSA",
        "skip_follow": [r"\s+1\.", r"\s+v1", r"\s+L[1-4]\b", r"\s+Level", r"\s+Build",
                        r"\s+Multi", r"\s+Track", r"\s+Framework", r"\.", r"\+", r"\(",
                        r"（", r"[:：]", r"\*"],
        # 文件同时讨论 SLSA 1.0/1.1 历史版本时不自动展开（版本语境敏感）
        "file_veto": r"SLSA\s+(?:1\.[01]\b|v1\.[01]\b)",
    },
    {
        "name": "EU CRA",
        "replacement": "EU CRA 2024/2847",
        "full_patterns": [r"EU CRA 2024/2847", r"EU CRA \(2024\)", r"Cyber Resilience Act",
                          r"2024/2847"],
        "alias": r"EU CRA",
        "skip_follow": [r"\s+2024", r"\(", r"（"],
    },
]

QUIZ_OPTION = re.compile(r"^\s*[-*]\s+[A-D][.、)]")
HEADING = re.compile(r"^#{1,6}\s+")
LINK_SPAN = re.compile(r"\[[^\]]*\]\([^)]*\)")
INLINE_CODE = re.compile(r"`[^`]*`")


def mask_line(line: str) -> str:
    """把行内代码与 Markdown 链接替换为等长空格，保持偏移。"""
    def blank(m: re.Match) -> str:
        return " " * (m.end() - m.start())
    masked = INLINE_CODE.sub(blank, line)
    masked = LINK_SPAN.sub(blank, masked)
    return masked


def is_excluded(rel_path: str) -> bool:
    return any(p.search(rel_path) for p in EXCLUDE_PATTERNS)


def collect_files() -> List[Path]:
    files: List[Path] = []
    for d in SCOPE_DIRS:
        files.extend(sorted((PROJECT_ROOT / d).rglob("*.md")))
    for f in SCOPE_FILES:
        p = PROJECT_ROOT / f
        if p.exists():
            files.append(p)
    result = []
    for p in files:
        rel = p.relative_to(PROJECT_ROOT).as_posix()
        if not is_excluded(rel):
            result.append(p)
    return result


def process_file(path: Path, apply: bool) -> List[str]:
    """返回该文件的修改日志（dry-run 或实际修改）。"""
    rel = path.relative_to(PROJECT_ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    logs: List[str] = []

    # 预计算行状态
    in_code = False
    in_front = False
    states = []  # (original, masked, protected_line)
    for i, line in enumerate(lines):
        stripped = line.strip()
        if i == 0 and stripped == "---":
            in_front = True
            states.append((line, "", True))
            continue
        if in_front:
            states.append((line, "", True))
            if stripped == "---" or stripped == "...":
                in_front = False
            continue
        if stripped.startswith("```"):
            in_code = not in_code
            states.append((line, "", True))
            continue
        protected = (
            in_code
            or stripped.startswith("|")
            or HEADING.match(stripped)
            or QUIZ_OPTION.match(stripped)
            or "✅" in stripped
            or "❌" in stripped
        )
        states.append((line, mask_line(line), protected))

    changed = False

    # ---- Part A：全量安全替换（跳过含 http 的行，保守处理引用块）
    # 匹配在 masked 行上进行（行内代码/链接文本已被置空），再按偏移回写原行；
    # 斜体引用标题（*Title*）内的命中跳过。
    for idx, (orig, masked, protected) in enumerate(states):
        if protected or "http" in orig.lower():
            continue
        cur, cur_masked = orig, masked
        for pattern, repl, desc in PART_A:
            spans = []
            for m in pattern.finditer(cur_masked):
                s = m.start()
                if cur[max(0, s - 1):s] in "<(":
                    continue
                if cur[:s].count("*") % 2 == 1:  # 斜体引用标题内
                    continue
                spans.append((m.start(), m.end()))
            if spans:
                for s, e in reversed(spans):
                    cur = cur[:s] + repl + cur[e:]
                cur_masked = mask_line(cur)
                logs.append(f"[A] {rel}:{idx + 1} ({desc})")
        if cur != orig:
            lines[idx] = cur
            states[idx] = (cur, cur_masked, protected)
            changed = True

    # ---- Part B：首次出现展开
    for fam in FAMILIES:
        if fam.get("file_veto") and re.search(fam["file_veto"], text):
            continue
        full_res = [re.compile(p) for p in fam["full_patterns"]]
        alias_re = re.compile(rf"(?<![A-Za-z0-9\-./®]){fam['alias']}(?![A-Za-z0-9\-./])")
        skip_f = [re.compile(p) for p in fam.get("skip_follow", [])]
        skip_p = [re.compile(p) for p in fam.get("skip_precede", [])]

        done = False
        for idx, (orig, masked, protected) in enumerate(states):
            if done or protected:
                continue
            has_http = "http" in orig.lower()
            # 同一行任意位置出现全称，视为已引入
            if any(fr.search(masked) for fr in full_res):
                done = True
                continue
            # 找该行最早的"全称"或"裸简写"出现
            best: Optional[Tuple[int, str, re.Match]] = None  # (pos, kind, match)
            for fr in full_res:
                m = fr.search(masked)
                if m and (best is None or m.start() < best[0]):
                    best = (m.start(), "full", m)
            for m in alias_re.finditer(masked):
                s, e = m.start(), m.end()
                # 前后语境检查（基于原行）
                if orig[max(0, s - 1):s] in "<(":
                    continue
                if any(sp.search(orig[:s]) for sp in skip_p):
                    continue
                tail = orig[e:e + 40]
                if any(sf.match(tail) for sf in skip_f):
                    continue
                if best is None or s < best[0]:
                    best = (s, "alias", m)
                break  # 只需该别名在行内的第一个有效出现
            if best is None:
                continue
            if best[1] == "full":
                done = True  # 全称已先出现，无需处理
                continue
            if has_http:
                continue  # 引用/链接行：不替换，也不算引入，继续向后找
            # 执行首次出现展开
            s, e = best[2].start(), best[2].end()
            new_line = orig[:s] + fam["replacement"] + orig[e:]
            lines[idx] = new_line
            states[idx] = (new_line, mask_line(new_line), protected)
            changed = True
            logs.append(f"[B:{fam['name']}] {rel}:{idx + 1} :: {orig.strip()[:80]}")
            done = True

    if changed and apply:
        path.write_text("\n".join(lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")
    return logs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="实际写入修改（默认 dry-run）")
    args = ap.parse_args()

    files = collect_files()
    total_logs: List[str] = []
    touched = 0
    for p in files:
        logs = process_file(p, apply=args.apply)
        if logs:
            touched += 1
            total_logs.extend(logs)
    for line in total_logs:
        print(line)
    print(f"\n共 {len(total_logs)} 处修改，涉及 {touched} 个文件"
          f"（{'已应用' if args.apply else 'dry-run'}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
