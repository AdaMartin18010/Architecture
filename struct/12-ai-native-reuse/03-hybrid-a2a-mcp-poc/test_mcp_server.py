#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试用 MCP Server — 供 A2A + MCP PoC 端到端验证使用

提供工具：
- get_weather(city: str) -> 天气信息
- calculator(expression: str) -> 计算结果
- search_docs(query: str) -> 文档搜索结果

运行方式（由 hybrid_agent_server.py 通过 stdio 自动启动）：
    python test_mcp_server.py
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TestMCPServer")


@mcp.tool()
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    # 简单的模拟数据
    conditions = {
        "beijing": (28, "sunny"),
        "shanghai": (26, "cloudy"),
        "tokyo": (22, "rainy"),
        "new york": (18, "windy"),
        "london": (15, "overcast"),
    }
    temp, condition = conditions.get(city.lower(), (25, "sunny"))
    return f"Weather in {city}: {condition}, {temp}°C. (Source: TestMCP)"


@mcp.tool()
def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely."""
    try:
        # 安全求值：仅允许基本运算符和数字
        allowed = {"__builtins__": {}}
        # 替换常见符号
        expr = expression.replace("x", "*").replace("X", "*")
        result = eval(expr, allowed, {})
        return f"Result of '{expression}' = {result} (Source: TestMCP)"
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


@mcp.tool()
def search_docs(query: str) -> str:
    """Search internal documentation."""
    docs_db = [
        "Reusable Component Patterns v2.1",
        "Architecture Decision Records (ADR) Template",
        "FinOps Cost Allocation Guide",
        "Formal Verification with TLA+ and Alloy",
        "A2A Protocol Integration Best Practices",
    ]
    matches = [d for d in docs_db if query.lower() in d.lower()]
    if not matches:
        matches = docs_db[:2]
    lines = "\n".join(f"- {m}" for m in matches)
    return f"Found {len(matches)} document(s) for '{query}':\n{lines}\n(Source: TestMCP)"


if __name__ == "__main__":
    mcp.run(transport="stdio")
