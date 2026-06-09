#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
术语查询脚本 v2.0 — 跨标准术语定义、对比与检索 CLI 工具

内置标准覆盖：
  - ISO/IEC/IEEE 42010:2022（架构描述术语）
  - ISO/IEC 26550:2015（产品线工程术语）
  - TOGAF 10（企业架构术语）
  - IEEE 1517-2010（复用过程术语）
  - SLSA 1.2（供应链安全术语）
  - MCP 2025-11-25（AI 协议术语）

用法示例：
    python terminology-query.py search "architecture view"
    python terminology-query.py search "复用" --lang zh
    python terminology-query.py compare "reusability" --standards iso25010,ieee1517
    python terminology-query.py list --standard togaf10
    python terminology-query.py --test

要求：Python 3.10+
"""

import argparse
import json
import re
import sys
from difflib import get_close_matches
from typing import Any

# ---------------------------------------------------------------------------
# 内置术语数据库（≥43 条，覆盖 6 大标准及其交叉定义）
# 结构：{term: {definitions: {标准: 定义}, aliases: [别名], related: [相关术语]}}
# ---------------------------------------------------------------------------

TERM_DB: dict[str, dict[str, Any]] = {
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
            "ISO/IEC 25010:2024": (
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
            "ISO/IEC 25010:2024": (
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

# ---------------------------------------------------------------------------
# 标准别名映射（支持缩写/简写搜索）
# ---------------------------------------------------------------------------

STD_ALIASES: dict[str, list[str]] = {
    "ISO/IEC/IEEE 42010:2022": ["iso42010", "ieee42010", "42010", "iso_iec_ieee_42010"],
    "ISO/IEC 26550:2015": ["iso26550", "26550", "ple", "iso_iec_26550"],
    "TOGAF 10": ["togaf", "togaf10"],
    "IEEE 1517-2010": ["ieee1517", "1517"],
    "SLSA 1.2": ["slsa", "slsa1.2", "slsa12"],
    "MCP 2025-11-25": ["mcp", "mcp2025"],
    "ISO/IEC 25010:2024": ["iso25010", "25010", "iso_iec_25010"],
    "General": ["general"],
}

# ---------------------------------------------------------------------------
# 索引构建
# ---------------------------------------------------------------------------


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


ALIAS_INDEX, STD_INDEX, ALL_ALIASES = _build_indices()

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

    # 差异分析（内置启发式说明）
    print("**差异要点**:" if lang == "zh" else "**Key Differences**:")
    notes: list[str] = []
    if canonical == "Reusability":
        notes.append("- IEEE 1517-2010 强调资产在'其他系统'中复用，突出跨系统迁移能力。")
        notes.append("- ISO/IEC 25010:2024 强调资产在'多个系统'或'构建其他资产'中的通用程度。")
    elif canonical == "Domain Engineering":
        notes.append("- ISO/IEC 26550:2015 侧重产品线的共性与可变性管理，产出领域资产。")
        notes.append("- IEEE 1517-2010 侧重领域信息的识别与组织，以支持系统化复用。")
    elif canonical == "Application Engineering":
        notes.append("- ISO/IEC 26550:2015 强调利用产品线可变性构建单个产品。")
        notes.append("- IEEE 1517-2010 强调从复用库中选取合格资产来构造特定系统。")
    elif canonical == "Adaptation":
        notes.append("- IEEE 1517-2010 将适配视为针对特定目标系统的修改过程。")
        notes.append("- ISO/IEC 25010:2024 将适应性视为系统对环境变化的固有能力（质量特性）。")
    elif canonical == "Asset":
        notes.append("- IEEE 1517-2010 将资产视为复用候选（软件产品、工作产物）。")
        notes.append("- General 定义将资产视为系统中可替换的模块化部件（与 Component 类似）。")
    else:
        notes.append(
            "- 不同标准对该术语的侧重点和上下文有所不同，请结合具体标准文档深入理解。"
            if lang == "zh"
            else "- Different standards emphasize different aspects; refer to the original documents."
        )
    for note in notes:
        print(note)
    print()
    return 0


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


# ---------------------------------------------------------------------------
# 单元测试
# ---------------------------------------------------------------------------


def run_tests() -> int:
    """运行内置简单单元测试，验证核心检索与对比功能。"""
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

    # 6. 数据库规模
    check(len(TERM_DB) >= 30, f"term count >= 30, got {len(TERM_DB)}")
    check(len(STD_INDEX) >= 6, f"standard count >= 6, got {len(STD_INDEX)}")

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
        description="术语查询脚本 v2.0 — 跨标准术语定义、对比与检索 CLI 工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python terminology-query.py search "architecture view"
  python terminology-query.py search "复用" --lang zh
  python terminology-query.py compare "reusability" --standards iso25010,ieee1517
  python terminology-query.py list --standard togaf10
  python terminology-query.py --test
        """,
    )
    parser.add_argument("--test", action="store_true", help="运行内置单元测试")
    parser.add_argument("--version", action="version", version="%(prog)s 2.0")

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

    args = parser.parse_args()

    if args.test:
        return run_tests()

    if args.command == "search":
        return cmd_search(args)
    elif args.command == "compare":
        return cmd_compare(args)
    elif args.command == "list":
        return cmd_list(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
