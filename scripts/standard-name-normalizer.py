#!/usr/bin/env python3
"""
standard-name-normalizer.py
===========================

全项目标准名称归一检查器（R4：一号一 URL / 全称统一）。

功能：
- 读取 canonical-names.yaml 中的 canonical 与 aliases。
- 扫描 struct/ 与 view/ 下 Markdown 文件，发现使用别名/简写的位置。
- 生成报告 reports/standard-name-normalization-report.md，建议替换为 canonical 全称。

用法：
    python scripts/standard-name-normalizer.py
    python scripts/standard-name-normalizer.py --fix-safe   # 对纯正文安全替换

退出码：0（仅报告，不导致 CI 失败）
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_NAMES_PATH = PROJECT_ROOT / "struct" / "99-reference" / "tools" / "canonical-names.yaml"
REPORT_PATH = PROJECT_ROOT / "reports" / "standard-name-normalization-report.md"


def load_aliases(path: Path) -> Dict[str, str]:
    """返回 alias -> canonical 的映射（不含 canonical 自身）。"""
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    alias_map: Dict[str, str] = {}
    for item in data.get("standards", []):
        canonical = item.get("canonical", "")
        if not canonical:
            continue
        for alias in item.get("aliases", []):
            if alias and alias != canonical:
                alias_map[alias] = canonical
    return alias_map


def build_alias_patterns(alias_map: Dict[str, str]) -> List[Tuple[re.Pattern, str, str]]:
    """把 alias 编译成正则，要求前后不是字母/数字/连字符/句点/斜杠。"""
    patterns = []
    for alias, canonical in sorted(alias_map.items(), key=lambda x: -len(x[0])):
        # 对含特殊字符的 alias 做转义；允许前后是中文标点、空格、行首/行尾
        escaped = re.escape(alias)
        pattern = re.compile(rf"(?<![A-Za-z0-9\-./]){escaped}(?![A-Za-z0-9\-./])")
        patterns.append((pattern, alias, canonical))
    return patterns


def scan_file(file_path: Path, patterns: List[Tuple[re.Pattern, str, str]]) -> List[Dict]:
    """扫描单个 Markdown 文件，只报告普通正文中的别名使用。"""
    findings = []
    try:
        text = file_path.read_text(encoding="utf-8")
    except Exception:
        return findings

    in_code_block = False
    in_mermaid = False
    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.rstrip("\n")
        stripped = line.strip()
        # 代码块边界
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            in_mermaid = in_code_block and "mermaid" in stripped.lower()
            continue
        # 跳过代码块、Mermaid 图、表格行、标题
        if in_code_block or in_mermaid or stripped.startswith("|") or re.match(r"^#{1,6}\s+", stripped):
            continue
        for pattern, alias, canonical in patterns:
            for match in pattern.finditer(line):
                start, end = match.start(), match.end()
                # 跳过 URL 尖括号 / 普通 Markdown 链接文本括号内 / 全称展开式的括号内（含全角括号）
                if line[max(0, start - 1):start] in "<(（":
                    continue
                # 如果别名后紧跟 `:YYYY`，说明当前已经是更完整的版本写法，跳过
                if re.match(r":\d{4}", line[end:end + 5]):
                    continue
                findings.append({
                    "file": file_path.relative_to(PROJECT_ROOT).as_posix(),
                    "line_no": line_no,
                    "line": line.strip(),
                    "alias": alias,
                    "canonical": canonical,
                })
    return findings


def generate_report(findings: List[Dict]) -> str:
    lines = [
        "# 标准名称归一检查报告（R4）",
        "",
        f"> 扫描范围：`struct/` + `view/` 下所有 Markdown 正文段落",
        f"> 发现问题：{len(findings)} 处别名/简写使用",
        "> 规则：出现别名时建议统一替换为 canonical 全称，确保项目内一号一称。",
        "",
        "| 文件 | 行号 | 当前写法 | 建议 canonical | 上下文 |",
        "|------|------|----------|----------------|--------|",
    ]
    for f in findings:
        ctx = f["line"].replace("|", "\\|")
        # 把上下文中的 Markdown 链接转为纯文本，避免被 link-checker 误判
        ctx = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1（\2）", ctx)
        if len(ctx) > 120:
            ctx = ctx[:117] + "..."
        lines.append(
            f"| `{f['file']}` | {f['line_no']} | {f['alias']} | {f['canonical']} | {ctx} |"
        )
    lines.extend([
        "",
        "## 说明",
        "",
        "- 本报告仅扫描普通正文段落；代码块、Mermaid 图、表格、标题、URL 中的命中已被过滤。",
        "- 是否替换需结合上下文判断（如历史版本讨论、列表项可保留简写）。",
        "- canonical 定义见 [`struct/99-reference/tools/canonical-names.yaml`](../struct/99-reference/tools/canonical-names.yaml)。",
        "",
    ])
    return "\n".join(lines)


# 安全替换规则：
# - 使用负向回顾 (?<![A-Za-z0-9\-/.]) 避免把已有完整前缀中的简写再拼接。
# - 仅处理明确年份的变体，避免跨版本误伤。
SAFE_REPLACEMENTS = [
    (r"(?<![A-Za-z0-9\-/.])ISO 42010:2022", "ISO/IEC/IEEE 42010:2022", "ISO 42010:2022 缺 IEC/IEEE"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 42010:2022", "ISO/IEC/IEEE 42010:2022", "ISO/IEC 42010:2022 缺 IEEE"),
    (r"(?<![A-Za-z0-9\-/.])ISO 42010\b(?!:)", "ISO/IEC/IEEE 42010:2022", "ISO 42010 简写"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 42010\b(?!:)", "ISO/IEC/IEEE 42010:2022", "ISO/IEC 42010 缺 IEEE/年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO 25010:2023", "ISO/IEC 25010:2023", "ISO 25010:2023 缺 IEC"),
    (r"(?<![A-Za-z0-9\-/.])ISO 25010\b(?!:)", "ISO/IEC 25010:2023", "ISO 25010 简写"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 25010:2024", "ISO/IEC 25010:2023", "ISO/IEC 25010:2024 不存在版本"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 25010\b(?!:)", "ISO/IEC 25010:2023", "ISO/IEC 25010 缺年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO 26550:2015", "ISO/IEC 26550:2015", "ISO 26550:2015 缺 IEC"),
    (r"(?<![A-Za-z0-9\-/.])ISO 26550\b(?!:)", "ISO/IEC 26550:2015", "ISO 26550 简写"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 26550:2025", "ISO/IEC 26550:2015", "ISO/IEC 26550:2025 不存在版本"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 26550\b(?!:)", "ISO/IEC 26550:2015", "ISO/IEC 26550 缺年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO 15288:2023", "ISO/IEC/IEEE 15288:2023", "ISO 15288:2023 缺 IEC/IEEE"),
    (r"(?<![A-Za-z0-9\-/.])ISO 15288\b(?!:)", "ISO/IEC/IEEE 15288:2023", "ISO 15288 简写"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC/IEEE 15288\b(?!:)", "ISO/IEC/IEEE 15288:2023", "ISO/IEC/IEEE 15288 缺年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO 24765\b", "ISO/IEC/IEEE 24765:2017", "ISO 24765 缺 IEC/IEEE/年份"),
    (r"(?<![A-Za-z0-9\-/.])ISO 42020:2019", "ISO/IEC/IEEE 42020:2019", "ISO 42020:2019 缺 IEEE"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 42020:2019", "ISO/IEC/IEEE 42020:2019", "ISO/IEC 42020:2019 缺 IEEE"),
    (r"(?<![A-Za-z0-9\-/.])ISO 42020\b(?!:)", "ISO/IEC/IEEE 42020:2019", "ISO 42020 简写"),
    (r"(?<![A-Za-z0-9\-/.])ISO 42030:2019", "ISO/IEC/IEEE 42030:2019", "ISO 42030:2019 缺 IEEE"),
    (r"(?<![A-Za-z0-9\-/.])ISO/IEC 42030:2019", "ISO/IEC/IEEE 42030:2019", "ISO/IEC 42030:2019 缺 IEEE"),
    (r"(?<![A-Za-z0-9\-/.])ISO 42030\b(?!:)", "ISO/IEC/IEEE 42030:2019", "ISO 42030 简写"),
    (r"(?<![A-Za-z0-9\-/.])ISO 12207:2017", "ISO/IEC/IEEE 12207:2017", "ISO 12207:2017 缺 IEC/IEEE"),
    (r"(?<![A-Za-z0-9\-/.])ISO 12207\b(?!:)", "ISO/IEC/IEEE 12207:2017", "ISO 12207 简写"),
    (r"(?<![A-Za-z0-9\-/.])IEEE 42010\b(?!:)", "ISO/IEC/IEEE 42010:2022", "IEEE 42010 简写"),
    (r"(?<![A-Za-z0-9\-/.])IEEE 42020\b(?!:)", "ISO/IEC/IEEE 42020:2019", "IEEE 42020 简写"),
    (r"(?<![A-Za-z0-9\-/.])IEEE 42030\b(?!:)", "ISO/IEC/IEEE 42030:2019", "IEEE 42030 简写"),
    (r"(?<![A-Za-z0-9\-/.])IEEE 15288\b(?!:)", "ISO/IEC/IEEE 15288:2023", "IEEE 15288 简写"),
    (r"(?<![A-Za-z0-9\-/.])IEEE 12207\b(?!:)", "ISO/IEC/IEEE 12207:2017", "IEEE 12207 简写"),
    (r"(?<![A-Za-z0-9\-/.])IEEE 1517\b(?!:)", "ISO/IEC/IEEE 1517:2010", "IEEE 1517 简写"),
    (r"(?<![A-Za-z0-9\-/.])IEEE Std 1517-2010", "ISO/IEC/IEEE 1517:2010", "IEEE Std 1517-2010 变体"),
    (r"(?<![A-Za-z0-9\-/.])IEEE 1517-2010", "ISO/IEC/IEEE 1517:2010", "IEEE 1517-2010 变体"),
    (r"(?<![A-Za-z0-9\-/.])TOGAF 10\b", "TOGAF Standard 10", "TOGAF 版本简写"),
    (r"(?<![A-Za-z0-9\-/.])ArchiMate 4(?!\.0)", "ArchiMate 4.0", "ArchiMate 版本简写"),
    (r"(?<![A-Za-z0-9\-/.])A2A v1\.0\b", "A2A v1.0.0", "A2A 版本简写"),
]


def apply_safe_fixes(file_path: Path) -> int:
    """对单个文件执行低风险标准名称替换，返回替换次数。"""
    text = file_path.read_text(encoding="utf-8")
    original = text
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
        new_line = line
        for pattern, repl, _ in SAFE_REPLACEMENTS:
            # 仅替换当前行中未在 URL / 链接文本内的命中
            def replacer(m: re.Match) -> str:
                start = m.start()
                if line[max(0, start - 1):start] in "<(":
                    return m.group(0)
                return repl
            new_line, count = re.subn(pattern, replacer, new_line)
            replacements += count
        new_lines.append(new_line)
    if text != "\n".join(new_lines):
        file_path.write_text("\n".join(new_lines), encoding="utf-8")
    return replacements


def main() -> int:
    parser = argparse.ArgumentParser(description="全项目标准名称归一检查器")
    parser.add_argument("--fix-safe", action="store_true", help="对 struct/ 下纯正文非代码块位置执行安全替换")
    args = parser.parse_args()

    alias_map = load_aliases(CANONICAL_NAMES_PATH)
    patterns = build_alias_patterns(alias_map)

    md_files = sorted((PROJECT_ROOT / "struct").rglob("*.md"))
    findings: List[Dict] = []
    fixed_count = 0
    for md_file in md_files:
        if "_ARCHIVE" in md_file.parts or "_HISTORICAL" in md_file.parts:
            continue
        if args.fix_safe:
            fixed_count += apply_safe_fixes(md_file)
        findings.extend(scan_file(md_file, patterns))

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(generate_report(findings), encoding="utf-8")
    print(f"标准名称归一报告已保存: {REPORT_PATH} ({len(findings)} 处建议)")
    if args.fix_safe:
        print(f"已执行安全替换: {fixed_count} 处")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
