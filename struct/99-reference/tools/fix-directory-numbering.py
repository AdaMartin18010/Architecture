#!/usr/bin/env python3
"""
fix-directory-numbering.py
检测并重命名 struct/ 下重复编号的子目录，使其在同级目录内连续唯一。
同时更新项目 Markdown 文件中的相对路径链接。

用法:
    python fix-directory-numbering.py --dry-run    # 预览变更
    python fix-directory-numbering.py --apply      # 执行重命名与链接更新
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

PROJECT_ROOT = Path("e:/_src/Architecture")
STRUCT_ROOT = PROJECT_ROOT / "struct"


def parse_numbered_dir(name: str) -> tuple[int, str] | None:
    """解析形如 '01-foo-bar' 的目录名，返回 (number, slug)。"""
    m = re.match(r"^(\d{2,})-(.+)$", name)
    if not m:
        return None
    return int(m.group(1)), m.group(2)


def collect_numbered_dirs() -> dict[Path, list[tuple[Path, int, str]]]:
    """按父目录收集所有编号子目录。"""
    grouped: dict[Path, list[tuple[Path, int, str]]] = defaultdict(list)
    for parent in STRUCT_ROOT.rglob("*"):
        if not parent.is_dir():
            continue
        for child in parent.iterdir():
            if not child.is_dir():
                continue
            parsed = parse_numbered_dir(child.name)
            if parsed is None:
                continue
            num, slug = parsed
            grouped[parent].append((child, num, slug))
    return grouped


def find_duplicates(
    grouped: dict[Path, list[tuple[Path, int, str]]]
) -> dict[Path, list[tuple[Path, int, str]]]:
    """找出存在编号重复的父目录。"""
    duplicates = {}
    for parent, items in grouped.items():
        nums = [num for _, num, _ in items]
        if len(nums) != len(set(nums)):
            duplicates[parent] = items
    return duplicates


def build_rename_plan(
    duplicates: dict[Path, list[tuple[Path, int, str]]]
) -> list[tuple[Path, Path]]:
    """
    为每个重复父目录生成重命名计划。
    规则：按当前 (num, slug) 排序后重新分配连续编号。
    """
    plan: list[tuple[Path, Path]] = []
    for parent in sorted(duplicates):
        items = duplicates[parent]
        # 按当前编号+slug排序，保证稳定
        items_sorted = sorted(items, key=lambda x: (x[1], x[2]))
        for new_idx, (old_path, _, slug) in enumerate(items_sorted, start=1):
            new_name = f"{new_idx:02d}-{slug}"
            new_path = parent / new_name
            if old_path.name != new_name:
                plan.append((old_path, new_path))
    return plan


def update_markdown_links(plan: list[tuple[Path, Path]], dry_run: bool) -> dict[Path, int]:
    """扫描所有 Markdown 文件，更新受影响的相对/绝对路径链接。"""
    # 建立 old_relative -> new_relative 映射
    renames: dict[str, str] = {}
    for old_path, new_path in plan:
        old_rel = old_path.relative_to(PROJECT_ROOT).as_posix()
        new_rel = new_path.relative_to(PROJECT_ROOT).as_posix()
        renames[old_rel] = new_rel

    md_files = list(PROJECT_ROOT.rglob("*.md"))
    md_files = [p for p in md_files if ".venv" not in p.parts and "node_modules" not in p.parts]

    file_counts: dict[Path, int] = defaultdict(int)

    for md_path in md_files:
        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[WARN] 无法读取 {md_path}: {e}", file=sys.stderr)
            continue

        new_text = text
        for old_rel, new_rel in renames.items():
            # 同时替换 POSIX 和 Windows 风格斜杠
            old_win = old_rel.replace("/", "\\")
            new_win = new_rel.replace("/", "\\")
            new_text = new_text.replace(old_rel, new_rel)
            if old_win != old_rel:
                new_text = new_text.replace(old_win, new_win)

        if new_text != text:
            count = sum(text.count(old_rel) for old_rel in renames)
            file_counts[md_path] += count
            if not dry_run:
                md_path.write_text(new_text, encoding="utf-8")

    return dict(file_counts)


def run_git_mv(plan: list[tuple[Path, Path]], dry_run: bool) -> None:
    """执行 git mv 重命名。"""
    for old_path, new_path in plan:
        if dry_run:
            print(f"[DRY-RUN git mv] {old_path.relative_to(PROJECT_ROOT)} -> {new_path.relative_to(PROJECT_ROOT)}")
        else:
            subprocess.run(
                ["git", "mv", str(old_path), str(new_path)],
                cwd=PROJECT_ROOT,
                check=True,
            )


def main() -> int:
    parser = argparse.ArgumentParser(description="修复 struct/ 下重复编号目录")
    parser.add_argument("--apply", action="store_true", help="执行重命名与链接更新")
    args = parser.parse_args()
    dry_run = not args.apply

    grouped = collect_numbered_dirs()
    duplicates = find_duplicates(grouped)

    if not duplicates:
        print("✅ 未发现重复编号的子目录。")
        return 0

    plan = build_rename_plan(duplicates)

    print(f"{'='*60}")
    print(f"目录编号修复")
    print(f"模式: {'预览 (dry-run)' if dry_run else '执行 (--apply)'}")
    print(f"发现重复父目录数: {len(duplicates)}")
    print(f"计划重命名目录数: {len(plan)}")
    print(f"{'='*60}\n")

    print("【重复诊断】")
    for parent in sorted(duplicates):
        items = duplicates[parent]
        nums = [num for _, num, _ in items]
        print(f"  {parent.relative_to(PROJECT_ROOT)}: {len(items)} 个子目录，编号 {sorted(nums)}")

    print("\n【重命名计划】")
    for old_path, new_path in plan:
        print(f"  {old_path.relative_to(PROJECT_ROOT)} -> {new_path.relative_to(PROJECT_ROOT)}")

    print("\n【执行重命名】")
    run_git_mv(plan, dry_run)

    print("\n【更新 Markdown 链接】")
    file_counts = update_markdown_links(plan, dry_run)
    if file_counts:
        total = sum(file_counts.values())
        print(f"  更新 {len(file_counts)} 个文件，共 {total} 处链接")
        for md_path, count in sorted(file_counts.items()):
            print(f"    {md_path.relative_to(PROJECT_ROOT)}: {count} 处")
    else:
        print("  无 Markdown 链接需要更新")

    print(f"\n{'='*60}")
    if dry_run:
        print("本次为预览，未实际修改文件。确认无误后追加 --apply 执行。")
    print(f"{'='*60}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
