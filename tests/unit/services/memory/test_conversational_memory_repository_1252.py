"""#1252 P7 (ADR-071 D2) — ConversationalMemoryRepository owner_id scoping.

The repo had NO unit/integration coverage (the service tests mock it), so the
user_id→owner_id reader-migration needs its own real-DB test. In-memory SQLite
(mirrors the #1035 InsightRepository pattern). Verifies: save_entry dual-writes
owner_id (UUID); get_entries_since / delete_entries_before scope by owner_id;
cross-owner isolation holds.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy import select  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.database.models import ConversationalMemoryEntryDB  # noqa: E402
from services.memory.conversational_memory import ConversationalMemoryEntry  # noqa: E402
from services.repositories.conversational_memory_repository import (  # noqa: E402
    ConversationalMemoryRepository,
)

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"
_BETA = "22222222-2222-2222-2222-222222222222"


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda c: ConversationalMemoryEntryDB.__table__.create(c, checkfirst=True)
        )
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s
    await engine.dispose()


def _entry(
    conv: str = "conv-1", topic: str = "t", hours_ago: float = 0
) -> ConversationalMemoryEntry:
    return ConversationalMemoryEntry(
        conversation_id=conv,
        timestamp=datetime.now(timezone.utc) - timedelta(hours=hours_ago),
        topic_summary=topic,
        entities_mentioned=[],
        outcome=None,
        user_sentiment=None,
    )


class TestOwnerIdScoping1252:
    async def test_save_entry_dual_writes_owner_id(self, session):
        repo = ConversationalMemoryRepository(session)
        await repo.save_entry(_ALPHA, _entry())
        row = (await session.execute(select(ConversationalMemoryEntryDB))).scalar_one()
        assert str(row.owner_id) == _ALPHA
        assert row.user_id == _ALPHA  # legacy column still written during transition

    async def test_get_entries_since_scoped_by_owner(self, session):
        repo = ConversationalMemoryRepository(session)
        await repo.save_entry(_ALPHA, _entry(topic="alpha-topic"))
        await repo.save_entry(_BETA, _entry(topic="beta-topic"))
        since = datetime.now(timezone.utc) - timedelta(hours=1)

        alpha = await repo.get_entries_since(_ALPHA, since)
        assert [e.topic_summary for e in alpha] == ["alpha-topic"]
        beta = await repo.get_entries_since(_BETA, since)
        assert [e.topic_summary for e in beta] == ["beta-topic"]

    async def test_delete_entries_before_scoped_by_owner(self, session):
        repo = ConversationalMemoryRepository(session)
        await repo.save_entry(_ALPHA, _entry(topic="old-alpha", hours_ago=48))
        await repo.save_entry(_BETA, _entry(topic="old-beta", hours_ago=48))
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)

        deleted = await repo.delete_entries_before(_ALPHA, cutoff)
        assert deleted == 1  # only alpha's old entry

        # beta's entry is untouched (cross-owner isolation on delete)
        remaining = (await session.execute(select(ConversationalMemoryEntryDB))).scalars().all()
        assert [r.user_id for r in remaining] == [_BETA]
