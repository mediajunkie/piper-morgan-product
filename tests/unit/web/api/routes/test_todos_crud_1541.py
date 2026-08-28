"""#1541 — /todos page CRUD honesty: complete route + due_date persistence.

PM live-tested the /todos page (2026-08-09) and found:
- no completion control existed anywhere in the CRUD surface;
- the page's create dialog SENDS due_date, but CreateTodoRequest had no such
  field — Pydantic silently dropped it, so page-created due dates never
  persisted (and therefore could never reach /standup);
- the list/create responses never returned due_date, so the template's
  `${todo.due_date ? ...}` render branch was dead code.

These tests pin the API half of the fix at the route layer (mocked repo,
same style as test_todos_status_shadow_1436.py). The repo methods asserted
against here (`complete_todo(todo_id, owner_id=...)`) are the REAL
TodoRepository signatures — this suite exists because earlier tests were
scripted against imagined interfaces.
"""

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from web.api.routes.todos import (
    CreateTodoRequest,
    complete_todo,
    create_todo,
    list_todos,
)

CLAIMS = SimpleNamespace(sub="user-abc")


def _stored_todo(**overrides):
    base = dict(
        id="t1",
        title="Ship it",
        description="",
        status="pending",
        priority="medium",
        completed=False,
        completed_at=None,
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


# --- due_date persistence (create) -----------------------------------------


async def test_create_passes_due_date_through_to_domain_todo():
    """The page sends {title, due_date}; due_date must reach the domain Todo."""
    captured = {}

    async def capture_create(todo):
        captured["todo"] = todo
        return _stored_todo(due_date=todo.due_date)

    repo = SimpleNamespace(create_todo=AsyncMock(side_effect=capture_create))
    out = await create_todo(
        request=CreateTodoRequest(title="Ship it", due_date="2026-08-09"),
        current_user=CLAIMS,
        todo_repo=repo,
    )
    assert captured["todo"].due_date is not None, (
        "due_date was dropped at the API boundary (#1541 root: CreateTodoRequest "
        "had no due_date field, Pydantic silently ignored the page's value)"
    )
    assert captured["todo"].due_date.date().isoformat() == "2026-08-09"
    # And the response echoes it so the page can render what was saved
    assert out["due_date"] is not None
    assert out["due_date"].startswith("2026-08-09")


async def test_create_without_due_date_still_works():
    repo = SimpleNamespace(create_todo=AsyncMock(return_value=_stored_todo()))
    out = await create_todo(
        request=CreateTodoRequest(title="Ship it"),
        current_user=CLAIMS,
        todo_repo=repo,
    )
    assert out["due_date"] is None


async def test_create_rejects_garbage_due_date_with_400():
    repo = SimpleNamespace(create_todo=AsyncMock())
    with pytest.raises(HTTPException) as exc:
        await create_todo(
            request=CreateTodoRequest(title="Ship it", due_date="not-a-date"),
            current_user=CLAIMS,
            todo_repo=repo,
        )
    assert exc.value.status_code == 400
    repo.create_todo.assert_not_awaited()


async def test_list_response_includes_due_date():
    """The template renders todo.due_date; the list payload must carry it."""
    due = datetime(2026, 8, 9, 23, 59, tzinfo=timezone.utc)
    repo = SimpleNamespace(get_todos_by_owner=AsyncMock(return_value=[_stored_todo(due_date=due)]))
    out = await list_todos(current_user=CLAIMS, todo_repo=repo)
    assert out["todos"][0]["due_date"] is not None
    assert out["todos"][0]["due_date"].startswith("2026-08-09")


# --- complete route (did not exist before #1541) ----------------------------


async def test_complete_missing_todo_renders_404():
    repo = SimpleNamespace(
        get_todo_by_id=AsyncMock(return_value=None),
        complete_todo=AsyncMock(),
    )
    with pytest.raises(HTTPException) as exc:
        await complete_todo(todo_id="nope", current_user=CLAIMS, todo_repo=repo)
    assert exc.value.status_code == 404
    repo.complete_todo.assert_not_awaited()


async def test_complete_calls_real_repo_signature_and_reports_completed():
    """complete_todo(todo_id, owner_id=...) is the REAL TodoRepository shape."""
    done = _stored_todo(
        status="completed",
        completed=True,
        completed_at=datetime(2026, 8, 9, 15, 0, tzinfo=timezone.utc),
    )
    repo = SimpleNamespace(
        get_todo_by_id=AsyncMock(return_value=_stored_todo()),
        complete_todo=AsyncMock(return_value=done),
    )
    out = await complete_todo(todo_id="t1", current_user=CLAIMS, todo_repo=repo)
    repo.complete_todo.assert_awaited_once_with("t1", owner_id="user-abc")
    assert out["status"] == "completed"
    assert out["completed"] is True
    assert out["completed_at"] is not None


async def test_complete_repo_refusal_is_an_honest_500_not_fake_success():
    """If the repo can't complete an existing todo, the route must not claim it did."""
    repo = SimpleNamespace(
        get_todo_by_id=AsyncMock(return_value=_stored_todo()),
        complete_todo=AsyncMock(return_value=None),
    )
    with pytest.raises(HTTPException) as exc:
        await complete_todo(todo_id="t1", current_user=CLAIMS, todo_repo=repo)
    assert exc.value.status_code == 500
