# A2A v1.0 权威规范解读

> **版本**: 2026-06-06
> **权威来源**: Google A2A Protocol, Linux Foundation, Cloud Next 2026
> **定位**: 对齐 A2A v1.0 正式发布版本的核心概念与架构模式

---

## 1. A2A 发展历程

| 里程碑 | 时间 | 事件 |
|--------|------|------|
| 首次发布 | 2025-04 | Google 发布 A2A 协议，50+ 合作伙伴 |
| 捐赠 LF | 2025-06 | 捐赠给 Linux Foundation |
| v0.3 | 2026-03 | 增加 gRPC 支持、安全签名、多租户 |
| **v1.0** | **2026-04** | **Google Cloud Next 2026 正式发布** |

> **关键确认**: A2A v1.0 于 2026 年 4 月在 Google Cloud Next '26 大会上正式发布。此前文档中关于 2026-03-12 的日期需要修正。

---

## 2. A2A v1.0 核心对象

```
A2A Protocol
├── Agent Card（代理卡片）
│   ├── 发布在: /.well-known/agent.json
│   ├── 包含: 能力、端点、认证方案、制造商信息
│   └── v1.0 新增: 签名 Agent Cards（加密身份验证）
│
├── Task（任务）
│   ├── 状态: submitted → working → input-required → completed / canceled / failed
│   ├── 支持: 多轮交互、流式更新
│   └── v1.0 新增: 多租户支持
│
├── Message（消息）
│   ├── Role: user / agent
│   └── Parts: text / file / data
│
├── Artifact（产物）
│   ├── 类型: text / file / structured data
│   └── 作为 Task 的结果返回
│
└── Security（安全）
    ├── OAuth 2.1 with PKCE（v1.0 默认）
    ├── API Keys
    ├── mTLS
    └── Signed Agent Cards
```

---

## 3. Agent Card 规范

```json
{
  "name": "research-agent",
  "description": "A research specialist agent",
  "url": "https://agent.example.com/",
  "provider": {
    "organization": "Example Inc."
  },
  "version": "1.0.0",
  "documentationUrl": "https://docs.example.com/agent",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "stateTransitionHistory": true
  },
  "authentication": {
    "schemes": ["OAuth2", "ApiKey"]
  },
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text", "file"],
  "skills": [
    {
      "id": "web-research",
      "name": "Web Research",
      "description": "Performs deep web research on a topic",
      "tags": ["research", "web"],
      "examples": ["Research the latest AI safety guidelines"]
    }
  ]
}
```

### v1.0 新增字段

| 字段 | 说明 |
|------|------|
| `signature` | Agent Card 的数字签名 |
| `multiTenant` | 是否支持多租户 |
| `rateLimits` | 速率限制声明 |
| `pricing` | 服务定价信息 |

---

## 4. Task 状态机

```
Task Lifecycle
├── submitted（已提交）
├── working（处理中）
├── input-required（需要额外输入）
│   └── 可循环回到 working
├── completed（已完成）
├── canceled（已取消）
└── failed（失败）
```

### v1.0 增强

- **流式更新**: SSE 流式任务更新成为规范的一部分（而非扩展）
- **多租户**: 企业级隔离
- **gRPC 支持**: 高性能 Agent 通信
- **历史状态**: 可选的状态转换历史

---

## 5. A2A 与 MCP 的互补关系

```
完整 Agent 架构
│
├── Agent ↔ Tools: MCP
│   └── 数据库查询、API 调用、文件读取
│
├── Agent ↔ Agent: A2A
│   └── 任务委托、能力协商、结果交付
│
└── Agent ↔ Humans: 自然语言界面
```

| 维度 | MCP | A2A |
|------|-----|-----|
| 范围 | Agent → Tool | Agent → Agent |
| 关系 | Client-Server | Peer-to-Peer |
| 发现 | Server lists capabilities | Agent Card at well-known URL |
| 会话 | 有状态连接 | 基于 Task 的异步 |
| 流式 | 支持 | SSE 原生支持 |
| 认证 | OAuth 2.1 | OAuth 2.1 with PKCE |
| 创建者 | Anthropic → Linux Foundation | Google → Linux Foundation |

---

## 6. A2A v1.0 安全机制

### 6.1 Signed Agent Cards

v1.0 引入 Agent Card 签名：

```json
{
  "agent": { ... },
  "signature": {
    "algorithm": "Ed25519",
    "publicKey": "...",
    "signature": "..."
  }
}
```

**作用**:
- 防止 Agent Card 伪造
- 确保 Agent 身份可验证
- 支持 Agent-to-Agent 信任链

### 6.2 OAuth 2.1 with PKCE

v1.0 将 OAuth 2.1 with PKCE 设为默认认证方案，取代早期草案中的纯 Bearer Token。

### 6.3 Agent Payments Protocol (AP2)

v1.0 生态系统中出现 AP2（Agent Payments Protocol）：
- 支持 Agent 驱动的安全交易
- 60+ 组织支持
- 用于 Agent 服务的市场化支付

---

## 7. 生态系统状态（2026-04）

| 指标 | 数值 |
|------|------|
| 支持组织 | 150+ |
| GitHub Stars | 22,000+ |
| SDK 语言 | Python, JS, Java, Go, .NET |
| 云平台 | GCP, Azure, AWS |

### 主要支持平台

- Google Vertex AI Agent Builder（原生）
- Microsoft Azure AI Foundry
- Amazon Bedrock AgentCore Runtime
- LangGraph
- CrewAI
- AutoGen
- Semantic Kernel

---

## 8. 生产部署建议

### 网络架构

```
Kubernetes Deployment
├── Agent Pod
│   └── 暴露 /.well-known/agent.json
├── Service (ClusterIP)
├── Ingress (TLS)
│   └── 仅暴露 A2A Gateway
└── NetworkPolicy
    └── 限制 Agent 间流量
```

### 关键考虑

1. **可观测性**: 使用 OpenTelemetry GenAI 约定
2. **评估（Evals）**: 将评估作为 CI 门禁
3. **缓存**: 多层缓存降低延迟和成本
4. **模型选择**: 避免所有 Agent 默认调用最贵的模型

---

## 9. 对架构复用的影响

> **定理 A2A.2** (Agent Card Network Effect): A2A Agent 的复用价值与 A2A 生态中其他 Agent 的数量成正比。生态越大，单个 Agent 的价值越高。

> **定理 A2A.3** (Cross-Vendor Interoperability): A2A 的核心价值在于跨厂商 Agent 的互操作。单一厂商内部的 Agent 协调可以使用专有协议，但跨厂商必须使用开放标准。

---

## 10. 与 MCP 的集成模式

### 模式 1: A2A Agent 内部使用 MCP

```
Orchestrator Agent (A2A)
    ├── Specialist Agent A (A2A)
    │   └── 内部使用 MCP → Database Server
    ├── Specialist Agent B (A2A)
    │   └── 内部使用 MCP → API Server
    └── Specialist Agent C (A2A)
        └── 内部使用 MCP → File System
```

### 模式 2: Gateway 统一路由

```
User Request → A2A Gateway
    ├── MCP Tool Calls → MCP Servers
    └── A2A Task Delegation → Specialist Agents
```

---

> 最后更新: 2026-06-06
> 权威来源:
> - https://a2aprotocol.ai/
> - Google Cloud Next 2026 发布资料
> - Linux Foundation Agentic AI Foundation
> 勘误: A2A v1.0 正式发布时间为 2026-04，此前文档中的 2026-03-12 日期已修正。
