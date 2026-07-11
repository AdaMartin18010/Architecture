# 公理 E.2 成本-收益阈值的 Alloy 形式化验证

> **版本**: 2026-07-12
> **对应规约**: [`reuse-economics.als`](reuse-economics.als)
> **对应公理**: E.2 Cost-Benefit Threshold（[`axiom-system.md`](../../01-meta-model-standards/06-formal-axioms/axiom-system.md) §2）
> **交叉引用**: [`cross-layer-mapping.als`](cross-layer-mapping.als)（S.4 形式化）、[`trust-transitivity.als`](trust-transitivity.als)（S.3 形式化）、`struct/09-value-quantification/`（价值量化）、[`threshold-registry.yaml`](../../99-reference/tools/threshold-registry.yaml)（阈值登记项 THR-ECON-AAF-FLOOR）
> **理论来源**: Boehm, B. et al. *Software Cost Estimation with COCOMO II*; NASA RRL 实证

---

## 目录

- [公理 E.2 成本-收益阈值的 Alloy 形式化验证](#公理-e2-成本-收益阈值的-alloy-形式化验证)
  - [目录](#目录)
  - [概念定义](#概念定义)
  - [1. 模型说明](#1-模型说明)
    - [1.1 签名与谓词设计](#11-签名与谓词设计)
    - [1.2 整数编码与溢出防护](#12-整数编码与溢出防护)
    - [1.3 断言设计](#13-断言设计)
  - [2. 验证结果](#2-验证结果)
    - [2.1 机器验证输出](#21-机器验证输出)
    - [2.2 负对照实验](#22-负对照实验)
  - [3. 示例与反例](#3-示例与反例)
    - [3.1 示例：理性复用决策](#31-示例理性复用决策)
    - [3.2 反例：负长期价值（弱化 F2 后 Alloy 检出）](#32-反例负长期价值弱化-f2-后-alloy-检出)
  - [4. 边界条件](#4-边界条件)
  - [5. 与既有规约的关系](#5-与既有规约的关系)
  - [6. 权威来源](#6-权威来源)

## 概念定义

**定义**：成本-收益阈值（Cost-Benefit Threshold）是公理体系存在性公理 E.2 的核心命题：复用在经济上合理当且仅当复用成本严格小于自研成本与复用长期价值之和；进一步，当复用成本与自研成本之比（COCOMO II 改编调整因子 AAF）低于阈值 θ=0.7 时，复用是理性选择。本规约用 Alloy 有界整数将两层定义编码为谓词，验证"AAF 阈值判定蕴含经济可行性判定"这一一致性性质无反例。

---

## 1. 模型说明

### 1.1 签名与谓词设计

```alloy
sig ReuseCase { cReuse, cBuild, vReuse: one Int }

pred Viable[r: ReuseCase]   { r.cReuse < r.cBuild.plus[r.vReuse] }   -- E.2 第一式
pred Rational[r: ReuseCase] { r.cReuse.mul[10] < r.cBuild.mul[7] }   -- E.2 第二式（AAF < 0.7）
```

`ReuseCase` 建模对某候选资产的一次复用经济评估，三个字段分别对应公理的 $C_{\text{reuse}}$、$C_{\text{build}}$、$V_{\text{reuse}}$。`Viable` 是 E.2 第一式的逐字编码；`Rational` 是第二式 $\frac{C_{\text{reuse}}}{C_{\text{build}}} < 0.7$ 的等价改写——因 Alloy 整数除法会截断，改用交叉相乘 `C_reuse·10 < C_build·7`（由 F2 保证 $C_{\text{build}}>0$，不等号方向不变）。阈值 0.7 与 [`threshold-registry.yaml`](../../99-reference/tools/threshold-registry.yaml) 登记项 **THR-ECON-AAF-FLOOR**（canonical value 0.7，operator `<`）一致，未引入未登记阈值。

### 1.2 整数编码与溢出防护

Alloy 的 `Int` 是有界位宽整数（本规约用 8-bit，取值 -128..127），溢出会回绕并产生伪反例。为此 F3 将三个量限制在 [0, 12]：

- `cReuse·10 ≤ 120`、`cBuild·7 ≤ 84`、`cBuild+vReuse ≤ 24`，全部落在 8-bit 范围内；
- F1/F2 分别声明 `cReuse ≥ 0`、`cBuild > 0 ∧ vReuse ≥ 0`——后者既是 AAF 比率良定义的前提，也是公理"长期价值"语义的应有之义（价值为负意味着复用造成长期损害，不属 E.2 讨论的复用场景）。

### 1.3 断言设计

| 断言 | 内容 | 验证意图 |
|------|------|---------|
| `RationalImpliesViable` | `Rational[r] ⇒ Viable[r]` | E.2 两层定义的一致性：AAF 阈值判定不会放行经济不可行的复用 |
| `AAFThresholdIsStrict` | 不存在 `cReuse·10 = cBuild·7` 且 `Rational[r]` 的案例 | 阈值严格性（operator `<`）：比率恰为 0.7 时不构成理性选择 |

A1 的推理链：$C_{\text{reuse}} < 0.7 \cdot C_{\text{build}} \le C_{\text{build}} \le C_{\text{build}} + V_{\text{reuse}}$，末步依赖 F2 的 $V_{\text{reuse}} \ge 0$——这也是负对照的切入点。

---

## 2. 验证结果

### 2.1 机器验证输出

2026-07-12 使用 Alloy Analyzer 6.2.0（org.alloytools.alloy.dist，SAT4J 后端，Java 21）通过 `.tmp/RunAlloy.java` 逐条执行全部命令：

| 命令 | scope | 结果 |
|------|-------|------|
| `check RationalImpliesViable` | 3 ReuseCase, 8-bit Int | **no counterexample found**（断言成立） |
| `check AAFThresholdIsStrict` | 3 ReuseCase, 8-bit Int | **no counterexample found**（断言成立） |
| `run ShowRationalReuse` | 3 ReuseCase, 8-bit Int | **instance found**（事实集可满足） |

`run ShowRationalReuse` 找到见证实例（如 cBuild=10, cReuse=6, vReuse=2：60<70 且 6<12），证明事实集非空，两条 check 非空虚真。

### 2.2 负对照实验

临时注释 F2 中的 `vReuse ≥ 0` 后重跑全部命令：

| 命令 | 弱化后结果 |
|------|-----------|
| `check RationalImpliesViable` | **COUNTEREXAMPLE FOUND**（检出反例） |
| `check AAFThresholdIsStrict` | no counterexample found（该断言不依赖 vReuse，符合预期） |
| `run ShowRationalReuse` | instance found |

弱化后 A1 立即检出反例，证明"AAF ⇒ Viable"的成立确实依赖"长期价值非负"这一公理前提；而 A2 不受影响，说明两条断言各自承载了独立的语义——原模型验证通过不是空虚真。负对照副本存于 `.tmp/reuse-economics-negctrl.als`（未入库）。

---

## 3. 示例与反例

### 3.1 示例：理性复用决策

**示例**：某团队评估复用开源消息队列组件：自研成本 $C_{\text{build}}=10$（万人天），复用成本 $C_{\text{reuse}}=6$，长期价值 $V_{\text{reuse}}=2$。AAF = 0.6 < 0.7，且 6 < 10+2——两层判定一致放行，复用是理性且经济可行的选择。对应 `axiom-system.md` 正向示例 2（RabbitMQ→Kafka 切换）的决策依据。

### 3.2 反例：负长期价值（弱化 F2 后 Alloy 检出）

**反例**：弱化 F2 后 Alloy 给出反例：$C_{\text{build}}=10, C_{\text{reuse}}=6, V_{\text{reuse}}=-5$。AAF 判定 60 < 70 通过，但经济可行性 6 ≮ 10+(−5)=5 失败。工程含义：若复用引入长期损害（如绑定即将 EOL 的技术栈，$V_{\text{reuse}}<0$），AAF 比率可能仍"好看"，单看比率会做出错误决策——因此 E.2 的两层定义缺一不可，且 `axiom-system.md` 反模型示例（$C_{\text{reuse}}=600 \not< 400+100$ 的 ERP 复用）正是 A1 结论的反向应用。

---

## 4. 边界条件

- **有界整数近似**：成本/价值以整数人天建模，比率以交叉相乘代替除法。F3 的幅度约束保证无溢出，但也意味着验证域是 [0,12]³——反例若存在必出现在阈值边界（比率接近 0.7）处，该边界已被 scope 覆盖（7/10、5/7 等临界组合均可表示），故小范围验证充分。
- **AAF 单向性**：本规约只验证 `Rational ⇒ Viable`；逆向不成立（Viable 不要求 AAF 达标，如 $V_{\text{reuse}}$ 巨大时）——这是公理原文的语义而非建模缺陷，A1 刻意不写成等价。
- **θ=0.7 是经验值**：阈值来自 COCOMO II/NASA RRL 实证，属可证伪的经验常量（E.2 可证伪条件）。本规约验证的是"给定 θ=0.7 时两层定义的逻辑一致性"，不验证 0.7 本身的正确性；若登记项 THR-ECON-AAF-FLOOR 修订，只需改 `mul[10]/mul[7]` 两个系数。
- **货币量纲**：模型假设三个量同量纲（如人天）。跨量纲比较（如直接成本 vs 机会成本）需先折算，折算模型属 `09-value-quantification` 主题，不在本规约范围。

---

## 5. 与既有规约的关系

- 本规约是继 `cross-layer-mapping.als`（S.4）、`trust-transitivity.als`（S.3）之后第三条公理级 Alloy 形式化，沿用同一验证范式（公理原文引用 + check/run + 负对照 + 机器复验记录）。
- E.2 在统一复用决策栈中定位为 L1 战略判定层，其阈值与决策引擎的登记口径一致性由 [`threshold-registry.yaml`](../../99-reference/tools/threshold-registry.yaml) 保证。
- 公理→规约映射与兑现率统计见 [`formalization-mapping.md`](../../01-meta-model-standards/06-formal-axioms/formalization-mapping.md)。

---

## 6. 权威来源

> **权威来源**:
>
> - [Boehm, B. et al., Software Cost Estimation with COCOMO II](https://csse.usc.edu/tools/cocomoii.php) — AAF 改编调整因子的来源（核查日期：2026-07-12）
> - [NASA Technical Reports Server (NTRS)](https://ntrs.nasa.gov/) — NASA RRL 复用经济实证（核查日期：2026-07-12）
> - [Alloy Analyzer 6 (org.alloytools.alloy.dist)](https://github.com/AlloyTools/org.alloytools.alloy) — 本次验证所用工具（核查日期：2026-07-12）
> - [Daniel Jackson, Software Abstractions](https://alloytools.org/book/) — 有界整数建模与溢出分析（核查日期：2026-07-12）

---

> 最后更新: 2026-07-12
