"""Real MCP-consumer transport (#1220, WS-8).

A thin client over the official MCP SDK's ``ClientSession`` — the REAL transport
that replaces the simulation-only ``MCPProtocolClient`` for the connector ports
(ADR-070 D5). Connector adapters (e.g. the #1317 GitHub port's ``resolve()``) use
``MCPClient`` to talk to a real MCP server; the binding (#1229) supplies the
server reference.

Design (gameplan ``dev/2026/06/27/1220-real-mcp-transport-gameplan.md``):
**Shape B** — a NEW SDK-based client, NOT a retrofit of the hand-rolled
``MCPProtocolClient``. The legacy simulation stack stays live in
``services/queries/query_router.py`` (``simulation_mode``) untouched, so query
routing carries zero regression risk; cutting that path over to the real client
is a separate follow-up, explicitly out of #1220 scope.

Two construction modes:
  * ``MCPClient(session)`` — wrap an already-initialized ``ClientSession``
    (used by tests via the SDK's in-memory transport).
  * ``MCPClient.connect_stdio(params)`` — production async-context factory that
    spawns the MCP server subprocess over stdio, initializes the session, and
    yields a connected client.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Dict, Optional, Union

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.streamable_http import streamable_http_client
from pydantic import AnyUrl


class MCPClient:
    """Thin wrapper over a live MCP SDK ``ClientSession`` (the real transport)."""

    def __init__(self, session: ClientSession) -> None:
        self._session = session

    async def list_resources(self):
        """List the resources the connected MCP server exposes (real call)."""
        return await self._session.list_resources()

    async def read_resource(self, uri: Union[str, AnyUrl]):
        """Read a resource by URI (real call). Accepts a ``str`` or ``AnyUrl``."""
        return await self._session.read_resource(_as_url(uri))

    async def list_tools(self):
        """List the tools the connected MCP server exposes (real call)."""
        return await self._session.list_tools()

    async def call_tool(
        self, name: str, arguments: Optional[Dict[str, Any]] = None
    ):
        """Invoke a tool by name with arguments (real call)."""
        return await self._session.call_tool(name, arguments or {})

    @classmethod
    @asynccontextmanager
    async def connect_stdio(
        cls, server_params: StdioServerParameters
    ) -> AsyncIterator["MCPClient"]:
        """Production transport: spawn the MCP server over stdio, then yield a client.

        Usage::

            async with MCPClient.connect_stdio(params) as client:
                await client.list_resources()
        """
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                yield cls(session)

    @classmethod
    @asynccontextmanager
    async def connect_http(cls, url: str) -> AsyncIterator["MCPClient"]:
        """Production transport for a HOSTED MCP server (streamable-HTTP).

        The companion to ``connect_stdio``: stdio spawns a local server process, HTTP
        talks to a long-lived hosted server (e.g. an OAuth-owning remote like GitHub's
        ``api.githubcopilot.com/mcp/``). Usage::

            async with MCPClient.connect_http(url) as client:
                await client.list_resources()

        Auth (OAuth 2.1 / a pre-authorized httpx client) is a follow-on for the hosted
        hookup — the SDK takes it via ``streamable_http_client(url, http_client=...)``;
        this transport-level factory proves the wire, the OAuth flow rides on it next.
        """
        async with streamable_http_client(url) as (read, write, *_):
            async with ClientSession(read, write) as session:
                await session.initialize()
                yield cls(session)


def _as_url(uri: Union[str, AnyUrl]) -> AnyUrl:
    """Coerce a string URI to ``AnyUrl`` (the SDK's ``read_resource`` arg type)."""
    return uri if isinstance(uri, AnyUrl) else AnyUrl(uri)
