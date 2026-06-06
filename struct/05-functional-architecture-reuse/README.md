# 05 功能架构复用

## 定位

最细粒度的复用层次。覆盖算法、函数、业务规则、工作流、AI/LLM 功能的复用。

## 核心内容

- **Level 1**: 算法/数据结构复用（STL, Rust std, NumPy）
- **Level 2**: 函数/方法复用（纯函数、工具函数、API 端点）
- **Level 3**: 业务规则/策略复用（Drools, OPA, DMN 决策表）
- **Level 4**: 工作流/编排复用（Temporal, Camunda, Airflow, Saga）
- **Level 5**: AI/LLM 功能复用（Prompt 模板、RAG 管道、Agent 技能、MCP 工具）
- MCP (Model Context Protocol) 2025-11-25 协议深度解析
- A2A (Agent-to-Agent Protocol) v1.0.0 协议深度解析
- MCP + A2A 的互补复用架构
- Temporal 工作流复用深度
- 功能复用的粒度-成本-收益决策树

## 权威对齐

- [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) (Linux Foundation Agentic AI Foundation)
- [A2A Protocol](https://a2aprotocol.org) (Google / Linux Foundation, v1.0.0)
- [Temporal Documentation](https://docs.temporal.io)
- [DMN 1.5 Specification](https://www.omg.org/spec/DMN)

## 关键定理
>
> **定理 5.2** (AI Function Non-Determinism): AI 功能（LLM 调用、模型推理）的可复用性受**温度参数 (temperature)** 和**模型版本漂移**制约。其复用契约必须包含**确定性边界**（如 "P(正确性) ≥ 0.95"）。

## 当前状态

- [x] MCP + A2A 协议架构分析
- [x] 功能复用五层层次结构
- [x] MCP + A2A 协议架构复用分析 (`06-mcp-a2a-protocols/protocol-analysis.md`)
- [x] Temporal 工作流复用模式 (`04-workflow-orchestration/temporal-reuse-patterns.md`)
- [x] 功能复用粒度-成本-收益决策树 (`decision-tree-granularity-cost-roi.md`)
- [x] MCP 2025-11-25 权威深度解析（替换旧 2026-07-28 RC 引用） (`../12-ai-native-reuse/01-mcp-protocol/mcp-2025-11-25-deep-dive.md`)
- [x] AI 功能概率契约校准工具原型 (`../12-ai-native-reuse/04-probabilistic-contracts/calibration-tool.py`，基于 Conformal Prediction)

## 关联主题

- `12-ai-native-reuse`（AI 原生复用的协议层）
- `07-formal-verification`（AI 概率边界形式化）
