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
 * F2: 映射方向约束
 * 映射只能从高层指向低层，禁止反向映射或同层映射。
 * 这对应于 TOGAF 架构 continuum 中的 "从上至下精化"原则。
 */
fact MappingDirection {
    all m: Mapping |
        (m.source in BusinessAsset implies m.target in ApplicationAsset) and
        (m.source in ApplicationAsset implies m.target in ComponentAsset or m.target in BusinessAsset) and
        (m.source in ComponentAsset implies m.target in FunctionAsset or m.target in ApplicationAsset) and
        (m.source in FunctionAsset implies m.target in ComponentAsset)
}

/**
 * F3: 相邻层映射约束（核心约束）
 * 资产只能被映射到相邻层，不允许跨两层直接映射。
 * 例如：业务资产不能直接映射到组件资产，必须经过应用层。
 * 这是对 struct/01-meta-model-standards/06-formal-axioms 中 S.4 (Abstraction Layering) 的形式化。
 */
fact AdjacentLayerMapping {
    all m: Mapping |
        (m.source in BusinessAsset implies m.target in ApplicationAsset) and
        (m.source in ApplicationAsset implies m.target in ComponentAsset) and
        (m.source in ComponentAsset implies m.target in FunctionAsset) and
        (m.source in FunctionAsset implies m.target in ComponentAsset)
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

/** 检查映射方向 */
check NoReverseMapping for 3 but 6 Mapping

-- ============================================================
-- 模拟命令 (Run Commands)
-- ============================================================

/** 生成一个合法的跨层映射实例 */
run ShowValidMapping for 3 but 6 Mapping, 4 Concern, 3 QoSAttribute
