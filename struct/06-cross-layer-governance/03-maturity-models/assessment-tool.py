#!/usr/bin/env python3
"""
复用成熟度评估问卷 CLI 工具

用途：
    基于 ISO/IEC 26565:2026、RCMM、RiSE、NASA RRL 五级成熟度模型，
    通过交互式问卷评估组织的软件复用成熟度，并生成雷达图和报告。

按 SUBSEQUENT_PLAN_2026.md 决策 3A 开发：Python CLI 快速原型

用法:
    python assessment-tool.py
    python assessment-tool.py --json-input answers.json
    python assessment-tool.py --demo

权威来源:
    - ISO/IEC 26565:2026 (2026-05 正式发布)
      https://www.iso.org/standard/81436.html
    - NASA RRL (Reuse Readiness Levels)
      https://www.nasa.gov
    - RiSE Reuse Maturity Model
    - RCMM (Reuse Capability Maturity Model)
"""

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# 五级成熟度定义
LEVELS = {
    1: "Initial（初始）",
    2: "Managed（已管理）",
    3: "Defined（已定义）",
    4: "Quantitatively Managed（量化管理）",
    5: "Optimizing（优化中）",
}

# 五个评估维度（对应 CNCF Platform Engineering Maturity Model 五维度 + 复用专用）
DIMENSIONS = {
    "strategy": {
        "name": "复用战略与投资",
        "description": "组织是否有明确的复用战略、预算和专职团队",
        "weight": 1.0,
    },
    "process": {
        "name": "复用过程与治理",
        "description": "是否有标准化的复用流程、治理机制和决策框架",
        "weight": 1.0,
    },
    "assets": {
        "name": "资产管理与目录",
        "description": "复用资产的存储、分类、检索、版本控制和质量管理",
        "weight": 1.0,
    },
    "measurement": {
        "name": "度量与价值量化",
        "description": "是否有复用 ROI、成本分摊、成熟度度量和持续改进",
        "weight": 1.0,
    },
    "technology": {
        "name": "技术基础设施",
        "description": "IDP、包管理器、SBOM、SLSA、MCP 等技术支撑",
        "weight": 1.0,
    },
    "culture": {
        "name": "组织文化与采纳",
        "description": "开发者对复用的接受度、激励机制和知识共享",
        "weight": 1.0,
    },
}

# 问卷题目：每个维度 5 题，每题 1-5 分
QUESTIONS = [
    # strategy
    {"id": "S1", "dimension": "strategy", "text": "组织是否有书面的复用战略或路线图？", "levels": {
        1: "没有", 2: "非正式讨论", 3: "部门级战略", 4: "企业级战略", 5: "战略与业务目标对齐并定期回顾"
    }},
    {"id": "S2", "dimension": "strategy", "text": "是否为复用活动分配了专门预算？", "levels": {
        1: "没有", 2: "临时预算", 3: "项目级预算", 4: "年度预算", 5: "战略级持续投资"
    }},
    {"id": "S3", "dimension": "strategy", "text": "是否有专职的复用/平台工程团队？", "levels": {
        1: "没有", 2: "志愿者/兼职", 3: "小型中心化团队", 4: "专职平台团队", 5: "平台团队与产品团队协同演进"
    }},
    {"id": "S4", "dimension": "strategy", "text": "复用目标是否纳入绩效考核？", "levels": {
        1: "没有", 2: "偶尔提及", 3: "部分团队", 4: "多数团队", 5: "全员 KPI 并与激励挂钩"
    }},
    {"id": "S5", "dimension": "strategy", "text": "高层对复用的支持程度？", "levels": {
        1: "无支持", 2: "口头支持", 3: "资源支持", 4: "战略推动", 5: "高管直接参与并公开倡导"
    }},

    # process
    {"id": "P1", "dimension": "process", "text": "是否有标准化的复用决策流程？", "levels": {
        1: "没有", 2: "团队自发", 3: "部门指南", 4: "企业标准", 5: "持续优化并自动化"
    }},
    {"id": "P2", "dimension": "process", "text": "是否有资产入库/退役的治理流程？", "levels": {
        1: "没有", 2: "非正式", 3: "部门流程", 4: "企业流程", 5: "完全自动化并审计"
    }},
    {"id": "P3", "dimension": "process", "text": "复用流程是否与 SDLC/CI/CD 集成？", "levels": {
        1: "无集成", 2: "部分工具", 3: "关键节点集成", 4: "主线集成", 5: "全生命周期自动化"
    }},
    {"id": "P4", "dimension": "process", "text": "是否有跨项目资产协调机制？", "levels": {
        1: "没有", 2: "临时协调", 3: "部门委员会", 4: "企业架构评审", 5: "社区化治理（InnerSource）"
    }},
    {"id": "P5", "dimension": "process", "text": "是否有复用相关的风险/合规审查？", "levels": {
        1: "没有", 2: "临时审查", 3: "项目级", 4: "企业级", 5: "自动化合规扫描"
    }},

    # assets
    {"id": "A1", "dimension": "assets", "text": "是否有统一的资产目录或 IDP？", "levels": {
        1: "没有", 2: "分散文档", 3: "部门目录", 4: "企业目录", 5: "智能推荐与主动发现"
    }},
    {"id": "A2", "dimension": "assets", "text": "资产是否有标准化元数据（所有权、许可证、版本）？", "levels": {
        1: "没有", 2: "部分", 3: "关键资产", 4: "大多数资产", 5: "全部资产并自动化生成"
    }},
    {"id": "A3", "dimension": "assets", "text": "资产的版本控制和变更管理？", "levels": {
        1: "无版本控制", 2: "部分版本", 3: "标准 Semver", 4: "全生命周期", 5: "自动化版本和兼容性分析"
    }},
    {"id": "A4", "dimension": "assets", "text": "是否有资产质量门禁（测试/安全/文档）？", "levels": {
        1: "没有", 2: "手工检查", 3: "部分自动化", 4: "全自动化", 5: "AI 辅助质量预测"
    }},
    {"id": "A5", "dimension": "assets", "text": "是否生成并维护 SBOM？", "levels": {
        1: "没有", 2: "部分项目", 3: "关键系统", 4: "标准实践", 5: "全企业并上链/签名"
    }},

    # measurement
    {"id": "M1", "dimension": "measurement", "text": "是否度量复用率（代码/组件/功能级别）？", "levels": {
        1: "没有", 2: "偶尔估算", 3: "项目级", 4: "部门级", 5: "全企业自动化仪表板"
    }},
    {"id": "M2", "dimension": "measurement", "text": "是否计算复用 ROI 或成本节约？", "levels": {
        1: "没有", 2: "定性评估", 3: "项目级计算", 4: "年度计算", 5: "实时 FinOps 分摊"
    }},
    {"id": "M3", "dimension": "measurement", "text": "是否有复用成熟度基线和改进目标？", "levels": {
        1: "没有", 2: "非正式", 3: "部门目标", 4: "企业目标", 5: "OKR 驱动并季度回顾"
    }},
    {"id": "M4", "dimension": "measurement", "text": "是否追踪复用资产的采用度和满意度？", "levels": {
        1: "没有", 2: "临时反馈", 3: "季度调研", 4: "持续追踪", 5: "NPS + 使用数据 + 自动反馈"
    }},
    {"id": "M5", "dimension": "measurement", "text": "是否有复用相关的外部对标或基准？", "levels": {
        1: "没有", 2: "内部分享", 3: "行业报告", 4: "定期对标", 5: "参与开源/标准化社区"
    }},

    # technology
    {"id": "T1", "dimension": "technology", "text": "是否有内部开发者平台（IDP）支持复用？", "levels": {
        1: "没有", 2: "文档门户", 3: "模板库", 4: "自助式 IDP", 5: "Golden Path + 自动化治理"
    }},
    {"id": "T2", "dimension": "technology", "text": "包管理器和组件仓库的成熟度？", "levels": {
        1: "外部公共仓库", 2: "私有镜像", 3: "受管仓库", 4: "企业 artifact 管理", 5: "全球联邦 + 供应链安全"
    }},
    {"id": "T3", "dimension": "technology", "text": "是否有供应链安全工具（SLSA/SBOM/签名）？", "levels": {
        1: "没有", 2: "部分扫描", 3: "关键项目", 4: "标准实践", 5: "SLSA L3+ 全面覆盖"
    }},
    {"id": "T4", "dimension": "technology", "text": "是否支持 AI 原生复用协议（MCP/A2A）？", "levels": {
        1: "没有", 2: "调研中", 3: "试点项目", 4: "部分采用", 5: "企业级 MCP/A2A 注册表"
    }},
    {"id": "T5", "dimension": "technology", "text": "形式化验证或架构约束工具的应用？", "levels": {
        1: "没有", 2: "研究阶段", 3: "关键组件", 4: "多个项目", 5: "CI/CD 集成自动化验证"
    }},

    # culture
    {"id": "C1", "dimension": "culture", "text": "开发者对复用的接受度和主动性？", "levels": {
        1: "抵触", 2: "被动", 3: "接受", 4: "积极", 5: "主动贡献并维护"
    }},
    {"id": "C2", "dimension": "culture", "text": "是否有复用知识分享机制？", "levels": {
        1: "没有", 2: "偶尔", 3: "定期", 4: "制度化", 5: "社区化 + 内部大使"
    }},
    {"id": "C3", "dimension": "culture", "text": "是否表彰复用贡献者？", "levels": {
        1: "没有", 2: "非正式", 3: "团队内", 4: "公司级", 5: "晋升/奖励挂钩"
    }},
    {"id": "C4", "dimension": "culture", "text": "新员工是否接受复用培训？", "levels": {
        1: "没有", 2: "按需", 3: "入职提及", 4: "必修模块", 5: "持续学习路径"
    }},
    {"id": "C5", "dimension": "culture", "text": "跨团队协作复用的顺畅度？", "levels": {
        1: "困难", 2: "偶尔", 3: "项目驱动", 4: "平台驱动", 5: "社区自组织"
    }},
]


def score_to_level(avg_score: float) -> int:
    """将平均分映射到五级成熟度。"""
    if avg_score < 1.5:
        return 1
    elif avg_score < 2.5:
        return 2
    elif avg_score < 3.5:
        return 3
    elif avg_score < 4.5:
        return 4
    else:
        return 5


def ask_questions_interactive() -> Dict[str, List[int]]:
    """交互式提问并收集答案。"""
    print("=" * 70)
    print("软件复用成熟度评估问卷")
    print("基于 ISO/IEC 26565:2026 / RCMM / RiSE / NASA RRL")
    print("=" * 70)
    print("请为每道题选择 1-5 分（1=最低，5=最高），直接按回车默认 3 分。\n")

    answers: Dict[str, List[int]] = {dim: [] for dim in DIMENSIONS}

    current_dim = None
    for q in QUESTIONS:
        if q["dimension"] != current_dim:
            current_dim = q["dimension"]
            dim_info = DIMENSIONS[current_dim]
            print(f"\n【{dim_info['name']}】{dim_info['description']}")
            print("-" * 70)

        print(f"\n{q['id']}. {q['text']}")
        for level, desc in q["levels"].items():
            print(f"   {level}: {desc}")

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


def load_answers_from_json(path: str) -> Dict[str, List[int]]:
    """从 JSON 文件加载答案。"""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 支持两种格式：按题目 ID 映射，或按维度直接给分数列表
    if isinstance(data, dict) and all(isinstance(v, list) for v in data.values()):
        # 检查键是否是维度名
        if set(data.keys()).issubset(set(DIMENSIONS.keys())):
            return data

    # 否则假设是题目 ID -> 分数
    answers: Dict[str, List[int]] = {dim: [] for dim in DIMENSIONS}
    id_to_dim = {q["id"]: q["dimension"] for q in QUESTIONS}
    for qid, score in data.items():
        if qid in id_to_dim:
            answers[id_to_dim[qid]].append(int(score))
    return answers


def generate_demo_answers() -> Dict[str, List[int]]:
    """生成示例答案（模拟一个中等成熟度组织）。"""
    return {
        "strategy":  [3, 3, 2, 2, 3],
        "process":   [3, 3, 3, 2, 2],
        "assets":    [3, 3, 4, 3, 2],
        "measurement": [2, 2, 3, 3, 2],
        "technology": [3, 4, 3, 2, 2],
        "culture":   [3, 3, 2, 2, 3],
    }


def compute_results(answers: Dict[str, List[int]]) -> Tuple[Dict[str, dict], float, int]:
    """计算各维度得分和总体成熟度。"""
    dimension_results = {}
    total_weighted = 0.0
    total_weight = 0.0

    for dim, scores in answers.items():
        if not scores:
            continue
        avg = sum(scores) / len(scores)
        level = score_to_level(avg)
        weight = DIMENSIONS[dim]["weight"]
        dimension_results[dim] = {
            "name": DIMENSIONS[dim]["name"],
            "average_score": round(avg, 2),
            "level": level,
            "level_name": LEVELS[level],
            "scores": scores,
        }
        total_weighted += avg * weight
        total_weight += weight

    overall_avg = total_weighted / total_weight if total_weight > 0 else 0
    overall_level = score_to_level(overall_avg)

    return dimension_results, overall_avg, overall_level


def print_ascii_radar(dimension_results: Dict[str, dict]):
    """打印 ASCII 雷达图。"""
    print("\n" + "=" * 70)
    print("成熟度雷达图（平均分 / 5）")
    print("=" * 70)

    dims = list(DIMENSIONS.keys())
    n = len(dims)

    # 简化的雷达图：每个维度显示条形
    for dim in dims:
        info = dimension_results.get(dim, {"average_score": 0, "level": 1, "name": DIMENSIONS[dim]["name"]})
        score = info["average_score"]
        bar_len = int(round(score))
        bar = "█" * bar_len + "░" * (5 - bar_len)
        print(f"{info['name']:16s} [{bar}] {score:.1f} → {LEVELS[info['level']]}")


def print_report(dimension_results: Dict[str, dict], overall_avg: float, overall_level: int):
    """打印评估报告。"""
    print("\n" + "=" * 70)
    print("评估结果")
    print("=" * 70)
    print(f"总体平均分: {overall_avg:.2f} / 5.0")
    print(f"总体成熟度: Level {overall_level} — {LEVELS[overall_level]}")
    print("\n各维度详情:")
    for dim, info in dimension_results.items():
        print(f"  • {info['name']}: {info['average_score']:.2f} → Level {info['level']} ({info['level_name']})")

    print("\n改进建议:")
    sorted_dims = sorted(dimension_results.items(), key=lambda x: x[1]["average_score"])
    weakest = sorted_dims[0]
    second_weak = sorted_dims[1] if len(sorted_dims) > 1 else None
    print(f"  1. 优先改进维度: {weakest[1]['name']} (当前 {weakest[1]['average_score']:.2f} 分)")
    if second_weak:
        print(f"  2. 次要改进维度: {second_weak[1]['name']} (当前 {second_weak[1]['average_score']:.2f} 分)")
    print(f"  3. 参考标准: ISO/IEC 26565:2026, RCMM, RiSE-RM, NASA RRL")


def main():
    parser = argparse.ArgumentParser(
        description="软件复用成熟度评估问卷 CLI（基于 ISO/IEC 26565:2026）"
    )
    parser.add_argument(
        "--json-input",
        type=str,
        help="从 JSON 文件加载答案（题目 ID -> 分数 或 维度 -> 分数列表）",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="使用示例数据运行，不交互提问",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="输出报告 JSON 文件路径",
    )

    args = parser.parse_args()

    if args.demo:
        answers = generate_demo_answers()
        print("[演示模式] 使用示例数据运行评估\n")
    elif args.json_input:
        answers = load_answers_from_json(args.json_input)
    else:
        answers = ask_questions_interactive()

    dimension_results, overall_avg, overall_level = compute_results(answers)

    print_ascii_radar(dimension_results)
    print_report(dimension_results, overall_avg, overall_level)

    # 构建完整报告
    report = {
        "framework": "ISO/IEC 26565:2026 / RCMM / RiSE / NASA RRL",
        "overall_score": round(overall_avg, 2),
        "overall_level": overall_level,
        "overall_level_name": LEVELS[overall_level],
        "dimensions": dimension_results,
        "recommendations": {
            "priority_1": min(dimension_results.items(), key=lambda x: x[1]["average_score"])[1]["name"],
        },
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n报告已保存到: {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
