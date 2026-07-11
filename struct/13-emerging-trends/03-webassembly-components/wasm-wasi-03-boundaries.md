# P5-T4：WASM Component Model + WASI 0.3 复用边界更新

> **权威来源**：wasi.dev、bytecodealliance.org、wasmtime releases (v45.0.0 / LTS v36.0.0)、W3C WebAssembly 3.0 (2025.09)
> **版本**：2026-06
> **适用范围**：跨语言组件复用、边缘/云原生沙箱化部署

---

## 1. WASI 0.3 最新状态（2026-06-11 正式发布）

### 1.1 原生 async I/O：stream<T> / future<T>

WASI 0.3.0 于 **2026-06-11 正式发布**（2025 年 11 月进入 RC 阶段；Wasmtime 43+ / jco 已支持），其核心变革是引入了**原生异步 I/O 抽象**：

- **`stream<T>`**：表示异步数据流（如 HTTP 请求体、文件流），支持背压（backpressure）和批量读写
- **`future<T>`**：表示一次性异步计算结果，对标 Rust `Future`、JavaScript `Promise`

这一设计彻底解决了 WASI 0.2 中异步操作需通过外部轮询或回调实现的痛点。在 0.3 模型中，Host 可以直接向 Guest 传递未完成的 future，Guest 通过 WIT 生成的绑定代码以语言惯用方式（如 `await`）处理异步操作，无需显式管理轮询循环。

### 1.2 与 WASI 0.2 的兼容性策略

Bytecode Alliance 采取了**渐进式迁移**策略：

| 维度 | WASI 0.2 | WASI 0.3 | 兼容性措施 |
|------|----------|---------------|-----------|
| 异步模型 | 基于 `poll` 的显式轮询 | `stream<T>` / `future<T>` 原生 async | 0.3 运行时兼容执行 0.2 模块（通过适配层） |
| 接口版本 | `wasi:http@0.2.0` | `wasi:http@0.3.x` | 同一组件可同时导出 0.2 和 0.3 接口 |
| 工具链 | wit-bindgen 0.30+ | wit-bindgen 0.40+（支持 0.3） | 双版本 WIT 文件共存 |

**迁移建议**：现有 WASI 0.2 组件无需立即重写。Wasmtime v45 同时支持 0.2 和 0.3，组织可按**新组件用 0.3、存量组件逐步迁移**的节奏推进。

### 1.3 Wasmtime LTS 模式

| 版本 | 发布日期 | 支持周期 | 适用场景 |
|------|---------|---------|---------|
| **Wasmtime v45.0.0** | 2026-05 | 常规支持（约 6 个月） | 跟进最新特性、开发测试 |
| **Wasmtime LTS v36.0.0** | 2024-11 | **2 年安全支持** | 生产环境、合规要求长周期支持 |

LTS 版本保证安全补丁和关键修复的向后兼容，是金融、医疗等监管敏感行业的推荐选择。组织应在**平台工程层统一 Wasmtime 版本策略**，避免各业务线自行引入不同版本的运行时导致安全碎片化。

---

## 2. Component Model 跨语言复用边界

### 2.1 WIT 接口定义语言

WIT（Wasm Interface Types）是 Component Model 的接口契约语言，其设计目标类似于 gRPC 的 `.proto` 或 CORBA 的 IDL，但具备以下特性：

- **无序列化开销**：WIT 类型直接在宿主语言和 WASM 线性内存间传递，无需 JSON/Protobuf 编解码
- **跨语言一致**：同一 WIT 文件可生成 Rust、C、Go、Python、JavaScript 等语言的绑定
- **版本化**：`package my-org:analytics@1.0.0` 明确接口版本，支持向后兼容演进

```wit
// 示例：跨语言复用的分析接口
package my-org:analytics@1.0.0;

interface processor {
    record config {
        batch-size: u32,
        timeout-ms: u32,
    }

    enum status {
        ok,
        partial,
        error,
    }

    process-batch: func(data: list<string>, cfg: config) -> result<status, string>;
}

world analytics-world {
    export processor;
}
```

### 2.2 语言绑定现状

| 语言 | 绑定成熟度 | 生产就绪度 | 备注 |
|------|----------|-----------|------|
| **Rust** | ★★★★★ | 生产就绪 | `wasmtime` 和 `wit-bindgen` 的参考实现 |
| **C/C++** | ★★★★☆ | 生产就绪 | 通过 `componentize-py` 风格的 C 绑定生成 |
| **Go** | ★★★★☆ | 接近生产 | TinyGo + Go 原生 WASM 支持持续改进 |
| **Python** | ★★★☆☆ | 开发/测试 | `componentize-py` 支持，启动延迟仍需优化 |
| **JavaScript/TypeScript** | ★★★★☆ | 生产就绪 | JCO 工具链（ByteAlliance）将组件编译为 JS |
| **Java/Kotlin** | ★★★☆☆ | 实验性 | 依赖 WasmGC + Chicory 运行时 |

**复用策略**：当前**Rust/C/JS** 是 Component Model 的最佳实践语言。Python 适合胶水逻辑和原型验证，Java/Kotlin 建议等待 WasmGC 生态成熟。

### 2.3 复用粒度：组件→模块→函数

| 粒度 | 定义 | 复用边界 | 适用场景 |
|------|------|---------|---------|
| **函数级** | 单个 WIT 接口函数 | 最小契约单元 | 语言桥接、遗留系统封装 |
| **模块级** | 一组相关接口 + 类型（WIT `interface`） | 领域能力边界 | 日志处理、加密、配置管理 |
| **组件级** | 完整的 `world` 定义 + 实现（`.wasm` 组件） | 可独立部署单元 | 微服务替换、边缘函数、插件系统 |

**推荐粒度**：以**模块级**作为组织内复用的标准粒度。组件级适合对外交付或跨团队边界部署；函数级过细，契约维护成本高。

---

## 3. wasm-pkg-tools / OCI-based Registry

### 3.1 wkg 命令行工具

`wasm-pkg-tools`（简称 `wkg`）是 Bytecode Alliance 推出的 WASM 组件包管理工具集，提供类 `cargo` / `npm` 的体验：

```bash
# 从注册表获取组件依赖
wkg get my-org:analytics@1.0.0

# 将本地组件打包并推送
wkg publish ./target/wasm32-wasi/release/my_component.wasm \
  --registry ghcr.io/my-org/wasm-packages

# 生成依赖锁定文件（类似 Cargo.lock）
wkg resolve > wkg.lock
```

### 3.2 从 OCI 注册表分发组件

WASM 组件采用 **OCI Artifact** 规范封装，可直接推送至任何兼容 OCI 的注册表：

| 注册表 | 支持状态 | 组织场景 |
|--------|---------|---------|
| **GHCR (GitHub Container Registry)** | 完全支持 | 开源项目、团队级共享 |
| **Azure Container Registry** | 完全支持 | 企业私有组件分发 |
| **Docker Hub** | 支持 | 已有 Docker 生态的组织 |
| **Harbor** | 支持 | 自托管、多租户隔离 |

组件的 OCI 镜像与 Docker 镜像**共存于同一注册表**，但使用不同的 `mediaType`（`application/vnd.wasm.component.layer.v1+wasm`），互不影响。

### 3.3 与 Docker 镜像的共生关系

```
┌──────────────────────────────────────────────────────┐
│              部署单元选择矩阵                          │
├──────────────────────────────────────────────────────┤
│  Docker 容器          │  WASM 组件                    │
│  • 完整 OS 环境        │  • 沙箱化、无容器启动开销      │
│  • 适合单体/遗留应用    │  • 适合函数/微服务/插件        │
│  • 分钟级冷启动        │  • 毫秒级冷启动               │
│  • GB 级镜像           │  • MB/KB 级组件               │
├──────────────────────────────────────────────────────┤
│  共生模式：Container 内嵌 WASM 运行时执行组件           │
│  例：Kubernetes Pod (container) → wasmtime (sidecar) │
└──────────────────────────────────────────────────────┘
```

---

## 4. WebAssembly 3.0 的影响

### 4.1 WasmGC 对语言生态的影响

WebAssembly 3.0（W3C 标准，2025 年 9 月发布）引入 **WasmGC（Garbage Collection）** 提案，使托管语言可以直接编译为 WASM，无需自行实现 GC：

| 语言 | 3.0 之前 | 3.0 + WasmGC | 影响 |
|------|---------|-------------|------|
| **Java** | 不可用（需 TeaVM 等转译） | 原生编译（Chicory/JLama） | 企业 Java 生态可直接参与组件复用 |
| **Kotlin** | 实验性（Kotlin/WASM JS） | Kotlin/WASM WASI 支持 | 移动端/服务端 Kotlin 代码复用到边缘 |
| **Dart** | 仅 Flutter Web | Dart-to-WASM GC 原生 | Flutter 逻辑层可复用为通用组件 |

**短期影响（2026）**：WasmGC 工具链仍处于早期，不建议立即用于生产核心路径。
**中期影响（2027-2028）**：Java/Kotlin 组件将成为企业复用生态的重要组成部分，特别是 Spring 生态的"WASM 化"。

### 4.2 Memory64 对大内存应用的支持

Memory64 提案将 WASM 的线性内存寻址从 32 位扩展至 64 位，突破 4GB 内存限制：

- **受益场景**：大数据处理、科学计算、内存数据库、视频编解码
- **当前状态**：Wasmtime v45 实验性支持，需显式启用 `--wasm-features memory64`
- **复用意义**：此前因内存限制无法 WASM 化的领域（如 Spark 算子、ML 推理图）现在可被纳入组件复用范围

---

## 5. 复用决策树更新

### 5.1 何时选择 WASM Component？

```
                    ┌─────────────────┐
                    │  需要跨语言复用？  │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼ Yes                               ▼ No
    ┌───────────────┐                   ┌───────────────┐
    │ 需要亚秒冷启动？ │                   │ 用原生库/框架  │
    └───────┬───────┘                   │ (Go/Rust/Java) │
            │                           └───────────────┘
    ┌───────┴───────┐
    ▼ Yes           ▼ No
┌─────────┐   ┌─────────────┐
│ WASM    │   │ 容器 (Docker)│
│Component│   │ 或服务网格   │
└─────────┘   └─────────────┘
            │
            ▼
    ┌───────────────┐
    │ 需要强沙箱隔离？│
    └───────┬───────┘
            │
    ┌───────┴───────┐
    ▼ Yes           ▼ No
┌─────────┐   ┌─────────────┐
│ WASM    │   │ gRPC/REST   │
│Component│   │ 微服务      │
└─────────┘   └─────────────┘
```

### 5.2 四维权衡矩阵

| 维度 | WASM Component | Docker 容器 | 原生共享库 |
|------|---------------|-------------|-----------|
| **性能** | 接近原生（无容器化开销） | 好（有虚拟化开销） | 最优 |
| **安全** | ★★★★★（能力型沙箱） | ★★★☆☆（依赖 OS 隔离） | ★★☆☆☆（同进程内存） |
| **跨语言** | ★★★★★（WIT 契约） | ★★★☆☆（需网络协议） | ★★☆☆☆（需 FFI） |
| **包管理** | ★★★★☆（wkg + OCI） | ★★★★★（Docker 生态） | ★★★☆☆（语言特定） |

**结论**：WASM Component 在**安全隔离 + 跨语言复用**象限具有不可替代的优势；在纯同构语言栈且无需沙箱的场景，原生共享库仍是性能最优解；容器适合需要完整 OS 环境或已有庞大 Docker 生态的存量系统。

---

## 6. 实施建议

| 阶段 | 行动 | 产出 |
|------|------|------|
| **即时（0-1月）** | 在 CI 中引入 `wkg` 和 `wit-bindgen`，定义首个 WIT 接口 | 组织 WIT 规范初稿 |
| **短期（1-3月）** | 选择 1-2 个高频复用模块（如配置解析、日志格式化）WASM 化 | 生产组件 2-3 个 |
| **中期（3-6月）** | 搭建私有 OCI 组件注册表，与现有 Harbor/ACR 集成 | 组件复用目录上线 |
| **长期（6-12月）** | 评估 WasmGC 语言（Java/Kotlin）的组件化可行性 | Java 组件试点 |

---

## 参考文献

1. WASI 0.3 Roadmap, <https://wasi.dev>
2. Wasmtime v45.0.0 Release Notes, Bytecode Alliance, 2026-05
3. Wasmtime LTS Policy, <https://docs.wasmtime.dev/stability-release.html>
4. WebAssembly 3.0 W3C Recommendation, 2025-09
5. WebAssembly Component Model, W3C Phase 1, <https://component-model.bytecodealliance.org>
6. wasm-pkg-tools (wkg), <https://github.com/bytecodealliance/wasm-pkg-tools>
7. WasmGC Proposal, <https://github.com/WebAssembly/gc>
8. Memory64 Proposal, <https://github.com/WebAssembly/memory64>

---

## 5. WASI 1.0 迁移预对齐 Checklist

> WASI 1.0 目标发布时间为 **2026 末–2027 初**。以下清单用于在 1.0 发布后快速对齐项目知识体系与实施基线。

| 检查项 | WASI 0.3 现状 | WASI 1.0 预期 | 建议动作 | 优先级 |
|---|---|---|---|:---:|
| 异步 I/O 接口 | `stream<T>` / `future<T>`（原生 async） | 1.0 将稳定 async 世界与接口 | 评估现有 0.2 模块是否需要升级到 1.0 async 接口 | P0 |
| 运行时版本 | Wasmtime v45 常规支持；LTS v36 | 1.0 发布后需选择支持 1.0 的 LTS 版本 | 制定 Wasmtime 版本升级窗口，避免生产运行时碎片化 | P0 |
| WIT 版本 | `wasi:http@0.3.x` 等 | 1.0 WIT 将冻结并长期支持 | 提前将领域 WIT 接口与 1.0 预览版对齐，减少最终发布后的迁移成本 | P1 |
| 工具链 | wit-bindgen 0.40+ | 1.0 稳定版工具链 | 升级 CI/CD 中的 wit-bindgen、wasm-tools、wasm-pkg-tools | P1 |
| 组件注册表 | 早期 registry 生态 | 1.0 生态成熟后 registry 协议可能标准化 | 跟踪 WARG/Wasm Package Tools 进展，避免被锁定在私有 registry | P1 |
| 与 WASI 0.2 兼容 | 0.3 运行时兼容 0.2 | 1.0 可能继续提供兼容性适配层 | 验证关键 0.2 组件在 1.0 运行时上的行为一致性 | P1 |

> **跟踪来源**: <https://wasi.dev/>、<https://bytecodealliance.org/articles>、Wasmtime releases。

---

## 补充说明：P5-T4：WASM Component Model + WASI 0.3 复用边界更新

## 示例

**示例**：使用 Rust 实现图像处理组件，编译为 WIT 接口的 WASM 组件，在 Node.js、Python 与边缘运行时中复用同一二进制。

## 反例

**反例**：将 I/O 密集型服务盲目迁移到 WASM，WASI 能力不支持所需系统调用，性能与可维护性反而下降。

## 分析

**分析**：WASM 组件模型提供了真正的语言无关二进制复用，但生态与工具链仍在快速演进。
