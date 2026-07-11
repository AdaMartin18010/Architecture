# AI 原生复用 — 国际化案例集

> **语言**: 英文案例 + 中文分析
> **范围**: 国际组织中 MCP/A2A 采用、概率契约与 AI 治理的真实案例
> **版本**: 2026-07-08

---

## 概念定义

**AI 原生复用（AI-native reuse）** 是通过 MCP、A2A 等协议，将提示词、RAG 管道、工具、模型推理服务与 Agent 技能封装为可组合、可治理资产，并通过契约与校准约束其概率性行为的实践。

---

## 正向示例

### 案例 1：Anthropic — Model Context Protocol 生态

**来源**: <https://modelcontextprotocol.io/>, Anthropic 工程沟通

**决策**: Anthropic 推出 MCP 作为开放协议，将 LLM 宿主与工具/数据源集成解耦，从而形成可复用工具市场。

**结果**: 日益增长的 MCP 服务器生态（数据库、文件系统、API）可在任何 MCP 兼容宿主中复用，减少了一次性集成。

**经验**:

- 协议级标准化是跨 LLM 应用复用工具的前提。
- 能力协商让宿主与服务器可独立演进。
- 安全边界（用户同意、工具授权）必须自协议设计之初纳入。

### 案例 2：Google Cloud — A2A 协议与 Agent 互操作

**来源**: <https://a2a-protocol.org/>, Google Cloud Next 2026 公告

**决策**: Google 提出 A2A 作为开放协议，让 Agent 发现彼此能力、协商任务并通过签名 Agent Card 交付结果。

**结果**: 企业可跨不同厂商与内部团队组合多 Agent 工作流，无需硬编码成对集成。

**经验**:

- Agent Card 是信任与能力 advertisement 的可复用单元。
- 跨厂商互操作需要开放模式与认证标准。
- 多 Agent 治理（审计、升级）必须与协议采用同步设计。

### 案例 3：Microsoft — Agent Governance Toolkit

**来源**: <https://github.com/microsoft/agent-governance-toolkit>

**决策**: 微软开源 Agent Governance Toolkit，为自主 Agent 提供运行时治理、审计与策略执行，覆盖 OWASP Agentic AI 风险。

**结果**: 组织可在不同 Agent 实现中应用一致的治理策略，提升可审计性并减少过度授权。

**经验**:

- 可复用的治理策略与可复用的工具同等重要。
- 运行时 enforcement 是对设计时风险评估的补充。
- 与现有身份与可观测性栈集成可降低采用门槛。

---

## 反例 / 失败案例

### 反例 1：硬编码 Prompt 与 API

各团队在不同 Agent 中直接嵌入相同 Prompt 与厂商 API 调用，没有版本管理与输出契约；导致行为不一致、成本失控且难以审计。

**教训**: 应将 Prompt 与工具调用视为带定义契约的版本化、可复用资产。

### 反例 2：过度放权且无边界

某 Agent 被赋予广泛系统访问权限且缺乏审计日志。它自主修改了生产配置；事后既无法追溯决策过程，也无法确定责任归属。

**教训**: Agent 能力必须受策略约束，高影响动作必须强制人在回路，并保留不可变审计日志。

---

## 分析

AI 原生复用引入了两个传统软件复用中不存在的新挑战：

1. **概率性行为**: 输出非确定性，需要契约、校准与监控。
2. **自主行动**: Agent 可代表用户执行动作，需要治理设计。

成功案例结合了**开放协议**（MCP、A2A）、**信任工件**（Agent Card、签名能力）与**运行时治理**（策略执行、审计）。失败则发生在团队将 AI 集成视为传统确定性 API 时。

---

## 权威来源

- Model Context Protocol, <https://modelcontextprotocol.io/>
- Agent-to-Agent Protocol, <https://a2a-protocol.org/>
- Microsoft Agent Governance Toolkit, <https://github.com/microsoft/agent-governance-toolkit>
- OWASP Agentic AI Top 10, <https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/>
- 核查日期：2026-07-08

---

## 相关文档

- [`../01-mcp-protocol/mcp-2026-transition-guide.md`](../01-mcp-protocol/mcp-2026-transition-guide.md)
- [`../02-a2a-protocol/a2a-v1-authoritative.md`](../02-a2a-protocol/a2a-v1-authoritative.md)
- [`../05-probabilistic-contracts/probabilistic-contract-framework.md`](../05-probabilistic-contracts/probabilistic-contract-framework.md)