# A2A + MCP 混合 Agent 服务 PoC

> **定位**：演示 "A2A 用于 Agent 协作，MCP 用于工具调用" 的生产最佳实践。
> **对齐**：A2A v1.0.0.0.0.0.0, MCP 2025-11-25
> **权威来源**（已核查 2026-07-08）：
>
> | 来源 | URL |
> |------|-----|
> | A2A Protocol Specification v1.0.0 | <https://a2a-protocol.org/latest/specification/> |
> | A2A Protocol Latest | <https://a2a-protocol.org/latest/> |
> | MCP Specification 2025-11-25 | <https://modelcontextprotocol.io/specification/2025-11-25> |
> | MCP Introduction | <https://modelcontextprotocol.io/introduction> |
> | Agentic AI Foundation | <https://aaif.io/> |

---

## 概念定义

**A2A + MCP 混合 Agent**：采用 A2A（Agent-to-Agent Protocol）实现 Agent 之间的能力发现、任务委托与结果交付；采用 MCP（Model Context Protocol）实现 Agent 与外部工具/上下文源之间的标准化调用。两者分层互补，A2A 负责 Agent 协作边界，MCP 负责 Agent-工具能力边界。

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

**协议映射**：

| 功能 | 协议 | 关键方法/机制 |
|------|------|--------------|
| Agent 能力发现 | A2A | `/.well-known/agent-card.json` |
| 任务委托 | A2A | `tasks/send`、`tasks/sendSubscribe` |
| 工具发现 | MCP | `tools/list` |
| 工具调用 | MCP | `tools/call` |
| 认证 | A2A + MCP | OAuth 2.1 + PKCE |

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
        "parts": [{"text": "What'"'"'s the weather in Shanghai?"}]
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
| `test_e2e.py` | 端到端测试 |
| `test_mcp_server.py` | MCP 工具单元测试 |
| `README.md` | 本文档 |

---

## 示例：企业内部 AI 助手

某中型 SaaS 公司基于本 PoC 构建内部 AI 助手：

- **A2A 编排层**：统一入口 Agent 接收自然语言请求，根据 Agent Card 将任务路由给代码助手、销售助手或运维助手。
- **MCP 工具层**：代码助手调用 Git 检索、单元测试执行与文档搜索 MCP Server；销售助手调用 CRM 查询与邮件起草 MCP Server。
- **治理层**：所有工具调用通过 Agent OS 策略引擎判定权限，敏感操作触发人工复核。

**收益**：

- 新增业务助手平均只需 1 周，工具能力可跨 Agent 复用。
- 通过统一 A2A 接口，前端客户端无需关心各业务 Agent 的内部实现。

---

## 反例：绕过 A2A 直接调用 MCP 工具

**场景**：某团队为图方便，让前端应用直接调用 MCP Server 的工具端点，跳过 A2A 编排 Agent。

**问题**：

1. 前端需要理解每个 MCP Server 的 Schema 与认证方式，集成复杂度上升。
2. 跨工具任务编排（如“先查询订单，再发送邮件”）由前端硬编码，难以复用。
3. 缺乏统一的审计入口，无法追踪完整任务链路。
4. 权限控制散落在各 MCP Server，难以实施最小权限。

**后果**：每个前端团队重复建设编排逻辑，Agent 能力无法沉淀为企业资产。

**避免建议**：

1. 所有 Agent 间协作统一走 A2A，前端只与编排 Agent 交互。
2. MCP 工具仅作为 Agent 内部能力，不直接暴露给最终客户端。
3. 在 A2A Server 层统一记录 Task 生命周期、工具调用链与审计日志。

---

## 分析与讨论

本 PoC 的核心假设是：A2A 与 MCP 应在架构中分层使用，而非相互替代。A2A 提供 Agent 级别的抽象（Who can do what），MCP 提供工具级别的抽象（How to do it）。将两者混为一谈会导致：

- 前端需要理解底层工具 Schema，集成成本上升。
- 跨工具的业务流程编排碎片化，难以复用。
- 安全与审计边界模糊，责任难以追溯。

因此，生产演进应优先加固 A2A 编排层与 MCP 工具网关，而非让客户端直接穿透到工具层。

## 6. 生产演进路径

| 阶段 | 改进 |
|------|------|
| **当前 (PoC)** | Mock MCP 工具；内存任务存储；单进程 |
| **短期** | 替换 `MockMCPTools` 为真实 `mcp.ClientSession`；连接外部 MCP Server |
| **中期** | Redis 任务持久化；多 Worker 并发；OAuth2/JWT 认证 |
| **长期** | Signed Agent Cards (JWS)；OpenTelemetry 分布式追踪；多 Agent 联邦编排 |

---

## 7. 与项目结构的映射

| 项目目录 | 本 PoC 角色 |
|----------|-------------|
| `struct/12-ai-native-reuse/01-mcp-protocol/` | MCP 工具层规范 |
| `struct/12-ai-native-reuse/02-a2a-protocol/` | A2A Agent 协作规范 |
| `struct/04-component-architecture-reuse/` | Agent 作为可复用服务组件 |
| `struct/06-cross-layer-governance/` | Agent Card 注册表、任务审计 |

---

## 8. 权威来源

> **权威来源**（已核查 2026-07-08）：
>
> | 来源 | URL |
> |------|-----|
> | A2A Protocol Specification v1.0.0 | <https://a2a-protocol.org/latest/specification/> |
> | A2A Protocol Latest | <https://a2a-protocol.org/latest/> |
> | Model Context Protocol Specification 2025-11-25 | <https://modelcontextprotocol.io/specification/2025-11-25> |
> | MCP Introduction | <https://modelcontextprotocol.io/introduction> |
> | Agentic AI Foundation | <https://aaif.io/> |

---

*文档生成时间：2026-07-08 · 对齐 A2A v1.0.0.0.0.0.0 / MCP 2025-11-25*