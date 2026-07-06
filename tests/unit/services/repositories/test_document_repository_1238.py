"""#1238 (ADR-071 P2) — DocumentRepository: owner-anchoring for the ChromaDB doc store.

Verifies the read-authorization core (the (c,3)→(a,1+global-flag) close):
`get_readable_base_ids(principal)` returns base_ids where `is_global_pm_domain`
is true OR `owner_id == principal`; a None/non-UUID principal sees global-only
(m-40 graceful). Plus `upsert_document` idempotency by chromadb_base_id and
`get_by_base_id`. In-memory SQLite (#1035 pattern).
"""

from __future__ import annotations

import uuid
from unittest.mock import patch

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy import func, select  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.database.models import DocumentDB  # noqa: E402
from services.repositories.document_repository import (  # noqa: E402
    DocumentRepository,
    resolve_pm_owner_id,
)

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"
_BETA = "22222222-2222-2222-2222-222222222222"


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: DocumentDB.__table__.create(c, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s
    await engine.dispose()


async def _seed(session):
    """Global doc + alpha-private + beta-private."""
    repo = DocumentRepository(session)
    await repo.upsert_document("g1", owner_id=_ALPHA, is_global_pm_domain=True, title="global")
    await repo.upsert_document("p_alpha", owner_id=_ALPHA, is_global_pm_domain=False)
    await repo.upsert_document("p_beta", owner_id=_BETA, is_global_pm_domain=False)
    await session.commit()
    return repo


class TestUpsert1238:
    async def test_upsert_inserts_then_updates_no_duplicate(self, session):
        repo = DocumentRepository(session)
        await repo.upsert_document("pdf_x", owner_id=_ALPHA, is_global_pm_domain=False, title="v1")
        await session.commit()
        # Same base_id again → update in place, not a second row
        await repo.upsert_document("pdf_x", owner_id=_ALPHA, is_global_pm_domain=True, title="v2")
        await session.commit()
        count = (await session.execute(select(func.count()).select_from(DocumentDB))).scalar_one()
        assert count == 1
        row = await repo.get_by_base_id("pdf_x")
        assert row.title == "v2"
        assert row.is_global_pm_domain is True

    async def test_get_by_base_id_missing_returns_none(self, session):
        repo = DocumentRepository(session)
        assert await repo.get_by_base_id("nope") is None


class TestReadableBaseIds1238:
    async def test_owner_sees_global_plus_own_private(self, session):
        repo = await _seed(session)
        assert await repo.get_readable_base_ids(_ALPHA) == {"g1", "p_alpha"}
        assert await repo.get_readable_base_ids(_BETA) == {"g1", "p_beta"}

    async def test_none_principal_sees_global_only(self, session):
        repo = await _seed(session)
        assert await repo.get_readable_base_ids(None) == {"g1"}

    async def test_non_uuid_principal_sees_global_only(self, session):
        # m-40 graceful: a legacy non-UUID id can't match a UUID owner → global-only
        repo = await _seed(session)
        assert await repo.get_readable_base_ids("default_user") == {"g1"}

    async def test_uuid_object_principal_accepted(self, session):
        repo = await _seed(session)
        assert await repo.get_readable_base_ids(uuid.UUID(_ALPHA)) == {"g1", "p_alpha"}


class _FakeResult:
    def __init__(self, val):
        self._val = val

    def scalar_one_or_none(self):
        return self._val


class _FakeSession:
    """Minimal async-session stub for resolve_pm_owner_id logic tests.

    The real `users` table can't be created on SQLite (User.id is postgresql.UUID,
    which doesn't compile on SQLite), so we stub the DB boundary here and verify
    the resolution LOGIC. The real query is exercised against dev Postgres by the
    Phase-4 backfill (resolve → a25db09c / username 'xian').
    """

    def __init__(self, scalar_value=None):
        self._scalar_value = scalar_value
        self.executed = False

    async def execute(self, _stmt):
        self.executed = True
        return _FakeResult(self._scalar_value)


def _patch_pm_identity_config(username):
    """#1260: resolve_pm_owner_id now sources the username from PiperConfigLoader
    (server-owned config, ADR-066 D7) instead of a hardcoded 'xian' literal --
    stub that lookup so these tests exercise the query-resolution logic itself,
    independent of whether this environment's PIPER.user.md has a PM Identity
    section configured."""
    return patch(
        "services.configuration.piper_config_loader.piper_config_loader.load_pm_identity_config",
        return_value=username,
    )


class TestResolvePmOwnerId1238:
    async def test_resolves_by_username_query(self):
        sess = _FakeSession(scalar_value=uuid.UUID(_ALPHA))
        with _patch_pm_identity_config("xian"):
            resolved = await resolve_pm_owner_id(sess)
        assert str(resolved) == _ALPHA
        assert sess.executed  # the username query ran

    async def test_env_override_short_circuits_before_query(self, monkeypatch):
        monkeypatch.setenv("PIPER_PM_USER_ID", _BETA)
        sess = _FakeSession(scalar_value=uuid.UUID(_ALPHA))
        resolved = await resolve_pm_owner_id(sess)
        assert str(resolved) == _BETA
        assert not sess.executed  # valid override returns before any DB query

    async def test_invalid_env_falls_through_to_username_query(self, monkeypatch):
        monkeypatch.setenv("PIPER_PM_USER_ID", "not-a-uuid")
        sess = _FakeSession(scalar_value=uuid.UUID(_ALPHA))
        with _patch_pm_identity_config("xian"):
            resolved = await resolve_pm_owner_id(sess)
        assert str(resolved) == _ALPHA  # invalid override ignored → username query
        assert sess.executed

    async def test_none_when_query_empty(self):
        sess = _FakeSession(scalar_value=None)
        with _patch_pm_identity_config("xian"):
            resolved = await resolve_pm_owner_id(sess)
        assert resolved is None
        assert sess.executed  # query ran (configured username), found nothing

    async def test_none_when_pm_identity_not_configured(self):
        """#1260: no 'PM Identity' section in PIPER.user.md -> graceful None,
        same as an absent env override. The query never runs (nothing to look up)."""
        sess = _FakeSession(scalar_value=uuid.UUID(_ALPHA))
        with _patch_pm_identity_config(None):
            resolved = await resolve_pm_owner_id(sess)
        assert resolved is None
        assert not sess.executed


class TestListForOwner1238:
    """#1238 Radar surface: list the user's OWN docs (owner-scoped, not global)."""

    async def test_owner_sees_only_own_docs(self, session):
        repo = await _seed(session)
        # ALPHA owns g1 (global) + p_alpha; ownership match includes the global one
        assert {r.chromadb_base_id for r in await repo.list_for_owner(_ALPHA)} == {"g1", "p_alpha"}
        # BETA owns only p_beta — does NOT see ALPHA's global g1 in their personal radar
        assert {r.chromadb_base_id for r in await repo.list_for_owner(_BETA)} == {"p_beta"}

    async def test_none_principal_empty(self, session):
        repo = await _seed(session)
        assert await repo.list_for_owner(None) == []

    async def test_non_uuid_principal_empty(self, session):
        repo = await _seed(session)
        assert await repo.list_for_owner("default_user") == []
