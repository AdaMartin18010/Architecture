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
    python calibration-tool.py calibrate-temperature --data calibration.csv
    python calibration-tool.py calibrate-platt --data calibration.csv
    python calibration-tool.py calibrate-isotonic --data calibration.csv
    python calibration-tool.py --test
"""

import argparse
import csv
import io
import json
import math
import sys
import tempfile
from typing import Dict, List, Optional, Tuple

import numpy as np
from scipy import optimize, stats


# --------------------------------------------------------------------------- #
# 数据加载与校验
# --------------------------------------------------------------------------- #

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
            if not (0 <= r["prediction_score"] <= 1):
                raise ValueError(f"sample {r['sample_id']}: prediction_score 必须在 [0,1]")
            rows.append(r)
    return rows


def dump_data(path: str, rows: List[Dict]) -> None:
    """将数据行写入 CSV，仅保留核心字段。"""
    fields = ["sample_id", "prediction_score", "true_label", "temperature", "top_p", "model_version"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r[k] for k in fields})


# --------------------------------------------------------------------------- #
# Conformal Prediction 核心
# --------------------------------------------------------------------------- #

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


# --------------------------------------------------------------------------- #
# 校准指标
# --------------------------------------------------------------------------- #

def _clip(probs: np.ndarray, eps: float = 1e-15) -> np.ndarray:
    return np.clip(probs, eps, 1 - eps)


def expected_calibration_error(probs: np.ndarray, labels: np.ndarray, n_bins: int = 10) -> float:
    """等宽分桶计算 ECE。"""
    if len(probs) == 0:
        return 0.0
    probs = _clip(probs)
    labels = np.asarray(labels, dtype=float)
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0
    total = len(probs)
    for i in range(n_bins):
        low, high = bin_edges[i], bin_edges[i + 1]
        if i == n_bins - 1:
            mask = (probs >= low) & (probs <= high)
        else:
            mask = (probs >= low) & (probs < high)
        if not np.any(mask):
            continue
        bin_size = int(np.sum(mask))
        avg_conf = float(np.mean(probs[mask]))
        avg_acc = float(np.mean(labels[mask]))
        ece += (bin_size / total) * abs(avg_conf - avg_acc)
    return float(ece)


def brier_score(probs: np.ndarray, labels: np.ndarray) -> float:
    """计算 Brier Score。"""
    if len(probs) == 0:
        return 0.0
    probs = _clip(probs)
    labels = np.asarray(labels, dtype=float)
    return float(np.mean((probs - labels) ** 2))


def brier_decomposition(probs: np.ndarray, labels: np.ndarray, n_bins: int = 10) -> Dict:
    """
    Brier 三分解：Reliability - Resolution + Uncertainty。
     Murphy, A. H. (1973). "A New Vector Partition of the Probability Score".
    """
    if len(probs) == 0:
        return {"reliability": 0.0, "resolution": 0.0, "uncertainty": 0.0}
    probs = _clip(probs)
    labels = np.asarray(labels, dtype=float)
    n = len(labels)
    overall_mean = float(np.mean(labels))

    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    reliability = 0.0
    resolution = 0.0
    for i in range(n_bins):
        low, high = bin_edges[i], bin_edges[i + 1]
        if i == n_bins - 1:
            mask = (probs >= low) & (probs <= high)
        else:
            mask = (probs >= low) & (probs < high)
        if not np.any(mask):
            continue
        n_b = int(np.sum(mask))
        avg_conf = float(np.mean(probs[mask]))
        avg_acc = float(np.mean(labels[mask]))
        reliability += (n_b / n) * (avg_conf - avg_acc) ** 2
        resolution += (n_b / n) * (avg_acc - overall_mean) ** 2
    uncertainty = overall_mean * (1 - overall_mean)
    return {
        "reliability": round(reliability, 6),
        "resolution": round(resolution, 6),
        "uncertainty": round(uncertainty, 6),
    }


def reliability_diagram(probs: np.ndarray, labels: np.ndarray, n_bins: int = 10) -> List[Dict]:
    """生成 reliability diagram 数据：每个 bin 的区间、样本数、平均预测分数、实际准确率。"""
    probs = _clip(probs)
    labels = np.asarray(labels, dtype=float)
    bin_edges = np.linspace(0.0, 1.0, n_bins + 1)
    result = []
    for i in range(n_bins):
        low, high = bin_edges[i], bin_edges[i + 1]
        label = f"{low:.2f}-{high:.2f}"
        if i == n_bins - 1:
            mask = (probs >= low) & (probs <= high)
        else:
            mask = (probs >= low) & (probs < high)
        count = int(np.sum(mask))
        if count == 0:
            result.append({
                "bin": label,
                "bin_start": round(float(low), 4),
                "bin_end": round(float(high), 4),
                "count": 0,
                "avg_prediction": None,
                "actual_accuracy": None,
                "gap": None,
            })
            continue
        avg_pred = float(np.mean(probs[mask]))
        actual_acc = float(np.mean(labels[mask]))
        result.append({
            "bin": label,
            "bin_start": round(float(low), 4),
            "bin_end": round(float(high), 4),
            "count": count,
            "avg_prediction": round(avg_pred, 4),
            "actual_accuracy": round(actual_acc, 4),
            "gap": round(abs(avg_pred - actual_acc), 4),
        })
    return result


# --------------------------------------------------------------------------- #
# 温度缩放 / Platt Scaling / Isotonic Regression
# --------------------------------------------------------------------------- #

def _logit(p: np.ndarray, eps: float = 1e-15) -> np.ndarray:
    p = _clip(p, eps)
    return np.log(p / (1 - p))


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


def _temperature_probs(logits: np.ndarray, temperature: float) -> np.ndarray:
    return _sigmoid(logits / max(temperature, 1e-6))


def calibrate_temperature(data: List[Dict], metric: str = "ece", n_bins: int = 10) -> Dict:
    """温度缩放：寻找最优温度 T 使得 ECE 或 Brier 最小。"""
    probs = np.array([r["prediction_score"] for r in data])
    labels = np.array([r["true_label"] for r in data], dtype=float)
    logits = _logit(probs)

    def objective(t: float) -> float:
        calibrated = _temperature_probs(logits, t)
        if metric == "ece":
            return expected_calibration_error(calibrated, labels, n_bins)
        if metric == "brier":
            return brier_score(calibrated, labels)
        # 默认使用负对数似然
        calibrated = _clip(calibrated)
        return -float(np.mean(labels * np.log(calibrated) + (1 - labels) * np.log(1 - calibrated)))

    result = optimize.minimize_scalar(objective, bounds=(0.1, 10.0), method="bounded")
    optimal_t = float(result.x)
    calibrated = _temperature_probs(logits, optimal_t)
    return {
        "method": "temperature_scaling",
        "optimal_temperature": round(optimal_t, 4),
        "metric_optimized": metric,
        "ece": round(expected_calibration_error(calibrated, labels, n_bins), 4),
        "brier_score": round(brier_score(calibrated, labels), 4),
        "brier_decomposition": brier_decomposition(calibrated, labels, n_bins),
        "reliability_diagram": reliability_diagram(calibrated, labels, n_bins),
    }


def calibrate_platt(data: List[Dict], n_bins: int = 10) -> Dict:
    """Platt Scaling：用逻辑回归校准置信度分数。"""
    probs = np.array([r["prediction_score"] for r in data])
    labels = np.array([r["true_label"] for r in data], dtype=float)
    logits = _logit(probs)

    def nll(params: np.ndarray) -> float:
        a, b = params
        calibrated = _sigmoid(a * logits + b)
        calibrated = _clip(calibrated)
        return -float(np.mean(labels * np.log(calibrated) + (1 - labels) * np.log(1 - calibrated)))

    result = optimize.minimize(nll, x0=np.array([1.0, 0.0]), method="L-BFGS-B")
    a, b = result.x
    calibrated = _sigmoid(a * logits + b)
    return {
        "method": "platt_scaling",
        "params": {"a": round(float(a), 6), "b": round(float(b), 6)},
        "ece": round(expected_calibration_error(calibrated, labels, n_bins), 4),
        "brier_score": round(brier_score(calibrated, labels), 4),
        "brier_decomposition": brier_decomposition(calibrated, labels, n_bins),
        "reliability_diagram": reliability_diagram(calibrated, labels, n_bins),
    }


def calibrate_isotonic(data: List[Dict], n_bins: int = 10) -> Dict:
    """Isotonic Regression：使用 PAVA 算法得到单调非减校准映射。"""
    probs = np.array([r["prediction_score"] for r in data])
    labels = np.array([r["true_label"] for r in data], dtype=float)
    order = np.argsort(probs)
    x_sorted = probs[order]
    y_sorted = labels[order]

    # PAVA
    values = list(y_sorted.astype(float))
    blocks = [[v] for v in values]
    i = 0
    while i < len(blocks) - 1:
        if _block_mean(blocks[i]) > _block_mean(blocks[i + 1]):
            blocks[i] = blocks[i] + blocks[i + 1]
            del blocks[i + 1]
            i = max(0, i - 1)
        else:
            i += 1

    # 构建分段常数映射：每个原始值映射到所在块的均值
    calibrated = np.empty_like(probs)
    pos = 0
    mapping = []
    for block in blocks:
        mean_val = _block_mean(block)
        n_block = len(block)
        for _ in range(n_block):
            calibrated[order[pos]] = mean_val
            pos += 1
        mapping.append({
            "block_start": round(float(x_sorted[pos - n_block]), 4),
            "block_end": round(float(x_sorted[pos - 1]), 4),
            "calibrated_value": round(float(mean_val), 4),
            "count": n_block,
        })

    return {
        "method": "isotonic_regression",
        "ece": round(expected_calibration_error(calibrated, labels, n_bins), 4),
        "brier_score": round(brier_score(calibrated, labels), 4),
        "brier_decomposition": brier_decomposition(calibrated, labels, n_bins),
        "reliability_diagram": reliability_diagram(calibrated, labels, n_bins),
        "mapping_sample": mapping[:20],  # 避免输出过大
    }


def _block_mean(block: List[float]) -> float:
    return sum(block) / len(block)


# --------------------------------------------------------------------------- #
# 分层校准
# --------------------------------------------------------------------------- #

def stratify_data(data: List[Dict], keys: List[str]) -> Dict[Tuple, List[Dict]]:
    """按指定键对数据进行分层。"""
    groups: Dict[Tuple, List[Dict]] = {}
    for r in data:
        key = tuple(str(r.get(k, "unknown")) for k in keys)
        groups.setdefault(key, []).append(r)
    return groups


def stratified_calibration(
    data: List[Dict],
    stratify_by: List[str],
    method: str = "temperature",
    n_bins: int = 10,
    metric: str = "ece",
) -> Dict:
    """对数据按指定维度分层后执行校准。"""
    groups = stratify_data(data, stratify_by)
    results = []
    for key, group in sorted(groups.items()):
        if len(group) < 5:
            continue
        key_dict = {k: v for k, v in zip(stratify_by, key)}
        if method == "temperature":
            cal = calibrate_temperature(group, metric=metric, n_bins=n_bins)
        elif method == "platt":
            cal = calibrate_platt(group, n_bins=n_bins)
        elif method == "isotonic":
            cal = calibrate_isotonic(group, n_bins=n_bins)
        else:
            raise ValueError(f"不支持的校准方法: {method}")
        cal["stratum"] = key_dict
        cal["sample_size"] = len(group)
        results.append(cal)
    return {"stratify_by": stratify_by, "strata": results}


# --------------------------------------------------------------------------- #
# CLI 命令实现
# --------------------------------------------------------------------------- #

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
    predictions = []
    for r in new_data:
        classes, stmt = predict_set(r["prediction_score"], q)
        print(f"[{r['sample_id']}] score={r['prediction_score']:.3f} "
              f"set={classes} (size={len(classes)}) | {stmt}")
        predictions.append({
            "sample_id": r["sample_id"],
            "prediction_score": r["prediction_score"],
            "set": classes,
            "statement": stmt,
        })
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({"boundary": boundary_statement(args.alpha, q, emp),
                       "predictions": predictions}, f, ensure_ascii=False, indent=2)


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
    probs = np.array([r["prediction_score"] for r in data])
    labels = np.array([r["true_label"] for r in data], dtype=float)
    avg_size = float(np.mean([len(predict_set(r["prediction_score"], q)[0]) for r in data]))

    sets = [predict_set(r["prediction_score"], q)[0] for r in data]
    accept_rate = sum(1 for s in sets if s == [1]) / len(sets)
    reject_rate = sum(1 for s in sets if s == [0]) / len(sets)
    uncertain_rate = sum(1 for s in sets if set(s) == {0, 1}) / len(sets)

    report = {
        "contract_boundary": boundary_statement(args.alpha, q, emp),
        "calibration_size": len(data),
        "conformal_threshold_q": round(q, 4),
        "avg_prediction_set_size": round(avg_size, 2),
        "correct_rate": round(float(np.mean(labels)), 4),
        "avg_temperature": round(float(np.mean(temps)), 2),
        "avg_top_p": round(float(np.mean(top_ps)), 2),
        "model_versions": list(set(r["model_version"] for r in data)),
        "score_distribution": {
            "mean": round(float(np.mean(scores)), 4),
            "std": round(float(np.std(scores)), 4),
        },
        "ece": round(expected_calibration_error(probs, labels, args.n_bins), 4),
        "brier_score": round(brier_score(probs, labels), 4),
        "brier_decomposition": brier_decomposition(probs, labels, args.n_bins),
        "reliability_diagram": reliability_diagram(probs, labels, args.n_bins),
        "set_distribution": {
            "accept_rate": round(accept_rate, 4),
            "reject_rate": round(reject_rate, 4),
            "uncertain_rate": round(uncertain_rate, 4),
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)


def _print_calibration_result(result: Dict) -> None:
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cli_calibrate_temperature(args):
    data = load_data(args.data)
    result = calibrate_temperature(data, metric=args.metric, n_bins=args.n_bins)
    print(f"温度缩放校准完成，最优 temperature={result['optimal_temperature']}")
    print(f"ECE={result['ece']}, Brier={result['brier_score']}")
    if args.stratify_by:
        strat = stratified_calibration(data, args.stratify_by, method="temperature",
                                       n_bins=args.n_bins, metric=args.metric)
        result["stratified"] = strat
    _print_calibration_result(result)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)


def cli_calibrate_platt(args):
    data = load_data(args.data)
    result = calibrate_platt(data, n_bins=args.n_bins)
    print(f"Platt Scaling 校准完成，参数 a={result['params']['a']}, b={result['params']['b']}")
    print(f"ECE={result['ece']}, Brier={result['brier_score']}")
    if args.stratify_by:
        strat = stratified_calibration(data, args.stratify_by, method="platt", n_bins=args.n_bins)
        result["stratified"] = strat
    _print_calibration_result(result)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)


def cli_calibrate_isotonic(args):
    data = load_data(args.data)
    result = calibrate_isotonic(data, n_bins=args.n_bins)
    print(f"Isotonic Regression 校准完成，ECE={result['ece']}, Brier={result['brier_score']}")
    if args.stratify_by:
        strat = stratified_calibration(data, args.stratify_by, method="isotonic", n_bins=args.n_bins)
        result["stratified"] = strat
    _print_calibration_result(result)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------- #
# 内置测试
# --------------------------------------------------------------------------- #

def _make_test_data(seed: int = 42, n: int = 120) -> List[Dict]:
    rng = np.random.default_rng(seed)
    rows = []
    for i in range(n):
        # 构造一个稍微过度自信的数据集
        true_label = int(rng.random() > 0.4)
        if true_label == 1:
            score = min(0.99, rng.beta(5, 2))
        else:
            score = max(0.01, rng.beta(2, 5))
        rows.append({
            "sample_id": f"test-{i:03d}",
            "prediction_score": round(float(score), 3),
            "true_label": true_label,
            "temperature": round(float(rng.choice([0.1, 0.5, 1.0])), 1),
            "top_p": 0.9,
            "model_version": "llm-test-v1",
        })
    return rows


def run_tests() -> int:
    """运行内置测试，验证核心功能。"""
    print("运行内置测试...")
    data = _make_test_data()

    # 1. 基本校准
    q, emp, scores = calibrate(data, 0.10)
    assert 0 <= q <= 1, "q 应在 [0,1] 区间"
    assert 0 <= emp <= 1, "经验覆盖率应在 [0,1] 区间"
    assert len(scores) == len(data), "非一致性分数数量应等于样本数"

    # 2. 预测集合
    for r in data:
        classes, stmt = predict_set(r["prediction_score"], q)
        assert len(classes) >= 1, "预测集合非空"
        assert stmt in ("接受", "拒绝", "不确定", "未知"), f"未知状态 {stmt}"

    # 3. 漂移检测
    baseline = data[:60]
    new = data[60:]
    drift = drift_detect(baseline, new, 0.10)
    assert "ks_statistic" in drift and "p_value" in drift, "漂移检测应返回 KS 统计量与 p-value"

    # 4. 指标计算
    probs = np.array([r["prediction_score"] for r in data])
    labels = np.array([r["true_label"] for r in data], dtype=float)
    ece = expected_calibration_error(probs, labels)
    brier = brier_score(probs, labels)
    decomp = brier_decomposition(probs, labels)
    rel = reliability_diagram(probs, labels)
    assert 0 <= ece <= 1, f"ECE 越界: {ece}"
    assert 0 <= brier <= 1, f"Brier 越界: {brier}"
    assert len(rel) == 10, "默认 10 个 bin"
    assert all(k in decomp for k in ("reliability", "resolution", "uncertainty"))

    # 5. 温度缩放
    temp_result = calibrate_temperature(data, metric="ece")
    assert "optimal_temperature" in temp_result, "温度缩放应返回最优温度"
    assert 0.1 <= temp_result["optimal_temperature"] <= 10.0, "最优温度应在搜索区间内"
    assert "reliability_diagram" in temp_result, "温度缩放应返回 reliability diagram 数据"

    # 6. Platt 缩放
    platt_result = calibrate_platt(data)
    assert "params" in platt_result and "a" in platt_result["params"], "Platt 应返回参数"
    assert "reliability_diagram" in platt_result, "Platt 应返回 reliability diagram 数据"

    # 7. Isotonic 回归
    iso_result = calibrate_isotonic(data)
    assert "mapping_sample" in iso_result, "Isotonic 应返回映射样本"
    assert "reliability_diagram" in iso_result, "Isotonic 应返回 reliability diagram 数据"

    # 8. 分层校准
    strat = stratified_calibration(data, ["model_version", "temperature"], method="temperature")
    assert "strata" in strat and len(strat["strata"]) > 0, "分层校准应产生非空结果"

    # 9. CSV 写入/读取 round-trip
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
        path = f.name
    try:
        dump_data(path, data)
        loaded = load_data(path)
        assert len(loaded) == len(data), "CSV round-trip 后样本数应一致"
    finally:
        import os
        os.remove(path)

    # 10. CLI 端到端（调用现有命令函数）
    class FakeArgs:
        data = None
        alpha = 0.10
        output = None
        input = None
        baseline = None
        new = None
        n_bins = 10
        metric = "ece"
        stratify_by = None

    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as f:
        cal_path = f.name
    dump_data(cal_path, data)
    try:
        args = FakeArgs()
        args.data = cal_path
        cli_report(args)  # 输出到 stdout，只要无异常即通过
    finally:
        import os
        os.remove(cal_path)

    print("全部内置测试通过。")
    return 0


# --------------------------------------------------------------------------- #
# 参数解析与主入口
# --------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser(description="AI 功能复用概率契约校准工具")
    parser.add_argument("--test", action="store_true", help="运行内置测试")
    sub = parser.add_subparsers(dest="command")

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
    p_rep.add_argument("--n-bins", type=int, default=10, help="reliability diagram 分桶数")
    p_rep.add_argument("--output", help="输出 JSON 路径")

    p_temp = sub.add_parser("calibrate-temperature", help="温度缩放校准")
    p_temp.add_argument("--data", required=True, help="校准 CSV 路径")
    p_temp.add_argument("--alpha", type=float, default=0.05, help="目标错误率 α（用于一致性校验）")
    p_temp.add_argument("--metric", default="ece", choices=["ece", "brier", "nll"],
                        help="优化目标：ece / brier / nll")
    p_temp.add_argument("--n-bins", type=int, default=10, help="ECE 分桶数")
    p_temp.add_argument("--stratify-by", help="分层字段，逗号分隔，如 model_version,temperature")
    p_temp.add_argument("--output", help="输出 JSON 路径")

    p_platt = sub.add_parser("calibrate-platt", help="Platt Scaling 校准")
    p_platt.add_argument("--data", required=True, help="校准 CSV 路径")
    p_platt.add_argument("--alpha", type=float, default=0.05, help="目标错误率 α（用于一致性校验）")
    p_platt.add_argument("--n-bins", type=int, default=10, help="ECE 分桶数")
    p_platt.add_argument("--stratify-by", help="分层字段，逗号分隔")
    p_platt.add_argument("--output", help="输出 JSON 路径")

    p_iso = sub.add_parser("calibrate-isotonic", help="Isotonic Regression 校准")
    p_iso.add_argument("--data", required=True, help="校准 CSV 路径")
    p_iso.add_argument("--alpha", type=float, default=0.05, help="目标错误率 α（用于一致性校验）")
    p_iso.add_argument("--n-bins", type=int, default=10, help="ECE 分桶数")
    p_iso.add_argument("--stratify-by", help="分层字段，逗号分隔")
    p_iso.add_argument("--output", help="输出 JSON 路径")

    args = parser.parse_args()

    if args.test:
        return run_tests()

    if not args.command:
        parser.print_help()
        return 1

    if not (0 < args.alpha < 1):
        print("错误: alpha 必须在 (0,1) 区间", file=sys.stderr)
        return 1

    if hasattr(args, "stratify_by") and args.stratify_by:
        args.stratify_by = [s.strip() for s in args.stratify_by.split(",")]

    commands = {
        "calibrate": cli_calibrate,
        "predict": cli_predict,
        "drift": cli_drift,
        "report": cli_report,
        "calibrate-temperature": cli_calibrate_temperature,
        "calibrate-platt": cli_calibrate_platt,
        "calibrate-isotonic": cli_calibrate_isotonic,
    }
    return commands[args.command](args) or 0


if __name__ == "__main__":
    sys.exit(main())
