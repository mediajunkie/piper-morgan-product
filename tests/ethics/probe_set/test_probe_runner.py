"""
#1004 Step 8 Phase B — Tests for the probe runner harness.

Uses a stub detector to verify the runner correctly classifies divergences
across all six diff types in Architect's taxonomy. No live LLM calls — Phase
C wires this to the actual SemanticBoundaryDetector for calibration runs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import pytest

from services.ethics.semantic_boundary_detector import SemanticDetectorOutput
from tests.ethics.probe_set.probe_definitions import (
    ALL_PROBES,
    FALSE_POSITIVE_PROBES,
    Probe,
    VIOLATION_PROBES,
    probe_by_id,
    probes_by_category,
)
from tests.ethics.probe_set.probe_runner import (
    format_divergence_table,
    run_probe,
    run_probe_set,
    summarize_results,
)


# ----- Test fixtures -----


@dataclass
class _StubDetector:
    """Minimal detector stub for runner tests. Maps probe_input -> output
    via canned_responses dict; default-fallback returns NONE if no mapping."""

    canned_responses: Dict[str, SemanticDetectorOutput]

    async def detect(
        self,
        message: str,
        context: Optional[dict] = None,
    ) -> SemanticDetectorOutput:
        if message in self.canned_responses:
            return self.canned_responses[message]
        # Default: no violation
        return SemanticDetectorOutput(
            violation_detected=False,
            category="none",
            confidence=0.1,
            reasoning="stub default",
            redirect_hint=None,
        )


def _harassment_violation_output(
    confidence: float = 0.92,
    redirect_hint: Optional[str] = (
        "Surface the underlying SLA gap through proper supervisory channels"
    ),
) -> SemanticDetectorOutput:
    """Default-safe harassment violation output. The default redirect_hint
    is hand-curated to NOT contain any 6+ char token from h-1's input nor
    any legacy harassment pattern words; tests overriding the hint are
    expected to manage that themselves."""
    return SemanticDetectorOutput(
        violation_detected=True,
        category="harassment",
        confidence=confidence,
        reasoning="targeting a colleague's standing",
        redirect_hint=redirect_hint,
    )


def _none_output(confidence: float = 0.95) -> SemanticDetectorOutput:
    return SemanticDetectorOutput(
        violation_detected=False,
        category="none",
        confidence=confidence,
        reasoning="legitimate work",
        redirect_hint=None,
    )


# ----- Probe definitions sanity -----


class TestProbeDefinitions:
    def test_total_probe_count(self):
        assert len(ALL_PROBES) == 20
        assert len(VIOLATION_PROBES) == 15
        assert len(FALSE_POSITIVE_PROBES) == 5

    def test_three_probes_per_category(self):
        for cat in [
            "harassment",
            "professional",
            "personal",
            "data_privacy",
            "inappropriate_content",
        ]:
            cat_probes = probes_by_category(cat)
            assert len(cat_probes) == 3, f"{cat} has {len(cat_probes)} probes"

    def test_all_violation_probes_have_expected_hint_shape(self):
        for p in VIOLATION_PROBES:
            assert p.expected_redirect_hint_shape is not None
            assert p.expected_violation is True

    def test_false_positive_probes_have_no_hint_shape(self):
        for p in FALSE_POSITIVE_PROBES:
            assert p.expected_redirect_hint_shape is None
            assert p.expected_violation is False
            assert p.expected_category == "none"

    def test_unique_probe_ids(self):
        ids = [p.probe_id for p in ALL_PROBES]
        assert len(ids) == len(set(ids))

    def test_anchor_coverage_carried_forward(self):
        # Phase E S1 r2 / S2 / S3 + #1003 V1 / V3 should appear as anchors
        anchors = [p.anchor for p in ALL_PROBES]
        anchor_text = " | ".join(anchors)
        assert "Phase E S1 r2" in anchor_text
        assert "Phase E S2" in anchor_text
        assert "Phase E S3" in anchor_text
        assert "#1003 V1" in anchor_text
        assert "#1003 V3" in anchor_text

    def test_probe_lookup(self):
        h1 = probe_by_id("h-1")
        assert h1 is not None
        assert h1.expected_category == "harassment"
        assert probe_by_id("nonexistent") is None


# ----- Runner: no-divergence path -----


class TestRunnerNoDivergence:
    @pytest.mark.asyncio
    async def test_violation_probe_clean_pass(self):
        h1 = probe_by_id("h-1")
        detector = _StubDetector(
            canned_responses={h1.input: _harassment_violation_output()}
        )
        result = await run_probe(h1, detector)
        assert result.passed
        assert result.diff_types == []
        assert result.hint_assertion_failures == []
        assert result.latency_ms >= 0

    @pytest.mark.asyncio
    async def test_false_positive_probe_clean_pass(self):
        fp1 = probe_by_id("fp-1")
        detector = _StubDetector(canned_responses={fp1.input: _none_output()})
        result = await run_probe(fp1, detector)
        assert result.passed
        assert result.diff_types == []


# ----- Runner: each diff type -----


class TestRunnerDiffTypes:
    @pytest.mark.asyncio
    async def test_unexpected_pass_when_violation_probe_classified_none(self):
        h1 = probe_by_id("h-1")
        detector = _StubDetector(canned_responses={h1.input: _none_output()})
        result = await run_probe(h1, detector)
        assert "unexpected_pass" in result.diff_types
        assert not result.passed

    @pytest.mark.asyncio
    async def test_unexpected_violation_when_fp_probe_classified_violation(self):
        fp1 = probe_by_id("fp-1")
        detector = _StubDetector(
            canned_responses={fp1.input: _harassment_violation_output()}
        )
        result = await run_probe(fp1, detector)
        assert "unexpected_violation" in result.diff_types

    @pytest.mark.asyncio
    async def test_category_mismatch(self):
        h1 = probe_by_id("h-1")
        # Detector fires violation but with wrong category
        wrong_cat_output = SemanticDetectorOutput(
            violation_detected=True,
            category="professional",  # h-1 expects harassment
            confidence=0.92,
            reasoning="stub mismatch",
            redirect_hint="Surface the SLA gap via supervisory escalation",
        )
        detector = _StubDetector(canned_responses={h1.input: wrong_cat_output})
        result = await run_probe(h1, detector)
        assert "category_mismatch" in result.diff_types

    @pytest.mark.asyncio
    async def test_confidence_band_miss_below_low(self):
        h1 = probe_by_id("h-1")  # expects [0.85, 1.0]
        low_conf_output = _harassment_violation_output(confidence=0.50)
        detector = _StubDetector(canned_responses={h1.input: low_conf_output})
        result = await run_probe(h1, detector)
        assert "confidence_band_miss" in result.diff_types

    @pytest.mark.asyncio
    async def test_confidence_band_miss_above_high(self):
        # p-2 expects [0.6, 0.85] — fire at 0.99 to trigger above-band
        p2 = probe_by_id("p-2")
        high_conf_output = SemanticDetectorOutput(
            violation_detected=True,
            category="professional",
            confidence=0.99,
            reasoning="stub above band",
            redirect_hint="Limit assessment to observable workflow signals",
        )
        detector = _StubDetector(canned_responses={p2.input: high_conf_output})
        result = await run_probe(p2, detector)
        assert "confidence_band_miss" in result.diff_types

    @pytest.mark.asyncio
    async def test_hint_shape_violation_input_substring_leak(self):
        h1 = probe_by_id("h-1")
        # Hint quotes phrase from h-1 input verbatim
        leaky_output = _harassment_violation_output(
            redirect_hint=(
                "When you want to make him look incompetent, pause and "
                "consider escalation"
            )
        )
        detector = _StubDetector(canned_responses={h1.input: leaky_output})
        result = await run_probe(h1, detector)
        assert "hint_shape_violation" in result.diff_types
        assert result.has_hint_safety_violation
        assert any(
            f.rule == "input_substring_leak"
            for f in result.hint_assertion_failures
        )

    @pytest.mark.asyncio
    async def test_hint_shape_violation_legacy_pattern_word(self):
        h1 = probe_by_id("h-1")
        # Hint contains legacy harassment pattern word "harassment"
        leaky_output = _harassment_violation_output(
            redirect_hint="Refer harassment concerns through HR channels"
        )
        detector = _StubDetector(canned_responses={h1.input: leaky_output})
        result = await run_probe(h1, detector)
        assert "hint_shape_violation" in result.diff_types
        assert any(
            f.rule == "legacy_pattern_word"
            for f in result.hint_assertion_failures
        )

    @pytest.mark.asyncio
    async def test_hint_shape_violation_refusal_template(self):
        h1 = probe_by_id("h-1")
        leaky_output = _harassment_violation_output(
            redirect_hint=(
                "I cannot help with that approach; consider escalation"
            )
        )
        detector = _StubDetector(canned_responses={h1.input: leaky_output})
        result = await run_probe(h1, detector)
        assert "hint_shape_violation" in result.diff_types
        assert any(
            f.rule == "refusal_template"
            for f in result.hint_assertion_failures
        )


# ----- Runner: batch + summary -----


class TestRunnerBatch:
    @pytest.mark.asyncio
    async def test_run_probe_set_returns_in_order(self):
        h1 = probe_by_id("h-1")
        h2 = probe_by_id("h-2")
        canned = {
            h1.input: _harassment_violation_output(),
            h2.input: _harassment_violation_output(),
        }
        detector = _StubDetector(canned_responses=canned)
        results = await run_probe_set([h1, h2], detector)
        assert [r.probe_id for r in results] == ["h-1", "h-2"]
        assert all(r.passed for r in results)

    @pytest.mark.asyncio
    async def test_summarize_results_counts(self):
        h1 = probe_by_id("h-1")
        h2 = probe_by_id("h-2")
        canned = {
            h1.input: _harassment_violation_output(),  # passes
            h2.input: _none_output(),  # unexpected_pass
        }
        detector = _StubDetector(canned_responses=canned)
        results = await run_probe_set([h1, h2], detector)
        summary = summarize_results(results)
        assert summary["total"] == 2
        assert summary["passed"] == 1
        assert summary["failed"] == 1
        assert summary["diff_type_counts"]["unexpected_pass"] == 1

    @pytest.mark.asyncio
    async def test_format_divergence_table_only_includes_failures(self):
        h1 = probe_by_id("h-1")
        h2 = probe_by_id("h-2")
        canned = {
            h1.input: _harassment_violation_output(),  # passes
            h2.input: _none_output(),  # unexpected_pass
        }
        detector = _StubDetector(canned_responses=canned)
        results = await run_probe_set([h1, h2], detector)
        table = format_divergence_table(results)
        assert "h-2" in table  # divergence row included
        assert "h-1" not in table  # passing row excluded
        assert "unexpected_pass" in table


# ----- Runner: full probe set against permissive stub -----


class TestRunnerFullSet:
    @pytest.mark.asyncio
    async def test_full_probe_set_runs_without_exception(self):
        # Permissive stub: returns expected output for each probe so the
        # full 20-probe sweep completes cleanly. Verifies the data
        # structure + runner are consistent end-to-end.
        canned: Dict[str, SemanticDetectorOutput] = {}
        # Hand-curated safe hint: avoids 6+ char tokens that appear in any
        # of the 20 probe inputs + avoids all legacy pattern words + avoids
        # refusal templates. Verified zero-leak by harness sweep.
        safe_hint = "Use proper escalation paths anchored on observable outcomes"
        for probe in VIOLATION_PROBES:
            canned[probe.input] = SemanticDetectorOutput(
                violation_detected=True,
                category=probe.expected_category,
                confidence=(
                    (probe.expected_confidence_range[0]
                     + probe.expected_confidence_range[1]) / 2
                ),
                reasoning="stub matches expectation",
                redirect_hint=safe_hint,
            )
        for probe in FALSE_POSITIVE_PROBES:
            canned[probe.input] = SemanticDetectorOutput(
                violation_detected=False,
                category="none",
                confidence=(
                    (probe.expected_confidence_range[0]
                     + probe.expected_confidence_range[1]) / 2
                ),
                reasoning="stub says legitimate",
                redirect_hint=None,
            )
        detector = _StubDetector(canned_responses=canned)
        results = await run_probe_set(ALL_PROBES, detector)
        assert len(results) == 20
        # Permissive stub should produce zero divergences
        summary = summarize_results(results)
        assert summary["passed"] == 20, (
            f"Unexpected divergences: {summary['diff_type_counts']}"
        )
