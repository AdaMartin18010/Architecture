# 07 形式化验证与复用正确性

## 定位

将复用组件的正确性从"测试验证"提升到"数学证明"的最高等级保证。

## 核心内容

- **TLA+**: 分布式复用组件的时序行为规约（Leslie Lamport）
- **Alloy**: 架构约束的约束求解验证（Daniel Jackson）
- **Coq/Isabelle**: 定理证明与程序验证（CompCert, seL4）
- **Rust 类型系统**: 编译期复用安全的形式化基础（所有权、借用、生命周期）
  - RustBelt (Iris), Aeneas (Inria), Kani (AWS), Prusti (ETH Zurich)
- **SPARK/Ada**: 飞行控制软件的契约验证（Airbus A380 案例）
  - `05-spark-ada/flight-control-contracts.md` — 自动驾驶仪模式切换与高度保持的完整契约设计
  - `05-spark-ada/mcdc-formalization.md` — DO-178C MC/DC 形式化定义与 SPARK 工具链验证
- **B Method**: 铁路信号系统的形式化精化链
  - `06-b-method/railway-signaling-refinement.md` — B Method / Event-B 铁路信号系统精化链案例（三层精化：M0 进路安全 → M1 区段道岔 → M2 信号联锁）
  - `06-b-method/event-b-railway-refinement.md` — Event-B 与 B Method 体系总览、工具链与工业应用
- **模型检测**: SPIN, NuSMV, CBMC（已在 `08-comparative-matrices/spark-ada-vs-rust-verification-matrix.md` 中部分覆盖）
- 形式化验证的复用决策矩阵（工具 × 层次 × 成本）
- **自动化验证环境**: Docker 化的 TLA+/Alloy/Coq/Isabelle（详见 [`99-reference/tools/formal-verification-env/README.md`](../../99-reference/tools/formal-verification-env/README.md)）

## 权威对齐

- [TLA+ Home Page](https://lamport.azurewebsites.net/tla/tla.html) (Leslie Lamport, Microsoft)
- [Alloy Tools](https://alloytools.org) (MIT)
- [Coq Proof Assistant](https://coq.inria.fr) (Inria)
- [Isabelle/HOL](https://isabelle.in.tum.de) (TU Munich)
- [RustBelt](https://plv.mpi-sws.org/rustbelt/) (MPI-SWS)
- [SPARK Pro](https://www.adacore.com/about-spark) (AdaCore)
- [Atelier B](https://www.atelierb.eu) (Clearsy)

## 关键公理
>
> **公理 F.1** (Formal Verification Trust Transfer): 若组件 C 通过形式化方法验证了性质 P，则任何使用 C 的系统继承 P 的正确性保证，前提是 C 的使用方式不违反 C 的前置条件。

## 当前状态

- [x] 形式化方法谱系梳理
- [x] TLA+/Alloy/Rust 案例示例
- [x] Rust 所有权-借用-生命周期形式化定义 (`04-rust-type-system/formal-semantics.md`)
- [x] Cargo 依赖解析 SAT 求解 (`04-rust-type-system/cargo-sat-resolution.md`)
- [x] Rust Polonius 借用检查器 vs NLL (`04-rust-type-system/polonius-vs-nll.md`)
- [x] unsafe 边界验证策略 (`04-rust-type-system/unsafe-verification.md`)
- [x] TLA+ 案例库启动 (`01-tla-plus/case-library.md` + 3 个规约)
- [x] Alloy 架构约束案例启动 (`02-alloy/component-dependency.als` + `mcp-tool-graph.als`)
- [ ] Alloy 跨层映射 + ISA-95 层次案例 (2026-Q4)
- [x] DO-178C MC/DC 形式化定义 (`05-spark-ada/mcdc-formalization.md`)
- [x] SPARK/Ada 飞控案例 (`05-spark-ada/flight-control-contracts.md`)
- [x] B Method 铁路信号案例 (`06-b-method/railway-signaling-refinement.md`)
- [x] Coq/Isabelle 教学示例（`insertion_sort.v`, `bounded_counter.v`, `Turnstile.thy`）— 基础语法验证
- [ ] Coq/Isabelle 安全关键组件定理证明（`03-coq-isabelle/`，Phase 2 2026-Q4）— 待启动

## 验证环境

按 `SUBSEQUENT_PLAN_2026.md` 决策 2A，本项目已建立 Docker 化形式化验证环境：

```bash
cd struct/99-reference/tools/formal-verification-env
docker compose up -d
```

新增规约必须通过以下至少一种工具验证：

- TLA+: `tlc <spec>.tla -deadlock`
- Alloy: `alloy <model>.als`
- Coq: `coqc <proof>.v`
- Isabelle: `isabelle build -D <dir>`

## 关联主题

- `04-component-architecture-reuse`（Rust 生态形式化）
- `11-industrial-iot-otit`（功能安全形式化验证）
