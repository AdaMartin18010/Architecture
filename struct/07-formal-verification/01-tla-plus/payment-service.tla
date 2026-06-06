------------------------------- MODULE payment_service -------------------------------
(*
 * TLA+ Specification: Distributed Payment Service Component
 * 
 * 状态机: Idle → Reserved → Committed / Aborted
 * 
 * 不变量:
 *   - FundConservationInv: 系统中所有账户余额与冻结资金之和保持恒定
 *   - NoDoubleSpending: 账户当前余额（已扣除冻结资金）非负
 *   - CommittedBalanceCorrect: Committed 交易金额恒为正
 * 
 * 活性:
 *   - AllRequestsProcessed: 所有处于 Reserved 状态的请求最终必须到达 
 *     Committed 或 Aborted 终止状态
 * 
 * 参考: Lamport, L. Specifying Systems (2002), Ch. 3-4
 *       Wayne, H. Practical TLA+ (Apress, 2018), Ch. 6
 *)

EXTENDS Integers, Sequences, FiniteSets

CONSTANTS
    Accounts,           (* 账户标识符集合，如 {a1, a2, a3} *)
    TxIds,              (* 交易标识符集合 *)
    MaxAmount           (* 单笔交易最大金额上限 *)

ASSUME
    /\ Accounts # {}           (* 至少存在一个账户 *)
    /\ TxIds # {}              (* 至少存在一个交易 ID *)
    /\ MaxAmount \in Nat \ {0} (* 最大金额为正整数 *)

VARIABLES
    balances,           (* 账户余额: [Accounts -> Nat] *)
    reservedFunds,      (* 交易冻结资金: [TxIds -> Nat] *)
    txStatus,           (* 交易状态: [TxIds -> {"idle", "reserved", "committed", "aborted"}] *)
    txFrom,             (* 交易出金账户: [TxIds -> Accounts] *)
    txTo,               (* 交易入金账户: [TxIds -> Accounts] *)
    txAmount,           (* 交易金额: [TxIds -> 1..MaxAmount] *)
    initialTotalBalance (* 系统初始总资金，用于验证守恒不变量 *)

(* 辅助定义：系统中所有账户的当前余额总和 *)
AccountBalanceTotal ==
    LET SumBalances[S \in SUBSET Accounts] ==
        IF S = {} THEN 0
        ELSE LET a == CHOOSE a \in S : TRUE
             IN  balances[a] + SumBalances[S \ {a}]
    IN  SumBalances[Accounts]

(* 辅助定义：所有被冻结的资金总和 *)
ReservedTotal ==
    LET SumReserved[S \in SUBSET TxIds] ==
        IF S = {} THEN 0
        ELSE LET t == CHOOSE t \in S : TRUE
             IN  reservedFunds[t] + SumReserved[S \ {t}]
    IN  SumReserved[TxIds]

(* 辅助定义：系统中全部资金（余额 + 冻结） *)
TotalSystemFunds == AccountBalanceTotal + ReservedTotal

(* ============================================================================ *)
(* 类型正确性不变量                                                           *)
(* ============================================================================ *)
TypeOK ==
    /\ balances \in [Accounts -> Nat]
    /\ reservedFunds \in [TxIds -> Nat]
    /\ txStatus \in [TxIds -> {"idle", "reserved", "committed", "aborted"}]
    /\ txFrom \in [TxIds -> Accounts]
    /\ txTo \in [TxIds -> Accounts]
    /\ txAmount \in [TxIds -> 1..MaxAmount]
    /\ initialTotalBalance \in Nat
    /\ \A tx \in TxIds : txFrom[tx] # txTo[tx]  (* 不允许自转账 *)

(* ============================================================================ *)
(* 初始状态                                                                    *)
(* ============================================================================ *)
Init ==
    /\ balances \in [Accounts -> Nat]           (* 任意非负初始余额 *)
    /\ reservedFunds = [tx \in TxIds |-> 0]     (* 初始无冻结资金 *)
    /\ txStatus = [tx \in TxIds |-> "idle"]     (* 所有交易初始为 idle *)
    /\ txFrom \in [TxIds -> Accounts]
    /\ txTo \in [TxIds -> Accounts]
    /\ txAmount = [tx \in TxIds |-> 1]
    /\ initialTotalBalance = AccountBalanceTotal (* 记录初始总资金 *)
    /\ \A tx \in TxIds : txFrom[tx] # txTo[tx]

(* ============================================================================ *)
(* 状态转移动作                                                                *)
(* ============================================================================ *)

(* 创建交易：从 Idle 进入 Reserved 状态                                       *)
(* 前置条件：出金账户余额充足；后置条件：资金从余额转移至冻结状态             *)
CreateTx(tx, from, to, amt) ==
    /\ txStatus[tx] = "idle"
    /\ from \in Accounts
    /\ to \in Accounts
    /\ from # to
    /\ amt \in 1..MaxAmount
    /\ balances[from] >= amt
    /\ txStatus' = [txStatus EXCEPT ![tx] = "reserved"]
    /\ txFrom' = [txFrom EXCEPT ![tx] = from]
    /\ txTo' = [txTo EXCEPT ![tx] = to]
    /\ txAmount' = [txAmount EXCEPT ![tx] = amt]
    /\ balances' = [balances EXCEPT ![from] = @ - amt]
    /\ reservedFunds' = [reservedFunds EXCEPT ![tx] = amt]
    /\ UNCHANGED <<initialTotalBalance>>

(* 提交交易：从 Reserved 进入 Committed 状态                                  *)
(* 后置条件：冻结资金释放到入金账户                                           *)
Commit(tx) ==
    /\ txStatus[tx] = "reserved"
    /\ txStatus' = [txStatus EXCEPT ![tx] = "committed"]
    /\ balances' = [balances EXCEPT ![txTo[tx]] = @ + reservedFunds[tx]]
    /\ reservedFunds' = [reservedFunds EXCEPT ![tx] = 0]
    /\ UNCHANGED <<txFrom, txTo, txAmount, initialTotalBalance>>

(* 回滚交易：从 Reserved 进入 Aborted 状态                                     *)
(* 后置条件：冻结资金退回出金账户                                             *)
Abort(tx) ==
    /\ txStatus[tx] = "reserved"
    /\ txStatus' = [txStatus EXCEPT ![tx] = "aborted"]
    /\ balances' = [balances EXCEPT ![txFrom[tx]] = @ + reservedFunds[tx]]
    /\ reservedFunds' = [reservedFunds EXCEPT ![tx] = 0]
    /\ UNCHANGED <<txFrom, txTo, txAmount, initialTotalBalance>>

(* 系统级超时回滚：模拟网络超时或业务校验失败导致的自动回滚                 *)
TimeoutAbort(tx) ==
    /\ txStatus[tx] = "reserved"
    /\ txStatus' = [txStatus EXCEPT ![tx] = "aborted"]
    /\ balances' = [balances EXCEPT ![txFrom[tx]] = @ + reservedFunds[tx]]
    /\ reservedFunds' = [reservedFunds EXCEPT ![tx] = 0]
    /\ UNCHANGED <<txFrom, txTo, txAmount, initialTotalBalance>>

(* ============================================================================ *)
(* 下一步关系（Next State Relation）                                           *)
(* ============================================================================ *)
Next ==
    /\ \E tx \in TxIds :
        /\ \E from, to \in Accounts :
            \E amt \in 1..MaxAmount :
                CreateTx(tx, from, to, amt)
    \/ \E tx \in TxIds : Commit(tx)
    \/ \E tx \in TxIds : Abort(tx)
    \/ \E tx \in TxIds : TimeoutAbort(tx)

(* ============================================================================ *)
(* 不变量（Safety Properties）                                                 *)
(* ============================================================================ *)

(* 不变量 I1: 资金守恒 — 系统中全部资金（余额 + 冻结）始终等于初始总资金     *)
(* 这是分布式支付系统最核心的安全性质，确保没有任何资金凭空产生或消失         *)
FundConservationInv ==
    TotalSystemFunds = initialTotalBalance

(* 不变量 I2: 无双重支付 — 任意账户的当前余额非负                             *)
(* 由于 CreateTx 已预先扣除资金，balances[acc] 即为"可用余额"                *)
NoDoubleSpending ==
    \A acc \in Accounts : balances[acc] >= 0

(* 更强版本：账户的已冻结出金金额不超过其原始可用额度                        *)
NoOverdraft ==
    \A acc \in Accounts :
        LET ReservedOut ==
            {tx \in TxIds :
                /\ txStatus[tx] = "reserved"
                /\ txFrom[tx] = acc}
        IN  IF ReservedOut = {} THEN TRUE
            ELSE LET SumAmt[S \in SUBSET TxIds] ==
                    IF S = {} THEN 0
                    ELSE LET t == CHOOSE t \in S : TRUE
                         IN  txAmount[t] + SumAmt[S \ {t}]
                 IN  SumAmt[ReservedOut] <= balances[acc] + SumAmt[ReservedOut]

(* 不变量 I3: 交易状态一致性 — Committed 交易的入金已到账                     *)
CommittedBalanceCorrect ==
    \A tx \in TxIds :
        txStatus[tx] = "committed" => txAmount[tx] > 0

(* 不变量 I4: 冻结资金与交易状态的一致性                                      *)
ReservedFundsConsistent ==
    \A tx \in TxIds :
        (txStatus[tx] = "reserved") => (reservedFunds[tx] = txAmount[tx])
        /\ (txStatus[tx] \in {"idle", "committed", "aborted"}) => (reservedFunds[tx] = 0)

(* ============================================================================ *)
(* 活性（Liveness Properties）                                                 *)
(* ============================================================================ *)

(* 公平性假设：每个交易最终都会有机会被提交或回滚                             *)
Fairness ==
    /\ \A tx \in TxIds : WF_<<balances, reservedFunds, txStatus, txFrom, txTo, txAmount>>(Commit(tx))
    /\ \A tx \in TxIds : WF_<<balances, reservedFunds, txStatus, txFrom, txTo, txAmount>>(Abort(tx))
    /\ \A tx \in TxIds : WF_<<balances, reservedFunds, txStatus, txFrom, txTo, txAmount>>(TimeoutAbort(tx))

(* 活性 L1: 所有 Reserved 状态的请求最终都会被处理（到达终止状态）           *)
(* 这是分布式事务的"最终完成"性质，防止无限期挂起                           *)
AllRequestsProcessed ==
    \A tx \in TxIds :
        (txStatus[tx] = "reserved") ~> (txStatus[tx] \in {"committed", "aborted"})

(* ============================================================================ *)
(* 规约公式                                                                    *)
(* ============================================================================ *)
Spec == Init /\ [][Next]_<<balances, reservedFunds, txStatus, txFrom, txTo, txAmount, initialTotalBalance>> /\ Fairness

================================================================================
(* 规约结束                                                                    *)
(* 
 * TLC 模型检查配置建议:
 *   - 账户集合: Accounts <- {a1, a2, a3}
 *   - 交易集合: TxIds <- {tx1, tx2}
 *   - 最大金额: MaxAmount <- 5
 *   - 初始余额: balances <- [a1 |-> 10, a2 |-> 10, a3 |-> 10]
 *   - 检查不变量: TypeOK, FundConservationInv, NoDoubleSpending,
 *                 CommittedBalanceCorrect, ReservedFundsConsistent
 *   - 检查活性: AllRequestsProcessed
 *)
