#!/usr/bin/env python3
"""
knowledge-extractor.py
======================

Markdown 知识抽取器。

从 struct/ 下的 Markdown 文档中提取实体（术语、标准、案例、工具、主题等）
与关系（定义、引用、属于主题、正/反例等），输出为 JSONL，供知识图谱使用。

用法:
    python knowledge-extractor.py
    python knowledge-extractor.py --struct-dir ../../.. --output-dir ../knowledge-graph
    python knowledge-extractor.py --report

输出:
    - kg-entities.jsonl
    - kg-relations.jsonl
    - kg-extraction-report.md（--report 时）

"""

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_STRUCT_DIR = PROJECT_ROOT / "struct"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "struct" / "99-reference" / "knowledge-graph"

# 标准/框架/协议的关键词与正则
STANDARD_PATTERNS = [
    # ISO/IEC/IEEE 42010:2022, ISO/IEC 25010:2023 等
    (r"ISO/IEC(?:/IEEE)?\s+\d+(?::\d{4})?", "Standard"),
    # IEC 61508, IEC 63278 等
    (r"IEC\s+(?:TS\s+)?\d+(?::\d{4})?", "Standard"),
    # IEEE 1517-2010, IEEE 1012-2024 等
    (r"IEEE\s+\d+(?:\.\d+)?(?:-\d{4})?", "Standard"),
    # NIST SP 800-218, NIST AI RMF 等
    (r"NIST\s+(?:SP\s+)?\d{3}(?:[A-Z]|-\d+)?(?:\s+Rev\.\s*\d+)?", "Standard"),
    # OWASP Top 10, OWASP ASVS 等
    (r"OWASP\s+(?:Top\s+10\s+(?:for\s+Agentic\s+AI|MCP)?|ASVS|SCVS)", "Standard"),
    # SLSA 1.2
    (r"SLSA\s+(?:\d+\.\d+|L\d+)", "Standard"),
    # TOGAF 10
    (r"TOGAF\s*(?:Standard,?)?\s*\d+(?:th\s+Edition)?", "Standard"),
    # ArchiMate 3.2 / 4.0
    (r"ArchiMate\s*\d+(?:\.\d+)?", "Standard"),
    # SysML v2
    (r"SysML\s*v?\d+(?:\.\d+)?", "Standard"),
    # BPMN 2.0, DMN 1.5
    (r"(?:BPMN|DMN)\s*\d+(?:\.\d+)?", "Standard"),
    # MCP 2025-11-25, MCP 2026-07-28
    (r"MCP\s+\d{4}-\d{2}-\d{2}(?:\s+RC)?", "Protocol"),
    # A2A v1.0.0
    (r"A2A\s+v?\d+(?:\.\d+)*", "Protocol"),
    # OPC UA FX
    (r"OPC\s+UA\s*(?:FX)?", "Standard"),
    # ISA-95
    (r"ISA-95", "Standard"),
    # ISO 26262, ISO 21448
    (r"ISO\s+\d+(?::\d{4})?", "Standard"),
    # FAIR4RS
    (r"FAIR4RS", "Standard"),
    # SWEBOK V4
    (r"SWEBOK\s*V?\d+", "Standard"),
    # EU CRA 2024/2847
    (r"EU\s+CRA(?:\s+\d{4}/\d+)?", "Standard"),
]

# 组织/厂商
ORGANIZATION_PATTERNS = [
    (r"The Open Group", "Organization"),
    (r"ISO", "Organization"),
    (r"IEC", "Organization"),
    (r"IEEE", "Organization"),
    (r"NIST", "Organization"),
    (r"OWASP", "Organization"),
    (r"OpenSSF", "Organization"),
    (r"CNCF", "Organization"),
    (r"OMG", "Organization"),
    (r"W3C", "Organization"),
    (r"Google Cloud", "Organization"),
    (r"Microsoft", "Organization"),
    (r"Anthropic", "Organization"),
    (r"Spotify", "Organization"),
    (r"Netflix", "Organization"),
    (r"ING", "Organization"),
]

# 需要跳过的文件/目录模式
SKIP_PATTERNS = [
    "_ARCHIVE",
    "_HISTORICAL",
    "__pycache__",
    ".tmp",
]

# ---------------------------------------------------------------------------
# 类型与常量
# ---------------------------------------------------------------------------

class Entity:
    def __init__(
        self,
        id: str,
        name: str,
        type: str,
        source_file: str,
        source_line: int,
        context: str = "",
    ):
        self.id = id
        self.name = name
        self.type = type
        self.source_file = source_file
        self.source_line = source_line
        self.context = context

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "source_file": self.source_file,
            "source_line": self.source_line,
            "context": self.context,
        }


class Relation:
    def __init__(
        self,
        source_id: str,
        relation: str,
        target_id: str,
        source_file: str,
        source_line: int,
        weight: float = 1.0,
    ):
        self.source_id = source_id
        self.relation = relation
        self.target_id = target_id
        self.source_file = source_file
        self.source_line = source_line
        self.weight = weight

    def to_dict(self) -> Dict:
        return {
            "source_id": self.source_id,
            "relation": self.relation,
            "target_id": self.target_id,
            "source_file": self.source_file,
            "source_line": self.source_line,
            "weight": self.weight,
        }


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def should_skip(path: Path) -> bool:
    """判断文件或目录是否应跳过。"""
    for pat in SKIP_PATTERNS:
        if pat in path.parts:
            return True
    return False


def normalize_name(name: str) -> str:
    """规范化实体名称。"""
    return " ".join(name.split())


def make_id(entity_type: str, name: str) -> str:
    """为实体生成稳定 ID。"""
    safe = re.sub(r"[^\w\-]", "_", normalize_name(name)).strip("_")
    return f"{entity_type}:{safe}"[:120]


def extract_topic_from_path(file_path: Path, struct_dir: Path) -> Optional[str]:
    """从文件路径提取主题（如 01-meta-model-standards）。"""
    rel_parts = file_path.relative_to(struct_dir).parts
    if len(rel_parts) > 0 and re.match(r"^\d{2}-", rel_parts[0]):
        return rel_parts[0]
    return None


def detect_section(line: str) -> Optional[str]:
    """根据行内容检测当前章节类型。"""
    line_lower = line.lower()
    if "概念定义" in line or "## 定义" in line:
        return "definition"
    if "正向示例" in line or "positive example" in line_lower or "案例" in line and "失败" not in line_lower:
        return "positive_example"
    if "反例" in line or "anti-pattern" in line_lower or "失败案例" in line:
        return "negative_example"
    if "权威来源" in line or "authoritative source" in line_lower:
        return "authoritative_source"
    if "分析" in line or "analysis" in line_lower:
        return "analysis"
    return None


# ---------------------------------------------------------------------------
# 提取器
# ---------------------------------------------------------------------------

class KnowledgeExtractor:
    def __init__(self, struct_dir: Path):
        self.struct_dir = struct_dir
        self.entities: Dict[str, Entity] = {}
        self.relations: List[Relation] = []
        self.file_topic_cache: Dict[Path, Optional[str]] = {}
        self.section_stack: List[str] = []

    def add_entity(
        self,
        name: str,
        entity_type: str,
        source_file: str,
        source_line: int,
        context: str = "",
    ) -> Entity:
        name = normalize_name(name)
        entity_id = make_id(entity_type, name)
        # 如果同名同类型已存在，保留第一次出现的元数据
        if entity_id not in self.entities:
            self.entities[entity_id] = Entity(
                id=entity_id,
                name=name,
                type=entity_type,
                source_file=source_file,
                source_line=source_line,
                context=context,
            )
        return self.entities[entity_id]

    def add_relation(
        self,
        source_id: str,
        relation: str,
        target_id: str,
        source_file: str,
        source_line: int,
        weight: float = 1.0,
    ) -> None:
        self.relations.append(
            Relation(
                source_id=source_id,
                relation=relation,
                target_id=target_id,
                source_file=source_file,
                source_line=source_line,
                weight=weight,
            )
        )

    def extract_from_file(self, file_path: Path) -> None:
        """从单个 Markdown 文件提取实体与关系。"""
        if should_skip(file_path):
            return

        rel_path = file_path.relative_to(PROJECT_ROOT).as_posix()
        topic = extract_topic_from_path(file_path, self.struct_dir)

        try:
            text = file_path.read_text(encoding="utf-8")
        except Exception:
            return

        lines = text.splitlines()
        current_heading = ""

        # 文件实体
        file_entity = self.add_entity(
            name=str(rel_path),
            entity_type="File",
            source_file=rel_path,
            source_line=1,
            context=current_heading,
        )

        # 主题实体与 BELONGS_TO 关系
        if topic:
            topic_entity = self.add_entity(
                name=topic,
                entity_type="Topic",
                source_file=rel_path,
                source_line=1,
            )
            self.add_relation(
                source_id=file_entity.id,
                relation="BELONGS_TO",
                target_id=topic_entity.id,
                source_file=rel_path,
                source_line=1,
            )

        for line_no, raw_line in enumerate(lines, start=1):
            line = raw_line.strip()
            if not line:
                continue

            # 检测标题
            heading_match = re.match(r"^(#{1,4})\s+(.+)$", line)
            if heading_match:
                current_heading = heading_match.group(2).strip()
                # 提取术语型标题（如 "### Component (组件)"）
                self._extract_term_heading(current_heading, rel_path, line_no)
                # 检测章节类型
                section = detect_section(line)
                if section:
                    if section in ("definition", "authoritative_source", "analysis"):
                        self.section_stack = [section]
                    else:
                        self.section_stack.append(section)
                continue

            # 提取加粗术语
            self._extract_bold_terms(line, rel_path, line_no, current_heading)

            # 提取标准/协议
            self._extract_standards(line, rel_path, line_no, current_heading)

            # 提取组织
            self._extract_organizations(line, rel_path, line_no, current_heading)

            # 提取案例
            self._extract_cases(line, rel_path, line_no, current_heading)

            # 提取 Markdown 内部链接作为关系
            self._extract_internal_links(line, file_entity.id, rel_path, line_no)

            # 根据当前章节建立文件与标准/术语的关系
            self._infer_section_relations(
                line, file_entity.id, rel_path, line_no, current_heading
            )

    def _extract_term_heading(
        self, heading: str, source_file: str, source_line: int
    ) -> None:
        """从标题中提取术语（如 "### Term (中文)"）。"""
        # 匹配 "### Term" 或 "### Term (中文)"
        match = re.match(r"^([^\(（]+?)(?:\s*[\(（]([^\)）]+)[\)）])?$", heading)
        if not match:
            return
        term_en = match.group(1).strip()
        term_zh = match.group(2).strip() if match.group(2) else ""
        # 只保留看起来像术语的标题（长度适中、非纯中文短句）
        for term in (term_en, term_zh):
            if term and 2 <= len(term) <= 80 and re.search(r"[A-Za-z\u4e00-\u9fff]", term):
                self.add_entity(term, "Term", source_file, source_line, heading)

    def _extract_bold_terms(
        self, line: str, source_file: str, source_line: int, context: str
    ) -> None:
        """提取加粗文本中可能的术语。"""
        # 匹配 **Term** 或 **Term (中文)**
        for match in re.finditer(r"\*\*([^\*\n]+?)\*\*", line):
            term = match.group(1).strip()
            # 过滤过长、过短、纯数字、URL
            if (
                2 <= len(term) <= 60
                and not re.match(r"^\d+$", term)
                and not re.match(r"^https?://", term)
                and re.search(r"[A-Za-z\u4e00-\u9fff]", term)
            ):
                self.add_entity(term, "Term", source_file, source_line, context)

    def _extract_standards(
        self, line: str, source_file: str, source_line: int, context: str
    ) -> None:
        """提取标准与协议。"""
        for pattern, entity_type in STANDARD_PATTERNS:
            for match in re.finditer(pattern, line, re.IGNORECASE):
                name = match.group(0).strip()
                self.add_entity(name, entity_type, source_file, source_line, context)

    def _extract_organizations(
        self, line: str, source_file: str, source_line: int, context: str
    ) -> None:
        """提取组织/厂商。"""
        for pattern, entity_type in ORGANIZATION_PATTERNS:
            for match in re.finditer(pattern, line, re.IGNORECASE):
                name = match.group(0).strip()
                self.add_entity(name, entity_type, source_file, source_line, context)

    def _extract_cases(
        self, line: str, source_file: str, source_line: int, context: str
    ) -> None:
        """提取案例标题。"""
        # 匹配 "### 案例 N：标题" 或 "### Case N: Title"
        match = re.match(r"^#{1,4}\s+(?:案例|Case)\s*\d*[:：]\s*(.+)$", line, re.IGNORECASE)
        if match:
            case_name = match.group(1).strip()
            if case_name:
                self.add_entity(case_name, "CaseStudy", source_file, source_line, context)

    def _extract_internal_links(
        self, line: str, file_entity_id: str, source_file: str, source_line: int
    ) -> None:
        """提取内部 Markdown 链接作为 REFERENCES 关系。"""
        for match in re.finditer(r"\[([^\]]+)\]\(([^)\s]+)\)", line):
            target = match.group(2).strip()
            if target.startswith("http") or target.startswith("#") or target.startswith("mailto:"):
                continue
            # 目录链接或文件链接
            target_clean = target.rstrip("/")
            if target_clean.endswith(".md"):
                target_path = target_clean
            else:
                target_path = f"{target_clean}/README.md"
            target_entity = self.add_entity(
                target_path, "File", source_file, source_line
            )
            self.add_relation(
                source_id=file_entity_id,
                relation="REFERENCES",
                target_id=target_entity.id,
                source_file=source_file,
                source_line=source_line,
            )

    def _infer_section_relations(
        self,
        line: str,
        file_entity_id: str,
        source_file: str,
        source_line: int,
        context: str,
    ) -> None:
        """根据当前章节推断文件与标准/术语的关系。"""
        if not self.section_stack:
            return

        current_section = self.section_stack[-1]

        # 在概念定义章节出现的术语，文件 DEFINES 该术语
        if current_section == "definition":
            for match in re.finditer(r"\*\*([^\*\n]+?)\*\*", line):
                term = match.group(1).strip()
                if 2 <= len(term) <= 60:
                    entity = self.add_entity(term, "Term", source_file, source_line, context)
                    self.add_relation(
                        source_id=file_entity_id,
                        relation="DEFINES",
                        target_id=entity.id,
                        source_file=source_file,
                        source_line=source_line,
                    )

        # 在正/反例章节出现的案例，文件 PROVIDES_POSITIVE/NEGATIVE_EXAMPLE
        if current_section in ("positive_example", "negative_example"):
            rel = "PROVIDES_POSITIVE_EXAMPLE" if current_section == "positive_example" else "PROVIDES_NEGATIVE_EXAMPLE"
            for match in re.finditer(r"\*\*([^\*\n]+?)\*\*", line):
                term = match.group(1).strip()
                if 2 <= len(term) <= 60:
                    entity = self.add_entity(term, "Term", source_file, source_line, context)
                    self.add_relation(
                        source_id=file_entity_id,
                        relation=rel,
                        target_id=entity.id,
                        source_file=source_file,
                        source_line=source_line,
                    )

    def run(self) -> None:
        """遍历 struct/ 下所有 Markdown 文件并提取。"""
        md_files = sorted(self.struct_dir.rglob("*.md"))
        for file_path in md_files:
            self.extract_from_file(file_path)

    def save(self, output_dir: Path) -> Tuple[Path, Path]:
        """保存实体与关系到 JSONL。"""
        output_dir.mkdir(parents=True, exist_ok=True)
        entities_path = output_dir / "kg-entities.jsonl"
        relations_path = output_dir / "kg-relations.jsonl"

        with open(entities_path, "w", encoding="utf-8") as f:
            for entity in self.entities.values():
                f.write(json.dumps(entity.to_dict(), ensure_ascii=False) + "\n")

        with open(relations_path, "w", encoding="utf-8") as f:
            for relation in self.relations:
                f.write(json.dumps(relation.to_dict(), ensure_ascii=False) + "\n")

        return entities_path, relations_path

    def generate_report(self, output_dir: Path) -> Path:
        """生成抽取质量报告。"""
        report_path = output_dir / "kg-extraction-report.md"

        type_counts = Counter(e.type for e in self.entities.values())
        relation_counts = Counter(r.relation for r in self.relations)

        # 文件覆盖度
        covered_files = set(
            e.source_file for e in self.entities.values() if e.type != "File"
        )
        all_files = set(
            p.relative_to(PROJECT_ROOT).as_posix()
            for p in self.struct_dir.rglob("*.md")
            if not should_skip(p)
        )
        coverage = len(covered_files) / len(all_files) if all_files else 0

        lines = [
            "# 知识抽取质量报告",
            "",
            f"> **生成时间**: {datetime.now(timezone.utc).isoformat()}",
            f"> **源目录**: `struct/`",
            f"> **总 Markdown 文件数**: {len(all_files)}",
            f"> **被抽取覆盖的文件数**: {len(covered_files)}",
            f"> **覆盖率**: {coverage:.1%}",
            "",
            "## 实体统计",
            "",
            "| 实体类型 | 数量 |",
            "|----------|------|",
        ]
        for etype, count in type_counts.most_common():
            lines.append(f"| {etype} | {count} |")

        lines.extend([
            "",
            "## 关系统计",
            "",
            "| 关系类型 | 数量 |",
            "|----------|------|",
        ])
        for rel, count in relation_counts.most_common():
            lines.append(f"| {rel} | {count} |")

        lines.extend([
            "",
            "## 高频实体",
            "",
            "| 实体名称 | 类型 | 出现次数 |",
            "|----------|------|----------|",
        ])
        entity_freq = Counter(e.name for e in self.entities.values())
        for name, count in entity_freq.most_common(20):
            etype = next(e.type for e in self.entities.values() if e.name == name)
            lines.append(f"| {name} | {etype} | {count} |")

        lines.extend([
            "",
            "## 输出文件",
            "",
            "- `kg-entities.jsonl`",
            "- `kg-relations.jsonl`",
            "",
            "---",
            "> 本报告由 `knowledge-extractor.py` 自动生成",
        ])

        report_path.write_text("\n".join(lines), encoding="utf-8")
        return report_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Markdown 知识抽取器")
    parser.add_argument("--struct-dir", type=Path, default=DEFAULT_STRUCT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--report", action="store_true", help="生成抽取质量报告")
    args = parser.parse_args()

    extractor = KnowledgeExtractor(struct_dir=args.struct_dir)
    extractor.run()
    entities_path, relations_path = extractor.save(args.output_dir)

    print(f"实体已保存: {entities_path} ({len(extractor.entities)} 条)")
    print(f"关系已保存: {relations_path} ({len(extractor.relations)} 条)")

    if args.report:
        report_dir = PROJECT_ROOT / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = extractor.generate_report(report_dir)
        print(f"报告已生成: {report_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
