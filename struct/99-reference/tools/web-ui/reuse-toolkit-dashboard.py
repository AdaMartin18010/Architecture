#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
架构复用工具箱统一 Web UI（Streamlit）
包装现有 CLI 工具，提供统一的浏览器界面。

运行: streamlit run reuse-toolkit-dashboard.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import List

import streamlit as st

# ---------------------------------------------------------------------------
# 页面配置
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="架构复用工具箱",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏗️ 架构复用工具箱")
st.caption("Software Architecture Reuse Toolkit — Phase 2 可执行工具统一界面")

# ---------------------------------------------------------------------------
# 侧边栏导航
# ---------------------------------------------------------------------------
tool = st.sidebar.radio(
    "选择工具",
    [
        "📊 复用成熟度评估",
        "💰 FinOps 成本分摊",
        "🤖 AI 概率契约校准",
        "📖 术语查询",
        "📐 COCOMO II 复用估算",
    ],
)

# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def run_cli(cmd: List[str], cwd: Path | None = None) -> tuple[str, str, int]:
    """运行外部 CLI 命令并返回 stdout, stderr, returncode。"""
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return result.stdout, result.stderr, result.returncode


def tool_path(rel: str) -> Path:
    """返回相对于项目根的工具路径。"""
    return Path(__file__).resolve().parents[3] / rel


# ---------------------------------------------------------------------------
# 1. 复用成熟度评估
# ---------------------------------------------------------------------------
if tool == "📊 复用成熟度评估":
    st.header("📊 复用成熟度评估（ISO/IEC 26566:2026）")
    st.markdown("基于 RCMM / RiSE / NASA RRL 的 6 维度 × 5 题问卷，输出成熟度等级与雷达图。")

    demo_mode = st.checkbox("使用演示数据（随机生成）", value=False)

    if st.button("运行评估", type="primary"):
        script = tool_path("struct/06-cross-layer-governance/03-maturity-models/assessment-tool.py")
        cmd = [sys.executable, str(script)]
        if demo_mode:
            cmd.append("--demo")
        with st.spinner("评估中..."):
            stdout, stderr, rc = run_cli(cmd)
        if rc == 0:
            st.text(stdout)
            st.success("评估完成")
        else:
            st.error(f"运行失败: {stderr}")

    with st.expander("查看评估维度说明"):
        st.markdown("""
        - **复用战略与投资**：组织是否将复用视为战略优先事项
        - **复用过程与管理**：是否有标准化的复用流程
        - **资产开发与维护**：组件库的生命周期管理
        - **基础设施与支持**：工具、平台、目录的支持程度
        - **人员与培训**：团队的复用意识和技能
        - **度量与改进**：是否量化复用收益并持续改进
        """)

# ---------------------------------------------------------------------------
# 2. FinOps 成本分摊
# ---------------------------------------------------------------------------
elif tool == "💰 FinOps 成本分摊":
    st.header("💰 FinOps 跨层成本分摊")
    st.markdown("Business → Application → Component → Function 四层成本分摊计算器。")

    tab_demo, tab_csv = st.tabs(["演示模式", "CSV 上传"])

    with tab_demo:
        if st.button("运行演示", type="primary"):
            script = tool_path("struct/06-cross-layer-governance/04-finops-cost/templates/finops-allocation.py")
            with st.spinner("计算中..."):
                stdout, stderr, rc = run_cli([sys.executable, str(script), "--demo"])
            if rc == 0:
                st.text(stdout)
            else:
                st.error(f"运行失败: {stderr}")

    with tab_csv:
        uploaded = st.file_uploader("上传 FOCUS 风格 CSV 账单", type=["csv"])
        tag_key = st.text_input("直接分配标签键", value="business_unit")
        if uploaded and st.button("计算分摊", type="primary"):
            import tempfile
            with tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False) as f:
                f.write(uploaded.getvalue())
                tmp_path = f.name
            script = tool_path("struct/06-cross-layer-governance/04-finops-cost/templates/finops-allocation.py")
            cmd = [sys.executable, str(script), "--csv", tmp_path, "--tag-key", tag_key]
            with st.spinner("计算中..."):
                stdout, stderr, rc = run_cli(cmd)
            if rc == 0:
                try:
                    data = json.loads(stdout)
                    st.json(data)
                    st.metric("总成本", data.get("total_cost", "N/A"))
                    st.metric("分配准确率 (AAI)", f"{data.get('aai', 'N/A')}%")
                except json.JSONDecodeError:
                    st.text(stdout)
            else:
                st.error(f"运行失败: {stderr}")

# ---------------------------------------------------------------------------
# 3. AI 概率契约校准
# ---------------------------------------------------------------------------
elif tool == "🤖 AI 概率契约校准":
    st.header("🤖 AI 功能概率契约校准（Conformal Prediction）")
    st.markdown("为 LLM/AI 生成的候选代码/功能提供 `P(correctness) ≥ 1-α` 的统计保证。")

    col1, col2 = st.columns(2)
    with col1:
        alpha = st.slider("显著性水平 α", 0.01, 0.50, 0.10, 0.01)
        n_candidates = st.number_input("候选数量", 1, 100, 10)
    with col2:
        n_calibration = st.number_input("校准集大小", 10, 10000, 100)
        demo_mode = st.checkbox("使用演示数据", value=True)

    if st.button("运行校准", type="primary"):
        script = tool_path("struct/12-ai-native-reuse/04-probabilistic-contracts/calibration-tool.py")
        cmd = [sys.executable, str(script), "--alpha", str(alpha), "--candidates", str(n_candidates)]
        if demo_mode:
            cmd.append("--sample")
            cmd.append(str(n_calibration))
        with st.spinner("校准中..."):
            stdout, stderr, rc = run_cli(cmd)
        if rc == 0:
            st.text(stdout)
            # 尝试提取关键数字
            for line in stdout.splitlines():
                if "选中" in line or "selected" in line.lower():
                    st.success(line.strip())
        else:
            st.error(f"运行失败: {stderr}")

# ---------------------------------------------------------------------------
# 4. 术语查询
# ---------------------------------------------------------------------------
elif tool == "📖 术语查询":
    st.header("📖 跨标准术语查询")
    st.markdown("查询术语在 ISO 42010、TOGAF、ArchiMate、MCP 等标准中的定义差异。")

    query = st.text_input("输入术语", value="Component")
    if st.button("查询", type="primary"):
        script = tool_path("struct/99-reference/tools/terminology-query.py")
        # 术语查询工具可能为交互式，此处模拟输出
        st.info("术语查询工具当前为交互式 CLI。以下为常见术语对照示例：")
        st.table([
            {"术语": query, "ISO 42010": "系统或软件产品中可识别的组成部分", "TOGAF 10": "Architecture Building Block (ABB) 或 Solution Building Block (SBB)", "ArchiMate 3.2": "Application Component / Technology Service", "MCP 2025-11-25": "Tool / Resource / Prompt"},
            {"术语": "Viewpoint", "ISO 42010": "约定框架，用于创建、解释和使用视图", "TOGAF 10": "Stakeholder-specific 架构视角", "ArchiMate 3.2": "Layered / Capability / Motivation Viewpoint", "MCP 2025-11-25": "—"},
            {"术语": "Reuse", "ISO 42010": "—", "TOGAF 10": "Enterprise Continuum / Architecture Repository", "ArchiMate 3.2": "Serving / Realization 关系", "MCP 2025-11-25": "Sampling / Tool reuse"},
        ])

# ---------------------------------------------------------------------------
# 5. COCOMO II 复用估算
# ---------------------------------------------------------------------------
elif tool == "📐 COCOMO II 复用估算":
    st.header("📐 COCOMO II 复用成本估算")
    st.markdown("基于 COCOMO II Reuse Model 估算自研 vs 复用的成本差异。")

    col1, col2 = st.columns(2)
    with col1:
        sloc_new = st.number_input("新开发 SLOC", 0, 1000000, 10000)
        sloc_reused = st.number_input("复用 SLOC", 0, 1000000, 5000)
    with col2:
        adaptability = st.slider("适应性调整因子 (AAF)", 0.0, 1.0, 0.20, 0.05)
        understanding = st.slider("理解代价因子", 0.0, 1.0, 0.10, 0.05)

    if st.button("计算估算", type="primary"):
        script = tool_path("struct/99-reference/tools/cocomo-calculator.py")
        # COCOMO 工具可能为交互式，此处提供公式计算
        suoc = sloc_reused * (1 - adaptability / 100)  # 简化计算
        esloc = sloc_new + suoc
        cost_reduction = sloc_reused - suoc
        st.metric("等效 SLOC (ESLOC)", f"{esloc:,.0f}")
        st.metric("复用节省 SLOC", f"{cost_reduction:,.0f}")
        st.info("详细计算请运行 CLI: `python cocomo-calculator.py`")

# ---------------------------------------------------------------------------
# 页脚
# ---------------------------------------------------------------------------
st.divider()
st.caption("""
**架构复用知识体系** · Phase 2 可执行工具栈
- [成熟度评估](https://github.com/.../assessment-tool.py) · [FinOps 分摊](https://github.com/.../finops-allocation.py) · [CP 校准](https://github.com/.../calibration-tool.py)
- 文档生成时间：2026-06-06
""")
