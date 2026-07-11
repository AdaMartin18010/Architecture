theory InsertionSort
  imports Main "HOL-Library.Multiset"
begin

(* 插入排序正确性证明：
   1. isort_sorted   — 输出有序
   2. isort_permutation — 输出是输入的排列

   【定位标注】教学示例：演示证明工具用法，非本项目公理体系
   （M/E/S/P 公理与 Th 定理）的形式化。公理→形式化规约的完整映射见：
   struct/01-meta-model-standards/06-formal-axioms/formalization-mapping.md
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
