# ISO/IEC/IEEE AWI 42030 修订跟踪

> **版本**: 2026-06-10
> **跟踪对象**: ISO/IEC/IEEE AWI 42030 — Architecture Evaluation Framework（第二版）
> **当前状态**: Under development（阶段 20.00）
> **上一版本**: ISO/IEC/IEEE 42030:2019（第一版，2019-07-24 发布）
> **核查日期**: 2026-06-10
> **来源 URL**: <https://www.iso.org/standard/93814.html>

---

## 目录

- [ISO/IEC/IEEE AWI 42030 修订跟踪](#isoiecieee-awi-42030-修订跟踪)
  - [目录](#目录)
  - [1. 修订背景](#1-修订背景)
  - [2. 修订状态](#2-修订状态)
    - [阶段追踪](#阶段追踪)
  - [3. 2019 版核心内容回顾](#3-2019-版核心内容回顾)
    - [3.1 架构评估（AE）三层框架](#31-架构评估ae三层框架)
    - [3.2 与 42020 的协同](#32-与-42020-的协同)
  - [4. 预期修订方向（基于社区讨论与标准趋势）](#4-预期修订方向基于社区讨论与标准趋势)
    - [4.1 可能的增强领域](#41-可能的增强领域)
    - [4.2 与 42010:2022 的一致性更新](#42-与-420102022-的一致性更新)
  - [5. 跟踪机制](#5-跟踪机制)
    - [5.1 自动跟踪建议](#51-自动跟踪建议)
    - [5.2 关键里程碑检查清单](#52-关键里程碑检查清单)
  - [6. 本项目应对策略](#6-本项目应对策略)
  - [补充说明：ISO/IEC/IEEE AWI 42030 修订跟踪](#补充说明isoiecieee-awi-42030-修订跟踪)
  - [概念定义](#概念定义)
  - [示例](#示例)
  - [反例](#反例)
  - [分析](#分析)

## 1. 修订背景

ISO/IEC/IEEE 42030:2019 自发布以来，已成为架构评估领域的核心国际标准。随着软件系统复杂度的提升、AI/ML 系统的兴起、以及系统之系统（SoS）架构的普及，2019 版在以下方面需要更新：

- **AI/ML 系统的架构评估**：传统评估方法难以处理概率性、数据依赖的 AI 架构
- **持续架构评估（Continuous Architecture Evaluation）**：DevOps/敏捷环境下，架构评估不再是阶段性活动
- **架构债务评估**：与技术债务（Technical Debt）概念联动
- **评估自动化**：工具链和度量的更新

---

## 2. 修订状态

| 属性 | 详情 |
|:---|:---|
| **标准编号** | ISO/IEC/IEEE AWI 42030 |
| **注册日期** | 2026-04-22（ISO 官网登记为新项目） |
| **当前阶段** | 20.00 — New project registered in TC/SC work programme |
| **版本** | 第二版（Edition 2） |
| **预计发布** | 2027-2028（基于 ISO 标准平均 18-24 个月开发周期估算） |
| **技术委员会** | ISO/IEC JTC 1/SC 7 — Software and systems engineering |

### 阶段追踪

```text
ISO 标准生命周期
├── 00 预备阶段 (Preliminary) ──→ 完成
├── 10 提案阶段 (Proposal) ──→ 完成
├── 20 准备阶段 (Preparatory) ──→ ✅ 当前（AWI 已注册）
├── 30 委员会阶段 (Committee) ──→ 待启动
├── 40 征求意见阶段 (Enquiry/DIS) ──→ 预计 2027 中
├── 50 批准阶段 (Approval/FDIS) ──→ 预计 2027 末
├── 60 发布阶段 (Publication) ──→ 预计 2028 初
└── 90 复审阶段 (Review) ──→ 2033 左右
```

---

## 3. 2019 版核心内容回顾

AWI 42030 的修订将在 2019 版基础上演进。回顾现有框架：

### 3.1 架构评估（AE）三层框架

| 层级 | 内容 | 复用视角映射 |
|:---|:---|:---|
| **目标层（Objectives）** | 评估目的、利益相关者关注点 | 复用决策的业务目标对齐 |
| **因素层（Factors）** | 质量属性、架构决策、风险 | 复用资产的质量特性评估（ISO 25010） |
| **方法层（Methods）** | 场景法、度量法、利益相关者评审 | 复用资产的兼容性验证方法 |

### 3.2 与 42020 的协同

42030 的通用 AE 框架支持 42020 中定义的 Architecture Evaluation 过程（第 9 章）。特定框架可派生自该通用框架，映射到：

- ISO/IEC/IEEE 15288（系统生命周期过程）
- ISO/IEC/IEEE 12207（软件生命周期过程）

---

## 4. 预期修订方向（基于社区讨论与标准趋势）

> ⚠️ 以下内容为基于标准演进趋势和学术社区讨论的**合理推测**，非 ISO 官方承诺。将在标准正式发布后更新。

### 4.1 可能的增强领域

| 领域 | 2019 版状态 | 预期修订方向 | 对本项目的影响 |
|:---|:---|:---|:---|
| **AI/ML 架构评估** | 未覆盖 | 新增对概率性系统、模型漂移、数据依赖架构的评估指南 | 需更新 12 AI 原生复用中的评估方法 |
| **持续评估** | 阶段性评估为主 | 嵌入 CI/CD 的自动化架构评估 | 与 13 平台工程（IDP Golden Path）联动 |
| **架构债务量化** | 未明确 | 引入技术债务的架构维度评估 | 与 06 跨层治理的升级/降级矩阵关联 |
| **供应链安全评估** | 未覆盖 | 架构的第三方依赖风险评估 | 与 10 供应链安全（SLSA/SBOM）深度整合 |
| **可持续性评估** | 未覆盖 | 架构的能源效率与碳足迹评估 | 与 13/07-green-software 联动 |
| **评估工具能力** | 高阶描述 | 更具体的工具支持要求（如架构数字孪生） | 与 11 工业 IoT 数字孪生复用交叉 |

### 4.2 与 42010:2022 的一致性更新

2019 版 42030 引用的是 42010:2011。修订版预计将：

- 全面采用 42010:2022 的术语体系（Architecture Description / Viewpoint / View / Model）
- 支持 42010:2022 新增的模型种类（Model Kind）和架构描述语言概念
- 与 DIS 42024（架构基础）和 DIS 42042（参考架构）协调

---

## 5. 跟踪机制

### 5.1 自动跟踪建议

建议通过以下渠道跟踪 AWI 42030 进展：

| 来源 | URL | 跟踪频率 |
|:---|:---|:---:|
| ISO 官网项目页 | <https://www.iso.org/standard/93814.html> | 季度 |
| ISO/IEC JTC 1/SC 7 会议报告 | <https://www.iso.org/committee/45086.html> | 半年 |
| IEEE Computer Society S2ESC | <https://sagroups.ieeecs.org/42030/> | 季度 |
| arc42 质量博客 | <https://quality.arc42.org/standards/iso-iec-ieee-42030> | 月度 |

### 5.2 关键里程碑检查清单

- [ ] 2026-Q3: 确认是否进入阶段 30（委员会阶段）
- [ ] 2027-Q2: 确认是否发布 DIS（阶段 40）
- [ ] 2027-Q4: 确认是否发布 FDIS（阶段 50）
- [ ] 2028-Q1: 确认正式发布（阶段 60）

---

## 6. 本项目应对策略

在 AWI 42030 正式发布前，建议采取以下策略：

1. **继续以 42030:2019 为评估框架基准**：2019 版仍然有效，且其三层框架（目标-因素-方法）已足够支撑当前复用评估需求
2. **预留 AI/ML 评估扩展位**：在 12/05-probabilistic-contracts 和 12/07-conformal-prediction 中预留与新版 42030 的对接接口
3. **跟踪但不等待**：Phase D（2027-Q2 起）将正式对齐新版 42030，不阻塞当前 Phase A-C 的推进

---

> **权威来源**:
>
> - [ISO/IEC/IEEE 42030:2019 — Architecture evaluation framework](https://www.iso.org/standard/73436.html) — ISO（核查日期：2026-07-08）
> - [ISO/IEC/IEEE AWI 42030 项目页](https://www.iso.org/standard/93814.html) — ISO Stage 20.00（核查日期：2026-07-08）
> - [IEEE 42030-2019 官方页面](https://standards.ieee.org/ieee/42030/7602/) — IEEE SA（核查日期：2026-07-08）
> - [arc42 Quality Blog: ISO/IEC/IEEE 42030:2019 Overview](https://quality.arc42.org/standards/iso-iec-ieee-42030)（核查日期：2026-07-08）
>
> **核查日期**: 2026-07-08


---

## 正向示例

某电信运营商在引入共享计费服务前，依据 ISO/IEC/IEEE 42030:2019 的三层框架（Objectives-Factors-Methods）组织 ATAM 评审：目标层明确“支持 1 亿并发用户”，因素层识别性能、安全、可维护性，方法层采用场景法与度量法。评估发现缓存层存在单点故障风险，提前引入 Redis Cluster 与熔断机制，避免了上线后事故。

## 反例/反模式

某项目为赶进度跳过架构评估，直接复用开源消息队列。上线后流量峰值触发消息积压与消费延迟，运维团队才发现该组件未满足可靠性要求。因缺乏 42030 评估记录，无法追溯当初是否将可靠性列为评估因素，修复成本是评估成本的 8 倍。

**避免建议**：任何进入组织资产库的共享组件，必须在复用前完成 42030 评估，并将 Objectives、Factors、Methods 与评估结论作为资产元数据归档。

## 标准条款映射

| 标准条款 | 核心内容 | 本文件对应 |
|---|---|---|
| ISO/IEC/IEEE 42030:2019, Clause 4.3 | Architecture evaluation tiers（目标/因素/方法） | 第 3.1 节三层框架 |
| ISO/IEC/IEEE 42030:2019, Clause 6.1 | Evaluation synthesis general requirements | 第 5 节跟踪机制 |
| ISO/IEC/IEEE 42030:2019, Clause 6.2 | Value assessment | 第 4 节预期修订方向 |
| ISO/IEC/IEEE 42020:2019, Clause 9 | Architecture Evaluation process | 第 3.2 节与 42020 的协同 |

## 权威来源与核查日期

> **权威来源**：
>
> - [ISO/IEC/IEEE 42030:2019 — Architecture evaluation framework](https://www.iso.org/standard/73436.html) — ISO（核查日期：2026-07-08）
> - [ISO/IEC/IEEE AWI 42030 项目页](https://www.iso.org/standard/93814.html) — ISO Stage 20.00（核查日期：2026-07-08）
> - [IEEE 42030-2019 官方页面](https://standards.ieee.org/ieee/42030/7602/) — IEEE SA（核查日期：2026-07-08）
> - [arc42 Quality Blog: ISO/IEC/IEEE 42030:2019 Overview](https://quality.arc42.org/standards/iso-iec-ieee-42030)（核查日期：2026-07-08）
>
> **核查日期**：2026-07-08
