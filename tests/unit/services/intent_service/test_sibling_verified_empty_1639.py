"""#1639 — sibling gathers conflated verified-empty with never-gathered
(projects + completed-todos lanes; fix shape proven by #1544).

Found during #1544: `_compute_projects` and `_compute_completed_todos` still
returned None for a legitimately-empty result, so "you have no projects" /
"you completed nothing" remained structurally indistinguishable from
"projects/completed todos were never gathered" at the floor — the projects
lane could reproduce the exact conversation-scoped hedge #1544 killed for
pending todos (one-label-two-objects: an absent fact and an empty fact
wearing the same None).

The fix, per lane, mirrors #1544's:
- assembler returns the verified-empty dict with a REAL zero count instead
  of None/absent (a zero from a LIMIT-capped read is exact — no truncation
  at zero rows);
- the floor renderer gains a distinct "none — checked this turn" state
  beside populated, with absent staying silent.

#1645 upgraded the error path this file originally pinned as error→None:
a compute error now returns the distinct ``{"source_failed": True}`` state
(the #1573 shape), which must STILL never surface as verified-empty — the
pin's substance (failure is not an empty fact) is unchanged; only the
honest carrier changed. The #1645 lanes' own pins live in
test_projects_lane_honesty_1645.py.

Layer honesty (m-43): these tests pin the PROMPT text and the deterministic
CONTEXT-RENDERER seam — not a live model.
"""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversational_floor import (
    FLOOR_SYSTEM_PROMPT_ADDENDUM,
    ConversationalFloor,
)


def _fabrication_section() -> str:
    """The never-fabricate-user-data section of the floor prompt."""
    start = FLOOR_SYSTEM_PROMPT_ADDENDUM.index("CRITICAL — Never fabricate user data")
    end = FLOOR_SYSTEM_PROMPT_ADDENDUM.index("CRITICAL", start + 10)
    return FLOOR_SYSTEM_PROMPT_ADDENDUM[start:end]


class TestPromptLicensesSiblingLaneEmptyClaims:
    """#1544 rewrote the empty-data guidance; #1639 extends only the
    context-line examples (never reply strings — that was #1544's root
    cause) so the empty-list license visibly covers the sibling lanes."""

    def test_prompt_names_all_three_verified_empty_context_lines(self):
        section = _fabrication_section()
        assert "PENDING TODOS: none" in section
        assert "PROJECTS: none" in section
        assert "COMPLETED TODOS:" in section

    def test_no_conversation_scoping_reintroduced(self):
        section = _fabrication_section()
        assert "this conversation" not in section, section

    def test_no_transcript_reply_seed_reintroduced(self):
        # #1544's root cause was the prompt supplying reply strings the
        # model echoed verbatim. The #1639 extension adds context-line
        # examples only — pin that the known seed phrases stay gone.
        assert "I don't see any todos" not in FLOOR_SYSTEM_PROMPT_ADDENDUM
        assert "I don't see any projects" not in FLOOR_SYSTEM_PROMPT_ADDENDUM


class TestProjectsRendererThreeStates:
    """`_format_domain_context`, projects lane: populated, verified-empty,
    and absent must be three distinguishable states."""

    def setup_method(self):
        self.floor = ConversationalFloor(llm_client=MagicMock())

    def test_populated_renders_each_project(self):
        out = self.floor._format_domain_context(
            {"projects": [{"name": "piper-morgan"}, {"name": "klatch"}]}
        )
        assert '- Project "piper-morgan": tracked' in out
        assert '- Project "klatch": tracked' in out
        assert "PROJECTS: none" not in out

    def test_verified_empty_renders_checked_fact(self):
        out = self.floor._format_domain_context({"projects": [], "project_count": 0})
        assert "PROJECTS: none" in out
        assert "checked" in out
        assert "account-level" in out
        # No conversation-scoped framing anywhere in the rendered block.
        assert "this conversation" not in out
        assert "showing up" not in out

    def test_absent_key_renders_no_project_lines(self):
        out = self.floor._format_domain_context({"current_time": "now-ish"})
        assert "PROJECTS: none" not in out
        assert '- Project "' not in out
        assert "Active project count" not in out

    def test_verified_empty_suppresses_redundant_zero_count_line(self):
        # The verified-empty line IS the zero statement; a bare
        # "Active project count: 0" beside it would dilute it.
        out = self.floor._format_domain_context({"projects": [], "project_count": 0})
        assert "Active project count: 0" not in out

    def test_populated_count_rendering_unchanged(self):
        # #1530's truncation-note behavior must survive #1639 untouched.
        out = self.floor._format_domain_context(
            {
                "projects": [{"name": "a"}, {"name": "b"}],
                "project_count": 7,
            }
        )
        assert "Active project count: 7" in out
        assert "only the first 2 are listed above" in out


class TestCompletedTodosRendererThreeStates:
    """`_format_domain_context`, completed-todos lane: populated,
    verified-empty, and absent must be three distinguishable states."""

    def setup_method(self):
        self.floor = ConversationalFloor(llm_client=MagicMock())

    def test_populated_renders_items_with_row_derived_count(self):
        out = self.floor._format_domain_context(
            {
                "completed_todos": [{"text": "shipped the fix"}, {"text": "wrote the pins"}],
                "completed_todo_count": 2,
            }
        )
        assert "Recently completed todos (2):" in out
        assert "shipped the fix" in out
        assert "wrote the pins" in out
        assert "COMPLETED TODOS: none" not in out

    def test_populated_count_uses_total_not_display_slice(self):
        # #1639 (m-44): 12 completed rows, display capped — the stated
        # count must be the query's total, never the slice length.
        out = self.floor._format_domain_context(
            {
                "completed_todos": [{"text": f"item-{i}"} for i in range(10)],
                "completed_todo_count": 12,
            }
        )
        assert "Recently completed todos (12):" in out

    def test_verified_empty_renders_checked_fact(self):
        out = self.floor._format_domain_context({"completed_todos": [], "completed_todo_count": 0})
        assert "COMPLETED TODOS: none" in out
        assert "checked" in out
        assert "account-level" in out
        assert "this conversation" not in out
        assert "showing up" not in out

    def test_absent_key_renders_no_completed_lines(self):
        out = self.floor._format_domain_context({"current_time": "now-ish"})
        assert "COMPLETED TODOS" not in out
        assert "Recently completed todos" not in out


class TestProjectsAssemblerVerifiedEmpty:
    """Zero projects is a FACT (owner-scoped read succeeded) — it must
    survive compute → cache → gather; an errored read must NOT."""

    @pytest.mark.asyncio
    async def test_compute_returns_verified_empty_not_none(self):
        mock_result = MagicMock()
        mock_result.fetchall.return_value = []
        mock_session = MagicMock()
        mock_session.execute = AsyncMock(return_value=mock_result)

        @asynccontextmanager
        async def fake_scope():
            yield mock_session

        assembler = ContextAssembler()
        with patch("services.database.session_factory.AsyncSessionFactory") as mock_factory:
            mock_factory.session_scope = fake_scope
            result = await assembler._compute_projects(str(uuid4()))

        assert result == {"projects": [], "project_count": 0}, (
            "verified-empty must be a definite fact, not None "
            "(None is indistinguishable from never-gathered)"
        )

    @pytest.mark.asyncio
    async def test_compute_error_is_never_verified_empty(self):
        # A failed read is NOT a verified-empty — projects may exist.
        # #1645: the error carrier upgraded from None to the distinct
        # {"source_failed": True} state; the substance pinned here is that
        # it can never be mistaken for the verified-empty fact.
        @asynccontextmanager
        async def broken_scope():
            raise RuntimeError("db down")
            yield  # pragma: no cover

        assembler = ContextAssembler()
        with patch("services.database.session_factory.AsyncSessionFactory") as mock_factory:
            mock_factory.session_scope = broken_scope
            result = await assembler._compute_projects(str(uuid4()))

        assert result == {"source_failed": True}
        assert result != {"projects": [], "project_count": 0}

    @pytest.mark.asyncio
    async def test_cached_layer_passes_verified_empty_and_count_through(self):
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_compute_projects",
            new=AsyncMock(return_value={"projects": [], "project_count": 0}),
        ):
            result = await assembler._get_projects_cached(str(uuid4()), limit=5)

        assert result == {"projects": [], "project_count": 0}

    @pytest.mark.asyncio
    async def test_cached_layer_never_invents_a_count_for_stale_entries(self):
        # m-44: a cache entry predating #1645 carries no populated count —
        # the cached layer must not invent a project_count from slice
        # length. (#1645: fresh computes DO carry a real windowed COUNT;
        # that path is pinned in test_projects_lane_honesty_1645.py.)
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_compute_projects",
            new=AsyncMock(return_value={"projects": [{"name": "alpha"}]}),
        ):
            result = await assembler._get_projects_cached(str(uuid4()), limit=5)

        assert result == {"projects": [{"name": "alpha"}]}
        assert "project_count" not in result


class TestCompletedTodosAssemblerVerifiedEmpty:
    """Zero completed todos is a FACT (owner-scoped read succeeded) — it
    must survive compute → cache → gather; an errored read must NOT."""

    @pytest.mark.asyncio
    async def test_compute_returns_verified_empty_when_no_todos_at_all(self):
        mock_svc = MagicMock()
        mock_svc.list_todos = AsyncMock(return_value=[])

        assembler = ContextAssembler()
        with patch(
            "services.todo.todo_management_service.TodoManagementService",
            return_value=mock_svc,
        ):
            result = await assembler._compute_completed_todos(str(uuid4()))

        assert result == {"completed_todos": [], "completed_todo_count": 0}
        # Owner-scoping assertion: the read was keyed by user, completed included.
        _, call_kwargs = mock_svc.list_todos.call_args
        assert "user_id" in call_kwargs
        assert call_kwargs.get("include_completed") is True

    @pytest.mark.asyncio
    async def test_compute_returns_verified_empty_when_only_pending_exist(self):
        # The stronger case: todos exist but none are completed — still a
        # verified-empty COMPLETED lane, never an absence.
        pending_only = [MagicMock(completed=False), MagicMock(completed=False)]
        mock_svc = MagicMock()
        mock_svc.list_todos = AsyncMock(return_value=pending_only)

        assembler = ContextAssembler()
        with patch(
            "services.todo.todo_management_service.TodoManagementService",
            return_value=mock_svc,
        ):
            result = await assembler._compute_completed_todos(str(uuid4()))

        assert result == {"completed_todos": [], "completed_todo_count": 0}

    @pytest.mark.asyncio
    async def test_compute_error_is_never_verified_empty(self):
        # #1645: error carrier upgraded None → {"source_failed": True};
        # the substance pinned here is unchanged — a failure must never
        # read as the verified-empty fact.
        mock_svc = MagicMock()
        mock_svc.list_todos = AsyncMock(side_effect=RuntimeError("db down"))

        assembler = ContextAssembler()
        with patch(
            "services.todo.todo_management_service.TodoManagementService",
            return_value=mock_svc,
        ):
            result = await assembler._compute_completed_todos(str(uuid4()))

        assert result == {"source_failed": True}
        assert result != {"completed_todos": [], "completed_todo_count": 0}

    @pytest.mark.asyncio
    async def test_cached_layer_passes_verified_empty_through(self):
        assembler = ContextAssembler()
        with patch.object(
            assembler,
            "_compute_completed_todos",
            new=AsyncMock(return_value={"completed_todos": [], "completed_todo_count": 0}),
        ):
            result = await assembler._get_completed_todos_cached(str(uuid4()), limit=10)

        assert result == {"completed_todos": [], "completed_todo_count": 0}


class TestTemporalGatherCarriesVerifiedEmpty:
    """The TEMPORAL floor door gathers both sibling lanes via
    `_gather_temporal_context` — verified-empty must reach the floor
    context from there, counts included."""

    @pytest.mark.asyncio
    async def test_temporal_gather_carries_both_lanes_verified_empty(self):
        assembler = ContextAssembler()
        with (
            patch.object(assembler, "_gather_calendar_context", new=AsyncMock(return_value={})),
            patch.object(assembler, "_get_pending_todos_cached", new=AsyncMock(return_value=None)),
            patch.object(
                assembler,
                "_get_completed_todos_cached",
                new=AsyncMock(return_value={"completed_todos": [], "completed_todo_count": 0}),
            ),
            patch.object(
                assembler,
                "_get_projects_cached",
                new=AsyncMock(return_value={"projects": [], "project_count": 0}),
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
            ctx = await assembler._gather_temporal_context(user_id="u-1639")

        assert ctx.get("completed_todos") == []
        assert ctx.get("completed_todo_count") == 0
        assert ctx.get("projects") == []
        assert ctx.get("project_count") == 0


class TestVerifiedEmptyBlocksCarryNoTranscriptPhrases:
    """Regression pinning the #1544/#1570 transcript shape onto the sibling
    lanes: no deterministic surface may contain the misframe."""

    def test_sibling_verified_empty_block_contains_no_transcript_phrases(self):
        floor = ConversationalFloor(llm_client=MagicMock())
        out = floor._format_domain_context(
            {
                "projects": [],
                "project_count": 0,
                "completed_todos": [],
                "completed_todo_count": 0,
            }
        )
        for phrase in ("for this conversation", "on my end", "I don't see any"):
            assert phrase not in out, phrase
        # Both lanes' verified-empty lines render side by side.
        assert "PROJECTS: none" in out
        assert "COMPLETED TODOS: none" in out
