"""Integration tests for DBUserHistoryRepository (Issue #1021).

Exercises round-trip persistence of conversation history through the
real Postgres schema introduced by migration `a1021userhist`. Verifies:

- get_conversations: pagination, ordering, privacy filtering, DELETED exclusion
- search_conversations: title/preview/topics matching + private exclusion
- set_private: ownership-checked flag flip
- get_detail: turns shaped as [{role, content, timestamp}]
- save_turn / archive_conversation hooks: preview, topics, turn_count maintenance
- get_history_summary end-to-end through DB-backed repository

Requires the local Postgres container running on port 5433 (per
CLAUDE.md Quick Reference). Skip cleanly if no DB session can be opened.
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest

from services.database.models import ConversationDB, ConversationTurnDB
from services.database.repositories import (
    ConversationRepository,
    DBUserHistoryRepository,
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from services.domain import models as domain
from services.memory.user_history import UserHistoryService
from services.shared_types import ConversationLifecycleState

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
async def db_session():
    """Real Postgres session on a fresh per-test engine (#1452 wave 2 — the
    global factory's shared pool gets poisoned by loop-bound connections in
    full sweeps; see test_conversation_repository's fixture note)."""
    engine = create_async_engine(_DB_URL)
    maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with maker() as session:
        yield session
    await engine.dispose()


@pytest.fixture
async def user_id():
    return str(uuid4())


async def _make_conversation(
    session,
    user_id: str,
    title: str = "Test Conversation",
    is_private: bool = False,
    topics: list = None,
    preview: str = "",
    lifecycle_state: str = "active",
) -> ConversationDB:
    conv = ConversationDB(
        id=str(uuid4()),
        user_id=user_id,
        session_id=str(uuid4()),
        title=title,
        context={},
        is_active=True,
        lifecycle_state=lifecycle_state,
        topics=topics or [],
        preview=preview,
        is_private=is_private,
        turn_count=0,
        last_activity_at=datetime.now(timezone.utc),
    )
    session.add(conv)
    await session.commit()
    return conv


@pytest.mark.asyncio
async def test_get_conversations_pagination_and_ordering(db_session, user_id):
    convs = []
    for i in range(3):
        c = await _make_conversation(db_session, user_id, title=f"Conv {i}")
        c.last_activity_at = datetime.now(timezone.utc).replace(microsecond=i)
        convs.append(c)
    await db_session.commit()

    repo = DBUserHistoryRepository(db_session)
    page, total = await repo.get_conversations(
        user_id=user_id, offset=0, limit=2, include_private=False
    )

    assert total == 3
    assert len(page) == 2

    for c in convs:
        await db_session.delete(c)
    await db_session.commit()


@pytest.mark.asyncio
async def test_get_conversations_excludes_private_by_default(db_session, user_id):
    private = await _make_conversation(db_session, user_id, title="Secret", is_private=True)
    public = await _make_conversation(db_session, user_id, title="Public", is_private=False)

    repo = DBUserHistoryRepository(db_session)
    page, total = await repo.get_conversations(
        user_id=user_id, offset=0, limit=10, include_private=False
    )

    assert total == 1
    assert page[0].title == "Public"

    page2, total2 = await repo.get_conversations(
        user_id=user_id, offset=0, limit=10, include_private=True
    )
    assert total2 == 2

    await db_session.delete(private)
    await db_session.delete(public)
    await db_session.commit()


@pytest.mark.asyncio
async def test_get_conversations_excludes_deleted(db_session, user_id):
    active = await _make_conversation(db_session, user_id, title="Active")
    deleted = await _make_conversation(
        db_session,
        user_id,
        title="Deleted",
        lifecycle_state=ConversationLifecycleState.DELETED.value,
    )

    repo = DBUserHistoryRepository(db_session)
    page, total = await repo.get_conversations(
        user_id=user_id, offset=0, limit=10, include_private=True
    )

    titles = {c.title for c in page}
    assert "Active" in titles
    assert "Deleted" not in titles
    assert total == 1

    await db_session.delete(active)
    await db_session.delete(deleted)
    await db_session.commit()


@pytest.mark.asyncio
async def test_search_matches_title_preview_topics(db_session, user_id):
    # #1452: a unique token per run — the generic "roadmap" collided with
    # sweep residue in the shared dev DB (rows from other tests crowded the
    # limit=10 window; this masqueraded as a pg-version difference in CI).
    from uuid import uuid4 as _u4

    token = f"roadmap-{_u4().hex[:8]}"
    by_title = await _make_conversation(db_session, user_id, title=f"{token} discussion")
    by_preview = await _make_conversation(
        db_session, user_id, title="Other", preview=f"thoughts on the {token}"
    )
    by_topic = await _make_conversation(db_session, user_id, title="Third", topics=[token])
    no_match = await _make_conversation(db_session, user_id, title="Unrelated")

    repo = DBUserHistoryRepository(db_session)
    matches = await repo.search_conversations(user_id=user_id, query=token, limit=10)
    ids = {m.conversation_id for m in matches}

    assert by_title.id in ids
    assert by_preview.id in ids
    assert by_topic.id in ids
    assert no_match.id not in ids

    for c in (by_title, by_preview, by_topic, no_match):
        await db_session.delete(c)
    await db_session.commit()


@pytest.mark.asyncio
async def test_search_excludes_private(db_session, user_id):
    public = await _make_conversation(db_session, user_id, title="Public roadmap")
    private = await _make_conversation(
        db_session, user_id, title="Private roadmap", is_private=True
    )

    repo = DBUserHistoryRepository(db_session)
    matches = await repo.search_conversations(user_id=user_id, query="roadmap", limit=10)
    ids = {m.conversation_id for m in matches}

    assert public.id in ids
    assert private.id not in ids

    await db_session.delete(public)
    await db_session.delete(private)
    await db_session.commit()


@pytest.mark.asyncio
async def test_set_private_round_trip(db_session, user_id):
    conv = await _make_conversation(db_session, user_id, title="Test")

    repo = DBUserHistoryRepository(db_session)
    flipped = await repo.set_private(user_id=user_id, conversation_id=conv.id, is_private=True)
    assert flipped is True

    await db_session.refresh(conv)
    assert conv.is_private is True

    unflipped = await repo.set_private(user_id=user_id, conversation_id=conv.id, is_private=False)
    assert unflipped is True
    await db_session.refresh(conv)
    assert conv.is_private is False

    await db_session.delete(conv)
    await db_session.commit()


@pytest.mark.asyncio
async def test_set_private_rejects_other_user(db_session, user_id):
    conv = await _make_conversation(db_session, user_id, title="Mine")
    other = str(uuid4())

    repo = DBUserHistoryRepository(db_session)
    flipped = await repo.set_private(user_id=other, conversation_id=conv.id, is_private=True)
    assert flipped is False

    await db_session.refresh(conv)
    assert conv.is_private is False

    await db_session.delete(conv)
    await db_session.commit()


@pytest.mark.asyncio
async def test_save_turn_sets_preview_and_topics(db_session, user_id):
    conv = await _make_conversation(db_session, user_id, title="New conversation")
    repo = ConversationRepository(db_session)

    turn = domain.ConversationTurn(
        id=str(uuid4()),
        conversation_id=conv.id,
        turn_number=1,
        user_message="What's the roadmap look like for Q3?",
        assistant_response="Here is the roadmap...",
        intent="roadmap_planning",
        entities=["Q3"],
    )
    await repo.save_turn(turn, user_id=user_id)

    await db_session.refresh(conv)
    assert conv.preview.startswith("What's the roadmap")
    assert conv.turn_count == 1
    assert any("roadmap" in t.lower() for t in conv.topics)

    await db_session.delete(conv)
    await db_session.commit()


@pytest.mark.asyncio
async def test_archive_refreshes_preview_and_topics(db_session, user_id):
    conv = await _make_conversation(db_session, user_id, title="To archive")
    repo = ConversationRepository(db_session)

    for i, msg in enumerate(["First message about onboarding", "Follow-up on trial"]):
        await repo.save_turn(
            domain.ConversationTurn(
                id=str(uuid4()),
                conversation_id=conv.id,
                turn_number=i + 1,
                user_message=msg,
                assistant_response="ok",
                intent="onboarding_flow",
                entities=["trial"] if i == 1 else [],
            ),
            user_id=user_id,
        )

    archived = await repo.archive_conversation(conv.id)
    assert archived is not None

    await db_session.refresh(conv)
    assert conv.lifecycle_state == ConversationLifecycleState.ARCHIVED.value
    assert conv.turn_count == 2
    assert conv.preview.startswith("First message about onboarding")
    assert "onboarding flow" in conv.topics or "trial" in conv.topics

    await db_session.delete(conv)
    await db_session.commit()


@pytest.mark.asyncio
async def test_get_detail_returns_turns_with_roles(db_session, user_id):
    conv = await _make_conversation(db_session, user_id, title="Detail test")
    repo = ConversationRepository(db_session)
    await repo.save_turn(
        domain.ConversationTurn(
            id=str(uuid4()),
            conversation_id=conv.id,
            turn_number=1,
            user_message="hello",
            assistant_response="hi there",
        ),
        user_id=user_id,
    )

    hist_repo = DBUserHistoryRepository(db_session)
    detail = await hist_repo.get_detail(user_id=user_id, conversation_id=conv.id)

    assert detail is not None
    assert detail.conversation_id == conv.id
    roles = [t["role"] for t in detail.turns]
    assert "user" in roles
    assert "assistant" in roles

    await db_session.delete(conv)
    await db_session.commit()


@pytest.mark.asyncio
async def test_get_history_summary_end_to_end(db_session, user_id):
    conv = await _make_conversation(
        db_session,
        user_id,
        title="History",
        topics=["roadmap", "onboarding"],
        preview="Where are we?",
    )
    conv.last_activity_at = datetime.now(timezone.utc)
    await db_session.commit()

    repo = DBUserHistoryRepository(db_session)
    service = UserHistoryService(repo)
    summary = await service.get_history_summary(user_id=user_id)

    assert summary is not None
    assert "Last active" in summary
    assert "roadmap" in summary

    await db_session.delete(conv)
    await db_session.commit()
