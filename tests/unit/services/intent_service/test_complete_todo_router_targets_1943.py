"""#1943 — complete_todo acts on ROUTER-named targets (Arch's (a), 2026-10-05).

PM live, alpha v169 (2026-10-05): "Mark the first three complete and leave
the fourth one pending" completed ONE (the regex binder knew single
ordinals only); a verb answer carrying the list became complete_todo('it').
The ruling: the LLM decides meaning (the router emits args.targets /
args.exclude in a small mini-grammar — "1" · "1-3" · "last" · "all" ·
"name:<text>"), code decides permission (resolution against the real list,
and the #1190 confirm that ENUMERATES what will be touched and what won't).

Layer (m-43): handler-level tests with todo_service and the offer store
mocked — the resolver is pure; the confirm is asserted by the offer record
it arms and by the confirmed re-entry completing exactly the bound ids.
No LLM, no DB. The router's side is the scored corpus
(inversion-args-score-2026-10-06-anthropic.md, 13/13).
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from services.domain.models import Intent, IntentCategory, Todo
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
    CONFIRMED_CONTEXT_KEY,
)
from services.intent_service.todo_handlers import (
    BATCH_COMPLETE_IDS_KEY,
    BATCH_COMPLETE_LEFT_KEY,
    BATCH_COMPLETE_TEXTS_KEY,
    TodoIntentHandlers,
    resolve_router_targets,
)

_NOW = datetime.now(timezone.utc)


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


class TestResolveRouterTargets:
    def test_range_and_ordinals(self, four):
        picked, un = resolve_router_targets(["1-3"], four)
        assert [t.id for t in picked] == [t.id for t in four[:3]] and un == []
        picked, un = resolve_router_targets(["#2", "4"], four)
        assert [t.text for t in picked] == ["check the test card again", "revise the pr"]

    def test_last_and_all(self, four):
        assert resolve_router_targets(["last"], four)[0] == [four[3]]
        assert len(resolve_router_targets(["all"], four)[0]) == 4

    def test_name_matches_every_candidate_with_that_text(self, four):
        picked, un = resolve_router_targets(["name:check the test card again"], four)
        assert len(picked) == 2 and un == []

    def test_name_substring_unique_text(self, four):
        picked, un = resolve_router_targets(["name:revise"], four)
        assert [t.text for t in picked] == ["revise the pr"] and un == []

    def test_out_of_range_and_unknown_name_are_unresolved_never_guessed(self, four):
        picked, un = resolve_router_targets(["7", "name:water the plants"], four)
        assert picked == [] and un == ["7", "name:water the plants"]

    def test_ambiguous_name_across_different_texts_is_unresolved(self, four):
        picked, un = resolve_router_targets(["name:the pr"], four)
        assert picked == [] and un == ["name:the pr"]


def _intent(message: str, targets, exclude=None, extra=None) -> Intent:
    ctx = {"original_message": message, "inversion_args": {"targets": targets}}
    if exclude is not None:
        ctx["inversion_args"]["exclude"] = exclude
    if extra:
        ctx.update(extra)
    return Intent(
        category=IntentCategory.EXECUTION,
        action="complete_todo",
        original_message=message,
        confidence=0.95,
        context=ctx,
    )


class TestHandleCompleteTodoTargets:
    @pytest.fixture
    def handlers(self, four):
        h = TodoIntentHandlers()
        h.todo_service = AsyncMock()
        h.todo_service.list_todos = AsyncMock(return_value=four)
        # the real service returns the completed Todo (the formatter reads .text)
        h.todo_service.complete_todo = AsyncMock(
            side_effect=lambda todo_id, user_id: next(t for t in four if t.id == str(todo_id))
        )
        return h

    @pytest.fixture
    def offers(self):
        store = MagicMock()
        store.set_pending_offer = MagicMock()
        return store

    @pytest.mark.asyncio
    async def test_no_router_targets_returns_none_so_the_legacy_handler_runs(
        self, handlers, offers
    ):
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message="complete the PR review",
            context={"original_message": "complete the PR review"},
        )
        assert (
            await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u") is None
        )
        handlers.todo_service.complete_todo.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_pm_first_three_arms_the_enumerating_confirm_and_changes_nothing(
        self, handlers, offers, four
    ):
        """PM's 10-05 sentence, as the router now reads it: targets 1-3."""
        intent = _intent("Mark the first three complete and leave the fourth one pending.", ["1-3"])
        msg, armed = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        assert msg == (
            'Complete "check the test card again", "check the test card again" and '
            '"review the pr"? Leaving "revise the pr". (yes/no)'
        )
        handlers.todo_service.complete_todo.assert_not_awaited()
        offers.set_pending_offer.assert_called_once()
        _sid, offer = offers.set_pending_offer.call_args.args[:2]
        assert offer["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        assert offer["question"] == msg
        pa = offer["pending_action"]
        assert pa["kind"] == "todo_batch_complete" and pa["action"] == "complete_todo"
        assert pa["intent"].context[BATCH_COMPLETE_IDS_KEY] == [t.id for t in four[:3]]
        assert pa["intent"].context[BATCH_COMPLETE_LEFT_KEY] == ["revise the pr"]
        assert offer["decline_message"] == "Okay — I haven't changed any of them."

    @pytest.mark.asyncio
    async def test_confirmed_reentry_completes_exactly_the_bound_ids(self, handlers, offers, four):
        """The "yes" re-dispatches the bound intent — not a re-resolve."""
        intent = _intent(
            "Mark the first three complete and leave the fourth one pending.",
            ["1-3"],
            extra={
                CONFIRMED_CONTEXT_KEY: True,
                BATCH_COMPLETE_IDS_KEY: [t.id for t in four[:3]],
                BATCH_COMPLETE_TEXTS_KEY: [t.text for t in four[:3]],
                BATCH_COMPLETE_LEFT_KEY: ["revise the pr"],
            },
        )
        # the list may have shifted since the ask; the bound ids still rule
        handlers.todo_service.list_todos = AsyncMock(return_value=four[1:])
        msg, armed = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is False
        called = [
            str(c.kwargs["todo_id"]) for c in handlers.todo_service.complete_todo.call_args_list
        ]
        assert called == [t.id for t in four[:3]]
        assert msg.startswith("Marked 3 reminders done:")
        assert msg.rstrip().endswith('Left "revise the pr" as is.')
        offers.set_pending_offer.assert_not_called()

    @pytest.mark.asyncio
    async def test_two_named_targets_arm_with_both_quoted(self, handlers, offers):
        intent = _intent(
            "clear 'check the test card again' and 'review the pr' — mark them done",
            ["name:check the test card again", "name:review the pr"],
        )
        msg, armed = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        assert msg.startswith(
            'Complete "check the test card again", "check the test card again" and "review the pr"?'
        )
        assert 'Leaving "revise the pr".' in msg

    @pytest.mark.asyncio
    async def test_all_except_name_arms_with_the_exception_left(self, handlers, offers):
        intent = _intent(
            "mark all my reminders done except for 'revise the pr'",
            ["all"],
            exclude=["name:revise the pr"],
        )
        msg, armed = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        assert '"revise the pr"' not in msg.split("Leaving")[0]
        assert 'Leaving "revise the pr".' in msg

    @pytest.mark.asyncio
    async def test_single_target_completes_directly_no_question(self, handlers, offers):
        intent = _intent("complete the last one", ["last"])
        msg, armed = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is False
        handlers.todo_service.complete_todo.assert_awaited_once()
        assert "?" not in msg
        offers.set_pending_offer.assert_not_called()

    @pytest.mark.asyncio
    async def test_unresolved_target_asks_and_changes_nothing(self, handlers, offers):
        intent = _intent("mark the seventh one done", ["7"])
        msg, armed = await handlers.handle_complete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is False
        assert msg.startswith(
            'I couldn\'t find "7" in your due reminders — they are: 1. check the test card again'
        )
        assert msg.rstrip().endswith("Tell me which, and I'll mark it done.")
        assert "?" not in msg
        handlers.todo_service.complete_todo.assert_not_awaited()
        offers.set_pending_offer.assert_not_called()

    @pytest.mark.asyncio
    async def test_no_session_never_arms_an_unpoppable_offer(self, handlers, offers):
        intent = _intent("mark the first two complete", ["1-2"])
        msg, armed = await handlers.handle_complete_todo_targets(intent, None, uuid4(), offers, "u")
        assert armed is False
        offers.set_pending_offer.assert_not_called()
        handlers.todo_service.complete_todo.assert_not_awaited()
