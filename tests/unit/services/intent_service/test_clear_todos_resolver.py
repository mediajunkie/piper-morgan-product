"""Clear-family build plan piece 2 (2026-10-07) — ``clear_todos``, the
RESOLVER rail entry (Arch's ruling 2026-10-06; CXO's strings, same date).

``clear_todos`` mutates nothing: it resolves the ambiguous "clear/handle/
take care of/reset" verb (the #1605 three-variant question, or the user's
stored default) against the router's ``inversion_args``, then re-enters the
action-dispatch rail as a concrete ``complete_todo`` or ``delete_todo``
Intent carrying the SAME args, via ``workflow_dispatcher.dispatch_workflow``
— never calling ``todo_handlers`` directly, so the concrete op's own gates
(consent, the #1190 enumerating confirm) run unchanged.

Layer (m-43): handler/dispatcher-level tests. ``dispatch_workflow`` and the
rail registry are REAL (registered via ``register_default_workflows``) so
the re-entry is genuinely exercised end to end through
``run_complete_todo_workflow`` / ``run_delete_todo_workflow`` and
``todo_handlers.handle_complete_todo_targets`` / ``handle_delete_todo_
targets``; only ``todo_service`` (DB), the offer store, the session
context, and the verified-inference store are mocked. No LLM, no DB.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from services.domain.models import Intent, IntentCategory, Todo
from services.intent_service import clear_todos as ct
from services.intent_service import reminder_clear as rc
from services.intent_service import todo_handlers as th
from services.intent_service import workflow_entries as we
from services.intent_service.conversation_context import NumberedList
from services.intent_service.destructive_confirm import CONFIRMED_CONTEXT_KEY
from services.intent_service.todo_handlers import (
    BATCH_COMPLETE_IDS_KEY,
    BATCH_COMPLETE_LEFT_KEY,
    BATCH_COMPLETE_TEXTS_KEY,
    TodoIntentHandlers,
)

we.register_default_workflows()  # idempotent — the rail must be populated

_NOW = datetime.now(timezone.utc)
_USER_ID = str(uuid4())


def _due(text: str, minutes_ago: int) -> Todo:
    t = Todo(text=text, priority="medium")
    t.id = str(uuid4())
    t.reminder_date = _NOW - timedelta(minutes=minutes_ago)
    t.completed = False
    return t


@pytest.fixture
def four():
    return [
        _due("check the test card again", 400),
        _due("check the test card again", 300),
        _due("review the pr", 200),
        _due("revise the pr", 100),
    ]


@pytest.fixture
def intent_service(four, monkeypatch):
    svc = MagicMock()
    th_instance = TodoIntentHandlers()
    th_instance.todo_service = AsyncMock()
    th_instance.todo_service.list_todos = AsyncMock(return_value=four)
    th_instance.todo_service.complete_todo = AsyncMock(return_value=MagicMock())
    th_instance.todo_service.delete_todo = AsyncMock(return_value=True)
    svc.todo_handlers = th_instance

    # A REAL in-memory offer store (not a dumb MagicMock): the stored-delete
    # branch PEEKS what it just armed in order to overwrite its question —
    # a mock with a fixed return value wouldn't reflect that write. Spied
    # (side_effect=) so call-count/call_args assertions still work.
    from services.intent_service.soft_invocation import WorkflowOfferService

    real_offers = WorkflowOfferService()
    offers = MagicMock(wraps=real_offers)
    offers.set_pending_offer = MagicMock(side_effect=real_offers.set_pending_offer)
    offers.peek_pending_offer = MagicMock(side_effect=real_offers.peek_pending_offer)
    offers.get_and_clear_pending_offer = MagicMock(
        side_effect=real_offers.get_and_clear_pending_offer
    )
    svc.workflow_offer_service = offers

    ctx = MagicMock()
    ctx.last_numbered_list = None
    monkeypatch.setattr(
        "services.intent_service.conversation_context.get_or_create_context",
        lambda session_id, user_id=None: ctx,
    )
    svc._session_ctx = ctx
    return svc


def _clear_intent(targets, exclude=None, message="clear my reminders"):
    args = {"targets": targets}
    if exclude is not None:
        args["exclude"] = exclude
    ctx = {"original_message": message, "inversion_args": args}
    return Intent(
        category=IntentCategory.EXECUTION,
        action="clear_todos",
        original_message=message,
        confidence=0.9,
        context=ctx,
    )


def _always_live(op: str) -> bool:
    return True


@pytest.fixture(autouse=True)
def _live_by_default(monkeypatch):
    monkeypatch.setattr(ct, "_op_is_live_eligible", _always_live)


@pytest.fixture
def no_stored(monkeypatch):
    monkeypatch.setattr(
        "services.intent_service.verified_inference.get_verified_inference",
        AsyncMock(return_value=None),
    )


def _stored(monkeypatch, value):
    monkeypatch.setattr(
        "services.intent_service.verified_inference.get_verified_inference",
        AsyncMock(return_value={"value": value}),
    )


class TestUnresolved:
    @pytest.mark.asyncio
    async def test_unresolved_strikes_the_verb_clause(self, intent_service, no_stored):
        intent = _clear_intent(["name:nonexistent reminder"])
        result = await ct.run_clear_todos(intent, "s1", _USER_ID, intent_service)
        assert result.requires_clarification is False
        assert "Tell me which one." in result.message
        # the verb-neutral tail only — never "mark it done" / "delete it" /
        # "clear it"
        for word in ("mark", "delete", "clear it"):
            assert word not in result.message
        intent_service.workflow_offer_service.set_pending_offer.assert_not_called()

    @pytest.mark.asyncio
    async def test_unresolved_with_some_picked_promises_only_what_state_holds(
        self, intent_service, no_stored, four
    ):
        intent = _clear_intent(["name:review the pr", "name:nonexistent"])
        result = await ct.run_clear_todos(intent, "s1", _USER_ID, intent_service)
        assert "Nothing has been changed. Say it again with the right name or number." in (
            result.message
        )


class TestNoStoredDefault:
    @pytest.mark.asyncio
    async def test_variant_one_with_set_and_carve_out(self, intent_service, no_stored, four):
        """RECORDED: no-stored, 3 items, with a carve-out."""
        intent = _clear_intent(["1-3"], exclude=["3"])
        intent_service._session_ctx.last_numbered_list = NumberedList(
            kind="reminders", ids=[t.id for t in four], texts=[t.text for t in four]
        )
        result = await ct.run_clear_todos(intent, "s1", _USER_ID, intent_service)
        assert result.requires_clarification is True
        assert result.message == (
            'You want to clear 2 reminders: "check the test card again" (2 items). '
            'Leaving "review the pr" and "revise the pr" as is. '
            "Before I touch these — when you say 'clear' on a reminder, do you want "
            "me to mark it done, or delete it? I'll remember for next time."
        )
        intent_service.workflow_offer_service.set_pending_offer.assert_called_once()
        _sid, offer = intent_service.workflow_offer_service.set_pending_offer.call_args.args[:2]
        assert offer["question"] == result.message
        pa = offer["pending_action"]
        assert pa["kind"] == rc.CLEAR_VERB_QUESTION_KIND
        assert pa[ct.CLEAR_TODOS_RESOLVER_MARKER] is True
        assert len(pa["clear_target_ids"]) == 2

    @pytest.mark.asyncio
    async def test_variant_one_one_item_no_carve_out_no_leaving_line(
        self, intent_service, no_stored
    ):
        only = [_due("review the pr", 100)]
        intent_service.todo_handlers.todo_service.list_todos = AsyncMock(return_value=only)
        intent = _clear_intent(["name:review the pr"])
        result = await ct.run_clear_todos(intent, "s1", _USER_ID, intent_service)
        assert result.message == (
            'You want to clear the reminder "review the pr". '
            "Before I touch these — when you say 'clear' on a reminder, do you want "
            "me to mark it done, or delete it? I'll remember for next time."
        )
        assert "Leaving" not in result.message

    @pytest.mark.asyncio
    async def test_guard_returns_none_when_either_op_not_live(
        self, intent_service, no_stored, monkeypatch
    ):
        monkeypatch.setattr(ct, "_op_is_live_eligible", lambda op: op == "complete_todo")
        intent = _clear_intent(["name:review the pr"])
        result = await ct.run_clear_todos(intent, "s1", _USER_ID, intent_service)
        assert result is None


class TestStoredDone:
    @pytest.mark.asyncio
    async def test_one_item_completes_with_disclosure(self, intent_service, monkeypatch, four):
        """RECORDED: stored = done, 1 item."""
        _stored(monkeypatch, rc.VALUE_COMPLETE)
        intent = _clear_intent(["name:review the pr"])
        result = await ct.run_clear_todos(intent, "s1", _USER_ID, intent_service)
        assert result.requires_clarification is False
        intent_service.todo_handlers.todo_service.complete_todo.assert_awaited_once()
        assert result.message.endswith(
            "That's what 'clear' has meant for you. " "Say so if you meant delete this time."
        )

    @pytest.mark.asyncio
    async def test_multi_item_confirm_is_complete_todos_own_unchanged(
        self, intent_service, monkeypatch, four
    ):
        """CXO ruling 2: 2+ or a carve-out arms complete_todo's OWN
        enumerating confirm with NO extra clause."""
        _stored(monkeypatch, rc.VALUE_COMPLETE)
        intent = _clear_intent(["1-3"])
        intent_service._session_ctx.last_numbered_list = NumberedList(
            kind="reminders", ids=[t.id for t in four], texts=[t.text for t in four]
        )
        result = await ct.run_clear_todos(intent, "s1", _USER_ID, intent_service)
        assert result.requires_clarification is True
        assert result.message == (
            'Complete 3 reminders: "check the test card again" (2 items) and '
            '"review the pr"? Leaving "revise the pr" as is. (yes/no)'
        )
        assert "clear" not in result.message.lower()
        intent_service.todo_handlers.todo_service.complete_todo.assert_not_awaited()
        _sid, offer = intent_service.workflow_offer_service.set_pending_offer.call_args.args[:2]
        bound = offer["pending_action"]["intent"]
        assert bound.context.get(ct.VIA_CLEAR_VERB_CONTEXT_KEY) == "clear"

    @pytest.mark.asyncio
    async def test_confirmed_reentry_appends_disclosure_to_the_summary(self, intent_service, four):
        """The "yes" turn to the confirm above re-enters
        handle_complete_todo_targets directly (as run_confirm_pending_
        action_workflow would), with via_clear_verb carried on the bound
        Intent's context — the summary gets the disclosure appended."""
        picked = four[:3]
        ctx = {
            "inversion_args": {"targets": []},
            CONFIRMED_CONTEXT_KEY: True,
            BATCH_COMPLETE_IDS_KEY: [t.id for t in picked],
            BATCH_COMPLETE_TEXTS_KEY: [t.text for t in picked],
            BATCH_COMPLETE_LEFT_KEY: [four[3].text],
            ct.VIA_CLEAR_VERB_CONTEXT_KEY: "clear",
        }
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message="",
            confidence=1.0,
            context=ctx,
        )
        msg, armed = await intent_service.todo_handlers.handle_complete_todo_targets(
            intent, "s1", _USER_ID, intent_service.workflow_offer_service, _USER_ID
        )
        assert armed is False
        assert msg.endswith(
            "That's what 'clear' has meant for you. Say so if you meant delete this time."
        )
        assert msg.startswith("Marked 3 reminders done:")


class TestStoredDelete:
    @pytest.mark.asyncio
    async def test_one_item_confirm_is_variant_three(self, intent_service, monkeypatch):
        """RECORDED: stored = delete, 1 item (a pool of exactly one — no
        Leaving line, CXO's D1 shape mirrored)."""
        only = [_due("review the pr", 100)]
        intent_service.todo_handlers.todo_service.list_todos = AsyncMock(return_value=only)
        _stored(monkeypatch, rc.VALUE_DELETE)
        intent = _clear_intent(["name:review the pr"])
        result = await ct.run_clear_todos(intent, "s1", _USER_ID, intent_service)
        assert result.requires_clarification is True
        assert result.message == (
            "You've set 'clear' to mean delete — " 'delete the reminder "review the pr"? (yes/no)'
        )
        intent_service.todo_handlers.todo_service.delete_todo.assert_not_awaited()
        _sid, offer = intent_service.workflow_offer_service.set_pending_offer.call_args.args[:2]
        assert offer["question"] == result.message

    @pytest.mark.asyncio
    async def test_multi_item_confirm_is_variant_three_with_leaving(
        self, intent_service, monkeypatch, four
    ):
        _stored(monkeypatch, rc.VALUE_DELETE)
        intent = _clear_intent(["1-3"], exclude=["3"])
        intent_service._session_ctx.last_numbered_list = NumberedList(
            kind="reminders", ids=[t.id for t in four], texts=[t.text for t in four]
        )
        result = await ct.run_clear_todos(intent, "s1", _USER_ID, intent_service)
        assert result.message == (
            "You've set 'clear' to mean delete — "
            'delete 2 reminders: "check the test card again" (2 items)? '
            'Leaving "review the pr" and "revise the pr" as is. (yes/no)'
        )


class TestReentryUsesDispatchWorkflowWithSameArgs:
    @pytest.mark.asyncio
    async def test_complete_reentry_carries_the_same_args(self, intent_service, monkeypatch):
        captured = {}

        async def spy(workflow_type, session_id, user_id=None, context=None, resume=False):
            captured["workflow_type"] = workflow_type
            captured["args"] = context["intent"].context.get("inversion_args")
            from services.intent.intent_service import IntentProcessingResult

            return IntentProcessingResult(
                success=True, message="stub", intent_data={}, requires_clarification=False
            )

        monkeypatch.setattr("services.intent_service.workflow_dispatcher.dispatch_workflow", spy)
        _stored(monkeypatch, rc.VALUE_COMPLETE)
        intent = _clear_intent(["name:review the pr"], exclude=["name:revise the pr"])
        await ct.run_clear_todos(intent, "s1", _USER_ID, intent_service)
        assert captured["workflow_type"] == "complete_todo"
        assert captured["args"] == {
            "targets": ["name:review the pr"],
            "exclude": ["name:revise the pr"],
        }

    @pytest.mark.asyncio
    async def test_delete_reentry_carries_the_same_args(self, intent_service, monkeypatch):
        captured = {}

        async def spy(workflow_type, session_id, user_id=None, context=None, resume=False):
            captured["workflow_type"] = workflow_type
            captured["args"] = context["intent"].context.get("inversion_args")
            from services.intent.intent_service import IntentProcessingResult

            return IntentProcessingResult(
                success=True, message="stub", intent_data={}, requires_clarification=True
            )

        monkeypatch.setattr("services.intent_service.workflow_dispatcher.dispatch_workflow", spy)
        _stored(monkeypatch, rc.VALUE_DELETE)
        intent = _clear_intent(["name:review the pr"])
        await ct.run_clear_todos(intent, "s1", _USER_ID, intent_service)
        assert captured["workflow_type"] == "delete_todo"
        assert captured["args"] == {"targets": ["name:review the pr"]}


class TestAnswerTurnReentry:
    @pytest.mark.asyncio
    async def test_answer_turn_reenters_with_the_bound_ids(self, intent_service, monkeypatch):
        captured = {}

        async def spy(workflow_type, session_id, user_id=None, context=None, resume=False):
            captured["workflow_type"] = workflow_type
            captured["targets"] = context["intent"].context["inversion_args"]["targets"]
            from services.intent.intent_service import IntentProcessingResult

            return IntentProcessingResult(
                success=True, message="Marked done.", intent_data={}, requires_clarification=False
            )

        monkeypatch.setattr("services.intent_service.workflow_dispatcher.dispatch_workflow", spy)
        monkeypatch.setattr(
            "services.intent_service.verified_inference.store_verified_inference",
            AsyncMock(return_value=True),
        )
        payload = {
            "kind": rc.CLEAR_VERB_QUESTION_KIND,
            ct.CLEAR_TODOS_RESOLVER_MARKER: True,
            "clear_target_ids": ["id-1", "id-2"],
            "clear_target_texts": ["review the pr", "revise the pr"],
            "original_message": "clear my reminders",
        }
        result = await ct.handle_clear_todos_verb_answer(
            payload, "mark them done", "s1", _USER_ID, intent_service
        )
        assert captured["workflow_type"] == "complete_todo"
        assert captured["targets"] == ["name:review the pr", "name:revise the pr"]
        assert result["message"] == "Marked done."
        assert result["intent_data"]["verb_default_stored"] == rc.VALUE_COMPLETE

    @pytest.mark.asyncio
    async def test_dispatch_entry_point_delegates_through_the_marker(
        self, intent_service, monkeypatch
    ):
        """reminder_clear._handle_verb_answer_turn's added guard delegates
        to this module ONLY when the marker is set — the ratified #1605
        code below the guard is unreached for marker-bearing payloads."""
        called = {}

        async def fake_handler(
            payload, message, session_id, user_id, intent_service, armed_question=None
        ):
            called["hit"] = True
            return {"message": "delegated", "intent_data": {}}

        monkeypatch.setattr(ct, "handle_clear_todos_verb_answer", fake_handler)
        payload = {"kind": rc.CLEAR_VERB_QUESTION_KIND, ct.CLEAR_TODOS_RESOLVER_MARKER: True}
        out = await rc._handle_verb_answer_turn(payload, "anything", "s1", _USER_ID, intent_service)
        assert called.get("hit") is True
        assert out == {"message": "delegated", "intent_data": {}}
