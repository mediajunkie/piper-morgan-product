"""#1544 — "what todos are pending?" wrong-empty with conversation-scoped framing.

PM live 2026-08-09: with 2+ todos existing (page-visible), the reply was
"I don't see any todos in your list right now — nothing's showing up on my
end for this conversation." Two defects composed that sentence:

1. The floor system prompt ITSELF supplied both halves — the empty-data
   guidance's example strings were "I don't see any todos in your list right
   now" and "... in this conversation" (conversational_floor.py, the
   never-fabricate section). The model assembled PM's reply directly from
   the prompt's own teaching examples.
2. Verified-empty was structurally indistinguishable from never-gathered:
   `_compute_pending_todos` returned None for a user with zero pending
   todos, so the floor NEVER had a definite "list checked, zero rows" fact
   to state — every empty case was an absence the model hedged over.

The data path itself is owner-scoped end to end
(TodoManagementService.list_todos(user_id=...) → todo_repo.get_todos_by_owner)
— there is no conversation-scoped todo read anywhere; the "for this
conversation" scope was pure copy, seeded by the prompt.

Layer honesty (m-43): these tests pin the PROMPT text and the deterministic
CONTEXT-RENDERER seam — not a live model. The real-Postgres half lives in
tests/integration/test_pending_todos_query_1544.py.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversational_floor import (
    FLOOR_SYSTEM_PROMPT_ADDENDUM,
    ConversationalFloor,
)

# The exact shape from PM's 2026-08-09 transcript (issue #1544).
PM_TRANSCRIPT_REPLY = (
    "I don't see any todos in your list right now — nothing's showing up "
    "on my end for this conversation."
)


def _fabrication_section() -> str:
    """The never-fabricate-user-data section of the floor prompt."""
    start = FLOOR_SYSTEM_PROMPT_ADDENDUM.index("CRITICAL — Never fabricate user data")
    end = FLOOR_SYSTEM_PROMPT_ADDENDUM.index("CRITICAL", start + 10)
    return FLOOR_SYSTEM_PROMPT_ADDENDUM[start:end]


class TestPromptNoLongerSeedsTheMisframe:
    """The prompt taught the model PM's reply, phrase by phrase. Pin that
    both seed strings are gone from the empty-data guidance."""

    def test_transcript_seed_phrase_removed(self):
        # The reply's first half was the prompt's own example sentence.
        assert "I don't see any todos" not in FLOOR_SYSTEM_PROMPT_ADDENDUM

    def test_no_conversation_scoping_in_data_absence_guidance(self):
        # The reply's second half ("for this conversation") came from the
        # adjacent calendar example ("in this conversation"). The fabrication
        # section must not contain ANY conversation-scoped framing — absent
        # data is a visibility limit, never a per-chat fact.
        section = _fabrication_section()
        assert "this conversation" not in section, section

    def test_fabrication_prohibition_still_present(self):
        # The rewrite must not weaken the actual anti-fabrication rule.
        section = _fabrication_section()
        assert "Do NOT invent" in section
        assert "Never invent" in section

    def test_prompt_teaches_verified_empty_vocabulary(self):
        # The prompt must tell the model what a checked-and-empty list looks
        # like ("PENDING TODOS: none") and license the account-level claim
        # only for that case.
        section = _fabrication_section()
        assert "PENDING TODOS: none" in section
        assert "account-level" in section


class TestRendererVerifiedEmpty:
    """`_format_domain_context` must render three DISTINCT todo states:
    populated, verified-empty, and failed — and absent must stay silent."""

    def setup_method(self):
        self.floor = ConversationalFloor(llm_client=MagicMock())

    def test_verified_empty_renders_checked_fact(self):
        out = self.floor._format_domain_context(
            {"pending_todos": [], "pending_todo_count": 0}
        )
        assert "PENDING TODOS: none" in out
        assert "checked" in out
        # The account-level instruction, never a conversation-scoped hedge.
        assert "account-level" in out
        assert "this conversation" not in out
        assert "showing up" not in out

    def test_populated_renders_each_todo(self):
        out = self.floor._format_domain_context(
            {
                "pending_todos": [
                    {"text": "Review beta feedback", "deadline_proximity": "none"},
                    {"text": "Draft the release notes", "deadline_proximity": "none"},
                ],
                "pending_todo_count": 2,
            }
        )
        assert "PENDING TODOS (2)" in out
        assert "Review beta feedback" in out
        assert "Draft the release notes" in out
        assert "PENDING TODOS: none" not in out

    def test_absent_key_renders_no_todo_lines(self):
        out = self.floor._format_domain_context({"current_time": "now-ish"})
        assert "PENDING TODOS" not in out
        assert "Pending todo" not in out

    def test_source_failed_rendering_unchanged(self):
        # #1573's honesty line must survive the #1544 change untouched.
        out = self.floor._format_domain_context({"pending_todos_source_failed": True})
        assert "Todo check FAILED" in out
        assert "do not claim there are none" in out


class TestAssemblerVerifiedEmpty:
    """Zero pending todos is a FACT (owner-scoped read succeeded), not an
    absence — it must survive the compute → cache → gather pipeline."""

    @pytest.mark.asyncio
    async def test_compute_returns_verified_empty_not_none(self):
        mock_svc = MagicMock()
        mock_svc.list_todos = AsyncMock(return_value=[])

        from uuid import uuid4

        assembler = ContextAssembler()
        with patch(
            "services.todo.todo_management_service.TodoManagementService",
            return_value=mock_svc,
        ):
            result = await assembler._compute_pending_todos(str(uuid4()))

        assert result == {"pending_todos": [], "pending_todo_count": 0}, (
            "verified-empty must be a definite fact, not None "
            "(None is indistinguishable from never-gathered)"
        )
        # Owner-scoping assertion: the read was keyed by user, nothing else.
        _, call_kwargs = mock_svc.list_todos.call_args
        assert "user_id" in call_kwargs
        assert call_kwargs.get("include_completed") is False

    @pytest.mark.asyncio
    async def test_cached_layer_passes_verified_empty_through(self):
        mock_svc = MagicMock()
        mock_svc.list_todos = AsyncMock(return_value=[])

        from uuid import uuid4

        assembler = ContextAssembler()
        with patch(
            "services.todo.todo_management_service.TodoManagementService",
            return_value=mock_svc,
        ):
            result = await assembler._get_pending_todos_cached(str(uuid4()), limit=5)

        assert result == {"pending_todos": [], "pending_todo_count": 0}

    @pytest.mark.asyncio
    async def test_status_gather_carries_verified_empty_and_count(self):
        """The QUERY floor door gathers via _gather_status_priority_context
        (the #960 else-branch) — verified-empty must reach the floor context
        from there, count included."""
        assembler = ContextAssembler()
        with patch.object(
            assembler, "_gather_calendar_context", new=AsyncMock(return_value={})
        ), patch.object(
            assembler, "_get_user_context_cached", new=AsyncMock(return_value=None)
        ), patch.object(
            assembler,
            "_get_pending_todos_cached",
            new=AsyncMock(return_value={"pending_todos": [], "pending_todo_count": 0}),
        ), patch.object(
            assembler,
            "_gather_blocked_items_context",
            new=AsyncMock(return_value={}),
        ), patch.object(
            assembler,
            "_gather_active_milestones_context",
            new=AsyncMock(return_value={}),
        ), patch.object(
            assembler,
            "_gather_recent_activity_context",
            new=AsyncMock(return_value={}),
        ), patch.object(
            assembler,
            "_gather_high_priority_issues_context",
            new=AsyncMock(return_value={}),
        ), patch(
            "services.integrations.integration_status_service.IntegrationStatusService"
        ):
            ctx = await assembler._gather_status_priority_context(user_id="u-1544")

        assert ctx.get("pending_todos") == []
        assert ctx.get("pending_todo_count") == 0
        assert "pending_todos_source_failed" not in ctx


class TestTranscriptShapeEndToEndAtTheDeterministicLayer:
    """Regression pinning PM's transcript shape: given the verified-empty
    context the assembler now produces, the rendered context block hands the
    model a definite fact — the exact gap PM's reply hedged over no longer
    exists, and no deterministic surface contains the misframe."""

    def test_verified_empty_block_contains_no_transcript_phrases(self):
        floor = ConversationalFloor(llm_client=MagicMock())
        out = floor._format_domain_context(
            {"pending_todos": [], "pending_todo_count": 0}
        )
        for phrase in ("for this conversation", "on my end", "I don't see any todos"):
            assert phrase not in out, phrase

    def test_populated_block_contains_no_transcript_phrases(self):
        floor = ConversationalFloor(llm_client=MagicMock())
        out = floor._format_domain_context(
            {
                "pending_todos": [{"text": "repro-1544", "deadline_proximity": "none"}],
                "pending_todo_count": 1,
            }
        )
        for phrase in ("for this conversation", "on my end"):
            assert phrase not in out, phrase
