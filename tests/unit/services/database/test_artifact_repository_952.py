"""#952 ARTIFACT-MODEL — Phase 2-3: ArtifactDB + ArtifactRepository.

Real round-trip against in-memory SQLite (the #1035 pattern; ArtifactDB uses
plain JSON + String, so it builds on SQLite cleanly — no JSONB variant needed).
Verifies the storage layer + owner-scoped CRUD read/write API (#952 ACs).
"""

from __future__ import annotations

from datetime import datetime

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.database.models import ArtifactDB  # noqa: E402
from services.database.repositories import ArtifactRepository  # noqa: E402
from services.domain.models import (  # noqa: E402
    Artifact,
    ArtifactSourceType,
    Document,
)
from services.mux.lifecycle import LifecycleState  # noqa: E402


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sc: ArtifactDB.__table__.create(sc, checkfirst=True)
        )
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s
    await engine.dispose()


def _generated(owner="user-1", aid="art-1") -> Artifact:
    return Artifact(
        id=aid,
        content="A saved chat summary.",
        source_type=ArtifactSourceType.GENERATED,
        lifecycle_state=LifecycleState.RATIFIED,
        owner_id=owner,
        source_conversation_id="conv-9",
        created_at=datetime(2026, 6, 9, 10, 0, 0),
        updated_at=datetime(2026, 6, 9, 10, 0, 0),
    )


class TestArtifactDBRoundTrip:
    @pytest.mark.asyncio
    async def test_generated_artifact_db_round_trip(self, session):
        repo = ArtifactRepository(session)
        art = _generated()
        await repo.add(art)

        got = await repo.get_by_id("art-1")
        assert got is not None
        assert got.id == "art-1"
        assert got.content == "A saved chat summary."
        assert got.source_type == ArtifactSourceType.GENERATED
        assert got.lifecycle_state is LifecycleState.RATIFIED  # str↔enum survives
        assert got.owner_id == "user-1"
        assert got.source_conversation_id == "conv-9"

    @pytest.mark.asyncio
    async def test_document_payload_persists_json_safe(self, session):
        """A document-Artifact (datetime in payload) persists JSON-safe — the
        datetime-aware codec keeps ArtifactDB.payload storable."""
        doc = Document(
            id="art-doc", title="t", content="body",
            created_at=datetime(2026, 6, 9, 9, 0, 0),
            updated_at=datetime(2026, 6, 9, 9, 0, 0),
            last_accessed=datetime(2026, 6, 9, 9, 0, 0),
        )
        art = Artifact.from_document(doc)
        art.owner_id = "user-2"
        repo = ArtifactRepository(session)
        await repo.add(art)
        got = await repo.get_by_id("art-doc")
        assert got is not None
        assert got.source_type == ArtifactSourceType.DOCUMENT
        assert got.payload["title"] == "t"
        # datetime in payload survived as ISO string (JSON-safe projection)
        assert got.payload["last_accessed"] == "2026-06-09T09:00:00"


class TestArtifactRepositoryCRUD:
    @pytest.mark.asyncio
    async def test_list_for_owner_scoped(self, session):
        repo = ArtifactRepository(session)
        await repo.add(_generated(owner="user-A", aid="a1"))
        await repo.add(_generated(owner="user-A", aid="a2"))
        await repo.add(_generated(owner="user-B", aid="b1"))

        a_list = await repo.list_for_owner("user-A")
        assert {a.id for a in a_list} == {"a1", "a2"}
        b_list = await repo.list_for_owner("user-B")
        assert {a.id for a in b_list} == {"b1"}

    @pytest.mark.asyncio
    async def test_get_by_id_owner_scope_blocks_cross_owner(self, session):
        repo = ArtifactRepository(session)
        await repo.add(_generated(owner="user-A", aid="a1"))
        # wrong owner → None
        assert await repo.get_by_id("a1", owner_id="user-B") is None
        # right owner → found
        assert await repo.get_by_id("a1", owner_id="user-A") is not None
        # admin bypass → found regardless
        assert await repo.get_by_id("a1", owner_id="user-B", is_admin=True) is not None

    @pytest.mark.asyncio
    async def test_delete_owner_scoped(self, session):
        repo = ArtifactRepository(session)
        await repo.add(_generated(owner="user-A", aid="a1"))
        # cross-owner delete refused
        assert await repo.delete("a1", owner_id="user-B") is False
        assert await repo.get_by_id("a1") is not None
        # owner delete succeeds
        assert await repo.delete("a1", owner_id="user-A") is True
        assert await repo.get_by_id("a1") is None

    @pytest.mark.asyncio
    async def test_delete_missing_returns_false(self, session):
        repo = ArtifactRepository(session)
        assert await repo.delete("nope") is False


class TestArtifactRename1184:
    """#1184 — owner-scoped rename (update payload['title']). The rename must NOT
    introduce an (a,3) leak (the #1241 audit lesson): cross-owner rename → None."""

    @pytest.mark.asyncio
    async def test_update_title_persists_owner_scoped(self, session):
        repo = ArtifactRepository(session)
        await repo.add(_generated(owner="user-A", aid="a1"))
        updated = await repo.update_title("a1", "Q3 Planning Notes", owner_id="user-A")
        assert updated is not None
        assert updated.payload.get("title") == "Q3 Planning Notes"
        # persisted across a fresh read (JSON-column mutation actually flushed)
        got = await repo.get_by_id("a1")
        assert got.payload.get("title") == "Q3 Planning Notes"

    @pytest.mark.asyncio
    async def test_update_title_blocks_cross_owner(self, session):
        repo = ArtifactRepository(session)
        await repo.add(_generated(owner="user-A", aid="a1"))
        # cross-owner rename refused → None, title untouched (no (a,3) leak)
        assert await repo.update_title("a1", "Hacked", owner_id="user-B") is None
        got = await repo.get_by_id("a1")
        assert (got.payload or {}).get("title") != "Hacked"
        # admin bypass (the #470 pattern) works
        assert await repo.update_title("a1", "AdminSet", owner_id="user-B", is_admin=True) is not None

    @pytest.mark.asyncio
    async def test_update_title_missing_returns_none(self, session):
        repo = ArtifactRepository(session)
        assert await repo.update_title("nope", "X", owner_id="user-A") is None

    @pytest.mark.asyncio
    async def test_list_filter_by_source_type(self, session):
        repo = ArtifactRepository(session)
        await repo.add(_generated(owner="u", aid="g1"))
        doc_art = Artifact.from_document(
            Document(id="d1", content="x",
                     created_at=datetime(2026, 6, 9), updated_at=datetime(2026, 6, 9),
                     last_accessed=datetime(2026, 6, 9))
        )
        doc_art.owner_id = "u"
        await repo.add(doc_art)
        gens = await repo.list_for_owner("u", source_type="generated")
        assert {a.id for a in gens} == {"g1"}
