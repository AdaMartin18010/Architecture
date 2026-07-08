# 01 元模型与标准对齐

## 定位

整个知识体系的概念地基。定义"复用"的元模型、术语体系，以及与 ISO/IEC/IEEE、TOGAF、ArchiMate 等国际标准的对齐映射。

## 核心内容

- ISO/IEC/IEEE 420xx 系列（42010/42020/42030/DIS 42024/DIS 42042）的族谱与演进
- TOGAF 10 + ArchiMate 3.2（仍有效，与 4.0 向后兼容）；ArchiMate 4.0 已正式发布（2026-04-27，Document C260，白皮书 W262）
- ISO/IEC 26550:2015 产品线工程参考模型（领域工程 + 应用工程双轨）
- ISO/IEC 25010:2023 / 25040:2024 质量模型与评估过程
- **OMG RAS v2.2** 可复用资产规范（Classification / Solution / Usage / RelatedAssets）
- **FAIR4RS** 原则与软件资产可持续复用
- **IEEE 1517-2010** 软件生命周期复用过程
- SWEBOK V4 的知识领域对齐
- 复用视角的形式化公理体系（元公理、存在性公理、结构性公理、过程性公理）

## 权威对齐

- [ISO 42010:2022 官方标准](https://www.iso.org/obp/ui)
- [The Open Group TOGAF 10](https://www.opengroup.org/togaf)
- [ArchiMate 3.2 Specification](https://pubs.opengroup.org/architecture/archimate32-doc/) (仍有效，与 4.0 向后兼容)
- [ArchiMate 4 Specification](https://www.opengroup.org/archimate-licensed-downloads) (已正式发布，2026-04-27，Document C260)
- [OMG RAS v2.2](https://www.omg.org/spec/RAS/)
- [FAIR4RS Principles](https://ardc.edu.au/resource/fair-principles-for-research-software-fair4rs/)
- [IEEE 1517-2010](https://standards.ieee.org/standard/1517-2010.html)
- IREB CPRE Glossary 2.2 (ISO 26550, 29148 引用)

## 当前状态

- [x] 标准族谱梳理
- [x] TOGAF 10 ABB/SBB 与 ISO 42010 详细映射 (`02-togaf-10-alignment/detailed-mapping.md`)
- [x] ArchiMate 3.2/4.0 与 ISO 42010 对照表 (`04-archimate-4/archimate-iso-mapping.md`)；已按 4.0 正式发布状态更新
- [x] ISO 26550:2015 与 ISO 42010/42020 交叉映射 (`03-iso-26550-ple/ple-iso-integration.md`)
- [x] SWEBOK V4 知识领域对应关系 (`05-swebok-v4/swebok-alignment.md`)
- [x] OMG RAS v2.2 与四层复用架构对齐 (`07-omg-ras/ras-alignment.md`)
- [x] FAIR4RS 原则与软件复用对照 (`08-fair4rs/fair4rs-alignment.md`)
- [x] IEEE 1517-2010 与 ISO 12207 / 42020 复用过程映射 (`01-iso-420xx-family/ieee-1517-reuse-processes.md`)
- [x] DIS 42024/42042 当前状态对齐 (`01-iso-420xx-family/iso-42024-42042-dis-alignment.md`)
- [x] ISO/IEC 25010:2023 AI/ML质量特性影响矩阵 (`01-iso-420xx-family/iso-25010-2023-update.md`)
- [x] ArchiMate 4.0 映射更新（2026-04-27 已正式发布，映射已完成）

## 关联主题

- `02-business-architecture-reuse`（业务视点定义）
- `06-cross-layer-governance`（治理过程标准 42020/42030）
- `07-formal-verification`（形式化公理体系）


---

## 补充说明：01 元模型与标准对齐

## 概念定义

**定义**：元模型（Meta-model）是对架构描述元素、关系与规则的抽象规约；标准对齐则指将本知识体系的术语、过程与视图与国际/行业权威标准建立可追溯的映射。

## 示例

**示例**：在架构描述中采用 ISO/IEC/IEEE 42010:2022 的 Entity of Interest、Architecture Description Framework 与 Stakeholder Perspective，使架构视图与评估框架可直接对标国际标准。

## 反例

**反例**：团队自创“业务域/技术域/数据域”三分法却未与 TOGAF/ArchiMate 术语映射，导致与外部审计、供应商交流时出现语义偏差。

## 权威来源

> **权威来源**:
>
> - [ISO/IEC/IEEE Standards](https://www.iso.org)
> - [IEEE Standards](https://standards.ieee.org)
> - [The Open Group TOGAF](https://www.opengroup.org/togaf)
> - 核查日期：2026-07-07
