# 软件工程架构复用视角：结构化知识体系

> **版本**: 2026-06-06
> **定位**: 基于 `view/` 全部文档内容全面梳理后，对齐网络权威国际化内容，构建的可持续推进主题结构
> **对齐标准**: ISO/IEC/IEEE 42010:2022, 26550:2015, 26566:2026, TOGAF 10, SLSA 1.0, IEC 61508, ISA-95
> **权威参考**: Carnegie Mellon SEI, USC COCOMO II, ETH Zurich (RustBelt/Prusti), Inria (Aeneas), NASA RRL

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
  - [5. 文件夹结构导航](#5-文件夹结构导航)
  - [6. 持续推进路线图](#6-持续推进路线图)

---

## 1. 体系概览

本结构将 `view/` 中约 **31 万字** 的 8 份文档，按照 **13 个一级主题**、**约 80 个二级主题** 进行系统化重组，形成可独立演进、可交叉引用的知识模块。

```
软件工程架构复用视角
│
├── 基础层
│   ├── 01 元模型与标准对齐        ← 地基：概念、术语、标准族谱
│   ├── 07 形式化验证              ← 正确性保证：数学证明层
│   └── 08 认知架构                ← 人因工程：开发者决策层
│
├── 层次层（业务→应用→组件→功能）
│   ├── 02 业务架构复用            ← 最粗粒度：能力、价值流、流程
│   ├── 03 应用架构复用            ← 系统级：微服务、单体、数据架构
│   ├── 04 组件架构复用            ← 模块级：框架、库、包、模式
│   └── 05 功能架构复用            ← 最细粒度：算法、函数、AI功能
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
│   └── 13 新兴趋势                ← 平台工程、模块化单体、WASM
│
└── 参考层
    └── 99 参考索引                ← 标准总览、大学课程、术语表
```

---

## 2. 主题与 view/ 文件映射

| 一级主题 | 主要来源文件 | 覆盖范围 |
|----------|-------------|----------|
| 01 元模型与标准对齐 | `software_architecture_reuse_framework_2026.md`, `software_architecture_reuse_full_2026.md` | ISO 420xx、TOGAF 10、ArchiMate、26550 系列 |
| 02 业务架构复用 | `software_architecture_reuse_full_2026.md`, `software_architecture_reuse_extension_2026.md` | FEA BRM、BPMN/DMN、业务能力、价值流 |
| 03 应用架构复用 | `software_architecture_reuse_full_2026.md`, `software_architecture_reuse_extension_2026.md` | 云原生模式、服务网格、EDA、数据网格 |
| 04 组件架构复用 | `software_architecture_reuse_full_2026.md`, `software_architecture_reuse_extension_2026.md` | 依赖治理、供应链安全、语言生态 |
| 05 功能架构复用 | `software_architecture_reuse_full_2026.md`, `software_architecture_reuse_extension_2026.md` | MCP、A2A、Temporal、AI功能 |
| 06 跨层复用治理 | `software_architecture_reuse_full_2026.md`, `software_architecture_reuse_extension_2026.md` | RiSE/RCMM、FinOps、度量指标 |
| 07 形式化验证 | `software_architecture_reuse_deep_extension_2026.md`, `software_architecture_reuse_vol469_deep_2026.md` | TLA+、Alloy、Coq、SPARK/Ada、B Method |
| 08 认知架构 | `software_architecture_reuse_deep_extension_2026.md` | ACT-R、BDI、认知负荷、AI辅助决策 |
| 09 价值量化 | `software_architecture_reuse_deep_extension_2026.md` | COCOMO II、ROI、NPV、FinOps |
| 10 供应链安全 | `software_architecture_reuse_technical_deep_2026.md`, `software_architecture_reuse_vol469_deep_2026.md` | SLSA L4、SBOM、XZ Utils案例 |
| 11 工业 IoT/OT-IT | `software_architecture_reuse_industrial_2026.md`, `software_architecture_reuse_vol5_deep_2026.md` | ISA-95、OPC UA FX、PLCopen、AAS |
| 12 AI 原生复用 | `software_architecture_reuse_full_2026.md`, `software_architecture_reuse_technical_deep_2026.md` | MCP 2026-07-28、A2A v1.0、概率边界 |
| 13 新兴趋势 | `software_architecture_reuse_full_2026.md` | 平台工程、模块化单体、WASM组件 |

---

## 3. 国际标准与权威机构对齐

### 3.1 ISO/IEC/IEEE 核心标准族

| 标准编号 | 主题 | 状态 | 对应文件夹 |
|----------|------|------|-----------|
| ISO/IEC/IEEE 42010:2022 | 架构描述 (AD) | 生效 | `01-meta-model-standards/01-iso-420xx-family` |
| ISO/IEC/IEEE 42020:2019 | 架构过程 | 生效 | `01-meta-model-standards/01-iso-420xx-family` |
| ISO/IEC/IEEE 42030:2019 | 架构评估 | 生效 | `06-cross-layer-governance/02-quality-governance` |
| ISO/IEC/IEEE DIS 42024 | 架构基础 | 草案 | `01-meta-model-standards/01-iso-420xx-family` |
| ISO/IEC/IEEE DIS 42042 | 参考架构 | 草案 | `01-meta-model-standards/01-iso-420xx-family` |
| ISO/IEC 25010:2023 | 质量模型 (SQuaRE) | 生效 | `06-cross-layer-governance/02-quality-governance` |
| ISO/IEC 26550:2015 | 产品线工程参考模型 | 生效 | `01-meta-model-standards/03-iso-26550-ple` |
| ISO/IEC 26566:2026 | 成熟度框架 | **最新** | `06-cross-layer-governance/03-maturity-models` |
| IEEE 1517 | 软件生命周期复用过程 | 生效 | `05-functional-architecture-reuse/04-workflow-orchestration` |

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
| SLSA 1.0 | 供应链安全等级 | 生效 | `10-supply-chain-security/01-slsa-framework` |
| SPDX 2.3 | SBOM 格式 | 生效 | `10-supply-chain-security/02-sbom-standards` |
| CycloneDX 1.6 | SBOM 格式 | 生效 | `10-supply-chain-security/02-sbom-standards` |
| NIST SSDF | 安全软件开发框架 | 生效 | `10-supply-chain-security/04-zero-trust-supply-chain` |
| OWASP SCVS | 软件组件验证标准 | 生效 | `10-supply-chain-security/03-attack-vectors` |
| Sigstore/cosign | 构件签名 | 生效 | `10-supply-chain-security/01-slsa-framework` |

---

## 4. 国际大学课程对标

| 大学/机构 | 课程/研究方向 | 对应主题 | 核心贡献 |
|-----------|--------------|----------|----------|
| **Carnegie Mellon University** (SEI) | Software Architecture, ATAM | 01, 03, 06 | SAAM/ATAM 架构评估方法 |
| **University of Southern California** (USC) | COCOMO II, Software Economics | 09 | Barry Boehm 的成本估算模型 |
| **ETH Zurich** | Systems Group, Prusti | 07, 04 | Rust 形式化验证 (Viper) |
| **Inria Paris** | Gallium, Aeneas | 07, 04 | Rust 借用形式化语义 |
| **MIT CSAIL** | Programming Languages, Formal Methods | 07 | 类型理论、程序验证 |
| **Stanford** | CS 250: Formal Methods | 07 | TLA+、Coq 教学 |
| **TU Munich** | Software & Systems Engineering | 01, 02 | Klaus Pohl 的需求工程与产品线 |
| **University of Duisburg-Essen** | Model-Based Engineering | 01, 02 | 模型一致性、操作上下文 |
| **Technical University of Kosice** | Digital Twin / AAS | 11 | AAS + OPC UA 集成研究 |
| **Airbus / AdaCore** | SPARK/Ada 飞控软件 | 07, 11 | DO-178C 白金级验证 |
| **Siemens / Beckhoff / Rockwell** | Industrial Automation | 11 | OPC UA FX、PLCopen、TSN |
| **Linux Foundation / OpenSSF** | Supply Chain Security | 10 | SLSA、Sigstore、OpenSSF |
| **Google / Anthropic** | Agent Protocols (MCP, A2A) | 12 | 2026 核心协议标准 |

---

## 5. 文件夹结构导航

每个一级主题文件夹内部统一采用以下结构：

```
XX-topic-name/
├── XX-01-subtopic/          # 二级主题子文件夹
├── XX-02-subtopic/
├── ...
├── plans-tasks/             # 该主题下的计划与任务
│   ├── README.md            # 主题概述与当前状态
│   ├── roadmap.md           # 阶段性路线图
│   └── tasks/               # 具体任务分解
└── README.md                # 一级主题总览
```

---

## 6. 持续推进路线图

详见 `MASTER_PLAN.md`。

---

> **注意**: 本结构是"活文档"，随标准演进、技术发展和实践反馈持续更新。
> 最后更新: 2026-06-06
