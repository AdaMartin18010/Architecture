# 软件工程架构复用视角：MASTER PLAN（总体推进计划）

> **版本**: 2026-07-07
> **周期**: 2026 Q2 → 2027 Q4（6 个季度）
> **目标**: 将 view/ 中 ~31 万字源文档转化为结构化、可验证、可输出的知识产品
> **项目统计**: `struct/` 330 + `view/` 23 = 353 Markdown 文档 · 严格公理 10/启发式 5/定理 17 · ~109.2 万词 · 25+ 国际标准（真源 `reports/stats.json`）
> **历史计划**: [`_HISTORICAL_MASTER_PLAN_2026_NETWORK_ALIGNED.md`](./_ARCHIVE/_HISTORICAL_MASTER_PLAN_2026_NETWORK_ALIGNED.md)、[`_HISTORICAL_SUBSEQUENT_PLAN_2026.md`](./_ARCHIVE/_HISTORICAL_SUBSEQUENT_PLAN_2026.md)、[`_HISTORICAL_SUBSEQUENT_PLAN_2026_NETWORK_ALIGNED_v2.md`](./_ARCHIVE/_HISTORICAL_SUBSEQUENT_PLAN_2026_NETWORK_ALIGNED_v2.md)

---

## 关键决策确认（2026-06-06）

按用户确认执行以下策略：

- **1A**: 重构 README/MASTER_PLAN 与实际 `struct/` 目录 100% 匹配
- **2A**: ~~Docker 化 TLA+/Alloy/Coq 环境，新增规约必须自动验证~~ ➡️ **已调整**：不搭建形式化验证运行环境，重点做好现有规约的内容梳理、校对、权威来源对齐和概念文档化（文档级正确性优先）
- **3A**: 可执行工具采用 Python CLI + Streamlit 快速原型
- **4A**: 重点补齐 Conformal Prediction+形式化、WASI 0.3、Agentic Governance；暂缓量子计算
- **5A**: 每篇新增/更新文档必须列出 1-3 个国际权威来源 URL

---

## 目录

- [软件工程架构复用视角：MASTER PLAN（总体推进计划）](#软件工程架构复用视角master-plan总体推进计划)
  - [关键决策确认（2026-06-06）](#关键决策确认2026-06-06)
  - [目录](#目录)
  - [Phase A：止血与基础修复（2026-07，进行中）](#phase-a止血与基础修复2026-07进行中)
  - [Phase 0：基础奠基（2026-Q2，已完成）](#phase-0基础奠基2026-q2已完成)
  - [Phase 1：核心层次深化（2026-Q3）](#phase-1核心层次深化2026-q3)
  - [Phase 2：形式化与量化（2026-Q4）](#phase-2形式化与量化2026-q4)
  - [Phase 3：垂直领域扩展（2027-Q1）— ✅ 已完成（提前至 2026-06）](#phase-3垂直领域扩展2027-q1--已完成提前至-2026-06)
  - [Phase 4：安全与供应链（2027-Q2）— ✅ 已完成（提前至 2026-06）](#phase-4安全与供应链2027-q2--已完成提前至-2026-06)
  - [Phase 5：AI 原生与前沿（2027-Q3）— ✅ 内容已覆盖，按决策 D3 暂停扩展](#phase-5ai-原生与前沿2027-q3--内容已覆盖按决策-d3-暂停扩展)
  - [Phase C：扩展对齐与纵深（2026-06-10）— ✅ 已完成（方案 C：最大化推进）](#phase-c扩展对齐与纵深2026-06-10--已完成方案-c最大化推进)
  - [Phase 6：整合与输出（2027-Q4）— 🔄 进行中](#phase-6整合与输出2027-q4--进行中)
  - [持续机制](#持续机制)
    - [月度节奏](#月度节奏)
    - [季度节奏](#季度节奏)
    - [年度节奏](#年度节奏)
  - [任务优先级矩阵](#任务优先级矩阵)
  - [概念定义](#概念定义)
  - [正向示例](#正向示例)
  - [反例/反模式](#反例反模式)
  - [权威来源](#权威来源)

---

## Phase A：止血与基础修复（2026-07，进行中）

**目标**: 恢复统计真实性、停止批量模板污染、建立单一真源与清晰导航，为后续内容深度补齐奠定基础。

| 任务 | 状态 | 交付物 |
|------|------|--------|
| 校准 README/struct/README 统计口径 | ✅ 完成 | 更新后的 README.md / struct/README.md |
| 冻结 `batch-fix-quality-gate.py` 自动追加行为 | ✅ 完成 | 默认仅报告，需 `--apply` 才修改 |
| 清理已注入的"补充说明"模板污染 | ✅ 完成 | 220 个文件清理报告 |
| 合并/归档 4 个 Plan 文件 | 🔄 进行中 | MASTER_PLAN.md + 3 个历史归档 |
| 修复目录编号跳空 | ⏳ 待执行 | 目录结构调整说明 |
| 为 `view/` 添加历史快照声明 | ⏳ 待执行 | view/README.md |

**关键决策更新（2026-07-07）**:

- **A1**: 统计口径以实际文件数为准：`struct/` 330 + `view/` 23 = 353 Markdown，~109.2 万词（1,091,745）；严格公理 10 / 启发式 5 / 定理 17（机器真源：`reports/stats.json`）。
- **A2**: 停止批量模板注入；默认报告模式，人工复核后决定是否应用修复。
- **A3**: `view/` 定位为 2026-06 历史快照，`struct/` 为当前真源，长期通过同步脚本维护。

---

## Phase 0：基础奠基（2026-Q2，已完成）

| 任务 | 状态 | 交付物 |
|------|------|--------|
| 阅读 view/ 全部 8 份文档 | ✅ 完成 | 内容摘要 |
| 提取主题-子主题树 | ✅ 完成 | 13 个一级主题 × ~80 个二级主题 |
| 搜索网络权威内容对齐 | ✅ 完成 | 标准、论文、课程参考 |
| 创建 struct/ 文件夹结构 | ✅ 完成 | 本目录结构 |
| 编写 MASTER_PLAN | ✅ 完成 | 本文档 |

---

## Phase 1：核心层次深化（2026-Q3）

**目标**: 将业务→应用→组件→功能四层核心架构，从"提纲"深化为"可执行框架"

**当前进度（2026-06-06）**: Phase 1 已全面启动，7 条轨道并行推进。元模型、业务架构、应用架构、组件架构、功能架构、工业 IoT、形式化验证 Rust 深化等核心任务已完成或接近完成。详见各主题 `README.md` 和 `CHANGELOG.md`。

| 优先级 | 主题 | 核心任务 | 交付物 | 验收标准 | 状态 |
|--------|------|----------|--------|----------|------|
| P0 | 01 元模型与标准对齐 | 完成 ISO 420xx 族谱与 TOGAF 10 的对照表；更新 ArchiMate 3.2/4.0 状态（ArchiMate 4.0 已于 2026-04-27 正式发布，与 3.2 向后兼容） | `01/01-iso-420xx-family/alignment-matrix.md` | 覆盖 10+ 标准的概念映射 | ✅ 完成 |
| P0 | 02 业务架构复用 | 完成 FEA BRM 与 TOGAF Capability Map 的交叉映射；补充 BPMN 2.0 / DMN 1.5 复用元素详解 | `02/02-business-capability/capability-map-template.md` | 含 5 级层次结构 + 决策矩阵 | ✅ 完成 |
| P0 | 03 应用架构复用 | 完成云原生架构模式（单体→微服务→Serverless→模块化单体）的复用性矩阵 2026 版 | `03/07-cloud-native-patterns/reusability-matrix-2026.md` | 含 8+ 架构模式对比 | ✅ 完成 |
| P0 | 04 组件架构复用 | 完成 6 大语言生态（JVM/Node.js/Rust/Go/Python/.NET）的复用成熟度深度对比 | `04/07-language-ecosystems/comparison-matrix-2026.md` | 含包管理、组件模型、变性机制 | ✅ 完成 |
| P1 | 05 功能架构复用 | 完成 MCP 2025-11-25 + A2A v1.0 协议架构的复用分析 | `05/06-mcp-a2a-protocols/protocol-analysis.md` | 含协议栈层次 + 互补架构图 | ✅ 完成 |
| P1 | 06 跨层复用治理 | 完成复用度量指标体系（基于 ISO/IEC 26564:2022 + NASA RRL） | `06/05-metrics-kpi/metrics-framework.md` | 含资产级/项目级/组织级/生态级四级度量 | ✅ 完成 |

**对齐活动**:

- 对照 [IREB CPRE Glossary](https://isqi.org) 更新术语定义
- 对照 [ISO/IEC/IEEE 42010:2022 官方标准](https://www.iso.org/obp/ui) 验证概念映射

---

## Phase 2：形式化与量化（2026-Q4）

**目标**: 将形式化验证、认知架构、价值量化三个"深度方向"从理论深化为可操作方法论

| 优先级 | 主题 | 核心任务 | 交付物 | 验收标准 | 状态 |
|--------|------|----------|--------|----------|------|
| P0 | 07 形式化验证 | 完成 TLA+ / Alloy / Coq 三种方法的复用组件验证案例库（各 2+ 案例） | `07/01-tla-plus/case-library.md` | 含可运行规约 + 验证流程图 | ✅ 已完成（TLA+ ×6, Alloy ×4, Coq/Isabelle 教学示例已交付） |
| P0 | 07 形式化验证 | 完成 Rust 类型系统（所有权、Trait、Cargo 解析）的形式化语义梳理 | `07/04-rust-type-system/formal-semantics.md` | 含定理证明纲要 | ✅ 提前完成（2026-06） |
| P0 | 09 价值量化 | 完成 COCOMO II 复用模型的 2026 校准版（适配 AI 辅助开发、Serverless） | `09/01-cocomo-ii-reuse/cocomo-2026-calibration.md` | 含参数调整建议 | ✅ 提前完成（2026-06） |
| P0 | 09 价值量化 | 完成跨层 FinOps 成本分摊模型的可执行模板 | `06/04-finops-cost/cost-allocation-template.md` | 含公式 + 计算示例 | ✅ 提前完成（2026-06） |
| P1 | 08 认知架构 | 完成开发者复用决策的认知负荷量化模型（NASA-TLX 适配版） | `08/03-cognitive-load-theory/quantitative-model.md` | 含测量方法对照表 | ✅ 提前完成（2026-06） |
| P1 | 08 认知架构 | 完成 AI 辅助复用决策的认知增强架构设计 | `08/05-ai-cognitive-augmentation/augmentation-architecture.md` | 含 RAG 增强流程 | ✅ 提前完成（2026-06） |

**对齐活动**:

- 对照 USC COCOMO II 官方手册验证公式
- 对照 Leslie Lamport (TLA+)、Daniel Jackson (Alloy) 的教材验证规约语法
- 对照 ACT-R / BDI 认知科学文献验证模型映射

---

## Phase 3：垂直领域扩展（2027-Q1）— ✅ 已完成（提前至 2026-06）

**目标**: 将通用框架扩展到工业 IoT/OT-IT 融合领域

| 优先级 | 主题 | 核心任务 | 交付物 | 验收标准 | 状态 |
|--------|------|----------|--------|----------|------|
| P0 | 11 工业 IoT/OT-IT | 完成 ISA-95 五层模型（L0-L4）的复用资产目录 | `11/01-isa-95-model/asset-catalog.md` | 每层 5+ 复用单元 | ✅ 已完成 |
| P0 | 11 工业 IoT/OT-IT | 完成 OPC UA FX 协议栈的复用层次分析（C2C/C2D/D2D） | `11/02-opc-ua-fx/reuse-hierarchy.md` | 含帧结构 + 厂商支持矩阵 | ✅ 已完成 |
| P0 | 11 工业 IoT/OT-IT | 完成 PLCopen 运动控制功能块的状态机形式化验证（TLA+） | `11/04-plcopen-motion/tla-verification.md` | 含 MC_Power / MC_MoveAbsolute 规约 | ✅ 已完成 |
| P1 | 11 工业 IoT/OT-IT | 完成数字孪生 AAS（IEC 63278）与 OPC UA 的映射规范 | `11/05-digital-twin-aas/aas-opcua-mapping.md` | 含 XML/JSON 示例 | ✅ 已完成 |
| P1 | 11 工业 IoT/OT-IT | 完成功能安全（IEC 61508 / ISO 26262）复用决策树工具 | `11/06-functional-safety/reuse-decision-tool.md` | 含 SIL 等级判定逻辑 | ✅ 已完成 |

**对齐活动**:

- 对照 OPC Foundation 2026 规范更新 FX 状态
- 对照 IDTA (Industrial Digital Twin Association) AAS 子模型模板
- 对照 Siemens / Beckhoff / Rockwell 官方文档验证厂商支持矩阵

---

## Phase 4：安全与供应链（2027-Q2）— ✅ 已完成（提前至 2026-06）

**目标**: 构建软件供应链安全的纵深防御体系

| 优先级 | 主题 | 核心任务 | 交付物 | 验收标准 | 状态 |
|--------|------|----------|--------|----------|------|
| P0 | 10 供应链安全 | 完成 SLSA 1.1/1.2 Multi-Track 框架的复用安全边界详解 | `10/01-slsa-framework/slsa-reuse-boundaries.md` | 含 L1-L4 的复用决策矩阵 | ✅ 已完成 |
| P0 | 10 供应链安全 | 完成 SPDX vs CycloneDX vs SWID 的复用安全应用对比 | `10/02-sbom-standards/sbom-reuse-security.md` | 含 3 标准 × 4 应用场景矩阵 | ✅ 已完成 |
| P0 | 10 供应链安全 | 完成 XZ Utils 后门等 5+ 案例的深度分析 + 防御策略 | `10/06-case-studies/xz-utils-deep-dive.md` | 含攻击链 + 检测信号 | ✅ 已完成 |
| P1 | 10 供应链安全 | 完成零信任软件供应链架构设计模板 | `10/05-zero-trust-supply-chain/zero-trust-template.md` | 含 5 层防御矩阵 | ✅ 已完成 |
| P1 | 07 形式化验证 | 完成 Rust Polonius 借用检查器的形式化语义与 NLL 对比 | `07/04-rust-type-system/polonius-vs-nll.md` | 含代码示例 + 分析过程 | ✅ 已完成 |

**对齐活动**:

- 对照 OpenSSF SLSA 官方规范
- 对照 NIST SP 800-204D / SSDF
- 参与 OpenSSF 社区漏洞披露流程

---

## Phase 5：AI 原生与前沿（2027-Q3）— ✅ 内容已覆盖，按决策 D3 暂停扩展

**目标**: 将 AI/LLM 功能复用从"实验"提升为"工程"

| 优先级 | 主题 | 核心任务 | 交付物 | 验收标准 | 状态 |
|--------|------|----------|--------|----------|------|
| P0 | 12 AI 原生复用 | 完成 MCP 2025-11-25 规范的中文/英文双语深度解析 | `12/01-mcp-protocol/mcp-2025-11-25-deep-dive.md` | 含核心变更对照表（Tasks/Icons/Elicitation/OAuth） | ✅ 已完成 |
| P0 | 12 AI 原生复用 | 完成 A2A v1.0.0 协议的复用流程分析 + 安全机制 | `12/02-a2a-protocol/a2a-reuse-analysis.md` | 含 5 步流程 + Agent Card 模板 | ✅ 已完成 |
| P0 | 12 AI 原生复用 | 完成 AI 功能复用的概率契约框架（含校准方法） | `12/05-probabilistic-contracts/probabilistic-contract-framework.md` | 含 Python 示例代码 | ✅ 已完成 |
| P1 | 12 AI 原生复用 | 完成 Conformal Prediction 在代码生成中的应用案例 | `12/07-conformal-prediction/cp-code-generation.md` | 含统计保证证明 | ✅ 已完成 |
| P1 | 13 新兴趋势 | 完成平台工程（Platform Engineering）作为复用载体的组织设计 | `13/01-platform-engineering/platform-as-product.md` | 含 IDP + Golden Path 模板 | ✅ 已完成 |
| P1 | 13 新兴趋势 | 完成 WebAssembly Component Model 的跨语言复用边界分析 | `13/03-webassembly-components/wasm-reuse-boundaries.md` | 含 WIT 接口示例 | ✅ 已完成 |

**对齐活动**:

- 对照 Anthropic / Linux Foundation Agentic AI Foundation MCP（Model Context Protocol） 官方规范 (2025-11-25)
- 对照 Google A2A（Agent-to-Agent Protocol） / Linux Foundation 官方文档
- 对照 NVIDIA Omniverse / Microsoft Azure Digital Twins 工业数字孪生实践

---

## Phase C：扩展对齐与纵深（2026-06-10）— ✅ 已完成（方案 C：最大化推进）

**目标**: 在 Phase 1-5 基础上，引入 MBSE、数字孪生通用架构、国防/电信垂直行业、供应链验证与工具链 v2.0 等扩展内容

| 任务 ID | 主题 | 核心任务 | 交付物 | 验收标准 | 状态 |
|---------|------|----------|--------|----------|------|
| C-01 | 元模型标准层 | 完成 OMG SysML v2 复用语义与架构资产映射 | 01/09-sysml-v2/sysml2-reuse-mapping.md | 覆盖 ItemDefinition/PartDefinition/ActionDefinition/ConnectionDefinition 复用语义 | ✅ 已完成（2026-06-10） |
| C-02 | 元模型标准层 | 完成 MBSE 模型复用与产品线工程整合框架 | 01/10-mbse-reuse/mbse-ple-integration.md | 含 4 层复用层次 + 150% 模型与变体推导 | ✅ 已完成（2026-06-10） |
| C-03 | 工业 IoT/OT-IT | 完成数字孪生通用参考架构（非工业 AAS） | 11/08-digital-twin-general/dt-reference-architecture.md | 含 ISO 23247 / AEDT / Gartner 五维模型 + 与 AAS 互补分析 | ✅ 已完成（2026-06-10） |
| C-04 | 供应链安全 | 完成 OWASP SCVS 软件组件验证标准映射 | 10/07-owasp-scvs/scvs-reuse-controls.md | 含 6 大控制族 × 3 成熟度等级与复用决策映射 | ✅ 已完成（2026-06-10） |
| C-05 | 供应链安全 | 完成 GUAC 供应链图谱与复用风险评估 | 10/08-guac-supply-chain/guac-reuse-risk.md | 含知识图谱数据模型 + 传递风险分析 + 关键路径识别 | ✅ 已完成（2026-06-10） |
| C-06 | 业务架构复用 | 完成 TMForum ODF / eTOM 电信架构复用案例 | 02/case-studies/tmforum-telecom-reuse.md | 含 eTOM L1-L3 + SID + ODA + CAMARA 复用机制 | ✅ 已完成（2026-06-10） |
| C-07 | 业务架构复用 | 完成 NAF 4.0 / MODAF 与北约架构复用视角映射 | 02/07-defense-mission-engineering/naf-modaf-reuse.md | 含 NMM 元模型 + 7 个核心视点 + 与 DoDAF/UAF 互补 | ✅ 已完成（2026-06-10） |
| C-08 | 工具链 | 完成交互式复用决策工具 v2.0（CLI + Streamlit Web） | 99-reference/tools/reuse-decision-tool-v2/ | 支持 6 阶段决策流程 + 测试覆盖 + 数据驱动模板 | ✅ 已完成（2026-06-10） |
| C-09 | 供应链安全 | OWASP ASVS 5.0.0 + Top 10:2025 映射 | 10/09-owasp-asvs/ + 10/10-owasp-top10-2025/ | 14 个控制类别 × 3 等级与复用安全映射 | ✅ 已完成（2026-06-10） |
| C-10 | 供应链安全 | OpenSSF OSPS Baseline 映射 | 10/11-osps-baseline/ | 3 级成熟度 × 8 控制类别与复用评估 | ✅ 已完成（2026-06-10） |
| C-11 | AI 原生复用 | NIST AI RMF + 600-1 + CI Profile 映射 | 12/06-ai-governance/ | 4 大功能 × 4 层复用模型的 AI 风险映射 | ✅ 已完成（2026-06-10） |
| C-12 | 跨层治理 | Agentic AI Governance 框架映射 | 06/09-agentic-governance/ | IMDA/NIST/TRACE 五级自主模型 + 七阶段决策扩展 | ✅ 已完成（2026-06-10） |
| C-13 | 形式化验证 | IEEE 1012-2024 + NIST SSDF v1.2 更新 | 07/07-vv-standards/ + 10/12-nist-ssdf-update/ | SIL 四级完整性 + PW.4 复用组件安全实践 | ✅ 已完成（2026-06-10） |
| C-14 | 新兴趋势 | 平台工程深化（CNCF 毕业项目 + IDP AI） | 13/01-platform-engineering/ | Crossplane/Knative/Dragonfly + AI/ML IDP 参考架构；已合并至 01-platform-engineering | ✅ 已完成（2026-06-10） |
| C-15 | 形式化验证 | LLM + 定理证明前沿趋势 | 07/08-emerging-trends/ | LeanDojo/Verus/Agent Behavioral Contracts | ✅ 已完成（2026-06-10） |
| C-16 | 新兴趋势 | 绿色软件与碳成本量化 | 13/04-green-architecture/ | GSF SCI ISO + EU CSRD + 碳预算驱动复用 | ✅ 已完成（2026-06-10） |
| C-17 | 工业 IoT | 数字孪生网络级扩展 | 11/09-network-digital-twin/ | IETF NMRG Network DT + GB/T 45616-2025 | ✅ 已完成（2026-06-10） |
| C-18 | 认知架构 | 决策理论与复用决策 | 08/04-decision-making/ | Prospect Theory/MAUT/认知偏差与复用决策 | ✅ 已完成（2026-06-10） |
| C-19 | 价值量化 | 碳维度价值量化扩展 | 09/03-carbon-dimension/ | SCI + COCOMO II 碳扩展 + Green ROI | ✅ 已完成（2026-06-10） |
| C-20 | 组件架构 | 组件架构深化（4 子目录） | 04/01-04/05/ | 组件模型/接口契约/依赖管理/版本策略 | ✅ 已完成（2026-06-10） |
| C-21 | 功能架构 | 功能架构深化（3 子目录） | 05/01-05/03/ | API 设计/FaaS/事件驱动函数 | ✅ 已完成（2026-06-10） |
| C-22 | 工具链 | ASVS 5.0.0 复用安全检查清单 CLI | 99-reference/tools/asvs-checklist-cli/ | 13 项检查 × L1-L3 等级支持 | ✅ 已完成（2026-06-10） |
| — | 事实修复 | ISO 25010:2024 → 2023 全项目回滚 | 全 struct/ | 88 处引用修复 + 2 文件重命名 | ✅ 已完成（2026-06-10） |

**对齐活动**:

- 对照 OMG SysML v2 官方规范验证模型元素复用语义
- 对照 INCOSE SE Vision 2035 与 ISO/IEC 26550:2015 验证 MBSE-PLE 整合框架
- 对照 OWASP SCVS 1.0 与 SLSA 1.2 验证组件验证控制族映射
- 对照 TMForum ODF / eTOM / SID 验证电信业务架构复用点
- 对照 NATO NAF 4.0 / UK MODAF 验证国防架构复用视角

---

## Phase 6：整合与输出（2027-Q4）— 🔄 进行中

**目标**: 将分散的知识模块整合为可交付的知识产品

| 优先级 | 任务 | 交付物 | 验收标准 | 状态 |
|--------|------|--------|----------|------|
| P0 | 编写《软件工程架构复用视角》全书框架 | `99-reference/book-outline.md` | 12 章 + 附录，每章对应一个一级主题 | ✅ 已完成 v2026-06-10（全书框架 + 权威来源引用） |
| P0 | 制作国际标准对齐多维矩阵（总表） | `99-reference/standards-index/master-alignment-matrix.md` | 覆盖 42+ 标准 × 5 复用层次 | ✅ 已完成 v2.0（42+ 标准，新增 ISO 42020/42030/25040/SysML/SCVS/GUAC 等 18 项） |
| P0 | 制作公理-定理推理树（完整版） | `99-reference/glossary/axiom-theorem-tree.md` | 含 20+ 公理、35+ 定理 | ✅ 已完成 v2026-06-10（28 公理（含启发式）+ 38 定理 + 5 猜想 = 71 条） |
| P1 | 开发交互式决策工具（Web/CLI） | `99-reference/tools/reuse-decision-tool-v2/`（权威实现；v1 `reuse-decision-tool/` 已归档） | 支持 6 阶段复用决策流程 | ✅ 已完成（CLI + Streamlit Web 仪表盘 + 标准追踪器 v2.0） |
| P1 | 编写面向企业的复用成熟度评估问卷 | `06-cross-layer-governance/03-maturity-models/assessment-questionnaire.md` | 基于 ISO/IEC 26565:2026 产品线成熟度框架 | ✅ 已完成（含 CLI 与雷达图报告） |
| P2 | 制作 Mermaid 思维导图库 | `99-reference/visualizations/` | 覆盖全部 13 个主题的 Mermaid 源文件 | ✅ 已完成 v2026-06-10（13 主题 × 4-6 子图，平均 1900 bytes） |

---

## 持续机制

### 月度节奏

- **第 1 周**: 选择一个二级主题进行深度写作
- **第 2 周**: 对照权威来源（标准、论文、课程）进行对齐验证
- **第 3 周**: 编写形式化约束（公理/定理/定义）
- **第 4 周**: 审查、交叉引用、更新 MASTER_PLAN
- **第 5 周（月度审查）**: 事实核查 — 抽查 5-10 个外部引用的事实准确性（见 `99-reference/templates/fact-check-checklist.md`）

### 季度节奏

- **季度初**: 确认本季度聚焦的 2-3 个一级主题
- **季度中**: 中期审查，调整优先级
- **季度末**: 发布季度更新报告，更新 struct/ 中的 README

### 年度节奏

- **年度初**: 对照 ISO/ IEEE 标准更新状态，标记新增/废止标准
- **年度中**: 参加 1-2 个相关国际会议（如 ICSRE, SPLC, FM）
- **年度末**: 发布年度知识产品（白皮书、工具、课程材料）

---

## 任务优先级矩阵

```text
          高影响
            │
    P0 形式化验证案例库    P0 四层核心架构深化
    P0 COCOMO II 2026版    P0 供应链安全纵深防御
    P0 MCP/A2A 协议解析    P0 工业 IoT 复用资产目录
            │
  低 effort ─┼─ 高 effort
            │
    P1 认知架构量化模型    P1 AI 概率契约框架
    P1 零信任供应链模板    P1 平台工程组织设计
    P2 Mermaid 可视化库    P2 交互式决策工具
            │
          低影响
```

---

> **声明**: 本计划是"活文档"。随着标准演进（如 ISO 42024/42042 正式发布）、技术突破（如 SLSA 2.0、MCP 1.0）和实践反馈，计划将持续更新。
>
> 目录结构以 `struct/README.md` 中"实际文件夹结构导航"为准。历史 MASTER_PLAN 中规划但未创建的子目录（如 `quantum-computing`、`domain-driven-design`）按 `SUBSEQUENT_PLAN_2026.md` 决策 4A 处理。`coq-isabelle` 目录已在实际演进中创建并填充内容。
>
> 最后更新: 2026-06-10


---

## 概念定义

- **Roadmap / Master Plan**：项目总体路线图，描述从当前状态到目标状态的分阶段演进路径、关键决策点和验收标准。
- **Phase**：项目阶段，具有明确输入、输出、验收准则和退出条件的工作周期；本计划将项目划分为 Phase 0~6。
- **Milestone**：里程碑，标志阶段完成的关键事件或交付物；用于跟踪进度和管理风险。
- **Living Document**：活文档，随项目演进、标准更新和实践反馈持续修订的文档；计划类文档必须作为活文档维护。

## 正向示例

一个成功的架构复用知识体系路线图应包含：

1. **清晰的分层目标**：Phase 0 止血对齐、Phase 1 结构修复、Phase 2 内容深化、Phase 3 工具化、Phase 4 前沿跟踪、Phase 5 全书整合、Phase 6 社区反馈。
2. **明确的权威来源基线**：每阶段都标注对齐的 ISO/IEC、The Open Group、CNCF、IEC 等标准版本。
3. **可度量的质量门禁**：例如 Markdown 文档必须通过 `scripts/quality-gate.py`，通过率目标 ≥ 70%（当前已达 98%+）。
4. **风险登记册与勘误机制**：对易变标准（如 MCP、WASI、IEC 61508 Ed.3）建立持续监控和快速回退通道。

## 反例/反模式

- **反模式 1：计划与实际执行脱节**。路线图写得宏大但从不更新，导致目录结构、文档内容与计划严重不一致。
- **反模式 2：缺乏退出条件**。阶段划分模糊，无法判断何时进入下一阶段，造成范围蔓延。
- **反模式 3：忽视外部依赖风险**。对标准发布时间、工具成熟度等外部因素不做监控，导致大量返工。

## 权威来源

> **权威来源**:
>
> - ISO/IEC/IEEE 42010:2022. *Systems and software engineering — Architecture description*. <https://www.iso.org/standard/74393.html>
> - ISO/IEC/IEEE 15288:2023. *Systems and software engineering — System life cycle processes*. <https://www.iso.org/standard/81702.html>
> - ISO/IEC/IEEE 12207:2026. *Systems and software engineering — Software life cycle processes*. <https://www.iso.org/standard/90219.html>
> - Project Management Institute. *PMBOK® Guide — Seventh Edition*. <https://www.pmi.org/pmbok-guide-standards/foundational/pmbok>
>
> **核查日期**: 2026-07-07
