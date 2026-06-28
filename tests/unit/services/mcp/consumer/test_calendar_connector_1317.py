"""#1317 Calendar port — the binding-aware Connector-protocol rail (mirrors the github port).

Calendar's connect/status/resolve are now binding-aware with the honest-degrade rail
(#1231 / ADR-070 D5: never silently empty), reading the per-user ConnectorBinding store
(#1229 / D3 — bindings, never raw tokens). The live MCP resolution is provisioning-gated
(#1220), so a BOUND-but-unprovisioned binding honest-degrades to UNREACHABLE. The shared
logic is exercised in depth by the github tests; these assert calendar is wired with the
right connector-name ("calendar") + the degrade rail + a real-transport round-trip.
"""

from __future__ import annotations

import contextlib

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
from services.mcp.consumer import google_calendar_adapter as cal_mod  # noqa: E402
from services.mcp.consumer.connector import (  # noqa: E402
    Binding,
    ConnectRequired,
    ConnectorStatusState,
    DegradationReason,
    ResolveMiss,
    ResourceHandle,
    ResourceQuery,
)
from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter  # noqa: E402
from services.mcp.consumer.mcp_client import MCPClient  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"


@pytest_asyncio.fixture
async def sm(monkeypatch):
    """In-memory ConnectorBinding store; the calendar adapter's session_scope points at it."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s

    monkeypatch.setattr(cal_mod.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    yield maker
    await engine.dispose()


async def _seed(maker, status):
    async with maker() as s:
        await ConnectorBindingRepository(s).upsert(
            _ALPHA, "calendar", status=status, mcp_server_ref="calendar-mcp-server"
        )
        await s.commit()


def _texts(items):
    return [getattr(c, "text", "") for c in items if hasattr(c, "text")]


def _point_at_fixture(adapter):
    server = FastMCP("calendar-resolve-fixture")

    @server.tool(name=cal_mod._RESOLVE_TOOL)
    def resolve_resource(kind: str) -> str:
        return f"cal-handle:{kind}" if kind == "primary" else ""

    @contextlib.asynccontextmanager
    async def _ctx(binding):
        async with create_connected_server_and_client_session(server) as session:
            yield MCPClient(session)

    adapter._mcp_client_ctx = _ctx


class TestCalendarConnectStatus:
    async def test_no_binding_connect_is_connect_required(self, sm):
        res = await GoogleCalendarMCPAdapter().connect(_ALPHA)
        assert isinstance(res, ConnectRequired)
        assert res.degradation.user_message  # honest, never silently empty

    async def test_bound_connect_returns_binding(self, sm):
        await _seed(sm, "bound")
        res = await GoogleCalendarMCPAdapter().connect(_ALPHA)
        assert isinstance(res, Binding)
        assert res.binding_id

    async def test_no_binding_status_is_unbound(self, sm):
        st = await GoogleCalendarMCPAdapter().status(_ALPHA)
        assert st.state is ConnectorStatusState.UNBOUND


class TestCalendarResolveRail:
    async def test_no_binding_is_connect_required_miss(self, sm):
        res = await GoogleCalendarMCPAdapter().resolve(_ALPHA, ResourceQuery(kind="primary"))
        assert isinstance(res, ResolveMiss)
        assert res.degradation.reason is DegradationReason.CONNECT_REQUIRED

    async def test_bound_but_unprovisioned_is_unreachable_miss(self, sm):
        await _seed(sm, "bound")
        res = await GoogleCalendarMCPAdapter().resolve(_ALPHA, ResourceQuery(kind="primary"))
        assert isinstance(res, ResolveMiss)
        assert res.degradation.reason is DegradationReason.UNREACHABLE

    async def test_bound_hit_returns_resource_handle(self, sm):
        await _seed(sm, "bound")
        adapter = GoogleCalendarMCPAdapter()
        _point_at_fixture(adapter)
        res = await adapter.resolve(_ALPHA, ResourceQuery(kind="primary"))
        assert isinstance(res, ResourceHandle)
        assert res.handle == "cal-handle:primary"

    async def test_bound_miss_returns_resource_not_found(self, sm):
        await _seed(sm, "bound")
        adapter = GoogleCalendarMCPAdapter()
        _point_at_fixture(adapter)
        res = await adapter.resolve(_ALPHA, ResourceQuery(kind="nonexistent"))
        assert isinstance(res, ResolveMiss)
        assert res.degradation.reason is DegradationReason.RESOURCE_NOT_FOUND
