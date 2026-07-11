# T08: A2A Task 状态机的 TLA+ 规约说明

## 1. 概念定义

**TLA+**（Temporal Logic of Actions）是由 Leslie Lamport 提出的规约语言，通过状态、动作与时序不变量描述并发与分布式系统行为，常用于验证算法与架构设计的正确性。

**A2A Task 生命周期** 是 Agent-to-Agent 协议的核心语义骨架，定义了 Task 从提交到终止的合法状态转移及消息交互约束。

## 2. 规约背景与动机

Agent-to-Agent（A2A）协议是由 Google 于 2025 年 4 月发起、现由 Linux Foundation 维护的开放标准，旨在实现 AI Agent 之间的互操作通信[^7]。与 MCP（Model Context Protocol）解决"Agent ↔ Tool"的垂直集成问题不同，A2A 聚焦于"Agent ↔ Agent"的水平协作问题。A2A v1.0.0.0.0.0 规范（2026 年 3 月正式发布）定义了一个精细的任务生命周期（Task Lifecycle）状态机，这是协议的核心语义骨架[^8]。

Task 生命周期之所以需要形式化验证，原因在于：

1. **长时间运行（Long-running）**：Agent 任务可能持续数分钟甚至数小时（如代码审查、安全审计），期间涉及多次消息往返；
2. **人机协同（Human-in-the-loop）**：`input_required` 状态允许 Agent 暂停执行并向人类用户请求澄清，这使得状态机不再是简单的线性流程；
3. **资源管理**：处于终止状态（`completed`/`failed`/`canceled`）的 Task 必须释放其占用的消息通道和 Artifact 引用，否则将导致资源泄漏。

本规约 `a2a-task-lifecycle.tla` 对 A2A Task 状态机进行形式化建模，验证其安全性质（终止状态无消息交互、completed 必有 Artifact）和活性性质（working 最终必须终止）。

## 3. 状态机设计直觉

### 3.1 Task 状态全集

A2A v1.0 规范定义了以下状态[^8]：

| 状态 | 语义 | 允许转移 |
|------|------|----------|
| `submitted` | Task 已创建，等待 Server Agent 处理 | `working`, `canceled` |
| `working` | Server Agent 正在积极处理 | `input_required`, `completed`, `failed`, `canceled` |
| `input_required` | 需要额外输入才能继续 | `working`, `canceled`, `failed` |
| `completed` | 成功完成（终止状态） | 无 |
| `failed` | 处理失败（终止状态） | 无 |
| `canceled` | 被 Client 取消（终止状态） | 无 |

值得注意的是，A2A v1.0.0.0.0.0 还定义了 `auth_required` 和 `rejected` 状态，本规约出于简化考虑聚焦于最核心六态模型，但其扩展至八态模型在结构上完全同质。

### 3.2 消息与 Artifact 模型

A2A 协议中，Task 不仅是一个状态机，还是一个消息容器。每个 Task 附带一个消息序列（`taskMessages`），记录 Client 与 Server Agent 之间的所有交互。同时，Task 在 `completed` 状态下必须包含至少一个 Artifact——这是 A2A 与简单 RPC 调用的本质区别：Agent 协作的产出是可交付物（Artifact），而非仅仅是返回值。

本规约使用 TLA+ 的 `Sequences` 模块来建模消息历史，`SUBSET Artifacts` 来建模 Artifact 集合。`taskStepCount` 变量则用于实现超时机制：当 Task 在非终止状态停留超过 `TimeoutThreshold` 步时，系统自动将其转移至 `failed`。

### 3.3 关键设计决策

**决策 1：Agent 角色的显式建模**

`taskOwner` 变量将每个 Task 绑定到一个特定的 Server Agent。这与 A2A 规范中"Task 由特定 Agent 负责处理"的语义一致。`StartWork`、`RequestInput`、`CompleteTask` 等动作均检查 `taskOwner[t] = agent`，确保只有责任 Agent 才能推进 Task 状态。

**决策 2：超时作为活性保证手段**

`TimeoutTask` 动作是活性性质 `WorkingEventuallyTerminates` 的关键支撑。在没有超时机制的情况下，一个恶意或故障的 Server Agent 可以无限期地将 Task 停留在 `working` 状态，从而违反活性。通过引入 `taskStepCount` 和 `TimeoutThreshold`，我们形式化地保证了"无论 Agent 行为如何，Task 最终都会到达终止状态"。这一设计在工业系统中对应 Kubernetes 的 Job TTL、AWS Step Functions 的 Timeout 等机制。

**决策 3：消息类型的细粒度区分**

`taskMessages` 中的每条消息包含 `type`、`from` 和 `to` 字段，覆盖了 A2A 规范中的核心交互原语：`send`（Client 提交 Task）、`request_input`（Agent 请求输入）、`provide_input`（Client 提供输入）、`complete`/`fail`/`cancel`（状态转移通知）。这种细粒度建模使得我们能够验证"终止状态下不再有消息交互"这一安全性质。

## 4. 不变量详解

### 4.1 TerminalNoMessages（终止状态无消息增长）

```
∀ t ∈ Tasks : taskState[t] ∈ TerminalStates ⇒ taskStepCount[t] ≤ TimeoutThreshold + 1
```

该不变量的直接形式化较为困难（因为 TLA+ 的下一个状态由 `Next` 定义），因此我们采用了一个间接策略：通过限制终止状态下的 `taskStepCount` 上界，结合 `Next` 中所有动作的前置条件要求 `taskState[t] ∈ NonTerminalStates`，来确保终止状态不会被任何动作再次修改。这一技巧在 *Specifying Systems* 第 4 章的"递增计数器"示例中有类似应用[^2]。

更强的版本 `CompletedLastMessageIsComplete` 进一步要求：`completed` 状态的消息序列末尾必须是 `complete` 类型的消息。这确保了状态转移与消息发送的原子性。

### 4.2 CompletedHasArtifact（completed 必须有 Artifact）

```
∀ t ∈ Tasks : taskState[t] = "completed" ⇒ taskArtifacts[t] ≠ {}
```

这是 A2A 规范中最具业务语义的安全性质。其保证机制在于：`CompleteTask` 动作的前置条件要求 `artifact ∈ Artifacts`，且其后置条件将该 Artifact 加入 `taskArtifacts[t]`。由于 `completed` 是终止状态，没有其他动作可以修改 `taskArtifacts`，因此该不变量一旦建立便永久保持。

如果实现者错误地在 `CompleteTask` 中使用了 `UNCHANGED taskArtifacts`，TLC 将给出反例轨迹：一个 Task 到达了 `completed` 状态但 `taskArtifacts` 为空。

### 4.3 NonTerminalHasMessages（非终止状态必有消息历史）

```
∀ t ∈ Tasks : taskState[t] ∈ {"working", "input_required"} ⇒ taskMessages[t] ≠ ⟨⟩
```

该不变量确保状态推进与消息发送的同步性：任何处于 `working` 或 `input_required` 状态的 Task，必然已经经历过至少一次消息交互（`StartWork`、`RequestInput` 或 `ProvideInput`）。这作为一个"防护网"，阻止由于规约编写错误导致的"无消息状态转移"。这一模式在 TLA+ Examples 仓库的多个基于消息的状态机规约中被采用[^4]。

### 4.4 FailedCanceledNoArtifacts（失败和取消状态 Artifact 为空）

```
∀ t ∈ Tasks : taskState[t] ∈ {"failed", "canceled"} ⇒ taskArtifacts[t] = {}
```

该不变量确保资源清理的完整性：失败的 Task 不应保留中间产物，取消的 Task 应回滚所有已生成 Artifact。这在实际工程中对应临时文件的清理、数据库事务的回滚等机制。

## 5. 活性详解

### 5.1 WorkingEventuallyTerminates（working 最终终止）

```
∀ t ∈ Tasks : (taskState[t] = "working") ~> (taskState[t] ∈ TerminalStates)
```

这是本规约的核心活性性质，对应 A2A 规范中的"Task 必须最终完成或失败"要求。其成立依赖于以下因素：

1. `CompleteTask` 和 `FailTask` 动作可以将 `working` 直接转移至 `completed` 或 `failed`；
2. `CancelTask` 动作允许 Client 从任意非终止状态取消 Task；
3. `TimeoutTask` 动作提供了最终的"保险丝"：即使 Server Agent 完全不响应，Task 也会在 `TimeoutThreshold` 步后强制失败。

弱公平性假设 `WF` 保证了 `CompleteTask`、`FailTask`、`CancelTask` 和 `TimeoutTask` 在持续可用时最终会被执行。这与 Leslie Lamport 在 TLA+ Video Course 中强调的"活性必须由公平性支撑"原则一致[^2]。

### 5.2 InputRequiredEventuallyResolved（input_required 最终解决）

```
∀ t ∈ Tasks : (taskState[t] = "input_required") ~>
    (taskState[t] ∈ TerminalStates ∨ taskState[t] = "working")
```

该性质刻画了人机协同场景下的进展性：Agent 请求输入后，要么收到输入并恢复工作，要么 Task 被取消/超时。这防止了"Agent 提出问题后永久等待"的僵局。

## 6. 正向示例：验证 A2A Task 活性

### 示例

对 `a2a-task-lifecycle.tla` 运行 TLC，配置 `TimeoutThreshold <- 10`、`Tasks <- {t1, t2}`、`Agents <- {client, server}`，验证 `WorkingEventuallyTerminates` 活性性质。TLC 会穷举两个 Task 在双角色 Agent 下的所有交错执行，确认：

- 无论 Server Agent 是否主动推进，`TimeoutTask` 都能保证 Task 在 10 步内进入终止状态；
- `completed` 状态的 Task 始终携带 Artifact；
- 终止状态后不再有消息追加。

该验证结果可直接用于 A2A Server 实现的回归测试基线。

## 7. 反例 / 反模式：遗漏超时导致活锁

### 反例

假设实现者认为"正常流程下 Agent 总会完成任务"，从而省略 `TimeoutTask` 动作或设置过长超时。TLC 将给出如下活性反例：

```
taskState[t1] = "working"  // 无限期保持，无 CompleteTask/FailTask/CancelTask 发生
```

在真实 A2A 部署中，这种遗漏会导致：

- 长时间运行的 Task 占用消息通道和 Artifact 引用；
- 人机协同场景下，Agent 请求输入后 Client 掉线，Task 永久挂起；
- 资源泄漏逐渐累积，最终触发服务降级或 OOM。

该反例说明：自然语言需求中的"最终完成"必须形式化为带公平性约束和超时保险的活性性质，否则无法排除恶意或故障 Agent 的拒绝服务行为。

## 8. 与 A2A v1.0 规范的对应关系

本规约与 A2A v1.0.0.0.0.0 规范的对应如下[^8]：

| 规约动作/变量 | A2A 规范对应 | 说明 |
|---------------|-------------|------|
| `taskState` | Task.status | 核心状态字段 |
| `taskMessages` | Task.messages | 消息历史数组 |
| `taskArtifacts` | Task.artifacts | 输出产物集合 |
| `StartWork` | `tasks/send` → `working` | Client 发送 Task |
| `RequestInput` | `input-required` 状态转移 | Agent 暂停请求输入 |
| `ProvideInput` | Client 回复 → `working` | 输入提供后恢复 |
| `CompleteTask` | `completed` + Artifacts | 任务完成交付 |
| `CancelTask` | `tasks/cancel` | 显式取消 |

特别地，A2A 规范中的 `contextId`（用于将多个相关 Task 分组到同一会话）在本规约的简化模型中未显式建模，但可以通过扩展 `taskOwner` 为 `taskContext` 轻松添加。

## 9. TLC 模型检查建议

- `Tasks <- {t1, t2}`：2 个并发 Task，覆盖交错执行
- `Agents <- {client, server}`：简化双角色模型
- `Artifacts <- {art1, art2}`：有限 Artifact 集合
- `TimeoutThreshold <- 10`：较短超时，加速状态空间搜索
- `MaxMessages <- 5`：限制消息序列长度，控制状态空间

TLC 将验证所有安全不变量和活性性质。若实现者意外允许从 `completed` 状态再次发送消息，TLC 将通过 `ValidStateTransitions` 立即发现该违规。

## 10. 标准条款与工具映射

| 标准 / 条款 | 本规约对应内容 | 工具 | 证据 |
|:---|:---|:---|:---|
| IEEE 1012-2024 §9.3（软件设计 V&V） | Task 状态机设计验证 | TLA+ / TLC | 不变量与活性报告 |
| IEEE 1012-2024 §9.5（软件实现 V&V） | 状态转移与消息一致性 | TLAPS（可选） | 形式化证明 |
| DO-333 §6.3.2（形式化分析替代测试） | 状态机活性穷举 | TLC 模型检验 | 模型检查报告 |
| A2A v1.0 Task Lifecycle | 协议语义形式化 | TLA+ Toolbox | 可执行参考文档 |

## 11. 参考文献

[^2]: Lamport, L. (2002). *Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers*. Addison-Wesley. <https://lamport.azurewebsites.net/tla/book.html>

[^4]: TLA+ Examples Repository. <https://github.com/tlaplus/Examples>

[^7]: PickAxe. (2026). *MCP vs A2A Protocol: What AI Agent Builders Actually Need to Know in 2026*. <https://pickaxe.co/post/mcp-vs-a2a-protocol>

[^8]: Google A2A Protocol. *Agent-to-Agent Protocol*. <https://a2a-protocol.org/latest/>

## 12. 权威来源

| 来源 | URL | 核查日期 |
|:---|:---|:---|
| TLA+ Home Page (Leslie Lamport) | <https://lamport.azurewebsites.net/tla/tla.html> | 2026-07-08 |
| *Specifying Systems* (Lamport) | <https://lamport.azurewebsites.net/tla/book.html> | 2026-07-08 |
| TLA+ Examples Repository | <https://github.com/tlaplus/Examples> | 2026-07-08 |
| Google A2A Protocol | <https://a2a-protocol.org/latest/> | 2026-07-08 |
| A2A v1.0 Task Lifecycle | <https://a2a-protocol.org/latest/topics/life-of-a-task> | 2026-07-08 |

## 13. 交叉引用

- MCP 能力协商 TLA+ 规约：[`mcp-capability-negotiation.md`](./mcp-capability-negotiation.md)
- A2A / MCP 协议对比分析：[`protocol-analysis.md`](../../05-functional-architecture-reuse/06-mcp-a2a-protocols/protocol-analysis.md)
- 形式化验证总览：[`struct/07-formal-verification/README.md`](../README.md)

> 最后更新：2026-07-08