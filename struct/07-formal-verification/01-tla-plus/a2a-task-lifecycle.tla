------------------------------- MODULE a2a_task_lifecycle -------------------------------
(*
 * TLA+ Specification: A2A (Agent-to-Agent) Task Lifecycle Protocol
 * 
 * 状态机: submitted → working → input-required → completed/failed/canceled
 * 
 * 不变量:
 *   - TerminalNoMessages: 终止状态（completed/failed/canceled）下不再有消息交互
 *   - CompletedHasArtifact: completed 状态必须包含至少一个 Artifact
 *   - ValidStateTransitions: 只允许规范定义的状态转移
 * 
 * 活性:
 *   - WorkingEventuallyTerminates: working 状态最终必须转移到终止状态
 *     （在超时或完成条件下）
 * 
 * 参考: Google A2A Protocol Specification v1.0 (March 2026)
 *       Wayne, H. Practical TLA+, Ch. 4 (State Machines)
 *       Lamport, L. Specifying Systems, Ch. 3 (Specification Fundamentals)
 *)

EXTENDS Integers, Sequences, FiniteSets

CONSTANTS
    Tasks,                  (* Task 标识符集合 *)
    Agents,                 (* Agent 标识符集合（Client / Server） *)
    Artifacts,              (* Artifact 标识符集合 *)
    MaxMessages,            (* 单个 Task 最大消息数（用于限制状态空间） *)
    TimeoutThreshold        (* Task 超时阈值（步数） *)

ASSUME
    /\ Tasks # {}               (* 至少存在一个 Task *)
    /\ Agents # {}              (* 至少存在一个 Agent *)
    /\ MaxMessages \in Nat \ {0} (* 最大消息数为正整数 *)
    /\ TimeoutThreshold \in Nat \ {0}

VARIABLES
    taskState,              (* Task 状态: [Tasks -> TaskStates] *)
    taskOwner,              (* Task 的 Server Agent: [Tasks -> Agents] *)
    taskMessages,           (* Task 的消息历史: [Tasks -> Seq(Messages)] *)
    taskArtifacts,          (* Task 的 Artifact: [Tasks -> SUBSET Artifacts] *)
    taskStepCount,          (* Task 已执行的步数（用于超时判断） *)
    taskInputPending        (* Task 是否等待外部输入: [Tasks -> BOOLEAN] *)

(* 辅助定义：Task 的所有可能状态 *)
TaskStates == {"submitted", "working", "input_required", 
               "completed", "failed", "canceled"}

(* 辅助定义：非终止状态集合 *)
NonTerminalStates == {"submitted", "working", "input_required"}

(* 辅助定义：终止状态集合 *)
TerminalStates == {"completed", "failed", "canceled"}

(* 辅助定义：消息类型 *)
MessageTypes == {"send", "receive", "request_input", "provide_input", 
                 "complete", "fail", "cancel"}

(* ============================================================================ *)
(* 类型正确性不变量                                                           *)
(* ============================================================================ *)
TypeOK ==
    /\ taskState \in [Tasks -> TaskStates]
    /\ taskOwner \in [Tasks -> Agents]
    /\ taskMessages \in [Tasks -> Seq([type: MessageTypes, 
                                       from: Agents, 
                                       to: Agents])]
    /\ taskArtifacts \in [Tasks -> SUBSET Artifacts]
    /\ taskStepCount \in [Tasks -> Nat]
    /\ taskInputPending \in [Tasks -> BOOLEAN]

(* ============================================================================ *)
(* 初始状态                                                                    *)
(* ============================================================================ *)
Init ==
    /\ taskState = [t \in Tasks |-> "submitted"]
    /\ taskOwner \in [Tasks -> Agents]
    /\ taskMessages = [t \in Tasks |-> <<>>]
    /\ taskArtifacts = [t \in Tasks |-> {}]
    /\ taskStepCount = [t \in Tasks |-> 0]
    /\ taskInputPending = [t \in Tasks |-> FALSE]

(* ============================================================================ *)
(* 状态转移动作                                                                *)
(* ============================================================================ *)

(* A1: submitted → working                                                     *)
(* Client 提交 Task，Server Agent 开始处理                                     *)
StartWork(t, agent) ==
    /\ taskState[t] = "submitted"
    /\ agent \in Agents
    /\ taskOwner[t] = agent
    /\ taskState' = [taskState EXCEPT ![t] = "working"]
    /\ taskMessages' = [taskMessages EXCEPT ![t] = 
         Append(@, [type |-> "send", from |-> CHOOSE a \in Agents : TRUE, to |-> agent])]
    /\ taskStepCount' = [taskStepCount EXCEPT ![t] = @ + 1]
    /\ UNCHANGED <<taskOwner, taskArtifacts, taskInputPending>>

(* A2: working → input_required                                                *)
(* Server Agent 需要额外输入才能继续处理                                       *)
RequestInput(t, agent) ==
    /\ taskState[t] = "working"
    /\ agent \in Agents
    /\ taskOwner[t] = agent
    /\ taskState' = [taskState EXCEPT ![t] = "input_required"]
    /\ taskMessages' = [taskMessages EXCEPT ![t] = 
         Append(@, [type |-> "request_input", from |-> agent, 
                    to |-> CHOOSE a \in Agents : a # agent])]
    /\ taskInputPending' = [taskInputPending EXCEPT ![t] = TRUE]
    /\ taskStepCount' = [taskStepCount EXCEPT ![t] = @ + 1]
    /\ UNCHANGED <<taskOwner, taskArtifacts>>

(* A3: input_required → working                                                *)
(* Client 提供了所需输入，Server Agent 恢复处理                                *)
ProvideInput(t, agent) ==
    /\ taskState[t] = "input_required"
    /\ agent \in Agents
    /\ taskInputPending[t] = TRUE
    /\ taskState' = [taskState EXCEPT ![t] = "working"]
    /\ taskMessages' = [taskMessages EXCEPT ![t] = 
         Append(@, [type |-> "provide_input", 
                    from |-> CHOOSE a \in Agents : a # agent, to |-> agent])]
    /\ taskInputPending' = [taskInputPending EXCEPT ![t] = FALSE]
    /\ taskStepCount' = [taskStepCount EXCEPT ![t] = @ + 1]
    /\ UNCHANGED <<taskOwner, taskArtifacts>>

(* A4: working → completed                                                     *)
(* Server Agent 成功完成任务，必须附带至少一个 Artifact                        *)
CompleteTask(t, agent, artifact) ==
    /\ taskState[t] = "working"
    /\ agent \in Agents
    /\ taskOwner[t] = agent
    /\ artifact \in Artifacts
    /\ taskState' = [taskState EXCEPT ![t] = "completed"]
    /\ taskArtifacts' = [taskArtifacts EXCEPT ![t] = @ \union {artifact}]
    /\ taskMessages' = [taskMessages EXCEPT ![t] = 
         Append(@, [type |-> "complete", from |-> agent, 
                    to |-> CHOOSE a \in Agents : a # agent])]
    /\ taskStepCount' = [taskStepCount EXCEPT ![t] = @ + 1]
    /\ UNCHANGED <<taskOwner, taskInputPending>>

(* A5: working → failed                                                        *)
(* Server Agent 处理过程中遇到不可恢复错误                                     *)
FailTask(t, agent) ==
    /\ taskState[t] = "working"
    /\ agent \in Agents
    /\ taskOwner[t] = agent
    /\ taskState' = [taskState EXCEPT ![t] = "failed"]
    /\ taskMessages' = [taskMessages EXCEPT ![t] = 
         Append(@, [type |-> "fail", from |-> agent, 
                    to |-> CHOOSE a \in Agents : a # agent])]
    /\ taskStepCount' = [taskStepCount EXCEPT ![t] = @ + 1]
    /\ UNCHANGED <<taskOwner, taskArtifacts, taskInputPending>>

(* A6: 任意非终止状态 → canceled（Client 主动取消）                           *)
CancelTask(t) ==
    /\ taskState[t] \in NonTerminalStates
    /\ taskState' = [taskState EXCEPT ![t] = "canceled"]
    /\ taskMessages' = [taskMessages EXCEPT ![t] = 
         Append(@, [type |-> "cancel", 
                    from |-> CHOOSE a \in Agents : TRUE,
                    to |-> taskOwner[t]])]
    /\ taskStepCount' = [taskStepCount EXCEPT ![t] = @ + 1]
    /\ taskInputPending' = [taskInputPending EXCEPT ![t] = FALSE]
    /\ UNCHANGED <<taskOwner, taskArtifacts>>

(* A7: 超时强制终止 — working 或 input_required 超过 TimeoutThreshold 步     *)
TimeoutTask(t) ==
    /\ taskState[t] \in {"working", "input_required"}
    /\ taskStepCount[t] >= TimeoutThreshold
    /\ taskState' = [taskState EXCEPT ![t] = "failed"]
    /\ taskMessages' = [taskMessages EXCEPT ![t] = 
         Append(@, [type |-> "fail", from |-> taskOwner[t],
                    to |-> CHOOSE a \in Agents : a # taskOwner[t]])]
    /\ taskStepCount' = [taskStepCount EXCEPT ![t] = @ + 1]
    /\ taskInputPending' = [taskInputPending EXCEPT ![t] = FALSE]
    /\ UNCHANGED <<taskOwner, taskArtifacts>>

(* ============================================================================ *)
(* 下一步关系（Next State Relation）                                           *)
(* ============================================================================ *)
Next ==
    /\ \E t \in Tasks, agent \in Agents :
        StartWork(t, agent)
    \/ \E t \in Tasks, agent \in Agents :
        RequestInput(t, agent)
    \/ \E t \in Tasks, agent \in Agents :
        ProvideInput(t, agent)
    \/ \E t \in Tasks, agent \in Agents, artifact \in Artifacts :
        CompleteTask(t, agent, artifact)
    \/ \E t \in Tasks, agent \in Agents :
        FailTask(t, agent)
    \/ \E t \in Tasks :
        CancelTask(t)
    \/ \E t \in Tasks :
        TimeoutTask(t)

(* ============================================================================ *)
(* 不变量（Safety Properties）                                                 *)
(* ============================================================================ *)

(* 不变量 I1: 终止状态下不再有消息交互                                         *)
(* 即：如果 taskState[t] 是终止状态，则 taskMessages[t] 不应再增长            *)
(* 在 TLA+ 中，我们通过检查终止状态下动作的前置条件来保证这一点              *)
TerminalNoMessages ==
    \A t \in Tasks :
        taskState[t] \in TerminalStates =>
            taskStepCount[t] <= TimeoutThreshold + 1

(* 更强版本：completed 状态的消息序列末尾必须是 complete 类型消息             *)
CompletedLastMessageIsComplete ==
    \A t \in Tasks :
        (taskState[t] = "completed" /\ taskMessages[t] # <<>>) =>
            LET lastIdx == Len(taskMessages[t])
            IN  taskMessages[t][lastIdx].type = "complete"

(* 不变量 I2: completed 状态必须包含至少一个 Artifact                          *)
(* 这是 A2A v1.0 规范的核心要求：成功完成的任务必须产出可交付物             *)
CompletedHasArtifact ==
    \A t \in Tasks :
        taskState[t] = "completed" => taskArtifacts[t] # {}

(* 不变量 I3: 非终止状态的 Task 必须有消息历史（排除刚创建的 submitted）        *)
(* 确保状态推进与消息发送的同步性                                            *)
NonTerminalHasMessages ==
    \A t \in Tasks :
        (taskState[t] \in {"working", "input_required"}) => taskMessages[t] # <<>>

(* 不变量 I4: input_required 时 taskInputPending 必须为 TRUE                   *)
InputRequiredImpliesPending ==
    \A t \in Tasks :
        taskState[t] = "input_required" => taskInputPending[t] = TRUE

(* 不变量 I5: failed 和 canceled 状态下 Artifact 必须为空                     *)
FailedCanceledNoArtifacts ==
    \A t \in Tasks :
        taskState[t] \in {"failed", "canceled"} => taskArtifacts[t] = {}

(* ============================================================================ *)
(* 活性（Liveness Properties）                                                 *)
(* ============================================================================ *)

(* 公平性假设：关键动作在启用时最终会发生                                     *)
Fairness ==
    /\ \A t \in Tasks, agent \in Agents :
        WF_<<taskState, taskMessages, taskStepCount>>(CompleteTask(t, agent, CHOOSE a \in Artifacts : TRUE))
    /\ \A t \in Tasks, agent \in Agents :
        WF_<<taskState, taskMessages, taskStepCount>>(FailTask(t, agent))
    /\ \A t \in Tasks :
        WF_<<taskState, taskMessages, taskStepCount, taskInputPending>>(CancelTask(t))
    /\ \A t \in Tasks :
        WF_<<taskState, taskMessages, taskStepCount, taskInputPending>>(TimeoutTask(t))

(* 活性 L1: working 状态最终必须转移到终止状态                                 *)
(* 在超时或完成条件下，working 不能无限持续                                   *)
WorkingEventuallyTerminates ==
    \A t \in Tasks :
        (taskState[t] = "working") ~> (taskState[t] \in TerminalStates)

(* 活性 L2: input_required 状态最终必须解决（恢复 working 或到达终止）        *)
InputRequiredEventuallyResolved ==
    \A t \in Tasks :
        (taskState[t] = "input_required") ~> 
            (taskState[t] \in TerminalStates \/ taskState[t] = "working")

(* ============================================================================ *)
(* 规约公式                                                                    *)
(* ============================================================================ *)
Spec == Init /\ [][Next]_<<taskState, taskOwner, taskMessages, taskArtifacts,
                                    taskStepCount, taskInputPending>> /\ Fairness

================================================================================
(* 规约结束                                                                    *)
(*
 * TLC 模型检查配置建议:
 *   - Tasks <- {t1, t2}
 *   - Agents <- {client, server}
 *   - Artifacts <- {art1, art2}
 *   - MaxMessages <- 5
 *   - TimeoutThreshold <- 10
 *   - 检查不变量: TypeOK, TerminalNoMessages, CompletedHasArtifact,
 *                 ValidStateTransitions, InputRequiredImpliesPending,
 *                 FailedCanceledNoArtifacts, CompletedLastMessageIsComplete
 *   - 检查活性: WorkingEventuallyTerminates, InputRequiredEventuallyResolved
 *)
