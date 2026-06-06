theory Turnstile
  imports Main
begin

(* 简单状态机：旋转门
   状态：locked（是否锁定）、alarm（是否报警）
   事件：Coin（投币）、Push（推杆）
   目标：证明 ok 不变量在 step 后保持
*)

record turnstile =
  locked :: bool
  alarm  :: bool

datatype event = Coin | Push

fun step :: "event \<Rightarrow> turnstile \<Rightarrow> turnstile" where
  "step Coin s = s\<lparr>locked := False, alarm := False\<rparr>" |
  "step Push s = (if locked s
                  then s\<lparr>alarm := True\<rparr>
                  else s\<lparr>locked := True\<rparr>)"

definition ok :: "turnstile \<Rightarrow> bool" where
  "ok s \<longleftrightarrow> (\<not> locked s) \<longrightarrow> (\<not> alarm s)"

lemma ok_step: "ok s \<Longrightarrow> ok (step e s)"
  by (cases e) (auto simp: ok_def)

end
