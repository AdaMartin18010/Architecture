# 04 组件架构复用

## 定位

模块级复用层次。覆盖框架、库、包、组件、设计模式的技术栈复用。

## 核心内容

- **Level 1**: 框架/平台复用（Spring Boot, React, .NET, Django, Actix）
- **Level 2**: 库/包复用（npm, Cargo, Go Modules, Maven, NuGet）
- **Level 3**: 组件/Bean/Module 复用（Spring Bean, React Component, Vue Component）
- **Level 4**: 设计模式/架构模式复用（GoF, POSA, Enterprise Integration Patterns）
- 依赖管理策略深度对比（版本锁定、Semver、范围依赖、供应商化）
- 供应链安全：SBOM (SPDX/CycloneDX/SWID) + SLSA 四级框架
- 组件版本策略（Semver 的复用语义）
- 各语言生态复用成熟度矩阵（2026）
  - JVM / Node.js / Rust / Go / Python / .NET / WebAssembly

## 权威对齐

- [Maven Central](https://central.sonatype.com), [npm Registry](https://www.npmjs.com)
- [crates.io](https://crates.io), [PyPI](https://pypi.org)
- [SLSA Framework](https://slsa.dev)
- [SPDX Specification](https://spdx.dev), [CycloneDX](https://cyclonedx.org)

## 关键公理
>
> **公理 4.1** (Interface Contract Completeness): 组件的可复用性取决于其**接口契约**的完备性（前置条件、后置条件、不变量、副作用声明），而非实现细节。

## 当前状态

- [x] 技术栈对比矩阵
- [x] 依赖治理框架
- [ ] Rust 生态深度形式化（所有权、Trait、Cargo SAT 求解）
- [ ] WASM Component Model 跨语言复用分析

## 关联主题

- `10-supply-chain-security`（SBOM、SLSA、漏洞管理）
- `07-formal-verification`（Rust 类型系统形式化）
