#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FinOps Excel 公式模板生成器 (L1–L4 Cost Allocation Template Generator)

功能：
    1. 使用 openpyxl 生成可复用的 FinOps 成本分摊 Excel 模板
    2. 包含 L1–L4 四个工作表，并使用 Excel 公式实现自动计算：
       - L1-原始成本：云服务原始账单（含 ResourceID、ServiceName、Cost、Tag:Team 等）
       - L2-分摊规则：定义 Team 的分摊键（AllocationKey%）与规则说明
       - L3-分摊结果：使用 SUMIFS + XLOOKUP/VLOOKUP 将 L1 成本按 L2 规则分摊到各 Team
       - L4-单位经济学：每用户/每交易/每 Token 成本计算（含公式）
    3. 命令行支持 --output 参数，默认输出到 dist/finops-cost-allocation-template.xlsx

用法：
    python finops-excel-template.py
    python finops-excel-template.py --output ./my-template.xlsx

依赖：
    - openpyxl

对齐来源：
    - FinOps Foundation Framework 2026
    - FOCUS (FinOps Open Cost and Usage Specification)
    - 本项目 unit-economics.md / ai-cost-allocation.md 模板
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List, Tuple

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False


# ---------------------------------------------------------------------------
# 常量与样例数据
# ---------------------------------------------------------------------------
DEFAULT_OUTPUT = Path("dist/finops-cost-allocation-template.xlsx")

# L1 原始成本样例：模拟一份云服务账单
L1_HEADERS = ["ResourceID", "ServiceName", "Cost", "Tag:Team", "Tag:Env", "Tag:Project"]
L1_SAMPLE_DATA: List[Tuple[str, str, float, str, str, str]] = [
    ("i-0a1b2c3d4e5f", "EC2", 5000.00, "Platform", "prod", "SharedPlatform"),
    ("rds-appa-001", "RDS", 2400.00, "AppA", "prod", "AppA-DB"),
    ("rds-appb-001", "RDS", 1800.00, "AppB", "prod", "AppB-DB"),
    ("eks-control", "EKS", 800.00, "Platform", "prod", "SharedPlatform"),
    ("openai-inference", "AzureOpenAI", 2400.00, "AppA", "prod", "AppA-AI"),
    ("s3-data-lake", "S3", 600.00, "Data", "prod", "DataLake"),
    ("datadog-sub", "SaaS", 1200.00, "Platform", "prod", "Observability"),
    ("lambda-appb", "Lambda", 400.00, "AppB", "prod", "AppB-API"),
    ("cloudfront-cdn", "CloudFront", 900.00, "AppA", "prod", "AppA-Frontend"),
    ("vpc-flow-logs", "VPC", 300.00, "Platform", "prod", "SharedPlatform"),
]

# L2 分摊规则：共享成本池按 Team 的比例进行二次分摊
# 注：L1 中已带 Tag:Team 的直接归属成本会按 Tag 汇总，未标签/共享部分按 L2 比例拆分。
L2_HEADERS = ["Team", "AllocationKey%", "RuleDescription"]
L2_SAMPLE_RULES: List[Tuple[str, float, str]] = [
    ("AppA", 0.35, "按活跃应用数与收入贡献分摊共享平台成本"),
    ("AppB", 0.25, "按活跃应用数分摊共享平台成本"),
    ("Platform", 0.25, "平台团队承担基础设施与可观测性共享成本"),
    ("Data", 0.15, "数据团队承担数据湖与存储共享成本"),
]

# L4 单位经济学样例数据
L4_HEADERS = [
    "Metric",
    "TotalCost",
    "UnitVolume",
    "CostPerUnit",
    "Notes",
]
L4_SAMPLE_DATA: List[Tuple[str, float, float, str]] = [
    ("CostPerUser", 12000.00, 571429.0, "Total Cloud COGS / MAU"),
    ("CostPerTransaction", 3500.00, 2500000.0, "Transaction-related cost / transactions"),
    ("CostPer1KInputTokens", 7200.00, 120000.0, "LLM input cost / (input tokens / 1000)"),
    ("CostPer1KOutputTokens", 10800.00, 30000.0, "LLM output cost / (output tokens / 1000)"),
    ("CostPerRequest", 50000.00, 2000000.0, "AI total cost / total requests"),
]


# ---------------------------------------------------------------------------
# 样式辅助
# ---------------------------------------------------------------------------
def _make_styles():
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    )
    return header_font, header_fill, header_align, thin_border


def _style_header(ws, row: int, cols: int):
    header_font, header_fill, header_align, thin_border = _make_styles()
    for col in range(1, cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = thin_border


def _auto_width(ws):
    for col in ws.columns:
        max_length = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            try:
                val_len = len(str(cell.value)) if cell.value is not None else 0
                if val_len > max_length:
                    max_length = val_len
            except Exception:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[col_letter].width = adjusted_width


# ---------------------------------------------------------------------------
# 工作表构建
# ---------------------------------------------------------------------------
def _build_l1_raw_cost(ws):
    """L1-原始成本：云服务原始账单。"""
    ws.title = "L1-原始成本"
    ws.append(L1_HEADERS)
    _style_header(ws, 1, len(L1_HEADERS))

    for row in L1_SAMPLE_DATA:
        ws.append(row)

    # 设置数字格式
    for row_idx in range(2, ws.max_row + 1):
        ws.cell(row=row_idx, column=3).number_format = '#,##0.00'

    _auto_width(ws)


def _build_l2_rules(ws):
    """L2-分摊规则：分摊键定义。"""
    ws.title = "L2-分摊规则"
    ws.append(L2_HEADERS)
    _style_header(ws, 1, len(L2_HEADERS))

    for team, key, desc in L2_SAMPLE_RULES:
        ws.append([team, key, desc])

    # 校验合计为 100%
    total_row = ws.max_row + 1
    ws.cell(row=total_row, column=1, value="合计")
    ws.cell(row=total_row, column=2, value=f"=SUM(B2:B{total_row - 1})")
    ws.cell(row=total_row, column=2).number_format = '0.00%'
    for col_idx in range(1, len(L2_HEADERS) + 1):
        ws.cell(row=total_row, column=col_idx).font = Font(bold=True)

    # 百分比格式
    for row_idx in range(2, total_row):
        ws.cell(row=row_idx, column=2).number_format = '0.00%'

    _auto_width(ws)


def _build_l3_allocation(ws):
    """L3-分摊结果：使用 SUMIFS + XLOOKUP/VLOOKUP 分摊成本。"""
    ws.title = "L3-分摊结果"
    headers = ["Team", "DirectCost", "SharedCost", "AllocatedCost", "AllocationKey%", "RuleDescription"]
    ws.append(headers)
    _style_header(ws, 1, len(headers))

    l1_sheet_name = "'L1-原始成本'"
    l2_sheet_name = "'L2-分摊规则'"

    for idx, (team, key, desc) in enumerate(L2_SAMPLE_RULES, start=2):
        # DirectCost: SUMIFS L1 Cost where Tag:Team == team
        direct_formula = (
            f"=SUMIFS({l1_sheet_name}!$C$2:$C$11,"
            f"{l1_sheet_name}!$D$2:$D$11,B{idx})"
        )

        # SharedCost: 将 Tag:Team="Platform" 的共享平台成本池按 L2 比例拆分
        shared_pool_formula = (
            f"SUMIFS({l1_sheet_name}!$C$2:$C$11,"
            f"{l1_sheet_name}!$D$2:$D$11,\"Platform\")"
        )
        shared_cost_formula = f"={shared_pool_formula}*E{idx}"

        # AllocatedCost = DirectCost + SharedCost
        allocated_formula = f"=B{idx}+C{idx}"

        # AllocationKey%: VLOOKUP/XLOOKUP from L2
        if _xlookup_available():
            key_formula = f"=XLOOKUP(B{idx},{l2_sheet_name}!$A$2:$A$5,{l2_sheet_name}!$B$2:$B$5,0)"
            desc_formula = f"=XLOOKUP(B{idx},{l2_sheet_name}!$A$2:$A$5,{l2_sheet_name}!$C$2:$C$5,\"\")"
        else:
            key_formula = f"=IFERROR(VLOOKUP(B{idx},{l2_sheet_name}!$A$2:$C$5,2,FALSE),0)"
            desc_formula = f"=IFERROR(VLOOKUP(B{idx},{l2_sheet_name}!$A$2:$C$5,3,FALSE),\"\")"

        ws.append([team, direct_formula, shared_cost_formula, allocated_formula, key_formula, desc_formula])

    # 合计行
    total_row = ws.max_row + 1
    ws.cell(row=total_row, column=1, value="合计")
    for col_idx in range(2, 5):
        col_letter = get_column_letter(col_idx)
        ws.cell(row=total_row, column=col_idx, value=f"=SUM({col_letter}2:{col_letter}{total_row - 1})")
        ws.cell(row=total_row, column=col_idx).number_format = '#,##0.00'
    ws.cell(row=total_row, column=5, value="=SUM(E2:E5)")
    ws.cell(row=total_row, column=5).number_format = '0.00%'
    for col_idx in range(1, len(headers) + 1):
        ws.cell(row=total_row, column=col_idx).font = Font(bold=True)

    # 数字/百分比格式
    for row_idx in range(2, total_row):
        ws.cell(row=row_idx, column=2).number_format = '#,##0.00'
        ws.cell(row=row_idx, column=3).number_format = '#,##0.00'
        ws.cell(row=row_idx, column=4).number_format = '#,##0.00'
        ws.cell(row=row_idx, column=5).number_format = '0.00%'

    _auto_width(ws)


def _xlookup_available() -> bool:
    """XLOOKUP 仅在较新 Excel 中可用；这里默认使用 VLOOKUP 保证兼容性。"""
    return False


def _build_l4_unit_economics(ws):
    """L4-单位经济学：每用户/每交易/每 Token 成本计算。"""
    ws.title = "L4-单位经济学"
    ws.append(L4_HEADERS)
    _style_header(ws, 1, len(L4_HEADERS))

    for idx, (metric, total_cost, unit_volume, notes) in enumerate(L4_SAMPLE_DATA, start=2):
        cost_per_unit_formula = f"=B{idx}/C{idx}"
        ws.append([metric, total_cost, unit_volume, cost_per_unit_formula, notes])

    # 合计/校验行
    total_row = ws.max_row + 1
    ws.cell(row=total_row, column=1, value="TotalCloudCOGS")
    ws.cell(row=total_row, column=2, value="='L3-分摊结果'!D6")
    ws.cell(row=total_row, column=2).number_format = '#,##0.00'
    ws.cell(row=total_row, column=5, value="从 L3 分摊结果合计引用")
    for col_idx in range(1, len(L4_HEADERS) + 1):
        ws.cell(row=total_row, column=col_idx).font = Font(bold=True)

    # 数字格式
    for row_idx in range(2, total_row):
        ws.cell(row=row_idx, column=2).number_format = '#,##0.00'
        ws.cell(row=row_idx, column=3).number_format = '#,##0'
        ws.cell(row=row_idx, column=4).number_format = '#,##0.000000'

    _auto_width(ws)


def _build_readme_sheet(ws):
    """额外增加一个使用说明工作表。"""
    ws.title = "使用说明"
    instructions = [
        ["FinOps L1–L4 成本分摊 Excel 公式模板", ""],
        ["", ""],
        ["工作表", "说明"],
        ["L1-原始成本", "填写或粘贴云服务原始账单；Tag:Team 用于直接归属。"],
        ["L2-分摊规则", "维护 Team 的分摊键，合计应等于 100%。"],
        ["L3-分摊结果", "自动按 SUMIFS 汇总直接成本，并按 L2 比例拆分共享成本。"],
        ["L4-单位经济学", "基于 L3 的 TotalCloudCOGS 或独立成本池计算单位成本。"],
        ["", ""],
        ["使用提示", ""],
        ["1", "将 L1 替换为贵组织的真实云账单（保持列结构一致）。"],
        ["2", "在 L2 中调整 AllocationKey%，确保团队比例符合 FinOps 分摊策略。"],
        ["3", "L3 中的公式会自动重新计算；如需更复杂的共享池逻辑，可拆分 Platform/Data 等共享项。"],
        ["4", "L4 中的单位经济学公式可按业务指标（MAU、交易数、Token 数）自行扩展。"],
        ["", ""],
        ["对齐来源", ""],
        ["FinOps Foundation Framework 2026", ""],
        ["FOCUS (FinOps Open Cost and Usage Specification)", ""],
    ]
    for row in instructions:
        ws.append(row)

    ws.cell(row=1, column=1).font = Font(bold=True, size=14)
    ws.cell(row=3, column=1).font = Font(bold=True)
    ws.cell(row=3, column=2).font = Font(bold=True)
    ws.column_dimensions['A'].width = 35
    ws.column_dimensions['B'].width = 80


# ---------------------------------------------------------------------------
# 主生成逻辑
# ---------------------------------------------------------------------------
def generate_template(output_path: Path) -> None:
    if not HAS_OPENPYXL:
        print(
            "错误：未检测到 openpyxl。请运行以下命令安装：\n"
            "  pip install openpyxl\n"
            "或使用虚拟环境：\n"
            "  python -m venv .venv\n"
            "  source .venv/bin/activate  # Windows: .venv\\Scripts\\activate\n"
            "  pip install openpyxl",
            file=sys.stderr,
        )
        sys.exit(1)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.Workbook()

    # 删除默认 sheet，按顺序创建
    wb.remove(wb.active)

    ws_l1 = wb.create_sheet()
    _build_l1_raw_cost(ws_l1)

    ws_l2 = wb.create_sheet()
    _build_l2_rules(ws_l2)

    ws_l3 = wb.create_sheet()
    _build_l3_allocation(ws_l3)

    ws_l4 = wb.create_sheet()
    _build_l4_unit_economics(ws_l4)

    ws_readme = wb.create_sheet()
    _build_readme_sheet(ws_readme)

    wb.save(str(output_path))
    print(f"FinOps Excel 公式模板已生成: {output_path.resolve()}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(
        description="FinOps Excel 公式模板生成器 (L1–L4 Cost Allocation Template Generator)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"输出文件路径（默认: {DEFAULT_OUTPUT}）",
    )
    args = parser.parse_args()

    try:
        generate_template(args.output)
    except Exception as exc:
        print(f"错误: 生成模板失败: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
