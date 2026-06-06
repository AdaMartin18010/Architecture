# WebAssembly 组件模型与 WASI 复用生态
>
> 版本: 2026-06-06
> 对齐来源: Bytecode Alliance、W3C WebAssembly CG、wasmCloud CNCF、WASI 路线图、Platform.Uno 2026 状态报告

## 1. 技术里程碑（2025–2026）

### 1.1 标准化完成（Phase 5）

| 特性 | 状态 | 意义 |
|-----|------|------|
| Exception Handling (exnref) | 已完成 | 所有主流浏览器支持 |
| JavaScript String Builtins | 已完成 | 跨语言字符串互操作 |
| Memory64 | 已完成 | 突破 4GB 内存限制（浏览器上限 16GB）|

### 1.2 进展中的关键提案

| 提案 | 阶段 | 说明 |
|-----|------|------|
| **Stack Switching** | Phase 3 | 允许多执行栈并发管理，支持 async/await、协程、生成器 |
| **Wide Arithmetic** | Phase 3 | 128-bit 整数运算加速（当前慢 2–7 倍）|
| **WebAssembly CSP** | 推进中 | `wasm-unsafe-eval` 关键词标准化，浏览器 CSP 支持 |

### 1.3 WebAssembly 3.0

- 2025 年宣布，将多项新特性纳入主规范
- 浏览器采用率：Chrome Platform Status 显示 5.5% 网站使用 Wasm（持续增长）
- 前 25 种编程语言中几乎全部支持 Wasm 编译目标

## 2. WASI 演进路线图

### 2.1 WASI 0.2（2024 早期）

- 引入 **Component Model** 支持多模块链接
- 定义 **Worlds** 概念：模块可访问的标准接口集合
- 支持 `wasi-http` 等高级世界

### 2.2 WASI 0.3（预期 2026-02 发布）

- **原生异步支持**：Component Model 内置 async/await
- **效果**：Wasmtime 运行时已有实验性支持
- **目标场景**：
  - 边缘设备
  - 异步与事件驱动架构
  - Serverless 环境
  - 大规模终端节点单次发布部署

### 2.3 WASI 1.0（预期 2026 底–2027 初）

- WASI 的完整稳定版
- Component Model 将在 0.3 或 1.0 后开始推进规范阶段

## 3. 组件模型（Component Model）

### 3.1 核心概念

组件模型是 WebAssembly 的**模块化与互操作层**：

- **语言无关**：不同语言编译的模块可通过标准接口互操作
- **接口类型（Interface Types, WIT）**：定义组件间契约
- **组合（Composition）**：将多个小组件组合为复杂应用

### 3.2 复用架构

```
Application Component
├── import "wasi:cli/stdout"
├── import "wasi:http/incoming-handler"
├── import "my:domain/payment-service"
└── export "my:domain/order-api"

Payment Service Component
├── import "wasi:io/streams"
└── export "my:domain/payment-service"
```

### 3.3 引用类型（Reference Types）

- 组件可暴露有意义的 API，开发者无需理解 Wasm 内部机制
- 大幅降低使用门槛，推动跨语言库复用

## 4. wasmCloud（CNCF 项目）

### 4.1 定位

> "wasmCloud is an open source CNCF project that enables teams to build, manage, and scale polyglot Wasm apps across any cloud, K8s, or edge."

### 4.2 关键版本

| 版本 | 时间 | 特性 |
|-----|------|------|
| 1.0 | 2024-05 | 稳定运行时、组件支持 |
| 2.0 | 2026-03-23 | 下一代运行时、性能提升 |
| WASI P3 | 2026-04 | 异步组件支持 |

### 4.3 核心能力

- **多语言应用**：Go、Rust、Python、C 等编译为 Wasm 组件，统一部署
- **分布式 ML/AI 工作负载**：模型推理组件在边缘/云端弹性调度
- **SPIFFE 工作负载身份**：2025-03 采用 SPIFFE 实现 WebAssembly 负载身份安全
- **平台工程集成**：Platform Harness 模式，将 Wasm 作为平台能力交付

### 4.4 企业采用

- Adobe：将 C 代码编译为 WebAssembly 组件运行于 wasmCloud
- 各类云原生/边缘场景的渐进采用

## 5. 语言与框架支持（2026）

| 语言 | Wasm 支持状态 | 组件模型支持 |
|-----|-------------|-------------|
| Rust | 原生一级支持 | `wasm32-wasip2` 目标 |
| Go | TinyGo + 官方支持 | wasmCloud Go SDK |
| Python | Componentize-py | 实验性 |
| C/C++ | Emscripten / WASI SDK | 成熟 |
| .NET | .NET 10 | 与 Uno Platform 协作多线程 |
| Kotlin | Beta Wasm 编译器 | Compose Multiplatform |
| JavaScript/TypeScript | JCO 工具链 | 组件封装与调用 |

## 6. 复用模式

### 6.1 跨语言库复用

- **场景**：Rust 编写的加密库被 Go、Python、JS 应用调用
- **机制**：WIT 接口定义 + 组件组合
- **优势**：无需 FFI 绑定，沙箱隔离保证安全

### 6.2 边缘-云协同复用

```
Cloud
├── 大型推理模型（LLM）
└── 训练与模型更新

Edge
├── 小型 Wasm 组件（预处理/过滤）
├── TinyML 推理组件
└── 本地决策逻辑
```

### 6.3 平台能力复用

| 能力 | Wasm 组件形式 | 运行时 |
|-----|-------------|--------|
| HTTP 网关 | `wasi:http` 处理器 | wasmCloud / WasmEdge |
| 密钥管理 | `wasi:keyvalue` | 任何 WASI 运行时 |
| 消息处理 | `wasi:messaging` | NATS + wasmCloud |
| AI 推理 | ONNX Runtime Wasm | wasmCloud ML 组件 |

## 7. 调试与工具链成熟

- **DWARF 支持**：LLDB 调试器支持独立运行时调试
- **VS Code 集成**：部分 IDE 集成浏览器调试，无需 DevTools
- **.NET 性能分析**：Wasm 性能剖析与诊断数据提取

## 8. 参考索引

- W3C WebAssembly Community Group: [webassembly.org](https://webassembly.org)
- Bytecode Alliance: [bytecodealliance.org](https://bytecodealliance.org)
- wasmCloud: [wasmcloud.com](https://wasmcloud.com)
- WasmEdge: [wasmedge.org](https://wasmedge.org)
- WASI Roadmap: [github.com/WebAssembly/WASI](https://github.com/WebAssembly/WASI)
- Platform.Uno: "The State of WebAssembly – 2025 and 2026" (2026-01-27)
- InfoQ / The New Stack: "WASI 1.0: WebAssembly 可能在 2026 悄然普及" (2026-01)
