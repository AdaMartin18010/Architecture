#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模板 Padding 治理脚本（ratchet 硬门控版）

扫描 struct/ 下所有 Markdown 文件，检测末尾或正文中机械重复的
「补充说明 / 概念定义 / 示例 / 反例 / 权威来源 / 分析 / 参考文献 /
延伸阅读 / 附录」等模板块，统计其占总行数比例，并输出 Top 20
padding 占比最高的文件列表。

门控机制（三层）：
  1. 硬上限（hard cap，默认 60%）：任何未豁免文件 padding 占比 ≥ 60%
     即 exit 1——此占比已无正当语境，视为模板污染。
  2. Ratchet 基线（scripts/.padding-baseline.json）：记录当前超过软阈值
     （30%）的未豁免文件。基线内文件仅警告；若占比较基线记录恶化
     （> baseline + 容差）也 exit 1。整改后用 --update-baseline 收紧。
  3. 新增超限：未豁免、不在基线内的文件占比 > 30% → exit 1。

豁免（scripts/.padding-exemptions.json）：per-file 豁免，依据
  struct/99-reference/templates/content-block-guideline.md §4
  （README 导航文件、99-reference/templates|audit|tools、历史归档）。
  豁免文件跳过全部门控，仅在报告中标注。

用法：
    python scripts/template-padding-check.py
    python scripts/template-padding-check.py --output reports/template-padding-report.md
    python scripts/template-padding-check.py --update-baseline   # 用当前超限文件收紧基线

退出码：
    0  无新增超限、无超硬上限、基线无恶化
    1  存在新增超限文件 / 超硬上限文件 / 基线恶化
    2  配置错误（基线/豁免文件损坏等）
"""

import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
BASELINE_FILE = SCRIPT_DIR / ".padding-baseline.json"
EXEMPTIONS_FILE = SCRIPT_DIR / ".padding-exemptions.json"

DEFAULT_THRESHOLD = 30.0
DEFAULT_HARD_CAP = 60.0
# 基线恶化容差（百分点）：避免行数微抖动导致误报
BASELINE_TOLERANCE = 1.0


@dataclass
class PaddingRecord:
    path: str
    total_lines: int
    padding_lines: int
    ratio: float
    matched_sections: List[str] = field(default_factory=list)
    status: str = ""  # "", "EXEMPT", "BASELINE", "BASELINE_WORSE", "NEW", "HARD_CAP"


# 被视为模板 Padding 的二级/三级/四级标题模式。
# 这些标题通常出现在文件末尾，机械重复「概念定义+示例+反例+权威来源」组合。
PADDING_HEADING_PATTERNS = [
    r"^(#{2,4})\s+补充说明",
    r"^(#{2,4})\s+概念定义\s*$",
    r"^(#{2,4})\s+示例\s*$",
    r"^(#{2,4})\s+反例\s*$",
    r"^(#{2,4})\s+权威来源\s*$",
    r"^(#{2,4})\s+分析\s*$",
    r"^(#{2,4})\s+参考文献\s*$",
    r"^(#{2,4})\s+延伸阅读\s*$",
    r"^(#{2,4})\s+附录\s*$",
]


def load_exemptions() -> Dict[str, str]:
    """加载 per-file 豁免配置，返回 path -> reason。"""
    if not EXEMPTIONS_FILE.exists():
        return {}
    try:
        data = json.loads(EXEMPTIONS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"错误：豁免配置 {EXEMPTIONS_FILE} 解析失败：{e}", file=sys.stderr)
        sys.exit(2)
    raw = data.get("exemptions", {})
    result = {}
    for path, val in raw.items():
        result[path] = val.get("reason", "") if isinstance(val, dict) else str(val)
    return result


def load_baseline() -> Dict[str, float]:
    """加载 ratchet 基线，返回 path -> 基线记录的占比。"""
    if not BASELINE_FILE.exists():
        return {}
    try:
        data = json.loads(BASELINE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"错误：基线文件 {BASELINE_FILE} 解析失败：{e}", file=sys.stderr)
        sys.exit(2)
    result = {}
    for path, val in data.get("files", {}).items():
        result[path] = float(val.get("ratio", 0.0)) if isinstance(val, dict) else float(val)
    return result


def write_baseline(records: List[PaddingRecord], threshold: float) -> None:
    """用当前超限且未豁免的文件重写基线（只增不删已整改文件）。"""
    files = {
        r.path: {"ratio": round(r.ratio, 2), "note": "auto-updated by --update-baseline"}
        for r in records
        if r.ratio > threshold and r.status != "EXEMPT"
    }
    data = {
        "version": 1,
        "description": (
            "template-padding-check.py 的 ratchet 基线：记录当前 padding 占比超过阈值"
            f"（{threshold:.0f}%）且未豁免的文件。基线内文件仅警告；新增超限文件或基线文件"
            "占比恶化即 exit 1。整改后用 --update-baseline 收紧基线（只减不增）。"
        ),
        "threshold": threshold,
        "files": files,
    }
    BASELINE_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def calculate_padding(lines: List[str]) -> tuple:
    """返回 (模板块行数, 命中的小节标题列表)。"""
    is_padding = [False] * len(lines)
    patterns = [re.compile(p) for p in PADDING_HEADING_PATTERNS]
    matched_sections: List[str] = []
    i = 0
    while i < len(lines):
        matched = False
        for p in patterns:
            m = p.match(lines[i])
            if m:
                level = len(m.group(1))
                title = lines[i].strip().lstrip("#").strip()
                matched_sections.append(title)
                is_padding[i] = True
                i += 1
                while i < len(lines):
                    m2 = re.match(r"^(#{1,6})\s", lines[i])
                    if m2 and len(m2.group(1)) <= level:
                        break
                    is_padding[i] = True
                    i += 1
                matched = True
                break
        if not matched:
            i += 1
    return sum(is_padding), matched_sections


def scan(root: Path) -> List[PaddingRecord]:
    records: List[PaddingRecord] = []
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root).as_posix()
        # 跳过模板、审计、工具说明自身，避免自我污染统计
        if any(
            p in rel
            for p in (
                "99-reference/templates/",
                "99-reference/audit/",
                "99-reference/tools/",
                "_HISTORICAL_",
                "plans-tasks/",
            )
        ):
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        total = len(lines)
        if total == 0:
            continue
        padding, sections = calculate_padding(lines)
        ratio = padding / total * 100
        records.append(
            PaddingRecord(
                path=rel,
                total_lines=total,
                padding_lines=padding,
                ratio=ratio,
                matched_sections=sections,
            )
        )
    records.sort(key=lambda r: r.ratio, reverse=True)
    return records


def classify(
    records: List[PaddingRecord],
    exemptions: Dict[str, str],
    baseline: Dict[str, float],
    threshold: float,
    hard_cap: float,
) -> List[PaddingRecord]:
    """为每条记录标注门控状态。"""
    for r in records:
        if r.path in exemptions:
            r.status = "EXEMPT"
        elif r.ratio >= hard_cap:
            r.status = "HARD_CAP"
        elif r.ratio > threshold:
            if r.path in baseline:
                if r.ratio > baseline[r.path] + BASELINE_TOLERANCE:
                    r.status = "BASELINE_WORSE"
                else:
                    r.status = "BASELINE"
            else:
                r.status = "NEW"
    return records


def generate_report(
    records: List[PaddingRecord],
    exemptions: Dict[str, str],
    baseline: Dict[str, float],
    threshold: float,
    hard_cap: float,
    top_n: int = 20,
) -> str:
    over = [r for r in records if r.ratio > threshold]
    lines = [
        "# Template Padding 治理报告",
        "",
        "> 生成命令：`python scripts/template-padding-check.py`",
        "",
        "## 统计概览",
        "",
        f"- 扫描文件数：{len(records)}",
        f"- 平均 Padding 占比：{sum(r.ratio for r in records) / len(records):.2f}%" if records else "- 平均 Padding 占比：0.00%",
        f"- 最高 Padding 占比：{records[0].ratio:.2f}%" if records else "- 最高 Padding 占比：0.00%",
        f"- 占比超过 {threshold:.0f}% 的文件数：{len(over)}"
        + f"（其中豁免 {sum(1 for r in over if r.status == 'EXEMPT')}，"
        + f"基线 {sum(1 for r in over if r.status in ('BASELINE', 'BASELINE_WORSE'))}，"
        + f"新增 {sum(1 for r in over if r.status == 'NEW')}）",
        f"- 门控配置：软阈值 {threshold:.0f}%（ratchet 基线），硬上限 {hard_cap:.0f}%（即失败）",
        "",
        f"## Top {top_n} Padding 占比文件",
        "",
        "| 排名 | 文件 | 总行数 | 模板块行数 | 占比 | 状态 | 命中板块 |",
        "|---:|---|---:|---:|---:|---|---|",
    ]
    status_label = {
        "EXEMPT": "🛡️ 豁免",
        "BASELINE": "📌 基线",
        "BASELINE_WORSE": "🔴 基线恶化",
        "NEW": "❌ 新增超限",
        "HARD_CAP": "❌ 超硬上限",
        "": "",
    }
    for idx, r in enumerate(records[:top_n], start=1):
        sections = "、".join(r.matched_sections[:4])
        if len(r.matched_sections) > 4:
            sections += "…"
        lines.append(
            f"| {idx} | `{r.path}` | {r.total_lines} | {r.padding_lines} "
            f"| {r.ratio:.2f}% | {status_label.get(r.status, '')} | {sections} |"
        )

    lines.extend(
        [
            "",
            "## 说明",
            "",
            "1. 「模板块」指机械重复的「补充说明 / 概念定义 / 示例 / 反例 / 权威来源 / 分析 / 参考文献 / 延伸阅读 / 附录」等小节。",
            "2. 占比 = 模板块行数 / 文件总行数 × 100%。",
            f"3. 门控：占比 ≥ {hard_cap:.0f}% 直接失败；> {threshold:.0f}% 的新增文件失败；基线文件（`scripts/.padding-baseline.json`）仅警告但恶化即失败。",
            "4. 豁免清单见 `scripts/.padding-exemptions.json`，依据 [`content-block-guideline.md`](../struct/99-reference/templates/content-block-guideline.md) §4。",
        ]
    )
    if exemptions:
        lines += ["", "## 豁免清单", ""]
        for path, reason in sorted(exemptions.items()):
            lines.append(f"- `{path}` — {reason}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="检测 Markdown 文件中的模板 Padding 占比（ratchet 硬门控）")
    parser.add_argument(
        "--output",
        default="reports/template-padding-report.md",
        help="报告输出路径（默认：reports/template-padding-report.md）",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="Top N 文件数（默认：20）",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help=f"软阈值百分比（默认：{DEFAULT_THRESHOLD:.0f}）",
    )
    parser.add_argument(
        "--hard-cap",
        type=float,
        default=DEFAULT_HARD_CAP,
        help=f"硬上限百分比，超过即 exit 1（默认：{DEFAULT_HARD_CAP:.0f}）",
    )
    parser.add_argument(
        "--update-baseline",
        action="store_true",
        help="用当前超限且未豁免的文件重写 ratchet 基线（整改后收紧用）",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    struct_root = project_root / "struct"

    exemptions = load_exemptions()
    baseline = load_baseline()

    records = scan(struct_root)
    records = classify(records, exemptions, baseline, args.threshold, args.hard_cap)

    if args.update_baseline:
        write_baseline(records, args.threshold)
        print(f"基线已更新：{BASELINE_FILE}")
        # --update-baseline 是运维操作（接受现状为基线），写入后直接退出，不做门控判定
        report = generate_report(records, exemptions, load_baseline(), args.threshold, args.hard_cap, top_n=args.top)
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = project_root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(f"报告已保存：{output_path}")
        return 0

    report = generate_report(records, exemptions, baseline, args.threshold, args.hard_cap, top_n=args.top)

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = project_root / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    hard_cap_hits = [r for r in records if r.status == "HARD_CAP"]
    worse_hits = [r for r in records if r.status == "BASELINE_WORSE"]
    new_hits = [r for r in records if r.status == "NEW"]
    baseline_hits = [r for r in records if r.status == "BASELINE"]

    if records:
        top = records[0]
        print(f"扫描完成：{len(records)} 个文件，最高占比 {top.ratio:.2f}%（{top.path}）")
        print(f"报告已保存：{output_path}")
        for r in baseline_hits:
            print(
                f"WARNING: 基线文件 {r.path} 占比 {r.ratio:.2f}% 超过 {args.threshold:.0f}%"
                f"（基线记录 {baseline[r.path]:.2f}%，仅警告）",
                file=sys.stderr,
            )
        for r in hard_cap_hits:
            print(
                f"FAIL: {r.path} 占比 {r.ratio:.2f}% 达到硬上限 {args.hard_cap:.0f}%",
                file=sys.stderr,
            )
        for r in worse_hits:
            print(
                f"FAIL: {r.path} 占比 {r.ratio:.2f}% 较基线 {baseline[r.path]:.2f}% 恶化",
                file=sys.stderr,
            )
        for r in new_hits:
            print(
                f"FAIL: {r.path} 占比 {r.ratio:.2f}% 超过 {args.threshold:.0f}%（新增超限，"
                "请精简整改或经评审后加入豁免/基线）",
                file=sys.stderr,
            )
    else:
        print("扫描完成：未找到 Markdown 文件。")

    if hard_cap_hits or worse_hits or new_hits:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
