# FEA BRM 2.0 与 TOGAF 10 Phase B 业务能力图交叉映射

> **版本**: 2026-06-06
> **对齐来源**: FEA BRM 2.0 Release Document (OMB, 2003/2004), DoD EA BRM Supplement (2004), TOGAF Standard 10th Edition (2022), DoDAF 2.02 Reference Models

---

## 1. FEA BRM 2.0 概述

### 1.1 定位

联邦企业架构业务参考模型（Federal Enterprise Architecture Business Reference Model, FEA BRM 2.0）由美国白宫 OMB 于 2003 年 6 月发布，是 FEA 五大参考模型（PRM, BRM, SRM, DRM, TRM）的**业务层基石**。
其核心设计原则是：**以功能驱动（function-driven）描述联邦政府业务运营，而非以机构组织（agency-oriented）描述**。

> "The BRM defines a structure of the Federal Government's lines of business, including operations and services for the citizen, **independent of the organizations that perform them**." — OMB FEA BRM 2.0

### 1.2 三层层级结构

FEA BRM 2.0 采用严格的三层分解结构：

```text
Business Area（业务域）
    └── Line of Business（业务线, LOB）
            └── Sub-function（子功能）
```

| 层级 | 数量 | 说明 |
|-----|------|------|
| **Business Area** | 4 | 最高层分类，按政府运营目的划分 |
| **Line of Business** | 39 | 19 条外部业务线（面向公民服务）+ 20 条内部业务线（支持运营） |
| **Sub-function** | 153 | 最细粒度，描述具体业务功能 |

### 1.3 四层业务域（Business Areas）详述

```text
FEA BRM 2.0
├── A. Services for Citizens（公民服务）
│   ├── 01 Health（健康）
│   ├── 02 Education（教育）
│   ├── 03 Transportation（交通）
│   ├── 04 Homeland Security（国土安全）
│   ├── 05 Defense & National Security（国防与国家安全）
│   ├── 06 International Affairs（国际事务）
│   ├── 07 Energy（能源）
│   ├── 08 Natural Resources（自然资源）
│   ├── 09 Economic Development（经济发展）
│   ├── 10 Environmental Management（环境管理）
│   ├── 11 General Science & Innovation（科学与创新）
│   ├── 12 Law Enforcement（执法）
│   ├── 13 Litigation & Judicial Services（诉讼与司法）
│   ├── 14 Financial Management（财政管理）
│   ├── 15 Workforce Management（劳动力管理）
│   ├── 16 Housing（住房）
│   ├── 17 Income Security（收入保障）
│   ├── 18 Food & Nutrition（食品与营养）
│   └── 19 General Government（总务管理）
│
├── B. Mode of Delivery（交付模式）
│   ├── 20 Federal Financial Assistance（联邦财政援助）
│   ├── 21 Federal Asset Sales（联邦资产销售）
│   ├── 22 Credit & Insurance（信贷与保险）
│   ├── 23 Public Goods Creation & Management（公共产品创建与管理）
│   └── 24 Knowledge Creation & Management（知识创建与管理）
│
├── C. Support Delivery of Services（服务交付支持）
│   ├── 25 Legislative Relations（立法关系）
│   ├── 26 Public Affairs（公共事务）
│   ├── 27 Regulatory Development（法规制定）
│   ├── 28 Planning & Resource Allocation（规划与资源配置）
│   ├── 29 Revenue Collection（税收征管）
│   ├── 30 Budget & Finance（预算与财务）
│   ├── 31 Controls & Oversight（控制与监督）
│   ├── 32 Personnel Management（人事管理）
│   ├── 33 Supply Chain Management（供应链管理）
│   ├── 34 Health & Safety Management（健康与安全管理）
│   ├── 35 Information & Technology Management（信息技术管理）
│   ├── 36 Communications（通信）
│   ├── 37 Travel（差旅）
│   ├── 38 Training & Development（培训与发展）
│   ├── 39 Human Resource Development（人力资源开发）
│   └── 40 Administration Management（行政管理）
│
└── D. Management of Government Resources（政府资源管理）
    ├── 41 Financial Resources Management（财务资源管理）
    ├── 42 Information Resources Management（信息资源管理）
    ├── 43 Technology Resources Management（技术资源管理）
    ├── 44 Human Capital Management（人力资本管理）
    ├── 45 Real Property Assets Management（实物资产管理）
    ├── 46 Other Fixed Assets Management（其他固定资产管理）
    ├── 47 Materiel Assets Management（物资资产管理）
    ├── 48 Information Technology Assets Management（IT 资产管理）
    └── 49 National Defense & Security Assets Management（国防安全资产管理）
```

> **注**: 部分资料将 FEA BRM 2.0 描述为"五层"，实际是指 FEA 整体框架的五大参考模型（PRM, BRM, SRM, DRM, TRM）。BRM 本身内部为三层分解（Area → LOB → Sub-function），外加与 FEA 其他四层参考模型的横向对齐，形成完整的五维业务架构视图。

---

## 2. TOGAF 10 Phase B 业务能力图

### 2.1 Phase B 核心交付物

TOGAF 10 Phase B（Business Architecture）定义以下与业务能力相关的核心交付物：

| 交付物 | 内容 | 与 FEA BRM 的对应关系 |
|-------|------|---------------------|
| **Business Capability Map** | 企业能力的分层分类图 | 对应 FEA BRM 的 Area + LOB 层级 |
| **Value Stream Map** | 端到端价值交付序列 | 跨越多个 LOB 的 Sub-function 组合 |
| **Organization Map** | 组织单元与能力的映射 | FEA BRM 明确分离：功能 ≠ 机构 |
| **Information Map** | 信息概念与能力的关联 | 对应 FEA DRM 的横向对齐 |

### 2.2 TOGAF 业务能力分层

```text
Level 0: Enterprise Capability（企业能力）
    ├── Level 1: Capability Group（能力组）
    │       ├── Level 2: Capability（能力）
    │       │       ├── Level 3: Sub-capability（子能力）
    │       │       │       └── Level 4: Activity（活动）
```

---

## 3. FEA BRM → TOGAF Capability Map 交叉映射

### 3.1 层级映射矩阵

| FEA BRM 2.0 | TOGAF 10 Phase B | 映射说明 |
|------------|-----------------|---------|
| **Business Area** | Capability Group (L1) | 按业务目的划分的大类，如"公民服务"对应"客户价值交付能力组" |
| **Line of Business** | Capability (L2) | 动词+名词形式的能力，如"Health"→"管理公民健康" |
| **Sub-function** | Sub-capability (L3) / Activity (L4) | 细粒度能力或流程活动，如"Disease Surveillance"→"监测疾病爆发" |
| **Cross-agency Collaboration** | Value Stream | 多个 Sub-function 按价值流串联，如"灾难响应"价值流 |

### 3.2 具体映射示例

#### 示例 A：健康领域（Health LOB）

```text
FEA BRM 2.0: Health (LOB)
├── Sub-function: Disease Surveillance
├── Sub-function: Health Care Delivery
├── Sub-function: Public Health Promotion
├── Sub-function: Health Resource Allocation
└── Sub-function: Health Regulation

    ↓ 映射为

TOGAF Capability Map
└── Capability Group: 公民健康服务 (L1)
    └── Capability: 管理公民健康 (L2)
        ├── Sub-capability: 监测疾病爆发 (L3)
        │   └── Activity: 收集流行病学数据 (L4)
        ├── Sub-capability: 交付医疗服务 (L3)
        │   └── Activity: 协调医疗资源调度 (L4)
        ├── Sub-capability: 促进公共卫生 (L3)
        ├── Sub-capability: 配置健康资源 (L3)
        └── Sub-capability: 执行健康法规 (L3)
```

#### 示例 B：信息技术管理（Information & Technology Management LOB）

```text
FEA BRM 2.0: Information & Technology Management (LOB)
├── Sub-function: IT Policy & Planning
├── Sub-function: IT Security
├── Sub-function: IT Operations
├── Sub-function: Data Management
└── Sub-function: Application Management

    ↓ 映射为

TOGAF Capability Map
└── Capability Group: 数字化使能 (L1)
    └── Capability: 管理信息技术 (L2)
        ├── Sub-capability: 制定 IT 政策与规划 (L3)
        ├── Sub-capability: 保障信息安全 (L3)
        ├── Sub-capability: 运营 IT 基础设施 (L3)
        ├── Sub-capability: 治理数据资产 (L3)
        └── Sub-capability: 管理应用组合 (L3)
```

### 3.3 映射规则总结

| 规则编号 | 映射规则 | 说明 |
|---------|---------|------|
| M1 | **名词动词化** | FEA BRM 的 LOB 名称为名词（如 "Health"），映射为 TOGAF Capability 时需转换为"动词+名词"（如 "管理公民健康"） |
| M2 | **粒度对齐** | FEA Sub-function 若包含独立输入/输出/治理边界，映射为 L3 Sub-capability；若仅为活动步骤，映射为 L4 Activity |
| M3 | **组织解耦** | FEA BRM 的"独立于机构"原则与 TOGAF Capability Map 的"能力稳定性"公理完全对齐 |
| M4 | **价值流串联** | 跨越多个 FEA LOB 的端到端服务，在 TOGAF 中建模为 Value Stream（如"从灾难预警到灾后重建"） |
| M5 | **数据层对齐** | FEA BRM 的 Sub-function 需映射到 FEA DRM 的 Data Entities，再映射到 TOGAF Information Map |

---

## 4. 复用决策矩阵：何时复用 FEA BRM，何时自定义

### 4.1 决策矩阵

| 评估维度 | 复用 FEA BRM 业务线 | 自定义业务线 | 混合策略 |
|---------|------------------|-----------|---------|
| **组织性质** | 政府机构、公共部门、政府承包商 | 私营企业、非政府组织（NGO） | 受监管行业（如医疗、金融）参考 FEA 结构后定制 |
| **合规要求** | 必须对接联邦预算申报（OMB Exhibit 53/300） | 无政府合规要求 | 州/省级政府项目需局部映射 |
| **跨机构协作** | 需与其他联邦/州机构共享数据或服务 | 完全内部运营 | 与政府机构有数据交换的私营企业 |
| **能力稳定性** | 公共服务能力（健康、交通、执法）具有跨机构稳定性 | 核心竞争能力（如专有算法、品牌运营） | 支持性能力（IT、财务、HR）复用 FEA，核心能力自定义 |
| **架构成熟度** | 企业处于架构建设初期，需快速基准 | 已有成熟能力地图，仅需增量优化 | 并购整合场景：目标公司用 FEA，收购方保留自定义 |

### 4.2 决策树

```text
业务线复用决策
│
├── 1. 是否为公共部门或政府承包商?
│   ├── 是 → 强制对齐 FEA BRM 2.0，确保预算申报与跨机构分析合规
│   └── 否 → 继续
│
├── 2. 是否需要与政府机构进行系统级数据/服务交换?
│   ├── 是 → 采用"映射优先"策略：内部自定义能力地图 ↔ 对外 FEA BRM 映射层
│   └── 否 → 继续
│
├── 3. 该业务线是否属于支持性功能（IT、财务、HR、供应链）?
│   ├── 是 → 建议复用 FEA BRM 对应 LOB 作为基准，减少从零设计成本
│   └── 否 → 继续
│
├── 4. 该业务线是否涉及企业核心差异化竞争力?
│   ├── 是 → 自定义能力地图，FEA BRM 仅作参考
│   └── 否 → 继续
│
└── 5. 架构团队是否处于初创期（< 2 年）?
    ├── 是 → 复用 FEA BRM 作为加速器，缩短能力地图建设周期 40-60%
    └── 否 → 在现有能力地图上增量引用 FEA BRM Sub-function 作为细化补充
```

### 4.3 典型场景建议

| 场景 | 建议策略 | 理由 |
|-----|---------|------|
| **美国联邦机构 IT 现代化** | 强制复用 FEA BRM 2.0 + DoD Supplement | OMB Circular A-11 合规要求 |
| **州级 Medicaid 系统集成** | 复用 FEA "Health" + "Financial Management" LOB，自定义州级政策层 | 联邦结构 + 州级自治 |
| **大型银行监管报送** | 参考 FEA "Controls & Oversight" + "Regulatory Development"，映射到 BIAN 服务域 | 监管逻辑与政府审计逻辑同源 |
| **跨国制造企业政府业务部** | 对政府业务单元强制 FEA 对齐，商业单元保持 ISA-95 + 自定义 | 同一企业内双轨制架构 |
| **智慧城市项目** | 复用 FEA "Transportation" + "Environmental Management" + "Public Safety"，叠加 IoT 特定能力 | 政府主导项目的标准基线 |

---

## 5. FEA BRM 与 TOGAF 企业连续体的集成

### 5.1 在架构连续体中的定位

```text
TOGAF Architecture Continuum
├── Foundation Architectures（基础架构）
│   └── ...
├── Common Systems Architectures（通用系统架构）
│   └── ...
├── Industry Architectures（行业架构）
│   └── FEA BRM 2.0 ← 政府/公共部门行业的业务参考模型
│   └── eTOM ← 电信行业
│   └── ARTS ← 零售行业
│   └── BIAN ← 银行业
│
└── Organization-Specific Architectures（组织特定架构）
    └── 某联邦机构基于 FEA BRM 2.0 定制的业务能力地图
```

### 5.2 在解决方案连续体中的映射

| FEA BRM 元素 | 对应的解决方案构建块（SBB）示例 |
|-------------|---------------------------|
| Health Care Delivery (Sub-function) | Epic EHR, Cerner Millennium, VA VistA |
| Revenue Collection (LOB) | IRS 现代电子税务系统、州级税务平台 |
| IT Security (Sub-function) | zero trust 架构平台、FedRAMP 合规云 |
| Supply Chain Management (LOB) | SAP Ariba、Oracle Procurement Cloud |

---

## 6. 与 01 元模型标准的术语对齐

| 本文件术语 | `struct/01-meta-model-standards/` 对应术语 | 说明 |
|----------|----------------------------------------|------|
| Business Area | Capability Group (L1) | 对齐 TOGAF 10 能力分层 |
| Line of Business | Capability (L2) | 公理 2.1 定义的最小可复用业务语义单元 |
| Sub-function | Sub-capability / Activity | 粒度由价值创造边界决定，非组织结构 |
| Cross-agency Value Stream | Value Stream | 对齐 `03-value-stream/` 的价值流复用模型 |
| Decision Service | Business Service (ArchiMate) | 业务层与应用层的桥接点（定理 2.3） |

---

## 参考索引

- OMB: *The Business Reference Model Version 2.0* (2004-06) — [https://www.dragon1.com/downloads/fea_brm_release_document_rev_2.pdf](https://www.dragon1.com/downloads/fea_brm_release_document_rev_2.pdf)
- DoD: *DoD Enterprise Architecture Business Reference Model* (V0.4, 2004) — DoD Supplement to FEA BRM 2.0
- DoDAF 2.02: *DoD Architecture Framework* — Reference Models 章节对 FEA BRM 的权威解释
- The Open Group: *TOGAF Standard, 10th Edition* (2022) — Phase B: Business Architecture
- HHS OCIO: *EPLC Business Process Modeling Practices Guide* — FEA BRM 在卫生部门的实施指南
- Sessions, R.: *Simple Architectures for Complex Enterprises* (Microsoft Press, 2008) — FEA 五大参考模型关系论述
- Internet Policy (ScienceDirect): FEA BRM 2.0 作为跨机构分析框架的理论基础

---

> 最后更新: 2026-06-06
