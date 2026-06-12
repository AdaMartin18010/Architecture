#!/usr/bin/env python3
"""
fix-p0-standards.py
执行 Phase A P0 级标准事实修复的批量替换脚本。

用法:
    python fix-p0-standards.py --dry-run    # 预览变更
    python fix-p0-standards.py --apply      # 执行变更

注意:
    - 仅针对已知 P0 事实错误进行替换。
    - 运行前建议先备份或提交 git。
    - 替换后请重新运行 standards-version-audit.py 验证。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from dataclasses import dataclass

PROJECT_ROOT = Path("e:/_src/Architecture")


@dataclass
class Replacement:
    """描述一次替换规则。"""
    path: Path
    old: str
    new: str
    description: str


# =============================================================================
# 替换规则定义
# =============================================================================

def build_replacements() -> list[Replacement]:
    rules: list[Replacement] = []

    # -------------------------------------------------------------------------
    # 1. ISO/IEC 25010: 2024 → 2023
    # -------------------------------------------------------------------------
    iso25010_files = [
        "README.md",
        # 注意：view/ 历史文档的勘误段落故意保留 "ISO/IEC 25010:2024" 作为历史错误记录，
        # 因此不再通过本规则批量替换，避免破坏勘误上下文。
        "view/software_architecture_reuse_framework_2026.md",
        "struct/99-reference/visualizations/standard-family-tree.mmd",
    ]
    for f in iso25010_files:
        rules.append(Replacement(
            path=PROJECT_ROOT / f,
            old="ISO/IEC 25010:2024",
            new="ISO/IEC 25010:2023",
            description="ISO/IEC 25010 版本回滚 :2024 → :2023",
        ))

    # 修正 view/ 文件中的勘误说明文字
    rules.append(Replacement(
        path=PROJECT_ROOT / "view/software_architecture_reuse_framework_2026.md",
        old=("本文档中 \"ISO/IEC 25010:2023\" 已更正为 **ISO/IEC 25010:2024**。"
             "2024 版已发布并取代 2011 版，新增 AI/ML 系统质量特性考量。正文保留早期认知记录。"),
        new=("本文档中此前误将版本标注为 **ISO/IEC 25010:2024**，经权威来源复核，"
             "官方正式版为 **ISO/IEC 25010:2023**（2023-11-15 发布，取代 2011 版）。"
             "正文已统一回滚，保留历史认知记录。"),
        description="修正 view/framework 勘误说明",
    ))
    rules.append(Replacement(
        path=PROJECT_ROOT / "view/software_architecture_reuse_full_2026.md",
        old='> 2. **"ISO/IEC 25010:2023"** — 版本号滞后。ISO/IEC 25010 当前生效版本为 **2024** 版（取代 2011 版，新增 AI/ML 质量考量）。',
        new='> 2. **"ISO/IEC 25010:2024"** — 版本号标注有误。经权威来源复核，ISO/IEC 25010 官方正式版为 **2023** 版（2023-11-15 发布，取代 2011 版，新增 AI/ML 质量考量）。',
        description="修正 view/full ISO 25010 勘误说明",
    ))
    rules.append(Replacement(
        path=PROJECT_ROOT / "view/software_architecture_reuse_full_2026.md",
        old='> **对齐标准**: ISO/IEC/IEEE 42010:2022, 42020:2019, 42030:2019, DIS 42024, DIS 42042, 25010:2024, TOGAF 10, **ArchiMate 3.2** (当前官方稳定版), **ArchiMate 4.0** (厂商预发布/预览, 未获官方正式发布确认), ISO/IEC 26550:2015,',
        new='> **对齐标准**: ISO/IEC/IEEE 42010:2022, 42020:2019, 42030:2019, DIS 42024, DIS 42042, 25010:2023, TOGAF 10, **ArchiMate 3.2** (仍有效，向后兼容), **ArchiMate 4.0** (已正式发布，2026-04-27), ISO/IEC 26550:2015,',
        description="修正 view/full 头部对齐标准行",
    ))
    rules.append(Replacement(
        path=PROJECT_ROOT / "view/software_architecture_reuse_full_2026.md",
        old=("> 1. **\"ArchiMate 4.0 / ArchiMate Next\"** — ~~截至 2026 年中，The Open Group 官方仍仅列出 ArchiMate 3.1/3.2。"
             "所谓 \"ArchiMate 4.0\" 未获官方确认，属于厂商预告。~~ ~~**【已纠正】The Open Group 已于 2026-04-27 正式发布 ArchiMate 4 Specification，"
             "与 ArchiMate 3.2 向后兼容。**~~ **【二次勘误（2026-06-08）】经核查 The Open Group 官方网站，ArchiMate 4.0 尚未获官方正式发布。"
             "当前官方稳定版仍为 ArchiMate 3.2。此前\"正式发布\"声明系误判，已回退为\"厂商预发布\"。"
             "正文保留项目早期的认知记录和历次勘误记录以供对照。**"),
        new=("> 1. **\"ArchiMate 4.0 / ArchiMate Next\"** — ~~截至 2026 年中，The Open Group 官方仍仅列出 ArchiMate 3.1/3.2。"
             "所谓 \"ArchiMate 4.0\" 未获官方确认，属于厂商预告。~~ ~~**【已纠正】The Open Group 已于 2026-04-27 正式发布 ArchiMate 4 Specification，"
             "与 ArchiMate 3.2 向后兼容。**~~ ~~**【二次勘误（2026-06-08）】经核查 The Open Group 官方网站，ArchiMate 4.0 尚未获官方正式发布。"
             "当前官方稳定版仍为 ArchiMate 3.2。此前\"正式发布\"声明系误判，已回退为\"厂商预发布\"。**~~ "
             "**【三次勘误（2026-06-12）】经 The Open Group 官方新闻稿确认，ArchiMate 4 Specification 已于 2026-04-27 正式发布（Document C260, April 2026），"
             "与 ArchiMate 3.2 向后兼容。项目据此更新为正式发布状态。正文保留历次勘误记录以供对照。**"),
        description="修正 view/full ArchiMate 勘误段落",
    ))

    # -------------------------------------------------------------------------
    # 2. ISO/IEC/IEEE 42020: 2023 → 2019
    # -------------------------------------------------------------------------
    rules.append(Replacement(
        path=PROJECT_ROOT / "README.md",
        old="ISO/IEC/IEEE 42020:2023",
        new="ISO/IEC/IEEE 42020:2019",
        description="ISO/IEC/IEEE 42020 版本回滚 :2023 → :2019",
    ))

    # -------------------------------------------------------------------------
    # 3. ISO/IEC 26550: 2023/2025 → 2015
    # -------------------------------------------------------------------------
    iso26550_files = [
        "struct/99-reference/alignment-matrix-phase-c.md",
        "struct/13-emerging-trends/09-frontier-tracking/frontier-status-2026-06.md",
        "struct/01-meta-model-standards/10-mbse-reuse/mbse-ple-integration.md",
        "struct/01-meta-model-standards/09-sysml-v2/sysml2-reuse-mapping.md",
    ]
    for f in iso26550_files:
        rules.append(Replacement(
            path=PROJECT_ROOT / f,
            old="ISO/IEC 26550:2023",
            new="ISO/IEC 26550:2015",
            description="ISO/IEC 26550 版本修正 :2023 → :2015",
        ))
        rules.append(Replacement(
            path=PROJECT_ROOT / f,
            old="ISO/IEC 26550:2025",
            new="ISO/IEC 26550:2015",
            description="ISO/IEC 26550 版本修正 :2025 → :2015",
        ))

    # -------------------------------------------------------------------------
    # 4. NIST SSDF 1.2: 正式版 → Initial Public Draft
    # -------------------------------------------------------------------------
    ssdf_files = [
        "struct/10-supply-chain-security/README.md",
        "struct/10-supply-chain-security/06-case-studies/nist-ssdf-1-2-alignment.md",
    ]
    for f in ssdf_files:
        rules.append(Replacement(
            path=PROJECT_ROOT / f,
            old="NIST SSDF 1.2 正式版",
            new="NIST SSDF 1.2 Initial Public Draft",
            description="NIST SSDF 1.2 标题状态修正",
        ))
        rules.append(Replacement(
            path=PROJECT_ROOT / f,
            old="SSDF 1.2 正式版",
            new="SSDF 1.2 Initial Public Draft",
            description="NIST SSDF 1.2 正文状态修正",
        ))
        rules.append(Replacement(
            path=PROJECT_ROOT / f,
            old="正式版（Final）",
            new="Initial Public Draft（征求意见稿）",
            description="NIST SSDF 1.2 Final 状态修正",
        ))

    # 修正 nist-ssdf-1-2-alignment.md 中的具体描述
    rules.append(Replacement(
        path=PROJECT_ROOT / "struct/10-supply-chain-security/06-case-studies/nist-ssdf-1-2-alignment.md",
        old="NIST 于 2024 年发布 **SP 800-218 Rev.1**，将 SSDF 从早期征求意见稿推进为正式版本。",
        new="NIST 于 2025-12-17 发布 **SP 800-218 Rev.1 Initial Public Draft**（SSDF v1.2 征求意见稿），目前尚未转为正式版本。",
        description="NIST SSDF 1.2 发布描述修正",
    ))
    rules.append(Replacement(
        path=PROJECT_ROOT / "struct/10-supply-chain-security/06-case-studies/nist-ssdf-1-2-alignment.md",
        old="截至 2024 年底，NIST SP 800-218 Rev.1 已作为**正式版（Final）**发布。",
        new="截至 2026-06，NIST SP 800-218 Rev.1 仍为 **Initial Public Draft（征求意见稿）**，正式版发布时间待定。",
        description="NIST SSDF 1.2 发布状态修正",
    ))

    # -------------------------------------------------------------------------
    # 5. ArchiMate 4.0 正式发布状态修正
    # -------------------------------------------------------------------------
    archimate_files = [
        "struct/01-meta-model-standards/README.md",
        "struct/01-meta-model-standards/04-archimate-4/archimate-iso-mapping.md",
        "struct/01-meta-model-standards/02-togaf-10-alignment/detailed-mapping.md",
        "struct/01-meta-model-standards/05-swebok-v4/swebok-alignment.md",
        "struct/01-meta-model-standards/01-iso-420xx-family/iso-42024-42042-dis-alignment.md",
        "struct/07-formal-verification/02-alloy/cross-layer-mapping.md",
        "struct/99-reference/standards-index/master-alignment-matrix.md",
        "struct/99-reference/book-outline.md",
        "struct/99-reference/book-outline-v2.md",
        "struct/99-reference/templates/citation-standard.md",
        "struct/SUBSEQUENT_PLAN_2026.md",
        "struct/99-reference/audit/comprehensive-gap-analysis-2026-06-08.md",
        "struct/99-reference/audit/network-authority-alignment-report-2026-06-10.md",
        "struct/99-reference/tools/standard-tracker.py",
        "struct/99-reference/tools/standard-tracker-report.md",
        "view/software_architecture_reuse_full_2026.md",
        "view/software_architecture_reuse_extension_2026.md",
    ]
    for f in archimate_files:
        # 将“厂商预发布/未获官方确认/预览”等表述改为正式发布。
        # 注意：仅替换与 ArchiMate 4.0 直接相邻的“厂商预发布”，避免触及历史勘误段落中的二次回退记录。
        rules.append(Replacement(
            path=PROJECT_ROOT / f,
            old="ArchiMate 4.0 (厂商预发布",
            new="ArchiMate 4.0 (已正式发布",
            description="ArchiMate 4.0 状态修正：厂商预发布 → 已正式发布",
        ))
        rules.append(Replacement(
            path=PROJECT_ROOT / f,
            old="**ArchiMate 4.0** (厂商预发布",
            new="**ArchiMate 4.0** (已正式发布",
            description="ArchiMate 4.0 状态修正：厂商预发布 → 已正式发布",
        ))
        # 注意：不再全局替换“未获官方确认”。历史勘误段落（如 view/ 文件、CHANGELOG）
        # 故意保留“未获官方确认”以记录早期认知；当前状态已在各自头部/正文中修正为正式发布。

    # 针对 CHANGELOG 中的特殊勘误记录，添加补充说明（已合并至 2026-06-12 Phase A P0 条目，此处保留规则但标记为可选历史记录）
    # 若未来需要在此处也追加说明，可取消注释并调整 old/new 以匹配当前 CHANGELOG 文本。
    pass

    return rules


# =============================================================================
# 执行逻辑
# =============================================================================

def apply_rules(rules: list[Replacement], dry_run: bool) -> tuple[int, int]:
    """应用替换规则，返回 (处理文件数, 替换次数)。"""
    file_count = 0
    total_replacements = 0

    for rule in rules:
        if not rule.path.exists():
            print(f"[SKIP] 文件不存在: {rule.path.relative_to(PROJECT_ROOT)}")
            continue

        try:
            content = rule.path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[ERROR] 无法读取 {rule.path}: {e}")
            continue

        if rule.old not in content:
            continue

        file_count += 1
        occurrences = content.count(rule.old)
        total_replacements += occurrences
        new_content = content.replace(rule.old, rule.new)

        action = "[DRY-RUN 将执行]" if dry_run else "[APPLIED]"
        print(f"{action} {rule.path.relative_to(PROJECT_ROOT)}: {rule.description} (×{occurrences})")

        if not dry_run:
            try:
                rule.path.write_text(new_content, encoding="utf-8")
            except Exception as e:
                print(f"[ERROR] 无法写入 {rule.path}: {e}")

    return file_count, total_replacements


def main() -> int:
    parser = argparse.ArgumentParser(description="P0 标准事实修复脚本")
    parser.add_argument("--apply", action="store_true", help="执行替换（默认仅预览）")
    args = parser.parse_args()

    dry_run = not args.apply
    rules = build_replacements()

    print(f"{'='*60}")
    print(f"Phase A P0 标准事实修复")
    print(f"模式: {'预览 (dry-run)' if dry_run else '执行 (--apply)'}")
    print(f"规则数: {len(rules)}")
    print(f"{'='*60}\n")

    file_count, total = apply_rules(rules, dry_run)

    print(f"\n{'='*60}")
    print(f"处理文件: {file_count}")
    print(f"总替换次数: {total}")
    if dry_run:
        print("本次为预览，未实际修改文件。确认无误后追加 --apply 执行。")
    print(f"{'='*60}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
