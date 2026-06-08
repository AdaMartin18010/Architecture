#!/usr/bin/env python3
"""
COCOMO II 2026 复用计算器 (MVP)

命令行工具，支持 AAM/SU/UNFM 参数输入，输出 ESLOC、工作量、工期、ROI。

Usage:
    python cocomo-calculator.py --sloc 50000 --aam 0.3 --su 0.4 --unfm 1.0 --effort 120
    python cocomo-calculator.py --sloc 100000 --aam 0.2 --su 0.5 --unfm 0.85 --effort 200 --mode intermediate

Parameters:
    --sloc      目标系统总源代码行数 (Source Lines of Code)
    --aam       改编调整因子 (Adaptation Adjustment Modifier), 范围 [0.0, 1.0]
    --su        软件理解度 (Software Understanding), 范围 [0.0, 1.0]
    --unfm      未熟悉度 (Unfamiliarity), 范围 [0.0, 1.0]
    --effort    实际投入工作量（人月），用于 ROI 计算
    --mode      计算模式: basic | intermediate (默认: basic)

Reference:
    - COCOMO II Model Definition Manual (Boehm et al., USC)
    - ISO/IEC 26550:2015 产品线工程与复用
"""

import argparse
import math
import sys


def compute_esloc(sloc: int, aam: float, su: float, unfm: float) -> float:
    """
    计算等效新源代码行数 (Equivalent New SLOC, ESLOC)。

    公式: ESLOC = SLOC * AAM * (SU + UNFM) / 2

    其中:
        AAM = 改编调整因子 (Adaptation Adjustment Modifier)
        SU  = 软件理解度 (Software Understanding)
        UNFM = 未熟悉度 (Unfamiliarity)

    Args:
        sloc: 目标系统总源代码行数
        aam: 改编调整因子 [0.0, 1.0]
        su: 软件理解度 [0.0, 1.0]
        unfm: 未熟悉度 [0.0, 1.0]

    Returns:
        ESLOC 值（浮点数）
    """
    if sloc < 0:
        raise ValueError("SLOC must be non-negative")
    if not (0.0 <= aam <= 1.0):
        raise ValueError("AAM must be in [0.0, 1.0]")
    if not (0.0 <= su <= 1.0):
        raise ValueError("SU must be in [0.0, 1.0]")
    if not (0.0 <= unfm <= 1.0):
        raise ValueError("UNFM must be in [0.0, 1.0]")

    # 综合复用调整因子 RAF (Reuse Adjustment Factor)
    raf = (su + unfm) / 2.0
    esloc = sloc * aam * raf
    return esloc


def compute_effort_basic(esloc: float) -> float:
    """
    COCOMO II Basic 模式工作量计算。

    公式: Effort = 2.94 * (ESLOC / 1000) ^ 1.099

    Args:
        esloc: 等效新源代码行数

    Returns:
        估计工作量（人月）
    """
    ks_loc = esloc / 1000.0
    effort = 2.94 * math.pow(ks_loc, 1.099)
    return effort


def compute_effort_intermediate(esloc: float, em_array: list[float]) -> float:
    """
    COCOMO II Intermediate 模式工作量计算。

    公式: Effort = 2.94 * (ESLOC / 1000) ^ 1.099 * ∏(EM_i)

    Args:
        esloc: 等效新源代码行数
        em_array: Effort Multipliers 列表（默认使用一组典型值）

    Returns:
        估计工作量（人月）
    """
    ks_loc = esloc / 1000.0
    base_effort = 2.94 * math.pow(ks_loc, 1.099)
    eaf = math.prod(em_array) if em_array else 1.0
    return base_effort * eaf


def compute_schedule(effort: float) -> float:
    """
    计算估计工期（月）。

    公式: Schedule = 3.67 * (Effort) ^ 0.3179

    Args:
        effort: 估计工作量（人月）

    Returns:
        估计工期（月）
    """
    if effort <= 0:
        return 0.0
    schedule = 3.67 * math.pow(effort, 0.3179)
    return schedule


def compute_roi(effort_reuse: float, effort_nominal: float, actual_effort: float = None) -> dict:
    """
    计算复用投资回报率 (ROI)。

    公式:
        成本节约 = effort_nominal - effort_reuse
        实际 ROI = (成本节约 - 实际投入) / 实际投入 * 100%
        理论 ROI = (成本节约) / effort_reuse * 100%

    Args:
        effort_reuse: 复用模式估计工作量
        effort_nominal: 从零开发估计工作量
        actual_effort: 实际投入工作量（人月），可选

    Returns:
        ROI 指标字典
    """
    cost_saving = effort_nominal - effort_reuse
    roi_nominal = (cost_saving / effort_reuse * 100.0) if effort_reuse > 0 else 0.0

    result = {
        "effort_nominal": effort_nominal,
        "effort_reuse": effort_reuse,
        "cost_saving": cost_saving,
        "roi_nominal_percent": roi_nominal,
    }

    if actual_effort is not None and actual_effort > 0:
        actual_saving = effort_nominal - actual_effort
        roi_actual = (actual_saving / actual_effort * 100.0)
        result["actual_effort"] = actual_effort
        result["actual_saving"] = actual_saving
        result["roi_actual_percent"] = roi_actual

    return result


def default_em_values() -> list[float]:
    """
    返回一组典型的 COCOMO II Effort Multipliers（中间 COCOMO 默认值）。

    所有乘数取 nominal (1.00) 作为 MVP 简化。
    """
    # 17 个成本驱动因子的典型 nominal 值
    return [1.00] * 17


def print_report(args, esloc, effort, schedule, roi_info, nominal_effort):
    """打印计算报告。"""
    print("=" * 60)
    print("COCOMO II 2026 复用计算器报告")
    print("=" * 60)
    print(f"  计算模式        : {args.mode}")
    print(f"  输入 SLOC       : {args.sloc:,}")
    print(f"  AAM (改编调整)  : {args.aam:.2f}")
    print(f"  SU  (理解度)    : {args.su:.2f}")
    print(f"  UNFM(未熟悉度)  : {args.unfm:.2f}")
    print("-" * 60)
    print(f"  ESLOC (等效新代码): {esloc:,.1f}")
    print(f"  估计工作量      : {effort:.2f} 人月")
    print(f"  估计工期        : {schedule:.2f} 月")
    print(f"  平均团队规模    : {effort / schedule:.2f} 人" if schedule > 0 else "  平均团队规模    : N/A")
    print("-" * 60)
    print("  复用 ROI 分析")
    print(f"    从零开发工作量: {nominal_effort:.2f} 人月")
    print(f"    复用节省工作量: {roi_info['cost_saving']:.2f} 人月")
    print(f"    理论 ROI      : {roi_info['roi_nominal_percent']:.1f}%")
    if "actual_effort" in roi_info:
        print(f"    实际投入工作量: {roi_info['actual_effort']:.2f} 人月")
        print(f"    实际 ROI      : {roi_info['roi_actual_percent']:.1f}%")
    print("=" * 60)

    # 复用决策建议
    if args.aam >= 0.7:
        print("⚠️  警告: AAM ≥ 0.7，复用改编成本接近重新开发，建议评估战略价值而非仅看直接 ROI。")
    elif roi_info.get("roi_actual_percent", roi_info["roi_nominal_percent"]) < 0:
        print("⚠️  警告: ROI 为负，复用未产生正向收益，请审查 AAM/SU/UNFM 参数假设。")
    else:
        print("✅ 复用方案经济可行，建议执行。")


def main():
    parser = argparse.ArgumentParser(
        description="COCOMO II 2026 复用计算器 MVP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python cocomo-calculator.py --sloc 50000 --aam 0.3 --su 0.4 --unfm 1.0
  python cocomo-calculator.py --sloc 100000 --aam 0.2 --su 0.5 --unfm 0.85 --effort 120 --mode intermediate
        """,
    )
    parser.add_argument("--sloc", type=int, required=True, help="目标系统总源代码行数")
    parser.add_argument("--aam", type=float, required=True, help="改编调整因子 [0.0, 1.0]")
    parser.add_argument("--su", type=float, required=True, help="软件理解度 [0.0, 1.0]")
    parser.add_argument("--unfm", type=float, required=True, help="未熟悉度 [0.0, 1.0]")
    parser.add_argument("--effort", type=float, default=None, help="实际投入工作量（人月），用于 ROI 计算")
    parser.add_argument("--mode", type=str, choices=["basic", "intermediate"], default="basic", help="计算模式")

    args = parser.parse_args()

    try:
        # 1. 计算 ESLOC
        esloc = compute_esloc(args.sloc, args.aam, args.su, args.unfm)

        # 2. 计算复用模式工作量
        if args.mode == "intermediate":
            effort = compute_effort_intermediate(esloc, default_em_values())
        else:
            effort = compute_effort_basic(esloc)

        # 3. 计算工期
        schedule = compute_schedule(effort)

        # 4. 计算从零开发工作量（用于 ROI 对比）
        if args.mode == "intermediate":
            nominal_effort = compute_effort_intermediate(float(args.sloc), default_em_values())
        else:
            nominal_effort = compute_effort_basic(float(args.sloc))

        # 5. 计算 ROI
        roi_info = compute_roi(effort, nominal_effort, args.effort)

        # 6. 输出报告
        print_report(args, esloc, effort, schedule, roi_info, nominal_effort)

    except ValueError as e:
        print(f"[错误] 参数校验失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
