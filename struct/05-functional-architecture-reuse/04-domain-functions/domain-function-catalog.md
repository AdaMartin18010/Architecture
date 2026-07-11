# 领域函数目录

> **版本**: 2026-07-08
> **定位**: 功能架构层 —— 基于领域驱动设计（DDD）的细粒度可复用函数目录
> **对齐标准**: Domain-Driven Design (Evans 2003), Functional Programming, DMN 1.5, Serverless Functions
> **状态**: ✅ 已完成

---

## 目录

- [领域函数目录](#领域函数目录)
  - [目录](#目录)
  - [1. 领域函数的定义](#1-领域函数的定义)
  - [2. 领域函数 vs. 应用服务 vs. 基础设施函数](#2-领域函数-vs-应用服务-vs-基础设施函数)
  - [3. 领域函数目录模板](#3-领域函数目录模板)
  - [4. 可复用领域函数分类](#4-可复用领域函数分类)
    - [4.1 实体工厂函数](#41-实体工厂函数)
    - [4.2 值对象计算函数](#42-值对象计算函数)
    - [4.3 领域规则判断函数](#43-领域规则判断函数)
    - [4.4 状态转换函数](#44-状态转换函数)
    - [4.5 聚合校验函数](#45-聚合校验函数)
  - [5. 与权威框架/标准的条款映射](#5-与权威框架标准的条款映射)
  - [6. 正例](#6-正例)
    - [正例 1：统一税率计算函数库](#正例-1统一税率计算函数库)
    - [正例 2：医疗领域的剂量校验函数](#正例-2医疗领域的剂量校验函数)
  - [7. 反例](#7-反例)
    - [反例 1：隐藏在应用服务中的领域规则](#反例-1隐藏在应用服务中的领域规则)
    - [反例 2：领域函数依赖外部状态](#反例-2领域函数依赖外部状态)
  - [8. 权威来源](#8-权威来源)
  - [9. 交叉引用](#9-交叉引用)

---

## 1. 领域函数的定义

**定义** (Domain Function): 领域函数是封装单一领域规则、计算或状态转换逻辑的**纯函数**或**无副作用函数**。它直接表达领域专家使用的语言（Ubiquitous Language），是 DDD 战术设计在函数粒度上的复用单元。

形式化：

```text
DomainFunction := ⟨Name, Input, Output, Invariant, SideEffect⟩

Name: 动词+名词，来自统一语言（如 calculateTax）
Input: 领域对象或值对象集合
Output: 新的领域对象、值对象或判断结果
Invariant: 执行前后必须保持的领域不变量
SideEffect: 无；或仅允许显式声明的副作用（如审计日志）
```

> **原则**：领域函数应优先为纯函数（Pure Function），即相同输入必然产生相同输出，且不依赖或修改外部状态。这一特性使其天然适合复用、测试和并行执行。

---

## 2. 领域函数 vs. 应用服务 vs. 基础设施函数

| 维度 | 领域函数 | 应用服务 | 基础设施函数 |
|---|---|---|---|
| 关注点 | 领域规则、计算、不变量 | 用例编排、事务边界 | 技术实现（存储、消息、HTTP） |
| 副作用 | 无（或显式声明） | 可协调多个领域操作 | 通常有 I/O 副作用 |
| 复用范围 | 跨用例、跨应用、跨服务 | 限定于特定用例 | 限定于特定技术栈 |
| 测试方式 | 单元测试（输入→输出） | 集成测试 | 集成测试 / Mock |
| 示例 | `calculateVAT`, `isEligibleForDiscount` | `placeOrder`, `processRefund` | `saveOrderToDB`, `sendEmail` |

> **分层规则**：领域函数只依赖领域层内的实体、值对象和领域服务；不直接调用应用层或基础设施层。

---

## 3. 领域函数目录模板

| 字段 | 说明 | 示例 |
|---|---|---|
| 函数 ID | 唯一标识 | DF-ORDER-001 |
| 函数名称 | 动词+名词，来自统一语言 | calculateOrderTotal |
| 所属领域 | 限界上下文 | 订单域 / Order Context |
| 输入 | 参数类型与含义 | Order, List<OrderLine> |
| 输出 | 返回值类型与含义 | Money (含税总价) |
| 不变量 | 执行前后必须保持的规则 | 总价 ≥ 0；税额 = 税基 × 税率 |
| 复用等级 | 上下文内 / 跨上下文 / 企业级 | 企业级 |
| 实现语言 | 可存在多语言实现 | Python / TypeScript / Java |
| 对应 DMN | 若适用，关联决策表 | DT-PRICING-001 |

---

## 4. 可复用领域函数分类

### 4.1 实体工厂函数

将领域对象的创建逻辑集中封装，避免在多处重复复杂的构造规则。

```python
def create_order(customer_id: CustomerId, lines: List[OrderLine]) -> Order:
    """创建订单，确保至少包含一个订单行且客户 ID 有效。"""
    if not lines:
        raise ValueError("订单必须包含至少一个订单行")
    return Order(id=OrderId.new(), customer_id=customer_id, lines=lines, status=OrderStatus.PENDING)
```

### 4.2 值对象计算函数

对金额、数量、比率、坐标等值对象进行计算，保证数学语义正确。

```python
def calculate_vat(amount: Money, rate: Decimal) -> Money:
    """计算增值税，结果按货币精度截断。"""
    return Money((amount.value * rate).quantize(amount.currency.precision), amount.currency)
```

### 4.3 领域规则判断函数

将业务规则封装为可复用的布尔判断函数，供流程、UI、AI Agent 共同使用。

```python
def is_eligible_for_bulk_discount(order: Order) -> bool:
    """当订单总行数 ≥ 100 或总金额 ≥ 10,000 时适用批量折扣。"""
    return len(order.lines) >= 100 or order.total.amount >= Decimal("10000")
```

### 4.4 状态转换函数

明确定义聚合根或实体状态机的合法转换，避免非法状态迁移。

```python
def pay_order(order: Order, payment: Payment) -> Order:
    """将订单从 PENDING 转移到 PAID，前提为支付金额等于订单金额。"""
    if order.status != OrderStatus.PENDING:
        raise DomainError("只有待支付订单可被支付")
    if payment.amount != order.total:
        raise DomainError("支付金额与订单金额不一致")
    return order.with_status(OrderStatus.PAID)
```

### 4.5 聚合校验函数

在持久化或发布事件前，验证聚合内部一致性。

```python
def validate_inventory_reservation(reservation: InventoryReservation) -> ValidationResult:
    """校验库存预留是否满足可用库存约束。"""
    if reservation.quantity > reservation.product.available_quantity:
        return ValidationResult.fail("预留数量超过可用库存")
    return ValidationResult.ok()
```

---

## 5. 与权威框架/标准的条款映射

| 本主题概念 | 对应标准/文献 | 映射说明 |
|:---|:---|:---|
| 领域函数 | DDD (Evans, 2003) | 战术设计中的领域逻辑单元，对应 Entity / Value Object / Domain Service 中的行为 |
| 统一语言 | DDD Strategic Design | 函数命名必须来自领域专家与开发者共享的语言 |
| 限界上下文 | DDD Strategic Design | 函数复用边界由 Bounded Context 决定 |
| 聚合不变量 | DDD Tactical Design | 函数执行前后需保持聚合内部一致性 |
| 纯函数 | Functional Programming | 无副作用、引用透明，便于并发与复用 |
| 类型状态 | Typestate Pattern | 通过类型系统强制合法状态转换 |
| 业务规则复用 | DMN 1.5 §6 Decision Service | 复杂判断逻辑可映射为 DMN 决策服务，供函数调用 |
| 函数部署 | Serverless Functions (FaaS) | 领域函数可作为无服务器函数部署，事件触发 |

---

## 6. 正例

### 正例 1：统一税率计算函数库

**背景**：某跨国 SaaS 公司的订单、发票、报销、财务报告四个系统分别实现了税率计算逻辑。

**复用实践**：

1. 识别"计算税费"为跨上下文的领域函数，定义统一输入（金额、税种、地区、时间）。
2. 用纯函数实现核心计算，覆盖增值税、消费税、地方附加税。
3. 在各系统中以库形式引入，版本通过 SemVer 管理。
4. 税务政策变更时，仅修改函数库并发布新版本。

**效果**：

- 税率调整上线时间从 2 周缩短至 2 天。
- 四个系统计算结果一致性从 92% 提升至 99.9%。
- 审计时可直接展示函数版本与计算规则对应关系。

### 正例 2：医疗领域的剂量校验函数

**背景**：某医院信息系统需要在挂号、药房、护理、计费多个模块中校验药品剂量是否超量。

**复用实践**：

1. 将"校验药品剂量"抽象为领域函数 `validate_dosage(patient, medication, dose)`。
2. 函数内部封装年龄、体重、肝肾功能、药物相互作用等规则。
3. 通过 DMN 决策表管理可变的剂量阈值规则。

**效果**：

- 新模块接入剂量校验只需调用函数，无需重写规则。
- 剂量相关医疗差错下降 45%。

---

## 7. 反例

### 反例 1：隐藏在应用服务中的领域规则

**场景**：某电商系统将"满减规则"直接写在订单应用服务的 `place_order` 方法中，与库存扣减、支付调用、消息发送等逻辑混合。

**问题**：

- 促销团队无法独立调整满减规则，必须提交 IT 需求。
- 同一满减规则在 App、小程序、B2B 平台中重复实现，规则不一致。
- 单元测试需要模拟整个下单流程，测试成本高昂。

**后果**：

- 一次双 11 促销因各平台规则实现不一致，导致客诉 3000+ 起。
- 后续重构时，无法安全提取规则，形成"大泥球"。

**避免建议**：

- 将"计算促销优惠"提取为独立领域函数 `calculate_promotion_discount`。
- 使用 DMN 决策表管理多变的促销规则。
- 应用服务只负责编排，不实现领域规则。

### 反例 2：领域函数依赖外部状态

**场景**：某团队将"汇率转换"实现为领域函数，但函数内部直接调用外部汇率 API 并缓存到全局变量。

**问题**：

- 函数不是纯函数，相同输入在不同时刻输出不同。
- 单元测试不稳定，需要 Mock 全局缓存和外部 API。
- 在高并发场景下出现汇率不一致，导致财务报表差异。

**避免建议**：

- 领域函数只接收汇率作为输入参数，不直接调用外部服务。
- 汇率获取由应用服务或防腐层（Anti-Corruption Layer）负责。
- 如需缓存，在调用方注入缓存后的汇率值。

---

## 8. 权威来源

> **权威来源**:
>
> - [Domain-Driven Design (Eric Evans)](https://www.domainlanguage.com/) — DDD 战术设计与统一语言；核查日期：2026-07-08
> - [Domain-Driven Design (Martin Fowler)](https://martinfowler.com/bliki/DomainDrivenDesign.html) — DDD 概述与战略设计；核查日期：2026-07-08
> - [OMG DMN 1.5 Specification](https://www.omg.org/spec/DMN/1.5/) — 决策服务与业务规则复用；核查日期：2026-07-08
> - [AWS Lambda Documentation](https://aws.amazon.com/lambda/) — Serverless Functions/FaaS；核查日期：2026-07-08
> - [Azure Functions Documentation](https://azure.microsoft.com/services/functions/) — Serverless Functions/FaaS；核查日期：2026-07-08
> - [Google Cloud Functions Documentation](https://cloud.google.com/functions) — Serverless Functions/FaaS；核查日期：2026-07-08
> - [Semantic Versioning 2.0.0](https://semver.org/) — 函数库版本管理；核查日期：2026-07-08
>
> **核查日期**: 2026-07-08

---

## 9. 交叉引用

- [功能架构复用概览](../README.md) — 功能复用五层层次结构
- [事件驱动函数复用模式](../03-event-functions/event-driven-function-reuse.md) — 事件触发下的函数复用
- [工作流编排复用模式](../04-workflow-orchestration/temporal-reuse-patterns.md) — 长事务与 Saga 中的领域函数编排
- [AI/LLM 功能复用模式](../05-ai-llm-functions/llm-function-reuse-patterns.md) — AI 功能作为领域函数的扩展
- [组件接口契约设计模式](../../04-component-architecture-reuse/04-design-patterns/interface-design-patterns.md) — 函数级复用的接口契约原则
