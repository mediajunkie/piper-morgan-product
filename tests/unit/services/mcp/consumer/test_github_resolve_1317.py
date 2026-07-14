"""#1317 GitHub port, increment 3 — resolve() over the real MCPClient, honest-degrade throughout.

The binding-aware degrade rail (folds #1231 / ADR-070 D5: never silently empty) is
server-agnostic and fully real — no binding / stale / unreachable / server-down each
yield the must-be-handled ``ResolveMiss`` with the matching reason. The bound-success
path wires the REAL ``MCPClient`` transport (#1220), proven by a round-trip against a
FastMCP fixture. The concrete github-mcp-server tool mapping (#1230) is provisioning-
gated (#1220 umbrella); a BOUND-but-unprovisioned binding therefore honestly degrades
to UNREACHABLE — which is itself asserted here.
"""

from __future__ import annotations

import contextlib
import logging

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from mcp.server.fastmcp import FastMCP  # noqa: E402
from mcp.shared.memory import create_connected_server_and_client_session  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors.binding_repository import ConnectorBindingRepository  # noqa: E402
from services.database.models import ConnectorBinding  # noqa: E402
from services.mcp.consumer import github_adapter as gh_mod  # noqa: E402
from services.mcp.consumer.connector import (  # noqa: E402
    ConnectRequired,
    DegradationReason,
    ResolveMiss,
    ResourceHandle,
    ResourceQuery,
)
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter  # noqa: E402
from services.mcp.consumer.mcp_client import MCPClient  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"


@pytest_asyncio.fixture
async def sm(monkeypatch):
    """In-memory ConnectorBinding store; the adapter's session_scope points at it."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s

    monkeypatch.setattr(gh_mod.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    yield maker
    await engine.dispose()


async def _seed(maker, status, ref="github-mcp-server"):
    async with maker() as s:
        await ConnectorBindingRepository(s).upsert(
            _ALPHA, "github", status=status, mcp_server_ref=ref
        )
        await s.commit()


def _fixture_server():
    """A real MCP server whose resolve tool mirrors the adapter's provisional contract."""
    server = FastMCP("github-resolve-fixture")

    @server.tool(name=gh_mod._RESOLVE_TOOL)
    def resolve_resource(kind: str, owner: str = "") -> str:
        # Hit for a known kind; empty (→ miss) otherwise.
        return f"gh-handle:{kind}" if kind == "default_repo" else ""

    return server


def _point_at_fixture(adapter, server):
    """Patch the adapter's MCPClient seam to yield a fixture-backed client (in-memory)."""

    @contextlib.asynccontextmanager
    async def _ctx(binding):
        async with create_connected_server_and_client_session(server) as session:
            yield MCPClient(session)

    adapter._mcp_client_ctx = _ctx


class TestResolveDegradeRail:
    """Server-agnostic honest-degrade — never silently empty (#1231)."""

    async def test_no_binding_is_connect_required_miss(self, sm):
        res = await GitHubMCPSpatialAdapter().resolve(_ALPHA, ResourceQuery(kind="default_repo"))
        assert isinstance(res, ResolveMiss)
        assert res.degradation.reason is DegradationReason.CONNECT_REQUIRED
        assert res.degradation.user_message  # honest message, never silently empty

    async def test_stale_binding_is_stale_token_miss(self, sm):
        await _seed(sm, "stale")
        res = await GitHubMCPSpatialAdapter().resolve(_ALPHA, ResourceQuery(kind="default_repo"))
        assert isinstance(res, ResolveMiss)
        assert res.degradation.reason is DegradationReason.STALE_TOKEN

    async def test_unbound_status_binding_is_connect_required_miss(self, sm):
        await _seed(sm, "unbound")
        res = await GitHubMCPSpatialAdapter().resolve(_ALPHA, ResourceQuery(kind="default_repo"))
        assert isinstance(res, ResolveMiss)
        assert res.degradation.reason is DegradationReason.CONNECT_REQUIRED

    async def test_unreachable_status_binding_is_unreachable_miss(self, sm):
        await _seed(sm, "unreachable")
        res = await GitHubMCPSpatialAdapter().resolve(_ALPHA, ResourceQuery(kind="default_repo"))
        assert isinstance(res, ResolveMiss)
        assert res.degradation.reason is DegradationReason.UNREACHABLE

    async def test_bound_but_unprovisioned_server_is_unreachable_miss(self, sm):
        """BOUND binding + no github-mcp-server provisioned (#1220) → honest UNREACHABLE,
        never a fake success. This is the real current production behavior."""
        await _seed(sm, "bound")
        res = await GitHubMCPSpatialAdapter().resolve(_ALPHA, ResourceQuery(kind="default_repo"))
        assert isinstance(res, ResolveMiss)
        assert res.degradation.reason is DegradationReason.UNREACHABLE


class TestResolveOverRealTransport:
    """Bound + a reachable MCP server: real round-trip via MCPClient (#1220)."""

    async def test_bound_hit_returns_resource_handle(self, sm):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter, _fixture_server())
        res = await adapter.resolve(
            _ALPHA, ResourceQuery(kind="default_repo", params={"owner": "acme"})
        )
        assert isinstance(res, ResourceHandle)
        assert res.handle == "gh-handle:default_repo"
        assert res.kind == "default_repo"

    async def test_bound_miss_returns_resource_not_found(self, sm):
        await _seed(sm, "bound")
        adapter = GitHubMCPSpatialAdapter()
        _point_at_fixture(adapter, _fixture_server())
        res = await adapter.resolve(_ALPHA, ResourceQuery(kind="nonexistent_kind"))
        assert isinstance(res, ResolveMiss)
        assert res.degradation.reason is DegradationReason.RESOURCE_NOT_FOUND


class TestConnectActionHint:
    """inc.2 slice E1 — an unbound connect() offers the connect URL (action_hint)."""

    async def test_unbound_connect_offers_connect_url(self, sm):
        from services.mcp.consumer.github_adapter import _CONNECT_URL

        res = await GitHubMCPSpatialAdapter().connect(_ALPHA)
        assert isinstance(res, ConnectRequired)
        assert res.degradation.action_hint == _CONNECT_URL


class TestResolveHttpSeam:
    """inc.2 slice E2 — the real _mcp_client_ctx connects over HTTP to the binding's
    server, forwarding the user's stored OAuth grant as the Authorization header."""

    async def test_mcp_client_ctx_connects_http_with_grant_header(self, sm, monkeypatch):
        # ADR-070-A (A1): the binding stores the LOGICAL key 'github'; the URL
        # resolves from deployment config at connect-time. (Pre-A this test seeded a
        # literal 'github-mcp-server' ref — stale once the resolver landed.)
        monkeypatch.setenv("GITHUB_MCP_SERVER_URL", "http://gh-mcp.internal:8082/mcp")
        await _seed(sm, "bound", ref="github")
        import services.mcp.consumer.github_adapter as gh

        class _GS:  # grant store → returns a token, ignores the session
            def __init__(self, *a, **k):
                pass

            async def get(self, *a, **k):
                return "gho_tok"

        monkeypatch.setattr(gh, "ConnectorGrantStore", _GS)

        captured = {}

        @contextlib.asynccontextmanager
        async def _fake_http(url, headers=None):
            captured["url"] = url
            captured["headers"] = headers
            yield object()  # dummy client; we only assert the connect args

        monkeypatch.setattr(gh.MCPClient, "connect_http", staticmethod(_fake_http))

        async with sm() as s:
            binding = await ConnectorBindingRepository(s).get(_ALPHA, "github")

        async with gh.GitHubMCPSpatialAdapter()._mcp_client_ctx(binding):
            pass

        assert captured["url"] == "http://gh-mcp.internal:8082/mcp"
        assert captured["headers"] == {"Authorization": "Bearer gho_tok"}


class TestMisconfiguredDegrade:
    """#1398 / ADR-070-A A4 — a server-ref RESOLUTION failure (unset env / unknown key)
    is a deployment CONFIG problem: it must degrade as MISCONFIGURED and log the missing
    config at ERROR, never masquerade as UNREACHABLE (the 2026-07-12 Fly phantom-outage).
    Arch 2026-07-12: the resolver named the config, but the adapter flattened it back to
    UNREACHABLE — this covers the integration point the 7 resolver tests didn't."""

    async def test_unset_env_degrades_misconfigured_and_logs_config(self, sm, monkeypatch, caplog):
        import services.mcp.consumer.github_adapter as gh

        # A bound binding storing the logical key 'github', but the deployment's
        # GITHUB_MCP_SERVER_URL is unset → resolve_server_ref raises (the A4 case).
        monkeypatch.delenv("GITHUB_MCP_SERVER_URL", raising=False)
        await _seed(sm, "bound", ref="github")

        class _GS:  # grant present, so resolution (not the grant fetch) is what fails
            def __init__(self, *a, **k):
                pass

            async def get(self, *a, **k):
                return "gho_tok"

        monkeypatch.setattr(gh, "ConnectorGrantStore", _GS)

        with caplog.at_level(logging.ERROR):
            res = await GitHubMCPSpatialAdapter().resolve(
                _ALPHA, ResourceQuery(kind="default_repo")
            )

        assert isinstance(res, ResolveMiss)
        # config-distinct, NOT UNREACHABLE
        assert res.degradation.reason is DegradationReason.MISCONFIGURED
        # generic-honest user message — never leaks the env-var name to testers
        assert "GITHUB_MCP_SERVER_URL" not in res.degradation.user_message
        # operator ERROR log names the missing config and calls it misconfigured
        assert any(
            r.levelno == logging.ERROR
            and "misconfigured" in r.getMessage().lower()
            and "GITHUB_MCP_SERVER_URL" in r.getMessage()
            for r in caplog.records
        )

    async def test_non_config_failure_still_unreachable(self, sm):
        """A genuine transport failure (not a config-resolution error) stays UNREACHABLE —
        MISCONFIGURED must not swallow real outages."""
        await _seed(sm, "bound", ref="github")
        adapter = GitHubMCPSpatialAdapter()

        @contextlib.asynccontextmanager
        async def _raise_generic(binding):
            raise RuntimeError("connection reset by peer")
            yield  # unreachable — present only to make this an async generator

        adapter._mcp_client_ctx = _raise_generic
        res = await adapter.resolve(_ALPHA, ResourceQuery(kind="default_repo"))
        assert isinstance(res, ResolveMiss)
        assert res.degradation.reason is DegradationReason.UNREACHABLE
