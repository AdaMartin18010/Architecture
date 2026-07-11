# 公理 S.3 信任传递性的 Alloy 形式化验证

> **版本**: 2026-07-12
> **对应规约**: [`trust-transitivity.als`](trust-transitivity.als)
> **对应公理**: S.3 Dependency Transitivity of Trust（[`axiom-system.md`](../../01-meta-model-standards/06-formal-axioms/axiom-system.md) §3）
> **交叉引用**: [`cross-layer-mapping.als`](cross-layer-mapping.als)（S.4 形式化）、[`mcp-tool-graph.als`](mcp-tool-graph.als)（S.3 的 MCP 领域实例）、`struct/10-supply-chain-security/`
> **理论来源**: Jackson, D. *Software Abstractions*; SLSA 1.2; OpenSSF 供应链安全研究

---

## 目录

- [公理 S.3 信任传递性的 Alloy 形式化验证](#公理-s3-信任传递性的-alloy-形式化验证)
  - [目录](#目录)
  - [概念定义](#概念定义)
  - [1. 模型说明](#1-模型说明)
    - [1.1 签名设计](#11-签名设计)
    - [1.2 核心事实：信任闭包 F1](#12-核心事实信任闭包-f1)
    - [1.3 断言设计](#13-断言设计)
  - [2. 验证结果](#2-验证结果)
    - [2.1 机器验证输出](#21-机器验证输出)
    - [2.2 负对照实验](#22-负对照实验)
  - [3. 示例与反例](#3-示例与反例)
    - [3.1 示例：合法依赖链](#31-示例合法依赖链)
    - [3.2 反例：信任盲区（弱化 F1 后 Alloy 检出）](#32-反例信任盲区弱化-f1-后-alloy-检出)
  - [4. 边界条件](#4-边界条件)
  - [5. 与既有规约的关系](#5-与既有规约的关系)
  - [6. 权威来源](#6-权威来源)

## 概念定义

**定义**：信任传递性（Dependency Transitivity of Trust）是公理体系结构性公理 S.3 的核心命题：若组件 A 依赖 B、B 依赖 C，则 A 的信任边界必须扩展至 C；等价地，信任边界是依赖关系的自反传递闭包。本规约用 Alloy 将该命题编码为可机器检验的关系约束，验证"信任边界沿依赖链传递"这一性质在有界实例空间内无反例。

---

## 1. 模型说明

### 1.1 签名设计

```alloy
sig Component {
    depends: set Component,        -- 直接依赖关系（公理中的 →）
    trustBoundary: set Component   -- 信任边界 Trust(c)
}
```

模型刻意保持最小：只有一个签名、两个关系。`depends` 对应公理的依赖箭头 →，`trustBoundary` 对应信任边界函数 Trust。这种"最小充分模型"风格与 `cross-layer-mapping.als` 一致——只捕获公理断言所依赖的结构，不引入无关概念。

### 1.2 核心事实：信任闭包 F1

```alloy
fact TrustClosure {
    all c: Component | c.trustBoundary = c.*depends
}
```

F1 直接采用公理的**等价形式** `Trust(A) = {x : A →* x}`：`*depends` 是 Alloy 的自反传递闭包算子。自反性保证组件自身在边界内，传递性保证任意深度的间接依赖都被纳入信任评估范围——这正是 SLSA 1.2 要求"所有传递依赖都必须进入 SBOM 审计范围"的形式化表达。

### 1.3 断言设计

| 断言 | 内容 | 对应公理表述 |
|------|------|-------------|
| `TrustBoundaryExtends` | A→B ∧ B→C ⇒ Trust(A) ⊇ Trust(B) ∪ Trust(C) | S.3 蕴含形式原文 |
| `TrustIsClosedUnderDependents` | B ∈ Trust(A) ⇒ Trust(B) ⊆ Trust(A) | 传递闭包的单调收缩性质 |

两条断言分工：A1 是公理原文的逐字编码；A2 是闭包定义的推论性质，用于交叉验证 F1 的语义强度。若 F1 仅要求 `trustBoundary ⊇ depends`（超集而非等式），A1 仍可能通过但 A2 失败，因此 A2 能捕获"边界定义过松"的建模缺陷。

---

## 2. 验证结果

### 2.1 机器验证输出

2026-07-12 使用 Alloy Analyzer 6.2.0（org.alloytools.alloy.dist，SAT4J 后端，Java 21）通过 `.tmp/RunAlloy.java` 逐条执行全部命令：

| 命令 | scope | 结果 |
|------|-------|------|
| `check TrustBoundaryExtends` | 5 | **no counterexample found**（断言成立） |
| `check TrustIsClosedUnderDependents` | 5 | **no counterexample found**（断言成立） |
| `run ShowTrustChain` | 5 | **instance found**（事实集可满足） |

`run ShowTrustChain` 找到实例（如链 a→b→c，a.trustBoundary={a,b,c}），证明事实集非空，两条 check 的"无反例"是真实蕴涵而非前提不可满足导致的空虚真。

### 2.2 负对照实验

临时将 F1 弱化为 `trustBoundary = depends`（信任边界仅含直接依赖，丧失传递性）后重跑全部命令：

| 命令 | 弱化后结果 |
|------|-----------|
| `check TrustBoundaryExtends` | **COUNTEREXAMPLE FOUND**（检出反例） |
| `check TrustIsClosedUnderDependents` | **COUNTEREXAMPLE FOUND**（检出反例） |
| `run ShowTrustChain` | instance found |

两条断言在弱化后均被检出反例，证明它们确实依赖 F1 的传递闭包语义——原模型的验证通过不是空虚真。负对照副本存于 `.tmp/trust-transitivity-negctrl.als`（未入库）。

---

## 3. 示例与反例

### 3.1 示例：合法依赖链

**示例**：`run ShowTrustChain` 生成的见证实例——AI 平台依赖链：应用组件 a → 模型库 b → 数值计算库 c，c 无依赖。由 F1 得 Trust(a)={a,b,c}、Trust(b)={b,c}、Trust(c)={c}。逐条核验：A1 中 Trust(b)∪Trust(c)={b,c} ⊆ Trust(a) ✓；A2 中 b ∈ Trust(a) 且 Trust(b)={b,c} ⊆ Trust(a) ✓。该实例对应"审计范围沿依赖链自动扩展"的正确实践。

### 3.2 反例：信任盲区（弱化 F1 后 Alloy 检出）

**反例**：弱化 F1 为 `trustBoundary = depends` 后，Alloy 对 A1 给出反例：a.depends={b}、b.depends={c}，但 Trust(a)={b} 不含 c——即"只审计直接依赖"的团队。这正是 `axiom-system.md` 反模式 2 的形式化再现：AI 平台仅审计直接依赖的模型库 A，未将训练框架 B、数值库 C 纳入信任边界，结果 C 的后门导致推理数据泄露。该反例同时印证 S.3 的**可证伪条件**方向：除非存在"形式化验证的隔离层"（本模型未建模），否则信任不可不传递。

---

## 4. 边界条件

- **有界性**：check 在 scope 5 内验证（最多 5 个组件），依赖链深度 ≤ 4。小范围定理（Small Scope Hypothesis）保证该结论对典型供应链深度有充分覆盖；更深的链不构成新的反例模式（反例必出现在最短违反路径上，长度 ≤ 2）。
- **隔离例外未建模**：S.3 原文可证伪条件提及"形式化验证的隔离层"可使 A 依赖 B 而不继承 B 的信任需求。本规约不建模隔离层——若引入，应增加 `isolated: set Component` 签名并将 F1 修正为 `trustBoundary = c.*depends - isolated.*depends` 之类的形式，A1 也需相应弱化。
- **循环依赖**：模型未禁止 `depends` 成环。环上组件的信任边界因自反传递闭包而相等（互为闭包），A1/A2 仍成立——这符合"循环依赖的组件属于同一信任域"的工程直觉，无需额外约束。
- **与 M.1 的分工**：信任边界是"约束集合"的安全子集（M.1 中 V 的实例），但本规约只验证传递性，不验证约束在上下文中的语义有效性（`⊨` 不可判定，见 `formalization-mapping.md` §3 M.1 行）。

---

## 5. 与既有规约的关系

- [`mcp-tool-graph.als`](mcp-tool-graph.als)：S.3 在 MCP 工具调用图上的**领域实例**（`CapabilityClosure` 断言"被调用工具必须在 Server 能力闭包内"），结构类比信任传递闭包，但不直接编码 Trust 谓词且无机器复验记录；本规约是 S.3 的**公理级**编码，二者互补而非替代。
- [`cross-layer-mapping.als`](cross-layer-mapping.als)：S.4 的公理级形式化（2026-07-12 复验），本规约沿用其"公理原文引用 + check/run + 负对照"的验证范式。
- 公理→规约映射与兑现率统计见 [`formalization-mapping.md`](../../01-meta-model-standards/06-formal-axioms/formalization-mapping.md)。

---

## 6. 权威来源

> **权威来源**:
>
> - [SLSA 1.2 — Supply-chain Levels for Software Artifacts](https://slsa.dev/) — 传递依赖纳入信任评估（核查日期：2026-07-12）
> - [OpenSSF — Open Source Security Foundation](https://openssf.org/) — 供应链安全研究（核查日期：2026-07-12）
> - [Daniel Jackson, Software Abstractions](https://alloytools.org/book/) — 自反传递闭包建模范式（核查日期：2026-07-12）
> - [Alloy Analyzer 6 (org.alloytools.alloy.dist)](https://github.com/AlloyTools/org.alloytools.alloy) — 本次验证所用工具（核查日期：2026-07-12）

---

> 最后更新: 2026-07-12
