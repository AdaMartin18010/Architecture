#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
术语查询脚本 v3.0 — 跨标准术语定义、对比与检索 CLI 工具

内置标准覆盖：
  - ISO/IEC/IEEE 42010:2022（架构描述术语）
  - ISO/IEC 26550:2015（产品线工程术语）
  - TOGAF 10（企业架构术语）
  - IEEE 1517-2010（复用过程术语）
  - SLSA 1.2（供应链安全术语）
  - MCP 2025-11-25（AI 协议术语）

外部数据库：
  - 优先加载同目录下的 terminology-db.yaml（或 terminology-db.json）。
  - 若外部文件不存在，则回退到内置字典，保证单文件可运行。

用法示例：
    python terminology-query.py search "architecture view"
    python terminology-query.py search "复用" --lang zh
    python terminology-query.py compare "reusability" --standards iso25010,ieee1517
    python terminology-query.py list --standard togaf10
    python terminology-query.py version-hint "reusability" --lang zh
    python terminology-query.py export-glossary --format md --output glossary.md
    python terminology-query.py sync --sources struct/99-reference/glossary/terminology-crosswalk.md
    python terminology-query.py --test

要求：Python 3.10+
"""

import argparse
import io
import json
import os
import re
import sys
import tempfile
from difflib import SequenceMatcher, get_close_matches
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# YAML 支持（未安装时自动回退到 JSON）
# ---------------------------------------------------------------------------

try:
    import yaml

    HAS_YAML = True
except Exception:  # pragma: no cover
    yaml = None  # type: ignore[assignment]
    HAS_YAML = False

# ---------------------------------------------------------------------------
# 路径常量
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH_YAML = SCRIPT_DIR / "terminology-db.yaml"
DB_PATH_JSON = SCRIPT_DIR / "terminology-db.json"

# ---------------------------------------------------------------------------
# 内置术语数据库（回退用，确保单文件可运行）
# 结构：{term: {definitions: {标准: 定义}, aliases: [别名], related: [相关术语]}}
# ---------------------------------------------------------------------------


_BUILTIN_TERM_DB: dict[str, dict[str, Any]] = {
    # ── ISO/IEC/IEEE 42010:2022 ─────────────────────────────────────────────
    "Architecture Description": {
        "definitions": {
            "ISO/IEC/IEEE 42010:2022": (
                "A work product used to express an architecture. "
                "It encompasses architecture views, viewpoint specifications, and correspondence rules."
            ),
        },
        "aliases": ["架构描述", "AD"],
        "related": ["View", "Viewpoint", "Correspondence", "Stakeholder"],
    },
    "View": {
        "definitions": {
            "ISO/IEC/IEEE 42010:2022": (
                "A representation of a whole system from the perspective of a related set of concerns."
            ),
        },
        "aliases": ["视图", "架构视图", "Architecture View"],
        "related": ["Viewpoint", "Concern", "Architecture Description", "Model Kind"],
    },
    "Viewpoint": {
        "definitions": {
            "ISO/IEC/IEEE 42010:2022": (
                "A specification of the conventions for constructing and using views, "
                "including model kinds, languages, notations, and analysis rules."
            ),
        },
        "aliases": ["视点", "视角"],
        "related": ["View", "Concern", "Stakeholder", "Model Kind"],
    },
    "Model Kind": {
        "definitions": {
            "ISO/IEC/IEEE 42010:2022": (
                "A kind of model defined by conventions for its construction and usage within a viewpoint."
            ),
        },
        "aliases": ["模型种类", "模型类型"],
        "related": ["Viewpoint", "View", "Model"],
    },
    "Concern": {
        "definitions": {
            "ISO/IEC/IEEE 42010:2022": (
                "An interest in a system relevant to one or more of its stakeholders."
            ),
        },
        "aliases": ["关注点"],
        "related": ["Stakeholder", "Viewpoint", "View"],
    },
    "Stakeholder": {
        "definitions": {
            "ISO/IEC/IEEE 42010:2022": (
                "An individual, team, or organization with interests in, or concerns relative to, a system."
            ),
        },
        "aliases": ["利益相关者", "干系人"],
        "related": ["Concern", "Viewpoint", "Architecture Description"],
    },
    "Correspondence": {
        "definitions": {
            "ISO/IEC/IEEE 42010:2022": (
                "A relationship between two or more architecture description elements, such as views or models."
            ),
        },
        "aliases": ["对应关系", "Correspondence Rule", "对应规则"],
        "related": ["Architecture Description", "View", "Viewpoint"],
    },
    "Architecture Description Framework": {
        "definitions": {
            "ISO/IEC/IEEE 42010:2022": (
                "Conventions, principles, and practices for the description of architectures "
                "in a specific domain of application or community of stakeholders. (ADF)"
            ),
        },
        "aliases": ["ADF", "架构描述框架"],
        "related": ["Architecture Description", "Viewpoint", "Model Kind"],
    },
    "System": {
        "definitions": {
            "ISO/IEC/IEEE 42010:2022": (
                "A combination of interacting elements organized to achieve one or more stated purposes."
            ),
        },
        "aliases": ["系统"],
        "related": ["Concern", "Stakeholder", "Architecture Description"],
    },
    # ── ISO/IEC 26550:2015 ──────────────────────────────────────────────────
    "Product Line Engineering": {
        "definitions": {
            "ISO/IEC 26550:2015": (
                "An approach to developing and maintaining software-intensive systems "
                "using a shared set of software assets and a common means of production."
            ),
        },
        "aliases": ["产品线工程", "PLE", "Software Product Line Engineering"],
        "related": ["Domain Engineering", "Application Engineering", "Variability"],
    },
    "Domain Engineering": {
        "definitions": {
            "ISO/IEC 26550:2015": (
                "The process of defining and realizing the commonality and variability of the product line, "
                "producing reusable domain assets."
            ),
            "IEEE 1517-2010": (
                "The process of identifying, collecting, organizing, and representing the relevant information "
                "in a domain to support reuse."
            ),
        },
        "aliases": ["领域工程"],
        "related": ["Application Engineering", "Variability", "Commonality", "Domain Analysis"],
    },
    "Application Engineering": {
        "definitions": {
            "ISO/IEC 26550:2015": (
                "Building individual products by reusing domain assets and exploiting the variability "
                "captured during domain engineering."
            ),
            "IEEE 1517-2010": (
                "The process of constructing a specific system or application by reusing qualified assets "
                "from a reuse library."
            ),
        },
        "aliases": ["应用工程"],
        "related": ["Domain Engineering", "Variability", "Reusability"],
    },
    "Variability": {
        "definitions": {
            "ISO/IEC 26550:2015": (
                "The ability of a software artifact to be efficiently extended, changed, customized, "
                "or configured for use in a specific context."
            ),
        },
        "aliases": ["可变性", "变异性"],
        "related": ["Variability Model", "Commonality", "Adaptability", "Feature Model"],
    },
    "Commonality": {
        "definitions": {
            "ISO/IEC 26550:2015": (
                "Properties that are shared across all members of a product line and are not subject to variation."
            ),
        },
        "aliases": ["共性", "公共性"],
        "related": ["Variability", "Domain Engineering", "Product Line Engineering"],
    },
    "Feature Model": {
        "definitions": {
            "ISO/IEC 26550:2015": (
                "A hierarchically arranged set of features with relationships and constraints, "
                "used to model and manage product line variability."
            ),
        },
        "aliases": ["特征模型", "Variability Model", "可变性模型"],
        "related": ["Variability", "Commonality", "Domain Engineering"],
    },
    "Product": {
        "definitions": {
            "ISO/IEC 26550:2015": (
                "A software-intensive system that is developed and delivered to a customer."
            ),
        },
        "aliases": ["产品"],
        "related": ["Application Engineering", "Product Line Engineering"],
    },
    # ── TOGAF 10 ────────────────────────────────────────────────────────────
    "Architecture Building Block": {
        "definitions": {
            "TOGAF 10": (
                "Architecture Building Block (ABB): A constituent of the architecture model that describes "
                "a single aspect of the overall architecture; typically independent of implementation."
            ),
        },
        "aliases": ["ABB", "架构构建块"],
        "related": ["Solution Building Block", "Building Block", "Architecture Repository"],
    },
    "Solution Building Block": {
        "definitions": {
            "TOGAF 10": (
                "Solution Building Block (SBB): A candidate physical component that will realize "
                "one or more Architecture Building Blocks."
            ),
        },
        "aliases": ["SBB", "解决方案构建块"],
        "related": ["Architecture Building Block", "Building Block", "Implementation"],
    },
    "Architecture Repository": {
        "definitions": {
            "TOGAF 10": (
                "A logical place to hold all architecture-related outputs, including deliverables, models, patterns, and standards."
            ),
        },
        "aliases": ["架构仓库", "架构资源库"],
        "related": ["Enterprise Continuum", "Architecture Description", "Architecture Development Method"],
    },
    "Enterprise Continuum": {
        "definitions": {
            "TOGAF 10": (
                "A view of the Architecture Repository that provides methods for classifying architecture and solution artifacts."
            ),
        },
        "aliases": ["企业连续体"],
        "related": ["Architecture Repository", "Foundation Architecture", "Architecture Development Method"],
    },
    "Architecture Development Method": {
        "definitions": {
            "TOGAF 10": (
                "Architecture Development Method (ADM): The core iterative method for developing architectures in TOGAF, "
                "covering phases from Preliminary to Architecture Change Management."
            ),
        },
        "aliases": ["ADM", "架构开发方法"],
        "related": ["Architecture Repository", "Building Block", "Architecture Building Block"],
    },
    "Building Block": {
        "definitions": {
            "TOGAF 10": (
                "A potentially reusable component of business, IT, or architectural capability that combines "
                "with other building blocks to deliver architectures and solutions."
            ),
        },
        "aliases": ["构建块"],
        "related": ["Architecture Building Block", "Solution Building Block", "Reusability"],
    },
    "Foundation Architecture": {
        "definitions": {
            "TOGAF 10": (
                "Generic building blocks and their inter-relationships, together with associated standards, "
                "that define a generic foundational platform."
            ),
        },
        "aliases": ["基础架构"],
        "related": ["Enterprise Continuum", "Architecture Repository", "Building Block"],
    },
    # ── IEEE 1517-2010 ──────────────────────────────────────────────────────
    "Reusability": {
        "definitions": {
            "IEEE 1517-2010": (
                "The degree to which a software asset can be used in systems other than the one "
                "for which it was originally designed, with little or no modification."
            ),
            "ISO/IEC 25010:2023": (
                "The degree to which an asset can be used in more than one system, or in building other assets."
            ),
        },
        "aliases": ["可复用性", "复用性"],
        "related": ["Adaptability", "Variability", "Component", "Asset"],
    },
    "Reuse Library": {
        "definitions": {
            "IEEE 1517-2010": (
                "An organized collection of reusable assets, together with the processes, methods, and tools "
                "needed to support their storage, retrieval, and maintenance."
            ),
        },
        "aliases": ["复用库", "资产库", "Asset Library"],
        "related": ["Asset", "Domain Engineering", "Reusability"],
    },
    "Asset": {
        "definitions": {
            "IEEE 1517-2010": (
                "A software product, work product, or other item of value that is a candidate for reuse "
                "in the development or maintenance of software systems."
            ),
            "General": (
                "A modular, deployable, and replaceable part of a system that encapsulates implementation and exposes interfaces."
            ),
        },
        "aliases": ["资产", "软件资产"],
        "related": ["Component", "Reuse Library", "Reusability", "Building Block"],
    },
    "Domain Analysis": {
        "definitions": {
            "IEEE 1517-2010": (
                "The process of identifying, collecting, organizing, and representing relevant information in a domain, "
                "based on the study of existing systems and their development histories."
            ),
        },
        "aliases": ["领域分析"],
        "related": ["Domain Engineering", "Asset", "Reuse Library"],
    },
    "Qualification": {
        "definitions": {
            "IEEE 1517-2010": (
                "The process of evaluating a reusable asset to determine whether it meets specified requirements for reuse in a given context."
            ),
        },
        "aliases": ["资格认定", "资质认定", "Asset Qualification"],
        "related": ["Asset", "Reuse Library", "Certification"],
    },
    "Adaptation": {
        "definitions": {
            "IEEE 1517-2010": (
                "The process of modifying a reusable asset so that it conforms to the specific requirements of a target system or application."
            ),
            "ISO/IEC 25010:2023": (
                "The degree to which a product or system can be effectively and efficiently adapted for different or evolving environments."
            ),
        },
        "aliases": ["适配", "适应性"],
        "related": ["Reusability", "Variability", "Asset"],
    },
    "Certification": {
        "definitions": {
            "IEEE 1517-2010": (
                "The process of formally confirming that a reusable asset satisfies specified standards or requirements for reuse."
            ),
        },
        "aliases": ["认证", "资格认证"],
        "related": ["Qualification", "Asset", "Reuse Library"],
    },
    # ── SLSA 1.2 ────────────────────────────────────────────────────────────
    "Provenance": {
        "definitions": {
            "SLSA 1.2": (
                "The verifiable record describing how a software artifact was built, "
                "including the build process, inputs, and dependencies."
            ),
        },
        "aliases": ["来源证明", "出处", "Build Provenance"],
        "related": ["Attestation", "Artifact", "Supply Chain"],
    },
    "Attestation": {
        "definitions": {
            "SLSA 1.2": (
                "A cryptographically signed statement about a software artifact, typically used to assert facts such as provenance or test results."
            ),
        },
        "aliases": ["证明", "数字证明"],
        "related": ["Provenance", "Artifact", "Supply Chain"],
    },
    "Artifact": {
        "definitions": {
            "SLSA 1.2": (
                "An immutable blob of data, typically a software package, container image, or binary, "
                "described by attestations and provenance."
            ),
        },
        "aliases": ["制品", "构件"],
        "related": ["Provenance", "Attestation", "Supply Chain", "Asset"],
    },
    "Source Integrity": {
        "definitions": {
            "SLSA 1.2": (
                "The property that the source code used to build a software artifact has not been tampered with and is traceable to its origin."
            ),
        },
        "aliases": ["源代码完整性"],
        "related": ["Provenance", "Supply Chain", "Artifact"],
    },
    "Build Level": {
        "definitions": {
            "SLSA 1.2": (
                "A numbered level in the SLSA framework (Build L1–L3) that indicates the strength of build integrity guarantees."
            ),
        },
        "aliases": ["构建等级", "SLSA Level"],
        "related": ["Provenance", "Source Integrity", "Artifact"],
    },
    "Supply Chain": {
        "definitions": {
            "SLSA 1.2": (
                "The series of steps and actors involved in producing and distributing software, "
                "including dependencies, build tools, and distribution channels."
            ),
        },
        "aliases": ["供应链"],
        "related": ["Provenance", "Attestation", "Artifact", "Source Integrity"],
    },
    # ── MCP 2025-11-25 ──────────────────────────────────────────────────────
    "Model Context Protocol": {
        "definitions": {
            "MCP 2025-11-25": (
                "An open protocol that standardizes how applications provide context to large language models, "
                "enabling secure, bi-directional connections between AI systems and data sources."
            ),
        },
        "aliases": ["MCP", "模型上下文协议"],
        "related": ["Server", "Tool", "Resource", "Prompt"],
    },
    "Server": {
        "definitions": {
            "MCP 2025-11-25": (
                "An MCP server exposes capabilities (tools, resources, prompts) to clients over a standardized transport, "
                "typically local stdio or HTTP."
            ),
        },
        "aliases": ["服务器", "MCP Server"],
        "related": ["Model Context Protocol", "Tool", "Resource", "Client"],
    },
    "Tool": {
        "definitions": {
            "MCP 2025-11-25": (
                "A capability exposed by an MCP server that allows models to perform actions, "
                "such as querying a database or calling an API."
            ),
        },
        "aliases": ["工具"],
        "related": ["Model Context Protocol", "Server", "Resource"],
    },
    "Resource": {
        "definitions": {
            "MCP 2025-11-25": (
                "A read-only capability exposed by an MCP server that provides contextual data to models, "
                "such as file contents or database schemas."
            ),
        },
        "aliases": ["资源"],
        "related": ["Model Context Protocol", "Server", "Tool"],
    },
    "Prompt": {
        "definitions": {
            "MCP 2025-11-25": (
                "A pre-defined prompt template exposed by an MCP server that helps users accomplish specific tasks or workflows."
            ),
        },
        "aliases": ["提示词", "提示模板"],
        "related": ["Model Context Protocol", "Server", "Tool"],
    },
    "Sampling": {
        "definitions": {
            "MCP 2025-11-25": (
                "A mechanism by which an MCP server can request that the client generate model completions or embeddings, "
                "enabling server-side orchestration."
            ),
        },
        "aliases": ["采样"],
        "related": ["Model Context Protocol", "Server", "Client"],
    },
    "Client": {
        "definitions": {
            "MCP 2025-11-25": (
                "An MCP client connects to one or more MCP servers, aggregates their capabilities, "
                "and makes them available to an application or model."
            ),
        },
        "aliases": ["客户端"],
        "related": ["Model Context Protocol", "Server"],
    },
}

_BUILTIN_STD_ALIASES: dict[str, list[str]] = {
    "ISO/IEC/IEEE 42010:2022": ["iso42010", "ieee42010", "42010", "iso_iec_ieee_42010"],
    "ISO/IEC 26550:2015": ["iso26550", "26550", "ple", "iso_iec_26550"],
    "TOGAF 10": ["togaf", "togaf10"],
    "IEEE 1517-2010": ["ieee1517", "1517"],
    "SLSA 1.2": ["slsa", "slsa1.2", "slsa12"],
    "MCP 2025-11-25": ["mcp", "mcp2025"],
    "ISO/IEC 25010:2023": ["iso25010", "25010", "iso_iec_25010"],
    "ISO/IEC/IEEE 12207:2026": ["iso12207", "12207", "ieee12207"],
    "ArchiMate 4.0": ["archimate", "archimate4"],
    "NIST SSDF 1.2": ["ssdf", "nistssdf", "800-218"],
    "General": ["general"],
}

_BUILTIN_STD_VERSION_HINTS: dict[str, dict[str, str]] = {
    "ISO/IEC/IEEE 42010:2022": {"version": "2022", "status": "已发布", "note": ""},
    "ISO/IEC 26550:2015": {"version": "2015", "status": "现行", "note": "不存在 2025 版"},
    "TOGAF 10": {"version": "10", "status": "已发布", "note": ""},
    "IEEE 1517-2010": {"version": "2010", "status": "现行", "note": ""},
    "SLSA 1.2": {"version": "1.2", "status": "已发布", "note": "Build/Source Track 已发布"},
    "MCP 2025-11-25": {"version": "2025-11-25", "status": "现行稳定版", "note": "RC 2026-07-28 预期"},
    "ISO/IEC 25010:2023": {"version": "2023", "status": "已发布", "note": "不存在 2024 版"},
    "ISO/IEC/IEEE 12207:2026": {"version": "2026", "status": "已发布", "note": "2026-04-29 发布"},
    "ArchiMate 4.0": {"version": "4.0", "status": "已发布", "note": "2026-04-27 正式发布"},
    "NIST SSDF 1.2": {"version": "1.2", "status": "Initial Public Draft", "note": "非最终版"},
}


def _builtin_db() -> dict[str, Any]:
    """返回内置数据库的完整副本。"""
    return {
        "terms": json.loads(json.dumps(_BUILTIN_TERM_DB)),
        "aliases": json.loads(json.dumps(_BUILTIN_STD_ALIASES)),
        "version_hints": json.loads(json.dumps(_BUILTIN_STD_VERSION_HINTS)),
    }


# ---------------------------------------------------------------------------
# 数据库加载与保存
# ---------------------------------------------------------------------------


def load_db(yaml_path: Path | str | None = None, json_path: Path | str | None = None) -> dict[str, Any]:
    """
    加载外部术语数据库。

    优先级：
      1. YAML（terminology-db.yaml）— 需要 PyYAML
      2. JSON（terminology-db.json）— 无需第三方依赖
      3. 内置字典（保证单文件可运行）
    """
    yaml_path = Path(yaml_path) if yaml_path else DB_PATH_YAML
    json_path = Path(json_path) if json_path else DB_PATH_JSON

    if HAS_YAML and yaml_path.exists():
        try:
            with open(yaml_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if isinstance(data, dict) and "terms" in data:
                return data
        except Exception as exc:  # pragma: no cover
            print(f"警告: 加载 {yaml_path} 失败，回退到内置数据: {exc}", file=sys.stderr)

    if json_path.exists():
        try:
            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "terms" in data:
                return data
        except Exception as exc:  # pragma: no cover
            print(f"警告: 加载 {json_path} 失败，回退到内置数据: {exc}", file=sys.stderr)

    return _builtin_db()


def save_db(
    data: dict[str, Any],
    yaml_path: Path | str | None = None,
    json_path: Path | str | None = None,
) -> Path:
    """保存数据库到 YAML（优先）或 JSON。返回实际写入的路径。"""
    yaml_path = Path(yaml_path) if yaml_path else DB_PATH_YAML
    json_path = Path(json_path) if json_path else DB_PATH_JSON

    if HAS_YAML:
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False, width=120)
        return yaml_path

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return json_path


# ---------------------------------------------------------------------------
# 全局数据库与索引（模块加载时初始化）
# ---------------------------------------------------------------------------

TERM_DB: dict[str, dict[str, Any]] = {}
STD_ALIASES: dict[str, list[str]] = {}
STD_VERSION_HINTS: dict[str, dict[str, str]] = {}
ALIAS_INDEX: dict[str, str] = {}
STD_INDEX: dict[str, list[str]] = {}
ALL_ALIASES: list[str] = []


def init_globals(data: dict[str, Any] | None = None) -> None:
    """用给定的数据库初始化全局变量和索引。"""
    global TERM_DB, STD_ALIASES, STD_VERSION_HINTS, ALIAS_INDEX, STD_INDEX, ALL_ALIASES
    if data is None:
        data = load_db()
    TERM_DB = data.get("terms", {})
    STD_ALIASES = data.get("aliases", {})
    STD_VERSION_HINTS = data.get("version_hints", {})
    ALIAS_INDEX, STD_INDEX, ALL_ALIASES = _build_indices()


def _build_indices() -> tuple[dict[str, str], dict[str, list[str]], list[str]]:
    alias_index: dict[str, str] = {}
    std_index: dict[str, list[str]] = {}
    all_aliases: list[str] = []
    for term, rec in TERM_DB.items():
        alias_index[term.lower()] = term
        all_aliases.append(term)
        for alias in rec.get("aliases", []):
            alias_index[alias.lower()] = term
            all_aliases.append(alias)
        for std in rec.get("definitions", {}):
            std_index.setdefault(std, []).append(term)
    return alias_index, std_index, all_aliases


init_globals()

# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------


def resolve_term(key: str) -> str | None:
    """通过名称或别名精确查找术语的标准名称（不区分大小写）。"""
    k = key.lower()
    return ALIAS_INDEX.get(k)


def fuzzy_search(key: str, lang: str = "en", topn: int = 20) -> list[str]:
    """
    模糊搜索术语。
    优先级：1) 精确匹配 2) 子串匹配（术语名、别名、定义） 3) difflib 模糊匹配
    """
    k = key.lower()
    results: list[str] = []
    seen: set[str] = set()

    def add(term: str) -> None:
        if term not in seen:
            seen.add(term)
            results.append(term)

    # 1) 精确匹配 / 别名精确匹配
    exact = resolve_term(key)
    if exact:
        add(exact)
        return results

    # 2) 子串匹配
    for term, rec in TERM_DB.items():
        if k in term.lower():
            add(term)
            continue
        matched = False
        for alias in rec.get("aliases", []):
            if k in alias.lower():
                add(term)
                matched = True
                break
        if matched:
            continue
        for def_text in rec.get("definitions", {}).values():
            if k in def_text.lower():
                add(term)
                break

    # 3) difflib 模糊匹配（补充）
    if len(results) < topn:
        pool = [a.lower() for a in ALL_ALIASES]
        close = get_close_matches(k, pool, n=topn, cutoff=0.5)
        for c in close:
            term = ALIAS_INDEX.get(c)
            if term:
                add(term)

    return results[:topn]


def get_standards_for_term(term: str) -> list[str]:
    """返回定义了该术语的所有标准列表（排序后）。"""
    rec = TERM_DB.get(term, {})
    return sorted(rec.get("definitions", {}).keys())


def match_standard(short: str) -> list[str]:
    """通过缩写、别名或子串匹配标准全名（不区分大小写）。"""
    s = short.lower()
    matched: list[str] = []
    for std in STD_INDEX:
        if s in std.lower():
            matched.append(std)
            continue
        aliases = STD_ALIASES.get(std, [])
        if any(s == a.lower() for a in aliases):
            matched.append(std)
    # 去重并保持顺序
    seen: set[str] = set()
    uniq: list[str] = []
    for m in matched:
        if m not in seen:
            seen.add(m)
            uniq.append(m)
    return uniq


def truncate(text: str, width: int = 80) -> str:
    """截断过长文本并添加省略号。"""
    if len(text) <= width:
        return text
    return text[: width - 3] + "..."


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    """生成 Markdown 表格（含简单的终端对齐）。"""
    if not rows:
        return ""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(cell))
    lines: list[str] = []
    lines.append(" | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)))
    lines.append(" | ".join("-" * col_widths[i] for i in range(len(headers))))
    for row in rows:
        lines.append(" | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row)))
    return "\n".join(lines)


def term_to_row(term: str, lang: str = "en", max_def_len: int = 60) -> list[str]:
    """将术语转换为表格行 [Term, Standards, Aliases, DefinitionSnippet]。"""
    rec = TERM_DB[term]
    stds = ", ".join(sorted(rec.get("definitions", {}).keys()))
    aliases = rec.get("aliases", [])
    if lang == "zh":
        zh_aliases = [a for a in aliases if re.search(r"[\u4e00-\u9fff]", a)]
        en_aliases = [a for a in aliases if not re.search(r"[\u4e00-\u9fff]", a)]
        aliases = zh_aliases + en_aliases
    alias_str = ", ".join(aliases) if aliases else "-"
    first_def = next(iter(rec.get("definitions", {}).values()), "")
    return [term, stds, alias_str, truncate(first_def, max_def_len)]


def print_results(
    results: list[str],
    lang: str = "en",
    json_mode: bool = False,
    title: str = "",
) -> None:
    """打印搜索结果（Markdown 表格或 JSON）。"""
    if json_mode:
        data = []
        for term in results:
            rec = TERM_DB[term]
            data.append(
                {
                    "term": term,
                    "aliases": rec.get("aliases", []),
                    "standards": list(rec.get("definitions", {}).keys()),
                    "definitions": rec.get("definitions", {}),
                    "related": rec.get("related", []),
                }
            )
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    if not results:
        print("未找到匹配的术语。" if lang == "zh" else "No matching terms found.")
        return

    if title:
        print(f"\n{title}\n")

    headers = ["Term", "Standards", "Aliases", "Definition"]
    if lang == "zh":
        headers = ["术语", "标准", "别名", "定义"]

    rows = [term_to_row(term, lang=lang) for term in results]
    print(markdown_table(headers, rows))
    print()


# ---------------------------------------------------------------------------
# 跨标准差异分析
# ---------------------------------------------------------------------------


def _extract_distinctive_phrases(a: str, b: str) -> tuple[list[str], list[str]]:
    """使用 SequenceMatcher 提取两段文本中相互替换/增删的片段。"""
    aw = a.split()
    bw = b.split()
    sm = SequenceMatcher(None, aw, bw)
    a_phrases: list[str] = []
    b_phrases: list[str] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            phrase = " ".join(aw[i1:i2])
            if phrase:
                a_phrases.append(phrase)
        if tag in ("replace", "insert"):
            phrase = " ".join(bw[j1:j2])
            if phrase:
                b_phrases.append(phrase)
    return a_phrases, b_phrases


def _highlight_definition_diff(a: str, b: str) -> tuple[str, str]:
    """返回用 [] 标出差异片段的两段定义。"""
    aw = a.split()
    bw = b.split()
    sm = SequenceMatcher(None, aw, bw)
    a_parts: list[str] = []
    b_parts: list[str] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            a_parts.append(" ".join(aw[i1:i2]))
            b_parts.append(" ".join(bw[j1:j2]))
        elif tag == "replace":
            a_parts.append("[" + " ".join(aw[i1:i2]) + "]")
            b_parts.append("[" + " ".join(bw[j1:j2]) + "]")
        elif tag == "delete":
            a_parts.append("[" + " ".join(aw[i1:i2]) + "]")
        elif tag == "insert":
            b_parts.append("[" + " ".join(bw[j1:j2]) + "]")
    return " ".join(a_parts), " ".join(b_parts)


def _hardcoded_diff_notes(canonical: str, lang: str = "en") -> list[str] | None:
    """返回硬编码的差异说明；若不存在返回 None。"""
    notes: list[str] = []
    if canonical == "Reusability":
        if lang == "zh":
            notes.append("- IEEE 1517-2010 强调资产在'其他系统'中复用，突出跨系统迁移能力。")
            notes.append("- ISO/IEC 25010:2023 强调资产在'多个系统'或'构建其他资产'中的通用程度。")
        else:
            notes.append("- IEEE 1517-2010 emphasizes reuse in 'other systems', highlighting cross-system portability.")
            notes.append("- ISO/IEC 25010:2023 emphasizes general usability across 'more than one system' or for building other assets.")
    elif canonical == "Domain Engineering":
        if lang == "zh":
            notes.append("- ISO/IEC 26550:2015 侧重产品线的共性与可变性管理，产出领域资产。")
            notes.append("- IEEE 1517-2010 侧重领域信息的识别与组织，以支持系统化复用。")
        else:
            notes.append("- ISO/IEC 26550:2015 focuses on commonality and variability management within a product line.")
            notes.append("- IEEE 1517-2010 focuses on identifying and organizing domain information to support systematic reuse.")
    elif canonical == "Application Engineering":
        if lang == "zh":
            notes.append("- ISO/IEC 26550:2015 强调利用产品线可变性构建单个产品。")
            notes.append("- IEEE 1517-2010 强调从复用库中选取合格资产来构造特定系统。")
        else:
            notes.append("- ISO/IEC 26550:2015 emphasizes exploiting product-line variability to build individual products.")
            notes.append("- IEEE 1517-2010 emphasizes selecting qualified assets from a reuse library to construct specific systems.")
    elif canonical == "Adaptation":
        if lang == "zh":
            notes.append("- IEEE 1517-2010 将适配视为针对特定目标系统的修改过程。")
            notes.append("- ISO/IEC 25010:2023 将适应性视为系统对环境变化的固有能力（质量特性）。")
        else:
            notes.append("- IEEE 1517-2010 treats adaptation as a modification process for a specific target system.")
            notes.append("- ISO/IEC 25010:2023 treats adaptability as an inherent quality characteristic for changing environments.")
    elif canonical == "Asset":
        if lang == "zh":
            notes.append("- IEEE 1517-2010 将资产视为复用候选（软件产品、工作产物）。")
            notes.append("- General 定义将资产视为系统中可替换的模块化部件（与 Component 类似）。")
        else:
            notes.append("- IEEE 1517-2010 treats an asset as a reuse candidate (software product or work product).")
            notes.append("- The General definition treats an asset as a replaceable modular part of a system, similar to Component.")
    return notes if notes else None


def auto_diff_notes(defs: dict[str, str], lang: str = "en") -> tuple[list[str], list[str]]:
    """
    自动生成差异说明。

    返回 (highlights, emphasis_notes)：
      - highlights: 带 [] 高亮的定义列表（每条一行）
      - emphasis_notes: "X 标准强调…" 提示列表
    """
    standards = list(defs.keys())
    highlights: list[str] = []
    emphasis_notes: list[str] = []
    if len(standards) < 2:
        return highlights, emphasis_notes

    for i in range(len(standards) - 1):
        s1, s2 = standards[i], standards[i + 1]
        d1, d2 = defs[s1], defs[s2]
        hd1, hd2 = _highlight_definition_diff(d1, d2)
        highlights.append(f"- **{s1}**: {hd1}")
        highlights.append(f"- **{s2}**: {hd2}")
        phrases1, phrases2 = _extract_distinctive_phrases(d1, d2)
        hint1 = " / ".join(phrases1[:2]) if phrases1 else "specific aspects"
        hint2 = " / ".join(phrases2[:2]) if phrases2 else "specific aspects"
        if lang == "zh":
            emphasis_notes.append(f"- {s1} 强调 {hint1}；{s2} 强调 {hint2}。")
        else:
            emphasis_notes.append(f"- {s1} emphasizes {hint1}; {s2} emphasizes {hint2}.")
    return highlights, emphasis_notes


def print_compare(
    term: str,
    standards: list[str] | None = None,
    lang: str = "en",
    json_mode: bool = False,
) -> int:
    """打印单个术语的跨标准对比。"""
    canonical = resolve_term(term)
    if not canonical:
        candidates = fuzzy_search(term, topn=5)
        if len(candidates) == 1:
            canonical = candidates[0]
            print(f"提示: 未找到 '{term}'，已自动匹配到 '{canonical}'。")
        elif candidates:
            print(
                f"未找到术语 '{term}'。您是否想搜索: {', '.join(candidates)}?"
            )
            return 1
        else:
            print(f"未找到术语: {term}")
            return 1

    rec = TERM_DB[canonical]
    defs = rec.get("definitions", {})
    available = sorted(defs.keys())

    if standards:
        filtered: list[str] = []
        for s in standards:
            matched = match_standard(s)
            if matched:
                filtered.extend(matched)
            else:
                print(
                    f"警告: 无法识别的标准 '{s}'"
                    if lang == "zh"
                    else f"Warning: unrecognized standard '{s}'"
                )
        selected = [s for s in filtered if s in defs]
        if not selected:
            selected = available
    else:
        selected = available

    if json_mode:
        data = {
            "term": canonical,
            "aliases": rec.get("aliases", []),
            "compare": {s: defs[s] for s in selected},
            "related": rec.get("related", []),
        }
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    print(f"\n{'【跨标准对比】' if lang == 'zh' else '[Cross-Standard Comparison]'} {canonical}\n")

    if len(selected) < 2:
        print(
            "（该术语仅在以下标准中有定义，无法进行对比）\n"
            if lang == "zh"
            else "(This term is only defined in one standard; no comparison available.)\n"
        )
        for s in selected:
            print(f"- **{s}**: {defs[s]}")
        print()
        return 0

    headers = ["Standard", "Definition"]
    if lang == "zh":
        headers = ["标准", "定义"]

    rows = [[s, defs[s]] for s in selected]
    print(markdown_table(headers, rows))
    print()

    # 差异分析：优先硬编码，否则自动生成
    selected_defs = {s: defs[s] for s in selected}
    hard_notes = _hardcoded_diff_notes(canonical, lang)
    print("**差异要点**:" if lang == "zh" else "**Key Differences**:")
    if hard_notes:
        for note in hard_notes:
            print(note)
    else:
        highlights, emphasis = auto_diff_notes(selected_defs, lang)
        if highlights:
            print("\n**自动差异高亮**:" if lang == "zh" else "\n**Automatic Difference Highlights**:")
            for line in highlights:
                print(line)
        if emphasis:
            print()
            for line in emphasis:
                print(line)
        if not highlights and not emphasis:
            print(
                "- 不同标准对该术语的侧重点和上下文有所不同，请结合具体标准文档深入理解。"
                if lang == "zh"
                else "- Different standards emphasize different aspects; refer to the original documents."
            )
    print()
    return 0


# ---------------------------------------------------------------------------
# 导出功能
# ---------------------------------------------------------------------------


def export_glossary_markdown(lang: str = "en") -> str:
    """按标准分组生成 Markdown 术语表。"""
    std_terms: dict[str, list[str]] = {}
    for term, rec in TERM_DB.items():
        for std in rec.get("definitions", {}):
            std_terms.setdefault(std, []).append(term)
    for std in std_terms:
        std_terms[std].sort(key=str.lower)

    lines: list[str] = []
    title = "# 跨标准术语表" if lang == "zh" else "# Cross-Standard Glossary"
    lines.append(title)
    lines.append("")
    lines.append(f"> 生成时间: {__import__('datetime').datetime.now().isoformat(timespec='minutes')}" if lang == "zh" else f"> Generated: {__import__('datetime').datetime.now().isoformat(timespec='minutes')}")
    lines.append("")

    for std in sorted(std_terms.keys(), key=str.lower):
        terms = std_terms[std]
        lines.append(f"## {std}")
        lines.append("")
        headers = ["术语" if lang == "zh" else "Term", "别名" if lang == "zh" else "Aliases", "定义" if lang == "zh" else "Definition"]
        rows: list[list[str]] = []
        for term in terms:
            rec = TERM_DB[term]
            aliases = rec.get("aliases", [])
            alias_str = ", ".join(aliases) if aliases else "-"
            definition = rec["definitions"][std]
            rows.append([term, alias_str, definition])
        lines.append(markdown_table(headers, rows))
        lines.append("")
    return "\n".join(lines)


def export_glossary_json() -> str:
    """导出完整数据库为 JSON 字符串。"""
    data = {
        "terms": TERM_DB,
        "aliases": STD_ALIASES,
        "version_hints": STD_VERSION_HINTS,
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def export_glossary_yaml() -> str:
    """导出完整数据库为 YAML 字符串（YAML 不可用时回退 JSON）。"""
    data = {
        "terms": TERM_DB,
        "aliases": STD_ALIASES,
        "version_hints": STD_VERSION_HINTS,
    }
    if HAS_YAML:
        return yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120)
    return json.dumps(data, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Markdown 表格解析与同步
# ---------------------------------------------------------------------------


def parse_markdown_tables(md_text: str) -> list[list[list[str]]]:
    """
    解析 Markdown 文本中的所有表格。

    返回: [table, table, ...]，每个 table 是 [row, ...]，每个 row 是 [cell, ...]。
    """
    lines = md_text.splitlines()
    tables: list[list[list[str]]] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if "|" in line and not line.startswith("#"):
            table_lines: list[str] = []
            while i < len(lines) and "|" in lines[i]:
                table_lines.append(lines[i].strip())
                i += 1
            rows: list[list[str]] = []
            for tl in table_lines:
                cells = [c.strip() for c in tl.split("|")]
                # 去掉因首/尾 | 产生的空单元
                if cells and cells[0] == "":
                    cells = cells[1:]
                if cells and cells[-1] == "":
                    cells = cells[:-1]
                # 跳过分隔行
                if cells and all(re.fullmatch(r"[-:]+", c.strip(" ")) for c in cells):
                    continue
                if cells:
                    rows.append(cells)
            if rows:
                tables.append(rows)
        else:
            i += 1
    return tables


def _extract_parenthetical_aliases(text: str) -> list[str]:
    """从 'Architecture Description (AD)' 中提取 'AD' 等别名。"""
    aliases: list[str] = []
    for m in re.finditer(r"\(([^)]+)\)", text):
        aliases.append(m.group(1).strip())
    return aliases


def _split_slash_terms(text: str) -> list[str]:
    """将 'Architecture Repository / Catalog' 拆分为多个候选别名。"""
    parts = [p.strip() for p in re.split(r"[/\\]+", text)]
    return [p for p in parts if p]


def _normalize_term(text: str) -> str:
    """清理术语单元格中的文本（去掉括号别名、首尾空白、Markdown 加粗）。"""
    text = re.sub(r"\*+", "", text).strip()
    text = re.sub(r"\s*\([^)]*\)", "", text).strip()
    return text


def _looks_like_term(text: str) -> bool:
    """启发式判断文本是否像术语而非年份/版本号/日期。"""
    if not text or len(text) <= 1:
        return False
    # 过滤纯数字、纯版本号、日期
    if re.fullmatch(r"\d{4}", text):
        return False
    if re.fullmatch(r"v\d+.*|v0\.\d+|\d{4}-\d{2}(-\d{2})?", text, re.IGNORECASE):
        return False
    # 至少包含字母或中文字符
    if not re.search(r"[a-zA-Z\u4e00-\u9fff]", text):
        return False
    return True


def _is_crosswalk_table(headers: list[str]) -> bool:
    """启发式判断表格是否为术语对照表（排除变更日志、版本对照表、权威来源表）。"""
    lower_headers = [h.lower() for h in headers]
    joined = " ".join(lower_headers)
    # 排除变更日志
    if any(k in joined for k in ("日期", "变更", "责任人")):
        return False
    # 排除旧版/新版对比表
    if "旧版" in joined or "新版" in joined:
        return False
    # 排除权威来源/标准索引表（含 URL、状态、备注等元信息列）
    if any(k in joined for k in ("官方 url", "url", "状态", "备注")):
        return False
    return True


def extract_crosswalk_terms(tables: list[list[list[str]]]) -> dict[str, dict[str, Any]]:
    """
    从术语对照表中提取已存在术语的别名与跨标准映射。

    策略：
      - 仅把已存在于数据库的术语作为锚点，收集同义词/跨标准映射。
      - 不自动创建新术语，避免把对照表中大量映射对象误判为术语。

    返回结构示例：
      {
        "Architecture Description": {
          "aliases": ["AD", "Architecture Repository", "Catalog"],
          "related_standards": ["TOGAF 10"],
        }
      }
    """
    result: dict[str, dict[str, Any]] = {}

    def ensure(term: str) -> dict[str, Any]:
        if term not in result:
            result[term] = {"aliases": [], "related_standards": []}
        return result[term]

    for table in tables:
        if len(table) < 2:
            continue
        headers = table[0]
        if len(headers) < 2:
            continue
        if not _is_crosswalk_table(headers):
            continue

        # 识别标准名列（排除说明/含义/对应主题列）
        std_cols: list[tuple[int, str]] = []
        for idx, h in enumerate(headers):
            h_lower = h.lower()
            if any(k in h_lower for k in ("说明", "含义", "通用", "对应主题", "关键变化")):
                continue
            if re.search(r"\d{4}", h) or h in ("SLSA", "SBOM", "A2A", "UML", "OPC UA", "ISA-95", "MCP", "A2A v1.0"):
                std_cols.append((idx, h))
        if not std_cols:
            std_cols = [(0, headers[0]), (1, headers[1])]

        for row in table[1:]:
            if len(row) < max(idx for idx, _ in std_cols) + 1:
                continue

            # 只把已存在的术语作为锚点
            for idx, std in std_cols:
                if idx >= len(row):
                    continue
                raw = row[idx]
                normalized = _normalize_term(raw)
                canonical = resolve_term(normalized)
                if not canonical:
                    continue
                rec = ensure(canonical)
                # 收集当前单元格中的别名
                for alias in _extract_parenthetical_aliases(raw):
                    if alias not in rec["aliases"]:
                        rec["aliases"].append(alias)
                for alias in _split_slash_terms(raw):
                    if alias.lower() != canonical.lower() and alias not in rec["aliases"]:
                        rec["aliases"].append(alias)
                # 跨列收集别名和相关标准
                for other_idx, other_std in std_cols:
                    if other_idx == idx or other_idx >= len(row):
                        continue
                    other_raw = row[other_idx]
                    other_norm = _normalize_term(other_raw)
                    if not other_norm:
                        continue
                    other_canonical = resolve_term(other_norm)
                    if other_canonical:
                        if other_std not in rec["related_standards"]:
                            rec["related_standards"].append(other_std)
                    else:
                        # 其他单元格作为别名候选（过滤年份/版本号）
                        for alias in _extract_parenthetical_aliases(other_raw):
                            if alias not in rec["aliases"]:
                                rec["aliases"].append(alias)
                        for alias in _split_slash_terms(other_raw):
                            if alias.lower() != canonical.lower() and alias not in rec["aliases"]:
                                rec["aliases"].append(alias)
                        if _looks_like_term(other_norm) and other_norm not in rec["aliases"]:
                            rec["aliases"].append(other_norm)

    return result


def extract_authoritative_sources(tables: list[list[list[str]]]) -> dict[str, dict[str, str]]:
    """
    从 authoritative-sources-v2.md 表格中提取标准版本提示。

    期望列：标准/框架, 版本, 状态, 官方 URL, 备注
    过滤：跳过非标准表格（如只有 旧版/新版 的对比表）、变更日志行。
    """
    hints: dict[str, dict[str, str]] = {}
    for table in tables:
        if len(table) < 2:
            continue
        headers = [h.strip().lower() for h in table[0]]
        # 必须有“版本”列，且不能是“旧版/新版”这类对比列
        ver_idx = _find_header_index(headers, ["版本", "version", "edition"])
        if ver_idx is None:
            continue
        if "旧版" in headers[ver_idx] or "新版" in headers[ver_idx]:
            continue
        std_idx = _find_header_index(headers, ["标准/框架", "标准", "框架", "standard", "framework"])
        status_idx = _find_header_index(headers, ["状态", "status"])
        note_idx = _find_header_index(headers, ["备注", "note", "notes", "说明"])
        if std_idx is None:
            continue
        for row in table[1:]:
            if std_idx >= len(row) or ver_idx >= len(row):
                continue
            std_raw = row[std_idx].strip()
            version = row[ver_idx].strip()
            if not std_raw or not version:
                continue
            # 清理 Markdown 加粗与链接
            std_name = re.sub(r"\*+", "", std_raw).strip()
            version = re.sub(r"\*+", "", version).strip()
            # 跳过变更日志/日期行
            if re.fullmatch(r"\d{4}-\d{2}(-\d{2})?", std_name):
                continue
            if "变更" in std_name or "责任人" in std_name:
                continue
            status = ""
            if status_idx is not None and status_idx < len(row):
                status = re.sub(r"\*+", "", row[status_idx]).strip()
            note = ""
            if note_idx is not None and note_idx < len(row):
                note = re.sub(r"\*+", "", row[note_idx]).strip()
            # 同名标准保留首次出现（如 ArchiMate 4.0 / 3.2 应分别处理，
            # 但来源中名称相同，避免后者覆盖前者）
            if std_name not in hints:
                hints[std_name] = {"version": version, "status": status, "note": note}
    return hints


def _find_header_index(headers: list[str], candidates: list[str]) -> int | None:
    """根据候选名称查找列头索引。"""
    for cand in candidates:
        for idx, h in enumerate(headers):
            if cand in h:
                return idx
    return None


def _add_aliases(rec: dict[str, Any], target: str, aliases: list[str]) -> None:
    """把一组别名去重后添加到术语记录中。"""
    existing = {a.lower() for a in rec.get("aliases", [])}
    existing.add(target.lower())
    for alias in aliases:
        clean = alias.strip()
        if not clean or clean.lower() in existing:
            continue
        # 过滤过长或包含表格说明文字的别名
        if len(clean) > 120:
            continue
        rec.setdefault("aliases", []).append(clean)
        existing.add(clean.lower())


def _merge_sync_changes(
    current: dict[str, Any],
    crosswalk: dict[str, dict[str, Any]],
    hints: dict[str, dict[str, str]],
) -> dict[str, Any]:
    """计算合并后的数据库。"""
    new = {
        "terms": json.loads(json.dumps(current.get("terms", {}))),
        "aliases": json.loads(json.dumps(current.get("aliases", {}))),
        "version_hints": json.loads(json.dumps(current.get("version_hints", {}))),
    }

    # 应用 crosswalk 别名/相关标准
    for term, info in crosswalk.items():
        canonical = resolve_term(term)
        target = canonical if canonical else term
        if target not in new["terms"]:
            new["terms"][target] = {"definitions": {}, "aliases": [], "related": []}
        rec = new["terms"][target]
        _add_aliases(rec, target, info.get("aliases", []))
        for std in info.get("related_standards", []):
            if std not in rec.get("related", []):
                rec.setdefault("related", []).append(std)

    # 应用 version hints（仅更新已存在的标准，避免引入大量外部标准噪音）
    for std_name, hint in hints.items():
        existing_std = _match_existing_standard(std_name, new["aliases"])
        if not existing_std:
            continue
        old = new["version_hints"].get(existing_std, {})
        new_hint = {
            "version": hint.get("version", old.get("version", "")),
            "status": hint.get("status", old.get("status", "")),
            "note": hint.get("note", old.get("note", "")),
        }
        new["version_hints"][existing_std] = new_hint

    return new


def _match_existing_standard(std_name: str, aliases: dict[str, list[str]]) -> str | None:
    """尝试将来源中的标准名匹配到现有标准名。"""
    s = std_name.lower()
    for std, alias_list in aliases.items():
        if std.lower() == s:
            return std
        if s in std.lower():
            return std
        for a in alias_list:
            if a.lower() == s:
                return std
    # 特殊规则：去掉 Edition 等后缀
    base = re.sub(r"\s+(standard|edition|v\d+.*)$", "", s, flags=re.IGNORECASE).strip()
    for std in aliases:
        if base in std.lower():
            return std
    return None


def compute_sync_diff(
    current: dict[str, Any],
    crosswalk: dict[str, dict[str, Any]],
    hints: dict[str, dict[str, str]],
) -> dict[str, Any]:
    """计算 dry-run 差异摘要。"""
    diff: dict[str, Any] = {"new_terms": [], "new_aliases": [], "new_hints": [], "updated_hints": []}
    current_terms = current.get("terms", {})

    for term, info in crosswalk.items():
        canonical = resolve_term(term)
        target = canonical if canonical else term
        if target not in current_terms:
            diff["new_terms"].append(target)
        else:
            rec = current_terms[target]
            existing_lower = {a.lower() for a in rec.get("aliases", [])}
            existing_lower.add(target.lower())
            for alias in info.get("aliases", []):
                clean = alias.strip()
                if not clean or clean.lower() in existing_lower:
                    continue
                if len(clean) > 120:
                    continue
                diff["new_aliases"].append((target, clean))
                existing_lower.add(clean.lower())

    current_hints = current.get("version_hints", {})
    for std_name, hint in hints.items():
        existing_std = _match_existing_standard(std_name, current.get("aliases", {}))
        if not existing_std:
            continue
        if existing_std not in current_hints:
            diff["new_hints"].append((existing_std, hint))
        elif current_hints[existing_std] != hint:
            diff["updated_hints"].append((existing_std, current_hints[existing_std], hint))

    return diff


# ---------------------------------------------------------------------------
# 命令处理
# ---------------------------------------------------------------------------


def cmd_search(args: argparse.Namespace) -> int:
    """search 命令：中英文模糊搜索。"""
    keyword = args.keyword
    lang = args.lang or "en"
    results = fuzzy_search(keyword, lang=lang, topn=20)

    if not results:
        print("未找到匹配的术语。" if lang == "zh" else "No matching terms found.")
        close = get_close_matches(
            keyword.lower(), [a.lower() for a in ALL_ALIASES], n=5, cutoff=0.4
        )
        if close:
            terms = sorted({ALIAS_INDEX[c] for c in close if c in ALIAS_INDEX})
            print(
                ("您是否想找: " if lang == "zh" else "Did you mean: ")
                + ", ".join(terms)
                + "?"
            )
        return 1

    if args.compare:
        if len(results) == 1:
            return print_compare(results[0], lang=lang, json_mode=args.json)
        else:
            print(
                "找到多个术语，无法直接进入对比模式。请缩小搜索范围后使用 --compare。"
                if lang == "zh"
                else "Multiple terms found; cannot enter compare mode. Please refine your search."
            )
            title = (
                f"找到 {len(results)} 条与 '{keyword}' 相关的结果:"
                if lang == "zh"
                else f"Found {len(results)} result(s) for '{keyword}':"
            )
            print_results(results, lang=lang, json_mode=args.json, title=title)
            return 1

    title = (
        f"找到 {len(results)} 条与 '{keyword}' 相关的结果:"
        if lang == "zh"
        else f"Found {len(results)} result(s) for '{keyword}':"
    )
    print_results(results, lang=lang, json_mode=args.json, title=title)
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    """compare 命令：跨标准对比单个术语。"""
    standards = [s.strip() for s in args.standards.split(",")] if args.standards else None
    return print_compare(
        args.term, standards=standards, lang=args.lang or "en", json_mode=args.json
    )


def cmd_list(args: argparse.Namespace) -> int:
    """list 命令：列出指定标准下的术语。"""
    lang = args.lang or "en"
    matched = match_standard(args.standard)
    if not matched:
        print(
            ("未找到标准: " if lang == "zh" else "Standard not found: ") + args.standard
        )
        available = sorted(STD_INDEX.keys())
        print(
            ("可用标准: " if lang == "zh" else "Available standards: ")
            + ", ".join(available)
        )
        return 1

    results: list[str] = []
    for m in matched:
        results.extend(STD_INDEX[m])
    seen: set[str] = set()
    unique_results: list[str] = []
    for t in results:
        if t not in seen:
            seen.add(t)
            unique_results.append(t)
    unique_results.sort()

    if args.json:
        data = []
        for term in unique_results:
            rec = TERM_DB[term]
            data.append(
                {
                    "term": term,
                    "aliases": rec.get("aliases", []),
                    "standards": list(rec.get("definitions", {}).keys()),
                    "definitions": rec.get("definitions", {}),
                    "related": rec.get("related", []),
                }
            )
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    if lang == "zh":
        print(f"\n【标准列表】{', '.join(matched)} ({len(unique_results)} 条术语)\n")
    else:
        print(f"\n[Standard List] {', '.join(matched)} ({len(unique_results)} terms)\n")

    headers = ["Term", "Aliases"]
    if lang == "zh":
        headers = ["术语", "别名"]

    rows = []
    for term in unique_results:
        rec = TERM_DB[term]
        aliases = rec.get("aliases", [])
        if lang == "zh":
            zh_aliases = [a for a in aliases if re.search(r"[\u4e00-\u9fff]", a)]
            en_aliases = [a for a in aliases if not re.search(r"[\u4e00-\u9fff]", a)]
            aliases = zh_aliases + en_aliases
        alias_str = ", ".join(aliases) if aliases else "-"
        rows.append([term, alias_str])

    print(markdown_table(headers, rows))
    print()
    return 0


def cmd_version_hint(args: argparse.Namespace) -> int:
    """version-hint 命令：显示术语相关标准的权威版本提示。"""
    lang = args.lang or "en"
    term = resolve_term(args.term)
    if not term:
        print(("未找到术语: " if lang == "zh" else "Term not found: ") + args.term)
        return 1

    rec = TERM_DB[term]
    standards = list(rec.get("definitions", {}).keys())

    if args.json:
        data = {"term": term, "standards": []}
        for std in standards:
            hint = STD_VERSION_HINTS.get(std, {})
            data["standards"].append({
                "standard": std,
                "version": hint.get("version", "未知"),
                "status": hint.get("status", "未知"),
                "note": hint.get("note", ""),
            })
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    if lang == "zh":
        print(f"\n【术语】{term}")
        print(f"【相关标准权威版本提示】\n")
        headers = ["标准", "版本", "状态", "备注"]
    else:
        print(f"\n[Term] {term}")
        print(f"[Authoritative Version Hints]\n")
        headers = ["Standard", "Version", "Status", "Note"]

    rows = []
    for std in standards:
        hint = STD_VERSION_HINTS.get(std, {})
        rows.append([
            std,
            hint.get("version", "未知"),
            hint.get("status", "未知"),
            hint.get("note", ""),
        ])
    print(markdown_table(headers, rows))
    print()
    return 0


def cmd_export_glossary(args: argparse.Namespace) -> int:
    """export-glossary 命令：按标准分组导出术语表。"""
    fmt = (args.format or "md").lower()
    output = args.output
    lang = args.lang or "en"

    if fmt == "md":
        content = export_glossary_markdown(lang=lang)
    elif fmt == "json":
        content = export_glossary_json()
    elif fmt == "yaml":
        content = export_glossary_yaml()
    else:
        print(f"不支持的格式: {fmt}（支持 md/json/yaml）")
        return 1

    if output:
        out_path = Path(output)
        out_path.write_text(content, encoding="utf-8")
        print(f"已导出到: {out_path.resolve()}")
    else:
        print(content)
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    """sync 命令：从 Markdown 来源同步术语/别名/版本提示（默认 dry-run）。"""
    lang = args.lang or "en"
    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    apply = args.apply

    all_crosswalk: dict[str, dict[str, Any]] = {}
    all_hints: dict[str, dict[str, str]] = {}

    for src in sources:
        path = Path(src)
        if not path.exists():
            print(("来源不存在: " if lang == "zh" else "Source not found: ") + src)
            return 1
        md_text = path.read_text(encoding="utf-8")
        tables = parse_markdown_tables(md_text)
        cw = extract_crosswalk_terms(tables)
        hints = extract_authoritative_sources(tables)
        for term, info in cw.items():
            if term not in all_crosswalk:
                all_crosswalk[term] = {"aliases": [], "related_standards": []}
            all_crosswalk[term]["aliases"].extend(info.get("aliases", []))
            all_crosswalk[term]["related_standards"].extend(info.get("related_standards", []))
        all_hints.update(hints)

    current = {
        "terms": TERM_DB,
        "aliases": STD_ALIASES,
        "version_hints": STD_VERSION_HINTS,
    }
    diff = compute_sync_diff(current, all_crosswalk, all_hints)

    if apply:
        new_db = _merge_sync_changes(current, all_crosswalk, all_hints)
        saved_path = save_db(new_db)
        init_globals(new_db)
        print(f"已应用同步并保存到: {saved_path}")

    if lang == "zh":
        print("\n【同步差异预览】\n")
        print(f"来源文件: {', '.join(sources)}")
        print(f"模式: {'应用更新' if apply else 'dry-run（仅预览）'}\n")
        if diff["new_terms"]:
            print("新增术语:")
            for t in diff["new_terms"]:
                print(f"  + {t}")
        if diff["new_aliases"]:
            print("新增别名:")
            for term, alias in diff["new_aliases"]:
                print(f"  + {term}: {alias}")
        if diff["new_hints"]:
            print("新增版本提示:")
            for std, hint in diff["new_hints"]:
                print(f"  + {std}: {hint}")
        if diff["updated_hints"]:
            print("更新版本提示:")
            for std, old, new in diff["updated_hints"]:
                print(f"  ~ {std}: {old} -> {new}")
        if not any(diff.values()):
            print("未发现差异。")
    else:
        print("\n[Sync Diff Preview]\n")
        print(f"Sources: {', '.join(sources)}")
        print(f"Mode: {'apply' if apply else 'dry-run'}\n")
        if diff["new_terms"]:
            print("New terms:")
            for t in diff["new_terms"]:
                print(f"  + {t}")
        if diff["new_aliases"]:
            print("New aliases:")
            for term, alias in diff["new_aliases"]:
                print(f"  + {term}: {alias}")
        if diff["new_hints"]:
            print("New version hints:")
            for std, hint in diff["new_hints"]:
                print(f"  + {std}: {hint}")
        if diff["updated_hints"]:
            print("Updated version hints:")
            for std, old, new in diff["updated_hints"]:
                print(f"  ~ {std}: {old} -> {new}")
        if not any(diff.values()):
            print("No differences found.")
    print()
    return 0


# ---------------------------------------------------------------------------
# 单元测试
# ---------------------------------------------------------------------------


def run_tests() -> int:
    """运行内置简单单元测试，验证核心检索、对比、导出与同步功能。"""
    import datetime  # noqa: F401  # 供 export_glossary_markdown 动态导入使用

    errors = 0

    def check(cond: bool, msg: str) -> None:
        nonlocal errors
        if not cond:
            print(f"[FAIL] {msg}")
            errors += 1

    # 1. 别名解析
    check(resolve_term("AD") == "Architecture Description", "resolve_term AD")
    check(resolve_term("架构描述") == "Architecture Description", "resolve_term 架构描述")
    check(resolve_term("mcp") == "Model Context Protocol", "resolve_term mcp")
    check(resolve_term("视点") == "Viewpoint", "resolve_term 视点")
    check(resolve_term("SBB") == "Solution Building Block", "resolve_term SBB")

    # 2. 模糊搜索
    res = fuzzy_search("reus")
    check("Reusability" in res, f"fuzzy_search 'reus' -> {res}")
    res = fuzzy_search("复用")
    check(
        "Reusability" in res or "Reuse Library" in res,
        f"fuzzy_search '复用' -> {res}",
    )
    res = fuzzy_search("模型上下文")
    check("Model Context Protocol" in res, f"fuzzy_search '模型上下文' -> {res}")

    # 3. 标准匹配
    ms = match_standard("togaf10")
    check(any("TOGAF 10" in m for m in ms), f"match_standard togaf10 -> {ms}")
    ms = match_standard("ieee1517")
    check(any("IEEE 1517-2010" in m for m in ms), f"match_standard ieee1517 -> {ms}")
    ms = match_standard("slsa")
    check(any("SLSA 1.2" in m for m in ms), f"match_standard slsa -> {ms}")
    ms = match_standard("mcp")
    check(any("MCP 2025-11-25" in m for m in ms), f"match_standard mcp -> {ms}")

    # 4. 跨标准术语
    stds = get_standards_for_term("Reusability")
    check(len(stds) >= 2, f"Reusability standards >= 2, got {stds}")
    stds = get_standards_for_term("Domain Engineering")
    check(len(stds) >= 2, f"Domain Engineering standards >= 2, got {stds}")
    stds = get_standards_for_term("Adaptation")
    check(len(stds) >= 2, f"Adaptation standards >= 2, got {stds}")

    # 5. Markdown 表格
    table = markdown_table(["A", "B"], [["1", "2"], ["3", "4"]])
    check("|" in table, "markdown_table generation")

    # 6. 版本提示
    check(
        "ISO/IEC 25010:2023" in STD_VERSION_HINTS,
        "STD_VERSION_HINTS contains ISO/IEC 25010:2023",
    )
    check(
        "NIST SSDF 1.2" in STD_VERSION_HINTS,
        "STD_VERSION_HINTS contains NIST SSDF 1.2",
    )

    # 7. 数据库规模
    check(len(TERM_DB) >= 30, f"term count >= 30, got {len(TERM_DB)}")
    check(len(STD_INDEX) >= 6, f"standard count >= 6, got {len(STD_INDEX)}")

    # 8. YAML 加载
    if HAS_YAML:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8"
        ) as f:
            yaml.safe_dump({"terms": {}, "aliases": {}, "version_hints": {}}, f)
            empty_yaml = f.name
        loaded = load_db(yaml_path=empty_yaml)
        check(isinstance(loaded, dict) and "terms" in loaded, "load_db yaml")
        os.unlink(empty_yaml)
    else:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump({"terms": {}, "aliases": {}, "version_hints": {}}, f)
            empty_json = f.name
        loaded = load_db(json_path=empty_json)
        check(isinstance(loaded, dict) and "terms" in loaded, "load_db json")
        os.unlink(empty_json)

    # 9. export-glossary
    md_glossary = export_glossary_markdown(lang="zh")
    check("Architecture Description" in md_glossary, "export_glossary_markdown contains term")
    check("## ISO/IEC/IEEE 42010:2022" in md_glossary, "export_glossary_markdown grouped by standard")
    json_glossary = export_glossary_json()
    check("\"terms\"" in json_glossary, "export_glossary_json contains terms key")

    # 10. sync diff 输出（dry-run）
    sample_md = "## 测试\n\n| ISO 42010:2022 | TOGAF 10 | 说明 |\n|---|---|---|\n| Architecture Description (AD) | Architecture Repository | 架构描述载体 |\n"
    sample_tables = parse_markdown_tables(sample_md)
    check(len(sample_tables) >= 1, "parse_markdown_tables finds table")
    cw = extract_crosswalk_terms(sample_tables)
    check(any("Architecture Description" in k for k in cw), "extract_crosswalk_terms finds AD")

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        # 构造一个模拟 Namespace
        sync_args = argparse.Namespace(
            sources="dummy-not-exist.md",
            apply=False,
            lang="zh",
        )
        # 使用真实临时文件
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(sample_md)
            temp_md = f.name
        sync_args.sources = temp_md
        ret = cmd_sync(sync_args)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        os.unlink(temp_md)
        check(ret == 0, "cmd_sync dry-run returns 0")
        check("同步差异预览" in output or "Sync Diff Preview" in output, "cmd_sync prints diff preview")
        check("Architecture Description" in output, "cmd_sync preview mentions Architecture Description")
    finally:
        sys.stdout = old_stdout

    # 11. 自动差异标注
    highlights, emphasis = auto_diff_notes(
        {
            "Std-A": "A reusable software asset for many systems.",
            "Std-B": "A reusable component used in other systems.",
        },
        lang="zh",
    )
    check(len(emphasis) >= 1, "auto_diff_notes generates emphasis")

    if errors == 0:
        print("所有单元测试通过。")
    else:
        print(f"单元测试失败: {errors} 项。")
    return errors


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="术语查询脚本 v3.0 — 跨标准术语定义、对比与检索 CLI 工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python terminology-query.py search "architecture view"
  python terminology-query.py search "复用" --lang zh
  python terminology-query.py compare "reusability" --standards iso25010,ieee1517
  python terminology-query.py list --standard togaf10
  python terminology-query.py version-hint "reusability" --lang zh
  python terminology-query.py export-glossary --format md --output glossary.md
  python terminology-query.py export-glossary --format json --output glossary.json
  python terminology-query.py sync --sources struct/99-reference/glossary/terminology-crosswalk.md
  python terminology-query.py sync --sources crosswalk.md,authoritative.md --apply
  python terminology-query.py --test
        """,
    )
    parser.add_argument("--test", action="store_true", help="运行内置单元测试")
    parser.add_argument("--version", action="version", version="%(prog)s 3.0")

    sub = parser.add_subparsers(dest="command", help="可用命令")

    # search
    p_search = sub.add_parser("search", help="中英文模糊搜索术语（支持别名、子串、difflib 近似匹配）")
    p_search.add_argument("keyword", help="搜索关键词")
    p_search.add_argument("--lang", choices=["zh", "en"], default="en", help="输出语言偏好")
    p_search.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    p_search.add_argument(
        "--compare",
        action="store_true",
        help="若只匹配到一个术语，直接进入跨标准对比模式",
    )

    # compare
    p_compare = sub.add_parser("compare", help="跨标准对比单个术语的定义差异")
    p_compare.add_argument("term", help="要对比的术语（支持别名）")
    p_compare.add_argument(
        "--standards",
        default=None,
        help="指定对比的标准（逗号分隔，如 iso25010,ieee1517）",
    )
    p_compare.add_argument("--lang", choices=["zh", "en"], default="en", help="输出语言偏好")
    p_compare.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    # list
    p_list = sub.add_parser("list", help="列出指定标准下的所有术语")
    p_list.add_argument(
        "--standard",
        required=True,
        help="标准名称或缩写（如 togaf10, iso42010, slsa, mcp）",
    )
    p_list.add_argument("--lang", choices=["zh", "en"], default="en", help="输出语言偏好")
    p_list.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    # version-hint
    p_hint = sub.add_parser("version-hint", help="显示术语相关标准的权威版本提示")
    p_hint.add_argument("term", help="要查询的术语（支持别名）")
    p_hint.add_argument("--lang", choices=["zh", "en"], default="en", help="输出语言偏好")
    p_hint.add_argument("--json", action="store_true", help="以 JSON 格式输出")

    # export-glossary
    p_export = sub.add_parser("export-glossary", help="按标准分组导出生词表")
    p_export.add_argument(
        "--format",
        choices=["md", "json", "yaml"],
        default="md",
        help="导出格式（默认 md）",
    )
    p_export.add_argument(
        "--output",
        default=None,
        help="输出文件路径（默认输出到 stdout）",
    )
    p_export.add_argument("--lang", choices=["zh", "en"], default="en", help="输出语言偏好")

    # sync
    p_sync = sub.add_parser(
        "sync",
        help="从 Markdown 来源同步术语/别名/版本提示（默认 dry-run）",
    )
    p_sync.add_argument(
        "--sources",
        required=True,
        help="逗号分隔的 Markdown 来源文件路径",
    )
    p_sync.add_argument(
        "--apply",
        action="store_true",
        help="应用差异并更新外部数据库（否则仅预览）",
    )
    p_sync.add_argument("--lang", choices=["zh", "en"], default="en", help="输出语言偏好")

    args = parser.parse_args()

    if args.test:
        return run_tests()

    if args.command == "search":
        return cmd_search(args)
    elif args.command == "compare":
        return cmd_compare(args)
    elif args.command == "list":
        return cmd_list(args)
    elif args.command == "version-hint":
        return cmd_version_hint(args)
    elif args.command == "export-glossary":
        return cmd_export_glossary(args)
    elif args.command == "sync":
        return cmd_sync(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
