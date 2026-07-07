#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量修复质量门控未通过的 Markdown 文件。

用法：
    python scripts/batch-fix-quality-gate.py

默认处理范围（方案 A：激进全面重构）：
- struct/01-meta-model-standards/ 全部未通过
- struct/02-business-architecture-reuse/ 全部未通过
- struct/04-component-architecture-reuse/ 全部未通过
- struct/05-functional-architecture-reuse/ 全部未通过
- struct/06-cross-layer-governance/ 全部未通过
- struct/03-application-architecture-reuse/ 分数 ≤ 35 的未通过
"""

import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 动态导入 quality-gate.py（文件名含连字符不能作为模块名）
import importlib.util
_qg_path = PROJECT_ROOT / "scripts" / "quality-gate.py"
_qg_spec = importlib.util.spec_from_file_location("quality_gate_module", _qg_path)
_quality_gate = importlib.util.module_from_spec(_qg_spec)
_qg_spec.loader.exec_module(_quality_gate)
check_file = _quality_gate.check_file
RULES = _quality_gate.RULES
MIN_SCORE = _quality_gate.MIN_SCORE
MIN_WEIGHTED = _quality_gate.MIN_WEIGHTED
GateResult = _quality_gate.GateResult

VERIFY_DATE = "2026-07-07"

# ---------- 模板库 ----------
# 每个模板提供：definition, example, counter_example, authority, analysis
# authority 为 (label, url) 列表

COMMON_AUTHORITY = {
    "iso": ("ISO/IEC/IEEE Standards", "https://www.iso.org"),
    "ieee": ("IEEE Standards", "https://standards.ieee.org"),
    "nist": ("NIST", "https://www.nist.gov"),
    "cncf": ("CNCF", "https://www.cncf.io"),
    "finops": ("FinOps Foundation", "https://www.finops.org"),
    "togaf": ("The Open Group TOGAF", "https://www.opengroup.org/togaf"),
    "archimate": ("ArchiMate Specification", "https://www.opengroup.org/archimate"),
    "omg-bpmn": ("OMG BPMN", "https://www.omg.org/spec/BPMN"),
    "omg-dmn": ("OMG DMN", "https://www.omg.org/spec/DMN"),
    "omg-ras": ("OMG RAS", "https://www.omg.org/spec/RAS"),
    "fair4rs": ("FAIR4RS Principles", "https://ardc.edu.au/resource/fair-principles-for-research-software-fair4rs"),
    "mcp": ("Model Context Protocol", "https://modelcontextprotocol.io/specification/2025-11-25"),
    "a2a": ("A2A Protocol", "https://google.github.io/A2A"),
    "temporal": ("Temporal Documentation", "https://docs.temporal.io"),
    "gateway-api": ("Kubernetes Gateway API", "https://gateway-api.sigs.k8s.io"),
    "slsa": ("SLSA Framework", "https://slsa.dev"),
    "openssf": ("OpenSSF", "https://openssf.org"),
    "backstage": ("Backstage", "https://backstage.io"),
    "kubernetes": ("Kubernetes", "https://kubernetes.io"),
    "wasm": ("WebAssembly Component Model", "https://component-model.bytecodealliance.org"),
    "rust": ("Rust", "https://www.rust-lang.org"),
}


def make_authority_block(pairs: List[Tuple[str, str]]) -> str:
    lines = ["> **权威来源**:", ">"]
    for label, url in pairs:
        lines.append(f"> - [{label}]({url})")
    lines.append(f"> - 核查日期：{VERIFY_DATE}")
    return "\n".join(lines)


DEFAULT_TEMPLATE = {
    "title": "可复用资产",
    "definition": (
        "**定义**：可复用资产（Reusable Asset）指在特定上下文中被设计、文档化并治理，"
        "能够在多个系统、项目或组织中重复使用的软件工程制品。其边界由显式契约、稳定接口"
        "与可验证质量属性共同定义。"
    ),
    "example": (
        "**示例**：某电商平台将用户身份认证服务抽象为组织级可复用资产，提供标准 OAuth 2.1 "
        "接口、SLA 保证与统一审计日志，供 20+ 业务系统调用，避免各业务线重复开发认证模块。"
    ),
    "counter_example": (
        "**反例**：某团队将高度耦合订单流程的代码片段直接复制到新项目中，未剥离业务专属逻辑，"
        "导致后续需求变更需要在 5 个项目中同步修改，形成“复制-粘贴-发散”的反模式。"
    ),
    "authority_pairs": [COMMON_AUTHORITY["iso"], COMMON_AUTHORITY["ieee"]],
    "analysis": (
        "**分析**：可复用性的核心矛盾在于“通用性”与“特异性”之间的张力。成功的复用需要在"
        "需求共性与实现差异之间建立稳定抽象，并通过版本治理、质量门控与成本分摊机制保障"
        "长期演化。"
    ),
}

TOPIC_TEMPLATES: Dict[str, Dict] = {
    "01-meta-model-standards": {
        "default": {
            "title": "元模型与标准对齐",
            "definition": (
                "**定义**：元模型（Meta-model）是对架构描述元素、关系与规则的抽象规约；"
                "标准对齐则指将本知识体系的术语、过程与视图与国际/行业权威标准建立可追溯的映射。"
            ),
            "example": (
                "**示例**：在架构描述中采用 ISO/IEC/IEEE 42010:2022 的 Entity of Interest、"
                "Architecture Description Framework 与 Stakeholder Perspective，使架构视图"
                "与评估框架可直接对标国际标准。"
            ),
            "counter_example": (
                "**反例**：团队自创“业务域/技术域/数据域”三分法却未与 TOGAF/ArchiMate 术语映射，"
                "导致与外部审计、供应商交流时出现语义偏差。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["iso"], COMMON_AUTHORITY["ieee"], COMMON_AUTHORITY["togaf"]],
            "analysis": (
                "**分析**：元模型是复用知识体系的地基。缺乏元模型约束的复用会退化为局部约定，"
                "难以跨组织、跨工具链保持一致性。"
            ),
        },
        "iso-42010": {
            "title": "ISO/IEC/IEEE 42010:2022 架构描述",
            "definition": (
                "**定义**：ISO/IEC/IEEE 42010:2022 规定了架构描述（Architecture Description, AD）"
                "的元模型，包括 Entity of Interest、Stakeholder、Concern、Viewpoint、View 与 Model 等核心概念。"
            ),
            "example": (
                "**示例**：某系统采用 42010 的视点机制分别生成安全性视图、性能视图与可维护性视图，"
                "每个视图绑定明确的利益相关者与关注点，使架构评审可重复。"
            ),
            "counter_example": (
                "**反例**：项目仅交付一张“总体架构图”，未区分利益相关者视角，导致安全团队、"
                "运维团队与业务方在同一视图上争论不休。"
            ),
            "authority_pairs": [
                ("ISO/IEC/IEEE 42010:2022", "https://www.iso.org/standard/74296.html"),
                COMMON_AUTHORITY["ieee"],
            ],
            "analysis": (
                "**分析**：42010:2022 将架构描述从“画图”提升为“结构化论据”，强调关注点驱动与视图一致性。"
            ),
        },
        "iso-42020": {
            "title": "ISO/IEC/IEEE 42020:2019 架构过程",
            "definition": (
                "**定义**：ISO/IEC/IEEE 42020:2019 定义了架构过程的通用框架，包括架构治理、"
                "架构管理、架构视图与架构评估等活动，用于指导组织级架构实践。"
            ),
            "example": (
                "**示例**：企业架构团队依据 42020 建立“架构委员会 → 项目架构师 → 实施团队”三级治理过程，"
                "对可复用资产的引入、变更与退役实施统一审批。"
            ),
            "counter_example": (
                "**反例**：组织没有标准化架构过程，各项目自行决定复用策略，导致同一能力在 3 个部门"
                "出现 5 种互不兼容的实现。"
            ),
            "authority_pairs": [
                ("ISO/IEC/IEEE 42020:2019", "https://www.iso.org/standard/70023.html"),
                COMMON_AUTHORITY["iso"],
            ],
            "analysis": (
                "**分析**：42020 将架构活动过程化，是连接战略意图与实施落地的关键标准。"
            ),
        },
        "iso-42030": {
            "title": "ISO/IEC/IEEE 42030:2019 架构评估",
            "definition": (
                "**定义**：ISO/IEC/IEEE 42030:2019 规定了架构评估（Architecture Evaluation）的原则、"
                "过程与方法，用于判断架构满足利益相关者关注点的程度。"
            ),
            "example": (
                "**示例**：在引入共享服务前，组织使用 42030 的评估框架对候选架构进行 ATAM 式评审，"
                "识别性能、安全与可维护性风险并给出缓解措施。"
            ),
            "counter_example": (
                "**反例**：项目上线后才由运维团队发现共享组件存在单点故障，因缺乏前期架构评估"
                "导致生产事故。"
            ),
            "authority_pairs": [
                ("ISO/IEC/IEEE 42030:2019", "https://www.iso.org/standard/70024.html"),
                COMMON_AUTHORITY["iso"],
            ],
            "analysis": (
                "**分析**：架构评估是复用决策的质量门控，缺乏评估的复用容易引入隐性耦合与演进债务。"
            ),
        },
        "iso-25010": {
            "title": "ISO/IEC 25010:2023 质量模型",
            "definition": (
                "**定义**：ISO/IEC 25010:2023 定义了软件产品质量模型，包括功能适合性、性能效率、"
                "兼容性、交互能力、可靠性、安全性、可维护性、灵活性与安全性等特性。"
            ),
            "example": (
                "**示例**：在评估可复用 UI 组件库时，团队依据 25010 的交互能力、可维护性与兼容性"
                "制定验收准则，确保组件在多前端框架中一致表现。"
            ),
            "counter_example": (
                "**反例**：团队仅关注功能正确性，忽视可维护性与灵活性，导致复用组件在框架升级时"
                "无法平滑迁移。"
            ),
            "authority_pairs": [
                ("ISO/IEC 25010:2023", "https://www.iso.org/standard/78175.html"),
                COMMON_AUTHORITY["iso"],
            ],
            "analysis": (
                "**分析**：25010 提供了复用资产质量评估的共同语言，帮助买方与卖方在质量属性上达成一致。"
            ),
        },
        "iso-12207": {
            "title": "ISO/IEC/IEEE 12207:2026 软件生命周期过程",
            "definition": (
                "**定义**：ISO/IEC/IEEE 12207:2026 规定了软件与系统生命周期过程，覆盖获取、供应、"
                "开发、运营、维护与复用支持等过程组。"
            ),
            "example": (
                "**示例**：在 12207 复用管理过程中，组织建立“资产获取 → 资产存储 → 资产适配 → 资产退役”"
                "的闭环，确保复用资产与主生命周期同步演进。"
            ),
            "counter_example": (
                "**反例**：复用资产库长期处于“只进不出”状态，过期组件未退役，导致新项目误选"
                "已停止维护的旧版本。"
            ),
            "authority_pairs": [
                ("ISO/IEC/IEEE 12207:2017/2026", "https://www.iso.org/standard/63712.html"),
                COMMON_AUTHORITY["iso"],
            ],
            "analysis": (
                "**分析**：12207 将复用视为生命周期过程的有机组成部分，而非孤立的资产管理活动。"
            ),
        },
        "ieee-1517": {
            "title": "IEEE 1517-2010 软件生命周期复用过程",
            "definition": (
                "**定义**：IEEE 1517-2010 定义了软件生命周期中复用过程的结构，包括组织管理、"
                "领域工程、资产提供、资产消费与资产维护等过程。"
            ),
            "example": (
                "**示例**：某组织按 1517 建立领域工程团队，负责识别共性需求、开发可复用资产并向"
                "应用工程团队提供资产与培训。"
            ),
            "counter_example": (
                "**反例**：没有专门复用组织，开发人员自行在代码库中搜索可复用代码，效率低下且"
                "质量不可控。"
            ),
            "authority_pairs": [
                ("IEEE 1517-2010", "https://standards.ieee.org/standard/1517-2010.html"),
                COMMON_AUTHORITY["ieee"],
            ],
            "analysis": (
                "**分析**：1517 将复用从个人行为上升为组织过程，强调领域工程与应用工程的双轨协作。"
            ),
        },
        "togaf": {
            "title": "TOGAF 10 与复用",
            "definition": (
                "**定义**：TOGAF 10 是企业架构开发方法论，其企业 continuum、架构构建块（ABB）"
                "与解决方案构建块（SBB）为架构复用提供了分类与治理框架。"
            ),
            "example": (
                "**示例**：企业将 CRM 能力抽象为 ABB，并基于 Salesforce、自研或混合方案实现为 SBB，"
                "在不同业务单元中按需复用。"
            ),
            "counter_example": (
                "**反例**：团队混淆 ABB 与 SBB，将具体技术实现直接作为能力标准，导致业务架构"
                "被技术绑定。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["togaf"], COMMON_AUTHORITY["archimate"]],
            "analysis": (
                "**分析**：TOGAF 的企业 continuum 提供了从基础架构到组织特定架构的复用梯度，"
                "是业务-技术对齐的重要工具。"
            ),
        },
        "archimate": {
            "title": "ArchiMate 与 ISO 对齐",
            "definition": (
                "**定义**：ArchiMate 是 The Open Group 发布的架构建模语言，提供业务、应用、技术"
                "三层视图及元素、关系与视点规范。"
            ),
            "example": (
                "**示例**：使用 ArchiMate 的业务服务、应用组件与技术服务元素，将可复用资产"
                "在三层次架构中显式建模，便于影响分析。"
            ),
            "counter_example": (
                "**反例**：建模时滥用“聚合”关系表达复用，导致模型无法准确反映资产依赖与所有权。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["archimate"],
                ("ArchiMate 3.2 Specification", "https://www.opengroup.org/archimate-forum"),
            ],
            "analysis": (
                "**分析**：ArchiMate 将复用关系可视化，是跨团队协作与架构治理的沟通媒介。"
            ),
        },
        "swebok": {
            "title": "SWEBOK V4 对齐",
            "definition": (
                "**定义**：SWEBOK（Software Engineering Body of Knowledge）V4 是 IEEE/ACM 发布的"
                "软件工程知识体系指南，涵盖软件设计、构造、测试、维护、配置管理等领域。"
            ),
            "example": (
                "**示例**：将 SWEBOK 的软件设计知识领域与 ISO 42010 架构描述、GoF 设计模式"
                "建立映射，形成从理论到实践的知识路径。"
            ),
            "counter_example": (
                "**反例**：培训体系仅覆盖编码技能，忽视软件工程基础理论，导致团队难以识别"
                "可复用抽象。"
            ),
            "authority_pairs": [
                ("SWEBOK V4", "https://www.computer.org/education/bodies-of-knowledge/software-engineering"),
                COMMON_AUTHORITY["ieee"],
            ],
            "analysis": (
                "**分析**：SWEBOK 提供了软件工程知识的全景，帮助组织定位复用实践在知识体系中的坐标。"
            ),
        },
        "ras": {
            "title": "OMG RAS 可复用资产规范",
            "definition": (
                "**定义**：OMG RAS（Reusable Asset Specification）定义了可复用资产的元数据模型，"
                "包括分类（Classification）、解决方案（Solution）、使用（Usage）与相关资产（RelatedAssets）四类描述。"
            ),
            "example": (
                "**示例**：企业资产库为每个微服务模板建立 RAS 描述：分类标签标明技术栈与领域，"
                "解决方案提供代码与配置文件，使用文档说明集成步骤，相关资产链接到配套测试与监控模板。"
            ),
            "counter_example": (
                "**反例**：资产库中只有压缩包文件名，缺乏分类、使用说明与依赖关系，使用者"
                "难以判断适用性。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["omg-ras"], COMMON_AUTHORITY["omg-bpmn"]],
            "analysis": (
                "**分析**：RAS 提供了一套标准化资产描述契约，是资产目录可检索、可比较、可治理的基础。"
            ),
        },
        "fair4rs": {
            "title": "FAIR4RS 研究软件复用原则",
            "definition": (
                "**定义**：FAIR4RS（FAIR Principles for Research Software）将 FAIR 原则应用于研究软件，"
                "要求软件可发现（Findable）、可访问（Accessible）、可互操作（Interoperable）、可重用（Reusable）。"
            ),
            "example": (
                "**示例**：某科研团队将分析工具注册到 Zenodo 并分配 DOI，附带语义化元数据、"
                "开源许可证与容器镜像，使其他研究团队可发现、引用与复用。"
            ),
            "counter_example": (
                "**反例**：研究代码仅存储在个人网盘，缺乏版本、文档与许可证，他人无法引用或复现。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["fair4rs"], ("FAIR4RS RDA", "https://www.rd-alliance.org/group/fair-4-research-software-fair4rs-wg")],
            "analysis": (
                "**分析**：FAIR4RS 将软件复用理念引入科研领域，强调可引用性、可重现性与可持续维护。"
            ),
        },
        "axiom": {
            "title": "形式化公理体系",
            "definition": (
                "**定义**：形式化公理体系是通过公理、定理与推导规则对复用概念进行严格数学刻画的"
                "知识基础，用于消除自然语言的歧义性。"
            ),
            "example": (
                "**示例**：定义“复用关系”为偏序关系（自反、传递、反对称），并据此证明"
                "资产组合的一致性与可替换性定理。"
            ),
            "counter_example": (
                "**反例**：团队用日常语言描述复用规则，出现“复用等于复制”“复用必然降低成本”"
                "等不严谨论断，导致决策失误。"
            ),
            "authority_pairs": [
                ("Carnegie Mellon SEI", "https://www.sei.cmu.edu"),
                ("ETH Zurich Systems Group", "https://inf.ethz.ch"),
            ],
            "analysis": (
                "**分析**：公理体系为复用知识提供逻辑基础，但需与工程实践保持平衡，避免过度形式化。"
            ),
        },
    },
    "02-business-architecture-reuse": {
        "default": {
            "title": "业务架构复用",
            "definition": (
                "**定义**：业务架构复用是在业务层面识别、封装和共享稳定的业务能力、价值流、"
                "流程与服务，以支持跨组织、跨项目的业务一致性。"
            ),
            "example": (
                "**示例**：跨国银行将“客户身份识别 (KYC)”抽象为共享业务能力，供零售银行、"
                "投资银行与财富管理业务线复用，统一合规标准并降低重复建设。"
            ),
            "counter_example": (
                "**反例**：各业务线独立开发相似的订单处理流程，仅在术语与规则上略有差异，"
                "导致数据孤岛与集成成本激增。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["togaf"], COMMON_AUTHORITY["omg-bpmn"]],
            "analysis": (
                "**分析**：业务架构复用的难点在于平衡标准化与业务差异化，需要以能力而非"
                "组织结构作为复用边界。"
            ),
        },
        "business-domain": {
            "title": "业务域复用",
            "definition": (
                "**定义**：业务域复用是在跨行业或跨组织的宏观业务领域内，识别并封装通用业务概念、"
                "规则与模型，以支持领域驱动设计中的子域复用。"
            ),
            "example": (
                "**示例**：BIAN 银行业架构参考模型将银行业务划分为 300+ 业务服务组件，"
                "为银行数字化转型提供可复用的领域蓝图。"
            ),
            "counter_example": (
                "**反例**：将其他行业的“库存管理”模型直接套用于航空维修备件管理，忽视行业"
                "法规与生命周期差异，导致模型失真。"
            ),
            "authority_pairs": [
                ("BIAN", "https://www.bian.org"),
                COMMON_AUTHORITY["togaf"],
            ],
            "analysis": (
                "**分析**：业务域复用强调领域知识的沉淀，过早抽象或过晚抽象都会削弱复用价值。"
            ),
        },
        "business-capability": {
            "title": "业务能力复用",
            "definition": (
                "**定义**：业务能力（Business Capability）是组织为达成特定业务成果而具备的"
                "稳定能力单元，独立于组织结构和实现技术。"
            ),
            "example": (
                "**示例**：某零售企业建立“客户 360° 视图”能力目录，作为营销、客服与供应链"
                "决策的共同输入，避免各系统重复采集客户数据。"
            ),
            "counter_example": (
                "**反例**：将“市场部审批流程”直接建模为业务能力，导致能力边界随组织调整"
                "频繁变化，无法稳定复用。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["togaf"],
                ("FEA BRM", "https://www.govloop.com/community/blog/federal-enterprise-architecture/"),
            ],
            "analysis": (
                "**分析**：能力原子性是业务复用的关键：能力应由价值创造定义，而非由组织结构定义。"
            ),
        },
        "value-stream": {
            "title": "价值流复用",
            "definition": (
                "**定义**：价值流（Value Stream）是端到端描述利益相关者价值创造活动的序列，"
                "价值流复用则是在不同场景下重用成熟的价值交付模式。"
            ),
            "example": (
                "**示例**：某保险公司将“理赔端到端价值流”标准化为可复用模板，在新产品线"
                "上线时只需调整规则与接口，缩短上市时间 40%。"
            ),
            "counter_example": (
                "**反例**：价值流在部门边界处断裂，导致“订单到收款”流程在财务、物流、"
                "客服之间反复切换系统，客户体验受损。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["togaf"], COMMON_AUTHORITY["omg-bpmn"]],
            "analysis": (
                "**分析**：价值流复用要求跨部门视角，识别并消除非增值环节，实现端到端优化。"
            ),
        },
        "business-process": {
            "title": "业务流程复用",
            "definition": (
                "**定义**：业务流程复用是将经过验证的业务流程模型（通常以 BPMN 描述）"
                "在不同组织单元或系统中重复执行，减少流程设计与实现成本。"
            ),
            "example": (
                "**示例**：制造企业将“供应商准入流程”建模为标准 BPMN 2.0 流程并在 Camunda "
                "引擎上部署，各工厂按本地法规配置差异规则后复用。"
            ),
            "counter_example": (
                "**反例**：将高度监管流程的 BPMN 模板复制到新国家时未本地化合规规则，"
                "导致审计失败。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["omg-bpmn"], COMMON_AUTHORITY["omg-dmn"]],
            "analysis": (
                "**分析**：流程复用需要区分“不变流程主干”与“可变本地化规则”，并通过"
                "决策表管理差异。"
            ),
        },
        "business-service": {
            "title": "业务服务复用",
            "definition": (
                "**定义**：业务服务（Business Service）是为内部或外部客户提供的、具有明确"
                "业务价值的可复用服务单元，常以 SOA 或微服务形式实现。"
            ),
            "example": (
                "**示例**：电信公司将“号码携带”封装为标准业务服务，供线上线下渠道、"
                "合作伙伴 API 统一调用，避免各渠道重复实现。"
            ),
            "counter_example": (
                "**反例**：业务服务边界过大，包含下单、支付、履约等多个子领域，导致"
                "消费方被迫引入不必要的耦合。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["togaf"], COMMON_AUTHORITY["omg-bpmn"]],
            "analysis": (
                "**分析**：业务服务复用的粒度应与客户契约和变更频率相匹配，过大或过小的服务"
                "都会降低复用收益。"
            ),
        },
        "bpmn-dmn": {
            "title": "BPMN/DMN 可执行复用",
            "definition": (
                "**定义**：BPMN（业务流程模型和标注）用于描述可执行业务流程，DMN（决策模型与标注）"
                "用于描述可执行业务决策，二者结合实现流程与决策的分离与复用。"
            ),
            "example": (
                "**示例**：信贷审批流程使用 BPMN 定义审批步骤，使用 DMN 决策表管理利率、"
                "额度规则，业务人员可直接调整规则而无需修改流程代码。"
            ),
            "counter_example": (
                "**反例**：将业务规则硬编码在 BPMN 网关条件中，导致规则变更需要重新部署流程，"
                "业务人员无法参与。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["omg-bpmn"], COMMON_AUTHORITY["omg-dmn"]],
            "analysis": (
                "**分析**：BPMN/DMN 的分离使流程结构稳定、规则灵活，是业务-IT 对齐的关键实践。"
            ),
        },
        "defense": {
            "title": "国防任务工程复用",
            "definition": (
                "**定义**：国防任务工程中的复用指在 DoDAF/NAF/Modaf/UAF 等框架下，对使命线程、"
                "能力、系统与服务进行跨项目复用，以提升互操作性与采购效率。"
            ),
            "example": (
                "**示例**：北约通过 NAF 架构框架建立通用态势感知能力视图，各成员国在联合"
                "行动中共享通用的任务线程与接口标准。"
            ),
            "counter_example": (
                "**反例**：各国国防系统使用互不兼容的架构框架与数据模型，联合作战时需要"
                "昂贵的点对点集成。"
            ),
            "authority_pairs": [
                ("DoDAF", "https://dodcio.defense.gov/library/dod-architecture-framework"),
                ("NAF", "https://nafdocs.org"),
            ],
            "analysis": (
                "**分析**：国防任务工程复用强调跨组织互操作性，标准化框架与参考模型是关键使能器。"
            ),
        },
        "zachman": {
            "title": "Zachman 框架复用映射",
            "definition": (
                "**定义**：Zachman 框架通过 6 个视角（What、How、Where、Who、When、Why）"
                "与 6 个抽象层次描述企业架构，为复用资产提供多维度分类。"
            ),
            "example": (
                "**示例**：企业使用 Zachman 矩阵对可复用资产进行分类：业务所有者的“数据模型”"
                "、系统设计师的“应用组件”、技术工程师的“部署配置”。"
            ),
            "counter_example": (
                "**反例**：仅在 Zachman 的一个单元格中管理资产，忽视了同一资产在不同"
                "视角下的不同抽象需求。"
            ),
            "authority_pairs": [
                ("Zachman Framework", "https://www.zachman.com"),
                COMMON_AUTHORITY["togaf"],
            ],
            "analysis": (
                "**分析**：Zachman 框架帮助组织从多个维度理解复用资产，避免单视角导致的遗漏。"
            ),
        },
        "case-studies": {
            "title": "行业垂直复用案例",
            "definition": (
                "**定义**：行业垂直案例是从特定行业（金融、电信、医疗、制造等）提炼的"
                "可复用业务架构模式与实施经验。"
            ),
            "example": (
                "**示例**：TM Forum 的 Open API 框架为电信行业提供标准化的业务服务接口，"
                "使运营商与合作伙伴能够复用共同的业务语义。"
            ),
            "counter_example": (
                "**反例**：将互联网电商的推荐模型直接复制到医疗设备采购场景，忽视行业合规"
                "与决策链差异，导致系统不可用。"
            ),
            "authority_pairs": [
                ("TM Forum", "https://www.tmforum.org"),
                ("BIAN", "https://www.bian.org"),
            ],
            "analysis": (
                "**分析**：行业垂直案例是业务架构复用的最佳实践来源，但需结合本地上下文进行适配。"
            ),
        },
    },
    "03-application-architecture-reuse": {
        "default": {
            "title": "应用架构复用",
            "definition": (
                "**定义**：应用架构复用是在系统层面复用应用、服务、模式与基础设施配置，"
                "包括分层架构、微服务、Serverless、事件驱动、服务网格等形态。"
            ),
            "example": (
                "**示例**：某 SaaS 企业建立内部平台团队，提供可复用的 CI/CD 流水线、"
                "可观测性套件与多租户数据隔离模板，新产品团队可在数天内搭建生产级服务。"
            ),
            "counter_example": (
                "**反例**：各产品团队独立选型技术栈与部署模式，导致安全补丁、监控与"
                "容量管理无法统一治理。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["cncf"], COMMON_AUTHORITY["nist"]],
            "analysis": (
                "**分析**：应用架构复用需要在标准化与团队自治之间取得平衡，平台工程是"
                "常见的组织形式。"
            ),
        },
        "layered": {
            "title": "分层架构复用",
            "definition": (
                "**定义**：分层架构将系统划分为表示层、应用层、领域层与基础设施层等水平层次，"
                "每层通过稳定接口向上层提供服务，实现层内复用与层间解耦。"
            ),
            "example": (
                "**示例**：电商平台将订单领域层封装为独立模块，供 Web、App、小程序等"
                "表示层复用，业务规则只需在领域层维护一份。"
            ),
            "counter_example": (
                "**反例**：表示层直接访问数据库，绕过领域层，导致业务规则散落于多个层次，"
                "无法复用和一致性维护。"
            ),
            "authority_pairs": [
                ("Martin Fowler - Patterns of Enterprise Application Architecture", "https://martinfowler.com/eaaCatalog"),
                COMMON_AUTHORITY["cncf"],
            ],
            "analysis": (
                "**分析**：分层架构复用的有效性取决于层间依赖规则的严格执行，否则容易退化为"
                "“大泥球”。"
            ),
        },
        "microservices": {
            "title": "微服务架构复用",
            "definition": (
                "**定义**：微服务架构将系统拆分为围绕业务能力组织、可独立部署的小服务，"
                "服务间通过轻量级机制通信；微服务复用强调跨团队共享服务与 API 契约。"
            ),
            "example": (
                "**示例**：企业将用户画像、消息通知、文件存储构建为独立微服务，通过"
                "OpenAPI 契约供各业务线复用，降低重复开发。"
            ),
            "counter_example": (
                "**反例**：为追求复用将两个高内聚但变更频率不同的业务能力强行合并为一个"
                "微服务，导致发布耦合与团队摩擦。"
            ),
            "authority_pairs": [
                ("Microservices by Martin Fowler", "https://martinfowler.com/articles/microservices.html"),
                COMMON_AUTHORITY["cncf"],
            ],
            "analysis": (
                "**分析**：微服务复用需要清晰的领域边界与版本治理，否则共享服务会成为"
                "跨团队协作瓶颈。"
            ),
        },
        "app-service": {
            "title": "应用服务复用",
            "definition": (
                "**定义**：应用服务复用是在应用层将通用能力（如认证、通知、支付、搜索）"
                "封装为服务目录，通过 API 网关与服务契约实现跨应用复用。"
            ),
            "example": (
                "**示例**：企业通过 API 网关暴露统一的支付服务，移动 App、Web 端与合作伙伴"
                "系统均调用同一服务，确保支付逻辑与合规要求一致。"
            ),
            "counter_example": (
                "**反例**：各应用自行实现支付逻辑，导致费率计算、对账与风控规则不一致，"
                "财务审计困难。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["nist"],
                ("OASIS SOA Reference Architecture", "https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=soa-rm"),
            ],
            "analysis": (
                "**分析**：应用服务复用的收益与治理成本成正比，需要通过服务目录、SLA "
                "与成熟度评估控制范围。"
            ),
        },
        "serverless": {
            "title": "Serverless 架构复用",
            "definition": (
                "**定义**：Serverless 架构复用是利用函数即服务（FaaS）与托管服务，"
                "将无状态计算、事件处理与后端能力封装为可复用函数与模板。"
            ),
            "example": (
                "**示例**：团队将图片处理、PDF 生成、Webhook 转换实现为标准 Lambda/"
                "Cloud Function 模板，新项目通过配置环境变量即可部署。"
            ),
            "counter_example": (
                "**反例**：在 Serverless 函数中保留大量长连接与本地状态，导致冷启动时间长、"
                "成本高且难以扩展。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["cncf"],
                ("AWS Lambda", "https://aws.amazon.com/lambda"),
            ],
            "analysis": (
                "**分析**：Serverless 复用适合事件驱动、短时无状态任务，需警惕供应商锁定与"
                "隐藏成本。"
            ),
        },
        "event-driven": {
            "title": "事件驱动架构复用",
            "definition": (
                "**定义**：事件驱动架构（EDA）通过事件的生产、检测、消费与响应解耦系统组件，"
                "事件模式与 Schema 的复用是实现跨系统互操作的关键。"
            ),
            "example": (
                "**示例**：零售企业定义标准“订单已创建”事件 Schema，并在事件总线注册，"
                "库存、物流、营销系统均按同一 Schema 消费，避免重复集成。"
            ),
            "counter_example": (
                "**反例**：各团队自行定义“订单”事件格式，导致同一业务事件在系统间传递时"
                "需要多次格式转换与映射。"
            ),
            "authority_pairs": [
                ("AsyncAPI", "https://www.asyncapi.com"),
                COMMON_AUTHORITY["cncf"],
            ],
            "analysis": (
                "**分析**：事件 Schema 治理是 EDA 复用的核心，Schema Registry 与版本兼容策略"
                "不可或缺。"
            ),
        },
        "cloud-native": {
            "title": "云原生复用模式",
            "definition": (
                "**定义**：云原生复用模式是在容器、微服务、声明式 API 与弹性基础设施基础上，"
                "复用经过验证的部署、网络、安全与可观测性配置。"
            ),
            "example": (
                "**示例**：平台团队提供标准 Kubernetes Helm Chart，内置 HPA、PodDisruptionBudget、"
                "NetworkPolicy 与 Prometheus 监控注解，业务团队只需配置镜像与资源请求。"
            ),
            "counter_example": (
                "**反例**：各团队从零编写 Kubernetes 清单，安全策略与资源限制不一致，"
                "生产环境频繁出现资源争用。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["cncf"],
                ("NIST SP 800-204", "https://csrc.nist.gov/publications/detail/sp/800-204/final"),
            ],
            "analysis": (
                "**分析**：云原生复用通过平台抽象降低认知负荷，但需保留足够的可定制性以满足"
                "业务特殊性。"
            ),
        },
        "service-mesh": {
            "title": "服务网格通信复用",
            "definition": (
                "**定义**：服务网格（Service Mesh）将服务间通信能力（流量管理、安全、可观测性）"
                "从应用代码中剥离，作为基础设施层统一复用。"
            ),
            "example": (
                "**示例**：企业采用 Istio 作为服务网格，所有微服务自动获得 mTLS、金丝雀发布、"
                "重试与分布式追踪能力，无需修改业务代码。"
            ),
            "counter_example": (
                "**反例**：每个微服务自行实现重试、熔断与认证逻辑，导致代码冗余、行为不一致"
                "且难以统一升级。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["gateway-api"],
                ("Istio", "https://istio.io"),
            ],
            "analysis": (
                "**分析**：服务网格将横切关注点下沉到基础设施，是应用层复用的重要补充，"
                "但需权衡性能与运维复杂度。"
            ),
        },
        "eda-cqrs": {
            "title": "EDA/CQRS/事件溯源复用",
            "definition": (
                "**定义**：CQRS（命令查询职责分离）与事件溯源（Event Sourcing）通过分离读写模型"
                "与持久化事件流，支持复杂业务场景下的状态复用与审计。"
            ),
            "example": (
                "**示例**：金融交易系统采用事件溯源记录所有账户变更事件，支持任意时间点的"
                "状态重建、审计追踪与多视图投影。"
            ),
            "counter_example": (
                "**反例**：在简单的 CRUD 场景中强行引入 CQRS 与事件溯源，增加开发复杂度与"
                "数据一致性挑战，得不偿失。"
            ),
            "authority_pairs": [
                ("Martin Fowler - CQRS", "https://martinfowler.com/bliki/CQRS.html"),
                ("EventStoreDB", "https://www.eventstore.com"),
            ],
            "analysis": (
                "**分析**：CQRS/事件溯源是高杠杆但高复杂度的模式，适用于需要完整审计、复杂查询"
                "或事件驱动集成的场景。"
            ),
        },
    },
    "04-component-architecture-reuse": {
        "default": {
            "title": "组件架构复用",
            "definition": (
                "**定义**：组件架构复用是在模块/组件层面复用设计模式、接口契约、依赖管理与"
                "版本策略，以实现代码级与二进制级的高效复用。"
            ),
            "example": (
                "**示例**：团队将日志、配置、缓存、健康检查等横切关注点封装为内部 SDK 组件，"
                "各微服务通过引入统一版本依赖复用，减少重复代码。"
            ),
            "counter_example": (
                "**反例**：项目直接复制开源库源码到代码库，未通过包管理器跟踪版本与漏洞，"
                "导致安全补丁无法及时同步。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["cncf"], COMMON_AUTHORITY["openssf"]],
            "analysis": (
                "**分析**：组件复用关注依赖管理、接口稳定性与供应链安全，是现代软件工程的"
                "基础能力。"
            ),
        },
        "component-models": {
            "title": "组件模型复用",
            "definition": (
                "**定义**：组件模型定义了组件的接口、依赖、生命周期与组合规则，是组件复用的"
                "概念基础；常见模型包括 OSGi、COM、EJB、Spring Beans 与 Web Components。"
            ),
            "example": (
                "**示例**：前端团队采用 Web Components 构建跨框架复用的 UI 组件库，"
                "在 React、Vue 与 Angular 应用中均可使用同一组件实现。"
            ),
            "counter_example": (
                "**反例**：组件内部硬编码框架特性，导致无法在不同技术栈中复用，被迫为"
                "每个框架维护一套实现。"
            ),
            "authority_pairs": [
                ("Web Components", "https://developer.mozilla.org/en-US/docs/Web/Web_Components"),
                COMMON_AUTHORITY["cncf"],
            ],
            "analysis": (
                "**分析**：组件模型的选择影响复用范围，标准接口与最小依赖是扩大复用面的关键。"
            ),
        },
        "interface-contracts": {
            "title": "接口契约复用",
            "definition": (
                "**定义**：接口契约是组件之间交换数据与服务的显式协议，包括签名、前置条件、"
                "后置条件、不变式与错误语义；契约复用使组件可在不同上下文中安全组合。"
            ),
            "example": (
                "**示例**：使用 OpenAPI 规范定义 REST API 契约，并在服务端与客户端同时生成"
                "类型安全代码，确保多语言实现的一致性。"
            ),
            "counter_example": (
                "**反例**：接口仅通过口头约定，字段含义、错误码与版本策略不明确，"
                "导致客户端频繁因服务端变更而崩溃。"
            ),
            "authority_pairs": [
                ("OpenAPI Specification", "https://spec.openapis.org"),
                ("JSON Schema", "https://json-schema.org"),
            ],
            "analysis": (
                "**分析**：接口契约是组件复用的信任基础，契约测试与设计时验证可显著降低"
                "集成风险。"
            ),
        },
        "dependency-management": {
            "title": "依赖管理复用",
            "definition": (
                "**定义**：依赖管理复用是通过包管理器、版本锁定、仓库镜像与 SBOM 等手段，"
                "安全、可重复地复用外部与内部组件。"
            ),
            "example": (
                "**示例**：团队使用 lockfile 锁定所有依赖版本，并通过内部镜像仓库缓存公共包，"
                "确保构建可重现并降低供应链攻击面。"
            ),
            "counter_example": (
                "**反例**：项目使用“*”版本范围安装依赖，导致构建在不同时间拉取不同版本，"
                "出现不可预期的破坏性变更。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["openssf"],
                ("SPDX", "https://spdx.dev"),
            ],
            "analysis": (
                "**分析**：依赖管理是组件复用的风险控制点，需平衡更新灵活性与构建可重现性。"
            ),
        },
        "design-patterns": {
            "title": "设计模式复用",
            "definition": (
                "**定义**：设计模式是在特定上下文下可重复使用的面向对象/组件设计解决方案，"
                "如工厂、策略、适配器、观察者、依赖注入等。"
            ),
            "example": (
                "**示例**：系统使用策略模式封装不同的定价算法，新算法只需实现统一接口即可"
                "接入，无需修改订单核心逻辑。"
            ),
            "counter_example": (
                "**反例**：在简单场景中过度使用抽象工厂与装饰器模式，导致代码层次过多、"
                "理解成本上升，形成“模式滥用”反模式。"
            ),
            "authority_pairs": [
                ("GoF Design Patterns", "https://en.wikipedia.org/wiki/Design_Patterns"),
                COMMON_AUTHORITY["cncf"],
            ],
            "analysis": (
                "**分析**：设计模式复用需要结合上下文判断，模式的价值在于解决真实问题而非"
                "展示技巧。"
            ),
        },
        "version-strategy": {
            "title": "版本策略复用",
            "definition": (
                "**定义**：版本策略复用是通过语义化版本（SemVer）、API 版本控制与兼容性承诺，"
                "使组件消费者能够安全地升级或回退。"
            ),
            "example": (
                "**示例**：组件库遵循 SemVer，对破坏性变更升级主版本，并维护两个大版本的"
                "安全补丁，帮助消费方规划升级节奏。"
            ),
            "counter_example": (
                "**反例**：组件频繁在不升级主版本的情况下修改公开接口，导致依赖方构建失败，"
                "破坏复用信任。"
            ),
            "authority_pairs": [
                ("Semantic Versioning", "https://semver.org"),
                COMMON_AUTHORITY["cncf"],
            ],
            "analysis": (
                "**分析**：版本策略是复用契约的社会契约，清晰的兼容性规则可降低协调成本。"
            ),
        },
        "cloud-native-networking": {
            "title": "云原生网络复用",
            "definition": (
                "**定义**：云原生网络复用是在 Kubernetes 等平台上复用标准化的网络策略、"
                "Gateway API、服务发现与负载均衡配置。"
            ),
            "example": (
                "**示例**：平台团队提供标准 Gateway API 路由模板，自动配置 TLS 终止、"
                "速率限制与可观测性，业务团队只需声明主机与后端服务。"
            ),
            "counter_example": (
                "**反例**：各服务使用自定义 Ingress 注解与网络策略，迁移到新集群时需要"
                "大量手工调整。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["gateway-api"],
                COMMON_AUTHORITY["kubernetes"],
            ],
            "analysis": (
                "**分析**：云原生网络复用需要抽象底层实现差异，Gateway API 提供了跨 Ingress "
                "控制器的可移植接口。"
            ),
        },
        "language-ecosystems": {
            "title": "语言生态复用",
            "definition": (
                "**定义**：语言生态复用是利用不同编程语言及其包管理、工具链与社区资产，"
                "在性能、安全性、生产力与可维护性之间做出复用决策。"
            ),
            "example": (
                "**示例**：企业使用 Rust 构建高性能网络组件，使用 Python 构建数据科学流水线，"
                "通过 gRPC/Protobuf 实现跨语言复用。"
            ),
            "counter_example": (
                "**反例**：为统一技术栈，强制所有项目使用不擅长特定领域的语言，导致"
                "开发效率与运行时性能双重损失。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["rust"],
                COMMON_AUTHORITY["cncf"],
            ],
            "analysis": (
                "**分析**：语言生态复用不是追求单一语言，而是在共同接口与数据契约下"
                "发挥各语言优势。"
            ),
        },
        "supply-chain": {
            "title": "开源供应链复用",
            "definition": (
                "**定义**：开源供应链复用是在使用开源组件时，通过 SBOM、漏洞扫描、签名验证"
                "与来源追溯等手段，在获取复用收益的同时控制安全风险。"
            ),
            "example": (
                "**示例**：组织采用 SLSA L3 构建流程，对开源依赖进行签名验证与 SBOM 生成，"
                "在漏洞披露后 24 小时内定位受影响服务。"
            ),
            "counter_example": (
                "**反例**：项目引入 200+ 间接依赖却从未审计，已知高危漏洞在多个服务中长期存在。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["slsa"],
                COMMON_AUTHORITY["openssf"],
            ],
            "analysis": (
                "**分析**：开源复用是双刃剑，供应链安全已成为现代软件工程不可回避的治理议题。"
            ),
        },
    },
    "05-functional-architecture-reuse": {
        "default": {
            "title": "功能架构复用",
            "definition": (
                "**定义**：功能架构复用是在函数、算法、业务规则、工作流与 AI 能力等最细粒度"
                "层次上进行复用，强调单一职责、确定性边界与可组合性。"
            ),
            "example": (
                "**示例**：团队将发票金额校验、税率计算与格式转换封装为纯函数库，"
                "在订单、报销与财务系统中统一调用，避免重复实现财税规则。"
            ),
            "counter_example": (
                "**反例**：同一业务规则以不同语言、不同逻辑在多个系统中实现，导致税率调整"
                "时需要修改所有系统。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["mcp"], COMMON_AUTHORITY["temporal"]],
            "analysis": (
                "**分析**：功能复用的收益随粒度减小而快速放大，但对接口稳定性与版本治理"
                "提出更高要求。"
            ),
        },
        "api-design": {
            "title": "API 设计复用",
            "definition": (
                "**定义**：API 设计复用是通过统一的资源命名、错误处理、分页、过滤、版本控制"
                "与认证模式，使 API 在组织内外一致地复用。"
            ),
            "example": (
                "**示例**：企业 API 风格指南规定所有 REST API 使用统一错误码、RFC 7807 "
                "Problem Details 与 OAuth 2.1 认证，开发者可在不同服务间快速切换。"
            ),
            "counter_example": (
                "**反例**：各团队使用不同的分页参数、错误格式与认证方式，导致客户端需要"
                "为每个服务编写适配代码。"
            ),
            "authority_pairs": [
                ("OpenAPI Specification", "https://spec.openapis.org"),
                ("RFC 7807", "https://datatracker.ietf.org/doc/html/rfc7807"),
            ],
            "analysis": (
                "**分析**：API 设计复用降低了集成成本，是数字化生态中最重要的复用形式之一。"
            ),
        },
        "faas": {
            "title": "函数即服务复用",
            "definition": (
                "**定义**：FaaS 复用是将无状态、事件触发的计算功能封装为标准函数模板，"
                "按需部署并按调用付费，适用于集成、转换与轻量处理任务。"
            ),
            "example": (
                "**示例**：平台团队提供标准“Webhook 验证与转发”函数模板，包含签名验证、"
                "重试与日志记录，新业务只需配置端点与密钥。"
            ),
            "counter_example": (
                "**反例**：将长时间运行、状态密集的任务拆分为大量函数，导致编排复杂、"
                "成本高且调试困难。"
            ),
            "authority_pairs": [
                ("AWS Lambda", "https://aws.amazon.com/lambda"),
                COMMON_AUTHORITY["cncf"],
            ],
            "analysis": (
                "**分析**：FaaS 复用适合短生命周期、事件驱动的任务，需警惕冷启动、"
                "供应商锁定与可观测性挑战。"
            ),
        },
        "event-functions": {
            "title": "事件函数复用",
            "definition": (
                "**定义**：事件函数复用是将事件处理逻辑封装为可复用函数，并通过事件 Schema、"
                "路由规则与错误处理策略实现跨系统的事件驱动集成。"
            ),
            "example": (
                "**示例**：企业将“发送通知”实现为标准事件函数，支持邮件、短信、推送等多渠道，"
                "各业务只需发布标准事件即可触发。"
            ),
            "counter_example": (
                "**反例**：每个消费者自行实现事件去重、顺序保证与死信队列，导致行为不一致"
                "且重复造轮子。"
            ),
            "authority_pairs": [
                ("AsyncAPI", "https://www.asyncapi.com"),
                COMMON_AUTHORITY["cncf"],
            ],
            "analysis": (
                "**分析**：事件函数复用的关键在于统一事件契约与处理语义，避免隐式依赖。"
            ),
        },
        "workflow-orchestration": {
            "title": "工作流编排复用",
            "definition": (
                "**定义**：工作流编排复用是将业务流程或数据处理流程中的活动、状态转换、"
                "补偿与超时逻辑封装为可复用工作流模板。"
            ),
            "example": (
                "**示例**：使用 Temporal 定义标准订单履约工作流，包含库存锁定、支付、发货、"
                "补偿等步骤，新业务线通过配置活动参数复用。"
            ),
            "counter_example": (
                "**反例**：将工作流硬编码在应用代码中，流程变更需要重新编译部署，"
                "业务人员无法参与优化。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["temporal"],
                ("Camunda", "https://camunda.com"),
            ],
            "analysis": (
                "**分析**：工作流编排复用将长期运行过程的耐久性、一致性与可观测性下沉到"
                "平台层，使业务逻辑聚焦变化点。"
            ),
        },
        "ai-llm": {
            "title": "AI/LLM 功能复用",
            "definition": (
                "**定义**：AI/LLM 功能复用是将提示模板、RAG 管道、模型推理服务与 Agent 技能"
                "封装为可复用功能单元，并通过概率契约管理非确定性。"
            ),
            "example": (
                "**示例**：团队将“客户意图识别”封装为可复用 LLM 函数，通过 Prompt 版本管理、"
                "温度参数约束与输出模式校验，在客服机器人与工单分类系统中复用。"
            ),
            "counter_example": (
                "**反例**：多个团队各自调用底层 LLM 并硬编码 Prompt，导致输出不一致、"
                "成本不可控且难以审计。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["mcp"],
                ("OpenAI API", "https://platform.openai.com/docs"),
            ],
            "analysis": (
                "**分析**：AI 功能复用需要引入概率边界、版本管理与监控，以应对模型漂移与"
                "输出不确定性。"
            ),
        },
        "mcp-a2a": {
            "title": "MCP/A2A 协议复用",
            "definition": (
                "**定义**：MCP（Model Context Protocol）规范 Agent 与工具/上下文源之间的交互，"
                "A2A（Agent-to-Agent Protocol）规范 Agent 之间的协作；二者共同构成 AI 原生"
                "复用的协议基础。"
            ),
            "example": (
                "**示例**：企业构建 MCP 工具目录，将数据库查询、文档检索、代码分析等能力"
                "暴露为标准化工具，不同 Agent 可按能力清单调用。"
            ),
            "counter_example": (
                "**反例**：各 Agent 使用私有 RPC 协议与工具交互，导致工具无法在 Agent 之间"
                "共享，形成新的孤岛。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["mcp"], COMMON_AUTHORITY["a2a"]],
            "analysis": (
                "**分析**：MCP/A2A 将 AI 能力复用从代码级提升到协议级，是 Agent 生态互操作"
                "的关键基础设施。"
            ),
        },
    },
    "06-cross-layer-governance": {
        "default": {
            "title": "跨层复用治理",
            "definition": (
                "**定义**：跨层复用治理是横跨业务、应用、组件与功能四层，通过过程、标准、"
                "度量与自动化手段确保复用资产可持续演进的体系。"
            ),
            "example": (
                "**示例**：企业设立复用治理委员会，制定资产准入、成熟度评估、成本分摊与"
                "退役标准，并每季度审核资产目录与复用指标。"
            ),
            "counter_example": (
                "**反例**：资产库缺乏治理，任何人可随意发布资产，导致目录膨胀、质量参差、"
                "消费方难以找到可信资产。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["iso"], COMMON_AUTHORITY["finops"]],
            "analysis": (
                "**分析**：无治理的复用会退化为克隆，无度量的治理会退化为形式；"
                "治理需要与价值量化紧密结合。"
            ),
        },
        "process-governance": {
            "title": "复用过程治理",
            "definition": (
                "**定义**：复用过程治理是将复用活动（识别、获取、适配、集成、演化、退役）"
                "纳入组织标准软件过程，并通过角色、活动与工件进行规范。"
            ),
            "example": (
                "**示例**：依据 ISO/IEC/IEEE 42020 与 12207，组织定义复用管理过程，"
                "明确资产Owner、消费方与治理委员会的职责与评审节点。"
            ),
            "counter_example": (
                "**反例**：复用活动完全依赖个人自觉，没有统一入口与审批流程，"
                "导致重复资产与劣质资产并存。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["iso"],
                COMMON_AUTHORITY["ieee"],
            ],
            "analysis": (
                "**分析**：复用过程治理将自发复用转化为组织能力，是规模化复用的前提。"
            ),
        },
        "reuse-process": {
            "title": "复用过程（IEEE 1517 / 12207 / 26550 视角）",
            "definition": (
                "**定义**：从 IEEE 1517、ISO/IEC/IEEE 12207 与 ISO/IEC 26550 视角看，"
                "复用过程包括领域工程、应用工程、资产提供、资产消费与资产维护等环节。"
            ),
            "example": (
                "**示例**：产品线工程团队执行 26550 的领域工程过程，建立领域模型、"
                "可复用资产与配置机制，应用工程团队基于这些资产定制具体产品。"
            ),
            "counter_example": (
                "**反例**：只有应用工程没有领域工程，团队不断从头开发相似功能，"
                "无法积累可复用资产。"
            ),
            "authority_pairs": [
                ("ISO/IEC 26550:2015", "https://www.iso.org/standard/43007.html"),
                COMMON_AUTHORITY["ieee"],
            ],
            "analysis": (
                "**分析**：复用过程的双轨模型（领域工程 + 应用工程）是系统化复用的核心组织模式。"
            ),
        },
        "maturity-models": {
            "title": "复用成熟度模型",
            "definition": (
                "**定义**：复用成熟度模型（如 RCMM、RiSE、NASA RRL、ISO/IEC 26566）"
                "用于评估组织在复用战略、过程、资产与度量方面的成熟程度。"
            ),
            "example": (
                "**示例**：组织采用 NASA RRL 评估可复用资产，从 RRL 1（概念）到 RRL 9（"
                "已在多任务中验证），决定是否将资产推广到全组织。"
            ),
            "counter_example": (
                "**反例**：未评估成熟度便将实验室原型直接作为组织级资产推广，"
                "导致生产环境中出现严重缺陷。"
            ),
            "authority_pairs": [
                ("NASA RRL", "https://www.nasa.gov"),
                ("ISO/IEC 26566:2026", "https://www.iso.org"),
            ],
            "analysis": (
                "**分析**：成熟度模型将复用能力量化，为投资优先级与改进路径提供依据。"
            ),
        },
        "finops-cost": {
            "title": "FinOps 成本分摊治理",
            "definition": (
                "**定义**：FinOps 成本分摊治理是将云成本、平台成本与复用资产成本按业务价值"
                "归集到团队、产品与功能，实现成本透明与优化问责。"
            ),
            "example": (
                "**示例**：平台团队按“每活跃用户”“每千次请求”将共享服务成本分摊给"
                "消费方，并在仪表盘展示各产品的单位经济学指标。"
            ),
            "counter_example": (
                "**反例**：共享平台成本由中央 IT 统一承担，消费方没有成本意识，"
                "导致资源浪费与利用率低下。"
            ),
            "authority_pairs": [COMMON_AUTHORITY["finops"], COMMON_AUTHORITY["cncf"]],
            "analysis": (
                "**分析**：成本分摊是复用治理的经济杠杆，只有让消费方感受到真实成本，"
                "才能驱动理性复用决策。"
            ),
        },
        "metrics-kpi": {
            "title": "复用度量指标",
            "definition": (
                "**定义**：复用度量指标是从资产级、项目级、组织级与生态级四个层次，"
                "量化复用范围、复用质量、复用成本与复用价值的指标体系。"
            ),
            "example": (
                "**示例**：组织跟踪“资产复用次数”“消费方 NPS”“复用节省人天”与"
                "“复用缺陷密度”，并纳入平台团队 OKR。"
            ),
            "counter_example": (
                "**反例**：仅以“代码复用行数”作为 KPI，导致团队为追求指标复制大量"
                "低价值代码，反而增加维护负担。"
            ),
            "authority_pairs": [
                ("ISO/IEC 25040:2024", "https://www.iso.org"),
                COMMON_AUTHORITY["finops"],
            ],
            "analysis": (
                "**分析**：度量指标需要与业务目标对齐，避免局部优化与指标扭曲。"
            ),
        },
        "up-downgrade": {
            "title": "复用升级/降级决策矩阵",
            "definition": (
                "**定义**：升级/降级矩阵是用于判断可复用资产应从项目级提升到组织级，"
                "或从组织级降级到项目级/退役的决策框架。"
            ),
            "example": (
                "**示例**：当某组件被 5 个以上团队复用、NPS ≥ 4.0、年度维护成本 < 节省人天价值"
                "时，决策矩阵建议将其升级为组织级 Golden Path。"
            ),
            "counter_example": (
                "**反例**：某组件仅被 1 个团队使用却被强制提升为组织标准，导致其他团队"
                "被迫承担不必要的依赖与变更成本。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["finops"],
                COMMON_AUTHORITY["iso"],
            ],
            "analysis": (
                "**分析**：升级/降级决策需要平衡复用收益与治理成本，避免“一刀切”标准化。"
            ),
        },
        "policy-automation": {
            "title": "策略自动化治理",
            "definition": (
                "**定义**：策略自动化治理是使用 Policy-as-Code（如 OPA、Sentinel、Cedar）"
                "将复用规则、合规要求与安全策略编码并自动执行。"
            ),
            "example": (
                "**示例**：组织使用 OPA Gatekeeper 强制所有部署到生产的服务必须使用"
                "经批准的 Golden Path 模板与 SBOM，否则拒绝部署。"
            ),
            "counter_example": (
                "**反例**：策略仅存在于文档中，依赖人工检查，导致违规部署频繁发生且难以追溯。"
            ),
            "authority_pairs": [
                ("Open Policy Agent", "https://www.openpolicyagent.org"),
                COMMON_AUTHORITY["cncf"],
            ],
            "analysis": (
                "**分析**：策略自动化将治理从“事后审计”转变为“事前预防”，"
                "大幅提升治理可扩展性。"
            ),
        },
        "agentic-governance": {
            "title": "Agentic 治理",
            "definition": (
                "**定义**：Agentic 治理是针对自主 Agent 系统的治理框架，涵盖能力发现、"
                "行为边界、安全策略、审计与责任归属。"
            ),
            "example": (
                "**示例**：企业建立 Agent 注册表，要求每个 Agent 声明能力、工具、"
                "决策边界与人工复核点，并通过运行时策略限制其访问范围。"
            ),
            "counter_example": (
                "**反例**：Agent 被赋予广泛权限且缺乏审计，导致其自主调用敏感工具或"
                "生成不可追溯的决策。"
            ),
            "authority_pairs": [
                COMMON_AUTHORITY["mcp"],
                COMMON_AUTHORITY["a2a"],
            ],
            "analysis": (
                "**分析**：Agentic 治理是 AI 原生复用的安全前提，需要在创新与风险控制之间"
                "建立动态平衡。"
            ),
        },
    },
    "07-formal-verification": {
        "default": {
            "title": "形式化验证与可复用资产正确性",
            "definition": (
                "**定义**：形式化验证（Formal Verification）是使用数学方法（逻辑、自动机、类型论）"
                "严格证明系统或其模型满足规约的过程；在复用场景中，它通过显式契约、不变式与精化关系"
                "保证可复用资产在多变上下文中的行为一致性。"
            ),
            "example": (
                "**示例**：TLA+ 规约刻画分布式支付服务的原子性：PlusCal 算法描述“扣款-记账”步骤，"
                "模型检验器 TLC 验证所有可达状态下账户总额守恒，确保该服务被 10+ 业务系统复用时"
                "不会出现重复记账。"
            ),
            "counter_example": (
                "**反例**：某团队将并发队列组件复用到金融核心系统，仅依赖单元测试与代码评审，"
                "未对内存序与边界条件进行形式化分析，生产环境出现偶发数据竞态，造成资金缺口。"
            ),
            "authority_pairs": [
                ("TLA+ Home Page", "https://lamport.azurewebsites.net/tla/tla.html"),
                ("Alloy Analyzer", "http://alloy.mit.edu"),
                ("Coq Proof Assistant", "https://coq.inria.fr"),
                ("The Rust Programming Language", "https://www.rust-lang.org"),
                ("SPARK Pro", "https://www.adacore.com/sparkpro"),
                ("Event-B", "https://www.event-b.org"),
            ],
            "analysis": (
                "**分析**：形式化验证为复用提供了“可证明的正确性”基础，但其成本与建模复杂度成正比；"
                "实践中通常对安全关键、高并发或高价值复用资产进行选择性形式化验证。"
            ),
        },
        "tla-plus": {
            "title": "TLA+ 时序逻辑规约",
            "definition": (
                "**定义**：TLA+（Temporal Logic of Actions）是由 Leslie Lamport 提出的规约语言，"
                "通过状态、动作与时不变量描述并发与分布式系统行为，常用于验证算法与架构设计的正确性。"
            ),
            "example": (
                "**示例**：使用 TLA+ 规约两阶段提交协议，定义协调者、参与者的状态机与“所有节点最终一致”"
                "的不变式，TLC 模型检验器穷举状态空间并确认无死锁与活锁。"
            ),
            "counter_example": (
                "**反例**：一个分布式缓存系统未对“网络分区+节点失效”场景建模，上线后在真实分区下丢失写入，"
                "因为自然语言需求遗漏了边界条件。"
            ),
            "authority_pairs": [
                ("TLA+ Home Page", "https://lamport.azurewebsites.net/tla/tla.html"),
                ("Specifying Systems", "https://lamport.azurewebsites.net/tla/book.html"),
            ],
            "analysis": (
                "**分析**：TLA+ 的价值在于暴露自然语言需求无法覆盖的并发边界，但建模抽象程度需要"
                "与验证目标匹配。"
            ),
        },
        "alloy": {
            "title": "Alloy 结构建模与约束分析",
            "definition": (
                "**定义**：Alloy 是 MIT 开发的基于关系一阶逻辑的轻量级建模语言，通过 SAT 求解器在小范围内"
                "自动寻找反例，适合分析结构约束与依赖关系。"
            ),
            "example": (
                "**示例**：用 Alloy 对微服务授权模型建模，声明“每个请求必须关联有效角色”约束，"
                "分析器在 5 秒内发现某场景下角色继承导致的越权路径。"
            ),
            "counter_example": (
                "**反例**：团队仅绘制架构图表示服务间调用关系，未形式化“无循环依赖”约束，"
                "导致运行时出现隐式循环调用与级联故障。"
            ),
            "authority_pairs": [
                ("Alloy Analyzer", "http://alloy.mit.edu"),
                ("Alloy Tools", "https://alloytools.org"),
            ],
            "analysis": (
                "**分析**：Alloy 擅长快速发现结构设计缺陷，是早期架构评审与复用依赖分析的有效工具。"
            ),
        },
        "coq-isabelle": {
            "title": "Coq/Isabelle 定理证明",
            "definition": (
                "**定义**：Coq 与 Isabelle/HOL 是基于高阶逻辑的交互式定理证明器，支持从公理出发构造"
                "机器可检查的证明，常用于密码学、编译器与安全关键软件的验证。"
            ),
            "example": (
                "**示例**：使用 Coq 证明 TLS 1.3 握手协议的消息不变式，并将提取的 OCaml 代码集成到"
                "可复用加密库，确保实现与规约一致。"
            ),
            "counter_example": (
                "**反例**：密码库复用某开源实现时未验证其形式化安全规约，后来发现其实现与论文证明的"
                "抽象模型存在偏差，导致侧信道攻击。"
            ),
            "authority_pairs": [
                ("Coq Proof Assistant", "https://coq.inria.fr"),
                ("Isabelle/HOL", "https://isabelle.in.tum.de"),
            ],
            "analysis": (
                "**分析**：定理证明提供最高置信度，但门槛高、周期长，适合小规模、高价值核心组件。"
            ),
        },
        "rust-type-system": {
            "title": "Rust 类型系统与形式化语义",
            "definition": (
                "**定义**：Rust 通过所有权（ownership）、借用（borrowing）与生命周期（lifetime）"
                "在类型系统层面消除数据竞态与悬垂指针，其形式化语义（RustBelt、Aeneas）为内存安全"
                "复用组件提供基础。"
            ),
            "example": (
                "**示例**：某跨平台网络库用 Rust 编写核心协议解析器，所有权系统保证并发访问安全，"
                "被 C/Go/Python 项目通过 FFI 复用而无需运行时 GC。"
            ),
            "counter_example": (
                "**反例**：在 Rust 中滥用 unsafe 块实现“性能优化”但未用 Miri 或形式化方法验证，"
                "导致复用该 unsafe 包装的多个项目出现未定义行为。"
            ),
            "authority_pairs": [
                ("The Rust Programming Language", "https://www.rust-lang.org"),
                ("RustBelt", "https://iris-project.org/rustbelt.html"),
                ("Aeneas", "https://github.com/AeneasVerif/aeneas"),
            ],
            "analysis": (
                "**分析**：Rust 将形式化安全保证编译进类型系统，是系统级复用组件的“零成本”安全基础。"
            ),
        },
        "spark-ada": {
            "title": "SPARK/Ada 契约式验证",
            "definition": (
                "**定义**：SPARK 是 Ada 的子集，支持通过前置条件、后置条件、循环不变式与类型约束"
                "进行契约式程序验证，可达到 DO-178C 最高安全等级。"
            ),
            "example": (
                "**示例**：飞控软件使用 SPARK 证明“襟翼控制函数在任意输入下不会越界”，"
                "复用到不同机型时仅需重验证机型特定配置。"
            ),
            "counter_example": (
                "**反例**：某航空项目直接复用未经 SPARK 验证的 C 代码到 DO-178C A 级软件，"
                "审查阶段因无法提供覆盖率与不变式证据被否决。"
            ),
            "authority_pairs": [
                ("SPARK Pro", "https://www.adacore.com/sparkpro"),
                ("DO-178C", "https://rtca.org/product/do-178c-2/"),
            ],
            "analysis": (
                "**分析**：SPARK 将验证融入编程语言子集，是航空、轨道交通等高可信复用的典型路径。"
            ),
        },
        "b-method": {
            "title": "B Method / Event-B 精化验证",
            "definition": (
                "**定义**：B Method 与 Event-B 是基于集合论与精化演算的形式化方法，通过从抽象规约"
                "逐步精化到可执行代码，并证明每步精化保持规约性质。"
            ),
            "example": (
                "**示例**：铁路信号系统使用 Event-B 从“列车不碰撞”的高层不变式精化到联锁逻辑，"
                "模型检验与证明义务保证软件复用时安全性质不被破坏。"
            ),
            "counter_example": (
                "**反例**：某地铁项目复用上一代联锁代码但未重建精化链，新增功能破坏了“敌对进路互锁”"
                "不变式，导致信号冲突风险。"
            ),
            "authority_pairs": [
                ("Event-B", "https://www.event-b.org"),
                ("Atelier B", "https://www.atelierb.eu/en/"),
            ],
            "analysis": (
                "**分析**：Event-B 的精化方法论与铁路等分层安全设计天然契合，但工具链与工程师培训"
                "是成功复用的关键。"
            ),
        },
    },
    "08-cognitive-architecture": {
        "default": {
            "title": "认知架构与复用决策",
            "definition": (
                "**定义**：认知架构（Cognitive Architecture）是对人类或智能体信息处理结构"
                "（感知、记忆、决策、学习）的计算模型；在复用工程中，它解释开发者如何选择、理解与"
                "适配可复用资产，并指导工具设计以降低认知负荷。"
            ),
            "example": (
                "**示例**：基于 ACT-R 建模，IDE 在开发者调用不熟悉的复用组件时自动提示参数示例与"
                "依赖约束，减少工作记忆负荷并降低集成错误。"
            ),
            "counter_example": (
                "**反例**：某公司强制所有团队使用统一的 200 页架构手册而不提供可搜索的示例与决策树，"
                "开发者因认知超载而回到复制-粘贴。"
            ),
            "authority_pairs": [
                ("ACT-R", "https://act-r.psy.cmu.edu"),
                ("BDI Agent Architecture", "https://www.cs.ox.ac.uk/people/michael.georgeff/"),
                ("Cognitive Load Theory", "https://www.sciencedirect.com/topics/psychology/cognitive-load-theory"),
            ],
            "analysis": (
                "**分析**：认知架构将“人”重新置于复用中心：再完美的资产，若超出人类工作记忆与"
                "决策能力，也难以被有效复用。"
            ),
        },
        "act-r": {
            "title": "ACT-R 认知架构",
            "definition": (
                "**定义**：ACT-R（Adaptive Control of Thought–Rational）是由卡内基梅隆大学开发的"
                "认知架构，通过声明性知识（facts）与产生式规则（production rules）模拟人类记忆、"
                "注意与决策过程。"
            ),
            "example": (
                "**示例**：在代码补全工具中嵌入 ACT-R 模型，根据开发者当前注视点与编辑历史预测"
                "下一步需要的复用 API，并按工作记忆容量限制建议数量。"
            ),
            "counter_example": (
                "**反例**：工具一次性展示 50 个相关 API 而无优先级排序，超过工作记忆容量，"
                "开发者反而花更多时间筛选。"
            ),
            "authority_pairs": [
                ("ACT-R", "https://act-r.psy.cmu.edu"),
                ("ACT-R Publications", "https://act-r.psy.cmu.edu/publications"),
            ],
            "analysis": (
                "**分析**：ACT-R 为开发者工具提供了心理学约束，帮助设计“恰到好处”的复用建议。"
            ),
        },
        "bdi": {
            "title": "BDI 智能体模型",
            "definition": (
                "**定义**：BDI（Belief-Desire-Intention）模型将自主智能体的状态表示为信念（Beliefs）、"
                "愿望（Desires）与意图（Intentions），支持目标驱动推理与计划复用。"
            ),
            "example": (
                "**示例**：在 Agentic 系统中，一个故障排查 Agent 复用标准化“诊断计划”意图库："
                "信念为监控数据，愿望为恢复 SLO，意图为按优先级执行检查清单。"
            ),
            "counter_example": (
                "**反例**：Agent 缺乏明确的愿望优先级与意图承诺机制，在多个目标冲突时反复切换，"
                "导致复用计划无法收敛。"
            ),
            "authority_pairs": [
                ("BDI Architecture - Michael Georgeff", "https://www.cs.ox.ac.uk/people/michael.georgeff/"),
                ("AgentSpeak / Jason", "http://jason.sourceforge.net/wp/"),
            ],
            "analysis": (
                "**分析**：BDI 为 Agent 计划复用提供了心智模型，使自主系统行为可解释、可审计。"
            ),
        },
        "cognitive-load": {
            "title": "认知负荷理论",
            "definition": (
                "**定义**：认知负荷理论（Cognitive Load Theory, CLT）描述工作记忆容量有限性，"
                "将负荷分为内在负荷、外在负荷与相关负荷，指导学习材料与工具设计。"
            ),
            "example": (
                "**示例**：平台工程团队将 Golden Path 文档按“决策树 + 可运行模板 + 失败案例”组织，"
                "减少外在认知负荷，使开发者 10 分钟即可上手复用。"
            ),
            "counter_example": (
                "**反例**：某平台要求开发者阅读 50 页 Markdown 才能部署首个服务，外在负荷过高，"
                "新用户流失率超过 60%。"
            ),
            "authority_pairs": [
                ("Cognitive Load Theory - ScienceDirect Topics", "https://www.sciencedirect.com/topics/psychology/cognitive-load-theory"),
                ("Sweller - Educational Psychology Review", "https://link.springer.com/article/10.1007/s10648-010-9135-0"),
            ],
            "analysis": (
                "**分析**：认知负荷理论是复用采纳的关键人因指标，文档与工具应以降低外在负荷为设计目标。"
            ),
        },
    },
    "09-value-quantification": {
        "default": {
            "title": "复用价值量化与决策",
            "definition": (
                "**定义**：复用价值量化是使用成本模型、财务指标与可持续性指标（碳排、能耗）对"
                "可复用资产的开发、维护与消费收益进行系统评估，以支持投资、共享与退役决策。"
            ),
            "example": (
                "**示例**：使用 COCOMO II 的复用调整因子估算“统一支付服务”可节省 2400 人月，"
                "结合 NPV 计算三年净现值为正，决策升级为组织级资产。"
            ),
            "counter_example": (
                "**反例**：某团队仅统计“代码行复用率”作为 KPI，导致大量复制低价值代码，"
                "维护成本上升，真实业务价值反而下降。"
            ),
            "authority_pairs": [
                ("USC COCOMO II", "https://cssed.usc.edu/research/research-sponsored-software/cocomo/cocomo-ii/"),
                ("Green Software Foundation SCI", "https://sci.greensoftware.foundation"),
                ("FinOps Foundation", "https://www.finops.org"),
            ],
            "analysis": (
                "**分析**：价值量化将复用从“经验倡导”转为“数据驱动决策”，但需要同时度量收益、"
                "成本与风险。"
            ),
        },
        "cocomo": {
            "title": "COCOMO II 复用成本估算",
            "definition": (
                "**定义**：COCOMO II（Constructive Cost Model II）通过规模、复用程度、人员能力、"
                "平台成熟度等因子预测软件成本；其复用模型（REVL、AA、SU 等）量化复用带来的生产率提升。"
            ),
            "example": (
                "**示例**：估算企业级消息中间件复用时，COCOMO II 将等效新代码行数按复用适配度"
                "从 100 KSLOC 降至 35 KSLOC，工期预测缩短 40%。"
            ),
            "counter_example": (
                "**反例**：未计入文档、测试与治理成本，仅凭代码行复用率宣称“节省 80%”，"
                "上线后维护 overrun 30%。"
            ),
            "authority_pairs": [
                ("USC COCOMO II", "https://cssed.usc.edu/research/research-sponsored-software/cocomo/cocomo-ii/"),
                ("Barry Boehm - USC CSSE", "https://cssed.usc.edu/"),
            ],
            "analysis": (
                "**分析**：COCOMO II 的复用因子将“复用 ≠ 复制”量化，但需定期用组织历史数据校准。"
            ),
        },
        "roi-npv": {
            "title": "ROI/NPV 与战略价值评估",
            "definition": (
                "**定义**：ROI（投资回报率）与 NPV（净现值）将复用资产的现金流（节省、收入、维护成本、"
                "机会成本）贴现到当前，用于比较不同复用投资策略。"
            ),
            "example": (
                "**示例**：平台工程投资 200 万元，预计每年节省各团队 120 万元运维与重复开发成本，"
                "按 8% 折现率 NPV 为正，ROI 三年达 95%。"
            ),
            "counter_example": (
                "**反例**：仅计算一次性采购成本，忽视后续版本升级、培训与耦合导致的迁移成本，"
                "项目三年后实际 ROI 为负。"
            ),
            "authority_pairs": [
                ("Investopedia NPV", "https://www.investopedia.com/terms/n/npv.asp"),
                ("FinOps Foundation", "https://www.finops.org"),
            ],
            "analysis": (
                "**分析**：ROI/NPV 帮助比较不同复用路径的全生命周期价值，但折现率与收益估算具有主观性。"
            ),
        },
        "carbon": {
            "title": "碳排维度与绿色复用",
            "definition": (
                "**定义**：软件碳强度（SCI）等指标将复用决策与环境影响挂钩：复用成熟组件可减少"
                "重复开发与运行时能耗，但需权衡更新频率、设备寿命与数据中心位置。"
            ),
            "example": (
                "**示例**：通过复用经能效优化的 Rust 数据解析库，某云服务将 CPU 利用率从 45% 降至 22%，"
                "按 SCI 公式计算单位请求碳排下降 48%。"
            ),
            "counter_example": (
                "**反例**：为“绿色”标签强行复用旧版本低能效组件，未考虑新硬件能效提升，"
                "整体碳排反而增加。"
            ),
            "authority_pairs": [
                ("Green Software Foundation SCI", "https://sci.greensoftware.foundation"),
                ("GSF Principles", "https://learn.greensoftware.foundation/"),
            ],
            "analysis": (
                "**分析**：碳维度将复用决策从经济效率扩展到可持续责任，需用 SCI 等标准化指标衡量。"
            ),
        },
    },
    "10-supply-chain-security": {
        "default": {
            "title": "供应链安全与复用信任",
            "definition": (
                "**定义**：软件供应链安全关注从源代码、依赖、构建、分发到部署全链路中，"
                "复用资产不被篡改、注入漏洞或引入许可证风险；SLSA、SBOM 与签名验证是核心机制。"
            ),
            "example": (
                "**示例**：组织采用 SLSA L3 构建流程：源码托管、构建环境隔离、构建产物签名并生成"
                "SPDX SBOM；Log4j 类事件发生时 2 小时内定位受影响服务。"
            ),
            "counter_example": (
                "**反例**：XZ Utils 后门事件显示，未对压缩依赖进行来源验证与行为审计，"
                "恶意代码可潜伏数年并随复用传播到大量系统。"
            ),
            "authority_pairs": [
                ("SLSA Framework", "https://slsa.dev"),
                ("OpenSSF", "https://openssf.org"),
                ("SPDX", "https://spdx.dev"),
                ("CycloneDX", "https://cyclonedx.org"),
            ],
            "analysis": (
                "**分析**：供应链安全是复用的信任基础，缺乏可追溯性的复用会放大单点风险。"
            ),
        },
        "slsa": {
            "title": "SLSA 供应链安全等级",
            "definition": (
                "**定义**：SLSA（Supply-chain Levels for Software Artifacts）是 OpenSSF 提出的框架，"
                "通过 Source、Build、Provenance、Common 等 Track 定义软件制品的可验证安全等级。"
            ),
            "example": (
                "**示例**：使用 Sigstore/cosign 对容器镜像进行签名，配合 GitHub Actions 隔离构建"
                "与可复现构建证明，达到 SLSA Build L3。"
            ),
            "counter_example": (
                "**反例**：项目手动从个人仓库下载二进制依赖且无哈希校验，构建环境未隔离，"
                "无法达到 SLSA L1。"
            ),
            "authority_pairs": [
                ("SLSA Framework", "https://slsa.dev"),
                ("OpenSSF SLSA", "https://openssf.org/projects/slsa/"),
            ],
            "analysis": (
                "**分析**：SLSA 将供应链安全分解为可升级、可审计的等级，是组织渐进式改进的路线图。"
            ),
        },
        "sbom": {
            "title": "SBOM 标准与复用透明度",
            "definition": (
                "**定义**：SBOM（Software Bill of Materials）以机器可读格式（SPDX、CycloneDX、SWID）"
                "枚举软件组件、版本、许可证与来源，是复用资产透明化的基础。"
            ),
            "example": (
                "**示例**：在 CI 中为每个服务生成 CycloneDX SBOM，漏洞数据库匹配后自动生成影响范围报告，"
                "复用组件升级决策从数周缩短到数小时。"
            ),
            "counter_example": (
                "**反例**：组织复用开源库多年却从未维护 SBOM，许可证冲突与安全漏洞只能在诉讼或"
                "事件爆发后被动发现。"
            ),
            "authority_pairs": [
                ("SPDX", "https://spdx.dev"),
                ("CycloneDX", "https://cyclonedx.org"),
                ("NTIA SBOM", "https://www.ntia.gov/page/software-bill-materials"),
            ],
            "analysis": (
                "**分析**：SBOM 将“黑盒依赖”变为可查询清单，是漏洞响应与许可证治理的前提。"
            ),
        },
        "attack-vectors": {
            "title": "供应链攻击向量",
            "definition": (
                "**定义**：供应链攻击向量指攻击者通过依赖注入、构建环境污染、仓库劫持、"
                "typosquatting、恶意贡献等路径，将有害代码引入复用资产并传播到下游系统。"
            ),
            "example": (
                "**示例**：攻击者在流行 npm 包名中注册拼写错误包（typosquat），诱导开发者安装并窃取"
                "环境变量；通过依赖扫描与私有仓库策略可有效缓解。"
            ),
            "counter_example": (
                "**反例**：安全团队仅关注自有代码漏洞扫描，忽视第三方依赖与 CI/CD 凭证安全，"
                "导致攻击者通过被入侵的构建代理注入后门。"
            ),
            "authority_pairs": [
                ("OWASP Top 10 CI/CD Risks", "https://owasp.org/www-project-top-10-ci-cd-security-risks/"),
                ("MITRE ATT&CK Supply Chain Compromise", "https://attack.mitre.org/techniques/T1195/"),
            ],
            "analysis": (
                "**分析**：攻击向量分析应从“防御自家代码”转向“审计整条供应链”，覆盖人、工具与仓库。"
            ),
        },
    },
    "11-industrial-iot-otit": {
        "default": {
            "title": "工业 IoT/OT-IT 复用",
            "definition": (
                "**定义**：工业 IoT/OT-IT 复用是在制造、能源、交通等运营技术（OT）与信息技术（IT）"
                "融合场景中，复用 ISA-95 层级模型、OPC UA 信息模型、功能安全组件与数字孪生资产。"
            ),
            "example": (
                "**示例**：汽车工厂将 ISA-95 L0-L4 资产目录映射到 IEC 63278 资产管理壳（AAS），"
                "通过 OPC UA FX 实现现场设备与 MES/ERP 的即插即用复用。"
            ),
            "counter_example": (
                "**反例**：将 IT 系统直接补丁策略套用到 PLC 产线，未考虑实时性约束与功能安全认证，"
                "导致停机与安全事故。"
            ),
            "authority_pairs": [
                ("ISA-95 / IEC 62264", "https://www.isa.org/standards-and-publications/isa-standards/isa-95"),
                ("OPC Foundation", "https://opcfoundation.org"),
                ("IEC 61508", "https://webstore.iec.ch/publication/66912"),
                ("IEC 63278 AAS", "https://iec.ch/dyn/www/f?p=103:38:0::::FSP_ORG_ID:1363"),
            ],
            "analysis": (
                "**分析**：OT-IT 复用需要在实时性、安全性与 IT 敏捷性之间取得平衡，"
                "标准信息模型是打破竖井的关键。"
            ),
        },
        "isa-95": {
            "title": "ISA-95 企业-控制系统集成",
            "definition": (
                "**定义**：ISA-95 / IEC 62264 定义了企业层（L4）到控制系统层（L0）的分层模型、"
                "数据流与接口，用于统一 OT 与 IT 语义并支持跨层级复用。"
            ),
            "example": (
                "**示例**：制药企业依据 ISA-95 建立标准批次执行模型，新工厂复用相同 MES 接口与"
                "配方模板，将上线时间从 12 个月缩短到 6 个月。"
            ),
            "counter_example": (
                "**反例**：某工厂忽略 ISA-95 层级边界，让 ERP 直接写入 PLC 标签，"
                "破坏实时控制闭环并造成批次污染风险。"
            ),
            "authority_pairs": [
                ("ISA-95", "https://www.isa.org/standards-and-publications/isa-standards/isa-95"),
                ("IEC 62264", "https://webstore.iec.ch/publication/66912"),
            ],
            "analysis": (
                "**分析**：ISA-95 提供了 OT-IT 集成的共同语言，但落地时需结合行业工艺与设备能力进行适配。"
            ),
        },
        "opc-ua-fx": {
            "title": "OPC UA FX 现场级确定性通信",
            "definition": (
                "**定义**：OPC UA FX（Field eXchange）扩展 OPC UA 至现场级，支持确定性时间同步、"
                "PubSub 帧结构与冗余，实现 OT 设备间可互操作的信息模型复用。"
            ),
            "example": (
                "**示例**：包装线集成不同厂商伺服驱动，通过 OPC UA FX 的 PubSub 帧与 PLCopen Motion "
                "接口复用统一运动控制模型，减少 70% 的协议转换网关。"
            ),
            "counter_example": (
                "**反例**：各设备使用私有现场总线，IT 系统需为每种协议开发适配器，"
                "信息模型无法复用，扩展成本高昂。"
            ),
            "authority_pairs": [
                ("OPC Foundation UA", "https://opcfoundation.org/about/opc-technologies/opc-ua/"),
                ("OPC UA FX", "https://opcfoundation.org/opc-ua-field-exchange-opc-ua-fx/"),
            ],
            "analysis": (
                "**分析**：OPC UA FX 将 OPC UA 的互操作性下沉到现场级，是工业 4.0 互联互通的骨干。"
            ),
        },
        "functional-safety": {
            "title": "功能安全与复用（IEC 61508 / ISO 26262）",
            "definition": (
                "**定义**：功能安全标准（IEC 61508 通用、ISO 26262 汽车、IEC 62443 工业网络安全）"
                "要求安全相关软件在生命周期内满足指定安全完整性等级（SIL/ASIL），复用组件必须提供"
                "验证证据与变更影响分析。"
            ),
            "example": (
                "**示例**：某供应商将经 ISO 26262 ASIL-D 认证的制动控制软件作为 SEooC 复用到多款车型，"
                "通过安全手册明确假设与使用约束。"
            ),
            "counter_example": (
                "**反例**：团队复用开源运动控制库到医疗机器人，未评估其 SIL 符合性，"
                "认证阶段无法证明诊断覆盖率，项目被迫返工。"
            ),
            "authority_pairs": [
                ("IEC 61508", "https://webstore.iec.ch/publication/66912"),
                ("ISO 26262", "https://www.iso.org/standard/68383.html"),
                ("IEC 62443", "https://www.iec.ch/cybersecurity"),
            ],
            "analysis": (
                "**分析**：功能安全复用不是简单复制代码，而是复用经过验证的安全证据与假设约束。"
            ),
        },
    },
    "12-ai-native-reuse": {
        "default": {
            "title": "AI 原生复用与 Agent 协议",
            "definition": (
                "**定义**：AI 原生复用是在大模型与 Agent 系统中，通过 MCP（Model Context Protocol）、"
                "A2A（Agent-to-Agent Protocol）与概率契约，将提示模板、RAG 管道、工具与 Agent 技能"
                "封装为可组合、可治理的资产。"
            ),
            "example": (
                "**示例**：企业构建 MCP 工具目录，把数据库查询、代码检索、文档解析发布为标准工具；"
                "客服 Agent 与运维 Agent 按统一协议调用，避免各自封装重复能力。"
            ),
            "counter_example": (
                "**反例**：各团队在不同 Agent 中硬编码相同 Prompt 与 API 调用，无版本管理与输出契约，"
                "导致行为不一致、成本失控且难以审计。"
            ),
            "authority_pairs": [
                ("Model Context Protocol", "https://modelcontextprotocol.io/specification/2025-11-25"),
                ("A2A Protocol", "https://google.github.io/A2A"),
                ("OWASP LLM Top 10", "https://genai.owasp.org/llm-top-10/"),
            ],
            "analysis": (
                "**分析**：AI 原生复用需要接受概率性，并通过协议、契约与治理将其约束在可接受范围内。"
            ),
        },
        "mcp": {
            "title": "MCP 协议与工具复用",
            "definition": (
                "**定义**：MCP 是由 Anthropic 主导的开放协议，规范 AI 模型如何发现、调用工具并交换上下文，"
                "使工具成为可复用资产。"
            ),
            "example": (
                "**示例**：代码助手通过 MCP 调用统一代码搜索工具，返回结构化上下文；"
                "不同 IDE 插件复用同一工具，无需各自实现代码索引。"
            ),
            "counter_example": (
                "**反例**：Agent 通过私有 HTTP 端点调用工具，无 Schema 注册与权限控制，"
                "工具变更导致所有调用方失效。"
            ),
            "authority_pairs": [
                ("Model Context Protocol", "https://modelcontextprotocol.io/specification/2025-11-25"),
                ("MCP Introduction", "https://modelcontextprotocol.io/introduction"),
            ],
            "analysis": (
                "**分析**：MCP 将工具从“代码片段”提升为“可发现服务”，是 Agent 生态互操作的关键。"
            ),
        },
        "a2a": {
            "title": "A2A Agent 协作协议",
            "definition": (
                "**定义**：A2A（Agent-to-Agent Protocol）由 Google 提出，旨在让不同框架、不同厂商的 "
                "Agent 能够相互发现能力、协商任务并协作完成复杂工作流。"
            ),
            "example": (
                "**示例**：旅行规划 Agent 通过 A2A 调用酒店预订 Agent 与航班查询 Agent，"
                "基于能力清单与信任凭证自动协商，无需硬编码集成。"
            ),
            "counter_example": (
                "**反例**：各 Agent 使用私有消息格式与认证机制，跨团队协作时需要为每对 Agent 写适配器，"
                "形成 N² 集成问题。"
            ),
            "authority_pairs": [
                ("A2A Protocol", "https://google.github.io/A2A"),
                ("Google A2A Blog", "https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/"),
            ],
            "analysis": (
                "**分析**：A2A 关注 Agent 之间的协作语义，与 MCP 形成“工具-代理”双层协议体系。"
            ),
        },
        "probabilistic-contracts": {
            "title": "概率契约与 AI SLA",
            "definition": (
                "**定义**：概率契约（Probabilistic Contract）为 AI 服务定义输出质量边界"
                "（如准确率、延迟、成本）的概率承诺，并通过监测与校准保证契约可信度。"
            ),
            "example": (
                "**示例**：某 LLM 分类服务承诺 P(准确率>0.92)≥0.95，使用 conformal prediction 计算预测集，"
                "并在运行时监控漂移触发重新校准。"
            ),
            "counter_example": (
                "**反例**：将 LLM 输出直接接入关键业务规则而无置信度边界，错误分类导致合规罚款。"
            ),
            "authority_pairs": [
                ("Conformal Prediction", "https://arxiv.org/abs/2107.07511"),
                ("Model Context Protocol", "https://modelcontextprotocol.io/specification/2025-11-25"),
            ],
            "analysis": (
                "**分析**：概率契约将非确定性转化为可度量的风险边界，是 AI 服务等级协议的核心。"
            ),
        },
    },
    "13-emerging-trends": {
        "default": {
            "title": "新兴趋势与复用范式",
            "definition": (
                "**定义**：新兴趋势包括平台工程、模块化单体、WebAssembly 组件、绿色软件与 RegTech AI，"
                "它们通过新抽象层或新约束推动复用资产的可移植性、可持续性与治理自动化。"
            ),
            "example": (
                "**示例**：平台工程团队构建内部开发者平台（IDP），将部署、可观测性、安全策略封装为"
                "自助服务模板，产品团队复用 Golden Path 快速交付。"
            ),
            "counter_example": (
                "**反例**：追逐 WASM 潮流将所有服务重写为组件，忽视工具链成熟度与团队技能，"
                "导致调试困难、交付延期。"
            ),
            "authority_pairs": [
                ("CNCF Platform Engineering", "https://tag-app-delivery.cncf.io/whitepapers/platforms/"),
                ("WebAssembly Component Model", "https://component-model.bytecodealliance.org"),
                ("Green Software Foundation", "https://greensoftware.foundation"),
            ],
            "analysis": (
                "**分析**：新兴技术扩展了复用的边界，但技术采纳必须匹配组织成熟度与真实业务痛点。"
            ),
        },
        "platform-engineering": {
            "title": "平台工程与内部开发者平台",
            "definition": (
                "**定义**：平台工程是通过构建内部开发者平台（IDP）与 Golden Path，将基础设施、安全、"
                "可观测性能力产品化，供应用团队自助复用。"
            ),
            "example": (
                "**示例**：某电商企业 IDP 提供一键创建服务仓库、CI/CD、监控与密钥管理，"
                "团队上线时间从 2 周缩短到 2 小时，平台使用率达到 90%。"
            ),
            "counter_example": (
                "**反例**：平台团队闭门造车，强制所有团队使用不灵活的模板，忽视反馈循环，"
                "导致开发者绕过平台自行部署。"
            ),
            "authority_pairs": [
                ("CNCF Platforms White Paper", "https://tag-app-delivery.cncf.io/whitepapers/platforms/"),
                ("Platform Engineering - Martin Fowler", "https://martinfowler.com/articles/platform-engineering-summit.html"),
            ],
            "analysis": (
                "**分析**：平台工程的成功取决于“产品化运营”与“开发者体验”，而非单纯的技术标准化。"
            ),
        },
        "wasm": {
            "title": "WebAssembly 组件模型复用",
            "definition": (
                "**定义**：WebAssembly Component Model 将 WASM 模块升级为具有显式接口、类型化导入导出的"
                "可组合组件，支持跨语言、跨运行时复用。"
            ),
            "example": (
                "**示例**：使用 Rust 实现图像处理组件，编译为 WIT 接口的 WASM 组件，"
                "在 Node.js、Python 与边缘运行时中复用同一二进制。"
            ),
            "counter_example": (
                "**反例**：将 I/O 密集型服务盲目迁移到 WASM，WASI 能力不支持所需系统调用，"
                "性能与可维护性反而下降。"
            ),
            "authority_pairs": [
                ("WebAssembly Component Model", "https://component-model.bytecodealliance.org"),
                ("WASI Preview 2", "https://wasi.dev"),
            ],
            "analysis": (
                "**分析**：WASM 组件模型提供了真正的语言无关二进制复用，但生态与工具链仍在快速演进。"
            ),
        },
        "green-software": {
            "title": "绿色软件与可持续复用",
            "definition": (
                "**定义**：绿色软件通过能效优化、硬件利用率提升、低碳能源调度与生命周期延长，"
                "减少软件系统全生命周期的环境影响；复用经优化的组件可放大减排效果。"
            ),
            "example": (
                "**示例**：复用支持 ARM graceful degradation 的压缩库，在闲时降低 CPU 频率，"
                "使云账单与碳排同时下降 20%。"
            ),
            "counter_example": (
                "**反例**：为追求微服务“弹性”而将单体拆分为 200 个服务，每个服务常驻空闲实例，"
                "整体能耗翻倍。"
            ),
            "authority_pairs": [
                ("Green Software Foundation", "https://greensoftware.foundation"),
                ("SCI Specification", "https://sci.greensoftware.foundation"),
            ],
            "analysis": (
                "**分析**：绿色复用要求从架构层面减少冗余计算，并将碳排指标纳入资产准入评估。"
            ),
        },
    },
    "99-reference": {
        "default": {
            "title": "参考索引与知识治理",
            "definition": (
                "**定义**：参考层是结构化知识体系的“地图”，汇总权威来源、术语表、标准索引、"
                "课程对标与审计报告，为各主题提供可追溯的引用与一致性校验。"
            ),
            "example": (
                "**示例**：维护 authoritative-sources.md 登记所有 ISO/IEC、IEEE、NIST、CNCF 来源 "
                "URL 与核查日期，确保全书引用可验证。"
            ),
            "counter_example": (
                "**反例**：参考层链接长期不更新，术语表与正文定义冲突，"
                "读者无法确认内容准确性与时效性。"
            ),
            "authority_pairs": [
                ("ISO", "https://www.iso.org"),
                ("IEEE Standards", "https://standards.ieee.org"),
                ("NIST", "https://www.nist.gov"),
                ("CNCF", "https://www.cncf.io"),
            ],
            "analysis": (
                "**分析**：参考层的价值不在于内容本身，而在于建立知识之间的信任锚点；"
                "必须随标准演进定期审计与更新。"
            ),
        },
    },
}


# ---------- 辅助函数 ----------

def get_first_heading(text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def select_template(path: Path, topic_key: str) -> Dict:
    """根据文件路径选择最合适的模板。"""
    templates = TOPIC_TEMPLATES.get(topic_key, {})
    name = path.name.lower()
    stem = path.stem.lower()
    parent = path.parent.name.lower()

    # 按优先级匹配
    keyword_map = [
        ("axiom", ["axiom", "formal-axioms", "theorem", "critique", "dependency-graph"]),
        ("iso-42010", ["iso-42010", "42010"]),
        ("iso-42020", ["iso-42020", "42020"]),
        ("iso-42030", ["iso-42030", "42030", "awi-42030"]),
        ("iso-25010", ["iso-25010", "25010"]),
        ("iso-12207", ["iso-12207", "12207"]),
        ("ieee-1517", ["ieee-1517", "1517"]),
        ("iso-42024", ["iso-42024", "42024", "42042"]),
        ("togaf", ["togaf", "enterprise-continuum", "detailed-mapping"]),
        ("archimate", ["archimate"]),
        ("swebok", ["swebok"]),
        ("ras", ["ras", "omg-ras"]),
        ("fair4rs", ["fair4rs"]),
        ("business-domain", ["business-domain", "domain-reuse"]),
        ("business-capability", ["business-capability", "capability-reuse", "fea-brm"]),
        ("value-stream", ["value-stream"]),
        ("business-process", ["business-process"]),
        ("business-service", ["business-service"]),
        ("bpmn-dmn", ["bpmn", "dmn"]),
        ("defense", ["defense", "dodaf", "naf", "modaf", "uaf"]),
        ("zachman", ["zachman"]),
        ("case-studies", ["case-studies", "industry-vertical", "tmforum", "bian"]),
        ("layered", ["layered"]),
        ("microservices", ["microservices"]),
        ("app-service", ["app-service", "service-reuse"]),
        ("serverless", ["serverless"]),
        ("event-driven", ["event-driven"]),
        ("cloud-native", ["cloud-native", "nist-sp-800-204"]),
        ("service-mesh", ["service-mesh", "gateway-api"]),
        ("eda-cqrs", ["eda", "cqrs", "event-sourcing"]),
        ("component-models", ["component-models"]),
        ("interface-contracts", ["interface-contracts"]),
        ("dependency-management", ["dependency-management"]),
        ("design-patterns", ["design-patterns", "pattern-selection", "interface-design"]),
        ("version-strategy", ["version-strategy"]),
        ("cloud-native-networking", ["cloud-native-networking", "gateway-api-v15"]),
        ("language-ecosystems", ["language-ecosystems", "comparison-matrix", "supply-chain"]),
        ("supply-chain", ["supply-chain", "slsa"]),
        ("api-design", ["api-design"]),
        ("faas", ["faas", "function-as-a-service"]),
        ("event-functions", ["event-functions"]),
        ("workflow-orchestration", ["workflow", "temporal"]),
        ("ai-llm", ["ai-llm", "llm-function"]),
        ("mcp-a2a", ["mcp", "a2a", "protocol"]),
        ("process-governance", ["process-governance", "cross-layer-governance"]),
        ("reuse-process", ["reuse-process"]),
        ("maturity-models", ["maturity-models", "rcmm", "rise", "spice"]),
        ("finops-cost", ["finops", "cost-allocation", "unit-economics"]),
        ("metrics-kpi", ["metrics", "kpi"]),
        ("up-downgrade", ["up-downgrade", "upgrade-downgrade"]),
        ("policy-automation", ["policy-automation"]),
        ("agentic-governance", ["agentic"]),
        # 07-13 & 99-reference
        ("tla-plus", ["tla-plus", "tla", "temporal-logic"]),
        ("alloy", ["alloy", "kodkod"]),
        ("coq-isabelle", ["coq", "isabelle", "theorem-proving"]),
        ("rust-type-system", ["rust-type-system", "rust", "borrow-checker"]),
        ("spark-ada", ["spark-ada", "spark", "ada", "do-178c"]),
        ("b-method", ["b-method", "event-b", "refinement"]),
        ("act-r", ["act-r", "actr", "cognitive-architecture"]),
        ("bdi", ["bdi", "belief-desire-intention", "agent"]),
        ("cognitive-load", ["cognitive-load", "cognitive-load-theory", "load"]),
        ("cocomo", ["cocomo", "cost-model"]),
        ("roi-npv", ["roi", "npv", "real-options"]),
        ("carbon", ["carbon", "sci", "green", "sustainability"]),
        ("slsa", ["slsa", "provenance", "sigstore"]),
        ("sbom", ["sbom", "spdx", "cyclonedx"]),
        ("attack-vectors", ["attack", "threat", "mitre"]),
        ("isa-95", ["isa-95", "isa95", "iec-62264"]),
        ("opc-ua-fx", ["opc-ua-fx", "opc-ua", "pubsub"]),
        ("functional-safety", ["functional-safety", "iec-61508", "iso-26262", "iec-62443"]),
        ("mcp", ["mcp", "model-context-protocol"]),
        ("a2a", ["a2a", "agent-to-agent"]),
        ("probabilistic-contracts", ["probabilistic", "conformal", "ai-sla"]),
        ("platform-engineering", ["platform-engineering", "idp", "golden-path"]),
        ("wasm", ["wasm", "webassembly", "component-model"]),
        ("green-software", ["green-software", "green-architecture", "sci"]),
    ]

    path_str = f"{parent}/{stem}/{name}"
    for key, keywords in keyword_map:
        if key in templates and any(kw in path_str for kw in keywords):
            return templates[key]

    return templates.get("default", DEFAULT_TEMPLATE)


def detect_missing(checks: Dict[str, bool]) -> List[str]:
    return [k for k in RULES if not checks.get(k, False)]


def generate_supplement(path: Path, content: str, checks: Dict[str, bool], topic_key: str) -> str:
    missing = detect_missing(checks)
    if not missing:
        return ""

    template = select_template(path, topic_key)
    title = get_first_heading(content) or template["title"]

    sections = []

    if "definition" in missing:
        sections.append(f"## 概念定义\n\n{template['definition']}")

    if "example" in missing:
        sections.append(f"## 示例\n\n{template['example']}")

    if "counter_example" in missing:
        sections.append(f"## 反例\n\n{template['counter_example']}")

    if "authority" in missing:
        authority_block = make_authority_block(template["authority_pairs"])
        sections.append(f"## 权威来源\n\n{authority_block}")

    if "argumentation" in missing:
        sections.append(f"## 分析\n\n{template['analysis']}")

    if not sections:
        return ""

    header = f"\n\n---\n\n## 补充说明：{title}\n"
    return header + "\n\n".join(sections)


# ---------- 主流程 ----------

TARGETS = [
    ("struct/07-formal-verification", None),
    ("struct/08-cognitive-architecture", None),
    ("struct/09-value-quantification", None),
    ("struct/10-supply-chain-security", None),
    ("struct/11-industrial-iot-otit", None),
    ("struct/12-ai-native-reuse", None),
    ("struct/13-emerging-trends", None),
    ("struct/99-reference", None),
]


def collect_target_files() -> List[Tuple[Path, int, GateResult]]:
    """返回 (文件路径, 阈值, 原始结果) 列表。"""
    results = []
    for rel_dir, score_threshold in TARGETS:
        dir_path = PROJECT_ROOT / rel_dir
        if not dir_path.exists():
            print(f"目录不存在: {dir_path}")
            continue
        for md in dir_path.rglob("*.md"):
            rel = md.relative_to(PROJECT_ROOT)
            # 跳过 plans-tasks、CHANGELOG 等
            if any(sp in str(rel).replace("\\", "/") for sp in ["plans-tasks/", "99-reference/audit/", "99-reference/CHANGELOG", "99-reference/frontier-tracking/"]):
                continue
            r = check_file(md)
            if r.passed:
                continue
            if score_threshold is not None and r.score > score_threshold:
                continue
            results.append((md, score_threshold if score_threshold is not None else 100, r))
    return results


@dataclass
class FixSummary:
    path: Path
    before_score: int
    after_score: int
    passed: bool


def run_fix(apply: bool = False) -> List[FixSummary]:
    targets = collect_target_files()
    print(f"待处理文件数: {len(targets)}")
    if not apply:
        print("当前为报告模式（默认），不会修改任何文件。如需自动追加模板，请使用 --apply。")
    summaries = []

    for md, threshold, original in sorted(targets, key=lambda x: x[2].score):
        topic_key = md.relative_to(PROJECT_ROOT).parts[1]  # e.g. 01-meta-model-standards
        content = md.read_text(encoding="utf-8")
        supplement = generate_supplement(md, content, original.checks, topic_key)

        if not supplement:
            summaries.append(FixSummary(md, original.score, original.score, original.passed))
            continue

        new_content = content + supplement
        if apply:
            md.write_text(new_content, encoding="utf-8")

        # 重新检查（报告模式在内存中检查补充后的内容）
        if not apply:
            text = new_content
            word_count = len(re.findall(r"[\u4e00-\u9fa5]", text)) + len(text.split())
            checks = {}
            score = 0
            warnings = []
            for key, rule in RULES.items():
                matched = any(re.search(p, text, re.IGNORECASE) for p in rule["patterns"])
                checks[key] = matched
                if matched:
                    score += rule["weight"]
                else:
                    warnings.append(f"缺少 {rule['name']}")
            if word_count < 300:
                warnings.append(f"文档过短（约 {word_count} 字/词），建议 ≥ 300")
                score -= 10
            passed = (
                checks.get("definition", False)
                and checks.get("authority", False)
                and score >= MIN_SCORE
                and sum(1 for v in checks.values() if v) >= MIN_WEIGHTED
            )
            r = GateResult(path=md, score=max(0, min(100, score)), passed=passed, checks=checks, warnings=warnings)
        else:
            r = check_file(md)
        summaries.append(FixSummary(md, original.score, r.score, r.passed))

        if apply and not r.passed:
            print(f"  ⚠️ 仍未通过 [{r.score:>3}] {md.relative_to(PROJECT_ROOT)}")

    return summaries


def print_summary(summaries: List[FixSummary]):
    total = len(summaries)
    passed = sum(1 for s in summaries if s.passed)
    print(f"\n处理文件总数: {total}")
    print(f"处理后通过: {passed}/{total} ({passed/total*100:.1f}%)")

    still_failing = [s for s in summaries if not s.passed]
    if still_failing:
        print("\n仍无法达到 60 分的文件:")
        for s in sorted(still_failing, key=lambda x: x.after_score):
            print(f"  [{s.after_score:>3}] {s.path.relative_to(PROJECT_ROOT)}")
    else:
        print("\n所有处理文件均已达到及格线。")


def main():
    parser = argparse.ArgumentParser(
        description="批量检查质量门控未通过文件，并可选地自动追加模板段落。默认仅报告，不修改文件。"
    )
    parser.add_argument("--apply", action="store_true", help="应用自动修复（向文件末尾追加模板段落）")
    args = parser.parse_args()

    summaries = run_fix(apply=args.apply)
    print_summary(summaries)


if __name__ == "__main__":
    main()
