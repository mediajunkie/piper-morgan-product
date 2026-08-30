"""Real MCP-consumer transport (#1220, WS-8).

A thin client over the official MCP SDK's ``ClientSession`` — the REAL transport
that replaces the simulation-only ``MCPProtocolClient`` for the connector ports
(ADR-070 D5). Connector adapters (e.g. the #1317 GitHub port's ``resolve()``) use
``MCPClient`` to talk to a real MCP server; the binding (#1229) supplies the
server reference.

Design (gameplan ``dev/2026/06/27/1220-real-mcp-transport-gameplan.md``):
**Shape B** — a NEW SDK-based client, NOT a retrofit of the hand-rolled
``MCPProtocolClient``. (Historical note, corrected 2026-08-30: this docstring
originally said the legacy simulation stack "stays live in
services/queries/query_router.py" — that file was deleted long before the
2026-08-29 census, and services/queries/ itself was disposed 2026-08-30. The
simulation stack's last live constructor — GoogleCalendarMCPAdapter's eager
``MCPConsumerCore()`` — was removed by the #1699 surgery (also 2026-08-30), so
the stack is now import-reachable only (package inits), constructed by nothing
at runtime — see the connection_pool->adapters->spatial cascade HOLD in
services/mcp/__init__.py and the 2026-08-30 disposal record in decisions.log.)

Two construction modes:
  * ``MCPClient(session)`` — wrap an already-initialized ``ClientSession``
    (used by tests via the SDK's in-memory transport).
  * ``MCPClient.connect_stdio(params)`` — production async-context factory that
    spawns the MCP server subprocess over stdio, initializes the session, and
    yields a connected client.
"""

from __future__ import annotations

from contextlib import AsyncExitStack, asynccontextmanager
from typing import Any, AsyncIterator, Dict, Optional, Union

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.streamable_http import create_mcp_http_client, streamable_http_client
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

    async def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None):
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
    async def connect_http(
        cls, url: str, headers: Optional[Dict[str, str]] = None
    ) -> AsyncIterator["MCPClient"]:
        """Production transport for a HOSTED MCP server (streamable-HTTP).

        The companion to ``connect_stdio``: stdio spawns a local server process, HTTP
        talks to a long-lived hosted server. ``headers`` carries per-request auth — e.g.
        ``{"Authorization": "Bearer <user's GitHub OAuth token>"}`` forwarded to our
        self-hosted ``github-mcp-server`` (ADR-070 option C). Usage::

            async with MCPClient.connect_http(url, headers={"Authorization": ...}) as client:
                await client.list_resources()
        """
        async with AsyncExitStack() as stack:
            http_client = None
            if headers:
                # SDK builds an httpx.AsyncClient carrying the auth header; we own its
                # lifecycle via the stack (caller-supplied → not closed by the transport).
                http_client = await stack.enter_async_context(
                    create_mcp_http_client(headers=headers)
                )
            read, write, *_ = await stack.enter_async_context(
                streamable_http_client(url, http_client=http_client)
            )
            session = await stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            yield cls(session)


def _as_url(uri: Union[str, AnyUrl]) -> AnyUrl:
    """Coerce a string URI to ``AnyUrl`` (the SDK's ``read_resource`` arg type)."""
    return uri if isinstance(uri, AnyUrl) else AnyUrl(uri)
