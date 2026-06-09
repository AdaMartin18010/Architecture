#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式复用决策工具 v2.0 — Streamlit Web 界面

运行方式:
    streamlit run web_app.py

界面布局:
    - 左侧：输入面板（资产信息、上下文需求、约束条件）
    - 右侧：决策结果（通过/条件通过/拒绝）、风险热力图、推荐行动
    - 底部：导出报告（PDF/Markdown）
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import streamlit as st

from decision_engine import (
    AssetProfile,
    ContextProfile,
    DecisionResult,
    ReuseDecisionEngine,
    create_engine_from_data_dir,
)

# ---------------------------------------------------------------------------
# 页面配置
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="复用决策工具 v2.0",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# 初始化引擎（缓存）
# ---------------------------------------------------------------------------

@st.cache_resource
def get_engine() -> ReuseDecisionEngine:
    """缓存加载决策引擎，避免每次交互重新加载 JSON"""
    data_dir = Path(__file__).resolve().parent / "data"
    return create_engine_from_data_dir(data_dir)


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def status_color(status_value: str) -> str:
    """根据状态返回颜色码"""
    mapping = {
        "通过": "green",
        "条件通过": "orange",
        "拒绝": "red",
        "未评估": "gray",
        "批准复用": "green",
        "条件批准": "orange",
        "需要补充信息": "blue",
    }
    return mapping.get(status_value, "black")


def severity_color(severity: str) -> str:
    """根据严重程度返回颜色"""
    mapping = {"HIGH": "#ff4b4b", "MEDIUM": "#ffa421", "LOW": "#21c354"}
    return mapping.get(severity, "gray")


def render_risk_heatmap(risks: List[Any]) -> None:
    """渲染风险热力图（使用 Streamlit 原生组件模拟）"""
    if not risks:
        st.info("🎉 未发现显著风险")
        return

    st.subheader("🌡️ 风险热力图")

    # 按阶段分组统计
    phase_risks: Dict[str, List[Any]] = {}
    for r in risks:
        phase_risks.setdefault(r.phase, []).append(r)

    cols = st.columns(len(phase_risks)) if phase_risks else []
    for idx, (phase, rlist) in enumerate(phase_risks.items()):
        with cols[idx % len(cols)]:
            high = sum(1 for r in rlist if r.severity == "HIGH")
            medium = sum(1 for r in rlist if r.severity == "MEDIUM")
            low = sum(1 for r in rlist if r.severity == "LOW")

            # 用 metric 模拟热力
            st.metric(
                label=phase,
                value=f"{len(rlist)} 项",
                delta=f"🔴 {high}  🟡 {medium}  🟢 {low}",
            )

            for r in rlist:
                color = severity_color(r.severity)
                st.markdown(
                    f"<span style='color:{color};font-size:0.9em'>● {r.description[:40]}...</span>",
                    unsafe_allow_html=True,
                )


def render_phase_detail(phase_results: List[Any]) -> None:
    """渲染阶段详情"""
    st.subheader("📊 六阶段评估详情")

    for pr in phase_results:
        status_emoji = {"通过": "✅", "条件通过": "⚠️", "拒绝": "❌", "未评估": "⏳"}
        emoji = status_emoji.get(pr.status.value, "")
        expander_title = f"{emoji} {pr.phase_name} — 得分: {pr.score:.1f} — {pr.status.value}"

        with st.expander(expander_title):
            # 规则详情表格
            if pr.details:
                detail_data = []
                for d in pr.details:
                    detail_data.append(
                        {
                            "规则": d.get("rule_name", ""),
                            "通过": "✅" if d.get("passed") else "❌",
                            "实际值": str(d.get("actual", "—")),
                            "阈值": str(d.get("threshold", "—")),
                            "得分": d.get("score", 0),
                        }
                    )
                st.dataframe(detail_data, use_container_width=True, hide_index=True)

            if pr.messages:
                st.markdown("**异常信息:**")
                for msg in pr.messages:
                    st.warning(msg)
            else:
                st.success("该阶段无异常")


def render_recommendations(result: DecisionResult) -> None:
    """渲染推荐行动"""
    st.subheader("💡 推荐行动")

    decision_icons = {
        "批准复用": "🟢",
        "条件批准": "🟡",
        "拒绝复用": "🔴",
        "需要补充信息": "🔵",
    }
    icon = decision_icons.get(result.final_decision.value, "")

    st.markdown(
        f"### {icon} 最终决策: {result.final_decision.value} (置信度: {result.final_score}/100)"
    )

    for rec in result.recommendations:
        if rec.startswith("✅"):
            st.success(rec)
        elif rec.startswith("⚠️"):
            st.warning(rec)
        elif rec.startswith("❌"):
            st.error(rec)
        elif rec.startswith("🔍") or rec.startswith("💡"):
            st.info(rec)
        else:
            st.markdown(f"- {rec}")

    if result.upgrade_path:
        st.markdown(f"**⬆️ 升级路径**: {' → '.join(result.upgrade_path)}")
    if result.downgrade_path:
        st.markdown(f"**⬇️ 降级路径**: {' → '.join(result.downgrade_path)}")


def export_markdown_report(result: DecisionResult) -> str:
    """导出 Markdown 报告"""
    lines = [
        f"# 复用决策报告: {result.asset_name}",
        f"",
        f"- **资产 ID**: `{result.asset_id}`",
        f"- **上下文**: {result.context_name}",
        f"- **决策结果**: {result.final_decision.value}",
        f"- **置信度评分**: {result.final_score}/100",
        f"",
        f"## 六阶段评估详情",
        f"",
        "| 阶段 | 状态 | 得分 | 备注 |",
        "|------|------|------|------|",
    ]
    for pr in result.phase_results:
        msgs = "；".join(pr.messages) if pr.messages else "—"
        lines.append(f"| {pr.phase_name} | {pr.status.value} | {pr.score:.1f} | {msgs} |")

    lines.extend([f"", f"## 风险登记", f""])
    if result.risks:
        lines.append("| 风险 ID | 阶段 | 严重程度 | 描述 | 缓解措施 |")
        lines.append("|---------|------|----------|------|----------|")
        for r in result.risks:
            lines.append(f"| {r.risk_id} | {r.phase} | {r.severity} | {r.description} | {r.mitigation} |")
    else:
        lines.append("无显著风险。")

    lines.extend([f"", f"## 推荐行动", f""])
    for rec in result.recommendations:
        lines.append(f"- {rec}")

    lines.extend([
        f"",
        f"---",
        f"> 报告由 复用决策引擎 v2.0 自动生成",
    ])
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 主界面
# ---------------------------------------------------------------------------

def main() -> None:
    """Streamlit 主界面"""
    st.title("🧭 交互式复用决策工具 v2.0")
    st.caption("基于六阶段复用决策流程的智能评估系统")

    engine = get_engine()

    # -----------------------------------------------------------------------
    # 左侧边栏：输入面板
    # -----------------------------------------------------------------------
    with st.sidebar:
        st.header("📋 输入面板")

        st.subheader("资产信息")
        asset_name = st.text_input("资产名称", value="支付网关组件")
        asset_id = st.text_input("资产 ID", value="PAY-GW-001")
        asset_category = st.selectbox(
            "资产类别",
            ["微服务", "分层架构", "Serverless", "事件驱动", "MCP/AI Native", "WASM", "其他"],
        )
        asset_domain = st.text_input("适用领域（逗号分隔）", value="电商,金融")
        asset_tech = st.text_input("技术栈（逗号分隔）", value="Kubernetes,gRPC,Java")

        col_a1, col_a2 = st.columns(2)
        with col_a1:
            asset_rrl = st.slider("RRL", 0.0, 5.0, 3.5, 0.1)
            asset_maturity = st.slider("成熟度", 1, 5, 3)
        with col_a2:
            asset_reliability = st.slider("可靠性", 0.0, 1.0, 0.90, 0.01)
            asset_maintainability = st.slider("可维护性", 0.0, 1.0, 0.85, 0.01)

        asset_license = st.selectbox(
            "许可证",
            ["MIT", "Apache-2.0", "BSD", "GPL-3.0", "专有", "未知"],
        )
        asset_security = st.selectbox("安全等级", ["L1", "L2", "L3", "L4"])
        asset_slsa = st.slider("SLSA 等级", 1, 3, 2)
        asset_aaf = st.slider("预估 AAF", 0.0, 1.0, 0.35, 0.05)

        st.divider()
        st.subheader("上下文需求")
        context_name = st.text_input("上下文名称", value="电商微服务架构")
        req_domain = st.text_input("需求领域（逗号分隔）", value="电商")
        req_tech = st.text_input("约束技术栈（逗号分隔）", value="Kubernetes,Java")

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            min_rrl = st.slider("最小 RRL", 0.0, 5.0, 3.0, 0.1)
            min_maturity = st.slider("最小成熟度", 1, 5, 3)
        with col_c2:
            min_reliability = st.slider("最小可靠性", 0.0, 1.0, 0.85, 0.01)
            min_maintainability = st.slider("最小可维护性", 0.0, 1.0, 0.80, 0.01)

        min_security = st.selectbox("最小安全等级", ["L1", "L2", "L3", "L4"], index=1)
        min_slsa = st.slider("最小 SLSA", 1, 3, 1)
        max_payback = st.slider("最大回收期（年）", 0.5, 10.0, 3.0, 0.5)

        st.divider()
        st.subheader("组织治理")
        org_maturity = st.slider("组织复用成熟度", 1, 5, 3)
        process_standardized = st.checkbox("流程已标准化", value=False)
        asset_catalog_exists = st.checkbox("资产目录已建立", value=False)

        st.divider()
        run_clicked = st.button("🚀 执行决策评估", type="primary", use_container_width=True)

    # -----------------------------------------------------------------------
    # 右侧主面板
    # -----------------------------------------------------------------------
    if run_clicked:
        # 构建画像
        asset = AssetProfile(
            asset_id=asset_id,
            name=asset_name,
            category=asset_category,
            domain_scope=[d.strip() for d in asset_domain.split(",") if d.strip()],
            supported_tech=[t.strip() for t in asset_tech.split(",") if t.strip()],
            rrl=asset_rrl,
            maturity=asset_maturity,
            reliability=asset_reliability,
            maintainability=asset_maintainability,
            license=asset_license,
            security_level=asset_security,
            slsa_level=asset_slsa,
            aaf_typical=asset_aaf,
            npv_positive=True,
            extra={"estimated_aaf": asset_aaf, "estimated_npv": 1.0},
        )

        context = ContextProfile(
            name=context_name,
            required_domain=[d.strip() for d in req_domain.split(",") if d.strip()],
            tech_constraints=[t.strip() for t in req_tech.split(",") if t.strip()],
            min_rrl=min_rrl,
            min_maturity=min_maturity,
            min_reliability=min_reliability,
            min_maintainability=min_maintainability,
            approved_licenses=["MIT", "Apache-2.0", "BSD"],
            min_security_level=min_security,
            min_slsa_level=min_slsa,
            max_payback_years=max_payback,
            org_maturity_level=org_maturity,
            process_standardized=process_standardized,
            asset_catalog_exists=asset_catalog_exists,
            extra={"estimated_aaf": asset_aaf, "estimated_npv": 1.0},
        )

        with st.spinner("正在执行六阶段复用决策评估..."):
            result = engine.evaluate(asset, context)

        # 结果显示
        tab_result, tab_risk, tab_export = st.tabs(["📊 决策结果", "🌡️ 风险热力图", "📥 导出报告"])

        with tab_result:
            render_recommendations(result)
            st.divider()
            render_phase_detail(result.phase_results)

        with tab_risk:
            render_risk_heatmap(result.risks)

            if result.risks:
                st.subheader("📋 风险登记详情")
                risk_data = []
                for r in result.risks:
                    risk_data.append(
                        {
                            "风险 ID": r.risk_id,
                            "阶段": r.phase,
                            "严重程度": r.severity,
                            "描述": r.description,
                            "缓解措施": r.mitigation,
                        }
                    )
                st.dataframe(risk_data, use_container_width=True, hide_index=True)

        with tab_export:
            st.subheader("📥 导出报告")
            fmt = st.radio("格式", ["Markdown", "JSON"], horizontal=True)

            if fmt == "Markdown":
                report_md = export_markdown_report(result)
                st.download_button(
                    label="下载 Markdown 报告",
                    data=report_md,
                    file_name=f"reuse_decision_{result.asset_id}.md",
                    mime="text/markdown",
                )
                with st.expander("预览报告"):
                    st.markdown(report_md)
            else:
                report_json = json.dumps(result.to_dict(), ensure_ascii=False, indent=2)
                st.download_button(
                    label="下载 JSON 报告",
                    data=report_json,
                    file_name=f"reuse_decision_{result.asset_id}.json",
                    mime="application/json",
                )
                with st.expander("预览 JSON"):
                    st.json(result.to_dict())

    else:
        # 初始状态
        st.info("👈 请在左侧输入资产信息和上下文需求，然后点击「执行决策评估」")

        st.markdown("""
        ### 六阶段复用决策流程简介

        1. **语义兼容性判定** — 业务语义是否覆盖需求？技术约束是否匹配？
        2. **变性绑定判定** — 变性模型是否可交集？绑定时机是否可行？
        3. **质量达标判定** — RRL、成熟度、可靠性是否满足阈值？
        4. **安全合规判定** — 许可证是否在白名单？安全等级是否足够？
        5. **成本收益判定** — COCOMO II AAF < 0.7？NPV > 0？
        6. **治理合规判定** — 组织成熟度、流程标准化、资产目录是否就绪？
        """)

        # 展示内置模式库
        st.subheader("📚 内置复用模式")
        patterns = engine.patterns.get("patterns", [])
        pat_data = []
        for p in patterns:
            pat_data.append(
                {
                    "ID": p["id"],
                    "名称": p["name"],
                    "类别": p["category"],
                    "典型 AAF": p.get("cost_profile", {}).get("aaf_typical", "—"),
                    "RRL": p.get("quality_profile", {}).get("rrl", "—"),
                }
            )
        st.dataframe(pat_data, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
