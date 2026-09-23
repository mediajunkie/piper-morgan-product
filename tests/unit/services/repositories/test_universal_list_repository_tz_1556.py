"""#1556: naive-local datetime class in the universal-list repository layer.

Discovered by the #1493 audit's class sweep (2026-08-09) beyond the audited
todo-layer scope: `UniversalListRepository` / `UniversalListItemRepository`
wrote naive LOCAL `datetime.now()` to timestamptz columns (updated_at,
added_at) — the same class as #1493's todo-repository fix, drift not crash:
stored instants silently depend on the server's UTC offset.

These tests pin aware-UTC behavior WITHOUT wall-clock assertions: they assert
tz-awareness and a zero UTC offset on captured values (never "equals now").
An AST guard pins the file at zero bare `datetime.now()` calls, with the
denominator (files checked) asserted per m-44. Idiom matched from
tests/unit/services/repositories/test_todo_repository_tz_1493.py.
"""

import ast
import os
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

from services.repositories.universal_list_repository import (
    UniversalListItemRepository,
    UniversalListRepository,
)


def _assert_aware_utc(value, label):
    assert isinstance(value, datetime), f"{label} should be a datetime, got {value!r}"
    assert value.tzinfo is not None, (
        f"{label} is NAIVE — the #1493/#1556 class: naive local time written to a "
        f"timestamptz column drifts by the server's UTC offset"
    )
    assert value.utcoffset() == timezone.utc.utcoffset(
        None
    ), f"{label} is aware but not UTC (offset {value.utcoffset()})"


class _CaptureSession:
    """Fake AsyncSession recording executed statements, returning empty results."""

    def __init__(self):
        self.queries = []

    async def execute(self, query):
        self.queries.append(query)
        result = MagicMock()
        result.scalars.return_value.all.return_value = []
        result.scalar_one_or_none.return_value = None
        result.scalar.return_value = 0
        return result


async def test_update_list_writes_aware_utc_timestamp():
    """RED-FIRST (write site): update_list mutates the caller's `updates`
    dict in place with `updated_at` before issuing the UPDATE — capturing
    that dict is sufficient to observe naive vs aware without any DB."""
    repo = UniversalListRepository(_CaptureSession())
    updates = {"name": "renamed"}
    await repo.update_list("list-1", updates, owner_id="owner-1")
    _assert_aware_utc(updates["updated_at"], "update_list updated_at")


async def test_update_item_counts_writes_aware_utc_timestamp():
    """Write site: update_item_counts embeds `updated_at=datetime.now()`
    directly in the UPDATE .values() clause — capture via the compiled
    statement's bound params."""
    session = _CaptureSession()
    repo = UniversalListRepository(session)
    await repo.update_item_counts("list-1", owner_id="owner-1")

    update_queries = [q for q in session.queries if hasattr(q, "compile")]
    assert update_queries, "expected at least one executed statement"
    last = update_queries[-1]
    params = last.compile().params
    assert "updated_at" in params, f"expected updated_at bound param, got {params.keys()}"
    _assert_aware_utc(params["updated_at"], "update_item_counts updated_at")


async def test_add_item_to_list_writes_aware_utc_timestamp():
    """Write site: add_item_to_list builds a domain.ListItem with
    `added_at=datetime.now()` before persisting — capture the constructed
    domain object directly (create_item's session interactions are mocked
    out so we don't need a DB)."""
    item_repo = UniversalListItemRepository.__new__(UniversalListItemRepository)
    item_repo.session = _CaptureSession()
    item_repo.create_item = AsyncMock(side_effect=lambda item: item)

    result = await item_repo.add_item_to_list(
        list_id="list-1", item_id="item-1", item_type="todo", added_by="user-1", position=1
    )
    _assert_aware_utc(result.added_at, "add_item_to_list added_at")


class TestNoNaiveDatetimeNowInUniversalListRepository1556:
    """AST guard: zero bare `datetime.now()` (no tz argument) in
    services/repositories/universal_list_repository.py — covers all 6
    naive-write sites #1556 named, including the ones not individually
    exercised behaviorally above."""

    FILES = ["services/repositories/universal_list_repository.py"]

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
                f"{rel} missing — the #1556 guard's denominator is wrong; "
                f"update FILES rather than letting the scan go vacuous (m-44)"
            )
            files_checked += 1
            tree = ast.parse(open(rel, encoding="utf-8").read(), filename=rel)
            for node in ast.walk(tree):
                if self._is_bare_now(node):
                    violations.append(f"{rel}:{node.lineno}")

        assert (
            files_checked == len(self.FILES) == 1
        ), f"guard checked {files_checked} files, expected 1 (denominator)"
        assert not violations, (
            f"bare naive-local datetime.now() in universal_list_repository.py "
            f"(#1556) — use services.utils.datetime_utils.utc_now(): {violations} "
            f"(checked {files_checked} files)"
        )
