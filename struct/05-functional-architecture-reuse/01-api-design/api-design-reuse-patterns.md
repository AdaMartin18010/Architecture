# API 设计模式与功能复用

> **版本**: 2026-06-10
> **定位**: 功能架构层 —— API 作为功能复用的核心单元：设计模式、版本策略与组合架构
> **对齐标准**: OpenAPI 3.1, JSON:API, GraphQL, gRPC, AsyncAPI, Richardson Maturity Model
> **状态**: ✅ 已完成

---

## 目录

- [API 设计模式与功能复用](#api-设计模式与功能复用)
  - [目录](#目录)
  - [1. API 作为功能复用的核心单元](#1-api-作为功能复用的核心单元)
    - [1.1 API 复用的三个层次](#11-api-复用的三个层次)
    - [1.2 API 优先设计（API-First Design）](#12-api-优先设计api-first-design)
  - [2. API 设计模式对比](#2-api-设计模式对比)
    - [2.1 REST (Representational State Transfer)](#21-rest-representational-state-transfer)
    - [2.2 GraphQL](#22-graphql)
    - [2.3 gRPC](#23-grpc)
    - [2.4 AsyncAPI（事件驱动 API）](#24-asyncapi事件驱动-api)
  - [3. API 版本策略与复用](#3-api-版本策略与复用)
    - [3.1 版本策略对比](#31-版本策略对比)
    - [3.2 API 弃用策略](#32-api-弃用策略)
  - [4. API 组合模式](#4-api-组合模式)
    - [4.1 BFF (Backend-for-Frontend)](#41-bff-backend-for-frontend)
    - [4.2 API Gateway](#42-api-gateway)
    - [4.3 Backend-for-AI](#43-backend-for-ai)
  - [5. API 可复用性评估](#5-api-可复用性评估)
    - [5.1 评估维度](#51-评估维度)
    - [5.2 复用评分卡](#52-复用评分卡)
  - [6. 案例：Stripe API 设计对功能复用的最佳实践](#6-案例stripe-api-设计对功能复用的最佳实践)
    - [6.1 Stripe API 的设计原则](#61-stripe-api-的设计原则)
    - [6.2 Stripe API 的复用模式](#62-stripe-api-的复用模式)
  - [7. 权威来源](#7-权威来源)

---

## 1. API 作为功能复用的核心单元

### 1.1 API 复用的三个层次

```
API 复用层次模型
├── L1: 端点复用（Endpoint Reuse）
│   └── 直接调用现有 API 端点获取功能
│   └── 例：调用第三方支付 API 完成支付
├── L2: Schema 复用（Schema Reuse）
│   └── 复用 API 的数据模型和类型定义
│   └── 例：复用 OpenAPI 定义的 User、Order 模型
└── L3: 模式复用（Pattern Reuse）
    └── 复用 API 设计模式和架构风格
    └── 例：复用 Stripe 的资源命名、分页、错误处理模式
```

### 1.2 API 优先设计（API-First Design）

API 优先设计是功能复用的最佳实践：

- **先定义接口，后实现**: 确保接口设计独立于技术实现
- **契约驱动**: OpenAPI/AsyncAPI 规范作为开发和消费的契约
- **并行开发**: 消费者和提供者可以基于契约并行工作

---

## 2. API 设计模式对比

### 2.1 REST (Representational State Transfer)

**核心原则**: 资源导向、无状态、统一接口

```
REST API 设计检查清单
├── 资源命名
│   ├── ✅ /users（复数名词）
│   ├── ❌ /getUsers（动词）
│   └── ✅ /users/{id}/orders（嵌套资源）
├── HTTP 方法
│   ├── GET — 读取
│   ├── POST — 创建
│   ├── PUT — 全量更新
│   ├── PATCH — 部分更新
│   └── DELETE — 删除
├── 状态码
│   ├── 200 OK, 201 Created, 204 No Content
│   ├── 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
│   └── 500 Internal Server Error
└── HATEOAS（可选）
    └── 响应中包含相关资源链接
```

### 2.2 GraphQL

**核心原则**: 客户端驱动查询、单一端点、强类型 schema

**复用优势**:

- 消费者精确获取所需数据，避免过度获取
- Schema 作为强类型契约，支持代码生成
- 内省（Introspection）支持动态发现可用字段

**复用挑战**:

- 查询复杂度难以预估（需复杂度限制）
- 缓存策略比 REST 复杂
- 版本管理策略与 REST 不同（schema 演进）

### 2.3 gRPC

**核心原则**: 高性能 RPC、基于 HTTP/2、Protobuf 序列化

**复用优势**:

- 强类型接口定义（Protobuf）
- 流支持（Unary、Server Streaming、Client Streaming、Bidirectional）
- 代码生成（多语言客户端/服务端）

**复用场景**: 内部微服务通信、高性能数据交换

### 2.4 AsyncAPI（事件驱动 API）

**核心原则**: 异步消息契约、发布/订阅模式

**复用优势**:

- 定义事件 schema 和通道契约
- 支持多种协议（Kafka、MQTT、AMQP、WebSocket）
- 松耦合：生产者无需知道消费者

---

## 3. API 版本策略与复用

### 3.1 版本策略对比

| 策略 | 实现方式 | 优点 | 缺点 | 适用场景 |
|:---|:---|:---|:---|:---|
| **URL 版本** | `/v1/users`, `/v2/users` | 简单直观 | URL 污染 | 公共 API |
| **Header 版本** | `Accept: application/vnd.api.v2+json` | URL 干净 | 不够直观 | 内部 API |
| **内容协商** | `Content-Type` + `Accept` | HTTP 标准 | 复杂 | 需细粒度控制 |
| **无版本** | 永远向后兼容 | 最简单 | 约束强 | GraphQL、极少数 |

### 3.2 API 弃用策略

```
API 弃用时间线
├── T0: 发布新版本 API
├── T0 + 30 天: 向所有消费者发送弃用通知
│   └── 包含迁移指南和时间表
├── T0 + 90 天: 在旧版本响应中添加 Deprecation 头
│   └── Sunset: Thu, 31 Dec 2026 23:59:59 GMT
├── T0 + 180 天: 旧版本返回警告日志
├── T0 + 270 天: 旧版本开始限流
└── T0 + 365 天: 旧版本退役
```

---

## 4. API 组合模式

### 4.1 BFF (Backend-for-Frontend)

**定义**: 为每个前端平台（Web、iOS、Android）定制专用的后端 API 层。

**复用价值**: 前端团队复用底层服务，BFF 层处理聚合和适配。

### 4.2 API Gateway

**定义**: 统一的 API 入口，处理认证、限流、路由、聚合。

**复用价值**: 底层服务通过 Gateway 暴露，消费者复用 Gateway 的通用能力（认证、监控、缓存）。

### 4.3 Backend-for-AI

**新兴模式**: 为 AI Agent 和 LLM 应用定制的后端层。

**复用价值**:

- 封装 MCP 工具定义
- 管理 Agent 上下文和状态
- 提供结构化的功能接口供 LLM 调用

---

## 5. API 可复用性评估

### 5.1 评估维度

| 维度 | 权重 | 评估标准 |
|:---|:---:|:---|
| **一致性** | 20% | 命名规范、错误格式、分页方式统一 |
| **可发现性** | 20% | 文档完整、有 OpenAPI/AsyncAPI、支持内省 |
| **稳定性** | 20% | 版本策略清晰、变更记录完整、弃用通知及时 |
| **SDK 支持** | 15% | 官方 SDK、多语言支持、类型安全 |
| **性能** | 15% | 响应时间、吞吐量、可用性 SLA |
| **安全性** | 10% | 认证方式、授权粒度、审计日志 |

### 5.2 复用评分卡

```
API 复用评分卡（满分 100）
├── 一致性 (20)
│   ├── 资源命名规范 (+5)
│   ├── 错误格式统一 (+5)
│   ├── 分页方式一致 (+5)
│   └── HATEOAS / 导航支持 (+5)
├── 可发现性 (20)
│   ├── OpenAPI/AsyncAPI 规范 (+10)
│   ├── 交互式文档 (+5)
│   └── 代码示例 (+5)
├── 稳定性 (20)
│   ├── 版本策略文档化 (+5)
│   ├── 变更日志 (+5)
│   ├── 弃用通知机制 (+5)
│   └── SLA 承诺 (+5)
├── SDK 支持 (15)
│   ├── 官方 SDK (+10)
│   └── 社区 SDK (+5)
├── 性能 (15)
│   ├── p99 延迟 < 500ms (+5)
│   ├── 可用性 > 99.9% (+5)
│   └── 速率限制合理 (+5)
└── 安全性 (10)
    ├── OAuth 2.1 / OIDC (+5)
    └── 审计日志 (+5)
```

---

## 6. 案例：Stripe API 设计对功能复用的最佳实践

### 6.1 Stripe API 的设计原则

Stripe 被广泛认为是 REST API 设计的典范，其设计原则直接支持功能复用：

| 原则 | 实现 | 复用价值 |
|:---|:---|:---|
| **资源导向** | `/customers`, `/charges`, `/subscriptions` | 清晰的资源模型，易于理解和复用 |
| **幂等性** | `Idempotency-Key` 头 | 安全重试，消费者无需复杂去重逻辑 |
| **扩展性** | 所有对象包含 `metadata` 字典 | 消费者可扩展数据模型而不破坏接口 |
| **一致性** | 统一的错误格式、分页、过滤 | 学习一次，复用到所有端点 |
| **版本管理** | 日期版本（如 `2024-09-30.acacia`） | 消费者锁定版本，不受变更影响 |
| **SDK 生态** | 官方支持 10+ 语言 | 多语言团队均可复用 |

### 6.2 Stripe API 的复用模式

```
Stripe API 复用模式
├── 直接复用：调用 Stripe API 实现支付功能
├── 模式复用：采用 Stripe 的资源命名和错误处理模式
├── SDK 复用：复用 Stripe 的 SDK 设计模式构建内部 SDK
└── 文档复用：采用 Stripe 的文档风格和组织结构
```

---

## 7. 权威来源

| 来源 | URL | 核查日期 |
|:---|:---|:---|
| OpenAPI 3.1 | <https://spec.openapis.org/oas/v3.1.0> | 2026-06-10 |
| GraphQL Spec | <https://spec.graphql.org/> | 2026-06-10 |
| gRPC | <https://grpc.io/> | 2026-06-10 |
| AsyncAPI | <https://www.asyncapi.com/> | 2026-06-10 |
| JSON:API | <https://jsonapi.org/> | 2026-06-10 |
| Stripe API Docs | <https://docs.stripe.com/api> | 2026-06-10 |
| Richardson Maturity Model | <https://martinfowler.com/articles/richardsonMaturityModel.html> | 2026-06-10 |
