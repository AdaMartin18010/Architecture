# A2A + MCP 混合 Agent 服务 PoC

> **定位**：演示 "A2A 用于 Agent 协作，MCP 用于工具调用" 的生产最佳实践。
> **对齐**：A2A v1.2、MCP 2025-11-25

---

## 1. 架构设计

```text
┌─────────────────────────────────────────────────────────────┐
│  A2A Client (LangGraph / CrewAI / ADK / Browser)            │
│  └── HTTP POST /jsonrpc (tasks/send)                        │
├─────────────────────────────────────────────────────────────┤
│  A2A Server (FastAPI)                                       │
│  ├── GET /.well-known/agent-card.json                       │
│  ├── POST /jsonrpc                                          │
│  │   ├── tasks/send         → 同步任务处理                   │
│  │   ├── tasks/sendSubscribe → SSE 流式响应                  │
│  │   └── tasks/get          → 查询任务状态                   │
│  └── 内部：意图识别 → MCP 工具路由                            │
├─────────────────────────────────────────────────────────────┤
│  MCP Tool Layer (模拟 / 真实 MCP Server)                     │
│  ├── get_weather(city)                                      │
│  ├── calculator(expression)                                 │
│  └── search_docs(query)                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 快速开始

### 安装依赖

```bash
cd struct/12-ai-native-reuse/04-hybrid-a2a-mcp-poc/
pip install fastapi uvicorn
```

### 启动服务

```bash
python hybrid_agent_server.py
# 或
uvicorn hybrid_agent_server:app --reload --port 8000
```

### 测试 Agent Card 发现

```bash
curl http://localhost:8000/.well-known/agent-card.json
```

### 测试同步任务

```bash
curl -X POST http://localhost:8000/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tasks/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"text": "What's the weather in Shanghai?"}]
      }
    }
  }'
```

### 测试流式任务 (SSE)

```bash
curl -X POST http://localhost:8000/jsonrpc \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tasks/sendSubscribe",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"text": "Calculate 15 * 23 + 7"}]
      }
    }
  }'
```

### 测试文档搜索

```bash
curl -X POST http://localhost:8000/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tasks/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [{"text": "Search docs for reusable component patterns"}]
      }
    }
  }'
```

---

## 3. 代码结构

| 文件 | 说明 |
|------|------|
| `hybrid_agent_server.py` | FastAPI A2A Server + Mock MCP 工具层 |
| `README.md` | 本文档 |

---

## 4. 生产演进路径

| 阶段 | 改进 |
|------|------|
| **当前 (PoC)** | Mock MCP 工具；内存任务存储；单进程 |
| **短期** | 替换 `MockMCPTools` 为真实 `mcp.ClientSession`；连接外部 MCP Server |
| **中期** | Redis 任务持久化；多 Worker 并发；OAuth2/JWT 认证 |
| **长期** | Signed Agent Cards (JWS)；OpenTelemetry 分布式追踪；多 Agent 联邦编排 |

---

## 5. 与项目结构的映射

| 项目目录 | 本 PoC 角色 |
|----------|-------------|
| `struct/12-ai-native-reuse/01-mcp-protocol/` | MCP 工具层规范 |
| `struct/12-ai-native-reuse/02-a2a-protocol/` | A2A Agent 协作规范 |
| `struct/04-component-architecture-reuse/` | Agent 作为可复用服务组件 |
| `struct/06-cross-layer-governance/` | Agent Card 注册表、任务审计 |

---

*文档生成时间：2026-06-06 · 对齐 A2A v1.2 / MCP 2025-11-25*


---

## 补充说明：A2A + MCP 混合 Agent 服务 PoC

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
