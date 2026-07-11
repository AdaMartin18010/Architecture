# -*- coding: utf-8 -*-
"""AAF 统一判定函数 —— P1 语义硬门控。

设计要点：
- AAF 的 canonical 形式为 [0.0, 1.0] 的小数。
- 为兼容历史代码/文档中 [0, 100] 的百分比写法，>1.0 时按百分比自动归一化。
- COCOMO AAM 分支阈值 0.5 与复用经济阈值 0.7/0.9 解耦。
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class ReuseVerdict(Enum):
    REUSE_ECONOMIC = "REUSE_ECONOMIC"      # 优先复用
    TRADE_OFF = "TRADE_OFF"                # 权衡决策（需战略价值/风险复核）
    REBUILD = "REBUILD"                    # 建议重新实现


# 阈值常数（可抽离到 YAML/JSON 配置）
COCOMO_AAM_BRANCH: float = 0.5
AAF_ECONOMIC_FLOOR: float = 0.7
AAF_REBUILD_CEILING: float = 0.9


@dataclass(frozen=True)
class ReuseDecision:
    verdict: ReuseVerdict
    aaf: float
    aaf_normalized: float
    economic_upper_bound: float  # 1.0 + v_reuse_ratio
    reason: str


def normalize_aaf(aaf: float) -> float:
    """归一化 AAF 到 [0.0, 1.0]。"""
    if aaf is None:
        raise ValueError("AAF 不能为空")
    if aaf < 0:
        raise ValueError("AAF 不能为负")
    # 兼容历史百分比输入（如 70 表示 70%）
    return aaf / 100.0 if aaf > 1.0 else float(aaf)


def compute_aam(aa: float, aaf: float, su: float, unfm: float) -> float:
    """COCOMO II AAM 计算；aaf 为小数 canonical 形式。"""
    aaf_pct = aaf * 100.0
    aa_pct = aa * 100.0 if aa <= 1.0 else aa
    su_pct = su * 100.0 if su <= 1.0 else su
    if aaf_pct <= COCOMO_AAM_BRANCH * 100.0:
        return (aa_pct + aaf_pct * (1.0 + 0.02 * su_pct * unfm)) / 100.0
    return (aa_pct + aaf_pct + (su_pct * unfm)) / 100.0


def reuse_decision(
    aaf: float,
    *,
    strategic_value: bool = False,
    v_reuse_ratio: float = 0.0,
    economic_floor: float = AAF_ECONOMIC_FLOOR,
    rebuild_ceiling: float = AAF_REBUILD_CEILING,
) -> ReuseDecision:
    """统一复用经济判定函数。

    Args:
        aaf: 改编调整因子（小数或百分比，自动归一化）。
        strategic_value: 是否存在显著战略价值（可覆盖 REBUILD 到 TRADE_OFF）。
        v_reuse_ratio: V_reuse / C_build，用于 Th.6 的理论上限校验。
        economic_floor: 经济绿灯/黄灯阈值，默认 0.7。
        rebuild_ceiling: 黄灯/红灯阈值，默认 0.9。
    """
    aaf_n = normalize_aaf(aaf)
    absolute_upper = 1.0 + max(v_reuse_ratio, 0.0)

    if aaf_n >= absolute_upper:
        verdict = ReuseVerdict.REBUILD
        reason = f"AAF({aaf_n:.2f}) >= 理论可行上限({absolute_upper:.2f})"
    elif aaf_n >= rebuild_ceiling:
        verdict = ReuseVerdict.TRADE_OFF if strategic_value else ReuseVerdict.REBUILD
        reason = (
            f"AAF({aaf_n:.2f}) >= 重新实现阈值({rebuild_ceiling:.2f})"
            + ("；存在战略价值，进入权衡流程" if strategic_value else "；建议重新实现")
        )
    elif aaf_n >= economic_floor:
        verdict = ReuseVerdict.TRADE_OFF
        reason = f"AAF({aaf_n:.2f}) 在经济区间 [{economic_floor}, {rebuild_ceiling})，需权衡战略价值"
    else:
        verdict = ReuseVerdict.REUSE_ECONOMIC
        reason = f"AAF({aaf_n:.2f}) < 经济绿灯阈值({economic_floor:.2f})，优先复用"

    return ReuseDecision(
        verdict=verdict,
        aaf=aaf,
        aaf_normalized=aaf_n,
        economic_upper_bound=absolute_upper,
        reason=reason,
    )


# 对 cocomo-calculator.py 的向后兼容封装
def legacy_warning(aaf_or_aam: float, mode: str = "official") -> str:
    """替代原 70/0.7 硬编码警告。"""
    normalized = normalize_aaf(aaf_or_aam)
    dec = reuse_decision(normalized)
    if dec.verdict in (ReuseVerdict.TRADE_OFF, ReuseVerdict.REBUILD):
        return f"⚠️  {dec.reason}；建议评估战略价值而非仅看直接 ROI。"
    return "✅ 复用方案经济可行，建议执行。"
