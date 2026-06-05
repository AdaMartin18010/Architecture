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

```
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

**关键特征**:
- **Stateful connections**: 连接是有状态的，支持能力协商
- **Capability negotiation**: 连接时交换能力（capabilities）
- **JSON-RPC 2.0**: 基于 JSON-RPC 的消息格式
- **Multiple transports**: stdio、HTTP+SSE、Streamable HTTP

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

---

## 6. 传输方式

| 传输方式 | 适用场景 | 状态 |
|---------|---------|------|
| **stdio** | 本地进程间通信 | 稳定 |
| **HTTP+SSE** | 服务器端推送 | 被 Streamable HTTP 取代 |
| **Streamable HTTP** | 远程 Server，支持流式 | 2025-03-26 引入 |

### Streamable HTTP 要点

- Server 必须支持无 SSE 的普通 HTTP POST
- 当需要流式响应时，Server 可升级连接
- 使用 `MCP-Protocol-Version` 头部协商版本

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

> 最后更新: 2026-06-06
> 权威来源: https://modelcontextprotocol.io/specification/2025-11-25/
> 勘误: 此前文档中关于 2026-07-28 RC 无状态版本的描述不准确，已根据官方规范修正。
