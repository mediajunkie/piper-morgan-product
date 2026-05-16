"""End-to-end regression tests for #1079 — /standup multi-turn conversation state.

Before the fix, Turn 2 of a /standup conversation (any of the 3 documented
branches: "quick" / "detailed" / "no") would never reach the standup handler.
The conversation was being lost because:

1. `StandupConversationManager._session_scope()` opened a session via
   `AsyncSessionFactory.session_scope()`, which is a session-lifecycle-only
   context manager that does NOT commit on success. `repo.add(conversation)`
   only flushed, then the session closed without commit → conversation
   never persisted → `get_conversation_by_session` returned None on Turn 2 →
   `StandupProcessAdapter.check_active` returned False → registry didn't
   route Turn 2 to the standup handler.

2. Secondary: `StandupProcessAdapter.check_active` and several
   `conversation_manager.transition_state` writes used naive
   `datetime.now()` against tz-aware DB columns — timeout-elapsed
   subtraction raised `TypeError: can't subtract offset-naive and
   offset-aware datetimes`, which the registry caught and treated as
   "process not active" → Turn 2 fell through to classification.

Run 8 canonical retest (May 13) surfaced this via Q49/Q149/Q150 FAIL.
These tests cover all 3 documented branches end-to-end.
"""

import os
import uuid

import pytest

# Default to local Postgres dev port if not set (PM's standing convention).
os.environ.setdefault("POSTGRES_PORT", "5433")


@pytest.fixture(scope="module")
async def initialized_services():
    """One-time setup: LLM domain service + container + process registry."""
    from services.container import ServiceContainer
    from services.domain.llm_domain_service import LLMDomainService
    from services.process import register_default_processes

    llm = LLMDomainService()
    await llm.initialize()
    container = ServiceContainer()
    container._registry.register("llm", llm)
    container._initialized = True
    register_default_processes()

    yield  # Tests run here; no teardown needed for these read+write ops


@pytest.fixture
def fresh_session_id():
    """Unique session id per test to avoid cross-test conversation reuse."""
    return f"test-1079-{uuid.uuid4().hex[:8]}"


@pytest.fixture
def test_user_id():
    """Stable test user id for the standup flow."""
    return "11111111-1111-1111-1111-111111111111"


@pytest.fixture
async def intent_service(initialized_services):
    from services.intent.intent_service import IntentService

    return IntentService()


class TestStandupMultiTurnState:
    """All 3 documented /standup branches: quick / detailed / no."""

    @pytest.mark.asyncio
    async def test_q49_quick_path_reaches_standup_handler(
        self, intent_service, fresh_session_id, test_user_id
    ):
        """Q49 — /standup → 'quick' should produce a one-shot LLM standup."""
        r1 = await intent_service.process_intent(
            "/standup", session_id=fresh_session_id, user_id=test_user_id
        )
        assert r1.intent_data["action"] == "standup_started", (
            f"Expected standup_started on Turn 1; got {r1.intent_data.get('action')}"
        )

        r2 = await intent_service.process_intent(
            "quick", session_id=fresh_session_id, user_id=test_user_id
        )
        assert r2.intent_data["action"] == "standup_conversation_turn", (
            f"Turn 2 should route through the standup process; "
            f"got action={r2.intent_data.get('action')}, "
            f"msg={r2.message[:100]!r}"
        )

    @pytest.mark.asyncio
    async def test_q149_detailed_path_reaches_standup_handler(
        self, intent_service, fresh_session_id, test_user_id
    ):
        """Q149 — /standup → 'detailed' should start the 3-part collection flow."""
        await intent_service.process_intent(
            "/standup", session_id=fresh_session_id, user_id=test_user_id
        )
        r2 = await intent_service.process_intent(
            "detailed", session_id=fresh_session_id, user_id=test_user_id
        )
        assert r2.intent_data["action"] == "standup_conversation_turn"
        # 3-part flow starts with the yesterday question
        assert "yesterday" in r2.message.lower(), (
            f"Expected 3-part flow start (yesterday question); got {r2.message[:120]!r}"
        )

    @pytest.mark.asyncio
    async def test_q150_no_path_acknowledges_cancellation(
        self, intent_service, fresh_session_id, test_user_id
    ):
        """Q150 — /standup → 'no' should acknowledge cancellation, not pivot."""
        await intent_service.process_intent(
            "/standup", session_id=fresh_session_id, user_id=test_user_id
        )
        r2 = await intent_service.process_intent(
            "no", session_id=fresh_session_id, user_id=test_user_id
        )
        assert r2.intent_data["action"] == "standup_conversation_turn"
        # ABANDONED state acknowledgement
        assert "no problem" in r2.message.lower(), (
            f"Expected cancellation acknowledgement; got {r2.message[:120]!r}"
        )


class TestStandupConversationPersistence:
    """The core fix: conversation actually persists across the session boundary."""

    @pytest.mark.asyncio
    async def test_conversation_findable_after_turn_1(
        self, intent_service, fresh_session_id, test_user_id
    ):
        """After Turn 1, get_conversation_by_session must find the conversation."""
        from services.conversation.conversation_handler import _get_standup_components

        await intent_service.process_intent(
            "/standup", session_id=fresh_session_id, user_id=test_user_id
        )

        manager, _ = _get_standup_components()
        conv = await manager.get_conversation_by_session(fresh_session_id)
        assert conv is not None, (
            "Conversation should be persisted + findable by session_id after Turn 1. "
            "If None, _session_scope() may have reverted to session_scope() (no-commit) "
            "instead of transaction_scope() (auto-commit). See #1079."
        )
        assert str(conv.session_id) == fresh_session_id

    @pytest.mark.asyncio
    async def test_check_active_recognizes_fresh_conversation(
        self, intent_service, fresh_session_id, test_user_id
    ):
        """StandupProcessAdapter.check_active should return True for the new session."""
        from services.process import get_process_registry
        from services.process.adapters import StandupProcessAdapter

        await intent_service.process_intent(
            "/standup", session_id=fresh_session_id, user_id=test_user_id
        )

        reg = get_process_registry()
        adapter = next(
            h for h in reg._handlers if isinstance(h, StandupProcessAdapter)
        )
        is_active = await adapter.check_active(test_user_id, fresh_session_id)
        assert is_active is True, (
            "check_active must recognize fresh standup conversations. "
            "If False, either the conversation didn't persist (commit bug) or "
            "the timeout-elapsed check tripped a tz-aware/naive datetime "
            "subtraction error. See #1079."
        )
