# 02 业务架构复用

## 定位

最粗粒度的复用层次。从业务领域到业务服务，建立"业务语义可复用"的框架。

## 核心概念定义

业务架构复用是指在业务架构层对业务能力、价值流、业务流程与业务服务等资产进行识别、编目与跨场景复用的实践，其边界由价值创造而非组织结构定义。

## 核心内容

- **Level 1**: 业务领域复用（跨行业/跨组织宏观领域）
- **Level 2**: 业务能力复用（Capability-Based Planning）
- **Level 3**: 价值流复用（端到端价值交付序列）
- **Level 4**: 业务流程复用（BPMN 2.0 可执行流程）
- **Level 5**: 业务服务复用（SOA/ArchiMate Business Service）
- BPMN 2.0 / DMN 1.5 的复用元素详解
- FEA BRM（联邦企业架构业务参考模型）五层业务线结构
- 业务复用反模式：流程克隆、能力膨胀、价值流断裂

## 权威对齐

| 标准/框架 | 版本 | 核心条款/内容 | URL | 核查日期 |
|:---|:---|:---|:---|:---|
| OMG BPMN | 2.0.2 (2014) | §8.3 Process, §10.4 Collaboration, 可执行语义 | <https://www.omg.org/spec/BPMN/2.0.2/> | 2026-07-08 |
| OMG DMN | 1.5 (2024) | §6 Decision Requirements, §7 FEEL, §8 Decision Table | <https://www.omg.org/spec/DMN/1.5/> | 2026-07-08 |
| TOGAF | 10 (2022) | Phase B Business Architecture, Capability Mapping | <https://www.opengroup.org/togaf> | 2026-07-08 |
| FEA BRM | 2.0 | 五层业务线（Mission, Business, Customer, Data Management, Mission Support） | <https://obamawhitehouse.archives.gov/omb/e-gov/fea> | 2026-07-08 |
| ArchiMate | 4.2 | Business Layer: Capability, Value Stream, Business Process | <https://pubs.opengroup.org/architecture/archimate4-doc/> | 2026-07-08 |

## 关键公理

> **公理 2.1** (Capability Atomicity): 业务能力是可复用的最小业务语义单元，其边界由**价值创造**而非**组织结构**定义。

## 正向复用案例

**跨国银行的 KYC 能力复用**：某全球银行将"客户身份识别 (KYC)"抽象为企业级业务能力，统一客户尽调规则、风险评级标准与监管报告格式。零售银行、投资银行、财富管理三个业务线共享同一 KYC 服务目录，新市场开户合规审查周期从 6 周缩短至 1.5 周，监管审计问题减少 40%。

## 反例

**按组织架构切分的能力孤岛**：某制造企业将"市场部审批""财务部复核""法务部审核"直接建模为业务能力。半年后组织重组，市场部分拆为品牌市场与数字市场，原能力全部失效，能力地图被迫重构，基于能力的 IT 规划无法执行。根因在于能力边界被组织结构绑定，违背了"能力边界由价值创造定义"的公理。

## 当前状态

- [x] 五层层次结构定义
- [x] 决策矩阵与判定树
- [x] BPMN/DMN 可执行语义案例补充 (`06-bpmn-dmn/bpmn-dmn-executable-cases.md`)
- [x] FEA BRM 与 TOGAF Capability Map 交叉映射 (`02-business-capability/fea-brm-togaf-mapping.md`)
- [x] 行业垂直场景（金融、医疗、制造）案例库 (`case-studies/industry-vertical-cases.md`)

## 子目录导航

| 子目录 | 主题 | 状态 |
|:---|:---|:---:|
| `01-business-domain-reuse/` | 业务域复用 | 🆕 已创建 |
| `02-business-capability/` | 业务能力建模 | ✅ 核心文档 |
| `03-value-stream/` | 价值流复用 | ✅ 核心文档 |
| `04-business-process-reuse/` | 业务流程复用 | 🆕 已创建 |
| `05-business-service-reuse/` | 业务服务复用 | 🆕 已创建 |
| `06-bpmn-dmn/` | BPMN 2.0 / DMN 1.5 可执行案例 | ✅ 核心文档 |
| `07-defense-mission-engineering/` | 国防任务工程 | ✅ |
| `08-zachman-reuse-mapping/` | Zachman 框架复用映射 | ✅ |
| `case-studies/` | 行业垂直场景案例库 | ✅ |

## 交叉引用

- `03-application-architecture-reuse`（业务服务是业务层与应用层的桥接点）
- `06-cross-layer-governance`（业务能力目录治理）

## 标准条款映射

| 本主题概念 | 对应标准条款 | 映射说明 |
|:---|:---|:---|
| 业务能力 | TOGAF 10 §B.3.3 Business Capability | 能力为业务架构的内容元模型核心元素 |
| 价值流 | ArchiMate 4.0 §7.3 Value Stream | 端到端价值创造活动的结构化表达 |
| 业务流程 | BPMN 2.0 §8 Process | 可执行流程模型与人工可读图形的双重语义 |
| 业务决策 | DMN 1.5 §6 Decision Requirements Diagram | 决策逻辑与流程结构的解耦复用 |
| 业务线分类 | FEA BRM 2.0 Line of Business / Sub-function | 联邦政府跨机构业务能力复用基准 |
