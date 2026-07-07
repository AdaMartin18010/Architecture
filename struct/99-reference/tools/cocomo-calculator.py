#!/usr/bin/env python3
"""
COCOMO II + 复用投资回报计算器

基于 USC COCOMO II Model Definition Manual (Boehm et al.) 的简化模型，
在计算复用工作量的同时，评估复用资产的投资回报（NPV、ROI、投资回收期）。

基本公式：
    PM = A * SIZE^E * EM
    SIZE = AAF * KSLOC_reused  （等效新代码量）

投资回报模型：
    不复用成本 = PM_no_reuse * cost_per_pm
    复用成本   = PM_reuse * cost_per_pm
    年节省     = (no_reuse_cost - reuse_cost) * reuse_savings_rate
    NPV        = -initial_investment + Σ(annual_savings / (1 + discount_rate)^t)
    ROI        = (累计节省 - 初始投资) / 初始投资 * 100%

用法示例：
    # 基础用法
    python cocomo-calculator.py --ksloc-reused 50 --aaf 0.4 --em 1.2

    # 投资回报分析
    python cocomo-calculator.py --ksloc-reused 100 --aaf 0.3 --em 1.0 \
        --cost-per-pm 25000 --reuse-savings-rate 0.3 \
        --initial-investment 200000 --periods 5 --discount-rate 0.08

    # 运行默认示例并保存结果
    python cocomo-calculator.py --example --output-json result.json --output-csv result.csv
"""

import argparse
import csv
import json
import math
import sys
from pathlib import Path

# COCOMO II 默认值（需根据组织历史数据校准）
DEFAULT_A = 2.94  # COCOMO II.2000 校准系数
DEFAULT_B = 0.91  # 规模指数基数

# 经济模型默认值
DEFAULT_COST_PER_PM = 25000  # CNY / 人月
DEFAULT_REUSE_SAVINGS_RATE = 0.30
DEFAULT_INITIAL_INVESTMENT = 0.0
DEFAULT_PERIODS = 3
DEFAULT_DISCOUNT_RATE = 0.08


def calculate_effort(
    ksloc_reused: float,
    aaf: float,
    em: float,
    a: float = DEFAULT_A,
    b: float = DEFAULT_B,
):
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

    esloc = aaf * ksloc_reused
    e = b
    pm_nominal = a * (esloc ** e)
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


def calculate_investment_metrics(
    no_reuse_cost: float,
    reuse_cost: float,
    reuse_savings_rate: float,
    initial_investment: float,
    periods: int,
    discount_rate: float,
):
    """
    计算复用投资回报指标。

    Args:
        no_reuse_cost: 不复用场景的总成本
        reuse_cost: 复用场景的总成本
        reuse_savings_rate: 每年实际实现的复用节省比例（0-1）
        initial_investment: 复用资产的初始投资
        periods: 收益期数（年）
        discount_rate: 年折现率（0-1）

    Returns:
        dict: 包含 NPV、ROI、投资回收期等字段的字典
    """
    if periods < 1:
        raise ValueError("periods 必须大于等于 1")
    if not 0 <= reuse_savings_rate <= 1:
        raise ValueError("reuse_savings_rate 必须在 [0, 1] 范围内")
    if discount_rate < 0:
        raise ValueError("discount_rate 不能为负数")

    annual_savings = max(0.0, no_reuse_cost - reuse_cost) * reuse_savings_rate

    cash_flows = [-initial_investment]
    for t in range(1, periods + 1):
        cash_flows.append(annual_savings / ((1 + discount_rate) ** t))

    npv = sum(cash_flows)
    total_undiscounted_savings = annual_savings * periods

    # ROI：基于整个收益期的简单回报
    if initial_investment == 0:
        if total_undiscounted_savings > 0:
            roi_percent = math.inf
        else:
            roi_percent = 0.0
    else:
        roi_percent = ((total_undiscounted_savings - initial_investment) / initial_investment) * 100.0

    # 投资回收期（支持分数年）
    if annual_savings <= 0:
        payback_period = None  # 无法回收
    elif initial_investment <= 0:
        payback_period = 0.0
    else:
        cumulative = 0.0
        payback_period = None
        for t in range(1, periods + 1):
            cumulative += annual_savings / ((1 + discount_rate) ** t)
            if cumulative >= initial_investment:
                # 线性插值到更精确的回收点
                prev_cumulative = cumulative - annual_savings / ((1 + discount_rate) ** t)
                fraction = (
                    0.0
                    if t == 1 and prev_cumulative >= initial_investment
                    else (initial_investment - prev_cumulative)
                    / (cumulative - prev_cumulative)
                )
                payback_period = (t - 1) + fraction
                break
        if payback_period is None:
            payback_period = f"> {periods} 年"

    return {
        "annual_savings": annual_savings,
        "total_undiscounted_savings": total_undiscounted_savings,
        "cash_flows": cash_flows,
        "npv": npv,
        "roi_percent": roi_percent,
        "payback_period": payback_period,
    }


def build_result(args):
    """根据参数构建完整计算结果。"""
    # 复用场景
    reuse = calculate_effort(
        args.ksloc_reused, args.aaf, args.em, args.a, args.b
    )

    # 不复用场景：AAF = 1.0（全部按新代码开发）
    no_reuse = calculate_effort(
        args.ksloc_reused, 1.0, args.em, args.a, args.b
    )

    no_reuse_cost = no_reuse["pm_adjusted"] * args.cost_per_pm
    reuse_cost = reuse["pm_adjusted"] * args.cost_per_pm
    absolute_savings = no_reuse_cost - reuse_cost
    savings_percent = (
        (absolute_savings / no_reuse_cost * 100.0) if no_reuse_cost > 0 else 0.0
    )

    investment = calculate_investment_metrics(
        no_reuse_cost=no_reuse_cost,
        reuse_cost=reuse_cost,
        reuse_savings_rate=args.reuse_savings_rate,
        initial_investment=args.initial_investment,
        periods=args.periods,
        discount_rate=args.discount_rate,
    )

    return {
        "inputs": {
            "ksloc_reused": args.ksloc_reused,
            "aaf": args.aaf,
            "em": args.em,
            "a": args.a,
            "b": args.b,
            "cost_per_pm": args.cost_per_pm,
            "currency": "CNY",
            "reuse_savings_rate": args.reuse_savings_rate,
            "initial_investment": args.initial_investment,
            "periods": args.periods,
            "discount_rate": args.discount_rate,
        },
        "cocomo": {
            "no_reuse": {
                "esloc": no_reuse["esloc"],
                "pm_adjusted": no_reuse["pm_adjusted"],
                "cost": no_reuse_cost,
            },
            "reuse": {
                "esloc": reuse["esloc"],
                "pm_adjusted": reuse["pm_adjusted"],
                "cost": reuse_cost,
            },
        },
        "savings": {
            "absolute": absolute_savings,
            "percent": savings_percent,
        },
        "investment": {
            "annual_savings": investment["annual_savings"],
            "total_undiscounted_savings": investment["total_undiscounted_savings"],
            "cash_flows": investment["cash_flows"],
            "npv": investment["npv"],
            "roi_percent": investment["roi_percent"],
            "payback_period": investment["payback_period"],
        },
    }


def format_currency(value: float) -> str:
    """将数值格式化为人民币货币字符串。"""
    if value is None or (isinstance(value, float) and math.isinf(value)):
        return "N/A"
    return f"{value:,.2f} CNY"


def format_roi(roi_percent: float) -> str:
    """格式化 ROI 输出。"""
    if math.isinf(roi_percent):
        return "+∞%"
    return f"{roi_percent:,.2f}%"


def format_payback(payback_period) -> str:
    """格式化投资回收期输出。"""
    if payback_period is None:
        return "无法回收"
    if isinstance(payback_period, str):
        return payback_period
    return f"{payback_period:.2f} 年"


def print_report(result: dict):
    """打印计算结果报告。"""
    inputs = result["inputs"]
    no_reuse = result["cocomo"]["no_reuse"]
    reuse = result["cocomo"]["reuse"]
    savings = result["savings"]
    inv = result["investment"]

    print("=" * 60)
    print("COCOMO II + 复用投资回报计算报告")
    print("=" * 60)
    print(f"复用代码量 (KSLOC):         {inputs['ksloc_reused']:.2f}")
    print(f"改编调整因子 (AAF):         {inputs['aaf']:.2f}")
    print(f"工作量乘数 (EM):            {inputs['em']:.2f}")
    print(f"人月成本:                   {format_currency(inputs['cost_per_pm'])}")
    print(f"复用节省率:                 {inputs['reuse_savings_rate']*100:.1f}%")
    print(f"初始投资:                   {format_currency(inputs['initial_investment'])}")
    print(f"收益期数:                   {inputs['periods']} 年")
    print(f"折现率:                     {inputs['discount_rate']*100:.1f}%")
    print("-" * 60)
    print(f"不复用场景等效规模 (ESLOC): {no_reuse['esloc']:.2f}")
    print(f"不复用场景工作量:           {no_reuse['pm_adjusted']:.2f} 人月")
    print(f"不复用场景成本:             {format_currency(no_reuse['cost'])}")
    print("-" * 60)
    print(f"复用场景等效规模 (ESLOC):   {reuse['esloc']:.2f}")
    print(f"复用场景工作量:             {reuse['pm_adjusted']:.2f} 人月")
    print(f"复用场景成本:               {format_currency(reuse['cost'])}")
    print("-" * 60)
    print(f"节省成本（绝对）:           {format_currency(savings['absolute'])}")
    print(f"节省成本（百分比）:         {savings['percent']:.2f}%")
    print(f"年均可实现节省:             {format_currency(inv['annual_savings'])}")
    print("-" * 60)
    print(f"NPV（净现值）:              {format_currency(inv['npv'])}")
    print(f"ROI（投资回报率）:          {format_roi(inv['roi_percent'])}")
    print(f"投资回收期:                 {format_payback(inv['payback_period'])}")
    print("=" * 60)

    # 判定
    if inputs["aaf"] >= 0.7:
        print("⚠️  AAF ≥ 0.7：复用的直接经济价值已较低，需依赖战略价值 justify")
    else:
        print("✅ AAF < 0.7：复用具备直接经济价值")


def save_json(result: dict, path: str):
    """将结果保存为 JSON。"""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存为 JSON: {file_path.resolve()}")


def save_csv(result: dict, path: str):
    """将结果保存为 CSV。"""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    rows = [
        ["指标", "值", "单位"],
        ["复用代码量 (KSLOC)", result["inputs"]["ksloc_reused"], ""],
        ["AAF", result["inputs"]["aaf"], ""],
        ["EM", result["inputs"]["em"], ""],
        ["人月成本", result["inputs"]["cost_per_pm"], "CNY"],
        ["复用节省率", result["inputs"]["reuse_savings_rate"] * 100, "%"],
        ["初始投资", result["inputs"]["initial_investment"], "CNY"],
        ["收益期数", result["inputs"]["periods"], "年"],
        ["折现率", result["inputs"]["discount_rate"] * 100, "%"],
        ["不复用工作量", result["cocomo"]["no_reuse"]["pm_adjusted"], "人月"],
        ["不复用成本", result["cocomo"]["no_reuse"]["cost"], "CNY"],
        ["复用工作量", result["cocomo"]["reuse"]["pm_adjusted"], "人月"],
        ["复用成本", result["cocomo"]["reuse"]["cost"], "CNY"],
        ["节省成本（绝对）", result["savings"]["absolute"], "CNY"],
        ["节省成本（百分比）", result["savings"]["percent"], "%"],
        ["年均可实现节省", result["investment"]["annual_savings"], "CNY"],
        ["NPV", result["investment"]["npv"], "CNY"],
        ["ROI", result["investment"]["roi_percent"], "%"],
        ["投资回收期", result["investment"]["payback_period"], "年"],
    ]

    with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"结果已保存为 CSV: {file_path.resolve()}")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="COCOMO II + 复用投资回报计算器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --ksloc-reused 50 --aaf 0.4 --em 1.2
  %(prog)s --ksloc-reused 100 --aaf 0.3 --em 1.0 \
           --cost-per-pm 25000 --reuse-savings-rate 0.3 \
           --initial-investment 200000 --periods 5 --discount-rate 0.08
  %(prog)s --example --output-json result.json
""",
    )
    parser.add_argument("--ksloc-reused", type=float, help="复用的千行源代码数")
    parser.add_argument("--aaf", type=float, help="改编调整因子 (0-1)")
    parser.add_argument("--em", type=float, default=1.0, help="工作量乘数 (默认 1.0)")
    parser.add_argument("--a", type=float, default=DEFAULT_A, help=f"COCOMO A 系数 (默认 {DEFAULT_A})")
    parser.add_argument("--b", type=float, default=DEFAULT_B, help=f"COCOMO B 系数 (默认 {DEFAULT_B})")
    parser.add_argument(
        "--cost-per-pm", type=float, default=DEFAULT_COST_PER_PM,
        help=f"每人每月成本，单位 CNY (默认 {DEFAULT_COST_PER_PM})",
    )
    parser.add_argument(
        "--reuse-savings-rate", type=float, default=DEFAULT_REUSE_SAVINGS_RATE,
        help=f"每年实际实现的复用节省比例 (默认 {DEFAULT_REUSE_SAVINGS_RATE})",
    )
    parser.add_argument(
        "--initial-investment", type=float, default=DEFAULT_INITIAL_INVESTMENT,
        help=f"复用资产初始投资，单位 CNY (默认 {DEFAULT_INITIAL_INVESTMENT})",
    )
    parser.add_argument(
        "--periods", type=int, default=DEFAULT_PERIODS,
        help=f"收益期数，单位年 (默认 {DEFAULT_PERIODS})",
    )
    parser.add_argument(
        "--discount-rate", type=float, default=DEFAULT_DISCOUNT_RATE,
        help=f"年折现率 (默认 {DEFAULT_DISCOUNT_RATE})",
    )
    parser.add_argument("--output-json", type=str, help="将结果保存为 JSON 文件")
    parser.add_argument("--output-csv", type=str, help="将结果保存为 CSV 文件")
    parser.add_argument(
        "--example", action="store_true",
        help="运行默认示例：KSLOC=100, AAF=0.3, EM=1.0, 初始投资 200,000 CNY, 5 年期",
    )

    args = parser.parse_args(argv)

    if args.example:
        args.ksloc_reused = args.ksloc_reused if args.ksloc_reused is not None else 100.0
        args.aaf = args.aaf if args.aaf is not None else 0.30
        args.em = args.em if args.em is not None else 1.0
        args.initial_investment = (
            args.initial_investment
            if args.initial_investment != DEFAULT_INITIAL_INVESTMENT
            else 200000.0
        )
        args.periods = args.periods if args.periods != DEFAULT_PERIODS else 5
    elif args.ksloc_reused is None or args.aaf is None:
        parser.error("必须提供 --ksloc-reused 和 --aaf，或使用 --example 运行示例")

    return args


def main(argv=None):
    args = parse_args(argv)

    try:
        result = build_result(args)
    except ValueError as e:
        print(f"输入错误: {e}", file=sys.stderr)
        return 1

    print_report(result)

    if args.output_json:
        save_json(result, args.output_json)
    if args.output_csv:
        save_csv(result, args.output_csv)

    return 0


if __name__ == "__main__":
    sys.exit(main())
