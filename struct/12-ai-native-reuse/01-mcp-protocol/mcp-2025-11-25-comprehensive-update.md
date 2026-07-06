# MCP 2025-11-25 综合更新与复用影响评估

> **版本**: 2026-06-10
> **定位**: P5-T1 交付物 —— 基于 2025-11-25 稳定版规范及 2026 年 1–5 月生态进展，全面评估 MCP 对软件架构复用的影响
> **交叉引用**: 本文档与 [mcp-2025-11-25-deep-dive.md](./mcp-2025-11-25-deep-dive.md) 互补，后者侧重规范技术细节，本文档侧重生态演进与复用决策框架
> **权威来源**:
>
> - <https://modelcontextprotocol.io/specification/2025-11-25>
> - <https://modelcontextprotocol.io/specification/2025-11-25/changelog>
> - <https://registry.modelcontextprotocol.io>
> - <https://den.dev/blog/mcp-apps/>

---

## 1. MCP 2025-11-25 核心变更详解

2025-11-25 是 MCP 发布一周年的里程碑版本，被业界广泛视为"企业就绪"版本。以下按优先级组织六项核心特性。

### P0 — 架构级变更

#### 1.1 Tasks（实验性，SEP-1686）

| 维度 | 说明 |
|------|------|
| **问题背景** | 此前 MCP 缺乏标准化的异步原语，长时间运行的工具调用（如代码分析、批量数据处理）只能依赖客户端超时重试或带外轮询，导致状态不一致和资源泄漏 |
| **解决方案** | 引入标准化的 Task 生命周期：`working` → `input_required` → `completed`/`failed`/`cancelled`，支持 `tasks/get` 轮询、`tasks/cancel` 取消、`notifications/tasks/status` 服务器主动推送 |
| **复用影响** | Tasks 使 MCP Server 从"同步函数"升级为"可编排的工作流节点"，支持跨会话的持久化请求跟踪。在复用架构中，这意味着 MCP Server 可以作为长时间运行服务被集成，而非仅限于短时状态less函数调用。详见 [deep-dive §3.1](./mcp-2025-11-25-deep-dive.md#31-tasks-能力sep-1686) |

#### 1.2 Icons（SEP-973）

| 维度 | 说明 |
|------|------|
| **问题背景** | 随着 Registry 中 Server 数量爆炸式增长（见 §3），开发者和终端用户难以在 UI 中快速识别和区分不同的工具/资源/提示 |
| **解决方案** | Server 可为 `Tool`、`Resource`、`ResourceTemplate`、`Prompt` 附加 `icons` 数组，支持 HTTPS URL 或 `data:` URI，推荐 PNG/JPEG，SVG 需安全审查，支持 `theme: light \| dark` 适配 |
| **复用影响** | Icons 看似是 UI 层增强，实则是**可复用资产目录化**的关键步骤——为后续在 Registry 中进行视觉化浏览和分类奠定基础 |

#### 1.3 URL Mode Elicitation（SEP-1036）

| 维度 | 说明 |
|------|------|
| **问题背景** | 某些交互（OAuth 同意流、支付确认、API-key 输入）不适合通过 MCP 客户端的 JSON-RPC 通道直接传递，需要安全的带外交互机制 |
| **解决方案** | 新增 `mode: "url"` Elicitation，错误码 `-32042` (`URLElicitationRequiredError`) 表示需要 URL elicitation；服务器可通过 `notifications/elicitation/complete` 通知交互完成 |
| **复用影响** | 解决了 MCP Server 集成外部 SaaS 服务时的认证/授权断点问题，使"第三方工具复用"的边界从纯协议交互扩展到安全的 Web 重定向流 |

### P1 — 安全与协议增强

#### 1.4 OAuth 企业级增强

| 变更项 | 技术要点 | 复用意义 |
|--------|---------|---------|
| OIDC Discovery 1.0 | 标准化授权服务器发现机制 | 降低多厂商 Server 的认证配置复杂度 |
| RFC 9728 | OAuth 2.0 Protected Resource Metadata | Server 自描述安全要求，Client 自动适配 |
| 增量 scope 同意 | 通过 `WWW-Authenticate` 按需请求额外 scope | 实现最小权限原则的动态升级 |
| Client ID Metadata Documents (SEP-991) | `client_id` 推荐为指向 JSON 元数据文档的 URL | 支持联邦/多租户场景下的身份联邦 |
| PKCE S256 | 强制支持 | 防止授权码拦截攻击 |
| Resource Indicators (RFC 8707) | 客户端必须发送 `resource` 参数 | 防止 audience 混淆 |

> **关键约束**: Token passthrough（令牌透传）被**明确禁止**。MCP Server 不得将客户端 bearer token 转发给下游 API。这从根本上消除了一个重大的供应链信任风险。

#### 1.5 JSON Schema 2020-12 默认方言（SEP-1613）

Tool 的 `inputSchema` / `outputSchema` 默认使用 JSON Schema 2020-12，替代此前未明确指定的方言。这提高了 Tool 定义的标准化程度，使 Schema 驱动的代码生成、文档生成和验证工具能够跨 Server 一致地工作——是**功能级复用**的基础契约标准化。

### P2 — 传输层演进

#### 1.6 Streamable HTTP（SEP-1699）

Streamable HTTP 正式成为规范远程传输方式，旧 HTTP+SSE 已被标记为废弃。其核心优势在于：Server 必须支持无 SSE 的普通 HTTP POST，仅在需要流式响应时升级连接。配合 SSE 轮询/恢复语义，解决了生产环境中断线重连和负载均衡器兼容性问题，使 MCP Server 的远程部署和水平扩展具备工程可行性。

---

## 2. MCP Apps 扩展分析

### 2.1 架构图

```text
┌─────────────────────────────────────────────────────────────┐
│                        MCP Host (Claude/ChatGPT/VS Code)    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Host UI / Chat Interface               │    │
│  └──────────────────┬────────────────────────────────┬─┘    │
│                     │ postMessage 桥接               │      │
│  ┌──────────────────▼────────────────────────────────▼─┐    │
│  │         Sandboxed iframe (CSP 隔离)                 │    │
│  │  ┌─────────────────────────────────────────────┐    │    │
│  │  │   structuredContent → HTML 渲染              │    │    │
│  │  │   (来自 MCP Server 的富界面定义)              │    │    │
│  │  └─────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ MCP Protocol
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server                                │
│         (返回 structuredContent + 交互状态)                  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 对复用模式的影响

MCP Apps（2026-01-26 发布，首个官方扩展）代表了 MCP 从"纯文本函数调用"到"交互式组件复用"的范式跃迁：

- **首日合作伙伴**: Amplitude、Asana、Box、Canva、Figma、Slack 等 15+ 主流 SaaS
- **支持客户端**: Claude、ChatGPT、Goose、VS Code Insiders

这一扩展使得 MCP Server 不仅可以暴露数据和功能，还可以暴露**可嵌入的交互界面**。从复用架构视角，这意味着：

| 传统复用模式 | MCP Apps 新模式 |
|-------------|----------------|
| API 返回 JSON，客户端自行渲染 | Server 推送结构化 UI 定义 |
| 功能复用 + 界面自行开发 | 功能与界面一同复用 |
| 文本/卡片级交互 | 富表单、图表、配置向导 |

### 2.3 安全风险

| 风险 | 描述 | 缓解措施 |
|------|------|---------|
| **XSS** | `structuredContent` 中可能包含恶意脚本 | Host 必须通过严格 CSP 和 iframe 沙箱隔离 |
| **点击劫持** | iframe 内界面可能被恶意 Host 覆盖伪装 | Server 应验证 `X-Frame-Options` 和 `frame-ancestors` |
| **iframe 逃逸** | 沙箱逃逸可能导致 Host 上下文被访问 | 使用 `sandbox="allow-scripts"` 最小权限，禁止 `allow-same-origin` |
| **postMessage 伪造** | 恶意页面可能伪造 postMessage 来源 | 严格校验 `event.origin`，使用 `MessageChannel` 替代全局 postMessage |

---

## 3. MCP Registry 生态分析

### 3.1 规模数据（截至 2026-05）

| 指标 | 数值 | 来源/日期 |
|------|------|----------|
| Registry 总记录数 | 28,959 条 | registry.modelcontextprotocol.io，2026-05 |
| Server 记录数 | 9,652 条 | registry.modelcontextprotocol.io，2026-05 |
| SDK 月下载量 | 1.1 亿次 | 2026-04 统计 |

> 对比：2026-03 月 SDK 下载量为 9,700 万+（见 [authoritative.md §7](./mcp-2025-11-25-authoritative.md#7-mcp-生态系统状态2026-05)），**两个月内增长约 13%**，增速持续。

### 3.2 Registry 作为"可复用资产目录"的定位

MCP Registry 不仅是 Server 的枚举列表，它正在演进为 AI 原生时代的**可复用资产目录**：

- **发现层**: 按功能域、认证类型、传输方式分类检索
- **契约层**: 每个 Server 提供标准化的 `tools/list`、`resources/list`、`prompts/list` 能力声明
- **质量层**: 未来可能集成下载量、评分、安全审计状态

### 3.3 与 OMG RAS v2.2 Classification 的映射

| OMG RAS v2.2 维度 | MCP Registry 对应机制 |
|------------------|----------------------|
| **Solution** (功能域) | Server 的 `Implementation.description` + 分类标签 |
| **Classification** (分类) | Registry 中的分类目录 + 工具语义标注 |
| **Usage** (使用模式) | `tools/call` Schema、`inputSchema` 定义了调用契约 |
| **Quality** (质量属性) | 下载量、社区评分（未来）、SBOM 链接 |
| **Contract** (合约) | JSON-RPC 2.0 + MCP 规范 + 具体 Schema |

这种映射表明，MCP Registry 具备了作为**企业级可复用资产库**的结构性基础，但在质量元数据和治理流程方面仍需成熟。

---

## 4. AAIF 治理结构

### 4.1 中立治理的意义

2025-12-09，Anthropic 将 MCP 捐赠给 **Agentic AI Foundation (AAIF)**——Linux Foundation 下属的定向基金。AAIF 由 Block 和 OpenAI 共同创立，Microsoft 和 GitHub 深度参与。

**消除厂商锁定的结构保障**:

| 治理机制 | 作用 |
|---------|------|
| Specification Enhancement Proposal (SEP) | 正式、透明的变更流程 |
| 12+ 个月废弃窗口 | 企业用户有足够的迁移时间 |
| 公开废弃特性注册表 | 可预测的向后兼容性管理 |
| 多厂商技术委员会 | 单一厂商无法单方面改变协议方向 |

### 4.2 生态规模

截至 2026-05，AAIF 已有 **190 个成员组织**（来源：Linux Foundation 公开数据），包括：

- **Platinum 成员**: AWS、Anthropic、Block、Bloomberg、Cloudflare、Google、Microsoft、OpenAI

这一规模的多元利益相关方参与，确保了 MCP 不会演变为某一厂商的专属扩展，而是真正成为 AI 原生互操作的**公共基础设施**。

### 4.3 对协议稳定性的保证

AAIF 治理下，MCP 获得了类同 HTTP、Kubernetes 的稳定性预期：

- **版本策略**: 日期戳版本，明确的前向/后向兼容规则
- **传输兼容**: Streamable HTTP Server 可同时提供旧 HTTP+SSE 端点兼容旧客户端
- **安全响应**: 官方工作组管理安全披露和补丁流程

---

## 5. 复用决策框架更新

### 5.1 何时选择 MCP？

| 场景 | 选择 MCP | 理由 |
|------|---------|------|
| AI Agent 需要发现/调用外部工具 | ✅ | 标准化的能力发现和调用契约 |
| 需要向 AI 提供上下文资源 | ✅ | Resources 原语支持 URI 寻址和订阅 |
| 需要复用提示模板工作流 | ✅ | Prompts 支持参数化模板 |
| Server 需要请求 LLM 采样/推理 | ✅ | Sampling 支持递归 Agent 行为 |
| 纯机器间高速数据流 | ❌ | 直接使用 gRPC/REST，MCP 语义开销过高 |
| 强实时性要求（<100ms） | ❌ | MCP 的 JSON-RPC 和协商开销不适合 |

### 5.2 MCP vs A2A vs 直接 API 决策矩阵

| 维度 | MCP | A2A | 直接 API |
|------|-----|-----|---------|
| **层级** | Agent ↔ Tool | Agent ↔ Agent | Service ↔ Service |
| **核心问题** | 工具发现与调用 | 自主 Agent 协作与任务委托 | 功能调用与数据传输 |
| **协议基础** | JSON-RPC 2.0 | HTTP + JSON | 任意（REST/gRPC/GraphQL） |
| **能力发现** | 标准化 `initialize` 协商 | Agent Card 目录 | OpenAPI/Swagger |
| **状态模型** | 有状态连接 | 有状态任务会话 | 通常无状态 |
| **适用复用层** | 05 功能架构 / 12 AI 原生 | 03 应用架构 / 12 AI 原生 | 03 应用架构 / 04 组件架构 |
| **典型组合** | A2A Agent 内部调用 MCP Tools | 编排 Agent 委托子任务给专业 Agent | 非 AI 场景的遗留系统 |

> **最佳实践**: 在多层 Agent 架构中，外层 Agent 间使用 **A2A** 协作，每个 Agent 内部通过 **MCP** 访问工具和数据，底层通过 **直接 API** 连接传统服务。详见 [deep-dive §6](./mcp-2025-11-25-deep-dive.md#6-与-a2a-协议的关系)。

### 5.3 安全评估清单

在引入 MCP Server 作为可复用资产前，执行以下检查：

| 检查项 | 验证内容 | 风险等级 |
|--------|---------|---------|
| **OAuth Scope 审查** | 确认 Server 请求的 scope 是否最小必要；是否支持增量 scope 同意 | 🔴 高 |
| **Elicitation 风险评估** | 检查 Server 是否使用 `mode: "url"`；验证 URL 是否指向可信域名 | 🔴 高 |
| **Apps 沙箱验证** | 确认 Host 对 `structuredContent` 使用 iframe 沙箱 + CSP | 🔴 高 |
| **Token Passthrough 审计** | 确认 Server 不将客户端 token 透传给下游 | 🔴 高 |
| **Schema 验证** | 确认 `inputSchema` 使用 JSON Schema 2020-12，无注入风险 | 🟡 中 |
| **Annotations 可信度** | 将 `destructiveHint` / `openWorld` 视为不可信，需二次确认 | 🟡 中 |
| **供应链溯源** | 检查 Server provenance（SLSA、签名、SBOM） | 🟡 中 |
| **上下文隔离** | 多 Server 组合时，评估跨 Server 上下文污染风险 | 🟡 中 |

---

## 6. 权威来源

| 来源 | URL | 日期 |
|------|-----|------|
| MCP 2025-11-25 规范 | <https://modelcontextprotocol.io/specification/2025-11-25> | 2025-11-25 |
| 变更日志 | <https://modelcontextprotocol.io/specification/2025-11-25/changelog> | 2025-11-25 |
| MCP Registry | <https://registry.modelcontextprotocol.io> | 2026-05 |
| MCP Apps 发布 | <https://den.dev/blog/mcp-apps/> | 2026-01-26 |
| Anthropic 捐赠公告 | <https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation> | 2025-12-09 |
| GitHub Blog on LF Move | <https://github.blog/open-source/maintainers/mcp-joins-the-linux-foundation-what-this-means-for-developers-building-the-next-era-of-ai-tools-and-agents/> | 2025-12-09 |

---

> **最后更新**: 2026-06-10
> **文档状态**: P5-T1 交付物，与 [mcp-2025-11-25-deep-dive.md](./mcp-2025-11-25-deep-dive.md) 和 [mcp-2025-11-25-authoritative.md](./mcp-2025-11-25-authoritative.md) 构成 MCP 规范三层文档体系


---

## 补充说明：MCP 2025-11-25 综合更新与复用影响评估

## 概念定义

**定义**：MCP 是由 Anthropic 主导的开放协议，规范 AI 模型如何发现、调用工具并交换上下文，使工具成为可复用资产。

## 示例

**示例**：代码助手通过 MCP 调用统一代码搜索工具，返回结构化上下文；不同 IDE 插件复用同一工具，无需各自实现代码索引。

## 反例

**反例**：Agent 通过私有 HTTP 端点调用工具，无 Schema 注册与权限控制，工具变更导致所有调用方失效。
