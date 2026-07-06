# Rust 形式化验证工具链实践（2025‑2026）

> **版本**: 2026-06-08 (Phase 2 修订版)
> **定位**: 为架构复用体系中"可复用 Rust 组件"提供从测试到证明的分层验证路径；聚焦 Kani / Prusti / Miri 三工具的概念梳理与互补使用。
> **权威对齐**: Kani 0.66、Prusti、Miri 官方文档、RustBelt (Iris)、Verus 2024 OSDI 论文。
> **对齐公理**: `struct/01-meta-model-standards/06-formal-axioms/axiom-system.md` 之 S.1 Interface Substitution、F.1 Formal Verification Trust Transfer

---

## 目录

- [Rust 形式化验证工具链实践（2025‑2026）](#rust-形式化验证工具链实践20252026)
  - [目录](#目录)
  - [1. 分层验证策略](#1-分层验证策略)
  - [2. 工具链概述：Kani / Prusti / Miri 的互补定位](#2-工具链概述kani--prusti--miri-的互补定位)
    - [2.1 Kani（AWS）—— 基于模型检查的 Rust 验证器](#21-kaniaws-基于模型检查的-rust-验证器)
    - [2.2 Prusti（ETH Zurich）—— 基于 Viper 的 Rust 契约验证器](#22-prustieth-zurich-基于-viper-的-rust-契约验证器)
    - [2.3 Miri（Rust 官方）—— 未定义行为检测解释器](#23-mirirust-官方-未定义行为检测解释器)
  - [3. 概念说明与对比](#3-概念说明与对比)
  - [4. Rust 复用安全中的应用场景](#4-rust-复用安全中的应用场景)
    - [4.1 何时使用 Kani：验证 `unsafe` 代码块的内存安全](#41-何时使用-kani验证-unsafe-代码块的内存安全)
    - [4.2 何时使用 Prusti：为公共 API 添加前置 / 后置条件](#42-何时使用-prusti为公共-api-添加前置--后置条件)
    - [4.3 何时使用 Miri：检测跨 crate 边界的数据竞争](#43-何时使用-miri检测跨-crate-边界的数据竞争)
  - [5. 与 Rust 类型系统的衔接](#5-与-rust-类型系统的衔接)
    - [5.1 所有权系统已保证的 → 无需额外验证](#51-所有权系统已保证的--无需额外验证)
    - [5.2 所有权系统无法保证的 → 需要 Kani / Prusti / Miri](#52-所有权系统无法保证的--需要-kani--prusti--miri)
    - [5.3 `unsafe` 边界的特殊处理](#53-unsafe-边界的特殊处理)
  - [6. 安装与运行参考](#6-安装与运行参考)
    - [6.1 Miri](#61-miri)
    - [6.2 Kani](#62-kani)
    - [6.3 Prusti](#63-prusti)
  - [7. 推荐组合工作流](#7-推荐组合工作流)
  - [8. 文件索引](#8-文件索引)
  - [9. 权威参考](#9-权威参考)
  - [补充说明：Rust 形式化验证工具链实践（2025‑2026）](#补充说明rust-形式化验证工具链实践20252026)
  - [反例](#反例)
  - [权威来源](#权威来源)

## 1. 分层验证策略

对于可复用 Rust 组件，推荐按以下层次递进，成本从低到高，保证从弱到强：

```text
Level 1: cargo test + cargo-semver-checks          （功能回归 + API 兼容性）
Level 2: Miri                                      （UB 动态检测）
Level 3: Kani                                      （有界模型检验）
Level 4: Prusti / Verus / Aeneas                   （演绎式功能正确性证明）
```

---

## 2. 工具链概述：Kani / Prusti / Miri 的互补定位

Rust 形式化验证生态在 2024–2026 年形成了"动态检测 → 有界模型检验 → 演绎证明"的清晰分层。其中 **Kani**、**Prusti**、**Miri** 是覆盖最多工业场景的三个核心工具，分别对应不同的验证目标和技术路线。

### 2.1 Kani（AWS）—— 基于模型检查的 Rust 验证器

Kani 由 AWS 开源，核心是将 Rust 代码编译为中间表示（GOTO-C），然后调用 CBMC（C Bounded Model Checker）进行有界模型检验。其设计哲学是：**在不修改源代码的情况下，验证通用属性（如 panic 自由、内存安全、用户断言）**。

Kani 的关键特征是"proof harness"模式：开发者编写一个特殊的测试函数，使用 `kani::any()` 生成非确定性输入，然后调用被测函数并断言后置条件。Kani 会穷尽所有有界范围内的执行路径，若存在违反断言的路径则给出具体反例。

### 2.2 Prusti（ETH Zurich）—— 基于 Viper 的 Rust 契约验证器

Prusti 由 ETH Zurich 的 Viper 项目组开发，核心是将 Rust 代码和 `prusti_contracts` 宏中的前置/后置条件翻译为 Viper 中间语言，然后通过 Boogie/Z3 进行自动定理证明。其设计哲学是：**通过契约（contracts）显式规约接口行为，在编译期验证调用者是否满足前置条件、被调用者是否满足后置条件**。

Prusti 支持 `requires`、`ensures`、`pure`、`trusted` 等注解，与 Eiffel/SPARK 的 Design by Contract 传统一脉相承。与 Kani 的"黑箱验证"不同，Prusti 的验证是"白箱规约驱动"的——契约本身就是规约，验证过程检查代码是否精化（refine）了规约。

### 2.3 Miri（Rust 官方）—— 未定义行为检测解释器

Miri 是 Rust 编译器团队的官方工具，作为 Rust 中间表示（MIR）的解释器运行。它不验证功能正确性，而是**在 MIR 级别精确检测所有类别的未定义行为（Undefined Behavior, UB）**：越界访问、未初始化读取、违反别名规则（Stacked Borrows / Tree Borrows）、数据竞争等。

Miri 的核心优势是**语义保真**：它直接解释 MIR，而非翻译到另一种语言，因此其检测结果与 Rust 语言语义完全一致。但它只能检测"存在 UB 的某条执行路径"，不能证明"所有路径都无 UB"——后者需要 Kani 或 Prusti。

---

## 3. 概念说明与对比

| 维度 | Kani | Prusti | Miri |
|------|------|--------|------|
| **验证目标** | 内存安全、panic 自由、用户断言、功能正确性（有界） | 功能正确性（requires/ensures）、内存安全、终止性 | 未定义行为（UB）检测：越界、未初始化、别名违规、数据竞争 |
| **技术基础** | CBMC（有界模型检验）；GOTO-C 中间表示 | Viper（分离逻辑 + Boogie/Z3）；符号执行 + 自动定理证明 | MIR 解释器；动态执行 + 运行时检查 |
| **自动化程度** | 高 —— 编写 harness 后全自动验证，自动生成反例 | 中 —— 需手动编写契约（requires/ensures），证明过程自动 | 高 —— 直接运行测试，无需额外注解 |
| **适用范围** | `unsafe` 块、FFI 边界、算法正确性、安全关键函数 | 安全 Rust API 的契约设计、库接口规约、教学示例 | 所有含 `unsafe` 的代码、并发原语、跨 crate 边界的数据结构 |
| **保证强度** | 有界保证（循环展开深度、递归深度受限） | 无界保证（若证明通过，则对所有输入成立） | 单路径保证（仅验证实际执行的测试路径） |
| **与 Rust 类型系统关系** | 补充类型系统 —— 验证类型系统无法捕获的属性 | 扩展类型系统 —— 将契约作为"类型"的一部分 | 强化类型系统 —— 在运行时语义层检测类型系统的漏洞 |
| **典型运行时间** | 分钟级（取决于循环展开深度和状态空间大小） | 秒级到分钟级（取决于契约复杂度和自动证明器性能） | 秒级到分钟级（比原生测试慢 10–100 倍） |
| **CI 集成成熟度** | 高 —— AWS Firecracker 生产使用，GitHub Actions 支持完善 | 中 —— 需自定义 Docker 镜像或 GitHub Action，依赖 Viper 服务端 | 高 —— 官方 nightly 支持，`cargo miri test` 标准接口 |

---

## 4. Rust 复用安全中的应用场景

在架构复用体系中，Rust 组件的安全复用取决于两个条件：**接口契约的清晰性**（被复用方提供什么保证）和**使用方式的正确性**（复用方是否满足前置条件）。三个工具分别解决这两个条件的不同侧面。

### 4.1 何时使用 Kani：验证 `unsafe` 代码块的内存安全

Rust 的类型系统无法验证 `unsafe` 块内部的内存操作。当可复用组件包含 `unsafe`（如 FFI 调用、原始指针操作、手动内存布局）时，Kani 是唯一能在工业 CI 环境中自动验证其安全性的工具。

**典型场景**：

- 复用一个封装了 C 库的 Rust crate（如 `openssl-sys`、`libsqlite3-sys`），验证其 FFI 边界是否存在越界或 use-after-free。
- 验证 `Vec::set_len` + `std::ptr::copy_nonoverlapping` 的组合是否满足内存不变量。
- 为加密原语（如常量时间比较）编写 harness，验证其在所有输入下都不 panic 且输出正确。

```rust
#[cfg(kani)]
mod proofs {
    #[kani::proof]
    fn verify_abs() {
        let x: i32 = kani::any();
        let r = x.abs();
        assert!(r >= 0);
        if x < 0 { assert!(r == -x); }
        if x >= 0 { assert!(r == x); }
    }
}
```

Kani 的局限性在于**有界性**：循环必须指定展开深度，递归必须指定深度。因此它更适合验证"小内核函数"而非大型系统。AWS Firecracker 的实践表明，为每个 `unsafe` 边界函数编写一个 harness（约 50–200 行），是成本与收益的最佳平衡点。

### 4.2 何时使用 Prusti：为公共 API 添加前置 / 后置条件

Prusti 的核心价值在于**接口契约的可复用传递性**。当组件 A 被组件 B 复用时，A 的 `requires` 条件自动成为 B 的义务，A 的 `ensures` 条件自动成为 B 的权利。这直接实现了公理 F.1（Formal Verification Trust Transfer）的 Rust 版本：若组件 C 通过 Prusti 验证了契约，则任何使用 C 的系统继承 C 的后置条件保证，前提是调用者满足 C 的前置条件。

**典型场景**：

- 为数据结构库（如自定义 `BTreeMap`）的 `insert`/`remove`/`get` 方法添加契约，确保调用者不会传入非法键值。
- 为金融计算库添加 `requires(divisor != 0)` 和 `ensures(result * divisor == dividend || result * divisor == dividend - remainder)`，防止除零和精度丢失。
- 在微服务架构中，Prusti 契约可作为"可验证的 OpenAPI 规约"，替代部分运行时断言。

```rust
use prusti_contracts::*;

#[requires(a > 0 && b > 0)]
#[ensures(result == a + b)]
fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

Prusti 的局限性在于 **`unsafe` 支持有限**（需标记为 `#[trusted]`）和 **外部 crate 需手写 `extern_spec`**。因此它更适合纯安全 Rust 的库 API 设计，而非底层系统编程。

### 4.3 何时使用 Miri：检测跨 crate 边界的数据竞争

Miri 是**运行时 UB 检测的最后防线**。在复用场景下，即使单个 crate 通过了所有测试，跨 crate 边界的组合仍可能触发 UB——尤其是涉及 `unsafe`、并发原语或特定内存顺序时。

**典型场景**：

- 检测 `Send`/`Sync` 的手工实现是否真的有数据竞争风险。例如，一个 crate 声称 `unsafe impl Send for MyType`，Miri 可在多线程调度探索下验证该声明是否成立。
- 验证 `Rc<RefCell<T>>` 跨 crate 传递时是否存在别名违规（Stacked Borrows / Tree Borrows）。
- 检测 `std::mem::transmute` 是否违反了类型不变量（如将 `u8` 数组 transmute 为带有非法 discriminant 的 enum）。

```bash
# 多线程调度探索 —— 检测数据竞争
MIRIFLAGS="-Zmiri-many-seeds=0..16" cargo miri test
```

Miri 的局限性在于**只能检测实际执行的路径**。若测试用例未覆盖某个分支，Miri 无法发现该分支上的 UB。因此 Miri 应与高覆盖率测试套件（如 fuzzing + property-based testing）结合使用。

---

## 5. 与 Rust 类型系统的衔接

Rust 的所有权-借用-生命周期系统（OBL）已经是工业编程语言中最强的静态安全保证之一。理解"OBL 已经保证了什么"与"还需要什么工具补充"，是合理分配验证资源的前提。

### 5.1 所有权系统已保证的 → 无需额外验证

| 安全属性 | OBL 保证机制 | 额外工具需求 |
|---------|-------------|------------|
| 悬垂引用（use-after-free） | 所有权移动 + 生命周期检查 | 无 |
| 双重释放 | `Drop`  trait 的唯一调用 | 无 |
| 数据竞争（safe Rust） | `&mut T` 的排他性 + `&T` 的不可变性 | 无 |
| 空指针解引用（safe Rust） | 引用类型 `&T` 非空 | 无 |
| 迭代器失效 | 借用检查器阻止并发修改 | 无 |

在纯安全 Rust 中，上述属性由编译器静态保证，无需 Kani、Prusti 或 Miri。这是 Rust 复用安全的基础优势：任何通过编译的安全 Rust crate，其调用者自动获得上述保证，无需形式化验证。

### 5.2 所有权系统无法保证的 → 需要 Kani / Prusti / Miri

| 安全属性 | 为何 OBL 无法保证 | 推荐工具 |
|---------|------------------|---------|
| `unsafe` 块内的内存安全 | OBL 不检查原始指针操作 | Kani（验证）+ Miri（检测） |
| 数组/切片越界 | `vec[i]` 在运行时检查，OBL 不保证无 panic | Kani（证明 panic 自由） |
| 整数溢出（debug 模式 panic） | `overflow-checks` 是运行时行为 | Kani / Prusti（证明无溢出） |
| 功能正确性（算法输出正确） | OBL 只保证内存安全，不保证逻辑正确 | Prusti / Verus（契约验证） |
| 并发数据竞争（`unsafe impl Send/Sync`） | OBL 信任手工 trait 实现 | Miri（调度探索 + 检测） |
| 未初始化内存读取 | `MaybeUninit` 的正确使用依赖程序员 | Miri（运行时检测） |
| 类型布局违规（`transmute`） | OBL 允许 `transmute` 但无法验证其合法性 | Miri（检测非法 discriminant） |
| FFI 边界的安全性 | C 代码不遵循 OBL | Kani（验证 FFI 包装层） |

### 5.3 `unsafe` 边界的特殊处理

`unsafe` 是 Rust 形式化验证的重点区域。推荐的分层验证策略如下：

```text
unsafe 边界函数 f:
  ├─ 1. Miri: 运行所有现有测试，检测明显 UB
  ├─ 2. Kani: 为 f 编写 proof harness
  │          - 用 kani::any() 生成所有合法输入
  │          - 断言 f 不 panic、不越界、返回正确结果
  │          - 若 f 调用其他 unsafe 函数，逐一验证
  ├─ 3. Prusti: 为 f 的安全包装函数添加契约
  │          - unsafe 内部标记为 #[trusted]
  │          - 安全 API 的契约成为复用者的接口规约
  └─ 4. 文档: 在 rustdoc 中声明 "Verified with Kani/Prusti"
```

这与 `unsafe-verification.md` 中的策略一致：**`unsafe` 块的验证不是可选项，而是复用安全的前提条件**。公理 S.1（Interface Substitution）在 Rust 中的实例化即为：两个组件可互相替换，当且仅当它们的 `unsafe` 边界具有等价的安全保证。

---

## 6. 安装与运行参考

### 6.1 Miri

```bash
rustup toolchain install nightly --component miri
rustup override set nightly
cargo miri setup
cargo miri test
# 多线程调度探索
MIRIFLAGS="-Zmiri-many-seeds=0..16" cargo miri test
```

### 6.2 Kani

```bash
cargo install --locked kani-verifier
cargo kani setup
cargo kani
```

AWS Firecracker 已运行 27 个 Kani harnesses，每次约 15 分钟。

### 6.3 Prusti

```bash
prusti-rustc src/main.rs
# 或 cargo prusti
```

---

## 7. 推荐组合工作流

```bash
# 1. 日常开发
cargo test
cargo clippy -- -D warnings

# 2. 含 unsafe 的 PR
cargo miri test

# 3. 安全关键边界
# 为每个 unsafe 块编写 Kani harness
cargo kani

# 4. 公共 API 功能正确性
# 使用 Prusti 或 Verus 编写 requires/ensures

# 5. 发布前
cargo semver-checks
```

---

## 8. 文件索引

| 文件 | 说明 |
|------|------|
| `examples/miri_ub_demo.rs` | Miri 越界检测示例 |
| `examples/kani_abs_proof.rs` | Kani 绝对值证明 harness |
| `examples/prusti_add_contract.rs` | Prusti requires/ensures 示例 |
| `examples/verus_add_proof.rs` | Verus 加法无溢出证明 |
| `formal-semantics.md` | Rust 所有权-借用-生命周期形式化定义 |
| `unsafe-verification.md` | unsafe 边界验证策略总览 |
| `polonius-vs-nll.md` | Polonius 借用检查器与 NLL 对比 |

---

## 9. 权威参考

- **Kani**: <https://model-checking.github.io/kani/> —— AWS 开源的有界模型检验器；Firecracker 生产验证实践。
- **Prusti**: <https://www.pm.inf.ethz.ch/research/prusti.html> —— ETH Zurich 基于 Viper 的 Rust 契约验证器；用户指南 <https://viperproject.github.io/prusti-dev/user-guide/>。
- **Miri**: <https://github.com/rust-lang/miri> —— Rust 官方 MIR 解释器；UB 检测的语义基准。
- **RustBelt**: <https://plv.mpi-sws.org/rustbelt/> —— MPI-SWS 的 Rust 分离逻辑形式化；OBL 的数学基础。
- **Verus**: <https://verus-lang.github.io/verus/guide/> —— Microsoft/Amazon 工业级验证器；Anvil (OSDI'24) 验证 Kubernetes 控制器。
- **Aeneas / Charon**: <https://github.com/AeneasVerif/aeneas> —— Inria 的 Rust → Lean/Coq/F* 翻译链。
- **AutoVerus** (OOPSLA'25): <https://arxiv.org/abs/2409.13082> —— LLM 辅助 Verus 证明生成。
- **AlphaVerus**: <https://arxiv.org/abs/2412.06176> —— 神经符号证明合成。
- **Verina** (Lean 4 可验证代码生成): <https://arxiv.org/abs/2505.23135>

---

*文档生成时间：2026-06-08 · 对齐 Kani 0.66 / Prusti 活跃维护 / Miri POPL 2026 论文 · Phase 2 修订版*


---

## 补充说明：Rust 形式化验证工具链实践（2025‑2026）

## 反例

**反例**：在 Rust 中滥用 unsafe 块实现“性能优化”但未用 Miri 或形式化方法验证，导致复用该 unsafe 包装的多个项目出现未定义行为。

## 权威来源

> **权威来源**:
>
> - [The Rust Programming Language](https://www.rust-lang.org)
> - [RustBelt](https://iris-project.org/rustbelt.html)
> - [Aeneas](https://github.com/AeneasVerif/aeneas)
> - 核查日期：2026-07-07
