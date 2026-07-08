#!/usr/bin/env python3
"""
kg-query.py
===========

知识图谱查询接口。

用法示例:
    # 统计
    python kg-query.py stats

    # 列出所有标准
    python kg-query.py list-standards

    # 搜索术语
    python kg-query.py search-term "架构复用"

    # 查询与某实体相关的实体
    python kg-query.py related "架构复用"

    # 自定义 SPARQL
    python kg-query.py sparql "SELECT ?s ?label WHERE { ?s rdfs:label ?label } LIMIT 10"

"""

import argparse
import json
import re
from pathlib import Path
from typing import List, Tuple

from rdflib import Graph, Namespace, Literal, RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_KG = PROJECT_ROOT / "struct" / "99-reference" / "knowledge-graph" / "kg.ttl"

BASE_URI = "https://github.com/AdaMartin18010/Architecture/kg/"
AR = Namespace(BASE_URI)
ARO = Namespace(BASE_URI + "ontology/")


def load_graph(kg_path: Path) -> Graph:
    if not kg_path.exists():
        raise FileNotFoundError(f"找不到知识图谱: {kg_path}")
    g = Graph()
    g.parse(str(kg_path), format="turtle")
    return g


def literal_match(label: str, keyword: str) -> bool:
    return keyword.lower() in label.lower()


def find_entity(g: Graph, keyword: str) -> List[str]:
    """根据关键词查找实体 URI。"""
    results = []
    for s, o in g.subject_objects(RDFS.label):
        if isinstance(o, Literal) and literal_match(str(o), keyword):
            results.append(str(s))
    return results


def cmd_stats(g: Graph) -> dict:
    total_triples = len(g)
    q_classes = """
        SELECT ?cls (COUNT(?e) AS ?cnt) WHERE {
            ?e a ?cls .
            FILTER(STRSTARTS(STR(?cls), "https://github.com/AdaMartin18010/Architecture/kg/ontology/"))
        } GROUP BY ?cls ORDER BY DESC(?cnt)
    """
    classes = []
    for row in g.query(q_classes):
        cls_local = row.cls.split("/")[-1]
        classes.append({"class": cls_local, "count": int(row.cnt)})

    q_props = """
        SELECT ?p (COUNT(*) AS ?cnt) WHERE {
            ?s ?p ?o .
            FILTER(STRSTARTS(STR(?p), "https://github.com/AdaMartin18010/Architecture/kg/ontology/"))
        } GROUP BY ?p ORDER BY DESC(?cnt)
    """
    props = []
    for row in g.query(q_props):
        prop_local = row.p.split("/")[-1]
        props.append({"property": prop_local, "count": int(row.cnt)})

    return {
        "total_triples": total_triples,
        "classes": classes,
        "properties": props,
    }


def cmd_list_standards(g: Graph) -> List[dict]:
    q = """
        SELECT ?s ?label ?file ?line WHERE {
            ?s a aro:Standard ;
               rdfs:label ?label ;
               ar:sourceFile ?file ;
               ar:sourceLine ?line .
        } ORDER BY ?label
    """
    results = []
    for row in g.query(q, initNs={"aro": ARO, "ar": AR}):
        results.append({
            "uri": str(row.s),
            "label": str(row.label),
            "source_file": str(row.file),
            "source_line": int(row.line),
        })
    return results


def cmd_search_term(g: Graph, keyword: str) -> List[dict]:
    q = """
        SELECT ?s ?label ?type ?file ?line WHERE {
            ?s a ?type ;
               rdfs:label ?label ;
               ar:sourceFile ?file ;
               ar:sourceLine ?line .
            FILTER(CONTAINS(LCASE(STR(?label)), LCASE(?kw)))
        } ORDER BY ?label LIMIT 50
    """
    results = []
    for row in g.query(q, initNs={"ar": AR}, initBindings={"kw": Literal(keyword)}):
        results.append({
            "uri": str(row.s),
            "label": str(row.label),
            "type": str(row.type).split("/")[-1],
            "source_file": str(row.file),
            "source_line": int(row.line),
        })
    return results


def cmd_related(g: Graph, keyword: str) -> List[dict]:
    """查找与关键词匹配的实体通过对象属性直接关联的实体。"""
    entities = find_entity(g, keyword)
    if not entities:
        return []
    results = []
    for uri in entities[:5]:
        q = """
            SELECT ?p ?o ?label WHERE {
                ?s ?p ?o .
                ?o rdfs:label ?label .
                FILTER(?s = ?start)
                FILTER(STRSTARTS(STR(?p), "https://github.com/AdaMartin18010/Architecture/kg/ontology/"))
            } LIMIT 20
        """
        for row in g.query(q, initBindings={"start": URIRef(uri)}):
            results.append({
                "from": uri,
                "property": str(row.p).split("/")[-1],
                "to_uri": str(row.o),
                "to_label": str(row.label),
            })
    return results


def cmd_sparql(g: Graph, query: str) -> Tuple[List[str], List[dict]]:
    qres = g.query(query, initNs={"aro": ARO, "ar": AR, "rdfs": RDFS, "rdf": RDF})
    vars_ = [str(v) for v in qres.vars]
    rows = []
    for row in qres:
        rows.append({v: str(row[v]) for v in vars_})
    return vars_, rows


def main() -> int:
    parser = argparse.ArgumentParser(description="知识图谱查询接口")
    parser.add_argument("--kg", type=Path, default=DEFAULT_KG)
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("stats", help="图谱统计")
    sub.add_parser("list-standards", help="列出所有标准")

    p_search = sub.add_parser("search-term", help="搜索术语")
    p_search.add_argument("keyword")

    p_related = sub.add_parser("related", help="查询相关实体")
    p_related.add_argument("keyword")

    p_sparql = sub.add_parser("sparql", help="执行自定义 SPARQL")
    p_sparql.add_argument("query", nargs="+", help="SPARQL 查询字符串")

    args = parser.parse_args()

    try:
        g = load_graph(args.kg)
    except FileNotFoundError as e:
        print(e)
        return 1

    output = None
    if args.command == "stats":
        output = cmd_stats(g)
    elif args.command == "list-standards":
        output = cmd_list_standards(g)
    elif args.command == "search-term":
        output = cmd_search_term(g, args.keyword)
    elif args.command == "related":
        output = cmd_related(g, args.keyword)
    elif args.command == "sparql":
        query = " ".join(args.query)
        vars_, rows = cmd_sparql(g, query)
        output = {"vars": vars_, "rows": rows}

    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
