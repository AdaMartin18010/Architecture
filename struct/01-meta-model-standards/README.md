# 01 元模型与标准对齐

## 定位

整个知识体系的概念地基。定义"复用"的元模型、术语体系，以及与 ISO/IEC/IEEE、TOGAF、ArchiMate 等国际标准的对齐映射。

## 核心内容

- ISO/IEC/IEEE 420xx 系列（42010/42020/42030/DIS 42024/DIS 42042）的族谱与演进
- TOGAF Standard 10 + ArchiMate 3.2（仍有效，与 4.0 向后兼容）；ArchiMate 4.0 已正式发布（2026-04-27，Document C260，白皮书 W262）
- ISO/IEC 26550:2015 产品线工程参考模型（领域工程 + 应用工程双轨）
- ISO/IEC 25010:2023 / 25040:2024 质量模型与评估过程
- **OMG RAS v2.2** 可复用资产规范（Classification / Solution / Usage / RelatedAssets）
- **FAIR4RS** 原则与软件资产可持续复用
- **ISO/IEC/IEEE 1517:2010-2010** 软件生命周期复用过程
- SWEBOK V4 的知识领域对齐
- 复用视角的形式化公理体系（元公理、存在性公理、结构性公理、过程性公理）

## 标准-主题速查表

| 主题 | 核心国际标准 | 说明 |
|---|---|---|
| 架构描述 | ISO/IEC/IEEE 42010:2022 | 定义 Entity of Interest、ADF、Viewpoint、View Component |
| 架构过程 | ISO/IEC/IEEE 42020:2019 | Governance / Management / Conceptualization / Evaluation / Elaboration / Enablement |
| 架构评估 | ISO/IEC/IEEE 42030:2019 | Objectives-Factors-Methods 三层评估框架 |
| 产品线工程 | ISO/IEC 26550:2015 | 双轨生命周期 + 显式 Variability Model |
| 企业架构建模 | TOGAF 10 / ArchiMate 4.0 (C260/W262) | ADM 方法 + 通用域建模语言 |
| 可复用资产 | OMG RAS v2.2 / FAIR4RS | 资产规范与可持续复用原则 |
| 系统建模 | OMG SysML v2 | 下一代基于模型的系统工程语言 |

## 权威对齐

| 标准/框架 | 权威 URL | 核查日期 |
|---|---|---|
| ISO/IEC/IEEE 42010:2022 | <https://www.iso.org/standard/74393.html> | 2026-07-09 |
| ISO/IEC/IEEE 42010:2022 OBP 在线浏览 | <https://www.iso.org/obp/ui/#iso:std:iso-iec-ieee:42010:ed-2:v1:en> | 2026-07-09 |
| ISO/IEC/IEEE 42020:2019 | <https://www.iso.org/standard/68982.html> | 2026-07-09 |
| ISO/IEC/IEEE 42030:2019 | <https://www.iso.org/standard/73436.html> | 2026-07-09 |
| ISO/IEC 26550:2015 | <https://www.iso.org/standard/69529.html> | 2026-07-09 |
| The Open Group TOGAF Standard, 10th Edition | <https://www.opengroup.org/togaf> | 2026-07-09 |
| The Open Group TOGAF Library / Architecture Content | <https://publications.opengroup.org/togaf-library> | 2026-07-09 |
| ArchiMate 4 Specification (Document C260) | <https://www.opengroup.org/archimate-licensed-downloads> | 2026-07-09 |
| ArchiMate 4 变更动机白皮书 W262 | <https://publications.opengroup.org/w262> | 2026-07-09 |
| OMG RAS v2.2 | <https://www.omg.org/spec/RAS/2.2/> | 2026-07-09 |
| FAIR4RS Principles | <https://ardc.edu.au/resource/fair-principles-for-research-software-fair4rs/> | 2026-07-09 |
| IEEE 1517-2010 | <https://standards.ieee.org/ieee/1517/4603/> | 2026-07-09 |
| OMG SysML v2 Specification | <https://www.omg.org/spec/SysML/20250201/SysML.json> | 2026-07-09 |

## ISO/IEC/IEEE 42010:2022 核心条款映射

| 条款 | 核心内容 | 架构描述元素 | 复用意义 |
|---|---|---|---|
| Clause 5.2 | 架构描述概念模型 | EoI、Stakeholder、Concern、Perspective、Aspect、Viewpoint、View、Model Kind、View Component、Correspondence、Decision/Rationale | 建立可复用的元模型词汇表 |
| Clause 6.1–6.10 | AD 规约要求 | 识别 EoI、利益相关者、视角、关注点、视点、视图、视图组件、对应关系、决策与依据 | 定义架构描述必须包含的信息项，可直接作为模板检查清单 |
| Clause 7.1–7.2 | ADF / ADL 规约 | Architecture Description Framework、Architecture Description Language 的 conformance 要求 | TOGAF、ArchiMate、SysML 等框架可声明符合 42010 |
| Clause 8.1–8.3 | Viewpoint、Model Kind、View Method 规约 | 视点的关注点覆盖、模型种类的约定、视图方法 | 可复用视点与模型种类的标准化基础 |

## 当前状态

- [x] 标准族谱梳理
- [x] ISO/IEC/IEEE 42010:2022 条款级映射 (`01-iso-420xx-family/iso-42010-2022.md`)
- [x] ISO/IEC/IEEE 42020:2019 架构过程映射 (`01-iso-420xx-family/iso-42020-2019-architecture-processes.md`)
- [x] TOGAF Standard 10 ABB/SBB 与 ISO/IEC/IEEE 42010:2022 详细映射 (`02-togaf-10-alignment/detailed-mapping.md`)
- [x] ArchiMate 3.2/4.0 与 ISO/IEC/IEEE 42010:2022 对照表 (`04-archimate-4/archimate-iso-mapping.md`)；已按 4.0 正式发布状态更新
- [x] ISO/IEC 26550:2015 与 ISO/IEC/IEEE 42010:2022/42020 交叉映射 (`03-iso-26550-ple/ple-iso-integration.md`)
- [x] SWEBOK V4 知识领域对应关系 (`05-swebok-v4/swebok-alignment.md`)
- [x] OMG RAS v2.2 与四层复用架构对齐 (`07-omg-ras/ras-alignment.md`)
- [x] FAIR4RS 原则与软件复用对照 (`08-fair4rs/fair4rs-alignment.md`)
- [x] ISO/IEC/IEEE 1517:2010-2010 与 ISO/IEC/IEEE 12207:2017 / 42020 复用过程映射 (`01-iso-420xx-family/ieee-1517-reuse-processes.md`)
- [x] DIS 42024/42042 当前状态对齐 (`01-iso-420xx-family/iso-42024-42042-dis-alignment.md`)
- [x] ISO/IEC 25010:2023 AI/ML质量特性影响矩阵 (`01-iso-420xx-family/iso-25010-2023-update.md`)
- [x] ArchiMate 4.0 映射更新（2026-04-27 已正式发布，映射已完成）

## 交叉引用

- [02-business-architecture-reuse](../02-business-architecture-reuse/README.md)（业务视点定义）
- [06-cross-layer-governance](../06-cross-layer-governance/README.md)（治理过程标准 42020/42030）
- [07-formal-verification](../07-formal-verification/README.md)（形式化公理体系）

---

## 概念定义

**元模型（Meta-model）** 是对架构描述元素、关系与规则的抽象规约；**标准对齐** 则指将本知识体系的术语、过程与视图与国际/行业权威标准建立可追溯的映射。

## 示例

**正向示例 1：跨国银行架构描述统一**

某跨国银行采用 ISO/IEC/IEEE 42010:2022 的 Entity of Interest、Architecture Description Framework 与 Stakeholder Perspective，结合 TOGAF ADM Phase B/C 和 ArchiMate 4.0 通用域，统一了全球 12 个业务单元的架构描述语言。外部审计时，团队可在 2 小时内展示业务服务到应用组件的追溯链符合 ISO/IEC/IEEE 42010:2022 Clause 5.2 与 Clause 6.8 的要求。

**正向示例 2：汽车电子基于 ISO/IEC 26550:2015 的产品线复用**

某汽车电子供应商在 ISO/IEC 26550:2015 双轨生命周期指导下，将 ECU 软件平台拆分为领域工程资产（Feature Model + Variation Point）与应用工程资产（特定车型配置）。通过 ISO/IEC/IEEE 42010:2022 视点框架记录各车型架构描述，实现 78% 的代码复用率，并将新车型适配周期从 9 个月缩短至 3 个月。

## 反例

**反模式 1：术语私域化**

团队自创“业务域/技术域/数据域”三分法，却未在矩阵中映射到 TOGAF/ArchiMate/FEA 的正式术语。结果与外部审计交流时，“业务域”被误解为 TOGAF 的 Business Domain 或 FEA 的 Business Reference Model，供应商方案因术语不一致被多次退回，项目延期 6 周。

**反模式 2：跳过对应规则导致追溯断裂**

某项目为赶工期直接复用 ArchiMate 3.2 业务层模型，但未按 ISO/IEC/IEEE 42010:2022 Clause 6.9 记录业务服务与应用服务之间的 Correspondence Rule。当业务规则变更时，团队无法快速定位受影响的应用组件，导致 6 个微服务需要返工，额外投入 240 人天。

## 国际权威来源核查

> **权威来源**:
>
> - [ISO/IEC/IEEE 42010:2022 — Architecture description](https://www.iso.org/standard/74393.html) — ISO（核查日期：2026-07-08）
> - [ISO/IEC/IEEE 42020:2019 — Architecture processes](https://www.iso.org/standard/68982.html) — ISO（核查日期：2026-07-08）
> - [ISO/IEC/IEEE 42030:2019 — Architecture evaluation](https://www.iso.org/standard/73436.html) — ISO（核查日期：2026-07-08）
> - [ISO/IEC 26550:2015 — Product line engineering](https://www.iso.org/standard/69529.html) — ISO（核查日期：2026-07-08）
> - [The Open Group TOGAF Standard, 10th Edition](https://www.opengroup.org/togaf)（核查日期：2026-07-08）
> - [The Open Group ArchiMate 4.0 Specification (C260/W262)](https://www.opengroup.org/archimate-licensed-downloads)（核查日期：2026-07-08）
> - [OMG RAS v2.2](https://www.omg.org/spec/RAS/2.2/)（核查日期：2026-07-08）
> - [FAIR4RS Principles](https://ardc.edu.au/resource/fair-principles-for-research-software-fair4rs/)（核查日期：2026-07-08）
> - [OMG SysML v2 Specification](https://www.omg.org/spec/SysML/20250201/SysML.json)（核查日期：2026-07-08）
