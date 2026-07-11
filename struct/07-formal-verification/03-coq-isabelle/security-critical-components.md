# Coq / Isabelle Theorem Proving for Safety-Critical Components

**Version:** 2026-06-10
**Track:** T18b — Formal Verification
**Alignment Sources:** seL4, CompCert, VCC, Isabelle/HOL Refinement Framework
**Scope:** Industrial-strength machine-checked proofs for operating-system kernels, compilers, and mixed-criticality scheduling, with explicit cross-references to the `struct/` knowledge architecture.

---

## 目录

- [Coq / Isabelle Theorem Proving for Safety-Critical Components](#coq--isabelle-theorem-proving-for-safety-critical-components)
  - [目录](#目录)
  - [1. Gap Between Teaching Examples and Industrial Verification](#1-gap-between-teaching-examples-and-industrial-verification)
  - [2. seL4 Microkernel Style Case Study](#2-sel4-microkernel-style-case-study)
    - [2.1 Verification Goals](#21-verification-goals)
    - [2.2 Three-Layer Abstraction Stack](#22-three-layer-abstraction-stack)
    - [2.3 Core Proof Obligations with Coq / Isabelle Code Sketches](#23-core-proof-obligations-with-coq--isabelle-code-sketches)
      - [PO-1: Representation Relation (Bijection / Refinement Function)](#po-1-representation-relation-bijection--refinement-function)
      - [PO-2: Syscall Refinement (Forward Simulation)](#po-2-syscall-refinement-forward-simulation)
      - [PO-3: Invariant Preservation](#po-3-invariant-preservation)
    - [2.4 Mapping to `struct/` Topics](#24-mapping-to-struct-topics)
  - [3. CompCert Compiler Correctness Case Study](#3-compcert-compiler-correctness-case-study)
    - [3.1 Verification Goals](#31-verification-goals)
    - [3.2 Multi-Pass Compiler Refinement Chain](#32-multi-pass-compiler-refinement-chain)
    - [3.3 Simulation Relation Technique with Coq Code Sketch](#33-simulation-relation-technique-with-coq-code-sketch)
    - [3.4 Mapping to `struct/` Topics](#34-mapping-to-struct-topics)
  - [4. Mixed-Criticality Systems — Rate-Monotonic Scheduling Verification](#4-mixed-criticality-systems--rate-monotonic-scheduling-verification)
    - [4.1 Problem Definition (Liu \& Layland 1973)](#41-problem-definition-liu--layland-1973)
    - [4.2 Isabelle/HOL Proof Sketch for RM Schedulability Theorem](#42-isabellehol-proof-sketch-for-rm-schedulability-theorem)
    - [4.3 Alignment with Industrial Standards](#43-alignment-with-industrial-standards)
  - [5. Methodology Summary](#5-methodology-summary)
    - [5.1 Generic Pattern for Safety-Critical Verification (4 Layers)](#51-generic-pattern-for-safety-critical-verification-4-layers)
    - [5.2 Coq vs Isabelle Selection Guide](#52-coq-vs-isabelle-selection-guide)
    - [5.3 Authoritative Sources and Further Reading](#53-authoritative-sources-and-further-reading)
  - [6. Cross-References to Other `struct/` Topics](#6-cross-references-to-other-struct-topics)
  - [Status](#status)
  - [补充说明：Coq / Isabelle Theorem Proving for Safety-Critical Components](#补充说明coq--isabelle-theorem-proving-for-safety-critical-components)
  - [概念定义](#概念定义)
  - [示例](#示例)
  - [反例](#反例)
  - [权威来源](#权威来源)
  - [分析](#分析)

## 1. Gap Between Teaching Examples and Industrial Verification

Classical theorem-proving courses introduce induction over `nat`, list reversal, or a toy imperative language (WHILE).  Industrial verification must deal with C semantics, unbounded heap models, concurrency, and machine-code equivalence.  The table below maps the gap along seven dimensions.

| Dimension | Teaching Example | Industrial Target | Consequence for Proof Architecture |
|-----------|------------------|-------------------|-----------------------------------|
| **State space** | Small finite record (e.g., `pc :: nat`, `stk :: int list`) | Entire physical memory + device registers + MMU page tables | Need separation logic (VCC, Iris) or explicit memory model (seL4) |
| **Language** | Custom WHILE grammar with big-step SOS | Subset of C11 / C17, or ARM assembly | Deeply embedded operational semantics in Coq/Isabelle |
| **Abstraction layers** | 1–2 (e.g., spec + implementation) | 4–6 (abstract spec → executable spec → design → C → binary) | Layered refinement (Refinement Framework, Armada, L4.verified) |
| **Proof scale** | < 1 kLOC proof script | 200 k–1 M LOC proof script (seL4 ≈ 650 k, CompCert ≈ 150 k) | Modularity, parallel proof checking, CI for proofs |
| **Properties** | Partial correctness (`{P} c {Q}`) | Functional correctness + security (non-interference) + integrity + availability | Multiple property classes, each with own logic |
| **Code artifact** | No generated code; proof is the product | Extracted OCaml / Haskell, or verified C binary | Binary verification (Benediktse et al., seL4 binary verification) |
| **Change impact** | Re-prove one lemma | Re-prove thousands of lemmas after one C refactor | Proof maintainability, version pinning, proof engineering |

---

## 2. seL4 Microkernel Style Case Study

### 2.1 Verification Goals

The seL4 project (Klein et al., 2009–2020) provides the canonical blueprint for OS-kernel formal verification.  Its four goals are pursued sequentially:

1. **Functional correctness** — the C implementation refines the abstract Haskell specification.
2. **Integrity** — a subject can only modify objects it has explicit capabilities to.
3. **Security properties (non-interference)** — high-classification threads cannot leak information to low-classification threads via timing or storage channels.
4. **Binary verification** — the machine-code binary is semantically equivalent to the C source, eliminating compiler-bug and toolchain-trust risks.

### 2.2 Three-Layer Abstraction Stack

```
┌─────────────────────────────────────────┐
│  Layer 0: Abstract Haskell Spec         │  → Isabelle/HOL shallow embedding
│  (Capability-based access-control +     │    Functional, nondeterministic,
│   operational semantics)                │    large-step
├─────────────────────────────────────────┤
│  Layer 1: Executable Haskell Spec       │  → Haskell code, translated to
│  (Data-structure refinements,           │    Isabelle/HOL via translator
│   deterministic algorithm)              │
├─────────────────────────────────────────┤
│  Layer 2: C Design Model (CDL)          │  → Isabelle/HOL shallow embedding
│  (C semantics: memory, pointers,        │    of C subset; memory model
│   word arithmetic)                      │    by Tuch, Klein, Norrish
├─────────────────────────────────────────┤
│  Layer 3: C Source Code                 │  → Parsed by C-Parser into
│  (Production seL4 kernel)               │    Isabelle/HOL AST
├─────────────────────────────────────────┤
│  Layer 4: Binary (ARM / RISC-V / x86)   │  → Decompilation to Isabelle/HOL
│                                         │    by Magnus Myreen et al.
└─────────────────────────────────────────┘
```

### 2.3 Core Proof Obligations with Coq / Isabelle Code Sketches

#### PO-1: Representation Relation (Bijection / Refinement Function)

Between Layer 0 and Layer 1, an *abstraction function* `abs` maps concrete states to abstract states.  In Isabelle/HOL:

```isabelle
definition abs :: "kernel_state_concrete => kernel_state_abstract"
  where
  "abs s == <|
    threads = map_of (thread_array s),
    cdt = parent_of (cdt_array s),
    ...
  |>"

definition rep_inv :: "kernel_state_concrete => bool"
  where
  "rep_inv s ==
     array_wellformed (thread_array s) /\
     cdt_wellformed (cdt_array s) /\
     ..."

theorem abs_inj_on_rep_inv:
  assumes "rep_inv s1" and "rep_inv s2"
      and "abs s1 = abs s2"
    shows "s1 = s2"
  unfolding abs_def rep_inv_def
  by (auto intro: map_of_inj_on_wellformed ...)
```

In Coq the pattern is identical, using `Definition`, `Record`, and `Theorem` with `Proof. ... Qed.`:

```coq
Definition abs (s : concrete_state) : abstract_state := {|
  threads := map_of (thread_array s);
  cdt := parent_of (cdt_array s);
  ...
|}.

Definition rep_inv (s : concrete_state) : Prop :=
  array_wellformed (thread_array s) /\
  cdt_wellformed (cdt_array s) /\
  ... .

Theorem abs_inj_on_rep_inv :
  forall s1 s2,
    rep_inv s1 -> rep_inv s2 ->
    abs s1 = abs s2 ->
    s1 = s2.
Proof.
  unfold abs, rep_inv. intros. auto using map_of_inj_on_wellformed.
Qed.
```

#### PO-2: Syscall Refinement (Forward Simulation)

For every system call `invokeTCB`, the concrete implementation must *simulate* the abstract specification:

```isabelle
lemma invokeTCB_refine:
  "{| lambda s. valid_state s /\ tcb_inv_wf tinv /\ rep_inv s |}
     invokeTCB_impl tinv
   {| lambda rv s'. EX s''. (abs s, s'') : abstract_invokeTCB tinv
                    /\ abs s' = s'' /\ rep_inv s' |}"
  apply (wp, clarsimp, blast)
  done
```

The triple is a VCG (verification condition generator) Hoare triple in Isabelle/HOL.  The post-condition asserts that the concrete execution produces a state whose abstraction is reachable by the abstract operation.

In Coq (using Iris or a custom VCG):

```coq
Lemma invokeTCB_refine :
  {{{ valid_state s /\ tcb_inv_wf tinv /\ rep_inv s }}
    invokeTCB_impl tinv
  {{{ s' RET _, EX s'',
        abstract_step (abstract_invokeTCB tinv) (abs s) s'' /\
        abs s' = s'' /\
        rep_inv s'
  }}}.
Proof.
  iIntros (Phi) "[Hv [Hwf Hr]] Hpost".
  unfold invokeTCB_impl. wp_bind. ...
Qed.
```

#### PO-3: Invariant Preservation

All kernel entry points must preserve the top-level invariant `valid_state` (and all sub-invariants) assuming the user-mode precondition holds:

```isabelle
lemma kernelEntry_invariant:
  "{| valid_state /\ invs /\ user_context ctxt |}
     kernelEntry syscall
   {| lambda_. valid_state /\ invs |}"
```

### 2.4 Mapping to `struct/` Topics

| seL4 Concept | Maps to `struct/` Node |
|--------------|------------------------|
| Capability model (Layer 0) | `struct/04-component-architecture-reuse/01-capability-model/` |
| Refinement proof stack (Layers 0->3) | `struct/07-formal-verification/01-refinement-calculus/` |
| C semantics / memory model | `struct/07-formal-verification/02-separation-logic/` |
| Binary verification (Layer 4) | `struct/07-formal-verification/04-binary-verification/` |
| Non-interference proof | `struct/06-cross-layer-governance/02-security-traceability/` |
| DO-178C / CAST-32A alignment | `struct/09-value-quantification/01-certification-cost-model/` |

---

## 3. CompCert Compiler Correctness Case Study

### 3.1 Verification Goals

CompCert (Leroy, 2006–2024) proves that the compiled assembly program preserves the *observable behaviors* of the source C program.  The formal statement is **semantic preservation**:

> **Theorem (Semantic Preservation).** For every source program `S`, if `S` has a defined semantics (no undefined behavior), then every behavior of the compiled assembly program `T` is one of the allowed behaviors of `S`.

This eliminates an entire class of compiler-bug risks in safety-critical code.

### 3.2 Multi-Pass Compiler Refinement Chain

CompCert transforms the program through eight intermediate languages, each with its own small-step operational semantics:

```
CompCert C  -->  Clight  -->  Cminor  -->  RTL
                                              |
                                              v
                                            LTL  -->  Linear  -->  Mach  -->  Asm
```

- **CompCert C** — Source: pre-processed C, simplified control flow.
- **Clight** — C without side-effects in expressions.
- **Cminor** — Flat variables, explicit memory operations.
- **RTL** — Register Transfer Language, control-flow graph, 3-address code.
- **LTL** — Locations (registers + stack slots), linearized basic blocks.
- **Linear** — Sequential instructions, pending branches.
- **Mach** — Concrete stack layout, calling conventions.
- **Asm** — Target assembly (ARM, x86, RISC-V, PowerPC).

Each pass is proven correct independently; the composition yields end-to-end correctness.

### 3.3 Simulation Relation Technique with Coq Code Sketch

The core proof technique is a **forward simulation**: every source step is matched by zero, one, or several target steps, preserving a cross-language relation `match_states`.

```coq
(* In Coq/CompCert: common/Smallstep.v and backend/ ... .v *)

Record fsim_properties (S T : semantics) : Type := {
  fsim_index : Type;
  fsim_order : fsim_index -> fsim_index -> Prop;
  fsim_order_wf : well_founded fsim_order;
  fsim_match_states : fsim_index -> state S -> state T -> Prop;

  fsim_simulation :
    forall s1 s2 t, Step S s1 t s2 ->
    forall i s1', fsim_match_states i s1' s1 ->
    exists i', exists s2',
      (Plus T s1' t s2' \/ (Star T s1' t s2' /\ fsim_order i' i))
      /\ fsim_match_states i' s2' s2;

  fsim_match_initial_states :
    forall s1, initial_state S s1 ->
    exists i, exists s2, initial_state T s2 /\ fsim_match_states i s1 s2;

  fsim_match_final_states :
    forall i s1 s2 r,
    fsim_match_states i s1 s2 -> final_state S s1 r ->
    final_state T s2 r
}.
```

Each compiler pass (e.g., `RTL -> LTL`) instantiates `fsim_match_states` with a pass-specific relation (register allocation: pseudo-registers <-> hardware registers + spill slots) and proves the `fsim_simulation` clause.

### 3.4 Mapping to `struct/` Topics

| CompCert Concept | Maps to `struct/` Node |
|------------------|------------------------|
| Semantic preservation theorem | `struct/07-formal-verification/01-refinement-calculus/` |
| C semantics (Clight) | `struct/07-formal-verification/03-coq-isabelle/` (this file) |
| Separation logic for memory model | `struct/07-formal-verification/02-separation-logic/` |
| Binary equivalence / ASM proofs | `struct/07-formal-verification/04-binary-verification/` |
| Compiler as trusted supply-chain node | `struct/10-supply-chain-security/01-toolchain-provenance/` |

---

## 4. Mixed-Criticality Systems — Rate-Monotonic Scheduling Verification

### 4.1 Problem Definition (Liu & Layland 1973)

Consider a set of `n` independent periodic tasks `tau = {tau_1, ..., tau_n}` with:

- Period `T_i` (minimum inter-arrival time)
- Worst-case execution time `C_i`
- Utilization `U_i = C_i / T_i`

The **Rate-Monotonic (RM)** policy assigns static priorities inversely proportional to period: shorter period -> higher priority.  Liu & Layland proved that RM is optimal among fixed-priority policies, and provided a sufficient schedulability test:

> **Theorem (RM Schedulability).** If `sum C_i / T_i <= n (2^(1/n) - 1)`, then the task set is schedulable under RM on a uniprocessor.

For `n -> infinity`, the bound converges to `ln 2 ~= 0.693`.

### 4.2 Isabelle/HOL Proof Sketch for RM Schedulability Theorem

The proof has been mechanized in Isabelle/HOL (rt-scheduling AFP entry, and Prosa framework).  A condensed sketch:

```isabelle
theory RM_Schedulability
  imports "HOL-Analysis.Analysis" "AFP/Prosa......"
begin

(* Task model *)
record task =
  period :: nat
  cost   :: nat

definition utilization :: "task => real"
  where "utilization tau = real (cost tau) / real (period tau)"

definition rm_priority :: "task => task => bool"
  where "rm_priority tau1 tau2 <-> period tau1 <= period tau2"

(* Response-time analysis: critical-instant theorem *)
theorem response_time_bound_rm:
  assumes "forall tau : ts. period tau > 0 /\ cost tau <= period tau"
      and "total_utilization ts <= card ts * (2 powr (1 / card ts) - 1)"
    shows "forall tau : ts. EX R. R <= period tau /\ response_time tau <= R"
  unfolding total_utilization_def rm_priority_def
  (* Proof by induction on task priority level,
     using busy-window fixed-point iteration. *)
  sorry  (* Actual AFP proof is > 3 kLOC *)

end
```

In Coq, a similar proof can be structured using the **Prosa** formalization ported to Coq (RT-CertiKOS / Prosa Coq version), or using the **Mathematical Components** library for real analysis:

```coq
Require Import Reals Lra.

Record task := Task {
  period : nat;
  cost   : nat
}.

Definition utilization (tau : task) : R :=
  INR (cost tau) / INR (period tau).

Definition rm_le (tau1 tau2 : task) : Prop :=
  (period tau1 <= period tau2)%nat.

Theorem rm_schedulability_bound :
  forall (ts : seq task) (n := size ts),
    (forall tau, tau \in ts -> (0 < period tau)%nat) ->
    (forall tau, tau \in ts -> (cost tau <= period tau)%nat) ->
    \sum_(tau <- ts) utilization tau <= INR n * (2 ^ (1 / INR n) - 1) ->
    forall tau, tau \in ts ->
      exists R : R,
        R <= INR (period tau) /\
        response_time rm_le ts tau <= R.
Proof.
  (* Uses fixed-point iteration on busy window,
     induction on priority level, and real analysis
     lemmas from Mathematical Components. *)
Admitted.
```

### 4.3 Alignment with Industrial Standards

| Standard | Relevant Clause / Objective | How Formal Proof Helps |
|----------|----------------------------|------------------------|
| **DO-178C** (Avionics) | Supplement DO-333 (Formal Methods) | Machine-checked proof replaces some tests, satisfies MC/5 (mitigation of compiler errors via CompCert) |
| **ISO 26262** (Automotive) | ASIL D: Table A.4 (semi-formal methods), Table A.5 (formal design & verification) | RM schedulability proof satisfies "freedom from interference" (Part 6, 7.4.4) |
| **IEC 61508** (General) | SIL 4: Table A.3 (formal methods), Table B.3 (static analysis) | Theorem-prover output is a "highly recommended" technique; reduces diagnostic-coverage demands |

---

## 5. Methodology Summary

### 5.1 Generic Pattern for Safety-Critical Verification (4 Layers)

Based on seL4, CompCert, and Prosa, a reusable four-layer pattern emerges:

```
Layer 0 — Abstract Specification
          -> Mathematics (sets, relations, real-time calculus)
          -> Isabelle/HOL or Coq with SSReflect / MathComp

Layer 1 — Executable Algorithmic Specification
          -> Functional program (Haskell, Coq functions, Isabelle definitions)
          -> Deterministic, complexity-relevant

Layer 2 — Design Model / Low-Level Language
          -> C semantics, assembly semantics, or timed-automata semantics
          -> Operational semantics (small-step or big-step)

Layer 3 — Concrete Implementation / Binary
          -> C source, extracted OCaml, or target assembly
          -> Linked with hardware models for end-to-end binary proof
```

**Between each adjacent pair:** prove a refinement / simulation / equivalence theorem.

### 5.2 Coq vs Isabelle Selection Guide

| Criterion | Coq | Isabelle/HOL |
|-----------|-----|--------------|
| **Foundations** | Dependent types + Calculus of Inductive Constructions (CIC) | Simply-typed HOL + axiomatic type classes + locales |
| **Proof style** | Tactic scripts (Ltac, Ltac2, ssreflect) or proof terms | Tactic scripts (Isar, Eisbach) + ATP integration (Sledgehammer, Nitpick) |
| **Automation** | `auto`, `eauto`, `tauto`, limited ATP (coq-hammer) | Strong SMT/ATP bridge (Sledgehammer, z3, vampire, e) |
| **Standard library** | Standard Library + Mathematical Components (SSReflect) | Main HOL + AFP (Archive of Formal Proofs, > 700 entries) |
| **Extraction** | Native: extracts to OCaml, Haskell, Scheme | Limited: Isabelle/ML for tooling; code export less mature |
| **Industrial cases** | CompCert, VST (Verified Software Toolchain), CertiKOS, Prosa (Coq) | seL4, Isabelle/HOL Refinement Framework, PROSPER, l4.verified |
| **Learning curve** | Steeper if unfamiliar with dependent types; ssreflect is dense | Gentler for classical logic background; Isar reads like structured prose |
| **When to choose** | Compiler verification, deep language embeddings, dependently-typed data structures, program extraction | OS kernels, large refinement stacks, heavy automation, team readability |

**Pragmatic advice:** For a new project, choose the ecosystem whose existing libraries are closest to your domain.  Reusing AFP or CompCert infrastructure saves more effort than the language difference costs.

### 5.3 Authoritative Sources and Further Reading

| Source | Role | Link / Reference |
|--------|------|------------------|
| **seL4 proofs** | Complete Isabelle/HOL proof stack for an OS kernel | `https://github.com/seL4/l4v` |
| **CompCert** | Verified C compiler in Coq | `https://compcert.org/` |
| **Isabelle/HOL** | System and documentation | `https://www.cl.cam.ac.uk/research/hvg/Isabelle/` |
| **Coq** | System and documentation | `https://coq.inria.fr/` |
| **Coq'Art** | Textbook: interactive theorem proving in Coq | Bertot & Casteran, *Interactive Theorem Proving and Program Development* |
| **Isabelle/HOL Book** | Definitive reference for Isabelle/HOL | Nipkow, Klein, *Concrete Semantics* (free PDF) |
| **Refinement Framework** | Isabelle/HOL library for stepwise refinement | Lammich, *Refinement to Imperative/HOL* (AFP entry) |
| **VCC** | Verifier for Concurrent C (Boogie/Z3-based, not Coq/Isabelle but aligned) | `https://vcc.codeplex.com/` (legacy; see *Verifying C Programs with VCC*) |
| **Prosa** | Coq formalization of real-time scheduling | `https://prosa.mpi-sws.org/` |
| **Iris** | Higher-order concurrent separation logic framework in Coq | `https://iris-project.org/` |

---

## 6. Cross-References to Other `struct/` Topics

| This File (T18b) | Related `struct/` Node | Relationship |
|------------------|------------------------|--------------|
| `security-critical-components.md` | `struct/07-formal-verification/01-refinement-calculus/` | Refinement calculus provides the *method*; this file provides the *industrial instances* (seL4, CompCert). |
| `security-critical-components.md` | `struct/07-formal-verification/02-separation-logic/` | seL4 C semantics and Iris-style reasoning for heap safety. |
| `security-critical-components.md` | `struct/07-formal-verification/04-binary-verification/` | Layer 4 of seL4; CompCert produces Asm but does not verify the assembler/linker (see binary verification for that gap). |
| `security-critical-components.md` | `struct/06-cross-layer-governance/02-security-traceability/` | Non-interference proofs establish end-to-end security properties traceable from abstract spec to binary. |
| `security-critical-components.md` | `struct/10-supply-chain-security/01-toolchain-provenance/` | CompCert *is* the trusted compiler in the supply chain; its proof reduces toolchain TCB. |
| `security-critical-components.md` | `struct/09-value-quantification/01-certification-cost-model/` | DO-178C / DO-333 credits reduce testing effort, shifting cost to proof engineering. |
| `security-critical-components.md` | `struct/08-cognitive-architecture/01-agent-safety/` | Safety proofs for scheduling kernels extend to agent-computing resource partitioning. |

---

## Status

**T18b completed** — Coq / Isabelle theorem proving for safety-critical components documented with industrial case studies (seL4, CompCert, Rate-Monotonic scheduling), proof-obligation sketches, standard alignments, and full cross-reference mappings to the `struct/` knowledge architecture.


---

## 补充说明：Coq / Isabelle Theorem Proving for Safety-Critical Components

## 概念定义

**定义**：Coq 与 Isabelle/HOL 是基于高阶逻辑的交互式定理证明器，支持从公理出发构造机器可检查的证明，常用于密码学、编译器与安全关键软件的验证。

## 示例

**示例**：使用 Coq 证明 TLS 1.3 握手协议的消息不变式，并将提取的 OCaml 代码集成到可复用加密库，确保实现与规约一致。

## 反例

**反例**：密码库复用某开源实现时未验证其形式化安全规约，后来发现其实现与论文证明的抽象模型存在偏差，导致侧信道攻击。

## 权威来源

> **权威来源**:
>
> - [Coq Proof Assistant](https://coq.inria.fr)
> - [Isabelle/HOL](https://www.cl.cam.ac.uk/research/hvg/Isabelle)
> - 核查日期：2026-07-07

## 分析

**分析**：定理证明提供最高置信度，但门槛高、周期长，适合小规模、高价值核心组件。
