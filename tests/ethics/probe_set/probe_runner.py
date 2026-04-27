"""
#1004 Step 8 Phase B — Probe runner harness.

Async helper that runs a single probe against a SemanticBoundaryDetector
instance, applies the redirect_hint shape regression assertions, classifies
divergences per Architect's diff-type taxonomy, and returns a typed result
record.

The runner is detector-agnostic for testability — Phase B uses a stub
detector for harness self-tests; Phase C wires it to the live
`SemanticBoundaryDetector` from `services/ethics/semantic_boundary_detector.py`
for actual calibration rounds.

Diff-type taxonomy (per Architect Step 8 guidance + CXO probe set v0.1):
- category_mismatch — wrong category
- confidence_band_miss — confidence outside expected range
- hint_shape_drift — hint exists but wrong category-shape (manual review)
- unexpected_violation — false positive (probe expected NONE but got violation)
- unexpected_pass — false negative (probe expected violation but got NONE)
- hint_shape_violation — redirect_hint output violates one or more
  audit-safety regression assertions (CI-gate failure, not quality issue)
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, List, Optional, Protocol

from services.ethics.semantic_boundary_detector import SemanticDetectorOutput
from tests.ethics.probe_set.probe_definitions import Probe
from tests.ethics.probe_set.redirect_hint_assertions import (
    AssertionFailure,
    assert_redirect_hint_shape_safe,
)


DiffType = str  # one of: category_mismatch, confidence_band_miss,
# hint_shape_drift, unexpected_violation, unexpected_pass, hint_shape_violation


class _DetectorProtocol(Protocol):
    """Minimal interface the probe runner needs from a detector. The real
    SemanticBoundaryDetector satisfies this; test stubs implement it
    locally."""

    async def detect(
        self,
        message: str,
        context: Optional[dict] = None,
    ) -> SemanticDetectorOutput:
        ...


@dataclass
class ProbeRunResult:
    """Output of running one probe against the detector."""

    probe_id: str
    probe_input: str
    expected_violation: bool
    expected_category: str
    expected_confidence_range: tuple
    actual_output: SemanticDetectorOutput
    latency_ms: float
    hint_assertion_failures: List[AssertionFailure] = field(default_factory=list)
    diff_types: List[DiffType] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        """A probe passes when no diff types fired."""
        return len(self.diff_types) == 0

    @property
    def has_hint_safety_violation(self) -> bool:
        return "hint_shape_violation" in self.diff_types


async def run_probe(
    probe: Probe,
    detector: _DetectorProtocol,
    context: Optional[dict] = None,
) -> ProbeRunResult:
    """Run one probe end-to-end against the detector.

    Steps:
    1. Call detector.detect(probe.input, context=context), measuring latency.
    2. Compare actual output against probe expectations -> diff types.
    3. If actual violation_detected: apply redirect_hint shape assertions.
    4. Return typed result with all observations populated.
    """
    start = time.perf_counter()
    actual = await detector.detect(probe.input, context=context)
    latency_ms = (time.perf_counter() - start) * 1000.0

    diff_types: List[DiffType] = []

    # Violation match check
    if probe.expected_violation and not actual.violation_detected:
        diff_types.append("unexpected_pass")
    elif (not probe.expected_violation) and actual.violation_detected:
        diff_types.append("unexpected_violation")

    # Category match (only meaningful when both sides agree on violation
    # status — otherwise the unexpected_violation/unexpected_pass diff
    # already captures the divergence).
    if (
        probe.expected_violation
        and actual.violation_detected
        and probe.expected_category != actual.category
    ):
        diff_types.append("category_mismatch")

    # Confidence band check — applies whether violation matched or not,
    # since confidence shape matters in both directions.
    low, high = probe.expected_confidence_range
    if not (low <= actual.confidence <= high):
        diff_types.append("confidence_band_miss")

    # Redirect-hint shape assertions — only meaningful when actual fired
    # a violation (otherwise no hint was authored to check).
    hint_failures: List[AssertionFailure] = []
    if actual.violation_detected and actual.redirect_hint:
        hint_failures = assert_redirect_hint_shape_safe(
            actual.redirect_hint,
            probe.input,
        )
        if hint_failures:
            diff_types.append("hint_shape_violation")

    return ProbeRunResult(
        probe_id=probe.probe_id,
        probe_input=probe.input,
        expected_violation=probe.expected_violation,
        expected_category=probe.expected_category,
        expected_confidence_range=probe.expected_confidence_range,
        actual_output=actual,
        latency_ms=latency_ms,
        hint_assertion_failures=hint_failures,
        diff_types=diff_types,
    )


async def run_probe_set(
    probes: List[Probe],
    detector: _DetectorProtocol,
    context: Optional[dict] = None,
) -> List[ProbeRunResult]:
    """Run a list of probes sequentially. Returns results in input order."""
    results: List[ProbeRunResult] = []
    for probe in probes:
        result = await run_probe(probe, detector, context=context)
        results.append(result)
    return results


def summarize_results(results: List[ProbeRunResult]) -> dict:
    """Compute aggregate stats over a probe-run batch."""
    total = len(results)
    if total == 0:
        return {"total": 0, "passed": 0, "failed": 0, "diff_type_counts": {}}

    passed = sum(1 for r in results if r.passed)
    diff_counts: dict = {}
    for result in results:
        for diff in result.diff_types:
            diff_counts[diff] = diff_counts.get(diff, 0) + 1

    latencies = [r.latency_ms for r in results]
    return {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "diff_type_counts": diff_counts,
        "latency_ms_min": min(latencies),
        "latency_ms_max": max(latencies),
        "latency_ms_avg": sum(latencies) / total,
    }


def format_divergence_table(results: List[ProbeRunResult]) -> str:
    """Render results as the markdown divergence table CXO scans during
    calibration rounds. Probes with no diff types are omitted; only
    divergences are surfaced.
    """
    rows = [
        "| probe_id | expected (cat / conf-range) | actual (cat / conf) | diff_types | hint_assertion_failures |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        if r.passed:
            continue
        expected = (
            f"{r.expected_category} / "
            f"[{r.expected_confidence_range[0]:.2f}, "
            f"{r.expected_confidence_range[1]:.2f}]"
        )
        actual_cat = r.actual_output.category
        actual_conf = f"{r.actual_output.confidence:.2f}"
        diffs = ", ".join(r.diff_types)
        hint_fails = (
            "; ".join(
                f"{f.rule}={f.matched_text!r}"
                for f in r.hint_assertion_failures
            )
            if r.hint_assertion_failures
            else ""
        )
        rows.append(
            f"| {r.probe_id} | {expected} | {actual_cat} / {actual_conf} | "
            f"{diffs} | {hint_fails} |"
        )
    return "\n".join(rows)
