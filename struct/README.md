# 软件工程架构复用视角：结构化知识体系

> **版本**: 2026-06-10（目录一致性修复版）
> **定位**: 基于 `view/` 全部文档内容全面梳理后，对齐网络权威国际化内容，构建的可持续推进主题结构
> **对齐标准**: ISO/IEC/IEEE 42010:2022, 26550:2015, 26566:2026, TOGAF 10, SLSA 1.1/1.2, IEC 61508, ISA-95, MCP 2025-11-25, A2A v1.0
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

---

## 1. 体系概览

本结构将 `view/` 中约 **31 万字** 的 8 份文档，按照 **13 个一级主题**、**约 60 个实际二级主题** 进行系统化重组，形成可独立演进、可交叉引用的知识模块。

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
| 06 跨层复用治理 | `software_architecture_reuse_full_2026.md`, `software_architecture_reuse_extension_2026.md` | RiSE/RCMM、FinOps、ISO/IEC 26566:2026 |
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
| ISO/IEC 25010:2024 | 质量模型 (SQuaRE) | 生效 | `01-meta-model-standards/01-iso-420xx-family` |
| ISO/IEC 25040:2024 | 软件质量评估过程 | 生效 | `06-cross-layer-governance/05-metrics-kpi` |
| ISO/IEC 26550:2015 | 产品线工程参考模型 | 生效 | `01-meta-model-standards/03-iso-26550-ple` |
| ISO/IEC 26566:2026 | 产品线工程方法与工具能力 | **2026-05 正式发布** | `06-cross-layer-governance/03-maturity-models` |
| IEEE 1517-2010 | 软件生命周期复用过程 | 生效 | `01-meta-model-standards/01-iso-420xx-family` |
| OMG RAS v2.2 | 可复用资产规范 | 生效 | 待补充（见 `SUBSEQUENT_PLAN_2026.md` P2-T10） |

### 3.2 工业与垂直领域标准

| 标准编号 | 主题 | 状态 | 对应文件夹 |
|----------|------|------|-----------|
| ISA-95 / IEC 62264 | 企业-控制系统集成 | 生效 | `11-industrial-iot-otit/01-isa-95-model` |
| OPC UA FX 1.0 (2026) | 现场级确定性通信 | **新兴** | `11-industrial-iot-otit/02-opc-ua-fx` |
| IEC/IEEE 60802 TSN | 时间敏感网络 | 草案 | `11-industrial-iot-otit/03-tsn-deterministic` |
| IEC 61508-3-1:2016 | 功能安全软件复用 | 生效 | `11-industrial-iot-otit/06-functional-safety` |
| ISO 26262 | 汽车功能安全 | 生效 | `11-industrial-iot-otit/06-functional-safety` |
| IEC 63278 (AAS) | 资产管理壳 | 生效 | `11-industrial-iot-otit/05-digital-twin-aas` |
| IEC 62443 | 工业网络安全 | 生效 | `11-industrial-iot-otit/06-functional-safety` |

### 3.3 供应链与软件安全标准

| 标准/框架 | 主题 | 状态 | 对应文件夹 |
|-----------|------|------|-----------|
| SLSA 1.1 / 1.2 | 供应链安全等级（Multi-Track） | 生效/草案 | `10-supply-chain-security/01-slsa-framework` |
| SPDX 2.3 | SBOM 格式 | 生效 | `10-supply-chain-security/02-sbom-standards` |
| CycloneDX 1.6 | SBOM 格式 | 生效 | `10-supply-chain-security/02-sbom-standards` |
| NIST SSDF 1.2 | 安全软件开发框架 | 征求意见稿 | `10-supply-chain-security/05-case-studies` |
| OWASP SCVS / LLM / MCP / Agentic AI | 软件组件验证 / AI 安全 | 生效 | `10-supply-chain-security/03-attack-vectors`, `12-ai-native-reuse/04-probabilistic-contracts` |
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
├── README.md                         # 本文件
├── MASTER_PLAN.md                    # 总体推进计划
├── SUBSEQUENT_PLAN_2026.md           # 后续计划与任务（2026-2027）
│
├── 01-meta-model-standards/          # 元模型与标准对齐
│   ├── README.md
│   ├── plans-tasks/roadmap.md
│   ├── 01-iso-420xx-family/
│   ├── 02-togaf-10-alignment/
│   ├── 03-iso-26550-ple/
│   ├── 04-archimate-4/
│   ├── 05-swebok-v4/
│   ├── 06-formal-axioms/
│   ├── 07-omg-ras/
│   └── 08-fair4rs/
│
├── 02-business-architecture-reuse/   # 业务架构复用
│   ├── README.md
│   ├── 02-business-capability/
│   ├── 03-value-stream/
│   ├── 06-bpmn-dmn/
│   └── case-studies/
│
├── 03-application-architecture-reuse/ # 应用架构复用
│   ├── README.md
│   ├── 01-layered-architecture/
│   ├── 02-microservices/
│   ├── 03-app-service/
│   ├── 03-serverless/
│   ├── 04-data-architecture/
│   ├── 04-event-driven/
│   ├── 05-cloud-native-patterns/
│   ├── 06-service-mesh/
│   ├── 07-eda-cqrs/
│   └── 07-tosca-dmn-platform/
│
├── 04-component-architecture-reuse/  # 组件架构复用
│   ├── README.md
│   ├── 04-design-patterns/
│   ├── 06-cloud-native-networking/
│   └── 07-language-ecosystems/
│
├── 05-functional-architecture-reuse/ # 功能架构复用
│   ├── README.md
│   ├── 04-workflow-orchestration/
│   ├── 05-ai-llm-functions/
│   └── 06-mcp-a2a-protocols/
│
├── 06-cross-layer-governance/        # 跨层复用治理
│   ├── README.md
│   ├── 01-process-governance/
│   ├── 03-maturity-models/
│   ├── 04-finops-cost/
│   ├── 05-metrics-kpi/
│   └── 06-up-downgrade-matrix/
│
├── 07-formal-verification/           # 形式化验证
│   ├── README.md
│   ├── plans-tasks/roadmap.md
│   ├── 01-tla-plus/
│   ├── 02-alloy/
│   ├── 03-coq-isabelle/
│   ├── 04-rust-type-system/
│   ├── 05-spark-ada/
│   ├── 06-b-method/
│   └── 08-comparative-matrices/
│
├── 08-cognitive-architecture/        # 认知架构
│   ├── README.md
│   ├── 01-act-r-model/
│   ├── 02-bdi-model/
│   ├── 03-cognitive-load-theory/
│   └── 05-ai-cognitive-augmentation/
│
├── 09-value-quantification/          # 价值量化
│   ├── README.md
│   ├── 01-cocomo-ii-reuse/
│   └── 02-roi-npv-models/
│
├── 10-supply-chain-security/         # 供应链安全
│   ├── README.md
│   ├── 01-slsa-framework/
│   ├── 02-sbom-standards/
│   ├── 03-attack-vectors/
│   ├── 04-provenance-examples/
│   ├── 04-zero-trust-supply-chain/
│   └── 05-case-studies/
│
├── 11-industrial-iot-otit/           # 工业 IoT / OT-IT 融合
│   ├── README.md
│   ├── plans-tasks/roadmap.md
│   ├── 01-isa-95-model/
│   ├── 02-opc-ua-fx/
│   ├── 03-tsn-deterministic/
│   ├── 04-plcopen-motion/
│   ├── 05-digital-twin-aas/
│   ├── 06-functional-safety/
│   └── 07-edge-ai/
│
├── 12-ai-native-reuse/               # AI 原生复用
│   ├── README.md
│   ├── 01-mcp-protocol/
│   ├── 02-a2a-protocol/
│   ├── 03-agentic-infrastructure/
│   ├── 03-hybrid-a2a-mcp-poc/
│   ├── 04-probabilistic-contracts/
│   └── 05-conformal-prediction/
│
├── 13-emerging-trends/               # 新兴趋势
│   ├── README.md
│   ├── 01-platform-engineering/
│   ├── 02-modular-monolith/
│   ├── 03-webassembly-components/
│   ├── 04-rust-ecosystem/
│   ├── 05-regtech-ai/
│   └── 06-green-software/
│
└── 99-reference/                     # 参考索引
    ├── README.md
    ├── CHANGELOG.md
    ├── book-format-guide.md
    ├── book-outline.md
    ├── audit/
    ├── chapters/
    ├── external-links/
    ├── glossary/
    ├── standards-index/
    ├── templates/
    ├── tools/
    └── visualizations/
```

> **历史说明**: 早期 MASTER_PLAN 中规划的部分子目录（如 `02-business-process-reuse`、`03-domain-driven-design`、`01-api-design`、`quantum-computing` 等）在实际演进中被合并、重命名或尚未创建。本导航以实际文件为准。后续如需恢复，按 `SUBSEQUENT_PLAN_2026.md` 执行。
>
> **2026-06-08 更新**: 本次同步新增以下实际已创建的子目录：
>
> - `01-meta-model-standards/`: `07-omg-ras/`, `08-fair4rs/`
> - `03-application-architecture-reuse/`: `01-layered-architecture/`, `02-microservices/`, `03-serverless/`, `04-event-driven/`, `07-tosca-dmn-platform/`
> - `04-component-architecture-reuse/`: `06-cloud-native-networking/`
> - `07-formal-verification/`: `03-coq-isabelle/`（此前被标记为未创建，现已恢复）
> - `10-supply-chain-security/`: `04-provenance-examples/`
> - `12-ai-native-reuse/`: `03-hybrid-a2a-mcp-poc/`
> - `99-reference/`: `tools/`
>
> 部分主题存在编号重复的子目录（如 `03-app-service/` 与 `03-serverless/`、`04-data-architecture/` 与 `04-event-driven/`、`07-eda-cqrs/` 与 `07-tosca-dmn-platform/`），此为实际文件状态，后续可在整理阶段统一重新编号。

---

## 6. 持续推进路线图

详见：

- `MASTER_PLAN.md` — 总体阶段划分（Phase 0~6）
- `SUBSEQUENT_PLAN_2026.md` — 2026-Q3 → 2027-Q4 详细任务、国际对齐差距、风险与关键决策

当前处于 **阶段 A 修复完成**，即将进入 **阶段 B：深化与工具化**（2026-Q4 → 2027-Q2）。

阶段 A 已完成：

1. ✅ 修复 roadmap 与实际文件状态不一致（01/07/11 三个 roadmap 已更新）
2. ✅ 统一目录导航与实际结构（本 README 已同步）
3. ✅ 术语查询脚本 T15 已确认交付（`99-reference/tools/terminology-query.py`）
4. ⏸️ 前沿主题（CP+形式化融合、WASI 0.3、Agentic Governance）保持现有深度，按决策 D3 暂停扩展
5. ⏸️ GitBook/网站输出按决策 D4 推迟

---

> **注意**: 本结构是"活文档"，随标准演进、技术发展和实践反馈持续更新。每篇新增或更新文档必须列出 1-3 个国际权威来源 URL，并在 `99-reference/external-links/authoritative-sources.md` 中登记。
>
> 最后更新: 2026-06-10
