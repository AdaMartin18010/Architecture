#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
struct/ → view/ 同步与差异报告脚本

功能：
- 默认生成差异报告，不直接修改 view/
- --generate 参数从 struct/ 重新生成 view/ 卷册
- --topic 参数按主题选择同步范围（如 01-meta-model-standards）
- 将每个主题的 Markdown 文件聚合到一个 view 卷册中

用法：
    python scripts/sync-view-from-struct.py
    python scripts/sync-view-from-struct.py --generate
    python scripts/sync-view-from-struct.py --topic 01-meta-model-standards --generate
    python scripts/sync-view-from-struct.py --report reports/view-diff-report.md
"""

import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime


@dataclass
class DiffEntry:
    topic: str
    view_file: Path
    status: str  # missing, newer, older, same, orphan
    struct_files: List[str] = field(default_factory=list)
    message: str = ""


VIEW_HEADER_TEMPLATE = """# {title}

> **版本**: {date}
> **定位**: 由 `struct/{topic}` 自动聚合生成的视角卷册（view volume）
> **生成命令**: `python scripts/sync-view-from-struct.py --topic {topic} --generate`
> **说明**: 本文件为 struct/ 的只读聚合视角，修改请直接在 struct/ 对应文件进行。

---

"""


def _topic_dirs(struct_dir: Path) -> List[Path]:
    """返回 struct/ 下所有主题目录（01-, 02-, ...）"""
    topics = []
    if not struct_dir.exists():
        return topics
    for child in sorted(struct_dir.iterdir()):
        if child.is_dir() and re.match(r"^\d{2}-", child.name):
            topics.append(child)
    return topics


def _collect_topic_files(topic_dir: Path) -> List[Path]:
    """递归收集主题目录下的所有 Markdown 文件"""
    files = []
    if not topic_dir.exists():
        return files
    for md in sorted(topic_dir.rglob("*.md")):
        rel = md.relative_to(topic_dir)
        # 跳过审计、CHANGELOG、plans-tasks 等元数据
        rel_posix = rel.as_posix()
        if any(sp in rel_posix for sp in ["99-reference/audit/", "CHANGELOG", "frontier-tracking/", "plans-tasks/"]):
            continue
        files.append(md)
    return files


def _view_file_for_topic(view_dir: Path, topic: str) -> Path:
    """根据主题名生成 view 卷册文件名"""
    normalized = topic.lower().replace("_", "-")
    return view_dir / f"volume-{normalized}.md"


def _extract_first_heading(text: str) -> str:
    """提取文件的第一个 # 标题"""
    for line in text.splitlines():
        m = re.match(r"^#\s+(.+)$", line)
        if m:
            return m.group(1).strip()
    return "未命名章节"


def _rewrite_links(text: str, source_file: Path, struct_root: Path) -> str:
    """将文本中的相对 Markdown 链接重写为 struct/ 根目录相对路径，便于 view/ 卷册解析。"""
    link_re = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")

    def repl(m: re.Match) -> str:
        link_text = m.group(1)
        target = m.group(2).strip()
        # 保留锚点
        fragment = ""
        if "#" in target:
            target, fragment = target.split("#", 1)
            fragment = "#" + fragment
        # 跳过外部 URL、mailto、空链接
        if not target or re.match(r"^[a-z][a-z0-9+.-]*://", target, re.IGNORECASE) or target.startswith("mailto:"):
            return m.group(0)
        try:
            resolved = (source_file.parent / target).resolve()
            # 确保解析后的目标在 struct_root 内
            if struct_root in resolved.parents or resolved == struct_root:
                new_target = resolved.relative_to(struct_root).as_posix()
                return f"[{link_text}]({new_target}{fragment})"
        except Exception:
            pass
        return m.group(0)

    return link_re.sub(repl, text)


def generate_view_volume(topic_dir: Path, view_file: Path, project_root: Path) -> None:
    """将主题目录下的文件聚合并写入 view 卷册"""
    files = _collect_topic_files(topic_dir)
    if not files:
        return

    view_file.parent.mkdir(parents=True, exist_ok=True)
    title = _extract_first_heading(files[0].read_text(encoding="utf-8")) if files else topic_dir.name
    date = datetime.now().strftime("%Y-%m-%d")
    struct_root = project_root / "struct"

    parts = [VIEW_HEADER_TEMPLATE.format(title=title, date=date, topic=topic_dir.name)]
    parts.append(f"## 目录\n\n")
    for idx, md in enumerate(files, start=1):
        heading = _extract_first_heading(md.read_text(encoding="utf-8"))
        rel = md.relative_to(struct_root).as_posix()
        parts.append(f"{idx}. [{heading}]({rel})")
    parts.append("\n---\n")

    for md in files:
        text = md.read_text(encoding="utf-8")
        text = _rewrite_links(text, md, struct_root)
        rel = md.relative_to(struct_root).as_posix()
        parts.append(f"\n<!-- SOURCE: struct/{rel} -->\n")
        parts.append(text)
        parts.append("\n---\n")

    view_file.write_text("\n".join(parts), encoding="utf-8")


def compute_diff(struct_dir: Path, view_dir: Path, topic_filter: Optional[str] = None) -> List[DiffEntry]:
    """计算 struct/ 与 view/ 之间的差异"""
    diffs: List[DiffEntry] = []
    topics = _topic_dirs(struct_dir)

    for topic_dir in topics:
        if topic_filter and topic_dir.name != topic_filter:
            continue

        struct_files = _collect_topic_files(topic_dir)
        view_file = _view_file_for_topic(view_dir, topic_dir.name)

        if not struct_files:
            continue

        if not view_file.exists():
            diffs.append(DiffEntry(
                topic=topic_dir.name,
                view_file=view_file,
                status="missing",
                struct_files=[f.relative_to(struct_dir).as_posix() for f in struct_files],
                message=f"view 卷册缺失，需要生成（{len(struct_files)} 个 struct 文件）",
            ))
            continue

        view_mtime = view_file.stat().st_mtime
        newest_struct_mtime = max(f.stat().st_mtime for f in struct_files)
        view_text = view_file.read_text(encoding="utf-8")
        struct_files_rel = [f.relative_to(struct_dir).as_posix() for f in struct_files]
        sources_in_view = set(re.findall(r"<!-- SOURCE: struct/(.+?) -->", view_text))
        expected_sources = set(struct_files_rel)

        if sources_in_view != expected_sources:
            diffs.append(DiffEntry(
                topic=topic_dir.name,
                view_file=view_file,
                status="content_diff",
                struct_files=struct_files_rel,
                message=f"source 集合不一致（view 中 {len(sources_in_view)} 个，struct 中 {len(expected_sources)} 个）",
            ))
        elif newest_struct_mtime > view_mtime:
            diffs.append(DiffEntry(
                topic=topic_dir.name,
                view_file=view_file,
                status="newer",
                struct_files=struct_files_rel,
                message=f"struct 文件比 view 卷册新（最新 {newest_struct_mtime - view_mtime:.0f} 秒）",
            ))
        else:
            diffs.append(DiffEntry(
                topic=topic_dir.name,
                view_file=view_file,
                status="same",
                struct_files=struct_files_rel,
                message="已同步",
            ))

    # 检查 view/ 中孤儿文件
    if view_dir.exists():
        expected_view_files = {_view_file_for_topic(view_dir, t.name) for t in topics}
        for view_file in view_dir.glob("volume-*.md"):
            if view_file not in expected_view_files:
                diffs.append(DiffEntry(
                    topic=view_file.stem,
                    view_file=view_file,
                    status="orphan",
                    message="view/ 中无对应 struct/ 主题的孤儿卷册",
                ))

    return diffs


def write_diff_report(report_path: Path, diffs: List[DiffEntry], struct_dir: Path, view_dir: Path) -> None:
    lines = [
        "# struct/ → view/ 差异报告",
        "",
        f"- struct 目录: `{struct_dir}`",
        f"- view 目录: `{view_dir}`",
        f"- 生成时间: {datetime.now().isoformat()}",
        "",
        "## 差异汇总",
        "",
    ]

    status_icons = {
        "missing": "❌ 缺失",
        "content_diff": "⚠️ 内容差异",
        "newer": "🔄 struct 较新",
        "same": "✅ 已同步",
        "orphan": "🗑️ 孤儿卷册",
    }

    for d in diffs:
        icon = status_icons.get(d.status, d.status)
        lines.append(f"### {d.topic}")
        lines.append(f"- 状态: {icon}")
        lines.append(f"- view 文件: `{d.view_file}`")
        lines.append(f"- 说明: {d.message}")
        if d.struct_files:
            lines.append("- 相关 struct 文件:")
            for f in d.struct_files:
                lines.append(f"  - `{f}`")
        lines.append("")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="struct/ → view/ 同步与差异报告"
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="从 struct/ 重新生成 view/ 卷册（默认仅生成差异报告）",
    )
    parser.add_argument(
        "--topic",
        metavar="NAME",
        help="仅处理指定主题目录（如 01-meta-model-standards）",
    )
    parser.add_argument(
        "--report",
        metavar="PATH",
        default="reports/view-diff-report.md",
        help="差异报告输出路径（默认 reports/view-diff-report.md）",
    )
    parser.add_argument(
        "--struct-dir",
        metavar="PATH",
        default="struct",
        help="struct 目录路径（默认 struct/）",
    )
    parser.add_argument(
        "--view-dir",
        metavar="PATH",
        default="view",
        help="view 目录路径（默认 view/）",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    struct_dir = (project_root / args.struct_dir).resolve()
    view_dir = (project_root / args.view_dir).resolve()

    if not struct_dir.exists():
        print(f"错误：struct 目录不存在 {struct_dir}", file=sys.stderr)
        sys.exit(1)

    if args.generate:
        if args.topic:
            topic_dir = struct_dir / args.topic
            if not topic_dir.exists():
                print(f"错误：主题目录不存在 {topic_dir}", file=sys.stderr)
                sys.exit(1)
            view_file = _view_file_for_topic(view_dir, args.topic)
            generate_view_volume(topic_dir, view_file, project_root)
            print(f"已生成 view 卷册: {view_file}")
        else:
            topics = _topic_dirs(struct_dir)
            for topic_dir in topics:
                view_file = _view_file_for_topic(view_dir, topic_dir.name)
                generate_view_volume(topic_dir, view_file, project_root)
                print(f"已生成 view 卷册: {view_file} (from {topic_dir.name})")

    diffs = compute_diff(struct_dir, view_dir, args.topic)
    write_diff_report(Path(args.report), diffs, struct_dir, view_dir)
    print(f"差异报告已保存: {args.report}")

    # 仅将 missing / content_diff 视为未同步；newer 仅为 mtime 差异，source 集合一致
    out_of_sync = [d for d in diffs if d.status in ("missing", "content_diff")]
    newer_only = [d for d in diffs if d.status == "newer"]
    if out_of_sync:
        print(f"警告: {len(out_of_sync)} 个主题未同步")
    elif newer_only:
        print(f"提示: {len(newer_only)} 个主题 struct 文件 mtime 较新，但 source 集合一致")
        print("所有主题已同步")
    else:
        print("所有主题已同步")

    sys.exit(0 if not out_of_sync else 2)


if __name__ == "__main__":
    main()
