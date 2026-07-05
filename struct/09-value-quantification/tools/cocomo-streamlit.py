#!/usr/bin/env python3
"""
COCOMO II 2026 复用成本计算器 —— Streamlit 交互式应用

用法:
    streamlit run cocomo-streamlit.py

或查看帮助:
    python cocomo-streamlit.py --help
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# 复用 cocomo-calculator.py 中的核心函数
# ---------------------------------------------------------------------------

_FILE = Path(__file__).resolve()
_CALC_PATH = _FILE.with_name("cocomo-calculator.py")

_spec = importlib.util.spec_from_file_location("cocomo_calculator", _CALC_PATH)
if _spec is None or _spec.loader is None:
    raise RuntimeError(f"无法加载计算器模块: {_CALC_PATH}")

_cocomo: Any = importlib.util.module_from_spec(_spec)
sys.modules["cocomo_calculator"] = _cocomo
_spec.loader.exec_module(_cocomo)

build_params = _cocomo.build_params
run_scenario = _cocomo.run_scenario
sensitivity_analysis = _cocomo.sensitivity_analysis


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(page_title="COCOMO II 2026 Reuse Calculator", layout="wide")
    st.title("COCOMO II 2026 复用成本计算器")
    st.markdown(
        "基于官方 COCOMO II Reuse 模型（AAM / AAF / DM / CM / IM / SU / UNFM）"
        "与 2026 校准参数。"
    )

    mode = st.sidebar.radio(
        "计算模式",
        options=["official", "basic", "intermediate"],
        format_func=lambda x: {
            "official": "官方复用模型 (Reuse Model)",
            "basic": "向后兼容简化模式",
            "intermediate": "COCOMO II 中间模型",
        }[x],
        help="官方模型需输入 ASLOC、AA、DM/CM/IM、SU、UNFM 等参数。",
    )

    st.sidebar.header("基础参数")
    sloc = st.sidebar.number_input(
        "目标系统总 SLOC", min_value=0, value=10000, step=1000, help="Source Lines of Code"
    )
    actual_effort = st.sidebar.number_input(
        "实际投入工作量（人月，可选）",
        min_value=0.0,
        value=0.0,
        step=1.0,
        help="用于计算实际 ROI；留空 0 则只显示理论 ROI。",
    )

    # 官方复用模型参数
    if mode == "official":
        st.sidebar.header("官方复用模型参数")
        asloc = st.sidebar.number_input(
            "ASLOC（需适配代码行数）", min_value=0.0, value=3000.0, step=100.0
        )
        new_sloc = st.sidebar.number_input(
            "new SLOC（新增代码行数，可选）",
            min_value=0.0,
            value=0.0,
            step=100.0,
            help="默认 = sloc - asloc",
        )
        at = st.sidebar.slider("AT 自动转换 (%)", 0.0, 100.0, 0.0, 1.0)
        aa = st.sidebar.slider("AA 评估与同化 (%)", 0.0, 100.0, 10.0, 1.0)
        dm = st.sidebar.slider("DM 设计修改 (%)", 0.0, 100.0, 30.0, 1.0)
        cm = st.sidebar.slider("CM 代码修改 (%)", 0.0, 100.0, 20.0, 1.0)
        im = st.sidebar.slider("IM 集成修改 (%)", 0.0, 100.0, 50.0, 1.0)
        su = st.sidebar.slider("SU 软件理解度 (%)", 0.0, 100.0, 20.0, 1.0)
        unfm = st.sidebar.slider("UNFM 未熟悉度", 0.0, 2.0, 0.5, 0.1)
        aam = None
    else:
        asloc = 0.0
        new_sloc = 0.0
        at = 0.0
        aa = 0.0
        dm = 0.0
        cm = 0.0
        im = 0.0
        if mode == "basic":
            su = st.sidebar.slider("SU 软件理解度（小数）", 0.0, 1.0, 0.4, 0.05)
            unfm = st.sidebar.slider("UNFM 未熟悉度（小数）", 0.0, 1.0, 1.0, 0.05)
        else:
            su = st.sidebar.slider("SU 软件理解度 (%)", 0.0, 100.0, 20.0, 1.0)
            unfm = st.sidebar.slider("UNFM 未熟悉度", 0.0, 2.0, 0.5, 0.1)
        aam = st.sidebar.number_input(
            "AAM 改编调整乘数", min_value=0.0, max_value=1.0, value=0.3, step=0.05
        )

    st.sidebar.header("COCOMO II 参数")
    a = st.sidebar.number_input("A 常数", min_value=0.1, value=2.20, step=0.1)
    b = st.sidebar.number_input("B 常数", min_value=0.1, value=0.91, step=0.01)
    sf_str = st.sidebar.text_input("规模因子 SF（逗号分隔 5 项）", value="4,3,3,3,3")
    em_str = st.sidebar.text_input("综合工作量乘数 EM（单一值或逗号分隔乘积）", value="0.815")
    schedule_str = st.sidebar.text_input("工期参数 C,D", value="3.67,0.3179")
    sced = st.sidebar.number_input("SCED 进度约束", min_value=0.1, value=1.0, step=0.1)

    run_sens = st.sidebar.checkbox("执行敏感性分析并绘制 tornado 图", value=True)

    raw: dict[str, Any] = {
        "mode": mode,
        "sloc": int(sloc),
        "aam": aam,
        "asloc": asloc if mode == "official" else None,
        "new_sloc": new_sloc if mode == "official" and new_sloc > 0 else None,
        "at": at,
        "aa": aa,
        "dm": dm,
        "cm": cm,
        "im": im,
        "su": su,
        "unfm": unfm,
        "a": a,
        "b": b,
        "sf": sf_str,
        "em": em_str,
        "schedule": schedule_str,
        "sced": sced,
        "effort": actual_effort if actual_effort > 0 else None,
    }

    try:
        params = build_params(raw)
        result = run_scenario(params, "streamlit")
        if run_sens:
            result["sensitivity"] = sensitivity_analysis(params)
    except ValueError as exc:
        st.error(f"参数校验失败: {exc}")
        return
    except Exception as exc:
        st.error(f"计算异常: {exc}")
        return

    # 结果展示
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("ESLOC", f"{result['esloc']:,.1f}")
    col2.metric("总规模 (KSLOC)", f"{result['size_ksloc']:.4f}")
    col3.metric("估计工作量 (PM)", f"{result['effort_pm']:.2f}")
    col4.metric("估计工期 (月)", f"{result['schedule_months']:.2f}")

    if result["team_size"] is not None:
        st.metric("平均团队规模", f"{result['team_size']:.2f} 人")

    st.subheader("ROI 分析")
    roi = result["roi"]
    r1, r2, r3 = st.columns(3)
    r1.metric("从零开发工作量", f"{roi['effort_nominal']:.2f} 人月")
    r2.metric("复用节省工作量", f"{roi['cost_saving']:.2f} 人月")
    r3.metric("理论 ROI", f"{roi['roi_nominal_percent']:.1f}%")
    if "actual_effort" in roi:
        r4, r5 = st.columns(2)
        r4.metric("实际投入工作量", f"{roi['actual_effort']:.2f} 人月")
        r5.metric("实际 ROI", f"{roi['roi_actual_percent']:.1f}%")

    if run_sens and result.get("sensitivity"):
        st.subheader("敏感性分析（±20% 扰动）")
        sens_df = pd.DataFrame(result["sensitivity"])
        sens_df = sens_df.sort_values("impact", key=abs, ascending=True)
        chart_df = sens_df.set_index("parameter")[["impact"]]
        st.bar_chart(chart_df, horizontal=True)
        with st.expander("查看敏感性数据"):
            st.dataframe(
                sens_df[["parameter", "base_value", "effort_low", "effort_high", "impact", "impact_percent"]],
                use_container_width=True,
            )

    with st.expander("查看完整输入参数"):
        st.json(result["inputs"])


if __name__ == "__main__":
    if "--help" in sys.argv:
        print(__doc__)
        sys.exit(0)
    main()
