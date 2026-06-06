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

- **增加故障模型**：在支付服务中引入拜占庭故障节点；在 MCP 协商中引入消息丢失和乱序；
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

## 参考文献

[^1]: Lamport, L. (2002). *Specifying Systems: The TLA+ Language and Tools for Hardware and Software Engineers*. Addison-Wesley.

[^2]: Newcombe, C., Rath, T., Zhang, F., Munteanu, B., Brooker, M., & Deardeuff, M. (2015). How Amazon Web Services Uses Formal Methods. *Communications of the ACM*, 58(4), 66-73.
