# 《软件工程架构复用视角》网络权威内容全面对齐报告

> **报告日期**: 2026-06-10
> **分析范围**: 项目 13 个一级主题 + 99-reference 参考层
> **对齐基准**: ISO/IEC/IEEE 420xx 族谱、TOGAF Standard 10、SLSA 1.2、MCP/A2A、SWEBOK V4、CNCF、IEC/ISA 工业标准族、OpenSSF 安全框架、学术前沿（ICSA/ECSA/CP）
> **分析维度**: 主题覆盖对称差、标准版本准确性、视角差异、内容深度对比、后续补全计划

---

## 目录

- [《软件工程架构复用视角》网络权威内容全面对齐报告](#软件工程架构复用视角网络权威内容全面对齐报告)
  - [目录](#目录)
  - [执行摘要](#执行摘要)
  - [一、当前项目主题子主题全盘点](#一当前项目主题子主题全盘点)
  - [二、网络权威内容全景](#二网络权威内容全景)
    - [2.1 国际标准组织最新状态](#21-国际标准组织最新状态)
    - [2.2 企业架构框架生态](#22-企业架构框架生态)
    - [2.3 软件供应链安全权威](#23-软件供应链安全权威)
    - [2.4 AI 原生协议生态](#24-ai-原生协议生态)
    - [2.5 平台工程成熟度](#25-平台工程成熟度)
    - [2.6 学术与会议前沿](#26-学术与会议前沿)
  - [三、对称差分析：项目 ↔ 权威内容](#三对称差分析项目--权威内容)
    - [3.1 项目独有（权威未系统覆盖）](#31-项目独有权威未系统覆盖)
    - [3.2 权威强调但项目缺失/不足](#32-权威强调但项目缺失不足)
    - [3.3 双方均覆盖但视角差异](#33-双方均覆盖但视角差异)
  - [四、不同视角与相关内容对齐](#四不同视角与相关内容对齐)
    - [视角 1：企业架构本体论（Zachman / GERAM）](#视角-1企业架构本体论zachman--geram)
    - [视角 2：国防/使命工程（DoDAF / UAF 1.3 / NAF）](#视角-2国防使命工程dodaf--uaf-13--naf)
    - [视角 3：过程评估与合规（SPICE / ISO 12207:2026 / EU CRA）](#视角-3过程评估与合规spice--iso-122072026--eu-cra)
    - [视角 4：金融垂直架构（BIAN / TMForum）](#视角-4金融垂直架构bian--tmforum)
    - [视角 5：可持续架构（GreenArch / Green Software Foundation）](#视角-5可持续架构greenarch--green-software-foundation)
  - [五、后续计划与任务（待确认）](#五后续计划与任务待确认)
    - [Phase A 立即修复（2026-06 第 2-3 周）](#phase-a-立即修复2026-06-第-2-3-周)
    - [Phase B 补全深化（2026-Q3 剩余）](#phase-b-补全深化2026-q3-剩余)
    - [Phase C 扩展对齐（2026-Q4 → 2027-Q1）](#phase-c-扩展对齐2026-q4--2027-q1)
    - [Phase D 前沿跟踪（2027-Q2 → 2027-Q4）](#phase-d-前沿跟踪2027-q2--2027-q4)
  - [六、需要您确认的关键决策](#六需要您确认的关键决策)
    - [决策 1：是否立即执行 Phase A 的 7 项任务？](#决策-1是否立即执行-phase-a-的-7-项任务)
    - [决策 2：是否接受 Phase B 的 12 项任务？](#决策-2是否接受-phase-b-的-12-项任务)
    - [决策 3：Phase C 的 8 项任务优先级如何排序？](#决策-3phase-c-的-8-项任务优先级如何排序)
    - [决策 4：前沿主题取舍策略](#决策-4前沿主题取舍策略)
    - [决策 5：事实核查机制的正式化](#决策-5事实核查机制的正式化)

---

## 执行摘要

本项目（约 214 个 Markdown 文件、18 个 Python 工具、~50 万字）在**软件架构复用**领域的知识广度已处于行业前沿，尤其在**工业 IoT/OT-IT 融合**、**AI 原生协议（MCP/A2A）**、**形式化验证文档深度**三方面具有独创价值。

**经与网络权威内容全面对齐，发现：**

| 对齐状态 | 数量 | 说明 |
|:---|:---:|:---|
| ✅ 深度对齐 | ~18 项 | ISO 42010/42020/42030、TOGAF 10、SLSA 1.0-1.2、MCP 2025-11-25、A2A、ISA-95、IEC 61508 等 |
| ⚠️ 版本/状态需更新 | ~6 项 | AWI 42030（修订中）、ISO 12207:2026（刚发布）、ISO 25040:2024（未深入）、ArchiMate 4.0（勘误中）等 |
| ❌ 缺失或严重不足 | ~12 项 | DoDAF/NAF/UAF、BIAN、ISO 33000 SPICE、GERAM、GreenArch、EU CRA、OWASP SCVS、数字孪生通用架构等 |
| 🎯 项目独创贡献 | ~5 项 | 四层复用公理-定理体系、跨层治理决策矩阵、认知架构+价值量化融合、工业 AI MCP 协议草案、概率契约框架 |

**核心结论**：项目的"深度"和"独创性"已超越大多数同类知识产品，但"广度"上存在系统性缺口——特别是在**国防/金融垂直架构框架**、**过程评估标准（SPICE）**、**可持续软件架构**、**法规合规（EU CRA）**四个方向。

---

## 一、当前项目主题子主题全盘点

```text
软件工程架构复用视角（13 个一级主题，~60 个二级主题）
│
├── 01 元模型与标准对齐（8 个子主题，20 个文件）
│   ├── 01-iso-420xx-family（42010/42020/42030/DIS 42024/DIS 42042/25010/1517）
│   ├── 02-togaf-10-alignment（ABB/SBB/Enterprise Continuum 映射）
│   ├── 03-iso-26550-ple（领域工程+应用工程双轨）
│   ├── 04-archimate-4（3.2/4.0 ISO 映射，⚠️ 4.0 勘误中）
│   ├── 05-swebok-v4（知识领域对齐）
│   ├── 06-formal-axioms（15 公理+17 定理+依赖图+批判边界）
│   ├── 07-omg-ras（RAS v2.2 对齐）
│   └── 08-fair4rs（FAIR4RS 原则对照）
│
├── 02 业务架构复用（4 个子主题，7 个文件）
│   ├── 02-business-capability（FEA BRM + TOGAF Capability Map）
│   ├── 03-value-stream（价值流组合与编排）
│   ├── 06-bpmn-dmn（可执行案例+编排复用）
│   └── case-studies（行业垂直案例）
│
├── 03 应用架构复用（10 个子主题，18 个文件）
│   ├── 01-layered-architecture（⚠️ 仅 README，内容薄弱）
│   ├── 02-microservices（⚠️ 仅 README，内容薄弱）
│   ├── 03-app-service / 03-serverless（⚠️ 内容单薄）
│   ├── 04-data-architecture（Data Mesh + 数据产品复用）
│   ├── 04-event-driven（⚠️ 仅 README）
│   ├── 05-cloud-native-patterns（复用性矩阵 2026，最充实）
│   ├── 06-service-mesh（Istio/Envoy/Cilium 通信模式）
│   ├── 07-eda-cqrs（事件溯源+ CQRS 模式）
│   ├── 07-tosca-dmn-platform（TOSCA v2.0 + DMN 1.6）
│   └── 08-idp-practices（Backstage/Port/Cortex，⚠️ 待深化）
│
├── 04 组件架构复用（3 个子主题，7 个文件）
│   ├── 04-design-patterns（接口设计模式）
│   ├── 06-cloud-native-networking（Gateway API v1.5 + Gamma）
│   └── 07-language-ecosystems（6 大语言生态对比矩阵 2026）
│
├── 05 功能架构复用（4 个子主题，6 个文件）
│   ├── 04-workflow-orchestration（Temporal 复用模式）
│   ├── 05-ai-llm-functions（LLM 功能复用模式）
│   ├── 06-mcp-a2a-protocols（协议分析+PoC）
│   └── decision-tree-granularity-cost-roi（粒度-成本-收益决策树）
│
├── 06 跨层复用治理（5 个子主题，16 个文件）
│   ├── 01-process-governance（跨层治理框架）
│   ├── 03-maturity-models（RiSE/RCMM/NASA RRL + 评估 CLI）
│   ├── 04-finops-cost（成本分摊模板+Python/Excel 工具）
│   ├── 05-metrics-kpi（四级度量指标体系）
│   └── 06-up-downgrade-matrix（升级/降级决策矩阵）
│
├── 07 形式化验证（7 个子主题，41 个文件）
│   ├── 01-tla-plus（6 个案例：支付/MCP/A2A/OPC UA FX/任务生命周期）
│   ├── 02-alloy（4 个模型：组件依赖/MCP 工具图/跨层映射/ISA-95）
│   ├── 03-coq-isabelle（教学示例：排序/计数器/Turnstile）
│   ├── 04-rust-type-system（所有权/Polonius/Cargo SAT/unsafe 验证）
│   ├── 05-spark-ada（飞行控制契约+DO-333）
│   ├── 06-b-method（铁路信号精化链）
│   └── 08-comparative-matrices（工具×层次×成本矩阵）
│
├── 08 认知架构（4 个子主题，7 个文件）
│   ├── 01-act-r-model（模式匹配与复用识别）
│   ├── 02-bdi-model（信念-愿望-意图与复用决策）
│   ├── 03-cognitive-load-theory（NASA-TLX 适配量化模型）
│   └── 05-ai-cognitive-augmentation（RAG+LLM 认知增强原型）
│
├── 09 价值量化（3 个子主题，6 个文件）
│   ├── 01-cocomo-ii-reuse（2026 校准版+参数说明）
│   ├── 02-roi-npv-models（直接/间接/战略收益+NPV）
│   └── tools（COCOMO 计算器 Python CLI）
│
├── 10 供应链安全（6 个子主题，18 个文件）
│   ├── 01-slsa-framework（1.1/1.2 Multi-Track 深度解析）
│   ├── 02-sbom-standards（SPDX 2.3 / CycloneDX 1.6 / SWID 对比）
│   ├── 03-attack-vectors（攻击树+交互式可视化 Python）
│   ├── 04-provenance-examples（溯源案例）
│   ├── 04-zero-trust-supply-chain（5 层防御矩阵模板）
│   └── 05-case-studies（XZ Utils/SolarWinds/Log4j + NIST SSDF + EU CRA）
│
├── 11 工业 IoT/OT-IT（7 个子主题，39 个文件）
│   ├── 01-isa-95-model（L0-L4 资产目录+跨层矩阵）
│   ├── 02-opc-ua-fx（C2C/C2D/D2D 复用边界+UADP 帧结构）
│   ├── 03-tsn-deterministic（GCL 配置模板）
│   ├── 04-plcopen-motion（功能块接口+TLA+ 验证）
│   ├── 05-digital-twin-aas（AAS-OPC UA NodeSet 完整映射）
│   ├── 06-functional-safety（IEC 61508 PIU/ISO 26262 SEooC+贝叶斯工具）
│   └── 07-edge-ai（模型部署规范+MCP for Industrial AI 草案）
│
├── 12 AI 原生复用（6 个子主题，22 个文件）
│   ├── 01-mcp-protocol（2025-11-25 深度解析）
│   ├── 02-a2a-protocol（v1.0.0 复用流程+安全机制）
│   ├── 03-agentic-infrastructure（Agentic 治理组织设计）
│   ├── 03-hybrid-a2a-mcp-poc（混合协议 PoC）
│   ├── 04-probabilistic-contracts（置信度函数+校准方法）
│   └── 05-conformal-prediction（CP 代码生成应用）
│
├── 13 新兴趋势（6 个子主题，13 个文件）
│   ├── 01-platform-engineering（IDP 成熟度+Golden Path）
│   ├── 02-modular-monolith（Spring Modulith 等回归趋势）
│   ├── 03-webassembly-components（WASM 复用决策树+WASI 0.3）
│   ├── 04-rust-ecosystem（所有权+供应链安全）
│   ├── 05-regtech-ai（监管科技 Agentic 架构）
│   └── 06-green-software（⚠️ 仅框架，内容最薄弱）
│
└── 99 参考索引（8 个子主题，66 个文件）
    ├── audit（差距分析报告）
    ├── book-outline（全书 12 章框架，~32.6 万字规划）
    ├── standards-index（30+ 标准总矩阵）
    ├── glossary（术语表+公理-定理树）
    ├── tools（术语查询+复用决策工具+成熟度评估 CLI）
    └── visualizations（13 主题 Mermaid 图库）
```

> **完成度评估**：01/06/07/10/11/12 六个主题完成度最高；03/04/05 三个层次主题存在结构性子目录缺失；02 业务架构子目录命名混乱；13 新兴趋势中 green-software 最薄弱；08/09 理论丰富但工具转化率低。

---

## 二、网络权威内容全景

### 2.1 国际标准组织最新状态

| 标准编号 | 项目状态 | 国际最新状态（2026-06-10） | 差距评估 |
|:---|:---|:---|:---|
| ISO/IEC/IEEE 42010:2022 | ✅ 深度映射 | 生效 | 无差距 |
| ISO/IEC/IEEE 42020:2019 | ✅ 深度映射 | 生效 | 无差距 |
| ISO/IEC/IEEE 42030:2019 | ✅ 已映射 | ⚠️ **AWI 42030 正在修订**（2026-04-22 启动），预计 2027 发布新版 | 需跟踪修订方向 |
| ISO/IEC/IEEE DIS 42024 | ✅ 已跟踪 | 草案 40.60 | 无差距 |
| ISO/IEC/IEEE DIS 42042 | ✅ 已跟踪 | 草案 40.60，预计 2026 末/2027 初定稿 | 无差距 |
| ISO/IEC 25010:2023 | ✅ HOTFIX-4 已更新 | 生效（取代 2011 版），新增 AI/ML 质量特性 | 需补充 AI 质量特性影响矩阵 |
| ISO/IEC 25040:2024 | ⚠️ 未深入映射 | 生效（评估过程） | **缺失：复用评估流程映射** |
| ISO/IEC 26550:2015 | ✅ 已映射 | 生效 | 无差距 |
| ISO/IEC 26565:2026 | ✅ 已引用 | **2026-05 正式发布**（成熟度框架） | 需更新正式版内容 |
| ISO/IEC 26566:2026 | ✅ 已引用 | **2026-05 正式发布**（产品线纹理 product line texture 的方法与工具能力） | 需更新正式版内容 |
| ISO/IEC 12207:2026 | ❌ 未更新 | **2026-04-29 刚发布**（第三版） | **缺失：新版生命周期过程映射** |
| ISO/IEC 33000 系列 (SPICE) | ❌ 未系统引用 | 生效，过程能力六级模型 | **缺失：与 RCMM/RiSE 的映射** |
| IEEE 1517-2010 | ✅ 已映射 | 生效，但 12207:2017/2026 已覆盖复用过程 | 需明确对照 12207:2026 |
| OMG RAS v2.2 | ✅ 已映射 | 生效 | 无差距 |
| FAIR4RS | ✅ 已映射 | 2022 发布 | 无差距 |

**关键发现**：

- ISO/IEC/IEEE 12207:2026 于 2026-04-29 正式发布，项目当前仍引用 2017 版，需更新
- AWI 42030（架构评估）正在修订，项目应跟踪其如何从 2019 版演进
- ISO/IEC 26565:2026 + 26566:2026 于 2026-05 正式发布，项目已提前引用，但需对照正式版深化

### 2.2 企业架构框架生态

| 框架 | 项目状态 | 国际权威状态 | 差距 |
|:---|:---|:---|:---|
| TOGAF 10 | ✅ 深度映射 | 最广泛使用的 EA 框架 | 无 |
| ArchiMate 3.2 | ✅ 深度映射 | 官方稳定版 | 无 |
| ArchiMate 4.0 | ✅ 已正式发布 | **已正式发布（2026-04-27，Document C260）** | 与 3.2 向后兼容 |
| FEA 2.0 (BRM/ARM/SRM/DRM) | ✅ 已映射 | 美国联邦政府基准 | 无 |
| Zachman Framework | ❌ 未覆盖 | 1987 创立，EA 本体论基石 | **缺失：六维分类与复用映射** |
| DoDAF / UAF 1.3 | ❌ 未覆盖 | 美国防部/北约在用，UAF 1.3 2025-11 发布 | **缺失：国防架构复用视角** |
| MODAF / NAF 4.0 | ❌ 未覆盖 | 英国防部/北约在用 | **缺失：军事联盟架构复用** |
| BIAN | ❌ 未覆盖 | 银行业架构网络，服务域规范 | **缺失：金融服务垂直复用** |
| GERAM / ISO 15704 | ❌ 未覆盖 | 企业参考架构方法论 | **缺失：通用企业参考架构** |
| ISO 19439 | ❌ 未覆盖 | 企业建模框架 | 轻度缺失 |

**关键发现**：

- 项目覆盖了 TOGAF/FEA 两个政府/企业主流框架，但**完全缺失 Zachman（本体论基础）、DoDAF/NAF（国防）、BIAN（金融）**
- 在垂直行业框架方面，仅有工业 IoT（ISA-95），缺乏金融、电信、医疗等行业架构

### 2.3 软件供应链安全权威

| 标准/框架 | 项目状态 | 国际权威状态 | 差距 |
|:---|:---|:---|:---|
| SLSA 1.0 | ✅ 已映射 | 2023-04 发布 | 无 |
| SLSA 1.1/1.2 | ✅ 已跟踪 | 1.1 发布；1.2 Multi-Track（Build/Source/Environment）| 无 |
| SLSA L4 | ⚠️ 待验证 | **仍在开发中**，未正式发布 | 需标注开发状态 |
| SPDX 2.3 | ✅ 已映射 | 生效 | 无 |
| CycloneDX 1.6 | ✅ 已映射 | 生效 | 无 |
| NIST SSDF 1.2 | ⚠️ 草稿跟踪 | SP 800-218r1 征求意见稿 | 跟踪正式版 |
| EU CRA 2024/2847 | ❌ 未系统覆盖 | **2024-12 通过，2026-09-11 起强制报告漏洞** | **缺失：合规检查清单** |
| OpenSSF Scorecard | ❌ 未覆盖 | 100 万+ 项目扫描，周度评估 | **缺失：开源项目安全评分与复用决策** |
| OpenSSF Security Baseline | ❌ 未覆盖 | 2024-2025 发布，与 SLSA/Scorecard 联动 | **缺失：基线标准映射** |
| GUAC | ❌ 未覆盖 | Graph for Understanding Artifact Composition，供应链图谱 | **缺失：依赖图谱分析** |
| OWASP SCVS | ❌ 未覆盖 | 软件组件验证标准 | **缺失：组件验证控制族** |
| Sigstore/cosign | ✅ 已提及 | 生效，npm 采用 | 无 |

**关键发现**：

- SLSA/SBOM 覆盖较好，但**EU CRA（法规）、OpenSSF Scorecard（实践）、GUAC（图谱）、OWASP SCVS（验证）**缺失
- EU CRA 2026-09-11 起强制报告 actively exploited vulnerabilities，对软件复用合规影响重大

### 2.4 AI 原生协议生态

| 协议/技术 | 项目状态 | 国际权威状态 | 差距 |
|:---|:---|:---|:---|
| MCP 2025-11-25 | ✅ 深度解析 | 当前稳定版，已捐给 Linux Foundation AAIF | 无（版本引用已勘误） |
| MCP Tasks/Icons/Elicitation | ⚠️ 部分覆盖 | 2025-11-25 引入 | 可深化 |
| A2A v1.0.0 | ✅ 深度解析 | Google 发布，Linux Foundation 治理 | 无 |
| A2A 150+ 企业采用 | ⚠️ 未更新 | 2026-04 宣布 150+ 组织 | 可补充 |
| Conformal Prediction | ✅ 已覆盖 | 代码生成领域快速兴起 | 需修正引用来源 |
| Agentic Governance | ⚠️ 框架初建 | 新兴领域，无成熟标准 | 保持探索 |

**关键发现**：

- MCP/A2A 覆盖领先于大多数中文技术社区内容
- 需关注 MCP 2026-07-28 RC 进展，但目前应以 2025-11-25 为基准

### 2.5 平台工程成熟度

| 技术/框架 | 项目状态 | 国际权威状态 | 差距 |
|:---|:---|:---|:---|
| Backstage IDP | ✅ 已覆盖 | 89% 市场占有率（2026-01），3400+ 组织 | 无 |
| CNCF Platform Eng Maturity | ⚠️ 已提及 | 五维度模型（Investment/Adoption/Interfaces/Operations/Measurement）| **缺失：五维度逐条映射** |
| Port / Cortex / Humanitec | ⚠️ 已列出 | 竞品市场份额小（Port 8%, Cortex 5%）| 可深化对比 |
| Golden Path | ✅ 已覆盖 | 平台工程核心实践 | 无 |
| DORA 2025 | ⚠️ 未引用 | 认知负荷首次成为正式指标 | **缺失：DORA 度量与复用成熟度关联** |

### 2.6 学术与会议前沿

| 会议/社区 | 2025-2026 主题 | 项目覆盖 | 差距 |
|:---|:---|:---|:---|
| ICSA 2025/2026 | "Architecting for next-gen intelligent systems" / "Continuous Software Engineering" | 提及 | **缺失：主题映射** |
| ECSA 2025 | "impactful software architecture" | 未引用 | **缺失：架构影响力模型** |
| SAGAI / GreenArch 2026 | Generative AI + Sustainable Architecture | 未覆盖 | **缺失：绿色架构复用度量** |
| AEDT (Digital Twins) | 数字孪生参考架构通用框架 | 工业 AAS 已覆盖 | **缺失：通用数字孪生参考架构** |
| SPLC 2025/2026 | Software Product Line Conference | 26550/26566 已覆盖 | 可补充会议主题 |
| FM 2025/2026 | Formal Methods | TLA+/Alloy/Coq 已覆盖 | 可补充最新工业应用 |

---

## 三、对称差分析：项目 ↔ 权威内容

### 3.1 项目独有（权威未系统覆盖）

| 独创内容 | 价值评估 | 说明 |
|:---|:---|:---|
| **四层复用公理-定理体系** | ⭐⭐⭐⭐⭐ | 15 条公理 + 17 条定理 + 5 猜想，首次建立复用工程的形式化认识论 |
| **跨层升级/降级决策矩阵** | ⭐⭐⭐⭐⭐ | 功能→组件→应用→业务服务的升级触发条件与降级回退策略 |
| **认知架构 + 价值量化融合** | ⭐⭐⭐⭐☆ | ACT-R/BDI + COCOMO II + NASA-TLX 的跨学科整合 |
| **工业 AI MCP 协议草案** | ⭐⭐⭐⭐☆ | 将 MCP 映射到 OPC UA FX + IEC 62443 安全扩展 |
| **概率契约框架** | ⭐⭐⭐⭐☆ | AI 功能复用的置信度函数 γ(x) 与确定性边界声明 |
| **ISA-95 L0-L4 复用资产目录** | ⭐⭐⭐⭐⭐ | 中文技术社区最系统的工业软件架构复用资产分类 |
| **AAS-OPC UA NodeSet 完整映射** | ⭐⭐⭐⭐⭐ | 11 项映射表 + JSON/XML 示例 + 生命周期同步规则 |
| **SLSA 复用安全边界** | ⭐⭐⭐⭐☆ | 将 SLSA L1-L4 与四层复用粒度（组件→应用→系统）关联 |

### 3.2 权威强调但项目缺失/不足

| 缺失内容 | 权威来源 | 影响评估 | 建议优先级 |
|:---|:---|:---|:---:|
| **DoDAF / UAF 1.3 / NAF 4.0** | 美国防部/北约/NoMagic 2026x | 军事/国防/航天领域架构复用完全空白 | P1 |
| **Zachman Framework 复用映射** | Zachman 1987/FEAC Institute | EA 本体论基础缺失 | P2 |
| **BIAN 金融服务架构** | Banking Industry Architecture Network | 金融行业垂直复用空白 | P2 |
| **ISO/IEC 12207:2026** | 2026-04-29 正式发布 | 软件生命周期过程最新版未对齐 | P1 |
| **ISO/IEC 33000 (SPICE)** | 过程能力六级模型 | 复用成熟度评估缺少过程评估维度 | P2 |
| **ISO/IEC 25040:2024** | 软件质量评估过程 | 复用资产的评估流程未映射 | P2 |
| **GERAM / ISO 15704** | 企业参考架构方法论 | 通用企业参考架构基础 | P3 |
| **EU CRA 2024/2847 合规** | 2026-09-11 起强制 | 软件复用合规风险未覆盖 | P1 |
| **OpenSSF Scorecard / Security Baseline** | OpenSSF 2025 Vision Brief | 开源项目安全评分与复用决策 | P2 |
| **GUAC 供应链图谱** | Google + OpenSSF | 依赖关系可视化与风险传递 | P2 |
| **OWASP SCVS** | OWASP | 软件组件验证标准 | P2 |
| **GreenArch / 可持续软件架构** | Green Software Foundation | 碳感知架构复用度量 | P3 |
| **DORA 2025 认知负荷指标** | Google Cloud / DevOps Research | 平台工程与复用采纳率关联 | P2 |
| **数字孪生通用参考架构** | AEDT / ISO 23247 | 非工业领域的数字孪生复用 | P3 |
| **MBSE 与架构复用** | INCOSE / OMG SysML v2 | 基于模型的系统工程与复用 | P2 |

### 3.3 双方均覆盖但视角差异

| 主题 | 项目视角 | 权威视角 | 差异说明 |
|:---|:---|:---|:---|
| **架构描述** | 复用视角：视图/视点作为复用契约载体 | ISO 42010: 通用架构描述框架 | 项目强调"复用契约"语义；权威强调"利益相关者沟通" |
| **成熟度模型** | 整合 RiSE/RCMM/NASA RRL 的五级模型 | ISO 26565:2026 / CMMI / SPICE | 项目更关注复用特异性；权威更关注过程通用性 |
| **微服务复用** | 服务网格 + Gateway API + 云原生模式 | NIST SP 800-204 / CNCF | 项目强调模式复用；权威强调安全/治理 |
| **供应链安全** | SLSA + SBOM + 攻击案例 | OpenSSF 全景（Scorecard/Baseline/GUAC）| 项目深度聚焦 SLSA；权威广度覆盖生态 |
| **AI 功能复用** | MCP/A2A 协议 + 概率契约 | Agentic AI Foundation / LLM 工具生态 | 项目强调协议边界；权威强调生态集成 |
| **工业 IoT** | ISA-95 + OPC UA FX + 功能安全 | IEC 62443 + ISO 30141 (IoT RA) | 项目聚焦 OT-IT 融合；权威增加网络安全 |

---

## 四、不同视角与相关内容对齐

本项目当前主要采用**软件工程四层架构视角**（业务→应用→组件→功能）。经与网络权威内容对比，以下五个外部视角可显著增强知识体系的完整性：

### 视角 1：企业架构本体论（Zachman / GERAM）

- **核心差异**：项目以"复用粒度"分层；Zachman 以"六维疑问词"（What/How/Where/Who/When/Why）分类
- **补全价值**：可为四层复用模型增加**跨维度交叉矩阵**（如 "Why-业务" × "How-技术" 的复用决策）
- **建议行动**：在 02 业务架构中增加 Zachman 列映射，说明业务复用回答 "Why/What"、技术复用回答 "How/Where"

### 视角 2：国防/使命工程（DoDAF / UAF 1.3 / NAF）

- **核心差异**：项目面向商业企业软件；DoDAF 面向跨组织军事系统集成
- **补全价值**：引入 **Capability Viewpoint（能力视角）** 和 **Operational Viewpoint（作战视角）**，强化业务架构的"使命对齐"维度
- **建议行动**：新增 `02-business-architecture-reuse/07-defense-mission-engineering/` 或作为案例补充

### 视角 3：过程评估与合规（SPICE / ISO 12207:2026 / EU CRA）

- **核心差异**：项目关注"复用什么"和"如何复用"；SPICE/12207 关注"过程能力是否足够支撑复用"
- **补全价值**：将 RCMM/RiSE 与 ISO/IEC 33000 过程能力模型映射，提供**合规驱动的复用采纳路径**
- **建议行动**：在 06 跨层治理中增加 ISO/IEC 33000 映射；在 10 供应链安全中增加 EU CRA 合规检查清单

### 视角 4：金融垂直架构（BIAN / TMForum）

- **核心差异**：项目通用性强；BIAN 提供银行业 300+ 服务域的精确复用单元
- **补全价值**：为业务架构复用提供**行业级精确案例**（如 "客户信息管理服务域" 的跨银行复用）
- **建议行动**：在 02/case-studies 中增加 BIAN 服务域映射案例

### 视角 5：可持续架构（GreenArch / Green Software Foundation）

- **核心差异**：项目关注功能/效率/安全；GreenArch 关注**碳足迹与能源效率**
- **补全价值**：增加"复用即减碳"的量化维度（复用组件 = 减少重复开发 = 降低算力消耗）
- **建议行动**：深化 13/06-green-software，增加 SCI（Software Carbon Intensity）与复用率的关联模型

---

## 五、后续计划与任务（待确认）

基于以上全面对齐分析，提出以下四阶段后续计划，总计 **28 项任务**，供您审阅确认。

### Phase A 立即修复（2026-06 第 2-3 周）

> 目标：消除事实性错误，修复已知的权威性损害风险。

| 任务 ID | 任务 | 交付物 | 验收标准 | 优先级 |
|:---|:---|:---|:---|:---:|
| A-01 | ISO/IEC 12207:2026 发布状态跟踪与映射更新 | `01/01-iso-420xx-family/iso-12207-2026-alignment.md` | 覆盖新版与 2017 版差异，特别是复用过程变化 | P1 |
| A-02 | AWI 42030 修订状态跟踪 | `01/01-iso-420xx-family/awi-42030-tracking.md` | 记录修订启动时间、预期方向 | P2 |
| A-03 | ISO/IEC 26565:2026 + 26566:2026 正式版内容深化 | `06/03-maturity-models/iso-26565-26566-final.md` | 对照 2026-05 正式版更新成熟度模型描述 | P1 |
| A-04 | EU CRA 2024/2847 合规检查清单 | `10/06-case-studies/eu-cra-checklist.md` | 覆盖 Annex I/II/III 关键条款 | P1 |
| A-05 | Warg Registry → wasm-pkg-tools 更新 | `13/03-webassembly-components/wasm-registry-update.md` | 移除 Warg 引用，更新为 OCI-based registry | P2 |
| A-06 | 03 应用架构基础子目录内容补全（分层/微服务/Serverless/事件驱动） | `03/01/02/03/04/` 各至少 1 篇核心文档 | 每篇 ≥500 行，含复用模式+反模式 | P1 |
| A-07 | 建立标准引用"版本+URL+核查日期"三元组规范 | `99-reference/templates/citation-standard.md` | 所有新增/更新文档强制执行 | P2 |

### Phase B 补全深化（2026-Q3 剩余）

> 目标：填补对称差中的高优先级缺失项，深化现有内容的权威对齐。

| 任务 ID | 任务 | 交付物 | 对齐来源 | 优先级 |
|:---|:---|:---|:---|:---:|
| B-01 | DoDAF / UAF 1.3 与复用视角映射 | `02/07-defense-mission-engineering/dodaf-uaf-reuse.md` | DoD CIO / NoMagic 2026x / UAF 1.3 Spec | P1 |
| B-02 | Zachman Framework 复用映射 | `02/08-zachman-reuse-mapping/zachman-reusability-matrix.md` | Zachman Institute / FEAC | P2 |
| B-03 | ISO/IEC 33000 (SPICE) 与 RCMM/RiSE 映射 | `06/03-maturity-models/spice-rcmm-rise-mapping.md` | ISO 33004 / SEI | P2 |
| B-04 | ISO/IEC 25040:2024 复用评估流程映射 | `06/05-metrics-kpi/iso-25040-reuse-evaluation.md` | ISO 25040:2024 | P2 |
| B-05 | OpenSSF Scorecard + Security Baseline 与复用决策 | `10/01-slsa-framework/openssf-scorecard-reuse.md` | OpenSSF 2025 Vision Brief | P2 |
| B-06 | BIAN 金融服务域复用案例 | `02/case-studies/bian-banking-reuse-case.md` | BIAN Service Landscape 12.0 | P2 |
| B-07 | DORA 2025 认知负荷指标与复用采纳率关联 | `08/03-cognitive-load-theory/dora-2025-cognitive-load.md` | Google DORA 2025 Report | P2 |
| B-08 | ISO 30141:2024 IoT 参考架构对齐 | `11/01-isa-95-model/iso-30141-iot-ra-alignment.md` | ISO 30141:2024 | P2 |
| B-09 | IEC 62443 工业网络安全与复用 | `11/06-functional-safety/iec-62443-reuse-security.md` | IEC 62443-3-3 / -4-2 | P2 |
| B-10 | GreenArch / SCI 软件碳强度与复用度量 | `13/07-green-software/sci-reuse-carbon-model.md` | Green Software Foundation / SCI Spec | P3 |
| B-11 | 术语查询脚本完善（跨标准术语翻译+别名映射） | `99-reference/tools/terminology-query-v2.py` | IREB CPRE / ISO 42010 | P2 |
| B-12 | 全书框架 v2.0 更新（纳入新视角） | `99-reference/book-outline-v2.md` | — | P1 |

### Phase C 扩展对齐（2026-Q4 → 2027-Q1）

> 目标：引入 MBSE、数字孪生通用架构、OWASP SCVS、GUAC 等中等优先级内容。

| 任务 ID | 任务 | 交付物 | 对齐来源 | 优先级 |
|:---|:---|:---|:---|:---:|
| C-01 | OMG SysML v2 与架构复用 | `01/09-sysml-v2/sysml2-reuse-mapping.md` | OMG SysML v2 Spec | P2 |
| C-02 | MBSE 模型复用与产品线工程整合 | `01/10-mbse-reuse/mbse-ple-integration.md` | INCOSE / ISO 26550 | P2 |
| C-03 | 数字孪生通用参考架构（非工业 AAS） | `11/08-digital-twin-general/dt-reference-architecture.md` | ISO 23247 / AEDT | P3 |
| C-04 | OWASP SCVS 软件组件验证标准映射 | `10/07-owasp-scvs/scvs-reuse-controls.md` | OWASP SCVS 1.0 | P2 |
| C-05 | GUAC 供应链图谱与复用风险评估 | `10/08-guac-supply-chain/guac-reuse-risk.md` | Google GUAC / OpenSSF | P2 |
| C-06 | TMForum ODF / eTOM 电信架构复用 | `02/case-studies/tmforum-telecom-reuse.md` | TMForum | P3 |
| C-07 | NAF 4.0 / MODAF 与北约架构复用 | `02/07-defense-mission-engineering/naf-modaf-reuse.md` | NATO / UK MOD | P3 |
| C-08 | 交互式复用决策工具 v2.0（Web/CLI） | `99-reference/tools/reuse-decision-tool-v2/` | — | P1 |

### Phase D 前沿跟踪（2027-Q2 → 2027-Q4）

> 目标：跟踪标准演进、会议前沿、技术迭代。

| 任务 ID | 任务 | 交付物 | 跟踪对象 | 优先级 |
|:---|:---|:---|:---|:---:|
| D-01 | AWI 42030 正式版对齐 | `01/01-iso-420xx-family/iso-42030-202x-update.md` | ISO/IEC/IEEE 42030 修订版 | P1 |
| D-02 | MCP 2026-07-28（或后续版本）更新 | `12/01-mcp-protocol/mcp-next-version-tracking.md` | Linux Foundation AAIF | P2 |
| D-03 | WASI 1.0 正式发布对齐 | `13/03-webassembly-components/wasi-1-0-alignment.md` | W3C / Bytecode Alliance | P2 |
| D-04 | ICSA/ECSA/SPLC 会议主题年度映射 | `99-reference/external-links/conference-theme-index.md` | IEEE/ACM 会议 | P3 |
| D-05 | 全书整合与输出（GitBook/白皮书/课程） | `99-reference/output/` | — | P1 |

---

## 六、需要您确认的关键决策

### 决策 1：是否立即执行 Phase A 的 7 项任务？

- **建议**：全部执行。特别是 A-01（12207:2026）、A-03（26565/26566 正式版）、A-04（EU CRA）、A-06（03 应用架构补全）四项为 P1，如不执行将造成标准滞后或结构性缺口。

### 决策 2：是否接受 Phase B 的 12 项任务？

- **建议**：B-01（DoDAF/UAF）、B-03（SPICE）、B-06（BIAN）三项可显著提升知识体系在国防/金融垂直领域的覆盖；B-10（GreenArch）为 P3，可暂缓。

### 决策 3：Phase C 的 8 项任务优先级如何排序？

- **建议**：C-08（交互式决策工具 v2.0）为 P1，可提前至 Phase B 末尾；C-01/C-02（MBSE）和 C-04/C-05（SCVS/GUAC）为 P2，建议保留在 Phase C；C-03/C-06/C-07 为 P3，可灵活调整。

### 决策 4：前沿主题取舍策略

- **当前状态**：项目已覆盖 MCP/A2A/Conformal Prediction/WASM/平台工程/模块化单体
- **建议新增跟踪**：Quantum-resistant software architecture（后量子密码学对组件复用的影响）、Federated AI（联邦学习与组件复用的交叉）
- **建议暂缓**：Quantum computing（量子计算软件架构，与复用关联度低）

### 决策 5：事实核查机制的正式化

- **建议**：在 MASTER_PLAN 月度节奏中正式加入"第 5 周事实核查"，并使用 `99-reference/templates/fact-check-checklist.md` 作为强制检查清单，防止再次出现 ArchiMate 4.0 / MCP 版本类错误。

---

> **报告编制说明**：
>
> - 本报告基于对 `struct/` 全部 214 个 Markdown 文件的手动审计、18 个网络权威来源的交叉验证、与 30+ 国际标准的版本比对
> - 所有标准版本信息均来自 ISO 官网、The Open Group、OpenSSF、Linux Foundation 等一级来源
> - "对称差"分析遵循集合论严格定义：A Δ B = (A\B) ∪ (B\A)
>
> **确认请求**：请审阅以上全部内容，特别关注：
>
> 1. 是否同意执行 Phase A（7 项）+ Phase B（12 项）的立即与近期任务？
> 2. 是否接受新增的 5 个外部视角（Zachman/DoDAF/SPICE/BIAN/GreenArch）？
> 3. 是否有其他标准、框架或会议需要纳入对齐范围？
>
> *报告完成时间: 2026-06-10 05:00 CST*
