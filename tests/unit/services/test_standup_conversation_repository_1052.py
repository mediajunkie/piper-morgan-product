"""
#1052 Phase 1 — StandupConversationRepository unit tests.

Mirrors the #1018/#1035 in-memory-SQLite pattern: aiosqlite engine, table
created via SQLAlchemy metadata, full CRUD + query-shape coverage for the
new repository layer that will back the StandupConversationManager rewrite
in Phase 2.

Methods covered:
- add / get_by_id
- get_by_session_id (latest by created_at)
- get_active_for_user (filters terminal states)
- update (full replace; raises if id not found)
- delete (returns rowcount-bool)
- count_for_user (diagnostics)

User-scoping + multi-tenancy isolation verified throughout.
Round-trip (from_domain → to_domain) preservation verified for nested
fields (turns array, JSONB preferences/context).
"""

from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

import pytest
import pytest_asyncio

# Skip module if aiosqlite missing (parallel to #1018/#1035 pattern).
aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine  # noqa: E402

from services.database.models import StandupConversationDB  # noqa: E402
from services.database.repositories import StandupConversationRepository  # noqa: E402
from services.domain.models import ConversationTurn, StandupConversation  # noqa: E402
from services.shared_types import StandupConversationState  # noqa: E402

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def session():
    """Fresh in-memory SQLite session per test with table created."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: StandupConversationDB.__table__.create(sync_conn, checkfirst=True)
        )
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s
    await engine.dispose()


def _make_conv(
    *,
    conversation_id: str | None = None,
    session_id: str = "sess-1",
    user_id: str = "user-alpha",
    state: StandupConversationState = StandupConversationState.INITIATED,
    preferences: dict | None = None,
    turns_count: int = 0,
    created_at: datetime | None = None,
) -> StandupConversation:
    """Helper: build a StandupConversation with sensible defaults."""
    cid = conversation_id or str(uuid4())
    turns = [
        ConversationTurn(
            id=str(uuid4()),
            conversation_id=cid,
            turn_number=i + 1,
            user_message=f"msg {i + 1}",
            assistant_response=f"reply {i + 1}",
        )
        for i in range(turns_count)
    ]
    return StandupConversation(
        id=cid,
        session_id=session_id,
        user_id=user_id,
        state=state,
        preferences=preferences or {},
        turns=turns,
        created_at=created_at or datetime.now(),
        updated_at=created_at or datetime.now(),
    )


class TestAddAndGetById:
    """add() persists; get_by_id() round-trips."""

    async def test_add_and_get_round_trip(self, session):
        repo = StandupConversationRepository(session)
        conv = _make_conv(
            preferences={"focus": "github"},
            turns_count=3,
        )
        await repo.add(conv)

        recovered = await repo.get_by_id(conv.id)
        assert recovered is not None
        assert recovered.id == conv.id
        assert recovered.session_id == conv.session_id
        assert recovered.user_id == conv.user_id
        assert recovered.state == conv.state
        assert recovered.preferences == {"focus": "github"}
        assert len(recovered.turns) == 3
        assert recovered.turns[0].user_message == "msg 1"
        assert recovered.turns[2].turn_number == 3

    async def test_get_nonexistent_returns_none(self, session):
        repo = StandupConversationRepository(session)
        assert await repo.get_by_id("nonexistent") is None

    async def test_add_preserves_complex_context(self, session):
        repo = StandupConversationRepository(session)
        conv = _make_conv()
        conv.context = {
            "github_activity": [{"sha": "abc", "msg": "fix"}],
            "calendar_events": [],
            "metadata": {"source": "auto"},
        }
        await repo.add(conv)

        recovered = await repo.get_by_id(conv.id)
        assert recovered.context["github_activity"] == [{"sha": "abc", "msg": "fix"}]
        assert recovered.context["calendar_events"] == []
        assert recovered.context["metadata"]["source"] == "auto"


class TestGetBySessionId:
    """get_by_session_id() returns latest per session."""

    async def test_returns_conversation_for_session(self, session):
        repo = StandupConversationRepository(session)
        conv = _make_conv(session_id="sess-A")
        await repo.add(conv)

        recovered = await repo.get_by_session_id("sess-A")
        assert recovered is not None
        assert recovered.id == conv.id

    async def test_returns_latest_when_multiple_per_session(self, session):
        repo = StandupConversationRepository(session)
        old = _make_conv(
            session_id="sess-A",
            created_at=datetime.now() - timedelta(hours=2),
        )
        new = _make_conv(
            session_id="sess-A",
            created_at=datetime.now(),
        )
        await repo.add(old)
        await repo.add(new)

        recovered = await repo.get_by_session_id("sess-A")
        assert recovered.id == new.id

    async def test_returns_none_for_unknown_session(self, session):
        repo = StandupConversationRepository(session)
        assert await repo.get_by_session_id("never-existed") is None


class TestGetActiveForUser:
    """get_active_for_user() filters terminal states."""

    async def test_returns_active_conversations(self, session):
        repo = StandupConversationRepository(session)
        active = _make_conv(user_id="alpha", state=StandupConversationState.GATHERING_PREFERENCES)
        suspended = _make_conv(user_id="alpha", state=StandupConversationState.SUSPENDED)
        await repo.add(active)
        await repo.add(suspended)

        result = await repo.get_active_for_user("alpha")
        result_ids = {c.id for c in result}
        assert active.id in result_ids
        assert suspended.id in result_ids

    async def test_excludes_complete_state(self, session):
        repo = StandupConversationRepository(session)
        complete = _make_conv(user_id="alpha", state=StandupConversationState.COMPLETE)
        await repo.add(complete)

        result = await repo.get_active_for_user("alpha")
        assert all(c.id != complete.id for c in result)

    async def test_excludes_abandoned_state(self, session):
        repo = StandupConversationRepository(session)
        abandoned = _make_conv(user_id="alpha", state=StandupConversationState.ABANDONED)
        await repo.add(abandoned)

        result = await repo.get_active_for_user("alpha")
        assert all(c.id != abandoned.id for c in result)

    async def test_user_scoped(self, session):
        repo = StandupConversationRepository(session)
        a_conv = _make_conv(user_id="alpha", state=StandupConversationState.INITIATED)
        b_conv = _make_conv(user_id="beta", state=StandupConversationState.INITIATED)
        await repo.add(a_conv)
        await repo.add(b_conv)

        a_result = await repo.get_active_for_user("alpha")
        assert len(a_result) == 1
        assert a_result[0].id == a_conv.id

        b_result = await repo.get_active_for_user("beta")
        assert len(b_result) == 1
        assert b_result[0].id == b_conv.id

    async def test_returns_empty_for_unknown_user(self, session):
        repo = StandupConversationRepository(session)
        result = await repo.get_active_for_user("never-existed")
        assert result == []


class TestUpdate:
    """update() replaces full row."""

    async def test_update_persists_state_change(self, session):
        repo = StandupConversationRepository(session)
        conv = _make_conv(state=StandupConversationState.INITIATED)
        await repo.add(conv)

        # Mutate state + add a turn
        conv.state = StandupConversationState.GATHERING_PREFERENCES
        conv.turns.append(
            ConversationTurn(
                id=str(uuid4()),
                conversation_id=conv.id,
                turn_number=1,
                user_message="hi piper",
                assistant_response="hi user",
            )
        )
        await repo.update(conv)

        recovered = await repo.get_by_id(conv.id)
        assert recovered.state == StandupConversationState.GATHERING_PREFERENCES
        assert len(recovered.turns) == 1
        assert recovered.turns[0].user_message == "hi piper"

    async def test_update_persists_preferences_overwrite(self, session):
        repo = StandupConversationRepository(session)
        conv = _make_conv(preferences={"focus": "github"})
        await repo.add(conv)

        conv.preferences = {"focus": "calendar", "format": "brief"}
        await repo.update(conv)

        recovered = await repo.get_by_id(conv.id)
        assert recovered.preferences == {"focus": "calendar", "format": "brief"}

    async def test_update_raises_on_unknown_id(self, session):
        repo = StandupConversationRepository(session)
        ghost = _make_conv()  # never added
        with pytest.raises(ValueError, match="not found for update"):
            await repo.update(ghost)

    async def test_update_records_completed_at(self, session):
        repo = StandupConversationRepository(session)
        conv = _make_conv()
        await repo.add(conv)

        conv.state = StandupConversationState.COMPLETE
        conv.completed_at = datetime.now()
        await repo.update(conv)

        recovered = await repo.get_by_id(conv.id)
        assert recovered.state == StandupConversationState.COMPLETE
        assert recovered.completed_at is not None


class TestDelete:
    """delete() returns rowcount-bool."""

    async def test_delete_removes_existing(self, session):
        repo = StandupConversationRepository(session)
        conv = _make_conv()
        await repo.add(conv)

        result = await repo.delete(conv.id)
        assert result is True
        assert await repo.get_by_id(conv.id) is None

    async def test_delete_returns_false_for_unknown(self, session):
        repo = StandupConversationRepository(session)
        assert await repo.delete("never-existed") is False


class TestCountForUser:
    """count_for_user() includes all states (diagnostic)."""

    async def test_count_returns_all_states(self, session):
        repo = StandupConversationRepository(session)
        await repo.add(_make_conv(user_id="alpha", state=StandupConversationState.COMPLETE))
        await repo.add(_make_conv(user_id="alpha", state=StandupConversationState.ABANDONED))
        await repo.add(_make_conv(user_id="alpha", state=StandupConversationState.INITIATED))

        assert await repo.count_for_user("alpha") == 3

    async def test_count_user_scoped(self, session):
        repo = StandupConversationRepository(session)
        await repo.add(_make_conv(user_id="alpha"))
        await repo.add(_make_conv(user_id="beta"))
        await repo.add(_make_conv(user_id="alpha"))

        assert await repo.count_for_user("alpha") == 2
        assert await repo.count_for_user("beta") == 1


class TestRoundTripPreservation:
    """from_domain ↔ to_domain preserves nested structures."""

    async def test_preserves_nested_turn_metadata(self, session):
        repo = StandupConversationRepository(session)
        conv = _make_conv()
        conv.turns = [
            ConversationTurn(
                id="t1",
                conversation_id=conv.id,
                turn_number=1,
                user_message="hello",
                assistant_response="hi",
                intent="greeting",
                entities=["piper", "morgan"],
                references={"prev": "t0"},
                context_used={"github": True},
                metadata={"source": "test"},
                processing_time=12.5,
            )
        ]
        await repo.add(conv)

        recovered = await repo.get_by_id(conv.id)
        t = recovered.turns[0]
        assert t.id == "t1"
        assert t.intent == "greeting"
        assert t.entities == ["piper", "morgan"]
        assert t.references == {"prev": "t0"}
        assert t.context_used == {"github": True}
        assert t.metadata == {"source": "test"}
        assert t.processing_time == 12.5

    async def test_preserves_state_machine_history(self, session):
        repo = StandupConversationRepository(session)
        conv = _make_conv(state=StandupConversationState.GENERATING)
        conv.previous_state = StandupConversationState.GATHERING_PREFERENCES
        await repo.add(conv)

        recovered = await repo.get_by_id(conv.id)
        assert recovered.state == StandupConversationState.GENERATING
        assert recovered.previous_state == StandupConversationState.GATHERING_PREFERENCES

    async def test_preserves_standup_versions_array(self, session):
        repo = StandupConversationRepository(session)
        conv = _make_conv()
        conv.current_standup = "current text"
        conv.standup_versions = ["v1 text", "v2 text"]
        await repo.add(conv)

        recovered = await repo.get_by_id(conv.id)
        assert recovered.current_standup == "current text"
        assert recovered.standup_versions == ["v1 text", "v2 text"]
