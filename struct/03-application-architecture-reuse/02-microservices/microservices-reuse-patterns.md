# 微服务架构复用模式

> **版本**: 2026-06-08
> **定位**: 应用架构层（Level 2）—— 微服务粒度边界、边车模式与 API 契约复用
> **对齐标准**: CNCF Cloud Native Trail Map, NIST SP 800-204
> **状态**: ⏳ 框架填充中

---

## 1. 核心概念

微服务架构将应用拆分为**围绕业务能力组织、可独立部署的服务集合**。与单体架构相比，微服务的复用逻辑发生了本质变化：复用单元从"代码库"转变为"服务契约 + 运行实例"。

NIST SP 800-204 (Security Strategies for Microservices-based Application Systems) 指出：微服务复用的核心挑战在于**如何在保持服务自治的前提下实现安全、可控的跨团队复用**。

### 1.1 复用粒度边界

| 粒度 | 复用单元 | 适用场景 | 反模式 |
|------|---------|---------|--------|
| 细粒度（函数/类） | 共享 SDK / Sidecar | 横切关注点（日志、监控、认证） | 分布式单体 |
| 中粒度（服务/模块） | 完整微服务 | 用户服务、订单服务、支付服务 | 共享数据库 |
| 粗粒度（服务组/API） | API 网关聚合层 | BFF (Backend for Frontend) | 过度聚合 |

> **定理 M.1** (Service Reuse Granularity): 微服务的复用价值在服务粒度达到"一个业务能力 = 一个服务"时最大。粒度过细导致编排成本超过复用收益；粒度过粗则退化为分布式单体。

---

## 2. 核心复用模式

### 2.1 Sidecar 模式

将横切关注点（如日志、监控、TLS、服务发现）从主服务中剥离，以**独立进程**形式部署在同一 Pod/主机中。

- **复用边界**: Sidecar 二进制镜像
- **典型实现**: Envoy (服务代理), Fluent Bit (日志), OAuth2 Proxy (认证)
- **对齐**: CNCF 推荐的云原生基础模式

### 2.2 Ambassador 模式

Sidecar 的变体，专门用于**代理主服务与外部资源的连接**。例如：主服务通过本地 Ambassador 访问外部数据库，Ambassador 处理连接池、重试、断路等逻辑。

- **复用价值**: 连接逻辑与业务逻辑解耦，同一 Ambassador 可复用于多个服务
- **与 Sidecar 的区别**: Ambassador 代理出向连接，Sidecar 通常代理入向/双向

### 2.3 Anti-Corruption Layer (ACL)

当复用一个遗留系统或外部服务时，在边界处引入**防腐层**，将外部模型转换为内部领域模型。

- **复用价值**: 保护领域模型不被外部变更污染
- **成本**: 需要维护翻译映射，增加一层间接性
- **决策点**: 当外部系统变更频率 > 每季度一次时，ACL 的 ROI 为正

### 2.4 Strangler Fig 模式

逐步用微服务替换遗留系统的功能，通过**拦截层**将流量路由到新服务或旧系统。

- **复用路径**: 旧系统的部分功能被新服务替代后，新服务可被其他业务线复用
- **风险控制**: 回退机制确保替换失败时可切回旧系统

---

## 3. API 契约复用

微服务的真正复用边界是 **API 契约**，而非代码实现。

| 契约层级 | 形式 | 复用方式 |
|---------|------|---------|
| 协议 | REST / gRPC / GraphQL | 技术栈无关复用 |
| 接口定义 | OpenAPI / Protobuf Schema | 生成客户端/服务端 Stub |
| 数据模型 | JSON Schema / DTO | 跨服务共享领域语言 |
| 行为契约 | Pact / Consumer-Driven Contract | 运行时兼容性验证 |

> **定理 M.2** (API Contract Stability): API 契约的复用价值与其稳定性正相关。遵循**语义化版本控制（SemVer）**的 API，其 Major 版本变更应 ≤ 每年 1 次。

---

## 4. 安全复用约束（NIST SP 800-204 对齐）

- **零信任边界**: 即使内部复用，服务间通信也应经过 mTLS + 认证
- **最小权限 Sidecar**: Sidecar 不应拥有超出其代理范围的权限
- **API 网关作为安全复用层**: 统一处理速率限制、审计、威胁检测

---

> 最后更新: 2026-06-08
> 权威来源:
>
> - <https://landscape.cncf.io> (CNCF Cloud Native Trail Map)
> - <https://csrc.nist.gov/publications/detail/sp/800-204/final> (NIST SP 800-204)
> - <https://docs.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer>
