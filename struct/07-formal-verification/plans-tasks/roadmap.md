# 07 形式化验证 — 推进路线图

> **版本**: 2026-06-06
> **状态**: 基础文档已创建，案例库待扩充

---

## 当前进度

- [x] 01-tla-plus 目录结构
- [x] 02-alloy 目录结构
- [x] 03-coq-isabelle 目录结构（含 Coq `.v` 示例与 Isabelle `.thy` 理论）
- [x] 04-rust-type-system 目录结构
- [x] 05-spark-ada 目录结构
- [x] 06-b-method 目录结构
- [x] 09-comparative-matrices 目录结构
- [x] Rust 形式化语义初稿
- [x] TLA+ 案例库（T06-T08 已完成，T09-T10 跨主题交付于工业 IoT）
- [x] Alloy 架构约束案例（T11-T14 已完成）
- [x] SPARK/Ada 飞控案例（Phase 2 已完成）
- [x] B Method 铁路信号案例（Phase 2 已完成）

---

## Phase 1: Rust 类型系统深化（当前优先级最高）

**任务**:

- [x] T01: Rust 所有权-借用-生命周期形式化定义
- [x] T02: Trait 系统复用机制分析
- [x] T03: Cargo 依赖解析的 SAT 求解详细说明
  - 负责人: 写作代理
  - 验收: 含 PubGrub 算法伪代码
- [x] T04: Rust Polonius 借用检查器 vs NLL 对比
  - 负责人: 写作代理
  - 验收: 含 NLL 无法通过但 Polonius 可以通过的代码示例
- [x] T05: unsafe 边界的验证策略
  - 负责人: 写作代理
  - 验收: 含 Miri/Kani/Prusti 工具链对比

**交付物**:

- `04-rust-type-system/cargo-sat-resolution.md`
- `04-rust-type-system/polonius-vs-nll.md`
- `04-rust-type-system/unsafe-verification.md`

---

## Phase 2: TLA+ 案例库

**任务**:

- [x] T06: 分布式支付服务组件的 TLA+ 规约（来自 view/）
- [x] T07: MCP Server 能力协商协议的 TLA+ 规约
- [x] T08: A2A（Agent-to-Agent Protocol） Task 状态机的 TLA+ 规约
- [x] T09: OPC UA FX Connection Manager 的 TLA+ 规约（跨主题交付于 `11-industrial-iot-otit/02-opc-ua-fx/connection-manager/tla-specification.tla`）
- [x] T10: PLCopen MC_Power / MC_MoveAbsolute 的 TLA+ 规约（跨主题交付于 `11-industrial-iot-otit/04-plcopen-motion/plcopen-motion.tla`）

**交付物**:

- `01-tla-plus/case-library.md`
- `01-tla-plus/mcp-capability-negotiation.tla`
- `01-tla-plus/a2a-task-lifecycle.tla`
- `11-industrial-iot-otit/02-opc-ua-fx/connection-manager/tla-specification.tla`（跨主题）
- `11-industrial-iot-otit/04-plcopen-motion/plcopen-motion.tla`（跨主题）

---

## Phase 3: Alloy 架构约束

**任务**:

- [x] T11: 组件依赖无环性验证（来自 view/）
- [x] T12: MCP Tool 能力依赖图验证
- [x] T13: 跨层复用映射的约束验证
- [x] T14: ISA-95 资源层次一致性验证

**交付物**:

- `02-alloy/component-dependency.als`
- `02-alloy/mcp-tool-graph.als`
- `02-alloy/cross-layer-mapping.als`
- `02-alloy/isa95-hierarchy.als`

---

## Phase 4: 高安全等级形式化（2026-Q4）

**任务**:

- [x] T15: SPARK/Ada 飞控软件契约验证案例
- [x] T16: DO-178C MC/DC 形式化定义
- [x] T17: B Method 铁路信号系统精化链
- [x] T18a: Coq/Isabelle 教学示例（插入排序、有界计数器、旋转门）— 已完成
- [ ] T18b: Coq/Isabelle 安全关键组件定理证明（如 seL4/CompCert 风格）— Phase 2 2026-Q4

**交付物**:

- `05-spark-ada/flight-control-contracts.md`
- `05-spark-ada/mcdc-formalization.md`
- `06-b-method/railway-signaling-refinement.md`

---

## 依赖关系

```
T01-T02 (Rust 基础) → T03-T05 (Rust 深化)
    ↓
T06-T10 (TLA+ 案例) ─┐
T11-T14 (Alloy 案例)─┼→ T15-T18 (高安全等级)
                    │
T03-T05 (Rust) ──────┘
```

---

> 最后更新: 2026-06-10
