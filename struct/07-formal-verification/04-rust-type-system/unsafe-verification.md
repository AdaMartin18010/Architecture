# Rust unsafe 边界的验证策略：工具链对比与可复用组件检查清单

> **形式化级别**: 严格
> **版本**: 2026-06-06
> **对齐标准**: Rust 1.85+, Miri (POPL'26), Kani 0.66, Prusti (Viper), Aeneas (LLBC), Tree Borrows (PLDI'25)
> **定位**: 为复用包含 unsafe 的 Rust 组件提供分层验证策略与工具选型指南

---

## 目录

- [1. unsafe 边界的形式化定义](#1-unsafe-边界的形式化定义)
  - [1.1 内存安全契约](#11-内存安全契约)
  - [1.2 unsafe 作为信任边界](#12-unsafe-作为信任边界)
- [2. 验证工具链对比矩阵](#2-验证工具链对比矩阵)
  - [2.1 Miri：动态 UB 检测](#21-miri动态-ub-检测)
  - [2.2 Kani：有界模型检测](#22-kani有界模型检测)
  - [2.3 Prusti：契约式验证](#23-prusti契约式验证)
  - [2.4 Aeneas：借用到函数式精化](#24-aeneas借用到函数式精化)
  - [2.5 Verus：SMT 辅助的证明型 Rust](#25-verussmt-辅助的证明型-rust)
  - [2.6 Creusot：演绎验证](#26-creusot演绎验证)
  - [2.7 其他工具概览](#27-其他工具概览)
- [3. 工具链综合对比矩阵](#3-工具链综合对比矩阵)
- [4. 可复用 unsafe 组件的验证检查清单](#4-可复用-unsafe-组件的验证检查清单)
- [5. 分层验证策略](#5-分层验证策略)
- [6. 与组件架构复用的交叉引用](#6-与组件架构复用的交叉引用)
- [7. 关键定理与形式化保证](#7-关键定理与形式化保证)
- [8. 参考索引](#8-参考索引)

---

## 1. unsafe 边界的形式化定义

### 1.1 内存安全契约

**定义 U.1** (unsafe 块契约): 每个 unsafe 代码块隐含一个内存安全契约 Xi = (P, O, I)，其中：

- **前置条件 P**: 进入 unsafe 块前必须成立的条件
  - 指针非空且对齐
  - 借用规则满足
  - 生命周期有效

- **后置条件 O**: unsafe 块退出时必须保证的约定
  - 内存初始化
  - 类型不变量保持
  - 所有权归位

- **不变量 I**: unsafe 块执行期间维持的全局属性
  - 无数据竞争
  - 无 use-after-free

**定义 U.2** (Undefined Behavior, UB): 当 unsafe 块的实际执行违反契约 Xi 时，发生 Undefined Behavior。Rust 编译器对 UB 不提供任何保证。

形式化地：

$$
\text{UB} \iff \exists \text{unsafe block } B: \neg P_B \lor \neg O_B \lor \neg I_B
$$

### 1.2 unsafe 作为信任边界

**定义 U.3** (信任边界, Trust Boundary): unsafe 标记是 Rust 类型系统中的显式信任降级点：

```
safe Rust --[编译器保证]--> 内存安全 + 数据竞争自由
     |
     | unsafe { ... }
     v
unsafe Rust --[人工审查/工具验证]--> 内存安全 + 数据竞争自由
```

**公理 U.1** (Trust Degradation): 当复用包含 unsafe 的 crate 时，安全保证从"编译器自动证明"降级为"人工审查 + 工具辅助验证"。

**定理 U.1** (Unsafe Propagation): 若 crate C 包含 unsafe 代码，则任何依赖 C 的 crate D 的安全保证依赖于 C 的 unsafe 边界的正确性。

$$
\text{Soundness}(D) \implies \text{Soundness}(C_{\text{unsafe}})
$$

---

## 2. 验证工具链对比矩阵

### 2.1 Miri：动态 UB 检测

**原理**: Miri 是 Rust MIR（Mid-level IR）的解释器，在解释执行过程中动态检测 UB。

```rust
// 示例：Miri 检测错误的指针偏移
unsafe {
    let ptr = std::alloc::alloc(std::alloc::Layout::new::<i32>());
    // 错误：仅分配了 4 字节，但偏移 8 字节
    let bad_ptr = ptr.add(2);  // Miri报错！out-of-bounds pointer arithmetic
}
```

**核心能力**（截至 2026，POPL'26 论文）：

| 检测能力 | 状态 |
|---------|------|
| Use-after-free | 完整检测 |
| Double-free | 完整检测 |
| 未初始化内存读取 | 完整检测 |
| 数据竞争 | 通过非确定性调度器检测 |
| Stacked Borrows / Tree Borrows 违规 | 默认 Tree Borrows |
| 对齐违规 | 完整检测 |
| 类型 punning | 检测 |
| FFI / 原生调用 | 实验性支持 |

**局限**: 
- 动态分析：只能检测执行到的代码路径（覆盖率问题）
- 状态爆炸：复杂循环和递归需要限制迭代次数
- 无证明：通过测试不等于正确

**使用方式**:

```bash
rustup component add miri
MIRIFLAGS="-Zmiri-tree-borrows" cargo miri test
```

### 2.2 Kani：有界模型检测

**原理**: Kani 将 Rust MIR 翻译为 Goto-C，使用 CBMC (C Bounded Model Checker) 进行有界模型检测——通过 SMT 求解器穷举所有执行路径（在循环展开界内）。

```rust
// 示例：Kani 验证 unsafe 内存操作
#[kani::proof]
fn test_safe_write() {
    let mut x: i32 = 0;
    let ptr: *mut i32 = &mut x;
    
    unsafe {
        ptr.write(42);
    }
    
    assert_eq!(x, 42);  // Kani验证通过
}

#[kani::proof]
fn test_unaligned_write() {
    let mut bytes = [0u8; 8];
    let ptr = bytes.as_mut_ptr() as *mut u64;
    
    unsafe {
        // 若 ptr 未按 u64 对齐，Kani 检测为 UB
        ptr.write(0xDEADBEEF);
    }
}
```

**核心能力**（截至 Kani 0.66, 2026-01）：

| 能力 | 状态 |
|------|------|
| 内存安全断言 | 自动推导 |
| 用户指定属性 | 属性宏方式 |
| 动态 trait 对象 | 40+ 测试用例 |
| 并发程序 | 部分支持 |
| 循环验证 | BoundedArbitrary + loop invariants |
| 无需修改被测代码 | 支持 |
| 工业级部署 | AWS Firecracker 27 harnesses in CI |

**局限**:
- 有界性：循环需展开界，递归需深度限制
- 验证范围：状态空间随变量位宽指数增长
- 无功能性规约：验证安全属性，非功能正确性

**工程实践**: AWS Firecracker 在每次代码变更的 CI 中运行 Kani，约 15 分钟完成全套验证。

### 2.3 Prusti：契约式验证

**原理**: Prusti 基于 ETH Zurich 的 Viper 验证基础设施，通过分离逻辑验证 Rust 代码。用户通过 requires 和 ensures 宏显式声明契约。

```rust
use prusti_contracts::*;

// 前置条件: ptr 非空且对齐
// 后置条件: 返回值等于 ptr 指向的值
#[requires(ptr != std::ptr::null_mut())]
#[requires((ptr as usize) % std::mem::align_of::<i32>() == 0)]
#[ensures(result == unsafe { *ptr })]
fn deref_or_panic(ptr: *mut i32) -> i32 {
    unsafe { *ptr }
}
```

**核心能力**:

| 能力 | 状态 |
|------|------|
| 分离逻辑验证 | Viper 后端 |
| 契约宏 | 支持 |
| Panic 自由验证 | 支持 |
| 溢出检测 | 支持 |
| 循环不变量 | 支持 |
| 纯函数 | 支持 |
| 不安全代码支持 | 有限（需额外注解） |

**局限**:
- 维护状态：2024-03 后提交活动减缓
- 学习曲线：需掌握分离逻辑和 Viper 中间表示
- 自动化程度：低于 Kani，需手动编写契约

### 2.4 Aeneas：借用到函数式精化

**原理**: Aeneas (Inria) 将 safe Rust 翻译为纯函数式规约（LLBC, Low-Level Borrow Calculus），然后翻译成 F*、Coq 或 Lean 进行交互式证明。

```rust
// Aeneas 将以下 Rust 代码翻译为纯函数式规约
fn swap<T>(a: &mut T, b: &mut T) {
    let temp = std::mem::replace(a, std::mem::replace(b, *a));
    *b = temp;
}
```

**核心能力**:

| 能力 | 状态 |
|------|------|
| Safe Rust 完整翻译 | LLBC |
| 多后端证明器 (F*, Coq, Lean, HOL4) | 支持 |
| 借用模式自动处理 | 优于 Prusti 的循环重借用 |
| 功能正确性证明 | 交互式 |
| Unsafe Rust 支持 | 仅 safe Rust |
| 自动化程度 | 需交互式证明 |

### 2.5 Verus：SMT 辅助的证明型 Rust

**原理**: Verus 允许开发者用 Rust 自身编写规约和证明，利用 SMT 求解器自动化验证。支持 unsafe 代码的验证（需手动建模内存）。

```rust
use vstd::prelude::*;

verus! {
    fn abs(x: i64) -> (r: i64)
        ensures
            r >= 0,
            r == x || r == -x,
    {
        if x < 0 { -x } else { x }
    }
}
```

**核心能力**: 低级别系统代码验证（OOPSLA'23, SOSP'24），支持 unsafe（需内存模型假设），自动化程度高于 Aeneas。

### 2.6 Creusot：演绎验证

**原理**: Creusot (Inria) 将 Rust 翻译成 WhyML，使用 Why3 平台进行演绎验证。采用 prophecies 处理多借用，支持比 Prusti 更广泛的循环重借用模式。

**核心能力**: Safe Rust 功能正确性，多后端证明器 (Alt-Ergo, CVC5, Z3)，活跃维护（2026-01 持续更新）。

### 2.7 其他工具概览

| 工具 | 机构 | 技术路线 | 最新状态 (2026) |
|------|------|---------|----------------|
| RefinedRust | MPI-SWS | 类型系统 + Iris 分离逻辑 | PLDI'24, 基础验证框架 |
| RustHorn | 东北大学 | CHC 约束 + 自动验证 | TOPLAS'21, 维护中 |
| Crux-MIR | Galois | 符号执行 | 持续开发 |
| Flux | UCSD | 精化类型 (Refinement Types) | PLDI'23, 活跃 |
| Gillian-Rust | Imperial College | 混合符号执行 | 2025 进展中 |
| MIRChecker | 北大 | 静态分析 + 约束求解 | 学术研究 |
| Rudra | KAIST | 模式匹配检测 unsafe 反模式 | 2021, 静态扫描 |

---

## 3. 工具链综合对比矩阵

| 维度 | Miri | Kani | Prusti | Aeneas | Verus | Creusot |
|------|------|------|--------|--------|-------|---------|
| **验证范式** | 动态解释执行 | 有界模型检测 | 契约 + 分离逻辑 | 函数式翻译 + 交互证明 | SMT + 证明型 Rust | 演绎验证 (WhyML) |
| **分析范围** | 单条执行路径 | 所有路径（有界） | 所有路径 | 所有路径 | 所有路径 | 所有路径 |
| **Safe Rust** | 支持 | 支持 | 支持 | 支持 | 支持 | 支持 |
| **Unsafe Rust** | 完整支持 | 支持 | 有限 | 不支持 | 需建模 | 不支持 |
| **自动化程度** | 全自动 | 高 | 中 | 低 | 中 | 中 |
| **功能正确性** | 否 | 否 | 是 | 是 | 是 | 是 |
| **UB 检测精度** | 位精确 | 位精确 | 逻辑级 | N/A | 位精确 | N/A |
| **执行时间** | 慢 | 中等 | 慢 | 慢 | 中等 | 中等 |
| **学习曲线** | 低 | 低 | 高 | 很高 | 高 | 高 |
| **工业部署** | 社区广泛 | AWS 生产级 | 学术研究 | 研究/教学 | 研究/工业 | 研究 |
| **最新活跃** | POPL'26 | 2026-01 | 2024-03 | 2026-01 | 2026-01 | 2026-01 |

**选型决策树**:

```
需要验证 unsafe 代码？
├── 是 → 需要动态/位精确检测？
│   ├── 是 → Miri (快速 UB 筛查) 或 Kani (路径穷举)
│   └── 否 → Verus (手动内存建模)
└── 否 → 需要功能正确性证明？
    ├── 是 → 愿意交互式证明？
    │   ├── 是 → Aeneas (灵活后端) 或 Creusot (prophecies)
    │   └── 否 → Prusti (契约宏) 或 Verus (证明型 Rust)
    └── 否 → Kani (安全属性自动验证)
```

---

## 4. 可复用 unsafe 组件的验证检查清单

在复用包含 unsafe 的 crate 前，建议执行以下分层检查：

### Level 1: 依赖审计（必须）

- [ ] **unsafe 密度审查**: unsafe 代码占代码行数比例是否低于 5%？（工具：cargo-geiger）
- [ ] **unsafe 传播分析**: 哪些公开 API 触及 unsafe 边界？（工具：cargo-call-stack, 源码审查）
- [ ] **维护者信誉**: crate 作者是否有形式化验证或系统编程背景？
- [ ] **RustSec 检查**: cargo audit 是否报告已知漏洞？
- [ ] **MSRV 兼容性**: 目标 Rust 版本是否支持该 crate 的 unsafe 用法？

### Level 2: 动态验证（推荐）

- [ ] **Miri 通过**: cargo miri test 是否全部通过？
- [ ] **Miri 覆盖率**: 是否覆盖了所有 unsafe 块的分支？
- [ ] **Fuzz 测试**: 是否使用 cargo-fuzz 对 unsafe API 进行模糊测试？
- [ ] **Sanitizer 通过**: AddressSanitizer / MemorySanitizer 是否通过？

### Level 3: 静态验证（高保证场景）

- [ ] **Kani 验证**: 关键 unsafe 函数是否有 Kani harness？
- [ ] **契约文档**: unsafe 函数是否有完整的 SAFETY 注释？
- [ ] **Tree Borrows 兼容**: Miri 的 Tree Borrows 模式是否通过？

示例 SAFETY 注释模板：

```rust
/// # Safety
/// - ptr must be non-null and properly aligned for T
/// - ptr must point to a valid, live allocation of at least count * size_of::<T>() bytes
/// - The memory region must not be accessed through other references during this call
unsafe fn my_unsafe_fn<T>(ptr: *mut T, count: usize) { ... }
```

### Level 4: 形式化验证（关键基础设施）

- [ ] **内存模型合规**: 是否验证符合 Tree Borrows / Stacked Borrows 别名规则？
- [ ] **功能规约**: 是否有形式化的前置/后置条件？（Prusti / Verus / Creusot）
- [ ] **不变量保持**: unsafe 代码是否保持类型的不变量？
- [ ] **并发安全**: 若涉及并发，unsafe 代码是否正确使用原子序语和内存序？

---

## 5. 分层验证策略

针对不同风险等级的组件，采用差异化的验证深度：

| 风险等级 | 示例场景 | 最小验证 | 推荐增强 |
|---------|---------|---------|---------|
| **L0: 无 unsafe** | 纯 safe Rust 工具库 | cargo test + cargo audit | Miri 抽检 |
| **L1: 少量 unsafe** | 封装系统调用 | L0 + Miri 全覆盖 | Kani 关键路径 |
| **L2: 核心 unsafe** | 内存分配器、数据结构 | L1 + SAFETY 文档审查 | Kani + Fuzz |
| **L3: 大规模 unsafe** | 操作系统内核、VMM | L2 + 形式化规约 | Verus / Prusti |
| **L4: 安全关键** | 密码学、航空航天 | L3 + 独立审计 | 机器检验证明 |

---

## 6. 与组件架构复用的交叉引用

本文与 struct/04-component-architecture-reuse/ 的关联：

### 6.1 Rust 生态组件模型

在 comparison-matrix-2026.md 中，Rust 生态的"变性机制"维度获得满分（5/5），部分原因在于其 unsafe 边界提供了显式的安全降级点。与其他语言（C/C++ 的隐式 UB、Java 的 JNI 黑箱）相比，Rust 的 unsafe 关键字使安全审计可以聚焦于特定代码区域。

### 6.2 供应链安全

open-source-supply-chain-reuse.md 中提出的"分层防御"策略可直接映射到 unsafe 验证：

```
Layer 1: 依赖审计（cargo audit, cargo geiger）
    └── 识别包含 unsafe 的传递依赖
    
Layer 2: 动态验证（Miri, Sanitizer）
    └── 在 CI 中自动检测 UB
    
Layer 3: 静态验证（Kani, Prusti）
    └── 关键组件的形式化属性验证
    
Layer 4: 源码审查 + Vendoring
    └── 对关键 unsafe 组件进行人工审计和源码锁定
```

### 6.3 复用成熟度评分调整

对于包含 unsafe 的组件，建议在 comparison-matrix-2026.md 的评分基础上进行安全等级调整：

| 验证深度 | 评分调整 |
|---------|---------|
| 无验证 + 大量 unsafe | -1.0 |
| Miri 通过 + SAFETY 文档 | -0.3 |
| Kani/Prusti 验证通过 | -0.1 |
| 形式化证明（RustBelt / Iris）| 0.0（完全补偿） |

---

## 7. 关键定理与形式化保证

**定理 V.1** (Miri 可靠性): 若程序在 Miri 下执行且不报告 UB，则该执行路径符合 Rust 的 Tree Borrows 内存模型。

依据: Jung et al. (POPL'26) Miri: Practical Undefined Behavior Detection for Rust — Miri 的实现与 Tree Borrows 形式化模型严格对应。

**定理 V.2** (Kani 有界完备性): 对于给定的循环展开界 k 和递归深度 d，Kani 穷举所有长度小于等于 k 的执行路径。若所有路径满足属性 phi，则程序在所有有界执行中满足 phi。

依据: CBMC 的 bounded model checking 理论 + Kani 到 Goto-C 的语义保持翻译。

**定理 V.3** (Prusti 可靠性): 若 Prusti 报告程序满足契约 Xi = (P, O)，且所有 unsafe 块的外部规约正确，则程序在所有执行中满足 Xi。

依据: Viper 框架的分离逻辑可靠性 + Prusti 到 Viper 的翻译正确性 (Astrauskas et al., NFM'22)。

**定理 V.4** (Aeneas 翻译正确性): Aeneas 将 safe Rust 到 LLBC 的翻译保持操作语义等价。

依据: Ho & Protzenko (ICFP'22, ICFP'24) 的 borrow calculus 形式化。

**定理 U.2** (Unsafe 边界不可完全自动化): 对于任意 unsafe Rust 程序，判断其是否包含 UB 是不可判定问题（归约自停机问题）。

证明概要: unsafe 允许裸指针算术和任意内存访问，可编码通用图灵机状态到内存操作。UB 检测等价于判断图灵机是否进入非法状态。由停机问题的不可判定性，UB 检测不可判定。

此定理说明为什么需要分层验证策略——没有任何单一工具能完全保证 unsafe 代码的安全。

---

## 8. 参考索引

1. Jung, R., Kimock, B., Poveda, C., Sanchez Munoz, E., Scherer, O., & Wang, Q. (2026). Miri: Practical Undefined Behavior Detection for Rust. POPL'26. https://plf.inf.ethz.ch/research/popl26-miri.html
2. Villani, N., Hostert, J., Dreyer, D., & Jung, R. (2025). Tree Borrows. PLDI'25, Distinguished Paper Award.
3. VanHattum, A., et al. (2022). Verifying Dynamic Trait Objects in Rust. ICSE-SEIP'22.
4. Astrauskas, V., et al. (2022). Prusti: A Static Verifier for Rust. NFM'22.
5. Ho, S., & Protzenko, J. (2022). Aeneas: Rust Verification by Functional Translation. ICFP'22; (2024) ICFP'24 扩展.
6. Lattuada, A., et al. (2023). Verus: Verified Rust for low-level systems code. OOPSLA'23; SOSP'24.
7. Denis, X., et al. (2022). Creusot: A Foundational Deductive Verifier for Rust. ICFEM'22.
8. Gaher, L., et al. (2024). RefinedRust: A Type System for High-Assurance Verification of Rust Programs. PLDI'24.
9. Jung, R., et al. (2018). RustBelt: Securing the Foundations of the Rust Programming Language. POPL'18.
10. Rust Formal Methods Interest Group. https://rust-formal-methods.github.io/

---

> **交叉引用**: 本文与 struct/04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md 中"Rust 生态组件模型"和"供应链安全"章节直接对齐；与 struct/07-formal-verification/04-rust-type-system/formal-semantics.md 中"Unsafe Boundary"定理 (R.3) 形成深化；与 struct/10-supply-chain-security/ 的漏洞管理框架共享分层防御思想。
>
> 最后更新: 2026-06-06
