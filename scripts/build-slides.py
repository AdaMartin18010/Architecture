#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
幻灯片生成脚本（Phase 6）

基于 reveal.js 生成 HTML 幻灯片，每主题一个 deck。
依赖：pandoc（可选，若未安装则生成纯 HTML）

用法：
    python scripts/build-slides.py
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STRUCT_DIR = PROJECT_ROOT / "struct"
DIST_DIR = PROJECT_ROOT / "dist"
SLIDES_DIR = DIST_DIR / "slides"

REVEAL_CDN = "https://cdn.jsdelivr.net/npm/reveal.js@4.6.1"


def _topic_dirs() -> list:
    return sorted([d for d in STRUCT_DIR.iterdir() if d.is_dir() and re.match(r"^\d{2}-", d.name)], key=lambda d: d.name)


def _extract_first_heading(text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else "未命名"


def _split_into_slides(text: str) -> list:
    """将 Markdown 按二级标题拆分为幻灯片"""
    slides = []
    current_title = ""
    current_body = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current_title or current_body:
                slides.append((current_title, "\n".join(current_body)))
            current_title = line[3:].strip()
            current_body = []
        else:
            current_body.append(line)
    if current_title or current_body:
        slides.append((current_title, "\n".join(current_body)))
    return slides


def _markdown_to_html(md_text: str) -> str:
    if shutil.which("pandoc"):
        result = subprocess.run(
            ["pandoc", "-f", "markdown", "-t", "html"],
            input=md_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return result.stdout if result.returncode == 0 else f"<pre>{md_text}</pre>"
    # 极简 fallback：保留换行和代码块
    html = md_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html = re.sub(r"```(.+?)```", r"<pre><code>\1</code></pre>", html, flags=re.DOTALL)
    html = html.replace("\n", "<br>")
    return html


def build_deck(topic_dir: Path, output_file: Path) -> None:
    readme = topic_dir / "README.md"
    if not readme.exists():
        return

    title = _extract_first_heading(readme.read_text(encoding="utf-8"))
    slides = _split_into_slides(readme.read_text(encoding="utf-8"))

    sections = []
    for idx, (slide_title, body) in enumerate(slides):
        if idx == 0:
            # 第一张作为标题页
            sections.append(f"<section><h1>{title}</h1><p>{slide_title}</p></section>")
        else:
            body_html = _markdown_to_html(body)
            sections.append(f"<section><h2>{slide_title}</h2>{body_html}</section>")

    sections_html = "\n      ".join(sections)
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <link rel="stylesheet" href="{REVEAL_CDN}/dist/reveal.css">
  <link rel="stylesheet" href="{REVEAL_CDN}/dist/theme/white.css">
</head>
<body>
  <div class="reveal">
    <div class="slides">
      {sections_html}
    </div>
  </div>
  <script src="{REVEAL_CDN}/dist/reveal.js"></script>
  <script>Reveal.initialize({{hash: true, slideNumber: 'c/t'}});</script>
</body>
</html>
"""
    output_file.write_text(html, encoding="utf-8")


def main():
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)
    topics = _topic_dirs()
    for topic_dir in topics:
        output = SLIDES_DIR / f"{topic_dir.name}.html"
        build_deck(topic_dir, output)
        print(f"幻灯片已生成: {output}")
    print(f"\n共生成 {len(topics)} 个主题幻灯片，位于 {SLIDES_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
