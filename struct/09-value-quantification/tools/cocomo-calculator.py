#!/usr/bin/env python3
"""
COCOMO II 2026 复用成本计算器

支持官方 COCOMO II Reuse 模型（ESLOC / AAM / AAF / AT / DM / CM / IM / SU / UNFM）
以及 2026 校准参数，同时保持原有简化 CLI 的向后兼容。

核心公式
--------
官方复用模型（COCOMO II Reuse Model）::

    ESLOC = ASLOC × (1 - AT/100) × AAM

    AAM = [AA + AAF × (1 + 0.02 × SU × UNFM)] / 100   (AAF ≤ 50)
    AAM = [AA + AAF + (SU × UNFM)] / 100              (AAF > 50)

    AAF = 0.4 × DM + 0.3 × CM + 0.3 × IM

Post-Architecture / 2026 工作量模型::

    PM = A × (Size)^E × EM
    E  = B + 0.01 × Σ(SF)
    TDEV = C × PM^D × SCED

其中 Size 为 KSLOC（千等效源代码行）。

使用示例
--------
向后兼容的简化模式::

    python cocomo-calculator.py --sloc 50000 --aam 0.3 --su 0.4 --unfm 1.0 --effort 120

官方复用模型（推荐）::

    python cocomo-calculator.py \
        --sloc 10000 --asloc 3000 --aa 10 \
        --dm 30 --cm 20 --im 50 --su 20 --unfm 0.5 \
        --a 2.20 --sf 4,3,3,3,3 --em 0.815 --output result.json

敏感性分析::

    python cocomo-calculator.py --sloc 10000 --asloc 3000 --dm 30 --cm 20 --im 50 \
        --su 20 --unfm 0.5 --sensitivity

批量场景对比（YAML 配置）::

    python cocomo-calculator.py --config scenario.yaml --output report.md

单元测试::

    python cocomo-calculator.py --test

参考
----
- COCOMO II Model Definition Manual (Boehm et al., USC)
- `struct/09-value-quantification/01-cocomo-ii-reuse/cocomo-ii-reuse-model-deep-dive.md`
- `struct/09-value-quantification/01-cocomo-ii-reuse/cocomo-2026-calibration.md`
- ISO/IEC 26550:2015 产品线工程与复用
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import math
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# 默认常量
# ---------------------------------------------------------------------------

DEFAULT_BASIC_A: float = 2.94          # 传统 COCOMO II.2000 A 常数（简化模式）
DEFAULT_BASIC_E: float = 1.099         # 简化模式固定指数
DEFAULT_OFFICIAL_A: float = 2.20       # 2026 校准 A 常数（官方/中间模型）
DEFAULT_B: float = 0.91                # 规模指数基数
DEFAULT_SF: list[float] = [4.0, 3.0, 3.0, 3.0, 3.0]  # 默认 5 个规模因子评分
DEFAULT_SCHEDULE: tuple[float, float] = (3.67, 0.3179)  # (C, D)
DEFAULT_SCED: float = 1.0              # 进度约束乘数


# ---------------------------------------------------------------------------
# 复用模型计算
# ---------------------------------------------------------------------------

def compute_esloc_legacy(sloc: int, aam: float, su: float, unfm: float) -> float:
    """
    简化模式下的等效新源代码行数（向后兼容）。

    公式: ESLOC = SLOC × AAM × (SU + UNFM) / 2
    """
    if sloc < 0:
        raise ValueError("SLOC 必须为非负数")
    if not (0.0 <= aam <= 1.0):
        raise ValueError("AAM 必须在 [0.0, 1.0] 范围内")
    if not (0.0 <= su <= 1.0):
        raise ValueError("SU 必须在 [0.0, 1.0] 范围内（简化模式）")
    if not (0.0 <= unfm <= 1.0):
        raise ValueError("UNFM 必须在 [0.0, 1.0] 范围内")

    raf = (su + unfm) / 2.0
    return sloc * aam * raf


def compute_aaf(dm: float, cm: float, im: float) -> float:
    """
    改编调整因子 AAF（百分比形式）。

    公式: AAF = 0.4 × DM + 0.3 × CM + 0.3 × IM
    """
    return 0.4 * dm + 0.3 * cm + 0.3 * im


def compute_aam(aa: float, aaf: float, su: float, unfm: float) -> float:
    """
    适配调整乘数 AAM（小数形式，0-1）。

    公式:
        AAM = [AA + AAF × (1 + 0.02 × SU × UNFM)] / 100   (AAF ≤ 50)
        AAM = [AA + AAF + (SU × UNFM)] / 100              (AAF > 50)

    参数均为百分比，仅 UNFM 为 0-1 的小数。
    """
    if aaf <= 50.0:
        return (aa + aaf * (1.0 + 0.02 * su * unfm)) / 100.0
    return (aa + aaf + (su * unfm)) / 100.0


def compute_esloc_official(asloc: float, at: float, aam: float) -> float:
    """
    官方 COCOMO II Reuse 模型的 ESLOC。

    公式: ESLOC = ASLOC × (1 - AT/100) × AAM
    """
    return asloc * (1.0 - at / 100.0) * aam


def compute_effort(size_ksloc: float, a: float, e: float, em: float) -> float:
    """COCOMO II 工作量公式: PM = A × Size^E × EM。"""
    if size_ksloc < 0:
        raise ValueError("Size 必须为非负数")
    return a * math.pow(size_ksloc, e) * em


def compute_schedule(pm: float, c: float, d: float, sced: float = 1.0) -> float:
    """
    工期估算: TDEV = C × PM^D × SCED。

    当 pm <= 0 时返回 0，避免无意义的复数/错误结果。
    """
    if pm <= 0:
        return 0.0
    return c * math.pow(pm, d) * sced


def compute_roi(effort_reuse: float, effort_nominal: float, actual_effort: float | None = None) -> dict:
    """
    复用投资回报率。

    公式:
        成本节约 = effort_nominal - effort_reuse
        理论 ROI = 成本节约 / effort_reuse × 100%
        实际 ROI = (effort_nominal - actual_effort) / actual_effort × 100%
    """
    cost_saving = effort_nominal - effort_reuse
    roi_nominal = (cost_saving / effort_reuse * 100.0) if effort_reuse > 0 else 0.0

    result: dict[str, Any] = {
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


# ---------------------------------------------------------------------------
# 参数解析辅助函数
# ---------------------------------------------------------------------------

def parse_sf(value: str | list[float] | None) -> list[float]:
    """
    解析 5 个规模因子评分。

    接受逗号分隔的字符串或列表，返回 5 个 float。
    若未提供，返回默认 [4,3,3,3,3]（对应 E = 1.07）。
    """
    if value is None:
        return list(DEFAULT_SF)
    if isinstance(value, (list, tuple)):
        values = [float(v) for v in value]
    else:
        values = [float(v.strip()) for v in str(value).split(",") if v.strip() != ""]
    if len(values) != 5:
        raise ValueError("规模因子 --sf 必须提供 5 个数值（PREC, FLEX, RESL, TEAM, PMAT）")
    return values


def parse_em(value: str | float | list[float] | None) -> float:
    """
    解析工作量乘数。

    - 单一 float 直接返回。
    - 逗号分隔的多个乘数返回其乘积（可传入 17 个中间 COCOMO 成本驱动因子）。
    - 未提供返回 1.0。
    """
    if value is None:
        return 1.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, (list, tuple)):
        return math.prod(float(v) for v in value)
    parts = [float(v.strip()) for v in str(value).split(",") if v.strip() != ""]
    return math.prod(parts) if parts else 1.0


def parse_schedule(value: str | tuple[float, float] | None) -> tuple[float, float]:
    """
    解析 --schedule "C,D" 工期参数，返回 (C, D)。
    """
    if value is None:
        return DEFAULT_SCHEDULE
    if isinstance(value, (list, tuple)):
        return (float(value[0]), float(value[1]))
    parts = [float(v.strip()) for v in str(value).split(",") if v.strip() != ""]
    if len(parts) != 2:
        raise ValueError("--schedule 必须按 'C,D' 格式提供两个数值")
    return (parts[0], parts[1])


def _to_float_or_none(value: Any) -> float | None:
    return None if value is None else float(value)


# ---------------------------------------------------------------------------
# 场景参数构建
# ---------------------------------------------------------------------------

def build_params(raw: dict[str, Any]) -> dict[str, Any]:
    """
    将原始输入（CLI args 或配置项）转换为规范化的计算参数字典。

    自动识别官方复用模型与简化模式：
    - 当提供 --asloc / --aaf / --dm / --cm / --im / --aa / --at / --new-sloc 之一，
      或 mode == 'official' 时，使用官方 COCOMO II Reuse 公式。
    - 否则使用原有简化模式以保持向后兼容。
    """
    mode = str(raw.get("mode", "basic")).lower()
    official_keys = ["asloc", "aaf", "dm", "cm", "im", "aa", "at", "new_sloc"]
    is_official = (mode == "official") or any(raw.get(k) is not None for k in official_keys)

    params: dict[str, Any] = {
        "is_official": is_official,
        "mode": "official" if is_official else mode,
        "sloc": int(raw.get("sloc", 0)),
        "asloc": _to_float_or_none(raw.get("asloc")),
        "new_sloc": _to_float_or_none(raw.get("new_sloc")),
        "at": float(raw.get("at") if raw.get("at") is not None else 0.0),
        "aa": float(raw.get("aa") if raw.get("aa") is not None else 0.0),
        "aaf": _to_float_or_none(raw.get("aaf")),
        "aam": _to_float_or_none(raw.get("aam")) if not is_official else None,
        "dm": float(raw.get("dm") if raw.get("dm") is not None else 0.0),
        "cm": float(raw.get("cm") if raw.get("cm") is not None else 0.0),
        "im": float(raw.get("im") if raw.get("im") is not None else 0.0),
        "su": float(raw.get("su", 0.0)),
        "unfm": float(raw.get("unfm", 1.0)),
        "sf": parse_sf(raw.get("sf")),
        "em": parse_em(raw.get("em")),
        "a": _to_float_or_none(raw.get("a")),
        "b": float(raw.get("b", DEFAULT_B)),
        "schedule": parse_schedule(raw.get("schedule")),
        "sced": float(raw.get("sced", DEFAULT_SCED)),
        "actual_effort": _to_float_or_none(raw.get("effort")),
    }

    # 选择默认 A 常数
    if params["a"] is None:
        params["a"] = DEFAULT_OFFICIAL_A if is_official else DEFAULT_BASIC_A

    # 指数 E
    if is_official:
        # 官方复用模型使用 5 个规模因子计算 E
        params["e"] = params["b"] + 0.01 * sum(params["sf"])
    elif mode == "intermediate" and raw.get("sf") is not None:
        # 用户显式传入 SF 时使用中间模型公式
        params["e"] = params["b"] + 0.01 * sum(params["sf"])
    else:
        # 简化模式 / 未传入 SF 的 intermediate 模式保持原固定指数，确保向后兼容
        params["e"] = DEFAULT_BASIC_E

    # 校验
    if params["sloc"] < 0:
        raise ValueError("--sloc 必须为非负数")
    if is_official:
        if params["asloc"] is None:
            raise ValueError("官方复用模型必须提供 --asloc（需适配的源代码行数）")
        if not (0.0 <= params["at"] <= 100.0):
            raise ValueError("--at 必须在 [0, 100] 范围内（百分比）")
        if not (0.0 <= params["aa"] <= 100.0):
            raise ValueError("--aa 必须在 [0, 100] 范围内（百分比）")
        if not (0.0 <= params["dm"] <= 100.0):
            raise ValueError("--dm 必须在 [0, 100] 范围内（百分比）")
        if not (0.0 <= params["cm"] <= 100.0):
            raise ValueError("--cm 必须在 [0, 100] 范围内（百分比）")
        if not (0.0 <= params["im"] <= 100.0):
            raise ValueError("--im 必须在 [0, 100] 范围内（百分比）")
        if not (0.0 <= params["su"] <= 100.0):
            raise ValueError("--su 在官方模型中为百分比，必须在 [0, 100] 范围内")
        if not (0.0 <= params["unfm"] <= 2.0):
            raise ValueError("--unfm 必须在 [0.0, 2.0] 范围内")
    else:
        if not (0.0 <= params["su"] <= 1.0):
            raise ValueError("--su 在简化模式中为小数，必须在 [0.0, 1.0] 范围内")
        if not (0.0 <= params["unfm"] <= 1.0):
            raise ValueError("--unfm 在简化模式中必须在 [0.0, 1.0] 范围内")

    return params


# ---------------------------------------------------------------------------
# 单场景计算
# ---------------------------------------------------------------------------

def run_scenario(params: dict[str, Any], scenario_name: str = "default") -> dict[str, Any]:
    """执行单个场景计算，返回包含全部输入/输出的结果字典。"""
    is_official = params["is_official"]

    if is_official:
        aaf = params["aaf"] if params["aaf"] is not None else compute_aaf(params["dm"], params["cm"], params["im"])
        aam = compute_aam(params["aa"], aaf, params["su"], params["unfm"])
        esloc = compute_esloc_official(params["asloc"], params["at"], aam)
        new_code = params["new_sloc"] if params["new_sloc"] is not None and params["new_sloc"] > 0 else max(params["sloc"] - params["asloc"], 0.0)
        total_size = new_code + esloc
    else:
        aaf = None
        aam = params.get("aam") if params.get("aam") is not None else 0.0
        esloc = compute_esloc_legacy(params["sloc"], aam, params["su"], params["unfm"])
        total_size = esloc
        params["aam"] = aam

    size_ksloc = total_size / 1000.0
    effort = compute_effort(size_ksloc, params["a"], params["e"], params["em"])
    c, d = params["schedule"]
    schedule = compute_schedule(effort, c, d, params["sced"])

    # 以“全部从零开发”为基准计算 ROI
    nominal_effort = compute_effort(params["sloc"] / 1000.0, params["a"], params["e"], params["em"])
    roi = compute_roi(effort, nominal_effort, params["actual_effort"])

    result: dict[str, Any] = {
        "scenario": scenario_name,
        "inputs": {
            "mode": params["mode"],
            "sloc": params["sloc"],
            "asloc": params["asloc"],
            "new_sloc": params["new_sloc"],
            "at": params["at"],
            "aa": params["aa"],
            "aaf": aaf,
            "aam": aam,
            "dm": params["dm"],
            "cm": params["cm"],
            "im": params["im"],
            "su": params["su"],
            "unfm": params["unfm"],
            "sf": params["sf"],
            "em": params["em"],
            "a": params["a"],
            "b": params["b"],
            "e": params["e"],
            "schedule_c": c,
            "schedule_d": d,
            "sced": params["sced"],
            "actual_effort": params["actual_effort"],
        },
        "esloc": round(esloc, 2),
        "total_size": round(total_size, 2),
        "size_ksloc": round(size_ksloc, 4),
        "effort_pm": round(effort, 2),
        "schedule_months": round(schedule, 2),
        "team_size": round(effort / schedule, 2) if schedule > 0 else None,
        "roi": {k: round(v, 2) if isinstance(v, float) else v for k, v in roi.items()},
    }

    return result


# ---------------------------------------------------------------------------
# 敏感性分析
# ---------------------------------------------------------------------------

def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def sensitivity_analysis(params: dict[str, Any]) -> list[dict[str, Any]]:
    """
    对关键参数进行 ±20% 扰动，输出 tornado 表数据。

    官方模型分析: asloc, dm, cm, im, su, unfm, em, a
    简化模式分析: sloc, aam, su, unfm, em, a
    """
    is_official = params["is_official"]

    if is_official:
        param_specs = {
            "asloc": (0.0, float("inf")),
            "dm": (0.0, 100.0),
            "cm": (0.0, 100.0),
            "im": (0.0, 100.0),
            "su": (0.0, 100.0),
            "unfm": (0.0, 2.0),
            "em": (0.0, float("inf")),
            "a": (0.0, float("inf")),
        }
    else:
        param_specs = {
            "sloc": (0.0, float("inf")),
            "aam": (0.0, 1.0),
            "su": (0.0, 1.0),
            "unfm": (0.0, 1.0),
            "em": (0.0, float("inf")),
            "a": (0.0, float("inf")),
        }

    baseline_result = run_scenario(params)
    baseline = baseline_result["effort_pm"]

    rows: list[dict[str, Any]] = []
    for name, (lo, hi) in param_specs.items():
        if name not in params or params[name] is None:
            continue
        base_value = float(params[name])

        for direction, factor in (("+20%", 1.2), ("-20%", 0.8)):
            new_value = _clamp(base_value * factor, lo, hi)
            variant = dict(params)
            variant[name] = new_value
            variant_effort = run_scenario(variant)["effort_pm"]
            rows.append({
                "parameter": name,
                "base_value": base_value,
                "direction": direction,
                "variant_value": new_value,
                "effort_pm": variant_effort,
                "delta_percent": round((variant_effort - baseline) / baseline * 100.0, 2) if baseline else 0.0,
            })

    # 按最大影响幅度汇总
    grouped: dict[str, dict[str, Any]] = {}
    for row in rows:
        name = row["parameter"]
        grouped.setdefault(name, {"base_value": row["base_value"], "efforts": []})
        grouped[name]["efforts"].append(row["effort_pm"])

    summary = []
    for name, data in grouped.items():
        efforts = data["efforts"]
        impact = max(efforts) - min(efforts)
        summary.append({
            "parameter": name,
            "base_value": data["base_value"],
            "effort_low": round(min(efforts), 2),
            "effort_high": round(max(efforts), 2),
            "impact": round(impact, 2),
            "impact_percent": round(impact / baseline * 100.0, 2) if baseline else 0.0,
        })

    summary.sort(key=lambda x: abs(x["impact"]), reverse=True)
    return summary


# ---------------------------------------------------------------------------
# 报告导出
# ---------------------------------------------------------------------------

def _flatten_result(result: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    flat: dict[str, Any] = {}
    for key, value in result.items():
        full_key = f"{prefix}{key}" if not prefix else f"{prefix}.{key}"
        if isinstance(value, dict):
            flat.update(_flatten_result(value, full_key))
        elif isinstance(value, list):
            flat[full_key] = json.dumps(value)
        else:
            flat[full_key] = value
    return flat


def export_json(results: list[dict[str, Any]], path: str) -> None:
    """导出为 JSON。"""
    payload = results if len(results) > 1 else results[0]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def export_csv(results: list[dict[str, Any]], path: str) -> None:
    """导出为 CSV。"""
    flat_results = [_flatten_result(r) for r in results]
    fieldnames = list(dict.fromkeys(k for fr in flat_results for k in fr.keys()))
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for fr in flat_results:
            writer.writerow(fr)


def export_md(results: list[dict[str, Any]], path: str) -> None:
    """导出为 Markdown 报告。"""
    lines: list[str] = []
    lines.append("# COCOMO II 2026 复用成本计算报告\n")

    if len(results) == 1:
        r = results[0]
        lines.append(f"## 场景: {r['scenario']}\n")
        lines.append("### 输入参数\n")
        lines.append("| 参数 | 值 |")
        lines.append("|------|-----|")
        for k, v in r["inputs"].items():
            lines.append(f"| {k} | {v} |")
        lines.append("")
        lines.append("### 计算结果\n")
        lines.append("| 指标 | 值 |")
        lines.append("|------|-----|")
        for k in ["esloc", "total_size", "size_ksloc", "effort_pm", "schedule_months", "team_size"]:
            lines.append(f"| {k} | {r.get(k)} |")
        lines.append("")
        lines.append("### ROI\n")
        lines.append("| 指标 | 值 |")
        lines.append("|------|-----|")
        for k, v in r["roi"].items():
            lines.append(f"| {k} | {v} |")
        if "sensitivity" in r:
            lines.append("")
            lines.append("### 敏感性分析\n")
            lines.append("| 参数 | 基值 | 低值 PM | 高值 PM | 影响 | 影响% |")
            lines.append("|------|------|---------|---------|------|-------|")
            for row in r["sensitivity"]:
                lines.append(
                    f"| {row['parameter']} | {row['base_value']} | {row['effort_low']} | "
                    f"{row['effort_high']} | {row['impact']} | {row['impact_percent']}% |"
                )
    else:
        lines.append("## 多场景对比\n")
        keys = ["scenario", "esloc", "total_size", "size_ksloc", "effort_pm", "schedule_months", "team_size"]
        header = "| " + " | ".join(keys) + " |"
        lines.append(header)
        lines.append("|" + "|".join(["---"] * len(keys)) + "|")
        for r in results:
            row = "| " + " | ".join(str(r.get(k, "")) for k in keys) + " |"
            lines.append(row)

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def export_results(results: list[dict[str, Any]], path: str) -> None:
    """根据扩展名自动选择导出格式。"""
    ext = Path(path).suffix.lower()
    if ext == ".json":
        export_json(results, path)
    elif ext == ".csv":
        export_csv(results, path)
    elif ext in (".md", ".markdown"):
        export_md(results, path)
    else:
        raise ValueError(f"不支持的输出格式: {ext}（请使用 .json/.csv/.md）")


# ---------------------------------------------------------------------------
# 最小 YAML 加载器（仅依赖标准库）
# ---------------------------------------------------------------------------

def _parse_yaml_scalar(token: str) -> Any:
    """安全解析 YAML 标量值。"""
    token = token.strip()
    if not token:
        return None
    if token.startswith('"') and token.endswith('"'):
        return token[1:-1]
    if token.startswith("'") and token.endswith("'"):
        return token[1:-1]
    if token.startswith("[") and token.endswith("]"):
        return ast.literal_eval(token)
    try:
        return ast.literal_eval(token)
    except Exception:
        return token


def _yaml_clean_lines(text: str) -> list[tuple[int, str]]:
    """去除注释与空行，返回 (indent, content) 列表。"""
    lines: list[tuple[int, str]] = []
    for line in text.splitlines():
        # 简单去除行末注释（忽略引号内 # 的复杂情况，足够本项目使用）
        line = re.sub(r"\s+#.*$", "", line)
        stripped = line.lstrip()
        if not stripped:
            continue
        indent = len(line) - len(stripped)
        lines.append((indent, stripped))
    return lines


def _yaml_parse_block(lines: list[tuple[int, str]], idx: int, base_indent: int) -> tuple[Any, int]:
    """递归解析 YAML 块，返回 (value, next_idx)。"""
    if idx >= len(lines):
        return {}, idx

    first_indent, first_content = lines[idx]
    if first_content.startswith("- "):
        # 列表
        result: list[Any] = []
        while idx < len(lines):
            indent, content = lines[idx]
            if indent < base_indent:
                break
            if indent > base_indent:
                raise ValueError(f"YAML 缩进错误: {content}")
            item_content = content[2:].strip()
            if ":" in item_content:
                # 列表项内联键值，可能有子项
                key, rest = item_content.split(":", 1)
                item: dict[str, Any] = {}
                if rest.strip():
                    item[key.strip()] = _parse_yaml_scalar(rest)
                idx += 1
                if idx < len(lines) and lines[idx][0] > base_indent:
                    child_indent = lines[idx][0]
                    children, idx = _yaml_parse_block(lines, idx, child_indent)
                    if isinstance(children, dict):
                        item.update(children)
                    else:
                        item[key.strip()] = children
                result.append(item)
            else:
                result.append(_parse_yaml_scalar(item_content))
                idx += 1
        return result, idx
    else:
        # 字典
        result_dict: dict[str, Any] = {}
        while idx < len(lines):
            indent, content = lines[idx]
            if indent < base_indent:
                break
            if indent > base_indent:
                raise ValueError(f"YAML 缩进错误: {content}")
            if ":" not in content:
                raise ValueError(f"YAML 格式错误: {content}")
            key, rest = content.split(":", 1)
            key = key.strip()
            rest = rest.strip()
            if rest:
                result_dict[key] = _parse_yaml_scalar(rest)
                idx += 1
            else:
                idx += 1
                if idx < len(lines) and lines[idx][0] > base_indent:
                    child_indent = lines[idx][0]
                    child_value, idx = _yaml_parse_block(lines, idx, child_indent)
                    result_dict[key] = child_value
                else:
                    result_dict[key] = None
        return result_dict, idx


def load_yaml_simple(text: str) -> Any:
    """最小 YAML 解析器，支持本工具配置所需的基础映射与列表。"""
    lines = _yaml_clean_lines(text)
    if not lines:
        return {}
    first_indent = lines[0][0]
    result, _ = _yaml_parse_block(lines, 0, first_indent)
    return result


# ---------------------------------------------------------------------------
# 输出与展示
# ---------------------------------------------------------------------------

def print_report(result: dict[str, Any], sensitivity: list[dict[str, Any]] | None = None) -> None:
    """在终端打印计算报告。"""
    p = result["inputs"]
    print("=" * 70)
    print("COCOMO II 2026 复用成本计算报告")
    print("=" * 70)
    print(f"  场景名称        : {result['scenario']}")
    print(f"  计算模式        : {p['mode']}")
    print(f"  目标系统 SLOC   : {p['sloc']:,}")
    if p["mode"] == "official":
        print(f"  复用代码 ASLOC  : {p['asloc']:,.1f}")
        print(f"  自动转换 AT     : {p['at']:.1f}%")
        print(f"  评估同化 AA     : {p['aa']:.1f}%")
        print(f"  改编因子 AAF    : {p['aaf']:.2f}%" if p["aaf"] is not None else "  改编因子 AAF    : (由 DM/CM/IM 计算)")
        print(f"  DM/CM/IM        : {p['dm']:.1f}% / {p['cm']:.1f}% / {p['im']:.1f}%")
        print(f"  SU / UNFM       : {p['su']:.1f}% / {p['unfm']:.2f}")
    else:
        print(f"  输入 SLOC       : {p['sloc']:,}")
        print(f"  AAM (改编调整)  : {p['aam']:.4f}" if p.get('aam') is not None else "  AAM (改编调整)  : N/A")
        print(f"  SU (理解度)     : {p['su']:.2f}")
        print(f"  UNFM(未熟悉度)  : {p['unfm']:.2f}")
    print(f"  A 常数 / 指数 E : {p['a']:.2f} / {p['e']:.3f}")
    print(f"  综合乘数 EM     : {p['em']:.4f}")
    print(f"  工期参数 C,D    : {p['schedule_c']:.2f}, {p['schedule_d']:.4f}")
    print(f"  SCED 进度因子   : {p['sced']:.2f}")
    print("-" * 70)
    print(f"  ESLOC (等效新代码): {result['esloc']:,.1f}")
    print(f"  总规模 (SLOC)   : {result['total_size']:,.1f}")
    print(f"  总规模 (KSLOC)  : {result['size_ksloc']:.4f}")
    print(f"  估计工作量      : {result['effort_pm']:.2f} 人月")
    print(f"  估计工期        : {result['schedule_months']:.2f} 月")
    if result["team_size"] is not None:
        print(f"  平均团队规模    : {result['team_size']:.2f} 人")
    print("-" * 70)
    print("  复用 ROI 分析")
    print(f"    从零开发工作量: {result['roi']['effort_nominal']:.2f} 人月")
    print(f"    复用节省工作量: {result['roi']['cost_saving']:.2f} 人月")
    print(f"    理论 ROI      : {result['roi']['roi_nominal_percent']:.1f}%")
    if "actual_effort" in result["roi"]:
        print(f"    实际投入工作量: {result['roi']['actual_effort']:.2f} 人月")
        print(f"    实际 ROI      : {result['roi']['roi_actual_percent']:.1f}%")

    if sensitivity:
        print("-" * 70)
        print("  敏感性分析（±20% 扰动）")
        print(f"  {'参数':<10} {'基值':>10} {'低 PM':>10} {'高 PM':>10} {'影响':>10} {'影响%':>8}")
        for row in sensitivity:
            print(
                f"  {row['parameter']:<10} {row['base_value']:>10.2f} "
                f"{row['effort_low']:>10.2f} {row['effort_high']:>10.2f} "
                f"{row['impact']:>10.2f} {row['impact_percent']:>7.1f}%"
            )

    print("=" * 70)

    # 复用决策建议
    aaf_or_aam = result["inputs"].get("aaf")
    threshold_exceeded = False
    if result["inputs"]["mode"] == "official" and aaf_or_aam is not None and aaf_or_aam >= 70.0:
        threshold_exceeded = True
    elif result["inputs"]["mode"] != "official" and result["inputs"].get("aam", 0.0) >= 0.7:
        threshold_exceeded = True

    roi_key = "roi_actual_percent" if "roi_actual_percent" in result["roi"] else "roi_nominal_percent"
    roi_value = result["roi"][roi_key]

    if threshold_exceeded:
        print("⚠️  警告: AAF/AAM ≥ 0.7，复用改编成本接近重新开发，建议评估战略价值而非仅看直接 ROI。")
    elif roi_value < 0:
        print("⚠️  警告: ROI 为负，复用未产生正向收益，请审查输入参数假设。")
    else:
        print("✅ 复用方案经济可行，建议执行。")


# ---------------------------------------------------------------------------
# 配置批量模式
# ---------------------------------------------------------------------------

def run_config(args: argparse.Namespace) -> list[dict[str, Any]]:
    """读取 YAML 配置文件并批量运行场景。"""
    config_path = Path(args.config)
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    raw = load_yaml_simple(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("配置文件根节点必须是映射（mapping）")

    defaults = raw.get("defaults", {}) or {}
    scenarios = raw.get("scenarios", [{}])
    if not isinstance(scenarios, list):
        raise ValueError("配置中的 'scenarios' 必须是列表")

    results: list[dict[str, Any]] = []
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            scenario = {"name": str(scenario)}
        merged = dict(defaults)
        merged.update(scenario)
        scenario_name = str(merged.pop("name", f"scenario_{len(results) + 1}"))
        params = build_params(merged)
        result = run_scenario(params, scenario_name)
        if args.sensitivity:
            result["sensitivity"] = sensitivity_analysis(params)
        results.append(result)

    return results


# ---------------------------------------------------------------------------
# 单场景模式
# ---------------------------------------------------------------------------

def run_single(args: argparse.Namespace) -> list[dict[str, Any]]:
    """运行单个 CLI 场景。"""
    raw = vars(args)
    params = build_params(raw)
    result = run_scenario(params, "default")
    if args.sensitivity:
        result["sensitivity"] = sensitivity_analysis(params)
    return [result]


# ---------------------------------------------------------------------------
# 单元测试
# ---------------------------------------------------------------------------

def run_tests() -> None:
    """运行内置单元测试，验证公式、导出与敏感性分析。"""
    print("Running COCOMO II calculator unit tests...")

    # 1. 简化模式 ESLOC / 工作量 / 工期
    esloc_legacy = compute_esloc_legacy(50000, 0.3, 0.4, 1.0)
    assert abs(esloc_legacy - 10500.0) < 0.01, f"legacy esloc mismatch: {esloc_legacy}"
    effort_legacy = compute_effort(esloc_legacy / 1000.0, DEFAULT_BASIC_A, DEFAULT_BASIC_E, 1.0)
    assert 38.0 < effort_legacy < 40.0, f"legacy effort out of range: {effort_legacy}"
    schedule_legacy = compute_schedule(effort_legacy, 3.67, 0.3179)
    assert 11.0 < schedule_legacy < 13.0, f"legacy schedule out of range: {schedule_legacy}"

    # 2. 官方复用模型（无 AI 调整）
    aaf = compute_aaf(30.0, 20.0, 50.0)
    assert abs(aaf - 33.0) < 0.01, f"aaf mismatch: {aaf}"
    aam = compute_aam(10.0, aaf, 20.0, 0.5)
    expected_aam = (10.0 + 33.0 * (1.0 + 0.02 * 20.0 * 0.5)) / 100.0
    assert abs(aam - expected_aam) < 0.0001, f"aam mismatch: {aam}"
    esloc_official = compute_esloc_official(3000.0, 0.0, aam)
    assert abs(esloc_official - 1488.0) < 0.5, f"official esloc mismatch: {esloc_official}"

    # 3. AAF > 50 分支
    aam_high = compute_aam(5.0, 60.0, 20.0, 0.5)
    expected_aam_high = (5.0 + 60.0 + (20.0 * 0.5)) / 100.0
    assert abs(aam_high - expected_aam_high) < 0.0001, f"aam high branch mismatch: {aam_high}"

    # 4. 规模因子指数
    sf = parse_sf("4,3,3,3,3")
    assert sf == [4.0, 3.0, 3.0, 3.0, 3.0]
    e = DEFAULT_B + 0.01 * sum(sf)
    assert abs(e - 1.07) < 0.0001, f"exponent mismatch: {e}"

    # 5. 综合乘数解析
    assert abs(parse_em("0.71,0.85,1.25,1.08") - 0.815) < 0.001
    assert parse_em(None) == 1.0

    # 6. 完整官方场景（2026 校准示例近似）
    raw = {
        "mode": "official",
        "sloc": 10000,
        "asloc": 3000,
        "aa": 10,
        "dm": 30,
        "cm": 20,
        "im": 50,
        "su": 20,
        "unfm": 0.5,
        "a": 2.20,
        "sf": "4,3,3,3,3",
        "em": 0.815,
    }
    params = build_params(raw)
    result = run_scenario(params)
    assert abs(result["esloc"] - 1488.0) < 1.0, f"scenario esloc mismatch: {result['esloc']}"
    assert 16.0 < result["effort_pm"] < 19.0, f"scenario effort out of range: {result['effort_pm']}"

    # 7. 敏感性分析
    sens = sensitivity_analysis(params)
    assert len(sens) > 0
    assert all("impact" in row for row in sens)
    # 影响应已按绝对值降序排列
    for i in range(len(sens) - 1):
        assert abs(sens[i]["impact"]) >= abs(sens[i + 1]["impact"])

    # 8. 导出格式验证
    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = os.path.join(tmpdir, "result.json")
        csv_path = os.path.join(tmpdir, "result.csv")
        md_path = os.path.join(tmpdir, "result.md")

        export_json([result], json_path)
        with open(json_path, encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded["effort_pm"] == result["effort_pm"]

        export_csv([result], csv_path)
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        assert len(rows) == 1
        assert "effort_pm" in rows[0] or "effort_pm" in [c.strip() for c in rows[0].keys()]

        export_md([result], md_path)
        md_content = Path(md_path).read_text(encoding="utf-8")
        assert "COCOMO II" in md_content
        assert str(result["effort_pm"]) in md_content

    # 9. YAML 配置解析
    sample_yaml = """
defaults:
  sloc: 10000
  asloc: 3000
  aa: 10
  dm: 30
  cm: 20
  im: 50
  su: 20
  unfm: 0.5
  sf: [4, 3, 3, 3, 3]
  em: 0.815
  a: 2.20
scenarios:
  - name: baseline
  - name: high_reuse
    dm: 10
    cm: 5
"""
    config = load_yaml_simple(sample_yaml)
    assert config["defaults"]["sloc"] == 10000
    assert len(config["scenarios"]) == 2
    assert config["scenarios"][1]["name"] == "high_reuse"

    print("All tests passed.")


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="COCOMO II 2026 复用成本计算器（官方 Reuse 模型 + 2026 校准）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 向后兼容的简化模式
  python cocomo-calculator.py --sloc 50000 --aam 0.3 --su 0.4 --unfm 1.0 --effort 120

  # 官方 COCOMO II Reuse 模型
  python cocomo-calculator.py --sloc 10000 --asloc 3000 --aa 10 \\
      --dm 30 --cm 20 --im 50 --su 20 --unfm 0.5 \\
      --a 2.20 --sf 4,3,3,3,3 --em 0.815 --output result.json

  # 敏感性分析
  python cocomo-calculator.py --sloc 10000 --asloc 3000 --dm 30 --cm 20 --im 50 \\
      --su 20 --unfm 0.5 --sensitivity

  # 批量场景（YAML 配置）
  python cocomo-calculator.py --config scenario.yaml --output report.md

  # 单元测试
  python cocomo-calculator.py --test

说明:
  --sf  接受 5 个逗号分隔的规模因子评分（PREC, FLEX, RESL, TEAM, PMAT）。
  --em  可为单一综合乘数，或 17 个逗号分隔成本驱动因子的乘积。
  --schedule 格式为 "C,D"，例如 "3.67,0.3179"。
        """,
    )

    # 运行控制
    parser.add_argument("--test", action="store_true", help="运行内置单元测试")
    parser.add_argument("--config", type=str, default=None, help="YAML 配置文件路径（批量多场景）")
    parser.add_argument("--output", type=str, default=None, help="导出报告路径（.json/.csv/.md）")
    parser.add_argument("--sensitivity", action="store_true", help="执行敏感性分析并输出 tornado 表")

    # 原有参数（向后兼容）
    parser.add_argument("--sloc", type=int, default=0, help="目标系统总源代码行数（SLOC）")
    parser.add_argument("--aam", type=float, default=None, help="改编调整因子 AAM [0.0, 1.0]（简化模式）")
    parser.add_argument("--su", type=float, default=0.0, help="软件理解度 SU（简化模式 0-1，官方模型 0-100%%）")
    parser.add_argument("--unfm", type=float, default=1.0, help="未熟悉度 UNFM [0.0, 2.0]")
    parser.add_argument("--effort", type=float, default=None, help="实际投入工作量（人月），用于 ROI 计算")
    parser.add_argument("--mode", type=str, choices=["basic", "intermediate", "official"], default="basic",
                        help="计算模式: basic=简化（向后兼容）, intermediate=中间模型, official=官方复用模型")

    # 官方复用模型参数
    # 注意：默认值为 None，这样只有用户显式传入时才会触发官方复用模型，
    # 未传入时这些值在 build_params 中会被替换为 0.0。
    parser.add_argument("--asloc", type=float, default=None, help="需适配的源代码行数 ASLOC（SLOC）")
    parser.add_argument("--at", type=float, default=None, help="自动转换百分比 AT [0-100]（默认 0）")
    parser.add_argument("--aa", type=float, default=None, help="评估与同化百分比 AA [0-100]（默认 0）")
    parser.add_argument("--aaf", type=float, default=None, help="改编调整因子 AAF [0-100]，若未提供则由 DM/CM/IM 计算")
    parser.add_argument("--dm", type=float, default=None, help="设计修改百分比 DM [0-100]（默认 0）")
    parser.add_argument("--cm", type=float, default=None, help="代码修改百分比 CM [0-100]（默认 0）")
    parser.add_argument("--im", type=float, default=None, help="集成修改百分比 IM [0-100]（默认 0）")
    parser.add_argument("--new-sloc", type=float, default=None, help="除复用外的新开发代码行数（可选；默认 sloc - asloc）")

    # COCOMO II 中间模型参数
    parser.add_argument("--sf", type=str, default=None, help="5 个规模因子评分，逗号分隔，默认 4,3,3,3,3")
    parser.add_argument("--em", type=str, default=None, help="综合工作量乘数 EM，或 17 个逗号分隔乘数")
    parser.add_argument("--a", type=float, default=None, help=f"COCOMO A 常数（官方默认 {DEFAULT_OFFICIAL_A}，简化默认 {DEFAULT_BASIC_A}）")
    parser.add_argument("--b", type=float, default=DEFAULT_B, help=f"规模指数基数 B（默认 {DEFAULT_B}）")

    # 工期参数
    parser.add_argument("--schedule", type=str, default=f"{DEFAULT_SCHEDULE[0]},{DEFAULT_SCHEDULE[1]}",
                        help="工期参数 C,D，例如 '3.67,0.3179'")
    parser.add_argument("--sced", type=float, default=DEFAULT_SCED, help="进度约束乘数 SCED（默认 1.0）")

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.test:
        try:
            run_tests()
            return 0
        except AssertionError as exc:
            print(f"[测试失败] {exc}", file=sys.stderr)
            return 1
        except Exception as exc:
            print(f"[测试异常] {exc}", file=sys.stderr)
            return 1

    try:
        if args.config:
            results = run_config(args)
        else:
            results = run_single(args)

        # 终端输出
        for result in results:
            print_report(result, result.get("sensitivity") if args.sensitivity else None)
            if len(results) > 1:
                print()

        # 导出
        if args.output:
            export_results(results, args.output)
            print(f"报告已导出: {args.output}")

    except ValueError as exc:
        print(f"[错误] 参数校验失败: {exc}", file=sys.stderr)
        return 1
    except FileNotFoundError as exc:
        print(f"[错误] {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"[错误] {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
