# DO-178C MC/DC 的形式化定义与 SPARK 验证

> **版本**: 2026-06-06
> **对齐标准**: DO-178C/ED-12C Table A-7, DO-333/ED-216, MC/DC (Modified Condition/Decision Coverage)
> **定位**: 将结构覆盖率分析从测试执行提升到形式化证明的语义层面

---

## 目录

- [DO-178C MC/DC 的形式化定义与 SPARK 验证](#do-178c-mcdc-的形式化定义与-spark-验证)
  - [目录](#目录)
  - [1. MC/DC 的形式化定义](#1-mcdc-的形式化定义)
    - [1.1 基本定义](#11-基本定义)
    - [1.2 独立影响性语义](#12-独立影响性语义)
    - [1.3 与 DO-178C A 级目标的关联](#13-与-do-178c-a-级目标的关联)
  - [2. SPARK 工具链的 MC/DC 自动生成与验证](#2-spark-工具链的-mcdc-自动生成与验证)
    - [2.1 从契约到判定树](#21-从契约到判定树)
    - [2.2 GNATcoverage 与形式化 MC/DC](#22-gnatcoverage-与形式化-mcdc)
    - [2.3 证明即覆盖](#23-证明即覆盖)
  - [3. 复用安全关键组件时的 MC/DC 意义](#3-复用安全关键组件时的-mcdc-意义)
    - [3.1 组件级 MC/DC 的可传递性](#31-组件级-mcdc-的可传递性)
    - [3.2 契约变更的 MC/DC 影响分析](#32-契约变更的-mcdc-影响分析)
    - [3.3 DO-333 复用策略](#33-do-333-复用策略)
  - [4. 权威来源](#4-权威来源)
  - [补充说明：DO-178C MC/DC 的形式化定义与 SPARK 验证](#补充说明do-178c-mcdc-的形式化定义与-spark-验证)
  - [反例](#反例)
  - [权威来源](#权威来源)

---

## 1. MC/DC 的形式化定义

### 1.1 基本定义

**定义 M.1** (判定与条件): 设布尔表达式 `D = C₁ op C₂ op ... op Cₙ`，其中 `op ∈ {and, or, and then, or else, xor}`，则：

- `D` 称为**判定（Decision）**；
- 每个 `Cᵢ` 称为**条件（Condition）**，可以是布尔变量、关系表达式或嵌套判定。

**定义 M.2** (MC/DC — Modified Condition/Decision Coverage): 对于判定 `D` 中的每个条件 `Cᵢ`，MC/DC 要求存在两个测试用例（或形式化场景），使得：

1. `Cᵢ` 在两个场景中的取值不同（`True` vs `False`）；
2. 除 `Cᵢ` 外的所有其他条件在两个场景中取值相同；
3. 这两个场景导致 `D` 的整体取值不同。

即：`Cᵢ` **独立地影响**了判定 `D` 的结果。

**示例**：考虑飞控软件中的模式切换判定：

```ada
-- 判定：允许进入 Altitude_Hold 模式
Allow_AH := System_OK and then (Alt >= 1000) and then (Alt <= 45000);
```

该判定包含三个条件：`C₁ = System_OK`，`C₂ = (Alt >= 1000)`，`C₃ = (Alt <= 45000)`。

MC/DC 要求为每个条件构造独立影响对：

| 条件 | 场景 1 | 场景 2 | 其他条件固定值 |
|------|--------|--------|---------------|
| `C₁` | T, T, T → T | F, T, T → F | `C₂=T`, `C₃=T` |
| `C₂` | T, T, T → T | T, F, T → F | `C₁=T`, `C₃=T` |
| `C₃` | T, T, T → T | T, T, F → F | `C₁=T`, `C₂=T` |

### 1.2 独立影响性语义

**定义 M.3** (独立影响函数): 设判定 `D` 的条件集合为 `{C₁, ..., Cₙ}`，定义 `Cᵢ` 的独立影响函数为：

```
Indep(Cᵢ, D) ≡ ∃v₁, ..., vₙ, vᵢ', vᵢ'' :
  vᵢ' ≠ vᵢ''
  ∧ D(C₁=v₁, ..., Cᵢ=vᵢ', ..., Cₙ=vₙ) ≠ D(C₁=v₁, ..., Cᵢ=vᵢ'', ..., Cₙ=vₙ)
```

MC/DC 的本质是：对于判定中的每个条件 `Cᵢ`，`Indep(Cᵢ, D)` 必须被证明为真。这意味着每个条件都对判定的输出具有**非冗余的语义贡献**。

在 SPARK 中，这一语义可被表达为契约层面的证明义务。当 GNATprove 分析一个带 `Contract_Cases` 的子程序时，它实际上在验证每种情形下的条件组合是否穷尽且互斥——这正是 MC/DC 的形式化基础。

### 1.3 与 DO-178C A 级目标的关联

DO-178C Table A-7 定义了 A 级软件的结构覆盖率目标[^1]：

| 目标 | 说明 | 传统方法 |
|------|------|---------|
| 目标 1 | 语句覆盖（Statement Coverage）| 测试执行 |
| 目标 2 | 判定覆盖（Decision Coverage）| 测试执行 |
| 目标 3 | MC/DC | 测试执行 |

DO-333 补充件允许在满足以下条件时，用形式化方法替代 MC/DC 测试[^2]：

1. 形式化规范覆盖了判定中的所有条件组合；
2. 证明工具验证了源代码对规范的实现正确性；
3. 形式化分析遍历了所有可能的条件取值路径；
4. 工具链按 DO-330 完成资格认定。

SPARK 的 `Contract_Cases` 和穷尽性检查（exhaustiveness checking）天然满足上述要求。

---

## 2. SPARK 工具链的 MC/DC 自动生成与验证

### 2.1 从契约到判定树

SPARK 子程序的契约可被编译为**判定树（Decision Tree）**，其中每个 `Pre`、`Post` 和 `Contract_Cases` 子句的布尔表达式构成一组判定节点。GNATprove 在生成验证条件（VC）时，会为每个判定节点提取其条件集合。

```ada
procedure Set_Throttle_Command
  (Target_Throttle : in Throttle_Percent;
   Autopilot_On    : in Boolean;
   Emergency_Cutoff: in Boolean;
   Command         : out Throttle_Command)
  with
    Contract_Cases =>
      (Emergency_Cutoff = True => Command = Cutoff,
       Autopilot_On = True and then Emergency_Cutoff = False =>
         Command = Auto (Target_Throttle),
       Autopilot_On = False and then Emergency_Cutoff = False =>
         Command = Manual (Target_Throttle))
    -- 此 Contract_Cases 隐含三个互斥判定的穷尽分析
```

GNATprove 会自动验证：

1. **穷尽性（Exhaustiveness）**：三种情形覆盖了所有可能的输入组合；
2. **互斥性（Disjointness）**：任意输入组合不会同时满足两个以上的情形；
3. **条件独立性**：每个情形中的每个条件都对最终分支选择有独立影响。

这三项验证在语义上等价于 MC/DC 的分析要求。

### 2.2 GNATcoverage 与形式化 MC/DC

AdaCore 的 **GNATcoverage** 工具提供了从源代码到 MC/DC 覆盖率报告的完整工具链。当与 SPARK 结合使用时，其工作流如下[^3]：

```
SPARK 源代码 (Ada/SPARK)
    │
    ├──→ GNATprove（形式化证明）
    │       ├── 生成 Verification Conditions (VCs)
    │       ├── SMT 求解器证明（Alt-Ergo / Z3 / CVC5）
    │       └── 输出：所有路径已覆盖证明
    │
    └──→ GNATcoverage（覆盖率分析）
            ├── 静态分析判定结构
            ├── 提取条件-判定关系
            └── 输出：MC/DC 覆盖率报告
```

**关键优势**：在传统测试中，达到 100% MC/DC 需要精心设计大量测试用例，且无法保证不存在遗漏的边界条件。SPARK + GNATcoverage 的组合通过**符号执行**遍历所有条件组合，在编译期即可生成 MC/DC 的等价证据。

### 2.3 证明即覆盖

**定理 M.1** (Proof implies MC/DC): 若 SPARK 子程序 `P` 的所有验证条件（VCs）被 GNATprove 完全证明，且 `P` 包含 `Contract_Cases` 覆盖其所有输入判定的互斥分支，则 `P` 在语义上满足 MC/DC 要求。

**证明概要**：

1. GNATprove 为 `P` 的每个布尔判定生成 VC，要求证明该判定在所有可能输入下的行为符合契约；
2. 这些 VC 通过 SMT 求解器验证时，求解器隐式遍历了判定的所有条件组合；
3. 若任一条件 `Cᵢ` 对判定 `D` 无独立影响，则存在两个语义等价的分支，GNATprove 的穷尽性检查将报出"不可达分支"或"重叠情形"警告；
4. 因此，无警告的完全证明意味着每个条件都具有独立影响性，即 MC/DC 成立。

> **注意**：上述"证明即覆盖"的论点需经适航当局认可。当前工业实践中，SPARK 证明通常与结构化覆盖率测试结合使用：SPARK 证明覆盖复杂的算术和逻辑路径，测试覆盖编译器相关的目标代码路径。

---

## 3. 复用安全关键组件时的 MC/DC 意义

在安全关键软件的复用场景中，MC/DC 的形式化定义具有以下特殊价值：

### 3.1 组件级 MC/DC 的可传递性

当一个已通过 MC/DC 验证（无论是测试还是形式化证明）的组件 `C` 被复用到新系统 `S` 中时，组件内部的判定结构已被证明满足独立影响性。这意味着：

- **无需重新验证内部逻辑**：`C` 内部的每个条件都已证明对 `C` 的输出有独立语义贡献；
- **接口级 MC/DC 仍需验证**：`S` 调用 `C` 时的外部判定（如 `if C.Ready then C.Activate`）需单独分析；
- **回归风险量化**：若 `C` 的契约在复用时未改变，则其 MC/DC 证据可直接继承。

### 3.2 契约变更的 MC/DC 影响分析

SPARK 的契约驱动方法使得 MC/DC 的回归分析自动化：

```
组件 C 的契约变更 Δ
    │
    ├──→ 若 Δ 仅修改后置条件（输出约束），不影响判定结构
    │       └── 内部 MC/DC 证据保持有效
    │
    ├──→ 若 Δ 修改前置条件（输入约束）或 Contract_Cases
    │       └── GNATprove 重新生成 VC，仅重新验证受影响的判定
    │
    └──→ 若 Δ 引入新条件或重组判定
            └── 需重新运行完整证明流程
```

这种**细粒度影响分析**是传统测试覆盖率工具难以提供的，因为测试用例与源代码判定之间的映射是隐式的，而 SPARK 的契约与判定之间的映射是显式的。

### 3.3 DO-333 复用策略

DO-333 明确支持形式化证据的复用，前提是：

1. 源系统和目标系统的安全等级要求相同或更高；
2. 形式化规范在复用时未发生语义变更；
3. 工具链版本和配置保持一致。

SPARK 组件的 MC/DC 形式化证据（GNATprove 证明日志 + GNATcoverage 分析报告）可作为适航审定包的一部分直接复用，显著降低同类航空电子产品的审定周期和成本。

---

## 4. 权威来源

[^1]: RTCA DO-178C / EUROCAE ED-12C. *Software Considerations in Airborne Systems and Equipment Certification*. RTCA Inc., 2012. Table A-7 定义 A 级软件的结构覆盖率目标，包括 MC/DC。

[^2]: RTCA DO-333 / EUROCAE ED-216. *Formal Methods Supplement to DO-178C and DO-278A*. RTCA Inc., 2012. 第 FM.A-7 节定义形式化方法替代结构覆盖率测试的条件与额外验证目标。

[^3]: AdaCore. *GNATcoverage User's Guide — DO-178C / ED-12C Qualifiable Coverage Analysis*. [https://github.com/AdaCore/gnatcoverage](https://github.com/AdaCore/gnatcoverage). 详细说明 GNATcoverage 的 MC/DC 提取、分析和报告机制。



---

> 最后更新: 2026-06-06


---

## 补充说明：DO-178C MC/DC 的形式化定义与 SPARK 验证

## 反例

**反例**：某航空项目直接复用未经 SPARK 验证的 C 代码到 DO-178C A 级软件，审查阶段因无法提供覆盖率与不变式证据被否决。

## 权威来源

> **权威来源**:
>
> - [SPARK Pro](https://www.adacore.com/sparkpro)
> - [DO-178C](https://www.rtca.org/product/do-178c/)
> - 核查日期：2026-07-07
