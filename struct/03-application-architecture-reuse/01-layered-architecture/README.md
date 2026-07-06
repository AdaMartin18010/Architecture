# 01 分层架构复用

> **版本**: 2026-07-07
> **定位**: 03 应用架构复用的基础子主题 — 分层架构的复用模式与决策
> **对齐**: ISO/IEC/IEEE 42010:2022, SWEBOK v4, TOGAF 10
> **状态**: ✅ 核心内容已填充

---

## 核心内容

1. **概念定义（CARC 本体）**：分层架构、层、接口契约、单向依赖、可替换性。
2. **概念谱系**：从 Dijkstra 的分层系统到 Clean Architecture、Onion Architecture、Ports & Adapters。
3. **核心复用模式**：严格分层、松散分层、Clean Architecture、Onion Architecture、Ports & Adapters。
4. **层间依赖规则**：依赖方向、循环依赖禁止、接口稳定性约束。
5. **示例与反例**：Repository 跨项目复用、Controller 直接调用 DAO、框架注解污染领域对象。
6. **多维矩阵**：分层模式 × 复用维度、分层架构 vs 微服务 vs Serverless vs EDA。
7. **场景决策树**：根据团队规模、DDD 熟悉度、UI/数据库多样性选择分层模式。

## 主文档

- **[reuse-patterns.md](reuse-patterns.md)** — 分层架构复用模式完整指南

## 关联主题

- `03/02-microservices`（分层到微服务的演进）
- `03/07-cloud-native-patterns`（云原生模式对比）
- `04/04-design-patterns`（层内设计模式）
- `01-meta-model-standards/06-formal-axioms/four-layer-ontology.md`（四层架构概念本体）

---

> **权威来源**:
>
> - Buschmann et al. (1996). *Pattern-Oriented Software Architecture, Volume 1*.
> - Martin, R. C. (2012). *The Clean Architecture*.
> - ISO/IEC/IEEE 42010:2022.
>
> **核查日期**: 2026-07-07


---

## 补充说明：01 分层架构复用

## 概念定义

**定义**：分层架构将系统划分为表示层、应用层、领域层与基础设施层等水平层次，每层通过稳定接口向上层提供服务，实现层内复用与层间解耦。

## 示例

**示例**：电商平台将订单领域层封装为独立模块，供 Web、App、小程序等表示层复用，业务规则只需在领域层维护一份。

## 反例

**反例**：表示层直接访问数据库，绕过领域层，导致业务规则散落于多个层次，无法复用和一致性维护。

## 分析

**分析**：分层架构复用的有效性取决于层间依赖规则的严格执行，否则容易退化为“大泥球”。
