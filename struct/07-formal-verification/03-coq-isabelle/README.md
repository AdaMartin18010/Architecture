# Coq/Rocq & Isabelle/HOL 可复用组件验证案例

> **定位**：为高安全等级可复用组件提供可运行的形式化验证示例，覆盖函数级正确性与状态不变量。
> **环境**：Rocq 9.0+ / Isabelle2025+；详见 `struct/99-reference/tools/formal-verification-env/`。

---

## 1. 目录结构

```
03-coq-isabelle/
├── README.md                         # 本文件
├── coq-examples/
│   ├── insertion_sort.v              # 插入排序正确性（排序 + 保数）
│   └── bounded_counter.v             # 有界计数器状态不变量
├── isabelle-theories/
│   ├── InsertionSort.thy             # Isabelle 插入排序正确性
│   └── Turnstile.thy                 # 简单状态机（旋转门）不变量
└── ci-workflows.md                   # GitHub Actions / Docker 验证流程
```

---

## 2. Coq/Rocq 示例

### 2.1 快速验证

```bash
# 使用 Docker
docker run --rm -v "$PWD/coq-examples":/src -w /src rocq/rocq-prover:9.0 \
       rocq compile insertion_sort.v
```

### 2.2 插入排序正确性

文件：`coq-examples/insertion_sort.v`

验证目标：

- `insertion_sort_sorted`：输出列表是有序的。
- `insertion_sort_count`：输出列表是输入列表的排列（通过元素计数不变证明）。

### 2.3 有界计数器不变量

文件：`coq-examples/bounded_counter.v`

验证目标：

- `inc_preserves_invariant`：`value <= limit` 在 `inc` 操作后保持。

这是典型的高安全组件验证模式：**定义不变量 → 证明每个操作保持它**。

---

## 3. Isabelle/HOL 示例

### 3.1 快速验证

```bash
docker run --rm -v "$PWD/isabelle-theories":/project -w /project \
       makarius/isabelle:2025 \
       isabelle build -D .
```

### 3.2 插入排序正确性

文件：`isabelle-theories/InsertionSort.thy`

验证目标：

- `isort_sorted`：`isort xs` 输出有序列表。
- `isort_permutation`：`isort xs` 保持元素多重集不变。

### 3.3 旋转门状态机

文件：`isabelle-theories/Turnstile.thy`

验证目标：

- `ok_step`：若旋转门未锁定且没有报警，则 `Push` 事件不会触发误报警；`Coin` 事件解锁并清除报警。

---

## 4. 与 AI 的集成趋势

| 工具 | 用途 |
|------|------|
| **CoqPilot / RocqStar** | LLM 填充 `admit` 证明洞 |
| **Sledgehammer** | Isabelle 自动调用外部 ATP |
| **AutoCorrode** | AWS 开发的 Isabelle LLM 助手 |
| **AutoVerus / AlphaVerus** | Rust/Verus 自动生成证明 |

> **关键洞察（Verina 2025）**：当前 LLM 在“代码+规约+证明”的端到端可验证代码生成上仍只有个位数通过率；**人类写规约 + LLM 辅助证明 + 内核校验** 是最安全的工作流。

---

## 5. 延伸阅读

- Software Foundations: <https://softwarefoundations.cis.upenn.edu/>
- Isabelle Archive of Formal Proofs: <https://www.isa-afp.org/>
- Functional Algorithms Verified: <https://functional-algorithms-verified.org/>
- CoqPilot: <https://github.com/JetBrains-Research/coqpilot>
- Verina: <https://arxiv.org/abs/2505.23135>
