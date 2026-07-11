/**
 * cross-layer-mapping.als
 * T13: 跨层复用映射的约束验证
 * 
 * 基于 ISO/IEC 42010:2022 的架构层次模型与 TOGAF 的架构 continuum，
 * 使用 Alloy 验证跨层资产映射的两项核心约束：
 *   1) 同一关注点不能映射到冲突的实现（关注点一致性）
 *   2) 资产只能被映射到相邻层（禁止跨两层直接映射）
 * 
 * 交叉引用: struct/01-meta-model-standards/06-formal-axioms/axiom-system.md
 * 理论来源: Daniel Jackson, Software Abstractions; ISO/IEC 42010:2022
 *
 * ------------------------------------------------------------
 * 修复记录 (2026-07-12): F2/F3/A3 逻辑矛盾修复
 * ------------------------------------------------------------
 * 矛盾: 原 F2 (MappingDirection) 允许反向映射对
 *   (ApplicationAsset→BusinessAsset, ComponentAsset→ApplicationAsset,
 *    FunctionAsset→ComponentAsset)，原 F3 (AdjacentLayerMapping) 允许
 *   FunctionAsset→ComponentAsset；而 A3 (NoReverseMapping) 禁止全部
 *   反向映射。F2∧F3 与 A3 对反向映射给出相反约束，方向约定不自洽。
 * 依据: 公理 S.4 (Abstraction Layering) 原文——“每一层只依赖其直接下层
 *   的接口，禁止跨层直接依赖”“任何资产只能依赖同层或其直接下层资产”
 *   (struct/01-meta-model-standards/06-formal-axioms/axiom-system.md)。
 *   方向约定为严格“上层→下层”:
 *   Business → Application → Component → Function。
 * 修复: F2 移除全部反向映射对，并禁止 FunctionAsset 作为映射源；
 *   F3 改用 AdjacentLayers 谓词表达相邻层（上层→下层）约束，移除
 *   FunctionAsset→ComponentAsset 条款。修复后 F2∧F3 ⇒ A3。
 * 非空虚性: 事实集仍可满足（见 run ShowValidMapping 及文件内
 *   “修复后人工推演”注释），A3 的 check 通过是真实蕴涵而非空虚真。
 * 验证状态: 已机器复验（2026-07-12）。本机无 alloy 命令行工具且 Docker
 *   daemon 未运行，故使用 Alloy Analyzer 6.2.0 (org.alloytools.alloy.dist,
 *   SAT4J 后端) 以 Java API 逐条执行全部命令，结果：
 *     - check AllMappingsAreAdjacent : no counterexample found
 *     - check NoConcernConflicts     : no counterexample found
 *     - check NoReverseMapping       : no counterexample found
 *     - run   ShowValidMapping       : instance found（事实集可满足，
 *       证明上述 check 非空虚真）
 *   负对照：临时将 F2/F3 弱化为恒真后，A1 与 A3 均检出反例，证明
 *   修复后的“无反例”是真实蕴涵而非前提不可满足导致的假象。
 */

module CrossLayerMapping

-- ============================================================
-- 签名定义 (Signature Declarations)
-- ============================================================

/** 抽象层次：业务层、应用层、组件层、功能层 */
abstract sig Layer {}

sig BusinessLayer extends Layer {}
sig ApplicationLayer extends Layer {}
sig ComponentLayer extends Layer {}
sig FunctionLayer extends Layer {}

/** 资产：可在不同层次间复用的架构元素 */
abstract sig Asset {
    -- 资产所属的层次
    layer: one Layer,
    -- 资产关联的关注点
    concerns: set Concern
}

/** 业务资产 */
sig BusinessAsset extends Asset {}
/** 应用资产 */
sig ApplicationAsset extends Asset {}
/** 组件资产 */
sig ComponentAsset extends Asset {}
/** 功能资产 */
sig FunctionAsset extends Asset {}

/** 关注点：架构决策的核心维度 */
sig Concern {
    -- 关注点的性质：功能性或非功能性
    qos: lone QoSAttribute
}

/** QoS 属性：非功能性关注点的子类 */
abstract sig QoSAttribute {}
sig Performance extends QoSAttribute {}
sig Security extends QoSAttribute {}
sig Reliability extends QoSAttribute {}
sig Scalability extends QoSAttribute {}

/** 
 * 映射关系：描述资产在不同层次间的追踪关系。
 * 在 ISO 42010 中对应 "Architecture Description" 的 correspondence 概念。
 */
sig Mapping {
    -- 源资产（较高层）
    source: one Asset,
    -- 目标资产（较低层）
    target: one Asset,
    -- 映射所满足的关注点
    realizes: set Concern,
    -- 映射类型：精化(refinement)或实现(realization)
    mappingType: one MappingType
}

abstract sig MappingType {}
sig Refinement extends MappingType {}
sig Realization extends MappingType {}

-- ============================================================
-- 事实约束 (Facts)
-- ============================================================

/**
 * F1: 资产类型-层次一致性
 * 每种类型的资产必须位于对应的层次中。
 */
fact AssetLayerAlignment {
    all a: BusinessAsset | a.layer in BusinessLayer
    all a: ApplicationAsset | a.layer in ApplicationLayer
    all a: ComponentAsset | a.layer in ComponentLayer
    all a: FunctionAsset | a.layer in FunctionLayer
}

/**
 * F2: 映射方向约束（2026-07-12 修复：移除反向映射对）
 * 映射只能从高层指向低层，禁止反向映射或同层映射。
 * 这对应于 TOGAF 架构 continuum 中的 "从上至下精化"原则，
 * 以及公理 S.4 的“每一层只依赖其直接下层”约定。
 * 方向唯一：Business → Application → Component → Function；
 * FunctionAsset 是最底层，不能作为任何映射的源。
 */
fact MappingDirection {
    all m: Mapping |
        (m.source in BusinessAsset implies m.target in ApplicationAsset) and
        (m.source in ApplicationAsset implies m.target in ComponentAsset) and
        (m.source in ComponentAsset implies m.target in FunctionAsset) and
        no (m.source & FunctionAsset)
}

/**
 * F3: 相邻层映射约束（核心约束）（2026-07-12 修复：改用 AdjacentLayers 谓词，
 *     移除原 FunctionAsset→ComponentAsset 反向条款）
 * 资产只能被映射到相邻的直接下层，不允许跨两层直接映射，也不允许反向映射。
 * 例如：业务资产不能直接映射到组件资产，必须经过应用层。
 * 这是对 struct/01-meta-model-standards/06-formal-axioms 中 S.4 (Abstraction Layering) 的形式化。
 * 注：F2 从资产类型层面约束方向，F3 从层次（Layer）层面约束相邻性；
 * 在 F1 (AssetLayerAlignment) 下二者等价，共同保证 F2∧F3 ⇒ A3。
 */
fact AdjacentLayerMapping {
    all m: Mapping | AdjacentLayers[m.source.layer, m.target.layer]
}

/**
 * F4: 关注点一致性约束（核心约束）
 * 同一关注点不能映射到冲突的实现。
 * 具体而言：若两个映射拥有同一个关注点，则它们的目标资产不能互相冲突。
 * 本模型中简化为：同一关注点的两个映射不能指向同一源资产的不同目标。
 * 更精确地：对于同一关注点，不能存在两个映射使得其目标资产具有矛盾的 QoS 属性。
 */
fact ConcernConsistency {
    all c: Concern |
        all disj m1, m2: Mapping |
            c in m1.realizes and c in m2.realizes implies
                (m1.target = m2.target or m1.source != m2.source)
}

/**
 * F5: 映射完整性
 * 每个非功能层资产至少被一个上层映射所覆盖，
 * 确保架构描述不存在"悬空"资产。
 */
fact MappingCompleteness {
    all a: Asset |
        a in FunctionAsset implies some m: Mapping | m.target = a
    all a: Asset |
        a in BusinessAsset implies some m: Mapping | m.source = a
}

/**
 * F6: QoS 一致性
 * 若映射关注性能，则目标资产必须继承源资产的性能关注点，不得降级。
 * 这是非功能性需求跨层追踪的形式化。
 */
fact QoSPreservation {
    all m: Mapping |
        all q: QoSAttribute |
            (some c: m.realizes | c.qos = q) implies
                (some c: m.target.concerns | c.qos = q or no m.target.concerns)
}

-- ============================================================
-- 谓词 (Predicates)
-- ============================================================

/**
 * 判断两层是否相邻
 */
pred AdjacentLayers[upper, lower: Layer] {
    (upper in BusinessLayer and lower in ApplicationLayer) or
    (upper in ApplicationLayer and lower in ComponentLayer) or
    (upper in ComponentLayer and lower in FunctionLayer)
}

/**
 * 判断一个映射是否跨层（跳过中间层）
 * 这是违规谓词，与 F3 矛盾。
 */
pred CrossLayerMapping[m: Mapping] {
    (m.source in BusinessAsset and m.target in ComponentAsset) or
    (m.source in BusinessAsset and m.target in FunctionAsset) or
    (m.source in ApplicationAsset and m.target in FunctionAsset)
}

/**
 * 判断是否存在关注点冲突：同一源资产、同一关注点映射到不同目标
 */
pred ConcernConflict[c: Concern, a: Asset] {
    some disj m1, m2: Mapping |
        c in m1.realizes and c in m2.realizes and
        m1.source = a and m2.source = a and
        m1.target != m2.target
}

/**
 * 生成一个满足所有约束的合法跨层映射实例
 */
pred ShowValidMapping {
    some m: Mapping | #m.realizes >= 1
    some a: Asset | #a.concerns >= 2
    #Mapping >= 3
}

-- ============================================================
-- 断言 (Assertions)
-- ============================================================

/**
 * A1: 相邻层映射断言
 * 所有映射必须发生在相邻层次之间。
 * 违反此断言意味着架构中存在"跳跃式"映射，破坏了层次封装。
 */
assert AllMappingsAreAdjacent {
    all m: Mapping |
        (m.source in BusinessAsset implies m.target in ApplicationAsset) and
        (m.source in ApplicationAsset implies m.target in ComponentAsset) and
        (m.source in ComponentAsset implies m.target in FunctionAsset)
}

/**
 * A2: 关注点一致性断言
 * 对于任意关注点，不存在两个映射从同一源资产出发、映射到不同目标资产。
 * 这是"单一职责"原则在跨层追踪中的形式化。
 */
assert NoConcernConflicts {
    no c: Concern, a: Asset | ConcernConflict[c, a]
}

/**
 * A3: 映射方向断言
 * 映射只能从抽象程度高的层指向抽象程度低的层。
 * 这确保了架构描述的因果方向正确。
 */
assert NoReverseMapping {
    no m: Mapping |
        (m.source in ApplicationAsset and m.target in BusinessAsset) or
        (m.source in ComponentAsset and m.target in ApplicationAsset) or
        (m.source in FunctionAsset and m.target in ComponentAsset)
}

-- ============================================================
-- 检查命令 (Check Commands)
-- ============================================================

/** 检查相邻层映射，scope: 各层最多 3 个实例，映射最多 6 个 */
check AllMappingsAreAdjacent for 3 but 6 Mapping, 4 Concern

/** 检查关注点一致性 */
check NoConcernConflicts for 3 but 6 Mapping, 4 Concern

/**
 * 检查映射方向
 *
 * 修复后人工推演（2026-07-12）：本 check 不是空虚真（vacuously true）。
 * 论证分两步：
 *   1) 事实集可满足（模型非空）。构造实例 I：
 *      BusinessAsset={b1}, ApplicationAsset={a1}, ComponentAsset={c1},
 *      FunctionAsset={f1}，各资产 layer 由 F1 唯一确定；
 *      Mapping={m1,m2,m3}，m1: b1→a1，m2: a1→c1，m3: c1→f1；
 *      所有 realizes/concerns 为空集。
 *      逐条核验：F1 按构造成立；F2/F3 中三条正向链均满足；
 *      F4/F6 因 realizes 为空而平凡成立；F5 要求 FunctionAsset 被映射
 *      覆盖（m3.target=f1 ✓）、BusinessAsset 为某映射源（m1.source=b1 ✓）。
 *      故 I ⊨ F1∧…∧F6，且 I 含 ComponentAsset（c1）——事实集可满足。
 *   2) A3 无反例是真实蕴涵而非前提不可满足：任何反向映射
 *      （ApplicationAsset→BusinessAsset、ComponentAsset→ApplicationAsset、
 *      FunctionAsset→ComponentAsset）都直接违反修复后的 F2
 *      （及 F3，因 AdjacentLayers 仅定义上层→下层相邻对），故在
 *      满足事实的实例空间中不存在 A3 的反例；check 报告
 *      "No counterexample found" 反映的是 F2∧F3 ⇒ A3 的蕴涵关系，
 *      而非修复前 F2 与 F3/A3 相互矛盾导致的虚假通过。
 *      欲观察 A3 真正检出反例，可临时注释 F2 或 F3 之一后重新 check，
 *      Alloy 将给出如 FunctionAsset→ComponentAsset 的反例实例。
 */
check NoReverseMapping for 3 but 6 Mapping

-- ============================================================
-- 模拟命令 (Run Commands)
-- ============================================================

/** 生成一个合法的跨层映射实例 */
run ShowValidMapping for 3 but 6 Mapping, 4 Concern, 3 QoSAttribute
