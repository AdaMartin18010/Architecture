# 02 微服务架构复用

> **版本**: 2026-07-07
> **定位**: 03 应用架构复用的基础子主题 — 微服务架构的复用模式
> **对齐**: CNCF, NIST SP 800-204, ISO/IEC 25010:2023
> **状态**: ✅ 核心内容已填充

---

## 核心内容

1. **概念定义（CARC 本体）**：微服务、独立部署、去中心化数据、轻量级通信、容错设计。
2. **概念谱系**：从 SOA、REST、Amazon 服务化到 Netflix OSS、Kubernetes、Service Mesh。
3. **核心复用模式**：API 契约复用、Sidecar/Ambassador、Anti-Corruption Layer、Strangler Fig、BFF、Saga。
4. **服务边界与粒度**：实体级、聚合级、业务能力级、子域级服务的取舍。
5. **示例与反例**：支付服务复用、共享数据库反模式、分布式单体、过度拆分。
6. **多维矩阵**：微服务设计模式 × 适用场景、微服务 vs 分层架构 vs 模块化单体。
7. **场景决策树**：根据团队规模、业务边界清晰度、DevOps 能力选择是否采用微服务。

## 主文档

- **[reuse-patterns.md](reuse-patterns.md)** — 微服务架构复用模式完整指南

## 关联主题

- `03/01-layered-architecture`（从单体分层到微服务的拆分）
- `03/08-service-mesh`（服务网格通信复用）
- `04/07-language-ecosystems`（多语言微服务的组件复用）
- `01-meta-model-standards/06-formal-axioms/four-layer-ontology.md`（四层架构概念本体）

---

> **权威来源**:
>
> - Fowler, M., & Lewis, J. (2014). *Microservices*.
> - Newman, S. (2021). *Building Microservices* (2nd ed.).
> - Richardson, C. (2018). *Microservices Patterns*.
> - NIST SP 800-204.
>
> **核查日期**: 2026-07-07


---

## 补充说明：02 微服务架构复用

## 概念定义

**定义**：微服务架构将系统拆分为围绕业务能力组织、可独立部署的小服务，服务间通过轻量级机制通信；微服务复用强调跨团队共享服务与 API 契约。

## 示例

**示例**：企业将用户画像、消息通知、文件存储构建为独立微服务，通过OpenAPI 契约供各业务线复用，降低重复开发。

## 反例

**反例**：为追求复用将两个高内聚但变更频率不同的业务能力强行合并为一个微服务，导致发布耦合与团队摩擦。

## 分析

**分析**：微服务复用需要清晰的领域边界与版本治理，否则共享服务会成为跨团队协作瓶颈。
