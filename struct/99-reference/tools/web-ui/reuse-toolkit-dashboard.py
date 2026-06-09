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
        "🧭 复用决策向导",
    ],
)

# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def tool_path(rel: str) -> Path:
    """返回相对于项目根的工具路径。"""
    return PROJECT_ROOT / rel


def run_cli(cmd: List[str], cwd: Path | None = None) -> tuple[str, str, int]:
    """运行外部 CLI 命令并返回 stdout, stderr, returncode。"""
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    return result.stdout, result.stderr, result.returncode


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
            for line in stdout.splitlines():
                if "选中" in line or "selected" in line.lower():
                    st.success(line.strip())
        else:
            st.error(f"运行失败: {stderr}")

# ---------------------------------------------------------------------------
# 4. 术语查询（真正调用 CLI）
# ---------------------------------------------------------------------------
elif tool == "📖 术语查询":
    st.header("📖 跨标准术语查询")
    st.markdown("查询术语在 ISO 42010、TOGAF、ArchiMate、MCP 等标准中的定义差异。")

    script = tool_path("struct/99-reference/tools/terminology-query.py")

    tab_query, tab_search = st.tabs(["精确查询", "模糊搜索"])

    with tab_query:
        term = st.text_input("输入术语（英文）", value="Component")
        if st.button("查询", type="primary"):
            stdout, stderr, rc = run_cli([sys.executable, str(script), "query", term])
            if rc == 0:
                st.text(stdout)
            else:
                st.warning(f"精确查询失败，尝试模糊搜索...\n{stderr}")
                stdout2, stderr2, rc2 = run_cli([sys.executable, str(script), "search", term])
                if rc2 == 0:
                    st.text(stdout2)
                else:
                    st.error(stderr2)

    with tab_search:
        keyword = st.text_input("输入关键词", value="reuse")
        if st.button("搜索", type="primary"):
            stdout, stderr, rc = run_cli([sys.executable, str(script), "search", keyword])
            if rc == 0:
                st.text(stdout)
            else:
                st.error(f"搜索失败: {stderr}")

    with st.expander("查看支持的术语列表"):
        stdout, _, rc = run_cli([sys.executable, str(script), "list", "--standard", "ISO"])
        if rc == 0:
            st.text(stdout)
        else:
            st.info("术语列表加载失败，请直接运行 CLI: `python terminology-query.py list --standard 'ISO 42010:2022'`")

# ---------------------------------------------------------------------------
# 5. COCOMO II 复用估算（真正调用 CLI）
# ---------------------------------------------------------------------------
elif tool == "📐 COCOMO II 复用估算":
    st.header("📐 COCOMO II 复用成本估算")
    st.markdown("基于 COCOMO II Reuse Model 估算自研 vs 复用的成本差异。")

    col1, col2 = st.columns(2)
    with col1:
        ksloc_reused = st.number_input("复用 KSLOC", 0.0, 1000.0, 50.0, 5.0)
        aaf = st.slider("改编调整因子 (AAF)", 0.0, 1.0, 0.30, 0.05)
    with col2:
        em = st.slider("工作量乘数 (EM)", 0.5, 3.0, 1.0, 0.1)
        a_coeff = st.number_input("校准系数 A", 0.1, 10.0, 2.94, 0.1)

    if st.button("计算估算", type="primary"):
        script = tool_path("struct/99-reference/tools/cocomo-calculator.py")
        cmd = [
            sys.executable, str(script),
            "--ksloc-reused", str(ksloc_reused),
            "--aaf", str(aaf),
            "--em", str(em),
            "--a", str(a_coeff),
        ]
        stdout, stderr, rc = run_cli(cmd)
        if rc == 0:
            st.text(stdout)
            # 尝试解析关键指标
            for line in stdout.splitlines():
                if "ESLOC" in line or "PM" in line or "ROI" in line:
                    st.info(line.strip())
        else:
            st.error(f"计算失败: {stderr}")

# ---------------------------------------------------------------------------
# 6. 复用决策向导（新增）
# ---------------------------------------------------------------------------
elif tool == "🧭 复用决策向导":
    st.header("🧭 六阶段复用决策向导")
    st.markdown("基于 ISO/IEC 26550:2015 与 NASA RRL 的复用决策流程。")

    step = st.selectbox(
        "当前阶段",
        [
            "1️⃣ 需求分析 — 识别复用机会",
            "2️⃣ 资产发现 — 搜索可用资产",
            "3️⃣ 评估匹配 — 质量与适配度检查",
            "4️⃣ 适配改造 — 修改与集成",
            "5️⃣ 验证确认 — 测试与合规",
            "6️⃣ 反馈改进 — 度量与资产更新",
        ],
    )

    if "1️⃣" in step:
        st.subheader("阶段 1：需求分析")
        st.markdown("""
        **关键问题**:
        - 该功能是否已在组织资产库中存在？
        - 业务需求的稳定性如何？（稳定需求更适合复用）
        - 时间压力是否允许复用搜索与评估？
        """)
        stability = st.slider("需求稳定性", 1, 5, 3)
        urgency = st.slider("时间紧迫度 (1=宽松, 5=极紧)", 1, 5, 3)
        if stability >= 4 and urgency <= 3:
            st.success("✅ 建议优先考虑复用")
        elif urgency >= 4:
            st.warning("⚠️ 时间紧迫，需权衡复用搜索成本 vs 快速自研")
        else:
            st.info("ℹ️ 继续下一阶段评估")

    elif "2️⃣" in step:
        st.subheader("阶段 2：资产发现")
        st.markdown("搜索内部资产库、开源生态（GitHub/Package Registry）和商业组件。")
        sources = st.multiselect(
            "搜索范围",
            ["内部组件库", "开源社区", "商业 COTS", "SaaS API", "MCP/A2A Agent 市场"],
            default=["内部组件库", "开源社区"],
        )
        if sources:
            st.success(f"已选择 {len(sources)} 个搜索源")

    elif "3️⃣" in step:
        st.subheader("阶段 3：评估匹配")
        st.markdown("使用成熟度评估和质量检查清单。")
        quality = st.slider("资产质量评分 (1-5)", 1, 5, 3)
        adaptability = st.slider("适配难度 (1=极易, 5=极难)", 1, 5, 3)
        if quality >= 4 and adaptability <= 3:
            st.success("✅ 匹配度高，建议复用")
        elif adaptability >= 4:
            st.error("❌ 适配成本过高，建议自研或寻找替代资产")
        else:
            st.warning("⚠️ 需进一步成本分析（进入 COCOMO 估算）")

    elif "4️⃣" in step:
        st.subheader("阶段 4：适配改造")
        st.markdown("记录改编工作量并更新资产元数据。")
        aaf_est = st.slider("预估 AAF", 0.0, 1.0, 0.30, 0.05)
        if aaf_est < 0.3:
            st.success("✅ 低改编成本，经济可行")
        elif aaf_est < 0.7:
            st.warning("⚠️ 中等改编成本，需 ROI 验证")
        else:
            st.error("❌ 改编成本接近自研，复用经济性丧失")

    elif "5️⃣" in step:
        st.subheader("阶段 5：验证确认")
        st.markdown("运行测试套件、安全扫描和合规检查。")
        checks = st.multiselect(
            "验证项",
            ["单元测试", "集成测试", "SLSA 来源验证", "SBOM 更新", "许可证合规"],
            default=["单元测试", "集成测试"],
        )
        if len(checks) >= 3:
            st.success("✅ 验证充分，可进入部署")

    elif "6️⃣" in step:
        st.subheader("阶段 6：反馈改进")
        st.markdown("度量复用收益并将改进反馈到资产库。")
        feedback = st.text_area("改进建议", "记录适配过程中发现的通用化机会...")
        if st.button("提交反馈"):
            st.success("✅ 反馈已记录（实际系统中将写入资产库元数据）")

# ---------------------------------------------------------------------------
# 页脚
# ---------------------------------------------------------------------------
st.divider()
st.caption("""
**架构复用知识体系** · Phase 2-6 可执行工具栈
- [成熟度评估](https://github.com/.../assessment-tool.py) · [FinOps 分摊](https://github.com/.../finops-allocation.py) · [CP 校准](https://github.com/.../calibration-tool.py)
- 文档生成时间：2026-06-10
""")
