"""
Tests for #1096 slice 2 Pattern-073 fixes — templated empty-state copy that
overclaims relative to what the underlying logic actually verified.

Slice 1 (#1096) fixed:
- _handle_stale_prs
- _handle_shipped_this_week
- _handle_recurring_meetings_query
- _handle_week_calendar_query

Slice 2 (this file) covers:
- Q32: handle_create_reminder confirmation copy (reminder is surfaced via
  context_assembler passively, not actively push-notified)
- _format_empty_list_conscious empty-todo-list copy ("your mind is clear"
  was a categorical claim beyond verified knowledge of the DB)
"""

import inspect
from pathlib import Path

import pytest


@pytest.fixture
def todo_handlers_source() -> str:
    return Path("services/intent_service/todo_handlers.py").read_text()


@pytest.fixture
def todo_consciousness_source() -> str:
    return Path("services/consciousness/todo_consciousness.py").read_text()


# Q32 reminder copy -------------------------------------------------------


def test_reminder_copy_does_not_promise_active_notification(
    todo_handlers_source: str,
) -> None:
    """Pattern-073: 'I'll remind you to X' implied active push notification
    but the system surfaces reminders passively via context_assembler at
    next-conversation time. The new copy must describe the actual mechanism.
    """
    assert (
        "I'll remind you to" not in todo_handlers_source
    ), "Old copy promised active notification that the system doesn't deliver"


def test_reminder_copy_describes_passive_surfacing(
    todo_handlers_source: str,
) -> None:
    """The replacement copy describes the actual surfacing mechanism (passive,
    in conversation once the reminder is due). #1566 aligned the wording with
    the widened mechanism: any floor-bound (conversational) turn surfaces due
    reminders, but action commands still don't — so 'in conversation', not
    'the next time you check in' (which over-promised turn coverage).
    #1569 folded the clause into the reminders-are-todos teaching sentence
    ('...and I'll surface it in conversation once it's due') — 'this' became
    'it'; the mechanism claim is unchanged."""
    assert (
        "surface it in conversation once it's due" in todo_handlers_source
    ), "New copy must describe the passive surfacing mechanism"


def test_reminder_copy_uses_saved_not_promise_verb(
    todo_handlers_source: str,
) -> None:
    """'Reminder saved' is verifiable (we did save the todo with a
    reminder_date); 'I'll remind you' is a promise of future behavior."""
    assert "Reminder saved" in todo_handlers_source


# Empty todo-list copy ----------------------------------------------------


def test_empty_todo_list_drops_universal_mind_claim() -> None:
    """Pattern-073: 'your mind is clear' is a categorical claim that goes
    beyond the system's bounded knowledge of 'DB returned 0 todos'.

    The discipline check is on the *returned string* (what the user sees),
    not on the source file (which may legitimately reference the old copy
    in docstrings/comments as part of the discipline note)."""
    from services.consciousness.todo_consciousness import _format_empty_list_conscious

    rendered = _format_empty_list_conscious()
    assert "your mind is clear" not in rendered, (
        "Pattern-073 violation: empty-todo-list copy must not render " "'mind is clear' to user"
    )


def test_empty_todo_list_describes_bounded_observation() -> None:
    """Replacement copy describes the bounded observation: 'list is empty'."""
    from services.consciousness.todo_consciousness import _format_empty_list_conscious

    rendered = _format_empty_list_conscious()
    assert "checked your todo list and it's empty" in rendered


def test_empty_todo_list_keeps_actionable_guidance() -> None:
    """The replacement copy retains the actionable next-step prompt."""
    from services.consciousness.todo_consciousness import _format_empty_list_conscious

    rendered = _format_empty_list_conscious()
    assert "add todo:" in rendered


# Documentation-of-discipline tests ---------------------------------------


def test_empty_list_formatter_documents_pattern_073_reason(
    todo_consciousness_source: str,
) -> None:
    """Per Pattern-073 discipline + close-issue-properly: the WHY is
    captured in the docstring so future readers don't re-introduce the
    over-claim under good intent."""
    # Find the function definition + check the docstring
    from services.consciousness import todo_consciousness

    source = inspect.getsource(todo_consciousness._format_empty_list_conscious)
    assert "#1096" in source, "Docstring must cite #1096"
    assert "Pattern-073" in source, "Docstring must cite the discipline"


def test_reminder_handler_documents_pattern_073_reason(
    todo_handlers_source: str,
) -> None:
    """The reminder handler's new copy includes a comment explaining the
    discipline (so a future agent doesn't restore the 'I'll remind you' phrasing)."""
    assert (
        "#1096 slice 2" in todo_handlers_source
    ), "Reminder handler change must cite #1096 slice 2"
    assert "Pattern-073" in todo_handlers_source, "Reminder handler change must cite Pattern-073"
