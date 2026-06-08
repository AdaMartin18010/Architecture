#!/usr/bin/env python3
"""
AI Native Reuse - Probabilistic Contract Calibration Tool

基于 Split Conformal Prediction 的置信度校准工具。
为 AI 功能复用提供可证明的边际覆盖保证：
    P(y ∈ C(x)) ≥ 1 − α

用法:
    python calibration-tool.py calibrate --data calibration.csv --alpha 0.05
    python calibration-tool.py predict --data calibration.csv --input new.csv --alpha 0.05
    python calibration-tool.py drift --baseline v1.csv --new v2.csv --alpha 0.05
    python calibration-tool.py report --data calibration.csv --alpha 0.05
"""

import argparse
import csv
import json
import math
import sys
from typing import Dict, List, Tuple

import numpy as np
from scipy import stats


def load_data(path: str) -> List[Dict]:
    """加载 CSV 数据并校验温度(0-2)与 Top-p(0-1)范围。"""
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            r = {
                "sample_id": row.get("sample_id", ""),
                "prediction_score": float(row["prediction_score"]),
                "true_label": int(row["true_label"]),
                "temperature": float(row.get("temperature", 1.0)),
                "top_p": float(row.get("top_p", 1.0)),
                "model_version": row.get("model_version", "unknown"),
            }
            if not (0 <= r["temperature"] <= 2):
                raise ValueError(f"sample {r['sample_id']}: temperature 必须在 [0,2]")
            if not (0 <= r["top_p"] <= 1):
                raise ValueError(f"sample {r['sample_id']}: top_p 必须在 [0,1]")
            rows.append(r)
    return rows


def nonconformity_score(prediction_score: float, true_label: int) -> float:
    """非一致性分数：正确样本为 1-p，错误样本为 p。"""
    return 1.0 - prediction_score if true_label == 1 else prediction_score


def calibrate(data: List[Dict], alpha: float) -> Tuple[float, float, List[float]]:
    """计算 conformal 阈值 q、经验覆盖率及非一致性分数列表。"""
    n = len(data)
    scores = [nonconformity_score(r["prediction_score"], r["true_label"]) for r in data]
    k = math.ceil((1 - alpha) * (n + 1))
    k = min(k, n)
    q = float(np.partition(np.array(scores), k - 1)[k - 1])
    empirical = sum(1 for s in scores if s <= q) / n
    return q, empirical, scores


def predict_set(prediction_score: float, q: float) -> Tuple[List[int], str]:
    """
    构建预测集合 C(x)。
    包含条件：class 1 (correct) 当 p >= 1-q；class 0 (incorrect) 当 p <= q。
    保证非空。
    """
    classes = []
    if prediction_score >= 1.0 - q:
        classes.append(1)
    if prediction_score <= q:
        classes.append(0)
    if not classes:
        classes.append(1 if (1.0 - prediction_score) <= prediction_score else 0)
    stmt = {tuple([1]): "接受", tuple([0]): "拒绝",
            tuple([0, 1]): "不确定", tuple([1, 0]): "不确定"}.get(tuple(classes), "未知")
    return classes, stmt


def boundary_statement(alpha: float, q: float, empirical: float) -> str:
    return (f"在 α={alpha:.3f} 水平下，预测集合覆盖率为 {1-alpha:.1%}；"
            f"经验校准覆盖率 {empirical:.1%}；conformal 阈值 q={q:.4f}")


def drift_detect(baseline: List[Dict], new: List[Dict], alpha: float) -> Dict:
    """使用 Kolmogorov-Smirnov 检验检测模型版本漂移。"""
    _, _, s1 = calibrate(baseline, alpha)
    _, _, s2 = calibrate(new, alpha)
    stat, pvalue = stats.ks_2samp(s1, s2)
    return {
        "ks_statistic": round(stat, 4),
        "p_value": round(pvalue, 6),
        "drift_detected": pvalue < 0.05,
        "alert": "漂移警报：非一致性分数分布发生显著变化，建议重新校准" if pvalue < 0.05 else "无显著漂移",
        "recalibrate": pvalue < 0.05,
    }


def cli_calibrate(args):
    data = load_data(args.data)
    q, emp, _ = calibrate(data, args.alpha)
    avg_size = float(np.mean([len(predict_set(r["prediction_score"], q)[0]) for r in data]))
    print(boundary_statement(args.alpha, q, emp))
    print(f"平均预测集合大小: {avg_size:.2f}")
    out = {"alpha": args.alpha, "q": q, "empirical_coverage": emp, "avg_set_size": avg_size}
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        print(f"结果已保存至 {args.output}")


def cli_predict(args):
    cal_data = load_data(args.data)
    q, emp, _ = calibrate(cal_data, args.alpha)
    new_data = load_data(args.input)
    print(boundary_statement(args.alpha, q, emp))
    for r in new_data:
        classes, stmt = predict_set(r["prediction_score"], q)
        print(f"[{r['sample_id']}] score={r['prediction_score']:.3f} "
              f"set={classes} (size={len(classes)}) | {stmt}")


def cli_drift(args):
    b = load_data(args.baseline)
    n = load_data(args.new)
    d = drift_detect(b, n, args.alpha)
    print(f"KS 统计量: {d['ks_statistic']}, p-value: {d['p_value']}")
    print(d["alert"])
    if d["recalibrate"]:
        print("建议：立即执行重新校准 (calibrate)")
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)


def cli_report(args):
    data = load_data(args.data)
    q, emp, scores = calibrate(data, args.alpha)
    temps = [r["temperature"] for r in data]
    top_ps = [r["top_p"] for r in data]
    avg_size = float(np.mean([len(predict_set(r["prediction_score"], q)[0]) for r in data]))
    report = {
        "contract_boundary": boundary_statement(args.alpha, q, emp),
        "calibration_size": len(data),
        "conformal_threshold_q": round(q, 4),
        "avg_prediction_set_size": round(avg_size, 2),
        "correct_rate": sum(r["true_label"] for r in data) / len(data),
        "avg_temperature": round(float(np.mean(temps)), 2),
        "avg_top_p": round(float(np.mean(top_ps)), 2),
        "model_versions": list(set(r["model_version"] for r in data)),
        "score_distribution": {
            "mean": round(float(np.mean(scores)), 4),
            "std": round(float(np.std(scores)), 4),
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="AI 功能复用概率契约校准工具")
    sub = parser.add_subparsers(dest="command", required=True)

    p_cal = sub.add_parser("calibrate", help="从数据文件校准阈值")
    p_cal.add_argument("--data", required=True, help="校准 CSV 路径")
    p_cal.add_argument("--alpha", type=float, default=0.05, help="目标错误率 α")
    p_cal.add_argument("--output", help="输出 JSON 路径")

    p_pred = sub.add_parser("predict", help="对新输入生成预测集合")
    p_pred.add_argument("--data", required=True, help="校准 CSV 路径")
    p_pred.add_argument("--input", required=True, help="待预测 CSV 路径")
    p_pred.add_argument("--alpha", type=float, default=0.05)
    p_pred.add_argument("--output", help="输出 JSON 路径")

    p_drift = sub.add_parser("drift", help="检测模型版本漂移")
    p_drift.add_argument("--baseline", required=True, help="基线模型 CSV")
    p_drift.add_argument("--new", required=True, help="新模型 CSV")
    p_drift.add_argument("--alpha", type=float, default=0.05)
    p_drift.add_argument("--output", help="输出 JSON 路径")

    p_rep = sub.add_parser("report", help="生成校准报告")
    p_rep.add_argument("--data", required=True, help="校准 CSV 路径")
    p_rep.add_argument("--alpha", type=float, default=0.05)
    p_rep.add_argument("--output", help="输出 JSON 路径")

    args = parser.parse_args()
    if not (0 < args.alpha < 1):
        print("错误: alpha 必须在 (0,1) 区间", file=sys.stderr)
        return 1
    return {"calibrate": cli_calibrate, "predict": cli_predict,
            "drift": cli_drift, "report": cli_report}[args.command](args) or 0


if __name__ == "__main__":
    sys.exit(main())
