# 知识门户 Streamlit 入口（Phase 6 工具链封装）
# 运行：streamlit run struct/99-reference/tools/knowledge-portal/app.py

import re
import subprocess
import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
STRUCT_DIR = PROJECT_ROOT / "struct"

st.set_page_config(page_title="架构复用知识门户", layout="wide")
st.title("🏗️ 软件工程架构复用知识门户")
st.markdown("""
> **定位**: Phase 6 整合输出工具，统一检索、可视化、健康检查与课程导航
> **源码**: `struct/99-reference/tools/knowledge-portal/app.py`
""")


def list_topics():
    topics = []
    for d in sorted(STRUCT_DIR.iterdir()):
        if d.is_dir() and re.match(r"^\d{2}-", d.name):
            readme = d / "README.md"
            title = d.name
            if readme.exists():
                m = re.search(r"^#\s+(.+)$", readme.read_text(encoding="utf-8"), re.MULTILINE)
                title = m.group(1).strip() if m else d.name
            topics.append((d.name, title))
    return topics


tab_search, tab_viz, tab_health, tab_course, tab_quiz = st.tabs(["🔍 全文搜索", "📊 可视化", "🩺 健康检查", "🎓 课程", "📝 测验"])

with tab_search:
    keyword = st.text_input("输入关键词，搜索 struct/ 全部 Markdown", "")
    if keyword:
        matches = []
        for md in sorted(STRUCT_DIR.rglob("*.md")):
            text = md.read_text(encoding="utf-8", errors="ignore")
            if keyword.lower() in text.lower():
                title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
                title = title_match.group(1).strip() if title_match else md.name
                rel = md.relative_to(PROJECT_ROOT).as_posix()
                count = text.lower().count(keyword.lower())
                matches.append((count, rel, title))
        matches.sort(reverse=True, key=lambda x: x[0])
        st.write(f"找到 {len(matches)} 个结果")
        for count, rel, title in matches[:50]:
            st.markdown(f"- [{title}](../../../{rel}) — 出现 {count} 次")

with tab_viz:
    st.subheader("可视化图库")
    viz_dir = STRUCT_DIR / "99-reference" / "visualizations"
    svg_files = sorted(viz_dir.rglob("*.svg"))
    selected = st.selectbox("选择 SVG", [f.relative_to(viz_dir).as_posix() for f in svg_files])
    if selected:
        svg_path = viz_dir / selected
        st.image(str(svg_path), use_container_width=True)

with tab_health:
    st.subheader("项目健康检查")
    if st.button("运行 health-check.py"):
        with st.spinner("检查中..."):
            result = subprocess.run(
                [sys.executable, "scripts/health-check.py"],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
        st.code(result.stdout + result.stderr, language="text")

with tab_course:
    st.subheader("学习路径")
    topics = list_topics()
    for code, title in topics:
        st.markdown(f"- **{code}**: {title}")
    st.markdown("---")
    st.markdown("📖 [完整学习路径](../../../struct/99-reference/course/learning-path.md)")
    st.markdown("📋 [课程大纲](../../../struct/99-reference/course/syllabus.md)")


with tab_quiz:
    st.subheader("课程测验")
    quiz_file = STRUCT_DIR / "99-reference" / "course" / "quiz.md"
    if quiz_file.exists():
        quiz_text = quiz_file.read_text(encoding="utf-8")
        st.markdown(quiz_text)
    else:
        st.warning("未找到测验文件")
