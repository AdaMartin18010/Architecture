# 事件驱动架构（EDA）、CQRS 与事件溯源复用模式
>
> 版本: 2026-06-06
> 对齐来源: Microsoft Azure Patterns & Practices, Red Hat, CNCF, 2025 学术研究（WJAETS/WJARR）

## 1. 核心概念三角

```text
Event-Driven Architecture (EDA)
├── Event Notification（事件通知）
├── Event-Carried State Transfer（事件携带状态转移）
└── Event Sourcing（事件溯源）
    └── CQRS（命令查询职责分离）
```

| 模式 | 定义 | 复用层级 |
|-----|------|---------|
| **EDA** | 以事件的生产、检测和消费为中心的系统行为建模 | 应用架构 |
| **CQRS** | 读操作与写操作使用分离的接口和模型 | 应用/组件架构 |
| **Event Sourcing** | 系统状态变化以事件序列存储，支持状态重建 | 数据/组件架构 |

## 2. EDA 核心模式

### 2.1 事件通知（Event Notification）

- 服务发布事件表示某事发生，不携带完整状态
- 消费者收到通知后需查询源服务获取详情
- **适用**：松耦合、低带宽场景

### 2.2 事件携带状态转移（Event-Carried State Transfer, ECST）

- 事件包含消费者所需的完整状态快照
- 消费者无需回调查询源服务
- **适用**：高可用、断网容错、缓存预填充

### 2.3 事件溯源（Event Sourcing）

- 不存储实体当前状态，而是存储导致状态变化的**事件日志**
- 当前状态通过重放事件序列计算得出
- **优势**：
  - 完整审计追踪
  - 时间旅行查询（Point-in-time 重建）
  - 复杂事件处理（CEP）基础

## 3. CQRS 架构详解

### 3.1 基本分离

```text
Command Side（写模型）
├── 业务规则验证
├── 聚合根（Aggregate Root）
├── 事务一致性
└── 发布领域事件

Query Side（读模型）
├── 优化的查询模式
├── 物化视图（Materialized View）
├── 最终一致性
└── 专用数据存储（如搜索引擎、缓存）
```

### 3.2 与 Event Sourcing 的集成

```text
Command → Aggregate → 生成 Event → Event Store
                                        ↓
                                    Event Bus
                                        ↓
                              Projector → 更新 Read Model
```

### 3.3 常见挑战与缓解

| 挑战 | 缓解策略 |
|-----|---------|
| 最终一致性延迟 | 读取自写（Read-your-writes）模式、缓存标记 |
| 事件顺序与乱序 | 分区键保证顺序、版本号/序列号检测 |
| 幂等消费 | 消费者端幂等键、去重表 |
| 分布式追踪 | OpenTelemetry 跨异步边界传播 Trace Context |
| 事件 Schema 演化 | Schema Registry（Avro/Protobuf/JSON Schema）|

## 4. Saga 协调模式

在微服务事务中，Saga 将长事务拆分为本地事务序列，通过补偿事务处理失败：

| 类型 | 协调方式 | 适用场景 |
|-----|---------|---------|
| **编排式 Saga（Choreography）** | 每个服务完成本地事务后发送事件，触发下一个服务 | 简单流程、松耦合优先 |
| **编排式 Saga（Orchestration）** | 中央协调器（Saga Orchestrator）指挥各服务步骤 | 复杂流程、需要可见性 |

## 5. 技术实现栈

### 5.1 消息代理

| 系统 | 定位 | 复用特征 |
|-----|------|---------|
| **Apache Kafka** | 分布式日志、高吞吐 | 分区顺序保证、Schema Registry、Connect |
| **RabbitMQ** | 传统消息队列、灵活路由 | 交换机拓扑复用、死信队列 |
| **NATS / NATS JetStream** | 轻量、云原生 | 主题层级、流持久化 |
| **Pulsar** | 分层存储、多租户 | 统一消息与流、Geo-replication |

### 5.2 事件存储

| 系统 | 定位 |
|-----|------|
| **EventStoreDB** | 专用事件溯源数据库 |
| **Axon Server** | CQRS/ES 专用平台 |
| **PostgreSQL + 扩展** | 通用数据库 + 事件表 + 发布逻辑 |

### 5.3 框架与库

| 语言/平台 | 框架 | 能力 |
|----------|------|------|
| Java | Axon Framework | Saga、聚合、事件存储 |
| .NET | MassTransit / MediatR | 发布/订阅、Saga、Outbox |
| Go | Watermill / Eventus | 消息路由、CQRS 构建块 |
| TypeScript/NestJS | @nestjs/cqrs | 命令/查询总线、事件处理器 |

## 6. 与 DDD 的协同

EDA/CQRS/ES 与领域驱动设计（DDD）天然契合：

| DDD 概念 | EDA/CQRS 映射 |
|---------|--------------|
| 限界上下文（Bounded Context） | 微服务边界；上下文间通过事件集成 |
| 聚合（Aggregate） | 命令侧一致性边界；事件发布单位 |
| 领域事件（Domain Event） | 业务发生的事实；系统间契约 |
|  ubiquitous Language | 事件命名即业务语言 |

## 7. 云原生最佳实践

### 7.1 Outbox 模式

确保数据库事务与事件发布的原子性：

1. 业务数据变更与事件记录在同一数据库事务中写入 Outbox 表
2. 独立进程轮询 Outbox 表，将事件发布到消息代理
3. 发布成功后删除/标记 Outbox 记录

### 7.2 Materialized View 模式

- 读模型非实时计算，而是定期或事件触发更新预计算视图
- 支持复杂查询场景（如搜索、报表）而不影响写性能

### 7.3 Compensating Transaction 模式

- Saga 失败时执行补偿操作撤销已完成的步骤
- 补偿本身也是事件，需设计为幂等

## 8. 参考索引

- Microsoft Azure: *Cloud Application Architecture Guide* — CQRS / Event Sourcing / Materialized View
- Red Hat: *Illustrated CQRS*
- Martin Fowler: "Event Sourcing", "CQRS"
- Greg Young: "Why use Event Sourcing?"
- WJAETS 2025: "Event-Driven Microservices Architectures: Principles, Patterns and Best Practices"
- WJARR 2025: "Demystifying cloud-native enterprise architecture"
- Axon Framework: [axoniq.io](https://axoniq.io)
- EventStoreDB: [eventstore.com](https://eventstore.com)
