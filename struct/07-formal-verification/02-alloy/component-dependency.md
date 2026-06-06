# T11: 组件依赖无环性验证 (Alloy)

> **版本**: 2026-06-06
> **对应规约**: `component-dependency.als`
> **交叉引用**: `struct/04-component-architecture-reuse/`（依赖管理、组件架构复用）
> **理论来源**: Daniel Jackson, *Software Abstractions: Logic, Language, and Analysis* (MIT Press, 2012); Alloy Tools (<https://alloytools.org>)

---

## 1. 建模直觉

在软件架构复用中，组件依赖图（Component Dependency Graph, CDG）是最核心的静态结构之一。Daniel Jackson 在《Software Abstractions》中指出："大多数软件设计的深层错误并非算法错误，而是结构错误——对象之间的关系违背了设计者未曾言明的假设。"循环依赖正是这类结构错误中最典型的一种。

本 Alloy 规约将组件、模块、依赖关系建模为集合与关系，通过 SAT 求解器在有限 scope 内自动搜索反例，验证"系统中不存在循环依赖"这一架构约束。与单元测试不同，Alloy 的验证是穷举性的：只要在给定 scope 内存在任何违反断言的实例，Alloy Analyzer 都会生成最小的可视化反例。

---

## 2. 核心签名设计

### 2.1 Component（组件）

`Component` 被定义为抽象签名（`abstract sig`），下分为 `Interface` 和 `Implementation` 两个子签名。这种设计对应于面向组件架构中的"接口-实现分离"原则。`dependsOn` 是一个自反关系（`Component -> Component`），表示编译期或运行期的依赖方向。

```alloy
abstract sig Component {
    dependsOn: set Component,
    module: lone Module,
    version: one Version
}
```

`lone Module` 表示一个组件最多属于一个模块，但允许存在"游离"组件（用于建模第三方库或待分类组件）。

### 2.2 Module（模块）

`Module` 是组件的逻辑聚合单元，对应于 Maven 的 module、npm 的 package、Rust 的 crate。`members` 关系定义模块的成员，`imports` 定义模块间的导入关系。将依赖约束提升到模块级别，可以检测更高层次的循环导入（circular module imports），这在微服务架构和单体模块化中同样致命。

---

## 3. 关键事实约束

### F3: AcyclicDependency（无环依赖）

```alloy
fact AcyclicDependency {
    all c: Component | c not in c.^dependsOn
}
```

这是本规约的核心约束。`^dependsOn` 表示 `dependsOn` 关系的传递闭包（transitive closure）。`c not in c.^dependsOn` 禁止任何组件通过一条或多步依赖到达自身。在 Alloy 的基于 SAT 的语义中，这一约束排除了所有包含有向环的模型实例。

### F5: DependencyInversion（依赖倒置）

```alloy
fact DependencyInversion {
    all impl: Implementation |
        all dep: impl.dependsOn | dep in Interface
}
```

这一事实将 Robert C. Martin 的依赖倒置原则（DIP）形式化：实现类只能依赖于接口，不能直接依赖于其他实现类。在 Alloy 中，这种约束的表达是声明式的、紧凑的，无需遍历代码或 AST。

---

## 4. 断言与验证策略

本规约定义了三个断言，覆盖组件级、模块级和架构局部性三个维度：

| 断言 | 目的 | Scope |
|------|------|-------|
| `NoCircularDependencies` | 验证组件依赖图 DAG | 5 Component |
| `NoCircularModuleImports` | 验证模块导入图 DAG | 4 Module |
| `DependencyLocality` | 验证跨模块依赖必须通过导入声明 | 5 Component, 3 Module |

`check` 命令指示 Alloy Analyzer 在指定 scope 内搜索反例。若断言在 scope 内无反例，Alloy 返回 "no counterexample found"。虽然这并非数学上的绝对证明（受限于有限 scope），但正如 Jackson 所言："在大多数设计场景中，如果错误在 scope 为 5 时未出现，它在 scope 为 500 时也不会出现——因为错误通常是结构性的，而非规模性的。"

---

## 5. 循环依赖的危害：反例分析

若要观察循环依赖的 Alloy 反例，可临时注释掉 `F3` 和 `F4`，然后执行：

```alloy
run CyclicDependencyViolation for 4
```

Alloy Analyzer 将生成类似下图的实例：

```
Component_A -> dependsOn -> Component_B
Component_B -> dependsOn -> Component_C
Component_C -> dependsOn -> Component_A   -- 循环闭合
```

在真实系统中，这种循环会导致：

1. **构建不可判定**：构建工具（如 Maven、Cargo）无法确定编译顺序，导致构建失败或产生非确定性结果。
2. **测试不可隔离**：单元测试需要 mock 整个循环链，集成测试无法单独替换其中一个组件。
3. **部署顺序不可确定**：在微服务场景中，循环依赖意味着服务 A 的启动依赖于服务 B，而服务 B 又依赖于服务 A，导致级联启动失败。
4. **复用退化**：循环依赖的组件在逻辑上形成了一个"超级组件"，丧失了独立复用的价值。

这与 `struct/04-component-architecture-reuse/` 中提出的"依赖管理策略深度对比"相呼应：无论使用 Semver、范围依赖还是供应商化（vendoring），循环依赖都是架构层面的根本缺陷，无法通过版本策略弥补。

---

## 6. 与组件架构复用的交叉引用

- `04-component-architecture-reuse/07-language-ecosystems/open-source-supply-chain-reuse.md`：讨论了 Cargo、npm、Maven 的依赖解析算法。Alloy 规约中的 `AcyclicDependency` 是这些解析算法的前置条件——若依赖图含环，解析算法将陷入无限循环或产生不可预期的版本选择。
- `04-component-architecture-reuse/README.md` 公理 4.1（Interface Contract Completeness）：组件的可复用性取决于接口契约的完备性。`DependencyInversion` 事实正是这一公理在依赖关系上的形式化投射。

---

## 7. 权威来源

1. Jackson, D. (2012). *Software Abstractions: Logic, Language, and Analysis* (Revised ed.). MIT Press. —— Alloy 语言与设计哲学的权威教材。
2. Alloy Tools. <https://alloytools.org> —— MIT Software Design Group 维护的 Alloy 官方主页与文档。
3. Clements, P., & Northrop, L. (2001). *Software Product Lines: Practices and Patterns*. Addison-Wesley. —— 组件依赖与产品线工程中循环依赖的危害分析。
4. Martin, R. C. (2003). *Agile Software Development: Principles, Patterns, and Practices*. Prentice Hall. —— 依赖倒置原则（DIP）与无环依赖原则（Acyclic Dependencies Principle, ADP）。

---

> 最后更新: 2026-06-06
