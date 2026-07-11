#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用一致性检查脚本（v2：跨文件语义增强）

检查内容：
1. 公理编号是否被引用但未定义（如 "公理 M.1" 在当前项目中是否有定义）
2. 标准版本是否冲突：
   a. 文件内：同一文件内同一标准出现多个现行版本
   b. 跨文件（v2 新增）：按 canonical 标准名聚合全 struct/ 版本提及，
      同一标准出现多个"现行"（非历史/演进/对比语境）版本时报告；
      已在 canonical-names.yaml 登记的版本线降级为信息项
   c. 硬错误（v2 新增）：非历史语境引用了 canonical-names.yaml
      invalid_versions 明确判为错误的版本号（如 ISO/IEC 25010:2024）
3. x.y 版本号识别（v2 新增）：ArchiMate 3.2/4.0、SLSA 1.0/1.2、TOGAF 9.2/10、
   BPMN 2.0、DMN 1.5、SysML、SSDF 等已知标准的 x.y 版本（白名单正则表，
   避免把章节号/小数误判为版本）
4. 术语定义是否冲突（基于 glossary-master.md 的标题级定义）
5. 术语定义漂移（v2 新增，纯报告）：同一 glossary 术语在多文件以标题形式定义时，
   提取定义段落做 token Jaccard 相似度比对，< 0.3 判为"定义漂移"

退出码策略：
- exit 1：被引用但未定义的公理；或标准版本硬错误（invalid_versions 命中）
- exit 0：其余检查（文件内/跨文件版本差异、术语冲突、定义漂移）均为报告型

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
from typing import List, Dict, Tuple, Set, Optional
from collections import defaultdict

try:
    import yaml  # pyyaml 已在 requirements.txt 声明
except ImportError:  # pragma: no cover - 兜底
    yaml = None


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
class CrossFileVersionIssue:
    """跨文件版本问题：standard 的多个版本在非历史语境中出现。"""
    standard: str
    versions: Dict[str, List[Tuple[str, int, bool]]]  # version -> [(file, line, is_currency_claim)]
    registered: bool  # 全部版本均已在 canonical-names.yaml 登记（已知版本线，降级为信息）


@dataclass
class InvalidVersionError:
    """硬错误：引用了 canonical-names.yaml invalid_versions 判定的错误版本。"""
    standard: str
    version: str
    canonical: str
    locations: List[Tuple[str, int]]


@dataclass
class TermConflict:
    term: str
    definitions: List[Tuple[str, str]]  # (file, definition_snippet)


@dataclass
class DefinitionDrift:
    """定义漂移：同一术语在不同文件的定义段落相似度过低。"""
    term: str
    pairs: List[Tuple[str, int, str, int, float]]  # (file_a, line_a, file_b, line_b, jaccard)


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

# x.y 版本号识别表（v2 新增）：仅对已知标准名启用，避免把章节号/小数误判为版本。
# 版本统一归一到 x.y（第三位如 BPMN 2.0.2、ArchiMate 4.0.2 视为维护修订，折叠到 x.y）。
XY_STANDARD_RES: List[Tuple[str, re.Pattern]] = [
    ("ARCHIMATE", re.compile(r"\bArchiMate\s+v?(\d+(?:\.\d+){1,2})", re.IGNORECASE)),
    ("SLSA", re.compile(r"\bSLSA\s+v?(\d+(?:\.\d+){1,2})", re.IGNORECASE)),
    ("BPMN", re.compile(r"\bBPMN\s+v?(\d+(?:\.\d+){1,2})", re.IGNORECASE)),
    ("DMN", re.compile(r"\bDMN\s+v?(\d+(?:\.\d+){1,2})", re.IGNORECASE)),
    ("SSDF", re.compile(r"\bSSDF\s+v?(\d+(?:\.\d+){1,2})", re.IGNORECASE)),
    ("SYSML", re.compile(r"\bSysML\s+v?(\d+(?:\.\d+)?)", re.IGNORECASE)),
    ("TOGAF", re.compile(
        r"\bTOGAF\s+(?:Standard[,\s]+)?(?:the\s+)?v?(\d+(?:\.\d+)?)(?:st|nd|rd|th)?\b",
        re.IGNORECASE,
    )),
]


def _norm_xy_version(raw: str) -> str:
    """x.y.z -> x.y（维护修订折叠）；整数版本保持不变。"""
    parts = raw.split(".")
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return raw


HISTORICAL_CONTEXT_RE = re.compile(
    r"反例|历史|旧版|旧标准|前一版本|前版|前身|升级|演进|对比|timeline|roadmap|路线图|frontier|tracking|status|update|alignment|mapping|"
    r"采纳|系列|版本线|version line|lifecycle|生命周期|"
    r"deprecated|obsolete|取代|替代|previously|former|superseded|withdrawn|legacy|replaced by|first edition|prior|previous|edition|"
    r"evolution|history of|不存在|没有官方|尚无|非官方|预期|预计|草案|draft|beta|后续规划|后续版本规划|"
    r"声称|核实|复核|勘误|errata|跟踪",
    re.IGNORECASE,
)
# v2 收窄说明：移除过宽的“发布”“对照”（release/comparison 叙述中常伴随真正的现行主张，
# 使 matrix/tracking 类文件多版本共存永不报警）；同时补充更精确的豁免词：
# 否定语境（不存在/没有官方/尚无）、未来/草案语境（预期/预计/beta/后续规划/路线图）、
# 审计引用语境（声称/核实/复核/勘误）。

# 现行主张标记（同行）：用于在跨文件报告中标注高置信度“现行版本”断言
CURRENCY_CLAIM_RE = re.compile(
    r"现行|当前有效版本|当前版本|最新版本|最新正式版|生效|正式版|现役|current version|latest version",
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


def _norm_standard_key(std_raw: str) -> str:
    """归一标准名用于跨文件聚合：
    - ISO/IEC/IEEE N / ISO/IEC N / ISO N / IEC N / IEEE N / IEC/IEEE N 视为同一标准，
      保留 part 号（21838-1 与 21838-3 是不同部件，不合并）；
    - 统一空格与斜杠。
    """
    std = re.sub(r"\s+", " ", std_raw.strip().upper())
    std = re.sub(r"\s*/\s*", "/", std)
    m = re.match(r"(?:ISO/IEC/IEEE|ISO/IEC|ISO/IEEE|IEC/IEEE|ISO|IEC|IEEE)\s+(\d+(?:[-/]\d+)*)", std)
    if m:
        return "ISO " + m.group(1)
    return std


# 标准版本提及记录：(standard_key, version, file, line, is_historical, is_currency_claim)
VersionMention = Tuple[str, str, str, int, bool, bool]


def collect_version_mentions(root: Path) -> List[VersionMention]:
    """收集全库标准版本提及（4 位年份 + 已知标准 x.y），附带历史语境与现行主张标记。"""
    mentions: List[VersionMention] = []
    files = _collect_markdown_files(root)

    for md in files:
        text = md.read_text(encoding="utf-8")
        lines = text.splitlines()
        rel = md.relative_to(root).as_posix()
        for lineno, line in enumerate(lines, start=1):
            ctx_lines = lines[max(0, lineno - 11):lineno + 10]
            context = "\n".join(ctx_lines)
            is_historical = bool(HISTORICAL_CONTEXT_RE.search(context))
            is_currency = bool(CURRENCY_CLAIM_RE.search(line))
            for m in STANDARD_RE.finditer(line):
                key = _norm_standard_key(m.group(1))
                mentions.append((key, m.group(2), rel, lineno, is_historical, is_currency))
            for name, pattern in XY_STANDARD_RES:
                for m in pattern.finditer(line):
                    version = _norm_xy_version(m.group(1))
                    mentions.append((name, version, rel, lineno, is_historical, is_currency))
    return mentions


def extract_standard_version_conflicts(root: Path,
                                       mentions: Optional[List[VersionMention]] = None,
                                       registry: Optional["CanonicalRegistry"] = None,
                                       ) -> List[StandardVersionConflict]:
    """提取标准版本冲突（文件内）。

    冲突判定规则：
    1. 仅检查同一文件内同一标准出现多个版本；跨文件版本差异由
       extract_crossfile_version_issues 处理。
    2. 若旧版本仅出现在历史/反例/演进/对比语境（见 HISTORICAL_CONTEXT_RE），不视为冲突。
    """
    if mentions is None:
        mentions = collect_version_mentions(root)
    refs: Dict[str, Dict[str, List[Tuple[str, int, bool]]]] = defaultdict(lambda: defaultdict(list))
    for key, version, rel, lineno, is_historical, _is_currency in mentions:
        refs[key][version].append((rel, lineno, is_historical))

    conflicts = []
    for std, versions in refs.items():
        if len(versions) <= 1:
            continue
        # 按文件聚合：分别记录历史语境版本与非历史语境版本
        per_file_non_historical: Dict[str, Set[str]] = defaultdict(set)
        per_file_all: Dict[str, Set[str]] = defaultdict(set)
        for version, locs in versions.items():
            for file, line, is_historical in locs:
                per_file_all[file].add(version)
                if not is_historical:
                    per_file_non_historical[file].add(version)
        # 冲突定义：同一文件内存在多个版本，且至少两个版本在非历史语境中出现过
        intra_file_conflicts = any(
            len(per_file_non_historical.get(file, set())) > 1
            for file in per_file_all
        )
        if intra_file_conflicts:
            # 全部涉及版本均已在 canonical-names.yaml 登记（已知版本线，如 ArchiMate 3.2/4.0）
            # → 降级为跨文件报告的信息项，不计入文件内冲突
            nh_vers: Set[str] = set()
            for s in per_file_non_historical.values():
                nh_vers |= s
            if registry is not None and nh_vers and nh_vers <= registry.registered_versions.get(std, set()):
                continue
            # 报告中仅保留非历史语境的位置，便于定位
            filtered_versions: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
            for version, locs in versions.items():
                for file, line, is_historical in locs:
                    if not is_historical:
                        filtered_versions[version].append((file, line))
            conflicts.append(StandardVersionConflict(standard=std, versions=dict(filtered_versions)))
    return conflicts


# ---------------------------------------------------------------------------
# canonical-names.yaml 登记联动（v2 新增）
# ---------------------------------------------------------------------------

CANONICAL_NAMES_DEFAULT = "struct/99-reference/tools/canonical-names.yaml"


@dataclass
class CanonicalRegistry:
    """canonical-names.yaml 的精简视图：按归一 key 聚合已登记版本与 invalid 版本。"""
    registered_versions: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))
    invalid_versions: Dict[str, Set[str]] = field(default_factory=lambda: defaultdict(set))


def _parse_canonical_entries(data: dict) -> List[dict]:
    if isinstance(data, dict) and isinstance(data.get("standards"), list):
        return [e for e in data["standards"] if isinstance(e, dict) and e.get("canonical")]
    return []


def _mini_yaml_parse(text: str) -> List[dict]:
    """无 pyyaml 时的兜底解析：仅识别本文件用到的 canonical/invalid_versions 结构。"""
    entries: List[dict] = []
    current: Optional[dict] = None
    in_invalid = False
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        m = re.match(r"^\s*-\s*canonical:\s*\"?([^\"]+)\"?\s*$", line)
        if m:
            current = {"canonical": m.group(1).strip(), "invalid_versions": []}
            entries.append(current)
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
            current["invalid_versions"].append(m.group(1).strip())
    return entries


def load_canonical_registry(path: Path) -> CanonicalRegistry:
    registry = CanonicalRegistry()
    if not path.exists():
        return registry
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        try:
            entries = _parse_canonical_entries(yaml.safe_load(text))
        except Exception:
            entries = _mini_yaml_parse(text)
    else:
        entries = _mini_yaml_parse(text)

    for entry in entries:
        canonical = str(entry["canonical"]).strip()
        invalid = [str(v).strip() for v in entry.get("invalid_versions") or []]
        # 年份版标准：从 canonical 名提取归一 key 与版本
        m_std = re.match(
            r"(ISO\s*/\s*IEC\s*/\s*IEEE\s+\d+(?:[-/]\d+)*|ISO\s*/\s*IEC\s+\d+(?:[-/]\d+)*|"
            r"ISO\s+\d+(?:[-/]\d+)*|IEEE\s+\d+(?:[-/]\d+)*|IEC\s+\d+(?:[-/]\d+)*)",
            canonical, re.IGNORECASE,
        )
        if m_std:
            key = _norm_standard_key(m_std.group(1))
            m_ver = re.search(r":\s*(\d{4})\s*$", canonical)
            if m_ver:
                registry.registered_versions[key].add(m_ver.group(1))
            for v in invalid:
                if re.fullmatch(r"\d{4}", v):
                    registry.invalid_versions[key].add(v)
            continue
        # x.y 版标准：按已知标准名匹配
        upper = canonical.upper()
        for name, _pattern in XY_STANDARD_RES:
            # "NIST SSDF 1.2" 归到 SSDF key；"TOGAF Standard 10" 归到 TOGAF key
            if re.search(rf"\b{name}\b", upper):
                m_ver = re.search(r"(\d+(?:\.\d+){0,2})\s*$", canonical)
                if m_ver:
                    registry.registered_versions[name].add(_norm_xy_version(m_ver.group(1)))
                for v in invalid:
                    registry.invalid_versions[name].add(_norm_xy_version(v))
                break
    return registry


def extract_crossfile_version_issues(
    mentions: List[VersionMention],
    registry: CanonicalRegistry,
) -> Tuple[List[CrossFileVersionIssue], List[CrossFileVersionIssue], List[InvalidVersionError]]:
    """跨文件版本检查（v2 新增）。

    返回 (未登记版本冲突, 已登记版本线[信息], invalid 硬错误)。

    规则：
    1. 硬错误：非历史语境提及的版本命中 canonical-names.yaml 的 invalid_versions。
    2. 冲突：同一归一标准名下，≥2 个版本各自有非历史语境提及。
       若涉及版本全部已在 canonical-names.yaml 登记，则视为已知版本线（信息项）。
    """
    per_std: Dict[str, Dict[str, List[Tuple[str, int, bool, bool]]]] = defaultdict(lambda: defaultdict(list))
    for key, version, rel, lineno, is_historical, is_currency in mentions:
        per_std[key][version].append((rel, lineno, is_historical, is_currency))

    hard_errors: List[InvalidVersionError] = []
    for key, versions in per_std.items():
        invalid = registry.invalid_versions.get(key)
        if not invalid:
            continue
        for version, locs in versions.items():
            if version not in invalid:
                continue
            bad_locs = [(rel, lineno) for rel, lineno, is_hist, _c in locs if not is_hist]
            if bad_locs:
                hard_errors.append(InvalidVersionError(
                    standard=key, version=version, canonical="", locations=bad_locs,
                ))

    conflicts: List[CrossFileVersionIssue] = []
    registered_lines: List[CrossFileVersionIssue] = []
    for key, versions in sorted(per_std.items()):
        nh_versions: Dict[str, List[Tuple[str, int, bool]]] = {}
        for version, locs in versions.items():
            nh = [(rel, lineno, is_cur) for rel, lineno, is_hist, is_cur in locs if not is_hist]
            if nh:
                nh_versions[version] = nh
        if len(nh_versions) <= 1:
            continue
        registered = registry.registered_versions.get(key, set())
        issue = CrossFileVersionIssue(
            standard=key,
            versions=nh_versions,
            registered=bool(registered) and set(nh_versions) <= registered,
        )
        (registered_lines if issue.registered else conflicts).append(issue)
    return conflicts, registered_lines, hard_errors


# ---------------------------------------------------------------------------
# 术语定义
# ---------------------------------------------------------------------------

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


def extract_heading_definitions(root: Path, glossary_path: Path
                                ) -> Dict[str, List[Tuple[str, int, str]]]:
    """提取 glossary 术语在非 glossary 文件中的标题级定义段落。

    返回 term -> [(file, line, definition_text)]，定义文本为标题后至下一标题
    （或 800 字符上限）之间的段落。
    """
    glossary_terms = extract_term_definitions_from_glossary(glossary_path)
    heading_defs: Dict[str, List[Tuple[str, int, str]]] = defaultdict(list)
    files = _collect_markdown_files(root)

    for md in files:
        rel = md.relative_to(root).as_posix()
        if "glossary" in rel:
            continue
        # 跳过变更日志、外部链接索引、模板/索引/清单类文件，
        # 避免非定义性标题（索引条目、模板占位）被误报为定义
        if ("CHANGELOG" in rel or "external-links/authoritative-sources" in rel
                or "/templates/" in rel or "knowledge-index/" in rel
                or "deliverables-manifest" in rel or "book-outline" in rel):
            continue
        text = md.read_text(encoding="utf-8")
        for term in glossary_terms:
            term_escaped = re.escape(term)
            # 标题级定义：允许章节编号前缀（如 "### 3.1 复用率"）与括号别名后缀
            # （如 "## 服务网格 (Service Mesh)"），术语须位于标题起始位置
            pattern = re.compile(
                r"^#{2,4}\s+(?:[\d.]+\s*)?" + term_escaped + r"(?:\s*$|\s|[（(])",
                re.MULTILINE,
            )
            for m in pattern.finditer(text):
                line_no = text[:m.start()].count("\n") + 1
                # 定义文本从标题行之后开始（匹配可能终止于标题行中间）
                line_end = text.find("\n", m.end())
                body_start = line_end + 1 if line_end != -1 else len(text)
                rest = text[body_start:body_start + 800]
                next_heading = re.search(r"^#{1,4}\s+", rest, re.MULTILINE)
                snippet = rest[:next_heading.start()] if next_heading else rest
                def_text = re.sub(r"\s+", " ", snippet).strip()
                if def_text:
                    heading_defs[term].append((rel, line_no, def_text))
                break
    return heading_defs


def extract_term_conflicts(root: Path, glossary_path: Path,
                           heading_defs: Optional[Dict[str, List[Tuple[str, int, str]]]] = None
                           ) -> List[TermConflict]:
    """检测术语在 glossary 与正文中的定义冲突。

    仅检测以标题形式（##/###/#### Term）明确定义的术语，
    且该术语在 2 至 5 个不同非 glossary 文件中被定义；
    超高频通用术语或在大量文件中出现的标题不视为冲突。
    """
    if heading_defs is None:
        heading_defs = extract_heading_definitions(root, glossary_path)
    conflicts: List[TermConflict] = []

    for term, defs in heading_defs.items():
        files_set = {d[0] for d in defs}
        if 2 <= len(files_set) <= 5:
            conflicts.append(TermConflict(
                term=term,
                definitions=[(f, f"第 {line} 行") for f, line, _t in defs],
            ))

    return conflicts


_CJK_RE = re.compile(r"[\u4e00-\u9fff]+")
_LATIN_RE = re.compile(r"[a-z0-9]+")


def _definition_tokens(text: str) -> Set[str]:
    """定义段落 token 化：拉丁词（≥3 字符）+ 中文二元组，用于 Jaccard 相似度。"""
    text = text.lower()
    tokens = {w for w in _LATIN_RE.findall(text) if len(w) >= 3 and not w.isdigit()}
    for run in _CJK_RE.findall(text):
        for i in range(len(run) - 1):
            tokens.add(run[i:i + 2])
    return tokens


def extract_definition_drifts(heading_defs: Dict[str, List[Tuple[str, int, str]]],
                              threshold: float = 0.3) -> List[DefinitionDrift]:
    """定义漂移检测（v2 新增，纯报告）。

    同一术语在 2 至 5 个文件中以标题形式定义时，两两计算定义段落的
    token Jaccard 相似度，低于 threshold 的判定为定义漂移对。
    """
    drifts: List[DefinitionDrift] = []
    for term, defs in heading_defs.items():
        files_set = {d[0] for d in defs}
        if not (2 <= len(files_set) <= 5):
            continue
        tokenized = [(f, line, _definition_tokens(t)) for f, line, t in defs]
        pairs = []
        for i in range(len(tokenized)):
            for j in range(i + 1, len(tokenized)):
                fa, la, ta = tokenized[i]
                fb, lb, tb = tokenized[j]
                if fa == fb:
                    continue
                union = ta | tb
                jaccard = (len(ta & tb) / len(union)) if union else 1.0
                if jaccard < threshold:
                    pairs.append((fa, la, fb, lb, round(jaccard, 3)))
        if pairs:
            drifts.append(DefinitionDrift(term=term, pairs=pairs))
    return drifts


# ---------------------------------------------------------------------------
# 报告输出
# ---------------------------------------------------------------------------

def write_json_report(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_md_report(path: Path, undefined_axioms: List[AxiomIssue], multi_defined_axioms: List[AxiomIssue],
                    std_conflicts: List[StandardVersionConflict], term_conflicts: List[TermConflict],
                    crossfile_conflicts: List[CrossFileVersionIssue],
                    registered_lines: List[CrossFileVersionIssue],
                    invalid_errors: List[InvalidVersionError],
                    definition_drifts: List[DefinitionDrift]):
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

    lines.append("## 标准版本冲突（文件内）")
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

    # ---- v2 新增：跨文件标准版本一致性 ----
    lines.append("## 跨文件标准版本一致性（报告型）")
    lines.append("")

    lines.append("### 标准版本硬错误（invalid_versions 命中，触发 exit 1）")
    lines.append("")
    if invalid_errors:
        for e in invalid_errors:
            lines.append(f"- **{e.standard}:{e.version}** — canonical-names.yaml 判定该版本不存在/错误")
            for loc in e.locations[:5]:
                lines.append(f"  - `{loc[0]}` 第 {loc[1]} 行")
            if len(e.locations) > 5:
                lines.append(f"  - ... 还有 {len(e.locations) - 5} 处")
        lines.append("")
    else:
        lines.append("- 未发现 invalid 版本引用")
        lines.append("")

    lines.append("### 未登记版本冲突（同一标准多个非历史语境版本，未全部登记于 canonical-names.yaml）")
    lines.append("")
    if crossfile_conflicts:
        for issue in crossfile_conflicts:
            lines.append(f"#### {issue.standard}")
            for version, locs in issue.versions.items():
                currency_n = sum(1 for _f, _l, c in locs if c)
                marker = f"，其中 {currency_n} 处为显式现行主张" if currency_n else ""
                lines.append(f"- **{version}**（{len(locs)} 处非历史语境{marker}）")
                for f, line, is_cur in locs[:5]:
                    tag = " ⚠️现行主张" if is_cur else ""
                    lines.append(f"  - `{f}` 第 {line} 行{tag}")
                if len(locs) > 5:
                    lines.append(f"  - ... 还有 {len(locs) - 5} 处")
            lines.append("")
    else:
        lines.append("- 未发现未登记的跨文件版本冲突")
        lines.append("")

    lines.append("### 已登记版本线（信息项：多版本均已在 canonical-names.yaml 登记）")
    lines.append("")
    if registered_lines:
        for issue in registered_lines:
            ver_summary = ", ".join(
                f"{v}({len(locs)})" for v, locs in sorted(issue.versions.items())
            )
            lines.append(f"- **{issue.standard}**: {ver_summary}")
        lines.append("")
    else:
        lines.append("- 无")
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

    lines.append("## 术语定义漂移（文本相似度，报告型）")
    lines.append("")
    lines.append("同一 glossary 术语在多文件以标题形式定义，定义段落 token Jaccard < 0.3 的判定为漂移对。")
    lines.append("")
    if definition_drifts:
        for d in definition_drifts:
            lines.append(f"### {d.term}")
            for fa, la, fb, lb, sim in d.pairs:
                lines.append(f"- 相似度 {sim:.3f}: `{fa}` 第 {la} 行 ↔ `{fb}` 第 {lb} 行")
            lines.append("")
    else:
        lines.append("- 未发现定义漂移")
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
        "--canonical-names",
        metavar="PATH",
        default=CANONICAL_NAMES_DEFAULT,
        help="canonical 标准名字典路径（默认 struct/99-reference/tools/canonical-names.yaml）",
    )
    parser.add_argument(
        "--json",
        metavar="PATH",
        help="输出 JSON 报告路径",
    )
    parser.add_argument(
        "--report",
        metavar="PATH",
        default="reports/cross-index-report.md",
        help="输出 Markdown 报告路径（默认 reports/cross-index-report.md）",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    root = (project_root / args.root).resolve()
    glossary_path = (project_root / args.glossary).resolve()
    canonical_path = (project_root / args.canonical_names).resolve()

    if not root.exists():
        print(f"错误：根目录不存在 {root}", file=sys.stderr)
        sys.exit(1)

    print(f"扫描目录: {root}")
    print(f"术语表: {glossary_path}")
    print(f"canonical 字典: {canonical_path}")

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

    mentions = collect_version_mentions(root)
    registry = load_canonical_registry(canonical_path)
    std_conflicts = extract_standard_version_conflicts(root, mentions, registry)
    crossfile_conflicts, registered_lines, invalid_errors = extract_crossfile_version_issues(
        mentions, registry
    )

    heading_defs = extract_heading_definitions(root, glossary_path)
    term_conflicts = extract_term_conflicts(root, glossary_path, heading_defs)
    definition_drifts = extract_definition_drifts(heading_defs)

    print(f"公理问题: {len(undefined_axioms)} 个未定义, {len(multi_defined_axioms)} 个重复定义")
    print(f"标准版本冲突（文件内）: {len(std_conflicts)} 个")
    print(f"跨文件版本冲突（未登记）: {len(crossfile_conflicts)} 个；"
          f"已登记版本线（信息）: {len(registered_lines)} 个")
    print(f"标准版本硬错误（invalid_versions）: {len(invalid_errors)} 个")
    print(f"术语定义冲突: {len(term_conflicts)} 个")
    print(f"术语定义漂移: {len(definition_drifts)} 个")

    if undefined_axioms:
        print("\n未定义公理:")
        for a in undefined_axioms:
            print(f"  - {a.axiom_id} 引用处: {a.referenced_in[:3]}")

    if std_conflicts:
        print("\n标准版本冲突（文件内）:")
        for c in std_conflicts:
            versions = ", ".join(f"{v}({len(locs)})" for v, locs in c.versions.items())
            print(f"  - {c.standard}: {versions}")

    if crossfile_conflicts:
        print("\n跨文件版本冲突（未登记）:")
        for issue in crossfile_conflicts:
            versions = ", ".join(f"{v}({len(locs)})" for v, locs in issue.versions.items())
            print(f"  - {issue.standard}: {versions}")

    if invalid_errors:
        print("\n标准版本硬错误（invalid_versions 命中）:")
        for e in invalid_errors:
            print(f"  - {e.standard}:{e.version} 出现于 {e.locations[:3]}")

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
            "crossfile_version_conflicts": [
                {
                    "standard": issue.standard,
                    "registered": issue.registered,
                    "versions": {
                        v: [{"file": f, "line": l, "currency_claim": c} for f, l, c in locs]
                        for v, locs in issue.versions.items()
                    },
                }
                for issue in crossfile_conflicts + registered_lines
            ],
            "invalid_version_errors": [
                {
                    "standard": e.standard,
                    "version": e.version,
                    "locations": [{"file": f, "line": l} for f, l in e.locations],
                }
                for e in invalid_errors
            ],
            "term_conflicts": [
                {
                    "term": c.term,
                    "definitions": [{"file": f, "location": loc} for f, loc in c.definitions],
                }
                for c in term_conflicts
            ],
            "definition_drifts": [
                {
                    "term": d.term,
                    "pairs": [
                        {"file_a": fa, "line_a": la, "file_b": fb, "line_b": lb, "jaccard": sim}
                        for fa, la, fb, lb, sim in d.pairs
                    ],
                }
                for d in definition_drifts
            ],
        }
        write_json_report(Path(args.json), data)
        print(f"JSON 报告已保存: {args.json}")

    if args.report:
        write_md_report(Path(args.report), undefined_axioms, multi_defined_axioms, std_conflicts,
                        term_conflicts, crossfile_conflicts, registered_lines, invalid_errors,
                        definition_drifts)
        print(f"Markdown 报告已保存: {args.report}")

    # 退出码策略：
    # - 硬错误：被引用但未定义的公理；非历史语境引用 canonical-names.yaml 判定的 invalid 版本。
    # - 其余（文件内/跨文件版本差异、术语冲突、定义漂移）均为报告型，不阻塞退出码。
    has_error = bool(undefined_axioms) or bool(invalid_errors)
    if std_conflicts or crossfile_conflicts:
        print("\n注意：存在标准版本差异，已作为警告输出，请人工复核。")
    if term_conflicts or definition_drifts:
        print("\n注意：存在术语定义差异/漂移，已作为警告输出，请人工复核。")
    sys.exit(1 if has_error else 0)


if __name__ == "__main__":
    main()
