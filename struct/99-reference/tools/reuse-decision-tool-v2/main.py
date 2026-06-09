#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式复用决策工具 v2.0 — CLI 主入口

命令:
    decide          完整六阶段复用决策流程
    check-standard  检查标准对齐状态
    assess-maturity 评估复用成熟度
    card            生成复用决策卡片（Markdown/JSON）

用法示例:
    python -m reuse_decision_tool decide --asset "支付网关组件" --context "电商微服务架构" --output report.md
    python -m reuse_decision_tool check-standard --standard iso42010 --version 2022
    python -m reuse_decision_tool assess-maturity --level 3 --dimension all
    python -m reuse_decision_tool card --asset-id PAY-GW-001 --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from decision_engine import (
    AssetProfile,
    ContextProfile,
    ReuseDecisionEngine,
    create_engine_from_data_dir,
)


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def get_data_dir() -> Path:
    """获取数据目录路径"""
    return Path(__file__).resolve().parent / "data"


def print_banner() -> None:
    """打印 CLI 横幅"""
    print("=" * 60)
    print("  交互式复用决策工具 v2.0")
    print("  Reuse Decision Tool — 六阶段决策流程")
    print("=" * 60)
    print()


def load_engine() -> ReuseDecisionEngine:
    """加载决策引擎"""
    data_dir = get_data_dir()
    if not (data_dir / "decision_rules.json").exists():
        print(f"错误: 数据文件未找到于 {data_dir}", file=sys.stderr)
        sys.exit(1)
    return create_engine_from_data_dir(data_dir)


# ---------------------------------------------------------------------------
# 子命令: decide
# ---------------------------------------------------------------------------

def cmd_decide(args: argparse.Namespace) -> int:
    """执行完整决策流程"""
    print_banner()
    engine = load_engine()

    # 构建资产画像
    asset = AssetProfile(
        asset_id=args.asset_id or "ASSET-001",
        name=args.asset,
        category=args.category or "",
        domain_scope=args.domain.split(",") if args.domain else [],
        supported_tech=args.tech.split(",") if args.tech else [],
        rrl=args.rrl,
        maturity=args.maturity,
        reliability=args.reliability,
        maintainability=args.maintainability,
        license=args.license,
        security_level=args.security_level,
        slsa_level=args.slsa_level,
        aaf_typical=args.aaf,
        npv_positive=args.npv_positive,
        extra={"estimated_aaf": args.aaf, "estimated_npv": args.npv},
    )

    # 构建上下文画像
    context = ContextProfile(
        name=args.context,
        required_domain=args.domain.split(",") if args.domain else [],
        tech_constraints=args.tech.split(",") if args.tech else [],
        min_rrl=args.min_rrl,
        min_maturity=args.min_maturity,
        min_reliability=args.min_reliability,
        approved_licenses=args.licenses.split(",") if args.licenses else ["MIT", "Apache-2.0", "BSD"],
        min_security_level=args.min_security_level,
        min_slsa_level=args.min_slsa_level,
        max_payback_years=args.max_payback,
        org_maturity_level=args.org_maturity,
        process_standardized=args.process_standardized,
        asset_catalog_exists=args.asset_catalog,
        extra={"estimated_aaf": args.aaf, "estimated_npv": args.npv},
    )

    print(f"📝 资产: {asset.name}")
    print(f"🌐 上下文: {context.name}")
    print()

    result = engine.evaluate(asset, context)

    # 控制台输出
    print("─" * 60)
    print(f"最终决策: {result.final_decision.value}")
    print(f"置信度评分: {result.final_score}/100")
    print("─" * 60)
    print()

    print("【六阶段评估详情】")
    for pr in result.phase_results:
        status_icon = {"通过": "✅", "条件通过": "⚠️", "拒绝": "❌", "未评估": "⏳"}
        icon = status_icon.get(pr.status.value, "")
        print(f"  {icon} {pr.phase_name:20s} — 得分: {pr.score:5.1f} — {pr.status.value}")
        for msg in pr.messages:
            print(f"      ⚠ {msg}")
    print()

    if result.risks:
        print("【风险登记】")
        for r in result.risks:
            sev_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}
            print(f"  {sev_icon.get(r.severity, '')} [{r.severity}] {r.description}")
            print(f"      缓解: {r.mitigation}")
        print()

    print("【推荐行动】")
    for rec in result.recommendations:
        print(f"  • {rec}")
    print()

    if result.upgrade_path:
        print(f"【升级路径】 {' → '.join(result.upgrade_path)}")
    if result.downgrade_path:
        print(f"【降级路径】 {' → '.join(result.downgrade_path)}")

    # 输出报告
    if args.output:
        output_path = Path(args.output)
        if output_path.suffix.lower() == ".json":
            content = json.dumps(result.to_dict(), ensure_ascii=False, indent=2)
        else:
            # 默认 Markdown
            content = engine.generate_decision_card(result.asset_id, fmt="markdown")
            # 但用实际结果覆盖
            content = _result_to_markdown(result)

        output_path.write_text(content, encoding="utf-8")
        print(f"\n📄 报告已保存: {output_path}")

    # 退出码映射
    if result.final_decision.value == "批准复用":
        return 0
    elif result.final_decision.value == "条件批准":
        return 2
    else:
        return 1


def _result_to_markdown(result) -> str:
    """将决策结果转为 Markdown 报告"""
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
# 子命令: check-standard
# ---------------------------------------------------------------------------

def cmd_check_standard(args: argparse.Namespace) -> int:
    """检查标准对齐状态"""
    engine = load_engine()
    report = engine.check_standard_alignment(args.standard, args.version)

    if not report.get("found"):
        print(f"❌ {report['message']}", file=sys.stderr)
        return 1

    print(f"📋 标准: {report['name']}")
    print(f"   全称: {report['full_name']}")
    print(f"   当前版本: {report['current_version']}")
    print(f"   状态: {report['status']}")
    print(f"   URL: {report['url']}")
    print(f"   复用相关性: {report['relevance']}")
    if report.get("version_warning"):
        print(f"   ⚠️  {report['version_warning']}")
    print()

    print("【对齐检查清单】")
    for i, item in enumerate(report["alignment_checklist"], 1):
        print(f"  {i}. {item}")
    print()

    print("【合规等级定义】")
    for level, desc in report["compliance_levels"].items():
        print(f"  {level}: {desc}")

    return 0


# ---------------------------------------------------------------------------
# 子命令: assess-maturity
# ---------------------------------------------------------------------------

def cmd_assess_maturity(args: argparse.Namespace) -> int:
    """评估复用成熟度"""
    engine = load_engine()
    result = engine.assess_maturity(args.level, args.dimension)

    if "error" in result:
        print(f"❌ {result['error']}", file=sys.stderr)
        return 1

    print(f"📊 复用成熟度评估 — 目标等级: {result['target_level']} ({result['target_level_name']})")
    print(f"   描述: {result['target_level_description']}")
    print()

    for dim in result["gap_analysis"]:
        print(f"【{dim['dimension_id']}】{dim['dimension_name']}")
        for q in dim["questions"]:
            print(f"  ❓ {q['text']}")
            print(f"     🎯 目标状态: {q['target_level_answer']} (权重: {q['weight']})")
        print()

    print(f"💡 建议: {result['recommendation']}")
    return 0


# ---------------------------------------------------------------------------
# 子命令: card
# ---------------------------------------------------------------------------

def cmd_card(args: argparse.Namespace) -> int:
    """生成复用决策卡片"""
    engine = load_engine()
    card = engine.generate_decision_card(args.asset_id, fmt=args.format)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(card, encoding="utf-8")
        print(f"📄 决策卡片已保存: {output_path}")
    else:
        print(card)

    return 0


# ---------------------------------------------------------------------------
# CLI 参数解析
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """构建 CLI 参数解析器"""
    parser = argparse.ArgumentParser(
        prog="reuse_decision_tool",
        description="交互式复用决策工具 v2.0 — 支持六阶段复用决策流程",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 完整决策流程
  python -m reuse_decision_tool decide --asset "支付网关" --context "电商平台"

  # 快速检查标准对齐
  python -m reuse_decision_tool check-standard --standard iso42010

  # 评估成熟度（特定维度）
  python -m reuse_decision_tool assess-maturity --level 4 --dimension D1

  # 生成 JSON 格式决策卡片
  python -m reuse_decision_tool card --asset-id PAT-MICRO-002 --format json
        """,
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="可用子命令")

    # --- decide ---
    p_decide = subparsers.add_parser("decide", help="执行完整六阶段复用决策")
    p_decide.add_argument("--asset", required=True, help="资产名称")
    p_decide.add_argument("--asset-id", default=None, help="资产 ID（可选）")
    p_decide.add_argument("--context", required=True, help="上下文/需求场景名称")
    p_decide.add_argument("--category", default="", help="资产类别")
    p_decide.add_argument("--domain", default="", help="领域范围，逗号分隔")
    p_decide.add_argument("--tech", default="", help="技术约束，逗号分隔")
    p_decide.add_argument("--rrl", type=float, default=3.5, help="复用准备度 RRL (0-5)")
    p_decide.add_argument("--maturity", type=int, default=3, help="资产成熟度 (1-5)")
    p_decide.add_argument("--reliability", type=float, default=0.90, help="可靠性 (0-1)")
    p_decide.add_argument("--maintainability", type=float, default=0.85, help="可维护性 (0-1)")
    p_decide.add_argument("--license", default="MIT", help="许可证类型")
    p_decide.add_argument("--security-level", default="L2", help="安全等级 L1-L4")
    p_decide.add_argument("--slsa-level", type=int, default=1, help="SLSA 等级 1-3")
    p_decide.add_argument("--aaf", type=float, default=0.35, help="预估改编调整因子 AAF (0-1)")
    p_decide.add_argument("--npv", type=float, default=1.0, help="预估 NPV")
    p_decide.add_argument("--npv-positive", action="store_true", default=True, help="NPV 是否为正")
    p_decide.add_argument("--min-rrl", type=float, default=3.0, help="要求的最小 RRL")
    p_decide.add_argument("--min-maturity", type=int, default=3, help="要求的最小成熟度")
    p_decide.add_argument("--min-reliability", type=float, default=0.85, help="要求的最小可靠性")
    p_decide.add_argument("--licenses", default="MIT,Apache-2.0,BSD", help="批准的许可证列表，逗号分隔")
    p_decide.add_argument("--min-security-level", default="L2", help="要求的最小安全等级")
    p_decide.add_argument("--min-slsa-level", type=int, default=1, help="要求的最小 SLSA 等级")
    p_decide.add_argument("--max-payback", type=float, default=3.0, help="最大回收期（年）")
    p_decide.add_argument("--org-maturity", type=int, default=3, help="组织复用成熟度 (1-5)")
    p_decide.add_argument("--process-standardized", action="store_true", help="流程是否标准化")
    p_decide.add_argument("--asset-catalog", action="store_true", help="资产目录是否已建立")
    p_decide.add_argument("--output", "-o", default=None, help="输出报告路径 (.md 或 .json)")
    p_decide.set_defaults(func=cmd_decide)

    # --- check-standard ---
    p_std = subparsers.add_parser("check-standard", help="检查标准对齐状态")
    p_std.add_argument("--standard", required=True, help="标准键名，如 iso42010, slsa, mcp")
    p_std.add_argument("--version", default=None, help="指定版本号进行对比")
    p_std.set_defaults(func=cmd_check_standard)

    # --- assess-maturity ---
    p_mat = subparsers.add_parser("assess-maturity", help="评估复用成熟度")
    p_mat.add_argument("--level", type=int, required=True, help="目标成熟度等级 1-5")
    p_mat.add_argument(
        "--dimension",
        default="all",
        help="评估维度，如 D1(战略与投资), D2(过程与管理) 等，默认 all",
    )
    p_mat.set_defaults(func=cmd_assess_maturity)

    # --- card ---
    p_card = subparsers.add_parser("card", help="生成复用决策卡片")
    p_card.add_argument("--asset-id", required=True, help="资产 ID")
    p_card.add_argument("--format", choices=["markdown", "json"], default="markdown", help="输出格式")
    p_card.add_argument("--output", "-o", default=None, help="输出文件路径")
    p_card.set_defaults(func=cmd_card)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """CLI 主入口"""
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
