# TLA+ 案例库总览

> **Track**: 07 形式化验证 — Phase 2: TLA+ 案例库
> **创建日期**: 2026-06-06
> **状态**: 初始案例已完成（T06–T08），T10 工业控制案例已完成（2026-06-第4周）

---

## 1. 案例库定位

本案例库是软件工程架构复用知识体系中 **形式化验证（Formal Verification）** 轨道的核心交付物之一。TLA+（Temporal Logic of Actions）由图灵奖得主 Leslie Lamport 于 1999 年设计，是工业界验证分布式系统并发行为的首选形式化语言[^1]。Amazon Web Services、Microsoft Azure、MongoDB、CockroachDB 等企业已在其关键系统的设计阶段引入 TLA+，在生产事故之前捕获边界条件缺陷[^2]。

本案例库遵循 **"从协议到规约"（Protocol-to-Specification）** 的方法论：选取软件架构复用中高频出现的分布式协议与状态机，将其精确翻译为 TLA+ 规约，并通过不变量（Safety）和活性（Liveness）性质验证其设计正确性。

---

## 2. 案例索引

### 2.1 已完成的初始案例

| 编号 | 案例名称 | 规约文件 | 说明文档 | 核心状态机 | 不变量数 | 活性数 |
|------|----------|----------|----------|------------|----------|--------|
| T06 | 分布式支付服务组件 | `payment-service.tla` | `payment-service.md` | Idle → Reserved → Committed/Aborted | 5 | 1 |
| T07 | MCP Server 能力协商协议 | `mcp-capability-negotiation.tla` | `mcp-capability-negotiation.md` | Disconnected → Initializing → Negotiating → Active → Terminated | 5 | 2 |
| T08 | A2A Task 状态机 | `a2a-task-lifecycle.tla` | `a2a-task-lifecycle.md` | submitted → working → input-required → completed/failed/canceled | 5 | 2 |
| **T10** | **PLCopen MC_Power / MC_MoveAbsolute** | **`plcopen-motion.tla`** | **`tla-verification.md`** | **Disabled→Enabling→Standstill→ErrorStop; Idle→Busy→Active→Done/Error** | **5** | **3** |

### 2.2 待完成的后续案例

| 编号 | 案例名称 | 状态机特征 | 计划完成时间 |
|------|----------|------------|--------------|
| T09 | OPC UA FX Connection Manager | 工业以太网连接管理状态机（Closing → Opening → Operational → Aborting） | 2026-Q3 |

---

## 3. 案例共同特征

### 3.1 规约结构模板

所有案例遵循统一的 TLA+ 规约结构，便于阅读者快速定位关键部分：

```
MODULE <case_name>
  ├── 模块级注释：案例背景、状态机概览、性质清单
  ├── EXTENDS：导入的 TLA+ 标准模块
  ├── CONSTANTS：可配置的常量参数
  ├── ASSUME：常量约束假设
  ├── VARIABLES：状态变量声明
  ├── 辅助定义（辅助函数、集合构造）
  ├── TypeOK：类型正确性不变量
  ├── Init：初始状态谓词
  ├── 状态转移动作（A1, A2, ...）
  ├── Next：下一步关系（所有动作的析取）
  ├── 不变量（Safety Properties, I1, I2, ...）
  ├── 活性（Liveness Properties, L1, L2, ...）
  ├── Fairness：公平性假设
  └── Spec：完整规约公式
```

### 3.2 不变量设计原则

每个案例至少包含两类不变量：

1. **结构性不变量（Structural Invariants）**：确保状态变量始终处于合法取值范围，如 `TypeOK`、`ValidStateTransitions`；
2. **语义性不变量（Semantic Invariants）**：确保系统满足业务层面的安全性质，如 `FundConservation`、`CompletedHasArtifact`。

### 3.3 活性设计原则

每个案例至少包含一个 leads-to（`~>`）形式的活性性质，表达"如果某个条件持续成立，那么某个目标状态最终必然到达"。活性性质的成立依赖于弱公平性（Weak Fairness, `WF`）假设，这是 TLA+ 中从 Safety 推导 Liveness 的标准技术[^1]。

---

## 4. 权威来源引用

本案例库在规约设计和说明文档中引用了以下权威来源：

| 来源 | 作者/机构 | 引用场景 |
|------|----------|----------|
| *Specifying Systems* (2002) | Leslie Lamport, Microsoft Research | TLA+ 语法基础、状态机建模、公平性语义 |
| *Practical TLA+* (2018) | Hillel Wayne, Apress | 工程实践模式、PlusCal 对照、故障建模 |
| "How AWS Uses Formal Methods" (2015) | Newcombe et al., CACM | 工业级形式化验证动机、分布式系统缺陷案例 |
| MCP Specification (2025-03-26, 2025-11-25) | Anthropic / Linux Foundation | MCP 能力协商协议语义、JSON-RPC 消息格式 |
| A2A Protocol v1.0 (2026-03) | Google / Linux Foundation | A2A Task 生命周期、Agent Card 语义、Artifact 模型 |
| TLA+ Examples Repository | TLA+ Community, GitHub | Two-Phase Commit 规约参考、状态机模式复用 |

---

## 5. 使用指南

### 5.1 环境准备

建议使用以下工具链阅读和验证本案例库的 TLA+ 规约：

- **TLA+ Toolbox**：官方集成开发环境，支持 TLC 模型检查器和 TLAPS 证明系统
- **VS Code + TLA+ Nightly 扩展**：现代编辑器体验，语法高亮和错误提示
- **SANY**：TLA+ 语法检查器，可独立运行验证 `.tla` 文件的语法正确性

### 5.2 验证流程

对每个案例的验证遵循以下步骤：

1. **语法检查**：使用 SANY 确认 `.tla` 文件无语法错误；
2. **模型配置**：在 TLC 中配置常量赋值（如 `Accounts <- {a1, a2, a3}`）；
3. **不变量检查**：将所有 `*Inv` 和 `*Implies*` 谓词加入 Invariants 列表；
4. **活性检查**：将所有 `*Eventually*` 和 leads-to 性质加入 Properties 列表；
5. **状态空间分析**：观察 TLC 报告的 Distinct States 和 Diameter，评估模型复杂度。

### 5.3 扩展路径

读者可基于本案例库的模板，对以下方向进行扩展：

- **增加故障模型**：在支付服务中引入拜占庭故障节点；在 MCP（Model Context Protocol） 协商中引入消息丢失和乱序；
- **参数化验证**：使用 Apalache 符号模型检查器处理更大参数空间；
- **精化验证（Refinement）**：将 TLA+ 规约精化为 PlusCal 算法，再进一步精化为可执行代码。

---

## 6. 与知识体系其他主题的关联

```
07-formal-verification/01-tla-plus/
    ├── 向上关联：03-application-architecture-reuse（微服务编排的形式化验证）
    ├── 横向关联：04-component-architecture-reuse/（Rust 组件的并发安全验证）
    ├── 向下关联：11-industrial-iot-otit/（OPC UA / PLCopen 的形式化语义）
    └── 方法关联：02-alloy/（架构约束的声明式验证，与 TLA+ 的行为式验证互补）
```

---

> **维护说明**：本案例库随 Phase 2 推进持续扩充。每新增一个案例，需同步更新本总览的"案例索引"表格，并确保规约文件通过 SANY 语法检查。

---

## 7. 每个案例的 Init / Next / Invariant / Property 规格速查

下表汇总 T06–T10 四个案例的初始状态谓词、下一步关系、核心不变量与活性性质，便于读者快速对照 `.tla` 文件进行 TLC 配置。

| 编号 | Init | Next | 核心不变量 (Safety) | 活性 (Liveness) |
|------|------|------|---------------------|-----------------|
| **T06** 支付服务 | `balances ∈ [Accounts→Nat]`，`reservedFunds = 0`，`txStatus = [tx↦"idle"]`，`initialTotalBalance = AccountBalanceTotal` | `∃ tx: CreateTx(tx,...) ∨ Commit(tx) ∨ Abort(tx) ∨ TimeoutAbort(tx)` | `FundConservationInv`、`NoDoubleSpending`、`CommittedBalanceCorrect`、`ReservedFundsConsistent`、`TypeOK` | `AllRequestsProcessed` |
| **T07** MCP 协商 | `clientState = serverState = "disconnected"`，`agreedCaps = {}`，`networkStatus = "up"`，`messageQueue = <<>>` | `ClientConnect ∨ ServerRespondInit ∨ ClientReceiveInitAck ∨ ServerReceiveNegotiate ∨ ClientActivate ∨ ServerActivate ∨ ClientTerminate ∨ ServerTerminate ∨ NetworkFailure ∨ ClientRetry` | `ActiveImpliesCommonCaps`、`ConsistentProtocolVersion`、`NegotiationSubset`、`ErrorImpliesNetworkDown`、`TerminatedImpliesNoCaps`、`TypeOK` | `EventuallyActive`、`EventuallyTerminatedOrError` |
| **T08** A2A Task | `taskState = [t↦"submitted"]`，`taskMessages = [t↦<<>>]`，`taskArtifacts = [t↦{}]`，`taskStepCount = [t↦0]` | `StartWork ∨ RequestInput ∨ ProvideInput ∨ CompleteTask ∨ FailTask ∨ CancelTask ∨ TimeoutTask` | `TerminalNoMessages`、`CompletedHasArtifact`、`NonTerminalHasMessages`、`InputRequiredImpliesPending`、`FailedCanceledNoArtifacts`、`CompletedLastMessageIsComplete`、`TypeOK` | `WorkingEventuallyTerminates`、`InputRequiredEventuallyResolved` |
| **T10** PLCopen 运动 | `powerState = [a↦"Disabled"]`，`moveState = [a↦"Idle"]`，`axisState = [a↦"Disabled"]`，`stepCount = [a↦0]`，所有输出标志为 `FALSE`，ErrorID 为 0 | `PowerEnableOn ∨ PowerEnableReady ∨ PowerEnableError ∨ PowerDisable ∨ PowerDisabled ∨ PowerAxisError ∨ PowerReset ∨ MoveStart ∨ MoveStartError ∨ MoveActivate ∨ MoveComplete ∨ MoveAbort ∨ MoveError ∨ MoveIdle ∨ IncrementStepCount` | `StandstillRequiredForMove`、`ErrorImpliesErrorID`、`PowerStatusConsistency`、`MoveOutputConsistency`、`NoInvalidTransition`、`TypeOK` | `BusyEventuallyTerminates`、`PowerEnableEventuallyStandstill`、`ActiveEventuallyTerminates` |

> **说明**：T10 的完整规约与验证说明位于 `struct/11-industrial-iot-otit/04-plcopen-motion/tla-verification.md`，本表仅提供与案例库索引对应的速查入口。

---

## 8. TLC 验证命令模板与预期结果

### 8.1 命令行调用模板

在使用 [TLA+ Toolbox](https://lamport.azurewebsites.net/tla/toolbox.html) 或命令行工具时，可按以下模板执行模型检查：

```bash
# 1. 语法检查（SANY）
java -cp tla2tools.jar tla2sany.SANY payment_service.tla

# 2. TLC 模型检查（以 T06 为例）
java -cp tla2tools.jar tlc2.TLC -deadlock -config payment_service.cfg payment_service.tla
```

其中 `.cfg` 文件示例（T06）：

```tla
CONSTANTS
    Accounts = {a1, a2, a3}
    TxIds = {tx1, tx2}
    MaxAmount = 5

INIT Init
NEXT Next

INVARIANTS
    TypeOK
    FundConservationInv
    NoDoubleSpending
    CommittedBalanceCorrect
    ReservedFundsConsistent

PROPERTIES
    AllRequestsProcessed
```

### 8.2 各案例推荐配置与预期输出

| 编号 | 常量赋值 | 预期状态数 | 预期结果 |
|------|----------|-----------|----------|
| **T06** | `Accounts={a1,a2,a3}, TxIds={tx1,tx2}, MaxAmount=5, balances=[a1|->10,a2|->10,a3|->10]` | 约 5×10⁴–2×10⁵ 个不同状态（取决于 TLC 优化） | 所有不变量与活性通过，`No error` |
| **T07** | `AllCapabilities={"tools","resources","prompts"}, ProtocolVersions={"2025-03-26"}, MaxRetries=2` | 约 1×10⁴–5×10⁴ 个不同状态 | 所有不变量与活性通过 |
| **T08** | `Tasks={t1,t2}, Agents={client,server}, Artifacts={art1,art2}, MaxMessages=5, TimeoutThreshold=10` | 约 1×10⁵–5×10⁵ 个不同状态 | 所有不变量与活性通过 |
| **T10** | `Axes={axis1}, MaxTimeoutSteps=5, ErrorIDs={0,0x8A01,0x8A02,0x9001}` | 约 890 个不同状态（单轴） | 所有不变量与活性通过 |

> **边界条件**：若 TLC 报告不变量违反，通常意味着：
>
> - 遗漏了动作中的状态更新（如 `Abort` 未退回资金）；
> - 前置条件过弱，允许非法状态转移；
> - 公平性假设缺失，导致活性反例。
> 反例轨迹（Error Trace）会精确给出从 `Init` 到违反状态的动作序列，这是形式化方法相较于随机测试的核心优势。

### 8.3 与 Wikipedia 及权威来源的链接

- [TLA+ - Wikipedia](https://en.wikipedia.org/wiki/TLA%2B)
- [Formal methods - Wikipedia](https://en.wikipedia.org/wiki/Formal_methods)
- Lamport, L. *Specifying Systems*. <https://lamport.azurewebsites.net/tla/book.html>
- TLA+ Examples Repository. <https://github.com/tlaplus/Examples>
- Newcombe et al. (2015). *How Amazon Web Services Uses Formal Methods*. <https://doi.org/10.1145/2699415>

---

## 9. 参考文献

[^1]: Lamport, L. (2002). *Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers*. Addison-Wesley.

[^2]: Newcombe, C., Rath, T., Zhang, F., Munteanu, B., Brooker, M., & Deardeuff, M. (2015). How Amazon Web Services Uses Formal Methods. *Communications of the ACM*, 58(4), 66-73.


---

## 补充说明：TLA+ 案例库总览

## 概念定义

**定义**：TLA+（Temporal Logic of Actions）是由 Leslie Lamport 提出的规约语言，通过状态、动作与时不变量描述并发与分布式系统行为，常用于验证算法与架构设计的正确性。

## 反例

**反例**：一个分布式缓存系统未对“网络分区+节点失效”场景建模，上线后在真实分区下丢失写入，因为自然语言需求遗漏了边界条件。

## 分析

**分析**：TLA+ 的价值在于暴露自然语言需求无法覆盖的并发边界，但建模抽象程度需要与验证目标匹配。


---

## 补充章节

## 权威来源

> **权威来源**:
>
> - [TLA+ Home Page](https://lamport.azurewebsites.net/tla/tla.html)
> - [Specifying Systems](https://lamport.azurewebsites.net/tla/book.html)
> - 核查日期：2026-07-07
