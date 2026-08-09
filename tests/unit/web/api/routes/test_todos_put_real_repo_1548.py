"""#1548 — PUT /api/v1/todos/{id} must call the REAL TodoRepository.update_todo.

The route called ``todo_repo.update_todo(todo_obj)`` — an imagined signature
that passes a mutated domain object as the only argument. The real repository
method (services/repositories/todo_repository.py) is::

    async def update_todo(self, todo_id: str, updates: Dict, owner_id: str,
                          is_admin: bool = False) -> Optional[domain.Todo]

so against the real repo every PUT raised TypeError (missing ``updates`` /
``owner_id``), was swallowed by the generic except, and surfaced as a 500.
The existing suite never caught it because its mocks were hand-rolled to the
imagined interface (the exact #1541 delete-lie pattern: tests scripted against
an interface that doesn't exist).

These tests use ``create_autospec(TodoRepository)`` — the mock enforces the
REAL class's method signatures, so a route calling the imagined shape fails
here the same way it fails in production. Layer: route function with a
signature-faithful repo double (no DB); the repo's own behavior is covered by
tests/unit/services/repositories/ and integration suites.
"""

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import create_autospec

import pytest
from fastapi import HTTPException

from services.repositories.todo_repository import TodoRepository
from web.api.routes.todos import update_todo

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
        updated_at=datetime(2026, 8, 9, 12, 30, tzinfo=timezone.utc),
        due_date=None,
    )
    base.update(overrides)
    return SimpleNamespace(**base)


def _real_repo():
    """A repo double that enforces TodoRepository's REAL method signatures."""
    return create_autospec(TodoRepository, instance=True)


async def test_put_calls_real_update_todo_signature():
    """The route must call update_todo(todo_id, updates, owner_id=...).

    Red before the #1548 fix: the route's update_todo(todo_obj) call violates
    the autospec'd signature (TypeError), the generic except converts it to a
    500 — exactly the production failure shape.
    """
    repo = _real_repo()
    repo.get_todo_by_id.return_value = _stored_todo()
    repo.update_todo.return_value = _stored_todo(title="Renamed", priority="high")

    out = await update_todo(
        todo_id="t1",
        title="Renamed",
        # Direct call: FastAPI isn't resolving params, so the Query(None)
        # default sentinel must be supplied as the None production delivers.
        todo_status=None,
        priority="high",
        current_user=CLAIMS,
        todo_repo=repo,
    )

    # Domain model stores the title in `text` (title is a property), and the
    # repository routes `text` to the parent ItemDB table — the updates dict
    # must speak the repo's field names.
    repo.update_todo.assert_awaited_once_with(
        "t1", {"text": "Renamed", "priority": "high"}, owner_id="user-abc"
    )
    assert out["title"] == "Renamed"
    assert out["priority"] == "high"


async def test_put_status_and_description_flow_into_updates_dict():
    repo = _real_repo()
    repo.get_todo_by_id.return_value = _stored_todo()
    repo.update_todo.return_value = _stored_todo(status="in_progress", description="d")

    out = await update_todo(
        todo_id="t1",
        description="d",
        todo_status="in_progress",
        current_user=CLAIMS,
        todo_repo=repo,
    )

    repo.update_todo.assert_awaited_once_with(
        "t1", {"description": "d", "status": "in_progress"}, owner_id="user-abc"
    )
    assert out["status"] == "in_progress"


async def test_put_missing_todo_is_404_and_never_reaches_update():
    repo = _real_repo()
    repo.get_todo_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        await update_todo(todo_id="nope", title="x", current_user=CLAIMS, todo_repo=repo)

    assert exc.value.status_code == 404
    repo.update_todo.assert_not_awaited()


async def test_put_repo_refusal_is_an_honest_500_not_fake_success():
    """Ownership pre-check passed but update_todo returned None — the route
    must not fabricate a success payload (mirrors the #1541 complete route)."""
    repo = _real_repo()
    repo.get_todo_by_id.return_value = _stored_todo()
    repo.update_todo.return_value = None

    with pytest.raises(HTTPException) as exc:
        await update_todo(todo_id="t1", title="x", current_user=CLAIMS, todo_repo=repo)

    assert exc.value.status_code == 500
