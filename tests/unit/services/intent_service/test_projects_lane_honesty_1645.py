"""#1645 — the projects lane gets a true total, and projects +
completed-todos get a source-failed state distinct from never-gathered.

Both halves are sibling-lane honesty residue found during #1639:

1. ``_compute_projects`` was ``SELECT … LIMIT 5`` with no COUNT — a user
   with >5 projects got 5 "tracked" lines and no denominator (m-44: never
   an unlabeled subset). The fix mirrors #1530's shape (real row-derived
   total beside the truncated display slice) via ``COUNT(*) OVER ()``
   riding the same gather; the floor's #1530 renderer already states
   "showing N of M" when the total exceeds the slice.
2. Projects/completed-todos compute returned None on error —
   indistinguishable from never-gathered at the floor. The fix mirrors
   #1573's pending-todos shape: compute returns ``{"source_failed": True}``
   at ERROR level; the cached layer translates to a lane-specific key; the
   floor renders an explicit "check FAILED — do not claim there are none"
   line.

Layer honesty (m-43): these tests pin the assembler seams and the
deterministic CONTEXT-RENDERER — not a live model.
"""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversational_floor import ConversationalFloor


def _session_with_rows(rows):
    mock_result = MagicMock()
    mock_result.fetchall.return_value = rows
    mock_session = MagicMock()
    mock_session.execute = AsyncMock(return_value=mock_result)

    @asynccontextmanager
    async def fake_scope():
        yield mock_session

    return mock_session, fake_scope


class TestProjectsTrueTotal:
    """Half 1: the populated read carries the query's own denominator."""

    @pytest.mark.asyncio
    async def test_populated_compute_carries_the_windowed_total(self):
        # 5 display rows, each carrying the pre-LIMIT window total (9).
        rows = [(f"proj-{i}", None, None, 9) for i in range(5)]
        _, fake_scope = _session_with_rows(rows)

        assembler = ContextAssembler()
        with patch("services.database.session_factory.AsyncSessionFactory") as mock_factory:
            mock_factory.session_scope = fake_scope
            result = await assembler._compute_projects(str(uuid4()))

        assert result["project_count"] == 9
        assert len(result["projects"]) == 5
        assert result["projects"][0]["name"] == "proj-0"

    @pytest.mark.asyncio
    async def test_count_rides_the_same_query(self):
        # "A real COUNT query riding the same gather" — one execute, and
        # the statement itself carries the window COUNT.
        rows = [("only", None, None, 1)]
        mock_session, fake_scope = _session_with_rows(rows)

        assembler = ContextAssembler()
        with patch("services.database.session_factory.AsyncSessionFactory") as mock_factory:
            mock_factory.session_scope = fake_scope
            await assembler._compute_projects(str(uuid4()))

        assert mock_session.execute.await_count == 1
        stmt = str(mock_session.execute.await_args.args[0])
        assert "COUNT(*) OVER ()" in stmt
        assert "LIMIT 5" in stmt

    @pytest.mark.asyncio
    async def test_cached_layer_passes_the_populated_total_through(self):
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_compute_projects",
            new=AsyncMock(
                return_value={
                    "projects": [{"name": f"proj-{i}"} for i in range(5)],
                    "project_count": 9,
                }
            ),
        ):
            result = await assembler._get_projects_cached(str(uuid4()), limit=5)

        assert result["project_count"] == 9
        assert len(result["projects"]) == 5

    def test_floor_states_the_denominator_beside_the_slice(self):
        # The m-44 copy pin: 9 projects, 5 listed — the rendered block says
        # both numbers, never an unlabeled subset.
        floor = ConversationalFloor(llm_client=MagicMock())
        out = floor._format_domain_context(
            {
                "projects": [{"name": f"proj-{i}"} for i in range(5)],
                "project_count": 9,
            }
        )
        assert "- Active project count: 9 (only the first 5 are listed above)" in out
        assert out.count('": tracked') == 5


class TestProjectsSourceFailed:
    """Half 2a: a failed projects read is a distinct honest state."""

    @pytest.mark.asyncio
    async def test_compute_error_returns_source_failed(self):
        @asynccontextmanager
        async def broken_scope():
            raise RuntimeError("db down")
            yield  # pragma: no cover

        assembler = ContextAssembler()
        with patch("services.database.session_factory.AsyncSessionFactory") as mock_factory:
            mock_factory.session_scope = broken_scope
            result = await assembler._compute_projects(str(uuid4()))

        assert result == {"source_failed": True}

    @pytest.mark.asyncio
    async def test_cached_layer_translates_to_the_lane_specific_key(self):
        # The generic "source_failed" renders as a REMINDER-check failure on
        # the floor — the translation is what makes the copy lane-honest.
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_compute_projects",
            new=AsyncMock(return_value={"source_failed": True}),
        ):
            result = await assembler._get_projects_cached(str(uuid4()), limit=5)

        assert result == {"projects_source_failed": True}

    def test_floor_renders_couldnt_check_never_none(self):
        floor = ConversationalFloor(llm_client=MagicMock())
        out = floor._format_domain_context({"projects_source_failed": True})
        assert "Project check FAILED" in out
        assert "could not load the user's project list" in out
        assert "do not claim there are none" in out
        # Never the verified-empty fact, never a tracked line.
        assert "PROJECTS: none" not in out
        assert '": tracked' not in out

    def test_absent_key_renders_no_failure_line(self):
        floor = ConversationalFloor(llm_client=MagicMock())
        out = floor._format_domain_context({"current_time": "now-ish"})
        assert "Project check FAILED" not in out


class TestCompletedTodosSourceFailed:
    """Half 2b: a failed completed-todos read is a distinct honest state."""

    @pytest.mark.asyncio
    async def test_compute_error_returns_source_failed(self):
        mock_svc = MagicMock()
        mock_svc.list_todos = AsyncMock(side_effect=RuntimeError("db down"))

        assembler = ContextAssembler()
        with patch(
            "services.todo.todo_management_service.TodoManagementService",
            return_value=mock_svc,
        ):
            result = await assembler._compute_completed_todos(str(uuid4()))

        assert result == {"source_failed": True}

    @pytest.mark.asyncio
    async def test_cached_layer_translates_to_the_lane_specific_key(self):
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_compute_completed_todos",
            new=AsyncMock(return_value={"source_failed": True}),
        ):
            result = await assembler._get_completed_todos_cached(str(uuid4()), limit=10)

        assert result == {"completed_todos_source_failed": True}

    def test_floor_renders_couldnt_check_never_none(self):
        floor = ConversationalFloor(llm_client=MagicMock())
        out = floor._format_domain_context({"completed_todos_source_failed": True})
        assert "Completed-todo check FAILED" in out
        assert "could not load the user's completed todos" in out
        assert "do not claim there are none" in out
        assert "COMPLETED TODOS: none" not in out

    def test_absent_key_renders_no_failure_line(self):
        floor = ConversationalFloor(llm_client=MagicMock())
        out = floor._format_domain_context({"current_time": "now-ish"})
        assert "Completed-todo check FAILED" not in out


class TestTemporalGatherCarriesTheFailureFlags:
    """The TEMPORAL gather merges both lanes with ``context.update`` — the
    translated failure keys must reach the floor context intact."""

    @pytest.mark.asyncio
    async def test_temporal_gather_carries_both_failure_flags(self):
        assembler = ContextAssembler()
        with (
            patch.object(assembler, "_gather_calendar_context", new=AsyncMock(return_value={})),
            patch.object(assembler, "_get_pending_todos_cached", new=AsyncMock(return_value=None)),
            patch.object(
                assembler,
                "_get_completed_todos_cached",
                new=AsyncMock(return_value={"completed_todos_source_failed": True}),
            ),
            patch.object(
                assembler,
                "_get_projects_cached",
                new=AsyncMock(return_value={"projects_source_failed": True}),
            ),
            patch.object(
                assembler,
                "_gather_active_milestones_context",
                new=AsyncMock(return_value={}),
            ),
            patch.object(
                assembler,
                "_gather_recent_activity_context",
                new=AsyncMock(return_value={}),
            ),
        ):
            ctx = await assembler._gather_temporal_context(user_id="u-1645")

        assert ctx.get("projects_source_failed") is True
        assert ctx.get("completed_todos_source_failed") is True
        assert "projects" not in ctx
        assert "completed_todos" not in ctx
