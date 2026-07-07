#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量渲染 visualizations/ 下的所有 .mmd 文件为 SVG。
用法: python scripts/render-visualizations.py
"""

import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VIS_DIR = PROJECT_ROOT / "struct" / "99-reference" / "visualizations"


def render_one(mmd_path: Path) -> tuple:
    svg_path = mmd_path.with_suffix(".svg")
    try:
        # Windows 下使用 mmdc.cmd，避免 POSIX shell 脚本无法直接执行
        cmd = "mmdc.cmd" if sys.platform == "win32" else "mmdc"
        result = subprocess.run(
            [cmd, "-i", str(mmd_path), "-o", str(svg_path), "-b", "transparent"],
            capture_output=True,
            text=True,
            timeout=120,
            shell=(sys.platform == "win32"),
        )
        if result.returncode == 0:
            return (mmd_path, True, None)
        else:
            return (mmd_path, False, result.stderr[:500])
    except Exception as e:
        return (mmd_path, False, str(e)[:500])


def main():
    mmd_files = sorted(VIS_DIR.rglob("*.mmd"))
    print(f"发现 {len(mmd_files)} 个 Mermaid 源文件，开始渲染...")

    success = 0
    failed = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(render_one, f): f for f in mmd_files}
        for future in as_completed(futures):
            path, ok, err = future.result()
            rel = path.relative_to(VIS_DIR)
            if ok:
                success += 1
                print(f"  ✅ {rel}")
            else:
                failed.append((rel, err))
                print(f"  ❌ {rel}: {err}")

    print(f"\n渲染完成: {success}/{len(mmd_files)} 成功")
    if failed:
        print("\n失败文件:")
        for rel, err in failed:
            print(f"  - {rel}: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
