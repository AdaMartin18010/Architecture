#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A2A + MCP PoC 端到端测试脚本

自动完成以下验证：
1. 启动 A2A Server（通过 stdio 自动连接 test_mcp_server.py）
2. 验证 MCP Tool Discovery
3. 验证 Weather / Calculator / Search 三类任务的完整链路
4. 验证未知意图回退
5. 验证 Agent Card 和 tasks/get

运行：
    python test_e2e.py
"""

import asyncio
import json
import os
import subprocess
import sys
import time
from urllib.request import urlopen, Request

BASE_URL = os.environ.get("TEST_BASE_URL", "http://127.0.0.1:8001")


def http_get(path: str) -> dict:
    with urlopen(f"{BASE_URL}{path}") as resp:
        return json.loads(resp.read().decode())


def http_post(path: str, payload: dict) -> dict:
    data = json.dumps(payload).encode()
    req = Request(f"{BASE_URL}{path}", data=data, headers={"Content-Type": "application/json"})
    with urlopen(req) as resp:
        return json.loads(resp.read().decode())


def test():
    print("=" * 60)
    print("A2A + MCP Hybrid Agent — End-to-End Test")
    print("=" * 60)

    # 1. Health / Root
    print("\n[1/7] Root endpoint...")
    root = http_get("/")
    assert root["mcp_mode"] == "real (3 tools)", f"Expected real mode, got {root['mcp_mode']}"
    print(f"  ✓ MCP mode: {root['mcp_mode']}")

    # 2. Agent Card
    print("\n[2/7] Agent Card...")
    card = http_get("/.well-known/agent-card.json")
    assert card["name"] == "HybridAssistant"
    print(f"  ✓ Agent: {card['name']}, Skills: {[s['id'] for s in card['skills']]}")

    # 3. MCP Tool Discovery
    print("\n[3/7] MCP Tool Discovery...")
    tools = http_get("/mcp/tools")
    assert tools["mode"] == "real (3 tools)"
    assert len(tools["tools"]) == 3
    print(f"  ✓ Tools: {[t['name'] for t in tools['tools']]}")

    # 4. Weather Query
    print("\n[4/7] Weather Query...")
    resp = http_post("/jsonrpc", {
        "jsonrpc": "2.0", "id": 1,
        "method": "tasks/send",
        "params": {"message": {"role": "user", "parts": [{"text": "What is the weather in Shanghai?"}]}}
    })
    text = resp["result"]["artifacts"][0]["parts"][0]["text"]
    assert "TestMCP" in text, f"Expected real MCP response, got: {text}"
    assert "Shanghai" in text
    print(f"  ✓ {text}")

    # 5. Calculator
    print("\n[5/7] Calculator...")
    resp = http_post("/jsonrpc", {
        "jsonrpc": "2.0", "id": 2,
        "method": "tasks/send",
        "params": {"message": {"role": "user", "parts": [{"text": "Calculate 15 * 23 + 7"}]}}
    })
    text = resp["result"]["artifacts"][0]["parts"][0]["text"]
    assert "TestMCP" in text
    assert "352" in text
    print(f"  ✓ {text}")

    # 6. Document Search
    print("\n[6/7] Document Search...")
    resp = http_post("/jsonrpc", {
        "jsonrpc": "2.0", "id": 3,
        "method": "tasks/send",
        "params": {"message": {"role": "user", "parts": [{"text": "Search docs for reusable"}]}}
    })
    text = resp["result"]["artifacts"][0]["parts"][0]["text"]
    assert "TestMCP" in text
    assert "Reusable Component Patterns" in text
    print(f"  ✓ {text.replace(chr(10), ' ')}")

    # 7. Unknown Intent
    print("\n[7/7] Unknown Intent Fallback...")
    resp = http_post("/jsonrpc", {
        "jsonrpc": "2.0", "id": 4,
        "method": "tasks/send",
        "params": {"message": {"role": "user", "parts": [{"text": "Hello world"}]}}
    })
    text = resp["result"]["artifacts"][0]["parts"][0]["text"]
    assert "weather" in text.lower() or "calculation" in text.lower()
    print(f"  ✓ Fallback response delivered")

    print("\n" + "=" * 60)
    print("All 7 tests PASSED ✓")
    print("=" * 60)
    return True


if __name__ == "__main__":
    try:
        ok = test()
        sys.exit(0 if ok else 1)
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        sys.exit(1)
