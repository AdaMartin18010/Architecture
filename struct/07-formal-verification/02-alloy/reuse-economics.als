/**
 * reuse-economics.als
 * 公理 E.2 Cost-Benefit Threshold（成本-收益阈值）的 Alloy 形式化
 *
 * 对应公理原文（struct/01-meta-model-standards/06-formal-axioms/axiom-system.md §2 E.2）:
 *   "只有当复用成本严格小于自研成本与复用长期价值之和时，复用在经济上才是合理的。"
 *   形式化表述:
 *     EconomicallyViable(a) ⇔ C_reuse(a) < C_build(a) + V_reuse(a)
 *     Reuse(a) 是理性选择 ⇔ C_reuse(a)/C_build(a) < θ   （θ = 0.7，COCOMO II AAF）
 * 阈值口径: struct/99-reference/tools/threshold-registry.yaml 登记项
 *   THR-ECON-AAF-FLOOR（AAF 经济阈值下限，canonical value 0.7，operator "<"，
 *   权威来源 COCOMO II / NASA RRL 实证）。本规约不引入未登记阈值。
 *
 * 建模要点:
 *   - 成本/价值用有界整数建模（见 F3 幅度约束，避免 8-bit Int 溢出回绕）。
 *   - 为避免整数除法，AAF 阈值条件 C_reuse/C_build < 0.7 等价改写为
 *     C_reuse * 10 < C_build * 7（F2 已保证 C_build > 0，交叉相乘保号）。
 *   - 断言 RationalImpliesViable 编码 E.2 两层定义的一致性：
 *     满足 AAF 阈值（理性选择）的复用必然满足经济可行性不等式
 *     （在 V_reuse ≥ 0 下，C_reuse < 0.7·C_build ≤ C_build ≤ C_build + V_reuse）。
 *   - 断言 AAFThresholdIsStrict 编码阈值的严格性（operator "<"）：
 *     C_reuse/C_build 恰好等于 0.7 时不构成理性选择。
 *   - run ShowRationalReuse 生成满足全部事实且被判定为理性选择的实例，
 *     证明事实集可满足（非空虚真）。
 *
 * 验证状态: 已机器验证（2026-07-12）。使用 Alloy Analyzer 6.2.0
 *   (org.alloytools.alloy.dist, SAT4J 后端) 以 Java API 逐条执行全部命令，结果：
 *     - check RationalImpliesViable : no counterexample found
 *     - check AAFThresholdIsStrict  : no counterexample found
 *     - run   ShowRationalReuse     : instance found（事实集可满足，
 *       证明上述 check 非空虚真）
 *   负对照：临时注释 F2 (NonNegativeValue) 后，RationalImpliesViable 检出
 *   反例（如 C_build=10, C_reuse=6, V_reuse=-5：60<70 满足 AAF 但
 *   6 ≮ 10+(-5) 不可行），证明断言依赖"长期价值非负"这一公理前提，
 *   "无反例"是真实蕴涵而非空虚真。
 */

module ReuseEconomics

-- ============================================================
-- 签名定义 (Signature Declarations)
-- ============================================================

/**
 * 复用决策案例：对某个候选资产 a 的一次复用经济评估。
 * cReuse: 复用成本 C_reuse（学习、适配、集成、治理），非负
 * cBuild: 自研成本 C_build，严格为正（作为 AAF 比率的分母）
 * vReuse: 复用长期价值 V_reuse（维护、一致性、速度），非负
 */
sig ReuseCase {
    cReuse: one Int,
    cBuild: one Int,
    vReuse: one Int
}

-- ============================================================
-- 谓词 (Predicates)：E.2 的两层定义
-- ============================================================

/** 经济可行性：C_reuse < C_build + V_reuse */
pred Viable[r: ReuseCase] {
    r.cReuse < r.cBuild.plus[r.vReuse]
}

/**
 * 理性选择（AAF 阈值形式）：C_reuse/C_build < 0.7，
 * 等价改写为 C_reuse * 10 < C_build * 7（C_build > 0 由 F2 保证，保号）。
 */
pred Rational[r: ReuseCase] {
    r.cReuse.mul[10] < r.cBuild.mul[7]
}

-- ============================================================
-- 事实约束 (Facts)
-- ============================================================

/**
 * F1: 复用成本非负
 */
fact NonNegativeReuseCost {
    all r: ReuseCase | r.cReuse >= 0
}

/**
 * F2: 自研成本严格为正、长期价值非负（公理 E.2 的隐含量纲前提）
 * C_build > 0 是 AAF 比率良定义与交叉相乘保号的前提；
 * V_reuse ≥ 0 是 RationalImpliesViable 成立所依赖的公理前提
 * （负对照弱化点：注释 V_reuse ≥ 0 后 check 可检出反例）。
 */
fact PositiveBuildCostAndValue {
    all r: ReuseCase | r.cBuild > 0 and r.vReuse >= 0
}

/**
 * F3: 数值幅度约束
 * 限制各量绝对值 ≤ 12，使 cReuse*10 ≤ 120、cBuild*7 ≤ 84、
 * cBuild+vReuse ≤ 24，均在 8-bit Int（-128..127）范围内，
 * 杜绝有界整数溢出回绕导致的伪反例。
 */
fact BoundedMagnitudes {
    all r: ReuseCase |
        r.cReuse <= 12 and r.cBuild <= 12 and r.vReuse <= 12
}

-- ============================================================
-- 断言 (Assertions)
-- ============================================================

/**
 * A1: E.2 两层定义一致性断言
 * 满足 AAF 阈值（理性选择）的复用必然经济可行：
 *   C_reuse*10 < C_build*7  ⇒  C_reuse < C_build + V_reuse
 * 推理链：C_reuse < 0.7·C_build ≤ C_build ≤ C_build + V_reuse
 * （末步依赖 F2 的 V_reuse ≥ 0）。
 */
assert RationalImpliesViable {
    all r: ReuseCase | Rational[r] implies Viable[r]
}

/**
 * A2: AAF 阈值严格性断言（operator "<" 的形式化）
 * 比率恰好等于 0.7 时不构成理性选择——阈值为严格小于，
 * 与 threshold-registry.yaml 中 THR-ECON-AAF-FLOOR 的 operator "<" 一致。
 */
assert AAFThresholdIsStrict {
    no r: ReuseCase | r.cReuse.mul[10] = r.cBuild.mul[7] and Rational[r]
}

-- ============================================================
-- 模拟命令 (Run Commands)
-- ============================================================

/**
 * 生成一个被判定为理性选择的复用案例实例，证明事实集可满足。
 * 人工推演见证：cBuild=10, cReuse=6, vReuse=2：
 *   F1/F2/F3 成立；Rational: 60 < 70 ✓；Viable: 6 < 12 ✓。
 *   故两条 check 的无反例是真实蕴涵而非空虚真。
 */
pred ShowRationalReuse {
    some r: ReuseCase | Rational[r] and Viable[r]
}

-- ============================================================
-- 检查/模拟命令 (Check & Run Commands)
-- ============================================================

check RationalImpliesViable for 3 but 8 Int
check AAFThresholdIsStrict for 3 but 8 Int
run ShowRationalReuse for 3 but 8 Int
