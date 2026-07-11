# 模块化单体：复用的务实选择

> **版本**: 2026-06-06
> **定位**: 论述模块化单体作为一种被低估的复用架构选择

---

## 1. 为什么模块化单体值得重视

微服务成为默认答案后，许多团队陷入了"为分布式而分布式"的陷阱。模块化单体（Modular Monolith）提供了一种务实的中间态：

- 在运行时保持单一部署单元
- 在构建时保持清晰的模块边界
- 在需要时，单个模块可以逐步拆分为独立服务

> **定理 3.3** (Microservice Decomposition Limit, 重申): 过早拆分微服务会增加复用的协调成本，而模块化单体可以在不引入分布式复杂性的前提下获得大部分复用收益。

---

## 2. 模块化单体的核心特征

| 特征 | 说明 |
|------|------|
| **单一部署单元** | 整个应用作为一个单元构建和部署 |
| **清晰模块边界** | 模块间通过显式接口交互，禁止直接数据库访问 |
| **模块独立测试** | 每个模块可独立运行单元测试和集成测试 |
| **渐进式拆分** | 当模块需要独立扩展或团队时，可拆分为微服务 |
| **共享基础设施** | 数据库、缓存、消息队列可在模块间共享或由平台层提供 |

---

## 3. 模块化单体的复用策略

### 模块边界设计

```text
模块化单体
├── Module A: 用户管理
│   ├── API: UserService
│   ├── Repository: UserRepository
│   └── Events: UserRegisteredEvent
│
├── Module B: 订单管理
│   ├── API: OrderService
│   ├── Repository: OrderRepository
│   └── Events: OrderPlacedEvent
│
├── Module C: 库存管理
│   ├── API: InventoryService
│   ├── Repository: InventoryRepository
│   └── Events: StockReservedEvent
│
└── Shared Kernel
    ├── Common types
    ├── Cross-cutting concerns
    └── Infrastructure adapters
```

### 关键约束

1. **禁止跨模块直接数据库访问**: 模块间通信必须通过 API 或领域事件
2. **模块拥有独立的数据模型**: 即使物理数据库相同，逻辑模型独立
3. **共享内核最小化**: 只有真正的通用概念才能进入 Shared Kernel
4. **模块编译隔离**: 使用多模块构建工具（Maven、Gradle、NX、Turborepo）

---

## 4. 何时选择模块化单体

**适合模块化单体的场景**:

- 团队规模 < 50 人
- 业务领域边界仍在快速演进
- 不需要独立扩展特定功能
- 运维能力有限
- 需要快速迭代和验证业务假设

**不适合模块化单体的场景**:

- 某些模块需要独立扩展（流量差异 > 10x）
- 团队地理分布，需要高度自治
- 已有成熟的 DevOps 能力
- 特定模块需要不同的技术栈

---

## 5. 模块化单体 → 微服务的演进路径

```text
阶段 1: 单体混沌 (Big Ball of Mud)
    ↓ 重构：提取模块边界
阶段 2: 模块化单体 (Modular Monolith)
    ↓ 识别：哪些模块需要独立演进
阶段 3: 分布式模块化 (Modular Distributed)
    ↓ 拆分：高内聚模块成为独立服务
阶段 4: 微服务 (Microservices)
```

> **关键原则**: 不要在没有清晰模块边界的情况下直接拆分微服务。

---

## 6. 技术实现参考

| 语言/生态 | 工具 |
|-----------|------|
| Java | Spring Modulith, OSGi, JPMS |
| .NET | Modular Monolith with Clean Architecture |
| Node.js | NX Monorepo, NestJS Modules |
| Python | Django Apps, Flask Blueprints |
| Go | Go Modules + 清晰的包边界 |

---

> 最后更新: 2026-06-06


---

## 补充说明：模块化单体：复用的务实选择

## 概念定义

**定义**：新兴趋势包括平台工程、模块化单体、WebAssembly 组件、绿色软件与 RegTech AI，它们通过新抽象层或新约束推动复用资产的可移植性、可持续性与治理自动化。

## 示例

**示例**：平台工程团队构建内部开发者平台（IDP），将部署、可观测性、安全策略封装为自助服务模板，产品团队复用 Golden Path 快速交付。

## 反例

**反例**：追逐 WASM 潮流将所有服务重写为组件，忽视工具链成熟度与团队技能，导致调试困难、交付延期。

## 权威来源

> **权威来源**:
>
> - [CNCF Platform Engineering](https://tag-app-delivery.cncf.io/whitepapers/platforms/)
> - [WebAssembly Component Model](https://component-model.bytecodealliance.org)
> - [Green Software Foundation](https://greensoftware.foundation)
> - 核查日期：2026-07-07