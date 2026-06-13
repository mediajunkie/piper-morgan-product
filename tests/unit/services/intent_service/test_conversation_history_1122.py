"""#1122 floor-path antecedent fix — conversation-history plumbing tests.

Root cause being guarded: the in-memory conversation registry was the
de-facto history source for the floor AND slot-filling, but turns were
recorded on only one of five floor paths (user message only) and never
hydrated from the DB — so "Recent conversation" was empty and antecedents
("the doc", "that one") could not bind. Two slot-filling sites additionally
carried a positional `turns[:-1]` exclusion that dropped the latest prior
turn whenever the current turn wasn't recorded (i.e., always, on that path).

These tests pin the three mechanisms of the fix:
1. build_recent_history — shared builder; in-flight turn excluded by
   response-is-None, not list position.
2. hydrate_turns_from_db — backfills the in-memory window from persisted
   turns (restart / 30-min-prune / resumed conversation).
3. process_intent outer seam — records the in-flight turn for EVERY path
   and sets its response afterward (no more older-turn corruption).
"""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from services.intent_service.conversation_context import (
    build_recent_history,
    clear_context,
    get_or_create_context,
    hydrate_turns_from_db,
)


def _fresh_session():
    sid = f"t1122-{uuid4()}"
    uid = str(uuid4())
    return sid, uid


class TestBuildRecentHistory:
    def test_empty_session_returns_empty(self):
        sid, uid = _fresh_session()
        assert build_recent_history(sid, uid) == []

    def test_none_session_returns_empty(self):
        assert build_recent_history(None) == []
        assert build_recent_history("") == []

    def test_completed_turns_render_as_role_content_pairs(self):
        sid, uid = _fresh_session()
        ctx = get_or_create_context(sid, user_id=uid)
        t = ctx.add_turn(message="Update the Piper Morgan test page")
        t.response = "Found it — what should change?"
        history = build_recent_history(sid, uid)
        assert history == [
            {"role": "user", "content": "Update the Piper Morgan test page"},
            {"role": "assistant", "content": "Found it — what should change?"},
        ]
        clear_context(sid, uid)

    def test_in_flight_turn_excluded_by_response_not_position(self):
        """The #1122 regression core: the prior turn must SURVIVE the
        exclusion when the in-flight turn is present (old `[:-1]` dropped
        it whenever the current turn wasn't recorded)."""
        sid, uid = _fresh_session()
        ctx = get_or_create_context(sid, user_id=uid)
        t1 = ctx.add_turn(message="Update the test page")
        t1.response = "Found it."
        ctx.add_turn(message="Add a paragraph to the doc")  # in-flight
        history = build_recent_history(sid, uid)
        assert {"role": "user", "content": "Update the test page"} in history
        assert {"role": "assistant", "content": "Found it."} in history
        assert all(t["content"] != "Add a paragraph to the doc" for t in history)
        clear_context(sid, uid)

    def test_exclude_in_flight_false_includes_current(self):
        sid, uid = _fresh_session()
        ctx = get_or_create_context(sid, user_id=uid)
        ctx.add_turn(message="hello")  # in-flight
        history = build_recent_history(sid, uid, exclude_in_flight=False)
        assert history == [{"role": "user", "content": "hello"}]
        clear_context(sid, uid)

    def test_max_turns_caps_window(self):
        sid, uid = _fresh_session()
        ctx = get_or_create_context(sid, user_id=uid)
        for i in range(9):
            t = ctx.add_turn(message=f"msg {i}")
            t.response = f"resp {i}"
        history = build_recent_history(sid, uid, max_turns=2)
        assert len(history) == 4  # 2 turns x (user + assistant)
        assert history[0]["content"] == "msg 7"
        clear_context(sid, uid)


class TestHydrateTurnsFromDb:
    @pytest.mark.asyncio
    async def test_backfills_empty_window_from_manager(self):
        sid, uid = _fresh_session()
        ctx = get_or_create_context(sid, user_id=uid)
        persisted_turn = MagicMock()
        persisted_turn.user_message = "Update the roadmap doc"
        persisted_turn.assistant_response = "Which section?"
        manager = MagicMock()
        manager.get_recent_turns = AsyncMock(return_value=[persisted_turn])

        backfilled = await hydrate_turns_from_db(ctx, manager, sid)

        assert backfilled is True
        assert len(ctx.turns) == 1
        assert ctx.turns[0].message == "Update the roadmap doc"
        assert ctx.turns[0].response == "Which section?"
        # and the builder now sees it (completed turn, not excluded)
        assert build_recent_history(sid, uid) == [
            {"role": "user", "content": "Update the roadmap doc"},
            {"role": "assistant", "content": "Which section?"},
        ]
        clear_context(sid, uid)

    @pytest.mark.asyncio
    async def test_noop_when_window_already_populated(self):
        sid, uid = _fresh_session()
        ctx = get_or_create_context(sid, user_id=uid)
        ctx.add_turn(message="already here")
        manager = MagicMock()
        manager.get_recent_turns = AsyncMock()

        assert await hydrate_turns_from_db(ctx, manager, sid) is False
        manager.get_recent_turns.assert_not_called()
        clear_context(sid, uid)

    @pytest.mark.asyncio
    async def test_noop_without_manager_or_persisted(self):
        sid, uid = _fresh_session()
        ctx = get_or_create_context(sid, user_id=uid)
        assert await hydrate_turns_from_db(ctx, None, sid) is False
        manager = MagicMock()
        manager.get_recent_turns = AsyncMock(return_value=[])
        assert await hydrate_turns_from_db(ctx, manager, sid) is False
        clear_context(sid, uid)

    @pytest.mark.asyncio
    async def test_manager_exception_is_swallowed(self):
        sid, uid = _fresh_session()
        ctx = get_or_create_context(sid, user_id=uid)
        manager = MagicMock()
        manager.get_recent_turns = AsyncMock(side_effect=RuntimeError("redis down"))
        assert await hydrate_turns_from_db(ctx, manager, sid) is False
        assert ctx.turns == []
        clear_context(sid, uid)


class TestOuterSeamRecording:
    """The outer process_intent must record the in-flight turn for every
    path and set its response afterward — including paths that never touch
    the floor (canonical/structured handlers)."""

    @pytest.mark.asyncio
    async def test_turn_recorded_and_response_set_for_any_path(self):
        from services.intent.intent_service import IntentService

        sid, uid = _fresh_session()
        svc = IntentService.__new__(IntentService)  # no full init; outer flow only
        svc.conversation_manager = None
        svc.logger = MagicMock()
        # _process_intent_internal stands in for ANY handler path (incl.
        # canonical routes that never call the floor or add_turn).
        internal_result = MagicMock()
        internal_result.success = True
        internal_result.message = "Done — added the paragraph."
        svc._process_intent_internal = AsyncMock(return_value=internal_result)
        svc._save_conversation_turn = AsyncMock()
        svc._observe_action_verb = MagicMock()

        result = await IntentService.process_intent(
            svc, message="Add a paragraph to the doc", session_id=sid, user_id=uid
        )

        assert result is internal_result
        ctx = get_or_create_context(sid, user_id=uid)
        assert len(ctx.turns) == 1
        assert ctx.turns[0].message == "Add a paragraph to the doc"
        # #922 response write landed on the CURRENT turn (no corruption)
        assert ctx.turns[0].response == "Done — added the paragraph."
        clear_context(sid, uid)

    @pytest.mark.asyncio
    async def test_prior_turn_response_not_corrupted(self):
        """Regression for the #922 write: a completed prior turn must keep
        its own response when the next message routes through a path that
        (before #1122) never recorded its turn."""
        from services.intent.intent_service import IntentService

        sid, uid = _fresh_session()
        ctx = get_or_create_context(sid, user_id=uid)
        t1 = ctx.add_turn(message="Update the test page")
        t1.response = "Found it — what should change?"

        svc = IntentService.__new__(IntentService)
        svc.conversation_manager = None
        svc.logger = MagicMock()
        internal_result = MagicMock()
        internal_result.success = True
        internal_result.message = "Added the paragraph."
        svc._process_intent_internal = AsyncMock(return_value=internal_result)
        svc._save_conversation_turn = AsyncMock()
        svc._observe_action_verb = MagicMock()

        await IntentService.process_intent(
            svc, message="Add a paragraph to the doc", session_id=sid, user_id=uid
        )

        ctx = get_or_create_context(sid, user_id=uid)
        assert [t.message for t in ctx.turns] == [
            "Update the test page",
            "Add a paragraph to the doc",
        ]
        assert ctx.turns[0].response == "Found it — what should change?"  # intact
        assert ctx.turns[1].response == "Added the paragraph."
        # the floor/slot-filling history for the NEXT turn sees both turns
        history = build_recent_history(sid, uid)
        assert len(history) == 4
        clear_context(sid, uid)

    @pytest.mark.asyncio
    async def test_repeated_identical_message_records_new_turn(self):
        """'yes' then 'yes' again: the second must record (the dedupe guard
        only skips a same-message turn still awaiting its response)."""
        from services.intent.intent_service import IntentService

        sid, uid = _fresh_session()
        svc = IntentService.__new__(IntentService)
        svc.conversation_manager = None
        svc.logger = MagicMock()
        internal_result = MagicMock()
        internal_result.success = True
        internal_result.message = "ok"
        svc._process_intent_internal = AsyncMock(return_value=internal_result)
        svc._save_conversation_turn = AsyncMock()
        svc._observe_action_verb = MagicMock()

        await IntentService.process_intent(svc, message="yes", session_id=sid, user_id=uid)
        await IntentService.process_intent(svc, message="yes", session_id=sid, user_id=uid)

        ctx = get_or_create_context(sid, user_id=uid)
        assert [t.message for t in ctx.turns] == ["yes", "yes"]
        clear_context(sid, uid)


class TestFloorPromptAntecedentShaping:
    def test_reference_binding_block_present_with_history(self):
        from services.intent_service.conversational_floor import (
            ConversationalFloor,
            FloorContext,
        )

        floor = ConversationalFloor()
        ctx = FloorContext(
            user_message="Can you help me structure that?",
            session_id="s",
            conversation_history=[
                {"role": "user", "content": "I need to plan a stakeholder presentation"},
                {"role": "assistant", "content": "Happy to help — when is it?"},
            ],
        )
        prompt = floor._build_prompt(ctx)
        assert "Recent conversation:" in prompt
        assert "Reference binding" in prompt
        assert "stakeholder presentation" in prompt

    def test_no_binding_block_without_history(self):
        from services.intent_service.conversational_floor import (
            ConversationalFloor,
            FloorContext,
        )

        floor = ConversationalFloor()
        ctx = FloorContext(user_message="hello", session_id="s")
        prompt = floor._build_prompt(ctx)
        assert "Recent conversation:" not in prompt
        assert "Reference binding" not in prompt
