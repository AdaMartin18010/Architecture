# 03 应用架构复用

## 定位

系统级复用层次。覆盖从单体到 Serverless 的完整云原生架构模式，以及数据架构复用。

## 核心内容

- **Level 1**: 应用系统复用（COTS/GOTS/SaaS/多租户）
- **Level 2**: 应用组件复用（内部开源、组件库、共享服务）
- **Level 3**: 应用服务复用（API 网关、服务网格、事件总线）
- **Level 4**: 数据架构复用（MDM、数据网格、数据产品）
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
- [x] 2026 云原生架构模式复用性矩阵 (`05-cloud-native-patterns/reusability-matrix-2026.md`)
- [x] 服务网格通信模式复用 (`06-service-mesh/service-mesh-communication-patterns.md`)
- [x] Data Mesh 域导向复用深化 (`04-data-architecture/data-mesh-data-product-reuse.md`)
- [ ] 具体平台（Backstage、Port、Cortex）的 IDP 复用实践 (P1, 2026-Q4)

## 关联主题

- `04-component-architecture-reuse`（应用组件降维到组件层）
- `05-functional-architecture-reuse`（Serverless/FaaS 功能级复用）
