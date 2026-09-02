"""1717 — the five source-failed honest-degrade directives compose additively.

CXO verified in source (voice-watch memo, 2026-09-01) that
``_format_domain_context`` has five independent source-failed directive
sites — reminders, first-contact GitHub, projects, pending todos,
completed todos — with **no aggregation, no cap, no co-occurrence
handling**. These tests pin that composition fact.

Layer honesty (m-43): this pins the deterministic CONTEXT-RENDERER and the
composed PROMPT — not what a live model does with five directives at once
(that evidence lives in the 1717 live-probe transcripts, not here).

These are deliberately pins of CURRENT behavior, including the part CXO
flagged as a voice risk: when an aggregated-directive fix lands (CXO+Lead
design), the all-five and two-of-five tests below are the ones that MUST
start failing — that is their job as the regression seam for the fix.
"""

from unittest.mock import MagicMock

import pytest

from services.intent_service.conversational_floor import (
    ConversationalFloor,
    FloorContext,
)

# flag key in domain_context -> the directive line it appends (stable prefix)
DIRECTIVES = {
    "source_failed": "- Reminder check FAILED:",
    "first_contact_source_failed": "- First-exchange GitHub check FAILED:",
    "projects_source_failed": "- Project check FAILED:",
    "pending_todos_source_failed": "- Todo check FAILED:",
    "completed_todos_source_failed": "- Completed-todo check FAILED:",
}

ALL_FIVE = {flag: True for flag in DIRECTIVES}


def _floor() -> ConversationalFloor:
    return ConversationalFloor(llm_client=MagicMock())


class TestAllFiveCompose:
    """5-of-5: every directive lands, independently and additively."""

    def test_all_five_flags_render_all_five_directives(self):
        out = _floor()._format_domain_context(dict(ALL_FIVE))
        for flag, directive in DIRECTIVES.items():
            assert directive in out, f"{flag} directive missing from renderer output"

    def test_composition_is_additive_no_aggregation_no_cap(self):
        # The composition fact itself: five armed flags produce exactly five
        # separate "check FAILED" lines — nothing merges, caps, or
        # substitutes an aggregate. (The content lists in the same renderer
        # ARE capped; the failure lines are not.)
        out = _floor()._format_domain_context(dict(ALL_FIVE))
        assert out.count("check FAILED:") == 5

    def test_each_directive_carries_its_own_honesty_guard(self):
        # Every one of the five independently instructs "don't claim empty" —
        # five separate honesty guards, which is what makes the composed
        # shape a litany rather than one sentence.
        out = _floor()._format_domain_context(dict(ALL_FIVE))
        assert out.count("claim") >= 5

    def test_composed_prompt_carries_all_five(self):
        # One level up (m-43): the PROMPT the floor would hand the LLM —
        # not just the domain block in isolation — carries all five.
        ctx = FloorContext(
            user_message="good morning, what's my status?",
            session_id="pin-1717",
            domain_context=dict(ALL_FIVE),
        )
        prompt = _floor()._build_prompt(ctx)
        for flag, directive in DIRECTIVES.items():
            assert directive in prompt, f"{flag} directive missing from composed prompt"
        assert prompt.count("check FAILED:") == 5


class TestPartialShapes:
    """2-of-5 and 1-of-5: exactly the armed flags render, no bleed."""

    def test_two_of_five_renders_exactly_those_two(self):
        armed = {"source_failed": True, "projects_source_failed": True}
        out = _floor()._format_domain_context(armed)
        assert DIRECTIVES["source_failed"] in out
        assert DIRECTIVES["projects_source_failed"] in out
        for flag in DIRECTIVES.keys() - armed.keys():
            assert DIRECTIVES[flag] not in out, f"{flag} rendered while unarmed"
        assert out.count("check FAILED:") == 2

    @pytest.mark.parametrize("flag", sorted(DIRECTIVES))
    def test_one_of_five_renders_exactly_that_one(self, flag):
        out = _floor()._format_domain_context({flag: True})
        assert DIRECTIVES[flag] in out
        for other in DIRECTIVES.keys() - {flag}:
            assert DIRECTIVES[other] not in out, f"{other} rendered while unarmed"
        assert out.count("check FAILED:") == 1

    def test_zero_flags_render_no_failure_lines(self):
        out = _floor()._format_domain_context({"current_time": "now-ish"})
        assert "check FAILED:" not in out
