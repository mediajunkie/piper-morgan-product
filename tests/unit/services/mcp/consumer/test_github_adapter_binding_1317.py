"""#1317 GitHub port, increment 1 — connect()/status() read the ConnectorBinding store (#1229).

The github adapter's protocol methods now reflect real per-user binding health (ADR-070 D3 —
Piper stores bindings, never raw tokens), honest-degrading to ConnectRequired / UNBOUND when no
binding exists. (Increment 2 adds the OAuth callback that CREATES the binding per ADR-070 OQ-5;
increment 3 wires resolve().) Verified against an in-memory ConnectorBinding store with the
adapter's `session_scope` pointed at the test session.
"""

from __future__ import annotations

import contextlib

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors.binding_repository import ConnectorBindingRepository  # noqa: E402
from services.database.models import ConnectorBinding  # noqa: E402
from services.mcp.consumer import github_adapter as gh_mod  # noqa: E402
from services.mcp.consumer.connector import (  # noqa: E402
    Binding,
    ConnectRequired,
    ConnectorStatusState,
)
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter  # noqa: E402

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


async def _seed(maker, status):
    async with maker() as s:
        await ConnectorBindingRepository(s).upsert(
            _ALPHA, "github", status=status, mcp_server_ref="github-mcp-server"
        )
        await s.commit()


class TestStatus:
    async def test_no_binding_is_unbound(self, sm):
        st = await GitHubMCPSpatialAdapter().status(_ALPHA)
        assert st.state is ConnectorStatusState.UNBOUND

    async def test_bound_binding_reports_bound(self, sm):
        await _seed(sm, "bound")
        st = await GitHubMCPSpatialAdapter().status(_ALPHA)
        assert st.state is ConnectorStatusState.BOUND

    async def test_stale_binding_reports_stale(self, sm):
        await _seed(sm, "stale")
        st = await GitHubMCPSpatialAdapter().status(_ALPHA)
        assert st.state is ConnectorStatusState.STALE


class TestConnect:
    async def test_unbound_returns_connect_required_not_silent(self, sm):
        res = await GitHubMCPSpatialAdapter().connect(_ALPHA)
        assert isinstance(res, ConnectRequired)
        assert res.degradation.user_message  # honest "connect me", never silently empty

    async def test_unbound_binding_present_but_not_bound_still_connect_required(self, sm):
        await _seed(sm, "unbound")  # a row exists but isn't BOUND
        res = await GitHubMCPSpatialAdapter().connect(_ALPHA)
        assert isinstance(res, ConnectRequired)

    async def test_bound_returns_binding_with_id(self, sm):
        await _seed(sm, "bound")
        res = await GitHubMCPSpatialAdapter().connect(_ALPHA)
        assert isinstance(res, Binding)
        assert res.binding_id  # the binding row id (never a token — D3)
