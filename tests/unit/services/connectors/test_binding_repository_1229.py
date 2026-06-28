"""RECONNECT WS-2 (#1229) — ConnectorBindingRepository.

The per-user MCP-server binding store (ADR-070 D3: Piper stores bindings only, never raw creds).
Mirrors the WS-1 connector-config repo test setup (#1226): in-memory SQLite, single-table create
(the full metadata has PG-only types). Verifies get/upsert idempotency + per-owner isolation +
the strict-write/graceful-read asymmetry + status transitions + field round-trip + defaults.
"""

from __future__ import annotations

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy import func, select  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors.binding_repository import ConnectorBindingRepository  # noqa: E402
from services.database.models import ConnectorBinding  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"
_BETA = "22222222-2222-2222-2222-222222222222"


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        # single-table create: the full metadata has PG-only types (users.id = postgresql.UUID)
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s
    await engine.dispose()


async def _count(session) -> int:
    return (await session.execute(select(func.count()).select_from(ConnectorBinding))).scalar_one()


class TestUpsert:
    async def test_insert_then_update_in_place_no_duplicate(self, session):
        repo = ConnectorBindingRepository(session)
        await repo.upsert(_ALPHA, "github", mcp_server_ref="github-mcp-server", status="bound")
        await session.commit()
        # same (owner, connector) → update in place, not a second row
        await repo.upsert(_ALPHA, "github", status="stale")
        await session.commit()
        assert await _count(session) == 1
        row = await repo.get(_ALPHA, "github")
        assert row.mcp_server_ref == "github-mcp-server"  # preserved (not passed on 2nd upsert)
        assert row.status == "stale"  # updated

    async def test_fresh_binding_defaults(self, session):
        repo = ConnectorBindingRepository(session)
        await repo.upsert(_ALPHA, "slack")
        await session.commit()
        row = await repo.get(_ALPHA, "slack")
        assert row.status == "unbound"
        assert row.is_native_legacy is False
        assert row.capability_profile == {}
        assert row.mcp_server_ref is None

    async def test_field_round_trip(self, session):
        repo = ConnectorBindingRepository(session)
        await repo.upsert(
            _ALPHA,
            "calendar",
            mcp_server_ref="gcal-mcp",
            status="bound",
            capability_profile={"scopes": ["read", "write"]},
            is_native_legacy=True,
        )
        await session.commit()
        row = await repo.get(_ALPHA, "calendar")
        assert row.mcp_server_ref == "gcal-mcp"
        assert row.status == "bound"
        assert row.capability_profile == {"scopes": ["read", "write"]}
        assert row.is_native_legacy is True


class TestOwnerIsolation:
    async def test_owner_a_binding_invisible_to_owner_b(self, session):
        repo = ConnectorBindingRepository(session)
        await repo.upsert(_ALPHA, "github", mcp_server_ref="a-server")
        await session.commit()
        assert await repo.get(_BETA, "github") is None  # ADR-058 per-user isolation
        assert await repo.get(_ALPHA, "github") is not None


class TestReadWriteAsymmetry:
    async def test_bad_owner_read_returns_none(self, session):
        repo = ConnectorBindingRepository(session)
        assert await repo.get(None, "github") is None
        assert await repo.get("not-a-uuid", "github") is None

    async def test_bad_owner_write_raises(self, session):
        repo = ConnectorBindingRepository(session)
        with pytest.raises(ValueError):
            await repo.upsert(None, "github", status="bound")
        with pytest.raises(ValueError):
            await repo.upsert("not-a-uuid", "github", status="bound")


class TestSetStatus:
    async def test_set_status_updates(self, session):
        repo = ConnectorBindingRepository(session)
        await repo.upsert(_ALPHA, "notion", status="unbound")
        await session.commit()
        updated = await repo.set_status(_ALPHA, "notion", "bound")
        await session.commit()
        assert updated is not None and updated.status == "bound"
        assert (await repo.get(_ALPHA, "notion")).status == "bound"

    async def test_set_status_no_binding_returns_none(self, session):
        repo = ConnectorBindingRepository(session)
        # status is a no-op without a binding (can't be 'bound' before connect() creates the row)
        assert await repo.set_status(_ALPHA, "github", "bound") is None
        assert await repo.set_status(None, "github", "bound") is None
