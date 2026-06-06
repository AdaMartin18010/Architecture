#!/usr/bin/env python3
"""
COCOMO II 复用模型 2026 版计算器

按 SUBSEQUENT_PLAN_2026.md 决策 3A 开发：Python CLI 快速原型
对齐来源：USC COCOMO II Model Definition Manual (Boehm et al.)

基本公式：
  PM = A * SIZE^E * EM
  其中 SIZE = (AAF * KSLOC_reused) 的等效新代码量

用法:
    python cocomo-calculator.py --ksloc-reused 50 --aaf 0.4 --em 1.2
"""

import argparse
import math
import sys

# COCOMO II 默认值（需根据组织历史数据校准）
DEFAULT_A = 2.94  # COCOMO II.2000 校准系数
DEFAULT_B = 0.91  # 规模指数基数


def calculate_effort(ksloc_reused: float, aaf: float, em: float, a: float = DEFAULT_A, b: float = DEFAULT_B):
    """
    计算复用项目的等效工作量和调整工作量。

    Args:
        ksloc_reused: 复用的千行源代码数
        aaf: Adaptation Adjustment Factor（改编调整因子），范围 0~1
        em: Effort Multiplier（工作量乘数），综合所有成本驱动因子
        a: COCOMO II 校准系数 A
        b: COCOMO II 校准系数 B

    Returns:
        dict: 包含等效规模、基础工作量、调整后工作量的字典
    """
    if not 0 <= aaf <= 1:
        raise ValueError("AAF 必须在 [0, 1] 范围内")
    if ksloc_reused < 0:
        raise ValueError("KSLOC_reused 不能为负数")

    # 等效新代码量（ESLOC）
    esloc = aaf * ksloc_reused

    # 规模指数 E（简单形式，未包含 SF 调整）
    e = b

    # 基础工作量（person-months）
    pm_nominal = a * (esloc ** e)

    # 调整后工作量
    pm_adjusted = pm_nominal * em

    return {
        "ksloc_reused": ksloc_reused,
        "aaf": aaf,
        "em": em,
        "esloc": esloc,
        "e": e,
        "pm_nominal": pm_nominal,
        "pm_adjusted": pm_adjusted,
    }


def main():
    parser = argparse.ArgumentParser(description="COCOMO II 复用模型 2026 版计算器")
    parser.add_argument("--ksloc-reused", type=float, required=True, help="复用的千行源代码数")
    parser.add_argument("--aaf", type=float, required=True, help="改编调整因子 Adaptation Adjustment Factor (0-1)")
    parser.add_argument("--em", type=float, default=1.0, help="工作量乘数 Effort Multiplier (默认 1.0)")
    parser.add_argument("--a", type=float, default=DEFAULT_A, help=f"COCOMO A 系数 (默认 {DEFAULT_A})")
    parser.add_argument("--b", type=float, default=DEFAULT_B, help=f"COCOMO B 系数 (默认 {DEFAULT_B})")

    args = parser.parse_args()

    try:
        result = calculate_effort(args.ksloc_reused, args.aaf, args.em, args.a, args.b)
    except ValueError as e:
        print(f"输入错误: {e}", file=sys.stderr)
        return 1

    print("=" * 50)
    print("COCOMO II 复用模型 2026 版计算结果")
    print("=" * 50)
    print(f"复用代码量 (KSLOC):     {result['ksloc_reused']:.2f}")
    print(f"改编调整因子 (AAF):     {result['aaf']:.2f}")
    print(f"工作量乘数 (EM):        {result['em']:.2f}")
    print(f"等效新代码量 (ESLOC):   {result['esloc']:.2f}")
    print(f"规模指数 (E):           {result['e']:.2f}")
    print(f"基础工作量 (PM):        {result['pm_nominal']:.2f} 人月")
    print(f"调整后工作量 (PM_adj):  {result['pm_adjusted']:.2f} 人月")
    print("=" * 50)
    print("\n判定:")
    if result["aaf"] >= 0.7:
        print("⚠️  AAF ≥ 0.7：复用的直接经济价值已较低，需依赖战略价值 justify")
    else:
        print("✅ AAF < 0.7：复用具备直接经济价值")

    return 0


if __name__ == "__main__":
    sys.exit(main())
