#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A2A + MCP 混合 Agent 服务示例（真实 MCP SDK 集成版）

架构原则：
- 对外暴露 A2A 协议（Agent Card + Task Lifecycle）
- 内部使用 MCP 工具完成具体任务
- 演示 "A2A 用于 Agent 协作，MCP 用于工具调用" 的最佳实践
- 支持连接真实 MCP Server（stdio transport）+ 本地 Mock 工具 fallback

运行：
    # 仅启动 A2A + Mock MCP
    uvicorn hybrid_agent_server:app --reload --port 8000

    # 连接真实 MCP Server（示例：filesystem）
    MCP_SERVER_COMMAND="npx -y @modelcontextprotocol/server-filesystem e:\\_src\\Architecture" \
      uvicorn hybrid_agent_server:app --reload --port 8000

测试：
    curl http://localhost:8000/.well-known/agent-card.json
    curl -X POST http://localhost:8000/jsonrpc \
      -H "Content-Type: application/json" \
      -d '{"jsonrpc":"2.0","id":1,"method":"tasks/send","params":{"message":{"role":"user","parts":[{"text":"天气怎么样"}]}}}'
    curl http://localhost:8000/mcp/tools
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import uuid
from contextlib import AsyncExitStack
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Dict, List, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse

# ---------------------------------------------------------------------------
# MCP SDK 导入
# ---------------------------------------------------------------------------

try:
    from mcp import ClientSession
    from mcp.client.stdio import stdio_client, StdioServerParameters
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False

# ---------------------------------------------------------------------------
# MCP 工具层：真实 Client + Mock fallback
# ---------------------------------------------------------------------------

class MockMCPTools:
    """模拟 MCP 工具集合。当未配置真实 MCP Server 时自动降级使用。"""

    async def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {"name": "get_weather", "description": "Get current weather for a city", "inputSchema": {"type": "object", "properties": {"city": {"type": "string"}}}},
            {"name": "calculator", "description": "Evaluate mathematical expressions", "inputSchema": {"type": "object", "properties": {"expression": {"type": "string"}}}},
            {"name": "search_docs", "description": "Search internal documentation", "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}}},
        ]

    async def call(self, tool_name: str, arguments: dict) -> str:
        await asyncio.sleep(0.1)
        if tool_name == "get_weather":
            city = arguments.get("city", "Beijing")
            return json.dumps({"city": city, "temperature": 26, "condition": "sunny"})
        elif tool_name == "calculator":
            expr = arguments.get("expression", "0")
            try:
                result = eval(expr, {"__builtins__": {}}, {})
                return json.dumps({"result": result})
            except Exception as e:
                return json.dumps({"error": str(e)})
        elif tool_name == "search_docs":
            query = arguments.get("query", "")
            return json.dumps({"query": query, "results": [f"Doc A about {query}", f"Doc B about {query}"]})
        return json.dumps({"error": f"Unknown tool: {tool_name}"})


class RealMCPClient:
    """基于 mcp.ClientSession 的真实 MCP Client（stdio transport）。"""

    def __init__(self):
        self._session: Optional[ClientSession] = None
        self._exit_stack = AsyncExitStack()
        self._tools: List[Dict[str, Any]] = []

    async def connect(self, command: str, args: List[str]) -> None:
        """通过 stdio 连接外部 MCP Server。"""
        if not MCP_AVAILABLE:
            raise RuntimeError("mcp SDK not installed. Run: pip install mcp")

        server_params = StdioServerParameters(command=command, args=args)
        stdio_transport = await self._exit_stack.enter_async_context(stdio_client(server_params))
        self._session = await self._exit_stack.enter_async_context(ClientSession(*stdio_transport))
        await self._session.initialize()
        # 缓存工具列表
        tools_result = await self._session.list_tools()
        self._tools = [
            {"name": t.name, "description": t.description, "inputSchema": t.inputSchema}
            for t in tools_result.tools
        ]

    async def disconnect(self) -> None:
        await self._exit_stack.aclose()
        self._session = None
        self._tools = []

    async def list_tools(self) -> List[Dict[str, Any]]:
        return self._tools

    async def call(self, tool_name: str, arguments: dict) -> str:
        if self._session is None:
            raise RuntimeError("MCP session not connected")
        result = await self._session.call_tool(tool_name, arguments)
        # MCP CallToolResult 的 content 是 TextContent 列表
        texts = []
        for item in result.content:
            if hasattr(item, "text"):
                texts.append(item.text)
            else:
                texts.append(str(item))
        return "\n".join(texts) if texts else json.dumps({"result": "ok"})

    @property
    def connected(self) -> bool:
        return self._session is not None


# 全局工具管理器：优先使用真实 MCP，降级到 Mock
class MCPToolManager:
    """统一 MCP 工具管理器，自动选择真实 Client 或 Mock fallback。"""

    def __init__(self):
        self._mock = MockMCPTools()
        self._real: Optional[RealMCPClient] = None

    async def init_real(self, command: str, args: List[str]) -> bool:
        """尝试初始化真实 MCP 连接。返回是否成功。"""
        if not MCP_AVAILABLE:
            return False
        client = RealMCPClient()
        try:
            await asyncio.wait_for(client.connect(command, args), timeout=15.0)
            self._real = client
            return True
        except Exception as e:
            print(f"[MCP] 连接真实 MCP Server 失败: {e}，降级到 Mock")
            await client.disconnect()
            return False

    async def list_tools(self) -> List[Dict[str, Any]]:
        if self._real and self._real.connected:
            return await self._real.list_tools()
        return await self._mock.list_tools()

    async def call(self, tool_name: str, arguments: dict) -> str:
        if self._real and self._real.connected:
            return await self._real.call(tool_name, arguments)
        return await self._mock.call(tool_name, arguments)

    @property
    def mode(self) -> str:
        if self._real and self._real.connected:
            return f"real ({len(self._real._tools)} tools)"
        return "mock"


mcp_manager = MCPToolManager()

# ---------------------------------------------------------------------------
# A2A 数据模型
# ---------------------------------------------------------------------------

AGENT_CARD = {
    "name": "HybridAssistant",
    "description": "An A2A agent that internally uses MCP tools for weather, calculation, and document search.",
    "url": "http://localhost:8000",
    "version": "1.0.0",
    "capabilities": {
        "streaming": True,
        "pushNotifications": False
    },
    "defaultInputModes": ["text"],
    "defaultOutputModes": ["text"],
    "skills": [
        {
            "id": "weather_query",
            "name": "Weather Query",
            "description": "Get current weather for a city",
            "tags": ["weather", "utility"],
            "examples": ["What's the weather in Shanghai?"]
        },
        {
            "id": "calculator",
            "name": "Calculator",
            "description": "Evaluate mathematical expressions",
            "tags": ["math", "utility"],
            "examples": ["Calculate 15 * 23 + 7"]
        },
        {
            "id": "doc_search",
            "name": "Document Search",
            "description": "Search internal documentation",
            "tags": ["search", "docs"],
            "examples": ["Search docs for 'reusable component patterns'"]
        }
    ],
    "authentication": {
        "schemes": ["none"]
    }
}

# 内存中的任务存储（生产环境应使用 Redis/DB）
tasks_db: Dict[str, dict] = {}

# ---------------------------------------------------------------------------
# FastAPI 应用
# ---------------------------------------------------------------------------

app = FastAPI(title="A2A + MCP Hybrid Agent")


@app.on_event("startup")
async def startup_event():
    """启动时尝试连接真实 MCP Server（通过环境变量配置）。"""
    mcp_cmd = os.environ.get("MCP_SERVER_COMMAND")
    if mcp_cmd:
        parts = mcp_cmd.split()
        ok = await mcp_manager.init_real(parts[0], parts[1:])
        print(f"[startup] MCP mode: {mcp_manager.mode} (command: {mcp_cmd})" if ok else f"[startup] MCP mode: {mcp_manager.mode}")
    else:
        print("[startup] MCP mode: mock (set MCP_SERVER_COMMAND env to enable real MCP)")


@app.get("/.well-known/agent-card.json")
async def agent_card() -> dict:
    """A2A Agent Card 发现端点。"""
    return AGENT_CARD


@app.get("/mcp/tools")
async def list_mcp_tools() -> dict:
    """列出当前可用的 MCP 工具（真实或 Mock）。"""
    tools = await mcp_manager.list_tools()
    return {
        "mode": mcp_manager.mode,
        "tools": tools
    }


# ---------------------------------------------------------------------------
# 任务处理逻辑
# ---------------------------------------------------------------------------

async def process_task(task_id: str, user_text: str) -> AsyncGenerator[dict, None]:
    """处理 A2A 任务，内部调用 MCP 工具。"""

    # 更新状态: working
    tasks_db[task_id]["status"]["state"] = "working"
    yield {"jsonrpc": "2.0", "id": task_id, "result": {"id": task_id, "status": tasks_db[task_id]["status"]}}

    # 简单的意图识别 -> MCP 工具路由
    tool_name: Optional[str] = None
    tool_args: dict = {}

    text_lower = user_text.lower()
    if any(k in text_lower for k in ["weather", "天气", "temperature"]):
        tool_name = "get_weather"
        city = "Beijing"
        for c in ["Shanghai", "Beijing", "Tokyo", "New York", "London"]:
            if c.lower() in text_lower:
                city = c
                break
        tool_args = {"city": city}
    elif any(k in text_lower for k in ["calculate", "calculator", "计算", "*", "+", "-", "/"]):
        tool_name = "calculator"
        expr = user_text
        for prefix in ["calculate ", "计算 ", "Compute ", "Calculate "]:
            if prefix in user_text:
                expr = user_text.split(prefix, 1)[1]
        expr = expr.strip().rstrip("?").rstrip("！").rstrip("!")
        tool_args = {"expression": expr}
    elif any(k in text_lower for k in ["search", "doc", "文档", "查找"]):
        tool_name = "search_docs"
        query = user_text
        for prefix in ["search docs for ", "search ", "查找 "]:
            pl = prefix.lower()
            if pl in text_lower:
                # 找到前缀在原始文本中的位置，然后切片
                idx = text_lower.find(pl)
                query = user_text[idx + len(prefix):].strip().strip('"').strip("'")
                break
        tool_args = {"query": query}
    elif mcp_manager.mode.startswith("real"):
        # 当连接真实 MCP Server 时，尝试模糊匹配所有可用工具
        available_tools = await mcp_manager.list_tools()
        for t in available_tools:
            name = t.get("name", "").lower()
            desc = t.get("description", "").lower()
            # 简单关键词匹配
            keywords = re.findall(r'\b\w+\b', user_text.lower())
            score = sum(1 for kw in keywords if kw in name or kw in desc)
            if score > 0 and (tool_name is None or score > 0):
                tool_name = t["name"]
                # 从 inputSchema 推断参数
                schema = t.get("inputSchema", {})
                props = schema.get("properties", {})
                for prop_name in props:
                    # 简单启发：如果参数名出现在用户输入中则提取
                    if prop_name.lower() in text_lower:
                        # 提取后面跟着的词作为值（极度简化）
                        match = re.search(rf'{prop_name}\s*[:=]?\s*([^,;\n]+)', user_text, re.I)
                        if match:
                            tool_args[prop_name] = match.group(1).strip().strip('"')
                break

    if tool_name:
        mcp_result_raw = await mcp_manager.call(tool_name, tool_args)
        is_real = mcp_manager.mode.startswith("real")
        try:
            mcp_result = json.loads(mcp_result_raw)
            is_json = True
        except json.JSONDecodeError:
            mcp_result = {"text": mcp_result_raw}
            is_json = False

        if tool_name == "get_weather":
            if is_real and not is_json:
                response_text = mcp_result_raw
            else:
                response_text = f"The weather in {mcp_result.get('city', 'unknown')} is {mcp_result.get('condition', 'unknown')} with a temperature of {mcp_result.get('temperature', '?')}°C."
        elif tool_name == "calculator":
            if is_real and not is_json:
                response_text = mcp_result_raw
            elif "error" in mcp_result:
                response_text = f"Calculation error: {mcp_result['error']}"
            else:
                response_text = f"The result is {mcp_result.get('result', mcp_result_raw)}."
        elif tool_name == "search_docs":
            if is_real and not is_json:
                response_text = mcp_result_raw
            else:
                results = mcp_result.get("results", [])
                response_text = f"Found {len(results)} documents for '{mcp_result.get('query', '')}':\n" + "\n".join(f"- {r}" for r in results)
        else:
            # 真实 MCP Server 返回的通用格式化
            if isinstance(mcp_result, dict) and "text" in mcp_result:
                response_text = mcp_result["text"]
            else:
                response_text = str(mcp_result_raw)
    else:
        response_text = (
            "I can help with weather queries, calculations, or document searches.\n"
            "Try: 'What's the weather in Shanghai?' or 'Calculate 15 * 23' or 'Search docs for reuse patterns'\n"
            f"(Current MCP mode: {mcp_manager.mode})"
        )

    # 更新任务状态: completed
    tasks_db[task_id]["status"]["state"] = "completed"
    tasks_db[task_id]["artifacts"] = [
        {
            "parts": [{"text": response_text}]
        }
    ]
    tasks_db[task_id]["messages"].append(
        {"role": "agent", "parts": [{"text": response_text}]}
    )

    yield {
        "jsonrpc": "2.0",
        "id": task_id,
        "result": {
            "id": task_id,
            "status": tasks_db[task_id]["status"],
            "artifacts": tasks_db[task_id]["artifacts"],
            "messages": tasks_db[task_id]["messages"]
        }
    }


# ---------------------------------------------------------------------------
# JSON-RPC 端点
# ---------------------------------------------------------------------------

@app.post("/jsonrpc")
async def jsonrpc(request: Request):
    """A2A JSON-RPC 端点。支持 tasks/send 和 tasks/get。"""
    body = await request.json()
    method = body.get("method")
    params = body.get("params", {})
    req_id = body.get("id", str(uuid.uuid4()))

    if method == "tasks/send":
        task_id = str(uuid.uuid4())
        message = params.get("message", {})
        user_text = ""
        for part in message.get("parts", []):
            user_text += part.get("text", "")

        tasks_db[task_id] = {
            "id": task_id,
            "status": {"state": "submitted", "timestamp": datetime.now(timezone.utc).isoformat()},
            "messages": [message],
            "artifacts": []
        }

        async def collect():
            final = None
            async for event in process_task(task_id, user_text):
                final = event
            return final

        return await collect()

    elif method == "tasks/get":
        task_id = params.get("id")
        task = tasks_db.get(task_id)
        if not task:
            return JSONResponse(
                status_code=404,
                content={"jsonrpc": "2.0", "id": req_id, "error": {"code": -32000, "message": "Task not found"}}
            )
        return {"jsonrpc": "2.0", "id": req_id, "result": task}

    elif method == "tasks/sendSubscribe":
        # SSE 流式响应
        task_id = str(uuid.uuid4())
        message = params.get("message", {})
        user_text = ""
        for part in message.get("parts", []):
            user_text += part.get("text", "")

        tasks_db[task_id] = {
            "id": task_id,
            "status": {"state": "submitted", "timestamp": datetime.now(timezone.utc).isoformat()},
            "messages": [message],
            "artifacts": []
        }

        async def event_stream():
            async for event in process_task(task_id, user_text):
                yield f"data: {json.dumps(event)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    return JSONResponse(
        status_code=400,
        content={"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}
    )


@app.get("/")
async def root():
    return {
        "service": "A2A + MCP Hybrid Agent",
        "a2a_version": "v1.2",
        "mcp_version": "2025-11-25",
        "mcp_mode": mcp_manager.mode,
        "mcp_sdk_available": MCP_AVAILABLE,
        "agent_card": "http://localhost:8000/.well-known/agent-card.json",
        "endpoints": {
            "agent_card": "GET /.well-known/agent-card.json",
            "tasks_send": "POST /jsonrpc (method=tasks/send)",
            "tasks_get": "POST /jsonrpc (method=tasks/get)",
            "tasks_subscribe": "POST /jsonrpc (method=tasks/sendSubscribe) -> SSE",
            "mcp_tools": "GET /mcp/tools"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
