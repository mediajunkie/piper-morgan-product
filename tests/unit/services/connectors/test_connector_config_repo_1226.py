"""RECONNECT WS-1 (#1226 / #1199) P2 — ConnectorConfigRepository + ConnectorConfigService.

The DB-backed connector-config access layer (ADR-070 D4). Mirrors the #1238 doc-repo test
setup (in-memory SQLite, single-table create — the full metadata has PG-only types). Verifies
repo get/upsert idempotency + per-owner isolation + the strict-write/graceful-read asymmetry,
and the service's github default-repo accessors (the UserPreferenceManager drop-in).
"""
from __future__ import annotations

import uuid

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy import func, select  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors.config_repository import ConnectorConfigRepository  # noqa: E402
from services.connectors.config_service import ConnectorConfigService  # noqa: E402
from services.database.models import ConnectorConfig  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"
_BETA = "22222222-2222-2222-2222-222222222222"


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        # single-table create: the full metadata has PG-only types (users.id = postgresql.UUID)
        await conn.run_sync(lambda c: ConnectorConfig.__table__.create(c, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s
    await engine.dispose()


async def _count(session) -> int:
    return (await session.execute(select(func.count()).select_from(ConnectorConfig))).scalar_one()


class TestRepoUpsert1226:
    async def test_upsert_inserts_then_replaces_no_duplicate(self, session):
        repo = ConnectorConfigRepository(session)
        await repo.upsert(_ALPHA, "github", {"default_repository": "o/r1"})
        await session.commit()
        # same (owner, connector) → replace in place, not a second row
        await repo.upsert(_ALPHA, "github", {"default_repository": "o/r2"})
        await session.commit()
        assert await _count(session) == 1
        row = await repo.get(_ALPHA, "github")
        assert row.config["default_repository"] == "o/r2"

    async def test_get_missing_returns_none(self, session):
        repo = ConnectorConfigRepository(session)
        assert await repo.get(_ALPHA, "github") is None

    async def test_per_owner_isolation(self, session):
        repo = ConnectorConfigRepository(session)
        await repo.upsert(_ALPHA, "github", {"default_repository": "alpha/r"})
        await repo.upsert(_BETA, "github", {"default_repository": "beta/r"})
        await session.commit()
        assert (await repo.get(_ALPHA, "github")).config["default_repository"] == "alpha/r"
        assert (await repo.get(_BETA, "github")).config["default_repository"] == "beta/r"

    async def test_same_owner_distinct_connectors(self, session):
        repo = ConnectorConfigRepository(session)
        await repo.upsert(_ALPHA, "github", {"default_repository": "o/r"})
        await repo.upsert(_ALPHA, "slack", {"channel": "#general"})
        await session.commit()
        assert await _count(session) == 2  # (owner,github) and (owner,slack) are distinct

    async def test_get_none_or_nonuuid_owner_graceful(self, session):
        repo = ConnectorConfigRepository(session)
        assert await repo.get(None, "github") is None
        assert await repo.get("not-a-uuid", "github") is None

    async def test_upsert_none_owner_raises(self, session):
        # writes are STRICT — config must belong to the settled identity (owner_id NOT NULL, D2)
        repo = ConnectorConfigRepository(session)
        with pytest.raises(ValueError):
            await repo.upsert(None, "github", {"x": 1})
        with pytest.raises(ValueError):
            await repo.upsert("not-a-uuid", "github", {"x": 1})

    async def test_uuid_object_owner_accepted(self, session):
        repo = ConnectorConfigRepository(session)
        await repo.upsert(uuid.UUID(_ALPHA), "github", {"default_repository": "o/r"})
        await session.commit()
        assert (await repo.get(uuid.UUID(_ALPHA), "github")).config["default_repository"] == "o/r"


class TestServiceDefaultRepo1226:
    async def test_set_then_get_default_repo(self, session):
        svc = ConnectorConfigService(session)
        await svc.set_default_repo(_ALPHA, "owner/myrepo")
        await session.commit()
        assert await svc.get_default_repo(_ALPHA) == "owner/myrepo"

    async def test_get_default_repo_unset_is_none(self, session):
        svc = ConnectorConfigService(session)
        assert await svc.get_default_repo(_ALPHA) is None

    async def test_set_default_repo_none_clears(self, session):
        svc = ConnectorConfigService(session)
        await svc.set_default_repo(_ALPHA, "owner/myrepo")
        await session.commit()
        await svc.set_default_repo(_ALPHA, None)
        await session.commit()
        assert await svc.get_default_repo(_ALPHA) is None

    async def test_set_default_repo_preserves_other_keys(self, session):
        # setting default_repo must not clobber other config keys for the connector
        svc = ConnectorConfigService(session)
        await svc.set_config(_ALPHA, "github", {"other": "keep", "default_repository": "o/old"})
        await session.commit()
        await svc.set_default_repo(_ALPHA, "o/new")
        await session.commit()
        cfg = await svc.get_config(_ALPHA, "github")
        assert cfg["default_repository"] == "o/new"
        assert cfg["other"] == "keep"

    async def test_get_config_none_owner_graceful_empty(self, session):
        svc = ConnectorConfigService(session)
        assert await svc.get_config(None, "github") == {}
