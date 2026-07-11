#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可视化图库完整性检查（Figure Check）

检查项：
  1. 每个 .mmd 必须有同名 .svg          —— 缺失 → exit 1
  2. INDEX.yaml 必须覆盖全部 .mmd       —— 缺失条目 → exit 1
  3. .svg 不得落后于 .mmd（mtime 对比） —— 落后 → 警告并提示重渲染
  4. 统计图文绑定率（有 referenced_by 的图占比）输出到 reports/figure-check.md

退出码：①② 全部通过 → 0；否则 1。③④ 不影响退出码。

用法：
    python scripts/figure-check.py
    python scripts/figure-check.py --report reports/figure-check.md
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VIS_DIR = PROJECT_ROOT / "struct" / "99-reference" / "visualizations"
INDEX_PATH = VIS_DIR / "INDEX.yaml"
DEFAULT_REPORT = PROJECT_ROOT / "reports" / "figure-check.md"


def main() -> int:
    parser = argparse.ArgumentParser(description="可视化图库完整性检查")
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help="Markdown 报告输出路径")
    args = parser.parse_args()

    mmd_files = sorted(VIS_DIR.rglob("*.mmd"))

    # ① 同名 .svg 检查
    missing_svg = [m for m in mmd_files if not m.with_suffix(".svg").exists()]

    # ② INDEX.yaml 覆盖检查
    index_ids = set()
    index_error = None
    index_figures = []
    if INDEX_PATH.exists():
        try:
            data = yaml.safe_load(INDEX_PATH.read_text(encoding="utf-8"))
            index_figures = data.get("figures", []) if isinstance(data, dict) else []
            index_ids = {str(f.get("id", "")) for f in index_figures}
        except Exception as e:
            index_error = str(e)
    else:
        index_error = "INDEX.yaml 不存在"

    missing_index = []
    for m in mmd_files:
        fid = str(m.relative_to(VIS_DIR).with_suffix("")).replace("\\", "/")
        if fid not in index_ids:
            missing_index.append(fid)

    # ③ mtime 漂移检查（.svg 落后于 .mmd）
    stale = []
    for m in mmd_files:
        svg = m.with_suffix(".svg")
        if svg.exists() and svg.stat().st_mtime < m.stat().st_mtime:
            stale.append(str(m.relative_to(VIS_DIR)).replace("\\", "/"))

    # ④ 图文绑定率
    total = len(index_figures)
    bound = sum(1 for f in index_figures if f.get("referenced_by"))
    # 正文绑定：referenced_by 中含 struct/<NN-主题>/ 下的文档（排除 99-reference 元文档）
    body_bound = sum(
        1
        for f in index_figures
        if any(
            str(r).startswith("struct/") and not str(r).startswith("struct/99-reference/")
            for r in (f.get("referenced_by") or [])
        )
    )
    bind_rate = (bound / total * 100) if total else 0.0
    body_rate = (body_bound / total * 100) if total else 0.0

    # 输出控制台摘要
    print("=" * 60)
    print("可视化图库完整性检查")
    print("=" * 60)
    print(f"  .mmd 总数: {len(mmd_files)}")
    print(f"  ① 缺失 .svg: {len(missing_svg)}")
    for m in missing_svg:
        print(f"    ❌ {m.relative_to(VIS_DIR)}")
    print(f"  ② INDEX.yaml 缺失条目: {len(missing_index)}")
    for fid in missing_index:
        print(f"    ❌ {fid}")
    if index_error:
        print(f"    ❌ INDEX.yaml 读取失败: {index_error}")
    print(f"  ③ .svg 落后于 .mmd: {len(stale)}")
    for s in stale:
        print(f"    ⚠️  {s} —— 请运行 python scripts/render-visualizations.py 重渲染")
    print(f"  ④ 图文绑定率: {bound}/{total} ({bind_rate:.1f}%)，其中正文绑定: {body_bound}/{total} ({body_rate:.1f}%)")

    # 生成报告
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        "# 可视化图库检查报告",
        "",
        f"> 生成时间: {now} | 生成工具: `scripts/figure-check.py`",
        "",
        "## 检查摘要",
        "",
        "| 检查项 | 结果 |",
        "|---|---|",
        f"| ① .mmd → .svg 完整性 | {'✅ 通过' if not missing_svg else f'❌ 缺失 {len(missing_svg)} 个'} |",
        f"| ② INDEX.yaml 覆盖 | {'✅ 通过' if not missing_index and not index_error else f'❌ 缺失 {len(missing_index)} 条'} |",
        f"| ③ 渲染新鲜度（mtime） | {'✅ 全部最新' if not stale else f'⚠️ {len(stale)} 个 .svg 落后'} |",
        "",
        "## 图文绑定统计",
        "",
        f"- 图库总数（INDEX.yaml 条目）: **{total}**",
        f"- 被任意文档引用: **{bound}** ({bind_rate:.1f}%)",
        f"- 被正文文档（struct/ 主题目录）引用: **{body_bound}** ({body_rate:.1f}%)",
        "",
    ]
    if missing_svg:
        lines += ["## ❌ 缺失 .svg 的源文件", ""]
        lines += [f"- `{m.relative_to(VIS_DIR)}`" for m in missing_svg] + [""]
    if missing_index:
        lines += ["## ❌ INDEX.yaml 缺失条目", ""]
        lines += [f"- `{fid}`" for fid in missing_index] + [""]
    if stale:
        lines += [
            "## ⚠️ .svg 落后于 .mmd（需重渲染）",
            "",
            "运行 `python scripts/render-visualizations.py` 后提交更新后的 SVG。",
            "",
        ]
        lines += [f"- `{s}`" for s in stale] + [""]
    # 按类型绑定明细
    lines += ["## 按类型绑定明细", "", "| 类型 | 总数 | 已绑定 |", "|---|---|---|"]
    by_type = {}
    for f in index_figures:
        t = f.get("type", "unknown")
        by_type.setdefault(t, [0, 0])
        by_type[t][0] += 1
        if f.get("referenced_by"):
            by_type[t][1] += 1
    for t in sorted(by_type):
        n, b = by_type[t]
        lines.append(f"| {t} | {n} | {b} ({(b / n * 100) if n else 0:.0f}%) |")
    lines.append("")

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n报告已写入: {report_path}")

    ok = not missing_svg and not missing_index and not index_error
    print(f"\n{'✅ 检查通过' if ok else '❌ 检查失败'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
