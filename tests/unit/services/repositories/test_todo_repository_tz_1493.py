"""#1493: naive-local datetime class in the todo layer (repository writes/cutoffs).

The repository wrote naive LOCAL `datetime.now()` to timestamptz columns
(completed_at/updated_at) and used it as the recent/overdue cutoff — the same
timezone class as #1491's crash but the SQL-side shape: it can't raise the
Python TypeError, it silently drifts by the server's UTC offset and stores
ambiguous instants. `todo_management_service.py` already used aware-UTC for
the same columns; the repository predated that discipline.

These tests pin aware-UTC behavior WITHOUT wall-clock assertions: they assert
tz-awareness and a zero UTC offset on captured values (never "equals now").
An AST guard pins all named files at zero bare `datetime.now()` calls, with
the denominator (files checked) asserted per m-44.
"""

import ast
import os
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

from sqlalchemy.sql import visitors
from sqlalchemy.sql.elements import BindParameter

from services.repositories.todo_repository import TodoRepository


def _assert_aware_utc(value, label):
    assert isinstance(value, datetime), f"{label} should be a datetime, got {value!r}"
    assert value.tzinfo is not None, (
        f"{label} is NAIVE — the #1493 class: naive local time written to a "
        f"timestamptz column drifts by the server's UTC offset"
    )
    assert value.utcoffset() == timezone.utc.utcoffset(
        None
    ), f"{label} is aware but not UTC (offset {value.utcoffset()})"


class _CaptureSession:
    """Fake AsyncSession recording queries, returning empty results."""

    def __init__(self):
        self.queries = []

    async def execute(self, query):
        self.queries.append(query)
        result = MagicMock()
        result.scalars.return_value.all.return_value = []
        result.scalar_one_or_none.return_value = None
        result.scalar.return_value = 0
        return result


async def test_complete_todo_writes_aware_utc_timestamps():
    repo = TodoRepository(MagicMock())
    with patch.object(TodoRepository, "update_todo", new=AsyncMock(return_value=None)) as upd:
        await repo.complete_todo("t-1", owner_id="u-1")
    updates = upd.call_args.args[1]
    _assert_aware_utc(updates["completed_at"], "complete_todo completed_at")
    _assert_aware_utc(updates["updated_at"], "complete_todo updated_at")


async def test_reopen_todo_writes_aware_utc_timestamp():
    repo = TodoRepository(MagicMock())
    with patch.object(TodoRepository, "update_todo", new=AsyncMock(return_value=None)) as upd:
        await repo.reopen_todo("t-1", owner_id="u-1")
    updates = upd.call_args.args[1]
    _assert_aware_utc(updates["updated_at"], "reopen_todo updated_at")


async def test_get_due_todos_overdue_cutoff_is_aware_utc():
    """The include_overdue cutoff compared naive LOCAL now against timestamptz."""
    session = _CaptureSession()
    repo = TodoRepository(session)
    await repo.get_due_todos("u-1", include_overdue=True)
    assert len(session.queries) == 1
    cutoffs = [
        el.value
        for el in visitors.iterate(session.queries[0].whereclause)
        if isinstance(el, BindParameter) and isinstance(el.value, datetime)
    ]
    assert cutoffs, "expected a datetime cutoff bind in get_due_todos"
    for value in cutoffs:
        _assert_aware_utc(value, "get_due_todos overdue cutoff")


async def test_get_completion_stats_cutoff_is_aware_utc():
    session = _CaptureSession()
    repo = TodoRepository(session)
    await repo.get_completion_stats("u-1", days=7)
    cutoffs = [
        el.value
        for q in session.queries
        for el in visitors.iterate(q.whereclause)
        if isinstance(el, BindParameter) and isinstance(el.value, datetime)
    ]
    assert cutoffs, "expected datetime cutoff binds in get_completion_stats"
    for value in cutoffs:
        _assert_aware_utc(value, "get_completion_stats cutoff")


class TestNoNaiveDatetimeNowInTodoLayer1493:
    """AST guard: zero bare `datetime.now()` (no tz argument) in the todo-layer
    files #1493 names (plus the two that already carried the discipline, so a
    regression there is caught too)."""

    FILES = [
        "services/repositories/todo_repository.py",
        # services/api/todo_management.py disposed 2026-08-30 (census disposal
        # Batch 3) — the unmounted todos REST surface; #1493's live todo layer
        # is fully covered by the remaining four.
        "services/intent_service/temporal_utils.py",
        "services/intent_service/todo_handlers.py",
        "services/todo/todo_management_service.py",
    ]

    @staticmethod
    def _is_bare_now(node) -> bool:
        return (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "now"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "datetime"
            and not node.args
            and not node.keywords
        )

    def test_no_bare_datetime_now(self):
        violations = []
        files_checked = 0
        for rel in self.FILES:
            assert os.path.exists(rel), (
                f"{rel} missing — the #1493 guard's denominator is wrong; "
                f"update FILES rather than letting the scan go vacuous (m-44)"
            )
            files_checked += 1
            tree = ast.parse(open(rel, encoding="utf-8").read(), filename=rel)
            # datetime.now().astimezone() is SANCTIONED: aware local time,
            # the deliberate temporal_utils semantics (#1493). Collect those
            # inner calls first so they aren't flagged.
            sanctioned = set()
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "astimezone"
                    and self._is_bare_now(node.func.value)
                ):
                    sanctioned.add(id(node.func.value))
            for node in ast.walk(tree):
                if self._is_bare_now(node) and id(node) not in sanctioned:
                    violations.append(f"{rel}:{node.lineno}")

        assert (
            files_checked == len(self.FILES) == 4
        ), f"guard checked {files_checked} files, expected 4 (denominator)"
        assert not violations, (
            f"bare naive-local datetime.now() in the todo layer (#1493) — use "
            f"services.utils.datetime_utils.utc_now() (or an aware local time "
            f"where local semantics are deliberate): {violations} "
            f"(checked {files_checked} files)"
        )
