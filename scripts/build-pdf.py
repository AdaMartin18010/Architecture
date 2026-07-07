#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF/ePub 输出脚本（Phase 6）

依赖：pandoc + LaTeX（PDF）
用法：
    python scripts/build-pdf.py          # 默认生成 dist/book-full.pdf
    python scripts/build-pdf.py --epub   # 生成 dist/book-full.epub
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = PROJECT_ROOT / "dist"
BOOK_MD = DIST_DIR / "book-full.md"


def run(cmd: list) -> int:
    print("$ " + " ".join(cmd))
    return subprocess.call(cmd, cwd=PROJECT_ROOT)


def main():
    parser = argparse.ArgumentParser(description="生成 PDF/ePub 输出")
    parser.add_argument("--epub", action="store_true", help="生成 ePub 而非 PDF")
    args = parser.parse_args()

    if not shutil.which("pandoc"):
        print("错误：未检测到 pandoc，请先安装：https://pandoc.org/installing.html")
        print("PDF 输出还需要安装 LaTeX（如 TeX Live / MiKTeX）。")
        return 1

    if not BOOK_MD.exists():
        print(f"错误：未找到 {BOOK_MD}，请先运行 python scripts/build-deliverables.py")
        return 1

    DIST_DIR.mkdir(exist_ok=True)

    if args.epub:
        output = DIST_DIR / "book-full.epub"
        cmd = ["pandoc", str(BOOK_MD), "-o", str(output), "--toc", "--epub-metadata", "title=软件工程架构复用视角"]
    else:
        output = DIST_DIR / "book-full.pdf"
        cmd = [
            "pandoc",
            str(BOOK_MD),
            "-o",
            str(output),
            "--toc",
            "--pdf-engine=xelatex",
            "-V",
            "CJKmainfont=Noto Serif CJK SC",
            "-V",
            "geometry:margin=2.5cm",
        ]

    rc = run(cmd)
    if rc == 0:
        print(f"生成成功: {output}")
    else:
        print(f"生成失败，退出码: {rc}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
