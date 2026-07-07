#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识体系统一 CLI 入口（Phase 6 工具链封装）

用法：
    python scripts/knowledge-cli.py health          运行综合健康检查
    python scripts/knowledge-cli.py build           构建全书/课程/学习路径
    python scripts/knowledge-cli.py render          渲染所有 Mermaid 图为 SVG
    python scripts/knowledge-cli.py search <关键词>  搜索 struct/ 中的 Markdown
    python scripts/knowledge-cli.py stats           输出项目规模统计
"""

import subprocess
import sys
import re
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STRUCT_DIR = PROJECT_ROOT / "struct"


def run(cmd: list, cwd: Path = PROJECT_ROOT) -> int:
    return subprocess.call(cmd, cwd=cwd)


def cmd_health(_args):
    return run([sys.executable, "scripts/health-check.py"])


def cmd_build(_args):
    return run([sys.executable, "scripts/build-deliverables.py"])


def cmd_render(_args):
    return run([sys.executable, "scripts/render-visualizations.py"])


def cmd_search(args):
    if not args:
        print("用法: python scripts/knowledge-cli.py search <关键词>")
        return 1
    keyword = " ".join(args).lower()
    matches = []
    for md in sorted(STRUCT_DIR.rglob("*.md")):
        text = md.read_text(encoding="utf-8", errors="ignore")
        if keyword in text.lower():
            title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else md.name
            rel = md.relative_to(PROJECT_ROOT).as_posix()
            count = text.lower().count(keyword)
            matches.append((count, rel, title))
    matches.sort(reverse=True, key=lambda x: x[0])
    print(f"找到 {len(matches)} 个包含 '{keyword}' 的文件：\n")
    for count, rel, title in matches[:30]:
        print(f"  [{count}] {rel} — {title}")
    return 0


def cmd_stats(_args):
    md_files = list(STRUCT_DIR.rglob("*.md"))
    view_files = list((PROJECT_ROOT / "view").rglob("*.md"))
    mmd_files = list((STRUCT_DIR / "99-reference" / "visualizations").rglob("*.mmd"))
    svg_files = list((STRUCT_DIR / "99-reference" / "visualizations").rglob("*.svg"))

    def word_count(text: str) -> int:
        chinese = len(re.findall(r"[\u4e00-\u9fff]", text))
        english = len(re.findall(r"[a-zA-Z]+", text))
        return chinese + english

    total_words = sum(word_count(f.read_text(encoding="utf-8", errors="ignore")) for f in md_files)

    topic_dirs = [d for d in STRUCT_DIR.iterdir() if d.is_dir() and re.match(r"^\d{2}-", d.name)]
    topic_counter = Counter()
    for md in md_files:
        rel = md.relative_to(STRUCT_DIR).as_posix()
        top = rel.split("/")[0]
        topic_counter[top] += 1

    print("# 项目规模统计\n")
    print(f"- struct/ Markdown: {len(md_files)}")
    print(f"- view/ Markdown: {len(view_files)}")
    print(f"- 一级主题数: {len(topic_dirs)}")
    print(f"- Mermaid 源文件: {len(mmd_files)}")
    print(f"- SVG 渲染输出: {len(svg_files)}")
    print(f"- 累计字数（中文字 + 英文词）: {total_words:,}")
    print("\n## 各主题文件数\n")
    for topic, count in sorted(topic_counter.items()):
        print(f"- {topic}: {count}")
    return 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    command = sys.argv[1]
    args = sys.argv[2:]
    handlers = {
        "health": cmd_health,
        "build": cmd_build,
        "render": cmd_render,
        "search": cmd_search,
        "stats": cmd_stats,
    }
    handler = handlers.get(command)
    if not handler:
        print(f"未知命令: {command}\n")
        print(__doc__)
        return 1
    return handler(args)


if __name__ == "__main__":
    sys.exit(main())
