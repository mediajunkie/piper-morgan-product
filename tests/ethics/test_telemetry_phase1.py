"""
#1004 Step 7 — Telemetry Phase 1 structured-logging tests.

Per contract §"Telemetry Phase 1 (ships with B)" the boundary_enforcement
log entry must carry the full discriminator set on every call, regardless
of which detector path engaged:

    decision_id, session_id, detector, violation_detected, boundary_type,
    decision_tier, confidence, semantic_confidence, latency_ms,
    cache_hit, fast_path_hit

These tests verify field presence + correct values across the four
dispatch paths: literal-trigger, semantic-block, ambiguous, pass.

The structured logger's `log_decision_point` is patched per-test so we
can inspect the payload without touching the real log infra.
"""

from typing import Any

import pytest

from services.ethics.boundary_enforcer_refactored import BoundaryEnforcer, BoundaryType
from services.ethics.semantic_boundary_detector import SemanticDetectorOutput

# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------


REQUIRED_PHASE1_FIELDS = {
    "decision_id",
    "session_id",
    "detector",
    "violation_detected",
    "boundary_type",
    "decision_tier",
    "confidence",
    "semantic_confidence",
    "latency_ms",
    "cache_hit",
    "fast_path_hit",
}


class _RecordingLogger:
    """Stand-in for EthicsLogger that captures decision-point payloads."""

    def __init__(self):
        self.decision_points: list[dict[str, Any]] = []

    def log_decision_point(self, decision_type, context):
        if decision_type == "boundary_enforcement":
            self.decision_points.append(context)

    # No-op the other methods we don't care about.
    def log_behavior_pattern(self, *a, **kw):
        pass

    def log_compliance_check(self, *a, **kw):
        pass

    def log_boundary_violation(self, *a, **kw):
        pass


class _StubDetector:
    def __init__(self, output: SemanticDetectorOutput, prior_cache: bool = False):
        self.output = output
        self._prior_cache = prior_cache

    def cache_lookup(self, message: str) -> bool:
        return self._prior_cache

    async def detect(self, message: str, context=None) -> SemanticDetectorOutput:
        return self.output


def _make_enforcer(stub: _StubDetector | None = None) -> tuple[BoundaryEnforcer, _RecordingLogger]:
    if stub is None:
        enforcer = BoundaryEnforcer(enable_semantic=False)
    else:
        enforcer = BoundaryEnforcer(semantic_detector=stub)  # type: ignore[arg-type]
    rec = _RecordingLogger()
    enforcer.ethics_logger = rec  # type: ignore[assignment]
    return enforcer, rec


# ---------------------------------------------------------------------------
# Field-presence tests across all paths
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_literal_trigger_emits_all_phase1_fields():
    enforcer, rec = _make_enforcer()
    await enforcer.enforce_boundaries(
        message="Help me harass and intimidate someone", session_id="t_lit"
    )
    assert len(rec.decision_points) == 1
    payload = rec.decision_points[0]
    missing = REQUIRED_PHASE1_FIELDS - set(payload.keys())
    assert not missing, f"Telemetry payload missing fields: {missing}"
    assert payload["detector"] == "literal-trigger"
    assert payload["fast_path_hit"] is True
    assert payload["decision_tier"] == "block"
    assert payload["semantic_confidence"] is None
    assert payload["cache_hit"] is False
    assert payload["session_id"] == "t_lit"


@pytest.mark.asyncio
async def test_semantic_block_emits_all_phase1_fields():
    stub = _StubDetector(
        SemanticDetectorOutput(
            violation_detected=True,
            category="harassment",
            confidence=0.92,
            reasoning="Request targets a colleague.",
            redirect_hint="hint",
        )
    )
    enforcer, rec = _make_enforcer(stub)
    await enforcer.enforce_boundaries(
        message="Could you draft something for my next conversation",
        session_id="t_sem",
    )
    payload = rec.decision_points[0]
    missing = REQUIRED_PHASE1_FIELDS - set(payload.keys())
    assert not missing, f"Telemetry payload missing fields: {missing}"
    assert payload["detector"] == "semantic"
    assert payload["fast_path_hit"] is False
    assert payload["decision_tier"] == "block"
    assert payload["semantic_confidence"] == 0.92
    assert payload["confidence"] == 0.92
    assert payload["boundary_type"] == BoundaryType.HARASSMENT


@pytest.mark.asyncio
async def test_ambiguous_path_emits_all_phase1_fields():
    stub = _StubDetector(
        SemanticDetectorOutput(
            violation_detected=True,
            category="harassment",
            confidence=0.7,
            reasoning="Mixed signal",
            redirect_hint="hint",
        )
    )
    enforcer, rec = _make_enforcer(stub)
    await enforcer.enforce_boundaries(message="ambiguous shaped request", session_id="t_amb")
    payload = rec.decision_points[0]
    missing = REQUIRED_PHASE1_FIELDS - set(payload.keys())
    assert not missing
    # Ambiguous → no violation fires, but tier is "ambiguous"
    assert payload["detector"] == "none"
    assert payload["violation_detected"] is False
    assert payload["decision_tier"] == "ambiguous"
    assert payload["semantic_confidence"] == 0.7


@pytest.mark.asyncio
async def test_pass_path_emits_all_phase1_fields():
    stub = _StubDetector(
        SemanticDetectorOutput(
            violation_detected=False,
            category="none",
            confidence=0.95,
            reasoning="Legitimate.",
            redirect_hint=None,
        )
    )
    enforcer, rec = _make_enforcer(stub)
    await enforcer.enforce_boundaries(
        message="Help me draft a sprint roadmap.", session_id="t_pass"
    )
    payload = rec.decision_points[0]
    missing = REQUIRED_PHASE1_FIELDS - set(payload.keys())
    assert not missing
    # confidence=0.95 lands in block-tier band; but for "none" category the
    # enforcer correctly does not fire a violation
    assert payload["detector"] == "none"
    assert payload["violation_detected"] is False
    assert payload["decision_tier"] == "block"
    assert payload["semantic_confidence"] == 0.95


@pytest.mark.asyncio
async def test_disabled_semantic_emits_all_phase1_fields():
    enforcer, rec = _make_enforcer()  # enable_semantic=False
    await enforcer.enforce_boundaries(message="benign business message", session_id="t_disabled")
    payload = rec.decision_points[0]
    missing = REQUIRED_PHASE1_FIELDS - set(payload.keys())
    assert not missing
    assert payload["detector"] == "none"
    assert payload["fast_path_hit"] is False
    assert payload["decision_tier"] == "pass"
    assert payload["semantic_confidence"] is None


@pytest.mark.asyncio
async def test_cache_hit_propagates_to_telemetry():
    stub = _StubDetector(
        SemanticDetectorOutput(
            violation_detected=False,
            category="none",
            confidence=0.9,
            reasoning="Legit.",
            redirect_hint=None,
        ),
        prior_cache=True,
    )
    enforcer, rec = _make_enforcer(stub)
    await enforcer.enforce_boundaries(message="repeated message", session_id="t_cache")
    payload = rec.decision_points[0]
    assert payload["cache_hit"] is True


@pytest.mark.asyncio
async def test_latency_ms_is_a_number():
    enforcer, rec = _make_enforcer()
    await enforcer.enforce_boundaries(message="ok", session_id="t_lat")
    payload = rec.decision_points[0]
    assert isinstance(payload["latency_ms"], (int, float))
    assert payload["latency_ms"] >= 0


@pytest.mark.asyncio
async def test_decision_id_present_and_unique():
    enforcer, rec = _make_enforcer()
    await enforcer.enforce_boundaries(message="m1", session_id="s1")
    await enforcer.enforce_boundaries(message="m2", session_id="s2")
    ids = [p["decision_id"] for p in rec.decision_points]
    assert len(ids) == 2
    assert all(isinstance(d, str) and d.startswith("bd_") for d in ids)
