#!/usr/bin/env python3
"""
OWASP ASVS 5.0.0 复用安全检查清单 CLI
版本: 2026-06-10
对齐: OWASP ASVS 5.0.0, OWASP Top 10:2025
"""

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from pathlib import Path


@dataclass
class CheckItem:
    id: str
    category: str
    description: str
    level: int  # 1, 2, 3
    applies_to_reuse: bool
    verification_method: str
    pass_criteria: str
    status: str = "pending"  # pending, pass, fail, na
    notes: str = ""


ASVS_REUSE_CHECKS = [
    CheckItem("V1.1.1", "架构", "安全边界和信任边界在架构文档中明确标识", 1, True,
              "架构审查", "威胁模型包含所有第三方组件"),
    CheckItem("V1.2.3", "架构", "所有外部依赖被标识并纳入威胁建模", 1, True,
              "依赖分析", "威胁模型包含传递依赖"),
    CheckItem("V5.1.1", "输入验证", "所有输入使用白名单验证", 1, True,
              "代码审查", "复用的解析库实现安全解析"),
    CheckItem("V5.2.4", "序列化", "序列化操作使用安全类型系统", 2, True,
              "SCA扫描", "无已知反序列化漏洞"),
    CheckItem("V6.1.1", "加密", "仅使用行业验证的加密算法", 1, True,
              "加密审查", "无已弃用算法"),
    CheckItem("V6.2.2", "密钥管理", "密钥管理使用专用服务", 2, True,
              "配置审查", "无硬编码密钥"),
    CheckItem("V8.1.1", "数据保护", "数据分类和对应保护措施", 2, True,
              "数据流审查", "数据处理符合分类要求"),
    CheckItem("V11.1.1", "供应链", "维护所有第三方组件的SBOM", 1, True,
              "SBOM验证", "SPDX或CycloneDX格式完整"),
    CheckItem("V11.1.2", "供应链", "定期扫描第三方组件漏洞", 1, True,
              "SCA扫描", "无高危/严重CVE"),
    CheckItem("V11.1.3", "供应链", "验证第三方组件的完整性和来源", 2, True,
              "签名验证", "SLSA L2+或等价验证"),
    CheckItem("V11.1.4", "供应链", "评估第三方组件维护状态", 2, True,
              "社区分析", "最近6个月活跃"),
    CheckItem("V11.2.1", "供应链", "建立第三方组件退出策略", 2, True,
              "文档审查", "有替代方案和迁移计划"),
    CheckItem("V12.1.1", "API安全", "API实现认证和授权", 1, True,
              "API测试", "未授权访问被拒绝"),
]


def run_checklist(target_level: int = 2, output_format: str = "markdown") -> Dict:
    """执行 ASVS 复用安全检查清单"""
    results = {
        "target_level": target_level,
        "total": 0,
        "applicable": 0,
        "passed": 0,
        "failed": 0,
        "pending": 0,
        "items": []
    }
    
    for item in ASVS_REUSE_CHECKS:
        if item.level <= target_level and item.applies_to_reuse:
            results["applicable"] += 1
            results["items"].append(asdict(item))
    
    results["total"] = len(ASVS_REUSE_CHECKS)
    return results


def generate_markdown_report(results: Dict) -> str:
    """生成 Markdown 报告"""
    lines = [
        "# OWASP ASVS 5.0.0 复用安全检查清单报告",
        f"",
        f"**目标等级**: L{results['target_level']}",
        f"**适用检查项**: {results['applicable']} / {results['total']}",
        f"",
        "| 检查项 | 类别 | 描述 | 等级 | 验证方法 | 通过标准 | 状态 |",
        "|:---|:---|:---|:---:|:---|:---|:---:|",
    ]
    
    for item in results["items"]:
        lines.append(
            f"| {item['id']} | {item['category']} | {item['description']} | "
            f"L{item['level']} | {item['verification_method']} | "
            f"{item['pass_criteria']} | {item['status']} |"
        )
    
    lines.append("")
    lines.append("> **注意**: 本检查清单需结合人工审查和自动化工具执行。"
    )
    lines.append("> **对齐标准**: OWASP ASVS 5.0.0 (2025-05-30)")
    
    return "\n".join(lines)


def generate_json_report(results: Dict) -> str:
    """生成 JSON 报告"""
    return json.dumps(results, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="OWASP ASVS 5.0.0 复用安全检查清单 CLI"
    )
    parser.add_argument(
        "--level", type=int, choices=[1, 2, 3], default=2,
        help="目标 ASVS 等级 (默认: 2)"
    )
    parser.add_argument(
        "--format", choices=["markdown", "json"], default="markdown",
        help="输出格式 (默认: markdown)"
    )
    parser.add_argument(
        "--output", type=str, default="-",
        help="输出文件 (默认: 标准输出)"
    )
    
    args = parser.parse_args()
    
    results = run_checklist(args.level, args.format)
    
    if args.format == "markdown":
        report = generate_markdown_report(results)
    else:
        report = generate_json_report(results)
    
    if args.output == "-":
        print(report)
    else:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"报告已保存至: {args.output}")


if __name__ == "__main__":
    main()
