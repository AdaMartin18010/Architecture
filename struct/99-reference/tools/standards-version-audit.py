#!/usr/bin/env python3
"""
standards-version-audit.py
扫描项目 Markdown 文件中的标准编号/版本/状态引用，输出潜在不一致报告。

用法:
    python standards-version-audit.py [project_root]

输出:
    在 stdout 输出不一致项；可重定向到文件。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

# 权威基准：标准名称 -> (期望版本, 期望状态描述, 备注)
# 注意：这里使用小写的标准名作为键，便于匹配。
AUTHORITATIVE_BASELINE = {
    "iso/iec 25010": ("2023", "已发布", "不存在 2024 版"),
    "iso/iec 25040": ("2024", "已发布", ""),
    "iso/iec/ieee 42010": ("2022", "已发布", ""),
    "iso/iec/ieee 42020": ("2019", "现行", "计划修订"),
    "iso/iec/ieee 42030": ("2019", "现行", "AWI 修订中"),
    "iso/iec/ieee 12207": ("2026", "已发布", "2026-04-29 发布，取代 2017 版"),
    "iso/iec/ieee 15288": ("2023", "已发布", ""),
    "iso/iec 26550": ("2015", "现行", "不存在 2025 版"),
    "iso/iec 26566": ("2026", "已发布", ""),
    "iso/iec 30141": ("2024", "已发布", "2024-08 发布，取代 2018 版"),
    "iso/iec 5338": ("2023", "已发布", ""),
    "iso/iec 42001": ("2023", "已发布", ""),
    "archimate": ("4.0", "已发布", "2026-04-27 正式发布；3.2 仍有效"),
    "nist sp 800-218": ("1.2", "Initial Public Draft", "2025-12-17 征求意见稿；非最终版"),
    "ssdf": ("1.2", "Initial Public Draft", "2025-12-17 征求意见稿；非最终版"),
    "slsa": ("1.2", "已发布", "Build/Source Track 已发布；Build Environment Track / L4 仍在开发"),
    "iec 62443-4-2": ("2019", "现行", "不是 2025 版"),
    "iec ts 62443-6-2": ("2025", "已发布", "评估方法论"),
    "iec 61508": ("Ed.2 (2010)", "现行", "Ed.3 开发中"),
    "iso 26262": ("2018", "现行", "Ed.3 开发中"),
    "mcp": ("2025-11-25", "现行稳定版", "已捐给 Linux Foundation Agentic AI Foundation"),
    "a2a": ("v1.0.0", "已发布", ""),
    "wasi": ("0.3 Preview", "提案/预览", "非 1.0"),
    "bpmn": ("2.0", "现行", ""),
    "dmn": ("1.5", "2024 发布", ""),
    "omg ras": ("v2.2", "已发布", ""),
}

# 编译正则：匹配 "标准名 :版本" 或 "标准名:版本"
# 同时捕获一些常见状态词
PATTERN_STANDARD = re.compile(
    r"(?i)(iso[/\\]?iec[/\\]?(?:/ieee)?\s*\d{5}(?:[-:]\d+)?|"
    r"iso\s*\d{5}(?:[-:]\d+)?|"
    r"iec\s*(?:ts\s*)?\d{5}(?:[-:]\d+)?|"
    r"archimate|togaf|"
    r"nist\s*(?:sp\s*)?800[-:]?218|"
    r"ssdf|slsa|mcp|a2a|wasi|bpmn|dmn|omg\s*ras|fair4rs|swebok)"
    r"\s*[:：]\s*([^\s，,；;()（）\[\]\n]+)"
)

# 版本号应看起来像年份、Ed.、vX.Y 或 Preview；排除条款号（如 7.4.10）
VALID_VERSION_PATTERN = re.compile(r"^(\d{4}|v?\d+\.\d+|Ed\.\d+|Preview|preview|draft)", re.I)
# 条款号通常形如 X.Y.Z 或 X.Y，且 X 为个位数；单独排除
CLAUSE_NUMBER_PATTERN = re.compile(r"^\d\.\d+(\.\d+)?$")

# 历史/警告上下文：出现这些短语时，通常是在说明旧版、纠正错误或历史对照，应降低误报
HISTORICAL_CONTEXT_PATTERNS = [
    re.compile(r"不存在\s*[\"']?"),
    re.compile(r"误[写标用引].*?"),
    re.compile(r"勘误|误报|纠正|撤回|回退"),
    re.compile(r"历史(?:对照|基准|版本|记录)|前一版本|旧版|初始版本|第一版|演进|时间线|timeline|版本史"),
    re.compile(r"取代|replaced?\s+by|replaces"),
    re.compile(r"原表述|旧引用|旧版本|更新为|改为"),
    re.compile(r"草案|draft"),
    re.compile(r"⚠️|警告|注意|说明"),
    re.compile(r"~~.*?~~"),  # 删除线常用于保留历史记录
    re.compile(r"\d{4}\s*[–~—-]\s*\d{4}"),  # 年份区间，如 2005–2024
    re.compile(r"\d{4}\s*[:：]\s*ISO/IEC"),  # 时间线条目，如 2011: ISO/IEC...
    re.compile(r"[├└]──"),  # 树状时间线/版本演进标记
]


def expected_versions_match(version: str, expected: str) -> bool:
    """判断 found_version 是否与 expected_version 匹配。

    支持：
    - 前缀匹配 / 包含匹配
    - 从 expected 中提取年份（如 "Ed.2 (2010)" -> "2010"）进行匹配
    """
    if version.startswith(expected) or expected in version:
        return True
    # 尝试从 expected 中提取括号内的年份
    m = re.search(r"\((\d{4})\)", expected)
    if m and version.startswith(m.group(1)):
        return True
    return False

PATTERN_STATUS = re.compile(
    r"(?i)(已发布|正式发布|正式版|现行|draft|initial public draft|ipd|"
    r"征求意见稿|制定中|开发中|预览|preview|rc|已撤销|withdrawn|已废止)"
)


@dataclass
class Finding:
    file: Path
    line: int
    standard: str
    found_version: str
    expected_version: str
    expected_status: str
    note: str
    snippet: str


def normalize_standard_name(name: str) -> str:
    """将各种写法归一化为小写、无多余空格的关键字。"""
    n = name.lower().strip()
    n = re.sub(r"[\\/]", "/", n)
    n = re.sub(r"\s+", " ", n)
    n = re.sub(r"^(?:the\s+)?open\s+group\s+", "", n)
    return n


def find_baseline_key(normalized: str) -> str | None:
    """根据归一化名称找到基准字典中的键。"""
    for key in AUTHORITATIVE_BASELINE:
        if key in normalized or normalized in key:
            return key
    # 特殊处理：nist sp 800-218 / ssdf 互认
    if "800-218" in normalized or "ssdf" in normalized:
        return "ssdf"
    if "archimate" in normalized:
        return "archimate"
    return None


def scan_file(path: Path, project_root: Path) -> List[Finding]:
    findings: List[Finding] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"WARN: 无法读取 {path}: {e}", file=sys.stderr)
        return findings

    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in PATTERN_STANDARD.finditer(line):
            raw_name = match.group(1)
            version = match.group(2).strip()
            normalized = normalize_standard_name(raw_name)
            key = find_baseline_key(normalized)
            if not key:
                continue
            expected_version, expected_status, note = AUTHORITATIVE_BASELINE[key]
            # 简单判断：如果 found_version 与 expected_version 不同，则记录
            # 对于像 "2023-11" 这种，允许前缀匹配
            if not expected_versions_match(version, expected_version):
                # 排除一些明显不是版本号的匹配（如 URL 片段、条款号）
                if not VALID_VERSION_PATTERN.match(version):
                    continue
                if CLAUSE_NUMBER_PATTERN.match(version):
                    continue
                # 排除历史/警告上下文
                if any(p.search(line) for p in HISTORICAL_CONTEXT_PATTERNS):
                    continue
                snippet = line.strip()
                if len(snippet) > 120:
                    snippet = snippet[:120] + "..."
                findings.append(
                    Finding(
                        file=path.relative_to(project_root),
                        line=lineno,
                        standard=key.upper(),
                        found_version=version,
                        expected_version=expected_version,
                        expected_status=expected_status,
                        note=note,
                        snippet=snippet,
                    )
                )
    return findings


def main() -> int:
    project_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not project_root.is_dir():
        print(f"ERROR: {project_root} 不是目录", file=sys.stderr)
        return 1

    md_files = list(project_root.rglob("*.md"))
    # 排除 .venv、node_modules 等
    md_files = [
        p for p in md_files
        if ".venv" not in p.parts and "node_modules" not in p.parts
    ]

    all_findings: List[Finding] = []
    for p in md_files:
        all_findings.extend(scan_file(p, project_root))

    if not all_findings:
        print("✅ 未发现明显的标准版本不一致。")
        return 0

    print(f"⚠️  发现 {len(all_findings)} 处潜在标准版本/状态不一致：\n")
    # 按标准分组
    from collections import defaultdict
    grouped: dict[str, List[Finding]] = defaultdict(list)
    for f in all_findings:
        grouped[f.standard].append(f)

    for std in sorted(grouped):
        items = grouped[std]
        print(f"## {std}")
        print(f"期望版本/状态: {items[0].expected_version} / {items[0].expected_status}")
        if items[0].note:
            print(f"备注: {items[0].note}")
        for f in items:
            print(f"  - {f.file}:{f.line} 发现 `{f.found_version}`")
            print(f"    {f.snippet}")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
