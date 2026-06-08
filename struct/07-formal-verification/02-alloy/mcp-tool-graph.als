/**
 * mcp-tool-graph.als
 * T12: MCP Tool 能力依赖图验证
 * 
 * 基于 Model Context Protocol (MCP) 2025-11-25 规范中的工具能力模型，
 * 使用 Alloy 验证 MCP Server 内 Tool 调用的结构约束：
 *   1) 工具依赖图中不存在循环调用
 *   2) 每个被调用的 Tool 必须在其所属 Server 的能力列表中
 * 
 * 交叉引用: struct/05-functional-architecture-reuse/06-mcp-a2a-protocols/mcp-tool-design.md
 */

module MCPToolGraph

-- ============================================================
-- 签名定义 (Signature Declarations)
-- ============================================================

/** MCP Server：工具的宿主，通过 JSON-RPC 暴露能力 */
sig MCPServer {
    -- Server 声明的能力集合
    capabilities: set Capability,
    -- Server 暴露的工具集合
    tools: set MCPTool,
    -- Server 管理的资源集合
    resources: set Resource
}

/** MCP Tool：语义化函数签名，对应 MCP 规范中的 tool/list 和 tool/call */
sig MCPTool {
    -- 工具所属的 Server
    server: one MCPServer,
    -- 工具提供的具体能力
    provides: set Capability,
    -- 工具调用时依赖的其他工具（子调用）
    calls: set MCPTool,
    -- 工具访问的资源
    accesses: set Resource
}

/** Capability：能力语义单元，对应 MCP 规范中的 capability 声明 */
sig Capability {
    -- 能力所属的 Server（通过工具间接提供）
    -- 注：在 Alloy 中通过约束推导，非直接字段
}

/** Resource：MCP 资源，包括 URI 可寻址的文本、二进制、模板数据 */
sig Resource {
    -- 资源所属的 Server
    owner: one MCPServer
}

/** ToolDependency：显式依赖边，用于建模跨 Server 的 tool 调用 */
sig ToolDependency {
    caller: one MCPTool,
    callee: one MCPTool
}

-- ============================================================
-- 事实约束 (Facts)
-- ============================================================

/**
 * F1: Server-Tool 归属一致性
 * 工具必须属于暴露它的 Server，且 Server 的工具列表必须包含该工具。
 */
fact ServerToolConsistency {
    all t: MCPTool | 
        t.server = t.server and t in t.server.tools
    all s: MCPServer |
        s.tools.server in s
}

/**
 * F2: 能力归属一致性
 * 每个 Capability 必须通过至少一个 Tool 提供，且该 Tool 必须属于声明该 Capability 的 Server。
 */
fact CapabilityOwnership {
    all c: Capability |
        some t: MCPTool | c in t.provides and t.server in MCPServer
    all s: MCPServer |
        all c: s.capabilities |
            some t: s.tools | c in t.provides
}

/**
 * F3: Tool 调用无环性（核心约束）
 * 禁止工具通过调用链间接调用自身，防止级联调用中的死循环和堆栈溢出。
 * 对应于软件工程中的 Acyclic Dependencies Principle。
 */
fact AcyclicToolCalls {
    all t: MCPTool | t not in t.^calls
}

/**
 * F4: 能力封闭性（核心约束）
 * 任何被调用的工具（callee），其提供的能力必须包含在调用者所属 Server 的能力列表中，
 * 或通过合法的跨 Server 委托机制获得。
 * 本模型简化为：被调用工具必须属于同一 Server，或其能力在 caller Server 的能力超集中。
 */
fact CapabilityClosure {
    all t: MCPTool |
        all callee: t.calls |
            callee.server = t.server or
            callee.provides in t.server.capabilities
}

/**
 * F5: 资源访问隔离
 * 工具只能访问其所属 Server 拥有的资源，或明确共享的资源。
 */
fact ResourceAccessIsolation {
    all t: MCPTool |
        all r: t.accesses |
            r.owner = t.server
}

/**
 * F6: ToolDependency 与 calls 关系同步
 * 显式依赖边必须与隐式 calls 关系一致。
 */
fact DependencyEdgeSync {
    all d: ToolDependency |
        d.callee in d.caller.calls
    all t1, t2: MCPTool |
        t2 in t1.calls implies some d: ToolDependency | d.caller = t1 and d.callee = t2
}

-- ============================================================
-- 谓词 (Predicates)
-- ============================================================

/**
 * 判断一个工具是否为"叶节点"：不调用任何其他工具
 */
pred IsLeafTool[t: MCPTool] {
    no t.calls
}

/**
 * 判断一个工具是否为"根节点"：不被任何其他工具调用
 */
pred IsRootTool[t: MCPTool] {
    no t.~calls
}

/**
 * 生成一个满足所有约束的合法 MCP Server 实例
 */
pred ShowValidMCPServer {
    some s: MCPServer |
        #s.tools >= 3 and
        #s.capabilities >= 2 and
        some t: s.tools | #t.calls >= 1
}

/**
 * 生成一个违规实例：工具调用了不在 Server 能力列表中的外部工具
 * 注：此 pred 与 F4 矛盾，用于反例教学；需临时注释 F4 才能 run 出实例
 */
pred CapabilityViolation {
    some t: MCPTool |
        some callee: t.calls |
            callee.server != t.server and
            callee.provides not in t.server.capabilities
}

-- ============================================================
-- 断言 (Assertions)
-- ============================================================

/**
 * A1: 工具调用图无环性
 * MCP 工具之间不能存在循环调用。循环调用会导致：
 *   - JSON-RPC 请求的死循环和超时
 *   - 资源泄漏（连接池、内存、文件句柄）
 *   - 错误传播不可控（级联失败）
 */
assert NoCyclicToolCalls {
    no t: MCPTool | t in t.^calls
}

/**
 * A2: 能力包含性
 * 每个被调用的工具，其提供的能力必须是调用者 Server 已声明的能力的子集。
 * 这是"最小权限原则"在 MCP 架构中的形式化表达。
 */
assert CapabilityContainment {
    all t: MCPTool |
        all callee: t.calls |
            callee.provides in t.server.capabilities or callee.server = t.server
}

/**
 * A3: 资源访问边界
 * 工具不能访问不属于其 Server 的资源。
 * 违反此约束意味着存在潜在的信息泄露或权限提升通道。
 */
assert ResourceBoundary {
    all t: MCPTool |
        all r: t.accesses | r.owner = t.server
}

/**
 * A4: Server 能力非空性
 * 每个声明了工具的 Server 必须至少声明一项能力。
 * 空能力列表的 Server 不应暴露任何工具。
 */
assert ServerCapabilityNonEmpty {
    all s: MCPServer |
        some s.tools implies some s.capabilities
}

-- ============================================================
-- 检查命令 (Check Commands)
-- ============================================================

/** 检查工具调用无环性，scope: 4 Server, 8 Tool, 6 Capability */
check NoCyclicToolCalls for 4 but 8 MCPTool, 6 Capability

/** 检查能力包含性，scope: 4 Server, 8 Tool, 6 Capability, 5 Resource */
check CapabilityContainment for 4 but 8 MCPTool, 6 Capability, 5 Resource

/** 检查资源访问边界 */
check ResourceBoundary for 4 but 8 MCPTool, 5 Resource

-- ============================================================
-- 模拟命令 (Run Commands)
-- ============================================================

/** 生成一个合法的 MCP Server 工具依赖图实例 */
run ShowValidMCPServer for 3 but 6 MCPTool, 4 Capability, 4 Resource

/**
 * 尝试生成能力违规实例（预期无 instance，因为被 F4 排除）
 * 教学用途：临时注释 F4 后执行，可观察 Alloy 生成的反例图
 */
-- run CapabilityViolation for 3 but 6 MCPTool, 4 Capability
