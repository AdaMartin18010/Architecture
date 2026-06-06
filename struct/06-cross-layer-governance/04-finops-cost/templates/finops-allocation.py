#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FinOps 跨层成本分摊计算器
对齐：FinOps Foundation Framework 2025、FOCUS 1.0、Allocation Accuracy Index

层模型：Business -> Application -> Component -> Function
方法：direct / proportional / step_down / equal
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass, field, asdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from typing import Dict, List, Optional

try:
    import xlsxwriter
    HAS_XLSX = True
except ImportError:
    HAS_XLSX = False


@dataclass
class CostLine:
    line_id: str
    provider: str  # aws, azure, gcp, saas, ai, onprem
    resource_id: str
    effective_cost: Decimal  # FOCUS 风格标准化成本
    tags: Dict[str, str] = field(default_factory=dict)
    usage_quantity: Decimal = Decimal("0")
    usage_unit: str = ""


@dataclass
class AllocationRule:
    rule_id: str
    cost_pool: str
    method: str  # direct | proportional | step_down | equal | fixed
    driver: Optional[str] = None
    consumers: List[str] = field(default_factory=list)
    fixed_shares: Optional[Dict[str, Decimal]] = None


@dataclass
class LayerNode:
    node_id: str
    layer: str  # business | application | component | function
    parent_id: Optional[str] = None
    direct_cost: Decimal = Decimal("0")
    inherited_cost: Decimal = Decimal("0")
    children_ids: List[str] = field(default_factory=list)
    driver: Decimal = Decimal("0")  # 用于本层向下分摊的驱动量

    @property
    def total_cost(self) -> Decimal:
        return (self.direct_cost + self.inherited_cost).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )


def d(value: str | float | int | Decimal) -> Decimal:
    return Decimal(str(value))


def fmt_currency(v: Decimal) -> str:
    return f"{v.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"


# ---------------------------------------------------------------------------
# 分配引擎
# ---------------------------------------------------------------------------

def allocate_direct(lines: List[CostLine], tag_key: str = "cost_center") -> Dict[str, Decimal]:
    """直接分配：按标签中的 owner 直接归属。"""
    result: Dict[str, Decimal] = {"unallocated": Decimal("0")}
    for line in lines:
        owner = line.tags.get(tag_key) or "unallocated"
        result[owner] = result.get(owner, Decimal("0")) + line.effective_cost
    return result


def allocate_proportional(
    pool_cost: Decimal,
    driver_values: Dict[str, Decimal]
) -> Dict[str, Decimal]:
    """比例分配：按驱动量比例拆分共享成本池。"""
    total = sum(driver_values.values())
    if total == 0:
        return {k: Decimal("0") for k in driver_values}
    return {
        k: (pool_cost * v / total).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        for k, v in driver_values.items()
    }


def allocate_step_down(
    support_depts: List[tuple[str, Decimal, Dict[str, Decimal]]]
) -> Dict[str, Decimal]:
    """
    阶梯式分配：按支持部门顺序依次向下分摊。
    support_depts: [(dept_id, direct_cost, {consumer: driver}), ...]
    """
    accumulated: Dict[str, Decimal] = {}
    for dept_id, direct_cost, consumers in support_depts:
        total_driver = sum(consumers.values())
        if total_driver == 0:
            continue
        for consumer, driver in consumers.items():
            allocated = (direct_cost * driver / total_driver).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
            accumulated[consumer] = accumulated.get(consumer, Decimal("0")) + allocated
    return accumulated


def calculate_aai(directly_attributed: Decimal, total: Decimal) -> Decimal:
    if total == 0:
        return Decimal("0")
    return (directly_attributed / total * 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# ---------------------------------------------------------------------------
# 跨层分摊树
# ---------------------------------------------------------------------------

class LayeredCostModel:
    def __init__(self):
        self.nodes: Dict[str, LayerNode] = {}

    def add_node(self, node: LayerNode) -> None:
        self.nodes[node.node_id] = node
        if node.parent_id and node.parent_id in self.nodes:
            self.nodes[node.parent_id].children_ids.append(node.node_id)

    def rollup(self, driver_map: Dict[str, Decimal]) -> None:
        """自顶向下按 driver_map 分摊成本。"""
        roots = [n for n in self.nodes.values() if n.parent_id is None]
        for root in roots:
            self._distribute(root.node_id, driver_map)

    def _distribute(self, node_id: str, driver_map: Dict[str, Decimal]) -> Decimal:
        node = self.nodes[node_id]
        children = [self.nodes[cid] for cid in node.children_ids]
        if not children:
            return node.total_cost

        total_driver = sum(driver_map.get(c.node_id, Decimal("0")) for c in children)
        if total_driver > 0:
            for child in children:
                share = driver_map.get(child.node_id, Decimal("0")) / total_driver
                child.inherited_cost += (node.total_cost * share).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )

        child_total = Decimal("0")
        for child in children:
            child_total += self._distribute(child.node_id, driver_map)

        return node.total_cost + child_total

    def report(self) -> Dict[str, Dict[str, str]]:
        return {
            nid: {
                "layer": n.layer,
                "parent_id": n.parent_id or "",
                "direct_cost": fmt_currency(n.direct_cost),
                "inherited_cost": fmt_currency(n.inherited_cost),
                "total_cost": fmt_currency(n.total_cost),
            }
            for nid, n in self.nodes.items()
        }


# ---------------------------------------------------------------------------
# I/O 与 CLI
# ---------------------------------------------------------------------------

def load_cost_lines_csv(path: Path) -> List[CostLine]:
    lines: List[CostLine] = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tags = {}
            for k, v in row.items():
                if k.startswith("tag_"):
                    tags[k[4:]] = v
            lines.append(CostLine(
                line_id=row["line_id"],
                provider=row["provider"],
                resource_id=row["resource_id"],
                effective_cost=d(row["effective_cost"]),
                tags=tags,
                usage_quantity=d(row.get("usage_quantity", "0") or "0"),
                usage_unit=row.get("usage_unit", ""),
            ))
    return lines


def demo_data() -> List[CostLine]:
    return [
        CostLine("L1", "aws", "ec2-app-a", d("5000.00"),
                 {"business_unit": "BU1", "app": "AppA", "env": "prod"}, d("720"), "hrs"),
        CostLine("L2", "aws", "ec2-app-b", d("3000.00"),
                 {"business_unit": "BU1", "app": "AppB", "env": "prod"}, d("360"), "hrs"),
        CostLine("L3", "aws", "eks-control-plane", d("800.00"),
                 {"business_unit": "shared", "app": "platform", "env": "prod"}, d("1"), "cluster"),
        CostLine("L4", "azure", "openai-inference", d("2400.00"),
                 {"business_unit": "BU1", "app": "AppA", "feature": "chatbot"},
                 d("12000000"), "tokens"),
        CostLine("L5", "saas", "datadog", d("1200.00"),
                 {"business_unit": "shared", "app": "observability"}, d("1"), "subscription"),
    ]


def run_demo():
    lines = demo_data()
    direct = allocate_direct(lines, tag_key="business_unit")

    total = sum(line.effective_cost for line in lines)
    attributed = sum(v for k, v in direct.items() if k != "unallocated")
    aai = calculate_aai(attributed, total)

    print("=" * 60)
    print("FinOps 跨层成本分摊报告（DEMO）")
    print("=" * 60)
    print(f"\n总成本: {fmt_currency(total)}")
    print(f"直接归属成本: {fmt_currency(attributed)}")
    print(f"未分配成本: {fmt_currency(direct.get('unallocated', Decimal('0')))}")
    print(f"分配准确率指数 (AAI): {aai}%")

    print("\n-- 按 Business Unit 直接分配 --")
    for owner, cost in sorted(direct.items(), key=lambda x: -x[1]):
        print(f"  {owner}: {fmt_currency(cost)}")

    # 共享平台按比例分摊
    print("\n-- 共享平台成本按比例（compute hours）分摊到 App --")
    shared = [l for l in lines if l.tags.get("business_unit") == "shared"]
    shared_total = sum(l.effective_cost for l in shared)
    app_drivers = {
        "AppA": d("720"),
        "AppB": d("360"),
    }
    app_alloc = allocate_proportional(shared_total, app_drivers)
    for app, cost in sorted(app_alloc.items(), key=lambda x: -x[1]):
        print(f"  {app}: {fmt_currency(cost)}")

    # 跨层树
    print("\n-- 跨层成本树（Business -> Application -> Component） --")
    tree = LayeredCostModel()
    tree.add_node(LayerNode("BU1", "business", None, direct.get("BU1", Decimal("0"))))
    tree.add_node(LayerNode("AppA", "application", "BU1", d("5000.00") + d("2400.00")))
    tree.add_node(LayerNode("AppB", "application", "BU1", d("3000.00")))
    tree.add_node(LayerNode("SharedPlatform", "component", "BU1", shared_total))
    tree.add_node(LayerNode("CompA1", "component", "AppA", Decimal("0")))
    tree.add_node(LayerNode("CompA2", "component", "AppA", Decimal("0")))
    tree.add_node(LayerNode("CompB1", "component", "AppB", Decimal("0")))

    driver_map = {
        "AppA": d("720"),
        "AppB": d("360"),
        "SharedPlatform": d("1"),
        "CompA1": d("600"),
        "CompA2": d("120"),
        "CompB1": d("360"),
    }
    tree.rollup(driver_map)

    for nid, n in sorted(tree.nodes.items()):
        indent = "  " * ({"business": 0, "application": 1, "component": 2, "function": 3}[n.layer])
        print(f"{indent}{nid} [{n.layer}] direct={fmt_currency(n.direct_cost)} inherited={fmt_currency(n.inherited_cost)} total={fmt_currency(n.total_cost)}")

    # 复用节省估算
    print("\n-- 复用节省估算 --")
    duplicate_cost = d("3000")  # 假设不共享时每个 App 都需重复建设
    shared_cost = shared_total
    consumers = 2
    savings = (duplicate_cost * consumers) - shared_cost
    print(f"  重复建设成本: {fmt_currency(duplicate_cost)} x {consumers} = {fmt_currency(duplicate_cost * consumers)}")
    print(f"  共享平台成本: {fmt_currency(shared_cost)}")
    print(f"  估算节省: {fmt_currency(savings)}")


def write_excel_report(path: Path, lines: List[CostLine], direct: Dict[str, Decimal], report: Dict) -> None:
    """将成本报告写入 Excel（含公式）。"""
    workbook = xlsxwriter.Workbook(str(path))

    # 摘要页
    ws_summary = workbook.add_worksheet("摘要")
    bold = workbook.add_format({"bold": True})
    num_fmt = workbook.add_format({"num_format": "#,##0.00"})
    ws_summary.write_row(0, 0, ["指标", "值"], bold)
    ws_summary.write_row(1, 0, ["总成本", float(report["total_cost"])], num_fmt)
    ws_summary.write_row(2, 0, ["直接归属成本", float(report["attributed_cost"])], num_fmt)
    ws_summary.write_row(3, 0, ["未分配成本", float(report["unallocated_cost"])], num_fmt)
    ws_summary.write_row(4, 0, ["AAI (%)", float(report["aai"])])

    # 直接分配页
    ws_alloc = workbook.add_worksheet("直接分配")
    ws_alloc.write_row(0, 0, ["Owner", "成本"], bold)
    for i, (owner, cost) in enumerate(sorted(direct.items(), key=lambda x: -x[1]), start=1):
        ws_alloc.write_row(i, 0, [owner, float(cost)], num_fmt)

    # 明细页
    ws_detail = workbook.add_worksheet("账单明细")
    ws_detail.write_row(0, 0, ["line_id", "provider", "resource_id", "effective_cost", "usage_quantity", "usage_unit", "tags"], bold)
    for i, line in enumerate(lines, start=1):
        ws_detail.write_row(i, 0, [
            line.line_id,
            line.provider,
            line.resource_id,
            float(line.effective_cost),
            float(line.usage_quantity),
            line.usage_unit,
            json.dumps(line.tags, ensure_ascii=False)
        ])

    workbook.close()


def main():
    parser = argparse.ArgumentParser(description="FinOps 跨层成本分摊计算器")
    parser.add_argument("--demo", action="store_true", help="运行演示数据")
    parser.add_argument("--csv", type=Path, help="加载 FOCUS 风格 CSV 账单")
    parser.add_argument("--tag-key", default="cost_center", help="直接分配使用的标签键（默认: cost_center）")
    parser.add_argument("--output-json", type=Path, help="输出 JSON 报告")
    parser.add_argument("--output-excel", type=Path, help="输出 Excel 报告（需安装 xlsxwriter）")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    if args.csv:
        lines = load_cost_lines_csv(args.csv)
        direct = allocate_direct(lines, tag_key=args.tag_key)
        total = sum((l.effective_cost for l in lines), Decimal("0"))
        attributed = sum((v for k, v in direct.items() if k != "unallocated"), Decimal("0"))
        report = {
            "total_cost": fmt_currency(total),
            "attributed_cost": fmt_currency(attributed),
            "unallocated_cost": fmt_currency(direct.get("unallocated", Decimal("0"))),
            "aai": str(calculate_aai(attributed, total)),
            "direct_allocation": {k: fmt_currency(v) for k, v in direct.items()},
        }
        if args.output_json:
            with args.output_json.open("w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"报告已写入 {args.output_json}")
        if args.output_excel:
            if not HAS_XLSX:
                print("错误: 未安装 xlsxwriter，请运行 pip install xlsxwriter")
                sys.exit(1)
            write_excel_report(args.output_excel, lines, direct, report)
            print(f"Excel 报告已写入 {args.output_excel}")
        if not args.output_json and not args.output_excel:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
