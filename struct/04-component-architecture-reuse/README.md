# 04 组件架构复用

## 定位

模块级复用层次。覆盖框架、库、包、组件、设计模式的技术栈复用。

## 核心概念定义

组件架构复用是指在组件层对框架、库、包、组件、设计模式等模块级资产进行识别、封装、版本化与依赖治理，使其可在多个应用或系统中安全复用的实践。

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

| 标准/框架 | 版本 | 核心条款/内容 | URL | 核查日期 |
|:---|:---|:---|:---|:---|
| UML | 2.5.1 | §11 Components, §19.3 Component Diagrams | <https://www.omg.org/spec/UML/2.5.1/> | 2026-07-08 |
| ISO/IEC/IEEE 42010 | 2022 | Architecture Description: Viewpoint, View, Correspondence | <https://www.iso.org/standard/74393.html> | 2026-07-08 |
| IEEE 1471 | 2000 | Recommended Practice for Architectural Description | <https://standards.ieee.org/standard/1471-2000.html> | 2026-07-08 |
| GoF Design Patterns | 1994 | 23 Creational/Structural/Behavioral Patterns | <https://en.wikipedia.org/wiki/Design_Patterns> | 2026-07-08 |
| Enterprise Integration Patterns | 2003/2024 | 65 Messaging Patterns (Hohpe & Woolf) | <https://www.enterpriseintegrationpatterns.com/> | 2026-07-08 |
| SLSA | 1.0 | Supply-chain Levels for Software Artifacts | <https://slsa.dev/spec/v1.0/> | 2026-07-08 |
| SPDX | 2.3 | Software Package Data Exchange | <https://spdx.dev/specifications/> | 2026-07-08 |
| CycloneDX | 1.6 | Bill of Materials Standard | <https://cyclonedx.org/specification/overview/> | 2026-07-08 |

## 关键公理

> **公理 4.1** (Interface Contract Completeness): 组件的可复用性取决于其**接口契约**的完备性（前置条件、后置条件、不变量、副作用声明），而非实现细节。

## 正向复用案例

**跨团队共享的内部 SDK 组件**：某公司将日志、配置、缓存、健康检查、异常处理等横切关注点封装为内部 SDK 组件，通过私有 Maven/NuGet 仓库分发。各微服务引入统一版本依赖，重复代码减少 60%，安全补丁可在 1 天内全量推送。

## 反例

**源码复制式复用**：某项目将开源日志库的源码直接复制到代码库，未通过包管理器跟踪版本与漏洞。一年后该库出现高危 CVE，团队无法通过 `npm audit`/`cargo audit` 等工具感知，安全补丁滞后 4 个月，最终在生产环境被利用。

## 标准条款映射

| 本主题概念 | 对应标准条款 | 映射说明 |
|:---|:---|:---|
| 组件 / 接口 | UML 2.5.1 §11 Components | 组件通过提供的/需要的接口定义边界 |
| 组件图 | UML 2.5.1 §19.3 Component Diagrams | 可视化组件、接口与依赖关系 |
| 架构描述 | ISO/IEC/IEEE 42010:2022 §5.4 | 组件视图作为架构描述的一种视图 |
| 设计模式复用 | GoF (1994) | 创建型、结构型、行为型模式解决组件内部结构问题 |
| 集成模式复用 | Hohpe & Woolf (2003) | 消息路由、转换、端点模式解决组件间集成问题 |
| 供应链安全 | SLSA 1.0 | Build / Provenance / Source 等级保障组件来源可信 |

## 当前状态

- [x] 技术栈对比矩阵
- [x] 依赖治理框架
- [x] 6大语言生态复用成熟度深度对比 2026 (`07-language-ecosystems/comparison-matrix-2026.md`)
- [x] 设计模式与接口设计模式复用 (`04-design-patterns/interface-design-patterns.md`)
- [x] 依赖管理策略深度对比 (`07-language-ecosystems/open-source-supply-chain-reuse.md`)
- [ ] Rust 生态深度形式化（所有权、Trait、Cargo SAT 求解）(07-formal-verification 进行中)
- [ ] WASM Component Model 跨语言复用分析 (P1, 2026-Q4)

## 交叉引用

- `10-supply-chain-security`（SBOM、SLSA、漏洞管理）
- `07-formal-verification`（Rust 类型系统形式化）
