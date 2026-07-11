#!/usr/bin/env python3
"""
batch-normalize-aaf-thresholds.py
=================================

批量把 Markdown 中旧式 AAF 阈值表述（0.7 / 70% 等）统一为 canonical 小数写法，
并引用 reuse_thresholds.py 中的常量名。

仅处理普通段落与表格单元格，不改动代码块内容（由调用方控制）。

用法：
    python scripts/batch-normalize-aaf-thresholds.py
"""

import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

TARGETS = [
    "struct/01-meta-model-standards/06-formal-axioms/axiom-rigor-audit.md",
    "struct/05-functional-architecture-reuse/decision-tree-granularity-cost-roi.md",
    "struct/99-reference/tools/reuse-decision-tool-v2/README.md",
    "struct/99-reference/glossary/axiom-theorem-tree.md",
    "struct/01-meta-model-standards/01-iso-420xx-family/ieee-1517-reuse-processes.md",
    "struct/99-reference/book-outline.md",
    "struct/99-reference/book-outline-v2.md",
    "struct/99-reference/templates/academic-citation-template.md",
    "struct/99-reference/knowledge-index/qa-index.md",
]

# 统一替换规则（按顺序应用）
REPLACEMENTS = [
    # AAF < 0.7 的各种变体
    (r"AAF\s*<\s*0\.7", "AAF < AAF_ECONOMIC_FLOOR（0.7，canonical [0.0, 1.0]）"),
    # AAF ≥ 0.7 / >= 0.7
    (r"AAF\s*≥\s*0\.7", "AAF ≥ AAF_ECONOMIC_FLOOR（0.7）"),
    (r"AAF\s*>=\s*0\.7", "AAF ≥ AAF_ECONOMIC_FLOOR（0.7）"),
]


def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    original = text
    for pattern, repl in REPLACEMENTS:
        text = re.sub(pattern, repl, text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return 1
    return 0


def main() -> int:
    changed = 0
    for rel in TARGETS:
        path = PROJECT_ROOT / rel
        if path.exists():
            changed += process_file(path)
            print(f"处理: {rel}")
        else:
            print(f"跳过（不存在）: {rel}")
    print(f"\n共修改 {changed} 个文件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
