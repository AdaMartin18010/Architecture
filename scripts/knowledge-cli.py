#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识体系统一 CLI 入口（Phase 6 工具链封装）

用法：
    python scripts/knowledge-cli.py health          运行综合健康检查
    python scripts/knowledge-cli.py build           构建全书/课程/学习路径（串联 sync-view + build-deliverables）
    python scripts/knowledge-cli.py sync            仅同步 struct/ → view/ 卷册
    python scripts/knowledge-cli.py render          渲染所有 Mermaid 图为 SVG
    python scripts/knowledge-cli.py search <关键词>  搜索 struct/ 中的 Markdown
    python scripts/knowledge-cli.py stats           输出项目规模统计（生成 reports/stats.json + reports/stats.md）
"""

import subprocess
import sys
import json
import datetime
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
    """串联：先同步 view/，再构建 dist/ 交付物，确保 view/dist 同源同新。"""
    code = run([sys.executable, "scripts/sync-view-from-struct.py", "--generate"])
    if code != 0:
        return code
    return run([sys.executable, "scripts/build-deliverables.py"])


def cmd_sync(_args):
    return run([sys.executable, "scripts/sync-view-from-struct.py", "--generate"])


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


def _word_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text)) + len(re.findall(r"[a-zA-Z]+", text))


def _parse_axioms(path: Path) -> dict:
    """解析 axiom-system.md 公理标题，区分严格公理与工程启发式。"""
    strict_set, heur_set, warnings = set(), set(), []
    if not path.exists():
        return {"strict": {}, "heuristic": {}, "strict_total": 0, "heuristic_total": 0,
                "warnings": [f"缺文件 {path}"]}
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"^###\s+([MESP])\.(\d+)\b", line)
        if not m:
            continue
        (heur_set if "启发式" in line else strict_set).add((m.group(1), int(m.group(2))))

    def by_cat(s):
        return {k: sum(1 for x in s if x[0] == k) for k in "MESP" if any(x[0] == k for x in s)}

    return {"strict": by_cat(strict_set), "heuristic": by_cat(heur_set),
            "strict_total": len(strict_set), "heuristic_total": len(heur_set), "warnings": warnings}


def _parse_theorems(path: Path) -> dict:
    nums, warnings = set(), []
    if not path.exists():
        return {"count": 0, "max": 0, "warnings": [f"缺文件 {path}"]}
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"^###\s+Th\.(\d+)\b", line)
        if m:
            nums.add(int(m.group(1)))
    return {"count": len(nums), "max": max(nums) if nums else 0, "warnings": warnings}


def _crosscheck_axiom_tree(path: Path, strict_total: int, theorem_count: int) -> list:
    warnings = []
    if not path.exists():
        return [f"缺文件 {path}"]
    text = path.read_text(encoding="utf-8", errors="ignore")
    head = re.search(r"(\d+)\s*公理\s*\+\s*(\d+)\s*定理\s*=\s*(\d+)\s*条", text)
    totals = re.findall(r"\*\*总计\*\*\s*\|\s*\*\*(\d+)\*\*", text)
    if head:
        h_axiom, h_theorem = int(head.group(1)), int(head.group(2))
        if h_axiom != strict_total:
            warnings.append(
                f"axiom-theorem-tree 头部称公理 {h_axiom}，axiom-system 严格公理 {strict_total}（不一致）"
            )
        if h_theorem != theorem_count:
            warnings.append(
                f"axiom-theorem-tree 头部称定理 {h_theorem}，theorem-derivations 实 {theorem_count}（不一致）"
            )
    for t_str in totals:
        # 统计表总计校验：总计必须等于其上方各行“数量”列之和（而非无条件告警）
        row_m = re.search(rf"^\|\s*\*\*总计\*\*\s*\|\s*\*\*{t_str}\*\*.*$", text, re.MULTILINE)
        if not row_m:
            continue
        table_head = text.rfind("###", 0, row_m.start())
        block = text[table_head:row_m.start()] if table_head != -1 else text[:row_m.start()]
        rows = re.findall(r"^\|[^|]*\|\s*(\d+)\s*\|", block, re.MULTILINE)
        if rows and sum(int(x) for x in rows) != int(t_str):
            warnings.append(
                f"axiom-theorem-tree 统计表总计 = {t_str}，各行合计 = {sum(int(x) for x in rows)}（不一致）"
            )
    return warnings


def _scan_jsonl(path: Path, key_candidates: tuple):
    total, by, warns = 0, {}, []
    if not path.exists():
        return 0, {}, [f"缺文件 {path}"]
    with path.open(encoding="utf-8", errors="ignore") as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            total += 1
            t = "?"
            try:
                obj = json.loads(ln)
                for k in key_candidates:
                    if obj.get(k):
                        t = obj[k]
                        break
            except Exception:
                t = "__parse_error__"
            by[t] = by.get(t, 0) + 1
    return total, by, warns


def _kg_stats(kg_dir: Path) -> dict:
    out = {"entities_total": 0, "relations_total": 0, "entities_by_type": {},
           "relations_by_type": {}, "ttl_lines_approx": 0, "warnings": []}
    ent = kg_dir / "kg-entities.jsonl"
    rel = kg_dir / "kg-relations.jsonl"
    ttl = kg_dir / "kg.ttl"
    et, eb, w1 = _scan_jsonl(ent, ("type", "entity_type", "kind"))
    rt, rb, w2 = _scan_jsonl(rel, ("relation", "type", "predicate"))
    out["entities_total"], out["entities_by_type"] = et, eb
    out["relations_total"], out["relations_by_type"] = rt, rb
    out["warnings"] += w1 + w2
    if ttl.exists():
        n = 0
        for ln in ttl.read_text(encoding="utf-8", errors="ignore").splitlines():
            s = ln.strip()
            if s and not s.startswith(("#", "@")) and " " in s:
                n += 1
        out["ttl_lines_approx"] = n
    return out


def cmd_stats(_args):
    md_files = list(STRUCT_DIR.rglob("*.md"))
    view_files = list((PROJECT_ROOT / "view").rglob("*.md"))
    dist_dir = PROJECT_ROOT / "dist"
    dist_volumes = list((dist_dir / "book-volumes").rglob("*.md")) if (dist_dir / "book-volumes").exists() else []
    dist_book_full = dist_dir / "book-full.md"
    viz_dir = STRUCT_DIR / "99-reference" / "visualizations"
    mmd_files = list(viz_dir.rglob("*.mmd"))
    svg_files = list(viz_dir.rglob("*.svg"))

    total_words = sum(_word_count(f.read_text(encoding="utf-8", errors="ignore")) for f in md_files)

    topic_dirs = [d for d in STRUCT_DIR.iterdir() if d.is_dir() and re.match(r"^\d{2}-", d.name)]
    topic_counter = Counter()
    for md in md_files:
        rel = md.relative_to(STRUCT_DIR).as_posix()
        topic_counter[rel.split("/")[0]] += 1

    axiom_path = STRUCT_DIR / "01-meta-model-standards" / "06-formal-axioms" / "axiom-system.md"
    theorem_path = STRUCT_DIR / "01-meta-model-standards" / "06-formal-axioms" / "theorem-derivations.md"
    axiom_tree_path = STRUCT_DIR / "99-reference" / "glossary" / "axiom-theorem-tree.md"
    axioms = _parse_axioms(axiom_path)
    theorems = _parse_theorems(theorem_path)
    kg = _kg_stats(STRUCT_DIR / "99-reference" / "knowledge-graph")

    warnings = list(axioms["warnings"]) + list(theorems["warnings"]) + list(kg["warnings"])
    warnings += _crosscheck_axiom_tree(axiom_tree_path, axioms["strict_total"], theorems["count"])

    stats = {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "struct_md": len(md_files),
        "view_md": len(view_files),
        "dist_volume_md": len(dist_volumes),
        "dist_book_full_exists": dist_book_full.exists(),
        "topic_count": len(topic_dirs),
        "mermaid_mmd": len(mmd_files),
        "svg": len(svg_files),
        "total_words": total_words,
        "topics": dict(sorted(topic_counter.items())),
        "axioms": axioms,
        "theorems": theorems,
        "knowledge_graph": kg,
        "warnings": warnings,
    }

    lines = [
        "# 项目规模统计（机器真源）",
        "",
        f"> 生成时间: {stats['generated_at']}",
        "> 生成命令: `python scripts/knowledge-cli.py stats`",
        "> 真源文件: `reports/stats.json`（README/MASTER_PLAN/COMPLETION 应引用此文件，禁止手工改数）",
        "",
        "## 文档与主题",
        "",
        f"- struct/ Markdown: **{len(md_files)}**",
        f"- view/ Markdown: **{len(view_files)}**",
        f"- dist/book-volumes Markdown: **{len(dist_volumes)}**（book-full.md 存在: {dist_book_full.exists()}）",
        f"- 一级主题数: **{len(topic_dirs)}**",
        f"- Mermaid 源文件: **{len(mmd_files)}**",
        f"- SVG 渲染输出: **{len(svg_files)}**",
        f"- 累计字数（中文字 + 英文词）: **{total_words:,}**",
        "",
        "## 公理与定理（解析自 axiom-system.md / theorem-derivations.md）",
        "",
        f"- 严格公理总计: **{axioms['strict_total']}**（按类 {axioms['strict']}）",
        f"- 工程启发式总计: **{axioms['heuristic_total']}**（按类 {axioms['heuristic']}）",
        f"- 定理数: **{theorems['count']}**（最大编号 Th.{theorems['max']}）",
        "",
        "## 知识图谱（jsonl 行级统计）",
        "",
        f"- 实体总数: **{kg['entities_total']}**（按类型 {kg['entities_by_type']}）",
        f"- 关系总数: **{kg['relations_total']}**（按类型 {kg['relations_by_type']}）",
        f"- kg.ttl 含谓词行（近似，非精确三元组）: **{kg['ttl_lines_approx']}**",
        "",
        "## 各主题文件数",
        "",
    ]
    for topic, count in sorted(topic_counter.items()):
        lines.append(f"- {topic}: {count}")
    if warnings:
        lines += ["", "## 一致性警告（需 P1 归一，不在 P0 改数）", ""]
        for w in warnings:
            lines.append(f"- {w}")
    md_text = "\n".join(lines) + "\n"

    reports_dir = PROJECT_ROOT / "reports"
    reports_dir.mkdir(exist_ok=True)
    (reports_dir / "stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    (reports_dir / "stats.md").write_text(md_text, encoding="utf-8")
    print(md_text)
    print(f"已写出: reports/stats.json, reports/stats.md（warnings={len(warnings)}）")
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
        "sync": cmd_sync,
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
