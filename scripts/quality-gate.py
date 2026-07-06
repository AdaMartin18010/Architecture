#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容质量门控脚本（Quality Gate）

检查 Markdown 文档是否满足内容质量基线：
1. 概念定义（Definition）
2. 示例（Example）
3. 反例/失败案例/反模式（Counter-example / Anti-pattern）
4. 权威来源（Authority source）
5. 思维表征（图示/矩阵/决策树）

用法：
    python scripts/quality-gate.py [path/to/file.md|path/to/dir]

默认扫描 struct/ 下所有 .md 文件，但跳过 99-reference/audit/ 与 CHANGELOG。
"""

import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List


@dataclass
class GateResult:
    path: Path
    score: int           # 0-100
    passed: bool
    checks: dict
    warnings: List[str]


# 检查规则（可根据需要扩展）
RULES = {
    "definition": {
        "name": "概念定义",
        "patterns": [
            r"#{1,4}\s*定义",
            r"#{1,4}\s*.*概念",
            r"#{1,4}\s*.*术语",
            r"\*\*定义\*\*",
            r"\*\*概念\*\*",
            r"\*\*术语\*\*",
            r"##\s*\d+\.\s*.*定义",
        ],
        "weight": 20,
    },
    "example": {
        "name": "正向示例",
        "patterns": [
            r"#{1,4}\s*示例",
            r"#{1,4}\s*.*案例",
            r"\*\*示例\*\*",
            r"\*\*案例\*\*",
            r">\s*\[示例",
            r"例如：",
            r"例如，",
        ],
        "weight": 15,
    },
    "counter_example": {
        "name": "反例/反模式",
        "patterns": [
            r"#{1,4}\s*反例",
            r"#{1,4}\s*反模式",
            r"#{1,4}\s*失败案例",
            r"#{1,4}\s*边界.*条件",
            r"\*\*反例\*\*",
            r"\*\*反模式\*\*",
            r"\*\*失败案例\*\*",
            r"边界场景",
            r"不应.*复用",
            r"错误.*复用",
        ],
        "weight": 15,
    },
    "authority": {
        "name": "权威来源",
        "patterns": [
            r"#{1,4}\s*权威来源",
            r"#{1,4}\s*参考.*来源",
            r"#{1,4}\s*参考.*文献",
            r"\*\*权威来源\*\*",
            r"\*\*来源 URL\*\*",
            r"核查日期",
            r"\[来源\]\(https?://",
        ],
        "weight": 20,
    },
    "representation": {
        "name": "思维表征（图/矩阵/树）",
        "patterns": [
            r"```mermaid",
            r"```graphviz",
            r"#{1,4}\s*.*矩阵",
            r"#{1,4}\s*.*决策树",
            r"#{1,4}\s*.*判定树",
            r"#{1,4}\s*.*思维导图",
            r"#{1,4}\s*.*概念谱系",
            r"\|.*\|.*\|",  # 至少有一个表格
        ],
        "weight": 15,
    },
    "argumentation": {
        "name": "论证/证明/分析",
        "patterns": [
            r"#{1,4}\s*.*证明",
            r"#{1,4}\s*.*论证",
            r"#{1,4}\s*.*分析",
            r"#{1,4}\s*.*推理",
            r"\*\*证明\*\*",
            r"\*\*论证\*\*",
            r"公理",
            r"定理",
            r"因为.*所以",
            r"因此.*",
        ],
        "weight": 15,
    },
}

MIN_SCORE = 60      # 及格线
MIN_WEIGHTED = 3    # 至少通过 3 项（含 authority + definition）


def check_file(filepath: Path) -> GateResult:
    text = filepath.read_text(encoding="utf-8")
    word_count = len(re.findall(r"[\u4e00-\u9fa5]", text)) + len(text.split())

    checks = {}
    score = 0
    warnings = []

    for key, rule in RULES.items():
        matched = any(re.search(p, text, re.IGNORECASE) for p in rule["patterns"])
        checks[key] = matched
        if matched:
            score += rule["weight"]
        else:
            warnings.append(f"缺少 {rule['name']}")

    # 字数过少的额外警告
    if word_count < 300:
        warnings.append(f"文档过短（约 {word_count} 字/词），建议 ≥ 300")
        score -= 10

    # 必须有定义和权威来源
    passed = (
        checks.get("definition", False)
        and checks.get("authority", False)
        and score >= MIN_SCORE
        and sum(1 for v in checks.values() if v) >= MIN_WEIGHTED
    )

    return GateResult(
        path=filepath,
        score=max(0, min(100, score)),
        passed=passed,
        checks=checks,
        warnings=warnings,
    )


def scan_directory(root: Path) -> List[GateResult]:
    root = root.resolve()
    results = []
    skip_patterns = [
        "99-reference/audit/",
        "99-reference/CHANGELOG",
        "99-reference/frontier-tracking/",
        "plans-tasks/",
        "__pycache__",
        ".venv",
    ]
    for md in root.rglob("*.md"):
        rel = md.relative_to(root)
        if any(sp in str(rel).replace("\\", "/") for sp in skip_patterns):
            continue
        results.append(check_file(md))
    return results


def format_result(r: GateResult, root: Path) -> str:
    rel = r.path.relative_to(root.parent) if str(r.path).startswith(str(root.parent)) else r.path
    status = "✅ 通过" if r.passed else "❌ 未通过"
    detail = ", ".join(
        f"{'✓' if r.checks.get(k, False) else '✗'}{RULES[k]['name'][:2]}"
        for k in RULES
    )
    warn = "; ".join(r.warnings[:3]) if r.warnings else "无"
    return f"{status} [{r.score:>3}] {rel} | {detail} | 警告: {warn}"


def main():
    parser = argparse.ArgumentParser(description="Markdown 内容质量门控")
    parser.add_argument(
        "target",
        nargs="?",
        default="struct",
        help="目标文件或目录（默认: struct/）",
    )
    # 如果目标是相对路径，先 resolve
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="遇到第一个未通过文件即退出",
    )
    parser.add_argument(
        "--only-failures",
        action="store_true",
        help="仅显示未通过的文件",
    )
    args = parser.parse_args()

    root = Path(args.target).resolve()
    project_root = Path(__file__).resolve().parent.parent

    if root.is_file():
        results = [check_file(root)]
    elif root.is_dir():
        results = scan_directory(root)
    else:
        print(f"错误：路径不存在 {root}", file=sys.stderr)
        sys.exit(1)

    print(f"扫描文件数: {len(results)}")
    print(f"质量基线: 定义 + 权威来源 必须满足，总分 ≥ {MIN_SCORE}，通过项 ≥ {MIN_WEIGHTED}")
    print("-" * 100)

    failures = []
    for r in results:
        if args.only_failures and r.passed:
            continue
        print(format_result(r, project_root))
        if not r.passed:
            failures.append(r)
            if args.fail_fast:
                break

    print("-" * 100)
    total = len(results)
    passed = total - len(failures)
    print(f"统计: {passed}/{total} 通过，通过率 {passed/total*100:.1f}%")

    # 输出最严重的问题文件（Top 10）
    if failures:
        print("\n未通过文件 Top 10（按分数升序）:")
        for r in sorted(failures, key=lambda x: x.score)[:10]:
            rel = r.path.relative_to(project_root)
            print(f"  [{r.score}] {rel}: {', '.join(r.warnings[:3])}")

    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
