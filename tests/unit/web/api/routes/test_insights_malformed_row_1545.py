"""Issue #1545 — one malformed insight row must not kill the whole journal.

Live-confirmed 2026-08-09: GET /api/v1/insights died wholesale ("Failed to
load insights") when ONE row's `learning` JSON didn't deserialize —
`InsightRepository.list_for_user` ran `to_domain()` in a list comprehension,
so a single ValueError/AttributeError inside `ExtractedLearning.from_dict`
took down every good row with it. Fixing the bad row recovered the page.

Fix under test:
- Repo: per-row deserialization; a row that fails to parse is SKIPPED with an
  error log (id + error). `list_for_user_with_skips` returns
  (insights, skipped_count); `list_for_user` keeps its List contract.
- Route: payload includes `skipped_count` so the frontend can render
  "N insights could not be displayed".

Rows are REAL `InsightDB` instances (the deserialization failure is real —
`ExtractedLearning.from_dict` raising on a non-ISO created_at); only the DB
session is mocked, because aiosqlite isn't available in the runner env (the
sibling #1031/#1035 SQLite-backed repo suites skip there for the same
reason).
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from services.database.models import InsightDB
from services.database.repositories import InsightRepository
from services.mux.composting_models import ExtractedLearning, Pattern
from services.mux.composting_pipeline import SurfaceableInsight


def _good_row(*, user_id="alpha") -> InsightDB:
    learning = ExtractedLearning(
        pattern=Pattern(description="good pattern"),
        confidence=0.9,
        topic_tags=["productivity"],
        expression="You tend to batch reviews",
    )
    insight = SurfaceableInsight(
        object_id=f"obj-{uuid4().hex[:8]}", user_id=user_id, learning=learning
    )
    return InsightDB.from_domain(insight)


def _malformed_row(*, user_id="alpha") -> InsightDB:
    """Row whose learning JSON cannot deserialize: created_at is not an ISO
    timestamp, so ExtractedLearning.from_dict raises ValueError — the exact
    one-bad-row shape from the 2026-08-09 live incident."""
    return InsightDB(
        id=str(uuid4()),
        object_id=f"obj-bad-{uuid4().hex[:8]}",
        user_id=user_id,
        learning={"created_at": "definitely-not-a-timestamp", "confidence": 0.5},
    )


class _FakeScalarResult:
    def __init__(self, rows):
        self._rows = rows

    def scalars(self):
        rows = self._rows
        return SimpleNamespace(all=lambda: rows)


def _repo_with_rows(rows) -> InsightRepository:
    session = SimpleNamespace(execute=AsyncMock(return_value=_FakeScalarResult(rows)))
    return InsightRepository(session)


def test_malformed_row_really_fails_to_deserialize():
    """Guard: the seeded row exercises a REAL from_dict failure, so the tests
    below measure the skip path, not a fixture accident."""
    with pytest.raises(Exception):
        _malformed_row().to_domain()


# ---------------------------------------------------------------------------
# Repository layer
# ---------------------------------------------------------------------------


async def test_malformed_row_is_skipped_good_rows_survive():
    """Failing-first core: pre-fix, the bad row's ValueError escaped
    list_for_user's list comprehension and the caller got NOTHING."""
    good = _good_row()
    repo = _repo_with_rows([good, _malformed_row()])

    insights, skipped = await repo.list_for_user_with_skips("alpha")
    assert [i.id for i in insights] == [
        good.id
    ], "good rows must survive a sibling row's deserialization failure"
    assert skipped == 1


async def test_list_for_user_contract_unchanged_but_resilient():
    """Existing callers (home_state_service, context_assembler, InsightJournal)
    keep the plain-List contract — and inherit the skip resilience."""
    good = _good_row()
    repo = _repo_with_rows([_malformed_row(), good])

    results = await repo.list_for_user("alpha")
    assert [i.id for i in results] == [good.id]


async def test_all_good_rows_means_zero_skipped():
    a, b = _good_row(), _good_row()
    repo = _repo_with_rows([a, b])

    insights, skipped = await repo.list_for_user_with_skips("alpha")
    assert [i.id for i in insights] == [a.id, b.id]
    assert skipped == 0


# ---------------------------------------------------------------------------
# Route layer
# ---------------------------------------------------------------------------


async def test_route_payload_includes_skipped_count(monkeypatch):
    """GET /api/v1/insights returns the good rows plus skipped_count so the
    frontend CAN render 'N insights could not be displayed'."""
    import web.api.routes.insights as insights_route

    good_domain = _good_row(user_id="u-1").to_domain()

    class FakeRepo:
        def __init__(self, session):
            pass

        async def list_for_user_with_skips(self, user_id):
            assert user_id == "u-1"
            return [good_domain], 2

    @asynccontextmanager
    async def fake_scope():
        yield None

    monkeypatch.setattr(insights_route.AsyncSessionFactory, "session_scope", fake_scope)
    monkeypatch.setattr(insights_route, "InsightRepository", FakeRepo)

    payload = await insights_route.list_insights(current_user=SimpleNamespace(sub="u-1"))
    assert payload["count"] == 1
    assert payload["insights"][0]["id"] == good_domain.id
    assert payload["skipped_count"] == 2
