# MCP 2025-11-25 规范深度解析

> **定位**: 替换项目中已过时的 "MCP 2026-07-28 RC" 引用，提供 MCP 当前稳定版的权威技术解析
> **对齐来源**: Model Context Protocol Specification 2025-11-25 (Anthropic / Linux Foundation Agentic AI Foundation)
> **状态**: Phase 2 提前启动（关键勘误）
> **权威链接**:
>
> - <https://modelcontextprotocol.io/specification/2025-11-25>
> - <https://modelcontextprotocol.io/specification/2025-11-25/changelog>
> - <https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2025-11-25/schema.ts>

---

## 目录

- [MCP 2025-11-25 规范深度解析](#mcp-2025-11-25-规范深度解析)
  - [目录](#目录)
  - [1. 关键勘误](#1-关键勘误)
  - [2. 规范来源](#2-规范来源)
  - [3. 2025-06-18 → 2025-11-25 核心变更](#3-2025-06-18--2025-11-25-核心变更)
    - [3.1 Tasks 能力（SEP-1686）](#31-tasks-能力sep-1686)
    - [3.2 Icons（SEP-973）](#32-iconssep-973)
    - [3.3 Sampling 支持 Tools / ToolChoice（SEP-1577）](#33-sampling-支持-tools--toolchoicesep-1577)
    - [3.4 Elicitation 增强](#34-elicitation-增强)
    - [3.5 OAuth / OpenID Connect 企业级增强](#35-oauth--openid-connect-企业级增强)
    - [3.6 其他重要变更](#36-其他重要变更)
  - [4. 治理变化：Linux Foundation Agentic AI Foundation](#4-治理变化linux-foundation-agentic-ai-foundation)
  - [5. 版本与兼容性策略](#5-版本与兼容性策略)
    - [版本协商](#版本协商)
    - [特性生命周期（SEP-2596）](#特性生命周期sep-2596)
    - [传输兼容](#传输兼容)
  - [6. 与 A2A 协议的关系](#6-与-a2a-协议的关系)
  - [7. 复用视角下的 MCP 安全](#7-复用视角下的-mcp-安全)
    - [7.1 信任边界](#71-信任边界)
    - [7.2 认证与授权](#72-认证与授权)
    - [7.3 传输与网络安全](#73-传输与网络安全)
    - [7.4 本地服务器 / 供应链风险](#74-本地服务器--供应链风险)
    - [7.5 多服务器组合](#75-多服务器组合)
  - [8. 企业就绪评估](#8-企业就绪评估)
  - [9. 与四层复用架构的映射](#9-与四层复用架构的映射)
  - [10. 项目中的引用更新建议](#10-项目中的引用更新建议)
  - [11. 参考链接](#11-参考链接)
  - [补充说明：MCP 2025-11-25 规范深度解析](#补充说明mcp-2025-11-25-规范深度解析)
  - [概念定义](#概念定义)
  - [示例](#示例)
  - [反例](#反例)
  - [权威来源](#权威来源)
  - [分析](#分析)

## 1. 关键勘误

**MCP 当前稳定版本是 `2025-11-25`；`2026-07-28` 为官方 Release Candidate（RC，2026-05-29 发布），最终版预计 2026-07-28，尚未成为稳定版。**

`2026-07-28` 是官方 Release Candidate（RC，2026-05-29 发布），最终版预计 2026-07-28；截至 2026-07-11 最终版尚未发布，生产环境仍以 **MCP 2025-11-25** 为稳定基线。项目中所有对 "MCP 2026-07-28 RC" 的引用都应更新为 **MCP 2025-11-25**。

---

## 2. 规范来源

| 资源 | URL | 作用 |
|------|-----|------|
| 规范主页 | <https://modelcontextprotocol.io/specification/2025-11-25> | 官方 landing page |
| 变更日志 | <https://modelcontextprotocol.io/specification/2025-11-25/changelog> | 2025-06-18 → 2025-11-25 的完整变更 |
| 权威 Schema | GitHub `schema/2025-11-25/schema.ts` | 消息结构和方法的权威来源 |
| 版本策略 | <https://modelcontextprotocol.io/specification/versioning> | 日期戳版本和兼容性策略 |
| 功能生命周期 | <https://modelcontextprotocol.io/community/feature-lifecycle> | Active/Deprecated/Removed 三态 |
| 废弃特性注册表 | <https://modelcontextprotocol.io/specification/draft/deprecated> | 官方废弃特性清单 |

规范使用 RFC 2119 关键词（MUST / SHOULD / MAY）定义行为要求，Schema 是消息结构和方法清单的权威来源。

---

## 3. 2025-06-18 → 2025-11-25 核心变更

### 3.1 Tasks 能力（SEP-1686）

**Tasks** 是 2025-11-25 中最重要的新增能力，为长时间运行的请求提供标准化的异步原语。

**能力声明**:

```json
{
  "tasks": {
    "requests": {
      "tools.call": true,
      "sampling.createMessage": true,
      "elicitation.create": true
    }
  }
}
```

**任务状态**（来自权威 Schema）:

- `working` — 进行中
- `input_required` — 需要输入
- `completed` — 已完成
- `failed` — 失败
- `cancelled` — 已取消

**核心操作**:

- `tasks/get` — 轮询状态
- `tasks/result` — 获取最终结果（仅 completed 状态）
- `tasks/list` — 分页列出任务
- `tasks/cancel` — 取消未结束任务
- `notifications/tasks/status` — 服务器主动状态通知（可选）

**兼容性**: SEP-1686 明确声明**无破坏性变更**。不支持 Tasks 的服务器会忽略 task 元数据并返回同步响应。

### 3.2 Icons（SEP-973）

服务器可为以下对象附加可选 `icons` 数组：

- `Implementation`（客户端/服务器信息）
- `Tool`
- `Resource`
- `ResourceTemplate`
- `Prompt`

```typescript
{
  "src": "string",           // HTTPS URL 或 data: URI
  "mimeType?": "image/png",  // 推荐 PNG/JPEG，SVG 需安全审查
  "sizes?": ["48x48", "96x96"],
  "theme?": "light" | "dark"
}
```

### 3.3 Sampling 支持 Tools / ToolChoice（SEP-1577）

`sampling/createMessage` 现在可以携带 `tools` 和 `toolChoice`，让服务器能够请求 LLM 执行工具调用：

```typescript
{
  "tools": [...],           // 可用工具列表
  "toolChoice": {
    "type": "auto" | "required" | "none"
  }
}
```

**要求**:

- 客户端必须声明 `sampling.tools` 能力
- 支持多轮工具循环：assistant → `tool_use` → server 执行 → `tool_result` → follow-up
- 每条含 `ToolUseContent` 的 assistant 消息必须后接仅含匹配 `ToolResultContent` 的 user 消息

### 3.4 Elicitation 增强

**Form 模式改进**:

- 原始类型和枚举支持 `default` 默认值
- 使用 `oneOf` / `anyOf` + `title` 替代 `enumNames`（**注意：2025-11-25 未使用 `enumNames`**）
- 多选枚举使用数组 + `items.enum` 或 `items.anyOf`

**URL 模式（SEP-1036）**:

- 新增 `mode: "url"` 用于 OAuth 同意、支付流、API-key 输入等不适合通过 MCP 客户端传递的带外交互
- 错误码 `-32042` (`URLElicitationRequiredError`) 表示需要 URL elicitation
- 服务器可发送 `notifications/elicitation/complete`

### 3.5 OAuth / OpenID Connect 企业级增强

| 变更 | 详情 |
|------|------|
| OpenID Connect Discovery 1.0 | 新增支持的授权服务器发现机制 |
| 增量 scope 同意 | 通过 `WWW-Authenticate` 请求额外 scope |
| RFC 9728 对齐 | OAuth 2.0 Protected Resource Metadata 发现 |
| Client ID Metadata Documents (SEP-991) | `client_id` 推荐为指向 JSON 元数据文档的 URL |
| PKCE | 必须支持 `S256` |
| Resource Indicators (RFC 8707) | 客户端必须发送 `resource` 参数 |
| Token passthrough | **明确禁止** |

注册优先级：预注册凭证 > Client ID Metadata Documents > 动态客户端注册

### 3.6 其他重要变更

- **JSON Schema 2020-12 默认 dialect**（SEP-1613）：Tool 的 `inputSchema` / `outputSchema` 默认使用 JSON Schema 2020-12
- **输入验证作为 Tool 错误返回**（SEP-1303）：验证失败应返回 `isError: true`，让 LLM 可自我修正
- **`Annotations.lastModified`**：资源、提示和内容块支持最后修改时间
- **`Implementation.description`**：可选描述字段
- **Streamable HTTP 成为规范远程传输**：旧 HTTP+SSE 已废弃
- **SSE 轮询/恢复语义**（SEP-1699）

---

## 4. 治理变化：Linux Foundation Agentic AI Foundation

**2025-12-09**，Anthropic 将 MCP 捐赠给 **Agentic AI Foundation**，这是 Linux Foundation 下属的定向基金，由 Block 和 OpenAI 共同创立，Microsoft 和 GitHub 深度参与。

**影响**:

- MCP 不再是单一厂商协议，而是开放中立标准
- 官方工作组管理 SDK、传输、一致性测试、安全
- **Specification Enhancement Proposal (SEP)** 成为正式变更机制
- 提供 12 个月以上的废弃窗口和公开的废弃特性注册表

---

## 5. 版本与兼容性策略

### 版本协商

```text
Client: "latest_supported": "2025-11-25"
Server: "protocolVersion": "2025-11-25" 或回退到支持的版本
```

- 客户端若不支持服务器选择的版本，**应当断开连接**

### 特性生命周期（SEP-2596）

- **Active** → **Deprecated**（至少 12 个月） → **Removed**
- 已废弃示例：HTTP+SSE 传输、`includeContext: "thisServer"` / `"allServers"`

### 传输兼容

- Streamable HTTP 服务器可同时提供旧的 HTTP+SSE 端点以兼容旧客户端

---

## 6. 与 A2A 协议的关系

MCP 和 A2A **互补而非竞争**:

| 协议 | 层级 | 解决的问题 |
|------|------|-----------|
| **MCP** | Agent ↔ Tool | AI 如何发现、调用工具，访问资源和提示 |
| **A2A** | Agent ↔ Agent | 自主 Agent 如何相互发现、协商任务、委托工作、交换结果 |

**典型多 Agent 工作流**:

1. 规划 Agent 接收用户目标
2. 通过 **A2A** 将子任务委托给专业 Agent
3. 每个专业 Agent 通过 **MCP** 访问所需工具和数据
4. 结果通过 A2A 返回给编排器

两者目前都是 Linux Foundation 项目，设计上 intent  interoperable。

---

## 7. 复用视角下的 MCP 安全

### 7.1 信任边界

- **Tool 描述和注解不可完全信任**：恶意服务器可能谎报 tool 功能
- **用户同意是强制的**：敏感操作必须有人类在环

### 7.2 认证与授权

- **禁止 Token 透传**：MCP 服务器不得将客户端 bearer token 转发给下游 API
- **最小权限 scope**：通过 `WWW-Authenticate` 增量请求额外 scope
- **PKCE + Resource Indicators**：防止授权码拦截和 audience 混淆

### 7.3 传输与网络安全

- **TLS 强制**
- **Origin 头验证**：防止 DNS rebinding
- **SSRF 防护**：限制 OAuth 元数据 URL、审慎跟随重定向

### 7.4 本地服务器 / 供应链风险

- 一键安装的本地 MCP server 应显式展示执行命令、沙箱运行
- 企业应验证 server provenance（SLSA、签名、依赖扫描）
- 优先使用按项目的 MCP 配置而非全局配置

### 7.5 多服务器组合

- 组合多个 MCP server 会改变威胁模型：被攻破的 server 可通过 LLM 上下文影响其他 server
- 建议实施：能力发现控制、命名空间隔离、跨 server 监控、集中 tool 审批工作流

---

## 8. 企业就绪评估

2025-11-25 被广泛视为 MCP 的“企业就绪”版本，因为它解决了以下生产部署障碍：

| 企业需求 | 2025-11-25 解决方案 |
|---------|-------------------|
| 长时间运行工作流 | Tasks 提供标准异步句柄 |
| 受管认证 | CIMD、RFC 9728、PKCE、RFC 8707、增量 scope |
| 联邦 / M2M 访问 | Client ID Metadata Documents |
| 可扩展不碎片化 | Extensions 框架 |
| 组合式 Agent 架构 | Sampling with Tools |
| 远程可扩展部署 | Streamable HTTP |

---

## 9. 与四层复用架构的映射

| 本体系层次 | MCP 2025-11-25 映射 |
|-----------|---------------------|
| 05 功能架构 | Tool / Resource / Prompt / Sampling 是功能级复用的协议层 |
| 04 组件架构 | MCP Server 作为可复用组件，需 SBOM + SLSA provenance |
| 03 应用架构 | 多 MCP Server 组合构成 Agentic 应用架构 |
| 12 AI 原生复用 | MCP 是 AI 原生复用的核心协议 |
| 10 供应链安全 | MCP Server 的获取、验证、签名、SBOM 审查 |

---

## 10. 项目中的引用更新建议

以下文件/位置应将对 "MCP 2026-07-28 RC" 的引用更新为 "MCP 2025-11-25"：

- `05-functional-architecture-reuse/README.md`
- `05-functional-architecture-reuse/06-mcp-a2a-protocols/protocol-analysis.md`
- `07-formal-verification/01-tla-plus/mcp-capability-negotiation.tla`
- `07-formal-verification/01-tla-plus/mcp-capability-negotiation.md`
- `12-ai-native-reuse/README.md`
- `struct/README.md`（已完成）
- `struct/MASTER_PLAN.md`（已完成）

---

## 11. 参考链接

- MCP 2025-11-25 Spec: <https://modelcontextprotocol.io/specification/2025-11-25>
- Changelog: <https://modelcontextprotocol.io/specification/2025-11-25/changelog>
- Versioning: <https://modelcontextprotocol.io/specification/versioning>
- Tasks Spec: <https://modelcontextprotocol.io/specification/draft/basic/utilities/tasks>
- Authorization: <https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization>
- Security Best Practices: <https://modelcontextprotocol.io/specification/2025-11-25/basic/security_best_practices>
- Anthropic Donation Announcement: <https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation>
- GitHub Blog on LF Move: <https://github.blog/open-source/maintainers/mcp-joins-the-linux-foundation-what-this-means-for-developers-building-the-next-era-of-ai-tools-and-agents/>
- A2A Protocol: <https://github.com/google/A2A>


---

## 补充说明：MCP 2025-11-25 规范深度解析

## 概念定义

**定义**：MCP 是由 Anthropic 主导的开放协议，规范 AI 模型如何发现、调用工具并交换上下文，使工具成为可复用资产。

## 示例

**示例**：代码助手通过 MCP 调用统一代码搜索工具，返回结构化上下文；不同 IDE 插件复用同一工具，无需各自实现代码索引。

## 反例

**反例**：Agent 通过私有 HTTP 端点调用工具，无 Schema 注册与权限控制，工具变更导致所有调用方失效。

## 权威来源

> **权威来源**:
>
> - [Model Context Protocol](https://modelcontextprotocol.io/specification/2025-11-25)
> - [MCP Introduction](https://modelcontextprotocol.io/introduction)
> - 核查日期：2026-07-07

## 分析

**分析**：MCP 将工具从“代码片段”提升为“可发现服务”，是 Agent 生态互操作的关键。