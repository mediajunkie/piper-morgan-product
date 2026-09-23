"""#1556: naive-local datetime class in the file repository layer.

Discovered by the #1493 audit's class sweep (2026-08-09) beyond the audited
todo-layer scope: `FileRepository` wrote naive LOCAL `datetime.now()` to a
timestamptz column (last_referenced) and used naive-local `datetime.now()`
as the recency cutoff in three query methods — the same class as #1493's
todo-repository fix, drift not crash: stored/compared instants silently
depend on the server's UTC offset.

These tests pin aware-UTC behavior WITHOUT wall-clock assertions: they assert
tz-awareness and a zero UTC offset on captured values (never "equals now").
An AST guard pins the file at zero bare `datetime.now()` calls, with the
denominator (files checked) asserted per m-44. Idiom matched from
tests/unit/services/repositories/test_todo_repository_tz_1493.py.
"""

import ast
import os
from datetime import datetime, timezone
from unittest.mock import MagicMock

from sqlalchemy.sql import visitors
from sqlalchemy.sql.elements import BindParameter

from services.repositories.file_repository import FileRepository


def _assert_aware_utc(value, label):
    assert isinstance(value, datetime), f"{label} should be a datetime, got {value!r}"
    assert value.tzinfo is not None, (
        f"{label} is NAIVE — the #1493/#1556 class: naive local time written/compared "
        f"against a timestamptz column drifts by the server's UTC offset"
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


def _cutoff_binds(query):
    return [
        el.value
        for el in visitors.iterate(query.whereclause)
        if isinstance(el, BindParameter) and isinstance(el.value, datetime)
    ]


async def test_increment_reference_count_writes_aware_utc_timestamp():
    """Write site: last_referenced=datetime.now() in the UPDATE .values()."""
    session = _CaptureSession()
    repo = FileRepository.__new__(FileRepository)
    repo.session = session
    await repo.increment_reference_count("file-1", owner_id="owner-1")

    assert session.queries, "expected at least one executed statement"
    update_query = session.queries[0]
    params = update_query.compile().params
    assert "last_referenced" in params, f"expected last_referenced bound param, got {params.keys()}"
    _assert_aware_utc(params["last_referenced"], "increment_reference_count last_referenced")


async def test_get_recent_files_cutoff_is_aware_utc():
    """RED-FIRST (cutoff site): get_recent_files computes
    `cutoff_time = datetime.now() - timedelta(hours=hours)` and compares it
    against a timestamptz column."""
    session = _CaptureSession()
    repo = FileRepository.__new__(FileRepository)
    repo.session = session
    await repo.get_recent_files(owner_id="owner-1", hours=24)

    assert len(session.queries) == 1
    cutoffs = _cutoff_binds(session.queries[0])
    assert cutoffs, "expected a datetime cutoff bind in get_recent_files"
    for value in cutoffs:
        _assert_aware_utc(value, "get_recent_files cutoff")


async def test_search_files_by_name_all_sessions_cutoff_is_aware_utc():
    """Cutoff site: search_files_by_name_all_sessions."""
    session = _CaptureSession()
    repo = FileRepository.__new__(FileRepository)
    repo.session = session
    await repo.search_files_by_name_all_sessions("q", owner_id="owner-1", days=30)

    assert len(session.queries) == 1
    cutoffs = _cutoff_binds(session.queries[0])
    assert cutoffs, "expected a datetime cutoff bind in search_files_by_name_all_sessions"
    for value in cutoffs:
        _assert_aware_utc(value, "search_files_by_name_all_sessions cutoff")


async def test_get_recent_files_all_sessions_cutoff_is_aware_utc():
    """Cutoff site: get_recent_files_all_sessions."""
    session = _CaptureSession()
    repo = FileRepository.__new__(FileRepository)
    repo.session = session
    await repo.get_recent_files_all_sessions(owner_id="owner-1", days=7)

    assert len(session.queries) == 1
    cutoffs = _cutoff_binds(session.queries[0])
    assert cutoffs, "expected a datetime cutoff bind in get_recent_files_all_sessions"
    for value in cutoffs:
        _assert_aware_utc(value, "get_recent_files_all_sessions cutoff")


class TestNoNaiveDatetimeNowInFileRepository1556:
    """AST guard: zero bare `datetime.now()` (no tz argument) in
    services/repositories/file_repository.py — covers all 4 naive sites
    (1 write + 3 cutoffs) #1556 named."""

    FILES = ["services/repositories/file_repository.py"]

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
            f"bare naive-local datetime.now() in file_repository.py (#1556) — "
            f"use services.utils.datetime_utils.utc_now(): {violations} "
            f"(checked {files_checked} files)"
        )
