"""#1987 — 'delete that reminder' right after 'Reminder saved: …'.

Alpha c613beabf5, 2026-10-12 (Web's served run, turn 3 follow-up): the
reminder saved, then "delete that reminder" → "Which todo should I remove?
Try: 'delete todo [number]'" and nothing deleted. The words point at the row
the previous turn created; nothing in the text names it (that/it/this are
``_STOPWORDS``, "reminder" is ``_DELETE_COMMAND_NOISE``), so the #1666 gate's
no-number/no-name branch passed through to the handler's which-todo ask.

The fix under test, in the #1943 family's spirit (consume state, add no
binder): the create handlers record the row they made on the session
(``conversation_context.last_created_todo``, the ``last_numbered_list``
idiom); the gate's no-number/no-name branch, when the message points and the
session holds a created row still in the owner's list, arms the EXISTING
title-bound confirm with that row bound by id (reminder → CXO's D1 copy;
todo → the #1527 named-leg copy). Guards pinned: no session, no created row,
an indefinite ask, a numbered list shown AFTER the creation → the unchanged
passthrough; a created row gone from the list → honest didn't-find, nothing
armed. The named and numbered legs are unchanged with a created row present.

Layer (m-43): the async gate builder and the create_todo handler with
todo_service and the session context stubbed; the create_reminder call site
and the rail caller are pinned at source level. No LLM, no DB, no served
turn — the served create-then-delete on alpha is the issue's third AC and
stays owed.
"""

import datetime as _dt
import inspect
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent_service import conversation_context as cc
from services.intent_service import destructive_confirm as dc
from services.intent_service.conversation_context import CreatedTodo, NumberedList
from services.intent_service.destructive_confirm import (
    DESTRUCTIVE_CONFIRM_KIND,
    RESOLVED_TODO_CONTEXT_KEY,
    build_todo_delete_confirmation,
)
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.shared_types import IntentCategory

_USER = "3f7b8a52-1987-4b00-9e00-000000001987"
_SESSION = "sess-1987"


def _todo(text, reminder=True):
    return Todo(
        id=str(uuid4()),
        text=text,
        priority="medium",
        status="pending",
        completed=False,
        reminder_date=(
            _dt.datetime(2026, 10, 16, 16, 0, tzinfo=_dt.timezone.utc) if reminder else None
        ),
    )


def _intent(message, action="delete_todo"):
    return Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        original_message=message,
        confidence=0.95,
        context={"original_message": message},
    )


@pytest.fixture
def session_ctx(monkeypatch):
    ctx = SimpleNamespace(last_numbered_list=None, last_created_todo=None)
    monkeypatch.setattr(cc, "get_or_create_context", lambda session_id, user_id=None: ctx)
    return ctx


@pytest.fixture
def created():
    return _todo("send the invoice")


@pytest.fixture
def handlers(created):
    h = TodoIntentHandlers()
    h.todo_service = AsyncMock()
    h.todo_service.list_todos = AsyncMock(return_value=[_todo("review the pr"), created])
    return h


def _record(session_ctx, created, kind="reminder", minutes_ago=1):
    session_ctx.last_created_todo = CreatedTodo(
        id=created.id,
        text=created.text,
        kind=kind,
        created_at=_dt.datetime.now() - _dt.timedelta(minutes=minutes_ago),
    )


# ---------------------------------------------------------------------------
# 1. The record — what the create turn leaves on the session
# ---------------------------------------------------------------------------


class TestCreatedRecord:
    def test_remember_and_recall_round_trip(self, session_ctx, created):
        TodoIntentHandlers._remember_created_todo(_SESSION, _USER, created, "reminder")
        got = TodoIntentHandlers._recall_created_todo(_SESSION, _USER)
        assert isinstance(got, CreatedTodo)
        assert (got.id, got.text, got.kind) == (created.id, "send the invoice", "reminder")

    def test_no_session_records_nothing_and_recalls_none(self, session_ctx, created):
        TodoIntentHandlers._remember_created_todo(None, _USER, created, "todo")
        assert session_ctx.last_created_todo is None
        assert TodoIntentHandlers._recall_created_todo(None, _USER) is None

    @pytest.mark.asyncio
    async def test_create_todo_records_the_row_it_made(self, session_ctx, created):
        """The real create_todo handler, todo_service stubbed: the saved row
        lands on the session as kind 'todo'."""
        h = TodoIntentHandlers()
        h.todo_service = AsyncMock()
        made = _todo("send the invoice", reminder=False)
        h.todo_service.create_todo = AsyncMock(return_value=made)
        await h.handle_create_todo(
            _intent("add todo: send the invoice", "create_todo"), _SESSION, _USER
        )
        rec = session_ctx.last_created_todo
        assert rec is not None and rec.id == made.id and rec.kind == "todo"

    def test_create_reminder_records_at_the_real_save(self):
        """Source pin: the reminder handler records the row right after the
        REAL save (the same spot create_todo does) — the one place a
        'Reminder saved' row exists to point at."""
        src = inspect.getsource(TodoIntentHandlers.handle_create_reminder)
        assert 'self._remember_created_todo(session_id, user_id, todo, "reminder")' in src
        assert src.index("await self.todo_service.create_todo(") < src.index(
            "_remember_created_todo"
        )

    def test_rail_caller_threads_the_session(self):
        """Source pin: the consent-gate call site passes session_id, or the
        leg can never see the record."""
        from services.intent.intent_service import IntentService

        src = inspect.getsource(IntentService._dispatch_action_rail)
        call = src[src.index("await build_todo_delete_confirmation(") :]
        # up to the call's own closing paren (the first argument carries one)
        assert "session_id=session_id" in call[: call.index("\n                )")]


# ---------------------------------------------------------------------------
# 2. The gate's referent leg
# ---------------------------------------------------------------------------


class TestReferentLeg:
    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize(
        "message",
        ("delete that reminder", "delete it", "remove that", "cancel this reminder"),
    )
    async def test_pointer_after_a_saved_reminder_arms_d1_bound_to_that_row(
        self, message, handlers, session_ctx, created
    ):
        _record(session_ctx, created, "reminder")
        intent = _intent(message)
        gate = await build_todo_delete_confirmation(intent, handlers, _USER, session_id=_SESSION)
        assert gate.offer is not None and not gate.passthrough and gate.clarification is None
        assert gate.offer.question == 'Delete the reminder "send the invoice"? (yes/no)'
        record = gate.offer.offer
        assert record["question"] == gate.offer.question
        pa = record["pending_action"]
        assert pa["kind"] == DESTRUCTIVE_CONFIRM_KIND
        assert pa["action"] == "delete_todo" and pa["intent"] is intent
        assert 'won\'t delete the reminder "send the invoice"' in record["decline_message"]
        # WHAT-binding (#1666): the yes deletes exactly the created row, by id.
        resolved = intent.context[RESOLVED_TODO_CONTEXT_KEY]
        assert resolved["todo_id"] == created.id
        assert resolved["text"] == "send the invoice"
        assert resolved["number"] == "2"

    async def test_a_created_todo_uses_the_named_leg_copy(self, handlers, session_ctx, created):
        _record(session_ctx, created, "todo")
        intent = _intent("delete that")
        gate = await build_todo_delete_confirmation(intent, handlers, _USER, session_id=_SESSION)
        assert gate.offer is not None
        assert gate.offer.question == 'Delete the todo "send the invoice"? (yes/no)'
        assert intent.context[RESOLVED_TODO_CONTEXT_KEY]["todo_id"] == created.id

    async def test_no_created_row_is_the_unchanged_passthrough(self, handlers, session_ctx):
        intent = _intent("delete that reminder")
        gate = await build_todo_delete_confirmation(intent, handlers, _USER, session_id=_SESSION)
        assert gate.passthrough and gate.offer is None
        assert RESOLVED_TODO_CONTEXT_KEY not in (intent.context or {})

    async def test_no_session_is_the_unchanged_passthrough(self, handlers, session_ctx, created):
        _record(session_ctx, created)
        gate = await build_todo_delete_confirmation(
            _intent("delete that reminder"), handlers, _USER
        )
        assert gate.passthrough

    @pytest.mark.parametrize("message", ("delete a reminder", "delete my reminder"))
    async def test_an_indefinite_ask_does_not_take_the_created_row(
        self, message, handlers, session_ctx, created
    ):
        """CXO's 10-12 case ('delete a reminder' after two were set) names no
        referent — the which-todo ask stays; its own bar (list the candidates
        numbered, armed pick) is the other half of #1987."""
        _record(session_ctx, created)
        gate = await build_todo_delete_confirmation(
            _intent(message), handlers, _USER, session_id=_SESSION
        )
        assert gate.passthrough and gate.offer is None

    async def test_a_numbered_list_shown_after_the_creation_makes_that_ambiguous(
        self, handlers, session_ctx, created
    ):
        _record(session_ctx, created, minutes_ago=5)
        session_ctx.last_numbered_list = NumberedList(
            kind="reminders", ids=[created.id], texts=[created.text]
        )  # shown_at = now, i.e. AFTER the creation
        gate = await build_todo_delete_confirmation(
            _intent("delete that reminder"), handlers, _USER, session_id=_SESSION
        )
        assert gate.passthrough and gate.offer is None

    async def test_a_numbered_list_shown_before_the_creation_does_not_block(
        self, handlers, session_ctx, created
    ):
        session_ctx.last_numbered_list = NumberedList(
            kind="reminders",
            ids=["x"],
            texts=["older"],
            shown_at=_dt.datetime.now() - _dt.timedelta(minutes=10),
        )
        _record(session_ctx, created, minutes_ago=1)
        gate = await build_todo_delete_confirmation(
            _intent("delete that reminder"), handlers, _USER, session_id=_SESSION
        )
        assert gate.offer is not None

    async def test_created_row_gone_from_the_list_is_honest_and_arms_nothing(
        self, handlers, session_ctx, created
    ):
        _record(session_ctx, created)
        handlers.todo_service.list_todos = AsyncMock(return_value=[_todo("review the pr")])
        intent = _intent("delete that reminder")
        gate = await build_todo_delete_confirmation(intent, handlers, _USER, session_id=_SESSION)
        assert gate.offer is None and not gate.passthrough
        assert 'I can\'t find "send the invoice" anymore' in gate.clarification
        assert "nothing has been deleted" in gate.clarification
        assert RESOLVED_TODO_CONTEXT_KEY not in (intent.context or {})

    async def test_named_leg_still_wins_when_the_user_names_a_different_row(
        self, handlers, session_ctx, created
    ):
        _record(session_ctx, created)
        intent = _intent("delete my review the pr reminder")
        gate = await build_todo_delete_confirmation(intent, handlers, _USER, session_id=_SESSION)
        assert gate.offer is not None
        assert gate.offer.question == 'Delete the reminder "review the pr"? (yes/no)'
        assert intent.context[RESOLVED_TODO_CONTEXT_KEY]["todo_id"] != created.id

    async def test_numbered_leg_unchanged(self, handlers, session_ctx, created):
        _record(session_ctx, created)
        intent = _intent("delete todo 1")
        gate = await build_todo_delete_confirmation(intent, handlers, _USER, session_id=_SESSION)
        assert gate.offer is not None
        assert gate.offer.question == 'Delete the todo "review the pr"? (yes/no)'


class TestPointerCheck:
    def test_pointer_check_is_a_word_set_not_a_regex(self):
        """No new message-parsing regex on this path (the 1527 ratchet note);
        the pointer read is a set intersection over the message's words.
        (Its own class: the leg's class carries an asyncio mark, which warns
        on a sync test.)"""
        assert dc._points_at_recent("delete that reminder")
        assert dc._points_at_recent("Remove IT")
        assert not dc._points_at_recent("delete a reminder")
        assert not dc._points_at_recent("delete the itinerary reminder")  # 'it' inside a word
        assert isinstance(dc._REFERENT_WORDS, frozenset)
