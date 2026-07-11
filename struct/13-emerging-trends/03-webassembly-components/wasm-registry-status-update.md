# WebAssembly Registry 状态更新：Warg → OCI-based Registry

> **版本**: 2026-06-10
> **主题**: WebAssembly 组件分发机制演进
> **核查日期**: 2026-06-10
> **来源 URL**: <https://github.com/bytecodealliance/registry/> | <https://github.com/bytecodealliance/wasm-pkg-tools>

---

## 目录

- [WebAssembly Registry 状态更新：Warg → OCI-based Registry](#webassembly-registry-状态更新warg--oci-based-registry)
  - [目录](#目录)
  - [1. 状态摘要](#1-状态摘要)
  - [2. Warg Registry 历史与现状](#2-warg-registry-历史与现状)
  - [3. 当前推荐方案：OCI-based Registry + wasm-pkg-tools](#3-当前推荐方案oci-based-registry--wasm-pkg-tools)
    - [3.1 技术路线](#31-技术路线)
    - [3.2 wasm-pkg-tools 功能](#32-wasm-pkg-tools-功能)
    - [3.3 与容器生态的协同](#33-与容器生态的协同)
  - [4. 对本项目的影响](#4-对本项目的影响)
  - [5. 关键里程碑](#5-关键里程碑)
  - [补充说明：WebAssembly Registry 状态更新：Warg → OCI-based Registry](#补充说明webassembly-registry-状态更新warg--oci-based-registry)
  - [概念定义](#概念定义)
  - [示例](#示例)
  - [反例](#反例)
  - [分析](#分析)

## 1. 状态摘要

经全面核查，本项目在 WASM 相关文档中**未发现对 Warg Registry 的引用**（`grep -rni "warg" ./struct/13-emerging-trends/03-webassembly-components/` 无结果）。本文件作为预防性状态更新，记录 WebAssembly 组件注册表的技术演进，供后续文档引用时参考。

---

## 2. Warg Registry 历史与现状

| 时间 | 事件 |
|:---|:---|
| 2022-2023 | Bytecode Alliance 启动 Warg 项目，意图为 WebAssembly 组件建立专用注册协议 |
| 2024 | Warg 实现可用，但社区采用率低于预期 |
| 2025 | Bytecode Alliance 宣布 **停止 Warg 的积极开发** |
| 2026 初 | 社区共识转向 **基于 OCI 的注册表方案** |

**官方声明**（Bytecode Alliance registry 仓库）：
> "This repository is no longer being actively developed. The Bytecode Alliance is working with the community on next-generation approaches to WebAssembly component registries."

---

## 3. 当前推荐方案：OCI-based Registry + wasm-pkg-tools

### 3.1 技术路线

```text
WebAssembly 组件分发（2026 推荐方案）
├── 注册协议: OCI (Open Container Initiative) Distribution Spec
├── 存储格式: OCI Artifacts
├── 客户端工具: wasm-pkg-tools (Bytecode Alliance)
├── 支持平台:
│   ├── Docker Hub / GHCR / Azure CR（通过 OCI 兼容）
│   └── 私有 OCI 注册表（Harbor, Nexus, Artifactory）
└── 优势: 复用现有容器基础设施，无需新建协议栈
```

### 3.2 wasm-pkg-tools 功能

| 功能 | 说明 |
|:---|:---|
| `wasm-pkg-publish` | 将 Wasm 组件发布到 OCI 注册表 |
| `wasm-pkg-fetch` | 从 OCI 注册表获取 Wasm 组件 |
| `wasm-pkg-lock` | 生成并管理组件依赖锁定文件 |
| WIT 包管理 | 支持 WIT (WebAssembly Interface Types) 接口定义的版本化分发 |

### 3.3 与容器生态的协同

OCI-based 方案的最大优势是**复用现有容器供应链安全基础设施**：

- **SLSA Provenance**: OCI 镜像的 SLSA 溯源可直接应用于 Wasm 组件
- **Sigstore/cosign**: 镜像签名验证机制直接复用
- **SBOM**: SPDX/CycloneDX 格式的 SBOM 可直接附加到 OCI Artifact
- **漏洞扫描**: Trivy、Snyk 等 OCI 镜像扫描工具可直接扩展支持 Wasm

---

## 4. 对本项目的影响

| 本项目文档 | 状态 | 建议 |
|:---|:---|:---|
| `13/03-webassembly-components/wasm-reuse-decision-tree.md` | 未引用 Warg | 如后续修订，统一使用 "OCI-based registry / wasm-pkg-tools" 术语 |
| `13/03-webassembly-components/wasm-wasi-03-boundaries.md` | 计划中 | 组件分发章节应采用 OCI 方案 |
| `10-supply-chain-security/` 相关文档 | 未交叉引用 | 可在供应链安全文档中增加 "Wasm 组件的 OCI 溯源" 案例 |

---

## 5. 关键里程碑

| 时间 | 事件 |
|:---|:---|
| 2026-02 | WASI 0.3 Preview 发布，wasm-pkg-tools 初步支持 |
| 2026 末/2027 初 | WASI 1.0 预计发布，OCI-based 分发预计成为事实标准 |
| 持续 | Bytecode Alliance 与 W3C 推进 Component Model 标准化（W3C Phase 1 → 2） |

---

> **权威来源**:
>
> - Bytecode Alliance Registry Repository (archived). <https://github.com/bytecodealliance/registry/> (核查日期: 2026-06-10)
> - wasm-pkg-tools. <https://github.com/bytecodealliance/wasm-pkg-tools> (核查日期: 2026-06-10)
> - Platform Uno: State of WebAssembly 2025-2026. <https://platform.uno/blog/the-state-of-webassembly-2025-2026/> (核查日期: 2026-06-10)
> - WASI Roadmap. <https://wasi.dev/roadmap> (核查日期: 2026-06-10)
>
> **核查日期**: 2026-06-10


---

## 补充说明：WebAssembly Registry 状态更新：Warg → OCI-based Registry

## 概念定义

**定义**：WebAssembly Component Model 将 WASM 模块升级为具有显式接口、类型化导入导出的可组合组件，支持跨语言、跨运行时复用。

## 示例

**示例**：使用 Rust 实现图像处理组件，编译为 WIT 接口的 WASM 组件，在 Node.js、Python 与边缘运行时中复用同一二进制。

## 反例

**反例**：将 I/O 密集型服务盲目迁移到 WASM，WASI 能力不支持所需系统调用，性能与可维护性反而下降。

## 分析

**分析**：WASM 组件模型提供了真正的语言无关二进制复用，但生态与工具链仍在快速演进。