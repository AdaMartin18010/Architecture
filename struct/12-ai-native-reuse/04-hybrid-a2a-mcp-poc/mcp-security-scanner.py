#!/usr/bin/env python3
"""
mcp-security-scanner.py
=======================

MCP 服务器安全配置扫描器（PoC）。

用法:
    python mcp-security-scanner.py --server-config server-config.json
    python mcp-security-scanner.py --stdin < server-config.json

检查项:
- 是否声明 OAuth 2.1 / 授权机制
- 是否包含工具描述中未声明的高风险操作（如邮件转发、文件删除、网络请求）
- 是否缺少审计/日志配置
- 是否使用明文传输（http 而非 https）
- 是否缺少能力范围（capabilities）声明

退出码:
    0 未发现高风险问题
    1 发现高风险问题

"""

import argparse
import json
import re
import sys
from pathlib import Path

HIGH_RISK_KEYWORDS = [
    "delete",
    "remove",
    "drop",
    "exec",
    "execute",
    "forward",
    "send_email",
    "transfer",
    "write_file",
    "modify_config",
]


def load_config(path_or_stream) -> dict:
    if path_or_stream is None:
        return json.load(sys.stdin)
    text = Path(path_or_stream).read_text(encoding="utf-8")
    return json.loads(text)


def check_transport(config: dict) -> list[dict]:
    findings = []
    transport = config.get("transport", {})
    url = transport.get("url", "")
    if url.startswith("http://"):
        findings.append({
            "severity": "high",
            "category": "transport",
            "message": f"使用明文 HTTP 传输: {url}",
            "recommendation": "强制使用 HTTPS 或 TLS 保护的 stdio/SSE 通道",
        })
    return findings


def check_authorization(config: dict) -> list[dict]:
    findings = []
    auth = config.get("authorization", {})
    if not auth.get("enabled", False):
        findings.append({
            "severity": "high",
            "category": "authorization",
            "message": "未启用授权机制",
            "recommendation": "为 MCP Server 配置 OAuth 2.1 或等价授权，并在 issuer 校验中防止 issuer 混淆",
        })
    if auth.get("enabled") and not auth.get("issuer_validation", False):
        findings.append({
            "severity": "medium",
            "category": "authorization",
            "message": "授权已启用但未校验 issuer",
            "recommendation": "启用 issuer 校验（RFC 9207）以防范 issuer 混淆攻击",
        })
    return findings


def check_capabilities(config: dict) -> list[dict]:
    findings = []
    caps = config.get("capabilities", {})
    if not caps:
        findings.append({
            "severity": "medium",
            "category": "capabilities",
            "message": "未声明 capabilities",
            "recommendation": "明确声明 tools/resources/prompts/sampling 能力范围",
        })
    return findings


def check_tool_descriptions(config: dict) -> list[dict]:
    findings = []
    tools = config.get("tools", [])
    for tool in tools:
        name = tool.get("name", "unknown")
        desc = tool.get("description", "").lower()
        for keyword in HIGH_RISK_KEYWORDS:
            if keyword in name.lower() or keyword in desc:
                if not tool.get("annotations", {}).get("destructiveHint") and not tool.get("risk_level"):
                    findings.append({
                        "severity": "high",
                        "category": "tool-description",
                        "message": f"工具 '{name}' 可能包含高风险操作 '{keyword}'，但未声明风险注解",
                        "recommendation": "在 tool.annotations 中声明 destructiveHint / openWorldHint，并在调用前强制用户授权",
                    })
    return findings


def check_audit_logging(config: dict) -> list[dict]:
    findings = []
    logging_cfg = config.get("logging", {})
    if not logging_cfg.get("audit", False):
        findings.append({
            "severity": "medium",
            "category": "audit",
            "message": "未启用审计日志",
            "recommendation": "记录 tool 调用、采样请求、能力协商与授权事件",
        })
    return findings


def generate_report(config: dict, findings: list[dict]) -> str:
    lines = [
        "# MCP 安全配置扫描报告",
        "",
        f"> 扫描目标: {config.get('server_name', 'unknown')}",
        f"> 发现问题数: {len(findings)}",
        "",
        "| 严重级别 | 类别 | 问题 | 建议 |",
        "|---------|------|------|------|",
    ]
    for f in findings:
        lines.append(f"| {f['severity']} | {f['category']} | {f['message']} | {f['recommendation']} |")
    lines.append("")
    if not findings:
        lines.append("✅ 未发现明显高风险配置。")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="MCP 安全配置扫描器")
    parser.add_argument("--server-config", type=str, help="MCP 服务器配置文件路径")
    parser.add_argument("--stdin", action="store_true", help="从标准输入读取配置")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    if not args.stdin and not args.server_config:
        parser.print_help()
        return 1

    try:
        config = load_config(None if args.stdin else args.server_config)
    except Exception as e:
        print(f"读取配置失败: {e}", file=sys.stderr)
        return 1

    findings: list[dict] = []
    findings.extend(check_transport(config))
    findings.extend(check_authorization(config))
    findings.extend(check_capabilities(config))
    findings.extend(check_tool_descriptions(config))
    findings.extend(check_audit_logging(config))

    if args.json:
        print(json.dumps({
            "server_name": config.get("server_name", "unknown"),
            "findings": findings,
            "high_risk_count": sum(1 for f in findings if f["severity"] == "high"),
        }, ensure_ascii=False, indent=2))
    else:
        print(generate_report(config, findings))

    high_risk = any(f["severity"] == "high" for f in findings)
    return 1 if high_risk else 0


if __name__ == "__main__":
    sys.exit(main())
