#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dist/ 生成物质量门控

对 scripts/build-deliverables.py 的产出（dist/book-full.md 与 dist/book-volumes/）
执行三类校验：
1. 存在性与非空校验：book-full.md 与全部分卷文件存在且非空；
2. 漂移检测：比较 struct/ 源文件最新 mtime 与 dist/book-full.md 的生成时间，
   若 struct 更新（dist 落后于 struct）则判定漂移，提示重新构建；
3. 相对链接抽查：扫描 dist/ 内 Markdown 的本地相对链接，校验目标存在性，
   死链即失败（外部 URL / mailto / 纯锚点跳过）。

输出报告：reports/dist-check.md
退出码：0 = 全部通过；1 = 任一校验失败。

用法：
    python scripts/dist-check.py
"""

import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STRUCT_DIR = PROJECT_ROOT / "struct"
DIST_DIR = PROJECT_ROOT / "dist"
REPORT_PATH = PROJECT_ROOT / "reports" / "dist-check.md"
BOOK_FULL = DIST_DIR / "book-full.md"
VOLUMES_DIR = DIST_DIR / "book-volumes"

# build-deliverables.py 生成到 struct/ 内的派生文件（在 book 构建之后写入，
# 其 mtime 晚于 book-full.md 属正常现象，不参与漂移检测）
GENERATED_IN_STRUCT = {
    "struct/99-reference/course/learning-path.md",
    "struct/99-reference/course/syllabus.md",
}


def check_existence() -> Tuple[List[str], List[str]]:
    """校验 book-full.md 与分卷存在且非空。返回 (passed_items, failures)。"""
    passed: List[str] = []
    failures: List[str] = []

    if BOOK_FULL.exists() and BOOK_FULL.stat().st_size > 0:
        passed.append(f"dist/book-full.md 存在且非空（{BOOK_FULL.stat().st_size} 字节）")
    else:
        failures.append("dist/book-full.md 不存在或为空，请运行 `python scripts/build-deliverables.py`")

    volumes = sorted(VOLUMES_DIR.glob("*.md")) if VOLUMES_DIR.is_dir() else []
    if not volumes:
        failures.append("dist/book-volumes/ 不存在或无分卷文件，请运行 `python scripts/build-deliverables.py`")
    else:
        for vol in volumes:
            if vol.stat().st_size > 0:
                passed.append(f"dist/book-volumes/{vol.name} 非空（{vol.stat().st_size} 字节）")
            else:
                failures.append(f"dist/book-volumes/{vol.name} 为空文件")

    return passed, failures


def check_drift() -> Tuple[bool, str, str]:
    """漂移检测：struct 源文件最新 mtime 是否晚于 dist/book-full.md。

    返回 (is_stale, detail, newest_source_rel)。
    """
    if not BOOK_FULL.exists():
        return True, "dist/book-full.md 不存在，无法比较生成时间", ""

    book_mtime = BOOK_FULL.stat().st_mtime
    newest_path: Optional[Path] = None
    newest_mtime = -1.0
    for md in STRUCT_DIR.rglob("*.md"):
        rel = md.relative_to(PROJECT_ROOT).as_posix()
        if rel in GENERATED_IN_STRUCT:
            continue
        mtime = md.stat().st_mtime
        if mtime > newest_mtime:
            newest_mtime = mtime
            newest_path = md

    if newest_path is None:
        return False, "struct/ 下无 Markdown 源文件，跳过漂移检测", ""

    newest_rel = newest_path.relative_to(PROJECT_ROOT).as_posix()
    if newest_mtime > book_mtime:
        fmt = "%Y-%m-%d %H:%M:%S"
        detail = (
            f"最新源文件 `{newest_rel}` 修改于 "
            f"{datetime.fromtimestamp(newest_mtime).strftime(fmt)}，晚于 "
            f"dist/book-full.md 生成时间 {datetime.fromtimestamp(book_mtime).strftime(fmt)}"
        )
        return True, detail, newest_rel
    return False, f"dist/book-full.md 不晚于最新源文件 `{newest_rel}`", newest_rel


def extract_links(text: str) -> List[Tuple[str, str, int]]:
    """提取 Markdown 内联链接，跳过代码块（与 link-checker.py 逻辑一致）。"""
    links: List[Tuple[str, str, int]] = []
    in_code_block = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line):
            links.append((m.group(1), m.group(2).strip(), lineno))
    return links


def check_links() -> Tuple[int, List[Tuple[str, int, str, str]]]:
    """抽查 dist/ 内 Markdown 的本地相对链接目标存在性。

    返回 (checked_count, broken[(source, line, text, target)])。
    """
    md_files: List[Path] = []
    if BOOK_FULL.exists():
        md_files.append(BOOK_FULL)
    if VOLUMES_DIR.is_dir():
        md_files.extend(sorted(VOLUMES_DIR.glob("*.md")))

    checked = 0
    broken: List[Tuple[str, int, str, str]] = []
    for md_file in md_files:
        rel_source = md_file.relative_to(PROJECT_ROOT).as_posix()
        text = md_file.read_text(encoding="utf-8", errors="replace")
        for link_text, link_target, lineno in extract_links(text):
            # 跳过外部链接、mailto 与纯锚点
            if re.match(r"^[a-z][a-z0-9+.-]*:", link_target, re.IGNORECASE):
                continue
            bare = link_target.split("#", 1)[0]
            if not bare:
                continue
            checked += 1
            target = (md_file.parent / bare).resolve()
            if target.exists():
                continue
            # 目录链接：允许 README.md / index.md 兜底
            if target.is_dir() or "." not in Path(bare).name:
                if any((target / name).exists() for name in ("README.md", "index.md", "readme.md")):
                    continue
            broken.append((rel_source, lineno, link_text, link_target))

    return checked, broken


def write_report(existence_passed: List[str], existence_failures: List[str],
                 is_stale: bool, drift_detail: str,
                 link_checked: int, broken: List[Tuple[str, int, str, str]]) -> None:
    ok = not existence_failures and not is_stale and not broken
    lines = [
        "# dist/ 生成物质量门控报告",
        "",
        f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"> **检查脚本**: `python scripts/dist-check.py`",
        f"> **总体结果**: {'✅ 通过' if ok else '❌ 未通过'}",
        "",
        "---",
        "",
        "## 1. 存在性与非空校验",
        "",
    ]
    if existence_failures:
        for f in existence_failures:
            lines.append(f"- ❌ {f}")
    for p in existence_passed:
        lines.append(f"- ✅ {p}")

    lines.extend(["", "## 2. 漂移检测（struct → dist）", ""])
    if is_stale:
        lines.append(f"- ❌ dist/ 落后于 struct/：{drift_detail}")
        lines.append("- **处置**: 运行 `python scripts/build-deliverables.py` 重建 dist/")
    else:
        lines.append(f"- ✅ {drift_detail}")

    lines.extend(["", "## 3. 相对链接抽查", ""])
    lines.append(f"- 检查的本地相对链接数: **{link_checked}**")
    if broken:
        lines.append(f"- ❌ 死链数: **{len(broken)}**")
        lines.extend(["", "| 源文件 | 行号 | 链接文本 | 目标 |", "|--------|------|----------|------|"])
        for source, lineno, text, target in broken:
            lines.append(f"| {source} | {lineno} | {text} | `{target}` |")
    else:
        lines.append("- ✅ 未发现死链")

    lines.append("")
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    existence_passed, existence_failures = check_existence()
    is_stale, drift_detail, _ = check_drift()
    link_checked, broken = check_links()

    write_report(existence_passed, existence_failures, is_stale, drift_detail, link_checked, broken)

    print(f"存在性校验: {len(existence_passed)} 项通过, {len(existence_failures)} 项失败")
    print(f"漂移检测: {'❌ dist 落后于 struct' if is_stale else '✅ 无漂移'}")
    print(f"链接抽查: {link_checked} 个本地链接, {len(broken)} 个死链")
    print(f"报告已保存: {REPORT_PATH.relative_to(PROJECT_ROOT).as_posix()}")

    if existence_failures or is_stale or broken:
        if is_stale:
            print("提示: 运行 `python scripts/build-deliverables.py` 重建 dist/")
        return 1
    print("dist/ 质量门控全部通过 ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
