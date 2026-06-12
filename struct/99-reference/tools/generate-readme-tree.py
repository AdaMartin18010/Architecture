#!/usr/bin/env python3
"""
generate-readme-tree.py
根据 struct/ 实际目录结构生成 README.md 中的知识体系结构树。

用法:
    python generate-readme-tree.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path("e:/_src/Architecture")
STRUCT_ROOT = PROJECT_ROOT / "struct"
README_PATH = PROJECT_ROOT / "README.md"

# 目录简短描述映射（可扩展）
DESCRIPTIONS = {
    "01-meta-model-standards": "元模型与标准对齐",
    "01-iso-420xx-family": "ISO 42010/42020/42030 与 12207 族",
    "02-togaf-10-alignment": "TOGAF 10 企业架构",
    "03-iso-26550-ple": "ISO 26550 产品线工程",
    "04-archimate-4": "ArchiMate 3.2/4.0",
    "05-swebok-v4": "SWEBOK V4 知识领域",
    "06-formal-axioms": "形式化公理体系",
    "07-omg-ras": "OMG RAS 可复用资产",
    "08-fair4rs": "FAIR4RS 研究软件复用",
    "09-sysml-v2": "SysML v2 对齐",
    "10-mbse-reuse": "MBSE 与复用集成",
    "02-business-architecture-reuse": "业务架构复用",
    "02-business-capability": "业务能力建模",
    "03-value-stream": "价值流映射",
    "06-bpmn-dmn": "BPMN 2.0 / DMN 1.5",
    "07-defense-mission-engineering": "国防任务工程",
    "08-zachman-reuse-mapping": "Zachman 框架复用映射",
    "03-application-architecture-reuse": "应用架构复用",
    "01-layered-architecture": "分层架构模式",
    "02-microservices": "微服务架构",
    "03-app-service": "应用服务复用",
    "04-serverless": "Serverless 架构",
    "05-data-architecture": "数据架构复用",
    "06-event-driven": "事件驱动架构",
    "07-cloud-native-patterns": "云原生复用性矩阵 2026",
    "08-service-mesh": "服务网格通信模式",
    "09-eda-cqrs": "EDA/CQRS 深度",
    "10-tosca-dmn-platform": "TOSCA v2.0 / DMN 1.6",
    "11-idp-practices": "IDP 复用实践",
    "04-component-architecture-reuse": "组件架构复用",
    "01-component-models": "组件模型理论",
    "02-interface-contracts": "接口契约设计",
    "03-dependency-management": "依赖管理策略",
    "04-design-patterns": "设计模式与反模式",
    "05-version-strategy": "版本策略",
    "06-cloud-native-networking": "云原生网络",
    "07-language-ecosystems": "6 大语言生态深度对比",
    "05-functional-architecture-reuse": "功能架构复用",
    "01-api-design": "API 设计模式",
    "02-function-as-a-service": "FaaS 复用模式",
    "03-event-functions": "事件函数模式",
    "04-workflow-orchestration": "Temporal 工作流复用",
    "05-ai-llm-functions": "AI/LLM 功能复用",
    "06-mcp-a2a-protocols": "MCP + A2A 协议分析",
    "06-cross-layer-governance": "跨层治理与量化",
    "01-process-governance": "复用过程治理",
    "03-maturity-models": "成熟度模型（RCMM/RiSE/SPICE）",
    "04-finops-cost": "FinOps 成本分摊模板",
    "05-metrics-kpi": "四级度量指标体系",
    "06-up-downgrade-matrix": "升降级决策矩阵",
    "09-agentic-governance": "Agentic 治理",
    "07-formal-verification": "形式化验证",
    "01-tla-plus": "TLA+ 案例库",
    "02-alloy": "Alloy 案例库",
    "03-coq-isabelle": "Coq / Isabelle",
    "04-rust-type-system": "Rust 类型系统深化",
    "05-spark-ada": "SPARK/Ada 契约验证",
    "06-b-method": "B Method / Event-B",
    "07-vv-standards": "V&V 标准（IEEE 1012）",
    "08-emerging-trends": "形式化验证前沿",
    "09-comparative-matrices": "方法对比矩阵",
    "08-cognitive-architecture": "认知架构",
    "01-act-r-model": "ACT-R 模型",
    "02-bdi-model": "BDI 模型",
    "03-cognitive-load-theory": "认知负荷理论",
    "04-decision-making": "决策机制",
    "05-ai-cognitive-augmentation": "AI 认知增强",
    "09-value-quantification": "价值量化",
    "01-cocomo-ii-reuse": "COCOMO II 2026 校准",
    "02-roi-npv-models": "ROI 与 NPV 模型",
    "03-carbon-dimension": "碳排维度",
    "tools": "工具脚本",
    "10-supply-chain-security": "供应链安全",
    "01-slsa-framework": "SLSA 框架",
    "02-sbom-standards": "SBOM 标准",
    "03-attack-vectors": "攻击向量",
    "04-provenance-examples": "来源示例",
    "05-zero-trust-supply-chain": "零信任供应链",
    "06-case-studies": "案例研究",
    "07-owasp-scvs": "OWASP SCVS",
    "08-guac-supply-chain": "GUAC 供应链图",
    "09-owasp-asvs": "OWASP ASVS",
    "10-owasp-top10-2025": "OWASP Top 10 2025",
    "11-osps-baseline": "OSPS 基线",
    "12-nist-ssdf-update": "NIST SSDF 更新",
    "11-industrial-iot-otit": "工业 IoT / OT-IT 融合",
    "01-isa-95-model": "ISA-95 五层资产目录",
    "02-opc-ua-fx": "OPC UA FX 深化",
    "03-tsn-deterministic": "TSN 确定性网络",
    "04-plcopen-motion": "PLCopen Motion",
    "05-digital-twin-aas": "数字孪生 / AAS",
    "06-functional-safety": "功能安全（IEC 61508 / ISO 26262）",
    "07-edge-ai": "工业边缘 AI",
    "08-digital-twin-general": "数字孪生通用",
    "09-network-digital-twin": "网络数字孪生",
    "12-ai-native-reuse": "AI 原生复用",
    "01-mcp-protocol": "MCP 协议",
    "02-a2a-protocol": "A2A 协议",
    "03-agentic-infrastructure": "Agentic Infrastructure",
    "04-hybrid-a2a-mcp-poc": "A2A/MCP 混合 PoC",
    "05-probabilistic-contracts": "概率契约",
    "06-ai-governance": "AI 治理",
    "07-conformal-prediction": "Conformal Prediction",
    "13-emerging-trends": "前沿趋势",
    "01-platform-engineering": "平台工程成熟度",
    "02-modular-monolith": "模块化单体",
    "03-webassembly-components": "WASM Component Model",
    "04-green-architecture": "绿色架构",
    "05-rust-ecosystem": "Rust 生态",
    "06-regtech-ai": "RegTech AI",
    "07-green-software": "绿色软件",
    "09-frontier-tracking": "前沿跟踪",
    "99-reference": "参考索引",
    "audit": "审计报告",
    "chapters": "全书章节框架",
    "external-links": "外部链接",
    "frontier-tracking": "前沿跟踪",
    "glossary": "术语表",
    "knowledge-index": "知识索引",
    "standards-index": "标准索引",
    "templates": "模板",
    "tools": "工具脚本",
    "visualizations": "可视化",
}


def describe(name: str) -> str:
    return DESCRIPTIONS.get(name, name.replace("-", " "))


def build_tree() -> str:
    lines = ["```text", "struct/"]
    topic_dirs = sorted([d for d in STRUCT_ROOT.iterdir() if d.is_dir() and not d.name.startswith(".")])
    for topic in topic_dirs:
        subdirs = sorted([d for d in topic.iterdir() if d.is_dir() and not d.name.startswith(".")])
        is_last_topic = topic == topic_dirs[-1]
        topic_prefix = "└──" if is_last_topic else "├──"
        lines.append(f"{topic_prefix} {topic.name}/{' '*(35-len(topic.name))}# {describe(topic.name)}")
        for sub in subdirs:
            is_last_sub = sub == subdirs[-1]
            sub_prefix = "│   └──" if is_last_sub else "│   ├──"
            lines.append(f"{sub_prefix} {sub.name}/{' '*(31-len(sub.name))}# {describe(sub.name)}")
    lines.append("```")
    return "\n".join(lines)


def update_readme_tree(target_path: Path, require_exact: bool = True) -> bool:
    text = target_path.read_text(encoding="utf-8")
    new_tree = build_tree()
    # 找到 ```text\nstruct/\n...\n``` 块并替换
    pattern = re.compile(r"```text\nstruct/\n.*?\n```", re.DOTALL)
    if not pattern.search(text):
        if require_exact:
            print(f"[ERROR] 未在 {target_path.relative_to(PROJECT_ROOT)} 中找到 struct/ 树块", file=sys.stderr)
        return False
    new_text = pattern.sub(new_tree, text)
    target_path.write_text(new_text, encoding="utf-8")
    print(f"[OK] {target_path.relative_to(PROJECT_ROOT)} 知识体系树已更新")
    return True


if __name__ == "__main__":
    ok = update_readme_tree(README_PATH)
    # 同时更新 struct/README.md（如果存在且包含树块）
    struct_readme = PROJECT_ROOT / "struct" / "README.md"
    if struct_readme.exists():
        ok = update_readme_tree(struct_readme, require_exact=False) and ok
    sys.exit(0 if ok else 1)
