# 软件工程架构复用视角：后续计划与任务总览（2026-2027）

> **版本**: 2026-06-10（Phase D/E/F 更新版）
> **定位**: 在 Phase 1 基本完成（2026-06-06 净增 +20,172 行，92 个唯一文件）的基础上，全面梳理未完成项、内容缺口、与国际权威标准的对齐差距，输出 2026-Q3 → 2027-Q4 的后续推进计划
> **对齐来源**: ISO/IEC/IEEE 42010:2022、ISO/IEC 25010:2023、ISO/IEC 26566:2026、ISO/IEC/IEEE DIS 42042、OMG RAS、TOGAF 10、ArchiMate 3.2/4.0、IEEE 1517、SEI/CMU、FAIR4RS、ICSA/ECSA、SLSA 1.1/1.2、MCP 2025-11-25、WASI 0.3、CNCF Platform Engineering Maturity Model

---

## 目录

- [软件工程架构复用视角：后续计划与任务总览（2026-2027）](#软件工程架构复用视角后续计划与任务总览2026-2027)
  - [目录](#目录)
  - [1. 当前完成度总览](#1-当前完成度总览)
  - [2. 未完成计划与任务清单](#2-未完成计划与任务清单)
    - [2.1 显式标注的未完成项（来自 README/roadmap）](#21-显式标注的未完成项来自-readmeroadmap)
    - [2.2 结构性内容缺口（规划目录 vs 实际文件）](#22-结构性内容缺口规划目录-vs-实际文件)
    - [2.3 形式化验证可执行性缺口](#23-形式化验证可执行性缺口)
    - [2.4 工具/模板/可执行交付物缺口](#24-工具模板可执行交付物缺口)
  - [3. 与国际权威内容的差距分析](#3-与国际权威内容的差距分析)
    - [3.1 标准对齐差距](#31-标准对齐差距)
    - [3.2 技术生态差距](#32-技术生态差距)
    - [3.3 学术/会议前沿差距](#33-学术会议前沿差距)
  - [4. 后续推进计划（2026-Q3 → 2027-Q4）](#4-后续推进计划2026-q3--2027-q4)
    - [Phase 1.5 立即修复（2026-Q3 剩余 2-4 周）](#phase-15-立即修复2026-q3-剩余-2-4-周)
    - [Phase 2 形式化与量化深化（2026-Q4）](#phase-2-形式化与量化深化2026-q4)
    - [Phase 3 垂直领域扩展（2027-Q1）](#phase-3-垂直领域扩展2027-q1)
    - [Phase 4 安全与供应链纵深（2027-Q2）](#phase-4-安全与供应链纵深2027-q2)
    - [Phase 5 AI 原生与前沿（2027-Q3）](#phase-5-ai-原生与前沿2027-q3)
    - [Phase 6 整合与输出（2027-Q4）](#phase-6-整合与输出2027-q4)
    - [Phase D 前沿跟踪持续更新（2026-Q2 起，持续）](#phase-d-前沿跟踪持续更新2026-q2-起持续)
    - [Phase E 全书整合与排版（预计 2026-Q3）](#phase-e-全书整合与排版预计-2026-q3)
    - [Phase F 社区反馈与迭代（预计 2026-Q4）](#phase-f-社区反馈与迭代预计-2026-q4)
  - [5. 风险与依赖](#5-风险与依赖)
    - [持续机制补充](#持续机制补充)
    - [待解决项（延期处理）](#待解决项延期处理)
  - [6. 需要确认的关键决策](#6-需要确认的关键决策)
    - [决策 1：目录结构统一策略](#决策-1目录结构统一策略)
    - [决策 2：形式化验证工具链投入（已调整）](#决策-2形式化验证工具链投入已调整)
    - [决策 3：可执行工具开发策略](#决策-3可执行工具开发策略)
    - [决策 4：前沿主题取舍](#决策-4前沿主题取舍)
    - [决策 5：国际对齐深度](#决策-5国际对齐深度)
  - [2026-06-08 HOTFIX 完成记录](#2026-06-08-hotfix-完成记录)

---

## 1. 当前完成度总览

| 维度 | 当前状态 |
|------|----------|
| **一级主题覆盖** | 13/13 已启动（01-13 + 99-reference），全部有实质内容 |
| **Markdown 文件** | 241 个 |
| **形式化资产** | TLA+ × 4、Alloy × 4、Rust 文档 × 4、SPARK/Ada × 3、B Method × 2 |
| **公理-定理体系** | 20 条公理 + 35 条定理 + 5 猜想 + 依赖图 + 批判边界 |
| **本轮完成（2026-06-10）** | Phase A/B/C 全部完成；标准覆盖扩展至 42+ 项；工具链升级至 v2.0 |
| **主要短板** | 可执行模板/工具不足、Coq/Isabelle 空白、目录规划与实际结构不一致、部分前沿主题缺失 |

---

## 2. 未完成计划与任务清单

### 2.1 显式标注的未完成项（来自 README/roadmap）

| 主题 | 未完成内容 | 计划时间 | 优先级 |
|------|-----------|----------|--------|
| 01 元模型 | T15: 术语查询脚本（跨标准术语翻译） | 2026-Q3 | P1 |
| 01 元模型 | DIS 42024/42042 当前 DIS 状态对齐 | ~~待外部事件~~ ✅ 已完成 (`iso-42024-42042-dis-alignment.md`) | P2 |
| 01 元模型 | ArchiMate 4.0 正式发布后的映射更新 | ⏸️ **已冻结** — 经核查 The Open Group 官方尚未发布 ArchiMate 4.0（当前稳定版仍为 3.2），此前"已正式发布"声明已回退为"已正式发布/The Open Group 官方确认" | P2 |
| 03 应用架构 | Backstage / Port / Cortex IDP 复用实践 | 2026-Q4 | P1 |
| 04 组件架构 | Rust 生态深度形式化（所有权、Trait、Cargo SAT） | 07 已大部分完成 | P1 |
| 04 组件架构 | WASM Component Model 跨语言复用分析 | 2026-Q4 | P1 |
| 05 功能架构 | MCP 2025-11-25 权威对齐 | ✅ 已完成 (`mcp-2025-11-25-deep-dive.md`) | P1 |
| 05 功能架构 | AI 功能概率契约校准工具原型 | 2026-Q4 | P0 |
| 06 跨层治理 | 可执行的成熟度评估问卷 | ✅ 已完成 (`assessment-tool.py`) | P1 |
| 06 跨层治理 | FinOps 成本分摊工具模板（Python/Excel） | ✅ 已完成 (`finops-allocation.py` + Excel 导出) | P1 |
| 07 形式化验证 | Alloy 跨层映射 + ISA-95 层次案例 | 2026-Q4 | P1 |
| 07 形式化验证 | Coq/Isabelle 教学示例 | ✅ 已完成 (`insertion_sort.v`, `bounded_counter.v`, `Turnstile.thy`) | P0 |
| 07 形式化验证 | Coq/Isabelle 安全关键组件定理证明 | ⏳ Phase 2 2026-Q4 | P0 |
| 08 认知架构 | 眼动追踪/EEG 实验设计的复用认知研究方案 | 2027-Q1 | P2 |
| 08 认知架构 | AI 辅助复用系统原型设计 | 2026-Q4 | P1 |
| 09 价值量化 | 可执行的 Excel/Python 计算模板 | 2026-Q4 | P1 |
| 09 价值量化 | 跨层 FinOps 成本分摊可执行模板 | 2026-Q4 | P1 |
| 10 供应链安全 | SLSA L4 分布式构建验证（多签名、可复现性） | 2027-Q2 | P1 |
| 10 供应链安全 | 供应链攻击树可视化增强 | 2027-Q2 | P2 |
| 11 工业 IoT | AAS 到 OPC UA NodeSet 的完整映射规范 | 2026-06 第4周（文件已存在，需确认完整度） | P1 |
| 11 工业 IoT | PIU 贝叶斯方法扩展工具 | 2027-Q1 | P1 |
| 11 工业 IoT | PLCopen 功能块 TLA+ 验证 | 2026-06 第4周（文件已存在，需确认完整度） | P1 |
| 12 AI 原生 | Agentic Governance 组织设计模板 | 2026-Q4 | P1 |
| 13 新兴趋势 | RegTech Agentic 架构的案例验证 | 2027-Q3 | P2 |

### 2.2 结构性内容缺口（规划目录 vs 实际文件）

以下主题在顶层 README/MASTER_PLAN 中声明了子目录，但实际 `struct/` 中缺失或命名不一致：

| 主题 | 规划中应存在的子目录 | 实际状态 | 严重程度 |
|------|---------------------|----------|----------|
| 02 业务架构 | `01-business-capability-model` / `02-business-process-reuse` / `03-domain-driven-design` / `04-business-rules` | 缺失 3 个；`01` 重命名为 `02-business-capability` | 🟡 中 |
| 03 应用架构 | `01-layered-architecture` / `02-microservices` / `03-serverless` / `04-event-driven` | 全部缺失；内容合并到其他子目录 | 🟡 中 |
| 04 组件架构 | `01-component-models` / `02-interface-contracts` / `03-dependency-management` | 缺失 3 个 | 🟡 中 |
| 05 功能架构 | `01-api-design` / `02-function-as-a-service` / `03-event-functions` | 缺失 3 个 | 🟡 中 |
| 06 跨层治理 | `02-reuse-process` / `03-policy-automation` | 缺失 2 个 | 🟡 中 |
| 07 形式化验证 | `03-coq-isabelle` / `07-model-checking` | `03` 仅目录无文件；`07` 未在 README 列出 | 🔴 高 |
| 08 认知架构 | `04-decision-making` | 缺失 | 🟡 中 |
| 09 价值量化 | `03-finops-allocation` / `04-risk-adjusted-value` | 缺失（FinOps 内容实际在 06 下） | 🟡 中 |
| 10 供应链安全 | `01-threat-model` / `05-compliance` | 命名不一致 | 🟢 低 |
| 12 AI 原生 | `02-model-reuse` / `04-rag-patterns` | 缺失 2 个 | 🟡 中 |
| 13 新兴趋势 | `03-edge-computing` / `04-quantum-computing` / `05-sustainable-software` | 缺失 3 个；实际新增模块化单体/Rust/RegTech | 🟡 中 |

### 2.3 形式化验证可执行性缺口

| 缺口 | 说明 | 影响 |
|------|------|------|
| TLA+ 未跑 TLC/SANY | 环境无 Java，仅人工语法审查 | 无法保证规约无死锁/不变量成立 |
| Alloy 未跑 Alloy Analyzer | 未自动执行约束求解 | 无法验证模型可满足性 |
| Coq/Isabelle 空白 | 仅有教学示例，无安全关键组件证明 | 缺少定理证明层的高保证案例 |
| Rust 形式化未链接 Kani/Prusti | 文档深入但无实际可跑验证 | 缺少可复现的验证流水线 |

### 2.4 工具/模板/可执行交付物缺口

大量内容仍为 Markdown 理论文档，以下**可执行交付物**尚未完成：

1. **成熟度评估问卷** → 需从 Markdown 转为可交互表单（YAML/JSON + Python CLI）
2. **FinOps 成本分摊模板** → Excel + Python 实现
3. **COCOMO II 2026 计算器** → Python/Streamlit 或 Excel
4. **AI 概率契约校准工具** → Python 原型（Conformal Prediction 实现）
5. **PIU 贝叶斯统计验证工具** → Python（工业安全）
6. **供应链攻击树可视化** → Mermaid/Graphviz 动态渲染
7. **术语查询脚本** → Python CLI 跨标准术语检索
8. **复用决策交互工具** → Web/CLI（MASTER_PLAN Phase 6 目标）

---

## 3. 与国际权威内容的差距分析

### 3.1 标准对齐差距

| 国际标准 | 本项目中覆盖状态 | 差距 | 后续行动 |
|----------|-----------------|------|----------|
| **ISO/IEC 25010:2023** (SQuaRE) | 在 06/01 中提及，Reusability 作为 Maintainability 子特性 | 未深入展开 Reusability 与 Modularity/Analysability/Testability 的相互作用 | 补充 25010:2023 质量特性对复用的影响矩阵 |
| **ISO/IEC 25040:2024** (Evaluation) | 未明确引用 | 缺少"获取或复用预开发产品"的评估流程映射 | 增加 25040 评估流程与复用决策的对照 |
| **ISO/IEC/IEEE 42010:2022** | 已深度映射 | 基本完整，待 DIS 42042 发布后更新 | 跟踪 42042 进展 |
| **ISO/IEC/IEEE DIS 42042** (Reference Architectures) | 仅作为待跟踪项 | 草案接近 2026 定稿，缺少参考架构元模型 | 一旦发布，补充到 01-meta-model-standards |
| **IEEE 1517-2010** (Reuse Processes) | 已映射 | 12207:2026 已覆盖复用过程，IEEE 1517 提供更具体的复用活动定义 | 持续维护 IEEE 1517 与 12207:2026 的对照 |
| **OMG RAS v2.2** | 未引用 | 缺少可复用资产包装标准（Classification/Solution/Usage/Related Assets） | 新增 RAS 对齐章节 |
| **ISO/IEC 26566:2026** | 已引用（成熟度） | 2026-05 刚正式发布，可深化方法/工具能力映射 | 更新 06/03-maturity-models 以反映正式版 |
| **ISO/IEC 33000 系列** (SPICE) | 未系统引用 | 缺少过程能力六级模型与复用成熟度的映射 | 补充 33000 与 RCMM/RiSE 的映射 |
| **FAIR4RS Principles** | 未引用 | 研究软件复用的 Findable/Accessible/Interoperable/Reusable 原则对 AI 功能复用极具相关性 | 新增 FAIR4RS 与 AI 复用、SBOM 的对照 |

### 3.2 技术生态差距

| 技术/框架 | 国际最新状态（2026-06） | 本项目状态 | 差距 |
|-----------|----------------------|-----------|------|
| **MCP** | Anthropic 2025-11-25 为当前稳定版；已捐给 Linux Foundation Agentic AI Foundation；新增 Tasks、Icons、Elicitation URL mode、JSON Schema 2020-12 | 文档提及 2026-07-28 RC（CHANGELOG 已勘误），但 2025-11-25 的 Tasks/Icons 等新特性覆盖不足 | 需全面更新为 2025-11-25 特性解析 |
| **A2A** | Google Cloud Next 2026 发布 v1.0 | 已有深度解析 | 基本完整 |
| **SLSA** | v1.1 已发布，v1.2 引入 Multi-Track（Build/Source/Attested Build Environments）；L4 仍在开发 | 已更新到 1.1/1.2，但 L4 分布式构建验证仍为空白 | 补充 L4 多签名/可复现构建实践 |
| **WASI / Component Model** | WASI 0.3 preview 已发布（Wasmtime 37+），原生 async（stream/future）；WASI 1.0 目标 2026 末/2027 初 | 已有 WASM 决策树，但对 WASI 0.3 async、warg registry（已停止积极开发，社区转向 OCI-based registry）、多线程限制覆盖不足 | 补充 WASI 0.3 与跨语言复用边界 |
| **CNCF Platform Engineering** | Platform Engineering Maturity Model 五维度（Investment/Adoption/Interfaces/Operations/Measurement） | 已有 maturity model，但与 CNCF 五维度的逐条映射可深化 | 补充五维度评估检查清单 |
| **Conformal Prediction** | 在代码生成/验证领域快速兴起（Verina、AlphaVerus、AutoVerus 等） | 已有 `cp-code-generation.md` | 可补充与形式化验证（Lean/Coq）结合的 AI 验证框架 |

### 3.3 学术/会议前沿差距

| 会议/社区 | 2025-2026 主题 | 本项目覆盖 | 建议 |
|-----------|---------------|-----------|------|
| **ICSA 2025/2026** | "Architecting for next-gen intelligent systems" / "Architecting in Continuous Software Engineering" | 提及但未系统对齐 | 增加 ICSA 主题与本框架的映射 |
| **ECSA 2025** | "impactful software architecture" | 未引用 | 补充 ECSA 架构影响力模型 |
| **SAGAI / GreenArch 2026** | Generative AI + Sustainable Architecture | 未覆盖可持续软件架构 | 补充绿色架构复用度量 |
| **AEDT (Digital Twins)** | 数字孪生参考架构 | 工业 IoT 已覆盖 AAS | 补充数字孪生通用参考架构 |

---

## 4. 后续推进计划（2026-Q3 → 2027-Q4）

### Phase 1.5 立即修复（2026-Q3 剩余 2-4 周）

**目标**: 修复本轮（2026-06-06）遗留的一致性问题，为 Phase 2 扫清基础。

| 任务 ID | 任务 | 交付物 | 验收标准 | 优先级 |
|---------|------|--------|----------|--------|
| P1.5-T1 | 更新 01-roadmap：T05-T08 标记为 `[x]` | `01-meta-model-standards/plans-tasks/roadmap.md` | 与 `roadmap-consistency-audit.md` 一致 | P0 |
| P1.5-T2 | 更新 11-roadmap：T13-T17 标记为 `[x]`；确认 AAS-OPC UA 完整映射 | `11-industrial-iot-otit/plans-tasks/roadmap.md` | 已交付文件状态准确 | P0 |
| P1.5-T3 | 更新 07-roadmap：TLA+ 案例库状态；修正跨主题交付物路径 | `07-formal-verification/plans-tasks/roadmap.md` | OPC UA FX / PLCopen 路径指向 11/ 下实际文件 | P0 |
| P1.5-T4 | 重构 `struct/README.md` 文件夹结构导航 | `struct/README.md` | 与实际 `struct/` 目录一致（允许新增/重命名有说明） | P1 |
| P1.5-T5 | 清理 `.vscode/README.md` 中疑似 PostgreSQL 残留内容 | `.vscode/README.md` | 内容与项目主题一致 | P1 |
| P1.5-T6 | ~~建立形式化验证自动化环境（Java + TLA+ Toolbox + Alloy Analyzer）~~ ➡️ 形式化验证规约内容梳理与校对 | `99-reference/tools/formal-verification-env.md`（内容梳理文档） | 完成 TLA+/Alloy/Coq 现有规约的内容校对与一致性检查，不搭建运行环境 | P1 |

### Phase 2 形式化与量化深化（2026-Q4）

**目标**: 将认知架构、价值量化从"理论文档"转化为"可操作方法论 + 可执行工具"；完成形式化验证内容梳理；优先填补03应用架构缺失的基础子目录（分层架构、微服务、Serverless、事件驱动）

| 任务 ID | 任务 | 交付物 | 对齐来源 | 验收标准 |
|---------|------|--------|----------|----------|
| P2-T1 | Coq/Isabelle 高安全等级组件内容梳理（定理证明纲要整理，不搭建运行环境） | `07-formal-verification/03-coq-isabelle/README.md` + `.v`/`.thy` 案例整理 | Coq (Inria)、Isabelle/HOL (TU Munich)、seL4/CompCert | 2+ 案例证明纲要文档化，含概念说明和引用来源 |
| P2-T2 | Alloy 跨层映射 + ISA-95 层次约束内容梳理（模型文档化，不执行约束求解） | `07-formal-verification/02-alloy/cross-layer-mapping.md` 扩展 | Alloy Tools (MIT)、ISO/IEC 42010 | 新增 ISA-95 五层约束文档，含模型说明和逻辑推演 |
| P2-T3 | Rust 形式化验证工具链内容梳理（Kani/Prusti/Miri 概念说明与引用整理） | `07-formal-verification/04-rust-type-system/toolchain-practice.md` | RustBelt (MPI-SWS)、Kani (AWS)、Prusti (ETH) | 工具链概念文档化，含对比分析和权威来源引用 |
| P2-T4 | COCOMO II 2026 可执行计算器 | `09-value-quantification/tools/cocomo-calculator.py` + Excel | USC COCOMO II Manual (Boehm) | 支持 AAM/SU/UNFM 参数输入和 ROI 输出 |
| P2-T5 | FinOps 跨层成本分摊 Python/Excel 模板 | `06-cross-layer-governance/04-finops-cost/templates/` + `99-reference/tools/finops-template/` | FinOps Foundation | 含四级分摊公式和示例数据 |
| P2-T6 | 复用成熟度可执行评估问卷 | `06-cross-layer-governance/03-maturity-models/assessment-tool/` (YAML + Python CLI) | ISO/IEC 26566:2026、NASA RRL | 生成雷达图 + 成熟度报告 |
| P2-T7 | AI 功能概率契约校准工具原型 | `12-ai-native-reuse/05-probabilistic-contracts/calibration-tool.py` | Conformal Prediction (Vovk et al.)、OWASP LLM/MCP Top 10 | 支持温度/Top-p/模型版本漂移的边界计算 |
| P2-T8 | AI 辅助复用决策系统原型设计 | `08-cognitive-architecture/05-ai-cognitive-augmentation/prototype-design.md` | ACT-R (CMU)、NASA-TLX | 含 RAG+LLM 流程图和 PoC 架构 |
| P2-T9 | 术语查询脚本 | `99-reference/tools/terminology-query.py` | IREB CPRE Glossary、ISO/IEC 42010 | 支持跨标准术语搜索和别名映射 |
| P2-T10 | OMG RAS v2.2 对齐章节 | `01-meta-model-standards/07-omg-ras/ras-alignment.md` | OMG RAS v2.2 | 覆盖 Classification/Solution/Usage/Related Assets |
| P2-T11 | 03应用架构基础子目录内容填充（分层/微服务/Serverless/事件驱动） | `03/01-layered-architecture/`, `03/02-microservices/`, `03/04-serverless/`, `03/06-event-driven/` | SWEBOK v4, CNCF | 每个子目录至少1篇核心文档 |
| P2-T12 | ISO/IEC 25010:2023 AI/ML质量特性对复用决策的影响矩阵 | `01-meta-model-standards/01-iso-420xx-family/iso-25010-2023-ai-quality.md` | ISO/IEC 25010:2023 | 覆盖AI生成代码/组件的复用质量评估 |

### Phase 3 垂直领域扩展（2027-Q1）

**目标**: 深化工业 IoT/OT-IT 融合，补齐功能安全、边缘 AI、PIU 工具。

| 任务 ID | 任务 | 交付物 | 对齐来源 | 验收标准 |
|---------|------|--------|----------|----------|
| P3-T1 | IEC 61508 Proven-in-Use (PIU) 贝叶斯统计验证工具 | `11-industrial-iot-otit/06-functional-safety/piu-bayesian-tool.py` | IEC 61508-3-1:2016 | 支持失效数据输入 → SIL 可信度输出 |
| P3-T2 | ISO 26262 SEooC 复用流程模板 | `11-industrial-iot-otit/06-functional-safety/iso26262-seooc-template.md` | ISO 26262-8 Clause 12 | 含安全手册、假设、验证清单 |
| P3-T3 | 工业边缘 AI 模型部署规范 | `11-industrial-iot-otit/07-edge-ai/model-deployment-spec.md` + ONNX Runtime 示例 | TinyML、ONNX、IEC 62443 | 覆盖 TFLite/ONNX 部署流程 |
| P3-T4 | MCP for Industrial AI 协议草案 | `11-industrial-iot-otit/07-edge-ai/mcp-industrial-ai-draft.md` | MCP 2025-11-25、OPC UA FX | 定义工业场景 Tools/Resources 规范 |
| P3-T5 | AAS 到 OPC UA NodeSet 完整映射规范（确认/补全） | `11-industrial-iot-otit/05-digital-twin-aas/aas-opcua-nodeset-mapping.md` | IDTA AAS、OPC Foundation | XML/JSON 示例 + 映射表 |
| P3-T6 | FAIR4RS 原则与软件复用对照 | `01-meta-model-standards/08-fair4rs/fair4rs-alignment.md` | FAIR4RS (2022; ARDC) | 与 SBOM、MCP Tool 注册表的映射 |

### Phase 4 安全与供应链纵深（2027-Q2）

**目标**: 构建 SLSA L4、SBOM 深度应用、攻击树可视化的纵深防御体系。

| 任务 ID | 任务 | 交付物 | 对齐来源 | 验收标准 |
|---------|------|--------|----------|----------|
| P4-T1 | SLSA 1.2 Multi-Track 深度解析（Build/Source/Environment） | `10-supply-chain-security/01-slsa-framework/slsa-1-2-multi-track.md` | SLSA.dev (OpenSSF) | 三轨道 × L1-L3 要求矩阵 |
| P4-T2 | SLSA L4 分布式构建验证实践 | `10-supply-chain-security/01-slsa-framework/slsa-l4-distributed-builds.md` + sigstore/cosign 示例 | OpenSSF、Sigstore | 多签名 + 可复现构建 POC |
| P4-T3 | 供应链攻击树交互式可视化 | `10-supply-chain-security/03-attack-vectors/attack-tree-interactive.html` / `.py` | MITRE ATT&CK、OWASP SCVS | 支持点击展开/防御矩阵联动 |
| P4-T4 | NIST SSDF 1.2 Initial Public Draft 对齐 | `10-supply-chain-security/06-case-studies/nist-ssdf-1-2-alignment.md` 更新 | NIST SP 800-218r1 IPD | 同步征求意见稿；跟踪正式版变更 |
| P4-T5 | EU CRA 合规检查清单工具 | `10-supply-chain-security/06-case-studies/eu-cra-checklist.json` + CLI | Regulation (EU) 2024/2847 | 自动评估合规项 |
| P4-T6 | IEEE 1517 复用过程映射 | `01-meta-model-standards/01-iso-420xx-family/ieee-1517-reuse-processes.md` | IEEE 1517-2010 | 与 ISO 12207:2017 的对照 |

### Phase 5 AI 原生与前沿（2027-Q3）

**目标**: 将 AI/LLM 功能复用、Agentic Infrastructure、WASM、平台工程提升到工程化水平。

| 任务 ID | 任务 | 交付物 | 对齐来源 | 验收标准 |
|---------|------|--------|----------|----------|----------|
| P5-T1 | MCP 2025-11-25 全面更新（替换 2026-07-28 RC 旧引用） | `12-ai-native-reuse/01-mcp-protocol/mcp-2025-11-25-deep-dive.md` | modelcontextprotocol.io/specification/2025-11-25 | 覆盖 Tasks、Icons、Elicitation、OAuth 增量 |
| P5-T2 | Agentic Governance 组织设计模板 | `12-ai-native-reuse/03-agentic-infrastructure/agentic-governance-template.md` | Google A2A、Linux Foundation Agentic AI Foundation | 含 Agent RBAC、Golden Path、模型路由 |
| P5-T3 | CP + 形式化验证融合框架（研究探索方向，尚无成熟学术基础） | `12-ai-native-reuse/07-conformal-prediction/cp-formal-verification.md` | Conformal Prediction (Vovk et al.)、Cherian & Candès (NeurIPS 2024, LLM validity via enhanced CP)、Angelopoulos & Bates (CP 现代教程) | 提出探索性框架，明确标注为研究空白 | P2 |
| P5-T4 | WASM Component Model + WASI 0.3 复用边界更新（WASM Component Model 当前处于 W3C Phase 1（Feature Proposal），WASI 1.0 预计 2026年底/2027年初发布；使用 wasm-pkg-tools 替代 Warg registry） | `13-emerging-trends/03-webassembly-components/wasm-wasi-03-boundaries.md` | Bytecode Alliance、Wasmtime 37+ | 覆盖 stream/future、async、线程限制，标注标准化阶段 |
| P5-T5 | Backstage / Port / Cortex IDP 复用实践 | `03-application-architecture-reuse/11-idp-practices/backstage-port-cortex.md` | CNCF Platform Engineering Maturity Model | 三家平台对比 + Golden Path 模板 |
| P5-T6 | RegTech Agentic 架构案例验证 | `13-emerging-trends/06-regtech-ai/regtech-case-validation.md` | Financial regulators (FCA/SEC/EU) | 1+ 真实监管场景 POC 设计 |
| P5-T7 | 可持续软件架构（GreenArch）初探 | `13-emerging-trends/07-green-software/green-architecture-reuse.md` | GreenArch 2026、Green Software Foundation | 碳感知架构复用度量 |

### Phase 6 整合与输出（2027-Q4）

**目标**: 将分散知识模块整合为可交付产品。

| 任务 ID | 任务 | 交付物 | 验收标准 |
|---------|------|--------|----------|
| P6-T1 | 《软件工程架构复用视角》全书框架定稿 | `99-reference/book-outline.md` 更新 | 12 章 + 附录，每章对应一级主题 |
| P6-T2 | 国际标准对齐总矩阵 v2.0 | `99-reference/standards-index/master-alignment-matrix.md` 更新 | 覆盖 30+ 标准 × 5 复用层次 |
| P6-T3 | 公理-定理推理树完整版 | `99-reference/glossary/axiom-theorem-tree.md` 更新 | 20+ 公理、35+ 定理 |
| P6-T4 | 交互式复用决策工具（Web/CLI） | `99-reference/tools/reuse-decision-tool/` | 支持 6 阶段决策流程 |
| P6-T5 | Mermaid 可视化库补全 | `99-reference/visualizations/` | 覆盖 13 个主题 |
| P6-T6 | 项目官网/GitBook 发布准备 | `99-reference/website/` | 在线可浏览知识体系 |
| P6-T7 | 国际会议投稿/白皮书（ICSA/ECSA/绿会） | `99-reference/publications/` | 至少 1 份白皮书 |

### Phase D 前沿跟踪持续更新（2026-Q2 起，持续）

**目标**: 建立标准演进与会议前沿的持续跟踪机制，嵌入月度事实核查流程

| 任务 ID | 任务 | 交付物 | 跟踪对象 | 优先级 |
|---------|------|--------|----------|--------|
| D-01 | AWI 42030 正式版对齐 | `01/01-iso-420xx-family/iso-42030-202x-update.md` | ISO/IEC/IEEE 42030 修订版 | P1 |
| D-02 | MCP 后续版本更新 | `12/01-mcp-protocol/mcp-next-version-tracking.md` | Linux Foundation Agentic AI Foundation | P2 |
| D-03 | WASI 1.0 正式发布对齐 | `13/03-webassembly-components/wasi-1-0-alignment.md` | W3C / Bytecode Alliance | P2 |
| D-04 | ICSA/ECSA/SPLC 会议主题年度映射 | `99-reference/external-links/conference-theme-index.md` | IEEE/ACM 会议 | P3 |
| D-05 | 月度事实核查中加入前沿跟踪项 | `99-reference/templates/fact-check-checklist.md` 更新 | 标准 RSS / 会议议程 / 协议发布 | P1 |

### Phase E 全书整合与排版（预计 2026-Q3）

**目标**: 将 struct/ 知识体系整合为可交付的书稿与在线产品

| 任务 ID | 任务 | 交付物 | 验收标准 |
|---------|------|--------|----------|
| E-01 | 书稿内容整合与交叉引用校对 | `99-reference/book-outline-v2.md` 定稿 | 12 章 + 附录，无死链、无冲突引用 |
| E-02 | Markdown → 排版格式转换（PDF/EPUB） | `99-reference/output/book/` | 支持中文排版规范（book-format-guide.md） |
| E-03 | 在线浏览版本（GitBook/Docusaurus）发布 | `99-reference/website/` | 13 主题可导航，搜索可用 |
| E-04 | 目录编号不一致清理 | `struct/README.md` + 各子目录索引统一 | 全部目录编号与文件命名一致 |
| E-05 | 国际标准对齐总矩阵 v3.0 | `99-reference/standards-index/master-alignment-matrix.md` | 覆盖 42+ 标准 × 5 复用层次 |

### Phase F 社区反馈与迭代（预计 2026-Q4）

**目标**: 收集早期读者与社区反馈，启动知识产品迭代

| 任务 ID | 任务 | 交付物 | 验收标准 |
|---------|------|--------|----------|
| F-01 | 建立读者反馈渠道（GitHub Discussions / 邮件列表） | `99-reference/feedback/` | 至少 1 个活跃渠道 |
| F-02 | 收集并分类前 100 条反馈 | `99-reference/feedback/feedback-taxonomy.md` | 按主题/优先级分类 |
| F-03 | 发布 v2.1 修正版（基于反馈） | `CHANGELOG.md` 更新 | 关闭 P0/P1 反馈 ≥ 80% |
| F-04 | 规划 2027 年知识产品路线图 | `99-reference/roadmap-2027.md` | 明确 Q1-Q4 重点 |

---

## 5. 风险与依赖

| 风险 ID | 风险描述 | 影响 | 缓解措施 |
|---------|----------|------|----------|
| R1 | MCP/SLSA/42042 等标准在计划期内发布新版本 | 已写内容需返工 | 建立标准 RSS 监控；在文档中标注版本和勘误 |
| R2 | TLA+/Alloy/Coq 可执行验证管道 | 已延期至 2027-Q1 后 | 保持文档级正确性优先；视资源决定是否搭建运行环境 |
| R3 | 工业 IoT 领域标准（OPC UA FX 1.0、IEC 63278）获取成本高 | 内容权威性受限 | 优先使用公开规范摘要、厂商白皮书、IDTA 模板 |
| R4 | 可执行工具开发工作量大 | Phase 2/3 范围膨胀 | 用 Python CLI + Streamlit 快速原型，避免重前端 |
| R5 | 目录规划与实际结构长期不一致 | 维护成本增加 | Phase 1.5 彻底重构 README；后续严格执行变更日志 |
| R6 | AI 领域发展迅速，MCP/A2A 内容易过期 | 前沿章节准确性下降 | 按季度审查 12-ai-native-reuse；建立外部链接健康检查 |

### 持续机制补充

**月度事实核查**：按调整建议3，每月第5周执行事实核查，抽查5-10个外部引用的事实准确性，使用 `99-reference/templates/fact-check-checklist.md`。同时加入前沿跟踪项，包括标准版本更新（ISO/OMG/IEEE）、协议演进（MCP/A2A/WASI）、会议主题（ICSA/ECSA/SPLC）。

### 待解决项（延期处理）

| 任务 ID | 描述 | 延期原因 | 预计处理时间 |
|---------|------|----------|--------------|
| TBD-01 | 目录编号不一致清理 | 涉及大量交叉引用，需全书整合时统一处理 | Phase E（2026-Q3） |
| TBD-02 | TLA+/Alloy/Coq 可执行验证管道 | 按决策 2 已调整为内容梳理优先，运行环境搭建延期 | 2027-Q1 后视资源情况 |
| TBD-03 | 复用决策工具 v2.0 的 CI/CD 集成 | 当前为本地运行版本，需补充自动化测试与发布流水线 | Phase E/F（2026-Q3-Q4） |

---

## 6. 需要确认的关键决策

在启动 Phase 2 之前，请您确认以下决策：

### 决策 1：目录结构统一策略
>
> **选项 A（推荐）**: 重构 `struct/README.md` 和 `MASTER_PLAN.md` 中的目录树，使其 100% 匹配实际 `struct/` 目录，删除/合并规划中未实现的子目录。
> **选项 B**: 保留现有规划树，为缺失子目录创建占位符（README + TODO），后续按规划补齐。
> **选项 C**: 不调整顶层规划，仅在 README 中增加"实际目录与规划存在差异"的免责声明。

### 决策 2：形式化验证工具链投入（已调整）
>
> ~~选项 A（推荐）: 建立 Docker 化的 TLA+ Toolbox + Alloy Analyzer + Coq 环境~~ ➡️ **已按用户要求调整为内容梳理优先**：
> **选项 A'（当前执行）**: 不搭建形式化验证运行环境，重点做好 TLA+/Alloy/Coq/Isabelle 现有规约的**内容梳理、校对、权威来源对齐和概念文档化**。保持"文档级正确性"而非"机器验证级正确性"。
> ~~选项 B~~ / ~~选项 C~~ — 均不适用，已按 A' 执行。

### 决策 3：可执行工具开发策略
>
> **选项 A（推荐）**: 优先用 Python CLI + Streamlit 开发所有工具原型（COCOMO 计算器、FinOps 模板、成熟度问卷、PIU 工具），保持最低可用。
> **选项 B**: 投资一个统一的 Web 平台（如 Docusaurus + React）承载所有交互式工具。
> **选项 C**: 仅提供 Excel + Markdown 模板，不开发代码原型。

### 决策 4：前沿主题取舍
>
> **选项 A（推荐）**: 2027 年重点补齐 **Conformal Prediction + 形式化验证融合**、**WASI 0.3**、**Agentic Governance**；暂缓量子计算和边缘计算通用架构。
> **选项 B**: 按 MASTER_PLAN 原规划，恢复 `quantum-computing` 和 `sustainable-software` 子目录。
> **选项 C**: 仅维护现有 13 个主题，不扩展新前沿方向。

### 决策 5：国际对齐深度
>
> **选项 A（推荐）**: 每个新增/更新文档必须明确列出 1-3 个国际权威来源 URL，并在 `99-reference/external-links/authoritative-sources.md` 中登记。
> **选项 B**: 保持当前风格，在 README 中统一列出权威来源，不要求每文档标注。
> **选项 C**: 仅在关键标准文档中标注来源，日常内容不强制。

---

## 2026-06-08 HOTFIX 完成记录

| HOTFIX ID | 描述 | 状态 |
|-----------|------|------|
| HOTFIX-1 | ArchiMate | ✅ 已完成（2026-06-08） |
| HOTFIX-2 | MCP | ✅ 已完成（2026-06-08） |
| HOTFIX-3 | Kleppmann | ✅ 已完成（2026-06-08） |
| HOTFIX-4 | ISO 25010 | ✅ 已完成（2026-06-08） |
| HOTFIX-5 | Coq/Isabelle | ✅ 已完成（2026-06-08） |
| HOTFIX-6 | Warg | ✅ 已完成（2026-06-08） |

---

> **下一步**: Phase D 前沿跟踪已启动；Phase E（全书整合）待 2026-Q3 启动；Phase F（社区反馈）待 2026-Q4 启动。

---

*最后更新: 2026-06-10*
