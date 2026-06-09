# T12: MCP Tool 能力依赖图验证 (Alloy)

> **版本**: 2026-06-06
> **对应规约**: `mcp-tool-graph.als`
> **对齐标准**: Model Context Protocol (MCP) 2025-11-25（当前稳定版）
> **交叉引用**: `struct/05-functional-architecture-reuse/06-mcp-a2a-protocols/mcp-tool-design.md`
> **理论来源**: Jackson, D. *Software Abstractions*; MCP Specification (Anthropic, 2026)

---

## 目录

- [T12: MCP Tool 能力依赖图验证 (Alloy)](#t12-mcp-tool-能力依赖图验证-alloy)
  - [目录](#目录)
  - [1. 建模背景](#1-建模背景)
  - [2. 签名设计与 MCP 规范映射](#2-签名设计与-mcp-规范映射)
    - [2.1 MCPServer（服务器）](#21-mcpserver服务器)
    - [2.2 MCPTool（工具）](#22-mcptool工具)
    - [2.3 Capability（能力）](#23-capability能力)
    - [2.4 Resource（资源）](#24-resource资源)
  - [3. 核心约束的形式化](#3-核心约束的形式化)
    - [F3: AcyclicToolCalls（调用无环）](#f3-acyclictoolcalls调用无环)
    - [F4: CapabilityClosure（能力封闭）](#f4-capabilityclosure能力封闭)
  - [4. 断言与验证](#4-断言与验证)
  - [5. 反例教学：能力越权调用](#5-反例教学能力越权调用)
  - [6. 与功能架构复用的交叉引用](#6-与功能架构复用的交叉引用)
  - [7. 权威来源](#7-权威来源)

## 1. 建模背景

Model Context Protocol (MCP) 是 AI 代理与外部工具、数据资源之间的标准化接口协议。在 MCP 2025-11-25 规范中，Server 通过 `tools/list` 暴露工具集合，每个工具具有 JSON Schema 定义的输入输出和一组声明的 `annotations`。当 Agent 调用工具时，工具内部可能进一步调用其他工具，形成工具调用依赖图（Tool Invocation Dependency Graph, TIDG）。

本 Alloy 规约将 MCP 的 Server-Tool-Capability-Resource 结构形式化，验证两项关键架构约束：

1. **结构约束**：工具依赖图中不存在循环调用（防止死循环与级联失败）。
2. **安全约束**：每个被调用的工具，其能力必须在调用者 Server 的能力列表中（最小权限原则的形式化）。

---

## 2. 签名设计与 MCP 规范映射

### 2.1 MCPServer（服务器）

`MCPServer` 对应 MCP 规范中的 Server 实体，是能力的宿主容器。在 Alloy 中，Server 与 Tool、Capability、Resource 之间通过关系字段（`capabilities`、`tools`、`resources`）建模，这与 JSON-RPC 层面的 `initialize` 握手和 `tool/list` 响应语义一致。

### 2.2 MCPTool（工具）

`MCPTool` 对应规范中的 Tool 定义，包含 `name`、`description`、`inputSchema` 等元数据。在 Alloy 的抽象层面，我们聚焦于工具间的调用关系 `calls` 和能力提供关系 `provides`。`calls` 是一个自反关系（`MCPTool -> MCPTool`），表示工具在执行过程中发起的子调用。

### 2.3 Capability（能力）

`Capability` 是 MCP 规范中较新的抽象，用于语义化地描述工具"能做什么"。与工具的一对一关系不同，一个工具可以提供多种能力，一种能力也可以由多个工具实现。这种多对多关系在 Alloy 中通过 `provides: set Capability` 简洁表达。

### 2.4 Resource（资源）

`Resource` 对应 MCP 的 `resources/list` 和 `resources/read` 接口，代表 URI 可寻址的数据实体。`accesses` 关系建模工具对资源的访问权限，用于验证资源隔离性。

---

## 3. 核心约束的形式化

### F3: AcyclicToolCalls（调用无环）

```alloy
fact AcyclicToolCalls {
    all t: MCPTool | t not in t.^calls
}
```

这是本规约最核心的结构约束。`^calls` 表示 `calls` 的传递闭包。禁止任何工具通过一条或多步子调用回到自身。

在真实 MCP 部署中，循环调用的危害远超普通函数递归：

- **协议层死锁**：每个工具调用都是一个 JSON-RPC 请求，循环调用会导致请求链无限增长，最终耗尽连接池或触发超时。
- **上下文膨胀**：MCP 调用伴随上下文窗口（Context Window）的累积，循环调用将导致上下文无限膨胀，Token 成本指数级上升。
- **错误雪崩**：若循环链中任一工具失败，错误将沿循环传播，难以定位根因。

### F4: CapabilityClosure（能力封闭）

```alloy
fact CapabilityClosure {
    all t: MCPTool |
        all callee: t.calls |
            callee.server = t.server or
            callee.provides in t.server.capabilities
}
```

这一约束形式化了 MCP 安全模型中的"能力委托"原则。当一个工具调用另一个工具时，被调用工具的能力必须是调用者 Server 已显式声明的能力的子集。这类似于操作系统中的 capability-based security：进程只能使用其能力列表中授权的操作。

在 `struct/05-functional-architecture-reuse/06-mcp-a2a-protocols/mcp-tool-design.md` 中，定理 5.1（Tool Reuse Equivalence）指出 MCP Tool 的复用等价于其语义描述与模式约束的可传递性。`CapabilityClosure` 正是这一定理在安全性维度的补充：语义传递必须在授权边界内进行。

---

## 4. 断言与验证

| 断言 | 验证目标 | 教学意义 |
|------|---------|---------|
| `NoCyclicToolCalls` | 调用图 DAG | 防止协议层死循环 |
| `CapabilityContainment` | 能力子集关系 | 最小权限原则 |
| `ResourceBoundary` | 资源所有者匹配 | 数据隔离与防泄漏 |
| `ServerCapabilityNonEmpty` | 能力列表非空 | 防止空能力 Server 暴露工具 |

所有断言均通过 `check` 命令在有限 scope 内验证。若断言成立，Alloy 返回 "no counterexample found"；若失败，Alloy 生成有向图形式的最小反例，节点为工具实例，边为 `calls` 关系。

---

## 5. 反例教学：能力越权调用

若要展示"调用未授权工具"的危害，可临时注释掉 `F4`，执行：

```alloy
run CapabilityViolation for 3 but 6 MCPTool, 4 Capability
```

Alloy 可能生成如下反例：

```
Server_A (capabilities: {readFile, writeFile})
  └── Tool_1 (provides: {readFile}, calls: {Tool_2})

Server_B (capabilities: {executeSQL})
  └── Tool_2 (provides: {executeSQL})
```

在此反例中，`Tool_1` 调用了 `Server_B` 的 `Tool_2`，而 `Server_A` 并未声明 `executeSQL` 能力。这意味着 Agent 通过 `Server_A` 间接获得了数据库执行权限，构成了**能力越权（Capability Escalation）**。这与 CIS MCP Companion Guide (April 2026) 中提出的"per-tool authorization"控制要求直接冲突。

---

## 6. 与功能架构复用的交叉引用

- `05-functional-architecture-reuse/06-mcp-a2a-protocols/mcp-tool-design.md`：定义了 MCP Tool 的七元组结构和 SOLID-T 设计原则。Alloy 规约中的 `CapabilityClosure` 是 SOLID-T 中 "Interface Cohesion" 和 "Deterministic Defaults" 在形式化层面的保障。
- `05-functional-architecture-reuse/06-mcp-a2a-protocols/protocol-analysis.md`：分析了 MCP 的 JSON-RPC 传输和安全边界。本 Alloy 规约假设传输层已完成认证，专注于应用层的结构约束。
- `01-meta-model-standards/06-formal-axioms/axiom-system.md` 公理 S.3（Dependency Transitivity of Trust）：信任在依赖链上传递。MCP 工具调用链是这一公理的实例：若 Agent 信任 Server A，而 Server A 的工具调用了 Server B 的工具，则 Agent 间接信任 Server B。

---

## 7. 权威来源

1. Jackson, D. (2012). *Software Abstractions: Logic, Language, and Analysis* (Revised ed.). MIT Press. —— Alloy 建模方法论。
2. Anthropic / Linux Foundation Agentic AI Foundation. (2025). *Model Context Protocol Specification* (2025-11-25). <https://modelcontextprotocol.io/specification/2025-11-25> —— MCP 工具能力模型与资源抽象。
3. Repello. (2026). *CIS MCP Companion Guide* (April 2026). —— MCP 企业部署的 per-tool authorization 与域级网络控制。
4. Jamshidi et al. (2025). "Sealing the Audit–Runtime Gap for LLM Skills." *arXiv:2603.00195* —— MCP 包签名与能力治理的形式化分析。

---

> 最后更新: 2026-06-06
