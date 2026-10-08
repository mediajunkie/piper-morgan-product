"""#1914 — complete_todo swallows a trailing no-op clause as the target.

PM live, alpha v156, 2026-10-01, after the floor flagged two due reminders
and offered "If you'd like me to mark those complete, just tell me
directly":

    X: Mark the first one complete and leave the second one pending.
    P: I couldn't find a todo matching 'and leave the second one pending.'.
       Try 'show my todos' to see your list, then 'complete todo [number]'.

Two defects, both Lead's to fix (CXO owns arming the floor's own "those"
offer, out of scope here):

  1. The completion-text extractor took the WHOLE tail — including the
     conjunction and a second clause that is an explicit no-op — as the
     target. Fix: split at an unquoted clause boundary ("and"/"but"/"then"
     + a no-op/imperative verb) BEFORE any extraction runs
     (``_split_completion_clause``). A quoted/named todo title containing
     "and" is never split.
  2. "the first one" never bound to anything — the fuzzy text matcher has
     no todo whose words overlap "first one". Fix: when the target is
     ordinal/positional, bind it by POSITION against the due-reminder
     candidates (the same list the floor's "flagging N reminders" copy
     renders from) via the #1906 pick-target binder
     (``reminder_clear._resolve_pick_target`` — reused, not reimplemented).

Layer honesty (m-43): these are handler-level unit tests against
``TodoIntentHandlers.handle_complete_todo`` with ``todo_service`` mocked —
the same idiom ``test_todo_completion_lifecycle.py`` (#904) uses. No LLM
call, no live DB.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from services.domain.models import Intent, IntentCategory, Todo
from services.intent_service.todo_handlers import (
    TodoIntentHandlers,
    _split_completion_clause,
)

_NOW = datetime.now(timezone.utc)


def _due_reminder(text: str, minutes_ago: int = 30) -> Todo:
    t = Todo(text=text, priority="medium")
    t.id = str(uuid4())
    t.reminder_date = _NOW - timedelta(minutes=minutes_ago)
    t.completed = False
    return t


# ============================================================================
# 1. Pure clause-splitting helper
# ============================================================================


class TestSplitCompletionClause:
    def test_and_leave_boundary(self):
        head, tail = _split_completion_clause(
            "Mark the first one complete and leave the second one pending."
        )
        assert head == "Mark the first one complete"
        assert tail == "leave the second one pending."

    def test_but_leave_boundary_no_and(self):
        head, tail = _split_completion_clause(
            "complete the first one, but leave the second pending"
        )
        assert head == "complete the first one"
        assert tail == "leave the second pending"

    def test_number_based_with_tail(self):
        head, tail = _split_completion_clause("complete todo 1 and leave todo 2 pending")
        assert head == "complete todo 1"
        assert tail == "leave todo 2 pending"

    def test_quoted_title_with_and_not_split(self):
        """A quoted title containing 'and <trigger verb>' keeps its 'and' —
        the boundary must fall OUTSIDE any quoted span."""
        msg = "mark 'remember to water the plants and leave extra food' done"
        head, tail = _split_completion_clause(msg)
        assert head == msg
        assert tail is None

    def test_quoted_title_and_ship_not_split(self):
        """The task-card example: 'and ship it' isn't a no-op trigger verb
        at all, so this never split even before the quote guard — pinned
        so a future widening of the verb vocabulary can't regress it."""
        msg = 'mark "review the PR and ship it" done'
        head, tail = _split_completion_clause(msg)
        assert head == msg
        assert tail is None

    def test_plain_message_no_boundary(self):
        head, tail = _split_completion_clause("complete the PR review")
        assert head == "complete the PR review"
        assert tail is None


# ============================================================================
# 2. handle_complete_todo — clause split + ordinal binding, end to end
# ============================================================================


class TestCompleteTodoClauseSplitAndOrdinalBinding:
    @pytest.fixture
    def handlers(self):
        h = TodoIntentHandlers()
        h.todo_service = AsyncMock()
        return h

    @pytest.fixture
    def two_due_reminders(self):
        return [
            _due_reminder("Check the test card", minutes_ago=90),
            _due_reminder("Review the changelog", minutes_ago=30),
        ]

    def _intent(self, message: str) -> Intent:
        return Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message=message,
            confidence=0.9,
        )

    # #1943 step 6 (2026-10-08): the #1914 ordinal binder is RETIRED — complete_todo is
    # live, so the ROUTER names targets ("the first one" → targets ["1"]) and
    # handle_complete_todo_targets resolves them against the numbered list last shown
    # (test_complete_todo_router_targets_1943.py pins that path, and it passed LIVE on
    # alpha 10-07 with PM's own sentence). This legacy handler runs only when the router
    # named no targets; an ordinal here completes NOTHING and says so honestly.
    @pytest.mark.parametrize(
        "message",
        [
            "Mark the first one complete and leave the second one pending.",
            "complete the last one",
            "complete #2",
        ],
    )
    @pytest.mark.asyncio
    async def test_ordinal_on_the_legacy_path_completes_nothing_and_says_so(
        self, handlers, two_due_reminders, message
    ):
        handlers.todo_service.list_todos = AsyncMock(return_value=two_due_reminders)
        handlers.todo_service.complete_todo = AsyncMock()

        result = await handlers.handle_complete_todo(self._intent(message), "session1", uuid4())

        handlers.todo_service.complete_todo.assert_not_called()
        assert "couldn't find" in result.lower()
        assert "show my todos" in result.lower()

    @pytest.mark.asyncio
    async def test_quoted_title_with_and_is_not_split_and_still_completes(self, handlers):
        """'mark "review the PR and ship it" done' keeps its title intact
        and still resolves via fuzzy matching — the clause split never
        touches it."""
        todo = Todo(text="review the PR and ship it", priority="medium")
        todo.id = str(uuid4())
        handlers.todo_service.list_todos = AsyncMock(return_value=[todo])
        completed = Todo(text=todo.text, status="completed", completed=True)
        handlers.todo_service.complete_todo = AsyncMock(return_value=completed)

        intent = self._intent('mark "review the PR and ship it" done')
        result = await handlers.handle_complete_todo(intent, "session1", uuid4())

        handlers.todo_service.complete_todo.assert_called_once()
        assert "left the other one as is" not in result.lower()

    @pytest.mark.asyncio
    async def test_existing_text_completion_unaffected(self, handlers):
        """No clause boundary, no ordinal shape: behavior is byte-identical
        to the pre-#1914 path (#904 regression guard)."""
        todo = Todo(text="Review the PR for auth module", priority="medium")
        todo.id = str(uuid4())
        handlers.todo_service.list_todos = AsyncMock(return_value=[todo])
        completed = Todo(text=todo.text, status="completed", completed=True)
        handlers.todo_service.complete_todo = AsyncMock(return_value=completed)

        intent = self._intent("complete the PR review")
        result = await handlers.handle_complete_todo(intent, "session1", uuid4())

        handlers.todo_service.complete_todo.assert_called_once()
        assert "left the other one as is" not in result.lower()
