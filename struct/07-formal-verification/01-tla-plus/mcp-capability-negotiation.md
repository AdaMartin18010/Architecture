# T07: MCP Server 能力协商协议的 TLA+ 规约说明

## 1. 规约背景与动机

Model Context Protocol（MCP）是由 Anthropic 于 2024 年 11 月发布、现由 Linux Foundation Agentic AI Foundation 治理的开放标准[^5]。它定义了 AI 应用（Client）与外部工具/数据源（Server）之间的通信协议，使用 JSON-RPC 2.0 作为底层传输格式。MCP 的核心创新之一在于其**能力协商（Capability Negotiation）**机制：在会话建立阶段，Client 和 Server 必须交换各自支持的能力集合（如 `tools`、`resources`、`prompts`、`sampling` 等），并仅激活双方共同支持的功能子集。

能力协商的正确性至关重要。如果一个 Server 声明支持 `resources/subscribe`，但 Client 并未在初始化请求中声明 `resources` 能力，那么后续对 `resources/subscribe` 的调用将导致协议违规。更严重的是，如果协商进入 `Active` 状态但双方对共同能力的认知不一致，可能导致消息路由失败或安全策略绕过。因此，我们需要形式化规约来验证：

1. `Active` 状态时，双方的能力交集非空；
2. 协议版本在激活时达成一致；
3. 在网络正常的情况下，协商过程必然收敛到 `Active` 或 `Terminated`。

本规约 `mcp-capability-negotiation.tla` 正是为此目的而建。

## 2. 状态机设计直觉

### 2.1 双端状态机

MCP 的能力协商涉及两个独立的参与者：Client 和 Server。因此，我们的规约维护两个状态变量 `clientState` 和 `serverState`，分别追踪各自的生命周期：

| Client 状态 | Server 状态 | 语义 |
|-------------|-------------|------|
| `disconnected` | `disconnected` | 初始状态，未建立连接 |
| `initializing` | `initializing` | 已发送/收到 `initialize` 消息 |
| `negotiating` | `negotiating` | 正在交换能力集合和协议版本 |
| `active` | `active` | 协商成功，会话正式建立 |
| `terminated` | `terminated` | 连接正常关闭 |
| `error` | `error` | 网络故障或协商失败 |

### 2.2 消息队列抽象

为了精确建模 JSON-RPC 2.0 的请求-响应语义，我们引入了一个 FIFO 消息队列 `messageQueue`。每条消息是一个记录（record），包含 `type`（消息类型）、`caps`（能力集合）和 `version`（协议版本）三个字段。这一抽象直接对应 Lamport 在 *Specifying Systems* 第 8 章中讨论的"基于消息队列的分布式系统建模"方法[^2]。

消息类型的序列在成功的协商流程中为：

```
Client: init ──► Server: init_ack ──► Client: negotiate ──► Server: negotiate_ack ──► Client: active
                                                              (Server 同步进入 active)
```

### 2.3 关键设计决策

**决策 1：协议版本的降级策略**

在 `ClientReceiveInitAck` 动作中，当 Client 请求的协议版本与 Server 响应的版本不一致时，我们采用了一个简化的降级策略：从双方版本中非确定性地选择一个（`CHOOSE v ∈ {clientVersion, Head(messageQueue).version} : TRUE`）。这与 MCP 2025-03-26 规范中的"exact-match negotiation"语义一致：双方必须就单一版本达成一致才能继续[^5]。在 TLC 模型中，非确定性选择会被穷举为所有可能版本，从而验证版本协商的完备性。

**决策 2：网络故障的显式建模**

`NetworkFailure` 动作将 `networkStatus` 从 `"up"` 翻转为 `"down"`，并将处于协商中间状态的 Client/Server 转移至 `error` 状态。这对应了分布式系统中常见的"网络分区导致半开连接"问题。正如 Hillel Wayne 在 *Practical TLA+* 第 8 章中所建议的，"显式建模故障是发现系统脆弱性的最有效方式"[^3]。

**决策 3：有限重试机制**

`ClientRetry` 动作允许 Client 在 `error` 状态下进行有限次数的重试（受 `MaxRetries` 约束）。这模拟了现实 MCP 客户端中的指数退避重连逻辑，同时也防止了模型中出现无限重试导致的活性反例。

## 3. 不变量详解

### 3.1 ActiveImpliesCommonCaps（Active 状态必须有共同能力）

这是本规约的核心安全性质，直接翻译了 MCP 规范的语义要求：

```
(clientState = "active" ∧ serverState = "active") ⇒ agreedCaps ≠ {}
```

该不变量通过以下机制得到保证：

1. `ClientReceiveInitAck` 计算 `agreedCaps = clientCaps ∩ Head(messageQueue).caps`；
2. `ClientActivate` 的前置条件要求 `agreedCaps ≠ {}`；
3. `ServerActivate` 仅在 `clientState = "active"` 时触发，确保双端同步进入 `active`。

如果设计者错误地移除了 `ClientActivate` 中的 `agreedCaps ≠ {}` 守卫，TLC 将立即给出反例：一个 Client 和 Server 声明了完全不相交的能力集合，但错误地进入了 `active` 状态。

### 3.2 ConsistentProtocolVersion（一致的协议版本）

```
(clientState = "active" ∧ serverState = "active") ⇒ agreedVersion ∈ ProtocolVersions
```

该不变量确保激活状态下的协议版本不是占位符 `"none"`，且属于双方支持的版本集合。这防止了由于版本协商失败导致的协议兼容性问题。

### 3.3 NegotiationSubset（协商子集关系）

```
agreedCaps ⊆ clientCaps ∧ agreedCaps ⊆ serverCaps
```

这是一个结构性不变量，确保 `agreedCaps` 始终是双方声明能力的子集。它作为冗余检查，保护模型免受意外赋值错误的破坏。

### 3.4 ErrorImpliesNetworkDown（错误状态的归因）

```
(clientState = "error" ∧ serverState = "error") ⇒ networkStatus = "down"
```

该不变量形式化了一个重要的诊断性质：协商进入错误状态的唯一原因是网络不可用。如果双方能力无交集，规范要求进入 `terminated` 状态而非 `error` 状态。这在实际工程中对应运维告警的根因分析逻辑：区分"网络故障"与"能力不匹配"两类场景。

## 4. 活性详解

### 4.1 EventuallyActive（最终到达 Active）

```
(networkStatus = "up" ∧ clientCaps ∩ serverCaps ≠ {}) ~>
    (clientState = "active" ∧ serverState = "active")
```

该性质的直觉是："如果网络正常且双方至少有一个共同能力，那么协商最终必然成功"。弱公平性假设 `WF` 保证了 `ClientReceiveInitAck`、`ServerReceiveNegotiate`、`ClientActivate` 和 `ServerActivate` 这些关键动作在可用时不会被无限期延迟。

### 4.2 EventuallyTerminatedOrError（最终到达终止或错误）

```
(networkStatus = "down" ∨ clientCaps ∩ serverCaps = {}) ~>
    (clientState ∈ {"terminated", "error"} ∧ serverState ∈ {"terminated", "error"})
```

该性质刻画了协商的"收敛性"：即使在不利条件下，系统也不会无限期地停留在中间状态（如 `initializing` 或 `negotiating`），而是最终进入明确的终止或错误状态。这对于资源管理和连接池回收至关重要。

## 5. 与 MCP 规范的对应关系

本规约严格对应 MCP 2025-03-26 规范中的初始化流程[^6]：

| 规约动作 | MCP 规范对应 | JSON-RPC 方法 |
|----------|-------------|---------------|
| `ClientConnect` | Client 发送 initialize 请求 | `initialize` |
| `ServerRespondInit` | Server 返回 initialize 结果 | `initialize` response |
| `ClientReceiveInitAck` | Client 处理 Server 能力，计算交集 | 内部状态转移 |
| `ServerReceiveNegotiate` | Server 确认协商结果 | `notifications/initialized` |
| `ClientActivate` | 会话进入可操作状态 | 内部状态转移 |

这种一一对应关系使得本规约不仅是一个数学模型，更是 MCP 实现者的**可执行参考文档**。

## 6. TLC 模型检查建议

- `AllCapabilities <- {"tools", "resources", "prompts"}`：覆盖 MCP 三大核心原语
- `ProtocolVersions <- {"2025-03-26"}`：聚焦单一版本，避免组合爆炸
- `MaxRetries <- 2`：有限重试足以覆盖重试逻辑的正确性

TLC 将穷举所有可能的能力声明组合（Client 和 Server 各声明 `2^3 - 1 = 7` 种非空能力子集），验证所有安全不变量和活性性质。对于不相交的能力集合（如 Client 只声明 `tools`，Server 只声明 `prompts`），规约正确地阻止了进入 `active` 状态。

## 7. 参考文献

[^2]: Lamport, L. (2002). *Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers*. Addison-Wesley.

[^3]: Wayne, H. (2018). *Practical TLA+: Planning Driven Development*. Apress.

[^5]: Model Context Protocol Specification. (2025-11-25). *Model Context Protocol*. <https://modelcontextprotocol.io/specification/2025-11-25>

[^6]: Model Context Protocol Specification. (2025-03-26). *Initialization Flow*. <https://modelcontextprotocol.io/specification/2025-03-26/basic/lifecycle/#initialization>


---

## 补充说明：T07: MCP Server 能力协商协议的 TLA+ 规约说明

## 概念定义

**定义**：TLA+（Temporal Logic of Actions）是由 Leslie Lamport 提出的规约语言，通过状态、动作与时不变量描述并发与分布式系统行为，常用于验证算法与架构设计的正确性。

## 示例

**示例**：使用 TLA+ 规约两阶段提交协议，定义协调者、参与者的状态机与“所有节点最终一致”的不变式，TLC 模型检验器穷举状态空间并确认无死锁与活锁。

## 反例

**反例**：一个分布式缓存系统未对“网络分区+节点失效”场景建模，上线后在真实分区下丢失写入，因为自然语言需求遗漏了边界条件。

## 权威来源

> **权威来源**:
>
> - [TLA+ Home Page](https://lamport.azurewebsites.net/tla/tla.html)
> - [Specifying Systems](https://lamport.azurewebsites.net/tla/book.html)
> - 核查日期：2026-07-07
