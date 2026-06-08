# T13: 跨层复用映射的约束验证 (Alloy)

> **版本**: 2026-06-06
> **对应规约**: `cross-layer-mapping.als`
> **交叉引用**: `struct/01-meta-model-standards/06-formal-axioms/axiom-system.md`
> **理论来源**: Jackson, D. *Software Abstractions*; ISO/IEC 42010:2022; TOGAF 10

---

## 1. 建模动机

在软件工程架构复用知识体系中，"跨层映射"是连接不同抽象层次的关键机制。业务架构（Business Architecture）中的价值流需要映射到应用架构（Application Architecture）中的服务，再映射到组件架构（Component Architecture）中的模块，最终映射到功能架构（Function Architecture）中的函数。这种映射不是随意的——它必须满足严格的结构约束。

Daniel Jackson 在《Software Abstractions》中强调："建模的目的不是描述系统的所有细节，而是捕获那些最可能导致设计错误的约束。"跨层复用映射中最常见的两类错误是：

1. **跳跃式映射**：业务层资产直接映射到组件层资产，跳过应用层，导致应用层架构缺失。
2. **关注点冲突**：同一非功能性关注点（如安全、性能）在不同层次被映射到相互矛盾的实现上。

本 Alloy 规约将 ISO 42010 的架构描述概念和 TOGAF 的架构 continuum 形式化，通过 SAT 求解自动检测上述错误。

---

## 2. 签名设计：四层抽象模型

### 2.1 Layer（层次）

```alloy
abstract sig Layer {}
sig BusinessLayer extends Layer {}
sig ApplicationLayer extends Layer {}
sig ComponentLayer extends Layer {}
sig FunctionLayer extends Layer {}
```

四层抽象对应于本知识体系的一级主题划分：`02-business-architecture-reuse`、`03-application-architecture-reuse`、`04-component-architecture-reuse`、`05-functional-architecture-reuse`。使用 `extends` 而非 `in` 确保四层是互不相交的集合，符合 TOGAF 中"层次不可约"（Hierarchy Non-Reduction）的语义。

### 2.2 Asset（资产）

`Asset` 是各层次中可复用的架构元素。按层次细分为 `BusinessAsset`、`ApplicationAsset`、`ComponentAsset`、`FunctionAsset`。每个资产关联一组 `concerns`，对应 ISO 42010 中的"stakeholder concern"概念。

### 2.3 Mapping（映射）

`Mapping` 是本规约的核心关系签名。它不只是一个二元关系，而是一个具有自身属性的独立实体——包含 `source`、`target`、`realizes`（关注点集合）和 `mappingType`（精化或实现）。这种设计体现了 Jackson 所倡导的"将关系提升为一等公民"的建模风格，使得映射本身可以被约束、被断言、被可视化。

---

## 3. 核心约束解析

### F3: AdjacentLayerMapping（相邻层映射）

```alloy
fact AdjacentLayerMapping {
    all m: Mapping |
        (m.source in BusinessAsset implies m.target in ApplicationAsset) and
        (m.source in ApplicationAsset implies m.target in ComponentAsset) and
        (m.source in ComponentAsset implies m.target in FunctionAsset) and
        (m.source in FunctionAsset implies m.target in ComponentAsset)
```

这一约束形式化了 `struct/01-meta-model-standards/06-formal-axioms/axiom-system.md` 中的 **S.4 Abstraction Layering**（抽象分层）公理：

> "任何资产只能依赖同层或其直接下层资产。"

在 Alloy 中，我们将"依赖"具体化为"映射目标"，将"同层或直接下层"具体化为相邻层约束。允许 `ComponentAsset -> FunctionAsset` 的双向映射，是因为组件层和功能层之间存在紧密的往返关系：组件精化为函数，函数又反过来实现组件接口。

### F4: ConcernConsistency（关注点一致性）

```alloy
fact ConcernConsistency {
    all c: Concern |
        all disj m1, m2: Mapping |
            c in m1.realizes and c in m2.realizes implies
                (m1.target = m2.target or m1.source != m2.source)
}
```

这一约束解决了跨层映射中最微妙的问题：关注点漂移。假设业务层有一个"数据加密"关注点，映射到应用层的"TLS 传输加密"；同时同一个"数据加密"关注点又映射到组件层的"明文存储"——这就构成了关注点冲突。`disj` 关键字表示 m1 和 m2 是不同的映射实例，约束要求它们要么映射到同一目标，要么源自不同源资产。

---

## 4. 断言与验证

| 断言 | 约束内容 | 对应公理 |
|------|---------|---------|
| `AllMappingsAreAdjacent` | 映射仅发生在相邻层 | S.4 Abstraction Layering |
| `NoConcernConflicts` | 同一关注点不映射到冲突实现 | M.1 Architecture-Reuse Duality |
| `NoReverseMapping` | 映射方向只能从高层到低层 | M.3 Hierarchy Non-Reduction |

所有断言均通过 `check` 命令在有限 scope 内验证。若 `AllMappingsAreAdjacent` 失败，Alloy 将生成一个具体反例：例如一个从 `BusinessAsset` 指向 `ComponentAsset` 的 `Mapping` 实例。可视化图中，源和目标以不同颜色显示，违规映射以红色高亮，便于架构师快速定位设计缺陷。

---

## 5. 反例教学：跳跃式映射的危害

若要观察跳跃式映射的反例，可临时注释掉 `F3`，执行：

```alloy
run CrossLayerMapping for 3 but 4 Mapping
```

Alloy 可能生成如下反例结构：

```
BusinessAsset: "客户订单管理"
  └── Mapping [realizes: 数据一致性]
      └── ComponentAsset: "OrderRepositoryImpl"   -- 跳过 ApplicationLayer!
```

在这个反例中，业务概念"客户订单管理"直接映射到了组件实现"OrderRepositoryImpl"，中间没有应用层服务（如 `OrderService`）作为桥梁。这会导致：

1. **业务逻辑泄漏**：业务规则被硬编码在组件实现中，无法独立演化。
2. **复用退化**：当另一个应用需要复用"客户订单管理"时，它被迫直接依赖 `OrderRepositoryImpl`，而非更稳定的应用层接口。
3. **测试困难**：没有应用层抽象，单元测试必须直接操作组件实现，增加了测试脆弱性。

这与 `01-meta-model-standards/06-formal-axioms/axiom-system.md` 中 **M.3 Hierarchy Non-Reduction** 的论断一致："某一层的复用失败不能通过另一层的优化完全弥补。"

---

## 6. 与元模型标准的交叉引用

- `01-meta-model-standards/06-formal-axioms/axiom-system.md`：本规约是 15 条公理中 S.1–S.4 的 Alloy 实例化。特别是 S.4（Abstraction Layering）和 S.2（Compositionality）直接指导了 `AdjacentLayerMapping` 和 `ConcernConsistency` 的设计。
- `01-meta-model-standards/04-archimate-4/archimate-iso-mapping.md`：ArchiMate 3.2 的关系类型（serving、realization、aggregation）与本规约中的 `MappingType`（Refinement、Realization）语义对应；ArchiMate 4.0 预览内容尚未获官方正式发布确认。
- `01-meta-model-standards/02-togaf-10-alignment/detailed-mapping.md`：TOGAF 的 Architecture Continuum（基础→通用→行业→特定组织）与本规约的四层抽象模型同构。

---

## 7. 权威来源

1. Jackson, D. (2012). *Software Abstractions: Logic, Language, and Analysis* (Revised ed.). MIT Press. —— Alloy 建模方法论与"小范围建模，大思路验证"哲学。
2. ISO/IEC/IEEE 42010:2022. *Software, systems and enterprise — Architecture description*. —— 架构描述、关注点、对应关系（correspondence）的权威标准。
3. The Open Group. (2022). *TOGAF Standard, Version 10*. —— 架构层次、架构连续体（Architecture Continuum）的定义。
4. Bunge, M. (1977). *Treatise on Basic Philosophy: Ontology I: The Furniture of the World*. D. Reidel. —— BWW 本体论中的系统层次与不可约性原理。

---

> 最后更新: 2026-06-06
