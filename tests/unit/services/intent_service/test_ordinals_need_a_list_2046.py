"""Issue 2046 (CXO's lines, 2026-10-16): ordinals need a list, and one noun.

Served on alpha 6bb955919d with two reminders and NO list shown:
``delete the first two reminders`` answered "There's no number 1 in your
active to-dos. You have 2: buy milk call mom Tell me which one, and I'll
delete it." (numbers the user never saw, items run together), and the
by-title confirm said ``Delete todo: "buy milk"?`` where the numbered one
said ``Delete the reminder "buy milk"?``.

CXO's two lines, pinned per entry path:

1. Ordinals with no bound list → "I haven't shown you a numbered list yet.
   Here are your reminders:", the numbered list (one item per line, blank
   lines around it so Markdown renders a real list), then "I can delete one
   at a time for now. Tell me which one." when two or more were asked (the
   2019 cap), or "Tell me which one." for one. Nothing is deleted, nothing
   is armed, and the shown list is BOUND: the next ``delete reminder 1``
   resolves against it.
2. One noun: every one-item delete confirm reads ``Delete the reminder
   "buy milk"? (yes/no)`` (by title, by number, by pick, by "that"), and the
   result after a yes says "reminder". "to-do" only where the user said it.

Entry paths: ``handle_delete_todo_targets`` through the real rail entry
point (``run_delete_todo_workflow``); ``clear_todos.run_clear_todos``;
``handle_complete_todo_targets`` (it reached the same "no number" line);
the #1666 rail gate (``build_todo_delete_confirmation``) and its confirmed
yes in ``handle_delete_todo``; ``delete_todo_pick``'s bound pick.

Layer (m-43): handler and rail-entry-point level, todo_service, the offer
store and the session context stubbed. No LLM, no DB. The served re-run is
Web's.
"""

import datetime as _dt
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent_service import clear_todos as ct
from services.intent_service.delete_todo_pick import arm_delete_pick, handle_delete_todo_pick_turn
from services.intent_service.destructive_confirm import (
    CONFIRMED_CONTEXT_KEY,
    RESOLVED_TODO_CONTEXT_KEY,
    build_todo_delete_confirmation,
)
from services.intent_service.reminder_copy import (
    copy_noun,
    delete_confirm_question,
    no_list_reply,
)
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.intent_service.workflow_entries import run_delete_todo_workflow
from services.shared_types import IntentCategory

_USER = "5a1e2d40-2046-4b00-9e00-000000002046"
_SESSION = "sess-2046"
# Upcoming, never due: the served pair were saved for later, so the targets
# handler's pool is the active list (the "active to-dos" the served reply
# leaked), not the due reminders.
_LATER = _dt.datetime.now(_dt.timezone.utc) + _dt.timedelta(days=2)

OPENING = "I haven't shown you a numbered list yet. Here are your reminders:"
SERVED_REPLY = (
    f"{OPENING}\n"
    "\n"
    '1. "buy milk"\n'
    '2. "call mom"\n'
    "\n"
    # #2318 (CXO 11-07): the cap sentence, then the ARMED question.
    "I can delete one at a time for now. Which one should I delete? Say the number or the "
    "name, or 'never mind' to leave them alone."
)
SINGLE_REPLY = (
    f'{OPENING}\n\n1. "buy milk"\n2. "call mom"\n\n'
    "Which one should I delete? Say the number or the name, or 'never mind' to leave them alone."
)
MILK_CONFIRM = 'Delete the reminder "buy milk"? (yes/no)'
# #2219 (CXO 2026-11-05 19:25): "todo" when the person named neither noun.
MILK_CONFIRM_TODO = 'Delete the todo "buy milk"? (yes/no)'


def _todo(text, reminder_hours=None):
    return Todo(
        id=str(uuid4()),
        text=text,
        priority="medium",
        status="pending",
        completed=False,
        reminder_date=(
            (_LATER + _dt.timedelta(hours=reminder_hours)) if reminder_hours is not None else None
        ),
    )


def _intent(message, targets=None, action="delete_todo"):
    ctx = {"original_message": message}
    if targets is not None:
        ctx["inversion_args"] = {"targets": targets}
    return Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        original_message=message,
        confidence=0.95,
        context=ctx,
    )


class _Store:
    """One-slot stand-in for the #846 WorkflowOfferService."""

    def __init__(self):
        self.slot = None

    def set_pending_offer(self, session_id, offer, user_id=None):
        self.slot = offer

    def peek_pending_offer(self, session_id, user_id=None):
        return self.slot

    def get_and_clear_pending_offer(self, session_id, user_id=None):
        offer, self.slot = self.slot, None
        return offer


@pytest.fixture
def rows():
    # The served pair (saved for later), listed AFTER a plain todo so the
    # owner's raw list order is not the reminder order.
    return [_todo("water the plants"), _todo("buy milk", 1), _todo("call mom", 2)]


@pytest.fixture
def todo_service(rows):
    svc = AsyncMock()
    svc.list_todos = AsyncMock(return_value=rows)
    svc.delete_todo = AsyncMock(return_value=True)
    svc.complete_todo = AsyncMock(return_value=None)
    return svc


@pytest.fixture
def store():
    return _Store()


@pytest.fixture
def session_ctx(monkeypatch):
    ctx = SimpleNamespace(last_numbered_list=None, last_created_todo=None)
    monkeypatch.setattr(
        "services.intent_service.conversation_context.get_or_create_context",
        lambda session_id, user_id=None: ctx,
    )
    return ctx


@pytest.fixture
def intent_service(todo_service, store, session_ctx):
    handlers = TodoIntentHandlers()
    handlers.todo_service = todo_service
    return SimpleNamespace(todo_handlers=handlers, workflow_offer_service=store)


@pytest.fixture(autouse=True)
def _no_router(monkeypatch):
    """The pick's unresolved branch consults the router; keep it LLM-free."""
    from services.intent_service import inversion_live

    async def _none(*a, **k):
        return None

    monkeypatch.setattr(inversion_live, "read_op_claims_turn", _none)


async def _delete(intent_service, message, targets):
    return await run_delete_todo_workflow(
        _SESSION,
        user_id=_USER,
        context={"intent_service": intent_service, "intent": _intent(message, targets)},
    )


async def _say_yes(intent_service, store):
    """The confirmed re-entry the rail runs on a crisp yes: the bound
    intent, marked confirmed, back through the rail entry point."""
    offer = store.get_and_clear_pending_offer(_SESSION)
    bound = offer["pending_action"]["intent"]
    bound.context = {**bound.context, CONFIRMED_CONTEXT_KEY: True}
    return await run_delete_todo_workflow(
        _SESSION, user_id=_USER, context={"intent_service": intent_service, "intent": bound}
    )


# ---------------------------------------------------------------------------
# 1. The copy: one module, CXO's words
# ---------------------------------------------------------------------------


class TestCopy:
    def test_no_list_reply_is_cxos_line_with_a_real_numbered_list(self):
        reply = no_list_reply(
            ["buy milk", "call mom"],
            "reminder",
            "I can delete one at a time for now. Which one should I delete? Say the number or "
            "the name, or 'never mind' to leave them alone.",
        )
        assert reply == SERVED_REPLY
        # A real list: each item on its own line, a blank line on each side
        # (a line straight after a list item renders inside it, #2002).
        assert "\n\n1. " in reply and '"call mom"\n\n' in reply
        assert "There's no number" not in reply

    def test_never_a_question(self):
        """TestUnarmedAskSiteRatchet: an instruction, nothing armed."""
        for line in SERVED_REPLY.splitlines():
            assert not line.rstrip().endswith("?"), line

    @pytest.mark.parametrize(
        ("message", "noun"),
        [
            ("delete the first two reminders", "reminder"),
            ("delete buy milk", "todo"),  # #2219: todo by default
            ("delete 1", "todo"),
            ("delete todo 1", "todo"),
            ("delete the first two to-dos", "todo"),
            ("delete my milk todo reminder", "reminder"),  # reminder wins a mixed mention
        ],
    )
    def test_noun_is_todo_unless_the_user_said_reminder(self, message, noun):
        assert copy_noun(message) == noun

    def test_one_confirm_form(self):
        assert delete_confirm_question("buy milk") == MILK_CONFIRM_TODO
        assert delete_confirm_question("buy milk", "reminder") == MILK_CONFIRM


# ---------------------------------------------------------------------------
# 2. The served case: the targets path through the real rail entry point
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestTargetsPathNoListShown:
    async def test_first_two_shows_the_list_capped_and_deletes_nothing(
        self, intent_service, store, todo_service, session_ctx, rows
    ):
        result = await _delete(intent_service, "delete the first two reminders", ["1-2"])
        assert result.message == SERVED_REPLY
        # #2318 (CXO 11-07): the question is armed — the pick over the shown rows.
        assert result.requires_clarification is True
        assert not result.intent_data.get("destructive_confirmation_pending")
        assert store.slot["pending_action"]["kind"] == "delete_todo_pick_question"
        todo_service.delete_todo.assert_not_awaited()
        # Showing the list BINDS it — exactly the rows shown, in shown order.
        assert session_ctx.last_numbered_list.ids == [rows[1].id, rows[2].id]
        assert session_ctx.last_numbered_list.kind == "reminders"

    async def test_the_shown_list_binds_the_next_ordinal_then_yes_says_reminder(
        self, intent_service, store, todo_service, rows
    ):
        await _delete(intent_service, "delete the first two reminders", ["1-2"])
        asked = await _delete(intent_service, "delete reminder 1", ["1"])
        # "1" is buy milk, the first row SHOWN — not the owner's raw row 1.
        assert asked.message == MILK_CONFIRM
        assert asked.requires_clarification is True
        todo_service.delete_todo.assert_not_awaited()

        done = await _say_yes(intent_service, store)
        assert done.message == "Deleted 1 reminder:\n• buy milk"
        todo_service.delete_todo.assert_awaited_once_with(
            todo_id=UUID(rows[1].id), user_id=UUID(_USER)
        )

    async def test_one_ordinal_ends_on_the_armed_question(
        self, intent_service, store, todo_service
    ):
        result = await _delete(intent_service, "delete the first reminder", ["1"])
        assert result.message == SINGLE_REPLY
        assert store.slot["pending_action"]["kind"] == "delete_todo_pick_question"
        todo_service.delete_todo.assert_not_awaited()

    async def test_a_bare_number_after_it_reaches_the_confirm(
        self, intent_service, store, todo_service
    ):
        """#2318: the reason it is armed — a bare "2" binds the shown row 2."""
        from services.intent_service.delete_todo_pick import handle_delete_todo_pick_turn

        await _delete(intent_service, "delete the first reminder", ["1"])
        offer = store.get_and_clear_pending_offer(_SESSION)
        out = await handle_delete_todo_pick_turn(
            offer, "2", session_id=_SESSION, user_id=_USER, intent_service=intent_service
        )
        assert out["message"] == 'Delete the reminder "call mom"? (yes/no)'
        todo_service.delete_todo.assert_not_awaited()

    async def test_the_user_said_to_do(self, intent_service, rows):
        result = await _delete(intent_service, "delete the first two to-dos", ["1-2"])
        assert result.message.startswith(
            "I haven't shown you a numbered list yet. Here are your todos:\n\n"
            '1. "water the plants"\n2. "buy milk"\n3. "call mom"\n\n'
        )
        assert result.message.endswith(
            "I can delete one at a time for now. Which one should I delete? Say the number or "
            "the name, or 'never mind' to leave them alone."
        )

    async def test_a_shown_list_still_gets_todays_out_of_range_line(
        self, intent_service, todo_service
    ):
        """Only an UNBOUND ordinal gets the new opening: past the end of a
        list the user did see, the numbers are real."""
        await _delete(intent_service, "delete the first two reminders", ["1-2"])
        result = await _delete(intent_service, "delete reminder 5", ["5"])
        assert result.message.startswith("There's no number 5 in your reminders. You have 2:")
        todo_service.delete_todo.assert_not_awaited()


# ---------------------------------------------------------------------------
# 3. The other entry paths that reached "There's no number"
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestOtherEntryPaths:
    async def test_clear_todos_shows_the_list_and_binds_it(
        self, intent_service, store, todo_service, session_ctx, rows
    ):
        intent = _intent("clear the first two reminders", ["1-2"], action="clear_todos")
        result = await ct.run_clear_todos(intent, _SESSION, _USER, intent_service)
        # The verb is still open on this path (mark done or delete), so the
        # bare instruction; the cap is said where the delete leg resolves.
        assert result.message == f'{OPENING}\n\n1. "buy milk"\n2. "call mom"\n\nTell me which one.'
        assert store.slot is None
        todo_service.delete_todo.assert_not_awaited()
        todo_service.complete_todo.assert_not_awaited()
        assert session_ctx.last_numbered_list.ids == [rows[1].id, rows[2].id]

    async def test_complete_shows_the_list_never_no_number(
        self, intent_service, store, todo_service, session_ctx, rows
    ):
        msg, armed = await intent_service.todo_handlers.handle_complete_todo_targets(
            _intent("complete the first reminder", ["1"], action="complete_todo"),
            _SESSION,
            UUID(_USER),
            store,
            _USER,
        )
        assert armed is True  # #2318 (CXO 11-07)
        assert msg == (
            f'{OPENING}\n\n1. "buy milk"\n2. "call mom"\n\n'
            "Which one should I complete? Say the number or the name, or 'never mind' to "
            "leave them alone."
        )
        todo_service.complete_todo.assert_not_awaited()
        assert session_ctx.last_numbered_list.ids == [rows[1].id, rows[2].id]

    async def test_no_router_targets_keeps_the_armed_numbered_pick(
        self, intent_service, store, todo_service
    ):
        """Without router targets the legacy handler's armed pick answers
        (already numbered, already bound); it never says "no number"."""
        result = await _delete(intent_service, "delete the first two reminders", None)
        assert result.message.startswith("Which reminder should I delete?")
        assert "no number" not in result.message
        todo_service.delete_todo.assert_not_awaited()


# ---------------------------------------------------------------------------
# 4. One noun: every one-item confirm, and the result after yes
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestOneConfirmForm:
    async def test_by_title_matches_the_numbered_confirm(self, intent_service, rows):
        gate = await build_todo_delete_confirmation(
            _intent("delete buy milk"), intent_service.todo_handlers, UUID(_USER)
        )
        assert gate.offer.question == MILK_CONFIRM_TODO
        assert 'won\'t delete the todo "buy milk"' in gate.offer.offer["decline_message"]

    async def test_by_title_yes_says_reminder(self, intent_service, todo_service, rows):
        intent = _intent("delete buy milk")
        await build_todo_delete_confirmation(intent, intent_service.todo_handlers, UUID(_USER))
        intent.context[CONFIRMED_CONTEXT_KEY] = True
        msg = await intent_service.todo_handlers.handle_delete_todo(
            intent, _SESSION, user_id=UUID(_USER)
        )
        assert msg == "Deleted 1 todo:\n• buy milk"
        todo_service.delete_todo.assert_awaited_once_with(
            todo_id=UUID(rows[1].id), user_id=UUID(_USER)
        )

    async def test_by_title_after_yes_when_the_row_is_gone(self, intent_service, todo_service):
        intent = _intent("delete buy milk")
        await build_todo_delete_confirmation(intent, intent_service.todo_handlers, UUID(_USER))
        intent.context[CONFIRMED_CONTEXT_KEY] = True
        todo_service.delete_todo.return_value = None
        msg = await intent_service.todo_handlers.handle_delete_todo(
            intent, _SESSION, user_id=UUID(_USER)
        )
        assert msg == "Deleted nothing:\nCouldn't delete \"buy milk\" — it's already gone."

    async def test_by_title_when_the_user_said_to_do(self, intent_service):
        intent = _intent("delete the buy milk to-do")
        gate = await build_todo_delete_confirmation(
            intent, intent_service.todo_handlers, UUID(_USER)
        )
        assert gate.offer.question == 'Delete the todo "buy milk"? (yes/no)'
        assert intent.context[RESOLVED_TODO_CONTEXT_KEY]["noun"] == "todo"

    async def test_bare_number_leg_says_the_one_form(self, intent_service):
        gate = await build_todo_delete_confirmation(
            _intent("delete 2"), intent_service.todo_handlers, UUID(_USER)
        )
        # This leg indexes the owner's raw list (row 2 is buy milk here).
        assert gate.offer.question == MILK_CONFIRM_TODO

    async def test_pick_leg_says_the_one_form_and_yes_says_reminder(
        self, intent_service, store, todo_service, rows
    ):
        q = await arm_delete_pick(
            "delete a reminder", _SESSION, _USER, UUID(_USER), todo_service, store
        )
        assert q.startswith("Which reminder should I delete?")
        offer = store.get_and_clear_pending_offer(_SESSION)
        out = await handle_delete_todo_pick_turn(
            offer, "1", session_id=_SESSION, user_id=_USER, intent_service=intent_service
        )
        assert out["message"] == MILK_CONFIRM
        bound = store.slot["pending_action"]["intent"]
        assert bound.context[RESOLVED_TODO_CONTEXT_KEY]["noun"] == "reminder"
        bound.context[CONFIRMED_CONTEXT_KEY] = True
        msg = await intent_service.todo_handlers.handle_delete_todo(
            bound, _SESSION, user_id=UUID(_USER)
        )
        assert msg == "Deleted 1 reminder:\n• buy milk"
