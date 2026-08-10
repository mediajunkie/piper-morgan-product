"""#1570 (a) — internal context annotations must be structurally unable to
render in user copy.

PM live 2026-08-10: two floor replies carried the literal line
"[Available context: no todo data returned this turn]" / "... no project data
returned this turn]". That string exists NOWHERE in the codebase — it is the
MODEL imitating the floor's own scaffolding vocabulary (the system prompt
names "[Available context]" ~11 times; #1393's prompt-side prohibition,
commit 67538afe7, demonstrably does not hold under an empty context block).

The class kill is renderer-side (the carrier, not a phrase list): any
bracketed block that OPENS with one of our own scaffolding headers
("Available context", "Context:", "Reference binding", "Redirect context")
is machinery by construction — those headers are defined by _build_prompt /
_format_domain_context, never by user content — and is stripped from the
floor's output before it becomes user copy. Model paraphrases of the
CONTENT are untouched; only the bracketed machinery grammar is unrenderable.

Layer honesty (m-43): the respond()-level tests drive ConversationalFloor
with a stubbed LLM client and a static system-prompt base — they test the
renderer seam, not a live model or the full pipeline.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.intent_service.conversational_floor import (
    ConversationalFloor,
    FloorContext,
    strip_scaffolding_artifacts,
)

# The exact shapes from PM's live transcripts (issue #1570).
LEAK_TODOS = (
    "[Available context: no todo data returned this turn]\n"
    "I don't see any todos coming back right now."
)
LEAK_PROJECTS = (
    "Let me pull up your projects list now. "
    "[Available context: no project data returned this turn]"
)


class TestStripScaffoldingArtifacts:
    def test_strips_live_transcript_shape_todos(self):
        clean, n = strip_scaffolding_artifacts(LEAK_TODOS)
        assert n == 1
        assert "[Available context" not in clean
        assert "I don't see any todos coming back right now." in clean

    def test_strips_live_transcript_shape_projects_inline(self):
        clean, n = strip_scaffolding_artifacts(LEAK_PROJECTS)
        assert n == 1
        assert "[Available context" not in clean
        assert "Let me pull up your projects list now." in clean

    @pytest.mark.parametrize(
        "block",
        [
            "[Available context]",
            "[available context: nothing this turn]",
            "[Context: The user's message relates to 'STATUS'.]",
            "[Reference binding: resolve antecedents against the above]",
            "[Redirect context: steer back to sprint planning]",
            "[Available context about the user's current situation:\n- (none)\n]",
        ],
    )
    def test_every_scaffolding_header_family_is_stripped(self, block):
        clean, n = strip_scaffolding_artifacts(f"Sure thing.\n{block}\nDone.")
        assert n == 1
        assert "[" not in clean or "context" not in clean.lower().split("[")[-1][:20]
        assert "Sure thing." in clean
        assert "Done." in clean

    def test_legitimate_brackets_untouched(self):
        text = (
            "The [MVP] milestone has 3 open issues; see [1] for details. "
            "Issue #1570 [Beta Blocker] is one of them."
        )
        clean, n = strip_scaffolding_artifacts(text)
        assert n == 0
        assert clean == text

    def test_multiple_blocks_all_stripped(self):
        text = (
            "[Available context: none]\nHere's what I know.\n"
            "[Context: The user's message relates to 'PRIORITY'.]"
        )
        clean, n = strip_scaffolding_artifacts(text)
        assert n == 2
        assert "Here's what I know." in clean
        assert "[" not in clean

    def test_scaffolding_only_response_falls_back_nonempty(self):
        clean, n = strip_scaffolding_artifacts("[Available context: no todo data returned this turn]")
        assert n == 1
        assert clean.strip(), "a fully-scaffolding response must not become empty user copy"
        assert "[Available context" not in clean

    def test_empty_and_none_safe(self):
        assert strip_scaffolding_artifacts("")[0] == ""
        clean, n = strip_scaffolding_artifacts("plain answer")
        assert (clean, n) == ("plain answer", 0)

    def test_no_doubled_blank_lines_left_behind(self):
        text = "First paragraph.\n\n[Available context: none]\n\nSecond paragraph."
        clean, _ = strip_scaffolding_artifacts(text)
        assert "\n\n\n" not in clean


class TestFloorOutputNeverCarriesScaffolding:
    """respond()-level: the floor's user-visible message never contains the
    scaffolding header, no matter what the model emitted. RED before #1570:
    respond() returned the LLM text verbatim."""

    def _floor_with_llm_returning(self, text):
        llm = MagicMock()
        llm.complete = AsyncMock(return_value=text)
        return ConversationalFloor(
            llm_client=llm,
            system_prompt_base="You are Piper Morgan (test base).",
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("leak", [LEAK_TODOS, LEAK_PROJECTS])
    async def test_user_visible_message_never_contains_available_context(self, leak):
        floor = self._floor_with_llm_returning(leak)
        response = await floor.respond(
            FloorContext(
                user_message="what todos are pending?",
                session_id="sess-1570",
                user_id=None,  # no push path, no per-user prompt resolution
                intent_category="UNKNOWN",
            )
        )
        assert "[Available context" not in response.message, (
            "internal scaffolding leaked into user copy — the renderer must "
            "make this structurally impossible (#1570)"
        )
        assert response.message.strip(), "stripping must never yield empty user copy"

    @pytest.mark.asyncio
    async def test_clean_model_output_passes_through_verbatim(self):
        clean_text = "You have 3 pending todos — the closest deadline is Friday."
        floor = self._floor_with_llm_returning(clean_text)
        response = await floor.respond(
            FloorContext(
                user_message="what todos are pending?",
                session_id="sess-1570",
                user_id=None,
                intent_category="UNKNOWN",
            )
        )
        assert response.message == clean_text
