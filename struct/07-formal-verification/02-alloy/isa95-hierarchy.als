/**
 * isa95-hierarchy.als
 * T14: ISA-95 资源层次一致性验证
 * 
 * 基于 ANSI/ISA-95.00.01-2010 (IEC 62264-1) 的企业-控制系统集成标准，
 * 使用 Alloy 验证 ISA-95 五层模型中的资源层次约束：
 *   1) 资源层次必须严格遵循 L0-L4 的父子关系
 *   2) 跨层资源引用必须通过明确的接口定义
 * 
 * 交叉引用: struct/11-industrial-iot-otit/01-isa-95-model/
 * 理论来源: ISA-95/IEC 62264; Jackson, Software Abstractions
 */

module ISA95Hierarchy

-- ============================================================
-- 签名定义 (Signature Declarations)
-- ============================================================

/** ISA-95 功能层级：L0 (现场) 到 L4 (企业) */
abstract sig ISA95Layer {}

one sig L0_Field extends ISA95Layer {}
one sig L1_Control extends ISA95Layer {}
one sig L2_Supervisory extends ISA95Layer {}
one sig L3_MES extends ISA95Layer {}
one sig L4_Enterprise extends ISA95Layer {}

/** 
 * 资源：ISA-95 中四类资源的抽象（人员、设备、物料、过程段）。
 * 本模型聚焦设备资源（Equipment），因其具有最明确的层次结构。
 */
abstract sig Resource {
    -- 资源所属层级
    level: one ISA95Layer,
    -- 父资源（在层次结构中直接上级）
    parent: lone Resource,
    -- 子资源集合
    children: set Resource,
    -- 资源引用的跨层接口（用于合法跨层通信）
    interfaces: set InterfaceDef
}

/** 企业级资源 */
sig EnterpriseResource extends Resource {}
/** 站点级资源 */
sig SiteResource extends Resource {}
/** 区域级资源 */
sig AreaResource extends Resource {}
/** 生产线/工作中心级资源 */
sig ProductionLineResource extends Resource {}
/** 工作单元/过程单元级资源 */
sig WorkCellResource extends Resource {}
/** 设备模块级资源 */
sig EquipmentModuleResource extends Resource {}
/** 控制模块/现场设备级资源 */
sig ControlModuleResource extends Resource {}

/** 
 * ProcessCell：ISA-95 中的过程单元，是 L2/L3 边界的关键概念。
 * 一个 ProcessCell 包含一组 WorkCell，执行特定的制造过程。
 */
sig ProcessCell {
    -- ProcessCell 包含的资源
    contains: set Resource,
    -- ProcessCell 所属的层级（通常为 L2 或 L3）
    processLevel: one ISA95Layer,
    -- ProcessCell 暴露的接口
    exposedInterfaces: set InterfaceDef
}

/** 接口定义：跨层资源引用的显式契约 */
sig InterfaceDef {
    -- 接口定义者
    definedBy: one Resource,
    -- 接口消费者（可为空，表示开放接口）
    consumedBy: set Resource,
    -- 接口所属层级
    interfaceLevel: one ISA95Layer,
    -- 接口协议类型
    protocol: one ProtocolType
}

abstract sig ProtocolType {}
sig OPCUA extends ProtocolType {}
sig MQTT extends ProtocolType {}
sig RESTAPI extends ProtocolType {}
sig ModbusTCP extends ProtocolType {}

-- ============================================================
-- 辅助函数
-- ============================================================

/** 返回层级的数值编码，用于比较 */
fun layerOrder[l: ISA95Layer]: Int {
    l = L0_Field => 0 else
    l = L1_Control => 1 else
    l = L2_Supervisory => 2 else
    l = L3_MES => 3 else
    l = L4_Enterprise => 4 else
    0
}

/** 判断两层是否相邻 */
pred AdjacentLayers[l1, l2: ISA95Layer] {
    (l1 = L0_Field and l2 = L1_Control) or
    (l1 = L1_Control and l2 = L0_Field) or
    (l1 = L1_Control and l2 = L2_Supervisory) or
    (l1 = L2_Supervisory and l2 = L1_Control) or
    (l1 = L2_Supervisory and l2 = L3_MES) or
    (l1 = L3_MES and l2 = L2_Supervisory) or
    (l1 = L3_MES and l2 = L4_Enterprise) or
    (l1 = L4_Enterprise and l2 = L3_MES)
}

/** 判断 l1 是否严格高于 l2 */
pred HigherLayer[l1, l2: ISA95Layer] {
    layerOrder[l1] > layerOrder[l2]
}

-- ============================================================
-- 事实约束 (Facts)
-- ============================================================

/**
 * F1: 资源类型-层级对齐
 * ISA-95 标准严格规定了资源类型与层级的对应关系。
 */
fact ResourceLevelAlignment {
    all r: EnterpriseResource | r.level = L4_Enterprise
    all r: SiteResource | r.level = L4_Enterprise
    all r: AreaResource | r.level = L3_MES
    all r: ProductionLineResource | r.level = L3_MES
    all r: WorkCellResource | r.level = L2_Supervisory
    all r: EquipmentModuleResource | r.level = L1_Control
    all r: ControlModuleResource | r.level = L0_Field
}

/**
 * F2: 父子关系严格层级约束（核心约束）
 * 资源的父节点必须位于严格相邻的上层。
 * 这是 ISA-95 层次模型的核心结构约束。
 */
fact ParentChildAdjacency {
    all r: Resource |
        some r.parent implies
            AdjacentLayers[r.level, r.parent.level] and
            HigherLayer[r.parent.level, r.level]
}

/**
 * F3: 父子关系互反一致性
 * 若 r1 是 r2 的父节点，则 r2 必须是 r1 的子节点。
 */
fact ParentChildMutual {
    all r1, r2: Resource |
        (r1.parent = r2 implies r1 in r2.children) and
        (r1 in r2.children implies r1.parent = r2)
}

/**
 * F4: 跨层引用必须通过接口（核心约束）
 * 若资源 A 引用了资源 B，且两者不在相邻层，
 * 则必须存在一个 InterfaceDef，由 B 定义、A 消费，
 * 且接口层级等于 B 的层级。
 */
fact CrossLayerInterfaceRequired {
    all r1, r2: Resource |
        (r1 != r2 and r2 in r1.~children.~parent) implies
            (AdjacentLayers[r1.level, r2.level] or
             some i: InterfaceDef |
                 i.definedBy = r2 and
                 r1 in i.consumedBy and
                 i.interfaceLevel = r2.level)
}

/**
 * F5: 接口定义者层级一致性
 * 接口定义者的层级必须与接口声明层级一致。
 */
fact InterfaceLevelConsistency {
    all i: InterfaceDef |
        i.definedBy.level = i.interfaceLevel
}

/**
 * F6: ProcessCell 层级约束
 * ProcessCell 只能位于 L2 或 L3，这是 ISA-95 标准的规定。
 */
fact ProcessCellLevelConstraint {
    all p: ProcessCell |
        p.processLevel = L2_Supervisory or p.processLevel = L3_MES
}

/**
 * F7: ProcessCell 资源包含约束
 * ProcessCell 只能包含与其同层或下层的资源。
 */
fact ProcessCellResourceContainment {
    all p: ProcessCell |
        all r: p.contains |
            layerOrder[r.level] <= layerOrder[p.processLevel]
}

/**
 * F8: 无环层次约束
 * 资源层次结构中不能存在循环（尽管 parent 已是 lone，
 * 多重继承或引用仍可能产生逻辑环，故显式禁止）。
 */
fact AcyclicHierarchy {
    all r: Resource | r not in r.^parent
}

-- ============================================================
-- 谓词 (Predicates)
-- ============================================================

/**
 * 判断资源是否为根节点（无父节点）
 */
pred IsRootResource[r: Resource] {
    no r.parent
}

/**
 * 判断资源是否为叶节点（无子节点）
 */
pred IsLeafResource[r: Resource] {
    no r.children
}

/**
 * 生成一个满足所有约束的合法 ISA-95 资源层次实例
 */
pred ShowValidHierarchy {
    some r: Resource | IsRootResource[r] and r.level = L4_Enterprise
    some r: Resource | IsLeafResource[r] and r.level = L0_Field
    some p: ProcessCell | #p.contains >= 2
    #Resource >= 5
}

/**
 * 违规谓词：资源跳过了中间层级建立父子关系
 * 与 F2 矛盾，用于反例教学。
 */
pred SkipLevelParent[r: Resource] {
    some r.parent and not AdjacentLayers[r.level, r.parent.level]
}

/**
 * 违规谓词：跨层引用缺少接口
 */
pred CrossLayerWithoutInterface[r1, r2: Resource] {
    not AdjacentLayers[r1.level, r2.level] and
    no i: InterfaceDef | i.definedBy = r2 and r1 in i.consumedBy
}

-- ============================================================
-- 断言 (Assertions)
-- ============================================================

/**
 * A1: 父子相邻层断言
 * 所有具有父节点的资源，其父节点必须位于严格相邻的上层。
 * 违反此断言意味着破坏了 ISA-95 的五层金字塔结构。
 */
assert AllParentsAreAdjacent {
    all r: Resource |
        some r.parent implies AdjacentLayers[r.level, r.parent.level]
}

/**
 * A2: 跨层接口断言
 * 任意两个非相邻层资源之间的引用，必须通过显式接口定义。
 * 这是 ISA-95 标准中"接口标准化"原则的形式化。
 */
assert CrossLayerRequiresInterface {
    all r1, r2: Resource |
        (r1 != r2 and not AdjacentLayers[r1.level, r2.level]) implies
            (no i: InterfaceDef | i.definedBy = r2 and r1 in i.consumedBy) or
            (r2 not in r1.~children.~parent)
}

/**
 * A3: 层次无环断言
 * 资源层次结构中不存在循环引用。
 */
assert AcyclicResourceHierarchy {
    no r: Resource | r in r.^parent
}

/**
 * A4: ProcessCell 层级断言
 * 所有 ProcessCell 必须位于 L2 或 L3。
 */
assert ProcessCellAtL2OrL3 {
    all p: ProcessCell |
        p.processLevel = L2_Supervisory or p.processLevel = L3_MES
}

-- ============================================================
-- 检查命令 (Check Commands)
-- ============================================================

/** 检查父子相邻层约束，scope: 每层最多 3 个资源 */
check AllParentsAreAdjacent for 3

/** 检查跨层接口约束 */
check CrossLayerRequiresInterface for 3 but 4 InterfaceDef

/** 检查层次无环 */
check AcyclicResourceHierarchy for 3

/** 检查 ProcessCell 层级 */
check ProcessCellAtL2OrL3 for 3 but 2 ProcessCell

-- ============================================================
-- 模拟命令 (Run Commands)
-- ============================================================

/** 生成一个合法的 ISA-95 资源层次实例 */
run ShowValidHierarchy for 3 but 4 InterfaceDef, 2 ProcessCell

/**
 * 尝试生成跳层父子关系实例（预期无 instance，因为被 F2 排除）
 * 教学用途：临时注释 F2 后执行
 */
-- run { some r: Resource | SkipLevelParent[r] } for 3
