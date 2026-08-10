"""#1569 — reminders ARE todos (unified model, PM-ratified): the save
confirmation must TEACH that relationship, not leave the user to discover it
by surprise on the Todos page.

PM's priority order for #1569 is explanation first, visual distinction second.
This file is the explanation half: one plain sentence appended to the #1562
confirmation copy telling the user where the reminder lives (with your todos,
visible on the Todos page) and how it comes back (surfaced in conversation
once due — the passive mechanism, per Pattern-073/#1096 slice 2).

Layer: real handler call (handle_create_reminder with a mocked todo_service),
asserting on the RETURNED message — the string the user actually receives —
not on source-file presence (that discipline half lives in
tests/unit/services/test_pattern_073_empty_state_copy_1096.py).

The #1562 copy (honest-ask, "(scheduled for ...)" with the leading-"at"
strip) was reworked the same day and must survive intact — pinned here as a
canary alongside the new sentence.
"""

import re
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.shared_types import IntentCategory


@pytest.fixture
def handlers():
    return TodoIntentHandlers()


async def _saved_reminder_message(handlers, message: str) -> str:
    """Run handle_create_reminder down the SAVE path (mocked todo_service)."""
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="create_reminder",
        context={"original_message": message},
    )
    mock_todo = Todo(
        id=str(uuid4()),
        text="review the pr",
        priority="medium",
        status="pending",
        completed=False,
    )
    with patch.object(
        handlers.todo_service,
        "create_todo",
        new_callable=AsyncMock,
        return_value=mock_todo,
    ) as mock_create:
        result = await handlers.handle_create_reminder(intent, "session-1", uuid4())
    assert mock_create.called, "test precondition: the save path must be taken"
    return result


@pytest.mark.asyncio
async def test_confirmation_teaches_that_the_reminder_lives_with_todos(handlers):
    """#1569 explanation-first: the message must say the reminder lives with
    the user's todos and names the Todos page as where to see it."""
    result = await _saved_reminder_message(
        handlers, "remind me tomorrow at 3pm to review the PR"
    )
    assert "lives with your todos" in result, (
        "confirmation never teaches the unified reminders-are-todos model — "
        f"the user meets it as a surprise on /todos instead: {result!r}"
    )
    assert "Todos page" in result, (
        f"confirmation does not name WHERE the reminder is visible: {result!r}"
    )


@pytest.mark.asyncio
async def test_confirmation_still_describes_passive_surfacing(handlers):
    """The Pattern-073 mechanism claim (surfaced in conversation once due,
    never an active-push promise) must survive the new sentence."""
    result = await _saved_reminder_message(
        handlers, "remind me tomorrow at 3pm to review the PR"
    )
    assert "in conversation once it's due" in result, (
        f"passive-surfacing mechanism claim went missing: {result!r}"
    )
    assert "I'll remind you to" not in result, (
        "active-notification promise reintroduced (Pattern-073 regression)"
    )


@pytest.mark.asyncio
async def test_1562_copy_survives_intact(handlers):
    """Canary: the same-day #1562 rework (verifiable 'Reminder saved', the
    '(scheduled for ...)' label with its leading-'at' strip) stays intact."""
    result = await _saved_reminder_message(
        handlers, "remind me tomorrow at 3pm to review the PR"
    )
    assert "Reminder saved" in result
    assert "(scheduled for " in result
    assert "for at " not in result, f"'(scheduled for at ...)' doublet: {result!r}"


@pytest.mark.asyncio
async def test_new_sentence_introduces_no_doubled_tokens(handlers):
    """test_reminders.py pins a no-doubled-token property on this message;
    assert it here too so THIS file fails first if the new sentence breaks it."""
    result = await _saved_reminder_message(
        handlers, "remind me tomorrow at 3pm to review the PR"
    )
    assert not re.search(r"\b(\w+)\s+\1\b", result.lower()), (
        f"Doubled token in confirmation copy: {result!r}"
    )
