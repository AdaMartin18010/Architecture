# WASI 0.3 / Wasm Component Model：组件复用边界权威对齐（2025‑2026）

> **版本**：WASI 0.3 Preview · Wasmtime 37+ · WIT / Component Model 协定
> **来源对齐**：WebAssembly CG / WASI Subgroup、Wasmtime release notes、Bytecode Alliance blog
> **定位**：架构复用体系中 WebAssembly 组件边界的最新实践基准

---

## 1. 关键结论（TL;DR）

| 维度 | 关键结论 |
|------|----------|
| **WASI 0.3** | 2025 年进入 Preview，原生支持 `stream` / `future`，引入异步 IO；Wasmtime 37+ 已默认支持。 |
| **WASI 1.0** | 官方目标 2026 年末发布，届时 WASI 0.2（同步世界）进入维护模式，0.3 成为推荐主线。 |
| **组件复用边界** | 组件 = 强类型化的可组合 Wasm 单元，WIT 接口替代 ad‑hoc ABI，成为跨语言复用的“API 契约”。 |
| **可移植性** | 通过 `wasi:io/poll`、`wasi:clocks`、`wasi:http` 等标准化接口实现跨运行时复用。 |
| **与容器关系** | 组件不是容器的替代品，而是**更细粒度、冷启动更快、沙箱更轻**的复用单元，二者互补。 |
| **对项目意义** | 为 `struct/04-component-architecture-reuse/` 的组件层提供可执行、跨语言的最终运行时边界。 |

---

## 2. WASI 路线图：从 0.2 → 0.3 → 1.0

```text
2024 Q2      WASI 0.2 正式发布（同步 HTTP、文件系统、时钟）
2025 Q1‑Q3   WASI 0.3 Preview：引入 stream/future、异步 IO、Component Model 绑定
2025 Q4      Wasmtime 37 默认启用 0.3；工具链完善
2026 Q4      WASI 1.0 目标 GA，0.2 进入维护，0.3 转正
```

### 2.1 WASI 0.3 核心变更

| 能力 | 0.2 状态 | 0.3 状态 |
|------|----------|----------|
| IO 模型 | 同步 `blocking‑read/write` | 异步 `stream<T,E>` + `future<T,E>` |
| HTTP | `wasi:http/outgoing-handler` 同步 | 原生异步请求/响应流 |
| 文件系统 | 同步 open/read/write | 异步 `input‑stream` / `output‑stream` |
| 定时器 | `wasi:clocks/monotonic-clock` sleep | 与 async/await 集成 |
| 错误处理 | `result<T, string>` 为主 | 结构化错误 `result<T, E>`  richer variant |

> **来源**：Bytecode Alliance *WASI 0.3 Preview* 公告（2025）; Wasmtime 37 release notes。

---

## 3. Component Model 作为复用契约

### 3.1 组件 vs 模块

| 特性 | Wasm 模块 | Wasm Component |
|------|-----------|----------------|
| 接口 | 导出线性内存 + 函数表 | 导出 WIT 接口 |
| 类型系统 | 仅数值类型 | WIT record、variant、option、result、resource |
| 组合 | 低（依赖具体 ABI） | 高（`wasm-tools compose`） |
| 跨语言 | 需手动 FFI | 原生支持多语言 guest/host |
| 沙箱 | 线性内存 |  capability-based 子系统隔离 |

### 3.2 典型复用模式

```wit
// example: calculator.wit
package reuse:calculator@0.1.0;

interface ops {
    enum op { add, sub, mul, div }
    record expr { op: op, lhs: f64, rhs: f64 }
    eval: func(e: expr) -> result<f64, string>;
}

world calculator-world {
    export ops;
}
```

**多语言实现复用**：

- Guest：Rust（`cargo component`）、Go（`wit-bindgen-go`）、Python（`componentize-py`）
- Host：任何支持 Component Model 的运行时（Wasmtime、WasmEdge、JCO 等）

---

## 4. 架构复用分层中的 WASI 0.3 位置

```text
┌─────────────────────────────────────────────────────────┐
│  业务架构层 (Business Capabilities)                      │
├─────────────────────────────────────────────────────────┤
│  应用架构层 (Applications / Services)                    │
├─────────────────────────────────────────────────────────┤
│  组件架构层 (Components)                                 │
│  ├── 微服务组件（容器/K8s）                               │
│  ├── 库组件（crate / npm / PyPI）                        │
│  └── Wasm 组件（WIT 接口 + WASI 0.3 运行时）  ← 本文件    │
├─────────────────────────────────────────────────────────┤
│  功能架构层 (Functions / Serverless / FaaS)              │
└─────────────────────────────────────────────────────────┘
```

### 4.1 与项目既有结构的映射

| 项目目录 | WASI 0.3 角色 |
|----------|---------------|
| `struct/04-component-architecture-reuse/` | 组件层设计原则与模式 |
| `struct/05-functional-architecture-reuse/` | 函数级触发器、WASI 0.3 事件驱动 |
| `struct/10-supply-chain-security/` | 组件来源验证（SLSA + Wasm 签名） |
| `struct/13-emerging-trends/03-webassembly-components/` | 前沿趋势与实践 |

---

## 5. 运行时边界最佳实践

### 5.1 最小权限原则（Capability-based）

```sh
# 仅授权 HTTP 和时钟能力
wasmtime run --wasi http --wasi clocks ./my-component.wasm
```

WASI 0.3 保持 **capability-based security**：组件默认无任何系统访问权限，必须通过 WIT world 显式导入。

### 5.2 组件组合而非继承

```sh
wasm-tools compose -o composed.wasm \
  -c config.yaml \
  main-component.wasm plugin-component.wasm
```

复用策略：将高频更新的业务逻辑封装为小组件，通过 WIT 接口组合到稳定的核心组件中。

### 5.3 版本管理与注册表

| 工具 | 用途 |
|------|------|
| `wasm-pkg-tools` | 基于 OCI 的 WebAssembly 组件注册表工具链（Bytecode Alliance 推荐） |
| `cargo component` | Rust 组件开发工作流 |
| `wasm-tools` | 组件打包、组合、反汇编 |
| `wasmtime` | 参考运行时 |

---

## 6. 可执行示例：Rust → Wasm 组件 → Host 调用

### 6.1 WIT 定义

```wit
// adder.wit
package reuse:adder@0.1.0;

interface add {
    add: func(a: u32, b: u32) -> u32;
}

world adder {
    export add;
}
```

### 6.2 Rust Guest 实现（cargo component）

```rust
// src/lib.rs
#[allow(warnings)]
mod bindings;

use bindings::exports::reuse::adder::add::Guest;

struct Component;

impl Guest for Component {
    fn add(a: u32, b: u32) -> u32 {
        a + b
    }
}

bindings::export!(Component with_types_in bindings);
```

```toml
# Cargo.toml
[package]
name = "reuse-adder"
version = "0.1.0"
edition = "2021"

[dependencies]
wit-bindgen-rt = { version = "0.41.0", features = ["bitflags"] }

[package.metadata.component]
package = "reuse:adder"
```

构建：

```bash
cargo component build --release
# 输出 target/wasm32-wasip1/release/reuse_adder.wasm
```

### 6.3 Host 调用（Python + wasmtime）

```python
from wasmtime import Store, Module, Instance, Engine

engine = Engine()
store = Store(engine)
module = Module.from_file(engine, "target/wasm32-wasip1/release/reuse_adder.wasm")
instance = Instance(store, module, [])
add = instance.exports(store)["add"]
print(add(store, 2, 3))  # 5
```

> 注：实际 Component Model 调用需使用 `wasmtime.Component`，上述为简化示意。

---

## 7. 与 MCP / A2A 的互补关系

| 协议 | 定位 | 与 WASI 0.3 的关系 |
|------|------|---------------------|
| **MCP 2025-11-25** | AI Agent ↔ 工具/数据服务器协议 | WASI 0.3 组件可作为 MCP Server 的运行时沙箱 |
| **A2A** | Agent ↔ Agent 协作协议 | WASI 组件提供 A2A Agent 的跨语言可移植执行单元 |
| **WASI 0.3** | 组件能力与安全边界 | 为 MCP/A2A 工具提供**可验证、可组合、最小权限**的底层载体 |

**复用优势**：MCP Server 的算子逻辑可用 Rust 编写为 Wasm 组件，分发到任何支持 WASI 0.3 的运行时，无需重新编译或担心依赖冲突。

---

## 8. 工具链与版本速查

| 工具 | 推荐版本 | 说明 |
|------|----------|------|
| Wasmtime | ≥ 37 | 默认 WASI 0.3 支持 |
| wasm-tools | ≥ 1.228 | 组件组合、WIT 解析 |
| cargo-component | ≥ 0.22 | Rust 组件开发 |
| wit-bindgen | ≥ 0.41 | 多语言绑定生成 |
| `wasm-pkg-tools` | ≥ 0.4 | 基于 OCI 的组件注册表交互 |

---

## 9. 权威来源

1. **Bytecode Alliance — WASI 0.3 Preview**（2025）
2. **Wasmtime Release Notes 37+** — <https://github.com/bytecodealliance/wasmtime/releases>
3. **WebAssembly Component Model Spec** — <https://component-model.bytecodealliance.org/>
4. **WIT 设计文档** — <https://github.com/WebAssembly/component-model/blob/main/design/mvp/WIT.md>
5. **wasm-pkg-tools / OCI-based registry** — <https://github.com/bytecodealliance/wasm-pkg-tools>（warg 已停止积极开发，社区转向 OCI-based registry）
6. **《WebAssembly: The Definitive Guide》2nd ed.**（2026 预计出版）

---

## 10. 项目后续行动

1. **在本目录创建可运行的示例仓库**：一个 Rust 组件 + Python Host + CI 验证流程。
2. **更新 `struct/04-component-architecture-reuse/README.md`**，加入 Wasm 组件作为第四种组件形态（与库、服务、框架并列）。
3. **更新形式化验证环境**：探讨将 WASI 0.3 WIT 接口作为 TLA+/Alloy 的组件边界规约对象。
4. **与 SLSA 对齐**：Wasm 组件的 SBOM 与签名机制需与 `struct/10-supply-chain-security/` 的供应链安全框架打通。

---

*文档生成时间：2026-06-06 · 对齐官方 WASI 0.3 Preview 及 Wasmtime 37+ 状态*
