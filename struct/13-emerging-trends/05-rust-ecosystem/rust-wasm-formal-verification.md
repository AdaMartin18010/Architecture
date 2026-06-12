# Rust 生态：类型安全、WASM 目标与形式化验证
>
> 版本: 2026-06-06
> 对齐来源: Rust Project、Rust Formal Methods 社区、Kani/Miri/Prusti 项目、Rust WASM 工作组

## 1. Rust 类型系统的形式化基础

### 1.1 所有权（Ownership）与借用（Borrowing）

Rust 的核心创新是将内存安全规则编码进类型系统：

- **所有权规则**：每个值有且只有一个所有者；所有者离开作用域时值被释放
- **借用规则**：任意时刻，要么一个可变引用，要么任意数量的不可变引用
- **生命周期（Lifetimes）**：编译时验证引用始终有效

### 1.2 形式化研究

| 研究项目 | 机构 | 目标 |
|---------|------|------|
| **RustBelt** | MPI-SWS / IMDEA | Iris 框架下 Rust 核心语言的形式化语义 |
| **Aeneas** | EPFL | 从 Rust 提取纯函数式等价物用于证明 |
| **Creusot** | Inria | 基于 Why3 的 Rust 演绎验证 |
| **Prusti** | ETH Zurich / Viper Project | 基于 Viper 的 Rust 自动验证 |

## 2. 工业级验证工具链

### 2.1 Kani（AWS 开源）

- **定位**：Rust 代码的**模型检验器**
- **能力**：
  - 验证不安全（unsafe）代码块的内存安全
  - 检查并发原语的正确性
  - 证明属性在所有可能输入下成立
- **应用**：AWS 用于验证 Firecracker microVM、Bottlerocket 等关键组件

### 2.2 Miri（Rust 官方）

- **定位**：Rust 的**未定义行为检测器**
- **能力**：
  - 解释执行 Rust 中间表示（MIR）
  - 检测未对齐访问、数据竞争、无效内存使用
  - 验证不安全代码与 safe 抽象边界的正确性

### 2.3 Prusti

- **定位**：基于合同的 Rust 程序验证
- **能力**：
  - `#[requires(...)]` / `#[ensures(...)]` 合同注解
  - 纯函数（pure functions）与谓词（predicates）
  - 自动证明内存安全与功能正确性
- **状态**：研究原型，向工业可用性演进

### 2.4 工具对比

| 工具 | 方法 | 自动化 | 适用场景 |
|-----|------|--------|---------|
| Kani | 模型检验 | 高 | 不安全代码、并发、协议 |
| Miri | 动态解释 | 手动运行 | UB 检测、调试 |
| Prusti | 演绎验证 | 中高 | 合同驱动设计、算法正确性 |
| Creusot | 演绎验证 | 中 | 提取证明、功能验证 |

## 3. Rust 与 WebAssembly

### 3.1 WASM 作为 Rust 的一级目标

- Rust 原生支持 `wasm32-unknown-unknown` 和 `wasm32-wasip2` 目标
- `wasm32-wasip2`：支持 WASI 预览 2 和组件模型
- `wasm-bindgen`：Rust 与 JavaScript 的无缝互操作

### 3.2 组件模型开发

```rust
// WIT 接口定义
// package my:domain;
// interface calculator { add: func(a: u32, b: u32) -> u32; }

// Rust 实现（wasm32-wasip2 目标）
wit_bindgen::generate!({
    world: "calculator-world",
    exports: {
        "my:domain/calculator": Calculator,
    },
});

struct Calculator;
impl exports::my::domain::calculator::Guest for Calculator {
    fn add(a: u32, b: u32) -> u32 { a + b }
}
```

### 3.3 wasmCloud Rust SDK

- `wasmcloud-component` crate：预生成接口与惯用包装器
- 支持通过 `wasm32-wasip2` 目标构建组件
- 月下载量 1,700+（2026 初），增长迅速

## 4. Cargo 与依赖治理

### 4.1 依赖解析的确定性

- Cargo.lock 保证跨构建的依赖图一致性
- 与 SLSA 供应链安全天然契合：可复现构建基础

### 4.2 SBOM 生成

- `cargo-cyclonedx` / `cargo-spdx`：自动生成符合标准的 SBOM
- 与 EU CRA、NIST SSDF 合规要求对齐

### 4.3 不安全代码边界管理

| 策略 | 实现 | 复用保证 |
|-----|------|---------|
| `unsafe` 封装 | 最小化 `unsafe` 块，用 safe API 封装 | 调用方无需关心内部 unsafe |
| Miri CI | 持续集成中运行 Miri 检测 | 捕获回归的 UB |
| Kani 证明 | 对核心不安全代码进行模型检验 | 数学保证安全边界 |
| 审计 | `cargo-geiger` 统计 unsafe 使用量 | 透明度与风险评估 |

## 5. 跨领域复用案例

### 5.1 嵌入式（Embedded）

- `embedded-hal`：硬件抽象层trait，跨 MCU 厂商复用驱动
- `defmt`：高效的调试格式化，替代 `println!`
- `rtic` / `embassy`：异步嵌入式框架

### 5.2 系统编程

- Linux 内核模块（Rust for Linux）：逐步替代 C 驱动
- 操作系统（Redox OS）：纯 Rust 微内核
- 虚拟化（Firecracker）：AWS 的 microVM，Kani 验证关键路径

### 5.3 区块链与密码学

- `ring`、`rustls`：经形式化审查的密码学库
- Substrate / Polkadot：Wasm 运行时 + Rust 实现

## 6. 与功能安全的关系

Rust 尚未获得 IEC 61508 / ISO 26262 的工具资格认证，但正在向该方向演进：

- 内存安全保证减少系统性故障来源
- Kani/Miri 提供自动化验证证据
- 需要标准化机构评估 borrow checker 作为"技术"的资格

## 7. 参考索引

- Rust Project: [rust-lang.org](https://www.rust-lang.org)
- Kani Verifier: [github.com/model-checking/kani](https://github.com/model-checking/kani)
- Miri: [github.com/rust-lang/miri](https://github.com/rust-lang/miri)
- Prusti: [github.com/viperproject/prusti](https://github.com/viperproject/prusti)
- Creusot: [github.com/creusot-rs/creusot](https://github.com/creusot-rs/creusot)
- Rust for Linux: [rust-for-linux.com](https://rust-for-linux.com)
- wasmCloud Rust SDK: [crates.io/crates/wasmcloud-component](https://crates.io/crates/wasmcloud-component)
- Jung et al.: "RustBelt: Securing the Foundations of the Rust Programming Language" (POPL 2018)
