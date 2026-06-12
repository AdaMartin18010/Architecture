# 软件工程架构复用视角：后续计划与任务总览（网络对齐版 2026-06-07）

> **版本**: 2026-06-07（网络权威内容对齐版）
> **定位**: 在 `SUBSEQUENT_PLAN_2026.md`（2026-06-06）基础上，全面对齐国际最新标准、技术生态与学术前沿，重新编排未完成项与后续推进计划
> **对齐来源**: ISO/IEC/IEEE DIS 42042/42024、ISO 25010:2023、SLSA 1.2、MCP 2025-11-25 / Agentic AI Foundation、A2A v1.0、WASI 0.3 / Wasm 3.0、IEC 63278-1:2023、IEC 61508 Ed.3（预计2026）、ICSA 2026 / ECSA 2025 / GreenArch 2026、CNCF Platform Engineering Maturity Model、Green Software Foundation SCI

---

## 目录

- [软件工程架构复用视角：后续计划与任务总览（网络对齐版 2026-06-07）](#软件工程架构复用视角后续计划与任务总览网络对齐版-2026-06-07)
  - [目录](#目录)
  - [一、执行摘要](#一执行摘要)
  - [二、未完成计划与任务全景梳理](#二未完成计划与任务全景梳理)
    - [2.1 显式未完成项（Roadmap 级别）](#21-显式未完成项roadmap-级别)
    - [2.2 结构性内容缺口](#22-结构性内容缺口)
    - [2.3 可执行交付物缺口](#23-可执行交付物缺口)
    - [2.4 形式化验证环境缺口](#24-形式化验证环境缺口)
  - [三、国际权威内容对齐与差距更新](#三国际权威内容对齐与差距更新)
    - [3.1 国际标准演进更新（2026-06）](#31-国际标准演进更新2026-06)
    - [3.2 技术生态最新状态](#32-技术生态最新状态)
    - [3.3 学术前沿映射](#33-学术前沿映射)
  - [四、编排后的后续推进计划](#四编排后的后续推进计划)
    - [Phase 1.5 立即修复（2026-Q3 第 1-2 周）](#phase-15-立即修复2026-q3-第-1-2-周)
    - [Phase 2 形式化与量化深化（2026-Q3 第 3 周 ~ 2026-Q4）](#phase-2-形式化与量化深化2026-q3-第-3-周--2026-q4)
    - [Phase 3 垂直领域扩展（2027-Q1）](#phase-3-垂直领域扩展2027-q1)
    - [Phase 4 安全与供应链纵深（2027-Q2）](#phase-4-安全与供应链纵深2027-q2)
    - [Phase 5 AI 原生与前沿（2027-Q3）](#phase-5-ai-原生与前沿2027-q3)
    - [Phase 6 整合与输出（2027-Q4）](#phase-6-整合与输出2027-q4)
  - [五、关键决策确认](#五关键决策确认)
    - [决策 1：目录结构统一策略](#决策-1目录结构统一策略)
    - [决策 2：形式化验证工具链投入](#决策-2形式化验证工具链投入)
    - [决策 3：可执行工具开发策略](#决策-3可执行工具开发策略)
    - [决策 4：前沿主题取舍](#决策-4前沿主题取舍)
    - [决策 5：国际对齐深度](#决策-5国际对齐深度)
    - [决策 6：工业 IoT 标准跟踪策略（新增）](#决策-6工业-iot-标准跟踪策略新增)
  - [六、风险登记册](#六风险登记册)

---

## 一、执行摘要

本项目当前处于 **Phase 1 基本完成 → Phase 1.5 修复过渡期**。经过对 `struct/` 下 92+ 文件、`view/` 下 8 份历史文档（约 31 万字）及多份 roadmap 的全面梳理，结合对国际权威标准与前沿技术的网络对齐，得出以下核心结论：

1. **文档知识体系极为充实**：13 个一级主题全部启动，106+ Markdown 文件覆盖四层复用模型（业务→应用→组件→功能）+ 跨层治理 + 形式化验证 + 认知架构 + 价值量化 + 供应链安全 + 工业 IoT + AI 原生 + 新兴趋势。
2. **可执行交付物严重不足**：大量内容仍为理论 Markdown，Python/Streamlit 工具原型、形式化验证自动流水线、Excel 模板等"最后一公里"交付物缺口明显。
3. **国际标准对齐需紧急刷新**：ISO/IEC/IEEE DIS 42042 已进入 enquiry phase（2026-01 关闭投票）、WASI 0.3 已于 2026-02 发布 preview、MCP 已由 Linux Foundation Agentic AI Foundation 接管并推出 MCP Apps（2026-01）、SLSA 1.2 Multi-Track 已正式发布、IEC 61508 Ed.3 预计 2026 年发布且将强制要求 SIL 2+ 使用结构化代码分析工具。
4. **学术前沿存在映射机会**：ICSA 2026 主题"Architecting in Continuous Software Engineering"、GreenArch 2026（碳感知架构）、ECSA 2025 "impactful software architecture"均与本项目知识体系高度相关，具备投稿/白皮书产出条件。

---

## 二、未完成计划与任务全景梳理

### 2.1 显式未完成项（Roadmap 级别）

| 主题 | 未完成内容 | 计划时间 | 优先级 | 状态说明 |
|------|-----------|----------|--------|----------|
| **01 元模型** | T15: 术语查询脚本（跨标准术语翻译） | 2026-Q3 | P1 | `terminology-query.py` 已创建，待验证完整度 |
| **01 元模型** | OMG RAS v2.2 对齐章节 | 2026-Q4 | P1 | 完全空白，需新建 |
| **01 元模型** | FAIR4RS 原则与软件复用对照 | 2027-Q1 | P1 | 完全空白，需新建 |
| **01 元模型** | ISO/IEC 33000 (SPICE) 与复用成熟度映射 | 2027-Q2 | P2 | 规划中，未启动 |
| **03 应用架构** | Backstage / Port / Cortex IDP 复用实践 | 2026-Q4 | P1 | 目录未创建，需新建 `08-idp-practices/` |
| **04 组件架构** | WASM Component Model 跨语言复用分析（WASI 0.3 更新） | 2026-Q4 | P1 | 已有 WASM 决策树，需大幅更新 WASI 0.3 async 内容 |
| **05 功能架构** | AI 功能概率契约校准工具原型 | 2026-Q4 | P0 | `calibration-tool.py` 已创建，待验证完整度 |
| **07 形式化验证** | T18: Coq/Isabelle 在安全关键组件中的应用 | 2026-Q4 | P0 | 仅简单占位示例（`insertion_sort.v`, `Turnstile.thy`），需深化 |
| **07 形式化验证** | Rust 形式化验证工具链可运行示例（Kani/Prusti/Miri） | 2026-Q4 | P1 | 文档深入但无可复现 CI |
| **08 认知架构** | 眼动追踪/EEG 实验设计的复用认知研究方案 | 2027-Q1 | P2 | 规划中，未启动 |
| **08 认知架构** | AI 辅助复用系统原型设计（RAG+LLM 流程） | 2026-Q4 | P1 | 架构文档已完成，缺可交互原型 |
| **09 价值量化** | COCOMO II 2026 可执行计算器（完整 AAM/SU/UNFM） | 2026-Q4 | P1 | `cocomo-calculator.py` 已创建，待验证完整度 |
| **09 价值量化** | FinOps 跨层成本分摊 Excel 导出（带公式） | 2026-Q4 | P1 | `finops-allocation.py` 存在，Excel 导出 TODO 未关闭 |
| **10 供应链安全** | SLSA L4 分布式构建验证（多签名、可复现性） | 2027-Q2 | P1 | 完全空白 |
| **10 供应链安全** | 供应链攻击树交互式可视化 | 2027-Q2 | P2 | 静态 Markdown 存在，缺动态渲染 |
| **10 供应链安全** | EU CRA 合规检查清单工具（自动化评估） | 2027-Q2 | P1 | 规划中，未启动 |
| **11 工业 IoT** | T18: IEC 61508 Proven-in-Use 贝叶斯统计验证工具 | 2027-Q1 | P1 | 规划中，未启动 |
| **11 工业 IoT** | T19: ISO 26262 SEooC 复用流程模板 | 2027-Q1 | P1 | 规划中，未启动 |
| **11 工业 IoT** | T20: 工业边缘 AI 模型部署规范（ONNX/TFLite） | 2027-Q1 | P1 | 规划中，未启动 |
| **11 工业 IoT** | T21: MCP for Industrial AI 协议草案 | 2027-Q1 | P1 | 规划中，未启动 |
| **12 AI 原生** | Agentic Governance 组织设计模板 | 2026-Q4 | P1 | 规划中，未启动 |
| **12 AI 原生** | CP + 形式化验证融合框架（研究探索方向，尚无成熟学术基础） | 2027-Q3 | P2 | 完全空白，国际前沿 |
| **13 新兴趋势** | RegTech Agentic 架构的案例验证 | 2027-Q3 | P2 | 规划中，未启动 |
| **13 新兴趋势** | 可持续软件架构（GreenArch）初探 | 2027-Q3 | P2 | 完全空白，需对齐 GSF SCI |
| **99 参考** | 交互式复用决策工具（Web/CLI） | 2027-Q4 | P2 | Phase 6 目标 |

### 2.2 结构性内容缺口

| 主题 | 规划中应存在的子目录 | 实际状态 | 严重程度 |
|------|---------------------|----------|----------|
| 02 业务架构 | `01-business-capability-model` / `02-business-process-reuse` / `03-domain-driven-design` / `04-business-rules` | 缺失 3 个；`01` 重命名为 `02-business-capability` | 🟡 中 |
| 03 应用架构 | `01-layered-architecture` / `02-microservices` / `03-serverless` / `04-event-driven` | 全部缺失；内容合并到其他子目录 | 🟡 中 |
| 04 组件架构 | `01-component-models` / `02-interface-contracts` / `03-dependency-management` | 缺失 3 个 | 🟡 中 |
| 05 功能架构 | `01-api-design` / `02-function-as-a-service` / `03-event-functions` | 缺失 3 个 | 🟡 中 |
| 06 跨层治理 | `02-reuse-process` / `03-policy-automation` | 缺失 2 个 | 🟡 中 |
| 07 形式化验证 | `03-coq-isabelle` / `07-model-checking` | `03` 仅占位；`07` 未在 README 列出 | 🔴 高 |
| 08 认知架构 | `04-decision-making` | 缺失 | 🟡 中 |
| 09 价值量化 | `03-finops-allocation` / `04-risk-adjusted-value` | 缺失（FinOps 内容实际在 06 下） | 🟡 中 |
| 12 AI 原生 | `02-model-reuse` / `04-rag-patterns` | 缺失 2 个 | 🟡 中 |
| 13 新兴趋势 | `03-edge-computing` / `04-quantum-computing` / `05-sustainable-software` | 缺失 3 个；实际新增模块化单体/Rust/RegTech | 🟡 中 |

### 2.3 可执行交付物缺口

大量内容仍为 Markdown 理论文档，以下**可执行交付物**尚未达到"开箱即用"状态：

1. **成熟度评估问卷** → 需从 Markdown 转为可交互表单（YAML/JSON + Python CLI），生成雷达图 + 成熟度报告
2. **FinOps 成本分摊模板** → Excel 带公式导出（`xlsxwriter`/`openpyxl`），供财务人员直接使用
3. **COCOMO II 2026 计算器** → 支持 AAM/SU/UNFM 参数输入和 ROI 输出的 Python/Streamlit 或 Excel 工具
4. **AI 概率契约校准工具** → Conformal Prediction 实现，支持温度/Top-p/模型版本漂移的边界计算
5. **PIU 贝叶斯统计验证工具** → Python（工业安全），支持失效数据输入 → SIL 可信度输出
6. **供应链攻击树可视化** → Mermaid/Graphviz 动态渲染，支持点击展开/防御矩阵联动
7. **术语查询脚本** → Python CLI 跨标准术语检索（`terminology-query.py` 已创建，待完善）
8. **复用决策交互工具** → Web/CLI（MASTER_PLAN Phase 6 目标），支持 6 阶段决策流程
9. **EU CRA 合规检查清单工具** → JSON + CLI，自动评估合规项

### 2.4 形式化验证环境缺口

| 缺口 | 说明 | 影响 |
|------|------|------|
| TLA+ 未跑 TLC/SANY | `verify-all.sh` 中 TLC 命令被注释为 TODO；环境无 Java/TLA+ Toolbox | 无法保证规约无死锁/不变量成立 |
| Alloy 未跑 Alloy Analyzer | `verify-all.sh` 中 Alloy 命令被注释为 TODO | 无法验证模型可满足性 |
| Coq/Isabelle 空白 | T18 未完成，仅简单示例；`verify-all.sh` 中 Rocq/Isabelle 命令被注释 | 缺少定理证明层的高保证案例 |
| Rust 形式化未链接 Kani/Prusti | 文档深入但无实际可跑验证；缺少 CI 脚本 | 缺少可复现的验证流水线 |

---

## 三、国际权威内容对齐与差距更新

### 3.1 国际标准演进更新（2026-06）

| 国际标准 | 最新状态（网络对齐） | 本项目覆盖状态 | 差距 | 后续行动 |
|----------|---------------------|---------------|------|----------|
| **ISO/IEC/IEEE DIS 42042** | 2026-01 关闭投票（Stage 40.60 enquiry phase），预计 2026 年内定稿。覆盖 AI/ML/IoT/云计算/数字孪生等应用领域 | 仅作为待跟踪项 | 草案即将定稿，缺少参考架构元模型与复用框架的对照 | **紧急**：跟踪进展，一旦发布立即补充到 `01-meta-model-standards` |
| **ISO/IEC/IEEE DIS 42024** | 2026-01-12 截止公开征询，基础架构词汇与概念标准 | 未明确引用 | 缺少基础术语与复用视角的对照 | 补充到 `01-meta-model-standards` |
| **ISO/IEC 25010:2023** | 已正式发布（取代 2011 版）。Reusability 为 Maintainability 子特性；Modularity 独立；新增 Interaction capability/Flexibility/Safety；新增 AI/ML 质量考量 | 在 06/01 中提及，未深入展开 Reusability 与 Modularity/Analysability/Testability 的相互作用 | 需补充 25010:2023 质量特性对复用的影响矩阵 | 更新 `01-meta-model-standards` 或 `06-cross-layer-governance` |
| **ISO/IEC 25040:2024** | 已发布（Evaluation）。新增"获取或复用预开发产品"的评估流程 | 未明确引用 | 缺少评估流程与复用决策的对照 | 新增对照章节 |
| **SLSA 1.2** | **已正式发布**（OpenSSF）。Multi-Track：Build / Source / Attested Build Environments。Build Level 4 仍在开发 | 已更新到 1.1/1.2，但 L4 分布式构建验证仍为空白 | L4 多签名/可复现构建实践缺失 | 补充 `slsa-l4-distributed-builds.md` + sigstore/cosign 示例 |
| **IEC 61508 Ed.3** | **预计 2026 年发布**。关键变化：SIL 2+ 强制使用结构化代码分析工具；AI/ML 组件处理更新；模型驱动开发更清晰指导 | 当前基于 Ed.2，Ed.3 变化未对齐 | 一旦发布需更新功能安全章节 | 建立跟踪，发布后 4 周内更新 |
| **ISO 21448:2026 (SOTIF Ed.2)** | 已发布。扩展至 SAE L3-L5；新增场景完整性度量、分布偏移验证 | 未覆盖 | 对自动驾驶/工业 AI 复用极具相关性 | 可选补充到 `11-industrial-iot-otit/06-functional-safety` |
| **DO-178C AI/ML Supplement** | 2026-04 进入公众评议阶段（RTCA SC-228），涵盖数据集管理、可解释性、概率输出与确定性安全目标交互 | 未覆盖 | 对安全关键 AI 复用极具相关性 | 可选补充到 `07-formal-verification/05-spark-ada` 或新增 |
| **SysML v2** | 2026-03 正式发布（OMG）。全新文本语法 KerML、参数化模型、仿真接口 | 未引用 | 与 MBSE/数字孪生章节可建立映射 | 可选补充到 `11-industrial-iot-otit/05-digital-twin-aas` |

### 3.2 技术生态最新状态

| 技术/框架 | 国际最新状态（2026-06） | 本项目状态 | 差距 |
|-----------|----------------------|-----------|------|
| **MCP** | 1. **治理**：已捐给 Linux Foundation Agentic AI Foundation（AAIF），Anthropic/Block/OpenAI 共创。华为 2026-02 成为金牌会员。 2. **规范**：2025-11-25 为当前稳定版，新增 Tasks、Icons、Elicitation URL mode、JSON Schema 2020-12。 3. **生态**：2026-01 推出 MCP Apps（交互式 UI）；SDK 月下载 9700 万次（970x 年增长）。 4. **安全**：Microsoft 2026-04 发布 Agent Governance Toolkit；OWASP LLM/MCP Top 10 受关注 | 文档提及 2026-07-28 RC（CHANGELOG 已勘误），但 2025-11-25 的 Tasks/Icons/MCP Apps 等新特性覆盖不足 | **需全面更新**：替换旧引用，补充 Tasks/Icons/Elicitation/OAuth 增量，增加 Agent Governance Toolkit 对齐 |
| **A2A** | Google Cloud Next 2026 发布 **v1.0**；ACP 已并入 A2A（Linux Foundation LF AI & Data） | 已有深度解析（v0.3/v1.0），基本完整 | 更新 v1.0 最终特性，补充 ACP 合并背景 |
| **WASI / Component Model** | 1. **Wasm 3.0**：2025-09 成为 W3C 标准（WasmGC/异常处理/尾调用/SIMD）。 2. **WASI 0.3**：2026-02 preview 发布（Wasmtime 37+），原生 async（`stream<T>`/`future<T>`），Canonical ABI 级实现。 3. **WASI 1.0**：目标 2026 末/2027 初。 4. **.NET**：.NET 11 preview（2026 末）将包含 CoreCLR WebAssembly runtime，.NET 12（2027）全面支持 C# async/await in WASM | 已有 WASM 决策树，但对 WASI 0.3 async、warg registry（已停止积极开发，社区转向 OCI-based registry）、多线程限制覆盖不足 | **需大幅更新**：补充 WASI 0.3 与跨语言复用边界，更新 `wasm-wasi-03-boundaries.md` |
| **CNCF Platform Engineering** | Platform Engineering Maturity Model 五维度（Investment/Adoption/Interfaces/Operations/Measurement）。80% 大企业已建立平台工程团队（Gartner）。Backstage 被 3000+ 组织采用 | 已有 maturity model，但与 CNCF 五维度逐条映射可深化 | 补充五维度评估检查清单，增加 Backstage/Port/Cortex 对比矩阵 |
| **Rust 安全关键** | AdaCore + Ferrous Systems 2026-03 联合发布 DO-178C DAL A 资质套件（rustc 编译器工具资质+安全手册），使 Rust 成为航空最高安全等级的可行选项 | 已有 Rust 形式化语义文档，但未覆盖 DO-178C 资质路径 | 可选补充到 `07-formal-verification/04-rust-type-system` 或 `05-spark-ada` |
| **Conformal Prediction** | 在代码生成/验证领域快速兴起。与形式化验证（Lean/Coq）结合的 "AI 生成 + CP 筛选 + 定理证明" 三层保证框架成为前沿方向 | 已有 `cp-code-generation.md` | 可补充与 TLA+/Coq 结合的 AI 验证框架 |

### 3.3 学术前沿映射

| 会议/社区 | 2025-2026 主题 | 本项目覆盖 | 建议 |
|-----------|---------------|-----------|------|
| **ICSA 2026** (Amsterdam, Jun 22-26) | "Architecting in Continuous Software Engineering: Evolving Roles, Enduring Principles"。强调 AI 与架构融合、30 周年反思（1996-2026） | 提及但未系统对齐 | **高优先级**：增加 ICSA 主题与本框架的映射，为 Phase 6 白皮书/投稿做准备 |
| **ECSA 2025** (Limassol, Sep 15-19) | "impactful software architecture"。关注 AI/LLM 密集系统架构、可持续架构、数字孪生、量子软件 | 未引用 | 补充 ECSA 架构影响力模型，对齐 "impactful" 度量 |
| **GreenArch 2026** (ICSA Workshop) | "Software Architecture for Green Sustainable Carbon-aware Software Systems"。首个 ICSA 绿色架构 Workshop | 未覆盖 | **新增**：`13-emerging-trends/07-green-software/` 对齐 GSF SCI、碳感知架构复用度量 |
| **GREENS'26** | 绿色软件工程、Green AI、碳感知计算、LLM 可持续性 | 未覆盖 | 与 GreenArch 内容可合并或互补 |
| **SAGAI / SEAMS 2026** | 生成式 AI + 自适应系统、自适应性根因分析 | 未系统覆盖 | 可选：AI 辅助复用决策与自适应性结合 |

---

## 四、编排后的后续推进计划

> **编排原则**：
>
> 1. 优先级以"填补国际差距 + 可执行交付物"为核心；
> 2. 每个 Phase 明确列出对齐的国际来源；
> 3. 验收标准必须可验证（代码可运行 / 文档可审查 / 工具可演示）。

### Phase 1.5 立即修复（2026-Q3 第 1-2 周）

**目标**: 修复本轮（2026-06-06）遗留的一致性问题，激活形式化验证环境，为 Phase 2 扫清基础。

| 任务 ID | 任务 | 交付物 | 对齐来源 / 验收标准 | 优先级 |
|---------|------|--------|---------------------|--------|
| P1.5-T1 | 更新 01-roadmap：T05-T08 标记为 `[x]` | `01-meta-model-standards/plans-tasks/roadmap.md` | 与 `roadmap-consistency-audit.md` 一致 | P0 |
| P1.5-T2 | 更新 11-roadmap：T13-T17 标记为 `[x]`；确认 AAS-OPC UA 完整映射 | `11-industrial-iot-otit/plans-tasks/roadmap.md` | 已交付文件状态准确 | P0 |
| P1.5-T3 | 更新 07-roadmap：TLA+ 案例库状态；修正跨主题交付物路径 | `07-formal-verification/plans-tasks/roadmap.md` | OPC UA FX / PLCopen 路径指向 11/ 下实际文件 | P0 |
| P1.5-T4 | 重构 `struct/README.md` 文件夹结构导航 | `struct/README.md` | 与实际 `struct/` 目录一致（允许新增/重命名有说明） | P1 |
| P1.5-T5 | 清理 `.vscode/README.md` 中疑似 PostgreSQL 残留内容 | `.vscode/README.md` | 内容与项目主题一致 | P1 |
| P1.5-T6 | **建立形式化验证自动化环境（Docker）** | `99-reference/tools/formal-verification-env/docker-compose.yml` + `verify-all.sh` 激活 | **对齐**: TLA+ Toolbox / Alloy Analyzer / Coq (Rocq) / Isabelle。能运行 TLC 和 Alloy Analyzer 至少一个案例 | P0 |
| P1.5-T7 | 更新 CHANGELOG：记录 ArchiMate 4.0（2026-04-27）、MCP 2025-11-25、SLSA 1.2 等标准状态 | `99-reference/CHANGELOG.md` | 时间线准确，含权威来源 URL | P1 |

### Phase 2 形式化与量化深化（2026-Q3 第 3 周 ~ 2026-Q4）

**目标**: 将形式化验证、认知架构、价值量化从"理论文档"转化为"可操作方法论 + 可执行工具"。

| 任务 ID | 任务 | 交付物 | 对齐来源 | 验收标准 |
|---------|------|--------|----------|----------|
| P2-T1 | **Coq/Isabelle 高安全等级组件验证案例** | `07-formal-verification/03-coq-isabelle/README.md` + `.v`/`.thy` 案例（2+ 个） | Coq (Inria)、Isabelle/HOL (TU Munich)、seL4/CompCert | 含证明纲要和可执行脚本；Docker 环境可跑通 |
| P2-T2 | **Alloy 跨层映射 + ISA-95 层次一致性验证** | `07-formal-verification/02-alloy/cross-layer-mapping.md` 扩展 + `.als` | Alloy Tools (MIT)、ISO/IEC 42010 | 新增 ISA-95 五层约束，Alloy Analyzer 可运行 |
| P2-T3 | **Rust 形式化验证工具链实践（Kani/Prusti/Miri）** | `07-formal-verification/04-rust-type-system/toolchain-practice.md` + 3+ 可运行示例 + CI 脚本 | RustBelt (MPI-SWS)、Kani (AWS)、Prusti (ETH)、**AdaCore+Ferrous DO-178C kit** | CI 通过；示例覆盖内存安全/并发/unsafe 边界 |
| P2-T4 | **COCOMO II 2026 可执行计算器** | `09-value-quantification/tools/cocomo-calculator.py` + Excel | USC COCOMO II Manual (Boehm) | 支持 AAM/SU/UNFM 参数输入和 ROI 输出；Streamlit 可选 |
| P2-T5 | **FinOps 跨层成本分摊 Python/Excel 模板** | `06-cross-layer-governance/04-finops-cost/templates/` + `99-reference/tools/finops-template/` | FinOps Foundation | Excel 带公式导出；含四级分摊公式和示例数据 |
| P2-T6 | **复用成熟度可执行评估问卷** | `06-cross-layer-governance/03-maturity-models/assessment-tool/` (YAML + Python CLI) | ISO/IEC 26566:2026、NASA RRL、**CNCF Maturity Model 五维度** | 生成雷达图 + 成熟度报告；CNCF 五维度可选评估 |
| P2-T7 | **AI 功能概率契约校准工具原型** | `12-ai-native-reuse/05-probabilistic-contracts/calibration-tool.py` | Conformal Prediction (Vovk et al.)、OWASP LLM/MCP Top 10、**Microsoft Agent Governance Toolkit** | 支持温度/Top-p/模型版本漂移的边界计算；可视化输出 |
| P2-T8 | **AI 辅助复用决策系统原型设计** | `08-cognitive-architecture/05-ai-cognitive-augmentation/prototype-design.md` + PoC 架构 | ACT-R (CMU)、NASA-TLX | 含 RAG+LLM 流程图和最小可运行 PoC（Python） |
| P2-T9 | **术语查询脚本** | `99-reference/tools/terminology-query.py` | IREB CPRE Glossary、ISO/IEC 42010/42024 | 支持跨标准术语搜索和别名映射；CLI 可用 |
| P2-T10 | **OMG RAS v2.2 对齐章节** | `01-meta-model-standards/07-omg-ras/ras-alignment.md` | OMG RAS v2.2 | 覆盖 Classification/Solution/Usage/Related Assets |
| P2-T11 | **Backstage / Port / Cortex IDP 复用实践** | `03-application-architecture-reuse/11-idp-practices/backstage-port-cortex.md` | CNCF Platform Engineering Maturity Model、Backstage.io | 三家平台对比 + Golden Path 模板 + 选型决策树 |

### Phase 3 垂直领域扩展（2027-Q1）

**目标**: 深化工业 IoT/OT-IT 融合，补齐功能安全、边缘 AI、PIU 工具；对齐 IEC 61508 Ed.3 预览。

| 任务 ID | 任务 | 交付物 | 对齐来源 | 验收标准 |
|---------|------|--------|----------|----------|
| P3-T1 | **IEC 61508 Proven-in-Use (PIU) 贝叶斯统计验证工具** | `11-industrial-iot-otit/06-functional-safety/piu-bayesian-tool.py` | IEC 61508-3-1:2016、**Ed.3 预览版** | 支持失效数据输入 → SIL 可信度输出；含可视化 |
| P3-T2 | **ISO 26262 SEooC 复用流程模板** | `11-industrial-iot-otit/06-functional-safety/iso26262-seooc-template.md` | ISO 26262-8 Clause 12 | 含安全手册、假设、验证清单、复用决策树 |
| P3-T3 | **工业边缘 AI 模型部署规范** | `11-industrial-iot-otit/07-edge-ai/model-deployment-spec.md` + ONNX Runtime 示例 | TinyML、ONNX、IEC 62443 | 覆盖 TFLite/ONNX 部署流程；含性能基准 |
| P3-T4 | **MCP for Industrial AI 协议草案** | `11-industrial-iot-otit/07-edge-ai/mcp-industrial-ai-draft.md` | MCP 2025-11-25、OPC UA FX | 定义工业场景 Tools/Resources 规范；与 AAS 映射 |
| P3-T5 | **AAS 到 OPC UA NodeSet 完整映射规范（确认/补全）** | `11-industrial-iot-otit/05-digital-twin-aas/aas-opcua-nodeset-mapping.md` | IDTA AAS、OPC Foundation、**IEC 63278-1:2023** | XML/JSON 示例 + 映射表 + 与 FX ConnectionManager 的集成 |
| P3-T6 | **FAIR4RS 原则与软件复用对照** | `01-meta-model-standards/08-fair4rs/fair4rs-alignment.md` | FAIR4RS (2022; ARDC) | 与 SBOM、MCP Tool 注册表、AAS 子模型的映射 |
| P3-T7 | **ISO 21448 SOTIF Ed.2 对齐（可选）** | `11-industrial-iot-otit/06-functional-safety/iso21448-sotif-alignment.md` | ISO 21448:2026 | 分布偏移验证与 AI 功能复用概率契约的关联 |

### Phase 4 安全与供应链纵深（2027-Q2）

**目标**: 构建 SLSA L4、SBOM 深度应用、攻击树可视化的纵深防御体系；对齐 NIST SSDF 1.2 Initial Public Draft（征求意见稿），并跟踪其正式版发布。

| 任务 ID | 任务 | 交付物 | 对齐来源 | 验收标准 |
|---------|------|--------|----------|----------|
| P4-T1 | **SLSA 1.2 Multi-Track 深度解析（Build/Source/Environment）** | `10-supply-chain-security/01-slsa-framework/slsa-1-2-multi-track.md` | **SLSA.dev (OpenSSF) 正式版** | 三轨道 × L1-L3 要求矩阵；与复用决策矩阵联动 |
| P4-T2 | **SLSA L4 分布式构建验证实践** | `10-supply-chain-security/01-slsa-framework/slsa-l4-distributed-builds.md` + sigstore/cosign 示例 | OpenSSF、Sigstore | 多签名 + 可复现构建 POC；GitHub Actions 流水线可运行 |
| P4-T3 | **供应链攻击树交互式可视化** | `10-supply-chain-security/03-attack-vectors/attack-tree-interactive.html` / `.py` | MITRE ATT&CK、OWASP SCVS | 支持点击展开/防御矩阵联动；Streamlit/Dash 可选 |
| P4-T4 | **NIST SSDF 1.2 Initial Public Draft 对齐** | `10-supply-chain-security/06-case-studies/nist-ssdf-1-2-alignment.md` 更新 | NIST SP 800-218r1 IPD | 同步征求意见稿内容；跟踪正式版发布；与 SLSA 1.2 的映射 |
| P4-T5 | **EU CRA 合规检查清单工具** | `10-supply-chain-security/06-case-studies/eu-cra-checklist.json` + CLI | Regulation (EU) 2024/2847 | 自动评估合规项；生成差距报告 |
| P4-T6 | **IEEE 1517 复用过程映射** | `01-meta-model-standards/01-iso-420xx-family/ieee-1517-reuse-processes.md` | IEEE 1517-2010; ISO/IEC/IEEE 12207:2026 | 与 12207:2026 的对照；复用活动细化；2017 版仅作历史对照 |
| P4-T7 | **ISO/IEC 33000 (SPICE) 与复用成熟度映射（可选）** | `06-cross-layer-governance/03-maturity-models/spice-rcmm-mapping.md` | ISO/IEC 33000 系列 | 六级过程能力与 RCMM/RiSE 的映射 |

### Phase 5 AI 原生与前沿（2027-Q3）

**目标**: 将 AI/LLM 功能复用、Agentic Infrastructure、WASM、平台工程、可持续架构提升到工程化水平。

| 任务 ID | 任务 | 交付物 | 对齐来源 | 验收标准 |
|---------|------|--------|----------|----------|
| P5-T1 | **MCP 2025-11-25 全面更新（替换旧引用）** | `12-ai-native-reuse/01-mcp-protocol/mcp-2025-11-25-deep-dive.md` 更新 | modelcontextprotocol.io/specification/2025-11-25、**AAIF** | 覆盖 Tasks、Icons、Elicitation、OAuth 增量、**MCP Apps**、Agent Governance Toolkit |
| P5-T2 | **Agentic Governance 组织设计模板** | `12-ai-native-reuse/03-agentic-infrastructure/agentic-governance-template.md` | Google A2A v1.0、Linux Foundation Agentic AI Foundation、**Microsoft Agent Governance Toolkit** | 含 Agent RBAC、Golden Path、模型路由、审计追踪 |
| P5-T3 | **CP + 形式化验证融合框架（研究探索方向，尚无成熟学术基础）** | `12-ai-native-reuse/07-conformal-prediction/cp-formal-verification.md` | **Conformal Prediction (Vovk et al.)、Cherian & Candès (NeurIPS 2024, LLM validity via enhanced CP)、Angelopoulos & Bates (CP 现代教程)** | 提出"AI 生成 + CP 筛选 + 定理证明"三层保证（探索性框架） |
| P5-T4 | **WASM Component Model + WASI 0.3 复用边界更新** | `13-emerging-trends/03-webassembly-components/wasm-wasi-03-boundaries.md` | Bytecode Alliance、Wasmtime 37+、**WASI 1.0 roadmap** | 覆盖 stream/future、async、线程限制、.NET WASM runtime 前瞻 |
| P5-T5 | **CNCF Platform Engineering 五维度评估检查清单** | `13-emerging-trends/01-platform-engineering/platform-maturity-model.md` 扩展 | **CNCF TAG App Delivery** | 五维度（Investment/Adoption/Interfaces/Operations/Measurement）逐条映射 |
| P5-T6 | **RegTech Agentic 架构案例验证** | `13-emerging-trends/06-regtech-ai/regtech-case-validation.md` | FCA/SEC/EU regulators | 1+ 真实监管场景 POC 设计 |
| P5-T7 | **可持续软件架构（GreenArch）初探** | `13-emerging-trends/07-green-software/green-architecture-reuse.md` | **GreenArch 2026**、Green Software Foundation SCI、Carbon Aware SDK | 碳感知架构复用度量；与 FinOps 成本模型的关联 |
| P5-T8 | **ICSA 2026 / ECSA 2025 主题映射与投稿准备（可选）** | `99-reference/publications/icsa-2026-whitepaper-draft.md` | ICSA 2026、ECSA 2025 | 完成 1 份白皮书/短篇论文初稿 |

### Phase 6 整合与输出（2027-Q4）

**目标**: 将分散知识模块整合为可交付产品。

| 任务 ID | 任务 | 交付物 | 验收标准 |
|---------|------|--------|----------|
| P6-T1 | 《软件工程架构复用视角》全书框架定稿 | `99-reference/book-outline.md` 更新 | 12 章 + 附录，每章对应一级主题；预计 326,000 字 |
| P6-T2 | 国际标准对齐总矩阵 v2.0 | `99-reference/standards-index/master-alignment-matrix.md` 更新 | 覆盖 **30+ 标准** × 5 复用层次 |
| P6-T3 | 公理-定理推理树完整版 | `99-reference/glossary/axiom-theorem-tree.md` 更新 | **20+ 公理、35+ 定理** |
| P6-T4 | 交互式复用决策工具（Web/CLI） | `99-reference/tools/reuse-decision-tool/` | 支持 6 阶段决策流程；Streamlit 优先 |
| P6-T5 | Mermaid 可视化库补全 | `99-reference/visualizations/` | 覆盖 13 个主题 + 新增 GreenArch/CP |
| P6-T6 | 项目官网/GitBook 发布准备 | `99-reference/website/` | 在线可浏览知识体系 |
| P6-T7 | 国际会议投稿/白皮书（ICSA/ECSA/绿会） | `99-reference/publications/` | 至少 1 份白皮书被接收或发表 |

---

## 五、关键决策确认

在启动 Phase 2 之前，请您确认以下决策（与 `SUBSEQUENT_PLAN_2026.md` 保持一致，部分选项已根据网络对齐更新）：

### 决策 1：目录结构统一策略
>
> **选项 A（推荐）**: 重构 `struct/README.md` 和 `MASTER_PLAN.md` 中的目录树，使其 100% 匹配实际 `struct/` 目录，删除/合并规划中未实现的子目录（如 `quantum-computing` 按原 4A 决策暂缓）。
> **选项 B**: 保留现有规划树，为缺失子目录创建占位符（README + TODO），后续按规划补齐。
> **选项 C**: 不调整顶层规划，仅在 README 中增加"实际目录与规划存在差异"的免责声明。

### 决策 2：形式化验证工具链投入
>
> **选项 A（推荐）**: 建立 Docker 化的 TLA+ Toolbox + Alloy Analyzer + Coq (Rocq) 环境，要求所有新增形式化规约必须通过自动化验证。
> **选项 B**: 维持当前"人工语法审查"模式，仅在 Phase 6 前统一跑一遍工具。
> **选项 C**: 只对高优先级规约（MCP/A2A/PLCopen）跑工具，其余保持文档级。

### 决策 3：可执行工具开发策略
>
> **选项 A（推荐）**: 优先用 Python CLI + Streamlit 开发所有工具原型（COCOMO 计算器、FinOps 模板、成熟度问卷、PIU 工具），保持最低可用（MVP）。
> **选项 B**: 投资一个统一的 Web 平台（如 Docusaurus + React）承载所有交互式工具。
> **选项 C**: 仅提供 Excel + Markdown 模板，不开发代码原型。

### 决策 4：前沿主题取舍
>
> **选项 A（推荐）**: 2027 年重点补齐 **CP + 形式化验证融合（研究探索方向，尚无成熟学术基础）**、**WASI 0.3**、**Agentic Governance**、**GreenArch/可持续软件架构**；**暂缓量子计算和边缘计算通用架构**。
> **选项 B**: 按 MASTER_PLAN 原规划，恢复 `quantum-computing` 和 `sustainable-software` 子目录。
> **选项 C**: 仅维护现有 13 个主题，不扩展新前沿方向。

### 决策 5：国际对齐深度
>
> **选项 A（推荐）**: 每篇新增/更新文档必须明确列出 1-3 个国际权威来源 URL，并在 `99-reference/external-links/authoritative-sources.md` 中登记；建立标准 RSS/邮件列表监控机制（ISO/OMG/OpenSSF/Bytecode Alliance）。
> **选项 B**: 保持当前风格，在 README 中统一列出权威来源，不要求每文档标注。
> **选项 C**: 仅在关键标准文档中标注来源，日常内容不强制。

### 决策 6：工业 IoT 标准跟踪策略（新增）
>
> **选项 A（推荐）**: 建立 IEC 61508 Ed.3 和 ISO 21448 Ed.2 的跟踪通道，一旦发布立即启动差距分析（预计 2026 年内），4 周内更新相关章节。
> **选项 B**: 等待标准正式发布后再评估是否需要更新。
> **选项 C**: 不跟踪，保持现有 Ed.2 内容。

---

## 六、风险登记册

| 风险 ID | 风险描述 | 影响 | 缓解措施 | 状态 |
|---------|----------|------|----------|------|
| R1 | ISO 42042 / IEC 61508 Ed.3 / WASI 1.0 在计划期内发布新版本 | 已写内容需返工 | 建立标准 RSS/邮件列表监控；文档中标注版本和勘误；CHANGELOG 及时更新 | 🟡 监控中 |
| R2 | TLA+/Alloy/Coq 工具链环境搭建复杂 | Phase 2 延迟 | 优先 Docker 化验证环境；分阶段从人工→自动；仅对关键规约强制验证 | 🟡 监控中 |
| R3 | 工业 IoT 领域标准（OPC UA FX 1.0、IEC 63278）获取成本高 | 内容权威性受限 | 优先使用公开规范摘要、IDTA 模板、厂商白皮书、学术论文；必要时购买标准 PDF | 🟢 已缓解 |
| R4 | 可执行工具开发工作量大 | Phase 2/3 范围膨胀 | 用 Python CLI + Streamlit 快速原型，避免重前端；定义明确的 MVP 边界 | 🟡 监控中 |
| R5 | 目录规划与实际结构长期不一致 | 维护成本增加 | Phase 1.5 彻底重构 README；后续严格执行变更日志；禁止无计划新增目录 | 🟡 监控中 |
| R6 | AI 领域发展迅速，MCP/A2A/Agentic 内容易过期 | 前沿章节准确性下降 | 按季度审查 12-ai-native-reuse；建立外部链接健康检查；关注 AAIF 动态 | 🟡 监控中 |
| R7 | MCP SDK 生态质量参差不齐（平均分 44.7/100） | 若本项目涉及 MCP Server 推荐，可能引用低质量工具 | 建立 MCP Server 评估维度（安全/实用/维护/独特性），仅推荐高分工具 | 🟡 新增风险 |
| R8 | WASI 0.3 仍为 preview，WASI 1.0 尚未发布 | WASM 跨语言复用内容可能因标准变更而返工 | 明确标注 WASI 0.3 preview 状态；跟踪 Bytecode Alliance roadmap；WASI 1.0 发布后 2 周内更新 | 🟡 新增风险 |

---

> **下一步**: 请您审阅以上计划与决策，回复选项编号或提出修改意见。确认后，我将按 Phase 1.5 立即启动目录一致性修复和形式化验证环境搭建，并同步更新相关 roadmap 文件。
>
> **最后更新**: 2026-06-07（对齐 ISO DIS 42042/42024、SLSA 1.2、MCP AAIF、WASI 0.3、IEC 61508 Ed.3、ICSA 2026、GreenArch 2026 等最新权威来源）
