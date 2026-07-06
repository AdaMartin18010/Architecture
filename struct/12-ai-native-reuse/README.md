# 12 AI 原生复用

> **定位**：AI/LLM 功能复用是 2026 年软件工程的新边界。传统复用假设“确定性”，AI 复用必须处理“概率性”，并通过协议、契约与治理实现可组合、可审计的 AI 资产复用。

---

## 1. 概念定义

**AI 原生复用** 是在大模型与 Agent 系统中，通过 MCP（Model Context Protocol）、A2A（Agent-to-Agent Protocol）与概率契约，将提示模板、RAG 管道、工具、模型推理服务与 Agent 技能封装为可组合、可治理的资产。

| 概念 | 定义 | 复用层次 |
|------|------|----------|
| **MCP** | Model Context Protocol，模型与工具/上下文源之间的开放协议 | 工具与上下文复用 |
| **A2A** | Agent-to-Agent Protocol，Agent 之间的协作协议 | Agent 能力与任务复用 |
| **概率契约** | 对 AI 服务输出质量边界的概率承诺 | AI 服务等级与风险边界 |
| **Conformal Prediction** | 构造具有边际覆盖保证的预测集 | 不确定性量化与校准 |
| **Agentic Infrastructure** | 将 Agent 身份、RBAC、审计作为平台一等公民 | Agent 运行时治理 |

**概率性不可消除原则**：AI 输出的不确定性无法通过测试完全消除，但可以通过概率契约、监控与校准将其约束在业务可接受范围内。

---

## 2. AI 原生复用协议栈

```mermaid
graph TD
    A[AI 原生复用] --> B[MCP 工具层]
    A --> C[A2A Agent 层]
    A --> D[概率契约层]
    B --> E[数据库查询 / 代码检索 / 文档解析]
    C --> F[任务委托 / 能力发现 / 结果交付]
    D --> G[准确率 ≥ 0.92 / 延迟 ≤ 200ms / 成本 ≤ $0.01]
    E --> H[可复用 AI 能力]
    F --> H
    G --> H
```

---

## 3. 正向示例

### 示例 1：MCP 工具目录

企业构建 MCP 工具目录，将数据库查询、代码检索、文档解析发布为标准工具；客服 Agent、运维 Agent 与开发 Agent 按统一 Schema 调用，避免各自重复封装相同能力。

### 示例 2：A2A 跨 Agent 任务协作

旅行规划 Agent 通过 A2A 调用酒店预订 Agent 与航班查询 Agent；基于 Agent Card 中的能力清单与信任凭证自动协商，无需为每对 Agent 硬编码集成。

### 示例 3：概率契约 SLA

某 LLM 分类服务承诺 P(准确率 > 0.92) ≥ 0.95，使用 Conformal Prediction 计算预测集；运行时监控模型漂移，一旦偏离阈值即触发重新校准。

### 示例 4：Agentic 治理基础设施

企业建立 Agent 注册表，要求每个 Agent 声明能力、工具、决策边界与人工复核点；通过运行时策略限制 Agent 访问范围，实现可审计的自主决策。

### 示例 5：RAG 管道复用

企业将文档分块、向量化、重排序与引用生成封装为标准 RAG 管道，多个业务线复用同一管道；通过版本控制与数据源契约保证答案一致性与可追溯性。

---

## 4. 反例 / 失败案例

### 反例 1：硬编码 Prompt 与 API

各团队在不同 Agent 中硬编码相同 Prompt 与 API 调用，无版本管理与输出契约；导致行为不一致、成本失控且难以审计。

### 反例 2：缺乏置信度边界的关键业务接入

某公司将 LLM 输出直接接入信贷审批规则，未定义准确率与置信度边界；错误分类导致合规罚款与客户流失。

### 反例 3：私有 RPC 导致工具孤岛

Agent 通过私有 HTTP 端点调用工具，无 Schema 注册与权限控制；工具变更后所有调用方失效，形成新的能力孤岛。

### 反例 4：过度放权且无审计

某 Agent 被赋予广泛系统权限且缺乏审计，自主调用敏感工具修改生产配置；事后无法追溯决策过程与责任归属。

### 反例 5：忽视模型漂移

客服机器人复用固定 Prompt 与温度参数，未监控模型版本漂移；半年后回答准确率从 92% 降至 78%，客户投诉激增。

---

## 5. AI 复用决策矩阵

| 资产类型 | 协议/机制 | 关键治理点 | 风险 |
|----------|-----------|------------|------|
| 工具 | MCP | Schema 版本、权限、可观测性 | 工具变更导致调用失效 |
| Agent 能力 | A2A | 能力发现、信任凭证、任务委托 | Agent 协作不可控 |
| 提示模板 | 模板仓库 + 版本控制 | A/B 测试、输出模式校验 | 提示漂移 |
| 模型服务 | 概率契约 | 准确率、延迟、成本边界 | 业务决策错误 |
| RAG 管道 | 上下文契约 | 数据源版本、召回率监控 | 幻觉与过时信息 |

---

## 6. 关键定理

> **定理 AI.1**（Calibration Ceiling）：置信度校准的效果存在上限。当 LLM 的输出分布与真实分布的 KL 散度大于 ε 时，任何校准方法都无法使校准误差小于 δ。

---

## 7. 权威来源

> **权威来源**：
>
> - [Model Context Protocol Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)
> - [MCP Introduction](https://modelcontextprotocol.io/introduction)
> - [A2A Protocol](https://google.github.io/A2A)
> - [Google A2A Blog](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
> - [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/)
> - [Conformal Prediction Book (arXiv)](https://arxiv.org/abs/2107.07511)
> - [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
> - 核查日期：2026-07-07

---

## 8. 当前状态与关联主题

- [x] MCP + A2A 协议架构分析 (`01-mcp-protocol/`, `02-a2a-protocol/`)
- [x] 概率契约框架与校准工具 (`05-probabilistic-contracts/`)
- [x] A2A/MCP 混合 Agent PoC (`04-hybrid-a2a-mcp-poc/`)
- [x] Conformal Prediction 应用案例 (`07-conformal-prediction/`)
- [ ] Agentic Governance 组织设计模板 (P1, 2026-Q4)

关联主题：

- `05-functional-architecture-reuse`（AI 功能层）
- `08-cognitive-architecture`（AI 增强开发者认知）
- `07-formal-verification`（概率边界形式化）
- `10-supply-chain-security`（LLM / MCP 安全）

## 9. 实施检查单

- [ ] 建立 MCP 工具目录，统一工具 Schema、权限与版本管理。
- [ ] 为每个 AI 服务定义概率契约，明确准确率、延迟与成本边界。
- [ ] 部署运行时监控，跟踪模型漂移、输出分布与契约违反。
- [ ] 建立 Agent 注册表，声明能力、工具、决策边界与人工复核点。
- [ ] 将 AI 服务纳入供应链安全治理，审计模型来源与依赖。

## 10. 常见误区

- **误区 1：把 AI 当作确定性组件**。必须接受并管理概率性。
- **误区 2：只复用 Prompt 不管理版本**。Prompt 微小变化可能导致输出大幅漂移。
- **误区 3：忽视人工复核**。高影响决策必须保留人在回路。
- **误区 4：Agent 权限过大**。应遵循最小权限原则。
- **误区 5：只关注单次准确率**。需持续监控分布漂移与校准误差。

## 11. 一句话总结

> AI 原生复用需要接受概率性，并通过 MCP、A2A 与概率契约将其约束在可接受范围内；治理与可观测性是与能力同等重要的基础设施。

## 12. 版本记录

- 2026-07-07：补充 MCP、A2A、概率契约与 Conformal Prediction 的概念定义、示例、反例、关系图与权威来源。
- 2026-06-08：初始版本，梳理 AI 原生复用核心文件与状态。

## 13. 深度案例：企业 MCP 工具目录与 A2A 协作网络

某全球性科技公司希望让内部数十个 AI Agent 能够共享工具与协作能力，避免各团队重复开发数据库查询、代码检索与文档解析等功能。

实施要点：

1. **MCP 工具目录**：将常用能力封装为 MCP 工具，注册到统一目录；每个工具包含 Schema、示例、权限要求与 SLI。
2. **A2A Agent 网络**：不同业务线的 Agent 通过 A2A 协议相互发现能力，并在任务需要时委托子任务。
3. **概率契约**：对分类、摘要与代码生成服务分别定义准确率、延迟与成本边界，并接入监控告警。
4. **治理基础设施**：建立 Agent 注册表、运行时策略与审计日志，确保自主行为可追溯、可撤销。

结果：重复工具开发减少 60%，Agent 协作场景从 0 扩展到 20+，人工复核率保持在 5% 以下。

## 14. 延伸阅读

1. Anthropic. *Model Context Protocol Specification*。
2. Google. *Agent-to-Agent Protocol (A2A) Specification*。
3. Vovk, V., Gammerman, A., Shafer, G. *Algorithmic Learning in a Random World* — Conformal Prediction 经典。
4. OWASP. *LLM AI Security Top 10*。
5. NIST. *AI Risk Management Framework AI RMF 1.0*。

## 15. 持续改进方向

- 将概率契约与 SLA 模板化，纳入所有 AI 服务的默认交付物。
- 探索形式化方法对概率边界的表达与验证。
- 建立跨 Agent 任务的因果追踪与责任归属机制。
- 将 MCP/A2A 安全评估纳入供应链安全门控。

## 16. 关键行动项

- 识别组织中 5-10 个可被 Agent 复用的工具，封装为 MCP 服务。
- 为每个 AI 服务建立概率契约基线，并部署监控。
- 制定 Agent 能力注册、发现与委托的 A2A 接入规范。
- 开展 Agentic Governance 培训，明确安全、合规与责任边界。

## 17. 版本记录补充

- 持续跟踪 MCP、A2A、Conformal Prediction 与 NIST AI RMF 的最新版本，并更新权威来源与核查日期。

## 18. 总结

AI 原生复用正在重塑软件能力组合方式。协议、概率契约与治理基础设施的同步建设，是决定 AI 资产能否规模化复用的关键。
