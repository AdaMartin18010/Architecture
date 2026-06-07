# MCP 2026-07-28 RC 深度解析

> ⚠️ **过时文档警告 / OBSOLETE DOCUMENT WARNING**
>
> 经官方渠道核实，**MCP 当前稳定版为 `2025-11-25`**，Anthropic 已于 2025-12-09 将其捐赠给 Linux Foundation Agentic AI Foundation。本文件中引用的 **"MCP 2026-07-28 RC" 并不存在**，属于项目早期的错误假设。
>
> 请参考最新权威文档：
>
> - [`mcp-2025-11-25-deep-dive.md`](./mcp-2025-11-25-deep-dive.md)
> - [`mcp-2025-11-25-authoritative.md`](./mcp-2025-11-25-authoritative.md)
> - 官方规范：<https://modelcontextprotocol.io/specification/2025-11-25>
>
> **版本**: 2026-06-06
> **对齐标准**: MCP 2026-07-28 RC (2026-05-21 锁定) — **已勘误为 2025-11-25**
> **定位**: 历史存档，保留以展示项目认知迭代过程

---

## 目录

- [MCP 2026-07-28 RC 深度解析](#mcp-2026-07-28-rc-深度解析)
  - [目录](#目录)
  - [1. 核心变更对照表](#1-核心变更对照表)
  - [2. 无状态架构的复用意义](#2-无状态架构的复用意义)
  - [3. 协议栈的复用层次](#3-协议栈的复用层次)
  - [4. 传输层详解](#4-传输层详解)
    - [Streamable HTTP（2026-07-28 主推）](#streamable-http2026-07-28-主推)
    - [传输层选择决策矩阵](#传输层选择决策矩阵)
  - [5. 能力层详解](#5-能力层详解)
    - [Tools（函数复用）](#tools函数复用)
    - [Resources（数据复用）](#resources数据复用)
    - [Prompts（提示模板复用）](#prompts提示模板复用)
    - [Sampling（推理复用）](#sampling推理复用)
  - [6. 缓存语义与 ttlMs](#6-缓存语义与-ttlms)
  - [7. Extensions 框架](#7-extensions-框架)
    - [Tasks Extension（已毕业）](#tasks-extension已毕业)
  - [8. 安全机制](#8-安全机制)
    - [OAuth 2.1 + 防 Issuer 混淆](#oauth-21--防-issuer-混淆)
    - [威胁模型](#威胁模型)

---

## 1. 核心变更对照表

| 变更项 | 2025-11-25 (旧) | 2026-07-28 RC (新) | 复用影响 |
|--------|----------------|-------------------|----------|
| **传输模型** | 有状态会话 (Stateful) | **无状态核心 (Stateless)** | 支持负载均衡、自动扩缩容 |
| **握手协议** | initialize/initialized 握手 | **移除握手**，每请求自包含 | 降低连接开销，简化网关 |
| **会话标识** | Mcp-Session-Id 头部 | **移除** | 无需粘性会话 |
| **路由机制** | 网关需解析 JSON-RPC 体 | **Mcp-Method 头部路由** | 网关性能提升，可缓存 |
| **缓存机制** | 无标准缓存元数据 | **ttlMs 字段 + 缓存语义** | tools/list 可缓存，减少延迟 |
| **扩展框架** | 实验性扩展 | **正式 Extensions 框架** | 标准化扩展演进 |
| **Tasks 扩展** | 实验性 | **正式毕业** | 支持长时任务复用 |
| **MCP Apps** | 无 | **新增服务器渲染 UI** | 交互式工具复用 |
| **授权** | 基础 OAuth | **OAuth 2.1 + 防 issuer 混淆** | 企业级安全 |

---

## 2. 无状态架构的复用意义

```text
MCP 无状态架构的复用优势
├── 水平扩展
│   ├── 旧: 粘性会话 → 单实例瓶颈
│   └── 新: 轮询负载均衡 → 任意实例处理任意请求
│
├── 网关简化
│   ├── 旧: 网关需解析 JSON-RPC 体 → 高 CPU 开销
│   └── 新: Mcp-Method 头部路由 → 低延迟、可缓存
│
├── 缓存策略
│   ├── tools/list: 可缓存（ttlMs 控制）→ 减少重复发现
│   └── resources/read: 可缓存（不变资源）→ 减少 I/O
│
└── Serverless 兼容
    ├── 旧: 长连接会话 → 不适合 FaaS
    └── 新: 无状态请求 → 完美适配 Lambda/Cloud Functions
```

**形式化洞察**: 无状态化将 MCP Server 从"会话参与者"降级为"纯函数执行器"。每个请求 r 可表示为：

```text
Response(r) = f(Capabilities(r), Context(r), Parameters(r))
```

其中 f 是 MCP Server 的实现函数，无外部状态依赖。这使得 MCP Server 天然满足**引用透明性**（Referential Transparency），从而具备最高等级的功能复用性。

---

## 3. 协议栈的复用层次

```text
MCP 协议栈复用层次
├── 传输层 (Transport)
│   ├── stdio: 本地进程通信
│   ├── SSE (Server-Sent Events): 单向流
│   ├── Streamable HTTP: 双向流（2026-07-28 主推）
│   └── 复用单元: 传输适配器、连接池、健康检查
│
├── 协议层 (Protocol)
│   ├── JSON-RPC 2.0: 请求/响应/通知
│   ├── 生命周期: 初始化、能力协商、终止（2026-07-28 简化）
│   └── 复用单元: 协议处理器、消息路由器、错误处理
│
├── 能力层 (Capabilities)
│   ├── tools: 工具调用（函数复用）
│   ├── resources: 资源读取（数据复用）
│   ├── prompts: 提示模板（Prompt 复用）
│   ├── sampling: 模型采样（推理复用）
│   └── 复用单元: 能力定义、Schema 契约、版本管理
│
└── 应用层 (Application)
    ├── Agent 框架: LangChain, Mastra, Spring AI
    ├── IDE 集成: Cursor, VS Code, Claude Code
    └── 复用单元: Agent 技能、工作流模板、交互模式
```

---

## 4. 传输层详解

### Streamable HTTP（2026-07-28 主推）

```http
POST /mcp/v1 HTTP/1.1
Host: api.example.com
Content-Type: application/json
Mcp-Method: tools/call
Authorization: Bearer <token>

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "query_database",
    "arguments": {
      "sql": "SELECT * FROM orders WHERE id = 12345"
    }
  }
}
```

**关键设计**: `Mcp-Method` 头部允许网关在不解析 JSON 体的情况下进行路由和负载均衡，显著降低网关延迟。

### 传输层选择决策矩阵

| 场景 | 推荐传输 | 理由 |
|------|---------|------|
| 本地 CLI 工具 | stdio | 简单，无网络依赖 |
| 服务器→客户端单向推送 | SSE | 兼容性好，支持防火墙穿透 |
| 高并发 Web 服务 | Streamable HTTP | 无状态、可缓存、易扩展 |
| 实时双向流 | Streamable HTTP + SSE 混用 | 请求走 HTTP，推送走 SSE |

---

## 5. 能力层详解

### Tools（函数复用）

```json
{
  "name": "query_database",
  "description": "Execute a read-only SQL query",
  "inputSchema": {
    "type": "object",
    "properties": {
      "sql": { "type": "string" }
    },
    "required": ["sql"]
  }
}
```

**复用语义**: Tool 是可复用的函数接口，其 `inputSchema` 是前置条件的形式化声明。

### Resources（数据复用）

```json
{
  "uri": "file:///docs/api-guide.md",
  "mimeType": "text/markdown",
  "name": "API Guide",
  "ttlMs": 3600000
}
```

**复用语义**: Resource 是可缓存的数据单元。`ttlMs` 声明数据的新鲜度边界，支持缓存复用决策。

### Prompts（提示模板复用）

```json
{
  "name": "code_review",
  "description": "Review code for bugs and style issues",
  "arguments": [
    {
      "name": "code",
      "description": "Code to review",
      "required": true
    }
  ]
}
```

**复用语义**: Prompt 是可参数化的提示模板，将专家工程师的 Prompt 工程能力外化为可复用资产。

### Sampling（推理复用）

```json
{
  "method": "sampling/createMessage",
  "params": {
    "messages": [...],
    "modelPreferences": {...},
    "temperature": 0.1
  }
}
```

**复用语义**: Sampling 允许 Server 请求 Client 的模型进行推理，实现"模型即服务"的反向复用。

---

## 6. 缓存语义与 ttlMs

```text
缓存决策规则
├── ttlMs = undefined
│   └── 不缓存，每次请求重新获取
│
├── ttlMs = 0
│   └── 可缓存但立即过期（用于强制刷新语义）
│
├── ttlMs > 0
│   └── 在 ttlMs 毫秒内可复用缓存副本
│   └── 超过 ttlMs 后必须重新验证
│
└── 资源变更通知（Capability: resources/subscribe）
    └── Server 主动推送变更，Client 可提前使缓存失效
```

**形式化定义**: 设缓存副本 C 的生成时间为 t₀，ttlMs 为 T。则在时间 t 时：

```text
Valid(C, t) ↔ (t - t₀) ≤ T
```

若 `Valid(C, t)` 为假，则 Client 必须重新请求资源或验证资源是否变更。

---

## 7. Extensions 框架

2026-07-28 将 Extensions 从实验性提升为正式框架，允许 MCP 协议的可控演进。

```text
Extensions 注册机制
├── 1. 能力协商
│   └── Client 和 Server 在初始化时交换支持的 Extensions
│
├── 2. Extension 命名空间
│   ├── 标准 Extensions: mcp.ext.tasks, mcp.ext.sampling
│   └── 厂商 Extensions: com.example.custom-extension
│
├── 3. 向后兼容
│   └── 不支持的 Extension 必须被优雅忽略
│
└── 4. 毕业路径
    ├── 实验性 → 标准草案 → 正式标准
    └── 毕业条件: 2+ 独立实现 + 6 个月稳定运行
```

### Tasks Extension（已毕业）

```json
{
  "method": "tasks/send",
  "params": {
    "id": "task-001",
    "name": "generate_report",
    "arguments": {...},
    "timeout": 300000
  }
}
```

**复用语义**: 长时任务的异步执行模板，支持任务状态的查询、取消和结果获取。

---

## 8. 安全机制

### OAuth 2.1 + 防 Issuer 混淆

```text
安全流程
├── 1. 发现
│   └── Client 从 Server 的 .well-known/mcp-server.json 获取元数据
│
├── 2. Issuer 验证
│   └── 验证 issuer 声明与预期 Server 身份一致
│   └── 防止恶意 Server 冒充合法 Server
│
├── 3. Token 获取
│   └── 通过标准 OAuth 2.1 流程获取访问令牌
│
├── 4. 请求签名
│   └── 可选：请求使用 DPoP (Demonstrating Proof-of-Possession) 绑定
│
└── 5. 能力级授权
    └── Server 根据 Token 中的 scope 决定允许的 Tools/Resources/Prompts
```

### 威胁模型

| 威胁 | 防御机制 |
|------|---------|
| 恶意 MCP Server | Issuer 验证、TLS、证书固定 |
| Token 泄露 | DPoP、短有效期 Token、刷新令牌轮换 |
| 能力滥用 | 能力级 scope、最小权限原则 |
| Prompt 注入 | Tool 输入验证、Prompt 模板审计 |
| 数据泄露 | Resource 级访问控制、传输加密 |

---

> 最后更新: 2026-06-06
> 下次更新: MCP 2026-07-28 正式发布后
