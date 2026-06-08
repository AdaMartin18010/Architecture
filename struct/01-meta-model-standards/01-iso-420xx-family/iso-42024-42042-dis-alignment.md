# ISO/IEC/IEEE DIS 42024 + DIS 42042 权威对齐（2025‑2026）

> **定位**：ISO 42010 家族最新扩展，为架构描述评估与参考架构规范提供标准化基础。
> **权威来源**：ISO/IEC JTC 1/SC 7、IEEE SA、国家标准化机构 DIS 投票公告。

---

## 1. 关键结论（TL;DR）

| 标准 | 状态 | 核心内容 | 预期发布 |
|------|------|----------|----------|
| **ISO/IEC/IEEE DIS 42024** | DIS 投票中（截止 2026‑01） | 架构基础：词汇、概念、原则；显式覆盖 AI/ML/IoT/数字孪生 | 2026 末–2027 初 |
| **ISO/IEC/IEEE DIS 42042** | DIS 投票中（截止 2026‑01‑30） | 参考架构规范要求；支持领域特定 RA 的一致性评估 | 2026 末–2027 初 |
| **ArchiMate 4.0** | **厂商预发布/预览** | Common Domain、策略域、Path 概念（预览内容，未获官方确认）；与 3.2 向后兼容（预览承诺） | **未获 The Open Group 正式发布确认** |
| ~~ArchiMate 3.2~~ | 已发布（2022‑10） | 物理元素整合、元模型精化、新关系 | 仍有效，向后兼容 |
| **TOGAF 10** | 已发布（2022） | Fundamental Content + Series Guides 模块化 | 已发布 |
| **OMG Essence 2.0 beta 2** | 2026‑03 | 内核现代化，支持 DevOps/AI 增强开发 | 预计 2026‑2027 |

---

## 2. ISO DIS 42024 — Architecture Fundamentals

### 2.1 状态

- **阶段**：DIS（Draft International Standard）
- **公共审查截止**：2026 年 1 月（丹麦 DSF 2026‑01‑12；希腊 ELOT 2026‑01‑28）
- **项目启动**：2023‑12
- **预计发布**：2026 末–2027 初（若 DIS 投票通过）

### 2.2 内容

规定与架构及架构实践相关的**基础词汇、概念和原则**。明确列出的应用领域包括：

> 人工智能 (AI)、机器学习 (ML)、物联网 (IoT)、云计算、大数据、智慧城市、智能制造、网络安全、数字孪生、电信、航空航天、国防、银行、金融等。

### 2.3 对复用的意义

- **统一基础词汇**：减少跨领域复用架构工件时的语义摩擦
- **一致性评估**：为其他 42000 家族标准提供术语基准
- **AI/ML 覆盖**：支持 AI 系统的架构描述标准化，促进 AI 组件的跨域复用

---

## 3. ISO DIS 42042 — Reference Architectures

### 3.1 状态

- **阶段**：DIS（Draft International Standard）
- **投票截止**：2026‑01‑30
- **PAR 批准**：IEEE SA，2024‑02
- **预计发布**：2026 末–2027 初

### 3.2 内容

描述**领域特定参考架构**应满足的要求，涵盖：

- 软件、系统、企业、系统之系统
- 产品线、服务线
- 技术领域、业务领域

### 3.3 对复用的意义

这是 42000 家族中**最直接与复用相关**的新标准：

1. **认证可复用参考架构**：组织可认证其参考架构符合 42042
2. **一致性评估**：采购方可要求供应商的架构符合某参考架构
3. **促进RA标准化**：为智能制造、智慧城市、数字孪生等领域提供统一的参考架构文档规范

---

## 4. ArchiMate 现状澄清

### 4.1 官方状态

| 版本 | 状态 | 来源 |
|------|------|------|
| **ArchiMate 3.2** | 已发布（2022‑10） | 考试与工具认证基于 3.2；与 4.0 向后兼容 |
| **ArchiMate 4.0** | **厂商预发布/预览** | 未获官方正式发布确认；Common Domain、策略域、Path 概念为预览内容；向后兼容 3.2 为预览承诺 |

### 4.2 ArchiMate 4.0 主要特性

- **Common Domain**：跨所有域统一的行为元素（Service、Process、Function、Event）
- **策略域**：支持战略路线图的建模
- **Path 概念**：填补逻辑-物理分离空白
- **概念简化**：删除冗余元素，同时保持向后兼容
- **与 TOGAF 对齐**：更紧密地支持企业架构方法

> **项目建议**：ArchiMate 3.2 是当前官方稳定版本。新项目中应继续采用 3.2；ArchiMate 4.0 预览内容仅供参考，不具备标准合规效力，待 The Open Group 正式发布后再行迁移规划。

---

## 5. TOGAF 10 与 AI 集成

### 5.1 结构

- **Fundamental Content**：稳定核心（ADM、内容框架）
- **Series Guides (Extended Guidance)**：演进式专题指南（敏捷、业务架构、数据架构、安全架构、数字化转型）

### 5.2 AI 治理定位

TOGAF 10 正被定位为 **AI 增强企业架构的治理框架**：

- ADM 阶段映射到 AI 风险管理、伦理治理、数据就绪
- 识别 AI 转型所需的技能、数据和技术缺口
- Agentic AI 系统集成指导

### 5.3 复用关联

- **Enterprise Continuum** 和 **Architecture Repository** 仍是资产复用的核心机制
- Series Guides 模块化本身即复用模式——组织只采用相关指南

---

## 6. OMG Essence 2.0

### 6.1 状态

- **当前正式版**：Essence 1.2（2018‑07）
- **开发中**：Essence Kernel & Language for Engineering Methods 2.0 beta 2（2026‑03）
- **同时进行中**：Essence 2.1 RTF（Revision Task Force）

### 6.2 2.0 预期变化

- 内核现代化以支持 DevOps 和持续工程实践
- AI 增强开发工作流
- 与架构描述实践更好集成

### 6.3 复用意义

Essence 的 kernel 元素（Requirements、Software System、Work、Team 等）是**跨项目类型可复用**的。标准支持**情境化方法工程**——组织组合可复用的方法片段，而非采用整体流程。

---

## 7. 标准选型指南

### 7.1 私营企业 / 跨行业组织

| 目标 | 推荐标准组合 |
|------|-------------|
| 核心 EA 方法论 | TOGAF 10 (Fundamental + 相关 Series Guides) |
| 建模语言 | **ArchiMate 3.2**（当前稳定）；谨慎关注 "ArchiMate Next" 动向 |
| 架构描述一致性 | ISO/IEC/IEEE 42010:2022 |
| 基础术语与原则 | ISO/IEC/IEEE 42024（待发布） |
| 参考架构规范 | ISO/IEC/IEEE 42042（待发布） |
| 软件工程方法复用 | OMG Essence 1.2；准备 2.0 beta |
| 资产目录 / 复用仓库 | Backstage + 现代 API/Spec 注册表；RAS v2.2 概念仅用于遗留系统 |

### 7.2 美国联邦机构

- **FEAF v2**（2013）仍是联邦 EA 对齐的强制框架
- TOGAF 10 可作为补充方法论（在政策允许时采用混合方法）
- FEAF CRM 域映射到 TBM 分类法用于现代化和成本透明

### 7.3 AI 增强型 EA 项目

1. TOGAF 10 建立 AI 治理、风险和伦理阶段
2. ISO DIS 42042 定义领域特定 AI 参考架构
3. ArchiMate 3.2 应用/技术层建模 AI 服务、数据管道和基础设施
4. 跟踪 ISO DIS 42024 获取标准化 AI 架构词汇

---

## 8. 权威来源

| 标准 | URL |
|------|-----|
| ArchiMate (The Open Group) | <https://www.opengroup.org/archimate-forum/archimate-overview> |
| TOGAF 10 | <https://www.opengroup.org/togaf> |
| ISO 42010:2022 | <https://www.iso.org/standard/74296.html> |
| ISO DIS 42024 / 42042 | <https://www.iso.org/committee/45086/x/catalogue/> |
| OMG Specifications | <https://www.omg.org/spec/> |
| FEAF v2 | <https://obamawhitehouse.archives.gov/sites/default/files/omb/assets/egov_docs/fea_v2.pdf> |

---

*文档生成时间：2026-06-06 · 对齐 ISO DIS 42024/42042 投票状态 / ArchiMate 3.2 GA / TOGAF 10 / Essence 2.0 beta 2*
