#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
勘误规则 lint（errata-lint）

把 reports/authority-alignment-errata.md 的 R1–R9 机器校验规则编码为可回归检查。
单一事实源（SSOT）：struct/99-reference/standards-index/authoritative-sources-v2.md
canonical 字典：struct/99-reference/tools/canonical-names.yaml

检查项与 R 规则映射：
- CHK-INVALID-VERSION  (R2 版本号白名单，硬拦截)          -> exit 1
- CHK-STATUS-CONTRA    (R3 同文件状态矛盾：已发布 vs 草案/否认) -> 高置信 exit 1，窗口内 warn
- CHK-POLLUTION        (F 类 占位符/镜像污染：iteh.ai、66912 等)  -> 非归档 exit 1
- CHK-ONE-URL          (R4 一号一 URL：与基准表 URL 比对)       -> warn（报告型）
- CHK-BASELINE-GAP     (R5 基准完备性：正文高频标准未入基准)    -> warn（报告型）
- CHK-KG               (R6 KG 层静态扫描 invalid 版本实体)      -> exit 1
- CHK-ARCHIVE          (R8 归档隔离：归档区现时性主张)          -> warn（报告型）

R1（canonical 化基础设施）由 canonical-names.yaml + knowledge-extractor.py 承担，本脚本消费之；
R7（可达性降噪）归属 scripts/standard-status-checker.py；R9（跨文件状态一致）已由
scripts/cross-index-check.py v2 实现，本脚本不重复。

用法：
    python scripts/errata-lint.py
    python scripts/errata-lint.py --report reports/errata-lint.md
    python scripts/errata-lint.py --root struct --json reports/errata-lint.json
"""

import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    check: str
    severity: str  # "error" | "warning"
    file: str
    line: int
    message: str


# ---------------------------------------------------------------------------
# 文件收集与豁免
# ---------------------------------------------------------------------------

ARCHIVE_MARKERS = ("_ARCHIVE", "_HISTORICAL_")

# 行级豁免词（参照 cross-index-check.py 的 HISTORICAL_CONTEXT_RE 做法）：
# 勘误/修复/反例/历史叙述中的提及不算违规主张
EXEMPTION_RE = re.compile(
    r"勘误|errata|修复|回滚|反例|历史|演进|曾误|旧版|旧称|取代|替代|清理|原误|误填|"
    r"声称|占位符污染|已修正|更正|已回滚|不再使用|误引|幻觉|不存在",
    re.IGNORECASE,
)


def collect_md_files(root: Path) -> List[Path]:
    skip = {"__pycache__", ".venv", ".git", "node_modules"}
    files = []
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root).as_posix()
        if any(part in skip for part in md.parts):
            continue
        files.append(md)
    return files


def is_archive(path: Path) -> bool:
    return any(m in path.as_posix() for m in ARCHIVE_MARKERS)


# ---------------------------------------------------------------------------
# canonical-names.yaml 加载（invalid_versions → R2 硬拦截）
# ---------------------------------------------------------------------------

CANONICAL_NAMES_DEFAULT = "struct/99-reference/tools/canonical-names.yaml"
BASELINE_DEFAULT = "struct/99-reference/standards-index/authoritative-sources-v2.md"

# 年份版标准提及：ISO/IEC/IEEE 12345:2023 等（与 cross-index-check.py 对齐）
STANDARD_RE = re.compile(
    r"\b(ISO\s*/\s*IEC\s*/\s*IEEE\s+\d+(?:[-/]\d+)*|"
    r"ISO\s*/\s*IEC\s+\d+(?:[-/]\d+)*|"
    r"ISO\s+\d+(?:[-/]\d+)*|"
    r"IEEE\s+\d+(?:[-/]\d+)*|"
    r"IEC\s+\d+(?:[-/]\d+)*)"
    r"(?![\d])"
    r"[\s:：]*[:]?\s*(\d{4})",
    re.IGNORECASE,
)

# x.y 版标准提及（ArchiMate/SLSA/SSDF 等）
XY_STANDARD_RES: List[Tuple[str, re.Pattern]] = [
    ("ARCHIMATE", re.compile(r"\bArchiMate\s+v?(\d+(?:\.\d+){1,2})", re.IGNORECASE)),
    ("SLSA", re.compile(r"\bSLSA\s+v?(\d+(?:\.\d+){1,2})", re.IGNORECASE)),
    ("SSDF", re.compile(r"\bSSDF\s+v?(\d+(?:\.\d+){1,2})", re.IGNORECASE)),
]

# 日期版标准（MCP）
DATE_STANDARD_RES: List[Tuple[str, re.Pattern]] = [
    ("MCP", re.compile(r"\bMCP\s+(\d{4}-\d{2}-\d{2})", re.IGNORECASE)),
]


def _norm_standard_key(std_raw: str) -> str:
    """ISO/IEC/IEEE N / ISO N / IEC N 归一到 'ISO N'（保留 part 号）。"""
    std = re.sub(r"\s+", " ", std_raw.strip().upper())
    std = re.sub(r"\s*/\s*", "/", std)
    m = re.match(r"(?:ISO/IEC/IEEE|ISO/IEC|ISO/IEEE|IEC/IEEE|ISO|IEC|IEEE)\s+(\d+(?:[-/]\d+)*)", std)
    if m:
        return "ISO " + m.group(1)
    return std


def _norm_xy_version(raw: str) -> str:
    parts = raw.split(".")
    return f"{parts[0]}.{parts[1]}" if len(parts) >= 2 else raw


def _mini_yaml_invalid(text: str) -> Dict[str, Set[str]]:
    """无 pyyaml 时兜底：canonical + invalid_versions 两段式解析。"""
    result: Dict[str, Set[str]] = defaultdict(set)
    current: Optional[str] = None
    in_invalid = False
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = re.match(r"^\s*-\s*canonical:\s*\"?([^\"]+)\"?\s*$", line)
        if m:
            current = m.group(1).strip()
            in_invalid = False
            continue
        if current is None:
            continue
        if re.match(r"^\s*invalid_versions:\s*$", line):
            in_invalid = True
            continue
        if re.match(r"^\s*[a-z_]+:\s*", line) and not stripped.startswith("-"):
            in_invalid = False
            continue
        m = re.match(r"^\s*-\s*\"?([^\"]+?)\"?\s*$", line)
        if in_invalid and m:
            result[current].add(m.group(1).strip())
    return result


def load_invalid_versions(path: Path) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """返回 (年份版 invalid: key-> {year}, x.y 版 invalid: NAME -> {x.y})。"""
    year_invalid: Dict[str, Set[str]] = defaultdict(set)
    xy_invalid: Dict[str, Set[str]] = defaultdict(set)
    if not path.exists():
        return year_invalid, xy_invalid
    text = path.read_text(encoding="utf-8")
    entries: List[Tuple[str, List[str]]] = []
    if yaml is not None:
        try:
            data = yaml.safe_load(text)
            for e in (data or {}).get("standards", []) or []:
                if isinstance(e, dict) and e.get("canonical"):
                    entries.append((str(e["canonical"]).strip(),
                                    [str(v).strip() for v in (e.get("invalid_versions") or [])]))
        except Exception:
            entries = []
    if not entries:
        for canonical, invalids in _mini_yaml_invalid(text).items():
            entries.append((canonical, sorted(invalids)))

    for canonical, invalids in entries:
        if not invalids:
            continue
        m_std = re.match(
            r"(ISO\s*/\s*IEC\s*/\s*IEEE\s+\d+(?:[-/]\d+)*|ISO\s*/\s*IEC\s+\d+(?:[-/]\d+)*|"
            r"ISO\s+\d+(?:[-/]\d+)*|IEEE\s+\d+(?:[-/]\d+)*|IEC\s+\d+(?:[-/]\d+)*)",
            canonical, re.IGNORECASE,
        )
        if m_std:
            key = _norm_standard_key(m_std.group(1))
            for v in invalids:
                if re.fullmatch(r"\d{4}", v):
                    year_invalid[key].add(v)
            continue
        upper = canonical.upper()
        for name, _p in XY_STANDARD_RES:
            if re.search(rf"\b{name}\b", upper):
                for v in invalids:
                    xy_invalid[name].add(_norm_xy_version(v))
                break
    return year_invalid, xy_invalid


# ---------------------------------------------------------------------------
# CHK-INVALID-VERSION（R2）
# ---------------------------------------------------------------------------

def check_invalid_versions(root: Path, year_invalid: Dict[str, Set[str]],
                           xy_invalid: Dict[str, Set[str]]) -> List[Finding]:
    findings: List[Finding] = []
    for md in collect_md_files(root):
        if is_archive(md):
            continue  # 归档区由 CHK-ARCHIVE 处理
        rel = md.relative_to(root).as_posix()
        text = md.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            if EXEMPTION_RE.search(line):
                continue
            for m in STANDARD_RE.finditer(line):
                key = _norm_standard_key(m.group(1))
                if m.group(2) in year_invalid.get(key, set()):
                    findings.append(Finding(
                        "CHK-INVALID-VERSION", "error", rel, lineno,
                        f"引用基准判定不存在的版本 {key}:{m.group(2)}"
                        f"（canonical-names.yaml invalid_versions，R2 硬拦截）"))
            for name, pattern in XY_STANDARD_RES:
                for m in pattern.finditer(line):
                    ver = _norm_xy_version(m.group(1))
                    if ver in xy_invalid.get(name, set()):
                        findings.append(Finding(
                            "CHK-INVALID-VERSION", "error", rel, lineno,
                            f"引用基准判定不存在的版本 {name} {ver}"
                            f"（canonical-names.yaml invalid_versions，R2 硬拦截）"))
    return findings


# ---------------------------------------------------------------------------
# CHK-STATUS-CONTRA（R3：同文件状态矛盾）
# ---------------------------------------------------------------------------

# 强"已发布/现行"主张（排除"预计/尚未"等否定后缀）
FINAL_STRONG_RE = re.compile(
    r"已正式发布(?!前)|已发布(?!\s*[（(]?\s*(?:预计|前))|正式版(?!本?预计)|"
    r"现行(?!.*草案)|当前有效",
    re.IGNORECASE,
)
# 强"非最终"主张
NONFINAL_STRONG_RE = re.compile(
    r"尚未[^。；\n]{0,12}正式|仍是?\s*(?:Initial Public Draft|IPD|草案|Draft|CDV|DIS)|"
    r"Initial Public Draft|征求意见稿|制定中|草案阶段|预计\s*20\d\d[^。；\n]{0,6}发布|"
    r"非正式(?:版本|发布)",
    re.IGNORECASE,
)
# 否认存在主张
DENIAL_RE = re.compile(
    r"并非官方|否认|假设的未来|未发布|不是正式",
    re.IGNORECASE,
)
# "存在/真实"主张（与否认配对）
EXIST_RE = re.compile(r"真实存在|已发布|正式发布", re.IGNORECASE)

CONTRA_WINDOW = 15  # ±15 行窗口
CONTRA_HARD_WINDOW = 2  # 同行或相邻行直接矛盾 → 高置信 error

# SSOT 与勘误/索引类文件自身不参与矛盾判定（它们天然并列多状态）
CONTRA_EXCLUDE_FILES = (
    "standards-index/authoritative-sources-v2.md",
    "tools/canonical-names.yaml",
    "CHANGELOG.md",
)
# 状态跟踪报表（frontier/tracker）以“预期 vs 实际”并列多状态为常态，豁免
CONTRA_EXCLUDE_PATH_PARTS = ("frontier-tracking/", "standard-tracker")


def _line_standard_mentions(line: str) -> List[Tuple[str, str, int]]:
    """返回行内 (std_key, version, start_pos) 列表；version 可能为 ''。"""
    out: List[Tuple[str, str, int]] = []
    for m in STANDARD_RE.finditer(line):
        out.append((_norm_standard_key(m.group(1)), m.group(2), m.start()))
    for name, pattern in XY_STANDARD_RES:
        for m in pattern.finditer(line):
            out.append((name, _norm_xy_version(m.group(1)), m.start()))
    for name, pattern in DATE_STANDARD_RES:
        for m in pattern.finditer(line):
            out.append((name, m.group(1), m.start()))
    return out


def _nearest_mention(mentions: List[Tuple[str, str, int]], pos: int) -> Tuple[str, str]:
    """把状态词归属到行内最近的标准提及（避免多标准行交叉污染）。"""
    best = min(mentions, key=lambda t: abs(t[2] - pos))
    return best[0], best[1]


# 状态词否定前缀守卫：这些前缀后的“正式版/已发布”不是现行主张
NEGATION_PREFIX_RE = re.compile(r"(?:尚未|未转|未|不是|非|是否|能否|待|转为|进入)$")


def _is_negated(line: str, pos: int) -> bool:
    """状态词前 12 字符内含否定语境（如“尚未转为正式版”“是否进入正式版”）。"""
    prefix = line[max(0, pos - 12):pos]
    return bool(NEGATION_PREFIX_RE.search(prefix))


def check_status_contradiction(root: Path) -> List[Finding]:
    """同一文件内同一 (标准, 版本) 在 ±15 行内同时出现"已发布"与"草案/否认"主张。"""
    findings: List[Finding] = []
    for md in collect_md_files(root):
        if is_archive(md):
            continue
        rel = md.relative_to(root).as_posix()
        if any(rel.endswith(ex) or ex in rel for ex in CONTRA_EXCLUDE_FILES):
            continue
        if any(p in rel for p in CONTRA_EXCLUDE_PATH_PARTS):
            continue
        lines = md.read_text(encoding="utf-8").splitlines()
        # per (std, version): {"final": [(line, txt)], "nonfinal": [...], "denial": [...], "exist": [...]}
        claims: Dict[Tuple[str, str], Dict[str, List[Tuple[int, str]]]] = defaultdict(
            lambda: defaultdict(list))
        for i, line in enumerate(lines, start=1):
            if EXEMPTION_RE.search(line):
                continue
            mentions = _line_standard_mentions(line)
            if not mentions:
                continue
            for kind, regex in (("final", FINAL_STRONG_RE),
                                ("nonfinal", NONFINAL_STRONG_RE),
                                ("denial", DENIAL_RE),
                                ("exist", EXIST_RE)):
                for m in regex.finditer(line):
                    if kind in ("final", "exist") and _is_negated(line, m.start()):
                        continue
                    std, ver = _nearest_mention(mentions, m.start())
                    claims[(std, ver)][kind].append((i, line.strip()))
        for (std, ver), sides in claims.items():
            pairs: List[Tuple[str, str]] = [("final", "nonfinal"),
                                            ("final", "denial"),
                                            ("exist", "denial")]
            for a, b in pairs:
                for la, ta in sides.get(a, []):
                    for lb, tb in sides.get(b, []):
                        gap = abs(la - lb)
                        if gap > CONTRA_WINDOW or gap == 0:
                            # 同行并列多为合法状态描述（如"RC 已发布（2026-05-29）"、
                            # "现行 1.1，1.2 仍为 IPD"），矛盾须跨行才算
                            continue
                        label = f"{std}:{ver}" if ver else std
                        sev = "error" if gap <= CONTRA_HARD_WINDOW else "warning"
                        findings.append(Finding(
                            "CHK-STATUS-CONTRA", sev, rel, la,
                            f"同文件状态矛盾（{label}）：L{la}『{a}』vs L{lb}『{b}』"
                            f"（相距 {gap} 行，R3）| A: {ta[:60]} | B: {tb[:60]}"))
    # 去重（同一对行可能因多标准重复）
    seen = set()
    uniq: List[Finding] = []
    for f in findings:
        k = (f.file, f.line, f.message[:80])
        if k not in seen:
            seen.add(k)
            uniq.append(f)
    return uniq


# ---------------------------------------------------------------------------
# CHK-POLLUTION（F 类：占位符/镜像污染）
# ---------------------------------------------------------------------------

POLLUTION_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"iteh\.ai", re.IGNORECASE),
     "iteh.ai 盗版镜像域名污染"),
    (re.compile(r"webstore\.iec\.ch/(?:en/)?publication/66912\b"),
     "IEC webstore 66912 占位符污染（历史教训：该页非所引标准，见 fix-66912.py）"),
    (re.compile(r"(?<![\w/-])X{3,}(?![\w-])"),
     "XXX 占位符残留"),
    (re.compile(r"PLACEHOLDER"),
     "PLACEHOLDER 占位符标记残留"),
    (re.compile(r"iso\.org/standard/0{4,}\.html"),
     "伪造 ISO 标准编号 URL（全 0）"),
]
# XXX 豁免：CVE/GHSA 编号掩码（CVE-202X-XXXXX）属合规匿名化
POLLUTION_XXX_ALLOW_RE = re.compile(r"CVE|GHSA")
# 66912 唯一合法语境：同行明确指向 IEC 62443-4-1（该页真实归属）
POLLUTION_66912_ALLOW_RE = re.compile(r"62443-4-1")


def check_pollution(root: Path) -> List[Finding]:
    findings: List[Finding] = []
    for md in collect_md_files(root):
        rel = md.relative_to(root).as_posix()
        archived = is_archive(md)
        # 模板目录天然含占位符（如 ISO/IEC XXXXX），豁免
        if "/templates/" in md.as_posix():
            continue
        for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), start=1):
            if EXEMPTION_RE.search(line):
                continue
            for pattern, msg in POLLUTION_PATTERNS:
                if not pattern.search(line):
                    continue
                if "66912" in msg and POLLUTION_66912_ALLOW_RE.search(line):
                    continue
                if "XXX" in msg and POLLUTION_XXX_ALLOW_RE.search(line):
                    continue
                sev = "warning" if archived else "error"
                findings.append(Finding("CHK-POLLUTION", sev, rel, lineno, msg))
    return findings


# ---------------------------------------------------------------------------
# CHK-ONE-URL（R4：一号一 URL，与基准表比对）
# ---------------------------------------------------------------------------

BASE_ROW_RE = re.compile(r"^\|(.+)\|$")
ISO_URL_RE = re.compile(r"iso\.org/standard/(\d+)\.html")

# A2A 已知错误 URL（基准：https://a2a-protocol.org/latest/，见 errata C5）
A2A_BAD_URL_RE = re.compile(
    r"https?://(?:a2aprotocol\.(?:org|ai)|google\.github\.io/A2A)", re.IGNORECASE)


def load_baseline_urls(path: Path) -> Dict[str, str]:
    """解析基准表：'ISO 12207' -> '90219'（仅取官方 URL 列首个 iso.org 链接）。

    仅收录标准号不含 part 后缀歧义的行；part 行（如 21838）按裸号登记，
    正文带 part 的提及不参与 URL 比对（不同 part 可有不同 URL）。
    """
    urls: Dict[str, str] = {}
    if not path.exists():
        return urls
    for line in path.read_text(encoding="utf-8").splitlines():
        if not BASE_ROW_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or cells[0].startswith("-") or "标准" in cells[0]:
            continue
        name_cell = re.sub(r"\*+", "", cells[0])
        m_std = re.match(
            r"(ISO\s*/\s*IEC\s*/\s*IEEE|ISO\s*/\s*IEC|ISO|IEC|IEEE)\s+"
            r"(?:AWI\s+|DIS\s+|CD\s+)?(\d+(?:[-/]\d+)*)",
            name_cell, re.IGNORECASE,
        )
        if not m_std:
            continue
        key = _norm_standard_key(m_std.group(1) + " " + m_std.group(2))
        m_url = ISO_URL_RE.search(cells[3])
        if m_url:
            # AWI/DIS/CD 等工作项行（如 AWI 42030 = 93814）与正式版同号不同 URL，
            # 不作为该号的基准 URL（保留先登记的正式版行）
            if re.search(r"\b(AWI|DIS|CD|WD|FDIS)\b", name_cell):
                continue
            urls.setdefault(key, m_url.group(1))
    return urls


# URL 归属用的无年份标签提及（如表格中的 “ISO 26550: <url>”）
STD_LABEL_RE = re.compile(
    r"\b(ISO\s*/\s*IEC\s*/\s*IEEE\s+\d+(?:[-/]\d+)*|ISO\s*/\s*IEC\s+\d+(?:[-/]\d+)*|"
    r"ISO\s+\d+(?:[-/]\d+)*|IEC\s+\d+(?:[-/]\d+)*|IEEE\s+\d+(?:[-/]\d+)*)\s*[:：]",
    re.IGNORECASE,
)


def check_one_url(root: Path, baseline_urls: Dict[str, str]) -> List[Finding]:
    findings: List[Finding] = []
    # per exact key（含 part）：全项目出现的 iso.org standard id 集合（多 URL 发现）
    seen_urls: Dict[str, Dict[str, List[Tuple[str, int]]]] = defaultdict(lambda: defaultdict(list))
    for md in collect_md_files(root):
        if is_archive(md):
            continue
        rel = md.relative_to(root).as_posix()
        for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), start=1):
            if EXEMPTION_RE.search(line):
                continue
            # 行内标准提及（带年份 + 无年份标签），用于 URL 就近归属
            mentions: List[Tuple[str, int]] = []
            for m in STANDARD_RE.finditer(line):
                mentions.append((_norm_standard_key(m.group(1)), m.start()))
            for m in STD_LABEL_RE.finditer(line):
                mentions.append((_norm_standard_key(m.group(1)), m.start()))
            # 基准比对：URL 归属到行内最近的标准提及
            for um in ISO_URL_RE.finditer(line):
                if not mentions:
                    continue
                key = min(mentions, key=lambda t: abs(t[1] - um.start()))[0]
                seen_urls[key][um.group(1)].append((rel, lineno))
                base = baseline_urls.get(key)
                # 带 part 的提及（key 含 '-'）且基准只登记裸号 → 不比对
                if base and "-" not in key.split(" ", 1)[1] and um.group(1) != base:
                    findings.append(Finding(
                        "CHK-ONE-URL", "warning", rel, lineno,
                        f"{key} 的 URL iso.org/standard/{um.group(1)} 与基准 "
                        f"{base} 不一致（R4 一号一 URL）"))
            # A2A 错误域名（基准 a2a-protocol.org/latest/）
            if A2A_BAD_URL_RE.search(line) and re.search(r"\bA2A\b", line):
                findings.append(Finding(
                    "CHK-ONE-URL", "warning", rel, lineno,
                    "A2A URL 非基准 https://a2a-protocol.org/latest/（R4，errata C5）"))
    # 多 URL 发现（同一 key 出现 ≥2 个不同 iso.org id，且未命中基准比对）
    for key, url_map in sorted(seen_urls.items()):
        if len(url_map) < 2:
            continue
        if "-" in key.split(" ", 1)[1]:
            continue  # part 级多 URL 合法
        if key in baseline_urls:
            continue  # 基准已收录的号由逐行比对负责（AWI/正式版双 URL 合法）
        base = baseline_urls.get(key)
        locs = {u: ls[0] for u, ls in url_map.items()}
        findings.append(Finding(
            "CHK-ONE-URL", "warning", locs[sorted(locs)[0]][0], locs[sorted(locs)[0]][1],
            f"{key} 全项目出现多个 iso.org URL: "
            + ", ".join(f"{u}（{ls[0][0]}:{ls[0][1]} 等 {len(ls)} 处）"
                        for u, ls in sorted(url_map.items()))
            + (f"；基准={base}" if base else "；基准未收录")))
    return findings


# ---------------------------------------------------------------------------
# CHK-BASELINE-GAP（R5：基准完备性，报告型）
# ---------------------------------------------------------------------------

def check_baseline_gap(root: Path, baseline_path: Path,
                       min_mentions: int = 3, cap: int = 30) -> List[Finding]:
    """正文出现 ≥min_mentions 次但基准表未收录的标准号 → WARNING（待补录）。"""
    base_numbers: Set[str] = set()
    if baseline_path.exists():
        for line in baseline_path.read_text(encoding="utf-8").splitlines():
            for m in re.finditer(
                    r"(?:ISO\s*/\s*IEC\s*/\s*IEEE|ISO\s*/\s*IEC|ISO|IEC|IEEE)\s+"
                    r"(?:AWI\s+|DIS\s+|CD\s+|TS\s+|TR\s+)?(\d+(?:[-/]\d+)*)",
                    line, re.IGNORECASE):
                base_numbers.add(_norm_standard_key("ISO " + m.group(1)))
                # 同时登记裸号（21838-1 → 21838）
                bare = m.group(1).split("-")[0].split("/")[0]
                base_numbers.add("ISO " + bare)

    counter: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
    for md in collect_md_files(root):
        if is_archive(md):
            continue
        rel = md.relative_to(root).as_posix()
        for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), start=1):
            for m in re.finditer(
                    r"\b(ISO\s*/\s*IEC\s*/\s*IEEE\s+\d+|ISO\s*/\s*IEC\s+\d+|"
                    r"ISO\s+\d+|IEC\s+\d+|IEEE\s+\d+)",
                    line, re.IGNORECASE):
                key = _norm_standard_key(m.group(1))
                bare = "ISO " + key.split(" ", 1)[1].split("-")[0].split("/")[0]
                if key in base_numbers or bare in base_numbers:
                    continue
                counter[key].append((rel, lineno))

    findings: List[Finding] = []
    for key, locs in sorted(counter.items(), key=lambda kv: -len(kv[1])):
        if len(locs) < min_mentions:
            continue
        f0, l0 = locs[0]
        findings.append(Finding(
            "CHK-BASELINE-GAP", "warning", f0, l0,
            f"标准 {key} 在正文出现 {len(locs)} 次但基准表未收录"
            f"（R5 基准完备性，待补录；首见 {f0}:{l0}）"))
        if len(findings) >= cap:
            break
    return findings


# ---------------------------------------------------------------------------
# CHK-KG（R6：KG 层静态扫描）
# ---------------------------------------------------------------------------

KG_BAD_LABEL_RES: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"25010[:_]2024|25010:2025", re.IGNORECASE),
     "KG 含不存在的 ISO/IEC 25010:2024/2025 实体（errata A1）"),
    (re.compile(r"ArchiMate[\s_-]4\.[1-9]", re.IGNORECASE),
     "KG 含不存在的 ArchiMate 4.x(>4.0) 实体（errata A2）"),
    (re.compile(r"62443-4-2[_:]2025", re.IGNORECASE),
     "KG 含错年 IEC 62443-4-2:2025 实体（errata A3）"),
    (re.compile(r"26550[:_]2023|26550[:_]2025", re.IGNORECASE),
     "KG 含不存在的 ISO/IEC 26550:2023/2025 实体（errata A4）"),
]


def check_kg(project_root: Path) -> List[Finding]:
    findings: List[Finding] = []
    kg_dir = project_root / "struct/99-reference/knowledge-graph"
    for name in ("kg.ttl", "kg-entities.jsonl"):
        f = kg_dir / name
        if not f.exists():
            continue
        rel = f.relative_to(project_root).as_posix()
        for lineno, line in enumerate(f.read_text(encoding="utf-8").splitlines(), start=1):
            for pattern, msg in KG_BAD_LABEL_RES:
                if pattern.search(line):
                    findings.append(Finding("CHK-KG", "error", rel, lineno, msg))
    return findings


# ---------------------------------------------------------------------------
# CHK-ARCHIVE（R8：归档隔离，报告型）
# ---------------------------------------------------------------------------

CURRENCY_CLAIM_RE = re.compile(
    r"现行|最新版本|最新正式版|当前版本|当前有效|已发布|正式版",
    re.IGNORECASE,
)
ARCHIVE_REF_RE = re.compile(r"_ARCHIVE")


def check_archive(root: Path, project_root: Path) -> List[Finding]:
    findings: List[Finding] = []
    # 1) 归档区文件内的现时性主张 → 提醒标注（归档本为历史快照，报告型）
    for md in collect_md_files(root):
        if not is_archive(md):
            continue
        rel = md.relative_to(root).as_posix()
        for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), start=1):
            if not CURRENCY_CLAIM_RE.search(line):
                continue
            # 归档区自身的说明性文字（README/横幅/元注释）豁免
            if md.name == "README.md" or EXEMPTION_RE.search(line):
                continue
            findings.append(Finding(
                "CHK-ARCHIVE", "warning", rel, lineno,
                "归档区文件含现时性主张（现行/最新/已发布），"
                "建议在文件头加“已被 struct/ 现行状态取代”横幅（R8 归档隔离）"))
    # 2) 非归档正文引用归档路径作为状态依据 → 提醒
    for md in collect_md_files(root):
        if is_archive(md):
            continue
        rel = md.relative_to(root).as_posix()
        for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), start=1):
            if ARCHIVE_REF_RE.search(line) and not EXEMPTION_RE.search(line):
                findings.append(Finding(
                    "CHK-ARCHIVE", "warning", rel, lineno,
                    "正文引用 _ARCHIVE 归档路径，不得作为标准状态依据（R8）"))
    return findings


# ---------------------------------------------------------------------------
# 报告输出
# ---------------------------------------------------------------------------

R_RULE_STATUS = [
    ("R1", "标准号 canonical 化", "基础设施已存在",
     "canonical-names.yaml + knowledge-extractor.py 承担归一；本脚本消费该字典（CHK-INVALID-VERSION）"),
    ("R2", "版本号白名单硬拦截", "已实现",
     "CHK-INVALID-VERSION：invalid_versions 命中且非豁免语境 → error/exit 1"),
    ("R3", "未来/草案强制标识（禁把 IPD/RC 写成已发布）", "部分实现",
     "CHK-STATUS-CONTRA：同文件 ±15 行状态矛盾检测；'首次出现必须带标识'的强制性需理解引用意图，不可静态判定，未编码"),
    ("R4", "一号一 URL", "已实现（报告型）",
     "CHK-ONE-URL：与基准表 URL 比对 + 全项目多 URL 发现 + A2A 错误域名；URL 语义需人工确认故为 warning"),
    ("R5", "基准完备性门禁", "已实现（报告型）",
     "CHK-BASELINE-GAP：正文 ≥3 次出现的标准未入基准 → warning（待补录）"),
    ("R6", "KG/SHACL 真约束", "部分实现",
     "CHK-KG：对 kg.ttl/kg-entities.jsonl 做已知坏实体静态扫描（exit 1）；SHACL shape 级约束归属 scripts/kg-shacl-validate.py"),
    ("R7", "可达性降噪", "不可编码（本脚本范围外）",
     "属运行时网络检查，归属 scripts/standard-status-checker.py（iso.org 403 归入'反爬受限'类）"),
    ("R8", "归档隔离 lint", "已实现（报告型）",
     "CHK-ARCHIVE：归档区现时性主张 + 正文引用归档路径 → warning"),
    ("R9", "跨文件状态一致", "已由他处实现",
     "scripts/cross-index-check.py v2 已实现跨文件版本聚合 + invalid 硬错误；本脚本不重复"),
]


def write_report(path: Path, findings: List[Finding], scanned: int):
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    lines = [
        "# 勘误规则 Lint 报告（errata-lint）",
        "",
        "> 规则来源：`reports/authority-alignment-errata.md` R1–R9",
        "> 单一事实源：`struct/99-reference/standards-index/authoritative-sources-v2.md`",
        "> canonical 字典：`struct/99-reference/tools/canonical-names.yaml`",
        "",
        f"- 扫描文件：{scanned} 个 Markdown（struct/，含归档区分别定级）",
        f"- **error {len(errors)} 条**（触发 exit 1）｜warning {len(warnings)} 条（报告型）",
        "",
        "## R1–R9 编码状态",
        "",
        "| 规则 | 内容 | 编码状态 | 说明 |",
        "|------|------|----------|------|",
    ]
    for rid, name, status, note in R_RULE_STATUS:
        lines.append(f"| **{rid}** | {name} | {status} | {note} |")
    lines.append("")

    by_check: Dict[str, List[Finding]] = defaultdict(list)
    for f in findings:
        by_check[f.check].append(f)
    for check in ("CHK-INVALID-VERSION", "CHK-STATUS-CONTRA", "CHK-POLLUTION",
                  "CHK-ONE-URL", "CHK-BASELINE-GAP", "CHK-KG", "CHK-ARCHIVE"):
        items = by_check.get(check, [])
        lines.append(f"## {check}（{len(items)} 条）")
        lines.append("")
        if not items:
            lines.append("- 未发现问题")
            lines.append("")
            continue
        for f in items[:100]:
            icon = "🔴" if f.severity == "error" else "🟡"
            lines.append(f"- {icon} `{f.file}` 第 {f.line} 行：{f.message}")
        if len(items) > 100:
            lines.append(f"- ... 还有 {len(items) - 100} 条")
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="勘误规则 R1–R9 机器校验（errata-lint）")
    parser.add_argument("--root", default="struct", help="文档根目录（默认 struct/）")
    parser.add_argument("--canonical-names", default=CANONICAL_NAMES_DEFAULT,
                        help="canonical 字典路径")
    parser.add_argument("--baseline", default=BASELINE_DEFAULT, help="基准表路径")
    parser.add_argument("--report", default="reports/errata-lint.md", help="Markdown 报告输出")
    parser.add_argument("--json", metavar="PATH", help="JSON 报告输出（可选）")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    root = (project_root / args.root).resolve()
    if not root.exists():
        print(f"错误：根目录不存在 {root}", file=sys.stderr)
        sys.exit(1)

    year_invalid, xy_invalid = load_invalid_versions((project_root / args.canonical_names).resolve())
    baseline_urls = load_baseline_urls((project_root / args.baseline).resolve())

    findings: List[Finding] = []
    findings += check_invalid_versions(root, year_invalid, xy_invalid)
    findings += check_status_contradiction(root)
    findings += check_pollution(root)
    findings += check_one_url(root, baseline_urls)
    findings += check_baseline_gap(root, (project_root / args.baseline).resolve())
    findings += check_kg(project_root)
    findings += check_archive(root, project_root)

    scanned = len(collect_md_files(root))
    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]

    print(f"扫描文件: {scanned} 个（{root}）")
    print(f"invalid 版本白名单: {sum(len(v) for v in year_invalid.values())} 个年份版 + "
          f"{sum(len(v) for v in xy_invalid.values())} 个 x.y 版")
    print(f"基准 URL 条目: {len(baseline_urls)} 个")
    for check in ("CHK-INVALID-VERSION", "CHK-STATUS-CONTRA", "CHK-POLLUTION",
                  "CHK-ONE-URL", "CHK-BASELINE-GAP", "CHK-KG", "CHK-ARCHIVE"):
        n_e = sum(1 for f in findings if f.check == check and f.severity == "error")
        n_w = sum(1 for f in findings if f.check == check and f.severity == "warning")
        print(f"  {check}: error {n_e} / warning {n_w}")
    print(f"合计: error {len(errors)} / warning {len(warnings)}")

    if errors:
        print("\n硬错误（触发 exit 1）:")
        for f in errors[:20]:
            print(f"  🔴 {f.file}:{f.line} [{f.check}] {f.message[:100]}")

    if args.report:
        write_report(Path(args.report), findings, scanned)
        print(f"\nMarkdown 报告已保存: {args.report}")
    if args.json:
        data = [
            {"check": f.check, "severity": f.severity, "file": f.file,
             "line": f.line, "message": f.message}
            for f in findings
        ]
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"JSON 报告已保存: {args.json}")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
