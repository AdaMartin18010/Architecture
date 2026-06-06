/**
 * component-dependency.als
 * T11: 组件依赖无环性验证
 * 
 * 基于 Daniel Jackson《Software Abstractions》的约束求解思想，
 * 使用 Alloy Analyzer 验证组件依赖图中不存在循环依赖。
 * 
 * 交叉引用: struct/04-component-architecture-reuse/
 * 对齐标准: Alloy 6 / Alloy Analyzer (MIT Software Design Group)
 */

module ComponentDependency

-- ============================================================
-- 签名定义 (Signature Declarations)
-- ============================================================

/** 版本标识符，用于追踪组件演进 */
sig Version {
    major: one Int,
    minor: one Int
}

/** 组件：软件复用的基本单元 */
abstract sig Component {
    -- 组件依赖的其他组件集合
    dependsOn: set Component,
    -- 组件所属模块（一个组件最多属于一个模块）
    module: lone Module,
    -- 组件版本
    version: one Version
}

/** 接口定义组件 */
sig Interface extends Component {}

/** 实现类组件 */
sig Implementation extends Component {}

/** 模块：组件的逻辑聚合单元 */
sig Module {
    -- 模块直接包含的组件
    members: set Component,
    -- 模块之间的依赖关系
    imports: set Module
}

/** 系统：顶层容器，包含所有组件和模块 */
sig System {
    components: set Component,
    modules: set Module
}

-- ============================================================
-- 事实约束 (Facts)
-- ============================================================

/** 
 * F1: 模块成员关系一致性
 * 模块的成员必须反向指向该模块，且成员属于系统
 */
fact ModuleMemberConsistency {
    all m: Module | 
        all c: m.members | c.module = m
    all c: Component | 
        some c.module implies c.module.members = c.module.members + c
}

/**
 * F2: 系统封闭性
 * 系统中声明的组件和模块必须自包含
 */
fact SystemClosure {
    all s: System |
        s.components = Component and s.modules = Module
}

/**
 * F3: 依赖图的传递闭包约束
 * 依赖关系必须是良基的 (well-founded)：不存在无限下降链。
 * 在有限模型中等价于禁止循环依赖。
 */
fact AcyclicDependency {
    -- 核心无环约束：任何组件都不能通过依赖链到达自身
    all c: Component | c not in c.^dependsOn
}

/**
 * F4: 模块导入的层次性
 * 模块之间的导入关系也必须是 acyclic 的。
 * 这是组件依赖无环性在更高抽象层的推广。
 */
fact AcyclicModuleImports {
    all m: Module | m not in m.^imports
}

/**
 * F5: 接口-实现分离约束
 * 实现类只能依赖于接口，不能直接依赖于其他实现类
 *（这是组件架构复用中依赖倒置原则的形式化）
 */
fact DependencyInversion {
    all impl: Implementation |
        all dep: impl.dependsOn | dep in Interface
}

-- ============================================================
-- 谓词与函数 (Predicates & Functions)
-- ============================================================

/**
 * 判断两个组件是否处于同一个模块中
 */
pred SameModule[c1, c2: Component] {
    some m: Module | c1 in m.members and c2 in m.members
}

/**
 * 生成一个存在循环依赖的"坏"实例，用于展示反例
 * 注意：此 pred 与 fact AcyclicDependency 矛盾，run 时将得到 no instance
 * 若要观察反例，需临时注释掉 F3 和 F4
 */
pred CyclicDependencyViolation {
    some c: Component | c in c.^dependsOn
}

/**
 * 生成一个合法的系统实例：包含至少一个模块和两个组件
 */
pred ShowValidSystem {
    some m: Module | #m.members >= 2
    some c: Component | #c.dependsOn >= 1
}

-- ============================================================
-- 断言 (Assertions)
-- ============================================================

/**
 * A1: 组件依赖无环性断言
 * 系统中不存在任何组件直接或间接依赖自身的情况。
 * 这是软件架构中最基本的健康约束：循环依赖导致构建不可判定、
 * 测试不可隔离、部署顺序不可确定。
 */
assert NoCircularDependencies {
    no c: Component | c in c.^dependsOn
}

/**
 * A2: 模块导入无环性断言
 * 模块级别的循环导入会导致更严重的架构腐化：
 * 它意味着两个模块在逻辑上不可分离，违反了复用的基本前提。
 */
assert NoCircularModuleImports {
    no m: Module | m in m.^imports
}

/**
 * A3: 依赖局部性断言
 * 组件的依赖对象应当尽可能位于同一模块或低耦合模块中。
 * 若一个组件依赖了不属于同一模块且未被本模块导入的组件，
 * 则构成架构违规（architecture violation）。
 */
assert DependencyLocality {
    all c: Component |
        all dep: c.dependsOn |
            dep in c.module.members or
            dep.module in c.module.imports
}

-- ============================================================
-- 检查命令 (Check Commands)
-- ============================================================

/** 检查组件依赖无环性，scope 为最多 5 个组件实例 */
check NoCircularDependencies for 5

/** 检查模块导入无环性，scope 为最多 4 个模块 */
check NoCircularModuleImports for 4

/** 检查依赖局部性，scope 为 5 个组件 + 3 个模块 */
check DependencyLocality for 5 but 3 Module

-- ============================================================
-- 模拟命令 (Run Commands)
-- ============================================================

/** 生成一个满足所有约束的有效系统实例 */
run ShowValidSystem for 5 but 3 Module

/** 
 * 尝试生成循环依赖违规实例（预期无实例，因为被 fact 排除）
 * 若要观察 Alloy 的反例可视化，可临时注释掉 F3/F4 后执行此命令
 */
-- run CyclicDependencyViolation for 4
