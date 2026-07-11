# 软件工程架构复用视角：结构化知识体系

> **版本**: 2026-07-07（Phase A 止血与基础修复版）
> **定位**: 基于 `view/` 全部文档内容全面梳理后，对齐网络权威国际化内容，构建的可持续推进主题结构；当前正在进行统计口径校准、模板污染清理与内容深度补齐
> **对齐标准**: ISO/IEC/IEEE 42010:2022, 12207:2026, 15288:2023, 24765, 26550:2015, **26564:2022, 26565:2026**, 26566:2026, **21838 系列**, TOGAF 10, ArchiMate 4.0, SLSA 1.2, IEC 61508 Ed.3 (CDV/认证基准 2026; IEC 正式发布预计 ~2027), ISA-95, MCP 2025-11-25, A2A v1.0.0, OWASP MCP Top 10, Microsoft Agent Governance Toolkit, GSF SCI for AI
> **权威参考**: Carnegie Mellon SEI, USC COCOMO II, ETH Zurich (RustBelt/Prusti), Inria (Aeneas/Coq), NASA RRL

---

## 目录

- [软件工程架构复用视角：结构化知识体系](#软件工程架构复用视角结构化知识体系)
  - [目录](#目录)
  - [1. 体系概览](#1-体系概览)
  - [2. 主题与 view/ 文件映射](#2-主题与-view-文件映射)
  - [3. 国际标准与权威机构对齐](#3-国际标准与权威机构对齐)
    - [3.1 ISO/IEC/IEEE 核心标准族](#31-isoiecieee-核心标准族)
    - [3.2 工业与垂直领域标准](#32-工业与垂直领域标准)
    - [3.3 供应链与软件安全标准](#33-供应链与软件安全标准)
  - [4. 国际大学课程对标](#4-国际大学课程对标)
  - [5. 实际文件夹结构导航](#5-实际文件夹结构导航)
  - [6. 持续推进路线图](#6-持续推进路线图)
  - [7. 反例：目录规划与实际结构长期不一致](#7-反例目录规划与实际结构长期不一致)
  - [8. 权威来源](#8-权威来源)

---

## 1. 体系概览

本结构将 `view/` 中约 **31 万字** 的 8 份文档，按照 **13 个一级主题**、**约 60 个实际二级主题** 进行系统化重组，形成可独立演进、可交叉引用的知识模块。当前 `struct/` 实际包含 **301 个 Markdown 文件**，`view/` 包含 **8 个 Markdown 文件**，累计约 **75.5 万中文字 / 93.1 万总词**。

```text
软件工程架构复用视角
│
├── 基础层
│   ├── 01 元模型与标准对齐        ← 地基：概念、术语、标准族谱、公理体系
│   ├── 07 形式化验证              ← 正确性保证：数学证明层
│   └── 08 认知架构                ← 人因工程：开发者决策层
│
├── 层次层（业务→应用→组件→功能）
│   ├── 02 业务架构复用            ← 最粗粒度：能力、价值流、BPMN/DMN
│   ├── 03 应用架构复用            ← 系统级：云原生、服务网格、数据架构
│   ├── 04 组件架构复用            ← 模块级：语言生态、设计模式
│   └── 05 功能架构复用            ← 最细粒度：工作流、MCP/A2A、AI 功能
│
├── 治理层
│   ├── 06 跨层复用治理            ← 度量、成熟度、FinOps、升级/降级
│   └── 09 价值量化                ← COCOMO II、ROI、战略价值
│
├── 安全层
│   └── 10 供应链安全              ← SLSA、SBOM、零信任纵深防御
│
├── 垂直领域层
│   └── 11 工业 IoT/OT-IT 融合     ← ISA-95、OPC UA FX、功能安全
│
├── 前沿层
│   ├── 12 AI 原生复用             ← MCP、A2A、概率契约、Conformal Prediction
│   └── 13 新兴趋势                ← 平台工程、模块化单体、WASM、RegTech AI
│
└── 参考层
    └── 99 参考索引                ← 标准总览、大学课程、术语表、审计
```

> **说明**: 实际 `struct/` 目录与早期 MASTER_PLAN 的规划树存在差异。本 README 反映的是**实际存在的文件结构**。历史规划中的部分子目录（如 `quantum-computing`、`domain-driven-design`、`coq-isabelle` 等）尚未创建或已合并，详见各主题 README 与 `SUBSEQUENT_PLAN_2026.md`。

---

## 2. 主题与 view/ 文件映射

| 一级主题 | 主要来源文件 | 覆盖范围 |
|----------|-------------|----------|
| 01 元模型与标准对齐 | `software_architecture_reuse_framework_2026.md`, `software_architecture_reuse_full_2026.md` | ISO 420xx、TOGAF 10、ArchiMate、26550 系列、OMG RAS |
| 02 业务架构复用 | `software_architecture_reuse_full_2026.md`, `software_architecture_reuse_extension_2026.md` | FEA BRM、BPMN/DMN、业务能力、价值流 |
| 03 应用架构复用 | `software_architecture_reuse_full_2026.md`, `software_architecture_reuse_extension_2026.md` | 云原生模式、服务网格、EDA、数据网格 |
| 04 组件架构复用 | `software_architecture_reuse_full_2026.md`, `software_architecture_reuse_extension_2026.md` | 设计模式、语言生态、供应链安全 |
| 05 功能架构复用 | `software_architecture_reuse_full_2026.md`, `software_architecture_reuse_extension_2026.md` | MCP、A2A、Temporal、AI 功能 |
| 06 跨层复用治理 | `software_architecture_reuse_full_2026.md`, `software_architecture_reuse_extension_2026.md` | RiSE/RCMM、FinOps、ISO/IEC 26565:2026（产品线成熟度框架）/ 26566:2026（产品线纹理） |
| 07 形式化验证 | `software_architecture_reuse_deep_extension_2026.md`, `software_architecture_reuse_vol469_deep_2026.md` | TLA+、Alloy、Rust、SPARK/Ada、B Method、Coq/Isabelle |
| 08 认知架构 | `software_architecture_reuse_deep_extension_2026.md` | ACT-R、BDI、认知负荷、AI 辅助决策 |
| 09 价值量化 | `software_architecture_reuse_deep_extension_2026.md` | COCOMO II、ROI、NPV、FinOps |
| 10 供应链安全 | `software_architecture_reuse_technical_deep_2026.md`, `software_architecture_reuse_vol469_deep_2026.md` | SLSA 1.1/1.2、SBOM、XZ Utils 案例 |
| 11 工业 IoT/OT-IT | `software_architecture_reuse_industrial_2026.md`, `software_architecture_reuse_vol5_deep_2026.md` | ISA-95、OPC UA FX、PLCopen、AAS |
| 12 AI 原生复用 | `software_architecture_reuse_full_2026.md`, `software_architecture_reuse_technical_deep_2026.md` | MCP 2025-11-25、A2A v1.0、概率边界 |
| 13 新兴趋势 | `software_architecture_reuse_full_2026.md` | 平台工程、模块化单体、WASM 组件 |

---

## 3. 国际标准与权威机构对齐

### 3.1 ISO/IEC/IEEE 核心标准族

| 标准编号 | 主题 | 状态 | 对应文件夹 |
|----------|------|------|-----------|
| ISO/IEC/IEEE 42010:2022 | 架构描述 (AD) | 生效 | `01-meta-model-standards/01-iso-420xx-family` |
| ISO/IEC/IEEE 42020:2019 | 架构过程 | 生效 | `01-meta-model-standards/01-iso-420xx-family` |
| ISO/IEC/IEEE 42030:2019 | 架构评估 | 生效 | `06-cross-layer-governance/03-maturity-models` |
| ISO/IEC/IEEE DIS 42024 | 架构基础 | 草案 | `01-meta-model-standards/01-iso-420xx-family` |
| ISO/IEC/IEEE DIS 42042 | 参考架构 | 草案（预计 2026 定稿） | `01-meta-model-standards/01-iso-420xx-family` |
| ISO/IEC 25010:2023 | 质量模型 (SQuaRE) | 生效 | `01-meta-model-standards/01-iso-420xx-family` |
| ISO/IEC 25040:2024 | 软件质量评估过程 | 生效 | `06-cross-layer-governance/05-metrics-kpi` |
| ISO/IEC 26550:2015 | 产品线工程参考模型 | 生效 | `01-meta-model-standards/03-iso-26550-ple` |
| ISO/IEC/IEEE 12207:2026 | 软件生命周期过程 | **2026-04-29 发布** | `01-meta-model-standards/01-iso-420xx-family` |
| ISO/IEC 26566:2026 | 产品线纹理（product line texture）的方法与工具能力 | **2026-05 正式发布** | `06-cross-layer-governance/03-maturity-models` |
| IEEE 1517-2010 | 软件生命周期复用过程 | 生效 | `01-meta-model-standards/01-iso-420xx-family` |
| OMG RAS v2.2 | 可复用资产规范 | 生效 | `01-meta-model-standards/07-omg-ras` |

### 3.2 工业与垂直领域标准

| 标准编号 | 主题 | 状态 | 对应文件夹 |
|----------|------|------|-----------|
| ISA-95 / IEC 62264 | 企业-控制系统集成 | 生效 | `11-industrial-iot-otit/01-isa-95-model` |
| OPC UA FX 1.0 (2026) | 现场级确定性通信 | **新兴** | `11-industrial-iot-otit/02-opc-ua-fx` |
| IEC/IEEE 60802 TSN | 时间敏感网络 | 草案 | `11-industrial-iot-otit/03-tsn-deterministic` |
| IEC 61508 Ed.3 | 功能安全（含软件复用） | CDV 已完成；TÜV 等认证机构 2026 起可采用；IEC 官方正式发布预计 ~2027 | `11-industrial-iot-otit/06-functional-safety` |
| ISO 21448 Ed.2 | 预期功能安全 (SOTIF) | 制定中/预计 2026 发布 | `11-industrial-iot-otit/06-functional-safety` |
| ISO 26262 | 汽车功能安全 | 生效 | `11-industrial-iot-otit/06-functional-safety` |
| IEC 63278-1 (AAS) | 资产管理壳结构 | ✅ 已发布 (2023) | `11-industrial-iot-otit/05-digital-twin-aas` |
| IEC 63278-2 (AAS) | 信息元模型 | 🔄 DIS ballot / 开发中（预计 2026 末–2027 初发布） | `11-industrial-iot-otit/05-digital-twin-aas` |
| IEC 62443 | 工业网络安全 | 生效 | `11-industrial-iot-otit/06-functional-safety` |

### 3.3 供应链与软件安全标准

| 标准/框架 | 主题 | 状态 | 对应文件夹 |
|-----------|------|------|-----------|
| SLSA 1.2 | 供应链安全等级（Multi-Track） | **Build/Source Track 生效**；Build L4 开发中 | `10-supply-chain-security/01-slsa-framework` |
| SPDX 2.3 | SBOM 格式 | 生效 | `10-supply-chain-security/02-sbom-standards` |
| CycloneDX 1.6 | SBOM 格式 | 生效 | `10-supply-chain-security/02-sbom-standards` |
| NIST SSDF 1.2 | 安全软件开发框架 | Initial Public Draft（预计 2026-Q3 定稿） | `10-supply-chain-security/12-nist-ssdf-update` |
| OWASP SCVS / LLM / Agentic AI / MCP Top 10 | 软件组件验证 / AI 安全 | **MCP/Agentic Top 10 已发布** | `10-supply-chain-security/03-attack-vectors`, `12-ai-native-reuse/06-ai-governance` |
| Microsoft Agent Governance Toolkit | Agent 运行时治理 | **2026-04 开源** | `12-ai-native-reuse/03-agentic-infrastructure` |
| Sigstore/cosign | 构件签名 | 生效 | `10-supply-chain-security/01-slsa-framework` |

---

## 4. 国际大学课程对标

| 大学/机构 | 课程/研究方向 | 对应主题 | 核心贡献 |
|-----------|--------------|----------|----------|
| **Carnegie Mellon University** (SEI) | Software Architecture, ATAM, ADD | 01, 03, 06 | SAAM/ATAM 架构评估、架构战术 |
| **University of Southern California** (USC) | COCOMO II, Software Economics | 09 | Barry Boehm 成本估算模型 |
| **ETH Zurich** | Systems Group, Prusti | 07, 04 | Rust 形式化验证 (Viper) |
| **Inria Paris** | Gallium, Aeneas, Coq | 07, 04 | Rust 借用形式化语义、定理证明 |
| **MIT CSAIL** | Programming Languages, Formal Methods | 07 | 类型理论、程序验证 |
| **Stanford** | CS 250: Formal Methods | 07 | TLA+ 教学 |
| **TU Munich** | Software & Systems Engineering | 01, 02 | Klaus Pohl 需求工程与产品线 |
| **University of Duisburg-Essen** | Model-Based Engineering | 01, 02 | 模型一致性、操作上下文 |
| **Technical University of Kosice** | Digital Twin / AAS | 11 | AAS + OPC UA 集成研究 |
| **Airbus / AdaCore** | SPARK/Ada 飞控软件 | 07, 11 | DO-178C 白金级验证 |
| **Siemens / Beckhoff / Rockwell** | Industrial Automation | 11 | OPC UA FX、PLCopen、TSN |
| **Linux Foundation / OpenSSF** | Supply Chain Security | 10 | SLSA、Sigstore、OpenSSF |
| **Google / Anthropic / LF Agentic AI Foundation** | Agent Protocols (MCP, A2A) | 12 | 2025-11-25 MCP、A2A v1.0 |

---

## 5. 实际文件夹结构导航

> 以下列表反映 `struct/` 目录中**实际存在**的文件和子目录。每个一级主题均包含 `README.md`，部分主题包含 `plans-tasks/roadmap.md`。

```text
struct/
├── 01-meta-model-standards/            # 元模型与标准对齐
│   ├── 01-iso-420xx-family/            # ISO 42010/42020/42030 与 12207 族
│   ├── 02-togaf-10-alignment/          # TOGAF 10 企业架构
│   ├── 03-iso-26550-ple/               # ISO 26550 产品线工程
│   ├── 04-archimate-4/                 # ArchiMate 3.2/4.0
│   ├── 05-swebok-v4/                   # SWEBOK V4 知识领域
│   ├── 06-formal-axioms/               # 形式化公理体系
│   ├── 07-omg-ras/                     # OMG RAS 可复用资产
│   ├── 08-fair4rs/                     # FAIR4RS 研究软件复用
│   ├── 09-sysml-v2/                    # SysML v2 对齐
│   ├── 10-mbse-reuse/                  # MBSE 与复用集成
│   └── plans-tasks/                    # plans tasks
├── 02-business-architecture-reuse/     # 业务架构复用
│   ├── 01-business-domain-reuse/       # 01 business domain reuse
│   ├── 02-business-capability/         # 业务能力建模
│   ├── 03-value-stream/                # 价值流映射
│   ├── 04-business-process-reuse/      # 04 business process reuse
│   ├── 05-business-service-reuse/      # 05 business service reuse
│   ├── 06-bpmn-dmn/                    # BPMN 2.0 / DMN 1.5
│   ├── 07-defense-mission-engineering/ # 国防任务工程
│   ├── 08-zachman-reuse-mapping/       # Zachman 框架复用映射
│   └── case-studies/                   # case studies
├── 03-application-architecture-reuse/  # 应用架构复用
│   ├── 01-layered-architecture/        # 分层架构模式
│   ├── 02-microservices/               # 微服务架构
│   ├── 03-app-service/                 # 应用服务复用
│   ├── 04-serverless/                  # Serverless 架构
│   ├── 05-data-architecture/           # 数据架构复用
│   ├── 06-event-driven/                # 事件驱动架构
│   ├── 07-cloud-native-patterns/       # 云原生复用性矩阵 2026
│   ├── 08-service-mesh/                # 服务网格通信模式
│   ├── 09-eda-cqrs/                    # EDA/CQRS 深度
│   ├── 10-tosca-dmn-platform/          # TOSCA v2.0 / DMN 1.6
│   └── 11-idp-practices/               # IDP 复用实践
├── 04-component-architecture-reuse/    # 组件架构复用
│   ├── 01-component-models/            # 组件模型理论
│   ├── 02-interface-contracts/         # 接口契约设计
│   ├── 03-dependency-management/       # 依赖管理策略
│   ├── 04-design-patterns/             # 设计模式与反模式
│   ├── 05-version-strategy/            # 版本策略
│   ├── 06-cloud-native-networking/     # 云原生网络
│   └── 07-language-ecosystems/         # 6 大语言生态深度对比
├── 05-functional-architecture-reuse/   # 功能架构复用
│   ├── 01-api-design/                  # API 设计模式
│   ├── 02-function-as-a-service/       # FaaS 复用模式
│   ├── 03-event-functions/             # 事件函数模式
│   ├── 04-workflow-orchestration/      # Temporal 工作流复用
│   ├── 05-ai-llm-functions/            # AI/LLM 功能复用
│   └── 06-mcp-a2a-protocols/           # MCP + A2A 协议分析
├── 06-cross-layer-governance/          # 跨层治理与量化
│   ├── 01-process-governance/          # 复用过程治理
│   ├── 02-reuse-process/               # 02 reuse process
│   ├── 03-maturity-models/             # 成熟度模型（RCMM/RiSE/SPICE）
│   ├── 04-finops-cost/                 # FinOps 成本分摊模板
│   ├── 05-metrics-kpi/                 # 四级度量指标体系
│   ├── 06-up-downgrade-matrix/         # 升降级决策矩阵
│   ├── 07-policy-automation/           # 07 policy automation
│   ├── 08-reserved/                    # 预留编号
│   └── 09-agentic-governance/          # Agentic 治理
├── 07-formal-verification/             # 形式化验证
│   ├── 01-tla-plus/                    # TLA+ 案例库
│   ├── 02-alloy/                       # Alloy 案例库
│   ├── 03-coq-isabelle/                # Coq / Isabelle
│   ├── 04-rust-type-system/            # Rust 类型系统深化
│   ├── 05-spark-ada/                   # SPARK/Ada 契约验证
│   ├── 06-b-method/                    # B Method / Event-B
│   ├── 07-vv-standards/                # V&V 标准（IEEE 1012）
│   ├── 08-emerging-trends/             # 形式化验证前沿
│   ├── 09-comparative-matrices/        # 方法对比矩阵
│   └── plans-tasks/                    # plans tasks
├── 08-cognitive-architecture/          # 认知架构
│   ├── 01-act-r-model/                 # ACT-R 模型
│   ├── 02-bdi-model/                   # BDI 模型
│   ├── 03-cognitive-load-theory/       # 认知负荷理论
│   ├── 04-decision-making/             # 决策机制
│   └── 05-ai-cognitive-augmentation/   # AI 认知增强
├── 09-value-quantification/            # 价值量化
│   ├── 01-cocomo-ii-reuse/             # COCOMO II 2026 校准
│   ├── 02-roi-npv-models/              # ROI 与 NPV 模型
│   ├── 03-carbon-dimension/            # 碳排维度
│   └── tools/                          # 工具脚本
├── 10-supply-chain-security/           # 供应链安全
│   ├── 01-slsa-framework/              # SLSA 框架
│   ├── 02-sbom-standards/              # SBOM 标准
│   ├── 03-attack-vectors/              # 攻击向量
│   ├── 04-provenance-examples/         # 来源示例
│   ├── 05-zero-trust-supply-chain/     # 零信任供应链
│   ├── 06-case-studies/                # 案例研究
│   ├── 07-owasp-scvs/                  # OWASP SCVS
│   ├── 08-guac-supply-chain/           # GUAC 供应链图
│   ├── 09-owasp-asvs/                  # OWASP ASVS
│   ├── 10-owasp-top10-2025/            # OWASP Top 10 2025
│   ├── 11-osps-baseline/               # OSPS 基线
│   └── 12-nist-ssdf-update/            # NIST SSDF 更新
├── 11-industrial-iot-otit/             # 工业 IoT / OT-IT 融合
│   ├── 01-isa-95-model/                # ISA-95 五层资产目录
│   ├── 02-opc-ua-fx/                   # OPC UA FX 深化
│   ├── 03-tsn-deterministic/           # TSN 确定性网络
│   ├── 04-plcopen-motion/              # PLCopen Motion
│   ├── 05-digital-twin-aas/            # 数字孪生 / AAS
│   ├── 06-functional-safety/           # 功能安全（IEC 61508 / ISO 26262）
│   ├── 07-edge-ai/                     # 工业边缘 AI
│   ├── 08-digital-twin-general/        # 数字孪生通用
│   ├── 09-network-digital-twin/        # 网络数字孪生
│   └── plans-tasks/                    # plans tasks
├── 12-ai-native-reuse/                 # AI 原生复用
│   ├── 01-mcp-protocol/                # MCP 协议
│   ├── 02-a2a-protocol/                # A2A 协议
│   ├── 03-agentic-infrastructure/      # Agentic Infrastructure
│   ├── 04-hybrid-a2a-mcp-poc/          # A2A/MCP 混合 PoC
│   ├── 05-probabilistic-contracts/     # 概率契约
│   ├── 06-ai-governance/               # AI 治理
│   └── 07-conformal-prediction/        # Conformal Prediction
├── 13-emerging-trends/                 # 前沿趋势
│   ├── 01-platform-engineering/        # 平台工程成熟度
│   ├── 02-modular-monolith/            # 模块化单体
│   ├── 03-webassembly-components/      # WASM Component Model
│   ├── 04-green-architecture/          # 绿色架构
│   ├── 05-rust-ecosystem/              # Rust 生态
│   ├── 06-regtech-ai/                  # RegTech AI
│   ├── 07-green-software/              # 绿色软件
│   ├── 08-reserved/                    # 预留编号
│   └── 09-frontier-tracking/           # 前沿跟踪
└── 99-reference/                       # 参考索引
│   ├── audit/                          # 审计报告
│   ├── chapters/                       # 全书章节框架
│   ├── external-links/                 # 外部链接
│   ├── frontier-tracking/              # 前沿跟踪
│   ├── glossary/                       # 术语表（含主术语表、跨标准对照、公理树）
│   ├── knowledge-index/                # 知识索引
│   ├── standards-index/                # 标准索引
│   ├── templates/                      # 写作模板
│   ├── tools/                          # 工具脚本与模板子目录
│   └── visualizations/                 # 可视化
```

> **历史说明**: 早期 MASTER_PLAN 中规划的部分子目录（如 `02-business-process-reuse`、`03-domain-driven-design`、`01-api-design`、`quantum-computing` 等）在实际演进中被合并、重命名或尚未创建。本导航以实际文件为准。后续如需恢复，按 `SUBSEQUENT_PLAN_2026.md` 执行。
>
> **2026-07-06 更新**: 本次同步根据实际目录修正导航，并标注以下编号特点：
>
> - `03-application-architecture-reuse/` 实际编号为：`03-app-service/`、`04-serverless/`、`05-data-architecture/`、`06-event-driven/`、`07-cloud-native-patterns/`、`08-service-mesh/`、`09-eda-cqrs/`、`10-tosca-dmn-platform/`、`11-idp-practices/`。
> - `04-component-architecture-reuse/` 包含 `06-cloud-native-networking/`（编号 06 为历史保留，与 05 不连续）。
> - `06-cross-layer-governance/` 包含 `09-agentic-governance/`（编号 09 为后续新增，与 07/08 不连续）。
> - `10-supply-chain-security/` 包含 `12-nist-ssdf-update/`（编号 12 为后续新增）。
> - `13-emerging-trends/` 包含 `09-frontier-tracking/`（编号 09 为后续新增）。
>
> 以上编号不连续均为实际演进结果，不影响内容检索；在 Phase 5 全书整合阶段可统一重新编号。

---

## 6. 持续推进路线图

详见：

- `MASTER_PLAN.md` — 总体阶段划分（Phase 0~6）
- `SUBSEQUENT_PLAN_2026.md` — 2026-Q3 → 2027-Q4 详细任务（历史版）
- `SUBSEQUENT_PLAN_2026_NETWORK_ALIGNED_v2.md` — **当前执行版**：2026-07 网络权威对齐后的更新计划

当前处于 **Phase 0 立即修复与交付物验证**（2026-Q3 第 1-2 周），已确认关键决策：

1. **1-A**: 重构目录导航以匹配实际结构。
2. **2-A'**: 形式化验证不安装/不运行工具，仅做内容梳理与校对。
3. **3-A**: 可执行工具采用 Python CLI + Streamlit MVP 策略。
4. **4-A**: 重点 MCP/Agentic 安全、WASI 0.3、Agentic Governance、GreenArch/SCI for AI；暂缓量子计算。
5. **5-A**: 每篇文档列出权威来源 URL 并登记。
6. **6-A**: 建立 IEC 61508 Ed.3 / ISO 21448 Ed.2 跟踪通道。

---

## 7. 反例：目录规划与实际结构长期不一致

本项目早期曾出现规划子目录与实际文件结构系统性偏离的问题，例如：

- `03-application-architecture-reuse/` 中规划的分层架构、微服务、Serverless、事件驱动子目录一度只有占位 README，导致初学者无法建立从单体→分层→微服务→Serverless→事件驱动的完整认知路径。
- `coq-isabelle`、`quantum-computing` 等目录在规划中存在，但实际演进中被合并或暂缓，造成维护者困惑。

**教训**：知识体系结构必须与目录结构同步演进，每次重大结构调整都应更新 README 和 MASTER_PLAN，并记录变更原因。

---

## 8. 权威来源

> **权威来源**:
>
> - ISO/IEC/IEEE 42010:2022. *Systems and software engineering — Architecture description*. <https://www.iso.org/standard/74296.html>
> - The Open Group. *TOGAF® Standard, 10th Edition*. <https://www.opengroup.org/togaf>
> - The Open Group. *ArchiMate® 4 Specification* (2026-04-27 正式发布，Document C260). <https://www.opengroup.org/archimate-licensed-downloads>
> - ISO/IEC 26550:2015. *Software engineering — Reference model for product line engineering and management*. <https://www.iso.org/standard/69529.html>
>
> **核查日期**: 2026-07-07

---

> **注意**: 本结构是"活文档"，随标准演进、技术发展和实践反馈持续更新。每篇新增或更新文档必须列出 1-3 个国际权威来源 URL，并在 `99-reference/standards-index/authoritative-sources-v2.md` 中登记与复核。
>
> 最后更新: 2026-07-07
