"""#1220 (WS-8) — the real MCP-consumer transport via the official MCP SDK.

These tests prove `MCPClient` performs a REAL MCP protocol round-trip (not the
legacy simulation) against a `FastMCP` fixture server over the SDK's in-memory
transport: list + read a resource, list + call a tool. No subprocess is spawned
here (deterministic, fast) — the real stdio subprocess path is covered by the
inc.2 integration test.

Design: gameplan `dev/2026/06/27/1220-real-mcp-transport-gameplan.md` (Shape B —
a NEW SDK-based client; the legacy sim stack in query_router stays untouched).
"""
import pytest
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP
from mcp.shared.memory import create_connected_server_and_client_session

from services.mcp.consumer.mcp_client import MCPClient


@pytest.fixture
def fixture_server():
    """A real MCP server (FastMCP) exposing one known resource + one known tool."""
    server = FastMCP("piper-test-fixture")

    @server.resource("file:///greeting.txt")
    def greeting() -> str:
        return "hello from a real mcp server"

    @server.tool()
    def echo(text: str) -> str:
        return f"echo: {text}"

    return server


def _texts(items):
    """Pull .text off SDK content items (TextContent / TextResourceContents)."""
    return [getattr(c, "text", "") for c in items if hasattr(c, "text")]


class TestMCPClientRealRoundTrip:
    async def test_list_resources_returns_the_real_resource(self, fixture_server):
        async with create_connected_server_and_client_session(fixture_server) as session:
            client = MCPClient(session)
            result = await client.list_resources()
            uris = [str(r.uri) for r in result.resources]
            assert "file:///greeting.txt" in uris

    async def test_read_resource_returns_real_content(self, fixture_server):
        async with create_connected_server_and_client_session(fixture_server) as session:
            client = MCPClient(session)
            result = await client.read_resource("file:///greeting.txt")
            assert any("hello from a real mcp server" in t for t in _texts(result.contents))

    async def test_list_tools_returns_the_real_tool(self, fixture_server):
        async with create_connected_server_and_client_session(fixture_server) as session:
            client = MCPClient(session)
            result = await client.list_tools()
            assert "echo" in [t.name for t in result.tools]

    async def test_call_tool_executes_the_real_tool(self, fixture_server):
        async with create_connected_server_and_client_session(fixture_server) as session:
            client = MCPClient(session)
            result = await client.call_tool("echo", {"text": "ping"})
            assert any("echo: ping" in t for t in _texts(result.content))


class TestMCPClientProductionEntryPoint:
    def test_connect_stdio_is_an_async_context_manager_factory(self):
        """The production transport entry-point exists (subprocess round-trip = inc.2)."""
        from mcp.client.stdio import StdioServerParameters

        cm = MCPClient.connect_stdio(StdioServerParameters(command="true", args=[]))
        # asynccontextmanager-wrapped → supports the async-with protocol.
        assert hasattr(cm, "__aenter__") and hasattr(cm, "__aexit__")
