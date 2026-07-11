# 01 业务域复用（Business Domain Reuse）

> **版本**: 2026-07-11
> **定位**: 由 `struct/02-business-architecture-reuse` 自动聚合生成的视角卷册（view volume）
> **生成命令**: `python scripts/sync-view-from-struct.py --topic 02-business-architecture-reuse --generate`
> **说明**: 本文件为 struct/ 的只读聚合视角，修改请直接在 struct/ 对应文件进行。

---


## 目录


1. [01 业务域复用（Business Domain Reuse）](../struct/02-business-architecture-reuse/01-business-domain-reuse/README.md)
2. [业务能力复用](../struct/02-business-architecture-reuse/02-business-capability/capability-reuse.md)
3. [FEA BRM 2.0 与 TOGAF 10 Phase B 业务能力图交叉映射](../struct/02-business-architecture-reuse/02-business-capability/fea-brm-togaf-mapping.md)
4. [价值流复用的形式化组合](../struct/02-business-architecture-reuse/03-value-stream/value-stream-composition.md)
5. [04 业务流程复用（Business Process Reuse）](../struct/02-business-architecture-reuse/04-business-process-reuse/README.md)
6. [05 业务服务复用（Business Service Reuse）](../struct/02-business-architecture-reuse/05-business-service-reuse/README.md)
7. [BPMN 2.0 / DMN 1.5 可执行语义案例集](../struct/02-business-architecture-reuse/06-bpmn-dmn/bpmn-dmn-executable-cases.md)
8. [BPMN 2.0 / DMN 业务过程与决策的复用编排](../struct/02-business-architecture-reuse/06-bpmn-dmn/bpmn-dmn-reuse-orchestration.md)
9. [DoDAF / UAF 1.3 / NAF 4.0 与软件架构复用视角映射](../struct/02-business-architecture-reuse/07-defense-mission-engineering/dodaf-uaf-reuse.md)
10. [NAF 4.0 / MODAF 与北约架构复用视角映射](../struct/02-business-architecture-reuse/07-defense-mission-engineering/naf-modaf-reuse.md)
11. [Zachman Framework 与软件架构复用映射文档](../struct/02-business-architecture-reuse/08-zachman-reuse-mapping/zachman-reusability-matrix.md)
12. [BIAN 金融服务域复用案例](../struct/02-business-architecture-reuse/case-studies/bian-banking-reuse-case.md)
13. [行业垂直场景案例库](../struct/02-business-architecture-reuse/case-studies/industry-vertical-cases.md)
14. [C-06 TMForum ODF / eTOM 电信架构复用](../struct/02-business-architecture-reuse/case-studies/tmforum-telecom-reuse.md)
15. [02 业务架构复用](../struct/02-business-architecture-reuse/README.md)

---


<!-- SOURCE: struct/02-business-architecture-reuse/01-business-domain-reuse/README.md -->

# 01 业务域复用（Business Domain Reuse）

> **版本**: 2026-06-12
> **定位**: 02-business-architecture-reuse / 01-business-domain-reuse
> **对齐标准**: TOGAF Standard 10 Business Architecture, BMM (Business Motivation Model), FEA BRM

---

## 核心概念

业务域复用关注**最粗粒度**的业务能力组织：如何在企业层面识别、封装和复用业务域（Business Domain）。它与领域驱动设计（DDD）的战略模式相通，但更强调跨项目、跨系统的业务能力资产化。

| 概念 | 定义 | 复用价值 |
|:---|:---|:---|
| **业务域（Business Domain）** | 企业为达成特定业务目标而需要的一组连贯业务能力 | 作为能力投资组合的边界单元 |
| **业务能力（Business Capability）** | 企业为达成特定成果而具备的能力，通常稳定且独立于组织结构 | 跨系统复用的核心抽象 |
| **业务实体（Business Entity）** | 域内关键信息对象，如客户、订单、产品 | 数据模型复用的基础 |
| **价值流（Value Stream）** | 端到端交付价值的活动序列 | 识别复用机会的过程视图 |

---

## 复用模式

1. **域级参考模型复用**
   - 采用行业参考模型（如 FEA BRM、APQC PCF、BIAN 服务域）作为起点
   - 根据组织特点裁剪，形成企业级业务能力地图

2. **业务能力目录复用**
   - 建立分层能力目录（L1 域 → L2 能力 → L3 子能力 → L4 活动）
   - 通过能力热力图识别重复建设和高复用潜力领域

3. **业务实体共享服务**
   - 将跨域共享的实体（如 Party、Product、Location）上升为 enterprise canonical model
   - 通过主数据管理（MDM）或数据网格实现实体复用

---

## 检查清单

- [ ] 是否绘制了企业级业务能力地图？
- [ ] 业务域边界是否基于稳定的能力而非易变的组织/系统？
- [ ] 关键业务实体是否已识别并定义 canonical model？
- [ ] 是否评估了各能力的复用成熟度和投资回报？
- [ ] 域间依赖是否清晰，避免循环依赖？

---

## 关联主题

- `02-business-architecture-reuse/02-business-capability/` — 业务能力建模细化
- `02-business-architecture-reuse/03-value-stream/` — 价值流驱动的复用机会识别
- `02-business-architecture-reuse/04-business-process-reuse/` — 业务流程级复用
- `03-application-architecture-reuse/` — 业务能力到应用架构的映射


---

## 补充说明：01 业务域复用（Business Domain Reuse）

## 示例

**示例**：BIAN 银行业架构参考模型将银行业务划分为 300+ 业务服务组件，为银行数字化转型提供可复用的领域蓝图。

## 反例

**反例**：将其他行业的“库存管理”模型直接套用于航空维修备件管理，忽视行业法规与生命周期差异，导致模型失真。

## 权威来源

> **权威来源**:
>
> - [BIAN](https://www.bian.org)
> - [The Open Group TOGAF](https://www.opengroup.org/togaf)
> - 核查日期：2026-07-07

## 分析

**分析**：业务域复用强调领域知识的沉淀，过早抽象或过晚抽象都会削弱复用价值。

---


<!-- SOURCE: struct/02-business-architecture-reuse/02-business-capability/capability-reuse.md -->

# 业务能力复用

> **版本**: 2026-07-08
> **定位**: 将业务能力作为业务架构复用的核心单元
> **对齐标准**: TOGAF Standard 10, FEA BRM 2.0, ArchiMate 4.0, Zachman Framework

---

## 1. 业务能力的本质

**定义 2.1** (Business Capability): 业务能力是企业为达成特定结果而具备的**稳定能力**。它不依赖于具体的组织、流程、技术或实现。

形式化：

```text
Capability := ⟨What, Why, Outcome, Maturity, Owner⟩

What: 能力做什么（动词+名词，如"管理订单"）
Why: 存在的业务理由
Outcome: 可度量的业务成果
Maturity: 能力成熟度等级
Owner: 能力所有者
```

> **公理 2.1** (Capability Atomicity): 业务能力的可复用性与其粒度成反比，与其稳定性成正比。
>
> - 粒度过大：难以在不同上下文中复用
> - 粒度过小：复用价值不足以抵消管理成本
> - 不稳定：需求频繁变化，复用基础不存在

---

## 2. 业务能力层级

```text
Level 0: 企业能力（Enterprise Capability）
    ├── Level 1: 能力组（Capability Group）
    │       ├── Level 2: 能力（Capability）
    │       │       ├── Level 3: 子能力（Sub-capability）
    │       │       │       └── Level 4: 活动（Activity）
```

**示例**: 零售企业能力地图

```text
├── 战略与治理
├── 产品开发
├── 供应链管理
│   ├── 采购
│   ├── 库存管理
│   ├── 物流配送
│   └── 供应商管理
├── 销售与营销
│   ├── 客户获取
│   ├── 订单管理
│   ├── 定价管理
│   └── 促销活动
├── 客户服务
└── 财务管理
```

---

## 3. 业务能力复用的判定

```text
业务能力复用判定
│
├── 1. 稳定性判定
│   ├── 该能力在过去 2 年中是否发生过结构性变化？
│   │   ├── 是 → 复用价值低
│   │   └── 否 → 继续
│   └── 该能力是否与企业的核心价值链相关？
│       ├── 否 → 可考虑外包而非复用
│       └── 是 → 继续
│
├── 2. 通用性判定
│   ├── 该能力是否在多个业务单元/产品线中存在？
│   │   ├── 否 → 复用范围受限
│   │   └── 是 → 继续
│   └── 不同上下文中，该能力的"做什么"是否一致？
│       ├── 否 → 可能不是同一能力
│       └── 是 → 继续
│
├── 3. 实现可行性判定
│   ├── 是否存在至少一种技术实现？
│   ├── 该实现是否能被多个上下文消费？
│   └── 复用该实现的成本是否低于重复建设？
│       ├── 否 → 暂缓复用
│       └── 是 → 纳入复用资产目录
│
└── 输出: 复用等级（企业级 / 领域级 / 项目级 / 不建议）
```

---

## 4. 业务能力到 IT 实现的映射

```text
业务能力 "订单管理"
    ├── 业务服务: Order Management Service
    │       ├── 应用服务: createOrder, cancelOrder, getOrderStatus
    │       ├── 组件: OrderRepository, PaymentGateway, InventoryClient
    │       └── 功能: validateOrder, calculateTotal, sendNotification
    │
    ├── 价值流: "订单到现金" 中的核心阶段
    │
    └── 业务对象: Order, OrderLine, Customer, Payment
```

> **定理 2.3** (Business-Application Bridging): 业务服务是业务架构与应用架构的**桥接点**。当业务服务的技术实现契约稳定时，业务层与应用层解耦；当业务服务频繁变更时，两层耦合度指数上升。

---

## 5. 业务能力目录模板

| 字段 | 说明 | 示例 |
|------|------|------|
| 能力 ID | 唯一标识 | BC-SCM-003 |
| 能力名称 | 动词+名词 | 管理库存 |
| 父能力 | 上级能力 | 供应链管理 |
| 业务价值 | 为什么需要这个能力 | 确保可用库存满足客户需求 |
| KPI | 如何度量 | 库存周转率、缺货率 |
| 成熟度 | L1-L5 | L3 |
| 所有者 | 业务负责人 | 供应链总监 |
| 复用状态 | 企业级/领域级/项目级 | 企业级 |
| 相关 IT 服务 | 实现该能力的服务 | InventoryService |

---

## 6. 业务能力复用属性与成熟度模型

### 6.1 形式化定义

**定义** (Business Capability Reuse): 业务能力复用是指将企业中**稳定、通用、可度量**的业务能力单元作为可复用资产，在多个业务线、产品、流程或系统中共享其定义、行为、数据契约和价值度量，从而避免重复建设、加速业务创新并降低架构复杂度的实践。

```text
CapabilityReuse(C) := ⟨C, M(C), V(C), Gov(C)⟩

C: 业务能力单元
M(C): C 的成熟度模型（Level 1-5）
V(C): C 的价值度量集合（成本节约、上市时间、质量提升）
Gov(C): C 的治理主体、生命周期与版本策略
```

### 6.2 核心属性

| 属性 | 说明 | 可观察指标 | 重要性 |
|---|---|---|---|
| 稳定性 | 能力边界和核心语义随时间变化的程度 | 过去 24 个月结构性变更次数 | 高 |
| 通用性 | 能力在多个业务上下文中的适用程度 | 使用业务线/系统数量 | 高 |
| 原子性 | 能力粒度的适中性 | 能力分解到子能力的层级数 | 高 |
| 价值可度量性 | 能力成果可被量化评估的程度 | KPI 覆盖率、ROI 可追溯性 | 高 |
| 独立性 | 能力实现与组织结构、技术栈解耦程度 | 组织变更时的影响范围 | 中 |
| 可组合性 | 能力与其他能力组合形成价值流的能力 | 接口契约标准化程度 | 中 |

### 6.3 成熟度模型

| 成熟度等级 | 特征 | 复用表现 |
|---|---|---|
| L1 初始级 | 能力以职能或项目形式存在，无统一目录 | 复用靠个人关系，无治理 |
| L2 已管理级 | 部门级能力地图建立，但跨部门不一致 | 部门内复用，跨部门重复建设 |
| L3 已定义级 | 企业级统一能力地图，与价值流、IT 服务映射 | 跨部门复用，有标准接口 |
| L4 量化管理级 | 能力有明确 KPI、成本、质量度量 | 基于数据决策复用投资 |
| L5 优化级 | 能力持续演进，驱动业务创新 | 能力资产化，可对外输出 |

---

## 7. 与权威框架/标准的条款映射

| 框架/标准 | 对应概念 | 条款/章节 | 映射说明 |
|---|---|---|---|
| TOGAF 10 | Business Capability | Phase B §B.3.3, Content Metamodel | 业务能力映射到 TOGAF 内容元模型中的 Business Capability；Organization Unit 映射到能力的 Owner；Function 映射到能力下的活动 |
| TOGAF 10 | ABB / SBB | ADM Phase C/D | 业务能力定义为 ABB（架构构建块），具体 IT 实现为 SBB（解决方案构建块） |
| FEA BRM 2.0 | Line of Business / Sub-function | 五层业务线结构 | FEA BRM 的业务线（LoB）映射为能力组（Level 1），子功能映射为具体能力（Level 2-3） |
| ArchiMate 4.0 | Capability / Resource / Value | §5 Business Layer, §7.2 Capability | ArchiMate 的 Capability 与本概念等价；Resource 为能力实现；Value 为能力创造的价值 |
| Zachman Framework | What / How (Business Perspective) | C2-1, C2-2 | 业务能力映射到 Zachman 矩阵的"业务视角-做什么"与"业务视角-怎么做" |

---

## 8. 设计模式与反模式

### 8.1 业务能力-流程-服务映射矩阵

业务能力、业务流程与业务服务形成"能力 → 流程 → 服务"的层次映射：

| 概念 | 关注点 | 复用形态 | 与业务能力的关系 |
|---|---|---|---|
| 业务能力 | 做什么（What） | 能力目录、能力地图 | 核心复用单元 |
| 业务流程 | 怎么做（How） | 流程模板、BPMN 模型 | 能力的时序化执行 |
| 业务服务 | 如何调用（Interface） | API 契约、服务目录 | 能力的接口化封装 |
| 价值流 | 端到端价值（Value） | 价值流模板 | 能力的有序组合 |
| 业务对象 | 数据语义（Data） | 数据模型、Schema | 能力操作的核心实体 |

> **映射规则**：一个业务能力可由多条业务流程实现，每条流程通过一组业务服务对外暴露。稳定的业务服务契约使能力复用跨越技术与组织边界。

### 8.2 正例：跨渠道客户身份验证能力复用

**背景**：某银行在移动 App、网上银行、柜台、客服热线四个渠道分别建设了客户身份验证功能，导致：

- 各渠道验证规则不一致，同一客户在不同渠道体验差异大。
- 安全策略更新需要在四个系统分别修改，风险高。
- 监管审计时难以证明全渠道身份验证的合规性。

**复用实践**：

1. 建立企业级业务能力 **"验证客户身份"（BC-CUST-001）**，定义统一的能力边界和成果：确认客户身份的真实性。
2. 将能力拆分为子能力：证件 OCR、人脸识别、短信/邮箱 OTP、密码校验、风险评分。
3. 各渠道通过统一身份验证服务调用该能力，仅保留渠道特定的 UI/UX 和接入适配。
4. 能力 Owner 由安全与零售部门联合担任，统一制定验证策略和升级规则。

**效果**：

- 新增渠道（如小程序）接入身份验证的时间从 3 个月缩短至 2 周。
- 安全策略更新一次生效全渠道，风险事件响应时间缩短 60%。
- 监管合规审计时，可统一展示身份验证能力的覆盖率与执行日志。

### 8.3 正例：跨国零售企业的订单管理能力复用

**背景**：某跨国零售企业在亚太、欧洲、北美三大区域运营，各区域独立建设"订单管理"系统。

**复用实践**：

1. 建立企业级"订单管理"业务能力（BC-SCM-005），定义统一的能力边界和成果。
2. 将"订单捕获""订单校验""库存预留""订单履约"等子能力标准化。
3. 各区域保留"区域税务计算""本地支付方式"等变体能力。
4. 统一能力通过 API 目录暴露给各区域系统。

**效果**：

- 新促销规则上线时间从 6 周缩短至 1 周。
- 跨区域客户体验一致性评分提升 35%。
- 订单相关 IT 维护成本降低 28%。

### 8.4 反例：将组织职能直接建模为业务能力

**场景**：某公司将"市场部审批""财务部复核""法务部审核"直接建模为业务能力。

**问题**：

- 能力边界随组织架构调整而频繁变化。
- 当市场部拆分为"品牌市场"和"数字市场"后，原"市场部审批"能力失效。
- 能力复用性极低，因为每个能力都绑定了特定组织单元。

**后果**：

- 业务能力地图每半年需大规模重构。
- 基于能力的 IT 规划无法稳定执行。
- 团队对能力建模失去信心。

**避免建议**：

- 业务能力命名应采用**动词+名词**（如"审批营销方案"），而非"部门+动作"。
- 能力定义应聚焦**业务成果**（outcome），而非执行主体。
- 组织角色应映射到能力的 Who 维度，而非能力本身。

### 8.5 反例：能力目录过度工程化

**场景**：某企业在业务能力映射项目中，将能力分解到 5-6 层，产生超过 3000 个能力条目，每个条目都要求填写 20 多个字段。

**问题**：

- 能力粒度过细，许多"能力"实际上只是流程步骤或系统功能。
- 能力目录维护成本极高，半年后就出现大量过期和冲突条目。
- 业务人员难以理解能力地图，IT 规划时仍然回到系统视角。

**后果**：

- 能力目录成为"象牙塔产物"，实际项目很少引用。
- 投入大量人力建设的能力管理平台 ROI 为负。
- 团队对业务能力建模方法产生质疑。

**避免建议**：

- 能力分解一般不超过 4 层（企业 → 能力组 → 能力 → 子能力）。
- 优先识别高稳定性、高通用性的能力，避免为每个流程步骤都创建能力条目。
- 能力目录应与实际项目规划、预算、架构评审挂钩，确保"建之有用"。

---

## 9. 权威来源与交叉引用

> **权威来源**:
>
> - [The Open Group TOGAF Standard, 10th Edition](https://www.opengroup.org/togaf) — TOGAF Standard 10 Phase B 业务能力定义；核查日期：2026-07-08
> - [FEA BRM 2.0](https://obamawhitehouse.archives.gov/omb/e-gov/fea) — 联邦企业架构业务参考模型；核查日期：2026-07-08
> - [ArchiMate 4.0 Specification](https://pubs.opengroup.org/architecture/archimate4-doc/) — ArchiMate 业务层 Capability / Value Stream；核查日期：2026-07-08
> - [Zachman Framework](https://www.zachman.com/) — 企业架构 What/How 维度；核查日期：2026-07-08
>
> **核查日期**: 2026-07-08

**交叉引用**：

- [FEA BRM 2.0 与 TOGAF Standard 10 Phase B 业务能力图交叉映射](../struct/02-business-architecture-reuse/02-business-capability/fea-brm-togaf-mapping.md) — 业务能力与标准框架的详细映射
- [价值流复用的形式化组合](../struct/02-business-architecture-reuse/03-value-stream/value-stream-composition.md) — 能力如何组合为价值流
- [Zachman Framework 与软件架构复用映射](../struct/02-business-architecture-reuse/08-zachman-reuse-mapping/zachman-reusability-matrix.md) — 能力在 Zachman 矩阵中的位置
- [BIAN 金融服务域复用案例](../struct/02-business-architecture-reuse/case-studies/bian-banking-reuse-case.md) — 银行业能力复用实践

---


<!-- SOURCE: struct/02-business-architecture-reuse/02-business-capability/fea-brm-togaf-mapping.md -->

# FEA BRM 2.0 与 TOGAF 10 Phase B 业务能力图交叉映射

> **版本**: 2026-06-06
> **对齐来源**: FEA BRM 2.0 Release Document (OMB, 2003/2004), DoD EA BRM Supplement (2004), TOGAF Standard 10 (2022), DoDAF 2.02 Reference Models

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

- OMB: *The Business Reference Model Version 2.0* (2004-06) — [https://obamawhitehouse.archives.gov/omb/e-gov/fea](https://obamawhitehouse.archives.gov/omb/e-gov/fea)（归档页含 FEA/BRM 系列文档链接；原 dragon1 PDF 镜像仍可作为历史副本引用）
- DoD: *DoD Enterprise Architecture Business Reference Model* (V0.4, 2004) — DoD Supplement to FEA BRM 2.0
- DoDAF 2.02: *DoD Architecture Framework* — Reference Models 章节对 FEA BRM 的权威解释
- The Open Group: *TOGAF Standard 10* (2022) — Phase B: Business Architecture
- HHS OCIO: *EPLC Business Process Modeling Practices Guide* — FEA BRM 在卫生部门的实施指南
- Sessions, R.: *Simple Architectures for Complex Enterprises* (Microsoft Press, 2008) — FEA 五大参考模型关系论述
- Internet Policy (ScienceDirect): FEA BRM 2.0 作为跨机构分析框架的理论基础

---

> 最后更新: 2026-06-06


---

## 补充说明：FEA BRM 2.0 与 TOGAF 10 Phase B 业务能力图交叉映射

## 反例

**反例**：将“市场部审批流程”直接建模为业务能力，导致能力边界随组织调整频繁变化，无法稳定复用。

## 权威来源

> **权威来源**:
>
> - [The Open Group TOGAF](https://www.opengroup.org/togaf)
> - [FEA BRM](https://www.govloop.com/community/blog/federal-enterprise-architecture/)
> - 核查日期：2026-07-07


---


<!-- SOURCE: struct/02-business-architecture-reuse/03-value-stream/value-stream-composition.md -->

# 价值流复用的形式化组合

> **版本**: 2026-07-08
> **对齐标准**: TOGAF Value Stream, ArchiMate 4.0 Value Stream, SAFe, BPMN 2.0
> **定位**: 将价值流复用形式化为业务能力的有序组合

---

## 核心概念定义

价值流复用是指将端到端价值交付路径抽象为业务能力的有序组合，并在不同上下文（行业、产品线、区域）中通过适配接口契约与变性点实现复用的实践。价值流由能力阶段、阶段间接口契约与价值度量三元组构成。

## 正向复用案例

订单到现金（Order-to-Cash）是价值流复用的经典场景：零售、B2B 与订阅业务可共享“接收订单 → 信用检查 → 库存分配 → 发货 → 开票 → 收款”主干价值流，仅通过替换个别阶段或适配接口契约即可满足差异化需求。

## 1. 价值流的基本形式化

**定义 VS.1** (价值流): 价值流 V 是一个有序三元组 ⟨C, I, K⟩，其中：

- `C = {C₁, C₂, ..., Cₙ}`: 业务能力的有限集合
- `I = {I₁₂, I₂₃, ..., Iₙ₋₁ₙ}`: 阶段间接口契约集合
- `K = {K₁, K₂, ..., Kₙ}`: 每个阶段创造的价值度量集合

**定义 VS.2** (价值流复用): 价值流 V₁ 可复用于上下文 Ctx，当且仅当：

1. C(V₁) ∩ C(Ctx) ≠ ∅（能力交集非空）
2. I(V₁) 与 I(Ctx) 可适配
3. K(V₁) 满足 K(Ctx) 的最低价值要求

---

## 2. 价值流组合定理

> **定理 2.1** (Value Stream Composition): 若价值流 V 由阶段 {S₁, S₂, ..., Sₙ} 组成，且每个 Sᵢ 对应业务能力 Cᵢ，则 V 的复用等价于 {Cᵢ} 的**有序组合**加上**阶段间契约** {Iᵢ,ᵢ₊₁} 的复用。

形式化：

```text
Reuse(V) = Reuse({C₁, C₂, ..., Cₙ}) ∪ Reuse({I₁₂, I₂₃, ..., Iₙ₋₁ₙ})

其中:
- Reuse({Cᵢ}) 表示业务能力的有序调用
- Reuse({Iᵢ,ᵢ₊₁}) 表示阶段间数据/控制流的适配
```

**证明概要**：

- 价值流的本质是业务能力按时间顺序的执行序列
- 若各业务能力独立可复用，则其有序组合亦可复用
- 阶段间契约保证组合的语义正确性
- 缺少阶段间契约的组合是能力的简单堆砌，不是价值流

---

## 3. 经典价值流示例：订单到现金（Order-to-Cash）

```text
价值流: 订单到现金
├── S1: 接收订单
│   ├── 能力: 订单捕获 (Order Capture)
│   ├── 价值: 客户需求被记录
│   └── 接口 I₁₂: 订单数据（客户、产品、数量、价格）
│
├── S2: 信用检查
│   ├── 能力: 信用评估 (Credit Assessment)
│   ├── 价值: 交易风险被量化
│   └── 接口 I₂₃: 信用状态（通过/拒绝/待审）
│
├── S3: 库存分配
│   ├── 能力: 库存管理 (Inventory Management)
│   ├── 价值: 物理商品被预留
│   └── 接口 I₃₄: 库存预留确认
│
├── S4: 发货
│   ├── 能力: 物流配送 (Logistics Fulfillment)
│   ├── 价值: 商品在途
│   └── 接口 I₄₅: 发货通知 + 追踪号
│
├── S5: 开票
│   ├── 能力: 账单管理 (Billing Management)
│   ├── 价值: 应收账款建立
│   └── 接口 I₅₆: 发票数据
│
└── S6: 收款
    ├── 能力: 收款处理 (Payment Processing)
    └── 价值: 现金回笼
```

**复用分析**：

- 所有 6 个能力在零售、B2B、订阅业务中均可复用
- 阶段间契约（订单数据格式、信用状态枚举）需要标准化
- 订阅业务中 S3（库存分配）可能替换为 S3'（服务席位分配），但接口契约仍需兼容

---

## 4. 价值流复用的变性管理

| 变性类型 | 说明 | 复用策略 |
|----------|------|----------|
| **阶段数量调整** | 某些行业需要额外阶段 | 插入可选阶段，保持主干价值流不变 |
| **并行/串行切换** | 某些阶段可并行执行 | 定义阶段间的依赖关系图（而非简单线性） |
| **交付物格式差异** | 不同行业的输出格式不同 | 使用标准化数据契约 + 格式适配器 |
| **参与者角色映射** | 同一阶段由不同角色执行 | 角色抽象为泳道参数 |
| **SLA 差异** | 不同场景对时效要求不同 | SLA 作为阶段的非功能属性参数化 |

---

## 5. 价值流复用的判定树

```text
价值流复用判定
│
├── 1. 能力覆盖判定
│   ├── V 的业务能力集合 C(V) ⊇ Ctx 的需求能力集合 C(Ctx) ?
│   │   ├── 否 → 部分复用 / 能力缺口分析
│   │   └── 是 → 继续
│   └── 能力级别匹配: L(Cᵢ) ≥ L(Ctxᵢ) ?
│       ├── 否 → 能力升级 / 降级使用
│       └── 是 → 继续
│
├── 2. 接口契约判定
│   ├── V 的阶段间契约 I(V) 与 Ctx 的接口需求可适配?
│   │   ├── 否 → 设计适配层 / 重构接口
│   │   └── 是 → 继续
│   └── 数据格式、协议、SLA 是否兼容?
│       ├── 否 → 数据转换 / 协议桥接
│       └── 是 → 继续
│
├── 3. 价值守恒判定
│   ├── ∀Sᵢ ∈ V: V(S'ᵢ) ≥ V(Sᵢ) ?
│   │   ├── 否 → 替换将导致价值流退化，需重新设计
│   │   └── 是 → 继续
│   └── 端到端价值交付时间是否满足 Ctx 要求?
│       ├── 否 → 优化关键路径 / 并行化
│       └── 是 → 授权复用
│
└── 输出: 复用决策 + 适配设计 + 风险登记
```

---

## 6. 关键公理

> **公理 2.2** (Value Stream Conservation): 价值流中的价值总量守恒。若阶段 Sᵢ 被替换为 S'ᵢ，则必须保证 V(S'ᵢ) ≥ V(Sᵢ)，否则价值流整体退化。
> **定理 2.2** (Process-Service Duality): 业务流程是**时序化**的业务服务编排；业务服务是**接口化**的业务流程封装。二者在复用视角下构成对偶关系：Process = ∫Service dt; Service = dProcess/dt。
> **定理 2.3** (Business-Application Bridging): 业务服务是业务架构与应用架构的**桥接点**。当业务服务的技术实现契约稳定时，业务层与应用层解耦；当业务服务频繁变更时，两层耦合度指数上升。

---

## 7. 价值流组合模式

### 7.1 模式 1：线性顺序组合

最基本的组合模式，阶段按严格顺序执行。

```mermaid
flowchart LR
    A[触发事件] --> S1[阶段1：能力 C1]
    S1 --> I1[接口 I12]
    I1 --> S2[阶段2：能力 C2]
    S2 --> I2[接口 I23]
    I2 --> S3[阶段3：能力 C3]
    S3 --> V[价值交付]
```

### 7.2 模式 2：并行-汇聚组合

多个阶段可同时执行，全部完成后汇聚到下一阶段。

```mermaid
flowchart LR
    A[触发事件] --> S1[阶段1]
    S1 --> S2[阶段2a]
    S1 --> S3[阶段2b]
    S2 --> S4[汇聚阶段3]
    S3 --> S4
    S4 --> V[价值交付]
```

### 7.3 模式 3：条件分支组合

根据阶段输出或外部条件选择不同路径。

### 7.4 模式 4：可插拔阶段组合

主干价值流保持不变，某些阶段根据场景插入或跳过。

### 7.5 模式 5：循环反馈组合

价值流的最后一个阶段将反馈信息传递回早期阶段，形成持续改进闭环。

```mermaid
flowchart LR
    A[触发事件] --> S1[阶段1: 需求识别]
    S1 --> S2[阶段2: 方案设计]
    S2 --> S3[阶段3: 交付实施]
    S3 --> S4[阶段4: 反馈度量]
    S4 -->|优化建议| S1
    S4 --> V[价值交付]
```

### 7.6 模式 6：事件驱动组合

价值流的推进不由预设顺序决定，而由业务事件触发。

---

## 8. 价值流与业务能力/业务流程/业务服务的映射

| 概念 | 核心关注点 | 在价值流中的角色 | 复用形式 |
|---|---|---|---|
| 价值主张 | 为何做（Why） | 价值流的起点与终点 | 价值主张画布、商业模式 |
| 业务能力 | 做什么（What） | 价值流每个阶段的执行主体 | 能力目录、能力服务 |
| 业务流程 | 怎么做（How） | 能力在特定场景下的具体执行步骤 | BPMN 流程模板 |
| 业务服务 | 如何调用（Interface） | 阶段之间的接口契约 | OpenAPI / gRPC 契约 |
| 业务对象 | 操作什么（Data） | 阶段间传递的数据语义 | 数据模型、Schema |
| 价值度量 | 价值多大（KPI） | 阶段与端到端价值评估 | KPI 仪表盘、SLA |

> **映射规则**：价值流阶段 → 业务能力 → 业务流程 → 业务服务 → 业务对象。阶段之间的接口契约必须保持稳定，否则价值流复用将退化为系统集成的点对点适配。

---

## 9. 与权威框架/标准的条款映射

| 框架/标准 | 对应概念 | 条款/章节 | 映射说明 |
|---|---|---|---|
| TOGAF 10 | Value Stream | Phase B, Business Architecture | TOGAF 价值流描述端到端价值交付，由业务能力阶段组成 |
| ArchiMate 4.0 | Value Stream | §7.3 Value Stream | ArchiMate Value Stream 与本概念等价，可关联 Capability、Business Process |
| BPMN 2.0 | Process / Collaboration | §8 Process, §10 Collaboration | 价值流的可执行编排由 BPMN Process 承载，跨组织协作由 Collaboration 承载 |
| DMN 1.5 | Decision Service | §6 Decision Requirements, §8 Decision Table | 价值流中的条件分支与决策规则由 DMN 决策服务承载 |
| SAFe | Operational Value Stream | SAFe 6.0 Value Streams | 运营价值流（Operational Value Stream）定义端到端交付活动序列 |

---

## 10. 正例与反例

### 10.1 正例：保险公司的理赔价值流复用

**背景**：某保险公司在财产险、健康险、车险三条产品线分别建设了理赔系统，流程差异大但核心价值创造路径相似。

**复用实践**：

1. 定义统一理赔价值流：报案 → 查勘 → 定损 → 核赔 → 赔付。
2. 将每条产品线特定的阶段抽象为"可插拔变体"：
   - 车险：查勘阶段包含现场查勘和远程视频查勘
   - 健康险：查勘阶段包含医疗费用审核
   - 财产险：定损阶段包含第三方评估
3. 统一接口契约（报案号、理赔状态、赔付金额）。
4. 建立价值流模板库，新产品线只需选择变体。

**效果**：

- 新产品理赔流程设计时间从 3 个月缩短至 3 周
- 理赔处理成本降低 22%
- 客户满意度提升 18%

### 10.2 正例：制造业订单到交付价值流复用

**背景**：某制造业集团在亚太、欧洲、北美拥有多个工厂，各工厂独立设计"订单到交付（Order-to-Delivery, OTD）"流程。

**复用实践**：

1. 定义集团级 OTD 价值流：订单确认 → 生产排程 → 物料准备 → 生产制造 → 质量检验 → 物流配送 → 交付签收。
2. 将每个阶段映射到标准化业务能力：订单管理、生产计划、物料管理、质量管理、物流配送。
3. 各工厂保留本地变体：如欧洲工厂增加 GDPR 合规检查，亚太工厂支持多语言发票。
4. 通过统一事件总线和接口契约（订单状态、物流追踪号）实现跨区域协同。

**效果**：

- 新产品 OTD 流程设计时间从 8 周缩短至 2 周。
- 跨区域订单交付准时率提升 15%。
- 库存周转率提升 12%，缺货率下降 8%。

## 反例

### 10.3 反例：价值流与系统边界错位

**场景**：某电商公司将"订单到收款"价值流按现有系统边界切分为：前端系统负责"下单"、OMS 负责"订单处理"、WMS 负责"发货"、财务系统负责"开票收款"。

**问题**：

- 价值流在系统边界处断裂，每个系统只关注自己的"完成"。
- 客户退货时，需要在四个系统中分别操作，状态不一致。
- 端到端价值（客户满意、现金回笼）无人负责。

**后果**：

- 退货处理周期长达 7-10 天
- 客户投诉中 40% 与"状态不透明"相关
- 财务对账困难，应收账款账龄延长

**避免建议**：

- 价值流设计应**以价值交付为中心**，而非以系统边界为中心。
- 建立端到端价值流 Owner，跨越系统边界协调。
- 使用统一事件总线保持跨系统状态一致性。

### 10.4 反例：价值流过度泛化

**场景**：某企业在构建价值流目录时，将"员工入职""IT 服务请求""供应商付款"等差异巨大的流程都纳入同一个"端到端服务价值流"。

**问题**：

- 价值流边界模糊，阶段定义过于抽象，无法指导具体实施。
- 不同场景的业务能力、接口契约差异大，强行复用导致大量例外处理。
- 价值流 Owner 无法对如此宽泛的流程负责。

**后果**：

- 价值流目录失去实际指导意义，项目团队仍然按系统边界设计流程。
- 价值流阶段接口契约频繁变更，下游系统集成成本居高不下。

**避免建议**：

- 价值流应聚焦单一、可度量的价值主张，避免"万能价值流"。
- 当多个场景差异较大时，应拆分为多个价值流，并通过共享阶段实现复用。
- 价值流设计应经过业务 Owner 和技术 Owner 共同评审，确保端到端边界清晰。

---

## 11. 权威来源与交叉引用

> **权威来源**:
>
> - [The Open Group TOGAF Series Guide: Value Streams](https://www.opengroup.org/togaf) — TOGAF 价值流指南；核查日期：2026-07-08
> - [ArchiMate 4.0 Specification](https://pubs.opengroup.org/architecture/archimate4-doc/) — ArchiMate Value Stream 元模型；核查日期：2026-07-08
> - [OMG BPMN 2.0.2 Specification](https://www.omg.org/spec/BPMN/2.0.2/) — 价值流可执行编排标准；核查日期：2026-07-08
> - [OMG DMN 1.5 Specification](https://www.omg.org/spec/DMN/1.5/) — 决策服务与价值流条件分支；核查日期：2026-07-08
> - [SAFe Value Streams](https://scaledagileframework.com/value-streams/) — SAFe 价值流框架；核查日期：2026-07-08
>
> **核查日期**: 2026-07-08

**交叉引用**：

- [业务能力复用](../struct/02-business-architecture-reuse/02-business-capability/capability-reuse.md) — 价值流组合的能力单元
- [BPMN 2.0 / DMN 业务过程与决策的复用编排](../struct/02-business-architecture-reuse/06-bpmn-dmn/bpmn-dmn-reuse-orchestration.md) — 价值流的可执行编排
- [Zachman Framework 与软件架构复用映射](../struct/02-business-architecture-reuse/08-zachman-reuse-mapping/zachman-reusability-matrix.md) — 价值流在 Zachman Why/What/How 维度的映射
- [BIAN 金融服务域复用案例](../struct/02-business-architecture-reuse/case-studies/bian-banking-reuse-case.md) — 金融服务价值流复用

---


<!-- SOURCE: struct/02-business-architecture-reuse/04-business-process-reuse/README.md -->

# 04 业务流程复用（Business Process Reuse）

> **版本**: 2026-06-12
> **定位**: 02-business-architecture-reuse / 04-business-process-reuse
> **对齐标准**: BPMN 2.0, DMN 1.5, ISO/IEC 26550:2015, OMG RAS v2.2

---

## 核心概念

业务流程复用关注**流程模板、流程片段和流程编排**的复用。与业务能力复用不同，流程复用更贴近操作层面：它解决的是“如何以标准化方式完成一组业务活动”。

| 层级 | 复用对象 | 示例 |
|:---|:---|:---|
| **流程模板（Process Template）** | 完整端到端流程的可配置模型 | 订单到收款（Order-to-Cash）流程模板 |
| **流程片段（Process Fragment）** | 可嵌入多个主流程的子流程 | 客户身份验证、支付授权 |
| **任务模式（Task Pattern）** | 原子级活动模板 | 审批任务、通知任务、归档任务 |
| **决策服务（Decision Service）** | 可复用的业务规则集 | 信用评分、折扣策略、合规校验 |

---

## 复用模式

1. **流程目录与分类体系**
   - 按域、价值流、成熟度对流程资产分类
   - 使用 OMG RAS 元数据描述流程资产（分类、解决方案、使用、相关资产）

2. **可配置流程模板**
   - 将流程中的可变点参数化（如审批层级、分支条件）
   - 通过 BPMN 子流程和多实例活动实现可变性

3. **决策即服务（Decision-as-a-Service）**
   - 将业务规则封装为 DMN 决策服务
   - 通过 API 供多个流程和消费端复用

4. **流程挖掘驱动的复用发现**
   - 通过事件日志识别高频子流程和瓶颈
   - 将高频片段提取为可复用资产

---

## 检查清单

- [ ] 流程资产是否按域/价值流分类？
- [ ] 可变点是否已识别并参数化？
- [ ] 流程片段是否有清晰的输入/输出契约？
- [ ] DMN 决策服务是否从流程中解耦？
- [ ] 流程版本和变更是否可追溯？

---

## 关联主题

- `02-business-architecture-reuse/06-bpmn-dmn/` — BPMN/DMN 可执行案例
- `02-business-architecture-reuse/05-business-service-reuse/` — 流程到业务服务的映射
- `05-functional-architecture-reuse/` — 工作流与函数级复用


---

## 补充说明：04 业务流程复用（Business Process Reuse）

## 示例

**示例**：制造企业将“供应商准入流程”建模为标准 BPMN 2.0 流程并在 Camunda 引擎上部署，各工厂按本地法规配置差异规则后复用。

## 反例

**反例**：将高度监管流程的 BPMN 模板复制到新国家时未本地化合规规则，导致审计失败。

## 权威来源

> **权威来源**:
>
> - [OMG BPMN](https://www.omg.org/spec/BPMN)
> - [OMG DMN](https://www.omg.org/spec/DMN)
> - 核查日期：2026-07-07

## 分析

**分析**：流程复用需要区分“不变流程主干”与“可变本地化规则”，并通过决策表管理差异。

---


<!-- SOURCE: struct/02-business-architecture-reuse/05-business-service-reuse/README.md -->

# 05 业务服务复用（Business Service Reuse）

> **版本**: 2026-06-12
> **定位**: 02-business-architecture-reuse / 05-business-service-reuse
> **对齐标准**: SOA, OASIS SOA Reference Architecture, TOGAF Standard 10

---

## 核心概念

业务服务复用将业务能力封装为**自治、可组合、可消费的服务**。它是业务架构向应用架构过渡的桥梁：业务能力回答“做什么”，业务服务回答“如何以契约化方式对外提供什么”。

| 概念 | 定义 | 与复用的关系 |
|:---|:---|:---|
| **业务服务（Business Service）** | 为内部或外部利益相关者创造价值的可契约化能力单元 | 复用的基本交付单元 |
| **服务契约（Service Contract）** | 服务的功能、质量、SLA、接口约定 | 复用资产的边界定义 |
| **服务组合（Service Composition）** | 通过编排多个服务完成更复杂的业务能力 | 复用资产的组合机制 |
| **服务目录（Service Catalog）** | 组织级业务服务的统一注册与发现入口 | 复用资产的治理基础设施 |

---

## 复用模式

1. **服务目录驱动的复用**
   - 建立企业级业务服务目录，统一服务命名、版本、所有者
   - 与服务网格/API 网关集成，实现运行时发现和治理

2. **分层服务模型**
   - 基础服务（Foundation）→ 核心服务（Core）→ 复合服务（Composite）
   - 明确各层复用边界和组合规则

3. **业务能力-服务映射**
   - 每个业务能力可映射到一个或多个业务服务
   - 通过映射矩阵识别服务冗余和缺口

4. **外部业务服务复用**
   - SaaS/API 生态中的业务服务（如支付、身份、物流）
   - 通过供应商评估和适配层实现安全复用

---

## 检查清单

- [ ] 是否建立了业务服务目录？
- [ ] 每个业务服务是否有明确的服务契约？
- [ ] 服务与业务能力之间是否存在可追溯的映射？
- [ ] 是否区分了核心服务、基础服务和复合服务？
- [ ] 外部业务服务是否有供应商风险评估？

---

## 关联主题

- `03-application-architecture-reuse/03-app-service/` — 应用服务复用的技术实现
- `05-functional-architecture-reuse/01-api-design/` — API 设计与服务契约
- `10-supply-chain-security/` — 外部服务的供应链安全评估


---

## 补充说明：05 业务服务复用（Business Service Reuse）

## 示例

**示例**：电信公司将“号码携带”封装为标准业务服务，供线上线下渠道、合作伙伴 API 统一调用，避免各渠道重复实现。

## 反例

**反例**：业务服务边界过大，包含下单、支付、履约等多个子领域，导致消费方被迫引入不必要的耦合。

## 权威来源

> **权威来源**:
>
> - [The Open Group TOGAF](https://www.opengroup.org/togaf)
> - [OMG BPMN](https://www.omg.org/spec/BPMN)
> - 核查日期：2026-07-07

## 分析

**分析**：业务服务复用的粒度应与客户契约和变更频率相匹配，过大或过小的服务都会降低复用收益。

---


<!-- SOURCE: struct/02-business-architecture-reuse/06-bpmn-dmn/bpmn-dmn-executable-cases.md -->

# BPMN 2.0 / DMN 1.5 可执行语义案例集

> **版本**: 2026-06-06
> **对齐来源**: OMG BPMN 2.0.2, OMG DMN 1.5 (2024), ISO/IEC 19510:2013, Camunda 2024, Freund & Rücker — *Practical Process Automation* (O'Reilly)

---

## 引言

BPMN 2.0 与 DMN 1.5 的核心价值在于"同一模型、双重语义"：一张流程图或决策表，既是业务人员可读的沟通媒介，也是流程引擎可直接执行的 XML 规范。
本文通过三个生产级案例，展示如何将 BPMN 的**调用活动（Call Activity）**、**事件子流程（Event Subprocess）**与 DMN 的**决策服务（Decision Service）**转化为可复用的业务资产。

---

## 案例 1：订单审批流程（Order Approval Workflow）

### 1.1 业务背景

B2B 电商平台接收客户订单后，需根据订单金额、客户信用等级、库存可用性三个维度，决定订单的流转路径：自动通过、人工复核或拒绝。

### 1.2 BPMN 流程图（Mermaid）

```mermaid
flowchart TB
    Start([消息开始事件<br/>OrderReceived]) --> Validate[服务任务<br/>Validate Order Format]
    Validate --> CheckStock[服务任务<br/>Check Inventory]
    CheckStock --> Decision{独占网关<br/>库存充足?}
    Decision -- 否 --> Reject1[脚本任务<br/>Auto Reject]
    Reject1 --> NotifyReject[发送任务<br/>Notify Customer]
    NotifyReject --> EndReject([结束事件<br/>Order Rejected])
    Decision -- 是 --> CallDecision[[调用活动<br/>Call Activity: Risk Assessment]]
    CallDecision --> Route{独占网关<br/>决策结果?}
    Route -- APPROVED --> Fulfill[服务任务<br/>Create Fulfillment]
    Fulfill --> EndApprove([结束事件<br/>Order Approved])
    Route -- MANUAL_REVIEW --> UserTask[用户任务<br/>Senior Manager Review]
    UserTask --> ManagerDecision{独占网关<br/>经理决定?}
    ManagerDecision -- APPROVED --> Fulfill
    ManagerDecision -- REJECTED --> NotifyReject
    Route -- REJECTED --> NotifyReject

    subgraph EventSubprocess [事件子流程: 全局超时处理]
        direction TB
        TimerStart[定时开始事件<br/>48h Timeout] --> Escalate[升级任务<br/>Escalate to VP]
        Escalate --> EndEscalate([结束事件])
    end
```

### 1.3 DMN 决策表：订单风险评估

**决策名称**: `OrderRiskAssessment`
**命中策略**: `Unique`（唯一命中）

| 规则编号 | 订单金额 (Amount) | 客户信用等级 (Credit) | 库存状态 (Stock) | 输出: 决策结果 (Decision) | 输出: 原因 (Reason) |
|---------|------------------|---------------------|-----------------|------------------------|------------------|
| R1 | < 10,000 | AAA / AA | 充足 | AUTO_APPROVE | 低风险，自动通过 |
| R2 | < 50,000 | A / BBB | 充足 | MANUAL_REVIEW | 中等风险，需人工复核 |
| R3 | ≥ 50,000 | 任意 | 充足 | MANUAL_REVIEW | 高额订单，强制复核 |
| R4 | 任意 | BB 及以下 | 充足 | MANUAL_REVIEW | 信用等级低，需复核 |
| R5 | 任意 | 任意 | 不足 | AUTO_REJECT | 库存不足，自动拒绝 |

**FEEL 表达式片段**（用于输入校验）：

```feel
if order.amount < 0 then null
else if order.customer.creditScore in ["AAA","AA","A","BBB","BB","B","CCC"] then order.customer.creditScore
else null
```

### 1.4 复用点分析

| 复用元素 | BPMN/DMN 构造 | 复用方式 | 复用价值 |
|---------|--------------|---------|---------|
| **调用活动** | `Call Activity` 调用独立流程 `Risk Assessment` | 多个主流程（B2B 订单、B2C 大额订单、分销订单）共享同一风险评估子流程 | 规则变更时仅需修改一处，避免流程克隆 |
| **决策服务** | DMN `Decision Service` 封装 `OrderRiskAssessment` | 通过 REST API 暴露给 CRM、客服系统、移动端 | 信用评估逻辑跨渠道复用，版本独立演进 |
| **事件子流程** | 附加于主流程的 `Event Subprocess`（Timer Boundary） | 同一超时处理模式复用于所有审批类流程 | 横切关注点（SLA 监控、升级）统一治理 |
| **全局任务** | `Global User Task` — "Senior Manager Review" | 在多个审批流程中引用同一人工任务定义 | 表单模板、权限矩阵、提醒规则集中维护 |

> **公理 2.1 延伸**: 当决策逻辑（DMN）与流程控制流（BPMN）解耦后，两者的变更频率差异被隔离。决策规则可每周迭代，而流程结构可季度稳定。

---

## 案例 2：保险理赔决策（Insurance Claims Decisioning）

### 2.1 业务背景

财产险理赔流程中，需在受理报案后，依据保单类型、出险原因、历史理赔次数、是否在免赔额范围内，自动计算赔付比例并决定是否需要现场查勘。

### 2.2 BPMN 流程图（Mermaid）

```mermaid
flowchart TB
    StartClaim([消息开始<br/>Claim Reported]) --> Register[用户任务<br/>Register Claim]
    Register --> ValidatePolicy[服务任务<br/>Validate Policy Status]
    ValidatePolicy --> PolicyActive{独占网关<br/>保单有效?}
    PolicyActive -- 否 --> CloseDenial[脚本任务<br/>Denial: Policy Inactive]
    CloseDenial --> EndDeny([结束事件<br/>Claim Denied])
    PolicyActive -- 是 --> CallDmn[[调用活动<br/>Call Activity: Claim Evaluation]]
    CallDmn --> Result{独占网关<br/>评估结果?}
    Result -- AUTO_SETTLE --> Calculate[服务任务<br/>Calculate Payout]
    Calculate --> Pay[服务任务<br/>Trigger Payment]
    Pay --> EndSettle([结束事件<br/>Claim Settled])
    Result -- INVESTIGATE --> Assign[用户任务<br/>Assign Field Adjuster]
    Assign --> Investigation[子流程<br/>Field Investigation]
    Investigation --> AdjusterDecision{独占网关<br/>查勘结论?}
    AdjusterDecision -- FRAUD_SUSPECTED --> FraudProcess[调用活动<br/>Fraud Investigation Process]
    FraudProcess --> EndFraud([结束事件<br/>Fraud Case Opened])
    AdjusterDecision -- VALID --> Calculate
    Result -- PARTIAL --> CalculatePartial[服务任务<br/>Calculate Deductible]
    CalculatePartial --> NotifyPartial[发送任务<br/>Notify Partial Settlement]
    NotifyPartial --> EndPartial([结束事件<br/>Partially Settled])
```

### 2.3 DMN 决策需求图（DRD）与决策表

**DRD 结构**:

```text
ClaimEvaluation [决策]
├── Input Data: ClaimInfo
│   ├── incidentType: {"Collision", "Theft", "Fire", "Natural Disaster"}
│   ├── claimAmount: number
│   └── incidentDate: date
├── Input Data: PolicyInfo
│   ├── policyType: {"Comprehensive", "ThirdParty", "TheftOnly"}
│   └── deductible: number
├── Input Data: CustomerHistory
│   └── claimsLast3Years: number
├── Business Knowledge Model: CoverageMatrix
└── Decision: PayoutCalculation
    └── Business Knowledge Model: DepreciationTable
```

**主决策表 `ClaimEvaluation`**（命中策略: `First`）

| 规则 | 保单类型 | 出险类型 | 金额 vs 免赔额 | 近3年理赔次数 | 输出: action | 输出: payoutRate |
|-----|---------|---------|--------------|------------|-----------|---------------|
| R1 | Comprehensive | Collision | amount > deductible | ≤ 2 | AUTO_SETTLE | 0.95 |
| R2 | Comprehensive | Theft | amount > deductible | ≤ 2 | AUTO_SETTLE | 0.90 |
| R3 | ThirdParty | Collision | amount > deductible | ≤ 1 | AUTO_SETTLE | 0.80 |
| R4 | 任意 | Natural Disaster | amount > 10000 | 任意 | INVESTIGATE | null |
| R5 | 任意 | 任意 | amount ≤ deductible | 任意 | PARTIAL | 0.00 |
| R6 | 任意 | 任意 | 任意 | ≥ 3 | INVESTIGATE | null |
| R7 | 任意 | 任意 | 任意 | 任意 | INVESTIGATE | null |

**FEEL 表达式 — 折旧计算**:

```feel
if claim.incidentType = "Collision" and claim.vehicleAge > 5 then
    max(0.5, 1 - (claim.vehicleAge - 5) * 0.05)
else 1.0
```

### 2.4 复用点分析

| 复用元素 | BPMN/DMN 构造 | 复用方式 | 复用价值 |
|---------|--------------|---------|---------|
| **业务知识模型** | DMN `Business Knowledge Model` (BKM) `CoverageMatrix` | 被 `ClaimEvaluation` 及其他险种（健康险、责任险）决策引用 | 保险覆盖规则作为行业知识资产沉淀，跨产品线复用 |
| **调用活动** | `Call Activity: Fraud Investigation Process` | 理赔、续保核保、退保审核均调用同一反欺诈子流程 | 反欺诈规则集中，避免欺诈分子利用流程差异绕过检测 |
| **决策服务版本** | DMN Decision Service v1.2 | 旧保单使用 v1.1，新保单使用 v1.2，通过 API 路由控制 | 合规变更不影响历史案件回溯 |
| **嵌套子流程** | `Field Investigation` Embedded Subprocess | 作为模板复用于车险、财产险、企业险的查勘环节 | 查勘步骤标准化，数据采集字段统一 |

---

## 案例 3：费用报销与合规校验（Expense Reimbursement & Compliance）

### 3.1 业务背景

跨国企业员工提交差旅费用报销后，系统需根据费用类型、金额阈值、目的地国家合规政策、员工职级，自动判定报销是否合规、是否需要附加审批或进入合规审查队列。

### 3.2 BPMN 流程图（Mermaid）

```mermaid
flowchart TB
    StartExp([消息开始<br/>Expense Submitted]) --> OCR[服务任务<br/>OCR & Data Extraction]
    OCR --> Validate[服务任务<br/>Validate Receipt Format]
    Validate --> DmnCheck[[调用活动<br/>Call Activity: Compliance Check]]
    DmnCheck --> CompResult{独占网关<br/>合规结果?}
    CompResult -- COMPLIANT --> AmountGate{独占网关<br/>金额 > 阈值?}
    AmountGate -- 否 --> AutoPay[服务任务<br/>Auto-Reimburse]
    AutoPay --> EndAuto([结束事件<br/>Reimbursed])
    AmountGate -- 是 --> ManagerApproval[用户任务<br/>Direct Manager Approval]
    ManagerApproval --> ApproveDecision{独占网关<br/>审批结果?}
    ApproveDecision -- APPROVED --> AutoPay
    ApproveDecision -- REJECTED --> NotifyEmp[发送任务<br/>Notify Rejection]
    NotifyEmp --> EndRej([结束事件<br/>Rejected])
    CompResult -- NON_COMPLIANT --> ComplianceQueue[用户任务<br/>Compliance Team Review]
    ComplianceQueue --> CompDecision{独占网关<br/>合规判定?}
    CompDecision -- OVERRIDE --> AmountGate
    CompDecision -- CONFIRM_VIOLATION --> AuditTrail[脚本任务<br/>Log to Audit System]
    AuditTrail --> EndViolation([结束事件<br/>Violation Logged])

    subgraph AdHoc [Ad-hoc 子流程: AI 辅助审查]
        direction TB
        AIReview[服务任务<br/>AI Anomaly Detection]
        HumanConfirm[用户任务<br/>Confirm AI Flag]
    end
```

### 3.3 DMN 决策表：费用合规检查

**决策名称**: `ExpenseComplianceCheck`
**命中策略**: `Collect` + `List`（收集所有命中规则）

| 规则 | 费用类型 | 金额 (USD) | 目的地国家 | 员工职级 | 输出: complianceFlag | 输出: requiredAttachment |
|-----|---------|-----------|----------|---------|-------------------|-----------------------|
| R1 | 餐饮 | > 200 | 任意 | 任意 | "THRESHOLD_EXCEEDED" | {"receipt", "attendee_list"} |
| R2 | 机票 | 任意 | 任意 | 任意 | "COMPLIANT" | {"itinerary", "boarding_pass"} |
| R3 | 酒店 | > 500 / 晚 | 任意 | Junior | "POLICY_VIOLATION" | {"justification"} |
| R4 | 礼品 | > 50 | CN, US, DE | 任意 | "ANTI_BRIBERY_CHECK" | {"recipient_info", "business_purpose"} |
| R5 | 交通 | ≤ 100 | 任意 | 任意 | "COMPLIANT" | {"receipt"} |

**FEEL 上下文表达式 — 阈值动态计算**:

```feel
{
    threshold: if employee.level in ["VP","SVP","C-Level"] then 1000 else 500,
    dailyAllowance: lookup table by country code,
    violationSeverity: if count(complianceFlag) > 2 then "HIGH" else "MEDIUM"
}
```

### 3.4 复用点分析

| 复用元素 | BPMN/DMN 构造 | 复用方式 | 复用价值 |
|---------|--------------|---------|---------|
| **调用活动** | `Call Activity: Compliance Check` | 费用报销、采购申请、供应商付款均调用同一合规决策服务 | 合规政策（如反贿赂、税务规则）全局统一，一键更新 |
| **Ad-hoc 子流程** | `Ad-hoc Subprocess`（AI 辅助审查） | 用于非结构化审查场景：AI 标记异常后由人确认 | 为 AI Agent 提供确定性治理框架，符合本知识体系对 AI 编排的论述 |
| **DMN 决策表** | `ExpenseComplianceCheck` 按国家维度切片 | 不同国家子公司引用同一决策模型，通过输入数据 `countryCode` 区分规则 | 全球化企业的本地化合规与集中治理平衡 |
| **边界事件** | 附加于 `ManagerApproval` 的 `Timer Boundary Event`（72h） | 同一超时模式复用于所有人工审批任务 | SLA 可配置、可监控、可审计 |

---

## 4. 跨案例总结：BPMN/DMN 可复用元素速查表

| 元素类别 | 元素名称 | 可复用级别 | 复用模式 | 版本治理 |
|---------|---------|----------|---------|---------|
| **活动** | Call Activity | 流程级 | 跨流程调用全局流程定义 | 被调用流程独立版本 |
| **活动** | Global Task | 企业级 | 多流程引用同一任务定义 | 任务模板版本化 |
| **子流程** | Event Subprocess | 模板级 | 作为异常处理模板附加于任意流程 | 模板库管理 |
| **子流程** | Ad-hoc Subprocess | 场景级 | AI/知识工作者驱动的非结构化步骤 | 与主流程同版本 |
| **决策** | Decision Service | 服务级 | REST API / gRPC 暴露，跨系统调用 | Semantic Versioning |
| **决策** | Business Knowledge Model | 知识级 | 被多个 Decision 引用 | 知识库版本控制 |
| **数据** | Input Data / Item Definition | 元模型级 | 全局数据类型定义（如 `Customer`, `Policy`） | 与企业数据标准同步 |

---

## 5. 实施建议

1. **流程引擎选型**: 优先选择支持 BPMN `Common Executable` 子集与 DMN 1.5 Conformance Level 3 的引擎（如 Camunda 8, jBPM, Drools）。
2. **版本策略**: DMN 决策服务采用 Semantic Versioning（如 `OrderRiskAssessment/v2.1.0`），BPMN 流程采用流程引擎自带的版本管理机制。
3. **测试策略**: 对 DMN 决策表执行全规则覆盖测试（Hit Policy Verification），对 BPMN 调用活动执行集成契约测试。
4. **监控策略**: 在 Call Activity 入口/出口、Decision Service 调用点植入标准化追踪标识（Trace ID），实现端到端审计。

---

## 参考索引

- OMG: *Business Process Model and Notation (BPMN) Version 2.0.2* (2014) — [https://www.omg.org/spec/BPMN](https://www.omg.org/spec/BPMN)
- OMG: *Decision Model and Notation (DMN) Version 1.5* (2024) — [https://www.omg.org/spec/DMN](https://www.omg.org/spec/DMN)
- ISO/IEC 19510:2013 — *Information technology — Object Management Group Business Process Model and Notation*
- Bock, C.: *BPMN 2.0 Handbook* (2nd Edition, 2012) — 关于 Call Activity 与 Event Subprocess 的权威解释
- Freund, J. & Rücker, B.: *Practical Process Automation* (O'Reilly, 2021) — BPMN/DMN 集成实践
- ISD 2025 Research Paper: *DMN basis and applications* (2025) — DMN 1.5 语义与 FEEL 表达式应用综述
- Camunda GmbH: *BPMN: The open standard for process and agentic orchestration* (2024)

---

> 最后更新: 2026-06-06


---

## 补充说明：BPMN 2.0 / DMN 1.5 可执行语义案例集

## 概念定义

**定义**：BPMN（业务流程模型和标注）用于描述可执行业务流程，DMN（决策模型与标注）用于描述可执行业务决策，二者结合实现流程与决策的分离与复用。

## 反例

**反例**：将业务规则硬编码在 BPMN 网关条件中，导致规则变更需要重新部署流程，业务人员无法参与。

## 权威来源

> **权威来源**:
>
> - [OMG BPMN](https://www.omg.org/spec/BPMN)
> - [OMG DMN](https://www.omg.org/spec/DMN)
> - 核查日期：2026-07-07

---


<!-- SOURCE: struct/02-business-architecture-reuse/06-bpmn-dmn/bpmn-dmn-reuse-orchestration.md -->

# BPMN 2.0 / DMN 业务过程与决策的复用编排
>
> 版本: 2026-07-08
> 对齐来源: OMG BPMN 2.0.2 / DMN 1.5, ISO/IEC 19510:2013, Camunda 2024, Signavio/SAP, 澳大利亚 NSW 交通标准

## 1. 标准体系

| 标准 | 版本状态 | 标准化机构 | 关键特征 |
|-----|---------|-----------|---------|
| **BPMN** | 2.0.2 (2014) | OMG / ISO/IEC 19510:2013 | 人读 + 机执行的双重语义 |
| **DMN** | 1.5 (2024) | OMG | 决策需求图 + 决策表 + FEEL 表达式 |
| **CMMN** | 1.1 | OMG | 案例管理（非结构化流程）|

## 2. BPMN 作为复用载体的独特价值

### 2.1 双重语义

> "A BPMN diagram is simultaneously a visual that any stakeholder can read and an XML specification that an orchestration engine can run."

- **人读**：业务流程图让所有利益相关者理解流程
- **机执行**：BPMN 2.0 XML 可被流程引擎直接执行
- **结果**：业务批准的流程与生产运行的流程完全一致

### 2.2 与 AI 智能体时代的契合

BPMN 在 AI 时代的价值不降反升：

- **确定性骨架**：为非确定性 AI 智能体提供编排、升级、审批、审计的确定性框架
- **Agent 治理**：BPMN 将智能体视为普通参与者（服务、人员、系统），由流程决定何时调用、结果如何处理
- **可审计性**：每一步（无论由代码、智能体或人执行）进入同一审计轨迹

### 2.3 与专有方案的对比

| 维度 | BPMN (开放标准) | 专有低代码 | 纯代码编排器 |
|-----|---------------|-----------|------------|
| 开放标准 | ISO/IEC 19510, OMG 维护 | 厂商私有 | 无，仅代码构造 |
| 业务可读性 | 原生设计 | 受限于厂商 UI | 无，逻辑在代码中 |
| 工具/人才可移植性 | 100+ 工具支持 | 锁定厂商 | 锁定引擎 SDK |
| 人工任务支持 | User Task 为一等公民 | 套件内支持 | 需从零构建 |
| 智能体治理 | 外部+内部（ad-hoc subprocess）| 仅外部 | 仅外部 |
| 审计轨迹 | 自动记录，无需额外插桩 | 套件内；跨系统脆弱 | 仅日志，无端到端视图 |

## 3. BPMN 核心元素族

| 元素族 | 代表元素 | 复用场景 |
|-------|---------|---------|
| **事件（Events）** | Start, End, Timer, Message, Error, Boundary | 流程触发器、超时处理、异常恢复 |
| **任务（Tasks）** | User Task, Service Task, Business Rule Task, Script Task | 人工审批、API 调用、DMN 决策、脚本执行 |
| **网关（Gateways）** | Exclusive, Parallel, Inclusive, Event-based | 条件分支、并行处理、事件等待 |
| **子流程（Subprocesses）** | Embedded, Call Activity, Ad-hoc | 流程模块化、跨流程复用、非结构化 AI Agent 步骤 |
| **边界事件（Boundary Events）** | Timer, Error, Escalation | 步骤级超时、错误捕获、升级处理 |
| **消息流（Message Flows）** | Pool-to-Pool 虚线箭头 | 跨组织/跨系统/跨智能体通信 |

## 4. DMN 决策复用

### 4.1 三层结构

```text
Decision Requirements Diagram (DRD)
├── Decisions（决策节点）
├── Input Data（输入数据）
├── Business Knowledge Models（业务知识模型）
└── Knowledge Sources（知识来源）

Decision Table（决策表）
├── Inputs（条件列）
├── Outputs（结果列）
└── Rules（规则行）

FEEL Expressions（Friendly Enough Expression Language）
└── 上下文中的表达式计算
```

### 4.2 决策即服务（Decision-as-a-Service）

- DMN 决策表可独立于 BPMN 流程部署为可复用服务
- 多个流程共享同一决策逻辑（如信用评分、定价策略、合规检查）
- 决策变更无需修改调用流程，只需更新决策服务版本

### 4.3 与 BPMN 的集成

```text
BPMN Process
├── Business Rule Task
│   └── 调用 DMN Decision Service
└── 根据决策结果路由流程分支
```

## 5. 业务过程分层复用模型

参考澳大利亚 NSW 交通标准实践：

| 层级 | 内容 | 表示法 | 复用粒度 |
|-----|------|--------|---------|
| **Layer 1–3** | 企业地图与价值链 | 上下文/概念/逻辑功能 | 能力域 |
| **Layer 4** | 可执行工作流模型 | BPMN | 流程模板 |
| **Layer 5** | 可执行决策模型 | DMN | 决策服务 |

## 6. 过程资产复用模式

### 6.1 流程模板库

```text
Process Template Library
├── 审批类
│   ├── 请假审批（User Task → Manager Approval → HR Record）
│   ├── 费用报销（OCR → 规则校验 → 多级审批 → 支付）
│   └── 合同审批（Legal Review → Finance Review → Signature）
├── 订单类
│   ├── 电商订单（Create → Payment → Fulfillment → Delivery）
│   └── B2B 订单（Credit Check → Inventory Reserve → Shipping）
├── 客服类
│   ├── 投诉处理（Intake → Categorize → Resolve → Close）
│   └── 退换货（Return Request → Inspection → Refund/Exchange）
└── AI 增强类
    ├── RAG 查询流程（Retrieve → Generate → Human Review → Publish）
    └── 智能体协作（Orchestrator → Agent A → Agent B → Consolidate）
```

### 6.2 Call Activity 跨流程复用

- **定义**：在一个流程中调用另一个独立部署的流程
- **优势**：被调用流程更新不影响调用方定义；多个调用方共享同一子流程
- **典型用例**：通用审批子流程、支付子流程、通知子流程

### 6.3 事件子流程（Event Subprocess）复用

- 定义全局异常处理模式（如超时、升级、补偿）
- 附加于任何流程或子流程，实现横切关注点复用

## 7. 与 CMMN 的互补

| 场景 | BPMN | CMMN |
|-----|------|------|
| 结构化流程 | ✅ 完美适配 | ❌ 过度约束 |
| 知识工作者驱动 | ❌ 难以建模 | ✅ 案例文件 + 自由启动计划项 |
| 规则/事件复杂交织 | 流程图臃肿 | 案例模型清晰 |
| AI Agent 自主决策 | Ad-hoc Subprocess 有限 | 案例目标驱动更适合 |

## 8. 参考索引

- OMG BPMN 2.0.2 Specification
- OMG DMN 1.5 Specification
- ISO/IEC 19510:2013 — BPMN 标准
- Camunda: "BPMN: The open standard for process and agentic orchestration"
- SAP Signavio: BPMN 2.0 for Efficient Process Design
- Australia NSW Transport Standards: BPMN / DMN Layered Approach
- Freund & Rücker: "Practical Process Automation" (O'Reilly)


---

## 9. BPMN/DMN 复用编排模式

### 9.1 概念定义

**定义**：BPMN/DMN 复用编排（BPMN/DMN Reuse Orchestration）是指利用 BPMN 2.0 的流程可执行语义与 DMN 1.5 的决策服务语义，将稳定的过程结构、可变的决策规则与可复用的服务任务解耦，使流程模板、流程片段与决策服务能够在多个业务上下文、多个系统中重复组合与执行。

形式化：

```text
ReuseOrchestration := ⟨P, D, S, I, V⟩

P: 可复用流程模板集合（Process Templates）
D: 可复用决策服务集合（Decision Services）
S: 可复用服务任务集合（Service Tasks）
I: 流程-决策-服务之间的接口契约集合
V: 版本与兼容性规则集合
```

### 9.2 核心属性

| 属性 | 说明 | 重要性 |
|---|---|---|
| 结构稳定性 | 流程控制流（顺序、分支、并行）变更频率低 | 高 |
| 规则可变性 | 决策规则可独立于流程结构演进 | 高 |
| 服务可替换性 | 服务任务实现可替换，不影响流程定义 | 高 |
| 接口契约化 | 流程、决策、服务之间通过显式契约交互 | 高 |
| 版本兼容性 | 支持多版本流程/决策服务共存 | 中 |
| 执行可观测性 | 流程实例与决策执行可被追踪和审计 | 中 |

### 9.3 复用编排模式

#### 模式 1：流程模板库（Process Template Library）

将同类业务场景抽象为标准 [BPMN](https://en.wikipedia.org/wiki/Business_process_modeling) 模板，通过参数化适配不同上下文。

```mermaid
flowchart TB
    subgraph Library [流程模板库]
        A[审批类模板]
        B[订单类模板]
        C[客服类模板]
        D[AI 增强类模板]
    end
    subgraph Instance [上下文实例化]
        A --> A1[请假审批]
        A --> A2[费用报销]
        A --> A3[合同审批]
        B --> B1[电商订单]
        B --> B2[B2B 订单]
    end
```

#### 模式 2：调用活动跨流程复用（Call Activity Reuse）

独立部署的子流程被多个主流程调用，实现流程片段级复用。

```mermaid
flowchart LR
    P1[主流程：贷款申请] --> CA[[调用活动]]
    P2[主流程：信用卡申请] --> CA
    P3[主流程：开户申请] --> CA
    CA --> SP[子流程：信用评估]
    SP --> DS{DMN 决策服务}
```

#### 模式 3：决策服务复用（Decision-as-a-Service）

[DMN](https://en.wikipedia.org/wiki/Decision_Model_and_Notation) 决策表封装为独立 REST/gRPC 服务，供多个流程和系统共享。

```mermaid
flowchart LR
    subgraph Clients [调用方]
        C1[BPMN 流程]
        C2[移动 App]
        C3[客服系统]
    end
    Clients --> DS[DMN 决策服务]
    DS --> DT1[定价决策表]
    DS --> DT2[信用评分表]
    DS --> DT3[合规检查表]
```

#### 模式 4：事件子流程横切关注点复用

将超时、异常、升级等横切关注点抽象为事件子流程，附加于任意主流程。

### 9.4 流程片段复用

流程片段（Process Fragment）是 BPMN 中可独立识别、命名和版本化的子结构，包括：

- **子流程（Subprocess）**：嵌入式或可调用的流程模块
- **调用活动（Call Activity）**：调用独立流程定义的复用机制
- **全局任务（Global Task）**：跨流程共享的人工任务定义

**流程片段复用的最佳实践**：

1. 识别高频出现的流程结构（如"审批"、"通知"、"支付"）
2. 将高频结构提取为独立子流程或调用活动
3. 定义清晰的输入/输出契约和数据对象
4. 通过语义化版本控制管理变更

### 9.5 决策服务复用

**决策服务复用的层次**：

| 层次 | 复用内容 | 典型示例 |
|---|---|---|
| 决策表结构 | 输入/输出变量、命中策略、规则骨架 | 信用评分表结构 |
| 业务知识模型 | 可跨决策复用的计算逻辑 | 客户终身价值计算 |
| 完整决策服务 | 已部署的 DMN 服务 | 利率定价服务 |

**决策服务复用的反模式警示**：

- 将业务流程条件直接硬编码在 DMN 中，导致决策服务知道过多流程上下文。
- 将 DMN 决策表作为通用规则引擎，执行非决策类逻辑（如数据转换）。

### 9.6 版本管理反例

**反例：无版本隔离的决策服务复用**

**场景**：某金融机构将"信用评分"DMN 决策服务部署为单一版本，供贷款审批、信用卡审批、保险核保三个业务线共享。当贷款业务要求调整评分规则时，直接修改了共享决策服务。

**问题**：

- 三个业务线共享同一决策服务版本，未建立多版本并存机制。
- 修改未进行影响分析，信用卡审批和保险核保的规则被意外改变。

**后果**：

- 信用卡审批通过率异常下降 12%，客户投诉增加。
- 保险核保出现风险漏判，导致后续赔付率上升。
- 回滚困难，因为无法区分三个业务线各自的规则历史版本。

**避免建议**：

- 对共享决策服务实施**语义化版本控制**（Semantic Versioning）。
- 采用**蓝绿部署**或**金丝雀发布**进行决策服务版本切换。
- 在 BPMN 流程中通过版本参数显式指定调用的 DMN 版本。
- 建立决策服务消费者影响分析（Consumer Impact Analysis）流程。

### 9.7 与其他概念的关系

- **与业务复用层的关系**：BPMN 流程模板是业务复用资产中"How"维度的主要载体。
- **与应用复用层的关系**：BPMN 服务任务调用应用层服务契约（OpenAPI/gRPC）。
- **与组件复用层的关系**：DMN 引擎、BPMN 引擎本身是技术组件复用对象。
- **与价值流的关系**：价值流定义"端到端价值创造"，BPMN 定义"价值流的可执行编排"。

### 9.8 权威来源与交叉引用

> **权威来源**:
>
> - [OMG BPMN 2.0.2 Specification](https://www.omg.org/spec/BPMN/2.0.2/) — OMG 官方 BPMN 规范；核查日期：2026-07-08
> - [OMG DMN 1.5 Specification](https://www.omg.org/spec/DMN/1.5/) — OMG 官方 DMN 规范；核查日期：2026-07-08
> - [ISO/IEC 19510:2013](https://www.iso.org/standard/62652.html) — BPMN 国际标准；核查日期：2026-07-08
> - [Decision Model and Notation - Wikipedia](https://en.wikipedia.org/wiki/Decision_Model_and_Notation) — DMN 概述；核查日期：2026-07-08
> - [Business process modeling - Wikipedia](https://en.wikipedia.org/wiki/Business_process_modeling) — BPMN 在业务过程建模中的定位；核查日期：2026-07-08
>
> **核查日期**: 2026-07-08

**交叉引用**：

- [BPMN 2.0 / DMN 1.5 可执行语义案例集](../struct/02-business-architecture-reuse/06-bpmn-dmn/bpmn-dmn-executable-cases.md) — 具体可执行案例
- [BIAN 金融服务域复用案例](../struct/02-business-architecture-reuse/case-studies/bian-banking-reuse-case.md) — BPMN/DMN 在金融场景的结合
- [业务能力复用](../struct/02-business-architecture-reuse/02-business-capability/capability-reuse.md) — 业务复用层定义
- [价值流复用的形式化组合](../struct/02-business-architecture-reuse/03-value-stream/value-stream-composition.md) — 端到端价值流与 BPMN 编排的关系




## 10. BPMN/DMN 复用编排补充：可执行案例与业务能力映射

### 10.1 与业务能力的映射关系

[BPMN](https://en.wikipedia.org/wiki/Business_process_modeling) 与 [DMN](https://en.wikipedia.org/wiki/Decision_Model_and_Notation) 制品不仅是流程与决策的可视化符号，更是业务能力复用的可执行载体。下表给出 BPMN/DMN 关键制品与业务能力（Business Capability）之间的映射关系。

| BPMN/DMN 制品 | 业务能力维度 | 映射说明 |
|---|---|---|
| BPMN 流程模板 | How | 一个或多个业务能力按时间顺序编排，形成端到端价值流 |
| BPMN 调用活动（Call Activity） | How | 将可复用的子能力封装为独立子流程，被多个主流程共享 |
| BPMN 服务任务（Service Task） | How | 通过服务契约调用业务能力的 IT 实现 |
| BPMN 消息流（Message Flow） | Who / Where | 描述跨能力、跨组织、跨系统的协作与边界 |
| DMN 决策服务 | Why / How | 封装业务规则与决策逻辑，支撑能力执行中的判断分支 |
| DMN 业务知识模型（BKM） | Why | 提供跨决策复用的计算逻辑，如客户终身价值、风险权重 |

> **关键结论**：业务能力回答“做什么”，BPMN 回答“怎么做（流程编排）”，DMN 回答“怎么决定（规则）”。三者的解耦使能力复用可以在不修改流程结构的情况下，通过替换服务实现或调整决策表来适应不同上下文。

### 10.2 可执行案例：在线信贷审批

以下展示一个可执行的在线信贷审批场景，说明 BPMN 流程、DMN 决策表与业务能力如何协同复用。

**业务能力映射**：

- `C-001 客户信息查询` → BPMN 服务任务：调用客户信息服务
- `C-002 信用评估` → BPMN 调用活动 + DMN 信用评分决策服务
- `C-003 风险定价` → DMN 利率定价决策表
- `C-004 合同生成` → BPMN 服务任务：调用合同管理服务

**BPMN 流程片段（简化 XML）**：

```xml
<process id="loanApproval" name="在线信贷审批">
  <startEvent id="start" name="提交申请"/>
  <sequenceFlow sourceRef="start" targetRef="taskQueryCustomer"/>

  <serviceTask id="taskQueryCustomer" name="查询客户信息"
               camunda:delegateExpression="${customerInfoDelegate}"/>
  <sequenceFlow sourceRef="taskQueryCustomer" targetRef="callCreditAssessment"/>

  <callActivity id="callCreditAssessment" name="信用评估子流程"
                calledElement="creditAssessmentSubProcess"/>
  <sequenceFlow sourceRef="callCreditAssessment" targetRef="gwApprove"/>

  <exclusiveGateway id="gwApprove" name="审批决策"/>
  <sequenceFlow sourceRef="gwApprove" targetRef="taskPricing" name="通过"
                conditionExpression="${approved}"/>
  <sequenceFlow sourceRef="gwApprove" targetRef="endReject" name="拒绝"/>

  <businessRuleTask id="taskPricing" name="风险定价"
                    camunda:decisionRef="pricingDecision"/>
  <sequenceFlow sourceRef="taskPricing" targetRef="taskContract"/>

  <serviceTask id="taskContract" name="生成合同"
               camunda:delegateExpression="${contractDelegate}"/>
  <sequenceFlow sourceRef="taskContract" targetRef="endApprove"/>

  <endEvent id="endApprove" name="审批通过"/>
  <endEvent id="endReject" name="审批拒绝"/>
</process>
```

**DMN 信用评分决策表（简化）**：

| 规则 | 年收入（万元） | 信用历史 | 负债比率 | 输出：风险等级 |
|---|---|---|---|---|
| R1 | > 50 | 良好 | < 0.3 | 低 |
| R2 | 20 - 50 | 良好 | < 0.5 | 中 |
| R3 | < 20 | 一般 | > 0.5 | 高 |
| R4 | - | 差 | - | 高 |

**复用价值**：

- 信用评估子流程可被消费贷、车贷、小微企业贷等多种产品复用。
- 利率定价决策表可由业务人员直接调整，无需重新部署 BPMN 流程。
- 当新的风控数据源接入时，只需扩展 DMN 输入数据，不影响流程控制结构。

### 10.3 BPMN-DMN-业务能力分层映射图

```mermaid
flowchart TB
    subgraph 业务能力层
        C1[客户信息查询]
        C2[信用评估]
        C3[风险定价]
        C4[合同生成]
    end

    subgraph BPMN 流程编排层
        P1[提交申请]
        P2[查询客户信息]
        P3[调用信用评估]
        P4[风险定价]
        P5[生成合同]
    end

    subgraph DMN 决策服务层
        D1[信用评分表]
        D2[利率定价表]
    end

    P2 --> C1
    P3 --> C2
    P3 --> D1
    P4 --> C3
    P4 --> D2
    P5 --> C4
```

### 10.4 可执行信贷审批流程图

```mermaid
flowchart LR
    A[提交申请] --> B[查询客户信息]
    B --> C[信用评估子流程]
    C --> D{审批通过?}
    D -- 否 --> E[拒绝并通知]
    D -- 是 --> F[DMN 风险定价]
    F --> G[生成合同]
    G --> H[审批完成]
```

### 10.5 反例补充：BPMN 网关硬编码业务规则

**场景**：某团队在信贷审批 BPMN 流程的排他网关条件中直接写入规则，如 `${annualIncome > 500000 && creditScore > 700}`。

**问题**：

- 规则变更需要修改 BPMN XML 并重新部署流程，业务人员无法参与。
- 同一规则在多个网关中重复硬编码，导致规则不一致。
- 规则逻辑与流程结构紧耦合，难以复用。

**后果**：

- 市场部门要求调整信贷政策时，IT 部门需要 2-3 周才能完成流程重部署。
- 某次规则修改遗漏了一个网关，造成高风险客户被自动通过。

**避免建议**：

- 将所有业务判断逻辑下沉到 DMN 决策服务，BPMN 网关仅调用决策结果。
- 对决策服务实施版本管理，支持规则热更新与 A/B 测试。
- 建立 BPMN-DMN 契约测试，确保网关条件与决策输出语义一致。

### 10.6 权威来源与交叉引用补充

> **权威来源**:
>
> - [Camunda BPMN Documentation](https://docs.camunda.org/manual/latest/reference/bpmn20/) — BPMN 可执行语义参考；核查日期：2026-07-08
> - [Camunda DMN Documentation](https://docs.camunda.org/manual/latest/reference/dmn11/) — DMN 决策表执行参考；核查日期：2026-07-08
> - [OMG BPMN 2.0.2 Specification](https://www.omg.org/spec/BPMN/2.0.2/) — OMG 官方 BPMN 规范；核查日期：2026-07-08
> - [OMG DMN 1.5 Specification](https://www.omg.org/spec/DMN/1.5/) — OMG 官方 DMN 规范；核查日期：2026-07-08
>
> **核查日期**: 2026-07-08

**交叉引用**：

- [BPMN 2.0 / DMN 1.5 可执行语义案例集](../struct/02-business-architecture-reuse/06-bpmn-dmn/bpmn-dmn-executable-cases.md) — 更多可执行示例
- [业务能力复用](../struct/02-business-architecture-reuse/02-business-capability/capability-reuse.md) — 业务能力复用的定义与属性
- [价值流复用的形式化组合](../struct/02-business-architecture-reuse/03-value-stream/value-stream-composition.md) — BPMN 流程与价值流的关系

## 11. 标准条款映射与权威来源

### 11.1 标准条款映射

| 本主题概念 | 对应标准条款 | 映射说明 |
|:---|:---|:---|
| 流程模板复用 | BPMN 2.0 §8 Process, §10.4 Call Activity | BPMN Process 定义可执行流程；Call Activity 支持跨流程复用子流程 |
| 决策服务复用 | DMN 1.5 §6 Decision Requirements, §8 Decision Table | DMN Decision Service 封装决策逻辑，可被 BPMN Business Rule Task 调用 |
| 流程-决策集成 | DMN 1.5 §11.2 Invocation | DMN 决策服务可通过标准化接口被 BPMN 流程调用 |
| 可执行语义国际标准 | ISO/IEC 19510:2013 | BPMN 2.0 被 ISO 采纳为国际标准，确保跨工具互操作 |
| 案例管理补充 | OMG CMMN 1.1 | 对于非结构化知识工作者流程，CMMN 与 BPMN 互补 |

### 11.2 权威来源

> **权威来源**:
>
> - [OMG BPMN 2.0.2 Specification](https://www.omg.org/spec/BPMN/2.0.2/) — BPMN 官方规范；核查日期：2026-07-08
> - [OMG DMN 1.5 Specification](https://www.omg.org/spec/DMN/1.5/) — DMN 官方规范；核查日期：2026-07-08
> - [ISO/IEC 19510:2013](https://www.iso.org/standard/62652.html) — BPMN 国际标准；核查日期：2026-07-08
> - [Camunda BPMN Documentation](https://docs.camunda.org/manual/latest/reference/bpmn20/) — BPMN 可执行语义参考；核查日期：2026-07-08
> - [Camunda DMN Documentation](https://docs.camunda.org/manual/latest/reference/dmn11/) — DMN 决策表执行参考；核查日期：2026-07-08
>
> **核查日期**: 2026-07-08

---


<!-- SOURCE: struct/02-business-architecture-reuse/07-defense-mission-engineering/dodaf-uaf-reuse.md -->

# DoDAF / UAF 1.3 / NAF 4.0 与软件架构复用视角映射

> **版本**: 2026-06-10
> **定位**: 业务架构复用层 — 国防与使命工程视角
> **对齐标准**: DoDAF 2.02 / UAF 1.3 / NAF 4.0 / ISO/IEC/IEEE 42010:2022
> **状态**: ✅ 已完成
> **字数**: ~4000 字

---

## 目录

- [DoDAF / UAF 1.3 / NAF 4.0 与软件架构复用视角映射](#dodaf--uaf-13--naf-40-与软件架构复用视角映射)
  - [目录](#目录)
  - [1. DoDAF 2.02 概览](#1-dodaf-202-概览)
    - [1.1 八大核心视点](#11-八大核心视点)
    - [1.2 视点间的逻辑关系](#12-视点间的逻辑关系)
    - [1.3 元模型与本体基础](#13-元模型与本体基础)
  - [2. UAF 1.3 更新与使命工程建模](#2-uaf-13-更新与使命工程建模)
    - [2.1 UAF 的设计目标](#21-uaf-的设计目标)
    - [2.2 UAF 1.3 的域结构](#22-uaf-13-的域结构)
    - [2.3 Mission Engineering Modeling 扩展](#23-mission-engineering-modeling-扩展)
    - [2.4 NoMagic 2026x 实现特性](#24-nomagic-2026x-实现特性)
  - [3. NAF 4.0 简介](#3-naf-40-简介)
    - [3.1 NAF 4.0 的架构层级](#31-naf-40-的架构层级)
    - [3.2 NAF 4.0 的核心增强](#32-naf-40-的核心增强)
    - [3.3 与 UAF 的关系](#33-与-uaf-的关系)
  - [4. 复用视角映射](#4-复用视角映射)
    - [4.1 DoDAF Capability Viewpoint → 业务架构复用（能力视角）](#41-dodaf-capability-viewpoint--业务架构复用能力视角)
      - [映射逻辑](#映射逻辑)
      - [复用实践要点](#复用实践要点)
    - [4.2 DoDAF Services Viewpoint → 应用架构复用（服务契约）](#42-dodaf-services-viewpoint--应用架构复用服务契约)
      - [映射逻辑](#映射逻辑-1)
      - [复用实践要点](#复用实践要点-1)
    - [4.3 DoDAF Systems Viewpoint → 组件架构复用（系统元素）](#43-dodaf-systems-viewpoint--组件架构复用系统元素)
      - [映射逻辑](#映射逻辑-2)
      - [复用实践要点](#复用实践要点-2)
    - [4.4 DoDAF Operational Viewpoint → 业务流程复用（作战活动）](#44-dodaf-operational-viewpoint--业务流程复用作战活动)
      - [映射逻辑](#映射逻辑-3)
      - [复用实践要点](#复用实践要点-3)
    - [4.5 映射总结](#45-映射总结)
  - [5. 跨组织复用特殊挑战](#5-跨组织复用特殊挑战)
    - [5.1 多国安审（Multi-National Security Accreditation）](#51-多国安审multi-national-security-accreditation)
      - [挑战描述](#挑战描述)
      - [应对策略](#应对策略)
    - [5.2 保密分级与信息隔离](#52-保密分级与信息隔离)
      - [挑战描述](#挑战描述-1)
      - [应对策略](#应对策略-1)
    - [5.3 互操作性等级（Level of Interoperability, LOI）](#53-互操作性等级level-of-interoperability-loi)
      - [复用策略与 LOI 的对应](#复用策略与-loi-的对应)
    - [5.4 指挥关系与文化差异](#54-指挥关系与文化差异)
  - [6. 与 ISO/IEC/IEEE 42010:2022 的对照](#6-与-iso-420102022-的对照)
    - [6.1 ISO/IEC/IEEE 42010:2022 核心概念](#61-iso-420102022-核心概念)
    - [6.2 DoDAF 到 ISO/IEC/IEEE 42010:2022 的映射](#62-dodaf-到-iso-420102022-的映射)
    - [6.3 UAF 到 ISO/IEC/IEEE 42010:2022 的映射](#63-uaf-到-iso-420102022-的映射)
    - [6.4 NAF 4.0 到 ISO/IEC/IEEE 42010:2022 的映射](#64-naf-40-到-iso-420102022-的映射)
    - [6.5 综合对照意义](#65-综合对照意义)
  - [7. 案例：NATO 联邦任务网络中的架构复用实践](#7-案例nato-联邦任务网络中的架构复用实践)
    - [7.1 背景](#71-背景)
    - [7.2 FMN 的架构复用层级](#72-fmn-的架构复用层级)
      - [7.2.1 联盟级复用（Alliance Level）](#721-联盟级复用alliance-level)
      - [7.2.2 任务级复用（Mission Level）](#722-任务级复用mission-level)
      - [7.2.3 国家贡献级复用（National Contribution Level）](#723-国家贡献级复用national-contribution-level)
    - [7.3 FMN 中的 DoDAF/NAF 映射实践](#73-fmn-中的-dodafnaf-映射实践)
    - [7.4 FMN 互操作性等级与复用深度](#74-fmn-互操作性等级与复用深度)
    - [7.5 经验教训](#75-经验教训)
  - [8. 权威来源](#8-权威来源)

---

## 1. DoDAF 2.02 概览

美国国防部架构框架（Department of Defense Architecture Framework, DoDAF）2.02 版是指导美国国防及情报体系进行企业架构开发的核心标准。该框架以**视点（Viewpoint）**为中心组织，共定义了八个核心视点，每个视点提供一组模型，用于从特定利益相关者角度描述复杂国防系统的架构信息。

### 1.1 八大核心视点

| 视点缩写 | 全称 | 核心关注点 | 与复用体系的对应关系 |
|---------|------|-----------|-------------------|
| AV | All Viewpoint | 全局概述、范围、背景 | 体系级元数据与治理基线 |
| CV | Capability Viewpoint | 能力需求、能力层次、能力依赖 | **业务架构复用（能力视角）** |
| DIV | Data and Information Viewpoint | 数据模型、信息交换、语义互操作 | 跨层数据治理与信息复用 |
| OV | Operational Viewpoint | 作战活动、节点、信息流 | **业务流程复用（作战活动）** |
| PV | Project Viewpoint | 项目规划、采办里程碑、资源分配 | 项目组合治理与里程碑复用 |
| SvcV | Services Viewpoint | 服务描述、服务接口、服务组合 | **应用架构复用（服务契约）** |
| StdV | Standards Viewpoint | 技术标准、规范、协议约束 | 组件互操作性基线与标准复用 |
| SV | Systems Viewpoint | 系统组成、接口、功能分配 | **组件架构复用（系统元素）** |

### 1.2 视点间的逻辑关系

DoDAF 2.02 强调以**能力为中心**的架构开发方法（Capability-Based Planning）。各视点并非孤立存在，而是通过一系列跨视点关联形成有机整体：

- **CV → OV**: 能力需求驱动作战活动的定义与组织；
- **OV → SV**: 作战活动分解为系统功能，并分配至具体系统资源；
- **SV → SvcV**: 系统内部功能可通过服务化封装实现跨系统复用；
- **SvcV → StdV**: 服务接口必须遵循约定的技术标准，确保互操作性；
- **DIV 横贯全层**: 数据与信息视点提供跨所有视点的语义一致性保障。

这种以能力为牵引、多视点协同的架构方法，天然与本知识体系的四层复用模型（业务→应用→组件→功能）存在结构性对应关系。

### 1.3 元模型与本体基础

DoDAF 2.02 基于**DM2（DoDAF Meta-Model 2.0）**定义了严格的架构数据本体，包含：

- **概念数据模型（CDM）**: 高阶本体概念，如能力、活动、资源、服务；
- **逻辑数据模型（LDM）**: 概念之间的关系与约束；
- **物理交换规范（PES）**: 具体的 XML Schema 与交换格式。

DM2 的本体结构为跨项目、跨组织的架构资产复用提供了形式化基础。任何符合 DM2 的架构模型均可被解析、索引、匹配与重构，这是实现自动化架构复用的前提条件。

---

## 2. UAF 1.3 更新与使命工程建模

统一架构框架（Unified Architecture Framework, UAF）1.3 版由 Object Management Group（OMG）发布，并在 NoMagic（现 Dassault Systèmes）Cameo Systems Modeler 2026x 版本中实现。UAF 并非替代 DoDAF，而是对其进行统一、扩展与现代化的框架级整合。

### 2.1 UAF 的设计目标

UAF 1.3 的核心设计目标包括：

1. **统一多框架**: 将 DoDAF、MODAF（英国国防部架构框架）、NAF（北约架构框架）整合至单一元模型；
2. **兼容 SysML**: 基于 OMG SysML v2 的语义基础，实现系统建模与企业架构建模的无缝衔接；
3. **支持使命工程（Mission Engineering）**: 引入使命线程分析、使命效能评估等扩展概念；
4. **增强可执行性**: 支持行为模拟、参数分析、权衡空间探索。

### 2.2 UAF 1.3 的域结构

UAF 1.3 定义了以下核心域（Domain），每个域对应一组视图（View）：

| 域 | 说明 | 新增特性 |
|---|------|---------|
| Strategic | 战略目标、愿景、利益相关者需求 | 使命工程上下文映射 |
| Operational | 作战活动、资源流、状态机 | 增强的行为模拟支持 |
| Personnel | 人员角色、技能、组织关系 | 人力资源能力建模 |
| Resources | 物理与逻辑资源、系统、服务 | 与 SysML v2 块定义对齐 |
| Security | 安全策略、威胁、控制措施 | 网络安全与供应链安全扩展 |
| Projects | 项目、里程碑、采办决策 | 敏捷与 DevSecOps 融合 |
| Standards | 标准、协议、约束 | 动态标准版本追踪 |
| Actual Resources | 实际部署的实例化资源 | 数字孪生映射支持 |

### 2.3 Mission Engineering Modeling 扩展

UAF 1.3 最重要的新增特性之一是**使命工程建模**支持。使命工程强调从顶层使命目标出发，向下分解为可量化的能力需求、系统功能与资源配置。其关键建模元素包括：

- **Mission Thread**: 描述完成特定使命所需的端到端活动序列与资源交互；
- **Mission Measure**: 定义使命成功的量化指标（如时间、可用性、效能）；
- **Mission Element**: 参与使命的物理或逻辑实体，可与 DoDAF 的节点、系统、服务建立映射；
- **Operational Scenario**: 支持多分支、多状态的行为场景模拟。

从复用视角看，使命工程模型提供了**高阶意图（Intent）**的形式化表达。使命线程本身可作为复用资产，在不同任务背景下通过参数化调整实现快速重构。

### 2.4 NoMagic 2026x 实现特性

在工具层面，NoMagic Cameo Systems Modeler 2026x 对 UAF 1.3 的实现提供了以下关键特性：

- **多框架项目模板**: 支持在单一模型库中同时维护 DoDAF、MODAF、NAF、UAF 视图；
- **智能映射引擎**: 自动检测跨视点、跨框架的元素冗余，推荐复用或合并策略；
- **参数化架构模板**: 支持将完整的视点模型保存为可复用模板（Architecture Pattern），并在新项目中实例化；
- **API 与脚本支持**: 通过 Java/REST API 实现架构资产的程序化检索与复用。

---

## 3. NAF 4.0 简介

北约架构框架（NATO Architecture Framework, NAF）4.0 版是北约及其成员国进行企业架构开发与互操作性评估的标准框架。NAF 4.0 在继承 NAF 3.1 的基础上，进行了大幅度的结构优化与语义增强，并与 UAF 1.1+ 保持元模型级对齐。

### 3.1 NAF 4.0 的架构层级

NAF 4.0 采用四层结构组织架构描述：

1. **架构参考模型（Architecture Reference Model）**: 提供跨北约企业架构的通用语义基线；
2. **架构元模型（Architecture Meta-Model, NAF MM）**: 基于 UAF 元模型定制，包含北约特定的扩展（如联盟作战概念、多国指挥关系）；
3. **架构视图（Architecture Views）**: 共定义 8 个视点、47 个视图，与 DoDAF 2.02 视点基本对应但增加了北约特有的治理视图；
4. **架构产品（Architecture Products）**: 具体的模型实例、图表、文档与交换文件。

### 3.2 NAF 4.0 的核心增强

| 增强领域 | 具体内容 |
|---------|---------|
| 联盟互操作性 | 新增联盟互操作性等级（LOI）评估模型，直接关联架构描述 |
| 赛博安全 | 将赛博安全架构作为一级视点，而非横贯关注点 |
| 服务导向 | 强化服务视图（NSOV），与北约网络使能能力（NNEC）对齐 |
| 敏捷采办 | 引入增量交付与能力持续集成概念 |
| 数据主权 | 明确多国数据共享中的主权边界与访问控制 |

### 3.3 与 UAF 的关系

NAF 4.0 与 UAF 1.3 之间存在双向映射关系：

- **NAF → UAF**: NAF 元模型是 UAF 元模型的北约定制子集，任何符合 NAF 4.0 的模型均可无损导入 UAF 1.3 工具环境；
- **UAF → NAF**: UAF 的通用使命工程扩展可为 NAF 提供额外的分析能力，但需经过北约标准化办公室（NSO）的合规审查。

这种互操作性为北约框架下的多国架构复用奠定了技术基础。

---

## 4. 复用视角映射

本节建立 DoDAF / UAF / NAF 的架构视点与本知识体系四层复用模型之间的系统性映射关系，明确国防架构资产在软件架构复用中的定位与转换规则。

### 4.1 DoDAF Capability Viewpoint → 业务架构复用（能力视角）

#### 映射逻辑

DoDAF 能力视点（CV）关注"需要具备什么能力"，而非"如何实现"。这种与实现解耦的抽象层次，与业务架构复用层关注"业务能力标准化与复用"的目标高度一致。

| DoDAF CV 模型 | 复用层对应概念 | 复用模式 |
|--------------|--------------|---------|
| CV-1 能力愿景 | 业务愿景与战略目标模板 | 愿景陈述模板复用 |
| CV-2 能力分类 | 能力领域目录与分类体系 | 领域本体复用 |
| CV-3 能力阶段 | 能力演进路线图 | 路线图模式库复用 |
| CV-4 能力依赖 | 能力依赖关系网 | 依赖拓扑模式复用 |
| CV-5 能力到组织映射 | 业务能力到组织单元的分配模式 | 治理结构模板复用 |
| CV-6 能力到作战映射 | 能力到业务流程的追溯链 | 追溯矩阵模板复用 |
| CV-7 能力到服务映射 | 业务能力到 IT 服务的映射模式 | 业务-IT 对齐模板复用 |

#### 复用实践要点

1. **能力本体标准化**: 将 CV-2 的能力分类结构转化为可复用的领域本体（Domain Ontology），在多个国防项目中通过本体继承实现能力定义的一致性；
2. **能力差距分析模板**: CV-3 定义的能力阶段（如当前、中期、目标）可固化为差距分析模板，复用于不同项目的架构规划；
3. **能力依赖模式库**: CV-4 描述的能力依赖关系（如"情报监视能力依赖于通信传输能力"）可抽象为通用的依赖模式，在相似任务域中直接复用。

### 4.2 DoDAF Services Viewpoint → 应用架构复用（服务契约）

#### 映射逻辑

DoDAF 服务视点（SvcV）描述服务的规格、接口、行为与编排，这与应用架构复用层关注"服务契约标准化与服务组合复用"的核心目标直接对应。

| DoDAF SvcV 模型 | 复用层对应概念 | 复用模式 |
|----------------|--------------|---------|
| SvcV-1 服务组合 | 应用服务目录与组合结构 | 服务组合模板复用 |
| SvcV-2 服务资源流 | 服务间数据交换契约 | 接口契约模式复用 |
| SvcV-3a 系统-服务矩阵 | 系统到服务的映射矩阵 | 映射矩阵模板复用 |
| SvcV-3b 服务-服务矩阵 | 服务间交互矩阵 | 交互拓扑模式复用 |
| SvcV-4 服务功能 | 服务内部功能分解 | 功能分解模式复用 |
| SvcV-5 作战到服务映射 | 业务活动到服务的追溯 | 追溯链模板复用 |
| SvcV-6 服务资源流矩阵 | 服务交换的详细数据规范 | 消息契约模式复用 |
| SvcV-7 服务度量 | 服务级目标（SLO）定义 | 度量模板复用 |
| SvcV-8 服务演进 | 服务版本演进路线图 | 演进规划模板复用 |
| SvcV-9 服务技术与技能 | 服务实现所需技术栈 | 技术栈模板复用 |
| SvcV-10a 服务规则模型 | 服务业务规则 | 规则模式复用 |
| SvcV-10b 服务状态模型 | 服务生命周期状态机 | 状态机模式复用 |

#### 复用实践要点

1. **服务契约标准化**: 将 SvcV-6 的服务资源流规范转化为标准化的服务契约（如 OpenAPI、WSDL、IDL），纳入应用架构复用资产库；
2. **服务组合模式**: SvcV-1 描述的服务层次结构可抽象为通用的服务组合模式（如编排模式、协同模式、代理模式），在多个指挥控制系统中复用；
3. **服务度量基线**: SvcV-7 定义的服务度量指标可固化为国防特定行业的 SLO 模板，如通信服务的可用性≥99.9%、情报服务的响应时间≤5秒等。

### 4.3 DoDAF Systems Viewpoint → 组件架构复用（系统元素）

#### 映射逻辑

DoDAF 系统视点（SV）描述系统的组成、接口、功能分配与物理部署，与组件架构复用层关注"可复用系统元素与组件接口标准化"的目标直接对应。

| DoDAF SV 模型 | 复用层对应概念 | 复用模式 |
|-------------|--------------|---------|
| SV-1 系统组合 | 系统/子系统目录与层次结构 | 系统分解模式复用 |
| SV-2 系统资源流 | 系统间接口与数据交换 | 接口契约复用 |
| SV-3 系统-系统矩阵 | 系统互连关系矩阵 | 互连拓扑模式复用 |
| SV-4 系统功能 | 系统内部功能分解 | 功能分配模式复用 |
| SV-5 作战到系统映射 | 作战活动到系统功能的追溯 | 追溯链模板复用 |
| SV-6 系统资源流矩阵 | 系统交换的详细规范 | 消息协议复用 |
| SV-7 系统度量 | 系统性能指标基线 | 性能模板复用 |
| SV-8 系统演进 | 系统升级与替换路线图 | 演进规划模板复用 |
| SV-9 系统技术与技能 | 系统实现所需技术与人员技能 | 技术栈与技能模板复用 |
| SV-10a 系统规则模型 | 系统业务规则 | 规则引擎配置复用 |
| SV-10b 系统状态模型 | 系统状态机与模式转换 | 状态机模式复用 |
| SV-10c 系统事件-轨迹 | 系统事件序列与场景 | 场景模板复用 |

#### 复用实践要点

1. **系统元素目录化**: 将 SV-1 定义的系统组成结构转化为可检索的系统元素目录，每个系统元素附带标准化接口规范（SV-2）与性能基线（SV-7）；
2. **接口契约复用**: SV-2 与 SV-6 定义的系统间接口规范可直接作为组件架构的接口契约复用资产，特别适用于指挥控制（C2）系统、通信系统、传感器系统的集成场景；
3. **系统状态机模式**: SV-10b 描述的系统状态转换（如"待机→激活→任务执行→回收"）可抽象为通用的状态机模板，在相似装备类型的系统设计中复用。

### 4.4 DoDAF Operational Viewpoint → 业务流程复用（作战活动）

#### 映射逻辑

DoDAF 作战视点（OV）描述作战活动、节点、信息流与状态转换，是国防领域特有的"业务流程"表达形式，与本知识体系的业务流程复用层存在直接映射。

| DoDAF OV 模型 | 复用层对应概念 | 复用模式 |
|-------------|--------------|---------|
| OV-1 高层作战概念图 | 业务场景与高层流程视图 | 场景模板复用 |
| OV-2 作战资源流描述 | 作战节点间信息/物资流 | 流程流模式复用 |
| OV-3 作战资源流矩阵 | 资源流的详细规范 | 交换矩阵模板复用 |
| OV-4 组织关系图 | 组织架构与指挥关系 | 组织结构模板复用 |
| OV-5a 作战活动分解树 | 作战活动层次分解 | 活动分解模式复用 |
| OV-5b 作战活动模型 | 作战活动详细行为模型 | 流程模型复用 |
| OV-6a 作战规则模型 | 作战业务规则 | 规则模式复用 |
| OV-6b 作战状态转换 | 作战状态机 | 状态机模式复用 |
| OV-6c 作战事件-轨迹 | 作战场景与事件序列 | 场景模板复用 |

#### 复用实践要点

1. **作战活动标准化**: 将 OV-5a 的作战活动分解结构（如 OODA 环：观察→定向→决策→行动）固化为标准化的作战活动模板，在不同军种、不同任务类型的系统中复用；
2. **指挥关系模式**: OV-4 描述的组织与指挥关系可抽象为通用的指挥控制模式（如层级指挥、扁平化指挥、网络化指挥），在多国军演系统、联合特遣队支持系统中复用；
3. **信息流模式**: OV-2 与 OV-3 描述的节点间信息流可抽象为通用的信息交换模式（如请求-响应、发布-订阅、广播），在 C4ISR 系统的接口设计中复用。

### 4.5 映射总结

| 国防架构视点 | 复用模型层 | 核心复用资产类型 | 关键标准化对象 |
|-----------|----------|---------------|-------------|
| Capability Viewpoint (CV) | 业务架构复用 | 能力本体、路线图模板、差距分析模板 | 能力分类体系、度量指标 |
| Operational Viewpoint (OV) | 业务流程复用 | 作战活动模型、指挥关系模式、信息流模式 | 活动分解结构、状态机 |
| Services Viewpoint (SvcV) | 应用架构复用 | 服务契约、服务组合模式、SLO 模板 | 接口规范、服务编排规则 |
| Systems Viewpoint (SV) | 组件架构复用 | 系统元素目录、接口契约、状态机模式 | 接口协议、性能基线 |

---

## 5. 跨组织复用特殊挑战

国防领域的架构复用不同于商业领域，其核心特征在于**跨主权国家、跨保密等级、跨指挥体系**的协同需求。本节分析军事联盟中进行架构资产复用时面临的特殊挑战与应对策略。

### 5.1 多国安审（Multi-National Security Accreditation）

#### 挑战描述

北约或其他军事联盟中的架构复用必须满足每个成员国的独立安全审查要求。同一架构资产可能在不同国家被评定为不同的保密等级，导致"最低公分母"效应——即联盟只能复用所有国家均可访问的那部分资产，严重限制了复用深度。

#### 应对策略

1. **分级资产库**: 建立多级的架构资产库，同一资产维护多个保密等级的版本（如公开版、限制版、机密版），通过自动化脱敏工具生成低等级版本；
2. **联盟共同框架**: 在联盟层面预先定义"共同可复用基线"（Common Reusable Baseline），该基线仅包含经所有成员国预先审查通过的通用概念与接口；
3. **动态访问控制**: 基于属性的访问控制（ABAC）机制，根据用户国籍、军衔、任务角色动态决定可访问的架构资产范围。

### 5.2 保密分级与信息隔离

#### 挑战描述

国防架构模型中嵌入了大量敏感信息：部队编制、装备性能参数、通信频率、密码算法接口等。在复用过程中，如何剥离或泛化敏感信息，同时保留架构的结构价值，是核心难题。

#### 应对策略

1. **参数化泛化**: 将敏感数值参数抽象为变量占位符（如"最大通信距离 = $PARAM_RANGE"），复用时根据使用环境注入具体数值；
2. **视图级隔离**: 利用 DoDAF/UAF 的多视点结构，将敏感信息集中在特定视图（如 SV-7 性能度量）中，其他视图保持非密，实现"结构复用、数据隔离"；
3. **密码学保护**: 对高密级架构资产采用端到端加密存储与传输，仅在经认证的本地环境中解密使用。

### 5.3 互操作性等级（Level of Interoperability, LOI）

北约及多国联合作战语境下，互操作性不仅是一个二元概念（能否互通），而是分等级的成熟度模型。NAF 4.0 与 NATO NNEC 框架共同定义了 LOI 1-4 四个等级：

| 等级 | 名称 | 定义 | 架构复用含义 |
|-----|------|------|------------|
| LOI 1 | 孤立（Isolated） | 无互连，独立运行 | 无需考虑复用，架构资产完全独立 |
| LOI 2 | 连通（Connected） | 物理连通，可交换数据 | 需复用物理接口标准与数据格式规范 |
| LOI 3 | 功能（Functional） | 能理解交换数据的语义 | 需复用信息交换模型与语义本体 |
| LOI 4 | 领域（Domain） | 共享领域认知，协同决策 | 需复用完整的作战活动模型、指挥关系模式与决策规则 |

#### 复用策略与 LOI 的对应

- **目标 LOI 2**: 重点复用系统视点（SV）中的接口契约与数据交换规范；
- **目标 LOI 3**: 额外复用数据与信息视点（DIV）中的语义模型与信息交换矩阵；
- **目标 LOI 4**: 全面复用作战视点（OV）与能力视点（CV）中的业务流程、指挥关系与决策规则。

架构复用的深度应直接对应目标互操作性等级，避免"过度复用"（在高 LOI 场景中使用低 LOI 资产，导致语义不一致）或"复用不足"（在低 LOI 场景中强制引入高 LOI 资产，增加不必要的复杂度）。

### 5.4 指挥关系与文化差异

不同国家的军事组织在指挥哲学、决策流程、报告关系上存在深层文化差异。直接复用他国架构中的组织模型（OV-4）可能导致指挥冲突或决策延迟。

**应对策略**: 将组织模型中的"文化敏感元素"（如指挥链长度、决策授权级别）参数化，复用时根据参与国的组织文化注入适配值，保留结构骨架，灵活调整内容。

---

## 6. 与 ISO 42010:2022 的对照

ISO/IEC/IEEE 42010:2022《系统与软件工程 — 架构描述》是国际标准化组织发布的通用架构描述框架标准。
将 DoDAF/UAF/NAF 映射至 ISO/IEC/IEEE 42010:2022，有助于理解国防架构框架在通用架构理论中的定位，并促进国防架构与民用架构的互理解。

### 6.1 ISO 42010:2022 核心概念

ISO 42010:2022 定义了以下核心概念：

- **系统（System）**: 感兴趣的实体，可由其他系统组成；
- **架构（Architecture）**: 系统的基本组织方式，体现在其组件、组件间关系、组件与环境的关系，以及指导其设计与演化的原则；
- **利益相关者（Stakeholder）**: 对系统有关切的人、团队或组织；
- **关切（Concern）**: 利益相关者对系统的利益点；
- **视点（Viewpoint）**: 针对一类特定关切，进行架构描述的约定规范；
- **视图（View）**: 从特定视点出发的架构描述作品；
- **模型种类（Model Kind）**: 视图中使用的模型类型约定；
- **架构描述（Architecture Description）**: 记录架构的工件集合，由一个或多个视图组成。

### 6.2 DoDAF 到 ISO 42010:2022 的映射

| ISO 42010:2022 概念 | DoDAF 2.02 对应概念 | 说明 |
|-------------------|-------------------|------|
| 系统 | Mission / Capability / System | DoDAF 在不同视点中分别将任务、能力、系统作为"感兴趣系统" |
| 利益相关者 | 利益相关者（AV-1 中定义） | DoDAF AV-1 明确要求列出所有利益相关者 |
| 关切 | 关切（Concern） | DoDAF 2.02 在视点定义中隐含了关切分类，但未显式使用"Concern"术语 |
| 视点 | Viewpoint（AV-1, 各视点定义） | DoDAF 的 8 个视点直接对应 ISO 42010 的视点概念 |
| 视图 | View / Model | DoDAF 的模型（如 CV-1, OV-1）本质上是视图 |
| 模型种类 | DM2 概念数据模型 | DM2 定义了 DoDAF 使用的模型种类本体 |
| 架构描述 | 架构描述（Architecture Description） | DoDAF 2.02 明确要求产出完整的架构描述文档集 |
| 对应关系 | 对应关系（Mapping） | DoDAF 的跨视点关系矩阵对应 ISO 42010 的对应关系概念 |

### 6.3 UAF 到 ISO 42010:2022 的映射

UAF 1.3 在设计上更贴近 ISO/IEC/IEEE 42010:2022 的现代概念体系：

| ISO 42010:2022 概念 | UAF 1.3 对应概念 | 说明 |
|-------------------|----------------|------|
| 视点 | View Specification | UAF 明确使用视点规范定义视图约定 |
| 视图 | View / Diagram | UAF 的视图是视点的实例化 |
| 模型种类 | Model Kind | UAF 元模型中显式定义模型种类 |
| 架构描述 | Architecture Description | UAF 项目即是一个完整的架构描述 |
| 架构决策 | Trade-off Analysis / Decision | UAF 1.3 新增决策记录支持 |
| 架构原理 | Architectural Principle | UAF Strategic 域中可定义架构原理 |

### 6.4 NAF 4.0 到 ISO 42010:2022 的映射

NAF 4.0 在元模型设计中直接参考了 ISO/IEC/IEEE 42010:2022 的术语体系，其映射最为直接：

- **NAF 视点（Viewpoint）** = ISO/IEC/IEEE 42010:2022 视点
- **NAF 视图（View）** = ISO/IEC/IEEE 42010:2022 视图
- **NAF 元模型（Meta-Model）** = ISO/IEC/IEEE 42010:2022 模型种类规范 + 对应关系规范
- **NAF 架构描述（Architecture Description）** = ISO/IEC/IEEE 42010:2022 架构描述

### 6.5 综合对照意义

通过 ISO/IEC/IEEE 42010:2022 的中立框架，可以实现以下跨框架复用目标：

1. **元模型桥接**: 使用 ISO/IEC/IEEE 42010:2022 的对应关系机制，建立 DoDAF 元素与 UAF 元素、NAF 元素之间的形式化映射；
2. **工具互操作**: 任何符合 ISO/IEC/IEEE 42010:2022 的架构工具均可通过适配层导入/导出 DoDAF/UAF/NAF 模型；
3. **培训与知识转移**: 以 ISO/IEC/IEEE 42010:2022 为共同语言，降低不同框架背景架构师之间的沟通成本；
4. **复用资产标准化**: 将国防架构复用资产（如能力本体、服务契约、接口规范）封装为符合 ISO/IEC/IEEE 42010:2022 的通用架构描述组件，实现跨领域复用。

---

## 7. 案例：NATO 联邦任务网络中的架构复用实践

### 7.1 背景

NATO Federated Mission Networking（FMN）是北约推动的多国联合作战网络架构倡议，旨在通过标准化的架构框架、接口规范与治理流程，实现成员国军事网络在任务期间的快速互联、协同作战与安全信息共享。FMN 是国防领域架构复用的典型实践场域。

### 7.2 FMN 的架构复用层级

FMN 将架构复用组织为三个层级：

#### 7.2.1 联盟级复用（Alliance Level）

由北约标准化办公室（NSO）维护的**FMN 联盟架构描述（Federated Mission Networking Alliance Architecture Description, FMN AD）**是最高阶的复用资产，包含：

- **联盟能力视图（FMN CV）**: 定义所有 FMN 参与国共同认可的能力需求，如"态势感知共享能力"、"协同计划能力"；
- **联盟服务视图（FMN SvcV）**: 定义标准化的服务接口规范（如 BMSCS - Battle Management Services Core Services），任何成员国的系统只要实现该接口即可接入联盟网络；
- **联盟标准视图（FMN StdV）**: 定义强制性与推荐性技术标准清单，如 IPv6、NFFI（NATO Friendly Force Information）、STANAG 相关协议。

#### 7.2.2 任务级复用（Mission Level）

针对具体任务（如某次联合军演或实战部署），由任务网络设计机构（MNDA）基于联盟级资产定制**任务网络架构描述（Mission Network Architecture Description）**：

- 从联盟能力视图中选取与本任务相关的能力子集；
- 从联盟服务视图中选取需要部署的服务子集，并注入任务特定的参数（如通信带宽、延迟要求）；
- 复用联盟标准视图中的技术基线，必要时增加任务特定的补充标准。

#### 7.2.3 国家贡献级复用（National Contribution Level）

各成员国根据任务网络架构描述，将本国现有的军事信息系统（National Systems）适配为**国家贡献（National Contribution）**：

- 复用联盟定义的服务接口规范，开发或配置适配器（Adapter）；
- 复用联盟定义的作战活动模型（源自 OV-5a/b），将本国系统的业务功能映射至联盟标准作战活动；
- 复用联盟定义的信息交换模型（源自 DIV），确保本国系统产生的数据符合联盟语义标准。

### 7.3 FMN 中的 DoDAF/NAF 映射实践

FMN 架构描述采用 NAF 4.0 作为主要框架，同时通过 UAF 1.3 的工具支持实现与 DoDAF 2.02 的双向映射：

| FMN 架构资产 | 采用的框架 | 复用范围 |
|-----------|----------|---------|
| 联盟能力需求 | NAF 4.0 CV + DoDAF CV | 所有 FMN 参与国 |
| 联盟服务规范 | NAF 4.0 SvcV + DoDAF SvcV | 所有 FMN 参与国 |
| 联盟作战活动 | NAF 4.0 OV + DoDAF OV | 所有 FMN 参与国 |
| 国家系统架构 | DoDAF 2.02（美国）/ 各国等效框架 | 仅本国 |
| 国家-联盟映射 | UAF 1.3 跨框架映射 | 任务网络设计机构 |

### 7.4 FMN 互操作性等级与复用深度

FMN 将 LOI 概念应用于任务网络的规划与评估：

- **FMN Spiral 1-3（2015-2020）**: 主要达到 LOI 2（连通级），复用重点在系统视点的接口规范（物理层与数据链路层）；
- **FMN Spiral 4+（2021-至今）**: 目标达到 LOI 3（功能级），复用深度扩展至数据与信息视点的语义模型，要求所有参与系统使用统一的数据元素字典（如 JC3IEDM / ADatP-3）；
- **未来目标（FMN Vision 2030）**: 向 LOI 4（领域级）演进，要求复用完整的作战活动模型与决策支持规则，实现真正意义上的"联合认知域作战"。

### 7.5 经验教训

1. **标准化先于复用**: FMN 的成功证明，没有联盟层面的标准化架构描述（NAF/DoDAF 视点定义），跨组织复用无从谈起；
2. **渐进式 LOI 提升**: 试图一次性达到 LOI 4 是不现实的，FMN 采用螺旋式（Spiral）开发，逐步提升复用深度与互操作等级；
3. **治理重于技术**: 多国架构复用的最大障碍不是技术，而是治理——安全审查流程、知识产权归属、变更控制机制必须预先明确；
4. **工具链统一**: FMN 强制要求使用支持 UAF 1.3 的建模工具（如 Cameo Systems Modeler），确保所有成员国的架构模型可在同一环境中进行差异分析、一致性检查与复用推荐。

---

## 8. 权威来源

1. **DoDAF 2.02 官方规范**
   URL: <https://dodcio.defense.gov/library/dod-architecture-framework/>
   核查日期: 2026-06-10

2. **OMG Unified Architecture Framework (UAF) 1.3**
   URL: <https://www.omg.org/spec/UAF/>
   核查日期: 2026-06-10

3. **NATO Architecture Framework v4, NATO Standardization Office**
   URL: <https://nsa.nato.int/naf>
   核查日期: 2026-06-10

4. **ISO/IEC/IEEE 42010:2022, Systems and software engineering — Architecture description**
   URL: <https://www.iso.org/standard/74296.html>
   核查日期: 2026-06-10

5. **NATO Federated Mission Networking (FMN) Implementation Plan**
   URL: <https://www.act.nato.int/fmn>
   核查日期: 2026-06-10

6. **DoDAF Volume 1, Introduction, Overview, and Concepts Manager's Guide**
   URL: <https://dodcio.defense.gov/library/dod-architecture-framework/dodaf20_vol1/>
   核查日期: 2026-06-10

7. **DoDAF Volume 2, Architectural Data and Models**
   URL: <https://dodcio.defense.gov/library/dod-architecture-framework/dodaf20_vol2/>
   核查日期: 2026-06-10

8. **OMG SysML v2 Specification**
   URL: <https://www.omg.org/spec/SysML/>
   核查日期: 2026-06-10

9. **NATO NNEC (NATO Network-Enabled Capability) Feasibility Study**
   URL: <https://www.nato.int/cps/en/natohq/topics_91048.htm>
   核查日期: 2026-06-10

10. **Dassault Systèmes Cameo Systems Modeler — UAF Plugin Documentation**
    URL: <https://www.3ds.com/products-services/catia/products/no-magic/cameo-systems-modeler/>
    核查日期: 2026-06-10

---

> 本文档作为软件架构复用知识体系在国防与使命工程领域的视角映射，为军事联盟、国防承包商及跨国军演系统的架构师提供复用框架指引。在实际应用中，应结合具体任务的安全等级、互操作性目标与参与国治理要求，选择适当的视点映射策略与复用深度。

---


<!-- SOURCE: struct/02-business-architecture-reuse/07-defense-mission-engineering/naf-modaf-reuse.md -->

# NAF 4.0 / MODAF 与北约架构复用视角映射

> **版本**: 2026-06-10
> **定位**: 业务架构复用层 — 国防与使命工程视角（北约/英国专用补充）
> **对齐标准**: NAF 4.0 / MODAF / DoDAF 2.02 / UAF 1.3
> **状态**: ✅ 已完成
> **字数**: ~4500 字

---

## 目录

- [NAF 4.0 / MODAF 与北约架构复用视角映射](#naf-40--modaf-与北约架构复用视角映射)
  - [目录](#目录)
  - [1. MODAF 概述](#1-modaf-概述)
    - [1.1 英国国防部架构框架的历史演进](#11-英国国防部架构框架的历史演进)
    - [1.2 MODAF 的核心设计哲学](#12-modaf-的核心设计哲学)
    - [1.3 MODAF 与 DoDAF 的关键差异](#13-modaf-与-dodaf-的关键差异)
    - [1.4 更强的能力建模与服务导向](#14-更强的能力建模与服务导向)
  - [2. NAF 4.0 概述](#2-naf-40-概述)
    - [2.1 元模型层（NMM）](#21-元模型层nmm)
    - [2.2 方法论层](#22-方法论层)
    - [2.3 视点层（七个核心视点）](#23-视点层七个核心视点)
    - [2.4 视图层](#24-视图层)
  - [3. NAF 4.0 与 DoDAF 2.02 / UAF 1.3 的对比矩阵](#3-naf-40-与-dodaf-202--uaf-13-的对比矩阵)
    - [3.1 元模型差异：NMM vs DM2 vs UAF Metamodel](#31-元模型差异nmm-vs-dm2-vs-uaf-metamodel)
    - [3.2 视点差异](#32-视点差异)
    - [3.3 互操作性支持差异](#33-互操作性支持差异)
  - [4. 北约架构复用的特殊挑战](#4-北约架构复用的特殊挑战)
    - [4.1 多国安全分级体系](#41-多国安全分级体系)
    - [4.2 28+ 成员国的架构协调](#42-28-成员国的架构协调)
    - [4.3 联盟采办框架（NSPA）中的架构复用](#43-联盟采办框架nspa中的架构复用)
  - [5. NAF 复用视角映射](#5-naf-复用视角映射)
    - [5.1 NAF Operational View → 业务架构复用（作战活动）](#51-naf-operational-view--业务架构复用作战活动)
    - [5.2 NAF Capability View → 业务能力复用（联盟能力目标）](#52-naf-capability-view--业务能力复用联盟能力目标)
    - [5.3 NAF Service View → 应用服务复用（互操作服务）](#53-naf-service-view--应用服务复用互操作服务)
    - [5.4 NAF System View → 组件/系统复用（联合系统）](#54-naf-system-view--组件系统复用联合系统)
  - [6. 与 DoDAF B-01 文档的互补关系](#6-与-dodaf-b-01-文档的互补关系)
  - [7. 案例：NATO JISR 架构复用](#7-案例nato-jisr-架构复用)
    - [7.1 JISR 背景与架构需求](#71-jisr-背景与架构需求)
    - [7.2 JISR 中的 NAF 4.0 复用实践](#72-jisr-中的-naf-40-复用实践)
    - [7.3 JISR 复用的互操作性等级与经验](#73-jisr-复用的互操作性等级与经验)
  - [8. 权威来源](#8-权威来源)
  - [补充说明：NAF 4.0 / MODAF 与北约架构复用视角映射](#补充说明naf-40--modaf-与北约架构复用视角映射)
  - [概念定义](#概念定义)
  - [反例](#反例)

---

## 1. MODAF 概述

### 1.1 英国国防部架构框架的历史演进

英国国防部架构框架（Ministry of Defence Architecture Framework, MODAF）是英国国防部用于指导国防体系架构开发的标准化方法。MODAF 的历史可追溯至 2004 年，最初基于 DoDAF 1.0 开发，但在后续演进中逐步形成了独特的欧洲国防架构风格。

MODAF 的发展经历了三个关键阶段：

- **MODAF 1.0（2005-2007）**: 直接继承 DoDAF 1.0 的六视点结构，增加了英国特定的采办与能力规划模型；
- **MODAF 1.2（2007-2010）**: 引入战略视点（Strategic Viewpoint, StV），强化顶层能力规划与战略对齐，这一创新后来被 NAF 3.0 吸收；
- **MODAF 1.2.004（2010-2014）**: 增强服务导向架构（SOA）支持，引入服务视点的完整模型集，使 MODAF 成为当时最强调服务互操作的国防架构框架。

2014 年后，英国国防部正式采纳 NAF 3.1 及后续版本作为联盟环境下的首选框架，但 MODAF 的设计思想——尤其是其能力建模方法与服务导向扩展——深深融入了 NAF 4.0 的 DNA 中。

### 1.2 MODAF 的核心设计哲学

MODAF 的设计哲学可概括为以下三点：

1. **能力驱动（Capability-Driven）**: 所有架构开发始于能力需求，终于能力交付。MODAF 将"能力"定义为"在特定标准与条件下，通过特定方式完成特定任务并实现特定效果的能力（Ability）"，强调能力不仅包含系统性能，还包含人员、流程、组织与信息要素的整合。

2. **服务解耦（Service Decoupling）**: MODAF 在 DoDAF 的基础上显著强化了服务视点的地位，主张通过定义清晰的服务契约（Service Contract）实现系统间的松耦合。这一思想直接影响了北约后续的服务导向基础设施（Service Oriented Infrastructure, SOI）建设。

3. **层级抽象（Hierarchical Abstraction）**: MODAF 明确区分战略层（Strategic）、作战层（Operational）与系统层（System），要求每一层级的架构描述必须向上可追溯（Traceable Upwards）且向下可分配（Allocable Downwards）。

### 1.3 MODAF 与 DoDAF 的关键差异

| 对比维度 | MODAF | DoDAF 2.02 |
|---------|-------|-----------|
| **能力建模深度** | 引入能力层次结构（Capability Hierarchy）与能力配置（Capability Configuration），支持能力的动态组合 | 以能力视图（CV）为主，侧重能力分类与依赖关系 |
| **服务导向支持** | 独立的服务视点（SvcV），包含 12 个服务模型，强调服务契约与编排 | 服务视点（SvcV）与系统视点（SV）界限较模糊 |
| **战略对齐** | 独立的战略视点（StV），直接映射国家安全战略与国防战略目标 | 通过全视点（AV）与能力视点（CV）间接体现战略意图 |
| **采办集成** | 与英国国防采办框架（CADMID/T 周期）深度集成 | 与 DoD 5000 系列采办指令集成 |
| **本体基础** | 基于 IDEAS 本体（International Defence Enterprise Architecture Specification） | 基于 DM2（DoDAF Meta-Model 2.0）本体 |

### 1.4 更强的能力建模与服务导向

MODAF 的能力建模方法具有以下独特优势，也是其区别于 DoDAF 的最显著特征：

**能力层次结构（Capability Hierarchy）**:
MODAF 将能力组织为三层结构——战略能力（Strategic Capability）、作战能力（Operational Capability）与功能能力（Functional Capability）。战略能力对应国家安全目标（如"维护联盟集体防御"），作战能力对应军事任务（如"联合防空作战"），功能能力对应系统功能（如"雷达目标跟踪"）。这种层次化建模使架构复用可以在不同粒度上精准定位：联盟级复用聚焦战略能力映射，任务级复用聚焦作战能力组合，系统级复用聚焦功能能力分配。

**能力配置（Capability Configuration）**:
MODAF 创新性地引入"能力配置"概念，将能力实例化为特定的人员、组织、系统与流程组合。一个能力需求可以通过多种配置实现，不同配置之间可以进行互操作性比较与成本效益分析。这为架构复用提供了关键机制——当需要复用某国现有系统以满足联盟能力需求时，可通过能力配置模型快速评估该国系统的适配度。

**服务契约模型（Service Contract Model）**:
MODAF 的服务视点（SvcV）定义了比 DoDAF 更精细的服务模型集，包括：

- **SvcV-1**: 服务组合关系（Service Portfolio）
- **SvcV-2**: 服务资源流（Service Resource Flow）
- **SvcV-3**: 服务交互矩阵（Service Interactions）
- **SvcV-4**: 服务功能描述（Service Functions）
- **SvcV-5**: 服务效能分析（Operational Activity to Service Traceability）
- **SvcV-6**: 服务事件追踪（Service Event-Trace）
- **SvcV-7**: 服务度量（Service Measures）
- **SvcV-8**: 服务演进描述（Service Evolution）
- **SvcV-9**: 服务技术与技能预测（Service Technology & Skills Forecast）
- **SvcV-10a/b/c**: 服务规则/状态/场景模型

这种细粒度的服务建模为联盟环境下的服务复用提供了精确的技术基础——每个服务契约都可以被明确定义、版本化、验证与跨系统调用。

---

## 2. NAF 4.0 概述

北约架构框架（NATO Architecture Framework, NAF）4.0 版是北约标准化办公室（NATO Standardization Office, NSO）发布的联盟级架构开发标准。NAF 4.0 于 2018 年正式发布，是目前北约及其成员国、伙伴国进行国防与企业架构开发的核心框架。NAF 4.0 采用四层结构，从抽象到具体依次为元模型层、方法论层、视点层与视图层。

### 2.1 元模型层（NMM）

NAF 4.0 元模型（NATO Meta-Model, NMM）是整个框架的语义基础，定义了架构描述中所有概念的形式化定义、属性与关系。NMM 的设计吸收了 MODAF 的 IDEAS 本体与 UAF 的元模型精华，同时针对北约联盟环境进行了特定扩展。

NMM 的核心特征包括：

- **本体一致性**: NMM 采用形式化本体方法定义概念，确保所有成员国架构师对"能力"、"系统"、"服务"等核心术语具有统一的语义理解。这对于跨语言（英语/法语/德语等）的架构复用至关重要。
- **联盟扩展**: NMM 在标准国防架构概念基础上增加了联盟特定概念，如"联盟能力目标（NATO Capability Target）"、"互操作性级别（Level of Interoperability）"、"贡献国（Contributing Nation）"等。
- **与 UAF 的对齐**: NMM 与 OMG UAF 1.3 元模型保持高度一致，确保使用 UAF 工具（如 Cameo Systems Modeler）开发的北约架构模型可直接进行一致性检查与复用分析。

NMM 的主要域（Domain）包括：

| 域名称 | 核心概念 | 复用意义 |
|-------|---------|---------|
| 能力域（Capability） | 能力、能力目标、能力差距、能力配置 | 联盟能力目标映射与差距分析 |
| 作战域（Operational） | 作战活动、节点、作战代理、信息元素 | 跨国军种作战活动标准化 |
| 系统域（System） | 系统、系统端口、系统功能、系统角色 | 联合系统组件复用 |
| 服务域（Service） | 服务、服务接口、服务编排、服务级别协议 | 互操作服务的跨平台复用 |
| 技术域（Technical） | 技术标准、技术产品、技术规划 | 联盟技术基线统一 |
| 项目域（Programme） | 项目、里程碑、采办项目、资源 | 多国联合采办计划协调 |
| 全景域（All） | 架构描述、利益相关者、关注问题、目的 | 联盟架构治理与元数据管理 |

### 2.2 方法论层

NAF 4.0 的方法论层定义了使用框架开发架构的标准过程、角色与交付物。与 DoDAF 2.02 的"仅提供框架、不指定过程"不同，NAF 4.0 明确提供了方法论指导，尽管允许成员国根据本国实践进行裁剪。

NAF 4.0 方法论的核心要素包括：

- **架构开发过程**: 定义从架构愿景到架构交付的六阶段过程——启动（Initiation）、需求（Requirements）、设计（Design）、评估（Assessment）、批准（Approval）、维护（Maintenance）。
- **利益相关者分析**: 明确识别联盟架构中的多元利益相关者，包括北约军事委员会（MC）、北约标准化办公室（NSO）、成员国国家代表、联盟指挥部（如 SHAPE）、采办机构（NSPA）等。
- **架构一致性检查**: 提供跨视点、跨层级、跨组织的架构一致性规则，确保不同成员国提交的架构模型可以在联盟层面进行整合与比较。
- **复用指导**: 方法论层专门包含"架构复用（Architecture Reuse）"章节，指导架构师如何识别、评估与采纳现有架构资产，包括他国架构、历史任务架构与联盟参考架构。

### 2.3 视点层（七个核心视点）

NAF 4.0 定义了七个核心视点（Viewpoint），每个视点对应一组利益相关者的特定关注点：

| 视点缩写 | 全称 | 核心关注点 | 利益相关者 | 与复用体系的对应 |
|---------|------|-----------|-----------|---------------|
| NAV | NATO All Viewpoint | 架构全景、背景、范围、元数据 | 架构治理者、联盟决策层 | 联盟级元数据与治理基线 |
| NCV | NATO Capability Viewpoint | 能力需求、能力目标、能力差距、能力依赖 | 能力规划者、战略参谋 | **业务能力复用（联盟能力目标）** |
| NOV | NATO Operational Viewpoint | 作战活动、作战节点、信息流、指挥关系 | 作战指挥官、军种参谋 | **业务架构复用（作战活动）** |
| NSV | NATO System Viewpoint | 系统组成、系统接口、系统功能分配 | 系统工程师、技术管理者 | **组件/系统复用（联合系统）** |
| NSvcV | NATO Service Viewpoint | 服务描述、服务接口、服务编排、服务治理 | 服务架构师、互操作工程师 | **应用服务复用（互操作服务）** |
| NTV | NATO Technical Viewpoint | 技术标准、技术产品、技术规划、标准符合性 | 技术规划者、标准工程师 | 技术基线复用与标准治理 |
| NPV | NATO Programme Viewpoint | 项目规划、采办里程碑、资源分配、风险管理 | 采办管理者、项目经理 | 项目组合与里程碑复用 |

NAF 4.0 的视点设计体现了对联盟环境的特殊考量：

- **NCV（能力视点）** 强调"联盟能力目标（NATO Capability Target）"，这是北约各成员国通过国防规划过程（NDPP）共同认可的能力需求，是联盟架构复用的最高阶锚点；
- **NOV（作战视点）** 引入了"联盟联合作战活动（NATO Joint Operational Activity）"概念，如"联盟联合防空（NATO Joint Air Defence）"，为跨国军种的标准化作战流程提供复用基础；
- **NSvcV（服务视点）** 被提升为与 NSV（系统视点）并列的独立视点，反映了北约对"服务导向基础设施（SOI）"的战略重视。

### 2.4 视图层

视图层是 NAF 4.0 的具体实现层，包含每个视点下的具体视图（View）与模型（Model）。NAF 4.0 共定义了约 50 个具体视图，每个视图对应一个特定的架构问题与交付物格式。

视图层的设计遵循 ISO/IEC/IEEE 42010:2022 的架构描述标准，每个视图由以下要素构成：

- **关注问题（Concern）**: 该视图需要回答的具体架构问题；
- **利益相关者（Stakeholder）**: 该视图的主要受众；
- **模型（Model）**: 该视图采用的具体建模方法与图类型；
- **约定（Convention）**: 该视图的符号约定与建模规则。

NAF 4.0 的视图命名遵循严格规则：每个视图由视点缩写 + 数字标识组成，如 NOV-1（作战背景）、NCV-2（能力层次）、NSvcV-4（服务功能）等。这种命名体系确保了跨组织、跨工具、跨语言的架构资产可快速识别与检索，是架构复用的基础前提。

---

## 3. NAF 4.0 与 DoDAF 2.02 / UAF 1.3 的对比矩阵

### 3.1 元模型差异：NMM vs DM2 vs UAF Metamodel

| 对比维度 | NAF 4.0 NMM | DoDAF 2.02 DM2 | UAF 1.3 Metamodel |
|---------|------------|----------------|-------------------|
| **设计目标** | 支持 30+ 成员国/伙伴国的联盟架构互操作 | 支持美国国防部体系架构的端到端治理 | 提供跨框架、跨领域的统一建模语言 |
| **本体基础** | 基于 IDEAS + 北约联盟扩展本体 | 基于 DoDAF 2.0 核心本体 + 三套模型（概念/逻辑/物理） | 基于 UML/SysML 形式化语义 |
| **联盟概念** | 原生支持联盟能力目标、贡献国、互操作级别 | 通过联盟扩展（如 FMN）间接支持 | 通过 Profile 机制支持扩展 |
| **服务建模** | 独立服务域，原生服务契约概念 | 服务作为系统功能的一种封装形式 | 独立服务域，面向服务架构（SOA）语义 |
| **数据交换格式** | NAF XML / UAF XML / XMI | DoDAF 2.0 XML / CADM / PES | UAF XML / XMI / JSON |
| **工具兼容性** | 原生支持 Cameo / Enterprise Architect 等 UAF 工具 | 支持 DoDAF-specific 工具（如 System Architect） | 支持所有 UML/SysML 兼容工具 |
| **多语言支持** | 原生设计支持 NATO 官方语言（英/法） | 以英语为主 | 依赖工具实现本地化 |
| **版本管理** | 支持联盟级架构版本（如 FMN Spiral 4+） | 支持国防部体系版本（如 DoD IEA） | 支持模型级版本控制 |

**关键差异解析**:

NMM 与 DM2 的最大差异在于"联盟性"设计。DM2 假设所有架构元素在一个统一治理域（美国国防部）内管理，因此其本体侧重层级控制与命令链追溯。而 NMM 假设架构元素分布在多个主权国家，需要通过协商一致（Consensus）而非命令（Command）达成架构对齐。这一根本差异体现在 NMM 的"互操作性级别"概念上——NMM 不要求所有系统完全同质，而是允许不同系统在不同级别上实现互操作，从而在保持国家主权的同时实现联盟协同。

UAF 1.3 的元模型则是更抽象的一层，旨在统一 NAF、DoDAF、MODAF 及民用架构框架的语义。UAF 不直接替代 NMM 或 DM2，而是提供一种"通用语言"，使 NMM 模型与 DM2 模型可以在同一工具环境中进行映射与转换。对于架构复用而言，UAF 的价值在于：当需要从 NAF 格式的联盟架构资产中提取复用元素，并映射到 DoDAF 格式的本国架构时，UAF 提供了标准化的转换桥梁。

### 3.2 视点差异

| 对比维度 | NAF 4.0（七个视点） | DoDAF 2.02（八个视点） | UAF 1.3（领域结构） |
|---------|-------------------|----------------------|-------------------|
| **全景/全视点** | NAV | AV | Strategic, Summary |
| **能力视点** | NCV（独立） | CV（独立） | Capabilities Domain |
| **作战视点** | NOV（独立） | OV（独立） | Operational Domain |
| **系统视点** | NSV（独立） | SV（独立） | Resources, Systems |
| **服务视点** | NSvcV（独立，与系统并列） | SvcV（独立，但与系统界限模糊） | Services Domain |
| **数据视点** | 融入各视点（Data Model in NSV/NSvcV） | DIV（独立数据与信息视点） | Information Domain |
| **标准视点** | NTV（独立，含技术规划） | StdV（独立，侧重现行标准） | Standards Domain |
| **项目视点** | NPV（独立，含采办协调） | PV（独立，侧重项目跟踪） | Projects Domain |
| **战略视点** | 融入 NAV/NCV | 无独立战略视点 | Strategic Domain |

NAF 4.0 与 DoDAF 2.02 在视点设计上的核心差异：

1. **数据视点的处理**: DoDAF 2.02 将数据与信息（DIV）提升为独立视点，反映了美国防部对信息主导权（Information Superiority）的战略重视。NAF 4.0 则将数据模型融入系统与服务视点，这一设计源于北约的数据治理实践——在联盟环境中，数据标准往往通过技术标准（NTV）而非独立数据视点来推行，因为数据互操作本质上是一个技术协议问题。

2. **服务视点的地位**: NAF 4.0 明确将服务视点（NSvcV）与系统视点（NSV）置于同等地位，反映了北约对"能力即服务（Capability as a Service）"理念的采纳。DoDAF 2.02 的服务视点虽然独立，但在实际应用中常与系统视点混合使用，因为美国防部的采办体系仍以系统为中心。

3. **技术视点的深度**: NAF 4.0 的技术视点（NTV）不仅包含现行标准清单（对应 DoDAF StdV-1），还包含技术产品目录（Technology Product Catalogue）与技术规划映射（Technology Forecast），支持更长周期的技术演进规划。这对于联盟环境尤为重要——成员国需要在数年时间尺度上协调技术路线图，避免某国过早淘汰他国仍在使用的技术标准。

### 3.3 互操作性支持差异

| 维度 | NAF 4.0 | DoDAF 2.02 | UAF 1.3 |
|-----|---------|-----------|---------|
| **互操作定义** | 基于 NATO C3 分类法的六类互操作（技术/程序/语义/业务/政策/组织） | 基于 Net-Centric 数据策略的互操作 | 基于 ISO/IEC 19941 的云互操作扩展 |
| **互操作评估方法** | 联盟互操作验证（IV）与认证（IC）流程 | 联合互操作性测试命令（JITC）评估 | 依赖具体实现工具的验证功能 |
| **联盟特定机制** | 支持多国安全分级映射、贡献国配置管理 | 以美国为中心的互操作认证 | 框架中立，需通过 Profile 扩展 |
| **信息交换模型** | 基于 JC3IEDM / ADatP-3 的联盟数据模型 | 基于 USD(I) 数据策略的国防部数据模型 | 支持任意信息模型映射 |
| **服务互操作** | NSPA SOI 参考架构、NATO SOA 框架 | DoD SOA 参考模型、DISA 企业服务 | OMG SOA 建模规范 |

NAF 4.0 在互操作性支持上的独特优势在于其"联盟互操作验证（Interoperability Verification, IV）"机制。IV 不是一次性的测试活动，而是一个贯穿架构全生命周期的持续验证过程：

- **架构阶段**: 通过 NAF 模型进行静态互操作性检查，识别接口不匹配、数据语义冲突与标准不一致；
- **开发阶段**: 通过联盟测试床（如 NATO Interoperability Test Bed）进行系统间联调；
- **部署阶段**: 通过任务网络设计机构（MNDA）进行任务级互操作认证；
- **运行阶段**: 通过持续监控与反馈，更新架构模型以反映实际互操作水平。

这种全生命周期互操作验证机制，使 NAF 架构复用不仅是静态模型的复用，更是动态互操作能力的复用。

---

## 4. 北约架构复用的特殊挑战

### 4.1 多国安全分级体系

北约的安全分级体系与单一国家（如美国或英国）的分级体系存在结构性差异，这是北约架构复用的首要挑战。

**北约分级层级**:

| 分级 | 英文标识 | 复用影响 |
|-----|---------|---------|
| NATO UNCLASSIFIED | NU | 可在联盟内完全共享，公开可用 |
| NATO RESTRICTED | NR | 限于北约官方人员及授权承包商 |
| NATO CONFIDENTIAL | NC | 限于需要知情的联盟人员 |
| NATO SECRET | NS | 高敏感性，严格访问控制 |
| COSMIC TOP SECRET | CTS | 最高级别，仅限特定授权人员 |

**复用挑战**:

1. **分级映射不对称**: 各成员国的国家安全分级与北约分级不存在一一对应关系。例如，美国的"SECRET"与北约的"NATO SECRET"在访问控制规则上存在差异，某国"SECRET"级别的架构资产可能在北约框架下被归类为"NATO CONFIDENTIAL"或"NATO SECRET"，取决于信息内容与分发限制。

2. **释放（Releaseability）限制**: 即使安全分级对应，架构资产还受到释放标记限制，如"REL TO NATO"（可向北约释放）、"REL TO FIVE EYES"（仅向五眼联盟释放）等。一个被标记为"NOFORN"（不向外籍人员释放）的美国 DoDAF 架构模型，即使安全分级较低，也无法直接被北约联盟架构复用。

3. **多国安全审查（Multi-National Security Accreditation）**: 当某成员国的系统需要接入联盟任务网络时，其架构描述必须经过所有参与国的安全审查。这一过程可能持续数月甚至数年，严重制约架构资产的快速复用。

**应对策略**:

- **分层复用**: 将架构资产按安全等级分层管理，高等级资产仅在需要知情的范围内复用，低等级资产（如 NU 级别的作战活动模型、服务接口规范）作为联盟公共资产广泛复用；
- **匿名化与抽象化**: 对高等级架构资产进行匿名化处理，提取与安全性无关的架构模式（如指挥关系模式、信息流模式）供联盟复用；
- **信任框架**: 建立基于北约共同安全标准（如 NATO INFOSEC Standard）的互认机制，减少重复安全审查。

### 4.2 28+ 成员国的架构协调

北约目前拥有 32 个成员国（截至 2024 年），加上伙伴国与全球伙伴，架构协调的复杂度远超单一国防体系。

**协调挑战**:

1. **语言与文化差异**: 北约官方语言为英语和法语，但架构开发涉及大量专业术语，翻译一致性难以保证。例如，"Capability"在英语语境中强调"能力/效力"，在法语中译为"Capacité"，但在某些成员国的军事语境中更接近"Potential"（潜力）而非"Operational Ability"（作战能力）。语义差异可能导致架构复用时的误解。

2. **指挥关系差异**: 北约采用"联盟指挥与部队结构（NATO Command and Force Structure）"，但各成员国的本国指挥体系千差万别。美国的联合参谋部（Joint Staff）、法国的联合参谋部（État-Major des Armées）、德国的联邦国防军指挥与参谋学院（Führungsakademie）在决策流程、权限分配与信息流动模式上存在显著差异。将联盟作战活动模型（NOV-5）映射到各国系统时，必须考虑这些组织差异。

3. **采办周期差异**: 各成员国的国防采办周期长短不一。美国的 DoD 5000 系列采办流程、英国的 CADMID/T 周期、德国的 BAAINBw 采办流程在时间尺度、决策节点与审批层级上各不相同。联盟架构复用要求在一个时间窗口内协调多国系统的升级与替换，这在实践上极为困难。

**应对策略**:

- **参考架构（Reference Architecture）**: 北约标准化办公室（NSO）维护联盟参考架构（如 NNEC RA、FMN AD），作为所有成员国的架构对齐基线。各国架构只需证明与参考架构的兼容性，无需完全一致；
- **螺旋式协调（Spiral Coordination）**: 采用 FMN 的螺旋式开发方法，每一螺旋（Spiral）只要求部分成员国参与，逐步扩展参与范围与协调深度；
- **架构联盟（Architecture Federation）**: 不要求建立单一的联盟架构仓库，而是允许各国维护本国架构，通过标准化接口（如 UAF XML/XMI）实现架构模型的联邦式查询与复用。

### 4.3 联盟采办框架（NSPA）中的架构复用

北约支援与采办局（NATO Support and Procurement Agency, NSPA）是北约的主要采办执行机构，负责联盟共同资助的装备与服务的采办。NSPA 采办框架中的架构复用面临以下特殊挑战：

**多国出资与知识产权**:
联盟采办项目通常由多个成员国共同出资，但各国对采办成果的知识产权归属有不同理解。某国出资开发的系统架构是否自动成为联盟公共资产？其他成员国在复用该架构时是否需要支付许可费？这些问题在北约法律框架（如 Ottawa Agreement）中没有完全明确的答案。

**标准化与竞争的张力**:
NSPA 的采办政策要求在标准化（以实现互操作）与竞争（以降低成本）之间取得平衡。过度标准化的采办规格可能导致只有少数供应商能满足要求，削弱竞争；而过度开放的采办规格可能导致系统间互操作性不足。架构复用需要在标准化架构模型与竞争性采办需求之间找到最优解。

**联盟-国家双轨制**:
北约采办存在"联盟共同采办"与"国家独立采办"的双轨制。联盟共同采办（如 AGS 全球鹰无人机项目）的架构资产自然属于联盟，但国家独立采办（如各成员国的战斗机更新计划）的架构资产仅在自愿基础上向联盟贡献。如何激励成员国将国家采办架构贡献给联盟复用库，是 NSPA 面临的治理难题。

---

## 5. NAF 复用视角映射

### 5.1 NAF Operational View → 业务架构复用（作战活动）

NAF 作战视点（NOV）描述联盟作战活动、作战节点、信息交换与指挥关系，是北约联盟进行业务架构复用的核心视点。

**映射逻辑**:

| NAF 视图 | 复用元素 | 本知识体系对应层 |
|---------|---------|---------------|
| NOV-1 | 作战背景、战略上下文 | 业务架构 — 战略上下文复用 |
| NOV-2 | 作战节点与组织关系 | 业务架构 — 组织结构复用 |
| NOV-3 | 作战节点间的信息交换 | 业务架构 — 信息流复用 |
| NOV-4 | 作战活动分解 | 业务架构 — 业务流程复用 |
| NOV-5 | 作战活动模型（含输入/输出/控制/机制） | 业务架构 — 作战活动标准化 |
| NOV-6 | 作战事件追踪（时间序列） | 业务架构 — 场景与用例复用 |

**复用实践要点**:

1. **联盟联合作战活动库（NATO Joint Operational Activity Library）**: 北约标准化办公室维护标准化的作战活动层次结构，如"NCO-01 指挥与控制"、"NCO-02 情报收集"、"NCO-03 火力协调"等。任何成员国的作战系统架构在定义本国作战活动时，应优先引用联盟标准活动，而非重新定义。这确保了不同国家的系统在描述"同一任务"时使用相同的语义框架。

2. **指挥关系模式复用**: NOV-2 中的指挥关系模型（如"作战指挥（OPCON）"、"战术控制（TACON）"）是北约联盟的核心组织模式。这些模式在不同任务中反复出现，可被抽象为可复用的组织模板。例如，北约联合特遣部队（CJTF）的指挥结构是一个经过多任务验证的复用模式，新任务只需替换具体国家与人员，无需重新设计指挥链。

3. **信息交换矩阵（NOV-3）复用**: 联盟作战节点间的信息交换需求具有高度稳定性。例如，"预警机向战斗机发送目标指示"这一信息交换模式在北约联合防空任务中始终存在。NOV-3 的信息交换矩阵可被复用为联盟数据需求规格（Information Exchange Requirement, IER），进而驱动系统视点的接口设计。

### 5.2 NAF Capability View → 业务能力复用（联盟能力目标）

NAF 能力视点（NCV）是 NAF 4.0 最具联盟特色的视点，直接映射北约国防规划过程（NDPP）与联盟能力目标。

**映射逻辑**:

| NAF 视图 | 复用元素 | 本知识体系对应层 |
|---------|---------|---------------|
| NCV-1 | 能力层次结构 | 业务架构 — 能力战略复用 |
| NCV-2 | 能力分类与映射 | 业务架构 — 能力目录复用 |
| NCV-3 | 能力依赖与交互 | 业务架构 — 能力组合复用 |
| NCV-4 | 能力目标与差距 | 业务架构 — 差距分析复用 |
| NCV-5 | 能力配置 | 业务架构 — 能力实例化复用 |

**复用实践要点**:

1. **联盟能力目标（NATO Capability Target）复用**: 北约通过 NDPP 过程定义了约 200 个联盟能力目标，涵盖所有作战域（陆、海、空、天、网、认知）。这些能力目标是联盟架构开发的最高阶需求，具有极强的复用价值。例如，"联盟联合精确打击能力（NATO Joint Precision Strike）"这一目标被多个北约任务（如利比亚行动、波罗的海空中 policing）复用，每次复用时只需根据任务特定条件调整性能参数（如射程、精度、响应时间）。

2. **能力差距分析（NCV-4）复用**: 联盟能力差距分析不仅识别"缺少什么能力"，还识别"哪个成员国可以填补这一差距"。这种"能力差距-贡献国映射"是一种高度结构化的复用资产，支持联盟快速组建特遣部队。例如，当某任务需要"远程战略空运能力"时，NCV-4 可以直接指向拥有该能力的成员国（如美国、德国、法国），无需重新评估各国装备清单。

3. **能力配置模板（NCV-5）复用**: 能力配置是将抽象能力目标实例化为具体人员、系统与流程组合的模式。北约维护了一系列经过验证的能力配置模板，如"一个北约联合特遣部队（CJTF）的能力配置"包含约 50 个能力配置实例，涵盖指挥、情报、火力、后勤、通信等各领域。新任务在规划时可以直接复用这些模板，根据任务规模进行缩放。

### 5.3 NAF Service View → 应用服务复用（互操作服务）

NAF 服务视点（NSvcV）是北约推动服务导向基础设施（SOI）的核心技术基础，也是应用架构复用的关键视点。

**映射逻辑**:

| NAF 视图 | 复用元素 | 本知识体系对应层 |
|---------|---------|---------------|
| NSvcV-1 | 服务组合（Service Portfolio） | 应用架构 — 服务目录复用 |
| NSvcV-2 | 服务资源流 | 应用架构 — 服务接口契约复用 |
| NSvcV-3 | 服务交互矩阵 | 应用架构 — 服务编排复用 |
| NSvcV-4 | 服务功能描述 | 应用架构 — 服务功能规格复用 |
| NSvcV-5 | 作战活动到服务的可追溯性 | 应用架构 — 业务-服务映射复用 |
| NSvcV-6 | 服务事件追踪 | 应用架构 — 服务场景复用 |
| NSvcV-7 | 服务度量 | 应用架构 — 服务级别协议（SLA）复用 |

**复用实践要点**:

1. **核心服务规范（Core Service Specifications）复用**: 北约定义了一系列联盟核心服务规范，如 BMSCS（Battle Management Services Core Services）、C3 Taxonomy Core Services、FMN Spiral 服务规范等。这些服务规范定义了跨系统互操作的契约，任何成员国的系统只要实现这些规范即可接入联盟网络。核心服务规范是联盟层面最重要的应用服务复用资产。

2. **服务接口描述语言（NIDL）复用**: NAF 4.0 推荐使用 NATO Interface Description Language（NIDL）描述服务接口，这是一种基于 W3C WSDL / OASIS ODDIL 的联盟标准化接口描述格式。使用 NIDL 描述的服务接口可以被所有成员国理解与实现，消除了因接口描述语言差异导致的互操作障碍。

3. **服务编排模式复用**: 联盟作战活动往往需要多个服务的协同工作（服务编排）。NSvcV-3 的服务交互矩阵定义了服务间的调用关系、数据依赖与时序约束。这些编排模式（如"联合火力请求处理流程"的服务编排）经过验证后可以被不同任务复用，新任务只需替换具体服务实例（如将某国的"火力协调服务"替换为另一国的等效服务），而保持编排逻辑不变。

### 5.4 NAF System View → 组件/系统复用（联合系统）

NAF 系统视点（NSV）描述系统的组成、接口、功能分配与资源，对应组件架构复用层。

**映射逻辑**:

| NAF 视图 | 复用元素 | 本知识体系对应层 |
|---------|---------|---------------|
| NSV-1 | 系统组合结构 | 组件架构 — 系统组件目录复用 |
| NSV-2 | 系统资源流（系统间接口） | 组件架构 — 接口规格复用 |
| NSV-3 | 系统交互矩阵 | 组件架构 — 系统集成模式复用 |
| NSV-4 | 系统功能描述 | 组件架构 — 功能分配复用 |
| NSV-5 | 作战活动到系统功能的可追溯性 | 组件架构 — 业务-系统映射复用 |
| NSV-6 | 系统事件追踪 | 组件架构 — 系统场景复用 |
| NSV-7 | 系统度量 | 组件架构 — 性能基线复用 |
| NSV-8 | 系统演进 | 组件架构 — 系统生命周期复用 |

**复用实践要点**:

1. **联合系统配置（Joint System Configuration）复用**: 在北约任务中，"系统"往往不是单一国家的装备，而是多国系统的联合配置。例如，北约联合防空系统可能包含美国的雷达、法国的指挥控制系统、德国的导弹系统。NSV-1 的系统组合结构定义了这种联合配置的系统边界与内部组成，是可复用的系统架构资产。

2. **系统接口规范（NSV-2）复用**: 北约标准化协议（STANAG）定义了大量系统间接口规范，如 STANAG 5602（数据链路接口）、STANAG 7085（战术数据交换）。NSV-2 将这些标准化接口映射到具体系统的端口与协议，形成可直接实施的接口规格。这些接口规格在多个任务中复用，确保不同国家的系统可以通过标准化接口互联。

3. **系统功能分配模式（NSV-5）复用**: 联盟作战活动向系统功能的分配遵循特定模式。例如，"态势感知"这一作战活动通常被分配为：传感器系统（探测功能）→ 数据处理系统（关联功能）→ 显示系统（呈现功能）。这种功能分配模式在北约多个任务中反复出现，可被抽象为可复用的架构模式。

---

## 6. 与 DoDAF B-01 文档的互补关系

本文档（C-07: NAF/MODAF 复用视角）与 B-01 文档（DoDAF/UAF 复用视角）共同构成国防与使命工程领域的完整架构复用映射体系，二者之间存在明确的互补关系。

**聚焦范围差异**:

| 维度 | B-01 文档（DoDAF/UAF） | C-07 文档（NAF/MODAF） |
|-----|----------------------|----------------------|
| **主要适用对象** | 美国国防部体系、美国国防承包商、美国主导的多国任务 | 北约联盟、英国国防部、北约成员国、NSPA 采办项目 |
| **治理假设** | 单一主权国家内的层级治理 | 多国联盟内的协商治理 |
| **采办体系** | DoD 5000 系列采办指令 | NSPA 联盟采办框架 + 各国独立采办 |
| **互操作焦点** | 美军联合互操作（Joint Interoperability） | 联盟多国互操作（Allied Interoperability） |
| **安全框架** | 美国保密分级体系 | 北约保密分级体系 + 多国释放限制 |
| **核心案例** | NATO FMN（美军视角） | NATO JISR（联盟视角） |

**协同使用方式**:

1. **联盟-国家架构映射**: 当美国作为北约成员国参与联盟任务时，其本国架构使用 DoDAF 2.02 开发，而联盟架构使用 NAF 4.0 开发。B-01 与 C-07 共同提供了这两个框架之间的映射指南，支持美国系统的联盟集成。

2. **UAF 作为转换桥梁**: UAF 1.3 是两个文档共同依赖的转换层。B-01 描述了 DoDAF 到 UAF 的映射，C-07 描述了 NAF 到 UAF 的映射，二者结合即构成 DoDAF ↔ UAF ↔ NAF 的完整转换路径。

3. **能力目标对齐**: 美国防部的联合能力领域（Joint Capability Areas, JCA）与北约的联盟能力目标（NATO Capability Targets）需要在联盟任务中对齐。B-01 的 DoDAF CV 映射与 C-07 的 NAF NCV 映射共同支持这种跨体系的能力对齐。

4. **服务互操作补充**: B-01 侧重于美军内部的 SOA 实践（如 DISA 企业服务），C-07 侧重于北约联盟的服务基础设施（如 NSPA SOI）。当美军系统需要接入联盟网络时，需要同时参考两个文档的服务映射指南。

**使用建议**:

- 若项目完全在美国防部治理域内，优先使用 B-01；
- 若项目涉及北约联盟或多国协调，优先使用 C-07；
- 若项目涉及美军系统与北约系统的集成，两个文档应结合使用，以 UAF 1.3 作为转换桥梁。

---

## 7. 案例：NATO JISR 架构复用

### 7.1 JISR 背景与架构需求

NATO Joint Intelligence, Surveillance and Reconnaissance（JISR）是北约推动的联合情报、监视与侦察能力倡议，旨在通过标准化的架构框架、数据模型与服务接口，实现北约及成员国 ISR 资产（如预警机、无人机、卫星、地面传感器）的协同运用与信息共享。

JISR 的架构需求极为复杂：

- **多域资产集成**: 涉及空基（AWACS、Global Hawk）、天基（SAR-Lupe、Helios）、陆基（JSTARS、地面雷达）、海基（舰载 ISR 平台）及网基（开源情报、信号情报）等多域 ISR 资产；
- **多国指挥链**: ISR 任务的规划、执行与评估涉及北约盟军司令部作战指挥部（ACO）、北约盟军司令部转型指挥部（ACT）、各成员国国家指挥当局（NCA）及联合特遣部队（CJTF）的多层级指挥链；
- **实时信息共享**: ISR 信息（如目标图像、电子情报、移动目标指示）需要在数秒至数分钟时间尺度上从传感器传递至射手，对架构的实时互操作性要求极高；
- **严格安全分级**: ISR 信息往往涉及最高级别的保密分级（如 COSMIC TOP SECRET），同时需要在联盟内部分发，安全与共享的平衡是核心架构挑战。

### 7.2 JISR 中的 NAF 4.0 复用实践

JISR 是 NAF 4.0 在联盟环境下进行架构复用的典型实践，其复用实践涵盖 NAF 全部七个视点：

**NAV（全景视点）复用**:
JISR 采用 NATO Standardization Office 维护的 JISR 联盟架构描述（JISR Alliance Architecture Description）作为全景基线。该描述定义了 JISR 的架构范围、利益相关者、关键术语与治理流程，被所有 JISR 参与国复用为各自国家 JISR 架构的全景章节。

**NCV（能力视点）复用**:
JISR 的核心能力需求源自北约联盟能力目标"联合 ISR 能力（Joint ISR Capability）"。该能力目标在 NCV-1/2/3 中被分解为：

- 战略层：联盟持续态势感知能力
- 作战层：跨域 ISR 任务规划与执行能力
- 功能层：传感器任务分配、情报融合、目标分发能力

这些能力层次结构被所有 JISR 参与国复用，各国只需在 NCV-4/5 中标注本国已具备的能力配置与尚存的能力差距。

**NOV（作战视点）复用**:
JISR 定义了标准化的联盟 ISR 作战活动模型（JISR NOV-4/5），包括：

- **ISR 任务规划**: 从指挥官信息需求（PIR）到传感器任务分配的完整流程；
- **ISR 数据收集**: 传感器任务执行、原始数据采集与预处理；
- **ISR 数据处理**: 多源情报关联、融合与分析；
- **ISR 产品分发**: 情报产品打包、分级与按需分发；
- **ISR 效果评估**: 任务完成度评估与反馈闭环。

这些作战活动模型在北约多个 ISR 任务（如阿富汗任务、波罗的海空中 policing、地中海海上监视）中被反复复用，新任务只需根据特定作战环境调整活动参数（如传感器类型、覆盖区域、响应时间）。

**NSV（系统视点）复用**:
JISR 定义了标准化的 ISR 系统参考架构，包括：

- **传感器层**: 各类 ISR 传感器的标准化接口（如 STANAG 7085 用于数据交换）；
- **通信层**: 标准化的宽带与窄带通信链路（如 NATO SATCOM、Link-16/22）；
- **处理层**: 标准化的情报处理系统（如 NATO ISR 融合平台、成员国国家融合中心）；
- **应用层**: 标准化的 ISR 应用（如 NATO ISR 工具套件、JTSG - Joint Targeting Support Gateway）。

各成员国在接入 JISR 时，复用这些系统参考架构，将本国 ISR 系统映射到标准化的系统角色（System Role）与接口规范。

**NSvcV（服务视点）复用**:
JISR 的服务架构是北约 SOI 框架的重要实践场域，定义了以下核心服务的标准化接口：

- **传感器任务服务（Sensor Tasking Service）**: 标准化传感器任务请求与响应接口；
- **情报发布服务（Intelligence Publishing Service）**: 标准化情报产品的发布、订阅与推送接口；
- **目标数据服务（Target Data Service）**: 标准化目标信息的查询、更新与分发接口；
- **轨道相关服务（Track Correlation Service）**: 标准化多源轨道数据的关联与融合接口。

这些服务规范以 NIDL 描述，被所有 JISR 参与国的 ISR 系统实现复用，确保不同国家的系统可以通过标准化服务接口进行互操作。

**NTV（技术视点）复用**:
JISR 定义了强制的技术标准清单（NTV-1/2），包括数据格式标准（如 NITF、GeoTIFF）、通信协议标准（如 IP over SATCOM、MIDS/JTRS）、安全标准（如 NATO INFOSEC Standard）等。这些技术标准是联盟 ISR 互操作的技术基线，被所有参与国复用为系统开发的技术约束。

**NPV（项目视点）复用**:
JISR 的采办与部署通过 NSPA 及各国并行采办项目实现。NPV 定义了标准化的项目里程碑（如架构批准、接口验证、联调测试、运行认证），这些里程碑被各国 JISR 项目复用，确保各国系统的交付节奏与联盟集成计划对齐。

### 7.3 JISR 复用的互操作性等级与经验

JISR 的架构复用实践在互操作性等级（LOI）上取得了显著进展：

| LOI 等级 | JISR 实现状态 | 复用深度 |
|---------|-------------|---------|
| LOI 1（孤立级） | 已超越 | — |
| LOI 2（连通级） | 已实现 | 复用系统视点的物理接口规范（如 Link-16 数据链） |
| LOI 3（功能级） | 基本实现 | 复用服务视点的服务接口契约与数据语义模型（如 JC3IEDM / ADatP-3） |
| LOI 4（领域级） | 部分实现 | 复用作战视点的完整活动模型与决策规则 |
| LOI 5（集成级） | 目标愿景 | 复用能力视点的完整能力配置与演进规划 |

**经验教训**:

1. **数据模型是 ISR 复用的核心**: JISR 最成功的复用实践不是系统或服务，而是数据模型——JC3IEDM（Joint C3 Information Exchange Data Model）和 ADatP-3（Allied Data Publication No. 3）为所有参与国的 ISR 系统提供了统一的语义基础。没有统一的数据模型，再多的接口规范也无法实现真正的信息共享。

2. **渐进式服务化**: JISR 并非一开始就采用全面的 SOA 架构，而是从 LOI 2 的物理互联起步，逐步向 LOI 3/4 的服务化演进。这种渐进式策略降低了成员国系统的改造难度，使架构复用可以在实践中逐步深化。

3. **安全分级与信息分发的架构隔离**: JISR 在架构设计中明确区分了"多域 ISR 骨干网（Multi-Domain ISR Backbone）"与"国家 ISR 网络（National ISR Networks）"，通过标准化的安全网关（Security Gateway）实现跨域信息分发。这种架构隔离使高等级 ISR 信息可以在受控条件下向联盟复用，而无需暴露国家网络的全部细节。

4. **治理重于标准**: JISR 的经验表明，联盟 ISR 互操作的最大瓶颈不是缺乏技术标准，而是缺乏统一的治理机制——谁有权分配传感器任务？谁对情报产品的质量负责？这些治理问题必须在架构层面（特别是 NOV-2 的指挥关系模型与 NCV-3 的能力依赖模型）预先解决，技术标准才能有效落地。

---

## 8. 权威来源

1. **NATO Architecture Framework v4, NATO Standardization Office**
   URL: <https://nsa.nato.int/naf>
   核查日期: 2026-06-10

2. **MODAF 1.2.004, UK Ministry of Defence**
   URL: <https://www.gov.uk/guidance/mod-architecture-framework>
   核查日期: 2026-06-10

3. **DoDAF 2.02 官方规范, U.S. DoD CIO**
   URL: <https://dodcio.defense.gov/library/dod-architecture-framework/>
   核查日期: 2026-06-10

4. **OMG Unified Architecture Framework (UAF) 1.3**
   URL: <https://www.omg.org/spec/UAF/>
   核查日期: 2026-06-10

5. **NATO Joint Intelligence, Surveillance and Reconnaissance (JISR) Initiative**
   URL: <https://www.act.nato.int/jisr>
   核查日期: 2026-06-10

6. **NATO Standardization Office (NSO) — Standards & Standardization Agreements (STANAG)**
   URL: <https://nsa.nato.int/standards>
   核查日期: 2026-06-10

7. **NATO Support and Procurement Agency (NSPA) — Service Oriented Infrastructure (SOI)**
   URL: <https://www.nspa.nato.int/>
   核查日期: 2026-06-10

8. **NATO Federated Mission Networking (FMN) Implementation Plan**
   URL: <https://www.act.nato.int/fmn>
   核查日期: 2026-06-10

9. **JC3IEDM / ADatP-3 Allied Data Publication**
   URL: <https://nso.nato.int/adatp-3>
   核查日期: 2026-06-10

10. **IDEAS Foundation Ontology for Defence Architecture**
    URL: <https://www.ideasgroup.org/>
    核查日期: 2026-06-10

11. **ISO/IEC/IEEE 42010:2022, Systems and software engineering — Architecture description**
    URL: <https://www.iso.org/standard/74296.html>
    核查日期: 2026-06-10

12. **NATO Defence Planning Process (NDPP) Capability Targets**
    URL: <https://www.nato.int/cps/en/natohq/topics_49202.htm>
    核查日期: 2026-06-10

13. **UK Defence Architecture Framework (MOD) — CADMID/T Acquisition Cycle**
    URL: <https://www.gov.uk/guidance/mod-architecture-framework>
    核查日期: 2026-06-10

14. **NATO Information Security (INFOSEC) Standard**
    URL: <https://nsa.nato.int/infosec>
    核查日期: 2026-06-10

---

> 本文档作为软件架构复用知识体系在北约/英国国防领域的专用补充视角，与 B-01 文档（DoDAF/UAF 复用视角）共同构成完整的国防架构复用映射体系。在实际应用中，应根据项目的治理范围（单一国家 vs. 多国联盟）、安全分级要求与互操作性目标，选择适当的框架组合与映射策略。对于涉及北约联盟环境的项目，应优先遵循 NAF 4.0 的视点定义与方法论指导，同时利用 UAF 1.3 实现与 DoDAF 2.02 资产的双向转换与复用。


---

## 补充说明：NAF 4.0 / MODAF 与北约架构复用视角映射

## 概念定义

**定义**：国防任务工程中的复用指在 DoDAF/NAF/Modaf/UAF 等框架下，对使命线程、能力、系统与服务进行跨项目复用，以提升互操作性与采购效率。

## 反例

**反例**：各国国防系统使用互不兼容的架构框架与数据模型，联合作战时需要昂贵的点对点集成。

---


<!-- SOURCE: struct/02-business-architecture-reuse/08-zachman-reuse-mapping/zachman-reusability-matrix.md -->

# Zachman Framework 与软件架构复用映射文档

**版本**: 2026-06-10
**定位**: 四层复用模型（业务→应用→组件→功能）的顶层本体论映射与治理框架
**对齐标准**: Zachman Framework (1987, 2020 扩展版) / GERAM (ISO 15704:2019 企业参考架构方法论) / ISO/IEC/IEEE 42010:2022
**状态**: ✅ 已完成
**维护团队**: 架构复用标准委员会

---

## 目录

- [Zachman Framework 与软件架构复用映射文档](#zachman-framework-与软件架构复用映射文档)
  - [目录](#目录)
  - [1. Zachman Framework 核心概念](#1-zachman-framework-核心概念)
    - [1.1 框架起源与本体论定位](#11-框架起源与本体论定位)
    - [1.2 六疑问词（列维度）： interrogative abstractions](#12-六疑问词列维度-interrogative-abstractions)
    - [1.3 六视角（行维度）： stakeholder perspectives](#13-六视角行维度-stakeholder-perspectives)
    - [1.4 36 Cell 矩阵详解](#14-36-cell-矩阵详解)
      - [第1行：Scope / Planner（规划者视角）](#第1行scope--planner规划者视角)
      - [第2行：Business Model / Owner（业务所有者视角）](#第2行business-model--owner业务所有者视角)
      - [第3行：System Model / Designer（系统设计师视角）](#第3行system-model--designer系统设计师视角)
      - [第4行：Technology Model / Builder（技术构建者视角）](#第4行technology-model--builder技术构建者视角)
      - [第5行：Detailed Representation / Subcontractor（分包商/实施者视角）](#第5行detailed-representation--subcontractor分包商实施者视角)
      - [第6行：Functioning Enterprise / User（用户/运行视角）](#第6行functioning-enterprise--user用户运行视角)
    - [1.5 Zachman 矩阵的关键原则与复用启示](#15-zachman-矩阵的关键原则与复用启示)
    - [1.6 六视角/六抽象层次定义与复用性评估矩阵总览](#16-六视角六抽象层次定义与复用性评估矩阵总览)
    - [六视角与四层复用映射](#六视角与四层复用映射)
    - [六抽象层次的复用含义](#六抽象层次的复用含义)
    - [复用性评估矩阵总览](#复用性评估矩阵总览)
    - [Zachman 复用坐标映射图](#zachman-复用坐标映射图)
  - [2. 复用视角的 Zachman 映射](#2-复用视角的-zachman-映射)
    - [2.1 映射总览](#21-映射总览)
    - [2.2 业务复用 → Why / What（Scope / Business Model 行）](#22-业务复用--why--whatscope--business-model-行)
    - [2.3 应用复用 → How（System Model 行）](#23-应用复用--howsystem-model-行)
    - [2.4 组件复用 → How / Where（Technology Model 行）](#24-组件复用--how--wheretechnology-model-行)
    - [2.5 功能复用 → How（Builder / Subcontractor 行）](#25-功能复用--howbuilder--subcontractor-行)
    - [2.6 四层复用映射的纵向一致性](#26-四层复用映射的纵向一致性)
  - [3. 六维疑问词 × 四层复用 交叉矩阵](#3-六维疑问词--四层复用-交叉矩阵)
    - [3.1 矩阵定义](#31-矩阵定义)
    - [3.2 交叉矩阵全表](#32-交叉矩阵全表)
    - [3.3 交叉矩阵的决策支持应用](#33-交叉矩阵的决策支持应用)
      - [3.3.1 What 列：复用资产发现与目录编制](#331-what-列复用资产发现与目录编制)
      - [3.3.2 How 列：复用资产组合与编排](#332-how-列复用资产组合与编排)
      - [3.3.3 Where 列：复用资产部署拓扑](#333-where-列复用资产部署拓扑)
      - [3.3.4 Who 列：复用资产的治理主体](#334-who-列复用资产的治理主体)
      - [3.3.5 When 列：复用资产生命周期时序](#335-when-列复用资产生命周期时序)
      - [3.3.6 Why 列：复用决策的动机与约束](#336-why-列复用决策的动机与约束)
  - [4. 与 GERAM / ISO 15704 的关联](#4-与-geram--iso-15704-的关联)
    - [4.1 GERAM 概述](#41-geram-概述)
    - [4.2 GERAM 核心构件与复用映射](#42-geram-核心构件与复用映射)
    - [4.3 ISO 15704:2019 的复用要求](#43-iso-157042019-的复用要求)
      - [要求 1：参考架构必须提供企业全生命周期的覆盖](#要求-1参考架构必须提供企业全生命周期的覆盖)
      - [要求 2：参考架构必须区分不同抽象层次](#要求-2参考架构必须区分不同抽象层次)
      - [要求 3：参考架构必须支持多视角描述](#要求-3参考架构必须支持多视角描述)
      - [要求 4：参考架构必须支持模型集成](#要求-4参考架构必须支持模型集成)
      - [要求 5：参考架构必须提供方法论指导](#要求-5参考架构必须提供方法论指导)
      - [要求 6：参考架构必须具备可扩展性](#要求-6参考架构必须具备可扩展性)
    - [4.4 Zachman-GERAM-四层复用 的三层元模型映射](#44-zachman-geram-四层复用-的三层元模型映射)
    - [4.5 ISO 15704:2019 对复用资产标准化的启示](#45-iso-157042019-对复用资产标准化的启示)
  - [5. Zachman 在复用治理中的应用](#5-zachman-在复用治理中的应用)
    - [5.1 复用盲区识别方法论](#51-复用盲区识别方法论)
      - [5.1.1 盲区识别流程](#511-盲区识别流程)
      - [5.1.2 典型盲区模式](#512-典型盲区模式)
    - [5.2 复用资产准入评审的 Zachman 检查清单](#52-复用资产准入评审的-zachman-检查清单)
      - [准入检查清单模板](#准入检查清单模板)
    - [5.3 复用治理的组织映射](#53-复用治理的组织映射)
    - [5.4 复用成熟度评估的 Zachman 维度](#54-复用成熟度评估的-zachman-维度)
  - [6. 案例：企业级复用资产目录规划](#6-案例企业级复用资产目录规划)
    - [6.1 案例背景：GlobalFin 金融科技集团](#61-案例背景globalfin-金融科技集团)
    - [6.2 复用资产目录的 Zachman 坐标规划](#62-复用资产目录的-zachman-坐标规划)
      - [6.2.1 业务复用层（Business Reuse）规划](#621-业务复用层business-reuse规划)
      - [6.2.2 应用复用层（Application Reuse）规划](#622-应用复用层application-reuse规划)
      - [6.2.3 组件复用层（Component Reuse）规划](#623-组件复用层component-reuse规划)
      - [6.2.4 功能复用层（Functional Reuse）规划](#624-功能复用层functional-reuse规划)
    - [6.3 复用盲区识别结果](#63-复用盲区识别结果)
    - [6.4 实施路线图](#64-实施路线图)
      - [第一阶段（0-6 个月）：基础覆盖](#第一阶段0-6-个月基础覆盖)
      - [第二阶段（6-12 个月）：横向扩展](#第二阶段6-12-个月横向扩展)
      - [第三阶段（12-18 个月）：度量优化](#第三阶段12-18-个月度量优化)
    - [6.5 案例启示](#65-案例启示)
  - [8. Zachman 复用性评估矩阵](#8-zachman-复用性评估矩阵)
    - [8.1 评估维度与量化模型](#81-评估维度与量化模型)
    - [8.2 六维度属性表](#82-六维度属性表)
    - [8.3 复用性评估决策树](#83-复用性评估决策树)
    - [8.4 行业案例：三大行业的 Zachman 复用坐标](#84-行业案例三大行业的-zachman-复用坐标)
      - [银行业（基于 BIAN）](#银行业基于-bian)
      - [电信业（基于 TM Forum）](#电信业基于-tm-forum)
      - [制造业](#制造业)
    - [8.5 复用性评估矩阵的行业应用扩展](#85-复用性评估矩阵的行业应用扩展)
      - [医疗健康业](#医疗健康业)
      - [零售与电商业](#零售与电商业)
      - [政府与公共服务业](#政府与公共服务业)
      - [行业复用性热力分区](#行业复用性热力分区)
  - [9. 反例与常见失败模式](#9-反例与常见失败模式)
    - [9.1 反例一：把 Zachman 当成方法论而非分类学](#91-反例一把-zachman-当成方法论而非分类学)
    - [9.2 反例二：跨抽象层次复用导致语义坍塌](#92-反例二跨抽象层次复用导致语义坍塌)
    - [9.3 反例三：为复用而复用——忽视 Why 维度](#93-反例三为复用而复用忽视-why-维度)
    - [9.4 反例四：忽视 Where 维度导致"开发可用、生产不可用"](#94-反例四忽视-where-维度导致开发可用生产不可用)
    - [9.5 反例五：忽视 Who 维度导致治理真空](#95-反例五忽视-who-维度导致治理真空)
  - [10. 与其他概念的关系](#10-与其他概念的关系)
    - [10.1 与四层复用模型的关系](#101-与四层复用模型的关系)
    - [10.2 与 GERAM / ISO 15704 的关系](#102-与-geram--iso-15704-的关系)
    - [10.3 与 TOGAF / ArchiMate 的关系](#103-与-togaf--archimate-的关系)
    - [10.4 与 BPMN / DMN 的关系](#104-与-bpmn--dmn-的关系)
  - [11. 权威来源与交叉引用](#11-权威来源与交叉引用)
    - [11.1 权威来源](#111-权威来源)
    - [11.2 交叉引用](#112-交叉引用)
  - [7. 权威来源与参考文献](#7-权威来源与参考文献)
    - [7.1 核心标准与框架来源](#71-核心标准与框架来源)
    - [7.2 企业架构与复用方法论来源](#72-企业架构与复用方法论来源)
    - [7.3 软件复用与架构来源](#73-软件复用与架构来源)
    - [7.4 领域驱动设计与组件化来源](#74-领域驱动设计与组件化来源)
    - [7.5 本文档引用说明](#75-本文档引用说明)

---

## 1. Zachman Framework 核心概念

### 1.1 框架起源与本体论定位

Zachman Framework 由 John A. Zachman 于 1987 年在 IBM Systems Journal 首次发表，是企业架构（Enterprise Architecture, EA）领域最具影响力和持久力的本体论框架之一。该框架的核心理念在于：**任何复杂系统（尤其是企业系统）的描述都可以通过对六个基本疑问词（What, How, Where, Who, When, Why）与六个利益相关者视角（Planner, Owner, Designer, Builder, Subcontractor, User）进行正交组合，形成 36 个互斥且穷尽的描述单元（cell）**。

与许多过程式或方法论导向的框架不同，Zachman Framework 本质上是一个**分类学（taxonomy）**，而非方法论。它不规定"如何"实施企业架构，而是回答"存在哪些架构描述维度"以及"谁需要看到什么信息"。这一本体论定位使其成为软件架构复用资产分类、目录编制与治理的理想元模型。

### 1.2 六疑问词（列维度）： interrogative abstractions

| 疑问词 | 英文全称 | 核心语义 | 对应架构描述焦点 |
|--------|----------|----------|------------------|
| What | Inventory | 事物清单与本体 | 数据实体、业务对象、系统组件清单 |
| How | Process | 功能与过程转换 | 业务流程、系统功能、技术实现过程 |
| Where | Network | 位置与分布拓扑 | 网络节点、部署位置、地理分布 |
| Who | People / Agent | 角色与组织单元 | 业务角色、系统用户、操作责任人 |
| When | Time | 时序与事件触发 | 业务周期、系统调度、事务时序 |
| Why | Motivation | 动机与约束规则 | 业务目标、合规要求、设计原则 |

每个疑问词列代表一类**不可约减的架构抽象**。在复用语境下，这些列对应着复用资产的六类元数据维度：复用"什么"、复用"如何"实现、复用资产部署"在哪里"、复用资产由"谁"消费/维护、复用"何时"发生、复用"为何"必要。

### 1.3 六视角（行维度）： stakeholder perspectives

| 视角层级 | 英文名称 | 利益相关者 | 抽象粒度 | 核心问题 |
|----------|----------|------------|----------|----------|
| 第1行 | Scope / Planner | 规划者/投资者 | 最粗粒度 | 企业的边界与范围是什么？ |
| 第2行 | Business Model / Owner | 业务所有者 | 业务概念 | 业务如何运作？ |
| 第3行 | System Model / Designer | 系统设计师 | 逻辑模型 | 系统如何支持业务？ |
| 第4行 | Technology Model / Builder | 技术构建者 | 物理设计 | 技术如何构建系统？ |
| 第5行 | Detailed Representation / Subcontractor | 分包商/实施者 | 详细规范 | 组件如何制造与集成？ |
| 第6行 | Functioning Enterprise / User | 最终用户 | 运行实例 | 实际运行中的企业是什么？ |

Zachman 强调每一行都是一种**投影（projection）**：同一企业实体在不同行中被不同利益相关者以不同抽象层次观察，但本质上描述的是同一现实。这一特性使得复用资产可以在不同抽象层之间进行**纵向追溯（vertical traceability）**。

### 1.4 36 Cell 矩阵详解

以下对每个 cell 的语义进行完整解析，并标注其在复用体系中的角色。

#### 第1行：Scope / Planner（规划者视角）

| Cell | 疑问词 | 语义描述 | 典型交付物 | 复用角色 |
|------|--------|----------|------------|----------|
| C1-1 | What | 企业关注的核心事物清单 | 业务术语表、高阶实体清单 | 复用范围定义 |
| C1-2 | How | 企业执行的顶层业务流程 | 价值链图、宏观流程 | 端到端流程模板 |
| C1-3 | Where | 企业的地理/网络边界 | 运营区域图、站点清单 | 部署范围基线 |
| C1-4 | Who | 最高层组织单元与角色 | 组织架构图、汇报线 | 组织复用模板 |
| C1-5 | When | 企业关键业务周期与里程碑 | 战略时间表、财年周期 | 时间框架模板 |
| C1-6 | Why | 企业使命、愿景与战略动机 | 商业模式画布、战略目标 | 战略意图复用基线 |

第1行在复用体系中的核心作用是**定义复用的边界与战略对齐**。所有复用资产必须与第1行的 Why（战略动机）保持可追溯性，否则复用将沦为无目的的技术堆砌。

#### 第2行：Business Model / Owner（业务所有者视角）

| Cell | 疑问词 | 语义描述 | 典型交付物 | 复用角色 |
|------|--------|----------|------------|----------|
| C2-1 | What | 业务实体及其关系 | 概念数据模型、业务对象图 | 业务对象模式 |
| C2-2 | How | 业务过程与工作流 | 业务流程图（BPMN）、用例 | 业务流程模板库 |
| C2-3 | Where | 业务位置与设施分布 | 办公地点图、渠道网络 | 渠道/网络拓扑模板 |
| C2-4 | Who | 业务角色、职责与技能 | RACI 矩阵、岗位说明书 | 角色定义模板 |
| C2-5 | When | 业务事件与状态转换 | 业务周期图、状态机 | 业务规则时序模板 |
| C2-6 | Why | 业务规则、政策与合规要求 | 业务规则目录、合规框架 | 合规规则资产库 |

第2行是**业务复用（Business Reuse）**的主战场。业务复用资产主要对应 C2-1（业务对象模式）、C2-2（业务流程模板）和 C2-6（业务规则/合规框架）。这些资产具有最高的跨项目复用价值，因为它们独立于技术实现，可以在不同技术栈中反复使用。

#### 第3行：System Model / Designer（系统设计师视角）

| Cell | 疑问词 | 语义描述 | 典型交付物 | 复用角色 |
|------|--------|----------|------------|----------|
| C3-1 | What | 逻辑数据模型与信息架构 | 逻辑 ER 图、类图、领域模型 | 领域驱动设计模式 |
| C3-2 | How | 系统功能与逻辑处理 | 系统用例、服务契约、API 规范 | 应用服务/微服务模板 |
| C3-3 | Where | 逻辑部署拓扑与网络分区 | 逻辑网络图、安全区划分 | 部署架构蓝图 |
| C3-4 | Who | 系统用户角色与权限模型 | 用户角色矩阵、权限模型 | 安全与权限模式 |
| C3-5 | When | 系统事件、批处理与调度逻辑 | 事件流图、调度表 | 事件驱动架构模式 |
| C3-6 | Why | 系统级约束、非功能需求 | NFR 规格书、架构决策记录 | 架构决策模板（ADRs） |

第3行是**应用复用（Application Reuse）**的核心层。C3-2（系统功能/服务契约）直接对应应用层可复用资产，如微服务模板、API 网关模式、服务编排规范。C3-1（逻辑数据模型）则支撑领域模型的跨系统复用，是领域驱动设计（DDD）战略层的基础。

#### 第4行：Technology Model / Builder（技术构建者视角）

| Cell | 疑问词 | 语义描述 | 典型交付物 | 复用角色 |
|------|--------|----------|------------|----------|
| C4-1 | What | 物理数据模型与存储结构 | 物理 Schema、数据字典 | 数据库设计模式 |
| C4-2 | How | 技术组件与实现算法 | 组件图、算法规范、代码框架 | 可复用组件/框架 |
| C4-3 | Where | 物理基础设施与部署节点 | 基础设施图、云资源拓扑 | IaC 模板（Terraform/Bicep） |
| C4-4 | Who | 技术角色与运维责任 | DevOps 责任矩阵、值班表 | 运维流程模板 |
| C4-5 | When | 系统作业调度与批处理时间窗 | Cron 规范、批处理窗口 | 调度编排模板 |
| C4-6 | Why | 技术约束、平台标准与选型理由 | 技术雷达、平台规范 | 技术选型决策库 |

第4行是**组件复用（Component Reuse）**的主要映射层。C4-2（技术组件）直接产出可复用软件组件、框架和中间件；C4-3（物理部署）对应基础设施即代码（IaC）模板；C4-1（物理数据模型）则对应数据库迁移脚本和 ORM 映射模式。

#### 第5行：Detailed Representation / Subcontractor（分包商/实施者视角）

| Cell | 疑问词 | 语义描述 | 典型交付物 | 复用角色 |
|------|--------|----------|------------|----------|
| C5-1 | What | 数据结构定义与序列化格式 | XSD、JSON Schema、Protobuf | 数据序列化模式 |
| C5-2 | How | 程序代码、模块与单元实现 | 源代码、函数库、SDK | 可复用函数/库/SDK |
| C5-3 | Where | 机器配置、节点规格与网络参数 | 配置文件、网络策略 | 配置模板与环境基线 |
| C5-4 | Who | 用户账号、证书与访问令牌 | IAM 策略、密钥管理规范 | 安全凭证模板 |
| C5-5 | When | 事务日志、时间戳与审计追踪 | 审计日志格式、TTL 策略 | 日志/审计模板 |
| C5-6 | Why | 代码注释、文档与决策依据 | 代码注释、设计模式文档 | 内联复用指南 |

第5行是**功能复用（Functional Reuse）**的最底层映射。C5-2（程序代码）对应函数库、SDK 和代码片段；C5-1（数据结构定义）对应跨语言共享的数据契约；C5-3（机器配置）对应容器镜像和环境配置模板。

#### 第6行：Functioning Enterprise / User（用户/运行视角）

| Cell | 疑问词 | 语义描述 | 典型交付物 | 复用角色 |
|------|--------|----------|------------|----------|
| C6-1 | What | 运行时的业务数据实例 | 生产数据集、主数据记录 | 测试数据生成模板 |
| C6-2 | How | 实际运行的业务流程实例 | 工作流实例、订单生命周期 | 业务流程监控模板 |
| C6-3 | Where | 实际网络流量与节点状态 | 网络拓扑监控、CDN 日志 | 可观测性配置模板 |
| C6-4 | Who | 实际操作用户与行为数据 | 用户画像、行为日志 | 用户分析模型 |
| C6-5 | When | 实际业务发生的时间序列 | 事件时间线、SLA 达成记录 | SLA 监控基线 |
| C6-6 | Why | 实际决策结果与业务成效 | KPI 仪表盘、ROI 报告 | 复用成效度量模板 |

第6行在复用体系中具有特殊地位：它描述的是**复用资产的实际运行成效**。C6-6（业务成效/ROI）直接对应复用治理中的价值量化维度——通过追踪复用资产在生产环境的表现，评估其对业务目标的实际贡献。

### 1.5 Zachman 矩阵的关键原则与复用启示

1. **完整性原则（Completeness）**：36 个 cell 构成一个完整集合，任何企业架构描述都可以映射到其中至少一个 cell。在复用治理中，这意味着**每个复用资产都应当具有明确的 Zachman 坐标**，从而避免资产归属模糊。

2. **正交性原则（Orthogonality）**：行与列相互独立，改变某一行的描述不应影响其他行的内部一致性。复用启示：同一业务对象模式（C2-1）可以映射到多种技术实现（C4-1/C5-1），实现业务与技术的解耦复用。

3. **非冗余原则（No Redundancy）**：每个 cell 描述的是独特的抽象，不同 cell 之间不应存在语义重复。复用启示：复用资产目录必须消除跨 cell 的重复资产，例如不应同时在 C3-2 和 C4-2 中维护两套独立但语义重叠的服务定义。

4. **递归性原则（Recursion）**：Zachman 框架可以递归应用于企业的任何子系统。复用启示：大型复用资产（如企业级领域模型）可以在子系统级别再次应用 Zachman 进行细分，形成**分形复用目录结构**。

---


### 1.6 六视角/六抽象层次定义与复用性评估矩阵总览

**定义**：[Zachman Framework](https://en.wikipedia.org/wiki/Zachman_Framework) 将企业架构描述抽象为一个由 **6 个利益相关者视角（行）** 与 **6 个基本疑问词（列）** 构成的 6×6 矩阵。每一行代表一种抽象层次（从企业边界到运行实例），每一列代表一种不可约减的描述维度（What、How、Where、Who、When、Why）。在软件架构复用语境下，Zachman 矩阵既是复用资产的分类坐标系，也是评估资产可复用性的结构化框架。

### 六视角与四层复用映射

| 视角（行） | 英文名称 | 抽象层次 | 主要复用层 | 核心复用问题 |
|---|---|---|---|---|
| Scope / Planner | Planner | 企业边界 | 业务复用（战略层） | 复用支持什么战略目标？（Why at Scope） |
| Business Model / Owner | Owner | 业务概念 | 业务复用 | 复用什么业务能力/对象/流程？（What / How at Business） |
| System Model / Designer | Designer | 逻辑模型 | 应用复用 | 系统如何支撑复用资产？（How at System） |
| Technology Model / Builder | Builder | 物理设计 | 组件复用 | 技术在何处、如何实现复用？（How / Where at Technology） |
| Detailed Representation / Subcontractor | Subcontractor | 详细规范 | 功能复用 | 代码与配置如何被复用？（How at Subcontractor） |
| Functioning Enterprise / User | User | 运行实例 | 运行反馈/度量 | 复用产生了哪些可度量的业务成效？（Why at User） |

### 六抽象层次的复用含义

1. **Scope / Planner（规划者视角）**：描述企业的边界、范围和战略意图。该层的复用资产主要是**战略意图模板、商业模式画布、宏观价值链**，为下层复用提供方向约束。
2. **Business Model / Owner（业务所有者视角）**：描述业务概念、业务对象、业务流程和业务规则。该层是**业务复用的主战场**，资产包括业务对象模式、流程模板、规则库。
3. **System Model / Designer（系统设计师视角）**：描述逻辑数据模型、服务契约、逻辑部署和事件驱动模式。该层支撑**应用复用**，核心资产是领域模型、API 规范、架构决策记录。
4. **Technology Model / Builder（技术构建者视角）**：描述物理数据模型、技术组件、基础设施和运维流程。该层支撑**组件复用**，资产包括组件库、IaC 模板、技术栈规范。
5. **Detailed Representation / Subcontractor（分包商/实施者视角）**：描述数据结构、源代码、配置和安全策略。该层支撑**功能复用**，资产包括函数库、Schema、环境配置。
6. **Functioning Enterprise / User（用户/运行视角）**：描述运行时的业务实例、流程实例和成效度量。该层提供**复用价值的反馈闭环**，资产包括 SLA 基线、ROI 报告和可观测性模板。

### 复用性评估矩阵总览

下表给出 36 cell 中典型复用资产的复用性等级（高 / 中 / 低），用于指导复用投资优先级。

| 行 \ 列 | What | How | Where | Who | When | Why |
|---|---|---|---|---|---|---|
| **Scope** | 低 | 低 | 低 | 低 | 低 | 中 |
| **Business Model** | 高 | 高 | 中 | 中 | 中 | 高 |
| **System Model** | 高 | 高 | 中 | 中 | 中 | 中 |
| **Technology Model** | 中 | 中 | 中 | 中 | 中 | 中 |
| **Detailed Rep.** | 中 | 中 | 低 | 低 | 低 | 低 |
| **Functioning Enterprise** | 低 | 低 | 低 | 低 | 低 | 中 |

> **解释**：Business Model 与 System Model 行的 What / How / Why 列抽象程度高、变更频率低，是高复用区；Scope 行过于抽象、Functioning Enterprise 行过于具体，通常直接复用价值低，但可作为度量和反馈来源。

### Zachman 复用坐标映射图

```mermaid
flowchart LR
    subgraph 视角行
        P1[Scope]
        P2[Business Model]
        P3[System Model]
        P4[Technology Model]
        P5[Detailed Rep.]
        P6[Functioning Enterprise]
    end

    subgraph 疑问词列
        Q1[What]
        Q2[How]
        Q3[Where]
        Q4[Who]
        Q5[When]
        Q6[Why]
    end

    P1 --> Q6
    P2 --> Q1 & Q2 & Q6
    P3 --> Q2 & Q1 & Q6
    P4 --> Q2 & Q3 & Q6
    P5 --> Q2 & Q1
    P6 --> Q6 & Q5
```

该图表明：不同视角行在复用治理中关注的疑问词列不同，高价值复用资产通常同时覆盖多个列维度，并形成纵向穿透链。

## 2. 复用视角的 Zachman 映射

### 2.1 映射总览

本项目提出的四层复用模型（业务→应用→组件→功能）并非与 Zachman 行一一对应，而是以**跨行的方式**嵌入 Zachman 矩阵。这种嵌入遵循"高层复用映射到高层行、低层复用映射到低层行"的基本原则，同时认识到复用资产往往**纵向穿透**多个行（例如一个业务对象模式从 C2-1 贯穿到 C5-1）。

```
四层复用模型 → Zachman 行映射关系

业务复用 ───────────→ Scope (Row 1) + Business Model (Row 2)
                      主要回答: Why / What

应用复用 ───────────→ System Model (Row 3)
                      主要回答: How

组件复用 ───────────→ Technology Model (Row 4)
                      主要回答: How / Where

功能复用 ───────────→ Builder (Row 4) + Subcontractor (Row 5)
                      主要回答: How
```

### 2.2 业务复用 → Why / What（Scope / Business Model 行）

**映射原理**：业务复用关注的是跨组织、跨系统的业务能力共享，其本质是对企业"做什么"（What）和"为什么做"（Why）的抽象。在 Zachman 矩阵中，这些内容集中在第1行（Scope）和第2行（Business Model）。

| 复用资产类别 | 对应 Zachman Cell | 资产示例 | 复用场景 |
|--------------|-------------------|----------|----------|
| 业务能力模型 | C1-6 (Why, Scope) | 企业战略地图、价值主张画布 | 新业务单元快速对齐战略 |
| 业务对象模式 | C2-1 (What, Business) | 客户、订单、产品概念模型 | 跨系统统一业务语言 |
| 业务流程模板 | C2-2 (How, Business) | 订单履约流程、客户准入流程 | 业务线间流程标准化 |
| 业务网络拓扑 | C2-3 (Where, Business) | 渠道布局模型、供应链网络 | 跨国/跨区域业务复制 |
| 组织角色模板 | C2-4 (Who, Business) | 岗位能力模型、RACI 模板 | 组织变革快速部署 |
| 业务规则库 | C2-6 (Why, Business) | 合规检查规则、风控策略 | 监管变化快速响应 |

**关键映射规则**：

- 业务复用资产应当优先从 C2-6（业务规则/动机）向下追溯到 C2-1（业务对象），确保任何可复用的业务对象都有明确的业务规则支撑。
- C1-6（战略 Why）是所有业务复用资产的"根"，每个业务复用资产必须能够回答"它支持哪项战略目标"。
- 业务复用资产的消费者主要是 Row 2（Business Owner），因此资产描述语言必须是业务术语，避免技术 jargon。

**纵向穿透示例**：一个"客户主数据"业务复用资产，其 Zachman 穿透路径为：

```
C1-1 (客户是关注实体) → C2-1 (客户业务对象定义)
  → C3-1 (客户逻辑数据模型) → C4-1 (客户物理表结构)
  → C5-1 (客户 JSON Schema) → C6-1 (运行时客户实例)
```

### 2.3 应用复用 → How（System Model 行）

**映射原理**：应用复用关注的是系统功能与服务的跨应用共享，其核心问题是"系统如何支持业务"（How at System Level）。这恰好对应 Zachman 第3行（System Model / Designer）的 How 列（C3-2），以及与之紧密相关的 What（C3-1）和 Why（C3-6）。

| 复用资产类别 | 对应 Zachman Cell | 资产示例 | 复用场景 |
|--------------|-------------------|----------|----------|
| 领域模型 | C3-1 (What, System) | 限界上下文图、聚合根定义 | 微服务划分与共享内核 |
| 应用服务契约 | C3-2 (How, System) | OpenAPI 规范、GraphQL Schema | 跨团队 API 复用 |
| 逻辑部署模式 | C3-3 (Where, System) | 安全区划分、逻辑网络拓扑 | 多环境部署标准化 |
| 权限与访问模型 | C3-4 (Who, System) | RBAC/ABAC 模型、IAM 策略 | 统一身份治理 |
| 事件驱动模式 | C3-5 (When, System) | 领域事件定义、事件总线契约 | 异步集成标准化 |
| 架构决策记录 | C3-6 (Why, System) | ADR-001 微服务拆分原则 | 架构一致性治理 |

**关键映射规则**：

- 应用复用资产的中心是 C3-2（系统功能/服务契约），所有其他列（C3-1, C3-3~6）都是对该服务契约的支撑或约束。
- C3-6（架构决策 Why）是应用复用的治理锚点：每个可复用服务必须附带架构决策记录，说明其设计约束和适用上下文，防止不当复用。
- 应用复用资产应当保持与第2行（Business Model）的向上追溯：C3-2 的每个服务契约必须能够映射到 C2-2 的业务流程步骤。

**服务契约复用的 Zachman 完整描述**：
一个可复用的"支付服务"应用资产，其在 Zachman 矩阵中的完整描述需要以下 cell 的协同：

- C2-2：支付在业务流程中的位置（业务 How）
- C3-1：支付相关的领域概念（系统 What）
- C3-2：支付服务接口定义（系统 How）
- C3-3：支付服务的逻辑部署约束（系统 Where）
- C3-4：支付服务的调用方身份模型（系统 Who）
- C3-5：支付服务的事务时序要求（系统 When）
- C3-6：支付服务采用异步设计的决策理由（系统 Why）

### 2.4 组件复用 → How / Where（Technology Model 行）

**映射原理**：组件复用关注的是技术组件（如 UI 组件、算法组件、中间件插件）的跨系统复用。这些资产位于 Zachman 第4行（Technology Model / Builder），同时强烈涉及 Where（部署位置）维度，因为技术组件的可复用性高度依赖于其运行环境约束。

| 复用资产类别 | 对应 Zachman Cell | 资产示例 | 复用场景 |
|--------------|-------------------|----------|----------|
| 技术组件库 | C4-2 (How, Technology) | React 组件库、日志采集 SDK | 前端/后端组件共享 |
| 基础设施模板 | C4-3 (Where, Technology) | Terraform 模块、K8s Helm Chart | 环境一键复制 |
| 数据访问模式 | C4-1 (What, Technology) | 读写分离模式、分库分表策略 | 数据库架构标准化 |
| 运维自动化脚本 | C4-4 (Who, Technology) | CI/CD Pipeline、发布编排 | DevOps 流程标准化 |
| 批处理调度模板 | C4-5 (When, Technology) | Airflow DAG 模板、定时任务框架 | 数据管道复用 |
| 技术栈规范 | C4-6 (Why, Technology) | 技术选型雷达、平台约束清单 | 技术债务预防 |

**关键映射规则**：

- 组件复用资产的"上下文边界"由 C4-3（Where）和 C4-6（Why）共同定义。一个技术组件只能在特定的部署拓扑和技术约束下被复用，因此其复用元数据必须包含完整的 C4-3/C4-6 描述。
- C4-2（技术 How）与 C3-2（系统 How）之间存在严格的抽象层次差异：C3-2 描述的是"系统做什么"（逻辑功能），C4-2 描述的是"技术如何实现"（物理组件）。混淆这两个层次是组件复用失败的常见原因。
- 组件复用资产必须具备 C4-3（部署 Where）的多态性：同一组件应当提供针对不同部署环境（云/边缘/本地）的变体。

**基础设施模板的复用 Zachman 描述**：
一个可复用的"容器化 Web 应用部署模板"：

- C3-3：逻辑部署需求（需要负载均衡、自动扩展）
- C4-2：技术组件清单（K8s Deployment、Service、Ingress）
- C4-3：基础设施拓扑（AKS 集群、VNet、NSG 规则）
- C4-5：调度参数（HPA 阈值、滚动更新策略）
- C4-6：技术约束（必须使用 Azure CNI、禁止特权容器）

### 2.5 功能复用 → How（Builder / Subcontractor 行）

**映射原理**：功能复用是最细粒度的复用形式，包括代码函数、算法实现、配置片段等。这些资产跨越 Zachman 第4行（Builder）和第5行（Subcontractor），以第5行为主，因为第5行代表了最详细的实现规格。

| 复用资产类别 | 对应 Zachman Cell | 资产示例 | 复用场景 |
|--------------|-------------------|----------|----------|
| 算法/函数库 | C5-2 (How, Subcontractor) | 排序算法、加密函数、数学库 | 代码级复用 |
| 数据结构契约 | C5-1 (What, Subcontractor) | DTO 定义、消息格式、API 模型 | 跨语言数据交换 |
| 环境配置模板 | C5-3 (Where, Subcontractor) | env 文件、YAML 配置、Feature Flag | 环境一致性保障 |
| 安全策略配置 | C5-4 (Who, Subcontractor) | OAuth Scope、JWT Claim 模板 | 安全策略复用 |
| 日志/追踪模板 | C5-5 (When, Subcontractor) | 结构化日志格式、Span 属性规范 | 可观测性标准化 |
| 代码注释规范 | C5-6 (Why, Subcontractor) | 设计模式说明、复用指引注释 | 知识传递 |

**关键映射规则**：

- 功能复用资产以 C5-2（代码实现）为核心，但其可复用性严重依赖于 C5-1（数据契约）和 C5-3（环境配置）的兼容性。
- C5-6（Why）在功能复用中往往被忽视，但实际上至关重要：每个可复用函数应当在其文档/注释中说明"为什么这样实现"（设计决策），以便复用者判断是否满足其上下文需求。
- 功能复用资产需要严格的 C5-5（When）约束：时间相关的代码（如超时逻辑、重试策略）在不同业务场景下的适用性差异极大，必须明确标注时间语义。

**代码函数复用的 Zachman 元数据示例**：
一个可复用的"带指数退避的重试函数"：

- C5-2：函数签名、实现代码、单元测试
- C5-1：输入参数结构（最大重试次数、基础延迟、最大延迟）
- C5-3：适用的运行时环境（Node.js 18+、支持 async/await）
- C5-5：时间语义（退避公式、Jitter 策略、超时传播规则）
- C5-6：设计决策（为何选择指数退避而非线性退避、适用场景说明）

### 2.6 四层复用映射的纵向一致性

四层复用模型在 Zachman 矩阵中的纵向一致性可以通过以下"复用穿透链"来验证：

```
业务复用 (Why/What)
  └─ C2-6: 业务规则"订单金额超过 10 万需风控审批"
      └─ C2-2: 业务流程"风控审批流程"
          └─ C3-2: 应用服务"风控检查服务接口"
              └─ C4-2: 技术组件"风控规则引擎组件"
                  └─ C5-2: 功能代码"规则匹配函数 evaluateRisk()"
                      └─ C6-2: 运行时实例"订单 #20250610001 的风控审批记录"
```

这条穿透链展示了复用资产如何在不同抽象层之间保持语义一致性。复用治理的核心任务之一就是维护这种纵向追溯能力，确保当业务规则（C2-6）发生变化时，能够自动识别所有下游受影响的复用资产（C3-2、C4-2、C5-2）。

---

## 3. 六维疑问词 × 四层复用 交叉矩阵

### 3.1 矩阵定义

以下交叉矩阵展示了 Zachman 的六疑问词列如何映射到四层复用模型的不同决策维度。每个 cell 描述的是：在特定复用层，针对特定疑问词，复用治理需要回答的核心问题。

### 3.2 交叉矩阵全表

| 疑问词 | 业务复用 (Business) | 应用复用 (Application) | 组件复用 (Component) | 功能复用 (Functional) |
|--------|---------------------|------------------------|----------------------|-----------------------|
| **What (Inventory)** | 复用哪些业务能力/对象？<br>→ 业务能力地图、业务对象目录 | 复用哪些领域模型/服务？<br>→ 领域模型库、服务目录 | 复用哪些技术组件/模板？<br>→ 组件仓库、IaC 模块库 | 复用哪些函数/数据结构？<br>→ 代码片段库、Schema 注册表 |
| **How (Process)** | 如何在业务层面组合复用资产？<br>→ 业务流程编排模板 | 如何在应用层面调用复用服务？<br>→ API 组合模式、BFF 模板 | 如何在技术层面集成组件？<br>→ 集成模式（适配器、外观） | 如何在代码层面调用函数？<br>→ 调用示例、Wrapper 代码 |
| **Where (Network)** | 业务能力部署在哪些区域？<br>→ 区域化业务部署策略 | 应用服务部署在哪些环境？<br>→ 多环境部署蓝图 | 组件运行在哪些节点？<br>→ 容器编排模板、边缘部署包 | 代码运行在哪些运行时？<br>→ 运行时兼容性矩阵 |
| **Who (People)** | 谁负责业务能力维护？<br>→ 业务能力 owner 制度 | 谁负责应用服务治理？<br>→ 服务 owner、API 治理委员会 | 谁负责组件版本管理？<br>→ 组件维护者、SIG 小组 | 谁负责代码质量？<br>→ 代码审查者、模块维护者 |
| **When (Time)** | 业务能力何时需要更新？<br>→ 业务周期驱动的版本规划 | 应用服务何时发布新版本？<br>→ 语义化版本策略、发布窗口 | 组件何时需要升级？<br>→ 依赖更新策略、安全补丁周期 | 代码何时过期？<br>→ 弃用策略、生命周期管理 |
| **Why (Motivation)** | 为何需要复用该业务能力？<br>→ 战略对齐检查表 | 为何选择该服务设计？<br>→ 架构决策记录 (ADR) | 为何使用该组件？<br>→ 技术选型决策、替代方案分析 | 为何采用该实现？<br>→ 设计模式说明、性能基准 |

### 3.3 交叉矩阵的决策支持应用

#### 3.3.1 What 列：复用资产发现与目录编制

在 What 维度上，四层复用模型形成了一个**从抽象到具体的资产分类体系**：

- **业务复用 What**：关注"业务能力"和"业务对象"等高阶概念。这些资产的发现方法包括业务能力映射（Business Capability Mapping）和领域分析（Domain Analysis）。
- **应用复用 What**：关注"领域模型"和"服务契约"等逻辑资产。发现方法包括 API 目录挖掘、服务依赖图分析。
- **组件复用 What**：关注"技术组件"和"基础设施模块"等物理资产。发现方法包括代码仓库分析、包管理器元数据抓取。
- **功能复用 What**：关注"代码函数"和"数据结构定义"等实现级资产。发现方法包括代码克隆检测（Clone Detection）、抽象语法树（AST）分析。

**治理决策**：在编制复用资产目录时，必须同时为每个资产标注其在四层 What 中的坐标。例如，一个"用户认证"资产：

- 业务 What：身份验证（Identity Verification）业务能力
- 应用 What：AuthService 领域服务
- 组件 What：Spring Security 配置模板 + JWT 解析组件
- 功能 What：`verifyToken()` 函数 + `Claims` DTO

#### 3.3.2 How 列：复用资产组合与编排

How 维度回答的是"如何使用复用资产"。四层 How 之间存在严格的**组合层次关系**：

```
业务 How (流程编排)
  └─ 调用 ─→ 应用 How (服务调用)
      └─ 调用 ─→ 组件 How (组件集成)
          └─ 调用 ─→ 功能 How (函数调用)
```

每一层的 How 都对下一层提出接口契约要求，而下一层的 How 实现必须满足上一层的契约。这种层次组合关系是复用架构治理的核心约束。

**反模式警示**：如果业务 How 直接调用功能 How（即业务流程直接调用底层代码函数），则破坏了复用层次结构，导致：

- 业务层与技术层紧耦合
- 功能变更时业务层无法隔离影响
- 复用资产的可替换性丧失

#### 3.3.3 Where 列：复用资产部署拓扑

Where 维度在复用决策中往往被低估，但实际上是决定复用成败的关键因素。

| 复用层 | Where 决策焦点 | 典型约束 | 复用影响 |
|--------|---------------|----------|----------|
| 业务 | 区域/法律管辖 | GDPR、数据主权、跨境合规 | 同一业务能力在不同区域可能需要不同实现 |
| 应用 | 环境/集群 | 多租户隔离、网络策略 | 服务复用必须考虑部署环境的网络拓扑兼容性 |
| 组件 | 节点/容器 | 资源限制、运行时版本 | 组件必须声明其资源需求和运行时依赖 |
| 功能 | 运行时/进程 | 语言版本、库依赖 | 函数复用受限于目标运行时的兼容性 |

**多态部署原则**：高价值复用资产应当提供多个 Where 变体。例如，同一业务对象模式应当同时提供：

- 公有云部署变体（C4-3：AKS/EKS/GKE）
- 私有云部署变体（C4-3：OpenShift/VMware）
- 边缘部署变体（C4-3：IoT Edge/K3s）

#### 3.3.4 Who 列：复用资产的治理主体

复用资产的可持续性高度依赖于明确的**治理主体（Who）**。四层 Who 模型如下：

```
业务 Owner（业务线负责人）
  └─ 委托 ─→ 应用 Owner（产品/系统负责人）
      └─ 委托 ─→ 组件 Owner（技术领域负责人）
          └─ 委托 ─→ 功能 Owner（模块开发者）
```

每一层 Owner 对其上层承担 SLA 责任，对其下层行使质量标准要求权。

**关键治理机制**：

- **业务能力 Owner**：负责业务复用资产的 ROI 评估和战略对齐审查，周期为季度。
- **应用服务 Owner**：负责应用复用资产的版本规划、兼容性保证和 deprecation 管理，周期为迭代。
- **组件维护者**：负责组件复用资产的技术债务管理、安全更新和文档维护，周期为周。
- **代码模块维护者**：负责功能复用资产的代码质量、测试覆盖率和性能基准维护，周期为日。

#### 3.3.5 When 列：复用资产生命周期时序

When 维度管理复用资产的**时间语义**：创建时间、有效时间、过期时间、更新时间。

| 时间概念 | 业务复用 | 应用复用 | 组件复用 | 功能复用 |
|----------|----------|----------|----------|----------|
| 创建时间 | 业务战略发布周期 | 产品路线图节点 | Sprint 发布日期 | 代码提交时间 |
| 有效时间 | 业务周期/财年起止 | 版本支持窗口 | 依赖兼容性窗口 | 运行时兼容性窗口 |
| 过期时间 | 业务能力退役计划 | API 弃用时间表 | 组件 EOL 公告 | 函数弃用警告 |
| 更新时间 | 战略调整触发 | 需求变更触发 | 安全漏洞触发 | Bug 修复触发 |

**时序一致性约束**：下层资产的 When 必须嵌套在上层资产的 When 之内。例如，如果一个业务复用资产（C2-2）计划在下个财年退役，那么所有依赖它的应用复用资产（C3-2）必须在业务资产退役之前完成迁移。

#### 3.3.6 Why 列：复用决策的动机与约束

Why 维度是复用治理的**决策锚点**。每个复用资产的引入、更新或退役都必须有明确的 Why 记录。

**Why 的层次结构**：

- **战略 Why（C1-6 / C2-6）**：复用该资产如何支持企业战略目标？例如，"统一支付服务复用以支持全球业务扩张战略"。
- **架构 Why（C3-6）**：复用该服务的设计决策理由是什么？例如，"采用事件驱动模式以支持高并发订单处理（ADR-042）"。
- **技术 Why（C4-6）**：选择该技术组件而非其他替代方案的理由是什么？例如，"选用 Redis 而非 Memcached 以支持持久化会话（技术雷达 2026-Q2）"。
- **实现 Why（C5-6）**：采用该实现方式的理由是什么？例如，"使用快速排序而非归并排序因为在目标数据规模下平均性能更优（基准测试报告 #1287）"。

**Why 的治理作用**：在复用资产目录中，Why 字段是防止"为复用而复用"（reuse for reuse's sake）的关键机制。每个资产在入库时必须提供至少一个战略 Why 和一个架构 Why。

---

## 4. 与 GERAM / ISO 15704 的关联

### 4.1 GERAM 概述

GERAM（Generalized Enterprise Reference Architecture and Methodology，通用企业参考架构和方法论）是由 IFIP-IFAC 任务组提出的企业工程元框架，后被 ISO 15704:2019《企业集成——企业参考架构方法论需求》采纳为国际标准。

GERAM 的核心目标是为企业架构方法论提供一个**元级框架（meta-framework）**，使得不同的企业架构框架（如 Zachman、TOGAF、ARIS、DoDAF）可以在统一的元模型下进行比较、映射和集成。

### 4.2 GERAM 核心构件与复用映射

GERAM 定义了以下核心构件，每个都与软件架构复用存在直接关联：

| GERAM 构件 | 定义 | 与四层复用的关联 | Zachman 映射 |
|------------|------|------------------|--------------|
| **GERA** (Generalized Enterprise Reference Architecture) | 通用企业参考架构，定义企业工程的概念 | 四层复用模型的元元模型 | 对应 Zachman 框架本身（元分类学） |
| **GEEM** (Enterprise Engineering Methodologies) | 企业工程方法论，指导如何实施企业架构 | 复用资产的开发、部署和维护方法论 | 对应 Zachman 行 3-5 的方法论层 |
| **GEMC** (Enterprise Modeling Languages) | 企业建模语言，提供描述企业的符号系统 | 复用资产的描述语言和元数据标准 | 对应各 cell 的交付物格式 |
| **GEOnt** (Enterprise Ontology) | 企业本体，定义企业领域的核心概念 | 复用资产的语义基础 | 对应 C1-1 / C2-1（What 列） |
| **EM** (Enterprise Models) | 企业模型，描述特定企业的架构 | 复用资产的实例化产物 | 对应全部 36 cell 的实例 |
| **EET** (Enterprise Engineering Tools) | 企业工程工具，支持建模和分析 | 复用资产的存储、检索和组合工具 | 对应复用平台/门户 |

### 4.3 ISO 15704:2019 的复用要求

ISO 15704:2019 规定了企业参考架构方法论（ERM）必须满足的六项基本要求。以下展示这些要求如何与复用治理对应：

#### 要求 1：参考架构必须提供企业全生命周期的覆盖

> *"The reference architecture shall cover the whole life-cycle of an enterprise from inception to retirement."*

**复用映射**：四层复用模型必须覆盖复用资产的全生命周期：概念（Business）→ 设计（Application）→ 构建（Component）→ 实现（Functional）→ 运行（User）→ 退役（Governance）。Zachman 的六行恰好提供了这一全生命周期视图。

#### 要求 2：参考架构必须区分不同抽象层次

> *"The reference architecture shall distinguish between different levels of abstraction."*

**复用映射**：四层复用模型本身就是一种抽象层次划分，且每一层在 Zachman 矩阵中跨越多个行。GERAM 要求这种层次划分必须显式且不可混淆——这与 Zachman 的正交性原则一致。

#### 要求 3：参考架构必须支持多视角描述

> *"The reference architecture shall support multiple views of the enterprise for different stakeholders."*

**复用映射**：Zachman 的六行就是六种利益相关者视角。在复用治理中，同一复用资产必须提供多视角描述：业务视角（Owner 看得懂）、设计视角（Designer 能使用）、构建视角（Builder 能部署）。

#### 要求 4：参考架构必须支持模型集成

> *"The reference architecture shall support the integration of models across different domains and levels."*

**复用映射**：这是复用的核心挑战——如何将不同抽象层、不同领域的复用资产组合为一致的整体。Zachman 的纵向穿透链（如第 2.6 节所示）提供了一种模型集成路径。GERAM 进一步要求这种集成必须有明确的语义映射规则，而不仅仅是命名约定。

#### 要求 5：参考架构必须提供方法论指导

> *"The reference architecture shall provide guidance for the development and use of enterprise models."*

**复用映射**：四层复用模型需要配套的方法论来说明：如何发现复用机会、如何提取复用资产、如何评估复用价值、如何管理复用版本。这些方法论对应 GERAM 的 GEEM 构件。

#### 要求 6：参考架构必须具备可扩展性

> *"The reference architecture shall be extensible to accommodate specific enterprise needs."*

**复用映射**：复用资产目录必须是可扩展的——能够容纳新的资产类型、新的描述维度和新的组合模式。Zachman 的递归性原则（框架可以递归应用于子系统）为此提供了扩展机制。

### 4.4 Zachman-GERAM-四层复用 的三层元模型映射

以下展示了三个框架之间的元级映射关系：

```
元-元层 (Meta-Meta Level)
├── GERAM GERA: 企业工程的通用概念框架
│   └── 定义了"什么是企业架构"、"架构描述需要哪些维度"
│
元层 (Meta Level)
├── Zachman Framework: 企业架构的分类学
│   └── 将 GERA 的概念实例化为 6×6 矩阵
│   └── 四层复用模型: 将复用概念映射到 Zachman 矩阵
│
实例层 (Instance Level)
├── 具体企业的复用资产目录
│   └── 每个资产在 Zachman 矩阵中有明确坐标
│   └── 每个资产遵循 GERAM 的生命周期和方法论要求
```

在这个三层结构中：

- **GERAM** 回答"为什么需要复用分类"（本体论基础）
- **Zachman** 回答"复用资产如何分类"（分类学框架）
- **四层复用模型** 回答"在软件架构领域具体复用什么"（领域实例化）

### 4.5 ISO 15704:2019 对复用资产标准化的启示

ISO 15704:2019 的附录中强调了**模型互操作性**的重要性。在复用语境下，这意味着：

1. **语义互操作**：不同复用层的资产必须使用统一的语义模型。例如，C2-1 中的"客户"业务对象必须与 C3-1 中的 Customer 领域类、C4-1 中的 customer 表、C5-1 中的 Customer DTO 保持语义一致性。GERAM 的 GEOnt（企业本体）为此提供了语义锚点。

2. **语法互操作**：复用资产的描述格式必须标准化。GERAM 的 GEMC（建模语言）要求定义统一的资产描述语法。在本项目中，这体现为复用资产的元数据规范（参见 `./struct/01-meta-model-standards/`）。

3. **过程互操作**：复用资产的开发、维护和退役过程必须标准化。GERAM 的 GEEM（方法论）要求定义统一的过程模型。在本项目中，这体现为复用资产生命周期管理流程（参见 `./struct/06-cross-layer-governance/`）。

---

## 5. Zachman 在复用治理中的应用

### 5.1 复用盲区识别方法论

Zachman 矩阵的最直接治理应用是**复用盲区识别（Reuse Blind Spot Detection）**。其核心思想是：在 36 cell 矩阵中，标记已经存在复用资产的 cell 和尚未覆盖的 cell，未覆盖的 cell 即为潜在的复用盲区。

#### 5.1.1 盲区识别流程

**步骤 1：资产盘点（Inventory）**
遍历复用资产目录，为每个资产标注其主坐标 cell（Primary Cell）和次要坐标 cell（Secondary Cells）。例如：

- 一个微服务模板：主坐标 C4-2，次要坐标 C3-2（上游逻辑设计）、C5-2（下游代码实现）。
- 一个业务流程模板：主坐标 C2-2，次要坐标 C1-2（上游战略规划）、C3-2（下游系统支撑）。

**步骤 2：热力图绘制（Heatmap）**
将 36 cell 矩阵可视化为热力图，颜色深浅表示该 cell 中复用资产的数量和成熟度。

**步骤 3：盲区分析（Gap Analysis）**
识别以下类型的盲区：

- **空 cell**：完全没有复用资产的 cell。
- **薄弱 cell**：资产数量少、成熟度低、缺乏维护的 cell。
- **孤岛 cell**：有资产但与其他 cell 缺乏纵向/横向追溯的 cell。

**步骤 4：优先级排序（Prioritization）**
根据业务价值和实施难度为盲区排序。高价值低难度的盲区优先填补。

#### 5.1.2 典型盲区模式

基于多个企业级复用项目的经验，以下是常见的复用盲区模式：

| 盲区模式 | 典型位置 | 成因 | 风险 | 治理对策 |
|----------|----------|------|------|----------|
| **战略-执行断层** | C1-6 (Why, Scope) 与 C2-6 (Why, Business) 之间缺乏追溯 | 战略层与业务层由不同团队负责，缺乏协同机制 | 复用资产与战略目标脱节，投资浪费 | 建立从 C1-6 到 C2-6 的战略分解机制 |
| **业务-系统鸿沟** | C2-2 (How, Business) 与 C3-2 (How, System) 映射不完整 | 业务分析师与系统架构师使用不同语言和工具 | 系统实现偏离业务需求，复用资产无法支撑真实业务 | 引入 BizDevOps 协同流程，统一 BPMN-API 映射规范 |
| **部署描述缺失** | C3-3 (Where, System) 和 C4-3 (Where, Technology) 资产匮乏 | 团队重视功能开发，忽视部署架构文档化 | 复用组件在目标环境无法运行，"开发环境可用，生产环境故障" | 将 IaC 模板纳入复用资产强制交付物 |
| **安全维度薄弱** | C3-4 (Who, System) 和 C4-4 (Who, Technology) 安全相关资产不足 | 安全团队与架构团队工作割裂 | 复用资产带来安全漏洞传播 | 建立安全模式库（Security Pattern Library）作为独立资产类别 |
| **时序语义忽略** | C2-5 (When, Business) 和 C3-5 (When, System) 事件/调度资产缺失 | 时序逻辑分散在代码中，未抽象为可复用资产 | 跨系统集成时的时序假设不一致，导致数据竞态和一致性问题 | 建立企业事件目录（Event Catalog）和调度策略模板 |
| **动机文档匮乏** | C3-6 (Why, System) 和 C4-6 (Why, Technology) 的 ADR/决策记录不足 | 团队追求交付速度，忽视决策记录 | 复用者无法理解设计约束，导致错误复用 | 将 ADR 作为应用/组件复用资产的强制附件 |
| **运行时反馈缺失** | C6-6 (Why, User) 复用成效度量资产空白 | 缺乏复用 ROI 度量体系和工具 | 无法证明复用价值，难以获得持续投资 | 建立复用成效仪表盘，将 C6-6 资产纳入治理范围 |

### 5.2 复用资产准入评审的 Zachman 检查清单

任何复用资产在入库前必须通过 Zachman 维度的评审。以下是标准化的检查清单：

#### 准入检查清单模板

```markdown
# 复用资产准入评审清单

## 基本信息
- 资产名称: [填写]
- 资产类型: [业务/应用/组件/功能]
- 提交日期: [填写]
- 提交人: [填写]

## Zachman 坐标核查

### What (Inventory)
- [ ] 该资产描述了什么？（实体/功能/组件/代码清单）
- [ ] 是否有明确的资产标识符和分类标签？
- [ ] 是否已在复用资产目录中查重？

### How (Process)
- [ ] 该资产如何被使用？（是否有使用指南/示例）
- [ ] 该资产如何与上下游资产组合？（是否有组合示例）
- [ ] 该资产的接口契约是否清晰？

### Where (Network)
- [ ] 该资产适用的部署环境是什么？（云/本地/边缘）
- [ ] 该资产是否有环境依赖声明？（配置文件/IaC）
- [ ] 该资产在多区域部署时是否有已知限制？

### Who (People)
- [ ] 该资产的 Owner/Maintainer 是谁？
- [ ] 该资产的目标用户群体是谁？
- [ ] 该资产的 SLA/支持承诺是什么？

### When (Time)
- [ ] 该资产的版本策略是什么？（语义化版本/日期版本）
- [ ] 该资产的支持生命周期起止时间？
- [ ] 该资产的弃用计划（如适用）？

### Why (Motivation)
- [ ] 该资产支持的战略目标是什么？（对应 C1-6/C2-6）
- [ ] 该资产的设计决策理由是什么？（对应 C3-6/C4-6）
- [ ] 该资产相比替代方案的优势是什么？
- [ ] 该资产的预期 ROI 或价值主张是什么？

## 纵向追溯核查
- [ ] 该资产是否能向上追溯到上层复用资产？
- [ ] 该资产是否能向下支撑下层复用资产？
- [ ] 追溯链中是否存在断裂或语义不一致？

## 评审结论
- [ ] 通过（满足所有检查项）
- [ ] 有条件通过（需补充以下项：[列出]）
- [ ] 拒绝（原因：[列出]）
```

### 5.3 复用治理的组织映射

Zachman 的六视角行可以与复用治理的组织结构映射：

| 治理层级 | 对应 Zachman 行 | 治理主体 | 核心职责 |
|----------|----------------|----------|----------|
| 战略治理层 | Row 1 (Planner) | 企业架构委员会 | 批准业务复用投资、制定复用战略 |
| 业务治理层 | Row 2 (Owner) | 业务能力中心 | 管理业务复用资产、定义业务标准 |
| 应用治理层 | Row 3 (Designer) | 应用架构委员会 | 评审应用复用设计、管理服务目录 |
| 技术治理层 | Row 4 (Builder) | 技术架构委员会 / Platform Team | 管理组件复用资产、制定技术规范 |
| 实施治理层 | Row 5 (Subcontractor) | 工程效能团队 / Guilds | 管理功能复用资产、代码质量 |
| 运营治理层 | Row 6 (User) | SRE / 运营团队 | 监控复用资产运行状态、度量 ROI |

这种组织映射确保了每一行视角都有对应的治理主体，避免了"人人有责、无人负责"的治理真空。

### 5.4 复用成熟度评估的 Zachman 维度

企业复用成熟度可以从 Zachman 矩阵的覆盖度来评估：

| 成熟度级别 | Zachman 覆盖特征 | 典型表现 |
|------------|------------------|----------|
| **L1 初始级** | 仅在少数 cell（通常是 C5-2 代码片段）存在非正式复用 | 复用靠个人关系，无统一目录 |
| **L2 已管理级** | C4-2/C5-2 组件/功能复用资产初步规范化 | 存在内部组件库，但缺乏上层追溯 |
| **L3 已定义级** | C2/C3/C4/C5 存在规范化的复用资产和纵向追溯 | 业务-应用-组件-功能四层复用目录完整 |
| **L4 量化管理级** | 全部 36 cell 至少达到"已识别"状态，关键 cell 达到"已度量" | 复用资产有明确的成熟度指标和使用统计 |
| **L5 优化级** | 36 cell 热力图均衡，C6 行（运行反馈）驱动资产持续优化 | 复用成效数据自动回流，驱动资产迭代 |

---

## 6. 案例：企业级复用资产目录规划

### 6.1 案例背景：GlobalFin 金融科技集团

**GlobalFin** 是一家跨国金融科技集团，拥有以下业务板块：零售银行、企业金融、保险科技、支付网络。集团内部存在大量相似但不一致的业务流程和技术实现，导致：

- 同一"客户开户"业务在不同国家子公司由不同系统支撑，无法共享最佳实践。
- 技术团队重复建设相似的微服务（用户服务、支付服务、通知服务），每个子公司的实现质量参差不齐。
- 缺乏统一的复用资产目录，新人无法快速找到可复用的现有资产。

GlobalFin 决定采用四层复用模型 + Zachman 矩阵来规划其企业级复用资产目录。

### 6.2 复用资产目录的 Zachman 坐标规划

#### 6.2.1 业务复用层（Business Reuse）规划

**目标 Cell**：C1-1~C1-6, C2-1~C2-6

| 资产编号 | 资产名称 | 主坐标 | 次要坐标 | 资产描述 | 覆盖子公司 |
|----------|----------|--------|----------|----------|------------|
| BR-001 | 全球客户主数据模型 | C2-1 | C1-1, C3-1 | 统一客户概念模型（个人/企业/机构） | 全部 |
| BR-002 | 客户准入流程模板 | C2-2 | C1-2, C2-6, C3-2 | KYC/KYB 标准流程，含区域合规变体 | 全部 |
| BR-003 | 反洗钱合规规则库 | C2-6 | C1-6, C2-2, C3-6 | AML 检查规则，支持 FATF/各国监管要求 | 全部 |
| BR-004 | 支付清算网络拓扑 | C2-3 | C1-3, C4-3 | 全球支付网络节点模型（SWIFT/本地清算） | 支付板块 |
| BR-005 | 保险理赔生命周期 | C2-2 | C2-5, C3-2 | 从报案到赔付的标准业务事件序列 | 保险板块 |
| BR-006 | 金融产品销售角色模型 | C2-4 | C2-2, C3-4 | 客户经理、风控专员、合规官角色定义 | 零售银行 |

**纵向追溯示例（BR-002 客户准入流程）**：

```
C1-2 (Scope): "集团须为所有客户提供统一的准入体验"
    ↓ 分解
C2-2 (Business): "客户准入流程 = 身份验证 + 风险评估 + 账户开通"
    ↓ 支撑
C3-2 (System): "准入编排服务 / 风险评估服务 / 账户开通服务"
    ↓ 实现
C4-2 (Technology): "工作流引擎组件 + 规则引擎组件 + 核心银行接口"
    ↓ 编码
C5-2 (Subcontractor): "orchestrateOnboarding() / evaluateRisk() / createAccount()"
    ↓ 运行
C6-2 (User): "客户 #GF-2025-089234 的准入实例记录"
```

#### 6.2.2 应用复用层（Application Reuse）规划

**目标 Cell**：C3-1~C3-6

| 资产编号 | 资产名称 | 主坐标 | 次要坐标 | 资产描述 | 消费者 |
|----------|----------|--------|----------|----------|--------|
| AR-001 | 客户领域模型 | C3-1 | C2-1, C4-1 | DDD 限界上下文：客户管理 BC | 全部应用 |
| AR-002 | 支付服务契约 | C3-2 | C2-2, C4-2, C5-1 | OpenAPI 3.0：支付发起/查询/撤销 | 支付/零售应用 |
| AR-003 | 通知服务契约 | C3-2 | C2-2, C4-2 | OpenAPI 3.0：邮件/SMS/推送统一通知 | 全部应用 |
| AR-004 | 多租户安全架构 | C3-3 | C3-4, C4-3 | 逻辑网络分区 + IAM 策略模型 | SaaS 应用 |
| AR-005 | 事件驱动集成模式 | C3-5 | C2-5, C4-5 | 领域事件定义 + 事件总线拓扑 | 全部应用 |
| AR-006 | 微服务拆分决策集 | C3-6 | C2-6, C4-6 | 12 条微服务拆分 ADR + 反模式清单 | 架构团队 |

**应用复用资产的关键特性**：每个 AR 资产必须附带完整的 C3-6（ADR）文档。例如，AR-002 支付服务契约必须包含：

- ADR-PAY-001：为何采用异步支付确认而非同步确认？
- ADR-PAY-002：为何支付金额使用 Decimal 而非 Float？
- ADR-PAY-003：为何支付接口要求幂等性 Key？

#### 6.2.3 组件复用层（Component Reuse）规划

**目标 Cell**：C4-1~C4-6

| 资产编号 | 资产名称 | 主坐标 | 次要坐标 | 资产描述 | 技术栈 |
|----------|----------|--------|----------|----------|--------|
| CR-001 | 分布式事务协调器 | C4-2 | C3-2, C5-2 | Saga 编排器组件，支持补偿事务 | Java/Spring |
| CR-002 | 全局 ID 生成器 | C4-2 | C3-1, C5-2 | 雪花算法实现，支持 4096 节点 | 多语言 |
| CR-003 | AKS 标准部署模块 | C4-3 | C3-3, C5-3 | Terraform 模块：VNet + AKS + Ingress | Terraform |
| CR-004 | 审计日志采集器 | C4-2 | C3-5, C5-2 | 自动拦截并记录关键业务操作 | Java/Go/Node |
| CR-005 | 缓存策略组件 | C4-2 | C3-2, C5-2 | 多级缓存（本地+Redis）抽象 | Java/Go |
| CR-006 | API 网关配置模板 | C4-3 | C3-3, C3-4 | Kong/Azure APIM 标准配置 | Kong/APIM |

**组件复用资产的 Where 多态要求**：
CR-003（AKS 标准部署模块）必须提供以下变体：

- `cr-003-azure`：Azure AKS 部署（主版本）
- `cr-003-aws`：AWS EKS 部署（次版本）
- `cr-003-gcp`：GCP GKE 部署（次版本）
- `cr-003-local`：Kind/Minikube 本地开发版（开发测试用）

每个变体必须在 C4-3 中声明其基础设施约束差异。

#### 6.2.4 功能复用层（Functional Reuse）规划

**目标 Cell**：C5-1~C5-6

| 资产编号 | 资产名称 | 主坐标 | 次要坐标 | 资产描述 | 语言 |
|----------|----------|--------|----------|----------|------|
| FR-001 | JWT 解析与验证库 | C5-2 | C3-4, C4-4, C5-4 | 支持 RS256/ES256，自动密钥轮换 | Java/Go/Node |
| FR-002 | 货币计算工具 | C5-2 | C2-1, C3-1, C5-1 | 基于 BigDecimal，支持 180+ 货币 | Java/Go/Python |
| FR-003 | 标准响应 DTO 模板 | C5-1 | C3-1, C5-2 | API 统一响应格式（含分页/错误/元数据） | 多语言 |
| FR-004 | 敏感数据脱敏函数 | C5-2 | C2-6, C4-4, C5-4 | 身份证号/银行卡号/手机号脱敏 | 多语言 |
| FR-005 | 分布式锁实现 | C5-2 | C4-2, C5-3 | Redis/ETCD 分布式锁，支持看门狗 | Java/Go |
| FR-006 | 健康检查端点模板 | C5-2 | C4-2, C5-3 |  readiness/liveness 探针标准实现 | 多语言 |

**功能复用资产的 Why 文档要求**：
FR-002（货币计算工具）必须包含以下 Why 文档：

```markdown
## Why: 为何需要专用货币计算工具？

### 背景
金融系统中使用浮点数（float/double）进行货币计算会导致精度损失，
这在审计和监管场景下是不可接受的。

### 决策
使用整数分（cents）+ BigDecimal 进行所有货币运算。

### 替代方案分析
- 方案 A：直接使用数据库 DECIMAL 字段 → 排除：应用层仍需计算
- 方案 B：使用第三方库（如 Joda-Money）→ 排除：引入额外依赖，且不支持部分特殊货币
- 方案 C：自研封装（本方案）→ 选择：轻量、可控、可扩展

### 适用约束
- 仅适用于会计精度要求为 2 位小数的场景
- 加密货币（精度 > 8 位）需使用扩展版本 fr-002-crypto
```

### 6.3 复用盲区识别结果

在 GlobalFin 的 Zachman 复用矩阵盘点中，发现了以下关键盲区：

| 盲区 Cell | 盲区类型 | 现状 | 影响 | 治理措施 |
|-----------|----------|------|------|----------|
| C1-6 (Why, Scope) | 空 cell | 无统一的集团级复用战略文档 | 各子公司复用目标不一致，投资重复 | 由企业架构委员会制定《GlobalFin 复用战略 2026》 |
| C2-5 (When, Business) | 薄弱 cell | 业务事件定义分散在多个流程文档中 | 跨系统集成时的时序假设冲突 | 建立企业级业务事件目录（Event Catalog） |
| C3-3 (Where, System) | 薄弱 cell | 逻辑部署图由各个团队自行维护，无统一标准 | 应用复用资产的多环境部署经常失败 | 制定标准逻辑部署图规范，纳入 AR 资产交付物 |
| C3-6 (Why, System) | 薄弱 cell | ADR 采用率 < 30% | 复用者无法理解设计约束，导致架构腐化 | 将 ADR 作为应用复用资产准入的强制条件 |
| C4-4 (Who, Technology) | 空 cell | 无统一的 DevOps 角色定义和运维责任模板 | 组件复用后运维责任不清，故障响应慢 | 建立 DevOps RACI 模板（CR-DEVOPS-001） |
| C6-6 (Why, User) | 空 cell | 无复用资产 ROI 度量体系和运行反馈 | 无法证明复用价值，难以持续获得投资 | 建立复用成效仪表盘，将 C6-6 资产纳入治理 |

### 6.4 实施路线图

基于 Zachman 盲区的优先级排序，GlobalFin 制定了以下三阶段实施路线图：

#### 第一阶段（0-6 个月）：基础覆盖

- 填补 C1-6 空白：制定集团复用战略，明确四层复用目标。
- 强化 C3-6：在所有应用复用资产中强制附加 ADR。
- 建立 C2-1/C3-1/C4-1 的纵向追溯：以客户主数据为试点，打通 What 列。

#### 第二阶段（6-12 个月）：横向扩展

- 填补 C2-5/C3-5 空白：建立企业事件目录，标准化事件驱动集成。
- 强化 C4-3/C5-3：扩展 IaC 模板库，覆盖所有主要云厂商。
- 建立 C4-4：发布 DevOps 角色模板和运维责任矩阵。

#### 第三阶段（12-18 个月）：度量优化

- 填补 C6-6 空白：上线复用成效仪表盘，自动采集复用资产的使用数据和业务价值。
- 建立 C6 行的全面覆盖：将运行反馈（User 视角）纳入资产迭代闭环。
- 达到成熟度 L4（量化管理级）：所有关键 cell 具备度量指标。

### 6.5 案例启示

GlobalFin 案例展示了 Zachman 矩阵在复用资产目录规划中的实际应用价值：

1. **结构化盘点**：36 cell 矩阵提供了一个穷尽且无冗余的检查框架，确保资产盘点不会遗漏关键维度。
2. **盲区可视化**：通过热力图直观展示复用覆盖的薄弱环节，为投资决策提供数据支撑。
3. **纵向一致性验证**：穿透链分析揭示了业务-系统-技术之间的断裂点，指导集成改进。
4. **治理组织映射**：Zachman 行视角与治理组织层级的映射，明确了每个 cell 的责任主体。

---

## 8. Zachman 复用性评估矩阵

### 8.1 评估维度与量化模型

**定义**：Zachman 复用性评估矩阵（Zachman Reusability Assessment Matrix, ZRAM）是基于 [Zachman Framework](https://en.wikipedia.org/wiki/Zachman_Framework) 的 6×6 单元结构，对每个架构描述单元（cell）中的复用资产从**稳定性、通用性、封装性、可组合性、可观测性、可治理性**六个维度进行量化评分的方法。

形式化：

```text
Reusability(cell) = Σ(wᵢ × scoreᵢ),  i ∈ {稳定性, 通用性, 封装性, 可组合性, 可观测性, 可治理性}

其中：
- scoreᵢ ∈ [0, 5]，由复用治理委员会评定
- wᵢ 为维度权重，默认各 1/6
- Reusability(cell) ∈ [0, 5]，≥4 视为"高复用性"，2-4 为"中复用性"，<2 为"低复用性"
```

### 8.2 六维度属性表

| 维度 | 说明 | 评分依据 | 重要性 |
|---|---|---|---|
| 稳定性 | 资产在过去 12-24 个月内的变更频率 | 变更次数越少得分越高 | 高 |
| 通用性 | 资产适用于 ≥2 个业务上下文的能力 | 适用场景越多得分越高 | 高 |
| 封装性 | 内部实现对使用者不可见的程度 | 接口契约清晰度、依赖隔离度 | 高 |
| 可组合性 | 与其他复用资产组合形成更大单元的难易度 | 接口标准化程度、文档完整性 | 高 |
| 可观测性 | 运行时行为与使用数据可被度量的程度 | 日志、指标、追踪覆盖度 | 中 |
| 可治理性 | 资产生命周期、版本、责任主体明确程度 | Owner、SLA、路线图完备度 | 中 |

### 8.3 复用性评估决策树

```mermaid
flowchart TD
    A[开始：评估复用资产] --> B{是否有明确的<br/>Zachman 坐标？}
    B -- 否 --> C[归入待分类资产<br/>需补全元数据]
    B -- 是 --> D{覆盖 Which 维度？}
    D -- What --> E[检查实体/功能/组件清单<br/>是否完整]
    D -- How --> F[检查流程/服务/代码<br/>使用指南是否清晰]
    D -- Where --> G[检查部署环境<br/>与多态变体]
    D -- Who --> H[检查 Owner 与<br/>治理主体]
    D -- When --> I[检查版本策略与<br/>生命周期]
    D -- Why --> J[检查战略/架构<br/>决策理由]
    E --> K{复用性评分 ≥ 4？}
    F --> K
    G --> K
    H --> K
    I --> K
    J --> K
    K -- 是 --> L[批准入库<br/>作为高复用性资产]
    K -- 否 --> M[有条件入库<br/>或返回改进]
```

**36 Cell 复用性分布规律**：

| 区域 | 典型 Cell | 复用性 | 原因 |
|---|---|---|---|
| 高复用区 | C2-1, C2-2, C2-6, C3-1, C3-2 | 4-5 | 业务对象、流程模板、服务契约抽象程度高、变更频率低 |
| 中复用区 | C3-3, C3-4, C3-5, C4-2, C4-3 | 2-4 | 部署拓扑、权限模型、调度策略与具体环境相关，需适配 |
| 低复用区 | C1-1~C1-6, C6-1~C6-6 | 1-2 | Scope 行过于抽象，Actual 行过于具体，通常不能直接复用 |

### 8.4 行业案例：三大行业的 Zachman 复用坐标

#### 银行业（基于 BIAN）

| Zachman Cell | 复用资产示例 | 复用价值 |
|---|---|---|
| C2-1 (What, Business) | Party / Customer / Account 业务对象 | 跨核心银行、CRM、渠道系统统一客户语义 |
| C2-2 (How, Business) | 开户、支付、贷款审批流程模板 | 加速新产品上市，降低合规成本 |
| C3-2 (How, System) | 标准化服务契约（OpenAPI） | 支持核心银行系统替换时的流程不变性 |
| C4-3 (Where, Technology) | 高可用部署拓扑模板 | 满足监管对灾备、RTO/RPO 的要求 |

#### 电信业（基于 TM Forum）

| Zachman Cell | 复用资产示例 | 复用价值 |
|---|---|---|
| C2-1 (What, Business) | Product / Service / Resource 业务实体 | 支撑 BSS/OSS 一体化 |
| C2-2 (How, Business) | 订单编排、服务保障流程 | 跨有线/无线/云业务复用 |
| C3-1 (What, System) | SID 数据模型 | 降低运营商系统集成成本 |
| C4-2 (How, Technology) | NFV MANO 组件模板 | 加速网络功能虚拟化部署 |

#### 制造业

| Zachman Cell | 复用资产示例 | 复用价值 |
|---|---|---|
| C2-1 (What, Business) | 物料清单（BOM）、产品配置器 | 支持按订单装配（ATO） |
| C2-2 (How, Business) | 订单到交付（OTD）流程模板 | 缩短供应链响应时间 |
| C4-2 (How, Technology) | 工业物联网边缘组件 | 跨工厂设备接入标准化 |
| C5-1 (What, Subcontractor) | OPC UA 数据契约 | 跨厂商设备互操作 |

---


### 8.5 复用性评估矩阵的行业应用扩展

除银行、电信、制造业外，[Zachman Framework](https://en.wikipedia.org/wiki/Zachman_Framework) 的复用性评估矩阵在医疗、零售和政府行业同样具有指导意义。以下补充三类行业的典型复用坐标与资产示例。

#### 医疗健康业

| Zachman Cell | 复用资产示例 | 复用价值 |
|---|---|---|
| C2-1 (What, Business) | 患者、诊疗、处方、医保协议等业务对象 | 统一电子病历与区域健康平台语义 |
| C2-2 (How, Business) | 入院-诊断-治疗-出院流程模板 | 支持医联体/医共体流程标准化 |
| C2-6 (Why, Business) | 临床路径、医保控费规则 | 降低重复检查，提升诊疗一致性 |
| C3-2 (How, System) | 患者主索引（EMPI）服务契约 | 跨系统患者身份识别与数据汇聚 |
| C4-2 (How, Technology) | HL7 FHIR 资源组件 | 加速互操作性实现，降低集成成本 |

#### 零售与电商业

| Zachman Cell | 复用资产示例 | 复用价值 |
|---|---|---|
| C2-1 (What, Business) | 商品、库存、订单、会员业务对象 | 支撑全渠道一致的商品与价格体系 |
| C2-2 (How, Business) | 促销、履约、退换货流程模板 | 快速复制到 new market / new brand |
| C3-2 (How, System) | 订单中心、库存中心服务契约 | 中台化能力沉淀，避免烟囱式系统 |
| C4-3 (Where, Technology) | 多云/多区域部署拓扑模板 | 支持大促弹性与全球化部署 |

#### 政府与公共服务业

| Zachman Cell | 复用资产示例 | 复用价值 |
|---|---|---|
| C1-6 (Why, Scope) | 政务服务“一网通办”战略目标 | 统一跨部门复用愿景与投资优先级 |
| C2-1 (What, Business) | 市民、企业、事项、证照业务对象 | 支撑跨委办局数据共享与业务协同 |
| C2-2 (How, Business) | 行政审批、公共服务流程模板 | 推动政务服务标准化与跨省通办 |
| C3-4 (Who, System) | 统一身份认证与授权模型 | 实现“一次登录、全网通办” |

#### 行业复用性热力分区

```mermaid
flowchart TB
    subgraph 高复用区
        A[C2-1 业务对象]
        B[C2-2 业务流程]
        C[C2-6 业务规则]
        D[C3-2 服务契约]
    end
    subgraph 中复用区
        E[C3-1 领域模型]
        F[C3-3 部署拓扑]
        G[C4-2 技术组件]
        H[C4-3 IaC 模板]
    end
    subgraph 低复用区
        I[C1-x Scope 行]
        J[C6-x 运行实例]
        K[C5-5 时间语义]
    end
    A --> E --> G
    B --> D --> H
    C --> F --> I
```

该图说明：高复用区资产应优先进入企业级复用目录，中复用区资产需附带环境适配说明，低复用区资产通常只作为上下文参考或度量输入。

## 9. 反例与常见失败模式

### 9.1 反例一：把 Zachman 当成方法论而非分类学

**场景**：某大型企业要求所有项目按照 Zachman 的 36 cell 顺序依次交付架构文档，导致在简单微服务改造项目中产生大量无价值的文档。

**问题**：

- Zachman 是**本体论分类框架（taxonomy）**，不是 ADM 式的方法论。
- 强制按 cell 顺序执行会制造流程官僚，而非架构价值。

**后果**：项目进度延迟 30%，开发团队对架构工作产生抵触，复用目录沦为"僵尸文档库"。

**避免建议**：

- 将 Zachman 用作**资产分类和盲区检查**工具，而非项目执行流程。
- 根据项目规模和风险选择性填充相关 cell。

### 9.2 反例二：跨抽象层次复用导致语义坍塌

**场景**：某银行将 C2-1（业务对象"客户"）直接映射为 C5-1（数据库表结构），省略了 C3-1（逻辑数据模型）和 C4-1（物理数据模型）。

**问题**：

- 业务对象的丰富语义（如法律关系、风险偏好、营销偏好）被压缩为几张数据库表。
- 当业务需求变化时，底层表结构被迫大改，影响所有依赖系统。

**后果**：核心系统改造周期从预计 6 个月延长至 18 个月，数据迁移成本超预算 200%。

**避免建议**：

- 坚持**纵向穿透链**完整性：C2-1 → C3-1 → C4-1 → C5-1。
- 每一层只向下层传递必要信息，保留本层的抽象语义。

### 9.3 反例三：为复用而复用——忽视 Why 维度

**场景**：某公司建立企业级组件库，强制所有团队复用通用"工作流引擎组件"，即使某些团队只需要简单的状态机。

**问题**：

- 缺少 C1-6/C2-6 的战略 Why 和业务 Why 论证。
- 组件与具体业务场景的匹配度低，引入不必要的复杂度。

**后果**：部分团队为规避强制复用，私下复制代码并改头换面，形成"影子组件库"，反而增加技术债务。

**避免建议**：

- 每个复用资产入库时必须提供**战略 Why + 架构 Why**。
- 允许团队在证明"替代方案总拥有成本更低"时申请豁免。

### 9.4 反例四：忽视 Where 维度导致"开发可用、生产不可用"

**场景**：某团队复用了 C4-2 的"缓存组件"，但未声明其仅适用于单数据中心部署。该组件被用于多区域部署后，出现跨区缓存一致性问题。

**问题**：

- 组件复用资产的 C4-3（Where）和 C4-6（Why）描述缺失。
- 复用者无法判断组件的运行环境约束。

**后果**：生产环境出现数据不一致，导致交易回滚和客户投诉。

**避免建议**：

- 将**部署拓扑约束**作为组件复用资产的强制元数据。
- 建立多态部署变体（云/本地/边缘）和兼容性矩阵。

---


### 9.5 反例五：忽视 Who 维度导致治理真空

**场景**：某企业在建立复用资产目录时，重点完善了 What（资产清单）、How（使用指南）和 Where（部署环境），但未明确每个资产的 Owner、维护者和消费者责任。资产入库后长期处于“无人认领”状态。

**问题**：

- 缺少 C2-4 / C3-4 / C4-4 的 Who 维度定义，资产变更时找不到决策主体。
- 消费者遇到问题时不知道该向谁反馈，问题长期悬而未决。
- 资产版本升级缺乏影响分析，多个下游系统被意外破坏。

**后果**：

- 复用目录中 40% 以上的资产标注为“维护者待定”，实际使用率不足 15%。
- 一次公共日志组件升级因未通知消费者，导致 6 个系统日志格式不兼容，排查耗时 3 天。
- 团队对复用平台信任度下降，重新倾向于本地复制代码。

**避免建议**：

- 将 **Owner / Maintainer / Consumer Representative** 作为复用资产元数据的强制字段。
- 建立 RACI 矩阵：业务 Owner 负责价值对齐，技术 Owner 负责版本与兼容性，平台团队负责目录治理。
- 在复用平台中为每个资产提供“问题反馈”和“变更通知”通道，形成 Who 维度的闭环。

## 10. 与其他概念的关系

### 10.1 与四层复用模型的关系

Zachman Framework 为四层复用模型（业务→应用→组件→功能）提供**元模型分类坐标**。四层复用模型回答"复用什么"，Zachman 回答"从哪些视角、在哪些抽象层描述复用资产"。

### 10.2 与 GERAM / ISO 15704 的关系

GERAM 是元-元框架，定义企业参考架构需要满足的需求；Zachman 是满足这些需求的一种具体分类学实现；四层复用模型则是在 Zachman 基础上的领域特化。

### 10.3 与 TOGAF / ArchiMate 的关系

TOGAF ADM 提供架构开发方法论，ArchiMate 提供建模语言，Zachman 提供分类框架。三者在复用治理中形成"方法-语言-分类"的互补。

### 10.4 与 BPMN / DMN 的关系

[BPMN](https://en.wikipedia.org/wiki/Business_process_modeling) 主要填充 Zachman 的 C2-2（How, Business）和 C3-2（How, System）；[DMN](https://en.wikipedia.org/wiki/Decision_Model_and_Notation) 填充 C2-6（Why, Business）中可执行业务规则部分。二者共同支撑 How 和 Why 维度的复用。

---

## 11. 权威来源与交叉引用

### 11.1 权威来源

> **权威来源**:
>
> - [Zachman Framework - Wikipedia](https://en.wikipedia.org/wiki/Zachman_Framework) — 概述、历史、六视角六疑问词结构
> - [Zachman International 官方网站](https://www.zachman.com/) — 2020 扩展版与认证
> - [ISO 15704:2019 - GERAM](https://www.iso.org/standard/64207.html) — 企业参考架构方法论需求
> - [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74296.html) — 系统与软件工程架构描述
> - [Business process modeling - Wikipedia](https://en.wikipedia.org/wiki/Business_process_modeling) — 与 BPMN 的关联
>
> **核查日期**: 2026-07-07

### 11.2 交叉引用

- 本主题内：[BIAN 金融服务域复用案例](../struct/02-business-architecture-reuse/case-studies/bian-banking-reuse-case.md) — 银行业的 Zachman 复用坐标实践
- 本主题内：[BPMN 2.0 / DMN 业务过程与决策的复用编排](../struct/02-business-architecture-reuse/06-bpmn-dmn/bpmn-dmn-reuse-orchestration.md) — 填充 Zachman How/Why 维度的可执行标准
- 本主题内：[业务能力复用](../struct/02-business-architecture-reuse/02-business-capability/capability-reuse.md) — 业务复用层核心资产定义
- 上层标准：[FEA BRM 2.0 与 TOGAF Standard 10 Phase B 业务能力图交叉映射](../struct/02-business-architecture-reuse/02-business-capability/fea-brm-togaf-mapping.md) — 业务能力框架映射
- 跨层治理：[复用成熟度模型](../struct/06-cross-layer-governance/03-maturity-models/reuse-maturity-models-rcmm-rise.md) — Zachman 成熟度评估
- 元模型：[ISO/IEC/IEEE 42010:2022 对齐](../struct/01-meta-model-standards/01-iso-420xx-family/alignment-matrix.md)



## 7. 权威来源与参考文献

### 7.1 核心标准与框架来源

1. **Zachman, J. A.** (1987). "A Framework for Information Systems Architecture." *IBM Systems Journal*, Vol. 26, No. 3, pp. 276-292.
   - URL: <https://www.zachman.com/about-the-zachman-framework> (官方网站，2020 扩展版说明)
   - 核查日期: 2026-06-10

2. **Zachman International** (2020). "The Zachman Framework Evolution."
   - URL: <https://www.zachman.com/>
   - 核查日期: 2026-06-10

3. **ISO 15704:2019** — *Enterprise integration — Requirements for enterprise-referencing architectures and methodologies* (GERAM 国际标准版)
   - URL: <https://www.iso.org/standard/64207.html>
   - 核查日期: 2026-06-10

4. **ISO/IEC/IEEE 42010:2022** — *Systems and software engineering — Architecture description*
   - URL: <https://www.iso.org/standard/74296.html>
   - 核查日期: 2026-06-10

### 7.2 企业架构与复用方法论来源

1. **IFIP-IFAC Task Force** (2003). "GERAM: Generalised Enterprise Reference Architecture and Methodology." *Version 1.6.3*.
   - URL: <https://www.popbizops.com/uploads/1/9/8/5/19859163/geram.pdf> (通过 PopBizOps 存档)
   - 核查日期: 2026-06-10

2. **The Open Group** (2022). *TOGAF® Standard, Version 9.2* — 包含对 Zachman Framework 和 GERAM 的映射说明。
   - URL: <https://www.opengroup.org/togaf>
   - 核查日期: 2026-06-10

3. **Schekkerman, J.** (2004). *How to Survive in the Jungle of Enterprise Architecture Frameworks*. Trafford Publishing.
   - URL: <https://www.enterprise-architecture.info/> (作者维护的 EA 框架比较资源站)
   - 核查日期: 2026-06-10

### 7.3 软件复用与架构来源

1. **Jacobson, I., Griss, M., & Jonsson, P.** (1997). *Software Reuse: Architecture, Process and Organization for Business Success*. ACM Press/Addison-Wesley.
   - 经典软件复用理论来源，与本项目的四层复用模型有直接理论传承关系。

2. **Microsoft Azure Well-Architected Framework** (2026). "Reuse and architectural patterns."
   - URL: <https://learn.microsoft.com/en-us/azure/well-architected/>
   - 核查日期: 2026-06-10

3. **OASIS** (2023). *Reference Architecture Foundation for Service Oriented Architecture (SOA-RAF)* — 对业务-应用-组件分层的服务复用提供标准化参考。
    - URL: <https://www.oasis-open.org/standard/soa-raf/>
    - 核查日期: 2026-06-10

### 7.4 领域驱动设计与组件化来源

1. **Evans, E.** (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley.
    - 为 C3-1（领域模型）和 C2-1（业务对象）的映射提供理论基础。

2. **Vernon, V.** (2016). *Domain-Driven Design Distilled*. Addison-Wesley.
    - 限界上下文与复用策略（共享内核、客户-供应商等）的直接映射。

### 7.5 本文档引用说明

本文档中关于 Zachman Framework 的 36 cell 语义描述基于 John Zachman 原始论文（1987）及 Zachman International 官方网站的 2020 扩展说明。GERAM 相关内容基于 ISO 15704:2019 标准文本及 IFIP-IFAC 任务组发布的 GERAM v1.6.3 技术报告。四层复用模型到 Zachman 矩阵的映射为本项目的原创性工作，建立在上述标准框架的理论基础之上。

---

*本文档由架构复用标准委员会维护。如有更新建议，请提交至 `./struct/02-business-architecture-reuse/08-zachman-reuse-mapping/` 目录下的 Issue 跟踪文件。*

---


<!-- SOURCE: struct/02-business-architecture-reuse/case-studies/bian-banking-reuse-case.md -->

<!--
  文档标识: B-06
  任务: BIAN 金融服务域复用案例
  版本: 2026-07-08
  定位: 业务架构复用领域的金融行业标准化实践指南
  对齐标准: BIAN Service Landscape 12.0/14.0, TOGAF Standard 10, FEA 6.0, ISO 20022, DMN 1.5, BPMN 2.0
  状态: ✅ 已完成
-->

# BIAN 金融服务域复用案例

## 目录

- [BIAN 金融服务域复用案例](#bian-金融服务域复用案例)
  - [目录](#目录)
  - [1. BIAN 概述：服务域概念与生态体系](#1-bian-概述服务域概念与生态体系)
    - [1.1 BIAN 的组织背景与使命](#11-bian-的组织背景与使命)
    - [1.2 服务域（Service Domain）概念](#12-服务域service-domain概念)
    - [1.3 300+ 服务域的精确分类](#13-300-服务域的精确分类)
    - [1.4 BIAN 服务域的复用定义](#14-bian-服务域的复用定义)
  - [2. BIAN Service Landscape 12.0 的核心结构](#2-bian-service-landscape-120-的核心结构)
    - [2.1 四级层次结构](#21-四级层次结构)
      - [2.1.1 业务场景（Business Scenario）](#211-业务场景business-scenario)
      - [2.1.2 业务领域（Business Area）](#212-业务领域business-area)
      - [2.1.3 业务子领域（Sub-domain）](#213-业务子领域sub-domain)
      - [2.1.4 服务域（Service Domain）](#214-服务域service-domain)
    - [2.2 业务对象（Business Object）](#22-业务对象business-object)
    - [2.3 行为（Behavior）](#23-行为behavior)
  - [3. BIAN 与 TOGAF/FEA 的映射关系](#3-bian-与-togaffea-的映射关系)
    - [3.1 映射的必要性](#31-映射的必要性)
    - [3.2 BIAN 服务域与 TOGAF ABB/SBB 的映射](#32-bian-服务域与-togaf-abbsbb-的映射)
      - [3.2.1 BIAN 服务域作为 TOGAF ABB](#321-bian-服务域作为-togaf-abb)
      - [3.2.2 从 BIAN 服务域到 TOGAF SBB](#322-从-bian-服务域到-togaf-sbb)
    - [3.3 BIAN 与 FEA 的映射](#33-bian-与-fea-的映射)
      - [3.3.1 BIAN 业务领域与 FEA BRM 的映射](#331-bian-业务领域与-fea-brm-的映射)
      - [3.3.2 BIAN 服务域与 FEA TRM 的映射](#332-bian-服务域与-fea-trm-的映射)
    - [3.4 映射的复用价值](#34-映射的复用价值)
  - [4. 金融服务复用案例](#4-金融服务复用案例)
    - [4.1 案例一："客户信息管理服务域"的跨银行复用](#41-案例一客户信息管理服务域的跨银行复用)
      - [4.1.1 服务域概述](#411-服务域概述)
      - [4.1.2 跨银行复用的挑战与解决方案](#412-跨银行复用的挑战与解决方案)
      - [4.1.3 复用效果评估](#413-复用效果评估)
    - [4.2 案例二："支付执行服务域"的标准化接口与 ISO 20022 对齐](#42-案例二支付执行服务域的标准化接口与-iso-20022-对齐)
      - [4.2.1 服务域概述](#421-服务域概述)
      - [4.2.2 ISO 20022 对齐的必要性](#422-iso-20022-对齐的必要性)
      - [4.2.3 复用实践：支付执行服务域的参考实现](#423-复用实践支付执行服务域的参考实现)
  - [5. BIAN 服务域作为可复用业务组件的粒度分析](#5-bian-服务域作为可复用业务组件的粒度分析)
    - [5.1 粒度分析的理论框架](#51-粒度分析的理论框架)
    - [5.2 BIAN 服务域的粒度特征](#52-bian-服务域的粒度特征)
      - [5.2.1 功能内聚度](#521-功能内聚度)
      - [5.2.2 数据自治性](#522-数据自治性)
      - [5.2.3 接口稳定性](#523-接口稳定性)
    - [5.3 与其他粒度标准的对比](#53-与其他粒度标准的对比)
    - [5.4 粒度调整策略](#54-粒度调整策略)
  - [6. BIAN 与 DMN/BPMN 的结合：可执行业务规则的金融复用](#6-bian-与-dmnbpmn-的结合可执行业务规则的金融复用)
    - [6.1 结合的必要性](#61-结合的必要性)
    - [6.2 BIAN 与 DMN 的结合](#62-bian-与-dmn-的结合)
      - [6.2.1 结合架构](#621-结合架构)
      - [6.2.2 金融复用案例：信贷审批决策](#622-金融复用案例信贷审批决策)
    - [6.3 BIAN 与 BPMN 的结合](#63-bian-与-bpmn-的结合)
      - [6.3.1 结合架构](#631-结合架构)
      - [6.3.2 金融复用案例：客户开户流程](#632-金融复用案例客户开户流程)
    - [6.4 DMN/BPMN/BIAN 三位一体的复用价值](#64-dmnbpmnbian-三位一体的复用价值)
  - [7. 实施建议与路线图](#7-实施建议与路线图)
    - [7.1 评估现状与差距分析](#71-评估现状与差距分析)
    - [7.2 分阶段实施路线图](#72-分阶段实施路线图)
  - [8. BIAN 服务景观与复用边界](#8-bian-服务景观与复用边界)
    - [8.1 BIAN Service Landscape 的形式化定义](#81-bian-service-landscape-的形式化定义)
    - [8.2 BIAN 服务域核心属性](#82-bian-服务域核心属性)
    - [8.3 BIAN Service Landscape 12.0 结构图](#83-bian-service-landscape-120-结构图)
    - [8.4 复用边界](#84-复用边界)
    - [8.5 复用边界的决策树](#85-复用边界的决策树)
  - [9. 反例：BIAN 复用的常见失败模式](#9-反例bian-复用的常见失败模式)
    - [9.1 反例一：机械照搬 BIAN 服务域，忽视遗留系统现实](#91-反例一机械照搬-bian-服务域忽视遗留系统现实)
    - [9.2 反例二：忽视本地监管变体，强制全球统一接口](#92-反例二忽视本地监管变体强制全球统一接口)
    - [9.3 反例三：复用接口但语义不一致](#93-反例三复用接口但语义不一致)
    - [9.4 反例四：只复用规范不复用治理](#94-反例四只复用规范不复用治理)
  - [10. 与其他概念的关系](#10-与其他概念的关系)
    - [10.1 与业务能力的关系](#101-与业务能力的关系)
    - [10.2 与 TOGAF/FEA 的关系](#102-与-togaffea-的关系)
    - [10.3 与 BPMN/DMN 的关系](#103-与-bpmndmn-的关系)
    - [10.4 与 ISO 20022 的关系](#104-与-iso-20022-的关系)
    - [10.5 与 Zachman 的关系](#105-与-zachman-的关系)
  - [11. 权威来源与交叉引用更新](#11-权威来源与交叉引用更新)
    - [11.1 新增权威来源](#111-新增权威来源)
    - [11.2 交叉引用](#112-交叉引用)
  - [12. BIAN 复用价值量化与教训总结](#12-bian-复用价值量化与教训总结)
    - [12.1 复用价值量化框架](#121-复用价值量化框架)
    - [12.2 正例补充：开放银行场景下的 BIAN 复用](#122-正例补充开放银行场景下的-bian-复用)
    - [12.3 反例补充/教训：忽视 BIAN 与现有能力映射导致目录悬置](#123-反例补充教训忽视-bian-与现有能力映射导致目录悬置)
    - [12.4 BIAN-业务能力-价值流映射图](#124-bian-业务能力-价值流映射图)
    - [12.5 权威来源与交叉引用补充](#125-权威来源与交叉引用补充)
  - [13. 仿真案例：亚太银行联盟基于 BIAN 的开放银行能力建设](#13-仿真案例亚太银行联盟基于-bian-的开放银行能力建设)
    - [13.1 场景](#131-场景)
    - [13.2 关键决策](#132-关键决策)
    - [13.3 实施路径](#133-实施路径)
    - [13.4 量化结果](#134-量化结果)
    - [13.5 教训总结](#135-教训总结)
  - [14. 标准条款映射](#14-标准条款映射)
  - [附录：权威来源](#附录权威来源)

---

## 1. BIAN 概述：服务域概念与生态体系

### 1.1 BIAN 的组织背景与使命

BIAN（Banking Industry Architecture Network，银行业架构网络）是一个全球性的非营利组织，成立于 2008 年，由全球主要银行、技术供应商和咨询公司共同发起。其核心使命是通过建立一套标准化的银行业务架构参考模型，降低银行系统之间的互操作成本，推动金融服务的模块化和可复用性。

与传统的技术架构标准（如 TOGAF）或数据标准（如 ISO 20022）不同，BIAN 的独特之处在于它从"业务服务"的视角出发，将银行的全部业务能力分解为细粒度、自治、可组合的服务单元。这种设计哲学与现代微服务架构和领域驱动设计（DDD）高度契合，使得 BIAN 不仅是一个业务架构框架，更是一个连接业务设计与技术实现的桥梁。

### 1.2 服务域（Service Domain）概念

服务域（Service Domain）是 BIAN 架构模型的核心原子单元。每个服务域代表银行业务中的一个自治功能领域，具有以下关键特征：

**自治性（Autonomy）**：每个服务域拥有独立的业务目标、数据模型和行为规范，可以独立于其他服务域进行开发、部署和演进。这种自治性确保了服务域作为复用单元时的低耦合性。

**标准化接口（Standardized Interface）**：每个服务域通过一组预定义的 API 接口对外提供服务。这些接口遵循 BIAN 的信息架构规范，使用统一的语义和语法，确保了不同厂商实现之间的互操作性。

**业务聚焦（Business Focus）**：服务域的边界不是按照技术系统或组织结构划分的，而是按照业务能力划分的。例如，"客户信息管理服务域"关注的是"管理客户信息"这一业务能力，而不是"客户信息系统"这一技术实体。

**可组合性（Composability）**：多个服务域可以通过标准化的服务编排机制组合成更复杂的业务流程。这种组合能力使得银行可以根据自身的业务需求灵活地"拼装"服务能力，而无需从零开发。

### 1.3 300+ 服务域的精确分类

### 1.4 BIAN 服务域的复用定义

**定义**：BIAN 服务域复用（BIAN Service Domain Reuse）是指金融机构基于 BIAN Service Landscape 中标准化的服务域（Service Domain）、业务对象（Business Object）、行为（Behavior）和信息交换规范（Information Exchange），将银行业务能力封装为自治、可组合、可替换的架构资产，并在内部系统、合作伙伴生态和跨银行协作中重复使用的实践。

形式化：

```text
BIAN_Reuse := ⟨SD, BO, B, IX, Gov, Adapt⟩

SD: BIAN 服务域集合
BO: 业务对象模型集合
B: 行为定义集合
IX: 信息交换规范集合
Gov: 服务域治理与版本管理规则
Adapt: 本地化适配规则（监管、税务、渠道等）
```


截至 BIAN Service Landscape 12.0 版本，BIAN 定义了超过 300 个服务域，覆盖了零售银行、公司银行、投资银行、资产管理、保险、支付等全部金融服务领域。这些服务域按照层次化的业务领域（Business Area）和业务能力（Business Capability）进行分类。

主要业务领域包括：

- **客户管理与支持（Customer Management & Support）**：涵盖客户信息管理、客户关系管理、客户画像、客户细分等服务域；
- **产品与服务管理（Product & Service Management）**：涵盖产品设计、产品定价、产品生命周期管理、产品目录等服务域；
- **销售与分销（Sales & Distribution）**：涵盖销售线索管理、销售执行、渠道管理、市场营销等服务域；
- **账户管理与交易处理（Account Management & Transaction Processing）**：涵盖账户开立、账户维护、交易处理、对账等服务域；
- **支付与清算（Payments & Clearing）**：涵盖支付发起、支付执行、清算结算、跨境支付等服务域；
- **风险管理与合规（Risk Management & Compliance）**：涵盖信用风险、市场风险、操作风险、反洗钱、合规报告等服务域；
- **财务管理与报告（Financial Management & Reporting）**：涵盖总账、财务报表、税务管理、成本核算等服务域；
- **人力资源与组织管理（Human Resources & Organization）**：涵盖员工管理、绩效管理、培训发展等服务域。

每个业务领域下又细分为多个子领域（Sub-domain），每个子领域包含若干个具体的服务域。这种层次化的分类体系使得银行可以在不同粒度上进行架构复用——既可以复用单个服务域，也可以复用整个业务领域的标准化参考模型。

---

## 2. BIAN Service Landscape 12.0 的核心结构

### 2.1 四级层次结构

BIAN Service Landscape 12.0 采用了清晰的四级层次结构，从抽象的业务意图逐步细化到可执行的服务规范：

```
业务场景（Business Scenario）
    │
    ├── 业务领域（Business Area）
    │       │
    │       ├── 业务子领域（Sub-domain）
    │       │       │
    │       │       └── 服务域（Service Domain）
    │       │               │
    │       │               ├── 业务对象（Business Object）
    │       │               └── 行为（Behavior）
    │       │
```

#### 2.1.1 业务场景（Business Scenario）

业务场景是 BIAN 模型的最高抽象层，描述了银行在特定市场环境或监管要求下需要实现的端到端业务能力。例如：

- "零售客户开户场景"：从客户初次接触到账户正式启用的完整流程；
- "跨境支付场景"：从支付发起到最终结算的跨境资金转移流程；
- "小微贷款审批场景"：从贷款申请到审批决策的完整信贷流程。

业务场景不是静态的参考模型，而是随着市场变化、技术发展和监管演进而持续更新的动态视图。BIAN 通过场景库（Scenario Library）为会员提供最新的行业场景定义。

#### 2.1.2 业务领域（Business Area）

业务领域是对银行全部业务能力的宏观划分，每个领域代表一个相对独立的业务价值链片段。BIAN Service Landscape 12.0 定义了约 20 个顶级业务领域，这些领域共同构成了银行的完整业务版图。

业务领域的设计遵循"高内聚、低耦合"原则：领域内部的业务活动紧密相关，领域之间的依赖关系尽量减少。这种设计使得银行可以独立地对某个业务领域进行数字化转型，而不必一次性重构全部系统。

#### 2.1.3 业务子领域（Sub-domain）

业务子领域是对业务领域的进一步细分，每个子领域代表一个更为聚焦的业务功能集群。例如，在"支付与清算"业务领域下，可以细分为：

- 支付发起子领域（Payment Initiation）
- 支付执行子领域（Payment Execution）
- 清算结算子领域（Clearing & Settlement）
- 支付查询与纠纷子领域（Payment Inquiry & Dispute）

子领域的划分粒度通常对应于银行内部的一个中型业务部门或一条产品线。

#### 2.1.4 服务域（Service Domain）

服务域是 BIAN 模型中最细粒度的标准化单元，也是架构复用的核心对象。每个服务域包含以下要素：

- **服务域标识符**：唯一的编码和名称，如 "Customer Information Management"（客户信息管理）；
- **业务定义**：该服务域的核心业务目的和范围边界；
- **业务对象模型**：该服务域所管理的核心业务实体及其属性；
- **行为定义**：该服务域对外提供的服务操作（如创建、读取、更新、删除、查询、验证等）；
- **服务域状态模型**：描述业务对象在其生命周期中可能经历的状态及状态转换规则；
- **信息交换规范**：定义该服务域与其他服务域之间交换的数据结构和语义。

### 2.2 业务对象（Business Object）

业务对象是服务域内部的核心数据实体，代表了该服务域所管理的业务概念。例如，在"客户信息管理服务域"中，核心业务对象包括：

- **Customer Profile（客户档案）**：客户的基本身份信息、联系方式、偏好设置等；
- **Customer Relationship（客户关系）**：客户与银行之间的法律关系、服务协议、授权委托等；
- **Customer Segment（客户细分）**：客户所属的市场细分、风险评级、价值评级等；
- **Customer Consent（客户同意）**：客户对数据使用、营销沟通、第三方共享等的授权记录。

每个业务对象都包含一组标准化的属性定义，这些属性使用 BIAN 的统一信息模型进行语义标注，确保了跨服务域、跨银行的数据一致性。

### 2.3 行为（Behavior）

行为定义了服务域对外提供的服务能力，通常以动词-名词的形式命名，如 "Create Customer Profile"、"Validate Customer Identity"、"Update Customer Contact Details"。每个行为定义包含：

- **行为目的**：该服务操作的业务意图；
- **输入参数**：调用该操作需要提供的数据；
- **输出结果**：操作成功或失败后返回的数据；
- **前置条件**：执行该操作前必须满足的业务规则；
- **后置条件**：操作执行后对业务状态的影响；
- **异常处理**：操作失败时的错误码和恢复建议。

BIAN 将行为分为两类：

- **记录型行为（Record Behavior）**：对业务对象进行持久化变更的操作（如创建、更新、删除）；
- **评估型行为（Evaluate Behavior）**：对业务状态进行查询或评估而不产生持久化变更的操作（如查询、验证、计算）。

---

## 3. BIAN 与 TOGAF/FEA 的映射关系

### 3.1 映射的必要性

TOGAF（The Open Group Architecture Framework）和 FEA（Federal Enterprise Architecture Framework）是全球最广泛使用的企业架构框架。在银行和其他金融机构中，TOGAF 尤其占据主导地位，成为架构治理和系统规划的标准方法论。

然而，TOGAF 和 FEA 本质上是"通用型"架构框架，它们提供了架构开发的方法论（ADM）、架构内容的分类结构（Content Metamodel）和架构能力的组织方式，但并未对特定行业（如银行业）的业务能力进行细化定义。BIAN 的出现填补了这一空白——它为银行业务提供了精确的架构内容（Architecture Building Blocks, ABB），而 TOGAF 提供了这些内容的管理方法和交付流程。

因此，在金融服务领域的架构复用实践中，理解 BIAN 与 TOGAF/FEA 的映射关系至关重要。

### 3.2 BIAN 服务域与 TOGAF ABB/SBB 的映射

TOGAF 的架构内容模型区分了架构构建块（Architecture Building Blocks, ABB）和解决方案构建块（Solution Building Blocks, SBB）：

- **ABB（架构构建块）**：描述架构的逻辑功能和能力，独立于具体的技术实现。ABB 回答的是"需要什么样的能力"；
- **SBB（解决方案构建块）**：描述 ABB 的具体技术实现。SBB 回答的是"如何实现这些能力"。

#### 3.2.1 BIAN 服务域作为 TOGAF ABB

BIAN 的服务域天然地对应于 TOGAF 的 ABB。每个服务域定义了一个自治的业务能力边界、标准化的接口规范和业务语义，这些都是 ABB 的核心特征。

具体映射关系如下：

| TOGAF ABB 属性 | BIAN 服务域对应要素 |
|---------------|-------------------|
| ABB 名称 | 服务域名称（如 "Customer Information Management"） |
| ABB 描述 | 服务域的业务定义和范围说明 |
| ABB 功能 | 服务域的行为定义（Record Behavior + Evaluate Behavior） |
| ABB 数据 | 服务域的业务对象模型 |
| ABB 接口 | 服务域的信息交换规范（API 定义） |
| ABB 依赖 | 服务域之间的协作关系（Collaboration Pattern） |

在 TOGAF 的架构开发方法（ADM）中，BIAN 服务域可以在以下阶段直接作为输入：

- **阶段 B：业务架构**：使用 BIAN 的业务领域和服务域作为业务能力模型的参考基线；
- **阶段 C：信息系统架构**：将服务域映射为应用组件（Application Component），将服务域之间的协作映射为应用接口（Application Interface）；
- **阶段 D：技术架构**：为每个服务域选择具体的技术平台和部署模式，形成 SBB。

#### 3.2.2 从 BIAN 服务域到 TOGAF SBB

当组织决定将某个 BIAN 服务域纳入其技术实现时，需要完成从 ABB 到 SBB 的转换：

1. **技术选型**：为服务域选择具体的技术栈（如 Java/Spring、.NET、Node.js）和数据存储（如关系型数据库、文档数据库）；
2. **实现细化**：将服务域的行为定义细化为具体的 API 端点、方法签名和数据传输对象（DTO）；
3. **非功能需求补充**：为服务域定义性能指标、可用性要求、安全控制等技术约束；
4. **集成适配**：将服务域的标准接口映射到组织现有的集成中间件（如 ESB、API Gateway、Message Queue）。

### 3.3 BIAN 与 FEA 的映射

FEA（Federal Enterprise Architecture Framework）虽然最初为美国联邦政府设计，但其"性能参考模型"（PRM）和"业务参考模型"（BRM）的概念对金融服务行业同样具有参考价值。

#### 3.3.1 BIAN 业务领域与 FEA BRM 的映射

FEA 的业务参考模型（BRM）将政府业务划分为"公民服务"、"服务交付支持"、"内部管理"等大类。在金融服务语境下，BIAN 的业务领域可以与 FEA BRM 进行如下对应：

| FEA BRM 一级分类 | BIAN 业务领域对应 |
|-----------------|------------------|
| 服务交付（Service Delivery） | 客户管理与支持、销售与分销、产品与服务管理 |
| 服务交付支持（Service Delivery Support） | 账户管理与交易处理、支付与清算 |
| 内部管理（Internal Management） | 风险管理与合规、财务管理与报告、人力资源与组织管理 |

#### 3.3.2 BIAN 服务域与 FEA TRM 的映射

FEA 的技术参考模型（TRM）定义了技术服务和组件的分类体系。BIAN 服务域在技术实现层面可以与 FEA TRM 进行映射，例如：

- "客户信息管理服务域"的实现依赖于 FEA TRM 中的"数据管理"和"身份与访问管理"技术服务；
- "支付执行服务域"的实现依赖于 FEA TRM 中的"事务处理"和"安全服务"技术服务。

### 3.4 映射的复用价值

建立 BIAN 与 TOGAF/FEA 的映射关系，对架构复用具有以下实际价值：

1. **降低架构治理的学习成本**：对于已经采用 TOGAF 作为架构治理框架的银行，可以直接将 BIAN 的内容嵌入现有的 ADM 流程，而无需引入全新的方法论；
2. **促进跨行业标准对齐**：当金融机构需要与政府系统（如税务、社保）或跨行业合作伙伴进行系统对接时，FEA 映射可以提供通用的架构语言；
3. **支持监管报告**：许多监管机构要求银行提交基于标准架构框架的系统架构描述，BIAN-TOGAF 映射可以简化这一流程；
4. **增强供应商管理**：在采购第三方系统时，可以要求供应商按照 BIAN 服务域的标准进行功能映射和接口适配，降低系统集成成本。

---

## 4. 金融服务复用案例

### 4.1 案例一："客户信息管理服务域"的跨银行复用

#### 4.1.1 服务域概述

"客户信息管理服务域"（Customer Information Management Service Domain）是 BIAN Service Landscape 中最基础、最广泛使用的服务域之一。其核心职责是集中管理银行的客户主数据（Customer Master Data），确保客户信息在所有业务渠道和系统中的唯一性、准确性和一致性。

该服务域的核心业务对象包括：

- **Customer Profile**：客户的基本身份信息（姓名、证件号码、出生日期等）；
- **Customer Contact**：客户的联系方式（地址、电话、邮箱等）；
- **Customer Preference**：客户的服务偏好（沟通语言、联系时间、渠道偏好等）；
- **Customer Relationship**：客户与银行之间的法律关系和服务协议；
- **Customer Consent**：客户对数据处理和第三方共享的授权记录。

#### 4.1.2 跨银行复用的挑战与解决方案

在传统的银行 IT 架构中，客户信息往往分散在多个系统中：核心银行系统管理账户持有人信息，CRM 系统管理客户关系信息，网上银行系统管理数字渠道偏好，移动银行系统管理生物识别信息。这种分散的数据架构导致了严重的数据不一致问题——同一客户在不同系统中的姓名拼写、联系方式或风险评级可能各不相同。

基于 BIAN "客户信息管理服务域"的标准化定义，多家银行参与了跨银行的复用实践：

**标准化数据模型复用**：

- 参与银行共同采纳 BIAN 定义的客户信息业务对象模型，统一了客户数据的语义定义；
- 例如，所有银行统一使用 BIAN 定义的 "Party" 概念来抽象"个人客户"和"企业客户"，替代了各家银行原有的不同命名（如 "Customer"、"Client"、"Counterparty"）。

**标准化 API 接口复用**：

- 基于 BIAN 的信息交换规范，参与银行共同定义了一组标准化的 RESTful API：
  - `POST /customer-profiles`：创建新客户档案；
  - `GET /customer-profiles/{id}`：查询客户档案详情；
  - `PATCH /customer-profiles/{id}`：更新客户信息；
  - `POST /customer-profiles/{id}/validate`：验证客户身份信息；
  - `GET /customer-profiles/{id}/consents`：查询客户授权记录。
- 这些 API 的输入输出数据结构严格遵循 BIAN 的业务对象定义，确保了不同银行系统之间的语义互操作性。

**技术实现复用**：

- 在部分合作项目中，参与银行共同投资开发了一个开源的"客户信息管理"参考实现（Reference Implementation），基于 BIAN 服务域规范构建；
- 该参考实现包含了完整的业务逻辑、数据持久化层、API 接口层和单元测试套件，参与银行可以基于该参考实现进行二次开发和定制化；
- 这种"共建共享"的模式显著降低了每家银行独立开发的成本，同时通过社区协作提升了代码质量。

#### 4.1.3 复用效果评估

参与跨银行复用实践的机构报告了以下效果：

- **数据一致性提升**：客户信息在不同系统和渠道之间的一致性错误率下降了约 70%；
- **系统集成成本降低**：与外部合作伙伴（如征信机构、支付网络）的系统对接时间平均缩短了 40%；
- **监管合规效率提升**：由于客户数据模型符合 BIAN 标准，生成监管报告（如 KYC、AML 报告）的自动化程度显著提高；
- **新客户上线时间缩短**：当银行收购或合并其他金融机构时，客户数据的迁移和整合时间大幅缩短。

### 4.2 案例二："支付执行服务域"的标准化接口与 ISO 20022 对齐

#### 4.2.1 服务域概述

"支付执行服务域"（Payment Execution Service Domain）负责处理支付指令的实际执行，包括支付验证、路由选择、清算提交和状态跟踪。这是支付价值链中的核心环节，直接涉及资金的转移和结算。

该服务域的核心业务对象包括：

- **Payment Order**：支付指令，包含付款人、收款人、金额、货币、用途等关键信息；
- **Payment Execution**：支付执行记录，跟踪一笔支付从发起到完成的完整生命周期；
- **Payment Clearing**：清算记录，记录支付在清算系统中的处理状态；
- **Payment Settlement**：结算记录，记录资金的实际转移和账户余额变更。

#### 4.2.2 ISO 20022 对齐的必要性

ISO 20022 是全球金融报文交换的国际标准，被 SWIFT、欧元区 TARGET2、英国 Faster Payments 等主要支付系统采纳。该标准使用基于 XML 的报文格式，对支付指令中的每个数据元素进行了严格的语义定义。

在全球支付系统加速向 ISO 20022 迁移的背景下，银行需要确保其支付执行系统能够生成和解析符合 ISO 20022 标准的报文。BIAN "支付执行服务域"的设计充分考虑了这一需求：

**业务对象与 ISO 20022 报文元素的映射**：

- BIAN 的 `Payment Order` 业务对象与 ISO 20022 的 `pain.001`（客户信用转账发起）和 `pain.008`（客户直接借记发起）报文直接对应；
- BIAN 的 `Payment Execution` 业务对象与 ISO 20022 的 `pacs.008`（FIToFICustomerCreditTransfer）报文对应；
- BIAN 的信息交换规范中明确定义了每个业务属性与 ISO 20022 报文元素的映射关系，确保了语义一致性。

**标准化接口设计**：

- BIAN 为支付执行服务域定义的标准 API 接口，其请求和响应数据结构可以直接序列化为 ISO 20022 XML 报文或 JSON 等价表示；
- 例如，`POST /payment-orders` API 的请求体可以直接映射为 `pain.001.001.09` 报文格式。

#### 4.2.3 复用实践：支付执行服务域的参考实现

多个国际银行和支付技术供应商参与了 BIAN 支付执行服务域的参考实现项目：

**场景一：跨境支付平台复用**：

- 一家全球性银行集团基于 BIAN 支付执行服务域的规范，开发了一套跨境支付处理平台；
- 该平台支持 SWIFT gpi、TARGET2、SEPA Instant 等多种支付网络，通过统一的 BIAN 标准化接口与集团的各个区域核心银行系统对接；
- 当集团在新市场开设业务时，可以直接复用该平台，只需适配当地的支付网络接口，而无需重新开发支付执行的核心逻辑。

**场景二：支付技术供应商的产品标准化**：

- 多家支付技术供应商（如核心银行系统厂商、支付中间件厂商）将 BIAN 支付执行服务域的规范作为其产品的标准功能模块；
- 当银行采购这些供应商的产品时，产品内置的支付执行功能已经符合 BIAN 标准，银行只需进行少量的配置和定制化，无需进行复杂的系统集成开发；
- 这种"供应商生态标准化"的模式进一步放大了 BIAN 服务域的复用价值。

**场景三：开放银行 API 的支付服务**：

- 在实施 PSD2（支付服务指令 II）开放银行要求的欧洲银行中，多家银行基于 BIAN 支付执行服务域的规范设计了其开放 API 的支付端点；
- 这种设计使得第三方支付发起服务提供商（PISP）可以通过标准化的接口发起支付，而银行后端系统可以直接使用符合 BIAN 规范的支付执行服务域进行处理；
- 由于 BIAN 与 ISO 20022 的语义对齐，银行在满足 PSD2 技术要求的同时，也确保了与欧洲支付生态的互操作性。

---

## 5. BIAN 服务域作为可复用业务组件的粒度分析

### 5.1 粒度分析的理论框架

在软件架构复用中，组件的粒度（Granularity）是一个关键的架构决策变量。粒度过大，组件的可复用性降低，因为不同使用场景只需要组件的部分功能；粒度过小，组件的管理和集成成本增加，因为需要组合大量细粒度组件才能完成有意义的业务功能。

BIAN 服务域的粒度设计经过十多年的行业实践验证，形成了相对稳定的"黄金粒度"范围。以下从多个维度分析 BIAN 服务域的粒度特征。

### 5.2 BIAN 服务域的粒度特征

#### 5.2.1 功能内聚度

每个 BIAN 服务域都围绕一个单一、聚焦的业务能力构建，具有高度的功能内聚性。例如：

- "客户信息管理服务域"专注于客户主数据的管理，不包含客户关系管理或客户营销的功能；
- "支付执行服务域"专注于支付指令的执行处理，不包含支付发起或支付查询的功能。

这种高内聚性确保了服务域作为复用单元时的功能完整性——复用者无需担心遗漏某些相关功能，也无需处理不相关的功能。

#### 5.2.2 数据自治性

每个服务域拥有独立的业务对象模型和数据主权。服务域之间通过标准化的信息交换进行协作，而不是直接共享数据库表或数据文件。这种数据自治性：

- 降低了服务域之间的耦合度，使得每个服务域可以独立演进；
- 支持服务域的分布式部署，不同服务域可以运行在不同的技术平台上；
- 简化了数据治理，每个服务域的数据质量、数据安全和数据生命周期由该服务域独立负责。

#### 5.2.3 接口稳定性

BIAN 服务域的接口设计遵循"开闭原则"——接口一旦发布，保持向后兼容，新增功能通过扩展接口实现，而不是修改已有接口。这种接口稳定性：

- 保护了复用者的投资，当服务域升级时，复用者无需修改已有的集成代码；
- 支持服务域的独立版本演进，不同服务域可以采用不同的发布节奏；
- 降低了回归测试的成本，接口的稳定性意味着集成测试用例可以长期复用。

### 5.3 与其他粒度标准的对比

| 粒度级别 | 典型代表 | 与 BIAN 服务域的对比 |
|---------|---------|-------------------|
| 粗粒度：整个业务系统 | 核心银行系统、全功能 CRM | BIAN 服务域的粒度远小于整个系统，一个典型的核心银行系统可以实现数十个 BIAN 服务域 |
| 中粒度：业务模块 | ERP 模块、CRM 模块 | BIAN 服务域的粒度与业务模块相当，但接口标准化程度更高，耦合度更低 |
| 细粒度：微服务 | 单一职责的微服务 | BIAN 服务域的粒度与微服务类似，但增加了业务语义层的标准化规范 |
| 极细粒度：函数/方法 | 可复用的代码库函数 | BIAN 服务域远大于函数级别，通常包含完整的业务逻辑、数据模型和 API 接口 |

从复用实践的角度来看，BIAN 服务域的粒度处于"中粒度"到"细粒度"之间，这是一个在可复用性、可管理性和可集成性之间取得平衡的"甜蜜点"（Sweet Spot）。

### 5.4 粒度调整策略

在实际应用中，组织可能需要根据自身的架构上下文对 BIAN 服务域的粒度进行调整：

**服务域合并**：

- 当多个服务域在技术上紧密耦合（如共享同一个遗留数据库），且短期内无法解耦时，可以暂时将它们合并为一个更大的复用单元；
- 例如，将"客户信息管理"和"客户联系历史"两个服务域合并为一个"客户主数据管理"组件。

**服务域拆分**：

- 当某个服务域的功能复杂度超过单个团队的维护能力时，可以将其拆分为更细粒度的子服务域；
- 例如，将"风险管理"服务域拆分为"信用风险管理"、"市场风险管理"和"操作风险管理"三个子服务域。

**服务域封装**：

- 在遗留系统现代化项目中，可以将一个遗留系统封装为一个或多个 BIAN 服务域的 facade（外观），在保持内部实现不变的情况下，对外暴露标准化的 BIAN 接口；
- 这种"封装复用"策略是银行进行渐进式架构演进的重要手段。

---

## 6. BIAN 与 DMN/BPMN 的结合：可执行业务规则的金融复用

### 6.1 结合的必要性

BIAN 服务域定义了"做什么"（What）——即标准化的业务能力和接口规范。然而，在实际业务执行中，还需要定义"怎么做"（How）——即业务规则、决策逻辑和流程编排。

DMN（Decision Model and Notation，决策模型与标记法）和 BPMN（Business Process Model and Notation，业务流程模型与标记法）是 OMG（Object Management Group）发布的两项国际标准，分别用于业务决策建模和业务流程建模。将 BIAN 与 DMN/BPMN 结合，可以实现从"标准化业务能力"到"可执行业务逻辑"的完整复用链条。

### 6.2 BIAN 与 DMN 的结合

#### 6.2.1 结合架构

在 BIAN-DMN 结合架构中：

- **BIAN 服务域**提供决策所需的数据输入（通过 Evaluate Behavior）和决策结果的执行动作（通过 Record Behavior）；
- **DMN 决策模型**定义业务规则的逻辑结构，包括决策表（Decision Table）、决策树和 Boxed Expression；
- **DMN 引擎**（如 Camunda、Red Hat Decision Manager）负责解析和执行 DMN 模型，调用 BIAN 服务域的 API 获取输入数据，并将决策结果回写到 BIAN 服务域。

#### 6.2.2 金融复用案例：信贷审批决策

以"小微企业贷款审批"场景为例，说明 BIAN 与 DMN 的结合方式：

**BIAN 服务域提供数据支持**：

- `Customer Information Management` 服务域提供客户的基本信息、信用历史和风险评级；
- `Product & Service Management` 服务域提供贷款产品的定价参数和审批规则配置；
- `Collateral Management` 服务域提供抵押物评估信息；
- `Account Management` 服务域提供客户的账户交易历史和余额信息。

**DMN 决策模型定义审批逻辑**：

- **输入数据**：客户年收入、经营年限、信用评分、抵押物价值、贷款金额、贷款期限等；
- **决策节点**：
  - "信用评分评估"：基于客户信用评分决定初步风险等级（高/中/低）；
  - "还款能力评估"：基于客户收入和负债比率计算还款能力指数；
  - "抵押物充足性评估"：基于抵押物价值和贷款金额计算抵押率；
  - "综合审批决策"：综合上述评估结果，输出审批决策（批准/拒绝/人工复审）和贷款定价（利率、期限）。

**可复用性体现**：

- 多家银行可以复用相同的 BIAN 服务域规范来获取标准化的客户数据；
- 同时，每家银行可以基于自身的风险偏好和监管要求，定制化其 DMN 决策模型；
- 由于 BIAN 服务域的接口标准化，DMN 决策模型中的数据输入定义可以跨银行复用，银行只需调整决策规则本身。

### 6.3 BIAN 与 BPMN 的结合

#### 6.3.1 结合架构

在 BIAN-BPMN 结合架构中：

- **BPMN 流程模型**定义端到端的业务流程，包括任务（Task）、网关（Gateway）、事件（Event）和泳道（Lane）；
- **BIAN 服务域**作为 BPMN 流程中"服务任务"（Service Task）的实现提供者，通过标准化的 API 接口执行业务操作；
- **BPMN 引擎**（如 Camunda、IBM BPM、Oracle BPM）负责流程的编排和状态管理，在流程执行到特定节点时调用相应的 BIAN 服务域 API。

#### 6.3.2 金融复用案例：客户开户流程

以"零售客户开户"场景为例，说明 BIAN 与 BPMN 的结合方式：

**BPMN 流程定义**：

```
[开始事件: 客户提交开户申请]
    │
    ▼
[服务任务: 验证客户身份]  ──▶ 调用 BIAN "Customer Information Management" 的 Validate Customer Identity 行为
    │
    ▼
[网关: 身份验证是否通过?]
    │── 否 ──▶ [用户任务: 通知客户补充材料] ──▶ [结束事件]
    │
    ▼ 是
[服务任务: 创建客户档案]  ──▶ 调用 BIAN "Customer Information Management" 的 Create Customer Profile 行为
    │
    ▼
[服务任务: 执行 KYC 检查]  ──▶ 调用 BIAN "Know Your Customer" 服务域的 Evaluate KYC Risk 行为
    │
    ▼
[网关: KYC 风险是否可接受?]
    │── 否 ──▶ [用户任务: 提交人工审核] ──▶ [结束事件]
    │
    ▼ 是
[服务任务: 开立账户]  ──▶ 调用 BIAN "Account Management" 的 Open Account 行为
    │
    ▼
[服务任务: 发送开户确认]  ──▶ 调用 BIAN "Customer Notification" 服务域的 Send Notification 行为
    │
    ▼
[结束事件: 开户完成]
```

**可复用性体现**：

- BIAN 服务域的标准化行为定义，使得 BPMN 流程中的"服务任务"可以直接映射为具体的 API 调用，而无需关心底层的技术实现；
- 当银行更换核心系统供应商时，只要新系统符合 BIAN 服务域规范，BPMN 流程模型无需修改即可继续运行；
- 不同银行可以复用相同的 BPMN 流程模板，只需根据自身的产品策略和合规要求调整流程中的网关判断条件和用户任务分配规则。

### 6.4 DMN/BPMN/BIAN 三位一体的复用价值

将 BIAN、DMN 和 BPMN 三者结合，形成了一个完整的、可执行的金融业务复用体系：

| 层次 | 标准 | 复用内容 | 复用范围 |
|-----|------|---------|---------|
| 业务能力层 | BIAN | 标准化的服务域定义、业务对象模型、API 接口规范 | 跨银行、跨系统 |
| 业务决策层 | DMN | 决策表结构、输入数据定义、决策结果格式 | 跨银行（需定制化规则） |
| 业务流程层 | BPMN | 流程模板、任务编排模式、异常处理流程 | 跨银行（需定制化规则） |

这种三位一体的架构使得金融机构可以在以下三个维度上实现规模化复用：

1. **数据语义复用**：通过 BIAN 标准化的业务对象模型，确保跨系统、跨组织的数据一致性；
2. **服务能力复用**：通过 BIAN 标准化的服务域接口，实现业务功能的即插即用；
3. **流程和决策复用**：通过 BPMN 和 DMN 标准化的流程和决策模型，实现业务运营最佳实践的共享和传播。

---

## 7. 实施建议与路线图

### 7.1 评估现状与差距分析

在引入 BIAN 进行架构复用之前，组织应首先进行现状评估：

- 梳理现有的业务能力和系统模块，识别与 BIAN 服务域的对应关系；
- 评估现有系统接口与 BIAN 标准化接口的差距；
- 识别最关键的业务领域（如支付、客户管理、风险管理），优先进行 BIAN 对齐。

### 7.2 分阶段实施路线图

**第一阶段：认知与试点（3-6 个月）**

- 组织 BIAN 培训和知识转移；
- 选取 1-2 个业务场景进行 BIAN 服务域映射试点；
- 建立内部的 BIAN 架构评审委员会。

**第二阶段：标准化与扩展（6-12 个月）**

- 制定组织级的 BIAN 采用标准和接口规范；
- 将 BIAN 服务域规范纳入系统设计和开发的标准流程；
- 在新系统建设中强制要求 BIAN 对齐。

**第三阶段：生态与深化（12-24 个月）**

- 与合作伙伴和供应商建立基于 BIAN 标准的协作机制；
- 引入 DMN/BPMN 与 BIAN 的集成，实现可执行业务规则的复用；
- 参与 BIAN 社区，贡献行业最佳实践和反馈标准改进建议。

---

## 8. BIAN 服务景观与复用边界

### 8.1 BIAN Service Landscape 的形式化定义

**定义**：BIAN Service Landscape（银行业服务景观）是 BIAN 组织维护的一套标准化银行业务能力参考模型，通过业务场景（Business Scenario）、业务领域（Business Area）、业务子领域（Sub-domain）、服务域（Service Domain）四级结构，将银行业务分解为 300+ 自治、可组合、可复用的服务域，每个服务域包含业务对象、行为、状态模型和标准化 API 接口。

形式化：

```text
BIAN_SL := ⟨BA, SD, BO, B, I, CP⟩

BA: 业务领域集合
SD: 服务域集合
BO: 业务对象集合
B: 行为集合
I: 信息交换规范集合
CP: 服务域协作模式集合
```

### 8.2 BIAN 服务域核心属性

| 属性 | 说明 | 可观察指标 | 重要性 |
|---|---|---|---|
| 自治性 | 服务域拥有独立业务目标和数据主权 | 外部依赖数量、数据共享范围 | 高 |
| 标准化接口 | 通过统一 API 规范对外服务 | OpenAPI 覆盖率、接口变更频率 | 高 |
| 业务聚焦 | 边界按业务能力划分，而非技术系统 | 是否包含非相关业务功能 | 高 |
| 可组合性 | 可与其他服务域编排成业务场景 | 被引用次数、协作模式数量 | 高 |
| 语义稳定性 | 业务对象和行为的定义长期稳定 | 版本变更中破坏性变更比例 | 高 |
| 实现无关性 | 规范独立于具体技术实现 | 是否规定特定数据库/中间件 | 中 |

### 8.3 BIAN Service Landscape 12.0 结构图

```mermaid
flowchart TB
    BS[业务场景<br/>Business Scenario] --> BA1[客户管理与支持]
    BS --> BA2[产品与服务管理]
    BS --> BA3[销售与分销]
    BS --> BA4[账户管理与交易处理]
    BS --> BA5[支付与清算]
    BS --> BA6[风险管理与合规]
    BS --> BA7[财务管理与报告]

    BA1 --> SD1[服务域：客户信息管理]
    BA1 --> SD2[服务域：客户关系管理]
    BA5 --> SD3[服务域：支付发起]
    BA5 --> SD4[服务域：支付执行]
    BA6 --> SD5[服务域：信用风险管理]

    SD1 --> BO1[业务对象：Customer Profile]
    SD1 --> BO2[业务对象：Customer Consent]
    SD4 --> BO3[业务对象：Payment Order]
    SD4 --> BO4[业务对象：Payment Execution]

    SD1 --> B1[行为：Create Customer Profile]
    SD1 --> B2[行为：Validate Customer Identity]
    SD4 --> B3[行为：Execute Payment]
    SD4 --> B4[行为：Track Payment Status]
```

### 8.4 复用边界

**应该复用的内容**：

| 边界内 | 说明 |
|---|---|
| 服务域规范 | 业务定义、边界、行为清单 |
| 业务对象模型 | 核心实体及其属性、关系 |
| 信息交换规范 | API 请求/响应结构、数据类型 |
| 协作模式 | 服务域之间的标准交互模式 |
| 参考实现 | 经社区验证的开源参考代码 |

**不应该强制复用的内容**：

| 边界外 | 说明 |
|---|---|
| 具体技术栈 | 服务域不强制 Java/.NET/特定数据库 |
| 本地化规则 | 各国监管、税务、合规变体 |
| 非功能性配置 | 性能参数、部署拓扑、容量规划 |
| 遗留系统封装细节 | 适配器实现因银行而异 |
| 用户界面 | 渠道特定的 UI/UX |

### 8.5 复用边界的决策树

```mermaid
flowchart TD
    A[评估潜在复用内容] --> B{是否在 BIAN 服务域规范中?}
    B -- 是 --> C{是否与技术实现无关?}
    B -- 否 --> D[不建议作为 BIAN 资产复用]
    C -- 是 --> E[适合跨银行/跨系统复用]
    C -- 否 --> F{是否可通过参数化适配?}
    F -- 是 --> G[作为可配置复用资产]
    F -- 否 --> H[作为本地扩展，不归入核心复用资产]
```

---

## 9. 反例：BIAN 复用的常见失败模式

### 9.1 反例一：机械照搬 BIAN 服务域，忽视遗留系统现实

**场景**：某中型银行决定全面采用 BIAN，要求所有新系统严格按照 BIAN 服务域拆分，并计划两年内替换核心银行系统。

**问题**：

- 忽视遗留核心系统的复杂性和数据耦合。
- 服务域拆分过细，导致大量分布式事务和集成点。
- 团队对 BIAN 理解不足，将"服务域"简单等同于"微服务"。

**后果**：

- 项目延期 18 个月，预算超支 160%。
- 数据一致性问题和性能问题频发。
- 部分服务域因过度拆分而难以独立交付价值。

**避免建议**：

- 采用**渐进式对齐**策略，先对新增业务能力采用 BIAN，遗留系统通过 facade 模式渐进暴露 BIAN 接口。
- 服务域不等于微服务，一个微服务可实现多个服务域，一个服务域也可由多个微服务实现。

### 9.2 反例二：忽视本地监管变体，强制全球统一接口

**场景**：某全球银行集团要求所有区域使用完全一致的"客户信息管理"API，包括数据字段和验证规则。

**问题**：

- 不同国家/地区对 KYC、数据隐私、身份证件类型的要求不同。
- 强制统一导致各地系统在 API 之上增加大量"变通层"。
- 原本的标准化接口反而增加了系统复杂度。

**后果**：

- 区域系统交付周期延长。
- API 变通层造成数据质量和审计追踪问题。
- 集团无法准确掌握各区域实际数据模型。

**避免建议**：

- 区分**核心标准数据元素**和**本地扩展数据元素**。
- 在信息交换规范中明确定义扩展点（extension points）和本地化适配机制。

### 9.3 反例三：复用接口但语义不一致

**场景**：两家银行都采用 BIAN "Payment Order" 业务对象，但一家将"收款人"定义为账户持有人，另一家定义为实际受益人。

**问题**：

- 虽然 API 字段名称相同，但业务语义存在细微差异。
- 在跨银行集成时，资金被错误路由。

**后果**：

- 跨境支付测试阶段发现错误，险些造成资金损失。
- 两家银行被迫进行昂贵的接口重新映射。

**避免建议**：

- 复用 BIAN 规范时，必须进行**语义对齐验证**。
- 建立业务术语表（Business Glossary）和数据血统（Data Lineage）治理。
- 在集成测试中增加语义断言，而非仅验证字段格式。

### 9.4 反例四：只复用规范不复用治理

**场景**：某银行引入 BIAN 服务域目录，但未建立相应的服务域 Owner、版本管理和变更影响分析流程。

**问题**：

- 多个团队随意修改"共享"服务域接口。
- 版本管理混乱，消费者无法及时了解变更。
- 服务域之间的协作关系无人维护。

**后果**：

- 接口频繁破坏性变更，下游系统反复返工。
- 团队开始绕过标准接口直接访问数据库。
- BIAN 复用计划名存实亡。

**避免建议**：

- 建立**服务域 Owner 制度**，每个服务域有明确的业务和技术负责人。
- 实施语义化版本控制和消费者影响分析。
- 将 BIAN 规范纳入架构评审和质量门禁。

---

## 10. 与其他概念的关系

### 10.1 与业务能力的关系

BIAN 服务域是银行业务能力的标准化表达，可映射到通用业务能力模型。参见 [业务能力复用](../struct/02-business-architecture-reuse/02-business-capability/capability-reuse.md)。

### 10.2 与 TOGAF/FEA 的关系

BIAN 提供银行业特定的 ABB（架构构建块），TOGAF 提供 ABB 的管理方法论，FEA BRM 提供跨行业业务能力分类参考。详细映射见 [FEA BRM 2.0 与 TOGAF Standard 10 Phase B 业务能力图交叉映射](../struct/02-business-architecture-reuse/02-business-capability/fea-brm-togaf-mapping.md)。

### 10.3 与 BPMN/DMN 的关系

BIAN 定义"做什么"（服务域和能力），[BPMN](https://en.wikipedia.org/wiki/Business_process_modeling) 定义"怎么做"（流程编排），[DMN](https://en.wikipedia.org/wiki/Decision_Model_and_Notation) 定义"怎么决定"（业务规则）。

### 10.4 与 ISO 20022 的关系

BIAN 业务对象与 [ISO 20022](https://en.wikipedia.org/wiki/ISO_20022) 报文元素存在映射，共同支撑金融报文互操作。

### 10.5 与 Zachman 的关系

BIAN 服务域可映射到 Zachman 矩阵的 C2-1（What, Business）、C2-2（How, Business）和 C3-2（How, System）等 cell。参见 [Zachman Framework 与软件架构复用映射](../struct/02-business-architecture-reuse/08-zachman-reuse-mapping/zachman-reusability-matrix.md)。

---

## 11. 权威来源与交叉引用更新

### 11.1 新增权威来源

> **权威来源**:
>
> - [Banking Industry Architecture Network - Wikipedia](https://en.wikipedia.org/wiki/Banking_Industry_Architecture_Network) — BIAN 组织概述
> - [ISO 20022 - Wikipedia](https://en.wikipedia.org/wiki/ISO_20022) — 金融报文标准
> - [Business process modeling - Wikipedia](https://en.wikipedia.org/wiki/Business_process_modeling) — BPMN 关联
> - [Decision Model and Notation - Wikipedia](https://en.wikipedia.org/wiki/Decision_Model_and_Notation) — DMN 关联
> - [BIAN 官方网站](https://bian.org/) — Service Landscape 12.0 与服务域规范
> - [The Open Group TOGAF](https://www.opengroup.org/togaf) — 架构开发方法
> - [FEA Framework](https://obamawhitehouse.archives.gov/omb/e-gov/fea) — 联邦企业架构框架
>
> **核查日期**: 2026-07-07

### 11.2 交叉引用

- [Zachman Framework 与软件架构复用映射](../struct/02-business-architecture-reuse/08-zachman-reuse-mapping/zachman-reusability-matrix.md) — BIAN 服务域在 Zachman 矩阵中的坐标
- [BPMN 2.0 / DMN 业务过程与决策的复用编排](../struct/02-business-architecture-reuse/06-bpmn-dmn/bpmn-dmn-reuse-orchestration.md) — BIAN 与 BPMN/DMN 的结合
- [业务能力复用](../struct/02-business-architecture-reuse/02-business-capability/capability-reuse.md) — 服务域作为银行业务能力单元
- [价值流复用的形式化组合](../struct/02-business-architecture-reuse/03-value-stream/value-stream-composition.md) — 金融服务价值流组合
- [FEA BRM 2.0 与 TOGAF Standard 10 Phase B 业务能力图交叉映射](../struct/02-business-architecture-reuse/02-business-capability/fea-brm-togaf-mapping.md) — BIAN 与 FEA/TOGAF 的映射基础




## 12. BIAN 复用价值量化与教训总结

### 12.1 复用价值量化框架

BIAN 服务域复用的价值不仅体现在技术层面，更体现在业务敏捷性、合规效率和生态协同上。下表给出可量化的复用价值评估框架。

| 价值维度 | 典型指标 | 计算方法 | 示例目标 |
|---|---|---|---|
| 成本节约 | 复用避免重复建设成本 | （自建成本 - 复用适配成本）× 复用次数 | 单个服务域年节约 ≥ 50 万美元 |
| 上市时间 | 新业务/产品上线周期 | 复用后平均上线周数 / 复用前平均上线周数 | 缩短 30%-50% |
| 质量提升 | 接口缺陷率、数据一致性错误率 | 复用前后缺陷数对比 | 数据一致性错误下降 ≥ 60% |
| 合规效率 | 监管报告生成时间、审计问题数 | 复用标准模型后报告自动化率 | KYC/AML 报告生成时间缩短 40% |
| 生态协同 | 与合作伙伴/供应商集成周期 | 平均集成周数 | 与第三方支付/征信对接缩短 50% |
| 架构敏捷性 | 服务域替换/升级所需人天 | 复用标准化接口后的系统替换人天 | 核心系统替换周期缩短 25% |

> **说明**：价值量化应结合定性评估（如战略对齐、组织能力沉淀）与定量指标，避免仅以短期成本节约衡量 BIAN 复用成效。

### 12.2 正例补充：开放银行场景下的 BIAN 复用

**背景**：某欧洲银行在实施 PSD2 开放银行要求时，需要向第三方支付发起服务提供商（PISP）和账户信息服务提供商（AISP）开放标准化 API。

**复用实践**：

1. 采用 BIAN **支付发起（Payment Initiation）** 和 **支付执行（Payment Execution）** 服务域作为开放 API 的设计基线。
2. 将 BIAN 业务对象（如 `Payment Order`、`Payment Execution`）映射到 ISO 20022 报文元素，确保与欧洲支付生态互操作。
3. 通过 BIAN 标准化接口，将银行内部核心系统与开放 API 层解耦：核心系统只需符合 BIAN 规范，开放 API 层可独立演进。
4. 复用 BIAN 与 [DMN](https://en.wikipedia.org/wiki/Decision_Model_and_Notation) 结合的风险决策模型，对每笔开放支付进行实时欺诈检测。

**效果**：

- 开放银行 API 从设计到上线用时 4 个月，较行业平均 9 个月大幅缩短。
- 与 12 家第三方 PISP/AISP 的集成平均耗时 2 周，显著降低生态接入成本。
- 核心系统无需为每一家第三方单独定制接口，维护成本降低 35%。

### 12.3 反例补充/教训：忽视 BIAN 与现有能力映射导致目录悬置

**场景**：某银行投入大量资源将 BIAN Service Landscape 翻译为中文并导入内部架构库，但未将其与现有业务能力地图、系统清单、项目组合建立映射。

**问题**：

- BIAN 服务域目录成为独立的“标准陈列馆”，项目团队不知道如何选择和引用。
- 现有系统改造时，没有从 BIAN 服务域到遗留模块的迁移路径。
- 能力 Owner 和系统 Owner 对 BIAN 目录缺乏认同感，认为“与我的工作无关”。

**后果**：

- 目录上线一年后，主动引用率不足 5%。
- 多个项目仍按原有系统边界设计，BIAN 对齐流于形式。
- 管理层质疑 BIAN 投资价值，后续推广预算被削减。

**避免建议**：

- 在引入 BIAN 的同时，建立 **BIAN 服务域 ↔ 业务能力 ↔ IT 系统 ↔ 项目组合** 的四层映射。
- 选择 2-3 个高价值业务场景（如支付、客户信息管理）进行端到端映射试点，形成可复制的方法论。
- 将 BIAN 引用纳入架构评审、项目立项和供应商招标的强制检查项。

### 12.4 BIAN-业务能力-价值流映射图

```mermaid
flowchart TB
    subgraph BIAN 服务景观
        SD1[客户信息管理]
        SD2[支付执行]
        SD3[信用风险管理]
        SD4[账户管理]
    end

    subgraph 业务能力
        C1[管理客户信息]
        C2[执行支付]
        C3[评估信用风险]
        C4[管理账户]
    end

    subgraph 价值流
        V1[开户价值流]
        V2[支付价值流]
        V3[贷款审批价值流]
    end

    SD1 --> C1 --> V1
    SD2 --> C2 --> V2
    SD3 --> C3 --> V3
    SD4 --> C4 --> V1 & V2
```

该图说明：BIAN 服务域是银行业务能力的标准化表达，业务能力又是价值流的组成单元。只有当三者映射清晰时，BIAN 复用才能真正落地。

### 12.5 权威来源与交叉引用补充

> **权威来源**:
>
> - [BIAN 官方网站](https://bian.org/) — Service Landscape 12.0/14.0 与服务域规范；核查日期：2026-07-08
> - [BIAN Service Landscape 14.0 发布新闻](https://bian.org/news-room/bian-unveils-new-service-landscape-14-0-to-accelerate-ai-ready-banking-architecture/) — 2026-05 BIAN 14.0 更新；核查日期：2026-07-08
> - [ISO 20022 官方站点](https://www.iso20022.org/) — 金融报文标准；核查日期：2026-07-08
> - [The Open Group TOGAF](https://www.opengroup.org/togaf) — 架构开发方法；核查日期：2026-07-08
> - [Banking Industry Architecture Network - Wikipedia](https://en.wikipedia.org/wiki/Banking_Industry_Architecture_Network) — BIAN 组织概述；核查日期：2026-07-08
>
> **核查日期**: 2026-07-08

**交叉引用**：

- [业务能力复用](../struct/02-business-architecture-reuse/02-business-capability/capability-reuse.md) — BIAN 服务域作为银行业务能力单元
- [价值流复用的形式化组合](../struct/02-business-architecture-reuse/03-value-stream/value-stream-composition.md) — 金融服务价值流组合
- [BPMN 2.0 / DMN 业务过程与决策的复用编排](../struct/02-business-architecture-reuse/06-bpmn-dmn/bpmn-dmn-reuse-orchestration.md) — BIAN 与 BPMN/DMN 的结合
- [Zachman Framework 与软件架构复用映射](../struct/02-business-architecture-reuse/08-zachman-reuse-mapping/zachman-reusability-matrix.md)

## 13. 仿真案例：亚太银行联盟基于 BIAN 的开放银行能力建设

> 说明：本案例为基于 BIAN 公开文档、ISO 20022 迁移实践与 PSD2/开放银行监管要求的**仿真场景**，用于演示 BIAN 复用中的关键决策、实施路径与教训。

### 13.1 场景

"亚太银行联盟"由 5 家中小型银行组成，计划在 18 个月内建成统一的开放银行平台，向第三方金融科技公司（TPP）提供账户信息、支付发起与信贷预审批服务。各成员银行的核心系统异构：2 家使用某国际核心银行系统，2 家使用国产核心系统，1 家为自研核心。

### 13.2 关键决策

| 决策点 | 选项 | 最终决策 | 决策依据 |
|---|---|---|---|
| 业务能力基线 | 自建术语体系 vs. 采用 BIAN | 采用 BIAN Service Landscape 12.0 作为基线，关注 14.0 新增 AI/支付服务域 | 降低跨银行语义协商成本；BIAN 14.0 强化了 ISO 20022 对齐与 AI 服务域 |
| 服务域粒度 | 机械照搬 300+ 服务域 vs. 聚焦高价值域 | 首批聚焦 18 个服务域：客户信息管理、账户管理、支付发起、支付执行、信用风险评估、KYC | 优先覆盖开放银行 MVP 价值链；避免一次性重构全部遗留系统 |
| 遗留系统适配 | 全面替换 vs. Facade 适配 | Facade 适配：核心系统保留，开放 API 层按 BIAN 语义暴露 | 控制风险和预算；符合 BIAN"规范可复用、实现可本地化"边界 |
| 报文标准 | 专有 JSON vs. ISO 20022 | 开放 API 采用 ISO 20022 JSON/API 格式，内部保留 BIAN 语义映射层 | 确保与区域支付生态、SWIFT gpi 互操作 |
| 决策规则 | 硬编码在流程中 vs. DMN 决策服务 | 信用预审批、反欺诈评分采用 DMN 1.5 决策服务 | 业务人员可直接调整规则；支持 A/B 测试与监管解释 |

### 13.3 实施路径

**第一阶段（0-6 个月）：基线建立**

- 建立 BIAN-业务能力-价值流-IT 系统四层映射库。
- 选定 3 个试点服务域：客户信息管理、支付发起、账户管理。
- 与遗留核心系统团队共同设计 Facade 接口。

**第二阶段（6-12 个月）：平台构建**

- 部署 BIAN 语义 API 网关，统一对外开放接口。
- 集成 DMN 决策引擎，实现信用预审批与反欺诈规则。
- 引入 Pact 契约测试，确保跨银行接口语义一致。

**第三阶段（12-18 个月）：生态运营**

- 向 TPP 发布开发者门户与沙箱环境。
- 建立服务域 Owner 制度与语义化版本控制。
- 基于使用数据持续优化服务域边界。

### 13.4 量化结果

| 指标 | 复用前（估算） | 复用后 | 说明 |
|---|---|---|---|
| 与 TPP 集成周期 | 4-6 个月/家 | 2-3 周/家 | BIAN 标准化接口减少定制开发 |
| 新市场支付产品上线 | 9-12 个月 | 3-4 个月 | 复用支付发起/执行服务域 |
| 监管报告生成时间 | 2-3 周 | 2-3 天 | KYC/账户信息数据语义统一 |
| 跨银行数据一致性错误 | 月均 15 起 | 月均 3 起 | 统一 Customer Profile / Payment Order 语义 |
| 三年总拥有成本 | 基准 100% | 约 65% | 避免 5 家银行分别建设开放银行平台 |

### 13.5 教训总结

1. **不要在没有映射的情况下引入 BIAN**：若仅将 BIAN 目录导入架构库而不与现有系统、项目、能力地图建立映射，目录会迅速沦为"标准陈列馆"。
2. **服务域不等于微服务**：一个 BIAN 服务域可由多个微服务实现，一个微服务也可实现多个服务域。初期过度拆分会导致分布式事务和运维复杂度激增。
3. **语义一致比接口格式一致更重要**：两家银行即使都使用 REST/JSON，若对"收款人""受益人"等概念理解不同，仍会导致资金路由错误。
4. **治理必须同步建设**：只复用规范不复用治理（Owner、版本、影响分析）会导致接口频繁破坏性变更，复用计划名存实亡。

## 14. 标准条款映射

| 本主题概念 | 对应标准条款 | 映射说明 |
|:---|:---|:---|
| BIAN 服务域 | BIAN Service Landscape 12.0/14.0 Service Domain | 银行业务能力的标准化原子单元，包含业务对象、行为、信息交换规范 |
| 架构构建块（ABB） | TOGAF 10 Phase B/C | BIAN 服务域作为银行业的 ABB，TOGAF ADM 提供管理方法论 |
| 金融报文语义 | ISO 20022 pain.001 / pacs.008 / camt.053 | BIAN Payment Order / Payment Execution 与 ISO 20022 报文元素映射 |
| 可执行决策 | DMN 1.5 §6 Decision Service | 信贷审批、反欺诈评分等决策逻辑封装为可复用决策服务 |
| 可执行流程 | BPMN 2.0 §8 Process, §10 Collaboration | 客户开户、支付执行等价值流由 BPMN 流程编排 |
| 企业架构分类 | Zachman Framework C2-1/C2-2/C3-2 | BIAN 服务域映射到业务视角 What/How 与系统视角 How |

## 附录：权威来源

| 序号 | 来源 | URL | 核查日期 |
|:---|:---|:---|:---|
| 1 | BIAN (Banking Industry Architecture Network) 官方网站 | <https://bian.org/> | 2026-07-08 |
| 2 | BIAN Service Landscape 12.0/14.0 官方文档 | <https://bian.org/bian-library/> | 2026-07-08 |
| 3 | BIAN 服务域详细规范与 API 定义 | <https://bian.org/servicelandscape/> | 2026-07-08 |
| 4 | BIAN Service Landscape 14.0 发布新闻（2026-05） | <https://bian.org/news-room/bian-unveils-new-service-landscape-14-0-to-accelerate-ai-ready-banking-architecture/> | 2026-07-08 |
| 5 | TOGAF 10 标准文档（The Open Group） | <https://www.opengroup.org/togaf> | 2026-07-08 |
| 6 | FEA Framework 6.0（美国联邦企业架构框架） | <https://obamawhitehouse.archives.gov/omb/e-gov/fea> | 2026-07-08 |
| 7 | ISO 20022 金融报文标准官方站点 | <https://www.iso20022.org/> | 2026-07-08 |
| 8 | DMN 1.5 规范（Object Management Group） | <https://www.omg.org/spec/DMN/1.5/> | 2026-07-08 |
| 9 | BPMN 2.0.2 规范（Object Management Group） | <https://www.omg.org/spec/BPMN/2.0.2/> | 2026-07-08 |
| 10 | BIAN 与 ISO 20022 映射指南 | <https://bian.org/iso-20022/> | 2026-07-08 |
| 11 | SWIFT 官方：ISO 20022 迁移资源中心 | <https://www.swift.com/standards/iso-20022> | 2026-07-08 |
| 12 | Camunda DMN/BPMN 引擎文档（开源参考实现） | <https://docs.camunda.org/> | 2026-07-08 |
| 13 | 欧洲银行管理局（EBA）PSD2 技术要求指南 | <https://www.eba.europa.eu/regulation-and-policy/payment-services-and-electronic-money/regulation-payment-services-psd-2> | 2026-07-08 |

---


<!-- SOURCE: struct/02-business-architecture-reuse/case-studies/industry-vertical-cases.md -->

# 行业垂直场景案例库

> **版本**: 2026-06-06
> **定位**: 业务架构层复用实践——金融、医疗、制造三大行业的业务能力复用案例
> **权威来源**:
>
> - BIAN (Banking Industry Architecture Network) Service Landscape 2026
> - HL7 FHIR R5 (Healthcare Level Seven)
> - ISA-95 / IEC 62264 (制造领域)
> - TOGAF Standard 10 Phase B (Business Architecture)

---

## 目录

- [行业垂直场景案例库](#行业垂直场景案例库)
  - [目录](#目录)
  - [案例 1：金融 — 开放银行核心能力复用](#案例-1金融--开放银行核心能力复用)
    - [1.1 业务背景](#11-业务背景)
    - [1.2 业务能力分层（基于 BIAN）](#12-业务能力分层基于-bian)
    - [1.3 价值流：客户贷款申请](#13-价值流客户贷款申请)
    - [1.4 复用资产清单](#14-复用资产清单)
    - [1.5 关键洞察](#15-关键洞察)
  - [案例 2：医疗 — 临床路径与 FHIR 资源复用](#案例-2医疗--临床路径与-fhir-资源复用)
    - [2.1 业务背景](#21-业务背景)
    - [2.2 业务能力分层（基于 HL7 FHIR）](#22-业务能力分层基于-hl7-fhir)
    - [2.3 价值流：糖尿病患者管理](#23-价值流糖尿病患者管理)
    - [2.4 复用资产清单](#24-复用资产清单)
    - [2.5 关键洞察](#25-关键洞察)
  - [案例 3：制造 — 智能工厂价值流复用](#案例-3制造--智能工厂价值流复用)
    - [3.1 业务背景](#31-业务背景)
    - [3.2 业务能力分层（基于 ISA-95）](#32-业务能力分层基于-isa-95)
    - [3.3 价值流：按订单生产 (MTO)](#33-价值流按订单生产-mto)
    - [3.4 复用资产清单](#34-复用资产清单)
    - [3.5 关键洞察](#35-关键洞察)
  - [跨行业复用对比](#跨行业复用对比)
  - [补充说明：行业垂直场景案例库](#补充说明行业垂直场景案例库)
  - [概念定义](#概念定义)
  - [反例](#反例)

---

## 案例 1：金融 — 开放银行核心能力复用

### 1.1 业务背景

开放银行（Open Banking）要求银行通过标准化 API 向第三方开放账户、支付、信贷等核心能力。
这本质上是一种**业务能力的外部化复用**。

### 1.2 业务能力分层（基于 BIAN）

| 层级 | 能力名称 | BIAN 服务域 | 复用策略 |
|------|---------|------------|---------|
| **L1 业务域** | 零售银行业务 | Retail Banking | 跨渠道统一 |
| **L2 能力组** | 支付管理 | Payment Execution | 标准化 API |
| **L3 子能力** | 即时支付 | Immediate Payment | ISO 20022 消息标准 |
| **L4 流程** | 支付指令验证 | Payment Instruction Validation | 规则引擎复用 |
| **L5 服务** | SEPA Instant API | SEPA Credit Transfer | PSD2 合规封装 |

### 1.3 价值流：客户贷款申请

```mermaid
flowchart LR
    A[客户申请] --> B[身份验证]
    B --> C[信用评估]
    C --> D[利率定价]
    D --> E[合同生成]
    E --> F[资金拨付]

    style C fill:#e1f5e1
    style D fill:#e1f5e1
```

**复用点**（绿色标注）：

- **信用评估**：复用央行征信 + 内部评分模型（标准化评估服务）
- **利率定价**：复用风险定价引擎（基于客户画像动态定价）

### 1.4 复用资产清单

| 资产类型 | 资产名称 | 复用范围 | 标准/规范 |
|---------|---------|---------|----------|
| 业务能力 | 客户身份验证 (KYC) | 全渠道复用 | eIDAS / FATF |
| 业务流程 | 反洗钱 (AML) 检查流程 | 所有交易场景 | FATF 40 项建议 |
| 业务服务 | SEPA 即时支付 API | 欧盟区银行互操作 | PSD2 / ISO 20022 |
| 决策表 | 信贷审批决策矩阵 | 零售/对公贷款 | Basel III/IV |

### 1.5 关键洞察

> **金融复用公理**: 银行业务能力的可复用性与其**监管标准化程度**正相关。支付（SEPA）> 信贷（Basel）> 财富管理（高度定制）。

---

## 案例 2：医疗 — 临床路径与 FHIR 资源复用

### 2.1 业务背景

医疗信息化的核心挑战是如何在保护患者隐私的前提下，实现临床数据和治疗路径的跨机构复用。
HL7 FHIR (Fast Healthcare Interoperability Resources) 提供了标准化的数据资源模型。

### 2.2 业务能力分层（基于 HL7 FHIR）

| 层级 | 能力名称 | FHIR 资源 | 复用策略 |
|------|---------|----------|---------|
| **L1 业务域** | 临床诊疗 | Clinical Care | 跨机构互操作 |
| **L2 能力组** | 患者管理 | Patient Administration | 主数据管理 (EMPI) |
| **L3 子能力** | 诊断管理 | Diagnostic Process | FHIR DiagnosticReport |
| **L4 流程** | 临床路径执行 | Clinical Pathway | BPMN + FHIR 组合 |
| **L5 服务** | 检验报告查询 | Lab Report API | FHIR Observation |

### 2.3 价值流：糖尿病患者管理

```mermaid
flowchart LR
    A[患者注册] --> B[初诊评估]
    B --> C[血糖监测计划]
    C --> D[用药方案]
    D --> E[随访提醒]
    E --> F[并发症筛查]
    F --> G[疗效评估]
    G -->|需调整| D

    style B fill:#e1f5e1
    style D fill:#e1f5e1
    style F fill:#e1f5e1
```

**复用点**：

- **初诊评估**：复用标准化糖尿病风险评估问卷 (ADA 标准)
- **用药方案**：复用临床决策支持系统 (CDSS) 的药物相互作用检查
- **并发症筛查**：复用眼底筛查、肾功能检查的标准化路径

### 2.4 复用资产清单

| 资产类型 | 资产名称 | 复用范围 | 标准/规范 |
|---------|---------|---------|----------|
| 数据资源 | FHIR Patient | 全院/区域共享 | HL7 FHIR R5 |
| 数据资源 | FHIR Observation (血糖) | 跨科室互操作 | LOINC 编码 |
| 临床路径 | 2型糖尿病管理路径 | 内分泌科标准化 | ADA / CDSG |
| 决策表 | 胰岛素剂量调整规则 | 住院/门诊通用 | 医院药事委员会 |
| 业务服务 | 检验报告查询 API | 区域健康信息平台 | IHE MHD Profile |

### 2.5 关键洞察

> **医疗复用公理**: 医疗业务能力的复用受**临床变异性**和**隐私合规**双重约束。
> 数据资源（FHIR）的复用性 > 临床路径（需适配）> 诊疗决策（高度个体化）。

---

## 案例 3：制造 — 智能工厂价值流复用

### 3.1 业务背景

智能制造将传统工厂转变为数据驱动的生产系统。
ISA-95 标准提供了企业-控制系统集成的五层模型，是制造领域业务能力复用的核心框架。

### 3.2 业务能力分层（基于 ISA-95）

| 层级 | 能力名称 | ISA-95 对应 | 复用策略 |
|------|---------|------------|---------|
| **L1 业务域** | 智能制造 | Smart Manufacturing | 跨工厂复制 |
| **L2 能力组** | 生产执行 | Manufacturing Operations | MES 系统标准化 |
| **L3 子能力** | 工单管理 | Production Scheduling | ISA-95 作业单模型 |
| **L4 流程** | 物料齐套检查 | Material Checking | BPMN + ISA-95 映射 |
| **L5 服务** | 设备 OEE 查询 | OEE API | OPC UA 信息模型 |

### 3.3 价值流：按订单生产 (MTO)

```mermaid
flowchart LR
    A[客户订单] --> B[产能检查]
    B --> C[物料齐套]
    C --> D[生产排程]
    D --> E[工单执行]
    E --> F[质量检验]
    F --> G[入库发货]

    style B fill:#e1f5e1
    style C fill:#e1f5e1
    style F fill:#e1f5e1
```

**复用点**：

- **产能检查**：复用 APS (高级计划排程) 引擎的产能模型
- **物料齐套**：复用 ERP 的 BOM 展开 + 库存检查逻辑
- **质量检验**：复用 SPC (统计过程控制) 规则和检验模板

### 3.4 复用资产清单

| 资产类型 | 资产名称 | 复用范围 | 标准/规范 |
|---------|---------|---------|----------|
| 业务能力 | 生产调度 | 全工厂复用 | ISA-95 第 3 部分 |
| 业务流程 | 不合格品处理流程 | 所有生产线 | ISO 9001 |
| 业务规则 | SPC 控制限规则 | 跨产品线 | ISO 22514 |
| 数据模型 | 产品主数据 (物料/工艺) | 企业级 | IEC 62264 |
| 业务服务 | 设备状态查询 API | 车间级 | OPC UA Companion Spec |

### 3.5 关键洞察

> **制造复用公理**: 制造业务能力的复用与**产品相似度**和**工艺标准化程度**正相关。
> 标准件生产（汽车/电子）> 定制件（航空/重工）> 单件（船舶/大型装备）。

---

## 跨行业复用对比

| 维度 | 金融 (开放银行) | 医疗 (智慧医院) | 制造 (智能工厂) |
|------|----------------|----------------|----------------|
| **核心驱动力** | 监管合规 (PSD2) | 患者安全 + 互操作 | 效率 + 质量 |
| **标准化程度** | 极高 (ISO 20022) | 高 (FHIR/HL7) | 中-高 (ISA-95) |
| **复用主要层次** | L5 业务服务 | L4 数据资源 + L5 服务 | L3 子能力 + L4 流程 |
| **最大约束** | 数据隐私 + 反洗钱 | 患者隐私 (HIPAA/GDPR) | OT 确定性 + 安全 |
| **复用成熟度** | ★★★★★ | ★★★★☆ | ★★★☆☆ |
| **跨行业可迁移性** | 支付能力 → 电商/物流 | 临床路径 → 康养/保险 | 排程能力 → 能源/交通 |

---

> **对齐验证**:
>
> - BIAN 内容对照 [bian.org](https://bian.org) Service Landscape 2026 验证
> - FHIR 内容对照 [hl7.org/fhir](https://hl7.org/fhir/R5/) R5 验证
> - ISA-95 内容对照 IEC 62264 官方标准验证
>
> 最后更新: 2026-06-06


---

## 补充说明：行业垂直场景案例库

## 概念定义

**定义**：行业垂直案例是从特定行业（金融、电信、医疗、制造等）提炼的可复用业务架构模式与实施经验。

## 反例

**反例**：将互联网电商的推荐模型直接复制到医疗设备采购场景，忽视行业合规与决策链差异，导致系统不可用。

---


<!-- SOURCE: struct/02-business-architecture-reuse/case-studies/tmforum-telecom-reuse.md -->

# C-06 TMForum ODF / eTOM 电信架构复用

| 属性 | 内容 |
|------|------|
| **版本** | 2026-06-10 |
| **定位** | Phase C — 业务架构复用 — 电信行业案例研究 |
| **对齐标准** | TMForum ODF（Open Digital Framework）、eTOM（Enhanced Telecom Operations Map）、SID（Shared Information/Data Model）、ODA（Open Digital Architecture）、CAMARA |
| **状态** | ✅ 已完成 |

---

## 目录

- [C-06 TMForum ODF / eTOM 电信架构复用](#c-06-tmforum-odf--etom-电信架构复用)
  - [目录](#目录)
  - [1. TMForum 概述](#1-tmforum-概述)
    - [1.1 电信管理论坛（TMForum）](#11-电信管理论坛tmforum)
    - [1.2 ODF（Open Digital Framework）](#12-odfopen-digital-framework)
    - [1.3 eTOM（Enhanced Telecom Operations Map）](#13-etomenhanced-telecom-operations-map)
  - [2. eTOM 业务过程框架 L1-L3](#2-etom-业务过程框架-l1-l3)
    - [2.1 L0 与 L1 层：三大过程域](#21-l0-与-l1-层三大过程域)
    - [2.2 L2 层：过程组细分](#22-l2-层过程组细分)
    - [2.3 L3 层：核心过程与复用点](#23-l3-层核心过程与复用点)
  - [3. SID（Shared Information/Data Model）](#3-sidshared-informationdata-model)
    - [3.1 SID 的核心定位](#31-sid-的核心定位)
    - [3.2 SID 的领域划分](#32-sid-的领域划分)
    - [3.3 SID 作为复用核心](#33-sid-作为复用核心)
    - [3.4 SID 与数据治理](#34-sid-与数据治理)
  - [4. ODA（Open Digital Architecture）](#4-odaopen-digital-architecture)
    - [4.1 ODA 的演进背景](#41-oda-的演进背景)
    - [4.2 ODA 的核心原则](#42-oda-的核心原则)
    - [4.3 ODA 的功能架构](#43-oda-的功能架构)
    - [4.4 ODA 的复用机制](#44-oda-的复用机制)
  - [5. 电信行业的复用特征](#5-电信行业的复用特征)
    - [5.1 5G 网络切片模板复用](#51-5g-网络切片模板复用)
    - [5.2 BSS / OSS 微服务复用](#52-bss--oss-微服务复用)
    - [5.3 Open API（CAMARA）标准化](#53-open-apicamara标准化)
  - [6. eTOM 与 TOGAF / BIAN 的映射对照](#6-etom-与-togaf--bian-的映射对照)
    - [6.1 eTOM 与 TOGAF 的映射](#61-etom-与-togaf-的映射)
    - [6.2 eTOM 与 BIAN 的映射](#62-etom-与-bian-的映射)
    - [6.3 多框架融合的实践建议](#63-多框架融合的实践建议)
  - [7. 案例：电信运营商的数字化复用平台](#7-案例电信运营商的数字化复用平台)
    - [7.1 Vodafone 的共享服务架构](#71-vodafone-的共享服务架构)
    - [7.2 O2（Telefónica UK）的 API-First 复用实践](#72-o2telefónica-uk的-api-first-复用实践)
    - [7.3 中国电信的"云改数转"复用平台](#73-中国电信的云改数转复用平台)
  - [8. 参考文献与权威来源](#8-参考文献与权威来源)
  - [补充说明：C-06 TMForum ODF / eTOM 电信架构复用](#补充说明c-06-tmforum-odf--etom-电信架构复用)
  - [概念定义](#概念定义)
  - [反例](#反例)
  - [分析](#分析)

---

## 1. TMForum 概述

### 1.1 电信管理论坛（TMForum）

TMForum（TeleManagement Forum，原称 TeleManagement Forum，现简称 TMForum）是全球电信行业最具影响力的标准化组织和行业协会，成立于 1988 年。TMForum 的成员涵盖全球超过 850 家通信服务提供商（CSP）、技术供应商、系统集成商和咨询公司，其使命是推动电信和数字服务行业的数字化转型和互操作性。

TMForum 的核心价值主张是：通过开放的数字框架、标准化的业务流程和信息模型，降低电信行业数字化转型的复杂度和成本，加速新服务的上市时间（Time-to-Market）。

### 1.2 ODF（Open Digital Framework）

ODF 是 TMForum 在 2019 年推出的综合性数字化转型框架，整合了 TMForum 二十多年来积累的全部标准资产。ODF 不是单一标准，而是一个相互关联的标准组合，旨在为通信服务提供商提供从战略到落地的完整数字化转型蓝图。

ODF 的核心组成包括：

- **eTOM（Enhanced Telecom Operations Map）**：业务过程框架，定义电信行业的标准业务流程。
- **SID（Shared Information/Data Model）**：共享信息/数据模型，提供跨系统的统一数据语义。
- **TAM（Telecom Application Map）**：电信应用地图，定义支撑业务流程的标准应用组件。
- **ODA（Open Digital Architecture）**：开放数字架构，定义云原生、API-first 的电信技术架构。
- **Open APIs**：标准化 API 集，支持不同供应商系统之间的即插即用集成。
- **Catalyst Program**：联合创新项目，验证新技术和业务模式的可行性。

ODF 的设计理念强调"模块化、可复用、可组合"——电信企业可以从 ODF 中选取适合自身发展阶段的标准模块，而非全盘照搬。

### 1.3 eTOM（Enhanced Telecom Operations Map）

eTOM 是 TMForum 最成熟、应用最广泛的标准，其历史可以追溯到 2000 年发布的 TOM（Telecom Operations Map）。eTOM 在 TOM 的基础上扩展了战略和企业管理维度，形成了覆盖电信企业全部业务活动的完整过程框架。

eTOM 的核心价值在于：

- **流程标准化**：为电信行业提供统一的语言和参考模型，使不同企业、不同系统之间的流程对标成为可能。
- **互操作基础**：基于 eTOM 的流程划分，可以设计标准化的系统接口和数据交换规范。
- **组织变革指导**：eTOM 的层级结构为电信企业的组织设计和职能划分提供参考。
- **采购与评估基准**：电信运营商在采购 BSS/OSS 系统时，常以 eTOM 覆盖度作为评估标准。

---

## 2. eTOM 业务过程框架 L1-L3

eTOM 采用分层的过程分解结构，从 L0（最高层）到 L5+（最细粒度），每一层都是对上一层的细化。以下重点介绍 L1 到 L3 的核心内容。

### 2.1 L0 与 L1 层：三大过程域

eTOM L0 将整个电信企业的业务活动划分为三大核心过程域（Level 1）：

| L1 过程域 | 英文名称 | 核心内容 |
|-----------|----------|----------|
| **战略、基础设施与产品** | Strategy, Infrastructure & Product（SIP） | 规划、生命周期管理、供应链管理 |
| **运营** | Operations（OPS） | 日常服务交付、客户支撑、资源运维 |
| **企业管理** | Enterprise Management（EM） | 财务、人力资源、法务、品牌等企业支撑职能 |

这三大过程域构成了电信企业的"价值创造全景"：SIP 负责"设计正确的事"，OPS 负责"正确地做事"，EM 负责"保障做事的能力"。

### 2.2 L2 层：过程组细分

在 L1 的基础上，eTOM 进一步将每个过程域分解为多个过程组（Level 2）：

**SIP 域的 L2 过程组**：

- **战略与承诺（Strategy & Commit, 1.1）**：企业战略规划、市场分析、投资决策。
- **基础设施生命周期管理（Infrastructure Lifecycle Management, 1.2）**：网络规划、建设、优化和退役。
- **产品生命周期管理（Product Lifecycle Management, 1.3）**：产品设计、定价、发布和退市。
- **营销/供应方开发管理（Marketing/Supply-Side Development, 1.4）**：合作伙伴管理、内容采购、渠道建设。

**OPS 域的 L2 过程组**：

- **客户关系管理（Customer Relationship Management, 2.1）**：销售、订单处理、客户服务、计费账务。
- **服务管理与运营（Service Management & Operations, 2.2）**：服务保障、服务配置、服务问题管理。
- **资源管理与运营（Resource Management & Operations, 2.3）**：网络资源调度、资源故障管理、资源性能监控。
- **供应商/合作伙伴关系管理（Supplier/Partner Relationship Management, 2.4）**：外包管理、SLA 监控、结算对账。

**EM 域的 L2 过程组**：

- **企业战略管理（Strategic Enterprise Management, 3.1）**
- **企业风险管理（Enterprise Risk Management, 3.2）**
- **企业财务管理（Enterprise Financial Management, 3.3）**
- **企业人力资源/资产/知识管理（HR/Asset/Knowledge, 3.4-3.6）**

### 2.3 L3 层：核心过程与复用点

L3 层是 eTOM 最具实操价值的层级，定义了可识别、可度量的核心业务流程。以下列举部分高复用价值的 L3 过程：

**高复用 L3 过程示例（CRM 域）**：

- **2.1.1 营销与获客管理（Marketing & Offer Management）**：客户细分、营销活动管理、产品推荐引擎。
- **2.1.2 销售与渠道管理（Selling & Channel Management）**：订单捕获、渠道佣金管理、销售漏斗分析。
- **2.1.3 订单处理（Order Handling）**：订单编排（Order Orchestration）、库存校验、服务开通。
- **2.1.4 问题处理（Problem Handling）**：工单管理、投诉升级、根因分析。
- **2.1.5 客户 QoS / SLA 管理（Customer QoS/SLA Management）**：服务质量监控、 SLA 违约判定、赔偿计算。
- **2.1.6 计费与账务管理（Billing & Account Management）**：计费引擎、账务周期、支付处理、信用管控。

**高复用 L3 过程示例（服务与资源域）**：

- **2.2.2 服务配置与激活（Service Configuration & Activation）**：服务编排、参数下发、端到端开通。
- **2.2.3 服务保障（Service Assurance）**：故障关联、影响分析、自动恢复。
- **2.3.2 资源配置与分配（Resource Provisioning & Allocation）**：网络切片分配、频谱管理、IP 地址分配。
- **2.3.3 资源性能管理（Resource Performance Management）**：KPI 采集、性能劣化预警、容量规划。

L3 过程的复用价值在于：它们定义了"做什么"而非"怎么做"，使得不同运营商可以在相同的过程框架下，采用不同的技术实现路径。

---

## 3. SID（Shared Information/Data Model）

### 3.1 SID 的核心定位

SID 是 TMForum 定义的共享信息/数据模型，是 eTOM 流程框架的数据基础。如果说 eTOM 回答了"电信企业有哪些业务流程"，那么 SID 回答的就是"这些流程处理哪些数据、数据之间是什么关系"。

SID 的设计目标包括：

- **打破信息孤岛**：为 BSS（业务支撑系统）和 OSS（运营支撑系统）提供统一的数据语义。
- **支持系统集成**：基于 SID 可以设计标准化的系统接口，降低异构系统集成的复杂度。
- **加速应用开发**：为软件供应商提供参考数据模型，减少重复的数据建模工作。
- **支撑业务分析**：统一的数据模型使得跨系统的数据分析和报表生成更加可靠。

### 3.2 SID 的领域划分

SID 采用面向对象的方法，将电信企业的信息划分为多个主题领域（Domain），每个领域包含一组相关的业务实体（Business Entity）：

| SID 主题领域 | 核心实体示例 | 复用价值 |
|-------------|-------------|----------|
| **客户域（Customer）** | 客户、账户、联系人、客户细分、偏好 | 360 度客户视图、客户数据平台（CDP） |
| **产品域（Product）** | 产品规格、产品提供、产品目录、定价 | 产品配置器、报价引擎、订单编排 |
| **服务域（Service）** | 服务规格、服务实例、服务拓扑、SLA | 服务保障、服务编排、服务目录 |
| **资源域（Resource）** | 物理资源、逻辑资源、网络拓扑、容量 | 资源管理、网络库存、容量规划 |
| **参与方域（Party）** | 员工、合作伙伴、供应商、角色 | 合作伙伴管理、权限控制 |
| **位置域（Location）** | 地址、地理区域、站点、覆盖范围 | 地址验证、覆盖分析、资源定位 |

### 3.3 SID 作为复用核心

SID 在电信行业架构复用中的核心地位体现在以下方面：

- **数据模型复用**：SID 的实体定义和关系模型可以直接作为企业数据仓库、主数据管理（MDM）系统的逻辑模型基础。
- **API 设计复用**：TMForum Open API 的设计直接基于 SID 实体，使得不同供应商的系统可以通过标准化 API 进行数据交换。
- **映射标准复用**：SID 提供了与其他行业标准（如 3GPP、ITU-T、IEEE）的映射指南，支持跨标准的数据对齐。
- **行业扩展复用**：SID 的框架不仅适用于传统电信，还被扩展应用于物联网（IoT）、云服务和数字平台经济。

### 3.4 SID 与数据治理

在电信企业的数据治理实践中，SID 通常被用作：

- **数据目录的分类框架**：企业数据资产按照 SID 主题领域进行编目和分类。
- **数据质量规则的参照基准**：基于 SID 实体的属性定义制定数据质量校验规则。
- **数据共享协议的语义基础**：不同部门或子公司之间的数据共享协议以 SID 实体为最小交换单元。

---

## 4. ODA（Open Digital Architecture）

### 4.1 ODA 的演进背景

ODA 是 TMForum 于 2020 年前后正式推出的新一代电信架构框架，是对传统 BSS/OSS 架构的彻底重构。ODA 的推出背景包括：

- **云原生转型需求**：传统单体式的 BSS/OSS 系统难以支撑电信业务的敏捷迭代和弹性扩展。
- **5G 网络切片驱动**：5G 的网络切片能力要求 BSS/OSS 具备分钟级的业务开通和配置能力。
- **IT/CT 融合趋势**：电信网络功能（CNF/VNF）与 IT 应用的边界日益模糊，需要统一的架构范式。
- **开放生态诉求**：电信运营商希望打破传统设备供应商的锁定，构建开放的数字化生态。

### 4.2 ODA 的核心原则

ODA 定义了电信行业数字化架构的六项核心原则：

1. **云原生（Cloud-Native）**：所有功能组件以微服务形式部署在容器化云平台上，支持自动扩缩容和故障自愈。
2. **API-First**：组件之间的所有交互通过标准化 API 完成，API 设计优先于内部实现。
3. **组件化与可编排（Componentized & Orchestrated）**：功能被拆分为细粒度的业务组件，通过编排引擎动态组合成完整业务流程。
4. **数据驱动（Data-Driven）**：架构内置数据分析和 AI/ML 能力，支持实时决策和自动化运营。
5. **开放与互操作（Open & Interoperable）**：基于开放标准和开源技术，支持多供应商环境的即插即用。
6. **客户为中心（Customer-Centric）**：架构设计围绕客户旅程而非内部系统边界展开。

### 4.3 ODA 的功能架构

ODA 将电信企业的数字化能力划分为以下核心功能域：

- **参与方管理（Party Management）**：客户、合作伙伴、员工的统一管理。
- **产品管理（Production Management）**：产品目录、配置、定价和生命周期管理。
- **订单管理（Order Management）**：订单编排、分解、跟踪和闭环。
- **服务管理与编排（Service Management & Orchestration）**：服务设计与实例化、服务保障、服务问题管理。
- **资源管理与编排（Resource Management & Orchestration）**：物理和虚拟资源的发现、分配、配置和监控。
- **计费与收入管理（Billing & Revenue Management）**：计费、账务、支付、收入保障。
- **客户互动管理（Customer Engagement Management）**：全渠道客户交互、营销自动化、客户体验管理。
- **智能运营（Intelligent Operations）**：AI 驱动的预测性运维、根因分析、自动化决策。

### 4.4 ODA 的复用机制

ODA 的设计天然支持复用：

- **微服务组件库**：TMForum 维护 ODA 组件目录，运营商和供应商可以基于目录开发可互替换的组件。
- **Open API 目录**：TMForum 定义了超过 50 组标准化 Open API，覆盖核心业务流程的交互点。
- **蓝图（Blueprint）复用**：TMForum 发布针对不同业务场景（如 5G 切片开通、IoT 平台运营）的 ODA 蓝图，企业可以基于蓝图快速搭建系统架构。

---

## 5. 电信行业的复用特征

### 5.1 5G 网络切片模板复用

5G 网络切片是电信行业架构复用的典型场景。网络切片允许在同一物理网络基础设施上创建多个逻辑隔离的虚拟网络，每个切片针对不同应用场景（如 eMBB、uRLLC、mMTC）进行优化。

- **切片模板复用**：运营商预先定义标准化的切片模板（Slice Template），包含 QoS 参数、网络功能拓扑、资源配额等。当企业客户申请切片时，只需选择模板并调整少数参数即可快速开通。
- **切片蓝图复用**：TMForum 的 ODA 蓝图定义了端到端切片编排的标准流程，不同运营商可以基于同一蓝图实现切片业务。
- **切片即服务（Slicing as a Service）**：通过将切片能力封装为标准化 API，运营商可以向垂直行业（智能制造、自动驾驶、远程医疗）提供可复用的网络切片服务。

### 5.2 BSS / OSS 微服务复用

云原生转型推动电信 BSS/OSS 从单体架构向微服务架构演进，带来了新的复用模式：

- **共享微服务层**：在多个 BSS/OSS 应用之间共享通用微服务，如客户画像服务、地址验证服务、支付网关服务、通知推送服务等。
- **可组合的业务能力**：将传统的大型系统拆分为可独立部署和复用的业务能力（Business Capability），如"信用评估能力"可以被 CRM、计费、风控等多个系统复用。
- **供应商组件互替**：基于 TMForum Open API 和 ODA 组件标准，运营商可以在不改动上层应用的情况下，替换底层供应商组件。

### 5.3 Open API（CAMARA）标准化

CAMARA 是 GSMA 和 TMForum 联合推动的电信 API 开放标准化项目，旨在将运营商的网络能力（如 QoD、设备位置、号码验证、SIM 交换检测）封装为标准化 API，供开发者 ecosystem 使用。

- **API 定义复用**：CAMARA 定义统一的 API 规范，全球运营商可以基于同一规范暴露网络能力，开发者无需为每个运营商重写集成代码。
- **沙箱与测试工具复用**：CAMARA 提供标准化的 API 测试工具和沙箱环境，可以被所有参与者复用。
- **计费和商业模型复用**：CAMARA 配套的计费事件模型和商业模式模板可以在不同运营商之间复用。

---

## 6. eTOM 与 TOGAF / BIAN 的映射对照

电信行业架构师在实际工作中，常常需要将 TMForum 标准与企业架构框架（如 TOGAF）和行业特定标准（如 BIAN）进行对照和映射。

### 6.1 eTOM 与 TOGAF 的映射

| 映射维度 | TOGAF ADM | eTOM / TMForum |
|----------|-----------|----------------|
| **架构开发方法** | ADM 阶段 A-H 的迭代过程 | ODF 的 Catalyst 创新流程和 ODA 蓝图设计 |
| **业务架构** | Business Architecture（阶段 B） | eTOM L1-L3 业务流程框架 |
| **数据架构** | Data Architecture（阶段 C） | SID 共享信息模型 |
| **应用架构** | Application Architecture（阶段 C） | TAM 电信应用地图、ODA 功能架构 |
| **技术架构** | Technology Architecture（阶段 D） | ODA 云原生技术参考架构 |
| **架构能力** | Architecture Capability（预备阶段） | TMForum 成熟度评估模型（DIGITAL maturity model） |

**映射要点**：

- eTOM 的 L1 过程域可以与 TOGAF 的业务功能域（Business Function）直接映射。
- SID 的实体模型可以作为 TOGAF 数据架构中的数据实体（Data Entity）的细化参考。
- TMForum 的 Open API 规范可以映射为 TOGAF 应用架构中的接口规范（Interface Catalog）。

### 6.2 eTOM 与 BIAN 的映射

BIAN（Banking Industry Architecture Network）是银行业架构标准，与 TMForum 有类似的使命。eTOM 与 BIAN 的映射对于提供金融+电信融合服务（如移动支付、数字银行、嵌入式金融）尤为重要。

| eTOM 过程域 | BIAN 服务域 | 映射说明 |
|-------------|-------------|----------|
| 客户关系管理（2.1） | 客户档案管理（Customer Profile）、客户信息交换（Customer Information Exchange） | 客户主数据在两个框架间高度对应 |
| 订单处理（2.1.3） | 产品目录（Product Directory）、订单履行（Order Fulfilment） | 订单编排逻辑可以跨行业复用 |
| 计费与账务（2.1.6） | 支付执行（Payment Execution）、收款（Collections） | 计费引擎的核心算法通用性强 |
| 服务保障（2.2.2） | 服务问题管理（Service Problem）、客户案件管理（Customer Case） | 工单处理和问题升级机制类似 |
| 产品生命周期（1.3） | 产品设计（Product Design）、产品定价（Product Pricing） | 产品配置和定价规则可跨行业借鉴 |

**映射价值**：

- 对于同时运营电信和金融业务的企业集团（如中国移动的金融科技子公司、Orange Bank），eTOM-BIAN 映射支持跨行业的架构复用和系统整合。
- 对于提供嵌入式金融服务的电信运营商，BIAN 的服务域定义可以作为电信 BSS 扩展金融能力的参考模型。

### 6.3 多框架融合的实践建议

在大型企业架构实践中，建议采用"以场景为导向的框架融合"策略：

1. **识别主导框架**：根据企业的核心业务确定主导框架（电信运营商以 TMForum 为主，银行以 BIAN 为主）。
2. **建立映射矩阵**：在数据架构层建立跨框架的实体映射矩阵，确保语义一致性。
3. **共享通用组件**：在应用架构层识别跨行业通用的业务能力（如客户管理、订单处理、计费），基于主导框架开发，通过适配层暴露给其他框架。
4. **统一治理模型**：在架构治理层采用 TOGAF 的架构能力模型，但将 TMForum/BIAN 的成熟度评估纳入治理度量体系。

---

## 7. 案例：电信运营商的数字化复用平台

### 7.1 Vodafone 的共享服务架构

Vodafone 是全球领先的电信运营商之一，在数字化转型过程中构建了高度复用化的共享服务架构。

- **One Vodafone 战略**：Vodafone 提出"One Vodafone"战略，旨在通过共享的技术平台和业务能力，消除各国子公司的重复建设，实现规模经济。
- **共享数字平台（Shared Digital Platform）**：
  - **统一客户数据平台**：基于 TMForum SID 客户域模型，构建覆盖全球市场的统一客户画像系统，为营销、销售、客服提供共享的客户数据服务。
  - **统一产品目录**：建立全球统一的产品规格管理系统，各国子公司可以基于共享产品模板快速本地化上线新产品。
  - **统一订单编排引擎**：基于 eTOM 订单处理流程（2.1.3）和 ODA 编排原则，构建可复用的订单编排平台，支撑移动、固定、IoT、云服务的统一开通。
- **复用成效**：通过共享平台的建设，Vodafone 显著缩短了新产品的上市周期，降低了 IT 系统的重复投资，并提升了跨市场客户体验的一致性。

### 7.2 O2（Telefónica UK）的 API-First 复用实践

O2 是英国主要的移动运营商，其母公司 Telefónica 在全球范围内推进"API-First"战略。

- **Open Gateway 计划**：Telefónica 推出 Open Gateway 计划，将核心网络能力（如边缘计算、QoS、身份验证、设备位置）封装为标准化 CAMARA API，向全球开发者和企业客户开放。
- **内部 API 复用**：在内部系统建设中，O2 要求所有新开发系统必须通过标准化 API 暴露能力，禁止点对点集成。这使得业务能力可以在不同渠道（自营门店、电商网站、合作伙伴平台）间高度复用。
- **微服务市场**：O2 建立了内部微服务市场（Internal Microservices Marketplace），各开发团队可以将可复用的微服务注册到市场，其他团队可以直接发现和调用。
- **复用成效**：API-First 策略使得 O2 的系统集成成本大幅降低，新渠道上线周期从数月缩短至数周。

### 7.3 中国电信的"云改数转"复用平台

中国电信在"云改数转"战略下，建设了面向政企客户的数字化复用平台。

- **云网融合编排平台**：基于 TMForum ODA 服务与资源编排框架，构建云网一体化编排能力，实现云资源（天翼云）与网络资源（5G/专线）的统一开通和协同调度。
- **行业解决方案模板库**：针对政务、医疗、教育、工业等垂直行业，建立标准化的解决方案模板库，每个模板包含预配置的网络架构、云服务组合和应用组件，支持快速复制部署。
- **共享中台体系**：构建业务中台（客户中心、产品中心、订单中心）、数据中台（统一数据湖、AI 能力平台）和技术中台（云原生 PaaS、DevOps 工具链），为前端行业应用提供共享能力支撑。
- **复用成效**：中台化架构使得中国电信在面对政企客户定制化需求时，复用率显著提升，项目交付效率提高 40% 以上。

---

## 8. 参考文献与权威来源

| 编号 | 来源 | URL | 核查日期 |
|------|------|-----|----------|
| 1 | TMForum Open Digital Framework (ODF) Overview | <https://www.tmforum.org/oda/> | 2026-06-10 |
| 2 | TMForum eTOM Business Process Framework GB921 | <https://www.tmforum.org/resources/standard/gb921-etom-business-process-framework/> | 2026-06-10 |
| 3 | TMForum SID Shared Information/Data Model GB922 | <https://www.tmforum.org/resources/standard/gb922-shared-information-data-model/> | 2026-06-10 |
| 4 | TMForum ODA (Open Digital Architecture) | <https://www.tmforum.org/oda/> | 2026-06-10 |
| 5 | TMForum Open APIs | <https://www.tmforum.org/oda/apis/> | 2026-06-10 |
| 6 | CAMARA Project — Open Source APIs for Telecom Networks | <https://camaraproject.org/> | 2026-06-10 |
| 7 | Vodafone Annual Report & Digital Transformation Strategy | <https://www.vodafone.com/> | 2026-06-10 |
| 8 | Telefónica Open Gateway | <https://www.telefonica.com/en/> | 2026-06-10 |
| 9 | BIAN — Banking Industry Architecture Network | <https://www.bian.org/> | 2026-06-10 |
| 10 | The Open Group TOGAF Standard Version 10 | <https://www.opengroup.org/togaf> | 2026-06-10 |
| 11 | TMForum ODA Component Catalog | <https://www.tmforum.org/oda/components/> | 2026-06-10 |
| 12 | GSMA Operator Platform Requirements | <https://www.gsma.com/solutions-and-impact/technologies/networks/operator-platform/> | 2026-06-10 |
| 13 | TMForum Digital Maturity Model | <https://www.tmforum.org/maturity-and-assessments/> | 2026-06-10 |
| 14 | 中国电信"云改数转"战略白皮书 | <https://www.chinatelecom.com.cn/> | 2026-06-10 |
| 15 | 5G Network Slicing — 3GPP TS 28.530 | <https://www.3gpp.org/specifications/specifications> | 2026-06-10 |

---

*本文档为 Phase C 任务 C-06 交付物，归属于业务架构复用 — 电信行业案例研究工作流。*


---

## 补充说明：C-06 TMForum ODF / eTOM 电信架构复用

## 概念定义

**定义**：行业垂直案例是从特定行业（金融、电信、医疗、制造等）提炼的可复用业务架构模式与实施经验。

## 反例

**反例**：将互联网电商的推荐模型直接复制到医疗设备采购场景，忽视行业合规与决策链差异，导致系统不可用。

## 分析

**分析**：行业垂直案例是业务架构复用的最佳实践来源，但需结合本地上下文进行适配。

---


<!-- SOURCE: struct/02-business-architecture-reuse/README.md -->

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

---
