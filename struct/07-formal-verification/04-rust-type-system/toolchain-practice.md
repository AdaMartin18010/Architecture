# Rust 形式化验证工具链实践（2025‑2026）

> **定位**：为架构复用体系中“可复用 Rust 组件”提供从测试到证明的分层验证路径。
> **权威对齐**：Kani 0.66、Prusti、Miri 官方文档、Verus 2024 OSDI 论文、Aeneas/Charon ICFP 论文。

---

## 1. 分层验证策略

对于可复用 Rust 组件，推荐按以下层次递进，成本从低到高，保证从弱到强：

```text
Level 1: cargo test + cargo-semver-checks          （功能回归 + API 兼容性）
Level 2: Miri                                      （UB 动态检测）
Level 3: Kani                                      （有界模型检验）
Level 4: Prusti / Verus / Aeneas                   （演绎式功能正确性证明）
```

---

## 2. 工具总览

| 工具 | 验证目标 | 成熟度 | 适用场景 |
|------|----------|--------|----------|
| **Miri** | UB（越界、未初始化读取、别名违规等） | 官方稳定 | 所有含 `unsafe` 的测试 |
| **Kani** | 内存安全、panic 自由、用户断言 | AWS 生产使用 | 安全边界、`unsafe` FFI |
| **Prusti** | 功能正确性（requires/ensures） | 研究级，活跃维护 | 安全 Rust API 合约 |
| **Verus** | 功能正确性、并发、资源权限 | 工业级（Microsoft/Amazon） | 高安全系统组件 |
| **Aeneas** | 功能正确性（翻译到 Lean/Coq/F*） | 研究级 | 密码学/安全协议 |
| **cargo-semver-checks** | 语义版本兼容性 | 事实标准 | 每次发布前 |

---

## 3. Miri：动态 UB 检测

### 3.1 安装

```bash
rustup toolchain install nightly --component miri
rustup override set nightly
cargo miri setup
```

### 3.2 运行

```bash
cargo miri test
# 多线程调度探索
MIRIFLAGS="-Zmiri-many-seeds=0..16" cargo miri test
```

### 3.3 示例：`unsafe` 越界检测

见 `examples/miri_ub_demo.rs`

```rust
pub fn buggy_write(x: &mut [u8]) {
    unsafe {
        let p = x.as_mut_ptr();
        *p.add(10) = 1; // 当 x.len() < 11 时越界
    }
}
```

Miri 报告：

```
error: Undefined Behavior: out-of-bounds pointer arithmetic
```

---

## 4. Kani：有界模型检验

### 4.1 安装

```bash
cargo install --locked kani-verifier
cargo kani setup
```

### 4.2 证明 harness 示例

见 `examples/kani_abs_proof.rs`

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

运行：

```bash
cargo kani
```

### 4.3 与 CI 集成

```yaml
- uses: actions/checkout@v4
- run: cargo install --locked kani-verifier && cargo kani setup
- run: cargo kani
```

AWS Firecracker 已运行 27 个 Kani harnesses，每次约 15 分钟。

---

## 5. Prusti：基于 Viper 的演绎验证

### 5.1 示例

见 `examples/prusti_add_contract.rs`

```rust
use prusti_contracts::*;

#[requires(a > 0 && b > 0)]
#[ensures(result == a + b)]
fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

### 5.2 运行

```bash
prusti-rustc src/main.rs
# 或 cargo prusti
```

### 5.3 局限

- 主要支持 safe Rust，`unsafe` 支持有限。
- 外部 crate 需要手写 `extern_spec`。

---

## 6. Verus：Microsoft 工业级验证器

### 6.1 示例

见 `examples/verus_add_proof.rs`

```rust
use vstd::prelude::*;

verus! {

fn add(a: u32, b: u32) -> (c: u32)
    requires a <= 0xffff_ffff - b,
    ensures c == a + b,
{
    a + b
}

}
```

### 6.2 关键成果

| 项目 | 成果 |
|------|------|
| **Anvil** (OSDI'24 Best Paper) | 验证 Kubernetes 控制器活性 |
| **VeriSMo** (OSDI'24 Best Paper) | 验证 AMD SVSM 安全模块，发现真实漏洞 |
| **Atmosphere / TickTock** (SOSP'25) | 验证操作系统内核隔离 |

---

## 7. Aeneas：向后端证明助手翻译

### 7.1 工作流程

```bash
# 1. Charon 将 Rust crate 转换为 LLBC
cd rust-crate && charon cargo --preset=aeneas

# 2. Aeneas 翻译为 Lean / Coq / F* / HOL4
./bin/aeneas -backend lean crate.llbc
```

### 7.2 局限

- 仅支持 safe Rust（`unsafe`、内部可变性、并发正在研究中）。
- 生成的证明助手代码较冗长。

---

## 8. cargo-semver-checks：API 兼容性

```bash
cargo install cargo-semver-checks --locked
cargo semver-checks
```

推荐在每次发布前运行，避免破坏下游用户。

---

## 9. 推荐组合工作流

```bash
# 1. 日常开发
cargo test
cargo clippy -- -D warnings

# 2. 含 unsafe 的 PR
cargo miri test

# 3. 安全关键边界
# 为每个 `unsafe` 块编写 Kani harness
cargo kani

# 4. 公共 API 功能正确性
# 使用 Prusti 或 Verus 编写 requires/ensures

# 5. 发布前
cargo semver-checks
```

---

## 10. 文件索引

| 文件 | 说明 |
|------|------|
| `examples/miri_ub_demo.rs` | Miri 越界检测示例 |
| `examples/kani_abs_proof.rs` | Kani 绝对值证明 harness |
| `examples/prusti_add_contract.rs` | Prusti requires/ensures 示例 |
| `examples/verus_add_proof.rs` | Verus 加法无溢出证明 |

---

## 11. 权威参考

- Kani Docs: <https://model-checking.github.io/kani/>
- Miri Docs: <https://github.com/rust-lang/miri>
- Prusti User Guide: <https://viperproject.github.io/prusti-dev/user-guide/>
- Verus Tutorial: <https://verus-lang.github.io/verus/guide/>
- Aeneas / Charon: <https://github.com/AeneasVerif/aeneas>
- cargo-semver-checks: <https://github.com/obi1kenobi/cargo-semver-checks>
- AutoVerus (OOPSLA'25): <https://arxiv.org/abs/2409.13082>
- AlphaVerus: <https://arxiv.org/abs/2412.06176>
- Verina (Lean 4 可验证代码生成): <https://arxiv.org/abs/2505.23135>

---

*文档生成时间：2026-06-06 · 对齐 Kani 0.66 / Verus 工业实践 / Miri POPL 2026 论文*
