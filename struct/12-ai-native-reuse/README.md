# 12 AI 原生复用

## 定位

AI/LLM 功能复用是 2026 年软件工程的新边界。传统复用假设"确定性"，AI 复用必须处理"概率性"。

## 核心内容

- **MCP (Model Context Protocol) 2025-11-25**（当前稳定版）
  - tools / resources / prompts / sampling 四层能力
  - Tasks 异步能力（SEP-1686）
  - Icons（SEP-973）、Elicitation URL 模式、Sampling with Tools
  - OAuth / OpenID Connect 企业级增强
  - 与 A2A 的互补架构
- **A2A (Agent-to-Agent Protocol) v1.0.0**
  - Agent Card / Task / Artifact / Message / Part
  - 能力发现 → 任务委托 → 消息交互 → 结果交付 → 安全验证
- **Agentic Infrastructure**: AI 作为平台一等公民
  - Agent 身份与 RBAC
  - Agent Golden Path
  - 提示词治理与模型路由
- **概率契约框架**
  - 置信度函数 γ(x) ∈ [0,1]
  - 温度参数、Top-p、模型版本漂移
  - 确定性边界声明
- **Conformal Prediction**: 不确定性量化的统计保证
  - 边际覆盖保证 P(y ∈ C(x)) ≥ 1-α
  - 在代码生成、审查中的应用

## 权威对齐

- [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) (Linux Foundation Agentic AI Foundation)
- [A2A Protocol](https://a2aprotocol.org) (Google / Linux Foundation)
- [LangChain](https://python.langchain.com) / [LlamaIndex](https://www.llamaindex.ai)
- [Conformal Prediction Book](https://arxiv.org/abs/2107.07511) (Vovk, Gammerman, Shafer)

## 关键定理
>
> **定理 AI.1** (Calibration Ceiling): 置信度校准的效果存在上限。当 LLM 的输出分布与真实分布的 KL 散度 > ε 时，任何校准方法都无法使校准误差 < δ。

## 当前状态

- [x] MCP + A2A 协议架构分析
- [x] 概率契约形式化定义
- [x] MCP 2025-11-25 + A2A v1.0 协议深度解析 (`01-mcp-protocol/mcp-2025-11-25-deep-dive.md`)
- [x] AI 概率契约校准工具原型 (`04-probabilistic-contracts/calibration-tool.py`，基于 Conformal Prediction)
- [x] A2A v1.0.0 协议复用分析 (`02-a2a-protocol/a2a-reuse-analysis.md`)
- [x] Conformal Prediction 代码生成应用案例 (`05-conformal-prediction/cp-code-generation.md`)
- [ ] Agentic Governance 的组织设计模板 (P1, 2026-Q4)

## 关联主题

- `05-functional-architecture-reuse`（AI 功能层）
- `08-cognitive-architecture`（AI 增强开发者认知）
- `07-formal-verification`（AI 概率边界形式化）
