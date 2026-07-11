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
import yaml
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
    # 尾部 (?![\dA-Za-z]) 防止把 "420xx" 族占位截断成 "ISO/IEC/IEEE 420"
    (r"ISO/IEC(?:/IEEE)?\s+\d+(?::\d{4})?(?![\dA-Za-z])", "Standard"),
    # IEC 61508, IEC 63278 等
    (r"IEC\s+(?:TS\s+)?\d+(?::\d{4})?(?![\dA-Za-z])", "Standard"),
    # IEEE 1517-2010, IEEE Std 1012-2024 等
    (r"IEEE(?:\s+Std)?\s+\d+(?:\.\d+)?(?:-\d{4})?(?![\dA-Za-z])", "Standard"),
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
    # A2A v1.0.0 / A2A 2.0（必须带 v 前缀或为小数版本，防止误抽 "A2A 150+ 企业采用"）
    (r"A2A\s+(?:v\d+(?:\.\d+)*|\d+\.\d+(?:\.\d+)?)(?![\d.+])", "Protocol"),
    # OPC UA FX
    (r"OPC\s+UA\s*(?:FX)?", "Standard"),
    # ISA-95
    (r"ISA-95", "Standard"),
    # ISO 26262, ISO 21448
    (r"ISO\s+\d+(?::\d{4})?(?![\dA-Za-z])", "Standard"),
    # FAIR4RS
    (r"FAIR4RS", "Standard"),
    # SWEBOK V4
    (r"SWEBOK\s*V?\d+", "Standard"),
    # EU CRA 2024/2847
    (r"EU\s+CRA(?:\s+\d{4}/\d+)?", "Standard"),
]

# ---------------------------------------------------------------------------
# Canonical 名称归一
# ---------------------------------------------------------------------------

CANONICAL_NAMES_PATH = PROJECT_ROOT / "struct" / "99-reference" / "tools" / "canonical-names.yaml"


def load_canonical_names(path: Path = CANONICAL_NAMES_PATH) -> Dict[str, Dict]:
    """加载标准/协议的 canonical 名称字典。"""
    registry: Dict[str, Dict] = {}
    if not path.exists():
        return registry
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    for item in data.get("standards", []):
        canonical = item.get("canonical", "").strip()
        if not canonical:
            continue
        aliases = set(item.get("aliases", []))
        aliases.add(canonical)
        registry[canonical] = {
            "aliases": aliases,
            "invalid_versions": set(str(v) for v in item.get("invalid_versions", [])),
        }
    return registry


CANONICAL_REGISTRY = load_canonical_names()


def _core_key(name: str) -> Tuple[Optional[str], Optional[str]]:
    """把标准名解析为 (编号, 版本)。"""
    # 去掉常见组织前缀
    s = re.sub(r"^(?:ISO/IEC/IEEE|ISO/IEC|IEEE|IEC|ISO)\s+", "", name, flags=re.IGNORECASE)
    s = s.strip()
    m = re.match(r"(\d+(?:\.\d+)?)(?::(\d{4}))?", s)
    if not m:
        return (None, None)
    return (m.group(1), m.group(2))


def canonicalize_name(name: str, entity_type: str) -> Optional[str]:
    """将标准/协议名称归一到 canonical 名称；对不存在版本返回 None（跳过）。"""
    if entity_type not in ("Standard", "Protocol"):
        return name
    if not CANONICAL_REGISTRY:
        return name

    # 1) 完全匹配 canonical 或 alias（大小写不敏感）
    name_lower = name.lower()
    for canonical, meta in CANONICAL_REGISTRY.items():
        if name_lower == canonical.lower() or name_lower in {a.lower() for a in meta["aliases"]}:
            return canonical

    # 2) 前缀 + 版本匹配：检查是否命中某个 canonical 的 invalid_versions
    version_match = re.search(r"[:\s\-]\s*(\d{4}|\d+\.\d+)$", name)
    if version_match:
        version = version_match.group(1)
        prefix = name[: version_match.start()].strip().rstrip("-: ")
        for canonical, meta in CANONICAL_REGISTRY.items():
            if version in meta["invalid_versions"]:
                canon_core = re.sub(r"[^a-z0-9]", "", canonical.lower())
                test_core = re.sub(r"[^a-z0-9]", "", prefix.lower())
                if canon_core == test_core or test_core in canon_core:
                    return canonical

    # 3) 编号 + 版本模糊归一（处理缺组织前缀 / 缺版本 / 小写变体）
    num, ver = _core_key(name)
    if num:
        for canonical, meta in CANONICAL_REGISTRY.items():
            cnum, cver = _core_key(canonical)
            if cnum != num:
                continue
            # 明确版本必须一致；name 无版本时按 canonical 文件顺序匹配第一个
            if ver and cver and ver != cver:
                continue
            return canonical
    return name


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
        self.canonical_hits: Dict[str, str] = {}
        self.invalid_standard_aliases: set = set()

    def add_entity(
        self,
        name: str,
        entity_type: str,
        source_file: str,
        source_line: int,
        context: str = "",
    ) -> Optional[Entity]:
        name = normalize_name(name)
        canonical = canonicalize_name(name, entity_type)
        if canonical is None:
            self.invalid_standard_aliases.add(name)
            return None
        if canonical != name:
            self.canonical_hits[name] = canonical
        name = canonical
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

    def _is_valid_term(self, term: str, max_len: int = 60) -> bool:
        """判断一个文本是否应作为 Term 实体入库。"""
        if not (2 <= len(term) <= max_len):
            return False
        if re.match(r"^\d+$", term) or re.match(r"^https?://", term):
            return False
        if not re.search(r"[A-Za-z\u4e00-\u9fff]", term):
            return False
        # 跳过编号/章节/模板化标题
        if re.match(r"^\d+(\.\d+)*\s*[\.、]", term):
            return False
        if self._is_section_title(term):
            return False
        # 跳过整句/错误 Term（含中文标点或发布/已于等叙事词）
        if re.search(r"[，。！？；]", term) and len(term) > 20:
            return False
        if re.search(r"Specification.*(?:发布|已于|announced)|(?:发布|已于).*Specification", term, re.IGNORECASE):
            return False
        # 跳过标准/协议与组织名，由专门抽取器统一 canonicalize
        if self._looks_like_standard_or_org(term):
            return False
        # 如果 term 内部包含标准/协议名但整段不是标准名，说明是整句/标题
        for pattern, _ in STANDARD_PATTERNS:
            m = re.search(pattern, term, re.IGNORECASE)
            if m and (m.start() > 0 or m.end() < len(term)):
                return False
        return True

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
            if self._is_valid_term(term, max_len=80):
                self.add_entity(term, "Term", source_file, source_line, heading)

    # 模板化章节标题黑名单（大小写不敏感）
    _SECTION_BLACKLIST = [
        "矩阵", "使用方法", "维护流程", "条款映射", "轨道模型", "补充说明",
        "权威来源", "交叉引用", "概念定义", "属性", "关系说明", "形式化",
        "示例", "反例", "反模式", "避免建议", "正向示例", "核心标准对齐",
        "表 ", "图 ", "定义", "版本", "定位", "目录", "来源 url", "跟踪对象",
        "当前状态", "上一版本", "标准编号", "注册日期", "当前阶段", "预计发布",
        "技术委员会", "阶段追踪", "目标层", "因素层", "方法层", "基于社区讨论",
        "评估自动化", "资产入库", "供应商评估", "审计合规", "标准更新监测",
        "影响评估", "专家评审", "版本发布", "通知与同步", "架构评审",
        "架构债务评估", "架构评估", "持续架构",
        "上位概念", "下位概念", "等价/映射概念", "依赖概念", "正例",
        "核查日期", "合理推测", "对齐来源", "状态", "权威链接",
        "评估框架基准", "扩展位", "跟踪但不等待", "互补", "修订跟踪",
        "双向过程", "领域分析", "domain engineering", "软件生命周期复用过程",
        "继续使用", "预留", "对齐标准", "关键变更", "技术过程", "技术管理",
        "新概念", "明确支持", "最后更新", "维护者", "公理", "定理", "发布较早",
        "缺少", "不够量化", "作为过程框架", "结合现代", "结合 ai", "持续跟踪",
        "10 项", "过程完整", "与主流标准兼容", "实践导向", "对齐", "正式发布",
        "关键概念", "引用标准", "新增或强化", "知识管理", "结论", "质量特性",
        "质量评估需求", "新增", "扩展", "平台工程作为复用载体", "快速评估框架",
        "长期维护成本", "过程裁剪", "信息项映射", "过程资产库", "协同", "复用含义",
        "跨组织业务服务复用", "服务网格通信复用", "分类体系", "专门化到",
        "附录", "意义", "勘误说明", "变更", "分析", "细化", "强化", "必要准入",
        "必要", "领域工程、应用工程",
    ]

    def _is_section_title(self, term: str) -> bool:
        """判断加粗文本是否为章节/模板化标题而非术语。"""
        lower = term.lower()
        for kw in self._SECTION_BLACKLIST:
            if kw.lower() in lower:
                return True
        # 编号开头
        if re.match(r"^\d+(\.\d+)*\s*[\.、]", term):
            return True
        return False

    def _extract_bold_terms(
        self, line: str, source_file: str, source_line: int, context: str
    ) -> None:
        """提取加粗文本中可能的术语。"""
        # 匹配 **Term** 或 **Term (中文)**
        for match in re.finditer(r"\*\*([^\*\n]+?)\*\*", line):
            term = match.group(1).strip()
            if self._is_valid_term(term, max_len=60):
                self.add_entity(term, "Term", source_file, source_line, context)

    def _looks_like_standard_or_org(self, term: str) -> bool:
        """判断加粗/标题文本是否应作为 Standard/Protocol/Organization 抽取。"""
        for pattern, _ in STANDARD_PATTERNS + ORGANIZATION_PATTERNS:
            if re.fullmatch(pattern, term, re.IGNORECASE):
                return True
        return False

    def _extract_standards(
        self, line: str, source_file: str, source_line: int, context: str
    ) -> None:
        """提取标准与协议。"""
        for pattern, entity_type in STANDARD_PATTERNS:
            for match in re.finditer(pattern, line, re.IGNORECASE):
                name = match.group(0).strip()
                entity = self.add_entity(name, entity_type, source_file, source_line, context)
                if entity is None:
                    continue

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
                if self._is_valid_term(term, max_len=60):
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
                if self._is_valid_term(term, max_len=60):
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

        # Canonical 归一统计
        lines.extend([
            "",
            "## Canonical 归一统计",
            "",
            f"- 归一条目数: {len(self.canonical_hits)}",
            f"- 拦截的不存在版本/非法别名数: {len(self.invalid_standard_aliases)}",
            "",
        ])
        if self.canonical_hits:
            lines.extend(["| 原始写法 | 归一后 |", "|----------|--------|"])
            for src, dst in sorted(self.canonical_hits.items())[:50]:
                lines.append(f"| {src} | {dst} |")
        if self.invalid_standard_aliases:
            lines.extend(["", "**被拦截的别名**:"])
            for alias in sorted(self.invalid_standard_aliases)[:50]:
                lines.append(f"- {alias}")

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
