# 07 形式化验证 — 内容梳理报告

> **日期**: 2026-06-08
> **范围**: TLA+ / Alloy / Coq / Isabelle / Rust / SPARK-Ada / B Method
> **原则**: 内容梳理优先，不搭建运行环境

---

## 资产清单

| 工具/方法 | 文件数 | 主题覆盖 | 内容状态 | 权威来源对齐 |
|-----------|--------|----------|----------|-------------|
| **TLA+** | 7 | 支付服务 (T06)、MCP 能力协商 (T07)、A2A Task 生命周期 (T08) | 初始案例完整，跨主题 T09/T10 在 `11-industrial-iot-otit/` 中交付 | Lamport《Specifying Systems》、Wayne《Practical TLA+》、AWS CACM'15 |
| **Alloy** | 8 | 组件依赖无环 (T11)、MCP Tool 图 (T12)、跨层映射 (T13)、ISA-95 层次 (T14) | 全部完成，均有配套 `.als` + `.md` | Jackson《Software Abstractions》、ISO 42010:2022、ISA-95 |
| **Coq/Isabelle** | 6 | 插入排序、有界计数器、旋转门状态机 | 教学示例完成 (T18a)，安全关键组件证明 (T18b) 待启动 | Software Foundations、Isabelle AFP |
| **Rust 类型系统** | 9 | 形式化语义、Cargo SAT/PubGrub、Polonius vs NLL、工具链实践、unsafe 验证 | Phase 1 全部完成 (T01–T05) | Rust 1.85+、RustBelt (Iris)、Tree Borrows (PLDI'25)、Kani 0.66 |
| **SPARK-Ada** | 3 | 飞控契约验证、DO-178C MC/DC 形式化、工业复用实践 | Phase 2 已完成 (T15–T16) | DO-178C/DO-333、AdaCore SPARK Pro 24.x |
| **B Method** | 2 | Event-B 体系总览、铁路信号精化链 (T17) | Phase 2 已完成 | Abrial《The B-Book》《Modeling in Event-B》、CENELEC EN 50128 |
| **对比矩阵** | 1 | SPARK-Ada vs Rust 验证能力矩阵 | 已完成 | 综合上述来源 |
| **计划/根文档** | 2 | 推进路线图、根 README | 根 README 存在状态滞后 | — |

**跨主题交付物（不在本目录但在索引中引用）**:

- `11-industrial-iot-otit/02-opc-ua-fx/connection-manager/tla-specification.tla` — T09 OPC UA FX Connection Manager
- `11-industrial-iot-otit/04-plcopen-motion/plcopen-motion.tla` — T10 PLCopen MC_Power / MC_MoveAbsolute

---

## 内容校对发现

### 1. 文件缺失与目录不一致

| 问题 | 位置 | 详情 |
|------|------|------|
| **ci-workflows.md 缺失** | `03-coq-isabelle/README.md` 目录结构中列出 | 实际文件不存在；README 中描述的 Docker 验证流程无独立 CI 文档支撑 |
| **T10 本地文件缺失** | `01-tla-plus/case-library.md` 案例索引 | 索引声称 `plcopen-motion.tla` 与 `tla-verification.md` 位于 `01-tla-plus/`，但本地不存在；T10 规约实际在 `11-industrial-iot-otit/04-plcopen-motion/plcopen-motion.tla`，且**无对应说明文档** |
| **T09 本地无索引** | `01-tla-plus/case-library.md` | T09 规约仅在跨主题目录存在，`01-tla-plus/` 下无本地入口或链接说明 |

### 2. 版本号与前瞻性声明未区分

| 问题 | 位置 | 详情 |
|------|------|------|
| **Rust 1.93 前瞻性声明** | `04-rust-type-system/cargo-sat-resolution.md` §3 伪代码后 | 声称 "Rust 1.93 (2026) 的 PubGrub 实现增加了 MSRV 感知"，但对齐标准仅声明 Rust 1.85+；**Rust 1.93 在 2026-06-08 尚未发布**，文档未明确标注此为预测性内容 |
| **Polonius "2026 稳定化"预测** | `04-rust-type-system/polonius-vs-nll.md` §1、§6.2 | 声称 "Polonius Alpha (Rust 1.85+ nightly, 目标 2026 稳定化)"；Rust 1.85 已于 2025-02 发布，Polonius 截至本报告日仍在 nightly，**"2026 稳定化"是项目目标而非既成事实**，文档未加预测性免责声明 |
| **Rocq 9.0+ 版本** | `03-coq-isabelle/README.md` | 声称环境为 "Rocq 9.0+"；Rocq 9.0 在 2026-06-08 可能尚未正式发布，属于前瞻性版本声明 |
| **T10 完成日期超前** | `01-tla-plus/case-library.md` 状态行 | "T10 工业控制案例已完成（2026-06-第4周）"；当前日期 2026-06-08 为**第 2 周**，日期超前约两周 |

### 3. 引用来源权威性存疑

| 问题 | 位置 | 详情 |
|------|------|------|
| **A2A 非官方域名** | `01-tla-plus/a2a-task-lifecycle.md` 参考文献 [^8] | 引用 `https://a2a-protocol.org` 作为 "Google A2A Protocol Specification v1.0" 来源；Google A2A 的官方发布渠道为 GitHub 仓库 (`google/A2A`)，该域名权威性需核实 |
| **第三方博客替代官方规范** | `01-tla-plus/a2a-task-lifecycle.md` [^7] | 引用 PickAxe 博客 "MCP vs A2A Protocol" 作为 A2A 背景来源，非权威规范文档 |
| **第三方博客替代官方规范** | `01-tla-plus/mcp-capability-negotiation.md` [^6] | 引用 DevelopersDigest 博客 "What Is the Model Context Protocol? A 2026 Primer" 作为 MCP 规范说明；官方规范来源应为 `https://spec.modelcontextprotocol.io` |
| **待核实文献** | `02-alloy/mcp-tool-graph.md` 参考文献 3–4 | 引用 "CIS MCP Companion Guide (April 2026)" 及 "Jamshidi et al. (2025). arXiv:2603.00195"；这两篇文献的可访问性与权威性需独立核实 |

### 4. 跨文件状态矛盾

| 问题 | 位置 | 详情 |
|------|------|------|
| **Alloy 案例状态不一致** | `07-formal-verification/README.md` 当前状态 | 根 README 将 "Alloy 跨层映射 + ISA-95 层次案例 (2026-Q4)" 标记为 **未完成**；但 `plans-tasks/roadmap.md` 明确标注 T13/T14 已完成，且 `cross-layer-mapping.als/md` 与 `isa95-hierarchy.als/md` 实际存在并内容完整 |
| **Polonius 案例标注** | `04-rust-type-system/polonius-vs-nll.md` §4.4 | Case 4（链式可变引用精确追踪）注释说明 "Alpha 分析**可能**不接受"，与 §5.1 表格中 "✅ 合法" 的标注存在细微不一致；建议统一为 "Alpha: 可能不接受 / 完整 Polonius: 接受" |

### 5. 跨文件引用路径检查

- **正确路径**（已验证存在）:
  - `99-reference/tools/formal-verification-env/README.md` ✅
  - `11-industrial-iot-otit/01-isa-95-model/isa-95-asset-catalog-deep-dive.md` ✅
  - `04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md` ✅
  - `01-meta-model-standards/06-formal-axioms/axiom-system.md` ✅
  - `05-functional-architecture-reuse/06-mcp-a2a-protocols/mcp-tool-design.md` ✅

- **路径存在但内容不匹配**:
  - `11-industrial-iot-otit/02-opc-ua-fx/connection-manager/tla-specification.tla` ✅（存在）
  - `11-industrial-iot-otit/04-plcopen-motion/plcopen-motion.tla` ✅（存在）

---

## 待补充内容（按 Phase 2 规划）

1. **Coq/Isabelle 安全关键组件定理证明纲要（P2-T1 / T18b）**
   - 当前仅含教学级示例（插入排序、有界计数器、旋转门）。
   - 按 `roadmap.md` 规划，需在 2026-Q4 补充 seL4/CompCert 风格的组件级定理证明模板或纲要文档。

2. **TLA+ T10 本地说明文档（P2-T2）**
   - `case-library.md` 索引中的 `tla-verification.md` 实际不存在。
   - 建议：在 `01-tla-plus/` 下创建 T10 说明文档（链接至跨主题规约），或更新 `case-library.md` 索引为跨主题路径并删除本地文件名声明。

3. **TLA+ T09 本地索引（P2-T3）**
   - `case-library.md` 的待完成表格中列出 T09，但无本地文件入口。
   - 建议：在 `01-tla-plus/` 下增加 T09 简要索引或跨主题链接说明。

4. **ci-workflows.md（P2-T4）**
   - 如 `03-coq-isabelle/` 仍需独立 CI 文档，应补充 `ci-workflows.md`；如不再计划，应更新 `README.md` 目录结构。

5. **根 README 状态同步（P2-T5）**
   - 根 `README.md` 中 "Alloy 跨层映射 + ISA-95 层次案例" 应标记为 **已完成**。

6. **前瞻性声明标注规范化（P2-T6）**
   - 对 Rust 1.93、Polonius 2026 稳定化、Rocq 9.0+ 等尚未发生的版本/事件，建议在正文中添加 `> **注意**: 此为项目目标/预测性声明，截至 2026-06-08 尚未正式发布` 的标注。

---

## 附录：文件树速查

```text
07-formal-verification/
├── README.md
├── plans-tasks/roadmap.md
├── 01-tla-plus/
│   ├── case-library.md
│   ├── payment-service.md / .tla
│   ├── mcp-capability-negotiation.md / .tla
│   └── a2a-task-lifecycle.md / .tla
│   (跨主题: 11-industrial-iot-otit/02-opc-ua-fx/...tla, 04-plcopen-motion/...tla)
├── 02-alloy/
│   ├── component-dependency.md / .als
│   ├── mcp-tool-graph.md / .als
│   ├── cross-layer-mapping.md / .als
│   └── isa95-hierarchy.md / .als
├── 03-coq-isabelle/
│   ├── README.md
│   ├── coq-examples/bounded_counter.v / insertion_sort.v
│   └── isabelle-theories/InsertionSort.thy / Turnstile.thy / ROOT
├── 04-rust-type-system/
│   ├── cargo-sat-resolution.md
│   ├── formal-semantics.md
│   ├── polonius-vs-nll.md
│   ├── toolchain-practice.md
│   ├── unsafe-verification.md
│   └── examples/{kani_abs,miri_ub,prusti_add,verus_add}.rs
├── 05-spark-ada/
│   ├── flight-control-contracts.md
│   ├── mcdc-formalization.md
│   └── spark-ada-do333-industrial.md
├── 06-b-method/
│   ├── event-b-railway-refinement.md
│   └── railway-signaling-refinement.md
└── 09-comparative-matrices/
    └── spark-ada-vs-rust-verification-matrix.md
```

---

> **维护建议**: 本报告随 Phase 2 推进定期更新。建议每次新增/修改规约后，同步更新 `case-library.md` 索引、`roadmap.md` 进度与根 `README.md` 状态，避免多文件状态漂移。


---

## 补充说明：07 形式化验证 — 内容梳理报告

## 概念定义

**定义**：形式化验证（Formal Verification）是使用数学方法（逻辑、自动机、类型论）严格证明系统或其模型满足规约的过程；在复用场景中，它通过显式契约、不变式与精化关系保证可复用资产在多变上下文中的行为一致性。

## 示例

**示例**：TLA+ 规约刻画分布式支付服务的原子性：PlusCal 算法描述“扣款-记账”步骤，模型检验器 TLC 验证所有可达状态下账户总额守恒，确保该服务被 10+ 业务系统复用时不会出现重复记账。

## 反例

**反例**：某团队将并发队列组件复用到金融核心系统，仅依赖单元测试与代码评审，未对内存序与边界条件进行形式化分析，生产环境出现偶发数据竞态，造成资金缺口。

## 权威来源

> **权威来源**:
>
> - [TLA+ Home Page](https://lamport.azurewebsites.net/tla/tla.html)
> - [Alloy Analyzer](http://alloy.mit.edu)
> - [Coq Proof Assistant](https://coq.inria.fr)
> - [The Rust Programming Language](https://www.rust-lang.org)
> - [SPARK Pro](https://www.adacore.com/sparkpro)
> - [Event-B](https://www.event-b.org)
> - 核查日期：2026-07-07
