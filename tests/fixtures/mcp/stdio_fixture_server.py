#!/usr/bin/env python3
"""Real MCP server fixture (stdio) for the #1220 inc.2 integration test.

A minimal FastMCP server exposing one known resource + one known tool, served
over stdio (FastMCP's default transport). It is spawned as a subprocess by
``tests/unit/services/mcp/consumer/test_mcp_client_1220.py`` to prove
``MCPClient.connect_stdio`` does a real round-trip over OS-level stdio — i.e. the
production transport path, not the in-memory transport used by the inc.1 tests.

This is a genuine MCP server (unlike ``scripts/mcp_file_server.py``, which is a
POC simulation). Run directly it speaks the MCP protocol on stdin/stdout.
"""
from mcp.server.fastmcp import FastMCP

server = FastMCP("piper-stdio-fixture")


@server.resource("file:///greeting.txt")
def greeting() -> str:
    return "hello from a real stdio mcp server"


@server.tool()
def echo(text: str) -> str:
    return f"echo: {text}"


if __name__ == "__main__":
    import sys

    # `--http --port N` serves the same server over streamable-HTTP (for the
    # connect_http integration test); otherwise FastMCP's default stdio transport.
    if "--http" in sys.argv:
        port = int(sys.argv[sys.argv.index("--port") + 1])
        server.settings.host = "127.0.0.1"
        server.settings.port = port
        server.run(transport="streamable-http")
    else:
        server.run()
