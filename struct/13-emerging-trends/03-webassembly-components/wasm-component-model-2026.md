# WebAssembly 组件模型与 WASI 复用生态
>
> 版本: 2026-07-09
> 对齐来源: Bytecode Alliance Component Model、WASI 0.3 Roadmap、Wasmtime、W3C WebAssembly 3.0、wasmCloud CNCF

## 1. 技术里程碑（2025–2026）

### 1.1 WebAssembly 3.0 标准化完成

2025 年 9 月 17 日，W3C WebAssembly 社区组与工作组的 **WebAssembly 3.0** 成为正式 live standard。该版本被规范作者称为自 Wasm 诞生以来最大的一次更新，整合了多项开发周期达 6–8 年的提案：

| 特性 | 状态 | 意义 |
|-----|------|------|
| Memory64 | 已完成 | 地址类型扩展为 `i64`，理论地址空间从 4 GB 提升到 16 EB，浏览器上限约 16 GB |
| WasmGC | 已完成 | 宿主引擎原生垃圾回收，Java/Kotlin/Dart 等语言无需打包完整 GC 运行时 |
| Exception Handling (exnref) | 已完成 | 结构化异常传播，所有主流浏览器已支持 |
| Tail Calls | 已完成 | 递归语言实现可进行尾调用优化 |
| 128-bit SIMD | 已完成 | 计算密集型负载标准化向量运算 |

浏览器采用率持续增长：Chrome Platform Status 显示约 **5.5%** 的网站使用 Wasm；全球前 25 种编程语言中几乎全部支持 Wasm 编译目标。

## 2. 核心概念与定义

### 2.1 组件模型（Component Model）

**WebAssembly Component Model** 是 Wasm 的模块化与互操作层，将单个 Wasm 模块提升为**组件（Component）**：一种具有显式、类型化导入（import）与导出（export）接口的可组合单元。组件之间通过 **WebAssembly Interface Types（WIT）** 定义契约，实现跨语言、跨运行时的二进制复用。

| 属性 | 说明 | 复用价值 |
|:---|:---|:---|
| **语言无关** | Rust、Go/TinyGo、Python、C#、JS/TS、C/C++ 等均可编译为组件 | 打破语言孤岛 |
| **接口类型化** | WIT 强类型接口，编译期与运行期均可校验 | 明确契约，降低集成风险 |
| **沙箱隔离** | 基于 capability-based security，默认最小权限 | 安全复用不可信第三方组件 |
| **可组合性** | 多个小组件可静态或动态组合为复杂应用 | 支持平台能力模块化交付 |
| **可移植性** | 一次编译，可在浏览器、边缘、K8s、Serverless 运行时运行 | 资产跨环境复用 |

### 2.2 WASI（WebAssembly System Interface）

WASI 是组件访问操作系统能力的标准接口集合。WASI 0.3 基于 Component Model 构建，在 ABI 层引入 `stream<T,E>` / `future<T,E>` 类型，使语言绑定可生成惯用的 `await`。

| 版本 | 发布时间 | 关键特性 |
|-----|---------|---------|
| WASI 0.1 (Preview 1) | 2019 | 基本文件/环境访问，类 POSIX ABI |
| WASI 0.2 (Preview 2) | 2024-01-25 | 稳定 Component Model、`wasi:http` / `wasi:sockets`、WIT 接口 |
| **WASI 0.3 (Preview 3)** | **2025-11 RC / 2026-02 preview** | **原生 async/await、`stream<T>`/`future<T>`、接口资源类型精简** |
| WASI 1.0 | 预计 2026 末–2027 初 | 长期稳定版，无破坏性变更 |

WASI 0.3 的关键改进：

- `wasi:http@0.3.0` 资源类型从 0.2.4 的 11 个精简到 5 个，降低约 55% 的 API 表面。
- 同一组件可同时导出 WASI 0.2 与 0.3 接口；0.3 运行时可通过适配层执行 0.2 模块，支持渐进迁移。
- Wasmtime 37+ 已提供实验性支持，Fermyon Spin v3.5（2025-11）已发布首个 RC 支持。

> **实践提示**：截至 2026 年中，生产部署仍建议以 WASI 0.2（`wasm32-wasip2`）为主，WASI 0.3 作为架构演进目标跟踪。详见 [`wasm-wasi-03-boundaries.md`](./wasm-wasi-03-boundaries.md)。

## 3. WIT：组件的接口契约语言

**WIT（WebAssembly Interface Types）** 是 Component Model 的接口定义语言（IDL）。一个 WIT 文件描述包（package）、接口（interface）和世界（world）：

```wit
package my:domain@0.1.0;

interface image-processor {
    resize: func(input: list<u8>, width: u32, height: u32) -> result<list<u8>, string>;
    detect-format: func(input: list<u8>) -> string;
}

world image-api {
    export image-processor;
    import wasi:io/streams@0.2.0;
}
```

- **package**：命名空间与版本管理单元，建议显式声明语义版本。
- **interface**：一组类型化函数，可被 import 或 export，是组织内复用的推荐粒度。
- **world**：组件可见能力集合，定义可使用的标准接口与暴露的自定义接口。

## 4. 复用架构与组合示例

### 3.1 跨语言库复用

```text
Application Component
├── import "wasi:cli/stdout"
├── import "wasi:http/incoming-handler"
├── import "my:domain/payment-service"
└── export "my:domain/order-api"

Payment Service Component
├── import "wasi:io/streams"
└── export "my:domain/payment-service"
```

**场景**：用 Rust 实现图像处理组件，被 Node.js、Python 和 Go 复用。

```rust
// Rust 实现（wasm32-wasip2 目标）
wit_bindgen::generate!({
    world: "image-api",
    exports: { "my:domain/image-processor": ImageProcessor }
});

struct ImageProcessor;
impl exports::my::domain::image_processor::Guest for ImageProcessor {
    fn resize(input: Vec<u8>, w: u32, h: u32) -> Result<Vec<u8>, String> { /* ... */ }
    fn detect_format(input: Vec<u8>) -> String { /* ... */ }
}
```

消费方绑定：

- **Node.js/TypeScript**：`@bytecodealliance/jco` 生成 ESM / TypeScript 存根。
- **Python**：`componentize-py` 生成 Python 绑定。
- **Go**：TinyGo + `wit-bindgen-go` 生成客户端。

结果：同一二进制组件在三种语言运行时中复用，无需手写 FFI。

### 3.2 边缘-云协同复用

```text
Cloud
├── 大型推理模型（LLM）
└── 训练与模型更新

Edge
├── 小型 Wasm 组件（预处理/过滤）
├── TinyML 推理组件
└── 本地决策逻辑
```

### 3.3 平台能力复用

| 能力 | Wasm 组件形式 | 运行时 |
|-----|-------------|--------|
| HTTP 网关 | `wasi:http` 处理器 | wasmCloud / WasmEdge / Wasmtime |
| 密钥管理 | `wasi:keyvalue` | 任何 WASI 运行时 |
| 消息处理 | `wasi:messaging` | NATS + wasmCloud |
| AI 推理 | ONNX Runtime Wasm | wasmCloud ML 组件 |

## 5. 运行时与平台生态

### 4.1 Wasmtime（Bytecode Alliance 参考运行时）

- 2022-09-20 发布 1.0 并宣布生产就绪。
- 2024-01-25 完整支持 WASI 0.2 / Component Model。
- 2026 年 Wasmtime 43+ 支持 WASI 0.3 运行时特性（实验性）。
- CLI 支持 `wasmtime run`、`wasmtime serve` 以及多语言嵌入绑定（Rust、C、Python、.NET、Go）。

### 4.2 wasmCloud（CNCF 项目）

> "wasmCloud is an open source CNCF project that enables teams to build, manage, and scale polyglot Wasm apps across any cloud, K8s, or edge."

| 版本 | 时间 | 特性 |
|-----|------|------|
| 1.0 | 2024-05 | 稳定运行时、组件支持 |
| 2.0 | 2026-03-23 | 下一代运行时、性能提升 |
| WASI P3 | 2026-04 | 异步组件支持 |

核心能力：

- 多语言应用统一通过 `wasm32-wasip2` 目标构建组件并部署。
- 2025-03 采用 SPIFFE 实现 WebAssembly 负载身份安全。
- Platform Harness 模式将 Wasm 作为平台能力交付。

企业采用案例：Adobe 将 C 代码编译为 WebAssembly 组件运行于 wasmCloud。

## 6. 语言与框架支持（2026）

| 语言 | Wasm 支持状态 | 组件模型支持 |
|-----|-------------|-------------|
| Rust | 原生一级支持 | `wasm32-wasip2`（Tier 2） |
| Go | TinyGo 官方支持 | `wit-bindgen-go` + wasmCloud Go SDK |
| Python | `componentize-py` | 稳定 |
| C/C++ | WASI SDK / Emscripten | 成熟 |
| C# / .NET | `componentize-dotnet` | 稳定 |
| JavaScript/TypeScript | `jco` + `componentize-js` | 稳定 |
| Kotlin | Kotlin/Wasm Beta | 与 Compose Multiplatform 协作 |
| Java | GraalWasm / Endive（2026-05 发布） | 路线图中 |

Rust 目标更新：自 Rust 1.84（2025-01）起，旧的 `wasm32-wasi` 目标被移除，取而代之的是 `wasm32-wasip1`（Tier 2）与 `wasm32-wasip2`（Tier 3，组件模型）。

## 7. WASM 组件复用边界与架构分析

组件复用并非"一切 WASM 化"。基于 [`wasm-wasi-03-boundaries.md`](./wasm-wasi-03-boundaries.md) 的边界分析，建议按以下规则决策：

| 适合 WASM Component | 不适合 WASM Component |
|:---|:---|
| 跨语言共享的算法/工具库（加密、图像处理、协议解析） | 强 OS 依赖、大量原生系统调用 |
| 需要亚秒级冷启动的边缘函数/插件 | 长时间运行、有状态且需要复杂线程模型的服务 |
| 多租户场景下的不可信第三方代码沙箱 | 对峰值吞吐延迟极度敏感、无法容忍任何虚拟化开销的核心路径 |
| 已通过 WIT 明确契约的模块级能力 | 未定义接口、频繁变更的内部实现细节 |

**推荐粒度**：

- 以 **WIT `interface`** 作为组织内复用的标准粒度；
- 完整 `world` 组件适合对外交付或跨团队部署；
- 函数级粒度过细，契约维护成本高；应用级粒度过粗，丧失组件组合优势。

## 8. 工具链与生态系统分析

- **DWARF 支持**：LLDB 调试器支持独立运行时调试。
- **VS Code 集成**：部分 IDE 集成浏览器调试，无需 DevTools。
- **组件注册表**：Bytecode Alliance 的 `warg` 协议与 OCI artifact 支持，使组件可通过标准基础设施分发。
- **工具链**：`wasm-tools`（链接、检查、验证）、`cargo-component`（Rust）、`jco`（JS/TS）、`componentize-py`（Python）、`wit-bindgen`（多语言绑定）。

## 9. 正向示例

### 示例：跨语言图像处理组件复用

某电商平台将图片压缩、格式转换、水印生成实现为独立的 Rust WASM 组件，通过 WIT 接口 `my:domain/image-processor` 暴露给：

- **Node.js 前端服务**：处理用户上传图片；
- **Python 批处理服务**：处理历史图片资产；
- **Go 边缘网关**：在边缘节点完成实时缩略图生成。

结果：

- 同一核心算法只需维护一份 Rust 代码；
- 组件更新时所有消费方自动获得一致行为；
- 新语言栈团队可在 1 天内接入，无需重写核心逻辑。

## 10. 反例 / 反模式

### 反例：阻塞式 I/O 直接迁移 WASM

某团队将大量阻塞式文件 I/O 逻辑直接迁移到 WASM，未使用 WASI 0.3 的异步 `stream`/`future` 能力，也未通过 WIT 暴露接口，而是依赖宿主与 Guest 之间的共享内存约定。结果：

- 运行时阻塞导致延迟飙升，CPU 利用率低下；
- 不同语言消费方需要各自实现内存编解码，重复了 FFI 的痛苦；
- 调试困难，组件边界模糊，最终回退为原生动态库。

### 反模式：过度拆分函数级组件

某团队将每个业务函数都编译为独立 Wasm 组件，导致：

- WIT 文件数量爆炸，版本管理困难；
- 组件组合和启动开销超过性能收益；
- 团队将大量时间花在接口契约维护而非业务逻辑上。

正确做法：以 **interface 粒度**组织复用单元，将紧密相关的函数放在同一接口中。

## 11. 权威来源

| 来源 | URL | 核查日期 |
|:---|:---|:---|
| WebAssembly Component Model | <https://component-model.bytecodealliance.org> | 2026-07-09 |
| WASI — WebAssembly System Interface | <https://wasi.dev> | 2026-07-09 |
| WASI Roadmap (GitHub) | <https://github.com/WebAssembly/WASI> | 2026-07-09 |
| Wasmtime Runtime | <https://github.com/bytecodealliance/wasmtime> | 2026-07-09 |
| wasmCloud | <https://wasmcloud.com> | 2026-07-09 |
| The State of WebAssembly 2025–2026 | <https://platform.uno/blog/the-state-of-webassembly-2025-2026/> | 2026-07-09 |

> **关键引用**：根据 Bytecode Alliance 与 Platform.Uno 2026-01-27 的状态报告，WebAssembly 3.0 于 2025-09-17 成为 live standard；WASI 0.3 在 2026-02 通过 Wasmtime 37+ 提供预览支持，预计 2026 末–2027 初发布 WASI 1.0。

## 12. 交叉引用

- WASI 0.3 边界分析详见 [`wasm-wasi-03-boundaries.md`](./wasm-wasi-03-boundaries.md)
- WASM 复用决策树详见 [`wasm-reuse-decision-tree.md`](./wasm-reuse-decision-tree.md)
- Rust/WASM 形式化验证详见 [`../05-rust-ecosystem/rust-wasm-formal-verification.md`](../05-rust-ecosystem/rust-wasm-formal-verification.md)
