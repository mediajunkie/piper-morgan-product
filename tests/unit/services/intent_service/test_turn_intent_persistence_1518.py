"""#1518: conversation_turns.intent must be populated for every processed turn.

ROOT CAUSE (found 2026-08-08): the intent column, its two indexes
(idx_conversation_turns_intent, idx_conversation_turns_conv_intent), the
domain field, and the ORM from_domain/to_domain mapping have carried `intent`
since PM-034 — but the ONLY live write path never passed it:

    IntentService.process_intent
      -> IntentService._save_conversation_turn        (no intent param)
      -> ConversationManager.save_conversation_turn   (no intent param)
      -> ConversationTurn(...)                        (intent defaults to None)
      -> repo.save_turn -> from_domain -> NULL column

So every live turn persisted with intent = NULL, and routing forensics
(#1488-class) had no telemetry. These tests pin the wire-through end to end
at the service layer:

- IntentService.process_intent derives an intent label from
  result.intent_data (shape: "category:action", or bare "category" when the
  handler set no action) and passes it to the persistence path.
- ConversationManager.save_conversation_turn accepts `intent` and sets it on
  the domain ConversationTurn it persists (from_domain already maps it).
- _resolve_turn_intent_label is defensive: dicts, Intent objects, enum
  values, and garbage (None / mocks / non-dicts) all resolve sanely —
  persistence must never crash the response path over a label.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.conversation_context import (
    clear_context,
    get_or_create_context,
)
from services.shared_types import IntentCategory

_SID = "sess-1518-test"
_UID = "user-1518-test"


def _fresh_service(intent_data):
    """IntentService with the internal pipeline mocked but the REAL
    _save_conversation_turn, so the test crosses the actual persistence seam
    down to ConversationManager.save_conversation_turn."""
    svc = IntentService.__new__(IntentService)
    svc.logger = MagicMock()
    internal_result = MagicMock()
    internal_result.success = True
    internal_result.message = "Here you go."
    internal_result.intent_data = intent_data
    svc._process_intent_internal = AsyncMock(return_value=internal_result)
    svc._observe_action_verb = MagicMock()
    svc._record_session_activity = AsyncMock()
    svc.conversation_manager = MagicMock()
    svc.conversation_manager.save_conversation_turn = AsyncMock()
    return svc


class TestResolveTurnIntentLabel:
    """Regression pins on the label-derivation helper (#1518)."""

    def test_category_and_action(self):
        assert (
            IntentService._resolve_turn_intent_label(
                {"category": "query", "action": "list_issues"}
            )
            == "query:list_issues"
        )

    def test_category_only(self):
        assert IntentService._resolve_turn_intent_label({"category": "guidance"}) == "guidance"

    def test_enum_category_coerced_to_value(self):
        # Some handlers put the enum itself in intent_data — must persist
        # the lowercase .value, not "IntentCategory.QUERY".
        assert (
            IntentService._resolve_turn_intent_label(
                {"category": IntentCategory.QUERY, "action": "list_issues"}
            )
            == "query:list_issues"
        )

    def test_intent_object_source(self):
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_issue",
            confidence=1.0,
            context={},
        )
        assert IntentService._resolve_turn_intent_label(intent) == "execution:create_issue"

    def test_intent_object_no_action(self):
        intent = Intent(
            category=IntentCategory.CONVERSATION,
            action=None,
            confidence=1.0,
            context={},
        )
        assert IntentService._resolve_turn_intent_label(intent) == "conversation"

    def test_empty_or_garbage_sources_resolve_none(self):
        assert IntentService._resolve_turn_intent_label(None) is None
        assert IntentService._resolve_turn_intent_label({}) is None
        assert IntentService._resolve_turn_intent_label({"confidence": 0.9}) is None
        # Non-dict, non-Intent garbage (e.g. a MagicMock intent_data in older
        # tests) must resolve to None, never a junk string.
        assert IntentService._resolve_turn_intent_label(MagicMock()) is None
        assert IntentService._resolve_turn_intent_label("query") is None


class TestProcessIntentPersistsIntentLabel:
    """End-to-end at the service layer: a processed turn reaches
    ConversationManager.save_conversation_turn with a non-null intent."""

    @pytest.mark.asyncio
    async def test_persisted_turn_carries_category_action_label(self):
        clear_context(_SID, _UID)
        svc = _fresh_service({"category": "query", "action": "list_issues", "confidence": 0.9})

        await IntentService.process_intent(
            svc, message="what issues do I have?", session_id=_SID, user_id=_UID
        )

        save = svc.conversation_manager.save_conversation_turn
        save.assert_awaited_once()
        assert save.await_args.kwargs["intent"] == "query:list_issues"
        clear_context(_SID, _UID)

    @pytest.mark.asyncio
    async def test_persisted_turn_carries_bare_category_when_no_action(self):
        clear_context(_SID, _UID)
        svc = _fresh_service({"category": "guidance"})

        await IntentService.process_intent(
            svc, message="what should I focus on?", session_id=_SID, user_id=_UID
        )

        save = svc.conversation_manager.save_conversation_turn
        save.assert_awaited_once()
        assert save.await_args.kwargs["intent"] == "guidance"
        clear_context(_SID, _UID)

    @pytest.mark.asyncio
    async def test_falls_back_to_in_memory_turn_intent(self):
        """When a handler's intent_data has no category/action (or is not a
        dict), the floor path's in-memory turn annotation (conv_ctx.turns[-1]
        .intent, set at classification) is the fallback telemetry source."""
        clear_context(_SID, _UID)
        svc = _fresh_service({"status": "ok"})  # no category/action

        # Simulate the floor-path annotation: the in-flight turn carries the
        # classified Intent (intent_service line ~11970 sets this).
        ctx = get_or_create_context(_SID, user_id=_UID)
        turn = ctx.add_turn(message="hello there")
        turn.intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="greeting",
            confidence=1.0,
            context={},
        )

        await IntentService.process_intent(
            svc, message="hello there", session_id=_SID, user_id=_UID
        )

        save = svc.conversation_manager.save_conversation_turn
        save.assert_awaited_once()
        assert save.await_args.kwargs["intent"] == "conversation:greeting"
        clear_context(_SID, _UID)


class TestConversationManagerPersistsIntent:
    """The manager must set intent on the domain turn it persists —
    from_domain already maps turn.intent to the DB column."""

    @pytest.mark.asyncio
    async def test_domain_turn_carries_intent(self):
        from services.conversation.conversation_manager import ConversationManager

        mgr = ConversationManager()
        mgr._get_next_turn_number = AsyncMock(return_value=1)
        mgr._save_turn_to_database = AsyncMock()
        mgr._update_cached_context = AsyncMock()

        turn = await mgr.save_conversation_turn(
            conversation_id="conv-1518",
            user_message="what issues do I have?",
            assistant_response="Here are your issues.",
            intent="query:list_issues",
        )

        assert turn.intent == "query:list_issues"
        # And the SAME object goes to the DB write (from_domain maps intent).
        persisted = mgr._save_turn_to_database.await_args.args[0]
        assert persisted.intent == "query:list_issues"

    @pytest.mark.asyncio
    async def test_intent_defaults_to_none_without_regression(self):
        """Callers that don't pass intent still work (best-effort paths)."""
        from services.conversation.conversation_manager import ConversationManager

        mgr = ConversationManager()
        mgr._get_next_turn_number = AsyncMock(return_value=1)
        mgr._save_turn_to_database = AsyncMock()
        mgr._update_cached_context = AsyncMock()

        turn = await mgr.save_conversation_turn(
            conversation_id="conv-1518",
            user_message="hi",
            assistant_response="hello",
        )
        assert turn.intent is None
