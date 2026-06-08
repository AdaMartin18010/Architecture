# 事件驱动架构（EDA）复用模式

> **版本**: 2026-06-08
> **定位**: 应用架构层（Level 2）—— EDA 四种复用模式、事件契约与消息中间件复用
> **对齐标准**: CNCF, OASIS, Apache Kafka / Pulsar 架构
> **状态**: ⏳ 框架填充中

---

## 1. 核心概念

事件驱动架构（Event-Driven Architecture, EDA）以**事件**作为系统间通信的核心原语，实现了生产者和消费者的完全解耦。从复用视角看，EDA 的复用单元包括：**事件类型定义、事件处理管道、事件存储层**以及**整体拓扑模式**。

OASIS 的 Advanced Message Queuing Protocol (AMQP) 和 CNCF 的 CloudEvents 标准为跨系统的事件互操作提供了基础。Kafka 和 Pulsar 作为事实上的事件基础设施，其 Topic/Partition/Subscription 模型构成了复用的物理边界。

---

## 2. EDA 四种复用模式

Martin Fowler 在 *Patterns of Enterprise Application Architecture* 中系统阐述了四种事件协作模式，其复用特征各不相同：

### 2.1 Event Notification（事件通知）

**定义**: 生产者发送轻量级事件，仅通知"某事发生"，消费者需自行查询详细信息。

- **复用单元**: 事件类型定义（如 `OrderCreatedEvent`）
- **复用边界**: 事件 Schema + Topic 名称
- **耦合度**: 低（消费者不依赖生产者的数据模型）
- **风险**: 消费者查询负载可能压垮生产者系统（N+1 查询问题）

### 2.2 Event-Carried State Transfer（事件携带状态转移）

**定义**: 事件 payload 包含完整的状态数据，消费者无需回查生产者。

- **复用单元**: 事件 Schema + 数据模型
- **复用边界**: 事件 payload 的版本兼容性
- **耦合度**: 中（消费者依赖事件的数据结构）
- **优势**: 消费者可构建本地物化视图，实现高可用读取

> **定理 E.1** (Event Payload Stability): 事件携带状态转移模式的复用稳定性与 payload 的向后兼容性强相关。字段只能新增（nullable），不可删除或修改类型。

### 2.3 CQRS（Command Query Responsibility Segregation）

**定义**: 将写模型（Command）和读模型（Query）分离，通过事件同步两者。

- **复用单元**: Command Handler / Query Handler / 投影（Projection）
- **复用边界**: 读写模型的领域边界
- **耦合度**: 中（投影逻辑依赖事件顺序和完整性）
- **典型实现**: Axon Framework, EventStoreDB

### 2.4 Event Sourcing（事件溯源）

**定义**: 系统的真实状态由事件日志推导而来，而非直接存储当前状态。

- **复用单元**: 领域事件定义 + 聚合（Aggregate）行为
- **复用边界**: 聚合边界 = 事件溯源的强一致性边界
- **耦合度**: 高（事件日志是系统的事实来源，所有消费者依赖其完整性）
- **优势**: 完整审计轨迹、时间旅行调试、状态重建

| 模式 | 复用粒度 | 耦合度 | 主要风险 | 适用场景 |
|------|---------|--------|---------|---------|
| Event Notification | 事件类型 | 低 | N+1 查询 | 跨系统解耦 |
| Event-Carried State Transfer | 事件 Schema | 中 | Payload 膨胀 | 数据同步 |
| CQRS | Handler / Projection | 中 | 最终一致性复杂度 | 读写过载分离 |
| Event Sourcing | 聚合 + 事件流 | 高 | 事件 Schema 演化困难 | 审计、合规 |

---

## 3. 事件契约复用

事件契约（Event Contract）是 EDA 复用的核心资产。

### 3.1 Schema 治理

- **Schema Registry**: Confluent Schema Registry / AWS Glue Schema Registry
- **兼容性模式**: BACKWARD（新代码读旧数据）、FORWARD（旧代码读新数据）、FULL（双向兼容）
- **版本策略**: 事件 Schema 的 Major 版本变更应视为**破坏性契约变更**，需消费者同步升级

### 3.2 CloudEvents 规范

CloudEvents 是 CNCF 主导的跨平台事件格式标准，定义了事件的通用元数据：

```json
{
  "specversion": "1.0",
  "type": "com.example.order.created",
  "source": "/orders",
  "id": "A234-1234-1234",
  "datacontenttype": "application/json",
  "data": { "orderId": "123", "amount": 100.00 }
}
```

**复用价值**: 使用 CloudEvents 的事件可在 Kafka、RabbitMQ、HTTP、S3 等不同传输层之间无缝迁移。

---

## 4. 消息中间件复用特征

| 特性 | Apache Kafka | Apache Pulsar |
|------|-------------|---------------|
| 存储模型 | 日志分段（Log Segment） | 分层存储（BookKeeper + 对象存储） |
| 多租户 | 弱（需物理集群隔离） | 强（命名空间 + 配额） |
| 地理复制 | MirrorMaker / MM2 | 内置 Geo-Replication |
| 函数计算 | Kafka Streams / ksqlDB | Pulsar Functions |
| 复用边界 | Topic + Consumer Group | Topic + Subscription + Namespace |

---

> 最后更新: 2026-06-08
> 权威来源:
>
> - <https://cloudevents.io/> (CloudEvents Specification, CNCF)
> - <https://martinfowler.com/articles/201701-event-driven.html>
> - <https://kafka.apache.org/documentation/> (Apache Kafka Docs)
