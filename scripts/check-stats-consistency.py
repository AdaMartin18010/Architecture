#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
校验 README.md / MASTER_PLAN.md / COMPLETION_REPORT_PHASE_1_5.md 的关键数字
与 reports/stats.json（机器真源）一致，且不含已知过时数字。

模式：数字存在性 + 过时数字黑名单（不依赖 STATS 块，KISS）。

用法：python scripts/check-stats-consistency.py
退出码：0 通过；1 不一致或含过时数字；2 缺 stats.json。
"""

import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STATS_JSON = PROJECT_ROOT / "reports" / "stats.json"

DOCS = {
    "README.md": PROJECT_ROOT / "README.md",
    "MASTER_PLAN.md": PROJECT_ROOT / "struct" / "MASTER_PLAN.md",
    "COMPLETION_REPORT_PHASE_1_5.md": PROJECT_ROOT / "COMPLETION_REPORT_PHASE_1_5.md",
}

# 已知过时/漂移数字（出现即失败）—— 随 P0/P1 推进逐步补充
STALE_PATTERNS = [
    "struct/ 307", "struct/ 301", "view/ 8 =", "view/ 8 ",
    "1,004,537", "~79.1 万", "~97.7 万", "~93.1 万", "~75.5 万",
    "15 公理 + 29 定理", "= 44 条", "公理-定理体系 × 20+",
    "defines=2312", "69 张图", "69 个 `.mmd`",
]


def main() -> int:
    if not STATS_JSON.exists():
        print("缺少 reports/stats.json，请先运行: python scripts/knowledge-cli.py stats", file=sys.stderr)
        return 2
    stats = json.loads(STATS_JSON.read_text(encoding="utf-8"))
    struct_md = str(stats["struct_md"])           # 330
    total_md = str(stats["struct_md"] + stats["view_md"])  # 353
    total_words = int(stats["total_words"])
    words = f"{total_words:,}"                       # 仅用于打印
    tol = max(5000, int(total_words * 0.02))          # 字数容差 ±2%（至少 ±5000）：内容微调不破坏校验

    # 结构性数字（文件数）必须精确子串匹配；字数按容差比对
    exact_required = {
        "README.md": [total_md, struct_md],
        "MASTER_PLAN.md": [total_md, struct_md],
        "COMPLETION_REPORT_PHASE_1_5.md": [struct_md],
    }
    num_re = re.compile(r"\d{1,3}(?:,\d{3})+")

    errors = []
    for name, path in DOCS.items():
        if not path.exists():
            errors.append(f"{name}: 文件不存在")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for stale in STALE_PATTERNS:
            if stale in text:
                errors.append(f"{name}: 含过时数字/表述 `{stale}`")
        for req in exact_required.get(name, []):
            if req not in text:
                errors.append(f"{name}: 缺少真源数字 `{req}`")
        big = [int(m.replace(",", "")) for m in num_re.findall(text) if int(m.replace(",", "")) >= 100_000]
        if not big:
            errors.append(f"{name}: 未找到字数锚点（带千分位的大数）")
        elif all(abs(n - total_words) > tol for n in big):
            nearest = min(big, key=lambda n: abs(n - total_words))
            errors.append(f"{name}: 字数漂移（文档锚点 {nearest:,}，真源 {words}，差 {abs(nearest - total_words):,}，容差 ±{tol:,}）")

    if errors:
        print("STATS 一致性校验失败：")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"STATS 一致性校验通过：3 处文档与真源一致（struct={struct_md}, 合计={total_md}, 字数={words}）。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
