# 软件工程架构复用视角：2026-2027 更新完善计划（网络权威对齐版 v2）

> **版本**: 2026-07-06
> **定位**: 在 `SUBSEQUENT_PLAN_2026.md`（2026-06-10）与 `MASTER_PLAN_2026_NETWORK_ALIGNED.md`（2026-06-07）基础上，结合本项目全部内容与 2026 年 7 月国际权威来源的最新状态，输出后续更新、改进、完善计划与任务清单，供确认后执行。
> **对齐来源**: ISO/IEC/IEEE 42010/42020/42030/42024/42042、ISO/IEC 25010:2023、ISO/IEC 26566:2026、ISO/IEC/IEEE 12207:2026、TOGAF 10、ArchiMate 4.0、OMG RAS v2.2、FAIR4RS、SysML v2/KerML、SLSA 1.2、NIST SSDF 1.2、OWASP MCP Top 10 / Agentic AI Top 10、Microsoft Agent Governance Toolkit、MCP 2025-11-25 / AAIF、A2A v1.0、WASI 0.3 / Component Model、CNCF Platform Engineering Maturity Model、GSF SCI / SCI for AI、IEC 61508 Ed.3、ISO 21448 Ed.2、IEC 63278 AAS、OPC UA FX、ICSA 2026 / ECSA 2025 / GreenArch 2026。

---

## 目录

- [软件工程架构复用视角：2026-2027 更新完善计划（网络权威对齐版 v2）](#软件工程架构复用视角2026-2027-更新完善计划网络权威对齐版-v2)
  - [目录](#目录)
  - [一、执行摘要](#一执行摘要)
    - [1.1 项目当前状态](#11-项目当前状态)
    - [1.2 本轮网络对齐的核心发现](#12-本轮网络对齐的核心发现)
    - [1.3 总体方向](#13-总体方向)
  - [二、国际权威来源对齐现状（2026-07）](#二国际权威来源对齐现状2026-07)
  - [三、内容缺口与优先级](#三内容缺口与优先级)
    - [3.1 主题级缺口](#31-主题级缺口)
    - [3.2 可执行交付物缺口](#32-可执行交付物缺口)
    - [3.3 形式化验证可执行性缺口](#33-形式化验证可执行性缺口)
  - [四、后续推进计划（2026-Q3 → 2027-Q4）](#四后续推进计划2026-q3--2027-q4)
    - [Phase 0 立即修复与交付物验证（2026-Q3 第 1-2 周）](#phase-0-立即修复与交付物验证2026-q3-第-1-2-周)
    - [Phase 1 形式化与可执行工具深化（2026-Q3 中 ~ 2026-Q4）](#phase-1-形式化与可执行工具深化2026-q3-中--2026-q4)
    - [Phase 2 垂直领域扩展（2027-Q1）](#phase-2-垂直领域扩展2027-q1)
    - [Phase 3 安全与供应链纵深（2027-Q2）](#phase-3-安全与供应链纵深2027-q2)
    - [Phase 4 AI 原生与前沿（2027-Q3）](#phase-4-ai-原生与前沿2027-q3)
    - [Phase 5 整合与输出（2027-Q4）](#phase-5-整合与输出2027-q4)
    - [Phase D 前沿跟踪持续更新（2026-Q3 起，持续）](#phase-d-前沿跟踪持续更新2026-q3-起持续)
  - [五、关键决策确认](#五关键决策确认)
    - [决策 1：目录结构统一策略](#决策-1目录结构统一策略)
    - [决策 2：形式化验证工具链投入](#决策-2形式化验证工具链投入)
    - [决策 3：可执行工具开发策略](#决策-3可执行工具开发策略)
    - [决策 4：前沿主题取舍](#决策-4前沿主题取舍)
    - [决策 5：国际对齐深度](#决策-5国际对齐深度)
    - [决策 6：工业 IoT 标准跟踪策略（新增）](#决策-6工业-iot-标准跟踪策略新增)
  - [六、风险登记册](#六风险登记册)
  - [七、验收标准与下一步](#七验收标准与下一步)
    - [7.1 总体验收标准](#71-总体验收标准)
    - [7.2 下一步行动](#72-下一步行动)
  - [概念定义](#概念定义)
  - [正向示例](#正向示例)
  - [反例/反模式](#反例反模式)
  - [权威来源](#权威来源)

---

## 一、执行摘要

### 1.1 项目当前状态

本项目已构建起一个**覆盖 13 个一级主题、约 290+ Markdown 文档、30+ 可执行脚本/工具、13+ 形式化规约**的软件架构复用知识体系。核心资产包括：

- **四层复用视角**：业务架构 → 应用架构 → 组件架构 → 功能架构。
- **跨层支撑**：治理、形式化验证、认知架构、价值量化、供应链安全、工业 IoT/OT-IT、AI 原生、新兴趋势。
- **公理-定理体系**：20+ 公理、35+ 定理、依赖关系图与批判边界。
- **国际标准对齐**：42+ 标准/框架的映射矩阵与权威来源索引。
- **可执行交付物**：COCOMO 计算器、FinOps 模板、成熟度评估 CLI、PIU 贝叶斯工具、AI 概率契约校准工具、供应链攻击树可视化、EU CRA 检查清单等。

### 1.2 本轮网络对齐的核心发现

2026 年 6–7 月，国际权威来源出现多处与本项目直接相关的变化：

1. **IEC 61508-3:2026 已实质性落地**：TÜV Rheinland 于 2026-06 宣布在德国等 CE 认可国家强制执行 IEC 61508-3:2026，SIL 2+ 验证记录与工具链审计成为强制要求。本项目工业功能安全章节仍以 Ed.2 为主，**需紧急更新**。
2. **OWASP MCP Top 10 / Agentic AI Top 10 发布**：2025 年底至 2026 年中，OWASP 先后发布 Agentic AI Top 10 与 MCP 专用 Top 10，Microsoft Agent Governance Toolkit（2026-04）亦开源。本项目 AI 原生安全治理需系统性对齐。
3. **MCP 生态进入 Linux Foundation Agentic AI Foundation（AAIF）**：2025-12-09 MCP 捐给 AAIF，2025-11-25 为当前稳定版，新增 Tasks、Icons、Elicitation URL mode、OAuth 增强。需全面替换旧引用并补充安全防御矩阵。
4. **A2A v1.0 已 GA**：Google Cloud Next 2026-04 发布 v1.0，Signed Agent Cards、多租户、AP2 支付协议进入稳定版；后续 v1.1/v1.2 在酝酿。需更新并补充 MCP-A2A 互补架构。
5. **WASI 0.3 preview 可用**：2026-02 发布，Wasmtime 37+ 支持原生 async（stream<T>/future<T>），但 WASI 1.0 仍瞄准 2026 末/2027 初。需更新 WASM 跨语言复用边界，并标注 preview 状态。
6. **SLSA 1.2 Multi-Track 已稳定**：Build/Source Track 已发布，Build Environment Track / Build Level 4 仍在开发。需补充 L4 分布式构建验证实践。
7. **NIST SSDF 1.2 即将定稿**：Initial Public Draft（SP 800-218r1）于 2025-12-17 发布，公众评议 2026-01-30 结束，最终版预计 2026 年 Q3 发布。需跟踪并同步。
8. **ArchiMate 4.0 正式发布**：The Open Group 2026-04-27 宣布发布，Document C260。本项目已对齐，需保持。
9. **SysML v2 / KerML 正式化**：OMG 已正式发布（2025），2026-03 已向 ISO 提交；数字孪生/AAS 章节可建立映射。
10. **GSF SCI for AI 已 ratified**：2026-Q1 发布，为 AI 系统碳强度测量提供 ISO 兼容方法。可持续软件章节需对齐。
11. **CNCF Platform Engineering Maturity Model**：五维度（Investment/Adoption/Interfaces/Operations/Measurement）仍是主流评估框架；2026 年数据显示 Measurement 是最大瓶颈。本项目 IDP 实践可深化五维度检查清单。

### 1.3 总体方向

本轮计划以“**补齐国际差距 + 激活可执行交付物 + 建立持续跟踪机制**”为核心，分 6 个阶段推进：

- **Phase 0（2026-Q3 第 1-2 周）**：立即修复一致性、验证已有工具、更新权威来源索引。
- **Phase 1（2026-Q3 中 ~ 2026-Q4）**：形式化验证可执行化、价值量化工具完善、应用架构基础子目录补全、AI 概率契约与 MCP 安全对齐。
- **Phase 2（2027-Q1）**：工业 IoT/OT-IT 纵深，IEC 61508 Ed.3 对齐，PIU/SEooC/边缘 AI/MCP Industrial AI 协议草案。
- **Phase 3（2027-Q2）**：供应链安全纵深，SLSA L4、OWASP MCP Top 10 防御矩阵、EU CRA 工具、NIST SSDF 1.2 定稿对齐。
- **Phase 4（2027-Q3）**：AI 原生与前沿，MCP/A2A 更新、Agentic Governance、WASI 0.3、GreenArch/SCI for AI、CP+形式化融合框架。
- **Phase 5（2027-Q4）**：全书整合、总矩阵 v3.0、交互式工具、在线发布、学术投稿。
- **Phase D（持续）**：月度事实核查、标准 RSS/会议跟踪。

---

## 二、国际权威来源对齐现状（2026-07）

> 以下信息基于 2026-07-06 网络权威来源核查。每个条目给出**官方/权威 URL**、**当前状态**、**本项目覆盖情况**与**建议行动**。

| 标准 / 框架 / 协议 | 权威来源 | 最新状态（2026-07） | 本项目覆盖 | 建议行动 |
|:---|:---|:---|:---|:---|
| **ISO/IEC/IEEE 42010:2022** | <https://www.iso.org/standard/74296.html> | 现行 | 深度映射 | 持续维护 |
| **ISO/IEC/IEEE DIS 42024** | <https://www.iso.org/standard/87510.html> | 草案；enquiry 2026-01-12 结束 | 已创建对齐文档 | 跟踪发布，补充术语对照 |
| **ISO/IEC/IEEE DIS 42042** | <https://www.iso.org/standard/87310.html> | 草案；stage 40.60，enquiry 2026-01-30 结束 | 已创建对齐文档 | 跟踪发布，补充参考架构要求 |
| **ISO/IEC 25010:2023** | <https://www.iso.org/standard/78175.html> | 已发布；Reusability 为 Maintainability 子特性；Modularity 独立；新增 Interaction capability/Flexibility/Safety | 已引用，未深入展开质量特性对复用决策的影响 | 补充 25010:2023 对 AI/复用组件的质量评估矩阵 |
| **ISO/IEC 25040:2024** | <https://www.iso.org/standard/83467.html> | 已发布；新增“获取或复用预开发产品”评估流程 | 未明确引用 | 新增 25040 评估流程与复用决策对照 |
| **ISO/IEC 26566:2026** | <https://www.iso.org/standard/81437.html> | 2026-05 发布 | 已引用 | 更新成熟度模型以反映正式版 |
| **ISO/IEC/IEEE 12207:2026** | <https://www.iso.org/standard/90219.html> | 2026-04-29 发布 | 已引用 | 更新与 IEEE 1517 的对照 |
| **ArchiMate 4.0** | <https://www.opengroup.org/archimate> | The Open Group 2026-04-27 正式发布（Document C260） | 已对齐 | 保持；必要时补充 Common Domain 变化 |
| **OMG RAS v2.2** | <https://www.omg.org/spec/RAS/2.2/PDF> | 已发布 | 已有章节 | 完善 Classification/Solution/Usage/Related Assets 映射 |
| **FAIR4RS v1.0** | <https://doi.org/10.15497/RDA00068> | 已发布 | 已有章节 | 深化与 SBOM、MCP Tool 注册表、AAS 子模型的映射 |
| **SysML v2 / KerML** | <https://www.omg.org/spec/SysML/> | OMG 正式发布 2025；2026-03 向 ISO 提交 | 已有章节 | 补充与 AAS/数字孪生的映射 |
| **SLSA 1.2** | <https://slsa.dev/spec/v1.2/> | Multi-Track（Build / Source / Attested Build Environments）；Build L4 开发中 | 已更新到 1.2 | 补充 Build Environment Track 与 L4 分布式构建实践 |
| **NIST SSDF 1.2** | <https://csrc.nist.gov/publications/detail/sp/800-218r1/draft> | Initial Public Draft 2025-12-17；公众评议 2026-01-30 结束；最终版临近 | 已标记为 IPD | 最终版发布后 2 周内更新 |
| **OWASP Top 10 for LLM Apps (2025)** | <https://owasp.org/www-project-top-ten-for-large-language-model-applications/> | 已发布 | 部分覆盖 | 整合到 AI 安全治理 |
| **OWASP Top 10 for Agentic Applications** | <https://owasp.org/www-project-agentic-ai/> | 2025-12 发布 | 未系统覆盖 | 新增 Agentic AI 安全映射 |
| **OWASP MCP Top 10** | 多家安全厂商/OWASP 社区 2026-06 | 2026 年 MCP 专用 Top 10 成型 | 未覆盖 | 新增 MCP 安全防御矩阵 |
| **Microsoft Agent Governance Toolkit** | <https://github.com/microsoft/agent-governance-toolkit> | 2026-04-02 开源；覆盖 OWASP Agentic Top 10；多语言 SDK | 未覆盖 | 新增 Agentic Governance 设计模板对齐 |
| **MCP 2025-11-25 / AAIF** | <https://modelcontextprotocol.io/specification/2025-11-25> | 当前稳定版；AAIF 2025-12-09 成立 | 已有深度解析 | 更新 Tasks/Icons/Elicitation/OAuth/MCP Apps；补充安全 |
| **A2A v1.0.0** | <https://a2a-protocol.org/latest/> | Cloud Next 2026-04 GA；Signed Agent Cards、AP2 | 已有深度解析 | 更新 v1.0 最终特性；跟踪 v1.1/v1.2 |
| **WASI 0.3 / Component Model** | <https://github.com/WebAssembly/WASI> | 2026-02 preview；Wasmtime 37+；原生 async；WASI 1.0 目标 2026末/2027初 | 已有章节 | 大幅更新 async/线程限制/.NET WASM 前瞻 |
| **CNCF Platform Engineering Maturity Model** | <https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/> | 五维度（Investment/Adoption/Interfaces/Operations/Measurement） | 已有成熟度模型 | 补充五维度逐条检查清单与 Backstage/Port/Cortex 对比 |
| **GSF SCI / SCI for AI** | <https://sci.greensoftware.foundation/> / <https://greensoftware.foundation/standards/sci-ai/> | SCI 已 ISO 21031:2024；SCI for AI 2026-Q1 ratified | 已有碳维度 | 对齐 SCI for AI，补充 AI 训练/推理碳强度度量 |
| **IEC 61508 Ed.3** | IEC/TC65 投票文档 65A/1231-1235 RVC | CDV 投票已完成；IEC 61508-3:2026 已被 TÜV 2026-06 强制采用 | 仍以 Ed.2 为主 | **紧急**：Ed.3 变化映射与更新 |
| **ISO 21448 Ed.2 (SOTIF)** | <https://www.iso.org/standard/93071.html> | AWI 已注册；多家来源称 2026 发布并扩展至 SAE L3-L5 | 未覆盖 | 可选补充到工业功能安全/自动驾驶 AI 复用 |
| **OPC UA FX 1.0** | <https://opcfoundation.org/about/opc-technologies/opc-ua/opc-ua-fx/> | Parts 80–84 已发布 | 已覆盖 | 跟踪 C2D/D2D 完善 |
| **IEC 63278-1 AAS** | <https://webstore.iec.ch/en/publication/65628> | 2023 已发布；Part 2 CDV 2026-08 投票 | 已映射 | 跟踪 Part 2 |

---

## 三、内容缺口与优先级

### 3.1 主题级缺口

| 主题 | 主要缺口 | 严重程度 | 优先级 |
|:---|:---|:---:|:---:|
| **01 元模型** | DIS 42024/42042 尚未定稿；25040:2024 未引用；25010:2023 AI 质量影响矩阵不足 | 🟡 中 | P1 |
| **03 应用架构** | 分层架构、微服务、Serverless、事件驱动基础子目录已创建但内容深度不均；IDP 实践需补全 Backstage/Port/Cortex | 🟡 中 | P1 |
| **04 组件架构** | WASM Component Model / WASI 0.3 async 内容待更新 | 🟡 中 | P1 |
| **05 功能架构** | MCP 2025-11-25 新特性与安全防御矩阵待补全；AI 概率契约校准工具需验证完整度 | 🟡 中 | P0 |
| **06 跨层治理** | CNCF 五维度评估检查清单缺失；FinOps Excel 带公式导出待验证 | 🟡 中 | P1 |
| **07 形式化验证** | TLA+/Alloy/Coq/Isabelle 自动化流水线未完全跑通；Kani/Prusti/Miri 可运行示例缺失 | 🔴 高 | P0 |
| **09 价值量化** | COCOMO AAM/SU/UNFM 完整参数支持待验证；SCI for AI 碳强度度量待补充 | 🟡 中 | P1 |
| **10 供应链安全** | OWASP MCP Top 10 / Agentic AI Top 10 未覆盖；SLSA L4 分布式构建空白；EU CRA 自动化 CLI 待验证 | 🟡 中 | P1 |
| **11 工业 IoT** | IEC 61508 Ed.3 未对齐；ISO 21448 SOTIF Ed.2 未覆盖；PIU 工具/SEooC 模板待完成 | 🔴 高 | P0 |
| **12 AI 原生** | Microsoft Agent Governance Toolkit、OWASP MCP Top 10 未覆盖；Agentic Governance 模板待启动 | 🟡 中 | P1 |
| **13 新兴趋势** | GreenArch/SCI for AI 内容待深化；RegTech Agentic 案例验证待启动 | 🟡 中 | P2 |
| **99 参考** | 权威来源索引需更新 v2.1；交互式复用决策工具需整合；Mermaid 可视化库需补全 | 🟡 中 | P1 |

### 3.2 可执行交付物缺口

| 交付物 | 当前状态 | 目标状态 | 优先级 |
|:---|:---|:---|:---:|
| 复用成熟度评估问卷 | CLI 已存在 | 交互式 Web/YAML + 雷达图 + CNCF 五维度 | P1 |
| COCOMO II 2026 计算器 | Python 已存在 | 完整 AAM/SU/UNFM + ROI + Streamlit/Excel | P1 |
| FinOps 跨层成本分摊 | Python 已存在 | Excel 带公式 + 四级分摊示例 | P1 |
| AI 概率契约校准工具 | Python 已存在 | 支持温度/Top-p/模型漂移 + 可视化 | P0 |
| PIU 贝叶斯统计验证工具 | 规划中 | Python 原型 + 可视化 | P1 |
| 供应链攻击树交互可视化 | 静态 Markdown | 交互式 HTML/Streamlit | P1 |
| EU CRA 合规检查清单 CLI | 规划中 | JSON + CLI + 差距报告 | P1 |
| 术语查询脚本 | Python 已存在 | 跨标准别名映射 + 版本提示 | P1 |
| 交互式复用决策工具 | v2 已存在 | 整合为统一 Web/CLI，支持 6 阶段流程 | P2 |

### 3.3 形式化验证可执行性缺口

| 工具 | 当前状态 | 目标状态 | 优先级 |
|:---|:---|:---|:---:|
| TLA+ Toolbox / TLC | 未配置运行环境 | Docker 化 + 至少 1 个案例自动跑通 | P0 |
| Alloy Analyzer | 未配置运行环境 | Docker 化 + ISA-95/跨层映射案例可运行 | P0 |
| Coq / Isabelle | 仅教学示例 | 2+ 安全关键组件证明 + 可执行脚本 | P0 |
| Rust Kani / Prusti / Miri | 仅文档 | 3+ 可运行示例 + CI 脚本 | P1 |


## 四、后续推进计划（2026-Q3 → 2027-Q4）

> **编排原则**：
>
> 1. 优先级以“填补国际差距 + 可执行交付物 + 安全关键领域”为核心。
> 2. 每个任务明确列出对齐的国际权威来源与可验证验收标准。
> 3. 工具开发统一采用 **Python CLI + Streamlit** 快速原型策略。

---

### Phase 0 立即修复与交付物验证（2026-Q3 第 1-2 周）

**目标**：修复一致性、验证已有工具、更新权威来源索引，为后续阶段扫清基础。

| 任务 ID | 任务 | 交付物 | 对齐来源 / 验收标准 | 优先级 |
|:---|:---|:---|:---|:---:|
| P0-T1 | 目录结构一致性校对 | `struct/README.md` + `MASTER_PLAN.md` 目录树 | 与实际 `struct/` 目录 100% 一致（允许新增/重命名有说明） | P0 |
| P0-T2 | 已有可执行工具运行验证 | 各工具目录下 `requirements.txt` + 运行截图/日志 | cocomo、finops、maturity、terminology、calibration、piu、attack-tree、eu-cra-checklist 至少可本地运行 | P0 |
| P0-T3 | 权威来源索引 v2.1 更新 | `struct/99-reference/standards-index/authoritative-sources-v2.md` | 新增 IEC 61508-3:2026、ISO 21448 Ed.2、OWASP MCP Top 10、MS Agent Governance Toolkit、SCI for AI 等条目，含 URL 与核查日期 | P0 |
| P0-T4 | CHANGELOG 更新 | `struct/99-reference/CHANGELOG.md` | 记录 2026-06 至 07 关键外部变化（IEC 61508 Ed.3、OWASP MCP Top 10、MS Agent Governance Toolkit、A2A v1.0 GA 等） | P1 |
| P0-T5 | 形式化验证环境搭建（或文档化确认） | `99-reference/tools/formal-verification-env/` + `verify-all.sh` | 若选决策 2-A：Docker 化 TLA+/Alloy/Coq 至少跑通 1 个案例；若选 2-A'：完成现有规约内容校对清单 | P0 |
| P0-T6 | 更新 01/07/11 各主题 roadmap 状态 | 各 `plans-tasks/roadmap.md` | 已交付文件标记 `[x]`，路径与实际文件一致 | P0 |

---

### Phase 1 形式化与可执行工具深化（2026-Q3 中 ~ 2026-Q4）

**目标**：将形式化验证、价值量化、AI 功能契约从“理论文档”转化为“可运行方法论 + 工具”。

| 任务 ID | 任务 | 交付物 | 对齐来源 | 验收标准 |
|:---|:---|:---|:---|:---|
| P1-T1 | Coq/Isabelle 高安全等级组件验证案例 | `07-formal-verification/03-coq-isabelle/` + `.v`/`.thy` | Coq (Inria)、Isabelle/HOL (TU Munich)、seL4/CompCert | 2+ 案例含证明纲要；Docker/CI 可运行 |
| P1-T2 | Rust 形式化验证工具链实践 | `07-formal-verification/04-rust-type-system/toolchain-practice.md` + 示例 | RustBelt、Kani (AWS)、Prusti (ETH)、Miri | 3+ 可运行示例覆盖内存安全/并发/unsafe；CI 通过 |
| P1-T3 | Alloy 跨层映射 + ISA-95 层次约束 | `07-formal-verification/02-alloy/cross-layer-mapping.md` + `.als` | Alloy Tools (MIT)、ISO/IEC 42010、ISA-95 | ISA-95 五层约束加入；Alloy Analyzer 可运行 |
| P1-T4 | COCOMO II 2026 可执行计算器 | `09-value-quantification/tools/cocomo-calculator.py` + Excel | USC COCOMO II Manual (Boehm) | 支持 AAM/SU/UNFM 参数输入与 ROI 输出；Streamlit 可选 |
| P1-T5 | FinOps 跨层成本分摊 Python/Excel 模板 | `06-cross-layer-governance/04-finops-cost/templates/` | FinOps Foundation | Excel 带公式导出；含四级分摊公式和示例数据 |
| P1-T6 | 复用成熟度可执行评估问卷 | `06-cross-layer-governance/03-maturity-models/assessment-tool/` | ISO/IEC 26566:2026、NASA RRL、**CNCF Maturity Model 五维度** | YAML/JSON + Python CLI；生成雷达图 + 报告；可选 CNCF 五维度评估 |
| P1-T7 | AI 功能概率契约校准工具原型 | `12-ai-native-reuse/05-probabilistic-contracts/calibration-tool.py` | Conformal Prediction (Vovk et al.)、OWASP MCP Top 10 | 支持温度/Top-p/模型版本漂移边界计算；可视化输出 |
| P1-T8 | 术语查询脚本完善 | `99-reference/tools/terminology-query.py` | IREB CPRE Glossary、ISO/IEC 42010/42024 | 支持跨标准术语搜索、别名映射、版本提示 |
| P1-T9 | OMG RAS v2.2 对齐章节 | `01-meta-model-standards/07-omg-ras/ras-alignment.md` | OMG RAS v2.2 | 覆盖 Classification/Solution/Usage/Related Assets |
| P1-T10 | ISO 25010:2023 质量特性对复用决策的影响矩阵 | `01-meta-model-standards/01-iso-420xx-family/iso-25010-2023-ai-quality.md` | ISO/IEC 25010:2023 | 覆盖 AI 生成代码/组件的复用质量评估 |
| P1-T11 | Backstage / Port / Cortex IDP 复用实践 | `03-application-architecture-reuse/11-idp-practices/backstage-port-cortex.md` | CNCF Platform Engineering Maturity Model、Backstage.io | 三家平台对比 + Golden Path 模板 + 选型决策树 |
| P1-T12 | ISO 25040:2024 评估流程与复用决策对照 | `01-meta-model-standards/01-iso-420xx-family/iso-25040-2024-evaluation.md` | ISO/IEC 25040:2024 | 覆盖“获取或复用预开发产品”评估流程 |

---

### Phase 2 垂直领域扩展（2027-Q1）

**目标**：深化工业 IoT/OT-IT 融合，补齐功能安全、边缘 AI、PIU 工具；对齐 IEC 61508 Ed.3。

| 任务 ID | 任务 | 交付物 | 对齐来源 | 验收标准 |
|:---|:---|:---|:---|:---|
| P2-T1 | **IEC 61508 Ed.3 变化映射与章节更新** | `11-industrial-iot-otit/06-functional-safety/iec-61508/iec-61508-ed3-alignment.md` | IEC 61508-3:2026 | 列出 Ed.3 关键变化（工具资质、OO 软件、AI/ML、结构化分析）并更新现有章节 |
| P2-T2 | IEC 61508 Proven-in-Use (PIU) 贝叶斯统计验证工具 | `11-industrial-iot-otit/06-functional-safety/piu-bayesian-tool.py` | IEC 61508-3-1:2016 / Ed.3 | 支持失效数据输入 → SIL 可信度输出；含可视化 |
| P2-T3 | ISO 26262 SEooC 复用流程模板 | `11-industrial-iot-otit/06-functional-safety/iso26262-seooc-template.md` | ISO 26262-8 Clause 12 | 含安全手册、假设、验证清单、复用决策树 |
| P2-T4 | 工业边缘 AI 模型部署规范 | `11-industrial-iot-otit/07-edge-ai/model-deployment-spec.md` + ONNX Runtime 示例 | TinyML、ONNX、IEC 62443 | 覆盖 TFLite/ONNX 部署流程；含性能基准 |
| P2-T5 | MCP for Industrial AI 协议草案 | `11-industrial-iot-otit/07-edge-ai/mcp-industrial-ai-draft.md` | MCP 2025-11-25、OPC UA FX | 定义工业场景 Tools/Resources 规范；与 AAS 映射 |
| P2-T6 | AAS 到 OPC UA NodeSet 完整映射规范确认/补全 | `11-industrial-iot-otit/05-digital-twin-aas/aas-opcua-nodeset-mapping.md` | IDTA AAS、OPC Foundation、IEC 63278-1:2023 | XML/JSON 示例 + 映射表 + FX ConnectionManager 集成 |
| P2-T7 | FAIR4RS 原则与软件复用对照 | `01-meta-model-standards/08-fair4rs/fair4rs-alignment.md` | FAIR4RS (2022; ARDC) | 与 SBOM、MCP Tool 注册表、AAS 子模型的映射 |
| P2-T8 | ISO 21448 SOTIF Ed.2 对齐（可选） | `11-industrial-iot-otit/06-functional-safety/iso21448-sotif-alignment.md` | ISO 21448:2026 | 分布偏移验证与 AI 功能复用概率契约关联 |

---

### Phase 3 安全与供应链纵深（2027-Q2）

**目标**：构建 SLSA L4、SBOM 深度应用、MCP/Agentic 安全防御的纵深防御体系；对齐 NIST SSDF 1.2 最终版。

| 任务 ID | 任务 | 交付物 | 对齐来源 | 验收标准 |
|:---|:---|:---|:---|:---|
| P3-T1 | SLSA 1.2 Multi-Track 深度解析（Build/Source/Attested Build Environments） | `10-supply-chain-security/01-slsa-framework/slsa-1-2-multi-track.md` | SLSA.dev (OpenSSF) | 三轨道 × L1-L3 要求矩阵；与复用决策矩阵联动 |
| P3-T2 | SLSA L4 分布式构建验证实践 | `10-supply-chain-security/01-slsa-framework/slsa-l4-distributed-builds.md` + sigstore/cosign 示例 | OpenSSF、Sigstore | 多签名 + 可复现构建 POC；GitHub Actions 流水线可运行 |
| P3-T3 | 供应链攻击树交互式可视化 | `10-supply-chain-security/03-attack-vectors/attack-tree-interactive.html` / `.py` | MITRE ATT&CK、OWASP SCVS | 支持点击展开/防御矩阵联动；Streamlit/Dash 可选 |
| P3-T4 | NIST SSDF 1.2 最终版对齐 | `10-supply-chain-security/12-nist-ssdf-update/nist-ssdf-1-2-alignment.md` | NIST SP 800-218 Rev. 1 Final | 同步最终版内容；与 SLSA 1.2 的映射 |
| P3-T5 | EU CRA 合规检查清单工具 | `10-supply-chain-security/06-case-studies/eu-cra-checklist.json` + CLI | Regulation (EU) 2024/2847 | 自动评估合规项；生成差距报告 |
| P3-T6 | OWASP MCP Top 10 / Agentic AI Top 10 防御矩阵 | `12-ai-native-reuse/06-ai-governance/owasp-mcp-agentic-defense-matrix.md` | OWASP MCP Top 10、OWASP Agentic AI Top 10 | 10 类风险 × 防御控制 × 工具映射 |
| P3-T7 | IEEE 1517 复用过程与 ISO 12207:2026 对照 | `01-meta-model-standards/01-iso-420xx-family/ieee-1517-reuse-processes.md` | IEEE 1517-2010; ISO/IEC/IEEE 12207:2026 | 复用活动细化；2017 版仅作历史对照 |
| P3-T8 | ISO/IEC 33000 (SPICE) 与复用成熟度映射（可选） | `06-cross-layer-governance/03-maturity-models/spice-rcmm-mapping.md` | ISO/IEC 33000 系列 | 六级过程能力与 RCMM/RiSE 的映射 |

---

### Phase 4 AI 原生与前沿（2027-Q3）

**目标**：将 AI/LLM 功能复用、Agentic Infrastructure、WASM、平台工程、可持续架构提升到工程化水平。

| 任务 ID | 任务 | 交付物 | 对齐来源 | 验收标准 |
|:---|:---|:---|:---|:---|
| P4-T1 | MCP 2025-11-25 全面更新（替换旧引用） | `12-ai-native-reuse/01-mcp-protocol/mcp-2025-11-25-deep-dive.md` 更新 | modelcontextprotocol.io/specification/2025-11-25、AAIF | 覆盖 Tasks、Icons、Elicitation、OAuth 增量、MCP Apps |
| P4-T2 | A2A v1.0+ 更新与 MCP-A2A 互补架构 | `12-ai-native-reuse/02-a2a-protocol/a2a-v1-update.md` | A2A v1.0、Linux Foundation | 更新 Signed Agent Cards、AP2、MCP-A2A 协同图 |
| P4-T3 | Agentic Governance 组织设计模板 | `12-ai-native-reuse/03-agentic-infrastructure/agentic-governance-template.md` | Google A2A、AAIF、**Microsoft Agent Governance Toolkit** | 含 Agent RBAC、Golden Path、模型路由、审计追踪 |
| P4-T4 | MCP 安全网关设计（对齐 OWASP MCP Top 10） | `12-ai-native-reuse/06-ai-governance/mcp-security-gateway-design.md` | OWASP MCP Top 10 | 工具描述签名、沙箱、最小权限、审计日志设计 |
| P4-T5 | WASM Component Model + WASI 0.3 复用边界更新 | `13-emerging-trends/03-webassembly-components/wasm-wasi-03-boundaries.md` | Bytecode Alliance、Wasmtime 37+、WASI 1.0 roadmap | 覆盖 stream/future、async、线程限制、.NET WASM runtime 前瞻 |
| P4-T6 | CNCF Platform Engineering 五维度评估检查清单 | `13-emerging-trends/01-platform-engineering/platform-maturity-model.md` 扩展 | CNCF TAG App Delivery | 五维度（Investment/Adoption/Interfaces/Operations/Measurement）逐条映射 |
| P4-T7 | Conformal Prediction + 形式化验证融合框架 | `12-ai-native-reuse/07-conformal-prediction/cp-formal-verification.md` | Vovk et al.、Cherian & Candès、Angelopoulos & Bates | 提出“AI 生成 + CP 筛选 + 定理证明”三层保证（研究探索方向） |
| P4-T8 | 可持续软件架构 / GreenArch 初探 | `13-emerging-trends/07-green-software/green-architecture-reuse.md` | GreenArch 2026、GSF SCI / SCI for AI | 碳感知架构复用度量；与 FinOps 成本模型关联 |
| P4-T9 | RegTech Agentic 架构案例验证 | `13-emerging-trends/06-regtech-ai/regtech-case-validation.md` | FCA/SEC/EU regulators | 1+ 真实监管场景 POC 设计 |

---

### Phase 5 整合与输出（2027-Q4）

**目标**：将分散知识模块整合为可交付产品。

| 任务 ID | 任务 | 交付物 | 验收标准 |
|:---|:---|:---|:---|
| P5-T1 | 《软件工程架构复用视角》全书框架定稿 | `99-reference/book-outline.md` 更新 | 12 章 + 附录，每章对应一级主题；预计 326,000 字 |
| P5-T2 | 国际标准对齐总矩阵 v3.0 | `99-reference/standards-index/master-alignment-matrix.md` 更新 | 覆盖 45+ 标准 × 5 复用层次 |
| P5-T3 | 公理-定理推理树完整版 | `99-reference/glossary/axiom-theorem-tree.md` 更新 | 20+ 公理、40+ 定理 |
| P5-T4 | 交互式复用决策工具（Web/CLI） | `99-reference/tools/reuse-decision-tool/` | 支持 6 阶段决策流程；Streamlit 优先 |
| P5-T5 | Mermaid 可视化库补全 | `99-reference/visualizations/` | 覆盖 13 主题 + GreenArch/MCP 安全 |
| P5-T6 | 项目官网/GitBook 发布准备 | `99-reference/website/` | 在线可浏览知识体系 |
| P5-T7 | 国际会议投稿/白皮书（ICSA/ECSA/GreenArch） | `99-reference/publications/` | 至少 1 份白皮书/短篇论文初稿 |

---

### Phase D 前沿跟踪持续更新（2026-Q3 起，持续）

| 任务 ID | 任务 | 交付物 | 跟踪对象 | 优先级 |
|:---|:---|:---|:---|:---:|
| D-01 | 月度事实核查 | `99-reference/templates/fact-check-checklist.md` | 外部引用 5-10 条/月 | P1 |
| D-02 | AWI 42030 / DIS 42024/42042 正式版对齐 | `01-meta-model-standards/01-iso-420xx-family/` | ISO/IEC/IEEE | P1 |
| D-03 | MCP / A2A 后续版本更新 | `12-ai-native-reuse/` | Linux Foundation AAIF | P2 |
| D-04 | WASI 1.0 正式发布对齐 | `13-emerging-trends/03-webassembly-components/` | W3C / Bytecode Alliance | P2 |
| D-05 | IEC 61508 Ed.3 / ISO 21448 Ed.2 发布跟踪 | `11-industrial-iot-otit/` | IEC / ISO | P1 |
| D-06 | ICSA/ECSA/SPLC/GreenArch 会议主题年度映射 | `99-reference/external-links/conference-theme-index.md` | IEEE/ACM/会议官网 | P3 |
| D-07 | NIST SSDF 1.2 最终版发布跟踪 | `10-supply-chain-security/12-nist-ssdf-update/` | NIST CSRC | P1 |


## 五、关键决策确认

在启动 Phase 0 之前，请您确认以下决策（与前期计划保持一致，部分选项已根据网络对齐更新）：

### 决策 1：目录结构统一策略

> **选项 A（推荐）**: 重构 `struct/README.md` 和 `MASTER_PLAN.md` 中的目录树，使其 100% 匹配实际 `struct/` 目录，删除/合并规划中未实现的子目录。
> **选项 B**: 保留现有规划树，为缺失子目录创建占位符（README + TODO），后续按规划补齐。
> **选项 C**: 不调整顶层规划，仅在 README 中增加“实际目录与规划存在差异”的免责声明。

### 决策 2：形式化验证工具链投入

> **选项 A（推荐）**: 建立 Docker 化的 TLA+ Toolbox + Alloy Analyzer + Coq (Rocq) / Isabelle 环境，要求所有新增形式化规约必须通过自动化验证。
> **选项 B**: 维持当前“人工语法审查”模式，仅在 Phase 5 前统一跑一遍工具。
> **选项 C**: 只对高优先级规约（MCP/A2A/PLCopen）跑工具，其余保持文档级。
> **选项 A'（替代）**: 若资源受限，可先进行内容梳理与校对（不搭建运行环境），将自动化验证延期至 2027-Q1 后。

### 决策 3：可执行工具开发策略

> **选项 A（推荐）**: 优先用 Python CLI + Streamlit 开发所有工具原型（COCOMO 计算器、FinOps 模板、成熟度问卷、PIU 工具），保持最低可用（MVP）。
> **选项 B**: 投资一个统一的 Web 平台（如 Docusaurus + React）承载所有交互式工具。
> **选项 C**: 仅提供 Excel + Markdown 模板，不开发代码原型。

### 决策 4：前沿主题取舍

> **选项 A（推荐）**: 2027 年重点补齐 **MCP/Agentic AI 安全（OWASP MCP Top 10 + MS Agent Governance Toolkit）**、**WASI 0.3**、**Agentic Governance**、**GreenArch/SCI for AI**、**CP + 形式化验证融合**；**暂缓量子计算和通用边缘计算架构**。
> **选项 B**: 按早期 MASTER_PLAN 原规划，恢复 `quantum-computing` 和 `sustainable-software` 子目录。
> **选项 C**: 仅维护现有 13 个主题，不扩展新前沿方向。

### 决策 5：国际对齐深度

> **选项 A（推荐）**: 每篇新增/更新文档必须明确列出 1-3 个国际权威来源 URL，并在 `99-reference/external-links/authoritative-sources.md` 中登记；建立标准 RSS/邮件列表监控机制（ISO/OMG/IEEE/IEC/OpenSSF/Bytecode Alliance）。
> **选项 B**: 保持当前风格，在 README 中统一列出权威来源，不要求每文档标注。
> **选项 C**: 仅在关键标准文档中标注来源，日常内容不强制。

### 决策 6：工业 IoT 标准跟踪策略（新增）

> **选项 A（推荐）**: 建立 IEC 61508 Ed.3 和 ISO 21448 Ed.2 的跟踪通道，一旦发布立即启动差距分析，4 周内更新相关章节。
> **选项 B**: 等待标准正式发布后再评估是否需要更新。
> **选项 C**: 不跟踪，保持现有 Ed.2 内容。

---

## 六、风险登记册

| 风险 ID | 风险描述 | 影响 | 缓解措施 | 状态 |
|:---|:---|:---|:---|:---:|
| R1 | IEC 61508 Ed.3 / ISO 21448 Ed.2 / WASI 1.0 / SLSA Build L4 在计划期内发布新版本 | 已写内容需返工 | 建立标准 RSS/邮件列表监控；文档中标注版本和勘误；CHANGELOG 及时更新 | 🟡 监控中 |
| R2 | TLA+/Alloy/Coq 工具链环境搭建复杂 | Phase 1 延迟 | 优先 Docker 化验证环境；分阶段从人工→自动；仅对关键规约强制验证 | 🟡 监控中 |
| R3 | 工业 IoT 领域标准（OPC UA FX、IEC 63278）获取成本高 | 内容权威性受限 | 优先使用公开规范摘要、IDTA 模板、厂商白皮书、学术论文；必要时购买标准 PDF | 🟢 已缓解 |
| R4 | 可执行工具开发工作量大 | Phase 1/2 范围膨胀 | 用 Python CLI + Streamlit 快速原型，避免重前端；定义明确的 MVP 边界 | 🟡 监控中 |
| R5 | 目录规划与实际结构长期不一致 | 维护成本增加 | Phase 0 彻底重构 README；后续严格执行变更日志；禁止无计划新增目录 | 🟡 监控中 |
| R6 | AI 领域发展迅速，MCP/A2A/Agentic 内容易过期 | 前沿章节准确性下降 | 按季度审查 12-ai-native-reuse；建立外部链接健康检查；关注 AAIF 动态 | 🟡 监控中 |
| R7 | MCP 生态质量参差不齐，低质量 Server 可能误导读者 | 推荐资产可信度下降 | 建立 MCP Server 评估维度（安全/实用/维护/独特性），仅推荐高分工具 | 🟡 新增风险 |
| R8 | WASI 0.3 仍为 preview，WASI 1.0 尚未发布 | WASM 跨语言复用内容可能因标准变更而返工 | 明确标注 WASI 0.3 preview 状态；跟踪 Bytecode Alliance roadmap；WASI 1.0 发布后 2 周内更新 | 🟡 新增风险 |
| R9 | OWASP MCP Top 10 / MS Agent Governance Toolkit 等新兴安全框架仍在快速迭代 | AI 安全防御矩阵可能过时 | 标注版本号；与官方仓库保持同步；每季度审查 | 🟡 新增风险 |

---

## 七、验收标准与下一步

### 7.1 总体验收标准

1. **文档可审查**：所有新增/更新 Markdown 文档均包含 1-3 个国际权威来源 URL 与核查日期。
2. **工具可运行**：Phase 0 列出的已有工具可在本地或 Docker 环境中成功运行；Phase 1/2/3 新增工具提供 `requirements.txt` 或 `Dockerfile` 及使用说明。
3. **标准可追踪**：`authoritative-sources-v2.md` 与 `master-alignment-matrix.md` 在 2026-09-30 前更新至 v2.1/v3.0 版本。
4. **形式化可验证**：若选择决策 2-A，至少 TLA+、Alloy、Coq/Isabelle 各有一个案例在 CI 中通过；若选择 2-A'，至少完成现有规约的内容校对清单。
5. **工业安全章节无重大过时**：IEC 61508 Ed.3 关键变化在 2026-Q4 前映射完成。

### 7.2 下一步行动

1. 请您审阅本计划与 6 项关键决策，回复选项编号或提出修改意见。
2. 确认后，我将立即启动 **Phase 0**：
   - 更新 `struct/README.md` 目录一致性；
   - 运行验证已有可执行工具；
   - 更新 `authoritative-sources-v2.md` 与 `CHANGELOG.md`；
   - 根据决策 2 的结果，搭建或文档化形式化验证环境。
3. 每完成一个 Phase，我将提交进度更新并请您验收。

---

> **文件位置**: `struct/SUBSEQUENT_PLAN_2026_NETWORK_ALIGNED_v2.md`
> **最后更新**: 2026-07-06
> **前置参考**: `struct/SUBSEQUENT_PLAN_2026.md`（2026-06-10）、`struct/MASTER_PLAN_2026_NETWORK_ALIGNED.md`（2026-06-07）


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
> - ISO/IEC/IEEE 42010:2022. *Systems and software engineering — Architecture description*. <https://www.iso.org/standard/74296.html>
> - ISO/IEC/IEEE 15288:2023. *Systems and software engineering — System life cycle processes*. <https://www.iso.org/standard/81702.html>
> - ISO/IEC/IEEE 12207:2017. *Systems and software engineering — Software life cycle processes*. <https://www.iso.org/standard/63712.html>
> - Project Management Institute. *PMBOK® Guide — Seventh Edition*. <https://www.pmi.org/pmbok-guide-standards/foundational/pmbok>
>
> **核查日期**: 2026-07-07
