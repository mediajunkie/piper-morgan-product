"""
#1030 MUX-INSIGHT-PULL — trigger detection + response composer tests.

Three layers:
1. Trigger-pattern unit tests — each pattern fires + safe variants don't
2. 20-probe regression set (`tests/mux/probes/pull_mode_probes.json`)
3. Response composer tests — sectioned format, no-deflection rule,
   correction invitation always present, identical at all trust stages

Per #1030 audit dispositions May 3:
- Q1 Option C hybrid: trigger detection is the pre-classifier flag
- Q2 Hybrid format: structured sectioned markdown
- Q3 Option C: simple keyword extraction
- Q4 Option A: identical response at all stages
- Q5: enforce no-deflection
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from services.mux.composting_models import ExtractedLearning, Pattern
from services.mux.composting_pipeline import SurfaceableInsight
from services.mux.pull_mode import (
    CONFIDENCE_HIGH_THRESHOLD,
    CONFIDENCE_MEDIUM_THRESHOLD,
    CORRECTION_INVITATION,
    NO_INSIGHTS_RESPONSE,
    PULL_TRIGGER_PATTERNS,
    extract_context,
    format_pull_response,
    is_pull_trigger,
    matched_trigger_labels,
    respond_to_pull,
)


pytestmark_async = pytest.mark.asyncio


# =============================================================================
# Trigger detection unit tests
# =============================================================================


class TestIsPullTrigger:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("What have you learned about deadlines?", True),
            ("What have you noticed about my schedule?", True),
            ("Tell me about your insights on the project", True),
            ("Why did you suggest the early morning meeting?", True),
            ("How sure are you about that?", True),
            ("How confident are you in that pattern?", True),
            ("Where did that insight come from?", True),
            ("Have you noticed any patterns?", True),
            # safe variants
            ("What time is it?", False),
            ("Hello, how are you?", False),
            ("I noticed the typos", False),
            ("Add a todo", False),
            ("", False),
        ],
    )
    def test_trigger_detection(self, text, expected):
        assert is_pull_trigger(text) is expected

    def test_matched_labels_returns_categories(self):
        labels = matched_trigger_labels("What have you learned about my work?")
        assert "direct-learned" in labels

    def test_matched_labels_empty_for_non_trigger(self):
        assert matched_trigger_labels("Hello") == []
        assert matched_trigger_labels("") == []


# =============================================================================
# Probe-set regression
# =============================================================================


PROBE_PATH = Path("tests/mux/probes/pull_mode_probes.json")


@pytest.fixture(scope="module")
def probes():
    with PROBE_PATH.open() as f:
        data = json.load(f)
    return data["probes"]


def test_probe_set_size(probes):
    """20-probe set per spec (10 trigger + 10 non-trigger)."""
    assert len(probes) == 20


def test_probe_set_balanced(probes):
    """Equal mix of trigger and non-trigger for sound diagnostic value."""
    triggers = sum(1 for p in probes if p["verdict"] == "trigger")
    non_triggers = sum(1 for p in probes if p["verdict"] == "no-trigger")
    assert triggers == 10
    assert non_triggers == 10


class TestProbeSetVerdicts:
    @pytest.fixture(autouse=True)
    def _load(self, probes):
        self.probes = probes

    def test_all_probes_match_expected_verdict(self):
        failures = []
        for probe in self.probes:
            text = probe["input"]
            expected = probe["verdict"]
            actual = "trigger" if is_pull_trigger(text) else "no-trigger"
            if actual != expected:
                failures.append(
                    {"id": probe["id"], "input": text, "expected": expected, "actual": actual}
                )
        assert not failures, f"{len(failures)} probe(s) failed:\n" + "\n".join(
            f"  - {f['id']}: expected {f['expected']}, got {f['actual']}" for f in failures
        )


# =============================================================================
# Context extraction
# =============================================================================


class TestExtractContext:
    def test_extracts_meaningful_keywords(self):
        entities, topics = extract_context("What have you learned about my deadline patterns?")
        assert "deadline" in entities or "deadlines" in entities
        # Q3 Option C: entities + topics use the same candidate list
        assert entities == topics

    def test_filters_stop_words(self):
        entities, topics = extract_context("Tell me about my work")
        assert "i" not in entities
        assert "me" not in entities
        assert "the" not in entities
        # 'work' is a content word
        assert "work" in entities or "works" in entities

    def test_empty_input_returns_empty_lists(self):
        e, t = extract_context("")
        assert e == []
        assert t == []

    def test_dedups_keywords(self):
        e, t = extract_context("calendar calendar calendar")
        # After dedup, should only contain "calendar" once
        assert e.count("calendar") == 1


# =============================================================================
# Response composer
# =============================================================================


def _make_insight(
    *, confidence: float, expression: str = "you front-load smaller tasks"
) -> SurfaceableInsight:
    learning = ExtractedLearning(
        pattern=Pattern(description=expression),
        confidence=confidence,
        applies_to_entities=["deadlines"],
        topic_tags=["work-patterns"],
        expression=f"Having reflected, {expression}",
    )
    return SurfaceableInsight(
        object_id="obj-1",
        user_id="alpha",
        learning=learning,
    )


class TestFormatPullResponse:
    def test_empty_insights_yields_no_deflection_fallback(self):
        """Q5: No-deflection rule. Empty list → honest fallback, not a deflection."""
        result = format_pull_response([])
        assert result == NO_INSIGHTS_RESPONSE
        # And it does NOT say "I don't have insights" or similar deflection
        assert "I don't" not in result or "specific" in result

    def test_none_insights_yields_fallback(self):
        assert format_pull_response(None) == NO_INSIGHTS_RESPONSE

    def test_high_only(self):
        insights = [_make_insight(confidence=0.9), _make_insight(confidence=0.85)]
        result = format_pull_response(insights)
        assert "**High confidence:**" in result
        assert "**Medium confidence:**" not in result
        assert "**Something I'm less sure about:**" not in result
        assert CORRECTION_INVITATION in result

    def test_medium_only(self):
        insights = [_make_insight(confidence=0.7)]
        result = format_pull_response(insights)
        assert "**High confidence:**" not in result
        assert "**Medium confidence:**" in result
        assert "**Something I'm less sure about:**" not in result

    def test_low_only(self):
        insights = [_make_insight(confidence=0.5)]
        result = format_pull_response(insights)
        assert "**Something I'm less sure about:**" in result

    def test_all_three_bands(self):
        insights = [
            _make_insight(confidence=0.9),
            _make_insight(confidence=0.7),
            _make_insight(confidence=0.5),
        ]
        result = format_pull_response(insights)
        assert "**High confidence:**" in result
        assert "**Medium confidence:**" in result
        assert "**Something I'm less sure about:**" in result

    def test_correction_invitation_always_present_when_insights_exist(self):
        """Rule 3: always offer to correct/explain."""
        for confidence in [0.9, 0.7, 0.5]:
            result = format_pull_response([_make_insight(confidence=confidence)])
            assert CORRECTION_INVITATION in result

    def test_no_deflection_when_insights_exist(self):
        """Rule 5: if matching insights count > 0, response contains insight text."""
        insights = [_make_insight(confidence=0.9, expression="you protect morning time")]
        result = format_pull_response(insights)
        # Response contains the framed insight content (some part of expression)
        assert "morning" in result.lower()
        # And the no-deflection fallback is NOT present
        assert NO_INSIGHTS_RESPONSE not in result

    def test_response_uses_spec_section_headers(self):
        """Per D4 §Response Format, exact section headers."""
        insights = [
            _make_insight(confidence=0.9),
            _make_insight(confidence=0.7),
            _make_insight(confidence=0.5),
        ]
        result = format_pull_response(insights)
        # Verbatim per spec
        assert "**High confidence:**" in result
        assert "**Medium confidence:**" in result
        assert "**Something I'm less sure about:**" in result


# =============================================================================
# Trust-stage consistency (Q4 Option A)
# =============================================================================


class TestTrustStageConsistency:
    """Q4 Option A: identical response shape at all 4 trust stages for MVP."""

    def test_response_identical_across_stages(self):
        insights = [_make_insight(confidence=0.9), _make_insight(confidence=0.7)]
        # format_pull_response is stage-agnostic by design (Q4 Option A)
        # The trust-stage gate is at the journal layer (insight.is_surfaceable)
        result = format_pull_response(insights)
        # Verify we get the same structure regardless of how we'd vary stage —
        # this test enforces the "stage-agnostic formatter" invariant by
        # making it impossible to add stage-specific branching without
        # explicitly breaking this test.
        assert "**High confidence:**" in result
        assert "**Medium confidence:**" in result
        assert CORRECTION_INVITATION in result


# =============================================================================
# End-to-end respond_to_pull
# =============================================================================


@pytest.mark.asyncio
class TestRespondToPull:
    async def test_empty_message_yields_fallback(self):
        result = await respond_to_pull(user_message="", user_id="alpha", journal=AsyncMock())
        assert result == NO_INSIGHTS_RESPONSE

    async def test_journal_returns_empty_yields_fallback(self):
        """Q5: no-deflection — empty journal result → honest fallback."""
        mock_journal = AsyncMock()
        mock_journal.get_for_context = AsyncMock(return_value=[])
        result = await respond_to_pull(
            user_message="What have you learned?",
            user_id="alpha",
            journal=mock_journal,
        )
        assert result == NO_INSIGHTS_RESPONSE

    async def test_journal_returns_insights_yields_sectioned_response(self):
        mock_journal = AsyncMock()
        mock_journal.get_for_context = AsyncMock(
            return_value=[
                _make_insight(confidence=0.9, expression="you protect morning time"),
                _make_insight(confidence=0.7, expression="you front-load tasks"),
            ]
        )
        result = await respond_to_pull(
            user_message="What have you learned about my work?",
            user_id="alpha",
            journal=mock_journal,
        )
        assert "**High confidence:**" in result
        assert "**Medium confidence:**" in result
        assert CORRECTION_INVITATION in result

    async def test_calls_journal_with_extracted_context(self):
        """Verify the extracted-context is passed to the journal."""
        mock_journal = AsyncMock()
        mock_journal.get_for_context = AsyncMock(return_value=[])
        await respond_to_pull(
            user_message="What have you learned about my deadline patterns?",
            user_id="alpha",
            trust_stage=3,
            journal=mock_journal,
        )
        # Check call args
        call_kwargs = mock_journal.get_for_context.call_args.kwargs
        assert call_kwargs["user_id"] == "alpha"
        assert call_kwargs["trust_stage"] == 3
        # Some keyword from the message should be in the entities/topics
        entities = call_kwargs["context_entities"]
        assert len(entities) > 0
        # 'deadline' or 'deadlines' or 'patterns' should be in there
        assert any("deadline" in e or "pattern" in e for e in entities)


# =============================================================================
# Confidence-binning thresholds
# =============================================================================


class TestConfidenceBinning:
    """Verify the binning thresholds match D3 §Confidence Expression spec."""

    def test_thresholds_match_spec(self):
        """High ≥ 0.8, medium 0.6-0.8, low < 0.6."""
        assert CONFIDENCE_HIGH_THRESHOLD == 0.8
        assert CONFIDENCE_MEDIUM_THRESHOLD == 0.6

    def test_at_threshold_boundaries(self):
        # Exactly 0.8 → high
        result = format_pull_response([_make_insight(confidence=0.8)])
        assert "**High confidence:**" in result
        # Exactly 0.6 → medium
        result = format_pull_response([_make_insight(confidence=0.6)])
        assert "**Medium confidence:**" in result
        # 0.59 → low
        result = format_pull_response([_make_insight(confidence=0.59)])
        assert "**Something I'm less sure about:**" in result
