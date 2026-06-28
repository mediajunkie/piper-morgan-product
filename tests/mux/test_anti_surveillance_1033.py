"""
#1033 — Anti-surveillance guardrail unit tests + probe-set regression.

Two layers of testing:
1. Unit tests for the regex patterns in `services/mux/anti_surveillance.py`
   (each forbidden pattern matches expected strings + doesn't false-positive
   on safe variants).
2. Probe-set regression: load `tests/mux/probes/composted_experience_probes.json`
   and assert each probe gets the expected verdict (pass / reject).

Per #1033 audit dispositions May 3:
- Q3 strict: regex match → reject + fallback
- Q4 unit + regex coverage; LLM-end-to-end deferred to AAXT layer
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from services.mux.anti_surveillance import (
    SURVEILLANCE_FALLBACK_MESSAGE,
    SurveillancePhrasingViolation,
    assert_no_surveillance_phrasing,
    detect_surveillance_phrasing,
    safe_surface,
)


# =============================================================================
# Pattern coverage — each forbidden pattern fires
# =============================================================================


class TestPatternMatching:
    @pytest.mark.parametrize(
        "text,expected_label",
        [
            ("I've been watching your activity.", "i've-been-watching"),
            ("I have been watching what you do.", "i've-been-watching"),
            ("While you were away, I noticed things.", "while-you-were-away"),
            ("Based on my surveillance, you prefer mornings.", "based-on-my-surveillance"),
            ("I've been monitoring your work this week.", "i've-been-monitoring"),
            ("I have been monitoring your patterns.", "i've-been-monitoring"),
            ("Monitoring your activities revealed a pattern.", "monitoring-your-activity"),
            ("I've been tracking your meetings.", "i've-been-tracking"),
            ("I detected a pattern in your work.", "i-detected-pattern"),
            ("I detected the pattern of late nights.", "i-detected-pattern"),
            ("Based on your behavior at 2pm Tuesday...", "based-on-your-behavior-at"),
            ("After analyzing your data, I see...", "after-analyzing-your-data"),
            ("My analysis shows you prefer Slack.", "my-analysis-shows"),
            ("I've been observing your work patterns.", "i've-been-observing"),
        ],
    )
    def test_each_pattern_fires(self, text, expected_label):
        matched = detect_surveillance_phrasing(text)
        assert (
            expected_label in matched
        ), f"Expected pattern '{expected_label}' to match in: {text!r}; got {matched}"


# =============================================================================
# Safe variants — patterns don't false-positive
# =============================================================================


class TestSafeVariants:
    @pytest.mark.parametrize(
        "text",
        [
            "Having had some time to reflect, you tend to front-load smaller tasks.",
            "Looking back on our recent work together, things have evolved.",
            "Something occurred to me about the project.",
            "I've been thinking about how that meeting went.",
            "I noticed that you front-load smaller tasks.",  # bare "I noticed" is OK
            "It seems like the pattern is shifting.",
            "In hindsight, the iterative approach worked well.",
            "Looking at what we've done, a few things stand out.",
        ],
    )
    def test_safe_text_clean(self, text):
        matched = detect_surveillance_phrasing(text)
        assert (
            matched == []
        ), f"Safe text triggered surveillance pattern: {text!r}; matched: {matched}"


# =============================================================================
# Strict assertion behavior
# =============================================================================


class TestAssertNoSurveillance:
    def test_clean_text_passes_silently(self):
        # No raise
        assert_no_surveillance_phrasing("Having had some time to reflect, things stood out.")

    def test_violation_raises(self):
        with pytest.raises(SurveillancePhrasingViolation) as exc_info:
            assert_no_surveillance_phrasing("I've been watching your patterns.")
        assert "i've-been-watching" in exc_info.value.matched_labels

    def test_multiple_violations_all_reported(self):
        text = "I've been monitoring your work; I detected a pattern in your habits."
        with pytest.raises(SurveillancePhrasingViolation) as exc_info:
            assert_no_surveillance_phrasing(text)
        labels = exc_info.value.matched_labels
        assert "i've-been-monitoring" in labels
        assert "i-detected-pattern" in labels

    def test_empty_text_passes(self):
        # No raise (vacuously safe)
        assert_no_surveillance_phrasing("")
        assert_no_surveillance_phrasing(None)  # type: ignore[arg-type]


# =============================================================================
# safe_surface convenience wrapper
# =============================================================================


class TestSafeSurface:
    def test_clean_passes_through(self):
        text = "Having had some time to reflect, things look clearer."
        assert safe_surface(text) == text

    def test_violation_returns_fallback(self):
        bad = "I've been watching your work patterns."
        assert safe_surface(bad) == SURVEILLANCE_FALLBACK_MESSAGE

    def test_empty_returns_fallback(self):
        assert safe_surface("") == SURVEILLANCE_FALLBACK_MESSAGE
        assert safe_surface(None) == SURVEILLANCE_FALLBACK_MESSAGE


# =============================================================================
# Probe-set regression
# =============================================================================


PROBE_PATH = Path("tests/mux/probes/composted_experience_probes.json")


@pytest.fixture(scope="module")
def probes():
    """Load the probe set."""
    with PROBE_PATH.open() as f:
        data = json.load(f)
    return data["probes"]


def test_probe_set_size_meets_q2_target(probes):
    """Q2 disposition: ~10 probes for MVP. Allow 8-15 range for tuning."""
    assert 8 <= len(probes) <= 15, f"Probe set size {len(probes)} outside MVP target band"


def test_probe_set_has_pass_and_reject_examples(probes):
    """A regression set with only one verdict has no diagnostic value."""
    verdicts = {p["verdict"] for p in probes}
    assert "pass" in verdicts
    assert "reject" in verdicts


class TestProbeSetVerdicts:
    """Each probe should produce its expected verdict against the guardrail."""

    @pytest.fixture(autouse=True)
    def _load(self, probes):
        self.probes = probes

    def test_all_probes_match_expected_verdict(self):
        failures = []
        for probe in self.probes:
            text = probe["input"]
            expected = probe["verdict"]
            matched = detect_surveillance_phrasing(text)
            actual = "reject" if matched else "pass"
            if actual != expected:
                failures.append(
                    {
                        "id": probe["id"],
                        "input": text,
                        "expected": expected,
                        "actual": actual,
                        "matched": matched,
                        "rationale": probe.get("rationale"),
                    }
                )
        assert not failures, f"{len(failures)} probe(s) failed:\n" + "\n".join(
            f"  - {f['id']}: expected {f['expected']}, got {f['actual']}; matched={f['matched']}"
            for f in failures
        )

    def test_pass_probes_round_trip_safe_surface(self):
        """Probes labeled 'pass' should round-trip through safe_surface unchanged."""
        for probe in self.probes:
            if probe["verdict"] == "pass":
                assert (
                    safe_surface(probe["input"]) == probe["input"]
                ), f"Pass probe {probe['id']!r} got modified by safe_surface"

    def test_reject_probes_yield_fallback(self):
        """Probes labeled 'reject' should be replaced with the fallback."""
        for probe in self.probes:
            if probe["verdict"] == "reject":
                result = safe_surface(probe["input"])
                assert (
                    result == SURVEILLANCE_FALLBACK_MESSAGE
                ), f"Reject probe {probe['id']!r} did not yield fallback: {result!r}"
