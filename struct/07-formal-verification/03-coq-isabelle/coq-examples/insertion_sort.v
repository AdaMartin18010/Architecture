(* Coq/Rocq 插入排序正确性证明
   目标：
   1. insertion_sort_sorted — 输出列表按升序排列
   2. insertion_sort_count — 输出保持元素计数不变（排列）

   编译：rocq compile insertion_sort.v
   兼容 Rocq 9.0+（使用 Stdlib 前缀）
*)

From Stdlib Require Import Arith List Lia.
Import ListNotations.

(* ---------- 1. 排序谓词 ---------- *)
Inductive sorted : list nat -> Prop :=
| sorted_nil  : sorted []
| sorted_one  : forall x, sorted [x]
| sorted_cons : forall x y l,
    x <= y -> sorted (y :: l) -> sorted (x :: y :: l).

(* ---------- 2. 插入排序实现 ---------- *)
Fixpoint insert (x : nat) (l : list nat) : list nat :=
  match l with
  | []      => [x]
  | y :: ys =>
      if x <=? y then x :: y :: ys else y :: insert x ys
  end.

Fixpoint insertion_sort (l : list nat) : list nat :=
  match l with
  | []      => []
  | x :: xs => insert x (insertion_sort xs)
  end.

(* ---------- 3. 插入保持有序 ---------- *)
Lemma insert_sorted :
  forall x l, sorted l -> sorted (insert x l).
Proof.
  intros x l H. induction H.
  - simpl. constructor.
  - simpl. destruct (x <=? x0) eqn:E.
    + constructor; [apply Nat.leb_le; exact E | constructor].
    + constructor; [apply Nat.leb_gt in E; lia | constructor].
  - simpl. destruct (x <=? x0) eqn:E.
    + constructor; [apply Nat.leb_le; exact E | constructor; assumption].
    + simpl. destruct (x <=? y) eqn:E2.
      * constructor; [apply Nat.leb_gt in E; lia | constructor; assumption].
      * constructor; [assumption | apply IHsorted].
Qed.

(* ---------- 4. 插入排序输出有序 ---------- *)
Theorem insertion_sort_sorted :
  forall l, sorted (insertion_sort l).
Proof.
  intros l. induction l.
  - simpl. constructor.
  - simpl. apply insert_sorted. exact IHl.
Qed.

(* ---------- 5. 元素计数 ---------- *)
Fixpoint count (v : nat) (l : list nat) : nat :=
  match l with
  | []      => 0
  | x :: xs => (if v =? x then 1 else 0) + count v xs
  end.

Lemma count_insert :
  forall x v l,
    count v (insert x l) = (if v =? x then 1 else 0) + count v l.
Proof.
  intros x v l; induction l as [|y ys IH]; simpl.
  - destruct (v =? x); reflexivity.
  - destruct (x <=? y); simpl; rewrite IH;
      destruct (v =? y); destruct (v =? x); reflexivity.
Qed.

(* ---------- 6. 插入排序保持计数 ---------- *)
Theorem insertion_sort_count :
  forall v l, count v (insertion_sort l) = count v l.
Proof.
  intros v l; induction l as [|x xs IH]; simpl.
  - reflexivity.
  - rewrite count_insert, IH. reflexivity.
Qed.
