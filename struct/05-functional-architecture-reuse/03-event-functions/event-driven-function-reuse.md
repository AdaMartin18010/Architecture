# 事件驱动函数复用模式

> **版本**: 2026-06-10
> **定位**: 功能架构层 —— 事件驱动架构中的函数复用：schema、路由与模式
> **对齐标准**: CloudEvents, AsyncAPI, Apache Kafka, Knative Eventing, AWS EventBridge, Azure Event Grid
> **状态**: ✅ 已完成

---

## 目录

- [事件驱动函数复用模式](#事件驱动函数复用模式)
  - [目录](#目录)
  - [1. 事件驱动函数概述](#1-事件驱动函数概述)
    - [1.1 EDA + FaaS 的结合](#11-eda--faas-的结合)
    - [1.2 事件驱动函数的核心要素](#12-事件驱动函数的核心要素)
  - [2. 事件 Schema 复用](#2-事件-schema-复用)
    - [2.1 Schema 演进策略](#21-schema-演进策略)
    - [2.2 Schema 注册中心](#22-schema-注册中心)
    - [2.3 CloudEvents 作为通用 Schema](#23-cloudevents-作为通用-schema)
  - [3. 事件路由与过滤复用模式](#3-事件路由与过滤复用模式)
    - [3.1 事件路由器模式](#31-事件路由器模式)
    - [3.2 可复用的事件处理中间件](#32-可复用的事件处理中间件)
  - [4. Saga 模式与补偿事务的函数复用](#4-saga-模式与补偿事务的函数复用)
    - [4.1 Saga 模式概述](#41-saga-模式概述)
    - [4.2 Saga 函数的复用](#42-saga-函数的复用)
  - [5. 事件溯源中的函数复用](#5-事件溯源中的函数复用)
    - [5.1 事件溯源概述](#51-事件溯源概述)
    - [5.2 投影函数的复用](#52-投影函数的复用)
  - [6. 案例：Kafka + CloudEvents + Knative Eventing 构建可复用事件处理流水线](#6-案例kafka--cloudevents--knative-eventing-构建可复用事件处理流水线)
    - [6.1 架构](#61-架构)
    - [6.2 可复用组件](#62-可复用组件)
  - [7. 权威来源](#7-权威来源)
  - [补充说明：事件驱动函数复用模式](#补充说明事件驱动函数复用模式)
  - [概念定义](#概念定义)
  - [分析](#分析)

---

## 1. 事件驱动函数概述

### 1.1 EDA + FaaS 的结合

事件驱动架构（EDA）与函数即服务（FaaS）的结合，形成了**事件驱动函数**模式：

- **松耦合**: 生产者无需知道消费者存在
- **可扩展**: 每个函数独立伸缩
- **可复用**: 同一函数可订阅多个事件流

### 1.2 事件驱动函数的核心要素

```
事件驱动函数模型
├── Event Producer（事件生产者）
│   ├── 业务系统
│   ├── IoT 设备
│   └── 外部服务
├── Event Broker（事件代理）
│   ├── Kafka
│   ├── RabbitMQ / AMQP
│   ├── MQTT Broker
│   └── Cloud Pub/Sub
├── Event Router（事件路由器）
│   ├── 过滤（Filter）
│   ├── 转换（Transform）
│   └── 路由（Route）
└── Event Consumer（事件消费者 / 函数）
    ├── 无状态处理函数
    ├── 有状态聚合函数
    └── 副作用函数（写数据库、发送通知）
```

---

## 2. 事件 Schema 复用

### 2.1 Schema 演进策略

| 策略 | 描述 | 兼容性 |
|:---|:---|:---:|
| **后向兼容** | 新增可选字段 | ✅ 旧消费者可用 |
| **前向兼容** | 消费者忽略未知字段 | ✅ 新消费者可用 |
| **完全兼容** | 同时支持前后向 | ✅✅ 最佳 |
| **不兼容** | 删除或修改现有字段 | ❌ 需协调升级 |

### 2.2 Schema 注册中心

**Confluent Schema Registry** 模式:

```
Schema 注册中心工作流
├── 生产者发布事件前注册 schema
│   └── 检查与历史版本的兼容性
├── 注册中心分配 schema ID
│   └── 紧凑的 Avro/Protobuf 序列化
├── 消费者从注册中心获取 schema
│   └── 动态解析事件格式
└── Schema 版本演进管理
    └── 兼容性策略强制执行
```

### 2.3 CloudEvents 作为通用 Schema

CloudEvents 提供了跨平台的事件包装标准：

```json
{
  "specversion": "1.0",
  "type": "com.example.order.created",
  "source": "/order-service/v1",
  "id": "A234-1234-1234",
  "time": "2026-06-10T12:00:00Z",
  "datacontenttype": "application/json",
  "data": {
    "orderId": "ORD-12345",
    "customerId": "CUST-67890",
    "amount": 199.99
  }
}
```

**复用价值**: 基于 CloudEvents 的函数可在 Kafka、MQTT、HTTP 等不同传输层间复用。

---

## 3. 事件路由与过滤复用模式

### 3.1 事件路由器模式

```
Event Router Pattern
├── Content-Based Router
│   └── 根据事件内容路由到不同处理函数
│   └── 例：order.amount > 1000 → 高价值订单处理
├── Message Filter
│   └── 过滤掉不感兴趣的事件
│   └── 例：仅处理 status = "completed" 的订单
├── Dynamic Router
│   └── 运行时决定路由目标
│   └── 例：根据负载动态分配处理函数
└── Recipient List
    └── 将事件广播给多个处理函数
    └── 例：订单创建同时触发库存扣减和通知发送
```

### 3.2 可复用的事件处理中间件

| 功能 | 工具 | 复用方式 |
|:---|:---|:---|
| 事件过滤 | AWS EventBridge Rules | 规则模板复用 |
| 事件转换 | Kafka Streams / Flink | 拓扑模板复用 |
| 事件聚合 | Kafka Streams Windowing | 窗口策略复用 |
| 事件排序 | Kafka Partitioning | 分区策略复用 |
| 死信队列 | 各平台 DLQ | 错误处理模板复用 |

---

## 4. Saga 模式与补偿事务的函数复用

### 4.1 Saga 模式概述

Saga 是长事务的分布式实现，将大事务拆分为多个本地事务，每个本地事务有对应的**补偿操作**。

```
Saga 执行流程（订单处理示例）
├── T1: 创建订单
│   └── C1: 取消订单
├── T2: 扣减库存
│   └── C2: 恢复库存
├── T3: 处理支付
│   └── C3: 退款
└── T4: 发送通知
    └── C4: （通常无需补偿）

正常流程: T1 → T2 → T3 → T4 → 完成
异常流程: T1 → T2 → T3 失败 → C2 → C1 →  Saga 失败
```

### 4.2 Saga 函数的复用

```
可复用的 Saga 组件
├── 事务函数库
│   ├── createOrder()
│   ├── deductInventory()
│   ├── processPayment()
│   └── sendNotification()
├── 补偿函数库
│   ├── cancelOrder()
│   ├── restoreInventory()
│   └── refundPayment()
└── Saga 编排器
    ├── 编排式 Saga（Orchestration）
    │   └── 中央协调器调用各函数
    └── 协同式 Saga（Choreography）
        └── 各函数通过事件相互触发
```

---

## 5. 事件溯源中的函数复用

### 5.1 事件溯源概述

事件溯源（Event Sourcing）将系统状态变化记录为不可变的事件序列，而非直接更新状态。

```
事件溯源架构
├── Command（命令）
│   └── 用户意图的表达
├── Aggregate（聚合）
│   └── 业务规则的执行者
│   └── 生成 Events
├── Event Store（事件存储）
│   └── 不可变的事件日志
│   └── 系统状态的"唯一真相源"
├── Projection（投影）
│   └── 从事件流构建读模型
│   └── 可复用的投影函数
└── Snapshot（快照）
    └── 性能优化，定期保存聚合状态
```

### 5.2 投影函数的复用

投影函数是从事件流到读模型的纯函数，天然可复用：

```python
# 可复用的投影函数示例
def project_order_summary(events: List[OrderEvent]) -> OrderSummary:
    """从订单事件流构建订单摘要"""
    summary = OrderSummary()
    for event in events:
        if isinstance(event, OrderCreated):
            summary.order_id = event.order_id
            summary.customer_id = event.customer_id
        elif isinstance(event, ItemAdded):
            summary.total_amount += event.price * event.quantity
        elif isinstance(event, PaymentProcessed):
            summary.payment_status = event.status
    return summary
```

**复用价值**:

- 同一投影函数可被多个读模型复用
- 投影函数无副作用，易于测试和验证
- 新读模型可通过组合现有投影函数快速构建

---

## 6. 案例：Kafka + CloudEvents + Knative Eventing 构建可复用事件处理流水线

### 6.1 架构

```
事件处理流水线
├── 生产者
│   └── 订单服务 → CloudEvents → Kafka
├── 事件代理
│   └── Kafka Cluster（多分区）
├── 事件路由（Knative Eventing）
│   ├── Trigger: type = order.created
│   ├── Trigger: type = order.updated
│   └── Trigger: type = order.cancelled
└── 消费者（Knative Services）
    ├── inventory-processor
    ├── notification-processor
    └── analytics-processor
```

### 6.2 可复用组件

| 组件 | 复用内容 | 复用方式 |
|:---|:---|:---|
| CloudEvents 包装器 | 事件格式标准化 | 共享库 |
| Kafka Producer | 发布事件 | 共享库/模板 |
| Knative Trigger | 事件路由规则 | YAML 模板 |
| 处理函数框架 | 日志、监控、错误处理 | 共享基础镜像 |
| DLQ Handler | 死信处理 | 共享函数 |

---

## 7. 权威来源

| 来源 | URL | 核查日期 |
|:---|:---|:---|
| CloudEvents | <https://cloudevents.io/> | 2026-06-10 |
| AsyncAPI | <https://www.asyncapi.com/> | 2026-06-10 |
| Apache Kafka | <https://kafka.apache.org/> | 2026-06-10 |
| Knative Eventing | <https://knative.dev/docs/eventing/> | 2026-06-10 |
| AWS EventBridge | <https://aws.amazon.com/eventbridge/> | 2026-06-10 |
| Azure Event Grid | <https://azure.microsoft.com/services/event-grid/> | 2026-06-10 |
| Confluent Schema Registry | <https://docs.confluent.io/platform/current/schema-registry/index.html> | 2026-06-10 |
| Saga Pattern (Microservices.io) | <https://microservices.io/patterns/data/saga.html> | 2026-06-10 |
| Event Sourcing (Martin Fowler) | <https://martinfowler.com/eaaDev/EventSourcing.html> | 2026-06-10 |


---

## 补充说明：事件驱动函数复用模式

## 概念定义

**定义**：事件函数复用是将事件处理逻辑封装为可复用函数，并通过事件 Schema、路由规则与错误处理策略实现跨系统的事件驱动集成。

## 分析

**分析**：事件函数复用的关键在于统一事件契约与处理语义，避免隐式依赖。
