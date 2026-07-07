#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 6 交付物构建脚本

一键生成：
- dist/book-full.md          全书聚合 Markdown
- dist/book-volumes/         按主题分卷
- struct/99-reference/course/learning-path.md  学习路径
- struct/99-reference/course/syllabus.md       课程大纲

用法：python scripts/build-deliverables.py
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
STRUCT_DIR = PROJECT_ROOT / "struct"
DIST_DIR = PROJECT_ROOT / "dist"
COURSE_DIR = STRUCT_DIR / "99-reference" / "course"


def _topic_dirs() -> List[Path]:
    """返回 struct/ 下所有主题目录，按编号排序"""
    dirs = [d for d in STRUCT_DIR.iterdir() if d.is_dir() and re.match(r"^\d{2}-", d.name)]
    return sorted(dirs, key=lambda d: d.name)


def _collect_md_files(topic_dir: Path) -> List[Path]:
    """收集主题目录下的 Markdown 文件，跳过元数据目录"""
    files = []
    if not topic_dir.exists():
        return files
    for md in sorted(topic_dir.rglob("*.md")):
        rel_posix = md.relative_to(topic_dir).as_posix()
        skip_patterns = [
            "99-reference/audit/",
            "CHANGELOG",
            "frontier-tracking/",
            "plans-tasks/",
            "_HISTORICAL_",
        ]
        if any(sp in rel_posix for sp in skip_patterns):
            continue
        files.append(md)
    return files


def _extract_first_heading(text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else "未命名"


def _rewrite_links(text: str, source_file: Path, struct_root: Path, output_root: Path) -> str:
    """将相对链接重写为输出文件可解析的路径。"""

    def replace_link(m: re.Match) -> str:
        md_prefix = m.group(1)
        link = m.group(2)
        suffix = m.group(3)
        if link.startswith(("http://", "https://", "mailto:", "#")):
            return m.group(0)
        source_dir = source_file.parent
        project_root = struct_root.parent
        fragment = ""
        bare = link
        if "#" in bare:
            bare, fragment = bare.split("#", 1)
            fragment = "#" + fragment
        if not bare:
            return m.group(0)

        def _rel_to_output(target: Path) -> str:
            try:
                return target.relative_to(output_root).as_posix()
            except ValueError:
                up = "../" * len(output_root.relative_to(project_root).parts)
                return up + target.relative_to(project_root).as_posix()

        # 目录链接：尝试指向 README.md
        if bare.endswith("/"):
            target_dir = (source_dir / bare).resolve()
            try:
                rel_dir = target_dir.relative_to(struct_root).as_posix()
                for readme in ("README.md", "index.md", "readme.md"):
                    if (target_dir / readme).exists():
                        new_target = (struct_root / rel_dir / readme).resolve()
                        return f"{md_prefix}{_rel_to_output(new_target)}{fragment}{suffix}"
            except ValueError:
                pass
            return m.group(0)

        target = (source_dir / bare).resolve()
        try:
            rel = target.relative_to(struct_root).as_posix()
            suffixes = (".md", ".py", ".yaml", ".yml", ".json", ".sh", ".html")
            has_known_ext = any(str(bare).lower().endswith(ext) for ext in suffixes)
            if target.exists() or any(target.with_suffix(ext).exists() for ext in suffixes):
                if not has_known_ext and (struct_root / rel).with_suffix(".md").exists():
                    rel += ".md"
                new_target = (struct_root / rel).resolve()
                return f"{md_prefix}{_rel_to_output(new_target)}{fragment}{suffix}"
        except ValueError:
            pass

        # 项目根目录下的其他资源（scripts/、dist/ 等）
        try:
            if project_root in target.parents or target == project_root:
                if target.exists():
                    return f"{md_prefix}{_rel_to_output(target)}{fragment}{suffix}"
        except Exception:
            pass
        return m.group(0)

    return re.sub(r"(\]\()([^)\s]+?)(\))", replace_link, text)


def _build_volume(topic_dir: Path, output_file: Path) -> Tuple[str, int]:
    """构建单个主题卷册，返回标题和文件数"""
    files = _collect_md_files(topic_dir)
    if not files:
        return "", 0

    title = _extract_first_heading(topic_dir.joinpath("README.md").read_text(encoding="utf-8")) \
        if (topic_dir / "README.md").exists() else topic_dir.name

    lines = [
        f"# {title}",
        "",
        f"> **来源**: `struct/{topic_dir.name}`",
        f"> **文件数**: {len(files)}",
        f"> **生成命令**: `python scripts/build-deliverables.py`",
        "",
        "---",
        "",
        "## 目录",
        "",
    ]

    for idx, md in enumerate(files, start=1):
        text = md.read_text(encoding="utf-8")
        heading = _extract_first_heading(text)
        rel = md.relative_to(STRUCT_DIR).as_posix()
        lines.append(f"{idx}. [{heading}](../../struct/{rel})")

    lines.extend(["", "---", ""])

    for md in files:
        text = md.read_text(encoding="utf-8")
        text = _rewrite_links(text, md, STRUCT_DIR, output_file.parent)
        rel = md.relative_to(STRUCT_DIR).as_posix()
        lines.append(f"\n<!-- SOURCE: struct/{rel} -->\n")
        lines.append(text)
        lines.append("\n---\n")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(lines), encoding="utf-8")
    return title, len(files)


def build_book() -> None:
    """构建全书聚合与分卷"""
    DIST_DIR.mkdir(exist_ok=True)
    volumes_dir = DIST_DIR / "book-volumes"
    volumes_dir.mkdir(exist_ok=True)

    topics = _topic_dirs()
    full_lines = [
        "# 软件工程架构复用视角 · 全书",
        "",
        "> **版本**: 2026-07-08",
        "> **定位**: 由 `struct/` 自动聚合生成的全书 Markdown 稿",
        "> **生成命令**: `python scripts/build-deliverables.py`",
        "",
        "---",
        "",
        "## 目录",
        "",
    ]

    for topic_dir in topics:
        volume_file = volumes_dir / f"volume-{topic_dir.name}.md"
        title, count = _build_volume(topic_dir, volume_file)
        if count == 0:
            continue
        rel = volume_file.relative_to(DIST_DIR).as_posix()
        full_lines.append(f"- [{title}]({rel}) — {count} 个源文件")

    full_lines.extend(["", "---", ""])

    for topic_dir in topics:
        volume_file = volumes_dir / f"volume-{topic_dir.name}.md"
        if not volume_file.exists():
            continue
        text = volume_file.read_text(encoding="utf-8")
        # book-volumes 中的链接使用 ../../ 前缀（相对 book-volumes/），
        # 在 book-full.md（相对 dist/）中应统一为 ../ 前缀
        text = text.replace("](../../", "](../")
        full_lines.append(text)
        full_lines.append("\n---\n")

    (DIST_DIR / "book-full.md").write_text("\n".join(full_lines), encoding="utf-8")
    print(f"全书已生成: {DIST_DIR / 'book-full.md'}")
    print(f"分卷已生成: {volumes_dir}")


def _build_learning_path() -> None:
    """构建学习路径"""
    COURSE_DIR.mkdir(parents=True, exist_ok=True)
    topics = _topic_dirs()

    lines = [
        "# 学习路径：从架构复用新手到专家",
        "",
        "> **版本**: 2026-07-08",
        "> **目标**: 为不同背景读者提供 4 条递进式学习路径",
        "> **生成命令**: `python scripts/build-deliverables.py`",
        "",
        "---",
        "",
        "## 路径总览",
        "",
        "| 路径 | 适合人群 | 预计学时 | 关键产出 |",
        "|------|----------|----------|----------|",
        "| 🏗️ 架构师路径 | 企业架构师、技术负责人 | 40h | 可复用架构设计文档 |",
        "| 💻 工程师路径 | 软件工程师、DevOps | 35h | 复用组件/服务设计 |",
        "| 🔒 安全工程师路径 | 安全架构师、合规专员 | 25h | 供应链安全评估报告 |",
        "| 🤖 AI 原生路径 | AI 平台工程师、Agent 开发者 | 30h | MCP/A2A 复用方案 |",
        "",
        "---",
        "",
        "## 按主题学习索引",
        "",
    ]

    for topic_dir in topics:
        readme = topic_dir / "README.md"
        title = topic_dir.name
        if readme.exists():
            title = _extract_first_heading(readme.read_text(encoding="utf-8"))
        lines.append(f"### {title}")
        lines.append("")
        files = _collect_md_files(topic_dir)
        for md in files[:5]:
            heading = _extract_first_heading(md.read_text(encoding="utf-8"))
            rel = md.relative_to(STRUCT_DIR).as_posix()
            lines.append(f"- [{heading}](../../{rel})")
        if len(files) > 5:
            lines.append(f"- … 共 {len(files)} 个文件")
        lines.append("")

    (COURSE_DIR / "learning-path.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"学习路径已生成: {COURSE_DIR / 'learning-path.md'}")


def _build_syllabus() -> None:
    """构建课程大纲"""
    COURSE_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# 课程大纲：软件架构复用工程",
        "",
        "> **版本**: 2026-07-08",
        "> **课时**: 16 周 × 3 学时/周 = 48 学时",
        "> **形式**: 讲授 50% + 案例研讨 30% + 工具实践 20%",
        "",
        "---",
        "",
        "## 课程目标",
        "",
        "1. 理解架构复用的元模型、标准与公理体系。",
        "2. 掌握业务/应用/组件/功能四层复用设计方法。",
        "3. 能够运用成熟度模型、度量指标与治理流程评估复用能力。",
        "4. 具备工业 IoT、AI 原生、供应链安全等垂直领域的复用分析能力。",
        "",
        "## 教学周历",
        "",
        "| 周次 | 主题 | 核心内容 | 实践作业 |",
        "|------|------|----------|----------|",
        "| 1 | 课程导论 | 知识体系结构、复用经济学、权威来源 | 建立个人知识索引 |",
        "| 2-3 | 元模型与标准 | ISO 42010/42020/42030、TOGAF 10、ArchiMate 4.0 | 标准对齐矩阵 |",
        "| 4-5 | 业务架构复用 | 业务能力、价值流、BPMN/DMN | 业务服务目录设计 |",
        "| 6-7 | 应用架构复用 | 微服务、事件驱动、云原生模式 | 复用性评估问卷 |",
        "| 8-9 | 组件与功能复用 | 接口契约、设计模式、API/MCP/A2A | 复用组件原型 |",
        "| 10 | 跨层治理 | 成熟度模型、度量、FinOps、Agentic 治理 | 治理流程图 |",
        "| 11 | 形式化验证 | TLA+/Alloy 案例、公理-定理推导 | 规约小练习 |",
        "| 12 | 价值量化 | COCOMO II 2026、ROI/NPV、碳排模型 | 复用 ROI 计算 |",
        "| 13 | 供应链安全 | SLSA、SBOM、OWASP SCVS、零信任供应链 | 攻击树分析 |",
        "| 14 | 工业 IoT / OT-IT | ISA-95、OPC UA FX、AAS、功能安全 | 工业资产目录 |",
        "| 15 | AI 原生复用 | MCP/A2A、Agentic Infrastructure、概率契约 | Agent 复用方案 |",
        "| 16 | 整合输出 | 全书框架、个人项目答辩 | 可发布知识产品 |",
        "",
        "## 考核方式",
        "",
        "- 平时作业 40%（标准对齐、复用设计、治理流程）",
        "- 期中项目 30%（选择一个垂直领域完成复用方案）",
        "- 期末答辩 30%（基于 `struct/` 知识库输出可发布作品）",
        "",
        "## 推荐工具",
        "",
        "- 健康检查：`python scripts/health-check.py`",
        "- 复用决策工具：`struct/99-reference/tools/reuse-decision-tool-v2/`",
        "- COCOMO 计算器：`struct/99-reference/tools/cocomo-calculator.py`",
        "- 全书构建：`python scripts/build-deliverables.py`",
    ]
    (COURSE_DIR / "syllabus.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"课程大纲已生成: {COURSE_DIR / 'syllabus.md'}")


def main():
    build_book()
    _build_learning_path()
    _build_syllabus()
    print("\nPhase 6 交付物构建完成。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
