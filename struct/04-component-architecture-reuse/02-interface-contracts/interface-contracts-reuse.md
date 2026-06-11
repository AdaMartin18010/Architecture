# 接口契约与架构复用

> **版本**: 2026-06-10
> **定位**: 组件架构层 —— 接口契约驱动的复用：从 IDL 到 OpenAPI 到 WIT 的演进
> **对齐标准**: OpenAPI 3.1, gRPC Protobuf, AsyncAPI, WIT, Pact, Spring Cloud Contract
> **状态**: ✅ 已完成

---

## 目录

- [接口契约与架构复用](#接口契约与架构复用)
  - [目录](#目录)
  - [1. 接口契约演进](#1-接口契约演进)
    - [1.1 历史脉络](#11-历史脉络)
    - [1.2 现代接口契约技术对比](#12-现代接口契约技术对比)
  - [2. 契约驱动的复用](#2-契约驱动的复用)
    - [2.1 Consumer-Driven Contracts（CDC）](#21-consumer-driven-contractscdc)
    - [2.2 契约作为复用单元](#22-契约作为复用单元)
  - [3. 接口版本策略](#3-接口版本策略)
    - [3.1 向后兼容（Backward Compatible）](#31-向后兼容backward-compatible)
    - [3.2 向前兼容（Forward Compatible）](#32-向前兼容forward-compatible)
    - [3.3 破坏性变更管理](#33-破坏性变更管理)
  - [4. 契约测试在复用流水线中的位置](#4-契约测试在复用流水线中的位置)
  - [5. 案例：基于 OpenAPI + Pact 的微服务契约复用](#5-案例基于-openapi--pact-的微服务契约复用)
    - [5.1 场景](#51-场景)
    - [5.2 契约定义](#52-契约定义)
    - [5.3 Pact 契约测试](#53-pact-契约测试)
    - [5.4 复用价值](#54-复用价值)
  - [6. 权威来源](#6-权威来源)

---

## 1. 接口契约演进

### 1.1 历史脉络

| 时代 | 技术 | 用途 | 复用粒度 |
|:---|:---|:---|:---|
| 1990s | CORBA IDL | 分布式对象 | 对象方法 |
| 2000s | WSDL | Web Service | 服务操作 |
| 2010s | Swagger/OpenAPI | REST API | HTTP 端点 |
| 2010s | Protobuf/gRPC | 高性能 RPC | 服务方法 |
| 2020s | AsyncAPI | 异步消息 | 事件通道 |
| **2020s** | **WIT** | **WASM 组件** | **组件接口** |

### 1.2 现代接口契约技术对比

| 技术 | 协议 | 序列化 | 流支持 | 代码生成 | 主要场景 |
|:---|:---|:---|:---:|:---:|:---|
| **OpenAPI 3.1** | HTTP/REST | JSON/XML | ❌ | ✅ | Web API、微服务 |
| **gRPC + Protobuf** | HTTP/2 | Protobuf | ✅ | ✅ | 内部服务、高性能 |
| **GraphQL** | HTTP | JSON | ❌ | ✅ | 客户端驱动查询 |
| **AsyncAPI** | MQTT/AMQP/Kafka | JSON/Avro/Protobuf | ✅ | ✅ | 事件驱动架构 |
| **WIT** | 组件导入/导出 | 语言原生 | ✅ (WASI 0.3) | ✅ | 跨语言组件 |
| **tRPC** | HTTP | JSON | ❌ | ✅ | 全栈 TypeScript |

---

## 2. 契约驱动的复用

### 2.1 Consumer-Driven Contracts（CDC）

**核心理念**: 由消费者定义期望的契约，提供者确保满足这些契约。

```
CDC 工作流程
├── 消费者团队编写契约测试
│   └── 定义期望的请求/响应格式
├── 契约发布到共享注册中心（Pact Broker）
├── 提供者团队拉取契约并验证
│   └── 在 CI 中运行提供者验证测试
└── 双方契约兼容时才能部署
```

### 2.2 契约作为复用单元

| 契约类型 | 复用内容 | 复用方式 |
|:---|:---|:---|
| **OpenAPI Spec** | API 定义、数据模型、示例 | 共享规范文件、代码生成 |
| **Protobuf** | 消息格式、服务定义 | 共享 `.proto` 文件、编译为各语言绑定 |
| **AsyncAPI** | 事件 schema、通道定义 | 共享 AsyncAPI 文档、生成发布/订阅代码 |
| **Pact 契约** | 消费者期望的交互模式 | 共享 Pact 文件、双向验证 |
| **WIT** | 组件接口、类型定义 | 共享 `.wit` 文件、生成语言绑定 |

---

## 3. 接口版本策略

### 3.1 向后兼容（Backward Compatible）

**安全变更**（消费者无需修改）:

- 添加新的可选字段
- 添加新的端点/操作
- 放宽输入验证规则
- 缩小输出范围（更具体）

### 3.2 向前兼容（Forward Compatible）

**安全变更**（旧消费者可处理新响应）:

- 使用 extensible 的 schema 设计
- 忽略未知字段
- 使用默认值处理缺失字段

### 3.3 破坏性变更管理

```
破坏性变更处理策略
├── 策略 1: 并行版本（URL 版本）
│   └── /v1/users → /v2/users
├── 策略 2: 内容协商（Header 版本）
│   └── Accept: application/vnd.api.v2+json
├── 策略 3: 弃用窗口
│   └── 发布 v2 后，v1 维护 6-12 个月
├── 策略 4: 兼容性层
│   └── v2 服务内部调用 v1 适配器
└── 策略 5: 消费者通知
    └── 自动化分析哪些消费者受影响
```

---

## 4. 契约测试在复用流水线中的位置

```
复用流水线中的契约测试
├── 开发阶段
│   ├── 消费者编写契约测试（Pact/WireMock）
│   └── 提供者实现接口并通过契约验证
├── 集成阶段
│   ├── CI 中运行契约验证（can-i-deploy 检查）
│   └── 契约兼容方可合并
├── 部署阶段
│   ├── 部署前验证生产环境契约兼容性
│   └── 契约破坏阻断部署
└── 运营阶段
    ├── 持续监控实际交互是否符合契约
    └── 契约漂移告警
```

---

## 5. 案例：基于 OpenAPI + Pact 的微服务契约复用

### 5.1 场景

电商系统中有三个微服务：

- **订单服务**（消费者）→ 调用 → **库存服务**（提供者）
- **支付服务**（消费者）→ 调用 → **库存服务**（提供者）

### 5.2 契约定义

```yaml
# OpenAPI 规范（库存服务接口）
openapi: 3.1.0
info:
  title: Inventory API
  version: 1.0.0
paths:
  /products/{id}/availability:
    get:
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: 库存可用性
          content:
            application/json:
              schema:
                type: object
                properties:
                  available:
                    type: boolean
                  quantity:
                    type: integer
                    minimum: 0
```

### 5.3 Pact 契约测试

```javascript
// 订单服务消费者测试
const { PactV3 } = require('@pact-foundation/pact');

describe('Inventory API contract', () => {
  const provider = new PactV3({
    consumer: 'order-service',
    provider: 'inventory-service'
  });

  it('returns product availability', () => {
    provider
      .given('product exists')
      .uponReceiving('get product availability')
      .withRequest({
        method: 'GET',
        path: '/products/PROD-123/availability'
      })
      .willRespondWith({
        status: 200,
        body: {
          available: true,
          quantity: 100
        }
      });
  });
});
```

### 5.4 复用价值

- 库存服务接口契约被两个消费者复用
- 契约测试确保任何接口变更不会破坏现有消费者
- Pact Broker 作为契约注册中心，支持契约的版本管理和兼容性检查

---

## 6. 权威来源

| 来源 | URL | 核查日期 |
|:---|:---|:---|
| OpenAPI Specification 3.1 | <https://spec.openapis.org/oas/v3.1.0> | 2026-06-10 |
| gRPC / Protocol Buffers | <https://grpc.io/> | 2026-06-10 |
| AsyncAPI | <https://www.asyncapi.com/> | 2026-06-10 |
| Pact (Consumer-Driven Contracts) | <https://pact.io/> | 2026-06-10 |
| Spring Cloud Contract | <https://spring.io/projects/spring-cloud-contract> | 2026-06-10 |
| WIT (WASM Interface Types) | <https://component-model.bytecodealliance.org/design/wit.html> | 2026-06-10 |
