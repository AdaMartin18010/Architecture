# Cargo 依赖解析的 SAT 求解：PubGrub 算法与复用一致性

> **形式化级别**: 严格
> **版本**: 2026-06-06
> **对齐标准**: Rust 1.85+ (PubGrub 解析器), Cargo 1.85+, Semantic Versioning 2.0
> **定位**: 从 SAT 求解角度理解 Cargo 如何保证可复用组件的版本一致性

---

## 目录

- [Cargo 依赖解析的 SAT 求解：PubGrub 算法与复用一致性](#cargo-依赖解析的-sat-求解pubgrub-算法与复用一致性)
  - [目录](#目录)
  - [1. 问题形式化](#1-问题形式化)
  - [2. PubGrub 算法核心逻辑](#2-pubgrub-算法核心逻辑)
    - [2.1 从 CDCL SAT 到版本求解](#21-从-cdcl-sat-到版本求解)
    - [2.2 单元传播：约束推导](#22-单元传播约束推导)
    - [2.3 冲突分析与子句学习](#23-冲突分析与子句学习)
    - [2.4 回溯与决策启发式](#24-回溯与决策启发式)
  - [3. PubGrub 伪代码实现](#3-pubgrub-伪代码实现)
  - [4. 与主流包管理器的解析策略对比](#4-与主流包管理器的解析策略对比)
    - [4.1 npm vs Cargo：统一版本 vs 多版本共存](#41-npm-vs-cargo统一版本-vs-多版本共存)
    - [4.2 Go MVS：极简主义的确定性](#42-go-mvs极简主义的确定性)
    - [4.3 Python uv：Rust 生态的算法反哺](#43-python-uvrust-生态的算法反哺)
  - [5. 复用安全性分析：版本锁定与一致性](#5-复用安全性分析版本锁定与一致性)
    - [5.1 Cargo.lock 作为可复用契约](#51-cargolock-作为可复用契约)
    - [5.2 版本锁定如何保证可复用组件的一致性](#52-版本锁定如何保证可复用组件的一致性)
    - [5.3 攻击面与防御](#53-攻击面与防御)
  - [6. 关键定理与证明概要](#6-关键定理与证明概要)
  - [7. 参考索引](#7-参考索引)

---

## 1. 问题形式化

**定义 D.1** (依赖图): 项目的依赖图 G = (P, E, C) 是一个有向无环图，其中：

- P = {p₁, p₂, ..., pₙ}: 包（crate）的有限集合
- E ⊆ P × P: 依赖边集合，(pᵢ, pⱼ) ∈ E 表示 pᵢ 直接依赖 pⱼ
- C: E → 𝒫(VersionRange): 版本约束映射，为每条边赋予一个版本范围集合

**定义 D.2** (版本解析): 版本解析是函数 σ: P → Version，满足：

$$
\forall (p_i, p_j) \in E: \sigma(p_j) \in C(p_i, p_j)
$$

即对于所有依赖边，被依赖包的版本必须满足约束范围。

**定义 D.3** (统一版本, Unification): Cargo 采用**统一版本**策略：

$$
\forall p_j \in P: |\{ \sigma(p_j) \mid \sigma \text{ 为合法解析} \}| = 1
$$

即对于任何包 pⱼ，整个依赖图中只能使用一个版本。这与 npm 的嵌套多版本策略形成根本对比。

**定义 D.4** (版本选择作为布尔可满足性): 将版本解析编码为 SAT 问题：

- 变量: 对每个包 p ∈ P 和每个可用版本 v ∈ Versions(p)，定义布尔变量 xₚ,ᵥ
- 约束:
  1. **唯一性约束**: ∀p ∈ P: ⨁ᵥ xₚ,ᵥ （恰好选择一个版本）
  2. **依赖约束**: ∀(pᵢ, pⱼ) ∈ E, ∀vᵢ, vⱼ: xₚᵢ,ᵥᵢ ∧ xₚⱼ,ᵥⱼ ⇒ vⱼ ∈ C(pᵢ, pⱼ)
  3. **统一约束**: ∀pⱼ ∈ P, ∀使用 pⱼ 的 pᵢ, pₖ: xₚⱼ,ᵥ 在所有路径上取值一致

**定理 D.1** (Cargo 解析的 NP-完全性): 在一般条件下（允许任意版本范围、特征组合、平台条件），Cargo 的依赖解析问题是 NP-完全的。

*证明概要*: 从 3-SAT 归约。将每个 3-CNF 子句映射为一个包的版本约束，变量赋值映射为版本选择。统一版本策略对应变量的一致性约束。∎

---

## 2. PubGrub 算法核心逻辑

PubGrub 是由 Natalie Weizenbaum 为 Dart 的 Pub 包管理器设计的版本求解算法，其核心是 **Conflict-Driven Clause Learning (CDCL)** SAT 求解技术的领域适配。2026 年，Cargo 已全面采用 PubGrub 作为其依赖解析引擎，取代了早期的回溯求解器。

### 2.1 从 CDCL SAT 到版本求解

标准 CDCL SAT 求解器操作于布尔变量上的 CNF 公式。PubGrub 将这一框架映射到版本求解领域：

| CDCL 概念 | PubGrub 版本求解映射 |
|-----------|---------------------|
| 布尔变量 x | "包 p 选择版本 v" 的赋值决策 |
| 子句 (Clause) | 不兼容性 (Incompatibility): 版本组合的冲突描述 |
| 单元传播 (Unit Propagation) | 约束推导: 若 p@v 被选择，则其依赖必须满足 |
| 冲突分析 (Conflict Analysis) | 从版本冲突中提取根因，构造新的不兼容性 |
| 子句学习 (Clause Learning) | 记录不兼容性到全局集合，永久剪枝搜索空间 |
| 非时序回溯 (Non-chronological Backjumping) | 跳过多余决策层级，直接回溯到冲突相关点 |

**定义 P.1** (不兼容性, Incompatibility): 不兼容性 I 是一个术语集合 {t₁, t₂, ..., tₙ}，每个术语 t 为 "包 p 必须满足约束 c" 或 "包 p 不存在"。I 表示：这些术语不能**同时**为真。即：

$$
\neg(t_1 \land t_2 \land \cdots \land t_n)
$$

等价于子句 (¬t₁ ∨ ¬t₂ ∨ ... ∨ ¬tₙ)。

**定义 P.2** (部分解, Partial Solution): 部分解 S 是一个赋值序列，每个赋值为 "包 p 选择版本 v"，附带推导原因（决策层级）。S 按赋值顺序构成决策层级结构。

### 2.2 单元传播：约束推导

当部分解中确定了某个包的版本后，PubGrub 立即推导该版本引入的约束：

```
给定: 包 p 已选择版本 v
推导:
  1. 读取 p@v 的依赖清单 (manifest)
  2. 对每个依赖 (q, constraint_c):
     - 若 q 尚未赋值: 将 "q 必须满足 c" 加入待满足队列
     - 若 q 已赋值为 v_q: 检查 v_q ∈ c
       * 若 v_q ∉ c: 发生冲突！构造不兼容性
```

形式化地，若 S 中已包含 p@v，且 p@v 依赖于 q ∈ [1.0, 2.0)，则推导出新约束：

$$
S \models (q \geq 1.0 \land q < 2.0)
$$

若后续决策导致 q = 0.9 被选择，则产生冲突，触发冲突分析。

### 2.3 冲突分析与子句学习

当单元传播产生冲突时，PubGrub 执行冲突分析，核心算法为 **Unique Implication Point (UIP)** 分析：

**定义 P.3** (蕴含图, Implication Graph): 蕴含图是一个有向图，节点为赋值决策，边为推导关系。若赋值 A 导致单元传播产生赋值 B，则存在有向边 A → B。

**定义 P.4** (Unique Implication Point): 对于当前决策层级 d 的冲突，UIP 是层级 d 上的一个节点，使得从该决策层级到冲突的所有路径都经过该节点。

冲突分析从冲突节点反向遍历蕴含图，寻找第一 UIP（最接近冲突的 UIP），构造学习子句：

```
ConflictAnalysis(conflict_node):
    // conflict_node 的入边来自层级 d 的多个赋值
    current_set = {冲突相关的所有赋值}

    while current_set 中层级 d 的赋值数量 > 1:
        // 选择最新赋值的节点进行解析
        node = current_set 中层级 d 最新赋值的节点
        // 与 node 的推导原因进行解析 (resolution)
        current_set = current_set ∪ reasons(node) - {node}

    learned_clause = { ¬literal | literal ∈ current_set }
    backtrack_level = max{ decision_level(literal) | literal ∈ learned_clause, level < d }

    return (learned_clause, backtrack_level)
```

**示例**: 假设存在以下依赖关系：

- Root 依赖 A ^1.0, B ^1.0
- A@1.5 依赖 C ^1.0
- B@1.2 依赖 C ^2.0

当 Root 选择 A@1.5 和 B@1.2 后，单元传播推导：

- C 必须满足 ^1.0（来自 A@1.5）
- C 必须满足 ^2.0（来自 B@1.2）

这两个约束互斥，产生冲突。冲突分析构造学习子句：

$$
\neg(A = 1.5) \lor \neg(B = 1.2)
$$

即 A@1.5 与 B@1.2 不兼容。该子句被永久记录，后续求解中若再次遇到 A@1.5 的选择，可直接排除 B@1.2。

### 2.4 回溯与决策启发式

PubGrub 采用**非时序回溯**（Non-chronological Backjumping）：不简单地撤销上一个决策，而是根据学习子句的语义，跳回到导致冲突的最早决策层级。

**决策启发式**（版本选择策略）：

1. **包排序**: 按依赖图拓扑排序，根项目优先，传递依赖次之
2. **版本排序**: 默认按版本号**降序**尝试（优先选择最新兼容版本）
3. **特征偏好**: 最小化启用的特征集合，避免不必要的依赖膨胀

---

## 3. PubGrub 伪代码实现

以下伪代码描述 PubGrub 的核心求解循环，适配 Cargo 的统一版本语义：

```text
算法: PubGrub-Solve
输入: 根项目 Root, 包源 Registry
输出: 版本赋值映射 Solution, 或不可满足报告

// 初始化
Incompatibilities ← ∅                          // 全局不兼容性集合
PartialSolution ← []                           // 部分解（赋值序列）
DecisionLevel ← 0                              // 当前决策层级

// 将根项目作为初始约束
Incompatibilities ← Incompatibilities ∪ { {Root: exists} }

function UnitPropagate():
    while 存在由 PartialSolution 推导出的单元子句:
        term ← 推导出的单元术语
        if term 与 PartialSolution 冲突:
            return CONFLICT(term)
        PartialSolution ← PartialSolution ∪ {term @ DecisionLevel}
    return OK

function ChoosePackage():
    // 选择下一个待决策的包：未赋值、且在未满足术语中出现
    // Cargo 启发式：优先选择约束最紧的包
    candidates ← { p | p 未赋值 ∧ p 出现在未满足术语中 }
    return argmin_{p ∈ candidates} |AvailableVersions(p)|

function ChooseVersion(p):
    // Cargo 默认：优先尝试最新版本
    candidates ← { v ∈ Registry[p] | v 满足所有当前约束 }
    return max(candidates)   // SemVer 降序

// 主循环
while true:
    result ← UnitPropagate()

    if result == CONFLICT(conflict_term):
        if DecisionLevel == 0:
            return UNSAT(生成错误报告(conflict_term))

        // 冲突分析
        (learned_incompatibility, backtrack_level) ←
            ConflictAnalysis(conflict_term, PartialSolution)

        Incompatibilities ← Incompatibilities ∪ {learned_incompatibility}

        // 非时序回溯
        PartialSolution ← 保留至层级 backtrack_level 的赋值
        DecisionLevel ← backtrack_level

        // 将学习的不兼容性加入单元传播队列
        标记 learned_incompatibility 为待推导

    else if 所有包已赋值:
        return SAT(提取版本映射(PartialSolution))

    else:
        // 新决策层级
        DecisionLevel ← DecisionLevel + 1
        p ← ChoosePackage()
        v ← ChooseVersion(p)

        if v == null:
            // 无可用版本，构造存在性不兼容性
            conflict ← { p: 所有约束的合取 }
            标记冲突并继续
        else:
            PartialSolution ← PartialSolution ∪ {p@v @ DecisionLevel}

// 错误报告生成（PubGrub 的核心优势）
function 生成错误报告(conflict_term):
    // 从不兼容性集合构建推导树
    tree ← BuildDerivationTree(conflict_term, Incompatibilities)
    return HumanReadableExplanation(tree)
```

**Cargo 特定扩展**: Rust 1.93（预计 2026 年下半年发布，截至 2026-06-08 尚未发布）的 PubGrub 实现增加了 **MSRV (Minimum Supported Rust Version)** 感知，将 Rust 编译器版本作为额外的约束维度：

$$
\forall p@v \in \text{Solution}: \text{msrv}(p@v) \leq \text{rustc\_version}
$$

---

## 4. 与主流包管理器的解析策略对比

| 维度 | Cargo (PubGrub) | npm (v11) / pnpm | Go Modules (MVS) | Python (uv / Poetry) |
|------|----------------|------------------|------------------|---------------------|
| **算法族** | CDCL SAT | 图遍历 + 严格隔离 | Minimal Version Selection | PubGrub (uv) / resolvelib (pip) |
| **时间复杂度** | NP-完全（实践毫秒级） | 多项式（但可能非终止） | **O(n) 线性** | NP-完全 |
| **版本范围支持** | ✅ `^`, `~`, `>=`, 复杂组合 | ✅ `^`, `~`, 范围 | ❌ 仅最小版本声明 | ✅ `^`, `>=`, 复杂组合 |
| **多版本共存** | ❌ 统一版本 | ✅ npm: 嵌套多版本; pnpm: 严格隔离 | ❌ 单一版本 | ✅ 允许 |
| **冲突检测** | 完备（学习子句剪枝） | 部分（循环依赖检测） | 无冲突（确定性选择） | 完备 (uv) / 启发式 (pip) |
| **错误报告质量** | ⭐⭐⭐⭐⭐ 精确推导树 | ⭐⭐⭐ 基本路径描述 | ⭐⭐⭐⭐ 确定性消息 | ⭐⭐⭐⭐ (uv) / ⭐⭐ (pip) |
| **SemVer 假设** | 软假设（可表达范围限制） | 软假设 | **硬假设**（违反即 bug） | 软假设 |
| **lockfile 确定性** | ✅ Cargo.lock | ✅ package-lock.json / pnpm-lock.yaml | ✅ go.sum | ✅ uv.lock / poetry.lock |
| **供应商化** | ✅ `cargo vendor` | ❌ | ✅ `go mod vendor` | ❌ |

### 4.1 npm vs Cargo：统一版本 vs 多版本共存

npm 采用**嵌套安装**策略：同一包的不同版本可共存于 `node_modules` 的不同层级。这避免了版本冲突的表面现象，但引入了**重复依赖膨胀**和**运行时类型不一致**风险（例如两个版本的 `react` 导致 Hook 状态断裂）。

Cargo 的统一版本策略强制所有依赖协商出单一版本。这要求生态严格遵守 SemVer，但保证了运行时类型一致性——对于 Rust 这种依赖类型系统的语言至关重要。

形式化对比：

- npm: σ: P × Context → Version（版本选择依赖于安装路径上下文）
- Cargo: σ: P → Version（全局函数，无上下文依赖）

### 4.2 Go MVS：极简主义的确定性

Go Modules 的 Minimal Version Selection (MVS) 是唯一提供**线性时间保证**的算法：

$$
\forall p \in P: \sigma_{\text{MVS}}(p) = \max \{ v_{\min}(p, q) \mid (q, p) \in E \}
$$

即对每个包，选择所有依赖方声明的**最小版本中的最大值**。

**优势**: 完全确定性、无解析抖动、O(n) 时间复杂度。

**代价**:

1. 无法表达版本上限（"我需要 X < 2.0"）
2. 若上游违反 SemVer，工具无法保护（Go 的立场是"联系作者修复"）
3. 可能选择过于陈旧的版本（仅满足最小约束，非最新兼容）

### 4.3 Python uv：Rust 生态的算法反哺

uv (Astral, 2026) 使用 `pubgrub-rs` crate 直接实现 PubGrub 算法，是算法跨生态复用的典范。uv 的 lockfile (`uv.lock`) 格式与 Cargo.lock 类似，采用 TOML + SHA-256 哈希。

---

## 5. 复用安全性分析：版本锁定与一致性

### 5.1 Cargo.lock 作为可复用契约

**定义 L.1** (Lockfile 契约): `Cargo.lock` 是一个形式化契约 L = (V, H, S)，其中：

- V: 精确版本映射，V(p) = v
- H: 密码学哈希集合，H(p@v) = sha256(crate_package)
- S: 包源元数据（registry URL、git commit hash 等）

**定理 L.1** (Lockfile 构建确定性): 给定相同的 `Cargo.lock` 和工具链版本，任何环境生成的二进制产物 bit-for-bit 相同（在无编译器非确定性优化时）。

*证明概要*:

1. `Cargo.lock` 固定所有直接和传递依赖的版本
2. SHA-256 哈希验证下载包的完整性
3. 无平台条件导致的隐式版本差异（统一版本策略）
∎

### 5.2 版本锁定如何保证可复用组件的一致性

可复用组件的一致性包含三个层面：

| 一致性层级 | 保证机制 | Cargo 实现 |
|-----------|---------|-----------|
| **语法一致性** | 编译通过 | 统一版本消除类型签名冲突 |
| **语义一致性** | 行为可预测 | Lockfile 固定精确版本 |
| **构建一致性** | 产物可复现 | SHA-256 哈希 + 供应商化 |

**场景分析**: 假设库 `serde v1.0.200` 和 `serde v1.0.210` 在 `Serialize` trait 的实现上有细微行为差异。在 npm 生态中，若依赖树中存在两个版本的 serde，序列化结果可能取决于模块解析路径——这是一种**隐式非确定性**。Cargo 的统一版本强制所有 crate 协商出单一 serde 版本，消除了此类风险。

### 5.3 攻击面与防御

| 攻击向量 | 原理 | Cargo 防御 |
|---------|------|-----------|
| Lockfile 注入 | 篡改 `Cargo.lock` 指向恶意版本 | PR 审查 + CI 中 `cargo vet` 扫描 |
| 哈希碰撞 | 伪造满足 sha256 的恶意包 | SHA-256 抗碰撞性 |
| 传递依赖劫持 | 通过合法包的依赖注入恶意传递包 | `cargo tree` 审查 + `cargo audit` |
| Registry 重放 | 替换 registry 上的历史版本 | crates.io 包不可变性 |

---

## 6. 关键定理与证明概要

**定理 P.1** (PubGrub 完备性): 若存在满足所有约束的版本解析，PubGrub 必能找到；若不存在，必能生成不可满足证明。

*证明概要*:

1. PubGrub 是 CDCL 的领域适配，CDCL 已被证明是可靠的（Sound）和完备的（Complete）
2. 版本求解到布尔 SAT 的编码保持语义等价
3. 学习子句永久剪枝无效搜索空间，不丢弃任何潜在解
4. 决策启发式仅影响效率，不影响完备性 ∎

**定理 P.2** (PubGrub 错误报告最优性): 在不可满足情况下，PubGrub 生成的错误报告是**最小不可满足核心**（Minimal Unsatisfiable Subset, MUS）的人类可读表示。

*证明概要*:

1. 冲突分析通过 UIP 解析构建推导树
2. 推导树的叶节点构成不可满足核心
3. 该核心是最小的：移除任意一个叶节点，约束变为可满足
4. `BuildDerivationTree` 将核心转换为因果链叙述 ∎

**定理 C.2** (Cargo Unification Safety): Cargo 的统一版本策略保证了依赖图中同一 crate 的类型系统一致性，消除了 npm 式多版本冲突。

*证明概要*:

1. 统一版本要求 ∀p ∈ P: |{σ(p)}| = 1
2. Rust 的类型系统基于 crate 边界：`extern crate` 引用的是特定版本的符号
3. 若允许多版本，同一 trait 的不同版本实现将被视为不同类型，导致 trait bound 失效
4. 统一版本消除了此问题，代价是版本协商失败时必须显式报错而非静默使用多版本 ∎

---

## 7. 参考索引

1. Weizenbaum, N. (2018). *PubGrub: Next-Generation Version Solving*. Medium. <https://medium.com/@nex3/pubgrub-2fb6470504f> — PubGrub 算法原始定义
2. `pubgrub-rs` Contributors (2019-present). *pubgrub-rs*. <https://github.com/pubgrub-rs/pubgrub> — Rust 参考实现，被 Cargo 和 uv 复用
3. Freumh, R. (2026). *Package Calculus* — SAT、PubGrub、MVS 的形式化对比
4. Cargo Team, Rust 1.85+ Release Notes — PubGrub 解析器集成与 MSRV 感知
5. crates.io Development Update (2026-01) — Cargo 解析器生产环境部署状态
6. Go Team. *Go Modules: Minimal Version Selection*. <https://go.dev/ref/mod#minimal-version-selection> — MVS 算法规范
7. pip / resolvelib, Python Packaging Authority — pip 依赖解析器实现
8. Astral (2026). *uv: Python Package Manager*. <https://docs.astral.sh/uv/> — PubGrub 跨生态复用案例

---

> **交叉引用**: 本文与 `struct/04-component-architecture-reuse/07-language-ecosystems/comparison-matrix-2026.md` 中"依赖解析算法深度对比"章节互为补充；与 `struct/04-component-architecture-reuse/07-language-ecosystems/open-source-supply-chain-reuse.md` 中"Lockfile 安全属性"分析直接对齐。
>
> 最后更新: 2026-06-06
