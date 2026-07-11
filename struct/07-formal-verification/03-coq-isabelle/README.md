# Coq/Rocq & Isabelle/HOL 可复用组件验证案例

> **定位**：为高安全等级可复用组件提供可运行的形式化验证示例，覆盖函数级正确性与状态不变量。
> **环境**：Rocq 9.0+ / Isabelle2025+；详见 `struct/99-reference/tools/formal-verification-env/`。

---

## 1. 概念定义

**Coq/Rocq** 与 **Isabelle/HOL** 是基于高阶逻辑的交互式定理证明器，支持从公理出发构造机器可检查的证明，常用于密码学、编译器与安全关键软件的验证。

**可复用形式化组件** 是指附带机器检查证明的函数、数据结构或状态机；消费方在满足前置条件的前提下，可直接继承其已证明的正确性性质，无需重新证明。

---

## 2. 目录结构

```text
03-coq-isabelle/
├── README.md                         # 本文件
├── coq-examples/
│   ├── insertion_sort.v              # 插入排序正确性（排序 + 保数）
│   └── bounded_counter.v             # 有界计数器状态不变量
├── isabelle-theories/
│   ├── InsertionSort.thy             # Isabelle 插入排序正确性
│   └── Turnstile.thy                 # 简单状态机（旋转门）不变量
└── ci-workflows.md                   # 待 Phase 2 创建（GitHub Actions / Docker 验证流程）
```

---

## 3. Coq/Rocq 示例

### 3.1 快速验证

```bash
# 使用 Docker
docker run --rm -v "$PWD/coq-examples":/src -w /src rocq/rocq-prover:9.0 \
       rocq compile insertion_sort.v
```

### 3.2 插入排序正确性

文件：`coq-examples/insertion_sort.v`

验证目标：

- `insertion_sort_sorted`：输出列表是有序的。
- `insertion_sort_count`：输出列表是输入列表的排列（通过元素计数不变证明）。

### 3.3 有界计数器不变量

文件：`coq-examples/bounded_counter.v`

验证目标：

- `inc_preserves_invariant`：`value <= limit` 在 `inc` 操作后保持。

这是典型的高安全组件验证模式：**定义不变量 → 证明每个操作保持它**。

---

## 4. Isabelle/HOL 示例

### 4.1 快速验证

```bash
docker run --rm -v "$PWD/isabelle-theories":/project -w /project \
       makarius/isabelle:2025 \
       isabelle build -D .
```

### 4.2 插入排序正确性

文件：`isabelle-theories/InsertionSort.thy`

验证目标：

- `isort_sorted`：`isort xs` 输出有序列表。
- `isort_permutation`：`isort xs` 保持元素多重集不变。

### 4.3 旋转门状态机

文件：`isabelle-theories/Turnstile.thy`

验证目标：

- `ok_step`：若旋转门未锁定且没有报警，则 `Push` 事件不会触发误报警；`Coin` 事件解锁并清除报警。

---

## 5. 正向示例：验证可复用排序组件

以 Coq/Rocq 的 `insertion_sort.v` 为例，该组件附带两个定理：

1. `insertion_sort_sorted`：对任意输入列表，输出为有序列表；
2. `insertion_sort_count`：输出列表与输入列表包含相同元素（多重集相等）。

消费方在复用该排序函数时，无需再次证明排序正确性，只需确保调用参数满足 `list T` 类型前置条件。该证明可被纳入资产目录，作为组件可信度证据。

类似地，Isabelle/HOL 的 `InsertionSort.thy` 提供等价的机器检查证明，展示同一算法在不同证明助理中的可移植表达。

### 5.1 正向示例：CompCert 与 seL4 等高可信复用资产

- **CompCert**（INRIA）使用 Coq/Rocq 证明了 C 语言子集优化编译器的前端到后端正确性，其生成的机器码保留了源程序语义。航空、汽车等高安全领域复用 CompCert 时，可显著降低编译器引入错误的信任假设。
- **seL4**（UNSW/TS）使用 Isabelle/HOL 证明了操作系统微内核的功能正确性与安全性质，成为全球首个通用操作系统内核完整形式化验证案例。seL4 的 proofs 以 AFP/开源形式维护，下游系统复用 seL4 时可将内核安全性质作为可信基。

这些案例说明：定理证明不仅服务于单函数正确性，更可以构建**跨项目继承的复用资产**。

---

## 6. 反例 / 反模式：密码库实现与证明模型脱节

### 反例

某团队复用一个开源密码库时，仅依赖其论文中的形式化安全证明，未验证具体实现是否与证明模型一致。后来发现实现中引入了论文模型未涵盖的侧信道（时序泄漏），导致攻击者可恢复密钥。

该案例说明：

- **形式化证明不能自动覆盖实现层面**；必须建立从规约到代码的追踪关系。
- 复用高安全组件时，应索取并审计 **证明假设（proof assumptions）** 与 **可信计算基（TCB）**。
- 对 Coq/Rocq 提取到 OCaml/Haskell 的代码，需验证提取过程保持语义；对 Isabelle 的 code generation 亦同。

### 6.1 反模式：证明依赖未声明的公理或提取语义不一致

某团队使用 Coq/Rocq 证明了一个关键访问控制策略，但在最终提取为 OCaml 服务时：

1. 规约中使用了 `functional_extensionality` 等公理，未在证据包中声明；
2. 提取后的代码依赖 `ExtrOcamlNatInt` 等外部插件，其语义与证明模型中的归纳类型存在细微差异；
3. 评审方无法复现证明环境（Rocq 8.17 vs 9.0 的 `Stdlib` 重命名导致 `Require Import` 失败）。

结果，形式化证据未能通过独立安全评估。教训：**所有公理、TCB、工具版本和提取配置必须作为证据包的一部分被审计**；复用高安全组件时，消费方应索取 `rocqchk`/proof checksum 及环境锁定文件。

---

## 7. 与 AI 的集成趋势

| 工具 | 用途 |
|------|------|
| **CoqPilot / RocqStar** | LLM 填充 `admit` 证明洞 |
| **Sledgehammer** | Isabelle 自动调用外部 ATP |
| **AutoCorrode** | AWS 开发的 Isabelle LLM 助手 |
| **AutoVerus / AlphaVerus** | Rust/Verus 自动生成证明 |

> **关键洞察（Verina 2025）**：当前 LLM 在“代码+规约+证明”的端到端可验证代码生成上仍只有个位数通过率；**人类写规约 + LLM 辅助证明 + 内核校验** 是最安全的工作流。

---

## 8. 标准条款与工具映射

| 标准 / 条款 | 本目录对应内容 | 工具 | 证据 |
|:---|:---|:---|:---|
| IEEE 1012-2024 §9.5（软件实现 V&V） | 函数级正确性证明 | Coq/Rocq, Isabelle/HOL | `.v` / `.thy` 证明脚本 |
| IEEE 1012-2024 SIL 4 | 高完整性组件验证 | 定理证明器 | 形式化证明证书 |
| DO-178C / DO-333（DAL A） | 航电级软件验证 | SPARK/Ada + Isabelle 辅助 | DO-333 证据包 |
| ISO/IEC 25010:2023（功能正确性） | 排序/计数器等功能正确 | 证明器 + CI | 回归验证报告 |

### 8.1 工具链版本与标准映射

| 工具/组件 | 推荐版本 | 适用标准/场景 | 典型证据 |
|:---|:---|:---|:---|
| Rocq Prover | 9.0+ / Coq 8.20 兼容 | IEEE 1012-2024 §9.5 | `.v` 证明脚本、`rocqchk` 校验 |
| Isabelle/HOL | Isabelle2025 | IEEE 1012-2024 §9.5 | `.thy` 证明脚本、会话记录 |
| SMT 后端 | cvc5 / Z3 / Alt-Ergo | DO-178C / DO-333 | 自动证明步骤日志 |
| Code Extraction | Rocq `Extraction` / Isabelle `code generation` | IEC 61508 SIL 4 | 提取配置与语义一致性审查 |

> **版本提示**：Rocq 9.0 将标准库拆分为 `Corelib` 与 `Stdlib`，并引入单一 `rocq` 二进制；迁移旧 Coq 证明时需更新 `Require` 路径。

---

## 9. 延伸阅读

- Software Foundations: <https://softwarefoundations.cis.upenn.edu/>
- Isabelle Archive of Formal Proofs: <https://www.isa-afp.org/>
- Functional Algorithms Verified: <https://softwarefoundations.cis.upenn.edu/vfa-current/index.html>
- CoqPilot: <https://github.com/JetBrains-Research/coqpilot>
- Verina: <https://arxiv.org/abs/2505.23135>

## 10. 权威来源

| 来源 | URL | 核查日期 |
|:---|:---|:---|
| The Rocq Prover 9.0 (原 Coq) | <https://rocq-prover.org/> | 2026-07-09 |
| Rocq Prover Releases | <https://rocq-prover.org/releases> | 2026-07-09 |
| ANSSI Requirements on the Use of Rocq (CC evaluations) | <https://inria.hal.science/hal-04452421v1/document> | 2026-07-09 |
| Isabelle/HOL | <https://isabelle.in.tum.de> | 2026-07-09 |
| Isabelle2025 Download | <https://isabelle.in.tum.de/index.html> | 2026-07-09 |
| Archive of Formal Proofs (AFP) | <https://www.isa-afp.org/> | 2026-07-09 |
| Software Foundations | <https://softwarefoundations.cis.upenn.edu/> | 2026-07-09 |
| Sledgehammer (Isabelle) | <https://isabelle.in.tum.de/dist/Isabelle2025/doc/sledgehammer.pdf> | 2026-07-09 |

## 11. 交叉引用

- 形式化验证总览：[`struct/07-formal-verification/README.md`](../README.md)
- SPARK/Ada 工业案例：[`struct/07-formal-verification/05-spark-ada/spark-ada-do333-industrial.md`](../05-spark-ada/spark-ada-do333-industrial.md)
- 定理证明指南：[`struct/07-formal-verification/03-coq-isabelle/theorem-proving-guidelines.md`](./theorem-proving-guidelines.md)

> 最后更新：2026-07-09