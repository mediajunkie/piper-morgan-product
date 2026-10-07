"""Clear-family build plan piece 1 (2026-10-07) — delete_todo acts on
ROUTER-named targets, mirroring complete_todo's #1943 mechanism
(test_complete_todo_router_targets_1943.py).

CXO's ruling (2026-10-06, strings D1-D6, pinned here verbatim): delete is
DESTRUCTIVE, so every consent cell is CONFIRM — unlike complete_todo, even a
SINGLE resolved target with no carve-out arms the enumerating #1190 confirm
rather than completing in the same turn. The unresolved-target reply is
complete_todo's reply with "delete" in place of "mark done"; the decline and
summary strings are delete's own (Deleted / Deleted nothing / already gone).
No undo claim appears anywhere (delete has no reopen path).

Layer (m-43): handler-level tests with todo_service, the offer store and the
session context mocked — the resolver is pure (shared with complete_todo,
already covered there); this file asserts the delete-specific copy, the
always-confirm rule, and the provenance rule (ids bound at ask time, never
re-sourced from inversion_args at the confirmed "yes"). No LLM, no DB.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from services.domain.models import Intent, IntentCategory, Todo
from services.intent_service import todo_handlers as th
from services.intent_service.conversation_context import NumberedList
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
    CONFIRMED_CONTEXT_KEY,
)
from services.intent_service.todo_handlers import (
    BATCH_DELETE_IDS_KEY,
    BATCH_DELETE_LEFT_KEY,
    BATCH_DELETE_TEXTS_KEY,
    TodoIntentHandlers,
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


class TestCopyHelpers:
    def test_d1_one_item_confirm(self):
        assert (
            th._delete_confirm_question(["review the pr"], [])
            == 'Delete the reminder "review the pr"? (yes/no)'
        )

    def test_d2_two_to_five_collapses_duplicates_and_shows_leaving(self):
        q = th._delete_confirm_question(
            ["check the test card again", "check the test card again", "review the pr"],
            ["revise the pr"],
        )
        assert q == (
            'Delete 3 reminders: "check the test card again" (2 items) and "review the pr"? '
            'Leaving "revise the pr" as is. (yes/no)'
        )

    def test_d3_more_than_five_uses_bullets(self):
        q = th._delete_confirm_question([f"t{i}" for i in range(7)], [f"l{i}" for i in range(4)])
        lines = q.splitlines()
        assert lines[0] == "Delete 7 reminders?"
        assert lines[1:8] == [f"• t{i}" for i in range(7)]
        assert lines[8] == "Leaving the other 4 as is."
        assert lines[-1] == "(yes/no)"

    def test_d4_summary_reports_only_what_deleted_and_partial_failure(self):
        s = th._delete_summary(["a", "a", "b"], [("c", "already gone")], ["d"])
        assert s.splitlines() == [
            "Deleted 3 reminders:",
            "• a (2 items)",
            "• b",
            "Couldn't delete \"c\" — it's already gone.",
            'Left "d" as is.',
        ]

    def test_d4_nothing_deleted(self):
        s = th._delete_summary([], [("x", "already gone")], [])
        assert s.splitlines() == ["Deleted nothing:", "Couldn't delete \"x\" — it's already gone."]

    def test_d5_decline_one_item(self):
        assert (
            th._delete_decline_message(["review the pr"])
            == 'Okay — I won\'t delete "review the pr". Nothing has been changed.'
        )

    def test_d6_decline_several(self):
        assert th._delete_decline_message(["a", "b", "c"]) == (
            "Okay — I won't delete those 3. Nothing has been changed."
        )

    def test_no_undo_phrase_anywhere(self):
        corpus = [
            th._delete_confirm_question(["x"], []),
            th._delete_confirm_question(["a", "b", "c"], ["d"]),
            th._delete_summary(["a"], [("b", "already gone")], ["c"]),
            th._delete_decline_message(["x"]),
            th._delete_decline_message(["x", "y"]),
        ]
        for text in corpus:
            low = text.lower()
            assert "undo" not in low
            assert "restore" not in low
            assert "can't be undone" not in low

    def test_complete_todo_strings_unchanged_by_the_refactor(self):
        """The shared helper must not move complete_todo's pinned strings."""
        assert (
            th._batch_confirm_question(["A", "B"], [])
            == 'Complete 2 reminders: "A" and "B"? (yes/no)'
        )
        s = th._batch_summary(["a", "a", "b"], [("c", "no longer there")], ["d"])
        assert s.splitlines() == [
            "Marked 3 reminders done:",
            "• a (2 items)",
            "• b",
            "Couldn't mark \"c\" done — it's no longer there.",
            'Left "d" as is.',
        ]
        assert th._batch_summary(["only"], [], []).startswith("Marked 1 reminder done:")


def _intent(message: str, targets, exclude=None, extra=None) -> Intent:
    ctx = {"original_message": message, "inversion_args": {"targets": targets}}
    if exclude is not None:
        ctx["inversion_args"]["exclude"] = exclude
    if extra:
        ctx.update(extra)
    return Intent(
        category=IntentCategory.EXECUTION,
        action="delete_todo",
        original_message=message,
        confidence=0.95,
        context=ctx,
    )


class TestHandleDeleteTodoTargets:
    @pytest.fixture
    def handlers(self, four):
        h = TodoIntentHandlers()
        h.todo_service = AsyncMock()
        h.todo_service.list_todos = AsyncMock(return_value=four)
        # the real service returns a truthy deletion result
        h.todo_service.delete_todo = AsyncMock(return_value=True)
        return h

    @pytest.fixture
    def offers(self):
        store = MagicMock()
        store.set_pending_offer = MagicMock()
        return store

    @pytest.fixture
    def session_ctx(self, monkeypatch):
        ctx = MagicMock()
        ctx.last_numbered_list = None
        monkeypatch.setattr(
            "services.intent_service.conversation_context.get_or_create_context",
            lambda session_id, user_id=None: ctx,
        )
        return ctx

    def _shown(self, session_ctx, four):
        session_ctx.last_numbered_list = NumberedList(
            kind="reminders", ids=[t.id for t in four], texts=[t.text for t in four]
        )

    @pytest.mark.asyncio
    async def test_no_router_targets_returns_none_so_the_legacy_handler_runs(
        self, handlers, offers, session_ctx
    ):
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="delete_todo",
            original_message="delete the PR review",
            context={"original_message": "delete the PR review"},
        )
        assert await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u") is None
        handlers.todo_service.delete_todo.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_single_resolved_target_still_arms_the_confirm(
        self, handlers, offers, session_ctx
    ):
        """DESTRUCTIVE: unlike complete_todo, ONE resolved item never
        deletes in the same turn — it always confirms. A pool of exactly
        one (nothing left over) renders the one-item sentence with no
        leaving clause — CXO string D1."""
        only = [_due("review the pr", 100)]
        handlers.todo_service.list_todos = AsyncMock(return_value=only)
        intent = _intent("delete 'review the pr'", ["name:review the pr"])
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        assert msg == 'Delete the reminder "review the pr"? (yes/no)'
        handlers.todo_service.delete_todo.assert_not_awaited()
        offers.set_pending_offer.assert_called_once()
        _sid, offer = offers.set_pending_offer.call_args.args[:2]
        assert offer["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        assert offer["question"] == msg
        pa = offer["pending_action"]
        assert pa["kind"] == "todo_batch_delete" and pa["action"] == "delete_todo"
        assert pa["intent"].context[BATCH_DELETE_IDS_KEY] == [only[0].id]
        assert pa["intent"].context[BATCH_DELETE_TEXTS_KEY] == ["review the pr"]
        assert pa["intent"].context[BATCH_DELETE_LEFT_KEY] == []
        assert offer["decline_message"] == (
            'Okay — I won\'t delete "review the pr". Nothing has been changed.'
        )

    @pytest.mark.asyncio
    async def test_single_resolved_target_with_leftovers_still_renders_the_one_item_sentence(
        self, handlers, offers, session_ctx, four
    ):
        """A single pick out of a bigger pool still gets the one-item
        sentence (D1's shape), with the leaving clause appended — the
        one-item template is not conditioned on the pool size."""
        self._shown(session_ctx, four)
        intent = _intent("delete the last one", ["last"])
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        assert msg == (
            'Delete the reminder "revise the pr"? '
            'Leaving "check the test card again" (2 items) and "review the pr" as is. (yes/no)'
        )
        handlers.todo_service.delete_todo.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_duplicate_title_and_carve_out_arms_the_enumerating_confirm(
        self, handlers, offers, session_ctx, four
    ):
        self._shown(session_ctx, four)
        intent = _intent("delete the first three except the pr one", ["1-3"], exclude=["3"])
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        assert msg == (
            'Delete 2 reminders: "check the test card again" (2 items)? '
            'Leaving "review the pr" and "revise the pr" as is. (yes/no)'
        )
        handlers.todo_service.delete_todo.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_more_than_five_renders_bullets(self, handlers, offers, session_ctx):
        twelve = [_due(f"item {i}", 100 - i) for i in range(12)]
        handlers.todo_service.list_todos = AsyncMock(return_value=twelve)
        intent = _intent("delete all of them", ["all"])
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        lines = msg.splitlines()
        assert lines[0] == "Delete 12 reminders?"
        assert lines[1:13] == [f"• item {i}" for i in range(12)]
        assert lines[-1] == "(yes/no)"

    @pytest.mark.asyncio
    async def test_ordinal_without_a_numbered_list_is_unresolved_says_delete_it(
        self, handlers, offers, session_ctx, four
    ):
        intent = _intent("delete the first one", ["1"])
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is False
        lines = msg.splitlines()
        assert lines[0] == "There's no number 1 in your due reminders. You have 4:"
        assert lines[1:5] == [f"{i + 1}. {t.text}" for i, t in enumerate(four)]
        assert lines[-1] == "Tell me which one, and I'll delete it."
        assert "mark it done" not in msg
        handlers.todo_service.delete_todo.assert_not_awaited()
        offers.set_pending_offer.assert_not_called()
        assert session_ctx.last_numbered_list.ids == [t.id for t in four]

    @pytest.mark.asyncio
    async def test_partial_resolution_promises_only_what_the_state_holds(
        self, handlers, offers, session_ctx, four
    ):
        self._shown(session_ctx, four)
        intent = _intent(
            "delete the first one and 'water the plants'", ["1", "name:water the plants"]
        )
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is False
        assert msg.splitlines()[-1] == (
            "Nothing has been changed. Say it again with the right name or number."
        )
        assert "Tell me which one" not in msg
        handlers.todo_service.delete_todo.assert_not_awaited()
        offers.set_pending_offer.assert_not_called()

    @pytest.mark.asyncio
    async def test_unknown_name_asks_naming_the_list_it_searched(
        self, handlers, offers, session_ctx
    ):
        intent = _intent("delete 'water the plants'", ["name:water the plants"])
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is False
        assert (
            msg.splitlines()[0]
            == 'I couldn\'t find "water the plants" in your due reminders. You have:'
        )
        assert msg.splitlines()[-1] == "Tell me which one, and I'll delete it."
        handlers.todo_service.delete_todo.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_nothing_matched_after_exceptions(self, handlers, offers, session_ctx):
        intent = _intent(
            "delete 'review the pr' except 'review the pr'",
            ["name:review the pr"],
            exclude=["name:review the pr"],
        )
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is False
        assert msg == "Nothing matched after the exceptions. Nothing has been changed."
        handlers.todo_service.delete_todo.assert_not_awaited()
        offers.set_pending_offer.assert_not_called()

    @pytest.mark.asyncio
    async def test_no_session_never_arms_an_unpoppable_offer(
        self, handlers, offers, session_ctx, four
    ):
        intent = _intent("delete 'review the pr'", ["name:review the pr"])
        msg, armed = await handlers.handle_delete_todo_targets(intent, None, uuid4(), offers, "u")
        assert armed is False
        offers.set_pending_offer.assert_not_called()
        handlers.todo_service.delete_todo.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_confirmed_reentry_deletes_exactly_the_bound_ids(
        self, handlers, offers, session_ctx, four
    ):
        """The "yes" re-dispatches the bound intent's ids — never a
        re-resolve of inversion_args at execution (Arch's provenance rule)."""
        intent = _intent(
            "delete the first three",
            ["1-3"],
            extra={
                CONFIRMED_CONTEXT_KEY: True,
                BATCH_DELETE_IDS_KEY: [t.id for t in four[:3]],
                BATCH_DELETE_TEXTS_KEY: [t.text for t in four[:3]],
                BATCH_DELETE_LEFT_KEY: ["revise the pr"],
            },
        )
        # the list may have shifted since the ask; the bound ids still rule,
        # and list_todos is never consulted on this path.
        handlers.todo_service.list_todos = AsyncMock(
            side_effect=AssertionError("must not resolve again")
        )
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is False
        called = [
            str(c.kwargs["todo_id"]) for c in handlers.todo_service.delete_todo.call_args_list
        ]
        assert called == [t.id for t in four[:3]]
        assert msg.splitlines() == [
            "Deleted 3 reminders:",
            "• check the test card again (2 items)",
            "• review the pr",
            'Left "revise the pr" as is.',
        ]
        offers.set_pending_offer.assert_not_called()

    @pytest.mark.asyncio
    async def test_confirmed_reentry_reports_partial_failure_as_already_gone(
        self, handlers, offers, session_ctx, four
    ):
        gone = four[1]
        handlers.todo_service.delete_todo = AsyncMock(
            side_effect=lambda todo_id, user_id: False if str(todo_id) == gone.id else True
        )
        intent = _intent(
            "x",
            ["1-3"],
            extra={
                CONFIRMED_CONTEXT_KEY: True,
                BATCH_DELETE_IDS_KEY: [t.id for t in four[:3]],
                BATCH_DELETE_TEXTS_KEY: [t.text for t in four[:3]],
                BATCH_DELETE_LEFT_KEY: ["revise the pr"],
            },
        )
        msg, _ = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert msg.splitlines()[0] == "Deleted 2 reminders:"
        assert "Couldn't delete \"check the test card again\" — it's already gone." in msg

    @pytest.mark.asyncio
    async def test_confirmed_reentry_nothing_deleted(self, handlers, offers, session_ctx, four):
        handlers.todo_service.delete_todo = AsyncMock(return_value=False)
        intent = _intent(
            "x",
            ["1"],
            extra={
                CONFIRMED_CONTEXT_KEY: True,
                BATCH_DELETE_IDS_KEY: [four[0].id],
                BATCH_DELETE_TEXTS_KEY: [four[0].text],
                BATCH_DELETE_LEFT_KEY: [],
            },
        )
        msg, _ = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert msg.splitlines()[0] == "Deleted nothing:"
        assert "already gone" in msg

    @pytest.mark.asyncio
    async def test_no_undo_claim_in_any_rendered_reply(self, handlers, offers, session_ctx, four):
        self._shown(session_ctx, four)
        intent = _intent("delete the last one", ["last"])
        msg, _ = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert "undo" not in msg.lower()
        assert "restore" not in msg.lower()
