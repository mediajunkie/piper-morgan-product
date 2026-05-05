"""
Issue #552 / #1052 Phase 2: Tests for StandupConversationManager.

Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Manager rewritten in #1052 Phase 2 (May 5, 2026) to delegate to
StandupConversationRepository (durable PostgreSQL). Tests exercise the
manager via in-memory SQLite by overriding its `_session_scope` to yield
a test-scoped session.

State machine semantics, lifecycle, turn management, preferences, and
content versioning are covered against the durable storage path.

Repository-layer correctness is covered separately in
`tests/unit/services/test_standup_conversation_repository_1052.py`.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timedelta

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine  # noqa: E402

from services.database.models import StandupConversationDB  # noqa: E402
from services.domain.models import (  # noqa: E402
    ConversationTurn,
    StandupConversation,
    StandupItem,
    StandupPartialCapture,
)
from services.shared_types import StandupConversationState  # noqa: E402
from services.standup.conversation_manager import (  # noqa: E402
    InvalidStateTransitionError,
    StandupConversationManager,
)

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def manager():
    """StandupConversationManager wired to in-memory SQLite.

    Each manager call opens a fresh session via the overridden
    `_session_scope` — mirrors the production AsyncSessionFactory shape
    but bound to a per-test SQLite engine.
    """
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: StandupConversationDB.__table__.create(
                sync_conn, checkfirst=True
            )
        )
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @asynccontextmanager
    async def _session_scope():
        async with SessionLocal() as s:
            try:
                yield s
                await s.commit()
            except Exception:
                await s.rollback()
                raise

    mgr = StandupConversationManager()
    mgr._session_scope = _session_scope  # override staticmethod with test scope
    yield mgr
    await engine.dispose()


# ---------------------------------------------------------------------------
# Enum + dataclass surface (no DB needed)
# ---------------------------------------------------------------------------


class TestStandupConversationState:
    def test_enum_has_all_states(self):
        states = [s.value for s in StandupConversationState]
        assert "initiated" in states
        assert "gathering_preferences" in states
        assert "gathering_yesterday" in states  # #900
        assert "gathering_today" in states  # #900
        assert "gathering_blockers" in states  # #900
        assert "generating" in states
        assert "refining" in states
        assert "finalizing" in states
        assert "complete" in states
        assert "abandoned" in states
        assert "suspended" in states

    def test_enum_count(self):
        # 8 base states + 3 new gathering states (#900 Phase 1) = 11
        assert len(StandupConversationState) == 11


class TestStandupConversation:
    def test_default_state_is_initiated(self):
        conv = StandupConversation(session_id="test", user_id="user1")
        assert conv.state == StandupConversationState.INITIATED
        assert conv.previous_state is None

    def test_generates_unique_id(self):
        conv1 = StandupConversation(session_id="test", user_id="user1")
        conv2 = StandupConversation(session_id="test", user_id="user1")
        assert conv1.id != conv2.id


# ---------------------------------------------------------------------------
# Lifecycle: create / get / find
# ---------------------------------------------------------------------------


class TestConversationLifecycle:
    async def test_create_persists_and_returns(self, manager):
        conv = await manager.create_conversation(
            session_id="session1",
            user_id="user1",
            initial_context={"source": "test"},
        )
        assert conv.session_id == "session1"
        assert conv.user_id == "user1"
        assert conv.state == StandupConversationState.INITIATED
        assert conv.context == {"source": "test"}

        # Round-trip from DB
        fetched = await manager.get_conversation(conv.id)
        assert fetched is not None
        assert fetched.id == conv.id
        assert fetched.context == {"source": "test"}

    async def test_create_without_context(self, manager):
        conv = await manager.create_conversation(session_id="s", user_id="u")
        assert conv.context == {}

    async def test_create_requires_user_id(self, manager):
        with pytest.raises(ValueError, match="user_id is required"):
            await manager.create_conversation(session_id="s", user_id="")

    async def test_get_conversation_not_found(self, manager):
        result = await manager.get_conversation("nonexistent")
        assert result is None

    async def test_get_by_session_returns_active(self, manager):
        conv = await manager.create_conversation("session1", "user1")
        found = await manager.get_conversation_by_session("session1")
        assert found is not None
        assert found.id == conv.id

    async def test_get_by_session_excludes_complete(self, manager):
        conv = await manager.create_conversation("session1", "user1")
        await manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await manager.transition_state(conv.id, StandupConversationState.FINALIZING)
        await manager.transition_state(conv.id, StandupConversationState.COMPLETE)

        found = await manager.get_conversation_by_session("session1")
        assert found is None

    async def test_get_by_session_excludes_abandoned(self, manager):
        conv = await manager.create_conversation("session1", "user1")
        await manager.transition_state(conv.id, StandupConversationState.ABANDONED)

        found = await manager.get_conversation_by_session("session1")
        assert found is None

    async def test_get_by_session_excludes_suspended_by_default(self, manager):
        conv = await manager.create_conversation("session1", "user1")
        await manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        found = await manager.get_conversation_by_session("session1")
        assert found is None

    async def test_get_by_session_includes_suspended_when_requested(self, manager):
        conv = await manager.create_conversation("session1", "user1")
        await manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        found = await manager.get_conversation_by_session(
            "session1", include_suspended=True
        )
        assert found is not None
        assert found.id == conv.id

    async def test_get_by_user(self, manager):
        conv = await manager.create_conversation("session1", "alice")
        found = await manager.get_conversation_by_user("alice")
        assert found is not None
        assert found.id == conv.id

    async def test_get_by_user_isolates_users(self, manager):
        await manager.create_conversation("s1", "alice")
        bob_found = await manager.get_conversation_by_user("bob")
        assert bob_found is None

    async def test_get_suspended_for_user_returns_only_suspended(self, manager):
        conv = await manager.create_conversation("s1", "alice")
        await manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        suspended = await manager.get_suspended_for_user("alice")
        assert suspended is not None
        assert suspended.id == conv.id

    async def test_get_suspended_for_user_skips_active(self, manager):
        await manager.create_conversation("s1", "alice")
        suspended = await manager.get_suspended_for_user("alice")
        assert suspended is None


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


class TestStateTransitions:
    @pytest_asyncio.fixture
    async def conversation(self, manager):
        return await manager.create_conversation("s1", "u1")

    async def test_initiated_to_gathering(self, manager, conversation):
        result = await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_PREFERENCES
        )
        assert result.state == StandupConversationState.GATHERING_PREFERENCES
        assert result.previous_state == StandupConversationState.INITIATED

    async def test_initiated_to_generating(self, manager, conversation):
        result = await manager.transition_state(
            conversation.id, StandupConversationState.GENERATING
        )
        assert result.state == StandupConversationState.GENERATING

    async def test_initiated_to_abandoned(self, manager, conversation):
        result = await manager.transition_state(
            conversation.id, StandupConversationState.ABANDONED
        )
        assert result.state == StandupConversationState.ABANDONED

    async def test_initiated_to_suspended(self, manager, conversation):
        result = await manager.transition_state(
            conversation.id, StandupConversationState.SUSPENDED
        )
        assert result.state == StandupConversationState.SUSPENDED

    async def test_gathering_to_generating(self, manager, conversation):
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_PREFERENCES
        )
        result = await manager.transition_state(
            conversation.id, StandupConversationState.GENERATING
        )
        assert result.state == StandupConversationState.GENERATING

    async def test_generating_to_refining(self, manager, conversation):
        await manager.transition_state(
            conversation.id, StandupConversationState.GENERATING
        )
        result = await manager.transition_state(
            conversation.id, StandupConversationState.REFINING
        )
        assert result.state == StandupConversationState.REFINING

    async def test_generating_to_finalizing(self, manager, conversation):
        await manager.transition_state(
            conversation.id, StandupConversationState.GENERATING
        )
        result = await manager.transition_state(
            conversation.id, StandupConversationState.FINALIZING
        )
        assert result.state == StandupConversationState.FINALIZING

    async def test_refining_to_generating(self, manager, conversation):
        await manager.transition_state(
            conversation.id, StandupConversationState.GENERATING
        )
        await manager.transition_state(
            conversation.id, StandupConversationState.REFINING
        )
        result = await manager.transition_state(
            conversation.id, StandupConversationState.GENERATING
        )
        assert result.state == StandupConversationState.GENERATING

    async def test_full_path_to_complete(self, manager, conversation):
        await manager.transition_state(
            conversation.id, StandupConversationState.GENERATING
        )
        await manager.transition_state(
            conversation.id, StandupConversationState.FINALIZING
        )
        result = await manager.transition_state(
            conversation.id, StandupConversationState.COMPLETE
        )
        assert result.state == StandupConversationState.COMPLETE
        assert result.completed_at is not None

    async def test_suspended_to_initiated(self, manager, conversation):
        await manager.transition_state(
            conversation.id, StandupConversationState.SUSPENDED
        )
        result = await manager.transition_state(
            conversation.id, StandupConversationState.INITIATED
        )
        assert result.state == StandupConversationState.INITIATED

    async def test_suspended_to_abandoned(self, manager, conversation):
        await manager.transition_state(
            conversation.id, StandupConversationState.SUSPENDED
        )
        result = await manager.transition_state(
            conversation.id, StandupConversationState.ABANDONED
        )
        assert result.state == StandupConversationState.ABANDONED

    async def test_invalid_transition_raises(self, manager, conversation):
        with pytest.raises(InvalidStateTransitionError) as exc_info:
            await manager.transition_state(
                conversation.id, StandupConversationState.COMPLETE
            )
        assert "Cannot transition" in str(exc_info.value)

    async def test_transition_unknown_conversation_raises_keyerror(self, manager):
        with pytest.raises(KeyError):
            await manager.transition_state(
                "nonexistent", StandupConversationState.GENERATING
            )

    async def test_terminal_states_have_no_outbound_transitions(
        self, manager, conversation
    ):
        await manager.transition_state(
            conversation.id, StandupConversationState.ABANDONED
        )
        with pytest.raises(InvalidStateTransitionError):
            await manager.transition_state(
                conversation.id, StandupConversationState.GENERATING
            )


# ---------------------------------------------------------------------------
# #900 Phase 1: 3-part gathering state machine
# ---------------------------------------------------------------------------


class TestThreePartGatheringTransitions:
    """3-part flow: INITIATED → GATHERING_YESTERDAY → GATHERING_TODAY →
    GATHERING_BLOCKERS → GENERATING."""

    @pytest_asyncio.fixture
    async def conversation(self, manager):
        return await manager.create_conversation("s1", "u1")

    async def test_initiated_to_gathering_yesterday(self, manager, conversation):
        result = await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_YESTERDAY
        )
        assert result.state == StandupConversationState.GATHERING_YESTERDAY
        assert result.previous_state == StandupConversationState.INITIATED

    async def test_yesterday_to_today(self, manager, conversation):
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_YESTERDAY
        )
        result = await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_TODAY
        )
        assert result.state == StandupConversationState.GATHERING_TODAY

    async def test_today_to_blockers(self, manager, conversation):
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_YESTERDAY
        )
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_TODAY
        )
        result = await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_BLOCKERS
        )
        assert result.state == StandupConversationState.GATHERING_BLOCKERS

    async def test_blockers_to_generating(self, manager, conversation):
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_YESTERDAY
        )
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_TODAY
        )
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_BLOCKERS
        )
        result = await manager.transition_state(
            conversation.id, StandupConversationState.GENERATING
        )
        assert result.state == StandupConversationState.GENERATING

    async def test_yesterday_early_completion_to_generating(self, manager, conversation):
        """User signals "skip rest" while gathering yesterday — jump to GENERATING."""
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_YESTERDAY
        )
        result = await manager.transition_state(
            conversation.id, StandupConversationState.GENERATING
        )
        assert result.state == StandupConversationState.GENERATING

    async def test_today_early_completion_to_generating(self, manager, conversation):
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_YESTERDAY
        )
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_TODAY
        )
        result = await manager.transition_state(
            conversation.id, StandupConversationState.GENERATING
        )
        assert result.state == StandupConversationState.GENERATING

    async def test_each_gathering_state_can_suspend(self, manager, conversation):
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_YESTERDAY
        )
        await manager.transition_state(
            conversation.id, StandupConversationState.SUSPENDED
        )
        # Resume back to INITIATED
        await manager.transition_state(
            conversation.id, StandupConversationState.INITIATED
        )
        # Re-enter gathering
        result = await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_YESTERDAY
        )
        assert result.state == StandupConversationState.GATHERING_YESTERDAY

    async def test_each_gathering_state_can_abandon(self, manager, conversation):
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_YESTERDAY
        )
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_TODAY
        )
        result = await manager.transition_state(
            conversation.id, StandupConversationState.ABANDONED
        )
        assert result.state == StandupConversationState.ABANDONED

    async def test_blockers_cannot_skip_back_to_yesterday(self, manager, conversation):
        """No backward transitions; gathering moves forward only."""
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_YESTERDAY
        )
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_TODAY
        )
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_BLOCKERS
        )
        with pytest.raises(InvalidStateTransitionError):
            await manager.transition_state(
                conversation.id, StandupConversationState.GATHERING_YESTERDAY
            )

    async def test_yesterday_cannot_skip_to_blockers(self, manager, conversation):
        """No skipping the middle state; flow is strictly sequential."""
        await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_YESTERDAY
        )
        with pytest.raises(InvalidStateTransitionError):
            await manager.transition_state(
                conversation.id, StandupConversationState.GATHERING_BLOCKERS
            )

    async def test_legacy_preference_path_still_works(self, manager, conversation):
        """INITIATED → GATHERING_PREFERENCES path preserved (legacy flow)."""
        result = await manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_PREFERENCES
        )
        assert result.state == StandupConversationState.GATHERING_PREFERENCES
        # And legacy GATHERING_PREFERENCES → GENERATING still works
        result = await manager.transition_state(
            conversation.id, StandupConversationState.GENERATING
        )
        assert result.state == StandupConversationState.GENERATING


# ---------------------------------------------------------------------------
# Turns
# ---------------------------------------------------------------------------


class TestTurnManagement:
    @pytest_asyncio.fixture
    async def conversation(self, manager):
        return await manager.create_conversation("s1", "u1")

    async def test_add_turn(self, manager, conversation):
        turn = await manager.add_turn(
            conversation.id,
            user_message="hello",
            assistant_response="hi back",
            intent="greeting",
            metadata={"foo": "bar"},
        )
        assert isinstance(turn, ConversationTurn)
        assert turn.turn_number == 1
        assert turn.user_message == "hello"

    async def test_turns_persist(self, manager, conversation):
        await manager.add_turn(
            conversation.id, user_message="first", assistant_response="r1"
        )
        await manager.add_turn(
            conversation.id, user_message="second", assistant_response="r2"
        )

        fetched = await manager.get_conversation(conversation.id)
        assert len(fetched.turns) == 2
        assert fetched.turns[0].user_message == "first"
        assert fetched.turns[1].user_message == "second"
        assert fetched.turns[1].turn_number == 2

    async def test_turns_trim_at_max_history(self, manager, conversation):
        # Add MAX_TURN_HISTORY + 2 turns
        for i in range(StandupConversationManager.MAX_TURN_HISTORY + 2):
            await manager.add_turn(
                conversation.id,
                user_message=f"u{i}",
                assistant_response=f"r{i}",
            )

        fetched = await manager.get_conversation(conversation.id)
        assert len(fetched.turns) == StandupConversationManager.MAX_TURN_HISTORY

    async def test_add_turn_unknown_conversation_raises_keyerror(self, manager):
        with pytest.raises(KeyError):
            await manager.add_turn(
                "nonexistent", user_message="x", assistant_response="y"
            )


# ---------------------------------------------------------------------------
# Preferences + content
# ---------------------------------------------------------------------------


class TestPreferencesAndContent:
    @pytest_asyncio.fixture
    async def conversation(self, manager):
        return await manager.create_conversation("s1", "u1")

    async def test_update_preferences_merges(self, manager, conversation):
        await manager.update_preferences(conversation.id, {"focus": "github"})
        await manager.update_preferences(conversation.id, {"length": "brief"})

        fetched = await manager.get_conversation(conversation.id)
        assert fetched.preferences == {"focus": "github", "length": "brief"}

    async def test_set_standup_content(self, manager, conversation):
        await manager.set_standup_content(conversation.id, "first version")
        fetched = await manager.get_conversation(conversation.id)
        assert fetched.current_standup == "first version"
        assert fetched.standup_versions == []

    async def test_set_standup_content_versions_previous(self, manager, conversation):
        await manager.set_standup_content(conversation.id, "v1")
        await manager.set_standup_content(conversation.id, "v2")
        await manager.set_standup_content(conversation.id, "v3")

        fetched = await manager.get_conversation(conversation.id)
        assert fetched.current_standup == "v3"
        assert fetched.standup_versions == ["v1", "v2"]


# ---------------------------------------------------------------------------
# #900 Phase 2: partial_capture persistence + parsing helpers
# ---------------------------------------------------------------------------


class TestPartialCapturePersistence:
    @pytest_asyncio.fixture
    async def conversation(self, manager):
        return await manager.create_conversation("s1", "u1")

    async def test_default_partial_capture_is_empty(self, manager, conversation):
        fetched = await manager.get_conversation(conversation.id)
        assert fetched.partial_capture is not None
        assert fetched.partial_capture.is_empty()

    async def test_update_partial_capture_persists(self, manager, conversation):
        capture = StandupPartialCapture(
            yesterday=[StandupItem(display="shipped #1052", source="user")],
            today=[StandupItem(display="start #900", source="user")],
            blockers=[],
        )
        await manager.update_partial_capture(conversation.id, capture)

        fetched = await manager.get_conversation(conversation.id)
        assert len(fetched.partial_capture.yesterday) == 1
        assert fetched.partial_capture.yesterday[0].display == "shipped #1052"
        assert len(fetched.partial_capture.today) == 1
        assert fetched.partial_capture.blockers == []

    async def test_update_partial_capture_unknown_raises_keyerror(self, manager):
        with pytest.raises(KeyError):
            await manager.update_partial_capture(
                "nonexistent", StandupPartialCapture()
            )

    async def test_partial_capture_round_trip_preserves_item_metadata(
        self, manager, conversation
    ):
        capture = StandupPartialCapture(
            yesterday=[
                StandupItem(
                    display="merged audit cascade",
                    source="commit",
                    lifecycle_state="GROWING",
                    icon="✅",
                )
            ],
            today=[],
            blockers=[],
        )
        await manager.update_partial_capture(conversation.id, capture)

        fetched = await manager.get_conversation(conversation.id)
        item = fetched.partial_capture.yesterday[0]
        assert item.source == "commit"
        assert item.lifecycle_state == "GROWING"
        assert item.icon == "✅"


class TestParsingHelpers:
    """#900 Phase 2: parse helper + skip-signal detection (handler-level)."""

    def test_skip_signals_match(self):
        from services.standup.conversation_handler import _is_skip_signal

        assert _is_skip_signal("skip")
        assert _is_skip_signal("nothing")
        assert _is_skip_signal("n/a")
        assert _is_skip_signal("none")
        assert _is_skip_signal("no")
        assert _is_skip_signal("nope")
        assert _is_skip_signal("no blockers")
        assert _is_skip_signal("nothing today")
        assert _is_skip_signal("")  # empty string treated as skip

    def test_skip_signals_do_not_match_real_content(self):
        from services.standup.conversation_handler import _is_skip_signal

        assert not _is_skip_signal("shipped #1052")
        assert not _is_skip_signal("planning to write tests")
        assert not _is_skip_signal("blocker: waiting on review")

    def test_parse_items_single_line(self):
        from services.standup.conversation_handler import _parse_items_from_message

        items = _parse_items_from_message("shipped #1052")
        assert len(items) == 1
        assert items[0].display == "shipped #1052"
        assert items[0].source == "user"

    def test_parse_items_multiline(self):
        from services.standup.conversation_handler import _parse_items_from_message

        items = _parse_items_from_message("shipped #1052\nstarted #900\n")
        assert len(items) == 2
        assert items[0].display == "shipped #1052"
        assert items[1].display == "started #900"

    def test_parse_items_strips_bullet_markers(self):
        from services.standup.conversation_handler import _parse_items_from_message

        items = _parse_items_from_message("- shipped #1052\n* started #900\n• fixed #1053")
        assert len(items) == 3
        assert items[0].display == "shipped #1052"
        assert items[1].display == "started #900"
        assert items[2].display == "fixed #1053"

    def test_parse_items_skips_empty_lines(self):
        from services.standup.conversation_handler import _parse_items_from_message

        items = _parse_items_from_message("\n\nshipped\n   \n\nfixed\n")
        assert len(items) == 2

    def test_parse_items_empty_message_returns_empty(self):
        from services.standup.conversation_handler import _parse_items_from_message

        assert _parse_items_from_message("") == []
        assert _parse_items_from_message("   \n  \n") == []


# ---------------------------------------------------------------------------
# Resume flow (#888 + #1052 bind_session_id)
# ---------------------------------------------------------------------------


class TestResumeFlow:
    async def test_bind_session_id_persists(self, manager):
        conv = await manager.create_conversation("session-old", "u1")
        await manager.bind_session_id(conv.id, "session-new")

        # Resume offer can find via new session_id
        found = await manager.get_conversation_by_session("session-new")
        assert found is not None
        assert found.id == conv.id

    async def test_bind_session_id_unknown_raises_keyerror(self, manager):
        with pytest.raises(KeyError):
            await manager.bind_session_id("nonexistent", "any-session")


# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------


class TestCleanup:
    async def test_cleanup_removes_stale_non_complete(self, manager):
        # Create a stale (older than max_age_minutes) non-COMPLETE conv
        stale = await manager.create_conversation("s1", "u1")
        async with manager._session_scope() as session:
            from sqlalchemy import update

            await session.execute(
                update(StandupConversationDB)
                .where(StandupConversationDB.id == stale.id)
                .values(updated_at=datetime.now() - timedelta(hours=2))
            )

        removed = await manager.cleanup_expired(max_age_minutes=60)
        assert removed == 1

        gone = await manager.get_conversation(stale.id)
        assert gone is None

    async def test_cleanup_preserves_complete(self, manager):
        conv = await manager.create_conversation("s1", "u1")
        await manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await manager.transition_state(conv.id, StandupConversationState.FINALIZING)
        await manager.transition_state(conv.id, StandupConversationState.COMPLETE)

        # Backdate updated_at to make it "stale"
        async with manager._session_scope() as session:
            from sqlalchemy import update

            await session.execute(
                update(StandupConversationDB)
                .where(StandupConversationDB.id == conv.id)
                .values(updated_at=datetime.now() - timedelta(hours=2))
            )

        removed = await manager.cleanup_expired(max_age_minutes=60)
        assert removed == 0

        kept = await manager.get_conversation(conv.id)
        assert kept is not None

    async def test_cleanup_skips_recent(self, manager):
        await manager.create_conversation("s1", "u1")
        removed = await manager.cleanup_expired(max_age_minutes=60)
        assert removed == 0
