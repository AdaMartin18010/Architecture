(* Coq/Rocq 有界计数器不变量证明
   目标：证明 inc 操作保持 value <= limit 不变量

   编译：rocq compile bounded_counter.v
*)

From Stdlib Require Import Arith Lia.

(* ---------- 1. 计数器定义 ---------- *)
Record bounded_counter := {
  value : nat;
  limit : nat
}.

(* ---------- 2. 操作 ---------- *)
Definition inc (c : bounded_counter) : bounded_counter :=
  if value c <? limit c then
    {| value := S (value c); limit := limit c |}
  else c.

(* ---------- 3. 不变量 ---------- *)
Definition invariant (c : bounded_counter) := value c <= limit c.

(* ---------- 4. 证明 inc 保持不变量 ---------- *)
Theorem inc_preserves_invariant :
  forall c, invariant c -> invariant (inc c).
Proof.
  intros c H. unfold invariant, inc.
  destruct (value c <? limit c) eqn:E.
  - simpl. apply Nat.ltb_lt in E. lia.
  - exact H.
Qed.
