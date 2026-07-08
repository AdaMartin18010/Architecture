#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容质量门控脚本 V2（Quality Gate V2）

在 quality-gate.py 基础上扩展：
1. 批量模板重复段检测（如 "## 补充说明" 段落）
2. 检测文件是否缺少定义/示例/反例/权威来源/交叉引用
3. Markdown 死链检测（相对链接指向不存在的文件）
4. 术语不一致检测（同一术语在不同文件中定义冲突）
5. 输出详细 JSON / Markdown 报告

用法：
    python scripts/quality-gate-v2.py [path/to/file.md|path/to/dir]
    python scripts/quality-gate-v2.py --json reports/quality-gate-v2.json struct/
    python scripts/quality-gate-v2.py --report reports/quality-gate-v2.md struct/
"""

import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict


@dataclass
class GateResult:
    path: str
    score: int
    passed: bool
    checks: Dict[str, bool]
    warnings: List[str]
    duplicated_sections: List[str] = field(default_factory=list)
    dead_links: List[Dict[str, str]] = field(default_factory=list)
    cross_refs: List[str] = field(default_factory=list)
    padding_ratio: float = 0.0


@dataclass
class TermConflict:
    term: str
    definitions: List[Tuple[str, str]]  # (file_relative_path, definition_line)


# 基础检查规则（继承并微调自 quality-gate.py）
RULES = {
    "definition": {
        "name": "概念定义",
        "patterns": [
            r"#{1,4}\s*定义",
            r"#{1,4}\s*.*概念",
            r"#{1,4}\s*.*术语",
            r"\*\*定义\*\*",
            r"\*\*概念\*\*",
            r"\*\*术语\*\*",
            r"##\s*\d+\.\s*.*定义",
        ],
        "weight": 20,
    },
    "example": {
        "name": "正向示例",
        "patterns": [
            r"#{1,4}\s*示例",
            r"#{1,4}\s*.*案例",
            r"\*\*示例\*\*",
            r"\*\*案例\*\*",
            r">\s*\[示例",
            r"例如：",
            r"例如，",
        ],
        "weight": 15,
    },
    "counter_example": {
        "name": "反例/反模式",
        "patterns": [
            r"#{1,4}\s*反例",
            r"#{1,4}\s*反模式",
            r"#{1,4}\s*失败案例",
            r"#{1,4}\s*边界.*条件",
            r"\*\*反例\*\*",
            r"\*\*反模式\*\*",
            r"\*\*失败案例\*\*",
            r"边界场景",
            r"不应.*复用",
            r"错误.*复用",
        ],
        "weight": 15,
    },
    "authority": {
        "name": "权威来源",
        "patterns": [
            r"#{1,4}\s*权威来源",
            r"#{1,4}\s*参考.*来源",
            r"#{1,4}\s*参考.*文献",
            r"\*\*权威来源\*\*",
            r"\*\*来源 URL\*\*",
            r"核查日期",
            r"\[来源\]\(https?://",
        ],
        "weight": 20,
    },
    "cross_reference": {
        "name": "交叉引用",
        "patterns": [
            r"交叉引用",
            r"参见",
            r"详见",
            r"相关.*链接",
            r"相关.*文档",
            r"->",
            r"→",
        ],
        "weight": 10,
    },
    "representation": {
        "name": "思维表征（图/矩阵/树）",
        "patterns": [
            r"```mermaid",
            r"```graphviz",
            r"#{1,4}\s*.*矩阵",
            r"#{1,4}\s*.*决策树",
            r"#{1,4}\s*.*判定树",
            r"#{1,4}\s*.*思维导图",
            r"#{1,4}\s*.*概念谱系",
            r"\|.*\|.*\|",
        ],
        "weight": 10,
    },
    "argumentation": {
        "name": "论证/证明/分析",
        "patterns": [
            r"#{1,4}\s*.*证明",
            r"#{1,4}\s*.*论证",
            r"#{1,4}\s*.*分析",
            r"#{1,4}\s*.*推理",
            r"\*\*证明\*\*",
            r"\*\*论证\*\*",
            r"公理",
            r"定理",
            r"因为.*所以",
            r"因此.*",
        ],
        "weight": 10,
    },
}

MIN_SCORE = 60
MIN_WEIGHTED = 3
BATCH_TEMPLATE_SECTIONS = ["## 补充说明", "## 概念定义", "## 正向示例", "## 反例"]

# 模板 Padding 检测：机械重复的二级/三级/四级标题
PADDING_HEADING_PATTERNS = [
    re.compile(r"^(#{2,4})\s+补充说明"),
    re.compile(r"^(#{2,4})\s+概念定义\s*$"),
    re.compile(r"^(#{2,4})\s+示例\s*$"),
    re.compile(r"^(#{2,4})\s+反例\s*$"),
    re.compile(r"^(#{2,4})\s+权威来源\s*$"),
    re.compile(r"^(#{2,4})\s+分析\s*$"),
    re.compile(r"^(#{2,4})\s+参考文献\s*$"),
    re.compile(r"^(#{2,4})\s+延伸阅读\s*$"),
    re.compile(r"^(#{2,4})\s+附录\s*$"),
]


def calculate_padding_ratio(text: str) -> float:
    """计算模板 Padding 行数占总行数的百分比。"""
    lines = text.splitlines()
    total = len(lines)
    if total == 0:
        return 0.0
    is_padding = [False] * total
    i = 0
    while i < total:
        matched = False
        for p in PADDING_HEADING_PATTERNS:
            m = p.match(lines[i])
            if m:
                level = len(m.group(1))
                is_padding[i] = True
                i += 1
                while i < total:
                    m2 = re.match(r"^(#{1,6})\s", lines[i])
                    if m2 and len(m2.group(1)) <= level:
                        break
                    is_padding[i] = True
                    i += 1
                matched = True
                break
        if not matched:
            i += 1
    return sum(is_padding) / total * 100.0


def _extract_markdown_links(text: str) -> List[Tuple[str, str, int]]:
    """提取 Markdown 内联链接与自动链接，返回 (链接文本, 链接目标, 行号)。

    跳过代码块（被 ``` 包围的行）中的链接，避免示例/占位链接被误判为死链。
    """
    links = []
    in_code_block = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        # 标准内联链接 [text](target)
        for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line):
            links.append((m.group(1), m.group(2), lineno))
        # 自动链接 <URL>
        for m in re.finditer(r"<([a-z][a-z0-9+.-]*://[^>]+)>", line, re.IGNORECASE):
            links.append((m.group(1), m.group(1), lineno))
    return links


def _resolve_relative_link(base_file: Path, link: str, project_root: Path) -> Optional[Path]:
    """解析相对路径链接，返回绝对路径（若链接以 http/https/ftp/mailto/anchor 开头则返回 None）"""
    link = link.strip()
    if not link:
        return None
    if re.match(r"^[a-z][a-z0-9+.-]*://", link, re.IGNORECASE):
        return None
    if link.startswith("mailto:") or link.startswith("#"):
        return None
    # 去掉锚点
    if "#" in link:
        link = link.split("#", 1)[0]
    if not link:
        return None
    target = (base_file.parent / link).resolve()
    try:
        # 允许指向项目根目录下的任何位置（struct/、scripts/、dist/ 等）
        if project_root not in target.parents and target != project_root:
            return None
    except ValueError:
        pass
    return target


def _build_anchors(text: str) -> Set[str]:
    """预计算文件中所有可用锚点。"""
    anchors: Set[str] = set()
    for line in text.splitlines():
        for m in re.finditer(r"\{#([^}]+)\}", line):
            anchors.add(m.group(1).lower())
    seen: Dict[str, int] = defaultdict(int)
    for line in text.splitlines():
        m = re.match(r"^#{1,6}\s+(.+?)(?:\s*\{[^}]*\})?\s*$", line)
        if m:
            title = m.group(1).strip().lower()
            slug = re.sub(r"[^\w\s\-]", "", title, flags=re.UNICODE).replace(" ", "-")
            slug = re.sub(r"-+", "-", slug).strip("-")
            if not slug:
                continue
            count = seen[slug]
            seen[slug] += 1
            anchors.add(slug)
            if count > 0:
                anchors.add(f"{slug}-{count}")
    return anchors


def _target_exists(target: Path) -> bool:
    if target.exists():
        return True
    if target.is_dir() or target.suffix == "":
        for name in ("README.md", "index.md", "readme.md"):
            if (target / name).exists():
                return True
    return False


def _extract_term_definitions(text: str, rel_path: str) -> Dict[str, str]:
    """提取文件中的术语定义，返回 term -> definition"""
    terms: Dict[str, str] = {}
    # 模式1: ### Term (中文)
    for m in re.finditer(r"^#{3,4}\s+(.+?)\s*\(([^)]+)\)\s*$", text, re.MULTILINE):
        term_en = m.group(1).strip()
        term_cn = m.group(2).strip()
        if term_en:
            terms[term_en] = rel_path
        if term_cn:
            terms[term_cn] = rel_path
    # 模式2: **定义**：... 或 **概念**：...
    for m in re.finditer(r"^\*\*(定义|概念|术语)\*\*\s*[:：]\s*(.+)$", text, re.MULTILINE):
        line = m.group(2).strip()
        # 截取第一句作为定义
        first_sentence = re.split(r"[。；;]", line)[0]
        terms[first_sentence] = rel_path
    # 模式3: - **Term**: definition（要求定义部分足够长，避免把简单列举当定义）
    for m in re.finditer(r"^-\s*\*\*([^*]+)\*\*\s*[:：]\s*(.+)$", text, re.MULTILINE):
        term = m.group(1).strip()
        definition = m.group(2).strip()
        if term and definition and len(definition) >= 15:
            terms[term] = rel_path
    return terms


def check_file(filepath: Path, root: Path, project_root: Optional[Path] = None) -> GateResult:
    text = filepath.read_text(encoding="utf-8")
    try:
        rel = filepath.relative_to(root).as_posix()
    except ValueError:
        rel = filepath.name
    if project_root is None:
        project_root = root
    word_count = len(re.findall(r"[\u4e00-\u9fa5]", text)) + len(text.split())

    checks = {}
    score = 0
    warnings = []

    for key, rule in RULES.items():
        matched = any(re.search(p, text, re.IGNORECASE) for p in rule["patterns"])
        checks[key] = matched
        if matched:
            score += rule["weight"]
        else:
            warnings.append(f"缺少 {rule['name']}")

    # 字数过少的额外警告
    if word_count < 300:
        warnings.append(f"文档过短（约 {word_count} 字/词），建议 ≥ 300")
        score -= 10

    # 模板 Padding 占比计算（不导致失败）
    padding_ratio = calculate_padding_ratio(text)
    if padding_ratio > 30:
        warnings.append(f"模板 padding 占比 {padding_ratio:.1f}%，建议按内容块复用规则精简")

    # 批量模板重复段检测：仅统计作为行首精确匹配的一级/二级标题
    duplicated_sections = []
    lines = text.splitlines()
    # view/ 卷册是聚合文件，允许章节重复出现
    is_view_aggregation = "view/" in filepath.as_posix() or filepath.parts[:2] == ("view",)
    threshold = 35 if is_view_aggregation else 1
    for sec in BATCH_TEMPLATE_SECTIONS:
        # 转义后按行首匹配，避免子串命中（如 "## 反例" 命中 "### 反例 1"）
        pattern = re.compile(r"^" + re.escape(sec) + r"\s*$")
        count = sum(1 for line in lines if pattern.match(line.strip()))
        if count > threshold:
            duplicated_sections.append(f"{sec} 出现 {count} 次")

    # 预计算本文件锚点，用于跨文件/同文件锚点校验
    local_anchors = _build_anchors(text)

    # 死链检测
    dead_links = []
    for link_text, link_target, lineno in _extract_markdown_links(text):
        # 纯锚点（同文件内）：不同渲染器生成规则差异大，本门控不严格检测
        if link_target.startswith("#"):
            continue

        target = _resolve_relative_link(filepath, link_target, project_root)
        if target is None:
            continue

        if not _target_exists(target):
            try:
                resolved_rel = target.relative_to(project_root).as_posix()
            except ValueError:
                resolved_rel = link_target
            dead_links.append({
                "line": lineno,
                "text": link_text,
                "target": link_target,
                "resolved": resolved_rel,
            })
            continue

        # 跨文件锚点校验
        if "#" in link_target:
            anchor = link_target.split("#", 1)[1]
            try:
                target_text = target.read_text(encoding="utf-8", errors="replace")
                if anchor.lower() not in _build_anchors(target_text):
                    dead_links.append({
                        "line": lineno,
                        "text": link_text,
                        "target": link_target,
                        "resolved": target.relative_to(project_root).as_posix(),
                    })
            except Exception:
                pass

    # 交叉引用提取
    cross_refs = []
    for _, link_target, _ in _extract_markdown_links(text):
        if link_target.endswith(".md"):
            cross_refs.append(link_target)

    # 必须有定义和权威来源，且死链不能过多
    passed = (
        checks.get("definition", False)
        and checks.get("authority", False)
        and score >= MIN_SCORE
        and sum(1 for v in checks.values() if v) >= MIN_WEIGHTED
        and len(dead_links) <= 3
        and not duplicated_sections
    )

    return GateResult(
        path=rel,
        score=max(0, min(100, score)),
        passed=passed,
        checks=checks,
        warnings=warnings,
        duplicated_sections=duplicated_sections,
        dead_links=dead_links,
        cross_refs=cross_refs,
        padding_ratio=padding_ratio,
    )


def _load_glossary_terms(glossary_path: Path) -> Set[str]:
    """从 glossary-master.md 加载核心术语集合（英文 + 中文）"""
    terms: Set[str] = set()
    if not glossary_path.exists():
        return terms
    text = glossary_path.read_text(encoding="utf-8")
    for m in re.finditer(r"^#{3,4}\s+(.+?)\s*\(([^)]+)\)\s*$", text, re.MULTILINE):
        en = m.group(1).strip()
        cn = m.group(2).strip()
        if en:
            terms.add(en)
        if cn:
            terms.add(cn)
    return terms


def scan_directory(root: Path) -> Tuple[List[GateResult], List[TermConflict]]:
    root = root.resolve()
    project_root = root.parent
    results = []
    skip_patterns = [
        "99-reference/audit/",
        "99-reference/CHANGELOG",
        "99-reference/frontier-tracking/",
        "99-reference/course/learning-path.md",
        "99-reference/course/syllabus.md",
        "plans-tasks/",
        "__pycache__",
        ".venv",
        "_HISTORICAL_",
        "MASTER_PLAN.md",
    ]

    # 加载主术语表，只报告 glossary 中术语的跨文件定义冲突
    glossary_path = root / "99-reference" / "glossary" / "glossary-master.md"
    glossary_terms = _load_glossary_terms(glossary_path)

    # 术语定义收集
    term_defs: Dict[str, List[Tuple[str, str]]] = defaultdict(list)

    for md in root.rglob("*.md"):
        rel = md.relative_to(root)
        rel_posix = rel.as_posix()
        if any(sp in rel_posix for sp in skip_patterns):
            continue
        result = check_file(md, root, project_root)
        results.append(result)

        # 术语提取：仅保留 glossary 中的术语
        text = md.read_text(encoding="utf-8")
        local_terms = _extract_term_definitions(text, rel_posix)
        for term, path in local_terms.items():
            if term not in glossary_terms:
                continue
            # 定位术语出现的行号
            for lineno, line in enumerate(text.splitlines(), start=1):
                if term in line:
                    term_defs[term].append((path, f"第 {lineno} 行"))
                    break
            else:
                term_defs[term].append((path, "-"))

    # 只保留跨文件定义冲突；排除 glossary 自身与 99-reference 元数据文件
    conflicts = []
    meta_patterns = ("99-reference/glossary/", "99-reference/deliverables-manifest.md", "99-reference/tools/")
    for term, defs in term_defs.items():
        non_meta_defs = [d for d in defs if not any(d[0].startswith(p) for p in meta_patterns)]
        files = {d[0] for d in non_meta_defs}
        if len(files) > 1:
            conflicts.append(TermConflict(term=term, definitions=non_meta_defs))

    return results, conflicts


def format_result(r: GateResult) -> str:
    status = "✅ 通过" if r.passed else "❌ 未通过"
    detail = ", ".join(
        f"{'✓' if r.checks.get(k, False) else '✗'}{RULES[k]['name'][:2]}"
        for k in RULES
    )
    warn = "; ".join(r.warnings[:3]) if r.warnings else "无"
    extra = []
    if r.duplicated_sections:
        extra.append("模板重复: " + "; ".join(r.duplicated_sections))
    if r.dead_links:
        extra.append(f"死链 {len(r.dead_links)} 个")
    if r.padding_ratio > 30:
        extra.append(f"padding {r.padding_ratio:.1f}%")
    extra_str = " | ".join(extra) if extra else ""
    base = f"{status} [{r.score:>3}] {r.path} | {detail} | 警告: {warn}"
    if extra_str:
        base += f" | {extra_str}"
    return base


def _result_to_dict(r: GateResult) -> dict:
    return {
        "path": r.path,
        "score": r.score,
        "passed": r.passed,
        "checks": r.checks,
        "warnings": r.warnings,
        "duplicated_sections": r.duplicated_sections,
        "dead_links": r.dead_links,
        "cross_refs": r.cross_refs,
        "padding_ratio": round(r.padding_ratio, 2),
    }


def write_json_report(path: Path, results: List[GateResult], conflicts: List[TermConflict], summary: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "summary": summary,
        "results": [_result_to_dict(r) for r in results],
        "term_conflicts": [
            {
                "term": c.term,
                "definitions": [{"file": d[0], "location": d[1]} for d in c.definitions],
            }
            for c in conflicts
        ],
    }
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_md_report(path: Path, results: List[GateResult], conflicts: List[TermConflict], summary: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Quality Gate V2 报告",
        "",
        "## 概览",
        "",
        f"- 扫描文件数: {summary['total']}",
        f"- 通过: {summary['passed']}/{summary['total']} ({summary['pass_rate']:.1f}%)",
        f"- 未通过: {summary['failed']}",
        f"- 死链总数: {summary['dead_link_count']}",
        f"- 模板重复段文件数: {summary['duplicated_count']}",
        f"- Padding 占比超过 30% 的文件数: {summary.get('high_padding_count', 0)}",
        f"- 术语冲突数: {len(conflicts)}",
        "",
        "## 未通过文件详情",
        "",
    ]
    failures = [r for r in results if not r.passed]
    if not failures:
        lines.append("无")
    else:
        for r in failures:
            lines.append(f"### {r.path} (分数: {r.score})")
            lines.append("")
            lines.append("- 检查项:")
            for k, v in r.checks.items():
                lines.append(f"  - {'✅' if v else '❌'} {RULES[k]['name']}")
            if r.warnings:
                lines.append("- 警告:")
                for w in r.warnings:
                    lines.append(f"  - {w}")
            if r.duplicated_sections:
                lines.append("- 模板重复段:")
                for ds in r.duplicated_sections:
                    lines.append(f"  - {ds}")
            if r.dead_links:
                lines.append("- 死链:")
                for dl in r.dead_links:
                    lines.append(f"  - 第 {dl['line']} 行: [{dl['text']}]({dl['target']}) -> {dl['resolved']}")
            if r.padding_ratio > 30:
                lines.append(f"- 模板 Padding 占比: {r.padding_ratio:.1f}%")
            lines.append("")

    if conflicts:
        lines.append("## 术语定义冲突")
        lines.append("")
        for c in conflicts:
            lines.append(f"### {c.term}")
            for d in c.definitions:
                lines.append(f"- {d[0]} ({d[1]})")
            lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Markdown 内容质量门控 V2（含模板重复、死链、术语一致性检测）"
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="struct",
        help="目标文件或目录（默认: struct/）",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="遇到第一个未通过文件即退出",
    )
    parser.add_argument(
        "--only-failures",
        action="store_true",
        help="仅显示未通过的文件",
    )
    parser.add_argument(
        "--json",
        metavar="PATH",
        help="输出 JSON 格式报告到指定路径",
    )
    parser.add_argument(
        "--report",
        metavar="PATH",
        help="输出 Markdown 格式报告到指定路径",
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=MIN_SCORE,
        help=f"及格分数（默认 {MIN_SCORE}）",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    target = Path(args.target)
    if not target.is_absolute():
        target = project_root / target
    target = target.resolve()

    if not target.exists():
        print(f"错误：路径不存在 {target}", file=sys.stderr)
        sys.exit(1)

    root = project_root
    if target.is_file():
        results = [check_file(target, root, project_root)]
        conflicts = []
    else:
        results, conflicts = scan_directory(target)

    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    dead_link_count = sum(len(r.dead_links) for r in results)
    duplicated_count = sum(1 for r in results if r.duplicated_sections)
    high_padding_count = sum(1 for r in results if r.padding_ratio > 30)
    summary = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": passed / total * 100 if total else 0.0,
        "dead_link_count": dead_link_count,
        "duplicated_count": duplicated_count,
        "high_padding_count": high_padding_count,
        "min_score": args.min_score,
    }

    print(f"扫描文件数: {total}")
    print(f"质量基线: 定义 + 权威来源 必须满足，总分 ≥ {args.min_score}，通过项 ≥ {MIN_WEIGHTED}，死链 ≤ 3，无模板重复")
    print("-" * 110)

    for r in results:
        if args.only_failures and r.passed:
            continue
        print(format_result(r))
        if args.fail_fast and not r.passed:
            break

    print("-" * 110)
    print(
        f"统计: {passed}/{total} 通过，通过率 {summary['pass_rate']:.1f}%，"
        f"死链 {dead_link_count} 个，模板重复 {duplicated_count} 个，"
        f"padding 超 30% {high_padding_count} 个，术语冲突 {len(conflicts)} 个"
    )

    if args.json:
        write_json_report(Path(args.json), results, conflicts, summary)
        print(f"JSON 报告已保存: {args.json}")

    if args.report:
        write_md_report(Path(args.report), results, conflicts, summary)
        print(f"Markdown 报告已保存: {args.report}")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
