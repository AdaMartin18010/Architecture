#!/usr/bin/env python3
"""
术语查询脚本 — 跨标准术语翻译与检索工具

用法:
    python terminology-query.py <查询词>
    python terminology-query.py --list-standards
    python terminology-query.py --standard iso42010

按 SUBSEQUENT_PLAN_2026.md 决策 3A 开发：Python CLI 快速原型
"""

import argparse
import json
import re
import sys
from pathlib import Path

# 内置核心术语库（按标准组织）
# 后续可扩展为从 terminology-crosswalk.md 自动解析
TERM_DATABASE = {
    "iso42010:2022": {
        "EoI": "Entity of Interest（关注点实体）",
        "ADF": "Architecture Description Framework（架构描述框架）",
        "AD": "Architecture Description（架构描述）",
        "viewpoint": "架构视点：针对一组相关关注点的观察视角的规约",
        "view": "架构视图：针对一组相关关注点，系统架构的表达",
        "model kind": "模型种类：约定、语言、符号的规约",
        "correspondence": "对应关系：不同架构描述元素之间的关联",
    },
    "iso25010:2024": {
        "reusability": "可复用性：资产能在多个系统或多个资产构建中被使用的程度",
        "modularity": "模块化：系统由独立组件组成的程度",
        "analysability": "可分析性：评估软件以确定修改影响范围的程度",
        "testability": "可测试性：为系统建立有效测试准则并执行测试的容易程度",
    },
    "togaf10": {
        "ABB": "Architecture Building Block（架构构建块）",
        "SBB": "Solution Building Block（解决方案构建块）",
        "ADM": "Architecture Development Method（架构开发方法）",
        "Enterprise Continuum": "企业连续体：从通用基础架构到组织特定架构的资产谱系",
    },
    "slsa": {
        "provenance": "来源证明：描述软件制品如何被构建的可验证记录",
        "hermetic build": "密闭构建：构建过程不依赖外部网络或可变状态",
        "reproducible build": "可复现构建：重复构建时产生逐位相同的输出",
        "attestation": " attestations：对软件制品某类声明的密码学签名声明",
    },
    "mcp": {
        "tool": "MCP 工具：服务器暴露的可执行能力，供 LLM 调用",
        "resource": "MCP 资源：服务器提供的可被客户端读取的数据",
        "prompt": "MCP 提示：服务器提供的预定义模板或工作流",
        "sampling": "MCP 采样：服务器请求客户端（LLM）生成内容的机制",
        "task": "MCP 任务（2025-11-25）：跟踪长时间运行请求的持久化抽象",
    },
    "a2a": {
        "Agent Card": "代理名片：描述 Agent 能力、端点和认证要求的元数据",
        "Task": "A2A 任务：Agent 之间委托的工作单元",
        "Artifact": "A2A 产物：任务生成的最终交付物",
        "Skill": "A2A 技能：Agent 能够执行的特定能力",
    },
}

ALIASES = {
    "entity of interest": "EoI",
    "architecture description framework": "ADF",
    "架构描述框架": "ADF",
    "关注点实体": "EoI",
    "可复用性": "reusability",
    "复用": "reusability",
}


def list_standards():
    print("支持的标准/框架：")
    for std in TERM_DATABASE:
        print(f"  - {std}")


def search_term(query: str):
    query_lower = query.lower().strip()
    results = []

    # 先检查别名
    if query_lower in ALIASES:
        query = ALIASES[query_lower]
        query_lower = query.lower()

    for standard, terms in TERM_DATABASE.items():
        for term, definition in terms.items():
            if query_lower in term.lower() or query_lower in definition.lower():
                results.append((standard, term, definition))

    return results


def search_by_standard(standard: str):
    standard_lower = standard.lower()
    matched = {}
    for std, terms in TERM_DATABASE.items():
        if standard_lower in std.lower():
            matched[std] = terms
    return matched


def main():
    parser = argparse.ArgumentParser(
        description="跨标准术语查询脚本（软件工程架构复用视角）"
    )
    parser.add_argument("query", nargs="?", help="要查询的术语或关键词")
    parser.add_argument(
        "--list-standards", action="store_true", help="列出支持的标准"
    )
    parser.add_argument(
        "--standard", metavar="STD", help="按标准列出全部术语"
    )

    args = parser.parse_args()

    if args.list_standards:
        list_standards()
        return 0

    if args.standard:
        matched = search_by_standard(args.standard)
        if not matched:
            print(f"未找到标准: {args.standard}")
            return 1
        for std, terms in matched.items():
            print(f"\n【{std}】")
            for term, definition in terms.items():
                print(f"  {term}: {definition}")
        return 0

    if not args.query:
        parser.print_help()
        return 1

    results = search_term(args.query)
    if not results:
        print(f"未找到与 '{args.query}' 相关的术语。")
        print("提示: 使用 --list-standards 查看支持的标准，或使用 --standard 浏览完整术语表。")
        return 1

    print(f"找到 {len(results)} 条与 '{args.query}' 相关的结果：\n")
    for std, term, definition in results:
        print(f"[{std}] {term}")
        print(f"  → {definition}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
