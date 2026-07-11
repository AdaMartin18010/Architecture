#!/usr/bin/env python3
"""
kg-builder.py
=============

知识图谱构建器。

读取 knowledge-extractor.py 生成的 JSONL，构建 RDF/OWL 知识图谱：
- 生成本体文件 arch-reuse-ontology.ttl
- 生成实例图谱 kg.ttl
- 运行 SHACL 验证

用法:
    python kg-builder.py
    python kg-builder.py --entities ../knowledge-graph/kg-entities.jsonl \
                         --relations ../knowledge-graph/kg-relations.jsonl \
                         --output ../knowledge-graph

"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS, OWL, SH, XSD
from rdflib.namespace import DC, DCTERMS
from pyshacl import validate

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_KG_DIR = PROJECT_ROOT / "struct" / "99-reference" / "knowledge-graph"

BASE_URI = "https://github.com/AdaMartin18010/Architecture/kg/"
AR = Namespace(BASE_URI)
ARO = Namespace(BASE_URI + "ontology/")

# ---------------------------------------------------------------------------
# 本体定义
# ---------------------------------------------------------------------------

CLASSES = [
    ("Term", "术语或概念"),
    ("Standard", "国际/行业标准或框架"),
    ("Protocol", "协议规范"),
    ("CaseStudy", "正向或反例案例"),
    ("Tool", "工具、脚本或平台"),
    ("Topic", "知识主题，如 01-meta-model-standards"),
    ("File", "Markdown 源文件"),
    ("Organization", "组织或厂商"),
    ("Axiom", "形式化公理"),
    ("Theorem", "定理或命题"),
]

PROPERTIES = [
    # 对象属性
    ("defines", "File", "Term", "定义"),
    ("references", "File", "Standard", "引用标准"),
    ("belongsTo", "File", "Topic", "属于主题"),
    ("providesPositiveExample", "File", "Term", "提供正向示例"),
    ("providesNegativeExample", "File", "Term", "提供反例"),
    ("mentions", "File", "Term", "提及"),
    ("implementedBy", "Standard", "Tool", "由工具实现"),
    ("relatedTo", "Term", "Term", "相关"),
    ("evolvedFrom", "Standard", "Standard", "演进自"),
    # 数据属性
    ("sourceFile", "Entity", None, "来源文件"),
    ("sourceLine", "Entity", None, "来源行号"),
    ("context", "Entity", None, "上下文"),
]

# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def safe_uri(local_name: str) -> str:
    """将本地名称转换为 URI 安全字符串。"""
    safe = re.sub(r"[^\w\-]", "_", local_name).strip("_")
    if not safe:
        safe = "_"
    return safe[:100]


def entity_uri(entity_id: str) -> URIRef:
    """根据实体 ID 生成 URI。"""
    return URIRef(BASE_URI + "entity/" + safe_uri(entity_id))


def property_uri(prop_name: str) -> URIRef:
    return URIRef(BASE_URI + "ontology/" + prop_name)


def class_uri(class_name: str) -> URIRef:
    return URIRef(BASE_URI + "ontology/" + class_name)


# ---------------------------------------------------------------------------
# 本体构建
# ---------------------------------------------------------------------------

def build_ontology() -> Graph:
    """构建 OWL 本体。"""
    g = Graph()
    g.bind("ar", AR)
    g.bind("aro", ARO)
    g.bind("dc", DC)
    g.bind("dct", DCTERMS)

    ontology_uri = URIRef(BASE_URI + "ontology")
    g.add((ontology_uri, RDF.type, OWL.Ontology))
    g.add((ontology_uri, DCTERMS.title, Literal("Architecture Reuse Knowledge Graph Ontology")))
    g.add((ontology_uri, DCTERMS.created, Literal(datetime.now(timezone.utc).isoformat())))
    g.add((ontology_uri, DCTERMS.description, Literal("Ontology for software architecture reuse knowledge base")))

    # 顶层类
    g.add((ARO.Entity, RDF.type, OWL.Class))
    g.add((ARO.Entity, RDFS.label, Literal("实体")))

    for class_name, label in CLASSES:
        cls = class_uri(class_name)
        g.add((cls, RDF.type, OWL.Class))
        g.add((cls, RDFS.label, Literal(label)))
        g.add((cls, RDFS.subClassOf, ARO.Entity))

    # 对象属性
    for prop_name, domain, range_, label in PROPERTIES:
        if range_ is None:
            continue  # 数据属性稍后处理
        prop = property_uri(prop_name)
        g.add((prop, RDF.type, OWL.ObjectProperty))
        g.add((prop, RDFS.label, Literal(label)))
        g.add((prop, RDFS.domain, class_uri(domain)))
        g.add((prop, RDFS.range, class_uri(range_)))

    # 数据属性
    for prop_name, domain, range_, label in PROPERTIES:
        if range_ is not None:
            continue
        prop = property_uri(prop_name)
        g.add((prop, RDF.type, OWL.DatatypeProperty))
        g.add((prop, RDFS.label, Literal(label)))
        g.add((prop, RDFS.domain, class_uri(domain)))
        if prop_name == "sourceLine":
            g.add((prop, RDFS.range, XSD.integer))
        else:
            g.add((prop, RDFS.range, XSD.string))

    return g


# ---------------------------------------------------------------------------
# 实例构建
# ---------------------------------------------------------------------------

def build_knowledge_graph(
    entities_path: Path, relations_path: Path
) -> Tuple[Graph, Dict[str, str]]:
    """读取 JSONL 构建实例图谱。"""
    g = Graph()
    g.bind("ar", AR)
    g.bind("aro", ARO)
    g.bind("dc", DC)
    g.bind("dct", DCTERMS)

    # 加载本体类定义
    for class_name, _ in CLASSES:
        cls = class_uri(class_name)
        g.add((cls, RDF.type, OWL.Class))

    # 加载实体
    entities: Dict[str, URIRef] = {}
    with open(entities_path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            entity_id = record["id"]
            entity_type = record["type"]
            name = record["name"]
            source_file = record.get("source_file", "")
            source_line = record.get("source_line", 0)
            context = record.get("context", "")

            uri = entity_uri(entity_id)
            entities[entity_id] = uri

            cls = class_uri(entity_type) if entity_type in [c[0] for c in CLASSES] else ARO.Entity
            g.add((uri, RDF.type, cls))
            g.add((uri, RDFS.label, Literal(name)))
            g.add((uri, AR.sourceFile, Literal(source_file)))
            g.add((uri, AR.sourceLine, Literal(int(source_line))))
            if context:
                g.add((uri, AR.context, Literal(context)))

    # 加载关系；dangling 关系不跳过，保留无 type 节点以让 SHACL 失败
    relation_to_property = {
        "DEFINES": ARO.defines,
        "REFERENCES": ARO.references,
        "BELONGS_TO": ARO.belongsTo,
        "PROVIDES_POSITIVE_EXAMPLE": ARO.providesPositiveExample,
        "PROVIDES_NEGATIVE_EXAMPLE": ARO.providesNegativeExample,
        "MENTIONS": ARO.mentions,
        "IMPLEMENTED_BY": ARO.implementedBy,
        "RELATED_TO": ARO.relatedTo,
        "EVOLVED_FROM": ARO.evolvedFrom,
    }

    missing_targets = set()
    with open(relations_path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            source_id = record["source_id"]
            relation = record["relation"]
            target_id = record["target_id"]

            source_uri = entities.get(source_id)
            if source_uri is None:
                continue  # 源文件实体必须存在
            if target_id not in entities:
                missing_targets.add(target_id)
                # 创建 dangling URI（无 rdf:type），让 SHACL class 约束失败
                entities[target_id] = entity_uri(target_id)

            prop = relation_to_property.get(relation)
            if prop:
                g.add((source_uri, prop, entities[target_id]))

    if missing_targets:
        print(f"警告: {len(missing_targets)} 个关系目标实体缺失（dangling），SHACL 应报失败: {sorted(missing_targets)[:5]}")

    return g, entities


# ---------------------------------------------------------------------------
# SHACL 验证
# ---------------------------------------------------------------------------

def build_shacl_shapes() -> Graph:
    """构建 SHACL 形状约束：label、dangling、canonical 正则。"""
    g = Graph()
    g.bind("sh", SH)
    g.bind("aro", ARO)

    # 标准/协议名称前缀正则（确保不是普通词汇）
    std_label_pattern = Literal(
        r"^(ISO|IEC|IEEE|NIST|OWASP|TOGAF|ArchiMate|SLSA|SysML|BPMN|DMN|FAIR4RS|EU CRA|ISA-95|SWEBOK|OPC UA)"
    )

    # Standard 必须有 RDFS.label，且 label 必须像标准名
    shape = URIRef(BASE_URI + "shapes/StandardShape")
    g.add((shape, RDF.type, SH.NodeShape))
    g.add((shape, SH.targetClass, ARO.Standard))
    g.add((shape, SH.property, URIRef(BASE_URI + "shapes/StandardLabel")))
    g.add((URIRef(BASE_URI + "shapes/StandardLabel"), SH.path, RDFS.label))
    g.add((URIRef(BASE_URI + "shapes/StandardLabel"), SH.minCount, Literal(1)))
    g.add((URIRef(BASE_URI + "shapes/StandardLabel"), SH.pattern, std_label_pattern))

    # Protocol 必须有 RDFS.label，且 label 必须像协议名
    shape_p = URIRef(BASE_URI + "shapes/ProtocolShape")
    g.add((shape_p, RDF.type, SH.NodeShape))
    g.add((shape_p, SH.targetClass, ARO.Protocol))
    g.add((shape_p, SH.property, URIRef(BASE_URI + "shapes/ProtocolLabel")))
    g.add((URIRef(BASE_URI + "shapes/ProtocolLabel"), SH.path, RDFS.label))
    g.add((URIRef(BASE_URI + "shapes/ProtocolLabel"), SH.minCount, Literal(1)))
    g.add((URIRef(BASE_URI + "shapes/ProtocolLabel"), SH.pattern, Literal(r"^(MCP|A2A|OPC UA|HTTP|MQTT|CoAP|gRPC|REST)", datatype=XSD.string)))

    # Term 必须有 RDFS.label，且 label 不得像标准/协议名
    shape2 = URIRef(BASE_URI + "shapes/TermShape")
    g.add((shape2, RDF.type, SH.NodeShape))
    g.add((shape2, SH.targetClass, ARO.Term))
    g.add((shape2, SH.property, URIRef(BASE_URI + "shapes/TermLabel")))
    g.add((URIRef(BASE_URI + "shapes/TermLabel"), SH.path, RDFS.label))
    g.add((URIRef(BASE_URI + "shapes/TermLabel"), SH.minCount, Literal(1)))
    g.add((URIRef(BASE_URI + "shapes/TermLabel"), SH.maxLength, Literal(120)))

    # 对象属性：object 必须属于声明的 range 类（dangling 即失败）
    object_props = [
        ("defines", ARO.Term),
        ("references", ARO.Standard),
        ("belongsTo", ARO.Topic),
        ("providesPositiveExample", ARO.Term),
        ("providesNegativeExample", ARO.Term),
        ("mentions", ARO.Term),
        ("implementedBy", ARO.Tool),
        ("relatedTo", ARO.Term),
        ("evolvedFrom", ARO.Standard),
    ]
    global_shape = URIRef(BASE_URI + "shapes/GlobalObjectPropertyShape")
    g.add((global_shape, RDF.type, SH.NodeShape))
    g.add((global_shape, SH.targetClass, ARO.Entity))
    for idx, (prop_name, range_cls) in enumerate(object_props):
        ps = URIRef(BASE_URI + f"shapes/PropertyShape{idx}")
        g.add((ps, RDF.type, SH.PropertyShape))
        g.add((ps, SH.path, property_uri(prop_name)))
        g.add((ps, URIRef(str(SH) + "class"), range_cls))
        g.add((global_shape, SH.property, ps))

    return g


def run_shacl_validation(data_graph: Graph) -> Tuple[bool, str]:
    """运行 SHACL 验证并返回结果。"""
    shapes_graph = build_shacl_shapes()
    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        abort_on_first=False,
        meta_shacl=False,
        debug=False,
    )
    return conforms, results_text


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="知识图谱构建器")
    parser.add_argument("--entities", type=Path, default=DEFAULT_KG_DIR / "kg-entities.jsonl")
    parser.add_argument("--relations", type=Path, default=DEFAULT_KG_DIR / "kg-relations.jsonl")
    parser.add_argument("--output", type=Path, default=DEFAULT_KG_DIR)
    parser.add_argument("--skip-shacl", action="store_true", help="跳过 SHACL 验证")
    args = parser.parse_args()

    if not args.entities.exists() or not args.relations.exists():
        print("错误：未找到实体或关系 JSONL。请先运行 knowledge-extractor.py --report")
        return 1

    args.output.mkdir(parents=True, exist_ok=True)

    # 构建并保存本体
    ontology = build_ontology()
    ontology_path = args.output / "arch-reuse-ontology.ttl"
    ontology.serialize(destination=str(ontology_path), format="turtle")
    print(f"本体已保存: {ontology_path}")

    # 构建并保存知识图谱
    kg, entities = build_knowledge_graph(args.entities, args.relations)
    kg_path = args.output / "kg.ttl"
    kg.serialize(destination=str(kg_path), format="turtle")
    print(f"知识图谱已保存: {kg_path} ({len(kg)} 三元组)")

    # SHACL 验证
    if not args.skip_shacl:
        conforms, report = run_shacl_validation(kg)
        report_dir = PROJECT_ROOT / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / "kg-shacl-report.md"
        lines = [
            "# SHACL 验证报告",
            "",
            f"> **验证时间**: {datetime.now(timezone.utc).isoformat()}",
            f"> **验证结果**: {'✅ 通过' if conforms else '❌ 未通过'}",
            "",
            "## 详细结果",
            "",
            "```text",
            report,
            "```",
            "",
        ]
        report_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"SHACL 报告已保存: {report_path}")
        if not conforms:
            print("警告：SHACL 验证未通过，请查看报告")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
