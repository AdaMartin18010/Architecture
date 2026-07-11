# 05 功能架构复用

## 定位

最细粒度的复用层次。覆盖算法、函数、业务规则、工作流、AI/LLM 功能的复用。

## 核心概念定义

功能架构复用是指在功能层对算法、函数、业务规则、工作流、AI/LLM 能力等细粒度资产进行封装、编目与组合复用的实践，强调确定性边界、版本契约与可观测性。

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

| 标准/框架 | 版本 | 核心条款/内容 | URL | 核查日期 |
|:---|:---|:---|:---|:---|
| MCP Specification | 2025-11-25 | Tools, Resources, Prompts, Sampling, Transports | <https://modelcontextprotocol.io/specification/2025-11-25> | 2026-07-08 |
| A2A Protocol | v1.0.0 | Agent-to-Agent Protocol (Google / Linux Foundation) | <https://a2aprotocol.org/> | 2026-07-08 |
| DMN | 1.5 | §6 Decision Requirements, §8 Decision Table | <https://www.omg.org/spec/DMN/1.5/> | 2026-07-08 |
| Temporal | 2026 | Workflows, Activities, Workers, Schedules | <https://docs.temporal.io/> | 2026-07-08 |
| DDD | Evans 2003 | Entities, Value Objects, Aggregates, Bounded Contexts | <https://martinfowler.com/bliki/DomainDrivenDesign.html> | 2026-07-08 |
| Serverless Functions | — | AWS Lambda, Azure Functions, Google Cloud Functions | <https://aws.amazon.com/lambda/> | 2026-07-08 |

## 关键定理

> **定理 5.2** (AI Function Non-Determinism): AI 功能（LLM 调用、模型推理）的可复用性受**温度参数 (temperature)** 和**模型版本漂移**制约。其复用契约必须包含**确定性边界**（如 "P(正确性) ≥ 0.95"）。

## 正向复用案例

**财税规则纯函数库**：团队将发票金额校验、税率计算与格式转换封装为纯函数库，在订单、报销与财务系统中统一调用。当增值税率调整时，只需修改函数库并升级版本，所有消费系统在 1 周内完成同步，避免重复实现导致的税率错误。

## 反例

**分布式规则泥潭**：同一业务规则以不同语言、不同逻辑在 ERP、CRM、电商中台三个系统中实现。当国家调整跨境电子服务税率时，三个团队分别修改，遗漏了 CRM 中的一处旧逻辑，导致季度税务申报差异 120 万元，补税并缴纳滞纳金。

## 标准条款映射

| 本主题概念 | 对应标准条款 | 映射说明 |
|:---|:---|:---|
| 纯函数 / 无副作用 | DDD Tactical Design | 领域逻辑的可复用单元应保持无副作用，便于测试与组合 |
| 业务规则复用 | DMN 1.5 §6 Decision Service | 规则封装为决策服务，可被流程、应用、AI Agent 调用 |
| 工作流复用 | BPMN 2.0 §8 Process / Temporal Workflows | 长事务、 Saga、定时任务等由工作流引擎编排 |
| 事件函数复用 | CloudEvents 1.0 / AsyncAPI | 事件 Schema 标准化使函数可在多传输层复用 |
| AI 工具复用 | MCP 2025-11-25 | Model Context Protocol 定义 LLM 工具、资源、提示词的标准契约 |
| Agent 协作 | A2A v1.0.0 | Agent-to-Agent Protocol 定义多 Agent 之间的任务与能力发现 |

## 当前状态

- [x] MCP + A2A 协议架构分析
- [x] 功能复用五层层次结构
- [x] MCP + A2A 协议架构复用分析 (`06-mcp-a2a-protocols/protocol-analysis.md`)
- [x] Temporal 工作流复用模式 (`04-workflow-orchestration/temporal-reuse-patterns.md`)
- [x] 功能复用粒度-成本-收益决策树 (`decision-tree-granularity-cost-roi.md`)
- [x] MCP 2025-11-25 权威深度解析（替换旧 2026-07-28 RC 引用） (`../12-ai-native-reuse/01-mcp-protocol/mcp-2025-11-25-deep-dive.md`)
- [x] AI 功能概率契约校准工具原型 (`../12-ai-native-reuse/05-probabilistic-contracts/calibration-tool.py`，基于 Conformal Prediction)

## 交叉引用

- `12-ai-native-reuse`（AI 原生复用的协议层）
- `07-formal-verification`（AI 概率边界形式化）