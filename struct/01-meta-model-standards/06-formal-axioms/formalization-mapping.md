# 公理→形式化规约映射表

> **版本**: 2026-07-12
> **定位**: 建立公理体系（`axiom-system.md` 15 条命题 + `theorem-derivations.md` 17 条定理）与 `struct/07-formal-verification/` 形式化规约资产之间的完整映射，如实标注每条命题的形式化状态与缺口，消除"形式化验证名实不符"问题
> **方法**: 逐一阅读 `07-formal-verification` 下全部 3 个 `.tla`、4 个 `.als`、2 个 `.v`、2 个 `.thy` 文件的头部注释、断言（assert/check/run）与配套说明文档，核实每个规约实际验证的性质，再与公理/定理陈述比对

---

## 1. 概念定义

**定义**：公理→形式化规约映射是将自然语言/LaTeX 陈述的公理与定理，对应到可被机器检验工具（TLC 模型检验器、Alloy Analyzer、Coq/Rocq、Isabelle/HOL）执行的规约文件的过程。映射状态分三级：

| 标记 | 含义 |
|------|------|
| ✅ 已机器验证 | 存在编码该公理/定理语义的规约文件，且有明确的机器验证记录（工具、版本、日期、结果） |
| 🟡 部分形式化 | 存在结构相关的规约（领域实例化或断言已编写），但未直接编码公理谓词，或缺少机器复验记录 |
| ⬜ 仅自然语言 | 公理/定理仅以自然语言 + LaTeX 陈述，无任何对应规约 |

**重要区分**：`07-formal-verification/` 中的多数规约是**领域案例规约**（支付服务、MCP（Model Context Protocol） 协商、A2A（Agent-to-Agent Protocol） 状态机、ISA-95 层次等），它们演示形式化方法在复用场景中的用法，但**不编码公理体系的命题**。本文件对二者严格区分，不把案例规约计为公理形式化。

---

## 2. 现状统计

| 类别 | 总数 | ✅ 已机器验证 | 🟡 部分形式化 | ⬜ 仅自然语言 |
|------|------|--------------|---------------|---------------|
| 严格公理（M.1–M.4, E.1–E.3, S.1–S.3） | 10 | 0 | 1（S.3） | 9 |
| 工程启发式（S.4, P.1–P.4） | 5 | 1（S.4） | 0 | 4 |
| **命题合计** | **15** | **1** | **1** | **13** |
| 定理（Th.1–Th.17） | 17 | 0 | 0 | 17 |

形式化兑现率：命题 1/15（6.7%）已机器验证，定理 0/17。这与第一轮批判报告（`reports/critical-review-semantic-consistency-2026-07.md` §2.2 "形式化代码零编码公理"）的结论一致；截至 2026-07-12，唯一已机器验证的公理形式化是 S.4（见下表）。

---

## 3. 公理→形式化规约映射表

| 编号 | 陈述摘要 | 形式化状态 | 对应规约文件 | 验证方式 | 缺口说明 |
|------|----------|-----------|--------------|----------|----------|
| M.1 | 架构-复用二元性：复用 ⇔ 约束传递（∃V′⊆V: V′⊨Ctx） | ⬜ | 无 | 无 | `cross-layer-mapping.md` 叙事性引用公理体系，但 `.als` 未编码"约束子集在上下文中语义有效"的谓词；`⊨` 在一阶逻辑中不可判定（见 `critique-and-boundaries.md`），需先给出可操作语义 |
| M.2 | 可变性：复用 ⇔ 共性/变性分离且绑定规则良定义 | ⬜ | 无 | 无 | 无规约建模变体点集 V 与绑定规则 Γ |
| M.3 | 层次不可约：层间不存在保持复用语义的双射 | ⬜ | 无 | 无 | 该命题是元层否定存在性陈述，Alloy/TLA+ 难以直接编码；`cross-layer-mapping.md` 仅叙事提及"与 M.3 一致"；`axiom-rigor-audit.md` 自承当前框架内不可证 |
| M.4 | 同一性保持：复用不改变资产本体标识 | ⬜ | 无 | 无 | 无规约建模 Id 函数与复用链（Th.4 的归纳结构适合 Coq/Isabelle，见路线图） |
| E.1 | 复用资产存在性：稳定 ∧ 通用 ∧ 封装 | ⬜ | 无 | 无 | 三谓词（Stable/General/Encapsulated）均无可操作定义，无法直接编码 |
| E.2 | 成本-收益阈值：C_reuse < C_build + V_reuse | ⬜ | 无 | 无 | 数值不等式本身易编码，但成本/价值量纲与 AAF 阈值口径跨文档不统一（批判报告 §4.2：AAF 五套口径），需先收口阈值注册表 |
| E.3 | 上下文适配性：Reuse ⇒ Fit ≥ τ | ⬜ | 无 | 无 | Fit 函数无可操作定义（`critique-and-boundaries.md` 自承），权重 w₁/w₂/w₃ 无校准来源 |
| S.1 | 接口可替换性：可观察行为等价 ⇔ 可替换 | ⬜ | 无 | 无 | `component-dependency.als` 验证的是依赖无环与依赖倒置，**不是**可观察行为等价；Obs 函数未在任何规约中编码 |
| S.2 | 组合性：局部正确 + 接口兼容 ⇒ 组合满足弱化规约 | ⬜ | 无 | 无 | `theorem-proving-guidelines.md` 将 Assume-Guarantee 作为指导思想引用，但无规约编码组合算子 ∘_I |
| S.3 | 信任传递性：Trust(A) ⊇ 依赖闭包 | 🟡 | [`mcp-tool-graph.als`](../../07-formal-verification/02-alloy/mcp-tool-graph.als) | Alloy（断言已编写：**无机器复验记录**） | `CapabilityClosure`/`CapabilityContainment` 验证"被调用工具必须在 Server 能力闭包内"，是依赖闭包性质的领域实例（MCP 工具调用图），结构类比信任传递闭包，但未直接编码 Trust 谓词；且 `check` 命令未见 TLC/Alloy 复验记录 |
| S.4（启发式） | 抽象分层：资产只能依赖同层或直接下层 | ✅ | [`cross-layer-mapping.als`](../../07-formal-verification/02-alloy/cross-layer-mapping.als) | Alloy Analyzer 6.2.0（SAT4J），2026-07-12 机器复验 | 三条 check（`AllMappingsAreAdjacent`/`NoConcernConflicts`/`NoReverseMapping`）均无反例，`run ShowValidMapping` 可生成实例（非空虚真），负对照实验确认修复有效。另：[`isa95-hierarchy.als`](../../07-formal-verification/02-alloy/isa95-hierarchy.als) 是分层思想在 ISA-95 的领域实例（相邻层父子约束），🟡 辅助，无机器复验记录 |
| P.1（启发式） | 演化独立性：资产生命周期不受单一消费者绑架 | ⬜ | 无 | 无 | 生命周期状态机可建模（TLA+ 适合），但无对应规约 |
| P.2（启发式） | 反馈收敛：改进须经治理函数过滤 | ⬜ | 无 | 无 | 依赖 Th.13 的不动点语义，而 Th.13 证明待补强（见 §5） |
| P.3（启发式） | 治理复杂度定律：G(N) = k·N·log(N) | ⬜ | 无 | 无 | log 底未指定（`axiom-system.md`），影响 Th.14 的 Lambert W 推导口径 |
| P.4（启发式） | 学习曲线单调性：Learn(a,n+1) ≤ Learn(a,n) | ⬜ | 无 | 无 | 单调数列性质适合 Coq/Isabelle 编码，但无对应规约 |

---

## 4. 定理→形式化规约映射表

全部 17 条定理均为 ⬜（仅自然语言 + 证明草图），无任何机器验证。下表给出每条定理的证明状态、最适合的形式化工具与主要缺口。

| 编号 | 名称（依赖公理） | 形式化状态 | 对应规约文件 | 验证方式 | 缺口说明 |
|------|------------------|-----------|--------------|----------|----------|
| Th.1 | 约束保持定理（M.1） | ⬜ | 无 | 无 | **证明待补强**（见 §5.1）：第 4 步"无共享约束即矛盾"无公理支持，第 5 步在"蕴含"语义下子集不保真 |
| Th.2 | 变体闭包定理（M.2） | ⬜ | 无 | 无 | 上界 `|Ctx|^|V|` 的基数论证可在 Coq/Isabelle 中形式化（有限集势），前提需 Γ 为全函数 |
| Th.3 | 层次失败独立性（M.3） | ⬜ | 无 | 无 | 加权可靠性模型 `(1-p)^w` 对非整数 w 需实分析；且隐含"层间失败独立"假设未声明（`theorem-derivations.md` §8.1 自承共因故障时仅为下界） |
| Th.4 | 同一性追溯定理（M.4） | ⬜ | 无 | 无 | 对链长 n 的数学归纳，结构清晰，**最适合优先机械化**（Coq/Isabelle） |
| Th.5 | 资产存在必要性（E.1） | ⬜ | 无 | 无 | 逆否命题直接由 E.1 等价式得到，逻辑 trivial；前提是 E.1 三谓词可判定 |
| Th.6 | 复用经济可行性定理（E.2） | ⬜ | 无 | 无 | 代数推导正确（C_build>0 除法保号）；但 AAF 阈值口径需与全库统一（批判报告 §4.2） |
| Th.7 | 适配边界定理（E.3） | ⬜ | 无 | 无 | 指数衰减模型是外加假设（非 E.3 推论），定理实质是"模型条件下的推论"，应标注条件定理 |
| Th.8 | 可替换性传递性（S.1） | ⬜ | 无 | 无 | 等价关系三性质由 Obs 等式直接得到，**适合优先机械化**（Coq/Isabelle，数十行可完成） |
| Th.9 | 组合结合律（S.2） | ⬜ | 无 | 无 | "弱化操作可交换"（第 6 步）依赖 φ₁∩φ₂=∅ 的具体语义，需先形式化 ∘ 与 ↓_φ |
| Th.10 | 信任边界扩展定理（S.3） | ⬜ | 无 | 无 | 几何级数下界假设依赖树正则（平均分支因子 b̄ 每层恒定），实际依赖图不满足，宜改述为期望意义 |
| Th.11 | 接口稳定性定律（S.4）[条件定理] | ⬜ | 无 | 无 | 传导模型 λ_i = λ_i^local + p·λ_{i-1} 是外加假设；结论是"越上层变更越频繁"（λ_i ≥ λ_{i-1}），与标题"越底层越稳定"一致但证明中单调方向表述需统一 |
| Th.12 | 演化独立性推论（P.1）[启发式推论] | ⬜ | 无 | 无 | "节奏不可近似整除同步"条件过强：几乎所有实数比都满足，定理信息量低，建议改述为概率度量形式 |
| Th.13 | 反馈收敛定理（P.2） | ⬜ | 无 | 无 | **证明待补强**（见 §5.2）：未定义完备度量空间；𝒢 的类型从 (Feedback, Strategy) 滑变为资产自映射；"不动点=最优稳定形态"无依据 |
| Th.14 | 治理崩溃阈值（P.3）[条件定理] | ⬜ | 无 | 无 | Lambert W 推导正确（以自然对数计）；但 P.3 的 log 底未指定，底变化会改变 k 的口径 |
| Th.15 | 专家悖论定理（P.4） | ⬜ | 无 | 无 | Search 函数未定义；"候选集更大 ⇒ 搜索更慢"依赖 overchoice 效应，是经验陈述非逻辑推论 |
| Th.16 | 组合风险叠加定理（S.2+S.3） | ⬜ | 无 | 无 | 下界公式中 α^depth 的放大机制是假设；"风险非独立故实际风险不低于下界"的论证方向需核实（非独立可能使联合风险低于独立情形） |
| Th.17 | 认知-治理双重约束（P.3+P.4）[条件定理] | ⬜ | 无 | 无 | min 组合直接由 Th.14 + P.4 得到，逻辑成立；依赖 Th.14 的口径统一 |

---

## 5. 定理证明漏洞核实（Th.1 / Th.13）

应第一轮批判报告（`reports/critical-review-semantic-consistency-2026-07.md` §2.2）的指控，本节逐条核实。

### 5.1 Th.1 约束保持定理 —— 漏洞成立，标注"证明待补强"

**指控**：由 `V₁⊨Ctx₁`、`V₂⊨Ctx₂` 不能推出 `(V₁∩V₂)⊨Ctx₁ ∧ (V₁∩V₂)⊨Ctx₂`，第 4–5 步循环论证。

**核实结论**：成立。具体缺口两处：

1. **第 4 步无公理支持**：证明断言"若 V₁∩V₂=∅，则与'同一架构复用'的定义矛盾"。但 M.1 仅保证对每次复用**各自存在**见证子集 V₁、V₂，并未公理化"同一架构的两次复用必须共享非空约束子集"——该断言实质就是定理结论本身，构成循环论证。反例：同一支付架构在电商上下文复用"限流+幂等"约束，在政务上下文复用"审计+留痕"约束，两者交集为空，并不与 M.1 矛盾。
2. **第 5 步子集不保真（依 ⊨ 的语义而定）**：若 `V′⊨Ctx` 读作"V′ 蕴含/满足上下文的要求"（与 §7.1"复用判定约化为 CSP"的读法一致），则子集蕴含更弱，`V₁∩V₂⊨Ctx₁` 不成立；仅当 `⊨` 读作"V′ 中每条约束在 Ctx 中有效"（子集单调）时第 5 步才成立，但此时定理退化为空虚真（取 V′=∅ 恒可满足），丧失"约束保持一致"的信息量。

**补强方向**：二选一——(a) 增加公理/定义"同一架构复用 ≡ 存在非空共享约束子集"，使第 4 步成为定义展开；(b) 将结论弱化为"存在（可能为空的）最大共享约束子集 V₁∩V₂，且其在子集单调语义下于两上下文均有效"，并明确 ⊨ 的语义。

### 5.2 Th.13 反馈收敛定理 —— 漏洞成立，标注"证明待补强"

**指控**：套用 Banach 不动点定理却未定义度量空间、未证压缩映射。

**核实结论**：成立（定理作为**条件命题**可挽救，但当前证明缺三个前提）。具体缺口：

1. **完备度量空间未定义**：Banach 不动点定理要求 (X, d) 为完备度量空间。资产空间 𝒜 的度量 d（何为两个资产之间的距离）从未定义，完备性更无从谈起。
2. **𝒢 的类型滑变**：P.2 中 𝒢 的签名是 `Change(a, t+δ) = 𝒢(Feedback(a, t), Strategy(a))`，输入是反馈与策略；证明第 4 步却写迭代 `a_{t+1} = 𝒢(a_t)`，把 𝒢 当作资产空间上的自映射。需显式构造 `𝒢̃(a) = 𝒢(Feedback(a, t), Strategy(a))` 并假设反馈仅依赖当前资产状态，压缩性才谈得上。
3. **"不动点 = 最优稳定形态"无依据**：Banach 定理只给出唯一不动点与收敛性，不保证任何最优性。"最优"是外加解释，应删除或另立命题。

**补强方向**：增补三条前提（资产空间配备完备度量；反馈是资产状态的函数从而 𝒢̃ 为自映射；𝒢̃ 是 Lipschitz 常数 L<1 的压缩映射），并将结论限定为"迭代收敛到唯一不动点"，删去"最优"表述。Th.13 在 `theorem-derivations.md` 中已按此加注。

---

## 6. 形式化规约资产清单（实际验证内容核实）

以下是对 `07-formal-verification/` 全部规约文件实际验证内容的核实结果（依据各文件头部注释与 assert/check/run 命令），用于防止把案例规约误计为公理形式化。

| 规约文件 | 实际验证的性质 | 与公理体系的关系 |
|----------|----------------|------------------|
| [`payment-service.tla`](../../07-formal-verification/01-tla-plus/payment-service.tla) | 资金守恒、无双花、Committed 金额为正等 5 条不变量 + 1 条活性 | 案例规约，非公理形式化 |
| [`mcp-capability-negotiation.tla`](../../07-formal-verification/01-tla-plus/mcp-capability-negotiation.tla) | Active 时能力交集非空、协议版本一致等 5 条不变量 + 2 条活性 | 案例规约，非公理形式化 |
| [`a2a-task-lifecycle.tla`](../../07-formal-verification/01-tla-plus/a2a-task-lifecycle.tla) | 终止态无消息、Completed 必有 Artifact、状态转移合法等 5 条不变量 + 2 条活性 | 案例规约，非公理形式化 |
| [`component-dependency.als`](../../07-formal-verification/02-alloy/component-dependency.als) | 组件依赖无环、模块导入无环、依赖局部性、依赖倒置 | 案例规约；DIP 与 S.1 语义不同，不计入 |
| [`cross-layer-mapping.als`](../../07-formal-verification/02-alloy/cross-layer-mapping.als) | 跨层映射相邻性、关注点一致性、无反向映射 | ✅ S.4 的形式化（2026-07-12 机器复验） |
| [`isa95-hierarchy.als`](../../07-formal-verification/02-alloy/isa95-hierarchy.als) | ISA-95 资源层次相邻性、无环、跨层须经接口 | 🟡 S.4 的工业领域实例，无机器复验记录 |
| [`mcp-tool-graph.als`](../../07-formal-verification/02-alloy/mcp-tool-graph.als) | 工具调用无环、能力闭包容纳、资源访问边界 | 🟡 S.3 的领域实例（能力闭包≈依赖闭包），无机器复验记录 |
| [`insertion_sort.v`](../../07-formal-verification/03-coq-isabelle/coq-examples/insertion_sort.v) | 插入排序输出有序且为输入的排列 | 教学示例，非公理形式化 |
| [`bounded_counter.v`](../../07-formal-verification/03-coq-isabelle/coq-examples/bounded_counter.v) | 有界计数器 inc 保持不变量 value ≤ limit | 教学示例，非公理形式化 |
| [`InsertionSort.thy`](../../07-formal-verification/03-coq-isabelle/isabelle-theories/InsertionSort.thy) | Isabelle 版插入排序正确性 | 教学示例，非公理形式化 |
| [`Turnstile.thy`](../../07-formal-verification/03-coq-isabelle/isabelle-theories/Turnstile.thy) | 旋转门状态机 ok 不变量在 step 后保持 | 教学示例，非公理形式化 |

另注：`01-tla-plus/case-library.md` 列出的 T10 案例 `plcopen-motion.tla` 实际位于 `struct/11-industrial-iot-otit/04-plcopen-motion/`，不属本主题目录；`theorem-proving-guidelines.md` 引用的"F.1 Formal Verification Trust Transfer"属另一公理命名空间（非 M/E/S/P 体系），不计入本映射。

---

## 7. 缺口分析

1. **元公理层（M.1–M.4）全部未形式化**：M.1 的 `⊨`、M.3 的否定存在性、M.4 的 Id 函数均缺可操作语义，是形式化的最大障碍；其中 M.3 在 `axiom-rigor-audit.md` 中已自承"当前框架内不可证"。
2. **存在性公理（E.1–E.3）依赖未定义原语**：Stable/General/Encapsulated/Fit 等谓词无量化定义，编码前需先补原语定义（呼应批判报告 Phase 3 的"补全核心原语精确定义"任务）。
3. **结构性公理仅 S.4 兑现、S.3 半兑现**：S.1（可观察行为等价）和 S.2（Assume-Guarantee 组合）是形式化方法的经典可编码对象（迹等价、契约组合），却无任何规约，是性价比最高的补强方向。
4. **定理层 0/17**：最易机械化的 Th.4（归纳）、Th.8（等价关系）尚未做；Th.1/Th.13 证明有漏洞（§5），Th.12/Th.15/Th.16 含未声明的经验假设。
5. **验证记录缺失**：除 `cross-layer-mapping.als` 外，其余 3 个 `.als` 与 3 个 `.tla` 均无 TLC/Alloy 复验记录（工具版本、日期、结果），"已验证"无法复核。
6. **教学示例未标注**：Coq/Isabelle 四个文件此前未声明"非公理形式化"，易被误读为公理兑现（已于 2026-07-12 在文件头部与 README 补注）。

---

## 8. 形式化路线图建议

| 阶段 | 任务 | 目标产出 | 对齐 |
|------|------|----------|------|
| 近期（2026-Q3） | ① 用 TLC 跑通 3 个 `.tla`、用 Alloy Analyzer 复验其余 3 个 `.als`，把工具版本/日期/结果写回各文件头部；② 为 S.1 编写 Alloy 规约（有限迹集上的可观察行为等价 ⇒ 可替换关系为等价关系，顺带机械化 Th.8 的结构版） | 验证记录全覆盖；S.1 进入 ✅/🟡 | 批判报告 Phase 4 |
| 中期（2026-Q4） | ① 用 Coq 或 Isabelle 机械化 Th.4（复用链同一性归纳）与 Th.8（等价关系三性质），替换教学示例的地位或并列存放；② 按 §5 补强 Th.1/Th.13 证明并复验；③ 统一 P.3/Th.14 的 log 底与 k 口径 | 定理实现 2–4/17 机器验证 | 批判报告 Phase 4 |
| 长期（2027，与 `critique-and-boundaries.md` 的 2027-Q4 计划对齐） | ① 补全原语定义（约束 V、复用语义、层次 L、Trust 取值空间）；② M.1 的 CSP 弱形式编码；③ M.4 + Th.4 的 SBOM 同一性追踪实例（与主题 10 联动） | 元公理层实现弱形式机器验证 | `critique-and-boundaries.md:429` |

---

## 9. 示例与反例

**示例**：名实相符的标注范式——`cross-layer-mapping.als` 头部明确写出"依据公理 S.4 原文"并记录修复矛盾的过程、Alloy Analyzer 6.2.0 复验结果与负对照实验——公理引用、规约断言、机器验证记录三者闭环，是后续形式化工作的范式。

**反例**：名实不符的标注——若把 `payment-service.tla`（资金守恒不变量）描述为"E.2 成本-收益阈值的形式化验证"，即为典型名实不符——该规约与 E.2 无任何语义联系。同理，把 `insertion_sort.v` 计入"公理体系已机器验证"会虚增兑现率。本文件 §6 的资产清单即为防止此类误计。

---

## 10. 权威来源

> **权威来源**:
>
> - [Leslie Lamport, Specifying Systems: The TLA+ Language and Tools](https://lamport.azurewebsites.net/tla/book.html) — TLA+ 与 TLC 模型检验（核查日期：2026-07-12）
> - [Daniel Jackson, Software Abstractions: Logic, Language, and Analysis](https://alloytools.org/book/) — Alloy 关系逻辑与小范围分析（核查日期：2026-07-12）
> - [Alloy Analyzer 6 (org.alloytools.alloy.dist)](https://github.com/AlloyTools/org.alloytools.alloy) — 本次 S.4 复验所用工具（核查日期：2026-07-12）
> - [The Rocq Prover (formerly Coq)](https://rocq-prover.org/) — 交互式定理证明（核查日期：2026-07-12）
> - [Isabelle/HOL](https://isabelle.in.tum.de/) — 高阶逻辑定理证明（核查日期：2026-07-12）
> - Banach, S. (1922). Sur les opérations dans les ensembles abstraits. *Fundamenta Mathematicae*, 3, 133-181 — Th.13 核实所依据的不动点定理原始形式
>
> **核查日期**：2026-07-12

---

## 11. 交叉引用

- [形式化公理体系](axiom-system.md) — 15 条命题的原始陈述
- [定理推导集](theorem-derivations.md) — 17 条定理及其证明（Th.1/Th.13 已加"证明待补强"标注）
- [公理严谨性审计](axiom-rigor-audit.md) — 71 条命题逐条分级
- [批判与边界](critique-and-boundaries.md) — 公理的认识论局限与不可判定性自陈
- [07 形式化验证主题 README](../../07-formal-verification/README.md)
- [Coq/Isabelle 案例 README](../../07-formal-verification/03-coq-isabelle/README.md) — 教学示例定位说明
- [跨层映射 Alloy 规约说明](../../07-formal-verification/02-alloy/cross-layer-mapping.md) — S.4 形式化的修复与复验记录
- [第一轮批判报告](../../../reports/critical-review-semantic-consistency-2026-07.md) — "形式化兑现"问题的原始审查（§2.2）

> 最后更新: 2026-07-12
