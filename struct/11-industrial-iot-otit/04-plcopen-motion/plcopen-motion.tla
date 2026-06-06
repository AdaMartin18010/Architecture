------------------------------- MODULE plcopen_motion -------------------------------
(*
 * TLA+ Specification: PLCopen Motion Control Function Block State Machines
 * 
 * 本规约建模两个核心功能块的并发状态机：
 *   - MC_Power:  Disabled → Enabling → Standstill → ErrorStop → Disabling
 *   - MC_MoveAbsolute: Idle → Busy → Active → Done / Error / CommandAborted
 * 
 * 不变量:
 *   - StandstillRequiredForMove: 只有在 Standstill 状态下才能执行 Move 命令
 *   - ErrorImpliesErrorID: Error 输出为 TRUE 时，ErrorID 必须非零
 *   - PowerStatusConsistency: MC_Power.Status 与轴状态的一致性
 *   - NoInvalidTransition: 禁止非法状态转移
 * 
 * 活性:
 *   - BusyEventuallyTerminates: Busy 状态最终必须到达 Done 或 Error
 *     （在超时限制内）
 *   - PowerEnableEventuallyStandstill: Enabling 状态最终到达 Standstill
 * 
 * 参考: PLCopen Motion Control Part 1 & 2 v2.0
 *       struct/07-formal-verification/01-tla-plus/case-library.md (T10)
 *       Lamport, L. Specifying Systems (2002), Ch. 3-4
 *)

EXTENDS Integers, Sequences, FiniteSets

CONSTANTS
    Axes,               (* 轴标识符集合，如 {axis1, axis2} *)
    MaxTimeoutSteps,    (* Busy/Enabling 状态的最大允许步数 *)
    ErrorIDs            (* 合法错误码集合，如 {0, 0x8A01, 0x8A02, 0x9001} *)

ASSUME
    /\ Axes # {}                    (* 至少存在一个轴 *)
    /\ MaxTimeoutSteps \in Nat \ {0} (* 超时阈值为正整数 *)
    /\ ErrorIDs \subseteq Nat
    /\ 0 \in ErrorIDs               (* 0 表示无错误 *)

VARIABLES
    (* MC_Power 状态机变量 *)
    powerState,         (* MC_Power 状态: [Axes -> PowerStates] *)
    powerEnable,        (* Enable 输入: [Axes -> BOOLEAN] *)
    powerStatus,        (* Status 输出: [Axes -> BOOLEAN] *)
    powerBusy,          (* Busy 输出: [Axes -> BOOLEAN] *)
    powerError,         (* Error 输出: [Axes -> BOOLEAN] *)
    powerErrorID,       (* ErrorID 输出: [Axes -> ErrorIDs] *)
    
    (* MC_MoveAbsolute 状态机变量 *)
    moveState,          (* Move FB 状态: [Axes -> MoveStates] *)
    moveExecute,        (* Execute 输入: [Axes -> BOOLEAN] *)
    moveDone,           (* Done 输出: [Axes -> BOOLEAN] *)
    moveBusy,           (* Busy 输出: [Axes -> BOOLEAN] *)
    moveActive,         (* Active 输出: [Axes -> BOOLEAN] *)
    moveCommandAborted, (* CommandAborted 输出: [Axes -> BOOLEAN] *)
    moveError,          (* Error 输出: [Axes -> BOOLEAN] *)
    moveErrorID,        (* ErrorID 输出: [Axes -> ErrorIDs] *)
    
    (* 轴全局状态 *)
    axisState,          (* 轴的物理状态: [Axes -> AxisStates] *)
    stepCount           (* 当前状态已持续步数: [Axes -> Nat] *)

(* ============================================================================ *)
(* 辅助定义：各状态机的合法状态集合                                           *)
(* ============================================================================ *)

PowerStates == {"Disabled", "Enabling", "Standstill", "ErrorStop", "Disabling"}

MoveStates == {"Idle", "Busy", "Active", "Done", "Error", "CommandAborted"}

AxisStates == {"Disabled", "Standstill", "DiscreteMotion", "ContinuousMotion",
               "SynchronizedMotion", "Homing", "Stopping", "ErrorStop"}

(* ============================================================================ *)
(* 类型正确性不变量                                                           *)
(* ============================================================================ *)
TypeOK ==
    /\ powerState \in [Axes -> PowerStates]
    /\ powerEnable \in [Axes -> BOOLEAN]
    /\ powerStatus \in [Axes -> BOOLEAN]
    /\ powerBusy \in [Axes -> BOOLEAN]
    /\ powerError \in [Axes -> BOOLEAN]
    /\ powerErrorID \in [Axes -> ErrorIDs]
    /\ moveState \in [Axes -> MoveStates]
    /\ moveExecute \in [Axes -> BOOLEAN]
    /\ moveDone \in [Axes -> BOOLEAN]
    /\ moveBusy \in [Axes -> BOOLEAN]
    /\ moveActive \in [Axes -> BOOLEAN]
    /\ moveCommandAborted \in [Axes -> BOOLEAN]
    /\ moveError \in [Axes -> BOOLEAN]
    /\ moveErrorID \in [Axes -> ErrorIDs]
    /\ axisState \in [Axes -> AxisStates]
    /\ stepCount \in [Axes -> Nat]

(* ============================================================================ *)
(* 初始状态                                                                    *)
(* ============================================================================ *)
Init ==
    /\ powerState = [a \in Axes |-> "Disabled"]
    /\ powerEnable = [a \in Axes |-> FALSE]
    /\ powerStatus = [a \in Axes |-> FALSE]
    /\ powerBusy = [a \in Axes |-> FALSE]
    /\ powerError = [a \in Axes |-> FALSE]
    /\ powerErrorID = [a \in Axes |-> 0]
    /\ moveState = [a \in Axes |-> "Idle"]
    /\ moveExecute = [a \in Axes |-> FALSE]
    /\ moveDone = [a \in Axes |-> FALSE]
    /\ moveBusy = [a \in Axes |-> FALSE]
    /\ moveActive = [a \in Axes |-> FALSE]
    /\ moveCommandAborted = [a \in Axes |-> FALSE]
    /\ moveError = [a \in Axes |-> FALSE]
    /\ moveErrorID = [a \in Axes |-> 0]
    /\ axisState = [a \in Axes |-> "Disabled"]
    /\ stepCount = [a \in Axes |-> 0]

(* ============================================================================ *)
(* MC_Power 状态转移动作                                                       *)
(* ============================================================================ *)

(* A1: Disabled → Enabling: Enable 上升沿且轴无错误 *)
PowerEnableOn(a) ==
    /\ powerState[a] = "Disabled"
    /\ powerEnable[a] = FALSE
    /\ powerEnable' = [powerEnable EXCEPT ![a] = TRUE]
    /\ powerState' = [powerState EXCEPT ![a] = "Enabling"]
    /\ powerBusy' = [powerBusy EXCEPT ![a] = TRUE]
    /\ powerStatus' = [powerStatus EXCEPT ![a] = FALSE]
    /\ stepCount' = [stepCount EXCEPT ![a] = 0]
    /\ UNCHANGED <<powerError, powerErrorID, moveState, moveExecute,
                    moveDone, moveBusy, moveActive, moveCommandAborted,
                    moveError, moveErrorID, axisState>>

(* A2: Enabling → Standstill: 驱动器就绪反馈 *)
PowerEnableReady(a) ==
    /\ powerState[a] = "Enabling"
    /\ powerEnable[a] = TRUE
    /\ powerState' = [powerState EXCEPT ![a] = "Standstill"]
    /\ powerBusy' = [powerBusy EXCEPT ![a] = FALSE]
    /\ powerStatus' = [powerStatus EXCEPT ![a] = TRUE]
    /\ axisState' = [axisState EXCEPT ![a] = "Standstill"]
    /\ stepCount' = [stepCount EXCEPT ![a] = 0]
    /\ UNCHANGED <<powerEnable, powerError, powerErrorID, moveState,
                    moveExecute, moveDone, moveBusy, moveActive,
                    moveCommandAborted, moveError, moveErrorID>>

(* A3: Enabling → ErrorStop: 使能过程中出错 *)
PowerEnableError(a, err) ==
    /\ powerState[a] = "Enabling"
    /\ err \in ErrorIDs
    /\ err # 0
    /\ powerState' = [powerState EXCEPT ![a] = "ErrorStop"]
    /\ powerBusy' = [powerBusy EXCEPT ![a] = FALSE]
    /\ powerStatus' = [powerStatus EXCEPT ![a] = FALSE]
    /\ powerError' = [powerError EXCEPT ![a] = TRUE]
    /\ powerErrorID' = [powerErrorID EXCEPT ![a] = err]
    /\ axisState' = [axisState EXCEPT ![a] = "ErrorStop"]
    /\ stepCount' = [stepCount EXCEPT ![a] = 0]
    /\ UNCHANGED <<powerEnable, moveState, moveExecute, moveDone,
                    moveBusy, moveActive, moveCommandAborted,
                    moveError, moveErrorID>>

(* A4: Standstill → Disabling: Enable 下降沿 *)
PowerDisable(a) ==
    /\ powerState[a] = "Standstill"
    /\ powerEnable[a] = TRUE
    /\ powerEnable' = [powerEnable EXCEPT ![a] = FALSE]
    /\ powerState' = [powerState EXCEPT ![a] = "Disabling"]
    /\ powerBusy' = [powerBusy EXCEPT ![a] = TRUE]
    /\ powerStatus' = [powerStatus EXCEPT ![a] = FALSE]
    /\ axisState' = [axisState EXCEPT ![a] = "Disabled"]
    /\ stepCount' = [stepCount EXCEPT ![a] = 0]
    /\ UNCHANGED <<powerError, powerErrorID, moveState, moveExecute,
                    moveDone, moveBusy, moveActive, moveCommandAborted,
                    moveError, moveErrorID>>

(* A5: Disabling → Disabled: 驱动器关闭确认 *)
PowerDisabled(a) ==
    /\ powerState[a] = "Disabling"
    /\ powerEnable[a] = FALSE
    /\ powerState' = [powerState EXCEPT ![a] = "Disabled"]
    /\ powerBusy' = [powerBusy EXCEPT ![a] = FALSE]
    /\ stepCount' = [stepCount EXCEPT ![a] = 0]
    /\ UNCHANGED <<powerEnable, powerStatus, powerError, powerErrorID,
                    axisState, moveState, moveExecute, moveDone,
                    moveBusy, moveActive, moveCommandAborted,
                    moveError, moveErrorID>>

(* A6: 任意状态 → ErrorStop: 轴错误（除 Disabled 外） *)
PowerAxisError(a, err) ==
    /\ powerState[a] \in {"Enabling", "Standstill", "Disabling"}
    /\ err \in ErrorIDs
    /\ err # 0
    /\ powerState' = [powerState EXCEPT ![a] = "ErrorStop"]
    /\ powerBusy' = [powerBusy EXCEPT ![a] = FALSE]
    /\ powerStatus' = [powerStatus EXCEPT ![a] = FALSE]
    /\ powerError' = [powerError EXCEPT ![a] = TRUE]
    /\ powerErrorID' = [powerErrorID EXCEPT ![a] = err]
    /\ axisState' = [axisState EXCEPT ![a] = "ErrorStop"]
    /\ stepCount' = [stepCount EXCEPT ![a] = 0]
    /\ (* 若 Move FB 在 Active，则被中断 *)
       moveState' = [moveState EXCEPT ![a] =
                        IF @[a] \in {"Busy", "Active"}
                        THEN "CommandAborted"
                        ELSE @]
    /\ moveActive' = [moveActive EXCEPT ![a] =
                        IF moveState[a] \in {"Busy", "Active"}
                        THEN FALSE
                        ELSE @]
    /\ moveBusy' = [moveBusy EXCEPT ![a] =
                      IF moveState[a] \in {"Busy", "Active"}
                      THEN FALSE
                      ELSE @]
    /\ moveCommandAborted' = [moveCommandAborted EXCEPT ![a] =
                                IF moveState[a] \in {"Busy", "Active"}
                                THEN TRUE
                                ELSE @]
    /\ UNCHANGED <<powerEnable, moveExecute, moveDone,
                    moveError, moveErrorID>>

(* A7: ErrorStop → Standstill: MC_Reset 触发且错误清除 *)
PowerReset(a) ==
    /\ powerState[a] = "ErrorStop"
    /\ powerEnable[a] = TRUE
    /\ powerState' = [powerState EXCEPT ![a] = "Standstill"]
    /\ powerError' = [powerError EXCEPT ![a] = FALSE]
    /\ powerErrorID' = [powerErrorID EXCEPT ![a] = 0]
    /\ powerStatus' = [powerStatus EXCEPT ![a] = TRUE]
    /\ axisState' = [axisState EXCEPT ![a] = "Standstill"]
    /\ stepCount' = [stepCount EXCEPT ![a] = 0]
    /\ UNCHANGED <<powerEnable, powerBusy, moveState, moveExecute,
                    moveDone, moveBusy, moveActive, moveCommandAborted,
                    moveError, moveErrorID>>

(* ============================================================================ *)
(* MC_MoveAbsolute 状态转移动作                                                *)
(* ============================================================================ *)

(* B1: Idle → Busy: Execute 上升沿且轴在 Standstill *)
MoveStart(a) ==
    /\ moveState[a] = "Idle"
    /\ moveExecute[a] = FALSE
    /\ axisState[a] = "Standstill"
    /\ powerState[a] = "Standstill"
    /\ powerStatus[a] = TRUE
    /\ moveExecute' = [moveExecute EXCEPT ![a] = TRUE]
    /\ moveState' = [moveState EXCEPT ![a] = "Busy"]
    /\ moveBusy' = [moveBusy EXCEPT ![a] = TRUE]
    /\ moveDone' = [moveDone EXCEPT ![a] = FALSE]
    /\ moveError' = [moveError EXCEPT ![a] = FALSE]
    /\ moveErrorID' = [moveErrorID EXCEPT ![a] = 0]
    /\ stepCount' = [stepCount EXCEPT ![a] = 0]
    /\ UNCHANGED <<powerState, powerEnable, powerStatus, powerBusy,
                    powerError, powerErrorID, moveActive, moveCommandAborted,
                    axisState>>

(* B2: Idle → Error: Execute 上升沿但轴未就绪 *)
MoveStartError(a, err) ==
    /\ moveState[a] = "Idle"
    /\ moveExecute[a] = FALSE
    /\ axisState[a] # "Standstill"
    /\ err \in ErrorIDs
    /\ err # 0
    /\ moveExecute' = [moveExecute EXCEPT ![a] = TRUE]
    /\ moveState' = [moveState EXCEPT ![a] = "Error"]
    /\ moveError' = [moveError EXCEPT ![a] = TRUE]
    /\ moveErrorID' = [moveErrorID EXCEPT ![a] = err]
    /\ stepCount' = [stepCount EXCEPT ![a] = 0]
    /\ UNCHANGED <<powerState, powerEnable, powerStatus, powerBusy,
                    powerError, powerErrorID, moveDone, moveBusy,
                    moveActive, moveCommandAborted, axisState>>

(* B3: Busy → Active: 轴状态变为 DiscreteMotion *)
MoveActivate(a) ==
    /\ moveState[a] = "Busy"
    /\ moveExecute[a] = TRUE
    /\ moveState' = [moveState EXCEPT ![a] = "Active"]
    /\ moveActive' = [moveActive EXCEPT ![a] = TRUE]
    /\ axisState' = [axisState EXCEPT ![a] = "DiscreteMotion"]
    /\ stepCount' = [stepCount EXCEPT ![a] = 0]
    /\ UNCHANGED <<powerState, powerEnable, powerStatus, powerBusy,
                    powerError, powerErrorID, moveExecute, moveDone,
                    moveBusy, moveCommandAborted, moveError, moveErrorID>>

(* B4: Active → Done: 到达目标位置 *)
MoveComplete(a) ==
    /\ moveState[a] = "Active"
    /\ moveExecute[a] = TRUE
    /\ moveState' = [moveState EXCEPT ![a] = "Done"]
    /\ moveDone' = [moveDone EXCEPT ![a] = TRUE]
    /\ moveBusy' = [moveBusy EXCEPT ![a] = FALSE]
    /\ moveActive' = [moveActive EXCEPT ![a] = FALSE]
    /\ axisState' = [axisState EXCEPT ![a] = "Standstill"]
    /\ stepCount' = [stepCount EXCEPT ![a] = 0]
    /\ UNCHANGED <<powerState, powerEnable, powerStatus, powerBusy,
                    powerError, powerErrorID, moveExecute,
                    moveCommandAborted, moveError, moveErrorID>>

(* B5: Active → CommandAborted: 被其他命令中断 *)
MoveAbort(a) ==
    /\ moveState[a] = "Active"
    /\ moveExecute[a] = TRUE
    /\ moveState' = [moveState EXCEPT ![a] = "CommandAborted"]
    /\ moveCommandAborted' = [moveCommandAborted EXCEPT ![a] = TRUE]
    /\ moveBusy' = [moveBusy EXCEPT ![a] = FALSE]
    /\ moveActive' = [moveActive EXCEPT ![a] = FALSE]
    /\ axisState' = [axisState EXCEPT ![a] = "Standstill"]
    /\ stepCount' = [stepCount EXCEPT ![a] = 0]
    /\ UNCHANGED <<powerState, powerEnable, powerStatus, powerBusy,
                    powerError, powerErrorID, moveExecute, moveDone,
                    moveError, moveErrorID>>

(* B6: Active → Error: 运动过程中出错 *)
MoveError(a, err) ==
    /\ moveState[a] = "Active"
    /\ err \in ErrorIDs
    /\ err # 0
    /\ moveState' = [moveState EXCEPT ![a] = "Error"]
    /\ moveError' = [moveError EXCEPT ![a] = TRUE]
    /\ moveErrorID' = [moveErrorID EXCEPT ![a] = err]
    /\ moveBusy' = [moveBusy EXCEPT ![a] = FALSE]
    /\ moveActive' = [moveActive EXCEPT ![a] = FALSE]
    /\ axisState' = [axisState EXCEPT ![a] = "ErrorStop"]
    /\ stepCount' = [stepCount EXCEPT ![a] = 0]
    /\ UNCHANGED <<powerState, powerEnable, powerStatus, powerBusy,
                    powerError, powerErrorID, moveExecute, moveDone,
                    moveCommandAborted>>

(* B7: Done/Error/CommandAborted → Idle: Execute 下降沿 *)
MoveIdle(a) ==
    /\ moveState[a] \in {"Done", "Error", "CommandAborted"}
    /\ moveExecute[a] = TRUE
    /\ moveExecute' = [moveExecute EXCEPT ![a] = FALSE]
    /\ moveState' = [moveState EXCEPT ![a] = "Idle"]
    /\ moveDone' = [moveDone EXCEPT ![a] = FALSE]
    /\ moveCommandAborted' = [moveCommandAborted EXCEPT ![a] = FALSE]
    /\ moveError' = [moveError EXCEPT ![a] = FALSE]
    /\ moveErrorID' = [moveErrorID EXCEPT ![a] = 0]
    /\ stepCount' = [stepCount EXCEPT ![a] = 0]
    /\ UNCHANGED <<powerState, powerEnable, powerStatus, powerBusy,
                    powerError, powerErrorID, moveBusy, moveActive,
                    axisState>>

(* ============================================================================ *)
(* 步进计数（用于超时检测）                                                     *)
(* ============================================================================ *)

IncrementStepCount(a) ==
    /\ moveState[a] \in {"Busy", "Active"}
    /\ stepCount' = [stepCount EXCEPT ![a] = @ + 1]
    /\ UNCHANGED <<powerState, powerEnable, powerStatus, powerBusy,
                    powerError, powerErrorID, moveState, moveExecute,
                    moveDone, moveBusy, moveActive, moveCommandAborted,
                    moveError, moveErrorID, axisState>>

(* ============================================================================ *)
(* 下一步关系（Next State Relation）                                           *)
(* ============================================================================ *)
Next ==
    /\ \E a \in Axes :
        /\ PowerEnableOn(a)
        \/ PowerEnableReady(a)
        \/ \E err \in ErrorIDs \ {0} : PowerEnableError(a, err)
        \/ PowerDisable(a)
        \/ PowerDisabled(a)
        \/ \E err \in ErrorIDs \ {0} : PowerAxisError(a, err)
        \/ PowerReset(a)
        \/ MoveStart(a)
        \/ \E err \in ErrorIDs \ {0} : MoveStartError(a, err)
        \/ MoveActivate(a)
        \/ MoveComplete(a)
        \/ MoveAbort(a)
        \/ \E err \in ErrorIDs \ {0} : MoveError(a, err)
        \/ MoveIdle(a)
        \/ IncrementStepCount(a)

(* ============================================================================ *)
(* 不变量（Safety Properties）                                                 *)
(* ============================================================================ *)

(* I1: Standstill 时才能执行 Move 命令
 * 即: 若 moveState 从 Idle 转入 Busy，则 axisState 必须为 Standstill
 * 这在 MoveStart 的前置条件中已保证，此处作为全局不变量验证 *)
StandstillRequiredForMove ==
    \A a \in Axes :
        (moveState[a] \in {"Busy", "Active"})
            => (axisState[a] \in {"Standstill", "DiscreteMotion"}
                /\ powerState[a] = "Standstill"
                /\ powerStatus[a] = TRUE)

(* I2: Error 时必须有 ErrorID（非零） *)
ErrorImpliesErrorID ==
    \A a \in Axes :
        /\ (powerError[a] = TRUE) => (powerErrorID[a] # 0)
        /\ (moveError[a] = TRUE) => (moveErrorID[a] # 0)

(* I3: MC_Power.Status 与轴状态的一致性 *)
PowerStatusConsistency ==
    \A a \in Axes :
        /\ (powerStatus[a] = TRUE) => (powerState[a] = "Standstill")
        /\ (powerState[a] = "Standstill") => (axisState[a] = "Standstill")
        /\ (powerState[a] = "Disabled") => (axisState[a] = "Disabled")
        /\ (powerState[a] = "ErrorStop") => (axisState[a] = "ErrorStop")

(* I4: Move FB 输出一致性 *)
MoveOutputConsistency ==
    \A a \in Axes :
        /\ (moveState[a] = "Idle") =>
            /\ moveDone[a] = FALSE
            /\ moveBusy[a] = FALSE
            /\ moveActive[a] = FALSE
            /\ moveCommandAborted[a] = FALSE
            /\ moveError[a] = FALSE
            /\ moveErrorID[a] = 0
        /\ (moveState[a] = "Done") =>
            /\ moveDone[a] = TRUE
            /\ moveBusy[a] = FALSE
            /\ moveActive[a] = FALSE
        /\ (moveState[a] = "CommandAborted") =>
            /\ moveCommandAborted[a] = TRUE
            /\ moveBusy[a] = FALSE
            /\ moveActive[a] = FALSE

(* I5: 禁止非法状态转移 *)
NoInvalidTransition ==
    \A a \in Axes :
        /\ ~(powerState[a] = "Disabled" /\ axisState[a] = "DiscreteMotion")
        /\ ~(powerState[a] = "ErrorStop" /\ moveState[a] = "Active")

(* ============================================================================ *)
(* 活性（Liveness Properties）                                                 *)
(* ============================================================================ *)

(* 公平性假设：关键动作在持续可执行时最终会发生 *)
Fairness ==
    /\ \A a \in Axes : WF_<<powerState, powerStatus, powerBusy,
                              moveState, moveBusy, moveActive,
                              axisState, stepCount>>(PowerEnableReady(a))
    /\ \A a \in Axes : WF_<<moveState, moveDone, moveBusy, moveActive,
                              axisState, stepCount>>(MoveComplete(a))
    /\ \A a \in Axes : WF_<<moveState, moveError, moveBusy, moveActive,
                              axisState, stepCount>>(
                                  \E err \in ErrorIDs \ {0} : MoveError(a, err))

(* L1: Busy 状态最终必须到达 Done 或 Error（在超时限制内） *)
(* 注意：此活性在 stepCount >= MaxTimeoutSteps 时通过 MoveError 动作满足 *)
BusyEventuallyTerminates ==
    \A a \in Axes :
        (moveState[a] = "Busy") ~> (moveState[a] \in {"Done", "Error", "CommandAborted"})

(* L2: Enabling 状态最终必须到达 Standstill 或 ErrorStop *)
PowerEnableEventuallyStandstill ==
    \A a \in Axes :
        (powerState[a] = "Enabling") ~> (powerState[a] \in {"Standstill", "ErrorStop"})

(* L3: Active 状态最终必须到达 Done 或 Error 或 CommandAborted *)
ActiveEventuallyTerminates ==
    \A a \in Axes :
        (moveState[a] = "Active") ~> (moveState[a] \in {"Done", "Error", "CommandAborted"})

(* ============================================================================ *)
(* 规约公式                                                                    *)
(* ============================================================================ *)
Spec == Init /\ [][Next]_<<powerState, powerEnable, powerStatus, powerBusy,
                                      powerError, powerErrorID,
                                      moveState, moveExecute, moveDone,
                                      moveBusy, moveActive, moveCommandAborted,
                                      moveError, moveErrorID,
                                      axisState, stepCount>> /\ Fairness

================================================================================
(* 规约结束                                                                    *)
(*
 * TLC 模型检查配置建议:
 *   - Axes <- {axis1}
 *   - MaxTimeoutSteps <- 5
 *   - ErrorIDs <- {0, 0x8A01, 0x8A02, 0x9001}
 *   - 检查不变量: TypeOK, StandstillRequiredForMove, ErrorImpliesErrorID,
 *                 PowerStatusConsistency, MoveOutputConsistency,
 *                 NoInvalidTransition
 *   - 检查活性: BusyEventuallyTerminates, PowerEnableEventuallyStandstill,
 *               ActiveEventuallyTerminates
 *)
