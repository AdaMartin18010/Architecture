# 04 事件驱动架构复用

> **版本**: 2026-07-07
> **定位**: 03 应用架构复用的基础子主题 — 事件驱动架构（EDA）的复用模式
> **对齐**: CNCF, OASIS, CloudEvents, ISO/IEC/IEEE 42010:2022
> **状态**: ✅ 核心内容已填充

---

## 核心内容

1. **概念定义（CARC 本体）**：事件、生产者、消费者、代理、事件契约、不可变性、最终一致性。
2. **概念谱系**：从观察者模式、发布-订阅、EIP、CEP 到 Kafka、CloudEvents、Event Mesh。
3. **核心复用模式**：Event Notification、Event-Carried State Transfer、Event Sourcing、CQRS、Saga、Event Mesh。
4. **事件契约与 Schema 治理**：CloudEvents 规范、Schema Registry、向后兼容。
5. **示例与反例**：电商订单事件流、IoT 遥测处理、EDA 当作 RPC、缺乏 Schema 治理。
6. **多维矩阵**：EDA 模式 × 适用场景、EDA vs 同步 API vs 批处理。
7. **场景决策树**：根据解耦需求、事实 vs 命令、审计需求选择 EDA 模式。

## 主文档

- **[reuse-patterns.md](reuse-patterns.md)** — 事件驱动架构复用模式完整指南

## 关联主题

- `03/09-eda-cqrs`（EDA/CQRS 深度内容）
- `05/03-event-functions`（功能层的事件函数复用）
- `12/02-a2a-protocol`（A2A 协议中的事件/消息交互）
- `01-meta-model-standards/06-formal-axioms/four-layer-ontology.md`（四层架构概念本体）

---

> **权威来源**:
>
> - Hohpe, G., & Woolf, B. (2003). *Enterprise Integration Patterns*.
> - CNCF. *CloudEvents Specification*.
> - Kleppmann, M. (2017). *Designing Data-Intensive Applications*.
> - ISO/IEC/IEEE 42010:2022.
>
> **核查日期**: 2026-07-07


---

## 补充说明：04 事件驱动架构复用

## 概念定义

**定义**：事件驱动架构（EDA）通过事件的生产、检测、消费与响应解耦系统组件，事件模式与 Schema 的复用是实现跨系统互操作的关键。

## 示例

**示例**：零售企业定义标准“订单已创建”事件 Schema，并在事件总线注册，库存、物流、营销系统均按同一 Schema 消费，避免重复集成。

## 反例

**反例**：各团队自行定义“订单”事件格式，导致同一业务事件在系统间传递时需要多次格式转换与映射。

## 分析

**分析**：事件 Schema 治理是 EDA 复用的核心，Schema Registry 与版本兼容策略不可或缺。