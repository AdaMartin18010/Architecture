#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 链接检查器

扫描 struct/、view/、reports/ 及根 README.md，检测本地相对链接的失效情况：
- 文件不存在（missing-file）
- 目录链接缺少 README.md/index.md（missing-dir-index）
- 锚点不存在（bad-anchor）
- 同文件内锚点不存在（bad-self-anchor）

注意：dist/ 为生成产物，其链接由生成脚本保证，本脚本不扫描 dist/。

用法：
    python scripts/link-checker.py
    python scripts/link-checker.py --json reports/link-checker.json
    python scripts/link-checker.py --report reports/link-checker.md
"""

import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Tuple, Optional, Dict, Set
from collections import defaultdict


@dataclass
class BrokenLink:
    source: str
    line: int
    text: str
    target: str
    kind: str
    suggestion: str = ""


def extract_links(text: str) -> List[Tuple[str, str, int]]:
    """提取 Markdown 内联链接，跳过代码块。"""
    links = []
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


def _github_slug(title: str) -> str:
    """生成接近 GitHub 风格的标题锚点 slug。"""
    s = title.lower()
    s = s.replace("&", " ")
    # 保留字母、数字、中文、空格、连字符；移除其他标点与格式符号
    s = re.sub(r"[^\w\s\-]", "", s, flags=re.UNICODE)
    s = s.replace(" ", "-")
    # 保留原始多连字符，同时生成单连字符变体，便于容错匹配
    return s.strip("-")


def _build_anchors(text: str) -> Set[str]:
    """预计算文件中所有可用锚点（含显式锚点与标题锚点）。"""
    anchors: Set[str] = set()
    for line in text.splitlines():
        # 显式锚点 {#id}
        for m in re.finditer(r"\{#([^}]+)\}", line):
            anchors.add(m.group(1).lower())

    # 标题锚点，重复标题按 GitHub 规则追加 -1, -2, ...
    seen: Dict[str, int] = defaultdict(int)
    for line in text.splitlines():
        m = re.match(r"^#{1,6}\s+(.+?)(?:\s*\{[^}]*\})?\s*$", line)
        if m:
            title = m.group(1).strip()
            slug = _github_slug(title)
            if not slug:
                continue
            count = seen[slug]
            seen[slug] += 1
            anchors.add(slug)
            if count > 0:
                anchors.add(f"{slug}-{count}")
            # 同时加入单连字符变体
            single = re.sub(r"-+", "-", slug).strip("-")
            anchors.add(single)
            if count > 0:
                anchors.add(f"{single}-{count}")
    return anchors


def resolve_link(base_file: Path, link: str) -> Tuple[Optional[Path], Optional[str]]:
    """解析相对链接为绝对路径和锚点。外部 URL 返回 (None, None)。"""
    link = link.strip()
    if not link:
        return None, None
    if re.match(r"^[a-z][a-z0-9+.-]*://", link, re.IGNORECASE):
        return None, None
    if link.startswith("mailto:"):
        return None, None
    if link.startswith("#"):
        return None, link[1:] or None

    anchor = None
    if "#" in link:
        link, anchor = link.split("#", 1)
    if not link:
        return None, anchor

    target = (base_file.parent / link).resolve()
    return target, anchor


def target_exists(target: Path) -> bool:
    if target.exists():
        return True
    if target.is_dir() or target.suffix == "":
        for name in ("README.md", "index.md", "readme.md"):
            if (target / name).exists():
                return True
    return False


def scan(project_root: Path, ignore_patterns: List[str], strict_self_anchors: bool = False) -> List[BrokenLink]:
    scan_dirs = [
        project_root / "struct",
        project_root / "view",
        project_root / "reports",
    ]
    md_files: List[Path] = []
    for d in scan_dirs:
        if d.exists():
            md_files.extend(d.rglob("*.md"))
    root_readme = project_root / "README.md"
    if root_readme.exists():
        md_files.append(root_readme)
    md_files = sorted(set(md_files))

    # 预加载内容并预计算锚点
    file_cache: Dict[str, str] = {}
    anchor_cache: Dict[str, Set[str]] = {}
    for md_file in md_files:
        rel = md_file.relative_to(project_root).as_posix()
        if any(pat in rel for pat in ignore_patterns):
            continue
        text = md_file.read_text(encoding="utf-8", errors="replace")
        file_cache[rel] = text
        anchor_cache[rel] = _build_anchors(text)

    broken: List[BrokenLink] = []
    for rel, text in file_cache.items():
        md_file = project_root / rel
        for link_text, link_target, lineno in extract_links(text):
            target, anchor = resolve_link(md_file, link_target)

            if target is None and anchor is None:
                continue

            if target is None:
                # 同文件锚点在不同渲染器下生成规则差异大，默认不严格检查
                if strict_self_anchors and anchor and anchor.lower() not in anchor_cache[rel]:
                    broken.append(BrokenLink(
                        source=rel,
                        line=lineno,
                        text=link_text,
                        target=f"#{anchor}",
                        kind="bad-self-anchor",
                        suggestion="补充同文件内对应标题或显式锚点 {#...}",
                    ))
                continue

            if not target_exists(target):
                kind = "missing-dir-index" if (target.is_dir() or link_target.rstrip().endswith("/")) else "missing-file"
                suggestion = ""
                if kind == "missing-dir-index":
                    suggestion = "在目录下添加 README.md，或将链接改为具体 .md 文件"
                else:
                    suggestion = "检查相对路径或文件名拼写"
                broken.append(BrokenLink(
                    source=rel,
                    line=lineno,
                    text=link_text,
                    target=link_target,
                    kind=kind,
                    suggestion=suggestion,
                ))
                continue

            if anchor:
                target_rel = target.relative_to(project_root).as_posix()
                target_anchors = anchor_cache.get(target_rel, set())
                if anchor.lower() not in target_anchors:
                    broken.append(BrokenLink(
                        source=rel,
                        line=lineno,
                        text=link_text,
                        target=link_target,
                        kind="bad-anchor",
                        suggestion="在目标文件补充对应标题或显式锚点 {#...}",
                    ))

    return broken


def write_json_report(report_path: Path, broken: List[BrokenLink]):
    report_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "summary": {
            "total_broken": len(broken),
            "by_kind": defaultdict(int),
        },
        "broken_links": [asdict(b) for b in broken],
    }
    for b in broken:
        data["summary"]["by_kind"][b.kind] += 1
    report_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_md_report(report_path: Path, broken: List[BrokenLink]):
    report_path.parent.mkdir(parents=True, exist_ok=True)
    by_kind = defaultdict(int)
    for b in broken:
        by_kind[b.kind] += 1

    lines = [
        "# Markdown 链接检查报告",
        "",
        "## 概览",
        "",
        f"- 失效链接总数: **{len(broken)}**",
    ]
    if by_kind:
        lines.append("- 按类型分布:")
        for kind, count in sorted(by_kind.items(), key=lambda x: -x[1]):
            lines.append(f"  - {kind}: {count}")
    else:
        lines.append("- 按类型分布: 无")

    lines.extend(["", "## 失效链接详情", ""])
    if not broken:
        lines.append("✅ 未发现失效链接。")
    else:
        by_source = defaultdict(list)
        for b in broken:
            by_source[b.source].append(b)
        for source, items in sorted(by_source.items()):
            lines.append(f"### {source}")
            for b in items:
                lines.append(f"- 第 {b.line} 行: [{b.text}]({b.target}) — `{b.kind}`")
                if b.suggestion:
                    lines.append(f"  - 建议: {b.suggestion}")
            lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Markdown 链接检查器")
    parser.add_argument("--json", metavar="PATH", help="输出 JSON 报告")
    parser.add_argument("--report", metavar="PATH", help="输出 Markdown 报告")
    parser.add_argument(
        "--ignore",
        metavar="PATTERN",
        nargs="*",
        default=["_HISTORICAL_"],
        help="忽略的匹配模式（默认: _HISTORICAL_）",
    )
    parser.add_argument(
        "--strict-anchors",
        action="store_true",
        help="严格检查同文件锚点（默认关闭，因各渲染器规则差异大）",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    broken = scan(project_root, args.ignore, strict_self_anchors=args.strict_anchors)

    print(f"Markdown 链接检查完成: {len(broken)} 个失效链接")
    if broken:
        by_kind = defaultdict(int)
        for b in broken:
            by_kind[b.kind] += 1
        for kind, count in sorted(by_kind.items(), key=lambda x: -x[1]):
            print(f"  {kind}: {count}")

    if args.json:
        write_json_report(Path(args.json), broken)
        print(f"JSON 报告已保存: {args.json}")
    if args.report:
        write_md_report(Path(args.report), broken)
        print(f"Markdown 报告已保存: {args.report}")

    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
