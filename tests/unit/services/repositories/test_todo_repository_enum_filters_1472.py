"""#1472: raw TodoStatus/TodoPriority enum comparisons against String columns.

`todo_items.status` / `todo_items.priority` are String columns ("Changed from
Enum to String") — binding a raw enum member raises asyncpg DataError
("expected str, got TodoStatus"), which each call site's try/except converts
into a degraded/failed lookup. Silent in production.

These tests pin the REPOSITORY half of the class without a DB: they capture
the SELECT each method builds and assert every bound literal destined for the
status/priority columns is a plain str, never an enum member. (The
canonical-handlers half is pinned by the integration round-trip in
tests/integration/test_retrospective_todos_1472.py and structurally by the
AST guard in tests/test_architecture_enforcement.py.)
"""

from unittest.mock import MagicMock

from sqlalchemy.sql import visitors
from sqlalchemy.sql.elements import BindParameter

from services.repositories.todo_repository import TodoRepository
from services.shared_types import TodoPriority, TodoStatus


class _CaptureSession:
    """Fake AsyncSession: records the query, returns an empty result."""

    def __init__(self):
        self.queries = []

    async def execute(self, query):
        self.queries.append(query)
        result = MagicMock()
        result.scalars.return_value.all.return_value = []
        result.scalar_one_or_none.return_value = None
        return result


def _enum_binds(query):
    """All bound literals in the WHERE clause that are raw enum members."""
    binds = [
        el.value
        for el in visitors.iterate(query.whereclause)
        if isinstance(el, BindParameter)
    ]
    return [v for v in binds if isinstance(v, (TodoStatus, TodoPriority))]


async def test_get_assigned_todos_status_filter_binds_str_not_enum():
    """Regression (#1472): get_assigned_todos bound the raw TodoStatus enum."""
    session = _CaptureSession()
    repo = TodoRepository(session)

    await repo.get_assigned_todos("user-1", status=TodoStatus.PENDING)

    assert len(session.queries) == 1
    offenders = _enum_binds(session.queries[0])
    assert offenders == [], (
        f"get_assigned_todos bound raw enum member(s) {offenders} against the "
        f"String-typed status column — asyncpg raises DataError "
        f"('expected str, got TodoStatus') at execution time (#1472)."
    )


async def test_get_due_todos_completed_exclusion_binds_str_not_enum():
    """Regression (#1472): get_due_todos compared status != TodoStatus.COMPLETED raw."""
    session = _CaptureSession()
    repo = TodoRepository(session)

    await repo.get_due_todos("user-1")

    assert len(session.queries) == 1
    offenders = _enum_binds(session.queries[0])
    assert offenders == [], (
        f"get_due_todos bound raw enum member(s) {offenders} against the "
        f"String-typed status column (#1472)."
    )


async def test_get_todos_by_owner_filters_still_bind_str():
    """#1460's fix (status/priority via .value) must not regress."""
    session = _CaptureSession()
    repo = TodoRepository(session)

    await repo.get_todos_by_owner(
        "user-1", status=TodoStatus.PENDING, priority=TodoPriority.HIGH
    )

    assert len(session.queries) == 1
    assert _enum_binds(session.queries[0]) == []
