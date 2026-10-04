"""#1930 (CXO's 2026-10-04 ruling §1): complete_todo — an explicit
completion of a named item does not deserve a "shall I?", but an
AMBIGUOUS text target (more than one plausible match) DOES ask which one
— disambiguation, not consent, and separate from the #1190 gate.

Reuses the SAME resolver the delete gate already asks with
(``resolve_named_todo_target``, ``destructive_confirm.py``'s named-target
leg) rather than building a new picker (CXO: "check what exists today,
don't build a new picker if one exists").

Also pinned here (CXO's other two constraints, already true before this
change, re-verified so a regression shows up here too):
- the completion reply NAMES the todo it completed
  (``format_todo_completed_conscious``);
- the reply does not promise an undo from chat.
"""

from __future__ import annotations

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from services.domain.models import Intent, IntentCategory, Todo
from services.intent_service.todo_handlers import TodoIntentHandlers


def _todo(text):
    t = Todo(text=text, priority="medium")
    t.id = str(uuid4())
    return t


def _intent(message: str) -> Intent:
    return Intent(
        category=IntentCategory.EXECUTION,
        action="complete_todo",
        original_message=message,
        confidence=0.9,
    )


@pytest.fixture
def handlers():
    h = TodoIntentHandlers()
    h.todo_service = AsyncMock()
    return h


class TestAmbiguousTextTargetAsksWhich:
    @pytest.mark.asyncio
    async def test_two_fuzzy_matches_no_unique_exact_asks_which(self, handlers):
        """'hydrate' against two non-exact fuzzy matches: no unique exact
        title, so resolve_named_todo_target returns both — ask which,
        don't silently complete the top-scored one."""
        todos = [_todo("hydrate the plants"), _todo("hydrate the cat")]
        handlers.todo_service.list_todos = AsyncMock(return_value=todos)

        result = await handlers.handle_complete_todo(
            _intent("complete the hydrate todo"), "session1", uuid4()
        )

        assert "which one should i complete" in result.lower()
        assert "1." in result and "2." in result
        handlers.todo_service.complete_todo.assert_not_called()

    @pytest.mark.asyncio
    async def test_unique_exact_match_still_completes_without_asking(self, handlers):
        """'call mom' against ['call mom', 'call the dentist']: both score
        fuzzy, but the unique EXACT title wins outright — behaviour-
        preserving for the single-match case the old
        `_find_best_matching_todo` call already handled."""
        todos = [_todo("call mom"), _todo("call the dentist")]
        handlers.todo_service.list_todos = AsyncMock(return_value=todos)
        completed = Todo(text="call mom", status="completed", completed=True)
        handlers.todo_service.complete_todo = AsyncMock(return_value=completed)

        result = await handlers.handle_complete_todo(
            _intent("complete call mom"), "session1", uuid4()
        )

        handlers.todo_service.complete_todo.assert_called_once()
        assert "call mom" in result


class TestCompletionNamesTheItem:
    @pytest.mark.asyncio
    async def test_completion_reply_names_the_completed_todo(self, handlers):
        todos = [_todo("Review the PR for auth module")]
        handlers.todo_service.list_todos = AsyncMock(return_value=todos)
        completed = Todo(text=todos[0].text, status="completed", completed=True)
        handlers.todo_service.complete_todo = AsyncMock(return_value=completed)

        result = await handlers.handle_complete_todo(
            _intent("complete the PR review"), "session1", uuid4()
        )

        assert todos[0].text in result


class TestNoUndoPromised:
    @pytest.mark.asyncio
    async def test_completion_reply_never_promises_an_undo(self, handlers):
        todos = [_todo("Write quarterly report")]
        handlers.todo_service.list_todos = AsyncMock(return_value=todos)
        completed = Todo(text=todos[0].text, status="completed", completed=True)
        handlers.todo_service.complete_todo = AsyncMock(return_value=completed)

        result = await handlers.handle_complete_todo(
            _intent("complete todo 1"), "session1", uuid4()
        )

        lowered = result.lower()
        for phrase in ("undo", "reopen", "bring it back", "restore it"):
            assert phrase not in lowered
