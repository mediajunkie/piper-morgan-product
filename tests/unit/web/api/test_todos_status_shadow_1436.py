"""#1436 B5: update_todo's error branches must raise HTTPException, not AttributeError.

Regression: the route had a query parameter literally named ``status``, which
shadowed the ``starlette.status`` module inside the function body — so every
error branch (``status.HTTP_404_NOT_FOUND`` etc.) raised AttributeError
('str'/'NoneType' has no attribute ...) and surfaced as a raw 500 instead of
the intended 404/400. Param renamed to ``todo_status`` with ``alias="status"``
so the public API is unchanged.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from web.api.routes.todos import update_todo

CLAIMS = SimpleNamespace(sub="user-abc")


async def test_missing_todo_renders_404_not_attributeerror():
    repo = SimpleNamespace(get_todo_by_id=AsyncMock(return_value=None))
    with pytest.raises(HTTPException) as exc:
        await update_todo(
            todo_id="nope",
            todo_status="done",  # a string in the old shadow slot
            current_user=CLAIMS,
            todo_repo=repo,
        )
    assert exc.value.status_code == 404


async def test_empty_title_renders_400():
    todo = SimpleNamespace(title="old", description="", status="pending", priority="medium")
    repo = SimpleNamespace(get_todo_by_id=AsyncMock(return_value=todo))
    with pytest.raises(HTTPException) as exc:
        await update_todo(
            todo_id="t1",
            title="   ",
            current_user=CLAIMS,
            todo_repo=repo,
        )
    assert exc.value.status_code == 400


async def test_status_update_still_flows_through_the_alias_param():
    todo = SimpleNamespace(
        title="t",
        description="",
        status="pending",
        priority="medium",
        id="t1",
        owner_id="user-abc",
        updated_at=None,
    )
    repo = SimpleNamespace(
        get_todo_by_id=AsyncMock(return_value=todo),
        update_todo=AsyncMock(return_value=todo),
    )
    out = await update_todo(
        todo_id="t1",
        todo_status="completed",
        current_user=CLAIMS,
        todo_repo=repo,
    )
    assert todo.status == "completed"
    assert out["id"] == "t1"
