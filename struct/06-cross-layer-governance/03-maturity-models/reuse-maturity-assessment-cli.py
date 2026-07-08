#!/usr/bin/env python3
"""
复用成熟度可执行评估问卷 CLI

基于 ISO/IEC 26565:2026、RCMM、RiSE、NASA RRL 五级成熟度模型。

用法:
    python reuse-maturity-assessment-cli.py --interactive
    python reuse-maturity-assessment-cli.py --input answers.json --output report.json
    python reuse-maturity-assessment-cli.py --input answers.json --compare baseline.json
"""

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# 五级成熟度（映射 RCMM / RiSE / ISO 26565 / NASA RRL）
LEVELS = {
    1: ("Initial", "初始级", "Ad-hoc 复用，无正式流程"),
    2: ("Managed", "已管理", "项目级复用，有基本管理"),
    3: ("Defined", "已定义", "组织级标准化复用流程"),
    4: ("Quantitatively Managed", "量化管理", "数据驱动的复用度量与管控"),
    5: ("Optimizing", "优化级", "持续改进，创新复用模式"),
}

DIMENSIONS = {
    "strategy": {"name": "战略与治理 (Strategy & Governance)", "weight": 1.0},
    "process": {"name": "流程与方法 (Process & Methodology)", "weight": 1.0},
    "assets": {"name": "资产与基础设施 (Assets & Infrastructure)", "weight": 1.0},
    "measurement": {"name": "度量与改进 (Measurement & Improvement)", "weight": 1.0},
    "people": {"name": "人员与文化 (People & Culture)", "weight": 1.0},
}

# 25 道评估题（每维度 5 题，1-5 李克特量表）
QUESTIONS = [
    {"id": "SG1", "dim": "strategy", "text": "组织是否制定了明确的软件复用战略或路线图？", "levels": {1: "无", 2: "非正式讨论", 3: "部门级战略", 4: "企业级战略", 5: "与业务目标对齐并定期回顾"}},
    {"id": "SG2", "dim": "strategy", "text": "是否为复用活动分配了专门预算？", "levels": {1: "无", 2: "临时预算", 3: "项目级预算", 4: "年度预算", 5: "战略级持续投资"}},
    {"id": "SG3", "dim": "strategy", "text": "是否有专职的复用治理团队或平台工程团队？", "levels": {1: "无", 2: "志愿者/兼职", 3: "小型中心化团队", 4: "专职平台团队", 5: "平台团队与产品团队协同演进"}},
    {"id": "SG4", "dim": "strategy", "text": "复用目标是否纳入组织绩效考核体系？", "levels": {1: "无", 2: "偶尔提及", 3: "部分团队", 4: "多数团队", 5: "全员 KPI 并与激励挂钩"}},
    {"id": "SG5", "dim": "strategy", "text": "高层管理者对复用举措的支持程度如何？", "levels": {1: "无支持", 2: "口头支持", 3: "资源支持", 4: "战略推动", 5: "高管直接参与并公开倡导"}},
    {"id": "PM1", "dim": "process", "text": "是否有标准化的复用决策流程（Make vs Buy vs Reuse）？", "levels": {1: "无", 2: "团队自发", 3: "部门指南", 4: "企业标准", 5: "持续优化并自动化"}},
    {"id": "PM2", "dim": "process", "text": "是否有资产入库、退役与版本治理的流程？", "levels": {1: "无", 2: "非正式", 3: "部门流程", 4: "企业流程", 5: "完全自动化并审计"}},
    {"id": "PM3", "dim": "process", "text": "复用流程是否与软件开发生命周期（SDLC）集成？", "levels": {1: "无集成", 2: "部分工具", 3: "关键节点集成", 4: "主线集成", 5: "全生命周期自动化"}},
    {"id": "PM4", "dim": "process", "text": "是否有跨项目/跨团队的资产协调与冲突解决机制？", "levels": {1: "无", 2: "临时协调", 3: "部门委员会", 4: "企业架构评审", 5: "社区化治理（InnerSource）"}},
    {"id": "PM5", "dim": "process", "text": "复用资产是否经过合规、安全与许可审查？", "levels": {1: "无", 2: "临时审查", 3: "项目级", 4: "企业级", 5: "自动化合规扫描"}},
    {"id": "AI1", "dim": "assets", "text": "是否有统一的复用资产目录或内部开发者平台（IDP）？", "levels": {1: "无", 2: "分散文档", 3: "部门目录", 4: "企业目录", 5: "智能推荐与主动发现"}},
    {"id": "AI2", "dim": "assets", "text": "资产是否附带标准化元数据（所有权、许可证、版本、质量等级）？", "levels": {1: "无", 2: "部分", 3: "关键资产", 4: "大多数资产", 5: "全部资产并自动化生成"}},
    {"id": "AI3", "dim": "assets", "text": "资产的版本控制、变更管理与兼容性追踪成熟度？", "levels": {1: "无版本控制", 2: "部分版本", 3: "标准 Semver", 4: "全生命周期", 5: "自动化版本和兼容性分析"}},
    {"id": "AI4", "dim": "assets", "text": "是否有资产质量门禁（测试覆盖率/安全扫描/文档完整性）？", "levels": {1: "无", 2: "手工检查", 3: "部分自动化", 4: "全自动化", 5: "AI 辅助质量预测"}},
    {"id": "AI5", "dim": "assets", "text": "是否生成并维护软件物料清单（SBOM）以追踪复用组件？", "levels": {1: "无", 2: "部分项目", 3: "关键系统", 4: "标准实践", 5: "全企业并签名/上链"}},
    {"id": "MI1", "dim": "measurement", "text": "是否度量复用率（代码/组件/架构模式级别）？", "levels": {1: "无", 2: "偶尔估算", 3: "项目级", 4: "部门级", 5: "全企业自动化仪表板"}},
    {"id": "MI2", "dim": "measurement", "text": "是否计算复用投资回报率（ROI）或成本节约？", "levels": {1: "无", 2: "定性评估", 3: "项目级计算", 4: "年度计算", 5: "实时 FinOps 分摊"}},
    {"id": "MI3", "dim": "measurement", "text": "是否建立复用成熟度基线并设定改进目标？", "levels": {1: "无", 2: "非正式", 3: "部门目标", 4: "企业目标", 5: "OKR 驱动并季度回顾"}},
    {"id": "MI4", "dim": "measurement", "text": "是否追踪复用资产的采用度、满意度与弃用率？", "levels": {1: "无", 2: "临时反馈", 3: "季度调研", 4: "持续追踪", 5: "NPS + 使用数据 + 自动反馈"}},
    {"id": "MI5", "dim": "measurement", "text": "是否参与行业对标或开源社区以持续改进复用实践？", "levels": {1: "无", 2: "内部分享", 3: "行业报告", 4: "定期对标", 5: "参与开源/标准化社区"}},
    {"id": "PC1", "dim": "people", "text": "开发者对复用的接受度与主动性如何？", "levels": {1: "抵触", 2: "被动", 3: "接受", 4: "积极", 5: "主动贡献并维护"}},
    {"id": "PC2", "dim": "people", "text": "是否有定期的复用知识分享或社区活动？", "levels": {1: "无", 2: "偶尔", 3: "定期", 4: "制度化", 5: "社区化 + 内部大使"}},
    {"id": "PC3", "dim": "people", "text": "是否表彰或奖励复用贡献者（代码/组件/文档）？", "levels": {1: "无", 2: "非正式", 3: "团队内", 4: "公司级", 5: "晋升/奖励挂钩"}},
    {"id": "PC4", "dim": "people", "text": "新员工是否接受复用相关的培训（平台使用、资产检索）？", "levels": {1: "无", 2: "按需", 3: "入职提及", 4: "必修模块", 5: "持续学习路径"}},
    {"id": "PC5", "dim": "people", "text": "跨团队协作复用的顺畅度与信任水平？", "levels": {1: "困难", 2: "偶尔", 3: "项目驱动", 4: "平台驱动", 5: "社区自组织"}},
]

# 改进建议：维度 -> (建议目标等级, 建议文本)
IMPROVEMENTS = {
    "strategy": [(2, "制定部门级复用战略，明确责任人与初步预算。"), (3, "将复用战略上升为企业级，建立治理委员会。"), (4, "将复用目标纳入绩效考核，定期回顾战略执行情况。"), (5, "持续优化战略，与业务目标深度对齐，探索创新复用模式。")],
    "process": [(2, "建立基本的复用决策指南和资产登记流程。"), (3, "标准化复用流程，与 SDLC 关键节点集成。"), (4, "实现跨项目资产协调，建立企业级架构评审机制。"), (5, "推动社区化治理（InnerSource），自动化合规与审计。")],
    "assets": [(2, "建立分散的资产文档库，统一基本元数据格式。"), (3, "部署部门级资产目录，实施 Semver 版本控制。"), (4, "建设企业级 IDP，实现全自动化质量门禁。"), (5, "引入智能推荐、SBOM 全链路追踪与供应链安全。")],
    "measurement": [(2, "开始定性评估复用收益，建立基本度量指标。"), (3, "在项目级计算复用率与 ROI，设定部门改进目标。"), (4, "构建自动化仪表板，持续追踪资产采用度与满意度。"), (5, "参与行业对标，将复用度量融入 FinOps 与 OKR 体系。")],
    "people": [(2, "组织非正式知识分享，提升开发者复用意识。"), (3, "建立定期分享机制，将复用培训纳入入职流程。"), (4, "设立公司级表彰体系，培养内部复用大使。"), (5, "构建自组织社区，将复用贡献与职业发展挂钩。")],
}


def score_to_level(avg: float) -> int:
    """将平均分映射到五级成熟度（RCMM / RiSE / ISO 26565 兼容）。"""
    if avg < 1.5:
        return 1
    elif avg < 2.5:
        return 2
    elif avg < 3.5:
        return 3
    elif avg < 4.5:
        return 4
    return 5


def level_to_rcmm(level: int) -> str:
    """映射到 RCMM 等级名称。"""
    return ["", "Basic", "Initial", "Intermediate", "Advanced", "Optimized"][level]


def level_to_rise(level: int) -> str:
    """映射到 RiSE 等级名称。"""
    return ["", "Ad-hoc", "Managed", "Defined", "Quantitatively Managed", "Optimizing"][level]


def ask_interactive() -> Dict[str, List[int]]:
    """交互式提问并收集答案。"""
    print("=" * 72)
    print("  软件复用成熟度可执行评估问卷")
    print("  基于 ISO/IEC 26565:2026 / RCMM / RiSE / NASA RRL")
    print("=" * 72)
    print("请为每道题选择 1-5 分（1=最低，5=最高），直接回车默认 3 分。\n")
    answers: Dict[str, List[int]] = {dim: [] for dim in DIMENSIONS}
    current_dim = None
    for q in QUESTIONS:
        if q["dim"] != current_dim:
            current_dim = q["dim"]
            print(f"\n【{DIMENSIONS[current_dim]['name']}】")
            print("-" * 72)
        print(f"\n{q['id']}. {q['text']}")
        for lv, desc in q["levels"].items():
            print(f"   {lv}: {desc}")
        while True:
            raw = input("   评分 (1-5) [3]: ").strip()
            if raw == "":
                score = 3
                break
            try:
                score = int(raw)
                if 1 <= score <= 5:
                    break
                print("   请输入 1-5 之间的整数。")
            except ValueError:
                print("   无效输入，请输入整数。")
        answers[current_dim].append(score)
    return answers


def load_answers(path: str) -> Dict[str, List[int]]:
    """从 JSON 文件加载答案（支持题目 ID 映射或维度分数列表）。"""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
        if set(data.keys()).issubset(set(DIMENSIONS.keys())):
            return {k: [int(x) for x in v] for k, v in data.items()}
    answers: Dict[str, List[int]] = {dim: [] for dim in DIMENSIONS}
    id_to_dim = {q["id"]: q["dim"] for q in QUESTIONS}
    for qid, score in data.items():
        if qid in id_to_dim:
            answers[id_to_dim[qid]].append(int(score))
    return answers


def compute_results(answers: Dict[str, List[int]]) -> Tuple[Dict, float, int]:
    """计算各维度得分和总体成熟度。"""
    dim_results = {}
    total_weighted = 0.0
    total_weight = 0.0
    for dim, scores in answers.items():
        if not scores:
            continue
        avg = sum(scores) / len(scores)
        level = score_to_level(avg)
        weight = DIMENSIONS[dim]["weight"]
        dim_results[dim] = {
            "name": DIMENSIONS[dim]["name"],
            "average_score": round(avg, 2),
            "level": level,
            "level_name": LEVELS[level][0],
            "level_name_cn": LEVELS[level][1],
            "scores": scores,
        }
        total_weighted += avg * weight
        total_weight += weight
    overall_avg = total_weighted / total_weight if total_weight > 0 else 0
    overall_level = score_to_level(overall_avg)
    return dim_results, overall_avg, overall_level


def get_recommendations(dim_results: Dict) -> List[Dict]:
    """基于低分维度生成改进建议。"""
    recs = []
    for dim_key, info in sorted(dim_results.items(), key=lambda x: x[1]["average_score"]):
        level = info["level"]
        text = ""
        for thresh, sug in IMPROVEMENTS.get(dim_key, []):
            if level <= thresh:
                text = sug
                break
        if not text and IMPROVEMENTS.get(dim_key):
            text = IMPROVEMENTS[dim_key][-1][1]
        recs.append({"dimension": info["name"], "score": info["average_score"], "level": level, "suggestion": text})
    return recs


def print_bar_chart(dim_results: Dict):
    """打印简单 ASCII 条形图。"""
    print("\n" + "=" * 72)
    print("  成熟度维度评分条形图")
    print("=" * 72)
    for dim in DIMENSIONS:
        info = dim_results.get(dim, {"average_score": 0, "level": 1})
        score = info["average_score"]
        bar_len = int(round(score))
        bar = "█" * bar_len + "░" * (5 - bar_len)
        name = DIMENSIONS[dim]["name"].split("(")[0].strip()
        print(f"  {name:24s} [{bar}] {score:.1f}  L{info['level']}")


def print_radar_ascii(dim_results: Dict):
    """打印 ASCII 雷达图（简化五角形）。"""
    print("\n" + "=" * 72)
    print("  成熟度雷达图（ASCII）")
    print("=" * 72)
    dims = list(DIMENSIONS.keys())
    n = len(dims)
    size = 5
    grid = [["  " for _ in range(2 * size + 1)] for _ in range(2 * size + 1)]
    cx, cy = size, size
    for r in range(1, size + 1):
        for i in range(n):
            a1 = 2 * math.pi * i / n - math.pi / 2
            a2 = 2 * math.pi * ((i + 1) % n) / n - math.pi / 2
            x1 = int(round(cx + r * math.cos(a1) * size / size))
            y1 = int(round(cy + r * math.sin(a1) * size / size))
            if 0 <= x1 <= 2 * size and 0 <= y1 <= 2 * size:
                grid[y1][x1] = "· "
    for i, dim in enumerate(dims):
        angle = 2 * math.pi * i / n - math.pi / 2
        score = dim_results.get(dim, {"average_score": 0})["average_score"]
        for r in range(1, size + 1):
            x = int(round(cx + r * math.cos(angle)))
            y = int(round(cy + r * math.sin(angle)))
            if 0 <= x <= 2 * size and 0 <= y <= 2 * size:
                if r == size:
                    grid[y][x] = dim[:2].upper()
                else:
                    grid[y][x] = "· "
        sx = int(round(cx + score * math.cos(angle)))
        sy = int(round(cy + score * math.sin(angle)))
        if 0 <= sx <= 2 * size and 0 <= sy <= 2 * size:
            grid[sy][sx] = "● "
    for row in grid:
        print("  " + "".join(row))
    labels = "  ".join([f"{d.upper()}={DIMENSIONS[d]['name'].split('(')[0].strip()}" for d in dims])
    print(f"  图例: ●=当前得分  ·=网格  {labels}")


def print_report(dim_results: Dict, overall_avg: float, overall_level: int):
    """打印终端文本报告。"""
    print("\n" + "=" * 72)
    print("  评估结果")
    print("=" * 72)
    lv = LEVELS[overall_level]
    print(f"  总体平均分: {overall_avg:.2f} / 5.00")
    print(f"  总体成熟度: Level {overall_level} — {lv[0]} ({lv[1]})")
    print(f"  等级描述: {lv[2]}")
    print(f"  标准映射: RCMM={level_to_rcmm(overall_level)}, RiSE={level_to_rise(overall_level)}")
    print("\n  各维度详情:")
    for dim, info in dim_results.items():
        print(f"    • {info['name']}: {info['average_score']:.2f} → Level {info['level']} ({info['level_name_cn']})")
    print("\n  改进建议（按优先级排序）:")
    for idx, rec in enumerate(get_recommendations(dim_results)[:3], 1):
        print(f"    {idx}. [{rec['dimension']}] (得分 {rec['score']:.2f})")
        print(f"       → {rec['suggestion']}")


def compare_with_baseline(dim_results: Dict, baseline_path: str) -> Dict:
    """与基线报告对比，输出差异分析。"""
    with open(baseline_path, "r", encoding="utf-8") as f:
        baseline = json.load(f)
    baseline_dims = baseline.get("dimensions", {})
    comparison = {}
    for dim, info in dim_results.items():
        b_info = baseline_dims.get(dim, {})
        b_score = b_info.get("average_score", 0)
        comparison[dim] = {
            "current_score": info["average_score"],
            "baseline_score": b_score,
            "delta": round(info["average_score"] - b_score, 2),
            "current_level": info["level"],
            "baseline_level": b_info.get("level", 1),
        }
    return comparison


def print_comparison(comparison: Dict):
    """打印与基线的对比结果。"""
    print("\n" + "=" * 72)
    print("  与基线对比分析")
    print("=" * 72)
    for dim, comp in comparison.items():
        name = DIMENSIONS[dim]["name"].split("(")[0].strip()
        delta = comp["delta"]
        symbol = "▲" if delta > 0 else ("▼" if delta < 0 else "-")
        print(f"  {name:24s} 当前 {comp['current_score']:.2f} | 基线 {comp['baseline_score']:.2f} | {symbol} {delta:+.2f} | L{comp['current_level']} ← L{comp['baseline_level']}")


def build_report(answers, dim_results, overall_avg, overall_level, comparison=None) -> Dict:
    """构建结构化报告字典。"""
    report = {
        "framework": "ISO/IEC 26565:2026 / RCMM / RiSE / NASA RRL",
        "overall_score": round(overall_avg, 2),
        "overall_level": overall_level,
        "overall_level_name": LEVELS[overall_level][0],
        "overall_level_name_cn": LEVELS[overall_level][1],
        "overall_description": LEVELS[overall_level][2],
        "standard_mappings": {"RCMM": level_to_rcmm(overall_level), "RiSE": level_to_rise(overall_level), "NASA_RRL": overall_level},
        "dimensions": dim_results,
        "recommendations": get_recommendations(dim_results),
    }
    if comparison is not None:
        report["baseline_comparison"] = comparison
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="复用成熟度可执行评估问卷 CLI（ISO/IEC 26565:2026 / RCMM / RiSE / NASA RRL）")
    parser.add_argument("--interactive", action="store_true", help="交互式问答模式")
    parser.add_argument("--input", dest="input_file", type=str, help="从 JSON 文件读取答案")
    parser.add_argument("--output", type=str, help="输出结构化报告 JSON 文件路径")
    parser.add_argument("--compare", type=str, help="与基线报告 JSON 对比")
    parser.add_argument("--demo", action="store_true", help="使用演示数据运行")
    args = parser.parse_args()

    if args.demo:
        answers = {"strategy": [3, 3, 2, 2, 3], "process": [3, 3, 3, 2, 2], "assets": [3, 3, 4, 3, 2], "measurement": [2, 2, 3, 3, 2], "people": [3, 3, 2, 2, 3]}
        print("[演示模式] 使用示例数据运行评估\n")
    elif args.input_file:
        answers = load_answers(args.input_file)
    elif args.interactive or not any([args.input_file, args.demo]):
        answers = ask_interactive()
    else:
        parser.print_help()
        return 1

    dim_results, overall_avg, overall_level = compute_results(answers)
    print_bar_chart(dim_results)
    print_radar_ascii(dim_results)
    print_report(dim_results, overall_avg, overall_level)

    comparison = None
    if args.compare:
        comparison = compare_with_baseline(dim_results, args.compare)
        print_comparison(comparison)

    report = build_report(answers, dim_results, overall_avg, overall_level, comparison)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n  报告已保存到: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
