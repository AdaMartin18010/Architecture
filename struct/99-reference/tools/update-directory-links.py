#!/usr/bin/env python3
"""
update-directory-links.py
在目录重命名后，批量更新项目文件中的路径引用。

用法:
    python update-directory-links.py --dry-run    # 预览
    python update-directory-links.py --apply      # 执行
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path("e:/_src/Architecture")
STRUCT_ROOT = PROJECT_ROOT / "struct"

# 旧目录名 -> 新目录名（仅目录名，不含父路径）
RENAME_MAP = {
    # 03-application-architecture-reuse
    "03-serverless": "04-serverless",
    "04-data-architecture": "05-data-architecture",
    "04-event-driven": "06-event-driven",
    "05-cloud-native-patterns": "07-cloud-native-patterns",
    "06-service-mesh": "08-service-mesh",
    "07-eda-cqrs": "09-eda-cqrs",
    "07-tosca-dmn-platform": "10-tosca-dmn-platform",
    "08-idp-practices": "11-idp-practices",
    # 07-formal-verification
    "06-vv-standards": "07-vv-standards",
    "07-emerging-trends": "08-emerging-trends",
    "08-comparative-matrices": "09-comparative-matrices",
    # 10-supply-chain-security
    "04-zero-trust-supply-chain": "05-zero-trust-supply-chain",
    "05-case-studies": "06-case-studies",
    "06-owasp-scvs": "07-owasp-scvs",
    "07-guac-supply-chain": "08-guac-supply-chain",
    "08-owasp-asvs": "09-owasp-asvs",
    "09-owasp-top10-2025": "10-owasp-top10-2025",
    "10-osps-baseline": "11-osps-baseline",
    "11-nist-ssdf-update": "12-nist-ssdf-update",
    # 12-ai-native-reuse
    "03-hybrid-a2a-mcp-poc": "04-hybrid-a2a-mcp-poc",
    "04-probabilistic-contracts": "05-probabilistic-contracts",
    "05-ai-governance": "06-ai-governance",
    "05-conformal-prediction": "07-conformal-prediction",
    # 13-emerging-trends
    "04-rust-ecosystem": "05-rust-ecosystem",
    "05-regtech-ai": "06-regtech-ai",
    "06-green-software": "07-green-software",
}


def update_file(path: Path, dry_run: bool) -> int:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[WARN] 无法读取 {path}: {e}", file=sys.stderr)
        return 0

    new_text = text
    total = 0
    for old_name, new_name in RENAME_MAP.items():
        # 仅在路径上下文中替换：前面是 / 或 \ 或 . 或开头；后面是 / 或 \ 或 . 或结尾
        pattern = re.compile(r"(?<=[/\\.\s])" + re.escape(old_name) + r"(?=[/\\.\s]|$)")
        matches = list(pattern.finditer(new_text))
        if matches:
            total += len(matches)
            new_text = pattern.sub(new_name, new_text)

    if total and not dry_run:
        path.write_text(new_text, encoding="utf-8")

    return total


def main() -> int:
    parser = argparse.ArgumentParser(description="更新目录重命名后的路径引用")
    parser.add_argument("--apply", action="store_true", help="执行替换")
    args = parser.parse_args()
    dry_run = not args.apply

    files = list(PROJECT_ROOT.rglob("*.md"))
    files += list(PROJECT_ROOT.rglob("*.py"))
    files = [p for p in files if ".venv" not in p.parts and "node_modules" not in p.parts]

    changed: dict[Path, int] = {}
    for f in files:
        count = update_file(f, dry_run)
        if count:
            changed[f] = count

    print(f"{'='*60}")
    print(f"目录链接更新")
    print(f"模式: {'预览 (dry-run)' if dry_run else '执行 (--apply)'}")
    print(f"更新文件数: {len(changed)}")
    print(f"总替换处数: {sum(changed.values())}")
    print(f"{'='*60}")

    for f, count in sorted(changed.items()):
        print(f"  {f.relative_to(PROJECT_ROOT)}: {count} 处")

    if dry_run:
        print("\n本次为预览，未实际修改文件。确认无误后追加 --apply 执行。")

    return 0


if __name__ == "__main__":
    sys.exit(main())
