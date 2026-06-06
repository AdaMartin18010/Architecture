------------------------------- MODULE mcp_capability_negotiation -------------------------------
(*
 * TLA+ Specification: MCP Server Capability Negotiation Protocol
 * 
 * 状态机: Disconnected → Initializing → Negotiating → Active → Terminated
 * 
 * 不变量:
 *   - ActiveImpliesCommonCaps: Active 状态时双方能力集合必须有非空交集
 *   - ConsistentProtocolVersion: Active 时协议版本必须一致
 * 
 * 活性:
 *   - EventuallyActiveOrTerminated: 若网络正常，协商最终到达 Active 或 Terminated
 * 
 * 参考: Model Context Protocol Specification (2025-03-26, 2025-11-25)
 *       JSON-RPC 2.0 Specification (jsonrpc.org)
 *       Lamport, L. Specifying Systems, Ch. 8 (FIFO channels)
 *)

EXTENDS Integers, Sequences, FiniteSets

CONSTANTS
    AllCapabilities,        (* 所有可能的能力集合，如 {"tools", "resources", "prompts", "sampling"} *)
    ProtocolVersions,       (* 支持的协议版本集合，如 {"2024-11-05", "2025-03-26", "2025-11-25"} *)
    MaxRetries              (* 最大重试次数 *)

ASSUME
    /\ AllCapabilities # {}       (* 至少存在一种能力 *)
    /\ ProtocolVersions # {}      (* 至少存在一个协议版本 *)
    /\ MaxRetries \in Nat         (* 最大重试次数为非负整数 *)

VARIABLES
    clientState,            (* Client 端状态: {"disconnected", "initializing", "negotiating", "active", "terminated", "error"} *)
    serverState,            (* Server 端状态: {"disconnected", "initializing", "negotiating", "active", "terminated", "error"} *)
    clientCaps,             (* Client 声明的能力集合: SUBSET AllCapabilities *)
    serverCaps,             (* Server 声明的能力集合: SUBSET AllCapabilities *)
    agreedCaps,             (* 协商达成一致的能力集合: SUBSET AllCapabilities *)
    clientVersion,          (* Client 请求的协议版本 *)
    serverVersion,          (* Server 响应的协议版本 *)
    agreedVersion,          (* 协商一致的协议版本 *)
    networkStatus,          (* 网络状态: {"up", "down"} *)
    retryCount,             (* 当前重试计数 *)
    messageQueue            (* 模拟 JSON-RPC 消息队列 *)

(* 辅助定义：状态集合 *)
ClientStates == {"disconnected", "initializing", "negotiating", "active", "terminated", "error"}
ServerStates == {"disconnected", "initializing", "negotiating", "active", "terminated", "error"}
NetworkStates == {"up", "down"}

(* ============================================================================ *)
(* 类型正确性不变量                                                           *)
(* ============================================================================ *)
TypeOK ==
    /\ clientState \in ClientStates
    /\ serverState \in ServerStates
    /\ clientCaps \in SUBSET AllCapabilities
    /\ serverCaps \in SUBSET AllCapabilities
    /\ agreedCaps \in SUBSET AllCapabilities
    /\ clientVersion \in ProtocolVersions \union {"none"}
    /\ serverVersion \in ProtocolVersions \union {"none"}
    /\ agreedVersion \in ProtocolVersions \union {"none"}
    /\ networkStatus \in NetworkStates
    /\ retryCount \in 0..MaxRetries
    /\ messageQueue \in Seq([type: {"init", "init_ack", "negotiate", "negotiate_ack", "terminate"},
                            caps: SUBSET AllCapabilities,
                            version: ProtocolVersions])

(* ============================================================================ *)
(* 初始状态                                                                    *)
(* ============================================================================ *)
Init ==
    /\ clientState = "disconnected"
    /\ serverState = "disconnected"
    /\ clientCaps = {}            (* Client 初始无能力声明 *)
    /\ serverCaps = {}            (* Server 初始无能力声明 *)
    /\ agreedCaps = {}
    /\ clientVersion = "none"
    /\ serverVersion = "none"
    /\ agreedVersion = "none"
    /\ networkStatus = "up"       (* 初始假设网络可用 *)
    /\ retryCount = 0
    /\ messageQueue = <<>>

(* ============================================================================ *)
(* 状态转移动作                                                                *)
(* ============================================================================ *)

(* A1: Client 发起连接（Disconnected → Initializing）                          *)
(* Client 发送 initialize 请求，携带自身能力和支持的协议版本                   *)
ClientConnect(caps, version) ==
    /\ clientState = "disconnected"
    /\ networkStatus = "up"
    /\ caps \in SUBSET AllCapabilities
    /\ caps # {}                  (* Client 至少声明一项能力 *)
    /\ version \in ProtocolVersions
    /\ clientState' = "initializing"
    /\ clientCaps' = caps
    /\ clientVersion' = version
    /\ messageQueue' = Append(messageQueue,
                               [type |-> "init",
                                caps |-> caps,
                                version |-> version])
    /\ UNCHANGED <<serverState, serverCaps, serverVersion, agreedCaps, 
                    agreedVersion, networkStatus, retryCount>>

(* A2: Server 接收初始化请求并响应（Disconnected → Initializing）              *)
(* Server 返回 initialize 响应，携带自身能力和选定的协议版本                   *)
ServerRespondInit(sCaps, sVersion) ==
    /\ serverState = "disconnected"
    /\ Len(messageQueue) > 0
    /\ Head(messageQueue).type = "init"
    /\ sCaps \in SUBSET AllCapabilities
    /\ sCaps # {}                 (* Server 至少声明一项能力 *)
    /\ sVersion \in ProtocolVersions
    /\ serverState' = "initializing"
    /\ serverCaps' = sCaps
    /\ serverVersion' = sVersion
    /\ messageQueue' = Append(Tail(messageQueue),
                               [type |-> "init_ack",
                                caps |-> sCaps,
                                version |-> sVersion])
    /\ UNCHANGED <<clientState, clientCaps, clientVersion, agreedCaps,
                    agreedVersion, networkStatus, retryCount>>

(* A3: Client 接收 init_ack 并进入协商阶段（Initializing → Negotiating）     *)
ClientReceiveInitAck ==
    /\ clientState = "initializing"
    /\ Len(messageQueue) > 0
    /\ Head(messageQueue).type = "init_ack"
    /\ networkStatus = "up"
    /\ clientState' = "negotiating"
    /\ agreedCaps' = clientCaps \intersect Head(messageQueue).caps
    /\ agreedVersion' = IF clientVersion = Head(messageQueue).version
                        THEN clientVersion
                        ELSE CHOOSE v \in {clientVersion, Head(messageQueue).version} : TRUE
    /\ messageQueue' = Append(Tail(messageQueue),
                               [type |-> "negotiate",
                                caps |-> agreedCaps',
                                version |-> agreedVersion'])
    /\ retryCount' = 0
    /\ UNCHANGED <<serverState, clientCaps, serverCaps, clientVersion, 
                    serverVersion, networkStatus>>

(* A4: Server 接收协商请求并进入协商阶段（Initializing → Negotiating）         *)
ServerReceiveNegotiate ==
    /\ serverState = "initializing"
    /\ Len(messageQueue) > 0
    /\ Head(messageQueue).type = "negotiate"
    /\ networkStatus = "up"
    /\ serverState' = "negotiating"
    /\ messageQueue' = Append(Tail(messageQueue),
                               [type |-> "negotiate_ack",
                                caps |-> Head(messageQueue).caps,
                                version |-> Head(messageQueue).version])
    /\ UNCHANGED <<clientState, clientCaps, serverCaps, agreedCaps,
                    clientVersion, serverVersion, agreedVersion, 
                    networkStatus, retryCount>>

(* A5: Client 接收 negotiate_ack 并进入 Active（Negotiating → Active）       *)
(* 前提：协商出的能力集合非空（符合 MCP 规范要求）                           *)
ClientActivate ==
    /\ clientState = "negotiating"
    /\ Len(messageQueue) > 0
    /\ Head(messageQueue).type = "negotiate_ack"
    /\ agreedCaps # {}            (* 必须有至少一个共同能力 *)
    /\ agreedVersion # "none"
    /\ networkStatus = "up"
    /\ clientState' = "active"
    /\ messageQueue' = Tail(messageQueue)
    /\ UNCHANGED <<serverState, clientCaps, serverCaps, agreedCaps,
                    clientVersion, serverVersion, agreedVersion, 
                    networkStatus, retryCount>>

(* A6: Server 同步进入 Active（Negotiating → Active）                          *)
ServerActivate ==
    /\ serverState = "negotiating"
    /\ clientState = "active"     (* Server 在 Client 确认后进入 Active *)
    /\ agreedCaps # {}
    /\ agreedVersion # "none"
    /\ networkStatus = "up"
    /\ serverState' = "active"
    /\ UNCHANGED <<clientState, clientCaps, serverCaps, agreedCaps,
                    clientVersion, serverVersion, agreedVersion,
                    networkStatus, retryCount, messageQueue>>

(* A7: Client 或 Server 发起终止连接                                         *)
ClientTerminate ==
    /\ clientState \in {"initializing", "negotiating", "active"}
    /\ clientState' = "terminated"
    /\ messageQueue' = Append(messageQueue,
                               [type |-> "terminate",
                                caps |-> {},
                                version |-> "none"])
    /\ UNCHANGED <<serverState, clientCaps, serverCaps, agreedCaps,
                    clientVersion, serverVersion, agreedVersion,
                    networkStatus, retryCount>>

ServerTerminate ==
    /\ serverState \in {"initializing", "negotiating", "active"}
    /\ serverState' = "terminated"
    /\ UNCHANGED <<clientState, clientCaps, serverCaps, agreedCaps,
                    clientVersion, serverVersion, agreedVersion,
                    networkStatus, retryCount, messageQueue>>

(* A8: 网络故障 — 将任意状态转移到 error（模拟网络分区）                     *)
NetworkFailure ==
    /\ networkStatus = "up"
    /\ networkStatus' = "down"
    /\ clientState' = IF clientState \in {"initializing", "negotiating"} 
                      THEN "error" ELSE clientState
    /\ serverState' = IF serverState \in {"initializing", "negotiating"} 
                      THEN "error" ELSE serverState
    /\ UNCHANGED <<clientCaps, serverCaps, agreedCaps, clientVersion,
                    serverVersion, agreedVersion, retryCount, messageQueue>>

(* A9: 重试机制 — 在 Negotiating 阶段允许有限次数的重试                     *)
ClientRetry(caps, version) ==
    /\ clientState = "error"
    /\ networkStatus = "up"
    /\ retryCount < MaxRetries
    /\ caps \in SUBSET AllCapabilities
    /\ caps # {}
    /\ version \in ProtocolVersions
    /\ clientState' = "initializing"
    /\ clientCaps' = caps
    /\ clientVersion' = version
    /\ retryCount' = retryCount + 1
    /\ messageQueue' = Append(messageQueue,
                               [type |-> "init",
                                caps |-> caps,
                                version |-> version])
    /\ UNCHANGED <<serverState, serverCaps, agreedCaps, serverVersion,
                    agreedVersion, networkStatus>>

(* ============================================================================ *)
(* 下一步关系（Next State Relation）                                           *)
(* ============================================================================ *)
Next ==
    /\ \E caps \in SUBSET AllCapabilities, version \in ProtocolVersions :
        ClientConnect(caps, version)
    \/ \E sCaps \in SUBSET AllCapabilities, sVersion \in ProtocolVersions :
        ServerRespondInit(sCaps, sVersion)
    \/ ClientReceiveInitAck
    \/ ServerReceiveNegotiate
    \/ ClientActivate
    \/ ServerActivate
    \/ ClientTerminate
    \/ ServerTerminate
    \/ NetworkFailure
    \/ \E caps \in SUBSET AllCapabilities, version \in ProtocolVersions :
        ClientRetry(caps, version)

(* ============================================================================ *)
(* 不变量（Safety Properties）                                                 *)
(* ============================================================================ *)

(* 不变量 I1: Active 状态时双方能力集合必须有非空交集                         *)
(* 这是 MCP 协议的核心语义：如果双方没有共同能力，会话无意义                  *)
ActiveImpliesCommonCaps ==
    (clientState = "active" /\ serverState = "active") =>
        agreedCaps # {} /\ agreedCaps \subseteq clientCaps /\ agreedCaps \subseteq serverCaps

(* 不变量 I2: Active 状态时协议版本必须一致                                   *)
ConsistentProtocolVersion ==
    (clientState = "active" /\ serverState = "active") =>
        agreedVersion # "none" /\ agreedVersion \in ProtocolVersions

(* 不变量 I3: 协商中的能力集合是双方声明的子集                                 *)
NegotiationSubset ==
    agreedCaps \subseteq clientCaps /\ agreedCaps \subseteq serverCaps

(* 不变量 I4: 错误状态仅在网络故障时出现（协商失败应进入 terminated）         *)
ErrorImpliesNetworkDown ==
    (clientState = "error" /\ serverState = "error") =>
        networkStatus = "down"

(* 不变量 I5: Terminated 状态时 agreedCaps 必须为空（资源已释放）             *)
TerminatedImpliesNoCaps ==
    (clientState = "terminated" /\ serverState = "terminated") =>
        agreedCaps = {} /\ agreedVersion = "none"

(* ============================================================================ *)
(* 活性（Liveness Properties）                                                 *)
(* ============================================================================ *)

(* 公平性假设：关键动作在启用时最终会发生                                     *)
Fairness ==
    /\ WF_<<clientState, serverState, messageQueue, agreedCaps, agreedVersion>>(ClientReceiveInitAck)
    /\ WF_<<clientState, serverState, messageQueue, agreedCaps, agreedVersion>>(ServerReceiveNegotiate)
    /\ WF_<<clientState, serverState, messageQueue>>(ClientActivate)
    /\ WF_<<clientState, serverState>>(ServerActivate)

(* 活性 L1: 若网络正常且能力有交集，协商最终到达 Active 状态                 *)
EventuallyActive ==
    (networkStatus = "up" /\ clientCaps \intersect serverCaps # {}) ~>
        (clientState = "active" /\ serverState = "active")

(* 活性 L2: 若网络故障或能力无交集，最终到达 Terminated 或 Error 状态         *)
EventuallyTerminatedOrError ==
    (networkStatus = "down" \/ clientCaps \intersect serverCaps = {}) ~>
        (clientState \in {"terminated", "error"} /\ serverState \in {"terminated", "error"})

(* ============================================================================ *)
(* 规约公式                                                                    *)
(* ============================================================================ *)
Spec == Init /\ [][Next]_<<clientState, serverState, clientCaps, serverCaps,
                                    agreedCaps, clientVersion, serverVersion,
                                    agreedVersion, networkStatus, retryCount, 
                                    messageQueue>> /\ Fairness

================================================================================
(* 规约结束                                                                    *)
(*
 * TLC 模型检查配置建议:
 *   - AllCapabilities <- {"tools", "resources", "prompts"}
 *   - ProtocolVersions <- {"2025-03-26"}
 *   - MaxRetries <- 2
 *   - 检查不变量: TypeOK, ActiveImpliesCommonCaps, ConsistentProtocolVersion,
 *                 NegotiationSubset, ErrorImpliesNetworkOrFailure, 
 *                 TerminatedImpliesNoCaps
 *   - 检查活性: EventuallyActive, EventuallyTerminatedOrError
 *)
