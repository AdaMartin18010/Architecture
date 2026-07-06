# 03 应用架构复用

## 定位

系统级复用层次。覆盖从单体到 Serverless 的完整云原生架构模式，以及数据架构复用。

## 核心内容

- **Level 1**: 应用系统复用（COTS/GOTS/SaaS/多租户）
- **Level 2**: 应用组件复用（内部开源、组件库、共享服务）
- **Level 3**: 应用服务复用（API 网关、服务网格、事件总线）
- **Level 4**: 数据架构复用（MDM、数据网格、数据产品）
- **四层架构概念本体（CARC）**: [`01-meta-model-standards/06-formal-axioms/four-layer-ontology.md`](../01-meta-model-standards/06-formal-axioms/four-layer-ontology.md)
- 云原生架构模式复用性矩阵（2026 版）
  - 单体 / 模块化单体 / SOA / 微服务 / 微前端 / Serverless / 服务网格 / EDA / 模块化宏服务
- 服务网格 (Istio/Envoy/Cilium) 的通信模式复用
- 事件驱动架构 (EDA) 的四种复用模式
- 数据网格 (Data Mesh) 的域导向复用

## 权威对齐

- [CNCF Cloud Native Trail Map](https://landscape.cncf.io)
- [Spring Modulith](https://spring.io/projects/spring-modulith) (模块化单体)
- [Istio Architecture](https://istio.io/latest/docs/ops/deployment/architecture/)
- [Data Mesh by Zhamak Dehghani](https://martinfowler.com/articles/data-mesh-intro.html)

## 关键定理
>
> **定理 3.2** (Data-Application Coupling): 数据架构与应用架构的复用独立当且仅当数据访问通过**抽象数据服务**而非**直接存储耦合**实现。

## 当前状态

- [x] 架构模式对比矩阵
- [x] 场景应用树
- [x] 2026 云原生架构模式复用性矩阵 (`07-cloud-native-patterns/reusability-matrix-2026.md`)
- [x] 服务网格通信模式复用 (`08-service-mesh/service-mesh-communication-patterns.md`)
- [x] Data Mesh 域导向复用深化 (`05-data-architecture/data-mesh-data-product-reuse.md`)
- [x] 分层架构复用框架 (`01-layered-architecture/`)
- [x] 微服务架构复用框架 (`02-microservices/`)
- [x] 应用服务复用框架 (`03-app-service/`)
- [x] Serverless 架构复用框架 (`04-serverless/`)
- [x] 事件驱动架构复用框架 (`06-event-driven/`)
- [x] 具体平台（Backstage、Port、Cortex）的 IDP 复用实践 (`11-idp-practices/backstage-port-cortex.md`)

## 子目录导航

| 子目录 | 主题 | 核心文档 | 状态 |
|:---|:---|:---|:---:|
| `01-layered-architecture/` | 分层架构复用模式 | [`reuse-patterns.md`](01-layered-architecture/reuse-patterns.md) | ✅ 已填充 |
| `02-microservices/` | 微服务架构复用模式 | [`reuse-patterns.md`](02-microservices/reuse-patterns.md) | ✅ 已填充 |
| `03-app-service/` | 应用服务复用 | — | ✅ 核心文档 |
| `04-serverless/` | Serverless/FaaS 复用模式 | [`reuse-patterns.md`](04-serverless/reuse-patterns.md) | ✅ 已填充 |
| `05-data-architecture/` | 数据架构复用（Data Mesh） | — | ✅ 核心文档 |
| `06-event-driven/` | 事件驱动架构复用模式 | [`reuse-patterns.md`](06-event-driven/reuse-patterns.md) | ✅ 已填充 |
| `07-cloud-native-patterns/` | 云原生架构模式复用性矩阵 | [`reusability-matrix-2026.md`](07-cloud-native-patterns/reusability-matrix-2026.md) | ✅ |
| `08-service-mesh/` | 服务网格通信复用 | — | ✅ |
| `09-eda-cqrs/` | EDA/CQRS 深度内容 | — | ✅ |
| `10-tosca-dmn-platform/` | TOSCA v2.0 / DMN 1.6 平台对齐 | — | ✅ |
| `11-idp-practices/` | IDP（Backstage/Port/Cortex）复用实践 | [`backstage-port-cortex.md`](11-idp-practices/backstage-port-cortex.md) | ✅ 已填充 |

## 关联主题

- `01-meta-model-standards/06-formal-axioms/four-layer-ontology.md`（四层架构概念本体）
- `04-component-architecture-reuse`（应用组件降维到组件层）
- `05-functional-architecture-reuse`（Serverless/FaaS 功能级复用）


---

## 补充说明：03 应用架构复用

## 概念定义

**定义**：应用架构复用是在系统层面复用应用、服务、模式与基础设施配置，包括分层架构、微服务、Serverless、事件驱动、服务网格等形态。

## 示例

**示例**：某 SaaS 企业建立内部平台团队，提供可复用的 CI/CD 流水线、可观测性套件与多租户数据隔离模板，新产品团队可在数天内搭建生产级服务。

## 反例

**反例**：各产品团队独立选型技术栈与部署模式，导致安全补丁、监控与容量管理无法统一治理。

## 权威来源

> **权威来源**:
>
> - [CNCF](https://www.cncf.io)
> - [NIST](https://www.nist.gov)
> - 核查日期：2026-07-07
