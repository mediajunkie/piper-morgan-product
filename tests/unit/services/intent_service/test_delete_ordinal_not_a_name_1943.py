"""#1943, the "first N" DELETE shape — a position is not a name.

Web's served run on alpha 4bd1a236e9 (2026-10-11): with five reminders
listed, `delete the first two reminders` armed ONE confirm naming the row
whose text contained the word "two" ('Delete todo: "web check alpha two"?').
Mechanism (read from source, reproduced here): the #1666 gate runs in the
consent layer BEFORE the rail entry point; its #1527 named-target leg turned
the message into the "name" `first two` and resolved it with the shared
fuzzy matcher. The router-targets hook (`handle_delete_todo_targets`, which
resolves positions against the numbered list the user saw) never ran.

The fix: a positional-only target ("first two", "last", "1-3", "the second
one") is nothing-named to the gate → passthrough → the rail entry point's
targets hook (router args) or the handler's numbered which-todo ask (no
router args). The named leg itself is untouched ("delete my hydrate
reminder" still binds). No LLM, no DB.
"""

from __future__ import annotations

import datetime as _dt
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent_service.conversation_context import NumberedList
from services.intent_service.destructive_confirm import (
    _is_positional_only,
    _named_delete_target,
    build_todo_delete_confirmation,
)
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.shared_types import IntentCategory

_USER = "3f7b8a52-1943-4b00-9e00-000000001943"

POSITIONAL = [
    "delete the first two reminders",
    "delete the first 2 reminders",
    "delete the last reminder",
    "delete reminders 1-3",
    "delete the second one",
    "remove the first three todos",
]
NAMED = [
    "delete my hydrate reminder",
    "delete the meeting todo",
    "delete the reminder about the budget review",
]


def _todo(text: str, when: _dt.datetime) -> Todo:
    return Todo(
        id=str(uuid4()),
        text=text,
        priority="medium",
        status="pending",
        completed=False,
        reminder_date=when,
    )


def _webs_list():
    """Web's 10-11 list shape: two real due items first, then the two seeded
    upcoming ones whose titles carry the words "one" and "two"."""
    now = _dt.datetime.now(_dt.timezone.utc)
    return [
        _todo("revise the pr", now - _dt.timedelta(hours=4)),
        _todo("send the budget review to finance", now - _dt.timedelta(hours=3)),
        _todo("web check alpha one", now + _dt.timedelta(days=1)),
        _todo("web check alpha two", now + _dt.timedelta(days=1, hours=1)),
    ]


class _Handlers:
    def __init__(self, todos):
        self._extract = TodoIntentHandlers._extract_todo_id
        self._todos = todos
        outer = self

        class _Svc:
            async def list_todos(self, user_id, include_completed=False):
                return list(outer._todos)

        self.todo_service = _Svc()

    def _extract_todo_id(self, message):
        return self._extract(self, message)


def _intent(message: str, targets=None) -> Intent:
    ctx = {"original_message": message}
    if targets is not None:
        ctx["inversion_args"] = {"targets": targets}
    return Intent(
        category=IntentCategory.EXECUTION,
        action="delete_todo",
        original_message=message,
        confidence=0.95,
        context=ctx,
    )


class TestPositionalOnly:
    @pytest.mark.parametrize("message", POSITIONAL)
    def test_positional_phrasings_name_nothing(self, message):
        named = _named_delete_target(message)
        assert named, "the seam's own guard relies on a non-empty candidate"
        assert _is_positional_only(named), (message, named)

    @pytest.mark.parametrize("message", NAMED)
    def test_named_phrasings_are_names(self, message):
        assert not _is_positional_only(_named_delete_target(message)), message

    def test_empty_is_not_positional(self):
        assert _is_positional_only("") is False


class TestGatePassesPositionsThrough:
    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize("message", POSITIONAL)
    async def test_positional_delete_is_a_passthrough_never_a_fuzzy_bind(self, message):
        gate = await build_todo_delete_confirmation(
            _intent(message), _Handlers(_webs_list()), _USER
        )
        assert gate.passthrough and gate.offer is None and gate.clarification is None, message

    async def test_webs_served_fail_shape_no_longer_binds_the_row_containing_two(self):
        """The exact 10-11 turn against the exact list shape: before the fix
        the gate armed 'Delete todo: "web check alpha two"?'."""
        gate = await build_todo_delete_confirmation(
            _intent("delete the first two reminders"), _Handlers(_webs_list()), _USER
        )
        assert gate.passthrough
        assert gate.offer is None

    async def test_named_leg_still_binds_a_real_name(self):
        gate = await build_todo_delete_confirmation(
            _intent("delete my budget review reminder"), _Handlers(_webs_list()), _USER
        )
        assert gate.offer is not None and not gate.passthrough
        assert "send the budget review to finance" in (gate.offer.question or "")

    async def test_numbered_delete_still_uses_the_number_leg(self):
        gate = await build_todo_delete_confirmation(
            _intent("delete todo 2"), _Handlers(_webs_list()), _USER
        )
        assert gate.offer is not None and not gate.passthrough
        assert "send the budget review to finance" in (gate.offer.question or "")


class TestThenTheTargetsHookOwnsTheTurn:
    """After the passthrough, the rail entry point reaches
    handle_delete_todo_targets with the router's positions."""

    @pytest.fixture
    def four(self):
        return _webs_list()

    @pytest.fixture
    def handlers(self, four):
        h = TodoIntentHandlers()
        h.todo_service = AsyncMock()
        h.todo_service.list_todos = AsyncMock(return_value=four)
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

    @pytest.mark.asyncio
    async def test_first_two_against_the_numbered_list_names_exactly_those_two(
        self, handlers, offers, session_ctx, four
    ):
        """Resolution unchanged (exactly rows 1 and 2 of the list shown);
        issue 2019 caps the turn: nothing armed, CXO's capped reply."""
        session_ctx.last_numbered_list = NumberedList(
            kind="reminders", ids=[t.id for t in four], texts=[t.text for t in four]
        )
        out = await handlers.handle_delete_todo_targets(
            _intent("delete the first two reminders", targets=["1-2"]), "s1", uuid4(), offers, "u"
        )
        assert out is not None
        msg, armed = out
        assert armed is False
        assert msg.startswith("I can delete one reminder at a time for now."), msg
        assert '1. "revise the pr"' in msg
        assert '2. "send the budget review to finance"' in msg
        assert "web check alpha" not in msg, msg
        handlers.todo_service.delete_todo.assert_not_awaited()
        offers.set_pending_offer.assert_not_called()

    @pytest.mark.asyncio
    async def test_first_two_with_no_numbered_list_shown_asks_honestly_and_numbers_the_list(
        self, handlers, offers, session_ctx
    ):
        out = await handlers.handle_delete_todo_targets(
            _intent("delete the first two reminders", targets=["1-2"]), "s1", uuid4(), offers, "u"
        )
        assert out is not None
        msg, armed = out
        assert armed is False
        # Issue 2046 (CXO): the list, numbered and bound, never "no number 1-2";
        # the 2019 cap sentence because two were asked.
        assert msg.startswith(
            "I haven't shown you a numbered list yet. Here are your reminders:\n\n"
        ), msg
        assert '\n1. "revise the pr"\n' in msg
        assert msg.endswith("\n\nI can delete one at a time for now. Tell me which one.")
        assert "no number" not in msg
        handlers.todo_service.delete_todo.assert_not_awaited()
