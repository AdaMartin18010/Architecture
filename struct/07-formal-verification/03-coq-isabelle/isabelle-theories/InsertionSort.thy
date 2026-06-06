theory InsertionSort
  imports Main "HOL-Library.Multiset"
begin

(* 插入排序正确性证明：
   1. isort_sorted   — 输出有序
   2. isort_permutation — 输出是输入的排列
*)

fun insort :: "nat \<Rightarrow> nat list \<Rightarrow> nat list" where
  "insort x [] = [x]" |
  "insort x (y#ys) = (if x \<le> y then x#y#ys else y#(insort x ys))"

fun isort :: "nat list \<Rightarrow> nat list" where
  "isort [] = []" |
  "isort (x#xs) = insort x (isort xs)"

lemma insort_sorted: "sorted xs \<Longrightarrow> sorted (insort x xs)"
  by (induct xs) auto

lemma insort_mset: "mset (insort x xs) = add_mset x (mset xs)"
  by (induct xs) auto

theorem isort_sorted: "sorted (isort xs)"
  by (induct xs) (auto simp: insort_sorted)

theorem isort_permutation: "mset (isort xs) = mset xs"
  by (induct xs) (auto simp: insort_mset)

end
