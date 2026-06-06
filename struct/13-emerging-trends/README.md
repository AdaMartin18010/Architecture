# 13 新兴趋势

## 定位

2026 年及以后的软件复用前沿方向。

## 核心内容

- **平台工程 (Platform Engineering)**
  - 内部开发者平台 (IDP) 作为复用的组织化载体
  - Golden Path / Software Catalog / 自服务模板
  - Gartner 预测：2026 年 80% 大型组织建立平台团队
- **模块化单体回归 (Modular Monolith)**
  - Spring Modulith / OSGi / JPMS
  - 渐进式拆分策略
  - 适用边界：团队 < 50 人，部署频率 < 1天/次
- **WebAssembly Component Model**
  - 跨语言、跨运行时的组件复用标准
  - WIT (Wasm Interface Types) / WASI 0.3
  - 边缘计算新边界
- **Rust 生态爆发**
  - 所有权系统驱动的复用安全
  - Cargo 统一版本策略
  - WASM 组件化的主力语言
- **RegTech AI 合规框架**
  - 从规则引擎到 Agentic 治理
  - 感知层 → 认知层 → 决策层 → 行动层 → 学习层

## 权威对齐

- [Gartner Platform Engineering](https://www.gartner.com)
- [CNCF Platforms White Paper](https://tag-app-delivery.cncf.io/whitepapers/platforms/)
- [WebAssembly Component Model](https://component-model.bytecodealliance.org)
- [Rust Foundation](https://foundation.rust-lang.org)

## 当前状态

- [x] 趋势识别与框架分析
- [x] 平台工程成熟度模型 (`01-platform-engineering/platform-maturity-model.md`)
- [x] WASM Component Model 复用决策树 (`03-webassembly-components/wasm-reuse-decision-tree.md`)
- [x] CNCF 平台工程 2026 (`01-platform-engineering/platform-engineering-cncf-2026.md`)
- [x] WASM 组件模型 2026 (`03-webassembly-components/wasm-component-model-2026.md`)
- [ ] RegTech Agentic 架构的案例验证 (P2, 2027-Q3)

## 关联主题

- `03-application-architecture-reuse`（模块化单体）
- `04-component-architecture-reuse`（Rust 生态、WASM）
- `12-ai-native-reuse`（Agentic Infrastructure）
