# Coq/Isabelle 安全关键组件定理证明纲要

> **版本**: 2026-06-08 (Phase 2)
> **定位**: 将教学级证明示例（插入排序、有界计数器）扩展到安全关键系统的工业级定理证明方法论
> **对齐公理**: `struct/01-meta-model-standards/06-formal-axioms/axiom-system.md` 之 S.2 Compositionality、F.1 Formal Verification Trust Transfer
> **状态**: 概念文档 — 证明结构说明，不执行完整证明

---

## 目录

- [Coq/Isabelle 安全关键组件定理证明纲要](#coqisabelle-安全关键组件定理证明纲要)
  - [目录](#目录)
  - [1. Coq/Isabelle 在安全关键系统中的定位](#1-coqisabelle-在安全关键系统中的定位)
    - [1.1 与 TLA+ 和 Alloy 的互补关系](#11-与-tla-和-alloy-的互补关系)
    - [1.2 何时选择定理证明](#12-何时选择定理证明)
  - [2. 安全关键组件证明纲要](#2-安全关键组件证明纲要)
    - [案例 A：seL4 风格的操作系统内核内存安全](#案例-asel4-风格的操作系统内核内存安全)
      - [系统描述与关键性质](#系统描述与关键性质)
      - [形式化规约语言选择：Coq](#形式化规约语言选择coq)
      - [证明策略概述](#证明策略概述)
      - [关键引理 / 定理列表（证明结构）](#关键引理--定理列表证明结构)
      - [可信计算基（TCB）分析](#可信计算基tcb分析)
    - [案例 B：飞行控制系统的状态不变量保持](#案例-b飞行控制系统的状态不变量保持)
      - [系统描述与关键性质](#系统描述与关键性质-1)
      - [形式化规约语言选择：Isabelle/HOL](#形式化规约语言选择isabellehol)
      - [证明策略概述](#证明策略概述-1)
      - [关键引理 / 定理列表（证明结构）](#关键引理--定理列表证明结构-1)
      - [可信计算基（TCB）分析](#可信计算基tcb分析-1)
  - [3. 与现有教学示例的衔接](#3-与现有教学示例的衔接)
    - [3.1 `insertion_sort.v` → 归纳证明基础](#31-insertion_sortv--归纳证明基础)
    - [3.2 `bounded_counter.v` → 不变量保持](#32-bounded_counterv--不变量保持)
    - [3.3 从教学示例到安全关键证明的过渡路径](#33-从教学示例到安全关键证明的过渡路径)
  - [4. 权威来源](#4-权威来源)
  - [补充说明：Coq/Isabelle 安全关键组件定理证明纲要](#补充说明coqisabelle-安全关键组件定理证明纲要)
  - [概念定义](#概念定义)
  - [反例](#反例)
  - [权威来源](#权威来源)

## 1. Coq/Isabelle 在安全关键系统中的定位

### 1.1 与 TLA+ 和 Alloy 的互补关系

形式化验证工具谱系中，Coq/Isabelle 位于**演绎证明**（deductive proof）的顶端，与 TLA+（行为规约/模型检验）和 Alloy（约束求解/结构验证）形成互补三角：

| 维度 | TLA+ | Alloy | Coq / Isabelle |
|------|------|-------|----------------|
| 验证对象 | 时序行为、活性/安全性 | 结构约束、架构一致性 | 功能正确性、数学性质 |
| 自动化 | 有限状态模型检验 | SAT 求解（有界） | 交互式 + 部分自动化 |
| 保证强度 | 有限实例上的保证 | 有界 scope 内的保证 | **数学上绝对的正确性** |
| 典型场景 | 分布式协议死锁检测 | 架构层次无循环 | 编译器正确性、OS 内核隔离 |

三者并非互斥。工业实践中常见的组合是：**Alloy 验证架构静态约束 → TLA+ 验证分布式时序行为 → Coq/Isabelle 验证核心算法的功能正确性**。这对应于公理 S.2（Compositionality）的分层组合思想：各层次的形式化保证通过 Assume-Guarantee 框架向上传递。

### 1.2 何时选择定理证明

定理证明的投入成本显著高于模型检验或约束求解。选择定理证明的决策条件：

1. **失效后果不可逆**：航空电子、医疗设备、核控制系统中，单个缺陷可能导致人员伤亡。
2. **无运行时可验证的降级路径**：与安全关键系统的" fail-safe "不同，某些组件（如编译器）的错误会在目标代码中潜伏，无法通过运行时监控捕获。
3. **需要组合性保证**：被复用组件的形式化证明可被下游系统继承（公理 F.1），形成"信任链"。
4. **涉及无限状态空间**：内存分配、递归数据结构、浮点运算等场景超出有限状态模型检验的能力边界。

---

## 2. 安全关键组件证明纲要

以下两个案例覆盖了操作系统内核（低层基础设施）和飞行控制系统（高安全等级应用）的典型证明模式。

---

### 案例 A：seL4 风格的操作系统内核内存安全

#### 系统描述与关键性质

seL4（Klein et al., 2009）是首个经过完整功能正确性证明的 OS 内核。其核心安全目标是：**任何用户态进程都无法通过内核接口破坏其他进程的内存隔离**。在本知识体系中，该内核作为"可复用安全基座"被多个上层系统继承其隔离保证。

关键性质（按证明依赖排序）：

| 性质 | 含义 | 安全等级 |
|------|------|---------|
| **无空指针解引用** | 内核代码永不访问无效地址 | SIL 2+ |
| **内存隔离** | 进程 A 无法读写进程 B 的物理页帧 | SIL 3+ |
| **能力传递完整性** | 能力（capability）的创建/撤销/转移符合授权图 | SIL 4 |
| **功能正确性** | C 代码与高层规约的精化关系 | SIL 4 |

#### 形式化规约语言选择：Coq

选择 Coq（而非 Isabelle）的核心原因：

1. **CompCert 生态兼容性**：Leroy (2009) 的 CompCert 编译器已在 Coq 中完成证明，使得"C 代码 → 汇编代码"的编译正确性可被纳入同一信任链。
2. **Verdi 框架**：Inria 的 Verdi 提供了分布式系统形式化的 Coq 基础设施，其"网络语义提取"技术可直接复用。
3. **依赖类型表达力**：内核中页表、能力等数据结构的不变量天然适合用依赖类型（`vect n A` 而非 `list A`）表达。

#### 证明策略概述

```text
证明层级（自底向上）：

Level 0: 机器语义 —— x86/ARM 操作语义的 Coq 形式化（使用 VST/CompCert）
Level 1: C 代码验证 —— 用 VST (Verified Software Toolchain) 证明 C 函数满足 Hoare 三元组
Level 2: 抽象规约 —— 状态机 + 不变量（受 bounded_counter.v 模式启发）
Level 3: 安全定理 —— 从不变量推导信息流安全（非干涉性, non-interference）
```

| 策略 | 适用层级 | Coq  tactic 示例 |
|------|---------|-----------------|
| 结构归纳法 | Level 0-2 | `induction p as […] using page_table_ind` |
| 反演/注入 | Level 1 | `inversion H; subst; clear H` |
| 重写 + `lia`/`nia` | Level 1-2 | `rewrite addr_offset_comm; lia` |
| 自动化脚本 (`auto`, `eauto`) | Level 1-2 | 自定义 hint 数据库 (`Hint Resolve page_valid_neq …`) |
| 高阶抽象（谓词转换器） | Level 3 | `wp_seq; wp_load; wp_store; iFrame` (Iris) |

#### 关键引理 / 定理列表（证明结构）

```coq
(* ---------- 引理层级 ---------- *)

(* L1: 页表遍历终止性 —— 对应 insertion_sort.v 中的归纳基础 *)
Lemma walk_page_table_terminates :
  forall (pt : page_table) (vaddr : virt_addr),
    well_formed pt -> exists paddr, walk pt vaddr = Some paddr.
Proof. (* 对页表层级深度进行强归纳 *) Qed.

(* L2: 映射保持隔离 —— 对应 bounded_counter.v 的不变量保持模式 *)
Lemma map_page_preserves_isolation :
  forall (s s' : kernel_state) (pid : process_id) (vaddr : virt_addr),
    kernel_invariant s ->
    kernel_map s pid vaddr = Some s' ->
    kernel_invariant s' /\ memory_isolated s'.
Proof. (* 展开 kernel_map，反演所有可能分支，验证不变量子项 *) Qed.

(* L3: 能力转移的授权单调性 *)
Lemma cap_transfer_auth_mono :
  forall (s s' : kernel_state) (src dst : process_id) (cap : capability),
    authorized s src cap ->
    kernel_transfer s src dst cap = Some s' ->
    authorized s' dst cap /\ (~authorized s' src cap \/ src = dst).
Proof. (* 能力图上的归纳，结合反证法 *) Qed.

(* T1: 核心安全定理 —— 非干涉性 *)
Theorem non_interference :
  forall (s1 s2 : kernel_state) (pid : process_id) (o : observable),
    kernel_invariant s1 -> kernel_invariant s2 ->
    equiv_except s1 s2 pid ->
    observe s1 pid o = observe s2 pid o.
Proof. (* 对系统调用轨迹进行共归纳，引用 L1-L3 *) Qed.
```

#### 可信计算基（TCB）分析

| TCB 组件 | 风险 | 缓解措施 |
|----------|------|---------|
| Coq 内核 (~30k LOC OCaml) | 证明检查器 bug 导致"假正确" | 独立 proof checker (Coqchk) + `coqchk` 交叉验证 |
| CompCert C 语义 | 语义与实际硬件不符 | 官方测试套件覆盖 ARMv8/x86_64；与硬件模拟器对比测试 |
| VST 内存模型 | 内存模型过强/过弱 | 使用 CompCert 的精细内存模型（非简化大堆模型） |
| 规约本身 | 规约未捕获真实安全需求 | 形式化规约与威胁模型文档的双向追溯 |

---

### 案例 B：飞行控制系统的状态不变量保持

#### 系统描述与关键性质

飞行控制系统（Flight Control System, FCS）是航空电子中安全完整性等级最高的软件之一（DAL-A，对应 IEC 61508 SIL 4）。TU Munich 在 Isabelle/HOL 中的 Aerospace 项目将该类系统的验证归纳为**状态不变量的保持**问题：系统在每个控制周期内读取传感器、计算控制面指令、输出作动器信号，全程必须保持一组关键不变量。

关键性质：

| 不变量 | 含义 | 失效后果 |
|--------|------|---------|
| **俯仰角有界** | $\|\theta\| \leq \theta_{\max}$ | 失速或结构过载 |
| **滚转角速率可控** | $\|\dot{\phi}\| \leq \dot{\phi}_{\max}$ | 螺旋失速 |
| **控制模式一致性** | 当前模式 $\in$ {NORMAL, DIRECT, ALTERNATE} 的合法转移图 | 模式混乱导致误操作 |
| **传感器交叉校验通过** | 三余度传感器中至少两路一致 | 单点故障未被检测 |

#### 形式化规约语言选择：Isabelle/HOL

选择 Isabelle/HOL 的核心原因：

1. **Sledgehammer 自动化**：飞行控制律涉及大量实数算术和代数变换，Sledgehammer 调用 Z3、Vampire 等 ATP 可大幅减少手工证明步骤。
2. **HOL-Analysis 库**：Isabelle 拥有最完备的数学分析库之一，适合表达控制理论的连续动态（微分不变量）。
3. **DO-333 资质路径**：Isabelle 已被用于 DO-178C / DO-333（形式化方法补充）的合规验证，有成熟的工业认证案例。
4. **结构化证明可读性**：Isabelle 的 Isar 证明语言接近自然语言，便于安全审计员（非形式化专家）审查。

#### 证明策略概述

```text
证明层级（自顶向下精化）：

Level 0: 物理模型 —— 飞行器六自由度动力学（连续微分方程）
Level 1: 离散控制器 —— 周期采样 + 控制律计算（ZOH 离散化）
Level 2: 软件实现 —— 定点算术 + 查表插值 + 模式机
Level 3: 代码生成 —— Simulink/SCADE → C 代码的精化证明
```

| 策略 | 适用层级 | Isabelle 方法 |
|------|---------|--------------|
| 重写 (`simp`, `auto`) | Level 2-3 | 控制律代数式的符号化简 |
| Sledgehammer | Level 0-1 | 实数不等式、矩阵正定性证明 |
| 归纳法 (`induct`) | Level 2 | 控制周期上的不变量保持 |
| 精化证明 (`refine`) | Level 2→3 | 抽象状态机到 C 代码的逐步精化 |
| 微分不变量 (`differential_invariant`) | Level 0-1 | 连续系统的安全区域保持 |

#### 关键引理 / 定理列表（证明结构）

```isabelle
theory FlightControlSafety
imports HOL.Real HOL.Analysis "HOL-Statespace.StateSpaceSyntax"
begin

(* ---------- 状态空间定义（受 Turnstile.thy 启发） ---------- *)
statespace flight_state =
  pitch_angle :: real    (* θ *)
  roll_rate   :: real    (* φ̇ *)
  mode        :: "Mode enum"
  sensor_votes :: "SensorVote set"

(* ---------- 不变量定义（受 bounded_counter.v 模式启发） ---------- *)
definition inv_pitch_bounded :: "flight_state => bool" where
  "inv_pitch_bounded s ≡ |pitch_angle s| ≤ θ_max"

definition inv_mode_legal :: "flight_state => bool" where
  "inv_mode_legal s ≡ mode s ∈ legal_modes"

(* ---------- 引理层级 ---------- *)

(* L1: 控制律输出保持俯仰角有界 —— 连续动态 *)
lemma control_law_preserves_pitch:
  assumes "inv_pitch_bounded s"
    and "sensor_votes_valid (sensor_votes s)"
  shows "inv_pitch_bounded (step_controller s)"
  using assms
proof (induct rule: controller_step_induct)
  (* Sledgehammer 自动处理实数不等式链 *)
  case (normal_mode s)
  then show ?case
    by (smt (verit, ccfv_SIG) control_gain_bound sensor_vote2_bound)
qed

(* L2: 模式转移的闭包性质 —— 状态机 *)
lemma mode_transition_closed:
  assumes "inv_mode_legal s" and "m' ∈ next_modes (mode s)"
  shows "m' ∈ legal_modes"
  using assms by (auto simp: legal_modes_def next_modes_def)

(* L3: 传感器交叉校验隐含可用性 —— 容错假设 *)
lemma sensor_votes_implies_safety:
  assumes "|sensor_votes s| ≥ 2"
    and "∀sv ∈ sensor_votes s. consistent sv"
  shows "∃v. dominant_vote (sensor_votes s) = Some v"
  using assms by (metis dominant_vote_def vote_majority)

(* T1: 核心安全定理 —— 每个控制周期保持所有不变量 *)
theorem fcs_safety_invariant:
  assumes "kernel_invariant s"  (* 借用公理 F.1 的信任传递概念 *)
    and "∀i. inv_i s"          (* 所有不变量在初始状态成立 *)
  shows "∀i. inv_i (control_cycle s)"
proof (induct "control_cycle" rule: cycle_induct)
  case base show ?case using assms by simp
  case (step s')
  show ?case
    by (meson L1 L2 L3 step.IH)
qed

end
```

#### 可信计算基（TCB）分析

| TCB 组件 | 风险 | 缓解措施 |
|----------|------|---------|
| Isabelle 内核 (~200k ML) | 证明检查器 bug | 独立内核 `HOL-Light` 交叉验证关键定理；归档证明（AFP）社区审查 |
| 自动定理证明器（Z3, E, Vampire） | ATP 返回错误证明 | Isabelle 对 ATP 返回的 proof sketch 进行独立重放验证 |
| 实数理论（HOL-Analysis） | 分析学公理不一致 | 基于 ZFC 的标准分析学；独立数学审查 |
| 代码生成器（Isabelle → SML/Scala/C） | 生成代码与规约语义偏差 | 使用经过验证的代码生成器（如 CakeML 链）；或采用手动审查 + 测试补充 |

---

## 3. 与现有教学示例的衔接

### 3.1 `insertion_sort.v` → 归纳证明基础

`insertion_sort.v` 中的 `insertion_sort_sorted` 定理展示了**结构归纳法**的最小完整模式：

```coq
Theorem insertion_sort_sorted : forall l, sorted (insertion_sort l).
Proof. intros l. induction l. (* 基例 + 归纳步 *) … Qed.
```

在安全关键证明中的扩展路径：

| 教学概念 | 安全关键扩展 | 案例 A / B 对应 |
|----------|-------------|----------------|
| 列表结构归纳 | 页表层级深度归纳 | 案例 A: `walk_page_table_terminates` |
| `sorted` 谓词 | `kernel_invariant` / `inv_pitch_bounded` | 案例 A/B 的不变量定义 |
| `insert_sorted` 引理 | `map_page_preserves_isolation` | 案例 A: 操作保持不变量 |
| `lia` 解线性不等式 | Sledgehammer / `smt` 解实数不等式 | 案例 B: 控制律有界性 |

### 3.2 `bounded_counter.v` → 不变量保持

`bounded_counter.v` 是安全关键验证的核心模式的极简表达：

```coq
Theorem inc_preserves_invariant :
  forall c, invariant c -> invariant (inc c).
```

在安全关键系统中，这一模式扩展为**多不变量族**（invariant family）：

```coq
(* 从单一不变量到不变量族 *)
Definition invariant_family (s : state) : Prop :=
  inv_memory_isolated s /\
  inv_capability_graph_acyclic s /\
  inv_interrupt_mask_consistent s /\
  … (* 数十个不变量的合取 *)
```

证明策略上，`destruct` + `lia` 的组合在简单算术中足够，但在内核级别需要：**反演不变量结构 → 分析操作分支 → 验证每个子不变量被保持 → 合取引入**。

### 3.3 从教学示例到安全关键证明的过渡路径

```
Step 1: 掌握基本 tactic（induction, destruct, rewrite, lia）
        └─> insertion_sort.v, bounded_counter.v

Step 2: 引入分离逻辑（Iris/VST）处理指针和内存
        └─> 验证链表/树等动态数据结构

Step 3: 构建复合不变量族，学习模块化证明
        └─> 案例 A 的 kernel_invariant（10+ 子不变量）

Step 4: 引入自动化（Sledgehammer / CoqHammer / eauto hints）
        └─> 案例 B 的控制律代数证明

Step 5: 跨工具信任链（CompCert + Coq / Isabelle 代码生成）
        └─> 完整 TCB 最小化
```

---

## 4. 权威来源

1. **Klein, G., et al. (2009).** seL4: formal verification of an OS kernel. *SOSP '09*. —— 操作系统内核功能正确性证明的里程碑；定义了"验证什么"（安全性质）与"如何验证"（分层抽象）的工业标准。
2. **Leroy, X. (2009).** A formally verified compiler back-end. *JAR 43(4)*. —— CompCert 编译器验证；证明 C 语义到汇编语义的精化关系，为内核 C 代码的可信编译提供基础。
3. **Nipkow, T., Paulson, L. C., & Wenzel, M. (2002).** *Isabelle/HOL: A Proof Assistant for Higher-Order Logic*. LNCS 2283. —— Isabelle 系统的权威教材；第 2 章（Foundation）和第 5 章（Isar）是结构化证明的核心参考。
4. **Appel, A. W. (2011).** *Verified Software Toolchain*. —— VST 的内存模型与 Hoare 逻辑形式化，连接 Coq 与 C 代码验证。
5. **Jung, R., et al. (2018).** Iris from the ground up. *JFP 28*. —— 现代分离逻辑框架，用于并发和高级语言特性的模块化推理。

---

> 最后更新: 2026-06-08
> 关联: `coq-examples/insertion_sort.v`, `coq-examples/bounded_counter.v`, `isabelle-theories/Turnstile.thy`


---

## 补充说明：Coq/Isabelle 安全关键组件定理证明纲要

## 概念定义

**定义**：Coq 与 Isabelle/HOL 是基于高阶逻辑的交互式定理证明器，支持从公理出发构造机器可检查的证明，常用于密码学、编译器与安全关键软件的验证。

## 反例

**反例**：密码库复用某开源实现时未验证其形式化安全规约，后来发现其实现与论文证明的抽象模型存在偏差，导致侧信道攻击。

## 权威来源

> **权威来源**:
>
> - [Coq Proof Assistant](https://coq.inria.fr)
> - [Isabelle/HOL](https://isabelle.in.tum.de)
> - 核查日期：2026-07-07
