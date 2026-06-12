"""#1143/#1035 regression: InsightJournal write methods must COMMIT.

`AsyncSessionFactory.session_scope()` does NOT auto-commit (despite its
docstring) — `repo.add` only flushes, so without an explicit `session.commit()`
the composting cycle silently failed to persist `SurfaceableInsight` rows
(found via live verification 2026-06-12; the other unit tests use the in-memory
FakeInsightJournal, so the real commit path was never exercised). These guard
against the commit being dropped again.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.mux.composting_pipeline import InsightJournal


def _session_cm(session):
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=session)
    cm.__aexit__ = AsyncMock(return_value=None)
    return cm


@pytest.mark.asyncio
async def test_add_commits_the_session():
    journal = InsightJournal()
    session = MagicMock()
    session.commit = AsyncMock()
    repo = MagicMock()
    repo.add = AsyncMock()
    with patch.object(InsightJournal, "_session_scope", return_value=_session_cm(session)), patch.object(
        InsightJournal, "_new_repo", return_value=repo
    ):
        await journal.add(MagicMock())
    repo.add.assert_awaited_once()
    session.commit.assert_awaited_once()  # the regression guard


@pytest.mark.asyncio
async def test_mark_surfaced_commits_the_session():
    journal = InsightJournal()
    session = MagicMock()
    session.commit = AsyncMock()
    repo = MagicMock()
    repo.mark_surfaced = AsyncMock(return_value=MagicMock())
    with patch.object(InsightJournal, "_session_scope", return_value=_session_cm(session)), patch.object(
        InsightJournal, "_new_repo", return_value=repo
    ):
        await journal.mark_surfaced("insight-1", "ok")
    repo.mark_surfaced.assert_awaited_once()
    session.commit.assert_awaited_once()
