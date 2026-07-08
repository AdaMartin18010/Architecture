# Rust Polonius 借用检查器 vs NLL：形式化对比与复用影响

> **形式化级别**: 严格（含证明级片段）
> **版本**: 2026-06-06
> **对齐标准**: Rust nightly 2026 (Polonius Alpha 通道), a-mir-formality, Rust Project Goals 2026
> **定位**: 理解 Polonius 如何通过更精确的区域推断使更多组件复用模式合法化

---

## 目录

- [Rust Polonius 借用检查器 vs NLL：形式化对比与复用影响](#rust-polonius-借用检查器-vs-nll形式化对比与复用影响)
  - [目录](#目录)
  - [1. 背景：从 Lexical Lifetimes 到 NLL 再到 Polonius](#1-背景从-lexical-lifetimes-到-nll-再到-polonius)
  - [2. NLL 的形式化定义与局限性](#2-nll-的形式化定义与局限性)
    - [2.1 NLL 的"点集"生命期模型](#21-nll-的点集生命期模型)
    - [2.2 NLL 的流不敏感性](#22-nll-的流不敏感性)
  - [3. Polonius 的形式化定义](#3-polonius-的形式化定义)
    - [3.1 从 Lifetimes 到 Origins](#31-从-lifetimes-到-origins)
    - [3.2 区域推断的子集关系](#32-区域推断的子集关系)
    - [3.3 Alpha 分析的位置敏感性](#33-alpha-分析的位置敏感性)
  - [4. 代码对比：NLL 无法通过但 Polonius 接受的案例](#4-代码对比nll-无法通过但-polonius-接受的案例)
    - [4.1 Case 1: NLL Problem Case 3（条件控制流跨分支）](#41-case-1-nll-problem-case-3条件控制流跨分支)
    - [4.2 Case 2: Lending Iterator（自借用迭代器）](#42-case-2-lending-iterator自借用迭代器)
    - [4.3 Case 3: 循环中的条件重新借用](#43-case-3-循环中的条件重新借用)
    - [4.4 Case 4: 链式可变引用的精确追踪](#44-case-4-链式可变引用的精确追踪)
  - [5. 对复用组件的影响](#5-对复用组件的影响)
    - [5.1 使更多组件模式合法化](#51-使更多组件模式合法化)
    - [5.2 API 设计范式转变](#52-api-设计范式转变)
    - [5.3 对现有组件的兼容性](#53-对现有组件的兼容性)
  - [6. 性能权衡与工程实践](#6-性能权衡与工程实践)
    - [6.1 编译时间开销](#61-编译时间开销)
    - [6.2 启用 Polonius](#62-启用-polonius)
  - [7. 关键定理与形式化保证](#7-关键定理与形式化保证)
  - [8. 参考索引](#8-参考索引)
  - [补充说明：Rust Polonius 借用检查器 vs NLL：形式化对比与复用影响](#补充说明rust-polonius-借用检查器-vs-nll形式化对比与复用影响)
  - [反例](#反例)
  - [权威来源](#权威来源)

---

## 1. 背景：从 Lexical Lifetimes 到 NLL 再到 Polonius

Rust 借用检查器经历了三代演进：

```
Lexical Lifetimes (Rust 1.0-1.30)
    ↓
Non-Lexical Lifetimes, NLL (Rust 1.31-1.84)
    ↓
Polonius Alpha (Rust 1.85+ nightly, 目标 2026 稳定化)
```

- **Lexical Lifetimes**: 生命期严格绑定于词法作用域，`{ ... }` 结束则生命期结束。导致大量安全代码被拒绝。
- **NLL**: 将生命期建模为**控制流图 (CFG) 上的点集**，允许生命期在最后一次使用后结束，而非作用域末尾。但仍存在流不敏感（flow-insensitive）的局限性。
- **Polonius**: 将生命期重新概念化为**loan 的 origin 集合**，引入**位置敏感（location-sensitive）**的子集约束推断，解决 NLL 的流不敏感问题。

---

## 2. NLL 的形式化定义与局限性

### 2.1 NLL 的"点集"生命期模型

**定义 N.1** (NLL 生命期): 在 NLL 中，生命期 `'a` 被建模为控制流图 (CFG) 上的一个点集（point-set）：

$$
\text{'a} \subseteq \text{Points(CFG)}
$$

其中 `Points(CFG)` 是 CFG 中所有程序点的集合。

**定义 N.2** (NLL Outlives 关系): `'a: 'b` 在 NLL 中表示点集包含：

$$
\text{'a}: \text{'b} \iff \text{'b} \subseteq \text{'a}
$$

即 `'a` outlives `'b` 当且仅当 `'a` 的点集包含 `'b` 的所有点。

**定义 N.3** (NLL Loan 活跃性): 对于 loan L（一次借用），其生命期 `lifetime(L)` 在 CFG 点 p 上活跃，当且仅当：

$$
p \in \text{lifetime}(L)
$$

活跃性决定在该点是否可以发生与 L 冲突的操作（如可变借用的二次借用）。

### 2.2 NLL 的流不敏感性

**定义 N.4** (流不敏感, Flow-Insensitivity): NLL 的核心局限性在于其**全局子集约束**：对于每个区域 `'a` 和 `'b`，NLL 计算**单一**的 `subset('a, 'b)` 关系，该关系在整个函数范围内成立：

$$
\text{NLL}: \quad \text{subset}('a, 'b) \in \{\text{true}, \text{false}\} \quad \text{(全局)}
$$

这意味着：若在某一分支中 `'a` 需要是 `'b` 的子集，NLL 会保守地认为**所有**分支中 `'a` 都是 `'b` 的子集。这种保守性导致安全代码被拒绝。

**示例**: 考虑以下条件分支：

```rust
if condition {
    // 分支 A: 'x 需要 outlive 'y
    let r: &'x T = ...;
    use(r);
} else {
    // 分支 B: 'x 不需要 outlive 'y
    // 无借用操作
}
```

NLL 会统一计算 `subset('y, 'x)` 并在两个分支中都强制执行，即使分支 B 根本不需要。

---

## 3. Polonius 的形式化定义

### 3.1 从 Lifetimes 到 Origins

**定义 P.1** (Origin): Polonius 将生命期重新定义为**origin**：一个 origin 是一个 loan 的集合：

$$
\text{Origin} \; O = \{ L_1, L_2, \ldots, L_n \}
$$

其中每个 Lᵢ 是一次具体的借用（loan）。Origin 不再是 CFG 上的点集，而是**借用的来源集合**。

**核心洞察**: 传统的"生命期 `'a` 在哪里活跃"问题被重新表述为"origin O 包含哪些 loan"，以及"在程序点 p，哪些 origin 是其他 origin 的子集"。

### 3.2 区域推断的子集关系

**定义 P.2** (位置敏感子集): Polonius 中，子集关系是**位置敏感**的——它在每个 CFG 点 p 上独立计算：

$$
\text{Polonius}: \quad \text{subset}_p('a, 'b) \in \{\text{true}, \text{false}\} \quad \text{(按点)}
$$

即 `'a ⊆ 'b` 的成立与否取决于当前程序点 p。

**定义 P.3** (Loan 活跃性的 Polonius 定义): loan L 在点 p 上活跃，当且仅当存在一个从 p 可达的使用点 q，使得 L ∈ origin(q)。形式化地：

$$
\text{Active}(L, p) \iff \exists q \in \text{Reach}(p): L \in O(q)
$$

其中 Reach(p) 是从 p 出发沿 CFG 可达的所有点，O(q) 是点 q 上的 origin。

### 3.3 Alpha 分析的位置敏感性

**定义 P.4** (Polonius Alpha 分析): Alpha 分析是 Polonius 的一个可稳定化子集，它通过**组合子集图 + CFG 的可达性分析**来确定 loan 活跃性：

$$
\text{Alpha}(L, p) = \text{Reachable}_{G_{\text{subset}} \cup \text{CFG}}(p, \text{Use}(L))
$$

其中 G_subset 是子集约束图，Use(L) 是 loan L 被使用的所有点。

**关键区别**:

- NLL: `Active(L, p)` 基于全局生命期点集，不考虑控制流分支差异
- Alpha: `Active(L, p)` 基于可达性分析，能区分不同分支中的活跃性

---

## 4. 代码对比：NLL 无法通过但 Polonius 接受的案例

### 4.1 Case 1: NLL Problem Case 3（条件控制流跨分支）

这是 Polonius 的标志性案例，来自 NLL RFC 中被推迟的问题 #3。

```rust
use std::collections::HashMap;
use std::hash::Hash;

/// NLL: ❌ 编译错误
/// Polonius: ✅ 编译通过
fn get_or_insert_default<'r, K: Hash + Eq + Copy, V: Default>(
    map: &'r mut HashMap<K, V>,
    key: K,
) -> &'r mut V {
    match map.get_mut(&key) {
        Some(value) => value,           // 分支 A: 直接返回现有值的引用
        None => {
            map.insert(key, V::default()); // 分支 B: 先插入，再返回引用
            map.get_mut(&key).unwrap()
        }
    }
}
```

**NLL 拒绝原因**:

NLL 看到 `map.get_mut(&key)` 在 `match` 处创建了一个可变借用（loan L）。在分支 A 中，返回值 `value` 要求 loan L 存活到函数结束（`'r`）。NLL 保守地认为 loan L 在**整个函数**范围内活跃，因此拒绝分支 B 中的 `map.insert`（需要另一个可变借用）。

形式化分析：

$$
\text{NLL}: \quad \text{Active}(L, \text{branch\_B}) = \text{true} \quad \text{(保守假设)}
$$

因为 NLL 全局地认为 loan L 与返回值的 `'r` 关联，而 `'r` 覆盖整个函数。

**Polonius 接受原因**:

Polonius 的 Alpha 分析计算可达性：

- 在分支 A 中：loan L 被 `value` 引用，需存活到函数结束
- 在分支 B 中：`value` 不存在，loan L 不流向任何使用点

因此：

$$
\text{Polonius}: \quad \text{Active}(L, \text{branch\_B}) = \text{false}
$$

分支 B 中的 `map.insert` 是合法的，因为 loan L 在该分支中不活跃。

### 4.2 Case 2: Lending Iterator（自借用迭代器）

Lending Iterator 是一种迭代器模式，其中 `next()` 返回的项借用了迭代器本身。这是 NLL 完全无法支持的模式。

```rust
/// Lending Iterator trait 定义
pub trait LendingIterator {
    type Item<'a>
    where
        Self: 'a;

    fn next(&mut self) -> Option<Self::Item<'_>>;

    /// NLL: ❌ 编译错误
    /// Polonius: ✅ 编译通过
    fn filter<P>(self, predicate: P) -> Filter<Self, P>
    where
        Self: Sized,
        P: FnMut(&Self::Item<'_>) -> bool,
    {
        Filter { iter: self, predicate }
    }
}

pub struct Filter<I, P> {
    iter: I,
    predicate: P,
}

impl<I: LendingIterator, P> LendingIterator for Filter<I, P>
where
    P: FnMut(&I::Item<'_>) -> bool,
{
    type Item<'a> = I::Item<'a> where Self: 'a;

    fn next(&mut self) -> Option<I::Item<'_>> {
        while let Some(item) = self.iter.next() {
            if (self.predicate)(&item) {
                return Some(item);  // item 借用了 self.iter
            }
            // NLL 问题：item 在此处应该已经释放
        }
        None
    }
}
```

**NLL 拒绝原因**:

在 `while let` 循环中，NLL 认为 `self.iter.next()` 创建的 loan 在整个循环体中活跃。当执行到下一次循环迭代时，NLL 报错：不能再次借用 `self.iter`，因为上一次借用的 loan 仍被认为活跃。

形式化地，NLL 将循环视为一个统一的"区域"，无法区分单次迭代内的借用边界。

**Polonius 接受原因**:

Alpha 分析追踪每次 `next()` 调用的 loan 在 CFG 上的精确可达性：

- 当 `if (self.predicate)(&item)` 为 true 时，`item` 被返回，loan 随返回值流出函数
- 当条件为 false 时，循环继续，但 `item` 不再被使用，其 loan 在循环回边之前已死亡

$$
\forall \text{循环迭代 } i: \text{Active}(L_i, \text{迭代 } i+1) = \text{false}
$$

即每次迭代的 loan 不会泄漏到下一次迭代。

### 4.3 Case 3: 循环中的条件重新借用

此案例展示了 Polonius 对循环内控制流的精确追踪能力。

```rust
struct Thing;

impl Thing {
    fn maybe_next(&mut self) -> Option<&mut Self> { None }
}

/// NLL: ❌ 编译错误 (E0499)
/// Polonius: ✅ 编译通过
fn traverse_chain() {
    let mut temp = &mut Thing;

    loop {
        match temp.maybe_next() {
            Some(v) => { temp = v; }   // 分支 A: temp 被重新赋值
            None => { break; }          // 分支 B: 退出循环
        }
    }
}
```

**NLL 拒绝原因**:

NLL 分析发现：

1. `temp.maybe_next()` 创建了对 `temp` 的可变借用（loan L）
2. 在分支 A 中，`v`（借用自 `temp`）被赋给 `temp`
3. NLL 认为 loan L "在循环中流动"——即 L 从一次迭代传递到下一次迭代
4. 因此在循环顶部再次借用 `temp` 时，NLL 报告错误：存在未结束的 loan

形式化地：

$$
\text{NLL}: \quad L \in \text{Origin}(\text{temp}) \text{ at loop header} \Rightarrow \text{冲突}
$$

**Polonius 接受原因**:

Alpha 分析进行更精细的追踪：

- 在分支 A 中：`temp = v` 意味着旧的 `temp` 被覆盖。下一次迭代借用的 `temp` 是一个**不同的内存位置**（链上的下一个节点），与 loan L 无关
- 在分支 B 中：循环终止，不存在下一次借用

通过可达性分析，Alpha 发现从 loan L 的使用点（`v`）到下一次循环头的路径，在分支 A 中被 `temp = v` 的赋值"打断"，在分支 B 中因循环终止而不存在。

### 4.4 Case 4: 链式可变引用的精确追踪

此案例展示了 Polonius 对"重新借用后原引用失效"的精确建模。

```rust
/// NLL: ❌ 编译错误
/// Polonius: ✅ 编译通过
fn reborrow_chain(data: &mut [i32]) -> i32 {
    let first = &mut data[0];
    let second = &mut *first;  // 从 first 重新借用
    *second = 42;

    // first 在此处已经失效（因为 second 是重新借用）
    // 但在 NLL 中，first 的生命期被保守延长
    *first = 100;  // NLL: 错误！认为 first 仍被 second 借用

    data[1]       // Polonius: 允许，因为 first/second 都已死亡
}
```

**注意**: 此案例需要 Polonius 的完整流敏感性（full flow-sensitivity），Alpha 分析**可能**不接受。这展示了 Alpha 的能力边界——它处理"逐分支差异"，但某些需要完整数据流追踪的模式仍需未来改进。

---

## 5. 对复用组件的影响

Polonius 对组件复用的影响体现在**表达能力**和**API 设计**两个维度：

### 5.1 使更多组件模式合法化

| 模式 | NLL 状态 | Polonius 状态 | 复用价值 |
|------|---------|--------------|---------|
| **get_or_insert** | ❌ 被拒绝 | ✅ 合法 | 集合 API 的惯用模式（如 `HashMap::entry` 的简化） |
| **Lending Iterator** | ❌ 完全不可表达 | ✅ 合法 | 流式解析器、字符迭代器、内存映射遍历 |
| **链表/树遍历** | ⚠️ 部分受限 | ✅ 显著改善 | 自引用数据结构、游标模式 |
| **条件重新借用** | ❌ 被拒绝 | ✅ 合法 | 状态机转换、解析器组合子 |
| **内部可变性过滤** | ❌ 被拒绝 | ✅ 合法 | `RefCell`/`Mutex` 守卫的条件释放 |

### 5.2 API 设计范式转变

**从 Workaround 到 First-Class**:

在 NLL 时代，许多本应自然的 API 被迫使用 workaround：

```rust
// NLL workaround: 使用 Entry API 替代 get_or_insert
map.entry(key).or_insert_with(Default::default)
```

Polonius 使直接写法合法化，降低了 API 使用者的认知负担。

**Lending Iterator 的复用革命**:

Lending Iterator 是许多底层组件的核心抽象：

```rust
// 零拷贝 CSV 解析：每行借用底层缓冲区
pub trait CsvRowIterator {
    type Item<'a> = CsvRow<'a>;
    fn next(&mut self) -> Option<Self::Item<'_>>;
}

// 内存映射文件的字节迭代：项借用映射区域
pub trait MmapIterator {
    type Item<'a> = &'a [u8];
    fn next(&mut self) -> Option<Self::Item<'_>>;
}
```

在 NLL 下，这些模式需要 `unsafe` 或 `Pin<&mut Self>` 的复杂 workaround。Polonius 使它们能在 safe Rust 中直接表达。

### 5.3 对现有组件的兼容性

**定理 P.5** (Polonius 超集性): Polonius Alpha 接受 NLL 接受的所有程序，即：

$$
\{ \text{Programs} \mid \text{NLL accepts} \} \subseteq \{ \text{Programs} \mid \text{Polonius accepts} \}
$$

*证明概要*: Alpha 分析在 NLL 计算 `Active(L, p) = false` 的所有点上，通过可达性分析也能得出 `false`。NLL 的保守近似不会比 Alpha 更宽松。∎

这意味着：启用 Polonius 不会破坏任何现有代码——它是纯扩展。

---

## 6. 性能权衡与工程实践

### 6.1 编译时间开销

Rust Project Goals 2026 明确接受 **10–20% 的编译时间开销**以换取表达能力提升。

| 分析阶段 | NLL 开销 | Polonius Alpha 开销 | 优化策略 |
|---------|---------|-------------------|---------|
| 约束生成 | O(n) | O(n) | 共享 NLL 的前端 |
| 子集传播 | O(n²) 最坏情况 | O(n × m) 可达性 | 惰性约束图重写 |
| 冲突检测 | 单次遍历 | 组合图遍历 | 限制传播到受影响块 |

其中 n = CFG 点数，m = loan 数量。

### 6.2 启用 Polonius

在 Rust 1.85+ nightly 中启用：

```bash
# 命令行
RUSTFLAGS="-Z polonius" cargo build

# 或配置于 .cargo/config.toml
[build]
rustflags = ["-Z", "polonius"]
```

**稳定化路线图**:

- 2025H2: nightly 功能预览
- 2026: Alpha 分析稳定化（当前目标）
- 2027+: 完整流敏感性改进

---

## 7. 关键定理与形式化保证

**定理 P.6** (Polonius Alpha 可靠性): 若程序通过 Polonius Alpha 检查，则该程序不存在数据竞争和 use-after-free。

*证明概要*:

1. Alpha 分析是 NLL 分析的精化（refinement）
2. NLL 已被证明是可靠的（RustBelt / Iris 框架中的机器检验证明）
3. 精化保持可靠性：更精确的分析不会接受不安全的程序
4. 形式化模型正在 a-mir-formality 中构建，将作为规范融入 Rust Reference ∎

**定理 P.7** (Polonius 对复用组件的扩展性): 对于任何 crate C，若 C 在 NLL 下编译通过，则在 Polonius 下也编译通过；存在 crate C' 使得 C' 在 Polonius 下编译通过但在 NLL 下不通过。

*证明概要*:

- 前半部分由定理 P.5（超集性）直接可得
- 后半部分由 Case 1-3 的构造性示例证明 ∎

**定理 P.8** (Lending Iterator 的 Polonius 必要性): 存在 Lending Iterator 的实现，在 NLL 下无可行的 safe Rust 实现，在 Polonius 下存在直接实现。

*证明概要*:

- Lending Iterator 要求 `next(&mut self) -> Option<Self::Item<'_>>` 中返回值借用 `self`
- NLL 的流不敏感性导致循环内每次 `next()` 的 loan 被保守合并
- Polonius 的位置敏感子集分析能区分每次迭代的独立 loan ∎

---

## 8. 参考索引

1. Rust Project Goals (2026). *Stabilize and model Polonius Alpha*. <https://rust-lang.github.io/rust-project-goals/2026/polonius.html> — 官方稳定化目标与 Alpha 分析定义
2. Rust Project Goals (2025H2). *Stabilizable Polonius support on nightly*. <https://rust-lang.github.io/rust-project-goals/2025h2/polonius.html> — Alpha 分析动机与案例
3. Inside Rust Blog (2023-10-06). *Polonius update*. <https://blog.rust-lang.org/inside-rust/2023/10/06/polonius-update.html> — 从 Datalog 到原生 rustc 实现的演进
4. Niko Matsakis et al. *NLL RFC*. <https://rust-lang.github.io/rfcs/2094-nll.html> — NLL 原始设计，含 Problem Case 3 的讨论
5. `a-mir-formality` 项目. <https://github.com/rust-lang/a-mir-formality/> — Polonius 形式化模型建设
6. Jung, R. et al. (2018). *RustBelt: Securing the Foundations of the Rust Programming Language*. POPL'18 — Rust 类型系统安全性的 Iris/分离逻辑证明
7. Villani, N. et al. (2025). *Tree Borrows*. PLDI'25 — Rust 别名模型的最新形式化进展
8. Rust Forum. *How to Understand NLL vs. Polonius Borrow Checking?* <https://users.rust-lang.org/t/how-to-understand-nll-vs-polonius-borrow-checking-with-example/86052> — 社区深度讨论

---

> **交叉引用**: 本文与 `struct/07-formal-verification/04-rust-type-system/formal-semantics.md` 中"所有权-借用-生命周期形式化定义"章节形成递进关系；与 `struct/04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md` 中 Rust 组件模型分析互为补充。
>
> 最后更新: 2026-06-06


---

## 补充说明：Rust Polonius 借用检查器 vs NLL：形式化对比与复用影响

## 反例

**反例**：在 Rust 中滥用 unsafe 块实现“性能优化”但未用 Miri 或形式化方法验证，导致复用该 unsafe 包装的多个项目出现未定义行为。

## 权威来源

> **权威来源**:
>
> - [The Rust Programming Language](https://www.rust-lang.org)
> - [RustBelt](https://plv.mpi-sws.org/rustbelt/)
> - [Aeneas](https://github.com/AeneasVerif/aeneas)
> - 核查日期：2026-07-07
