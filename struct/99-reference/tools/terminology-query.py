#!/usr/bin/env python3
"""
术语查询脚本 — 跨标准术语定义、对比与检索工具

用法:
    python terminology-query.py query <term>
    python terminology-query.py search <keyword>
    python terminology-query.py compare <term1> <term2>
    python terminology-query.py list --standard <std>
"""

import argparse
import sys
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# 内置术语数据库（≥30 条，跨 ISO 42010、TOGAF 10、产品线工程、软件复用）
# 每条记录: {definitions: {标准: 定义}, aliases: [别名], related: [相关术语]}
# ---------------------------------------------------------------------------
TERM_DB: Dict[str, Dict] = {
    # ISO 42010:2022
    "Viewpoint": {"definitions": {"ISO 42010:2022": "针对一组相关关注点的观察视角的规约，包括建模语言、符号、分析规则等。A specification of the conventions for constructing and using views."}, "aliases": ["视点", "视角"], "related": ["View", "Concern", "Stakeholder", "Model Kind"]},
    "View": {"definitions": {"ISO 42010:2022": "针对一组相关关注点，系统架构的表达。A representation of a whole system from the perspective of a related set of concerns."}, "aliases": ["视图", "架构视图"], "related": ["Viewpoint", "Concern", "Architecture Description"]},
    "Model Kind": {"definitions": {"ISO 42010:2022": "约定、语言、符号的规约，用于构建特定类型的模型。A kind of model defined by conventions for its construction and usage."}, "aliases": ["模型种类", "模型类型"], "related": ["Viewpoint", "View", "Model"]},
    "Concern": {"definitions": {"ISO 42010:2022": "利益相关者对系统的某一关注点或兴趣点。An interest in a system relevant to one or more of its stakeholders."}, "aliases": ["关注点"], "related": ["Stakeholder", "Viewpoint", "View"]},
    "Stakeholder": {"definitions": {"ISO 42010:2022": "对系统拥有关注点或利益的个人、团队或组织。An individual, team, or organization with interests in, or concerns relative to, a system."}, "aliases": ["利益相关者", "干系人"], "related": ["Concern", "Viewpoint"]},
    "Architecture Description": {"definitions": {"ISO 42010:2022": "用于表达架构的工作产物，由视图、视点规约和对应规则组成。A work product used to express an architecture."}, "aliases": ["架构描述", "AD"], "related": ["View", "Viewpoint", "Correspondence"]},
    "Correspondence": {"definitions": {"ISO 42010:2022": "不同架构描述元素之间的关联或映射关系。A relationship between two or more architecture description elements."}, "aliases": ["对应关系"], "related": ["Architecture Description", "View"]},
    # TOGAF 10
    "ABB": {"definitions": {"TOGAF 10": "描述架构某一单一方面的构成要素，通常独立于实现技术。Architecture Building Block: a constituent of the architecture model."}, "aliases": ["Architecture Building Block", "架构构建块"], "related": ["SBB", "Architecture Repository", "Building Block"]},
    "SBB": {"definitions": {"TOGAF 10": "实现一个或多个 ABB 的候选物理组件，对应具体实现。Solution Building Block: a candidate physical component that will realize one or more ABBs."}, "aliases": ["Solution Building Block", "解决方案构建块"], "related": ["ABB", "Building Block", "Implementation"]},
    "Architecture Repository": {"definitions": {"TOGAF 10": "存储所有架构相关产物的逻辑仓库，包括交付物、模型、模式等。A logical place to hold all architecture-related outputs."}, "aliases": ["架构仓库", "架构资源库"], "related": ["Enterprise Continuum", "Architecture Description"]},
    "Enterprise Continuum": {"definitions": {"TOGAF 10": "从通用基础架构到组织特定架构的资产谱系与分类方法。A view of the Architecture Repository for classifying architecture artifacts."}, "aliases": ["企业连续体"], "related": ["Architecture Repository", "Foundation Architecture"]},
    "ADM": {"definitions": {"TOGAF 10": "TOGAF 核心架构开发方法，包含预备、愿景、业务/应用/技术架构、迁移规划等阶段。Architecture Development Method."}, "aliases": ["Architecture Development Method", "架构开发方法"], "related": ["Architecture Repository", "Building Block"]},
    "Building Block": {"definitions": {"TOGAF 10": "业务、IT 或架构能力的潜在可复用组件。A potentially reusable component of business, IT, or architectural capability."}, "aliases": ["构建块"], "related": ["ABB", "SBB", "Reusability"]},
    # 产品线工程
    "Domain Engineering": {"definitions": {"PLE / ISO 26550": "定义和实现产品线共性与可变性的过程，产出领域资产。The process of defining and realizing the commonality and variability of the product line."}, "aliases": ["领域工程"], "related": ["Application Engineering", "Variability", "Commonality"]},
    "Application Engineering": {"definitions": {"PLE / ISO 26550": "通过复用领域资产并利用产品线可变性来构建单个产品。Building individual products by reusing domain assets and exploiting variability."}, "aliases": ["应用工程"], "related": ["Domain Engineering", "Variability", "Reusability"]},
    "Variability": {"definitions": {"PLE / ISO 26550": "软件资产在特定上下文中被有效扩展、变更、定制或配置的能力。The ability of a software artifact to be efficiently extended, changed, customized, or configured."}, "aliases": ["可变性", "变异性"], "related": ["Variability Model", "Commonality", "Adaptability"]},
    "Commonality": {"definitions": {"PLE / ISO 26550": "产品线所有成员共享的属性。Properties that are shared across all members of a product line."}, "aliases": ["共性", "公共性"], "related": ["Variability", "Domain Engineering"]},
    "Variability Model": {"definitions": {"PLE": "捕获和记录产品线可变性的模型，常以特征模型形式表达。A model that captures and documents the variability of a product line."}, "aliases": ["可变性模型", "特征模型"], "related": ["Variability", "Feature Model", "Domain Engineering"]},
    # 软件复用
    "Reusability": {"definitions": {"ISO 25010:2024": "资产能在多个系统或多个资产构建中被使用的程度。The degree to which an asset can be used in more than one system.", "NASA RRL": "软件资产在很少或不做修改的情况下再次使用的能力。The degree to which a software asset can be used again with little or no modification."}, "aliases": ["可复用性", "复用性"], "related": ["Adaptability", "Variability", "Component"]},
    "Adaptability": {"definitions": {"ISO 25010:2024": "产品或系统能被有效且高效地适配到不同或演进环境的能力。The degree to which a product can be effectively and efficiently adapted for different or evolving environments."}, "aliases": ["适应性", "可适应性"], "related": ["Reusability", "Modifiability", "Portability"]},
    "Component": {"definitions": {"General": "系统中模块化、可部署、可替换的部分，封装实现并暴露接口。A modular, deployable, and replaceable part of a system."}, "aliases": ["组件", "构件"], "related": ["Building Block", "Interface", "Reusability"]},
    "Interface": {"definitions": {"General": "两个独立实体之间交互的边界约定。A boundary across which two independent entities meet and interact."}, "aliases": ["接口"], "related": ["Component", "Model Kind", "View"]},
    "Framework": {"definitions": {"General": "可复用的库或类集合，提供基础结构与通用行为。A reusable set of libraries or classes for a software system.", "ISO 42010:2022": "Architecture Description Framework (ADF): conventions for the description of architectures."}, "aliases": ["框架"], "related": ["Architecture Description", "Model Kind", "Platform"]},
    "Platform": {"definitions": {"General": "一组子系统和接口构成的通用结构，用于高效开发和生产衍生产品。A set of subsystems and interfaces forming a common structure for derivative products."}, "aliases": ["平台"], "related": ["Framework", "Domain Engineering", "IDP"]},
    "IDP": {"definitions": {"General": "内部开发者平台，提供自助式抽象与工具层。Internal Developer Platform: a layer of abstraction and tooling for developer self-service."}, "aliases": ["Internal Developer Platform", "内部开发者平台"], "related": ["Platform", "Self-Service", "Developer Experience"]},
    "Self-Service": {"definitions": {"General": "允许用户无需其他团队人工干预即可获取资源与能力的模式。A model that allows users to access resources without manual intervention."}, "aliases": ["自助服务"], "related": ["IDP", "Platform", "Developer Experience"]},
    "Developer Experience": {"definitions": {"General": "开发者与工具、平台、流程和文档交互时的整体体验。The overall experience of developers as they interact with tools, platforms, processes, and documentation."}, "aliases": ["开发者体验", "DX"], "related": ["IDP", "Self-Service", "Platform"]},
    "Feature Model": {"definitions": {"PLE": "以层次结构组织的特征集合及其关系与约束，用于建模产品线可变性。A hierarchically arranged set of features with relationships and constraints."}, "aliases": ["特征模型"], "related": ["Variability Model", "Variability", "Commonality"]},
    "Pattern": {"definitions": {"General": "在特定上下文中对常见问题的通用可复用解决方案。A general reusable solution to a commonly occurring problem within a given context."}, "aliases": ["模式", "设计模式"], "related": ["Reusability", "Framework", "Architecture"]},
    "Golden Path": {"definitions": {"General": "受组织支持、有明确意见的软件构建与部署路径，平衡开发者自由与组织标准。An opinionated, supported path for building and deploying software."}, "aliases": ["黄金路径"], "related": ["IDP", "Platform", "Developer Experience"]},
    "InnerSource": {"definitions": {"General": "将开源实践和原则应用于内部软件开发。The application of open source practices and principles to internal software development."}, "aliases": ["内部开源"], "related": ["Reusability", "Developer Experience", "Platform"]},
    "SBOM": {"definitions": {"General": "软件物料清单，软件组件与依赖的形式化机器可读清单。Software Bill of Materials: a formal, machine-readable inventory of software components and dependencies."}, "aliases": ["Software Bill of Materials", "软件物料清单"], "related": ["Component", "Supply Chain", "Provenance"]},
    "Provenance": {"definitions": {"SLSA": "描述软件制品如何被构建的可验证记录。The verifiable record describing how a software artifact was built."}, "aliases": ["来源证明", "出处"], "related": ["SBOM", "Attestation", "Supply Chain"]},
    "Attestation": {"definitions": {"SLSA": "对软件制品某类声明的密码学签名声明。A cryptographically signed statement about a software artifact."}, "aliases": ["证明"], "related": ["Provenance", "SBOM", "Supply Chain"]},
    "Supply Chain": {"definitions": {"General": "软件生产与分发所涉及的步骤序列，包括依赖、构建工具和分发渠道。The series of steps involved in producing and distributing software."}, "aliases": ["供应链"], "related": ["SBOM", "Provenance", "SLSA"]},
}

# 别名反向索引
ALIAS_INDEX: Dict[str, str] = {}
for term, rec in TERM_DB.items():
    ALIAS_INDEX[term.lower()] = term
    for a in rec.get("aliases", []):
        ALIAS_INDEX[a.lower()] = term

# 标准来源反向索引
STD_INDEX: Dict[str, List[str]] = {}
for term, rec in TERM_DB.items():
    for std in rec["definitions"]:
        STD_INDEX.setdefault(std, []).append(term)


def find_term(key: str) -> Optional[str]:
    """通过名称或别名查找术语的标准名称。"""
    k = key.lower()
    if k in ALIAS_INDEX:
        return ALIAS_INDEX[k]
    for alias, canonical in ALIAS_INDEX.items():
        if alias.startswith(k) or k in alias:
            return canonical
    return None


def fmt_term(name: str, rec: Dict) -> str:
    """格式化单个术语的完整输出。"""
    lines = [f"【{name}】"]
    aliases = rec.get("aliases", [])
    if aliases:
        lines.append(f"  别名: {', '.join(aliases)}")
    lines.append("  定义:")
    for std, definition in rec["definitions"].items():
        lines.append(f"    [{std}] {definition}")
    related = rec.get("related", [])
    if related:
        lines.append(f"  相关术语: {', '.join(related)}")
    return "\n".join(lines)


def cmd_query(args) -> int:
    """精确查询术语定义。"""
    term = find_term(args.term)
    if not term:
        print(f"未找到术语: {args.term}")
        print(f"提示: 尝试使用 'search {args.term}' 进行模糊搜索。")
        return 1
    print(fmt_term(term, TERM_DB[term]))
    return 0


def cmd_search(args) -> int:
    """模糊搜索术语（名称、别名、定义内容）。"""
    kw = args.keyword.lower()
    results: List[Tuple[str, Dict]] = []
    for term, rec in TERM_DB.items():
        hit = kw in term.lower() or any(kw in a.lower() for a in rec.get("aliases", [])) or any(kw in d.lower() for d in rec["definitions"].values())
        if hit:
            results.append((term, rec))
    if not results:
        print(f"未找到与 '{args.keyword}' 相关的术语。")
        return 1
    print(f"找到 {len(results)} 条与 '{args.keyword}' 相关的结果:\n")
    for term, rec in results:
        first_std = next(iter(rec["definitions"]))
        first_def = rec["definitions"][first_std]
        print(f"  • {term}  [{first_std}]")
        print(f"    {first_def[:100]}{'...' if len(first_def) > 100 else ''}")
        aliases = rec.get("aliases", [])
        if aliases:
            print(f"    别名: {', '.join(aliases)}")
        print()
    return 0


def cmd_compare(args) -> int:
    """对比两个术语在不同标准中的定义差异。"""
    t1, t2 = find_term(args.term1), find_term(args.term2)
    if not t1:
        print(f"未找到术语: {args.term1}"); return 1
    if not t2:
        print(f"未找到术语: {args.term2}"); return 1
    r1, r2 = TERM_DB[t1], TERM_DB[t2]
    stds1, stds2 = set(r1["definitions"].keys()), set(r2["definitions"].keys())
    common = stds1 & stds2
    only1, only2 = stds1 - stds2, stds2 - stds1
    print(f"【术语对比】{t1}  vs  {t2}\n")
    if common:
        print("  共同标准中的定义差异:")
        for std in sorted(common):
            print(f"    [{std}]\n      {t1}: {r1['definitions'][std]}\n      {t2}: {r2['definitions'][std]}")
        print()
    else:
        print("  两个术语没有共同的标准来源。\n")
    if only1:
        print(f"  仅在 {t1} 中出现的标准:")
        for std in sorted(only1):
            print(f"    [{std}] {r1['definitions'][std]}")
        print()
    if only2:
        print(f"  仅在 {t2} 中出现的标准:")
        for std in sorted(only2):
            print(f"    [{std}] {r2['definitions'][std]}")
        print()
    print("  跨标准差异说明:")
    if t1 == t2:
        print(f"    两个查询指向同一术语 '{t1}'，无差异。")
    elif common:
        print(f"    '{t1}' 与 '{t2}' 在 {len(common)} 个标准中均有定义，侧重点可能不同。")
    else:
        print(f"    '{t1}' 主要出现在 {', '.join(sorted(only1))}；'{t2}' 主要出现在 {', '.join(sorted(only2))}。")
    inter = set(r1.get("related", [])) & set(r2.get("related", []))
    if inter:
        print(f"\n  共同相关术语: {', '.join(sorted(inter))}")
    return 0


def cmd_list(args) -> int:
    """列出某个标准下的所有术语。"""
    matched = [s for s in STD_INDEX if args.standard.lower() in s.lower()]
    if not matched:
        print(f"未找到标准: {args.standard}")
        print(f"支持的标准: {', '.join(sorted(STD_INDEX.keys()))}")
        return 1
    for mstd in matched:
        terms = STD_INDEX[mstd]
        print(f"\n【{mstd}】({len(terms)} 条术语)")
        for term in sorted(terms):
            rec = TERM_DB[term]
            aliases = rec.get("aliases", [])
            alias_str = f"  (别名: {', '.join(aliases)})" if aliases else ""
            print(f"  • {term}{alias_str}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="跨标准术语查询脚本（ISO 42010 / TOGAF 10 / PLE / 软件复用）")
    sub = parser.add_subparsers(dest="command", help="可用命令")
    p_query = sub.add_parser("query", help="精确查询术语定义")
    p_query.add_argument("term", help="要查询的术语")
    p_search = sub.add_parser("search", help="模糊搜索术语")
    p_search.add_argument("keyword", help="搜索关键词")
    p_compare = sub.add_parser("compare", help="对比两个术语在不同标准中的定义差异")
    p_compare.add_argument("term1", help="第一个术语")
    p_compare.add_argument("term2", help="第二个术语")
    p_list = sub.add_parser("list", help="列出某个标准下的所有术语")
    p_list.add_argument("--standard", required=True, help="标准名称（如 ISO 42010:2022, TOGAF 10）")
    args = parser.parse_args()
    if args.command == "query":
        return cmd_query(args)
    elif args.command == "search":
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
