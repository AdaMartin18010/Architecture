#!/usr/bin/env python3
"""
AI 功能概率契约校准工具

用途：
    为 LLM 生成的功能/代码/Tools 提供基于 Conformal Prediction 的统计保证。
    输出形如 P(correctness) >= 1-alpha 的概率契约边界。

理论基础：
    - Split Conformal Prediction (Vovk, Gammerman, Shafer; Angelopoulos & Bates)
    - 边际覆盖保证：在 calibration 与 test 数据可交换时，
      P(Y_{n+1} in C(X_{n+1})) >= 1-alpha

按 SUBSEQUENT_PLAN_2026.md 决策 3A 开发：Python CLI 快速原型

用法:
    python calibration-tool.py --calibration correctness_scores.json --alpha 0.05
    python calibration-tool.py --sample --n-cal 200 --alpha 0.10

权威来源:
    - Angelopoulos & Bates, "A Gentle Introduction to Conformal Prediction" (2021)
      https://arxiv.org/abs/2107.07511
    - Ye et al., "Verina: Benchmarking Verifiable Code Generation" (2025)
      https://arxiv.org/abs/2505.23135
"""

import argparse
import json
import math
import random
import sys
from pathlib import Path
from typing import List, Tuple


def load_scores(path: str) -> List[float]:
    """加载校准分数。支持 JSON 列表或每行一个分数的文本文件。"""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"校准文件不存在: {path}")

    if p.suffix == ".json":
        with p.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict) and "scores" in data:
            scores = data["scores"]
        elif isinstance(data, list):
            scores = data
        else:
            raise ValueError("JSON 文件必须是分数列表或包含 'scores' 字段的对象")
    else:
        scores = []
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    scores.append(float(line))

    if not scores:
        raise ValueError("校准分数为空")
    if any(not (0.0 <= s <= 1.0) for s in scores):
        raise ValueError("所有分数必须在 [0.0, 1.0] 范围内")

    return scores


def conformal_threshold(scores: List[float], alpha: float) -> float:
    """
    计算 conformal 阈值。

    假设 scores 是某种“非合规分数”或“错误概率”的估计。
    这里我们将 scores 解释为：s = 1 - correctness_score，
    即 s 越高表示越不可信。

    返回阈值 q，使得在 calibration 数据上：
        P(s_test <= q) >= 1-alpha
    """
    n = len(scores)
    # 计算分位数索引：向上取整 ((1-alpha) * (n+1)) / n
    # 对应 Split Conformal Prediction 中的标准公式
    k = math.ceil((1 - alpha) * (n + 1))
    k = min(k, n)  # 不能超过 n

    sorted_scores = sorted(scores)
    q = sorted_scores[k - 1]  # 0-indexed
    return q


def predict_set(candidates: List[dict], q: float, score_key: str = "error_score") -> Tuple[List[dict], bool]:
    """
    根据 conformal 阈值过滤候选。

    返回：
        selected: 被选中的候选列表（s <= q）
        abstain: 是否建议弃权（无候选通过或太多候选不通过）
    """
    selected = [c for c in candidates if c.get(score_key, 1.0) <= q]
    abstain = len(selected) == 0
    return selected, abstain


def generate_sample_data(n_cal: int, seed: int = 42) -> List[float]:
    """生成示例校准数据，模拟 LLM 代码生成的错误率分布。"""
    rng = random.Random(seed)
    scores = []
    for _ in range(n_cal):
        # 模拟：大多数生成质量较高（低 error_score），少数较差
        if rng.random() < 0.85:
            scores.append(rng.betavariate(2.0, 8.0))  # 低错误率
        else:
            scores.append(rng.betavariate(5.0, 3.0))  # 高错误率
    return scores


def generate_sample_candidates(n: int, seed: int = 100) -> List[dict]:
    """生成示例候选函数及其错误分数。"""
    rng = random.Random(seed)
    candidates = []
    for i in range(n):
        if rng.random() < 0.7:
            error_score = rng.betavariate(2.0, 8.0)
        else:
            error_score = rng.betavariate(5.0, 3.0)
        candidates.append({
            "id": f"candidate-{i+1}",
            "error_score": round(error_score, 4),
            "description": f"Generated function variant {i+1}",
        })
    return candidates


def main():
    parser = argparse.ArgumentParser(
        description="AI 功能概率契约校准工具（基于 Conformal Prediction）"
    )
    parser.add_argument(
        "--calibration",
        type=str,
        help="校准分数文件路径（JSON 列表或每行一个分数的文本文件）",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.10,
        help="期望的错误率上限 alpha（默认 0.10，即 90% 覆盖保证）",
    )
    parser.add_argument(
        "--candidates",
        type=str,
        help="候选文件路径（JSON 列表，每个元素需包含 error_score）",
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="使用示例数据运行演示",
    )
    parser.add_argument(
        "--n-cal",
        type=int,
        default=200,
        help="示例校准样本数（默认 200）",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="输出契约 JSON 文件路径",
    )

    args = parser.parse_args()

    if not (0 < args.alpha < 1):
        print("错误: alpha 必须在 (0, 1) 区间内", file=sys.stderr)
        return 1

    # 加载或生成校准分数
    if args.sample:
        scores = generate_sample_data(args.n_cal)
        print(f"[演示模式] 生成 {len(scores)} 条示例校准数据\n")
    elif args.calibration:
        scores = load_scores(args.calibration)
    else:
        parser.print_help()
        return 1

    # 计算 conformal 阈值
    q = conformal_threshold(scores, args.alpha)
    correctness_lower_bound = max(0.0, 1.0 - q)

    # 加载或生成候选
    if args.sample:
        candidates = generate_sample_candidates(10)
    elif args.candidates:
        with open(args.candidates, "r", encoding="utf-8") as f:
            candidates = json.load(f)
    else:
        candidates = []

    # 如果提供了候选，执行选择
    selected, abstain = predict_set(candidates, q) if candidates else ([], False)

    # 构建契约输出
    contract = {
        "protocol": "Conformal Prediction (Split CP)",
        "alpha": args.alpha,
        "coverage_guarantee": f"P(correctness) >= {1 - args.alpha:.2%}",
        "calibration_size": len(scores),
        "conformal_threshold_q": round(q, 4),
        "correctness_lower_bound": round(correctness_lower_bound, 4),
        "interpretation": (
            f"对于与 calibration 数据同分布的新样本，"
            f"其 error_score <= {q:.4f} 的候选至少有 {1 - args.alpha:.1%} 的概率是正确的。"
        ),
    }

    if candidates:
        contract["candidates_evaluated"] = len(candidates)
        contract["candidates_selected"] = len(selected)
        contract["abstain"] = abstain
        contract["selected_candidates"] = [
            {"id": c["id"], "error_score": c["error_score"]} for c in selected
        ]

    print("=" * 60)
    print("AI 功能概率契约")
    print("=" * 60)
    print(json.dumps(contract, ensure_ascii=False, indent=2))
    print("=" * 60)

    if args.sample:
        print("\n[示例候选过滤结果]")
        print(f"  评估候选: {len(candidates)}")
        print(f"  选中候选: {len(selected)}")
        print(f"  建议弃权: {'是' if abstain else '否'}")
        if selected:
            print("  选中列表:")
            for c in selected:
                print(f"    - {c['id']}: error_score={c['error_score']:.4f}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(contract, f, ensure_ascii=False, indent=2)
        print(f"\n契约已保存到: {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
