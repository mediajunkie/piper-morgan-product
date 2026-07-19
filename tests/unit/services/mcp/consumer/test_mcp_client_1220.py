"""#1220 (WS-8) — the real MCP-consumer transport via the official MCP SDK.

These tests prove `MCPClient` performs a REAL MCP protocol round-trip (not the
legacy simulation) against a `FastMCP` fixture server over the SDK's in-memory
transport: list + read a resource, list + call a tool. No subprocess is spawned
here (deterministic, fast) — the real stdio subprocess path is covered by the
inc.2 integration test.

Design: gameplan `dev/2026/06/27/1220-real-mcp-transport-gameplan.md` (Shape B —
a NEW SDK-based client, built alongside the then-extant legacy sim query_router
stack; that stack was deleted 2026-07-19, #1436 Family-3).
"""

import sys
from pathlib import Path

import pytest

from mcp.client.stdio import StdioServerParameters
from mcp.server.fastmcp import FastMCP
from mcp.shared.memory import create_connected_server_and_client_session

from services.mcp.consumer.mcp_client import MCPClient

# The real stdio MCP server fixture (spawned as a subprocess by inc.2).
# This file lives at tests/unit/services/mcp/consumer/ → parents[4] is tests/.
_STDIO_FIXTURE = str(
    Path(__file__).resolve().parents[4] / "fixtures" / "mcp" / "stdio_fixture_server.py"
)


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
        cm = MCPClient.connect_stdio(StdioServerParameters(command="true", args=[]))
        # asynccontextmanager-wrapped → supports the async-with protocol.
        assert hasattr(cm, "__aenter__") and hasattr(cm, "__aexit__")


@pytest.mark.integration
class TestMCPClientStdioSubprocess:
    """inc.2 — prove connect_stdio against a REAL MCP server subprocess over OS stdio.

    Spawns the FastMCP fixture server (tests/fixtures/mcp/stdio_fixture_server.py)
    via StdioServerParameters and round-trips the full production transport path:
    spawn → initialize → list/read resource + list/call tool. No github-mcp-server
    needed — the fixture server proves the transport itself.
    """

    async def test_real_stdio_round_trip(self):
        params = StdioServerParameters(command=sys.executable, args=[_STDIO_FIXTURE])
        async with MCPClient.connect_stdio(params) as client:
            resources = await client.list_resources()
            assert "file:///greeting.txt" in [str(r.uri) for r in resources.resources]

            read = await client.read_resource("file:///greeting.txt")
            assert any("hello from a real stdio mcp server" in t for t in _texts(read.contents))

            tools = await client.list_tools()
            assert "echo" in [t.name for t in tools.tools]

            called = await client.call_tool("echo", {"text": "pong"})
            assert any("echo: pong" in t for t in _texts(called.content))


@pytest.mark.integration
class TestMCPClientStreamableHttp:
    """inc.4 — prove connect_http against a REAL MCP server over streamable-HTTP.

    Serves the same FastMCP fixture in --http mode as a subprocess and round-trips via
    MCPClient.connect_http — the hosted-server transport (the companion to connect_stdio,
    and the one the recommended github-mcp-server provisioning option needs).
    """

    @pytest.fixture
    def http_server_url(self):
        import contextlib as _ctx
        import socket
        import subprocess
        import time

        import httpx

        sock = socket.socket()
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        sock.close()

        proc = subprocess.Popen([sys.executable, _STDIO_FIXTURE, "--http", "--port", str(port)])
        url = f"http://127.0.0.1:{port}/mcp"
        deadline = time.time() + 15
        ready = False
        while time.time() < deadline:
            if proc.poll() is not None:
                break  # server process died
            with _ctx.suppress(Exception):
                httpx.get(url, timeout=0.3)  # any HTTP response (even 4xx) = server is up
                ready = True
                break
            time.sleep(0.1)
        if not ready:
            proc.terminate()
            pytest.fail("HTTP fixture server did not become ready")
        try:
            yield url
        finally:
            proc.terminate()
            with _ctx.suppress(Exception):
                proc.wait(timeout=5)

    async def test_real_http_round_trip(self, http_server_url):
        async with MCPClient.connect_http(http_server_url) as client:
            tools = await client.list_tools()
            assert "echo" in [t.name for t in tools.tools]

            called = await client.call_tool("echo", {"text": "via-http"})
            assert any("echo: via-http" in t for t in _texts(called.content))


class TestMCPClientHttpAuthHeader:
    """inc.2 slice C — connect_http forwards an auth header (the user's GitHub OAuth token)
    to the self-hosted server (ADR-070 C). Network-free: asserts the header is wired into
    the SDK's http-client factory (security-critical — the token must reach the server)."""

    async def test_auth_header_passed_to_http_client_factory(self, monkeypatch):
        import services.mcp.consumer.mcp_client as mc

        captured = {}

        def _spy(headers=None, **kw):
            captured["headers"] = headers
            raise RuntimeError("stop-before-network")  # short-circuit; only assert wiring

        monkeypatch.setattr(mc, "create_mcp_http_client", _spy)
        with pytest.raises(RuntimeError):
            async with MCPClient.connect_http(
                "http://127.0.0.1:9/mcp", headers={"Authorization": "Bearer user-tok"}
            ):
                pass
        assert captured["headers"] == {"Authorization": "Bearer user-tok"}
