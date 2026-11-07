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
    RESOLVED_TODO_CONTEXT_KEY,
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
            == 'Delete the todo "review the pr"? (yes/no)'
        )

    def test_d2_two_to_five_collapses_duplicates_and_shows_leaving(self):
        q = th._delete_confirm_question(
            ["check the test card again", "check the test card again", "review the pr"],
            ["revise the pr"],
        )
        assert q == (
            'Delete 3 todos: "check the test card again" (2 items) and "review the pr"? '
            'Leaving "revise the pr" as is. (yes/no)'
        )

    def test_d3_more_than_five_uses_bullets(self):
        q = th._delete_confirm_question([f"t{i}" for i in range(7)], [f"l{i}" for i in range(4)])
        lines = q.splitlines()
        assert lines[0] == "Delete 7 todos?"
        assert lines[1:8] == [f"• t{i}" for i in range(7)]
        assert lines[8] == "Leaving the other 4 as is."
        assert lines[-1] == "(yes/no)"

    def test_d4_summary_reports_only_what_deleted_and_partial_failure(self):
        s = th._delete_summary(["a", "a", "b"], [("c", "already gone")], ["d"])
        assert s.splitlines() == [
            "Deleted 3 todos:",
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
            th._batch_confirm_question(["A", "B"], []) == 'Complete 2 todos: "A" and "B"? (yes/no)'
        )
        s = th._batch_summary(["a", "a", "b"], [("c", "no longer there")], ["d"])
        assert s.splitlines() == [
            "Marked 3 todos done:",
            "• a (2 items)",
            "• b",
            "Couldn't mark \"c\" done — it's no longer there.",
            'Left "d" as is.',
        ]
        assert th._batch_summary(["only"], [], []).startswith("Marked 1 todo done:")


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
    async def test_1975_gate_confirmed_yes_with_a_bound_row_is_left_to_the_legacy_handler(
        self, handlers, offers, session_ctx
    ):
        """#1975 (alpha 4bd1a236e9, Web's served run 2026-10-11): 'delete the
        reminder "web check alpha one"' named an UPCOMING reminder. The #1666
        rail gate resolved it against all active todos, asked 'Delete todo:
        "web check alpha one"? (yes/no)' and bound the row. The confirmed yes
        then reached THIS handler first (the router had named the target
        too), which re-resolved the name against due reminders only and
        answered "I couldn't find … in your due reminders" — the executor
        searching a different set from the confirm. A gate-confirmed carrier
        with a bound row is not this handler's turn: return None so
        handle_delete_todo deletes exactly the bound id."""
        upcoming = Todo(text="web check alpha one", priority="medium")
        upcoming.id = str(uuid4())
        upcoming.reminder_date = _NOW + timedelta(hours=16)
        upcoming.completed = False
        due_only = [_due("revise the pr", 100)]
        handlers.todo_service.list_todos = AsyncMock(return_value=due_only + [upcoming])
        intent = _intent(
            'delete the reminder "web check alpha one"',
            ["name:web check alpha one"],
            extra={
                CONFIRMED_CONTEXT_KEY: True,
                RESOLVED_TODO_CONTEXT_KEY: {
                    "todo_id": upcoming.id,
                    "text": upcoming.text,
                    "number": "2",
                },
            },
        )
        result = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert result is None
        handlers.todo_service.delete_todo.assert_not_awaited()
        offers.set_pending_offer.assert_not_called()

    @pytest.mark.asyncio
    async def test_1975_the_same_turn_unconfirmed_still_resolves_against_the_due_pool(
        self, handlers, offers, session_ctx
    ):
        """Boundary: without the gate's binding the handler's own path is
        unchanged — an upcoming reminder named while another is due is still
        unresolved against the due pool (that pool rule is #1943's, not this
        fix's). Pins that #1975 narrowed nothing but the confirmed re-entry."""
        upcoming = Todo(text="web check alpha one", priority="medium")
        upcoming.id = str(uuid4())
        upcoming.reminder_date = _NOW + timedelta(hours=16)
        upcoming.completed = False
        handlers.todo_service.list_todos = AsyncMock(
            return_value=[_due("revise the pr", 100), upcoming]
        )
        intent = _intent('delete the reminder "web check alpha one"', ["name:web check alpha one"])
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True  # #2318: the unresolved reply's question is armed
        assert msg.startswith('I couldn\'t find "web check alpha one" in your due reminders.')
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
        assert msg == 'Delete the todo "review the pr"? (yes/no)'
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
    async def test_single_target_without_exclude_is_exactly_d1(
        self, handlers, offers, session_ctx, four
    ):
        """CXO 2026-10-07: one named target, no carve-out → exactly D1. The
        Leaving line names what a carve-out spared; it never recites the rest
        of the list on a one-item question."""
        self._shown(session_ctx, four)
        intent = _intent("delete the last one", ["last"])
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        assert msg == 'Delete the reminder "revise the pr"? (yes/no)'
        offer = offers.set_pending_offer.call_args[0][1]
        assert offer["pending_action"]["intent"].context[BATCH_DELETE_LEFT_KEY] == []
        handlers.todo_service.delete_todo.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_single_target_with_an_exclude_keeps_the_leaving_line(
        self, handlers, offers, session_ctx, four
    ):
        """One target that remains after an explicit carve-out keeps the line."""
        self._shown(session_ctx, four)
        intent = _intent("delete the last two except the first of them", ["3-4"], exclude=["3"])
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        assert msg.startswith('Delete the reminder "revise the pr"? Leaving ')
        assert msg.endswith(" as is. (yes/no)")

    @pytest.mark.asyncio
    async def test_duplicate_title_and_carve_out_is_capped_issue_2019(
        self, handlers, offers, session_ctx, four
    ):
        """Issue 2019 (xian 2026-10-14): two resolved items after a carve-out
        delete nothing — CXO's capped reply names each item in the order
        resolved (was: the D2 enumerating confirm). #2318 (CXO 11-07): it asks
        an armed question, the #1987 pick over those lines, labelled as shown."""
        self._shown(session_ctx, four)
        intent = _intent("delete the first three except the pr one", ["1-3"], exclude=["3"])
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        assert msg == (
            "I can delete one reminder at a time for now. You asked about these:\n"
            '1. "check the test card again"\n'
            '2. "check the test card again"\n'
            "\n"
            "Which one should I delete first? Say the number or the name, or 'never mind' "
            "to leave them alone."
        )
        handlers.todo_service.delete_todo.assert_not_awaited()
        _sid, offer = offers.set_pending_offer.call_args.args[:2]
        assert offer["pending_action"]["kind"] == "delete_todo_pick_question"

    @pytest.mark.asyncio
    async def test_capped_reply_says_todo_when_the_person_said_todos_2219(
        self, handlers, offers, session_ctx, four
    ):
        """#2219 (Web 11-06, served on 7ffd460640): "delete the first two todos" got
        "one reminder". CXO's conversation rule: the person's own word wins."""
        self._shown(session_ctx, four)
        intent = _intent("delete the first two todos", ["1-2"])
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True  # #2318: the capped question is armed
        assert msg.splitlines()[0] == (
            "I can delete one todo at a time for now. You asked about these:"
        )
        handlers.todo_service.delete_todo.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_all_of_twelve_is_capped_issue_2019(self, handlers, offers, session_ctx):
        """Issue 2019: "delete all of them" over 12 rows deletes nothing and
        lists all 12 numbered (was: the D3 bulleted confirm); #2318: armed as
        the pick over the 12, numbered 1..12 since no list was shown."""
        twelve = [_due(f"item {i}", 100 - i) for i in range(12)]
        handlers.todo_service.list_todos = AsyncMock(return_value=twelve)
        intent = _intent("delete all of them", ["all"])
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        lines = msg.splitlines()
        assert lines[0] == "I can delete one reminder at a time for now. You asked about these:"
        assert lines[1:13] == [f'{i + 1}. "item {i}"' for i in range(12)]
        assert lines[-1] == (
            "Which one should I delete first? Say the number or the name, or 'never mind' "
            "to leave them alone."
        )
        handlers.todo_service.delete_todo.assert_not_awaited()
        _sid, offer = offers.set_pending_offer.call_args.args[:2]
        assert len(offer["pending_action"]["pick_ids"]) == 12

    @pytest.mark.asyncio
    async def test_ordinal_without_a_numbered_list_shows_the_list_and_asks(
        self, handlers, offers, session_ctx, four
    ):
        """Issue 2046 (CXO line 1): one ordinal, no list shown → the opening,
        the numbered list, then (#2318, CXO 11-07) the armed question (no cap
        sentence: one asked)."""
        intent = _intent("delete the first one", ["1"])
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        assert armed is True
        assert msg == (
            "I haven't shown you a numbered list yet. Here are your todos:\n\n"
            + "\n".join(f'{i + 1}. "{t.text}"' for i, t in enumerate(four))
            + "\n\nWhich one should I delete? Say the number or the name, or 'never mind' "
            "to leave them alone."
        )
        assert "mark it done" not in msg
        handlers.todo_service.delete_todo.assert_not_awaited()
        _sid, offer = offers.set_pending_offer.call_args.args[:2]
        assert offer["pending_action"]["verb"] == "delete"
        assert offer["pending_action"]["pick_ids"] == [str(t.id) for t in four]
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
        assert armed is True  # #2318: armed over the rows shown
        assert (
            msg.splitlines()[0]
            == 'I couldn\'t find "water the plants" in your due reminders. You have:'
        )
        assert msg.splitlines()[-1] == (
            "Which one should I delete? Say the number or the name, or 'never mind' "
            "to leave them alone."
        )
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
        re-resolve of inversion_args at execution (Arch's provenance rule).
        One bound id (issue 2019 caps the carrier at one item)."""
        intent = _intent(
            "delete the third one",
            ["3"],
            extra={
                CONFIRMED_CONTEXT_KEY: True,
                BATCH_DELETE_IDS_KEY: [four[2].id],
                BATCH_DELETE_TEXTS_KEY: [four[2].text],
                BATCH_DELETE_LEFT_KEY: [],
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
        assert called == [four[2].id]
        assert msg.splitlines() == ["Deleted 1 todo:", "• review the pr"]
        offers.set_pending_offer.assert_not_called()

    @pytest.mark.asyncio
    async def test_confirmed_reentry_with_several_bound_ids_is_capped_issue_2019(
        self, handlers, offers, session_ctx, four
    ):
        """Issue 2019 belt: a multi-id carrier armed before the cap shipped
        deletes NOTHING on its "yes" — the capped reply instead. The noun follows
        CXO's conversation rule (#2219): no noun said and no list shown, so "todo"
        (Web 11-06: the old default said "reminder" for todos)."""
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
        msg, armed = await handlers.handle_delete_todo_targets(intent, "s1", uuid4(), offers, "u")
        # #2318 (CXO 11-07): the belt asks the cap's armed pick, never deletes.
        assert armed is True
        assert msg == (
            "I can delete one todo at a time for now. You asked about these:\n"
            '1. "check the test card again"\n'
            '2. "check the test card again"\n'
            '3. "review the pr"\n'
            "\n"
            "Which one should I delete first? Say the number or the name, or 'never mind' "
            "to leave them alone."
        )
        handlers.todo_service.delete_todo.assert_not_awaited()
        _sid, offer = offers.set_pending_offer.call_args.args[:2]
        assert offer["pending_action"]["kind"] == "delete_todo_pick_question"

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
