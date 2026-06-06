# LLM 函数复用与智能体功能架构
>
> 版本: 2026-06-06
> 对齐来源: OpenAI Function Calling, MCP 2025-11-25, Semantic Kernel / AutoGen / Microsoft Agent Framework (MAF), Google A2A v1.0

## 1. LLM 函数调用生态演进

### 1.1 三代函数复用范式

| 世代 | 时间 | 范式 | 代表技术 |
|-----|------|------|---------|
| **Gen 1** | 2023–2024 | 原生 Function Calling | OpenAI Tools, Anthropic Tool Use |
| **Gen 2** | 2024–2025 | 框架抽象层 | LangChain Tools, Semantic Kernel Plugins, LlamaIndex Agents |
| **Gen 3** | 2025–2026 | 标准化协议层 | MCP (agent↔tool), A2A (agent↔agent), MAF (企业编排) |

### 1.2 核心问题：从"写函数"到"组合能力"

- **Gen 1/2**：每个框架有自己的工具定义格式，无法跨框架复用
- **Gen 3**：通过标准化协议（MCP/A2A）实现能力注册、发现、调用、安全治理的统一

## 2. MCP（Model Context Protocol）工具复用

### 2.1 工具作为复用单元

```json
{
  "name": "query_knowledge_base",
  "description": "查询企业知识库，返回相关文档片段",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string" },
      "top_k": { "type": "integer", "default": 5 }
    },
    "required": ["query"]
  }
}
```

### 2.2 工具注册与发现

| 层级 | 机制 | 复用范围 |
|-----|------|---------|
| **本地** | `stdio` 传输，本地进程 | 单用户/单会话 |
| **远程** | Streamable HTTP，OAuth 2.1 | 团队/企业 |
| **市场** | 社区 Registry（未来）| 跨组织生态 |

### 2.3 工具组合模式

```
Agent Session
├── Tool A: retrieve_documents(vector_db)
├── Tool B: query_database(sql_engine)
├── Tool C: send_email(notification_service)
└── Tool D: create_jira_ticket(project_mgmt)

Workflow（由 LLM 规划）:
  1. retrieve_documents("客户投诉处理流程")
  2. query_database("SELECT * FROM complaints WHERE id = 12345")
  3. 分析并决策
  4. send_email(to="manager", body="升级建议...")
  5. create_jira_ticket(project="CS", title="...")
```

## 3. Microsoft Agent Framework（MAF）

### 3.1 统一引擎（2025-10 发布，2026 Q1 GA）

MAF 将 Semantic Kernel 与 AutoGen 融合：

- **Semantic Kernel**：企业级 SDK，插件（Plugin）和记忆（Memory）抽象
- **AutoGen**：多智能体对话编排（Group Chat），灵活但缺乏生产级类型安全
- **MAF**：AutoGen 的编排模式 + Semantic Kernel 的企业级地基

### 3.2 复用层次

| 层次 | 复用单元 | 说明 |
|-----|---------|------|
| **Kernel Plugin** | 函数集合 | 封装 API 调用、数据库查询、文件操作 |
| **Agent** | 角色 + 工具 + 记忆 | 可复用的智能体模板（如"客服代理"、"代码审查代理"）|
| **Team** | 多智能体编排 | Group Chat 模式、层级汇报模式、竞争评审模式 |

## 4. A2A（Agent-to-Agent）能力复用

### 4.1 Agent Card 作为能力契约

```json
{
  "name": "travel-booking-agent",
  "description": "预订航班和酒店的智能体",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": false
  },
  "skills": [
    { "id": "flight-search", "name": "航班搜索" },
    { "id": "hotel-booking", "name": "酒店预订" }
  ],
  "authentication": {
    "schemes": ["OAuth2", "mTLS"]
  }
}
```

### 4.2 A2A 与 MCP 的互补复用

| 维度 | MCP | A2A |
|-----|-----|-----|
| 关系 | Agent ↔ Tool | Agent ↔ Agent |
| 协议 | JSON-RPC 2.0 | HTTP + JSON-RPC + SSE |
| 能力描述 | Tool Schema | Agent Card |
| 生命周期 | 会话级连接 | 任务级协作 |
| 安全 | OAuth 2.1 + RFC 8707 | OAuth 2.1 + PKCE + mTLS |
| **复用价值** | 工具标准化注册 | 智能体服务化发现 |

## 5. LLM 函数复用最佳实践

### 5.1 函数设计原则

| 原则 | 说明 |
|-----|------|
| **单一职责** | 每个函数只做一件事，便于 LLM 组合 |
| **自描述** | `description` 必须精确说明功能、输入、输出、副作用 |
| **幂等性** | 函数应尽可能幂等，支持重试 |
| **确定性** | 相同输入产生相同输出（或明确标记不确定性）|
| **防御性** | 参数校验、范围检查、优雅降级 |

### 5.2 版本与兼容性

```
Tool Registry
├── query_db@v1.0.0 (stable)
├── query_db@v1.1.0-beta (new features)
└── query_db@v2.0.0-rc (breaking changes)

Agent 声明依赖：
  "requiredTools": ["query_db@^1.0.0"]
```

### 5.3 安全边界

| 风险 | 缓解 |
|-----|------|
| 提示注入通过工具参数 | 输入净化、参数类型严格校验 |
| 工具过度授权 | 最小权限原则、能力证明（Capability Attestation）|
| 工具版本漂移 | 版本锁定、兼容性测试 |
| 敏感数据泄漏 | 输出过滤、审计日志、数据分类 |

## 6. 与功能架构复用的映射

| 传统功能复用 | LLM 时代映射 | 协议/标准 |
|------------|------------|----------|
| 共享库（Library）| Kernel Plugin / MCP Tool | MCP 2025-11-25 |
| 服务 API（Service）| Agent Skill / Agent Card | A2A v1.0 |
| 工作流（Workflow）| Agent Team / Group Chat | MAF / AutoGen |
| 业务规则（Business Rule）| LLM Prompt + Tool Guardrails | 自定义 |
| 数据访问（DAO）| Retrieval Resource | MCP Resource |

## 7. 参考索引

- OpenAI: Function Calling API Documentation
- Anthropic: Tool Use Documentation
- Microsoft: Semantic Kernel Documentation
- Microsoft: AutoGen Documentation
- Microsoft Agent Framework (MAF): 2025-10 Announcement, 2026-Q1 GA
- Model Context Protocol: Specification 2025-11-25
- Google A2A Protocol: v1.0 (Cloud Next 2026-04)
