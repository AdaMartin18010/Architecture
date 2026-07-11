# ISO/IEC/IEEE 42020:2019 架构过程与复用

> **版本**: 2026-07-09
> **定位**: 将 ISO/IEC/IEEE 42020:2019 的架构过程与软件工程架构复用知识体系对齐
> **权威来源**: ISO/IEC/IEEE 42020:2019; ISO/IEC/IEEE 42010:2022; ISO/IEC/IEEE 42030:2019

---

## 1. 概念定义

**定义**：ISO/IEC/IEEE 42020:2019 是系统与软件工程领域的**架构过程**标准，它规定了架构治理（Governance）、管理（Management）、概念化（Conceptualization）、评估（Evaluation）、细化（Elaboration）和使能（Enablement）六个核心过程。该标准与 ISO/IEC/ISO/IEC/IEEE 42010:2022（架构描述）和 42030（架构评估）共同构成 420xx 标准族的过程维度。

## 2. 核心过程概览

ISO/IEC/IEEE 42020:2019 将架构过程分为六个相互关联的过程：

```text
ISO/IEC/IEEE 42020:2019
│
├── 6 Architecture Governance（架构治理）
├── 7 Architecture Management（架构管理）
├── 8 Architecture Conceptualization（架构概念化）
├── 9 Architecture Evaluation（架构评估）
├── 10 Architecture Elaboration（架构细化）
└── 11 Architecture Enablement（架构使能）
```

| 过程 | 目的 | 关键活动 | 复用意义 |
|---|---|---|---|
| **Architecture Governance** | 确保架构集合与企业目标、政策和战略保持一致 | 制定治理指令、监控合规、做出治理决策 | 定义复用资产的准入、退役和治理规则 |
| **Architecture Management** | 实施治理指令并管理架构集合 | 维护架构集合、监控架构活动有效性 | 维护资产库版本、状态与依赖关系 |
| **Architecture Conceptualization** | 识别满足利益相关者关注点的解决方案 | 问题空间刻画、目标定义、候选架构形成 | 识别可复用的领域模式与参考架构 |
| **Architecture Evaluation** | 确定架构满足利益相关者需求的程度 | 确定评估目标、方法、测量技术并分析结果 | 评估复用资产的适用性与风险 |
| **Architecture Elaboration** | 完整记录架构以支持其预期用途 | 创建架构描述、视图、模型和交付物 | 将复用资产实例化为具体架构描述 |
| **Architecture Enablement** | 为其他架构过程提供必要支持 | 建立方法、工具、技能和知识管理 | 构建复用基础设施（资产库、工具链、培训） |

## 3. 条款映射（Clause 5–11）

| 条款 | 核心内容 | 过程输出/制品 | 本框架对应主题 |
|---|---|---|---|
| Clause 5.1 | 过程概述与应用 | 架构过程与生命周期、设计的关系 | 全过程治理视角 |
| Clause 5.2 | 架构与其他过程和信息元素的关系 | 架构过程与 ISO 15288/12207 的衔接 | 生命周期对齐 |
| Clause 5.3 | 治理与管理过程 | Governance 与 Management 的双层结构 | `06-cross-layer-governance` |
| Clause 5.4 | 概念化、评估与细化过程 | Conceptualization / Evaluation / Elaboration 的交互 | `02-business-architecture-reuse` / `07-formal-verification` |
| Clause 5.5 | 使能过程 | Enablement 的支撑作用 | `04-component-architecture-reuse` 资产库 |
| Clause 6.1–6.5 | Architecture Governance 目的、结果、实现、活动与任务、工作产品 | 治理策略、原则、合规评估、治理日志 | 治理策略目录 |
| Clause 7.1–7.5 | Architecture Management 目的、结果、实现、活动与任务、工作产品 | 架构集合管理计划、架构资产库、有效性监控 | 本主题矩阵维护 |
| Clause 8.1–8.5 | Architecture Conceptualization 目的、结果、实现、活动与任务、工作产品 | 问题空间描述、候选架构、架构目标与成功标准 | 业务能力地图 |
| Clause 9.1–9.5 | Architecture Evaluation 目的、结果、实现、活动与任务、工作产品 | 评估目标、准则、方法、结论与建议 | 质量门控与评估清单 |
| Clause 10.1–10.5 | Architecture Elaboration 目的、结果、实现、活动与任务、工作产品 | 架构描述、视图、模型、交付物 | ABB→SBB 细化 |
| Clause 11.1–11.5 | Architecture Enablement 目的、结果、实现、活动与任务、工作产品 | 方法、工具、培训、知识资产 | 组件资产库与接口契约 |

## 4. 与 ISO 42010:2022 的协同

ISO 42020 回答**“如何产生架构”**，ISO/IEC/IEEE 42010:2022 回答**“如何描述架构”**。两者协同关系如下：

| ISO 42020:2019 过程 | ISO 42010:2022 对应条款 | 协同说明 |
|---|---|---|
| Architecture Conceptualization (Clause 8) | Clause 5.2.3 / 6.4（关注点识别） | 概念化过程识别 EoI 与利益相关者关注点 |
| Architecture Elaboration (Clause 10) | Clause 6.6–6.8（视点、视图、视图组件） | 细化过程产生符合 42010 的 AD |
| Architecture Evaluation (Clause 9) | Clause 6.10（决策与依据） | 评估结果形成 Architecture Rationale |
| Architecture Governance (Clause 6) | Clause 7.1（ADF 规约） | 治理过程定义企业 ADF 与视点标准 |
| Architecture Enablement (Clause 11) | Clause 7.2 / 8.1–8.3（ADL / Viewpoint / Model Kind） | 使能过程提供可复用的 ADL、视点和模型种类 |

## 5. 与 TOGAF 10 / ArchiMate 的映射

| ISO 42020:2019 过程 | TOGAF 10 ADM 阶段 | ArchiMate 4.0 元素/域 | 复用场景 |
|---|---|---|---|
| Architecture Governance | Preliminary Phase | Motivation Domain（Goal / Principle） | 原则目录、治理框架 |
| Architecture Management | Preliminary Phase + Phase H | Implementation & Migration Layer | 架构仓库维护 |
| Architecture Conceptualization | Phase A（Architecture Vision） | Strategy Domain（Capability / Value Stream） | 业务能力地图复用 |
| Architecture Evaluation | Phase G（Compliance Review） + Requirements Management | Assessment / Gap | 合规审查、差距分析 |
| Architecture Elaboration | Phase B/C/D | Business / Application / Technology Layer | 各层 ABB/SBB 细化 |
| Architecture Enablement | Phase E/F + Requirements Management | Work Package / Deliverable / Plateau | 资产使能与迁移 |

## 示例

**正向示例：某金融机构基于 ISO/IEC/IEEE 42020:2019 建立架构资产治理体系**

- **Architecture Governance（Clause 6）**：架构委员会定义“所有新建系统必须使用企业级认证服务”的治理指令。
- **Architecture Management（Clause 7）**：架构办公室维护认证服务的 ABB 定义、已部署 SBB 清单和版本路线图。
- **Architecture Conceptualization（Clause 8）**：在新支付平台概念化阶段，识别出“强身份认证”关注点，并复用现有认证能力 ABB。
- **Architecture Evaluation（Clause 9）**：评估候选方案（Keycloak vs Okta vs 自研）对安全、成本和集成的满足度。
- **Architecture Elaboration（Clause 10）**：使用 ArchiMate 4.0 通用域生成认证服务视图，并按 ISO/IEC/IEEE 42010:2022 Clause 6 记录视点、视图组件和对应关系。
- **Architecture Enablement（Clause 11）**：建立认证服务模板库、CI/CD 流水线模板和架构师培训计划。

结果：新支付平台在 6 周内完成认证能力集成，较历史项目缩短 60%。

## 反例/反模式

**反模式：评估过程流于形式**

某团队在架构评审时仅检查“是否有架构图”，未按 ISO/IEC/IEEE 42020:2019 Clause 9 制定评估目标、准则和方法：

- 没有明确利益相关者关注点与评估准则的对应关系；
- 未记录评估假设和测量技术；
- 评估结论缺乏可追溯的决策依据（Architecture Rationale）。

结果：项目上线后，性能目标未达成，但无法回溯评估环节的缺失，外部审计判定架构治理不合规，项目被暂停整改。

## 8. 权威来源

> **权威来源**：
>
> - [ISO/IEC/IEEE 42020:2019 — Architecture processes](https://www.iso.org/standard/68982.html) — ISO（核查日期：2026-07-09）
> - [ISO/IEC/IEEE 42020:2019 OBP 在线浏览](https://www.iso.org/obp/ui/#iso:std:iso-iec-ieee:42020:ed-1:v1:en) — ISO（核查日期：2026-07-09）
> - [ISO/IEC/IEEE 42010:2022 — Architecture description](https://www.iso.org/standard/74296.html) — ISO（核查日期：2026-07-09）
> - [ISO/IEC/IEEE 42030:2019 — Architecture evaluation](https://www.iso.org/standard/73436.html) — ISO（核查日期：2026-07-09）
> - [The Open Group TOGAF Standard, 10th Edition](https://www.opengroup.org/togaf) — The Open Group（核查日期：2026-07-09）
> - [The Open Group ArchiMate 4.0 Specification (C260)](https://www.opengroup.org/archimate-licensed-downloads) — The Open Group（核查日期：2026-07-09）
>
> **核查日期**：2026-07-09

## 9. 交叉引用

- ISO/IEC/IEEE 42010:2022 核心概念详见 [`iso-42010-2022.md`](./iso-42010-2022.md)
- 标准对齐矩阵详见 [`alignment-matrix.md`](./alignment-matrix.md)
- TOGAF 详细映射详见 [`../02-togaf-10-alignment/detailed-mapping.md`](../02-togaf-10-alignment/detailed-mapping.md)
- ArchiMate 映射详见 [`../04-archimate-4/archimate-iso-mapping.md`](../04-archimate-4/archimate-iso-mapping.md)
- 形式化公理体系详见 [`../06-formal-axioms/axiom-system.md`](../06-formal-axioms/axiom-system.md)

---

> **最后更新**: 2026-07-09
> **维护者**: Track A — 01 元模型与标准对齐