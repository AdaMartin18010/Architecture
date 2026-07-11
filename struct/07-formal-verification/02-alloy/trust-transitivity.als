/**
 * trust-transitivity.als
 * 公理 S.3 Dependency Transitivity of Trust（信任传递性）的 Alloy 形式化
 *
 * 对应公理原文（struct/01-meta-model-standards/06-formal-axioms/axiom-system.md §3 S.3）:
 *   "若 A 依赖 B，且 B 依赖 C，则 A 的信任边界必须扩展至 C。信任在依赖链上是传递的。"
 *   形式化表述:
 *     A → B ∧ B → C ⇒ Trust(A) ⊇ Trust(B) ∪ Trust(C)
 *     等价地: Trust(A) = {x ∈ C : A →* x}   （→* 为依赖关系的自反传递闭包）
 * 依据: SLSA 1.2 / OpenSSF 供应链安全研究；任何间接依赖都必须纳入信任评估范围。
 *
 * 建模要点:
 *   - 信任边界 Trust(c) 直接按公理的等价形式定义为依赖的自反传递闭包
 *     c.*depends（含 c 自身），保证"任何间接依赖都在信任边界内"。
 *   - 断言 TrustBoundaryExtends 编码公理的蕴含形式：
 *     A→B ∧ B→C ⇒ Trust(A) ⊇ Trust(B) ∪ Trust(C)。
 *   - 断言 TrustIsClosedUnderDependents 编码闭包性质：
 *     信任边界内任一组件的信任边界仍被原边界包含（边界沿依赖链单调收缩）。
 *   - run ShowTrustChain 生成 ≥3 级依赖链实例，证明事实集可满足（非空虚真）。
 *
 * 验证状态: 已机器验证（2026-07-12）。使用 Alloy Analyzer 6.2.0
 *   (org.alloytools.alloy.dist, SAT4J 后端) 以 Java API 逐条执行全部命令，结果：
 *     - check TrustBoundaryExtends        : no counterexample found
 *     - check TrustIsClosedUnderDependents: no counterexample found
 *     - run   ShowTrustChain              : instance found（事实集可满足，
 *       证明上述 check 非空虚真）
 *   负对照：临时将 F1 (TrustClosure) 弱化为 trustBoundary = depends（仅直接依赖）
 *   后，两条 check 均检出反例（形如 A→B→C 但 C ∉ Trust(A)），证明"无反例"
 *   是传递闭包定义的真实蕴涵，而非前提不可满足导致的空虚真。
 */

module TrustTransitivity

-- ============================================================
-- 签名定义 (Signature Declarations)
-- ============================================================

/**
 * 组件：复用/供应链中的依赖单元。
 * depends: 直接依赖关系（对应公理中的 →）。
 * trustBoundary: 信任边界 Trust(c)，由 F1 定义为依赖的自反传递闭包。
 */
sig Component {
    depends: set Component,
    trustBoundary: set Component
}

-- ============================================================
-- 事实约束 (Facts)
-- ============================================================

/**
 * F1: 信任闭包（核心约束，公理 S.3 的等价形式）
 * Trust(A) = {x : A →* x}，即信任边界恰为依赖关系的自反传递闭包。
 * 自反性保证组件自身在边界内（A ∈ Trust(A)），传递性保证
 * 任意深度的间接依赖都被纳入信任评估范围。
 *
 * 负对照弱化点：将 c.*depends 改为 c.depends（仅直接依赖）后，
 * 两条 check 均可检出反例。
 */
fact TrustClosure {
    all c: Component | c.trustBoundary = c.*depends
}

-- ============================================================
-- 谓词 (Predicates)
-- ============================================================

/**
 * 生成一条至少 3 级的真实依赖链实例，证明事实集可满足。
 * 要求链上中间节点的信任边界严格大于其直接依赖集（体现传递性生效）。
 */
pred ShowTrustChain {
    some disj a, b, c: Component |
        b in a.depends and c in b.depends and no c.depends
    some a: Component | #a.trustBoundary >= 3
}

-- ============================================================
-- 断言 (Assertions)
-- ============================================================

/**
 * A1: 信任边界扩展断言（公理 S.3 的蕴含形式）
 * 若 A 依赖 B 且 B 依赖 C，则 Trust(A) ⊇ Trust(B) ∪ Trust(C)。
 * 违反此断言意味着存在"只审计直接依赖、遗漏间接依赖"的供应链盲区
 * （对应 axiom-system.md 反模式 2）。
 */
assert TrustBoundaryExtends {
    all a, b, c: Component |
        (b in a.depends and c in b.depends) implies
            (b.trustBoundary + c.trustBoundary) in a.trustBoundary
}

/**
 * A2: 信任边界闭包断言（传递闭包的单调收缩性质）
 * 信任边界内任一组件的信任边界仍被原边界包含：
 * 沿依赖链越往下，信任边界只会收缩不会扩张。
 */
assert TrustIsClosedUnderDependents {
    all a, b: Component |
        b in a.trustBoundary implies b.trustBoundary in a.trustBoundary
}

-- ============================================================
-- 检查命令 (Check Commands)
-- ============================================================

/**
 * 人工推演（非空虚性论证）：
 *   1) 事实集可满足。构造实例 I：Component={a,b,c}，
 *      a.depends={b}, b.depends={c}, c.depends=∅；
 *      由 F1 得 a.trustBoundary={a,b,c}, b.trustBoundary={b,c},
 *      c.trustBoundary={c}。F1 按构造成立，故 I ⊨ F1，
 *      且 I 正是 run ShowTrustChain 的见证。
 *   2) 两条 check 的无反例是真实蕴涵：F1 将 trustBoundary 绑定为
 *      自反传递闭包，A1/A2 是传递闭包的直接性质；在满足 F1 的
 *      实例空间中不存在反例。欲观察反例，可将 F1 弱化为
 *      trustBoundary = depends 后重新 check（见头部注释负对照记录）。
 */
check TrustBoundaryExtends for 5
check TrustIsClosedUnderDependents for 5

-- ============================================================
-- 模拟命令 (Run Commands)
-- ============================================================

/** 生成一条至少 3 级的依赖链实例（事实集可满足性见证） */
run ShowTrustChain for 5
