#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理 batch-fix-quality-gate.py 注入的"补充说明"模板段落。

用法：
    python scripts/cleanup-batch-template-injection.py [--dry-run]

默认执行清理；使用 --dry-run 仅预览不写入。
"""

import argparse
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 匹配从 "\n\n---\n\n## 补充说明：" 开始到文件末尾的内容
SUPPLEMENT_PATTERN = re.compile(r"\n\n---\n\n## 补充说明：.*$", re.DOTALL)


def collect_markdown_files():
    files = []
    for rel in ("struct", "view"):
        for md in (PROJECT_ROOT / rel).rglob("*.md"):
            files.append(md)
    return files


def cleanup_file(md: Path, dry_run: bool = False) -> dict:
    text = md.read_text(encoding="utf-8", errors="ignore")
    match = SUPPLEMENT_PATTERN.search(text)
    if not match:
        return {"path": md, "polluted": False, "removed_chars": 0}

    removed = match.group(0)
    cleaned = SUPPLEMENT_PATTERN.sub("", text)
    # 如果清理后文件末尾有多余换行， trim 到最多两个换行
    cleaned = cleaned.rstrip() + "\n"

    if not dry_run:
        md.write_text(cleaned, encoding="utf-8")

    return {"path": md, "polluted": True, "removed_chars": len(removed)}


def main():
    parser = argparse.ArgumentParser(
        description="清理 batch-fix-quality-gate.py 注入的模板段落"
    )
    parser.add_argument("--dry-run", action="store_true", help="仅预览不写入")
    args = parser.parse_args()

    files = collect_markdown_files()
    results = []
    total_removed = 0
    polluted_count = 0

    for md in files:
        result = cleanup_file(md, dry_run=args.dry_run)
        results.append(result)
        if result["polluted"]:
            polluted_count += 1
            total_removed += result["removed_chars"]

    mode = "【预览模式】" if args.dry_run else "【已执行清理】"
    print(f"{mode} 扫描文件数: {len(files)}")
    print(f"发现污染文件数: {polluted_count}")
    print(f"累计可清理字符数: {total_removed}")

    if polluted_count:
        print("\n污染文件清单（前 50）:")
        for r in [r for r in results if r["polluted"]][:50]:
            rel = r["path"].relative_to(PROJECT_ROOT)
            print(f"  - {rel} ({r['removed_chars']} 字符)")

    # 生成清理报告
    report_path = PROJECT_ROOT / "scripts" / "cleanup-report.md"
    lines = [
        "# 模板污染清理报告",
        "",
        f"- 扫描文件数: {len(files)}",
        f"- 发现污染文件数: {polluted_count}",
        f"- 累计清理字符数: {total_removed}",
        f"- 执行模式: {'dry-run' if args.dry_run else 'applied'}",
        "",
        "## 污染文件清单",
        "",
    ]
    for r in [r for r in results if r["polluted"]]:
        rel = r["path"].relative_to(PROJECT_ROOT)
        lines.append(f"- `{rel}` — {r['removed_chars']} 字符")

    if not args.dry_run:
        report_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"\n清理报告已保存: {report_path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
