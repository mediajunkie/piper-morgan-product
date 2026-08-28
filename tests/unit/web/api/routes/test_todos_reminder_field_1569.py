"""#1569 — the list payload must make reminder rows DISTINGUISHABLE.

Verified before writing (the honest answer the issue asked for): reminders
are todos with reminder_date set (unified model — handle_create_reminder
saves via todo_service.create_todo with reminder_date AND due_date), and
TodoDB.to_domain carries reminder_date onto every domain.Todo the repo
returns — but GET /api/v1/todos serialized only due_date. Since the handler
sets due_date equal to reminder_date, due_date alone CANNOT distinguish a
reminder from a due-dated todo: the field must be threaded through the list
response, never inferred from title text.

Layer: route function with a mocked repo (the test_todos_crud_1541.py /
test_todos_priority_passthrough_1512.py style). The fixture mirrors the real
domain.Todo shape, which always has a reminder_date attribute.
"""

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock

from web.api.routes.todos import list_todos

CLAIMS = SimpleNamespace(sub="user-abc")


def _stored_todo(**overrides):
    base = dict(
        id="t1",
        title="Ship it",
        description="",
        status="pending",
        priority="medium",
        owner_id="user-abc",
        created_at=datetime(2026, 8, 10, 12, 0, tzinfo=timezone.utc),
        updated_at=None,
        due_date=None,
        reminder_date=None,
        lifecycle_state=None,
    )
    base.update(overrides)
    return SimpleNamespace(**base)


async def test_list_response_carries_reminder_date_for_reminder_rows():
    """renderTodos keys the #1569 reminder identity (chip + grouping) off
    reminder_date; the list payload must carry it as aware ISO."""
    when = datetime(2026, 8, 11, 15, 0, tzinfo=timezone.utc)
    repo = SimpleNamespace(
        get_todos_by_owner=AsyncMock(return_value=[_stored_todo(reminder_date=when, due_date=when)])
    )
    out = await list_todos(current_user=CLAIMS, todo_repo=repo)
    row = out["todos"][0]
    assert "reminder_date" in row, (
        "list payload has no reminder_date — reminder rows are "
        "indistinguishable from due-dated todos (due_date is set to the same "
        "value on the reminder create path)"
    )
    assert row["reminder_date"] == when.isoformat()


async def test_plain_todos_carry_reminder_date_none():
    """A plain todo says so honestly: reminder_date present and null — the
    page's filter (t.reminder_date) must see falsy, not undefined-by-omission
    on some rows and a value on others."""
    repo = SimpleNamespace(get_todos_by_owner=AsyncMock(return_value=[_stored_todo()]))
    out = await list_todos(current_user=CLAIMS, todo_repo=repo)
    row = out["todos"][0]
    assert "reminder_date" in row
    assert row["reminder_date"] is None


async def test_due_dated_todo_without_reminder_is_not_marked():
    """The exact confusable case: due_date set, reminder_date not — must NOT
    read as a reminder."""
    due = datetime(2026, 8, 12, 0, 0, tzinfo=timezone.utc)
    repo = SimpleNamespace(get_todos_by_owner=AsyncMock(return_value=[_stored_todo(due_date=due)]))
    out = await list_todos(current_user=CLAIMS, todo_repo=repo)
    row = out["todos"][0]
    assert row["due_date"] is not None
    assert row["reminder_date"] is None
