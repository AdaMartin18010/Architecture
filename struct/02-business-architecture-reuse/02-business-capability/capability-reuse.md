# 业务能力复用

> **版本**: 2026-06-06
> **定位**: 将业务能力作为业务架构复用的核心单元

---

## 1. 业务能力的本质

**定义 2.1** (Business Capability): 业务能力是企业为达成特定结果而具备的**稳定能力**。
它不依赖于具体的组织、流程、技术或实现。

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

> 最后更新: 2026-06-06


---

## 6. 业务能力复用的形式化定义与属性

### 6.1 概念定义

**定义**：业务能力复用（Business Capability Reuse）是指将企业中**稳定、通用、可度量**的业务能力单元作为可复用资产，在多个业务线、产品、流程或系统中共享其定义、行为、数据契约和价值度量，从而避免重复建设、加速业务创新并降低架构复杂度的实践。

形式化：

```text
CapabilityReuse(C) := ⟨C, M(C), V(C), Gov(C)⟩

C: 业务能力单元
M(C): C 的成熟度模型（Level 1-5）
V(C): C 的价值度量集合（成本节约、上市时间、质量提升）
Gov(C): C 的治理主体、生命周期与版本策略
```

### 6.2 业务能力复用核心属性

| 属性 | 说明 | 可观察指标 | 重要性 |
|---|---|---|---|
| 稳定性 | 能力边界和核心语义随时间变化的程度 | 过去 24 个月结构性变更次数 | 高 |
| 通用性 | 能力在多个业务上下文中的适用程度 | 使用业务线/系统数量 | 高 |
| 原子性 | 能力粒度的适中性 | 能力分解到子能力的层级数 | 高 |
| 价值可度量性 | 能力成果可被量化评估的程度 | KPI 覆盖率、ROI 可追溯性 | 高 |
| 独立性 | 能力实现与组织结构、技术栈解耦程度 | 组织变更时的影响范围 | 中 |
| 可组合性 | 能力与其他能力组合形成价值流的能力 | 接口契约标准化程度 | 中 |

### 6.3 业务能力成熟度模型

| 成熟度等级 | 特征 | 复用表现 |
|---|---|---|
| L1 初始级 | 能力以职能或项目形式存在，无统一目录 | 复用靠个人关系，无治理 |
| L2 已管理级 | 部门级能力地图建立，但跨部门不一致 | 部门内复用，跨部门重复建设 |
| L3 已定义级 | 企业级统一能力地图，与价值流、IT 服务映射 | 跨部门复用，有标准接口 |
| L4 量化管理级 | 能力有明确 KPI、成本、质量度量 | 基于数据决策复用投资 |
| L5 优化级 | 能力持续演进，驱动业务创新 | 能力资产化，可对外输出 |

### 6.4 与 TOGAF / FEA BRM 的映射

| 框架 | 对应概念 | 映射说明 |
|---|---|---|
| TOGAF 10 | Business Capability / Organization Unit / Function | 业务能力映射到 TOGAF 内容元模型中的 Business Capability，组织单元映射到 Organization Unit，功能函数映射到 Function |
| TOGAF ABB/SBB | 业务能力为 ABB，具体 IT 实现为 SBB | 业务能力定义"做什么"，SBB 定义"怎么做" |
| FEA BRM 2.0 | Line of Business / Sub-function | FEA BRM 的业务线与子功能可映射为业务能力组（Level 1）和具体能力（Level 2-3） |
| ArchiMate 4 | Capability / Resource / Value | ArchiMate 的 Capability 与本概念等价，Resource 为能力实现，Value 为能力创造的价值 |

### 6.5 正例：跨国零售企业的能力复用

**背景**：某跨国零售企业在亚太、欧洲、北美三大区域运营，各区域独立建设"订单管理"系统，导致：

- 同一促销规则需在三个系统分别实现
- 客户体验不一致
- 系统集成成本高

**复用实践**：

1. 建立企业级"订单管理"业务能力（BC-SCM-005），定义统一的能力边界和成果。
2. 将"订单捕获"、"订单校验"、"库存预留"、"订单履约"等子能力标准化。
3. 各区域保留"区域税务计算"、"本地支付方式"等变体能力。
4. 统一能力通过 API 目录暴露给各区域系统。

**效果**：

- 新促销规则上线时间从 6 周缩短至 1 周
- 跨区域客户体验一致性评分提升 35%
- 订单相关 IT 维护成本降低 28%

### 6.6 反例：将组织职能直接建模为业务能力

**场景**：某公司将"市场部审批"、"财务部复核"、"法务部审核"直接建模为业务能力。

**问题**：

- 能力边界随组织架构调整而频繁变化。
- 当市场部拆分为"品牌市场"和"数字市场"后，原"市场部审批"能力失效。
- 能力复用性极低，因为每个能力都绑定了特定组织单元。

**后果**：

- 业务能力地图每半年需大规模重构
- 基于能力的 IT 规划无法稳定执行
- 团队对能力建模失去信心

**避免建议**：

- 业务能力命名应采用**动词+名词**（如"审批营销方案"），而非"部门+动作"。
- 能力定义应聚焦**业务成果**（outcome），而非执行主体。
- 组织角色应映射到能力的 Who 维度，而非能力本身。

### 6.7 与其他概念的关系

- **与价值流的关系**：价值流是业务能力的有序组合，业务能力复用是价值流复用的基础。
- **与业务流程的关系**：业务流程是能力的"时序化执行"，一个能力可由多个流程调用。
- **与业务服务的关系**：业务服务是能力的接口化封装，稳定的服务契约使能力复用跨越技术边界。
- **与应用架构的关系**：应用组件和微服务实现业务能力，通过服务契约向上暴露能力。
- **与 [Zachman Framework](https://en.wikipedia.org/wiki/Zachman_Framework) 的关系**：业务能力主要映射到 Zachman 的 C2-1（What, Business）和 C2-2（How, Business）。

### 6.8 权威来源与交叉引用

> **权威来源**:
>
> - [Business process modeling - Wikipedia](https://en.wikipedia.org/wiki/Business_process_modeling) — 业务过程建模与能力的关系
> - [Zachman Framework - Wikipedia](https://en.wikipedia.org/wiki/Zachman_Framework) — 企业架构分类框架
> - [The Open Group TOGAF Standard, 10th Edition](https://www.opengroup.org/togaf) — TOGAF 业务能力定义
> - [FEA BRM 2.0](https://www.whitehouse.gov/omb/management/federal-enterprise-architecture/) — 联邦企业架构业务参考模型
> - [ArchiMate 4 Specification](https://pubs.opengroup.org/architecture/archimate4-doc/) — ArchiMate 能力元模型
>
> **核查日期**: 2026-07-07

**交叉引用**：

- [FEA BRM 2.0 与 TOGAF 10 Phase B 业务能力图交叉映射](./fea-brm-togaf-mapping.md) — 业务能力与标准框架的详细映射
- [价值流复用的形式化组合](../03-value-stream/value-stream-composition.md) — 能力如何组合为价值流
- [Zachman Framework 与软件架构复用映射](../08-zachman-reuse-mapping/zachman-reusability-matrix.md) — 能力在 Zachman 矩阵中的位置
- [BIAN 金融服务域复用案例](../case-studies/bian-banking-reuse-case.md) — 银行业能力复用实践



## 补充说明：业务能力复用

## 概念定义

**定义**：业务能力（Business Capability）是组织为达成特定业务成果而具备的稳定能力单元，独立于组织结构和实现技术。

## 反例

**反例**：将“市场部审批流程”直接建模为业务能力，导致能力边界随组织调整频繁变化，无法稳定复用。

## 权威来源

> **权威来源**:
>
> - [The Open Group TOGAF](https://www.opengroup.org/togaf)
> - [FEA BRM](https://www.govloop.com/community/blog/federal-enterprise-architecture/)
> - 核查日期：2026-07-07
