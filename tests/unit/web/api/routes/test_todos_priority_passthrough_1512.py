"""#1512 — priority must survive the API boundary (the due_date drop-check).

#1541 found CreateTodoRequest silently dropped due_date (no field on the
Pydantic model → value discarded, no error). #1512 asked the same question of
priority now that the page's Add form sends it. Answer: priority was ALREADY
declared on CreateTodoRequest (`priority: Optional[str] = "medium"`) and
threaded into the domain Todo — no silent drop. These tests pin that so a
future model edit can't quietly reintroduce the due_date failure shape for
priority.

Layer: route function with a mocked repo capturing the domain object (same
style as tests/unit/web/api/routes/test_todos_crud_1541.py).
"""

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock

from web.api.routes.todos import CreateTodoRequest, create_todo, list_todos

CLAIMS = SimpleNamespace(sub="user-abc")


def _stored_todo(**overrides):
    base = dict(
        id="t1",
        title="Ship it",
        description="",
        status="pending",
        priority="medium",
        owner_id="user-abc",
        created_at=datetime(2026, 8, 9, 12, 0, tzinfo=timezone.utc),
        updated_at=None,
        due_date=None,
        # #1569: the list route now serializes reminder_date (real
        # domain.Todo always has the attribute; the mock mirrors it).
        reminder_date=None,
        lifecycle_state=None,
    )
    base.update(overrides)
    return SimpleNamespace(**base)


async def test_create_passes_priority_through_to_domain_todo():
    """The page now sends {title, priority}; priority must reach the domain
    Todo AND echo back in the response."""
    captured = {}

    async def capture_create(todo):
        captured["todo"] = todo
        return _stored_todo(priority=todo.priority)

    repo = SimpleNamespace(create_todo=AsyncMock(side_effect=capture_create))
    out = await create_todo(
        request=CreateTodoRequest(title="Ship it", priority="high"),
        current_user=CLAIMS,
        todo_repo=repo,
    )
    assert captured["todo"].priority == "high", (
        "priority was dropped at the API boundary — the due_date silent-drop "
        "shape (#1541) has recurred for priority"
    )
    assert out["priority"] == "high"


async def test_create_without_priority_defaults_to_medium():
    captured = {}

    async def capture_create(todo):
        captured["todo"] = todo
        return _stored_todo(priority=todo.priority)

    repo = SimpleNamespace(create_todo=AsyncMock(side_effect=capture_create))
    out = await create_todo(
        request=CreateTodoRequest(title="Ship it"),
        current_user=CLAIMS,
        todo_repo=repo,
    )
    assert captured["todo"].priority == "medium"
    assert out["priority"] == "medium"


async def test_list_response_carries_priority_for_the_page():
    """renderTodos consumes the list payload; priority must be in it."""
    repo = SimpleNamespace(
        get_todos_by_owner=AsyncMock(return_value=[_stored_todo(priority="urgent")])
    )
    out = await list_todos(current_user=CLAIMS, todo_repo=repo)
    assert out["todos"][0]["priority"] == "urgent"
