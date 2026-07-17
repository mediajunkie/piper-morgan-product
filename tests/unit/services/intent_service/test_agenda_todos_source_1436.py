"""#1436 (B12 family): _get_todays_todos must read domain.Todo's real fields.

Regression: the agenda's todo source read `.title` (domain.Todo has `.text`)
and `.priority.value` (priority is a plain str) — AttributeError on every todo,
swallowed into the #1425 None sentinel, so the agenda's Tasks section ALWAYS
rendered "couldn't check" even with real pending todos. Honest, but permanently
dead — the exact stopped-at-symptom shape this sprint exists to close.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from services.domain.models import Todo
from services.intent_service.canonical_handlers import CanonicalHandlers


async def test_real_todos_reach_the_agenda_dicts():
    todos = [
        Todo(text="Review the Q3 roadmap", priority="high"),
        Todo(text="Reply to Sam", priority="medium",
             due_date=datetime(2026, 7, 18, 17, 0, tzinfo=timezone.utc)),
    ]
    with patch(
        "services.repositories.todo_repository.TodoRepository.get_todos_by_owner",
        new=AsyncMock(return_value=todos),
    ):
        out = await CanonicalHandlers()._get_todays_todos(session_id=str(uuid4()))

    # Old code: AttributeError -> swallow -> None (source-failed). Now: real dicts.
    assert out is not None and len(out) == 2
    assert out[0]["title"] == "Review the Q3 roadmap"  # sourced from .text
    assert out[0]["priority"] == "high"  # plain str, no .value
    assert out[1]["due_date"].startswith("2026-07-18")


async def test_formatter_renders_the_tasks_section_from_these_dicts():
    todos = [
        Todo(text="Ship the fix", priority="high"),
    ]
    with patch(
        "services.repositories.todo_repository.TodoRepository.get_todos_by_owner",
        new=AsyncMock(return_value=todos),
    ):
        dicts = await CanonicalHandlers()._get_todays_todos(session_id=str(uuid4()))
    msg = CanonicalHandlers()._format_agenda_standard(None, dicts, [])
    assert "Ship the fix" in msg
    assert "No pending tasks" not in msg
    assert "couldn't check" not in msg.lower()
