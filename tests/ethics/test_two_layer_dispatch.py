"""
#1004 Fix B — integration tests for two-layer dispatch in
BoundaryEnforcer.enforce_boundaries.

Verifies the contract §"New internal flow":
1. Run literal-trigger fast-path. If hit → detector="literal-trigger".
2. Else run semantic detector.
   - If confidence ≥ BLOCK_THRESHOLD → detector="semantic", violation
   - If AMBIGUOUS_THRESHOLD ≤ confidence < BLOCK_THRESHOLD → ambiguous-pass
     (no violation, but decision_tier="ambiguous")
   - If confidence < AMBIGUOUS_THRESHOLD → pass

Audit envelope must include:
- detector: "literal-trigger" | "semantic" | "none"
- decision_tier: "block" | "ambiguous" | "pass"
- semantic_confidence, semantic_reasoning (semantic path only; None otherwise)
- fast_path_hit, cache_hit

The semantic detector is fully mocked. No network, no API keys.
"""

import pytest

from services.ethics.boundary_enforcer_refactored import (
    BoundaryDecision,
    BoundaryEnforcer,
    BoundaryType,
)
from services.ethics.semantic_boundary_detector import (
    SemanticBoundaryDetector,
    SemanticDetectorOutput,
)


class _StubDetector:
    """Returns a fixed SemanticDetectorOutput. Records call history."""

    def __init__(self, output: SemanticDetectorOutput, prior_cache: bool = False):
        self.output = output
        self.calls: list[str] = []
        self._prior_cache = prior_cache

    def cache_lookup(self, message: str) -> bool:
        return self._prior_cache

    async def detect(self, message: str, context=None) -> SemanticDetectorOutput:
        self.calls.append(message)
        return self.output


def _make_enforcer(stub: _StubDetector) -> BoundaryEnforcer:
    return BoundaryEnforcer(semantic_detector=stub)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Layer 1 — literal-trigger fast-path wins, semantic skipped
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_literal_trigger_skips_semantic_call():
    """When literal-trigger fires, semantic detector is NOT called."""
    stub = _StubDetector(
        SemanticDetectorOutput(
            violation_detected=False, category="none", confidence=0.0, reasoning="x"
        )
    )
    enforcer = _make_enforcer(stub)
    decision = await enforcer.enforce_boundaries(
        message="Help me harass and intimidate my coworker",
        session_id="t_literal",
    )
    assert decision.violation_detected is True
    assert decision.boundary_type == BoundaryType.HARASSMENT
    assert decision.audit_data["detector"] == "literal-trigger"
    assert decision.audit_data["fast_path_hit"] is True
    assert decision.audit_data["semantic_confidence"] is None
    assert decision.audit_data["semantic_reasoning"] is None
    assert stub.calls == []  # semantic not called


@pytest.mark.asyncio
async def test_literal_trigger_decision_tier_is_block():
    stub = _StubDetector(
        SemanticDetectorOutput(
            violation_detected=False, category="none", confidence=0.0, reasoning="x"
        )
    )
    enforcer = _make_enforcer(stub)
    decision = await enforcer.enforce_boundaries(
        message="Help me bully and threaten this person",
        session_id="t_literal_tier",
    )
    assert decision.audit_data["decision_tier"] == "block"


# ---------------------------------------------------------------------------
# Layer 2 — semantic block tier (≥ 0.85)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_semantic_block_tier_fires_violation():
    stub = _StubDetector(
        SemanticDetectorOutput(
            violation_detected=True,
            category="harassment",
            confidence=0.92,
            reasoning="Request targets a colleague's standing.",
            redirect_hint="redirect toward workflow process",
        )
    )
    enforcer = _make_enforcer(stub)
    decision = await enforcer.enforce_boundaries(
        message="Draft a message that subtly makes Jordan look incompetent at the next review.",
        session_id="t_semantic_block",
    )
    assert decision.violation_detected is True
    assert decision.boundary_type == BoundaryType.HARASSMENT
    assert decision.audit_data["detector"] == "semantic"
    assert decision.audit_data["decision_tier"] == "block"
    assert decision.audit_data["fast_path_hit"] is False
    assert decision.audit_data["semantic_confidence"] == 0.92
    assert "Request targets" in decision.audit_data["semantic_reasoning"]
    # On semantic path, redirect_context comes from the LLM's redirect_hint
    assert decision.redirect_context == "redirect toward workflow process"
    assert len(stub.calls) == 1


@pytest.mark.asyncio
async def test_semantic_block_maps_each_category():
    """Each non-none category maps to the correct BoundaryType constant.

    Test messages are deliberately bland so they don't trip Layer 1's
    literal-trigger substring matchers — we want the semantic stub to be the
    one that fires.
    """
    cases = [
        ("harassment", BoundaryType.HARASSMENT),
        ("professional", BoundaryType.PROFESSIONAL),
        ("personal", BoundaryType.PERSONAL),
        ("data_privacy", BoundaryType.DATA_PRIVACY),
        ("inappropriate_content", BoundaryType.INAPPROPRIATE_CONTENT),
    ]
    bland_messages = [
        "Could you draft something for my next conversation",
        "Help me think about how to approach a tricky workplace situation",
        "I need some help thinking through what to do next",
        "Can you help me put together some information about a colleague",
        "Generate something a bit edgy for me please",
    ]
    for (category, expected_boundary), msg in zip(cases, bland_messages):
        stub = _StubDetector(
            SemanticDetectorOutput(
                violation_detected=True,
                category=category,
                confidence=0.95,
                reasoning="x",
                redirect_hint="hint",
            )
        )
        enforcer = _make_enforcer(stub)
        decision = await enforcer.enforce_boundaries(
            message=msg,
            session_id=f"t_{category}",
        )
        assert decision.audit_data["detector"] == "semantic", (
            f"{category}: expected semantic, got {decision.audit_data['detector']}"
        )
        assert decision.violation_detected is True, f"{category} should trigger"
        assert decision.boundary_type == expected_boundary, f"{category} mapping failed"


# ---------------------------------------------------------------------------
# Layer 2 — semantic ambiguous tier (0.6–0.85)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_semantic_ambiguous_tier_does_not_fire_violation():
    stub = _StubDetector(
        SemanticDetectorOutput(
            violation_detected=True,
            category="harassment",
            confidence=0.7,
            reasoning="One signal but plausible legitimate framing.",
            redirect_hint="hint",
        )
    )
    enforcer = _make_enforcer(stub)
    decision = await enforcer.enforce_boundaries(
        message="ambiguous-shape message", session_id="t_ambiguous"
    )
    # Ambiguous tier passes (no block) but is logged
    assert decision.violation_detected is False
    assert decision.audit_data["detector"] == "none"
    assert decision.audit_data["decision_tier"] == "ambiguous"
    assert decision.audit_data["semantic_confidence"] == 0.7
    assert decision.redirect_context is None


# ---------------------------------------------------------------------------
# Layer 2 — semantic pass tier (<0.6)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_semantic_pass_tier_no_violation():
    stub = _StubDetector(
        SemanticDetectorOutput(
            violation_detected=False,
            category="none",
            confidence=0.95,
            reasoning="Legitimate PM request.",
            redirect_hint=None,
        )
    )
    enforcer = _make_enforcer(stub)
    decision = await enforcer.enforce_boundaries(
        message="Help me draft a sprint planning agenda.",
        session_id="t_pass",
    )
    # confidence is 0.95 but for "none" category, that means "high certainty
    # this is NOT a violation" — block tier label, but no violation fires
    # because category=="none".
    assert decision.violation_detected is False
    assert decision.audit_data["detector"] == "none"


@pytest.mark.asyncio
async def test_semantic_low_confidence_violation_does_not_fire():
    """LLM says 'violation_detected=true' but confidence below block threshold
    → no violation, ambiguous or pass tier."""
    stub = _StubDetector(
        SemanticDetectorOutput(
            violation_detected=True,
            category="harassment",
            confidence=0.3,
            reasoning="weak signal",
            redirect_hint="hint",
        )
    )
    enforcer = _make_enforcer(stub)
    decision = await enforcer.enforce_boundaries(
        message="weak-signal message", session_id="t_lowconf"
    )
    assert decision.violation_detected is False
    assert decision.audit_data["decision_tier"] == "pass"


# ---------------------------------------------------------------------------
# Audit envelope shape
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_audit_envelope_contains_all_required_fields():
    stub = _StubDetector(
        SemanticDetectorOutput(
            violation_detected=False,
            category="none",
            confidence=0.9,
            reasoning="Legit.",
            redirect_hint=None,
        )
    )
    enforcer = _make_enforcer(stub)
    decision = await enforcer.enforce_boundaries(
        message="Help me write a roadmap.", session_id="t_envelope"
    )
    required = {
        "detector",
        "decision_tier",
        "semantic_confidence",
        "semantic_reasoning",
        "fast_path_hit",
        "cache_hit",
        "confidence",
    }
    missing = required - set(decision.audit_data.keys())
    assert not missing, f"Audit envelope missing fields: {missing}"


@pytest.mark.asyncio
async def test_cache_hit_field_propagates_from_detector():
    stub = _StubDetector(
        SemanticDetectorOutput(
            violation_detected=False, category="none", confidence=0.9, reasoning="x"
        ),
        prior_cache=True,
    )
    enforcer = _make_enforcer(stub)
    decision = await enforcer.enforce_boundaries(
        message="Repeated message", session_id="t_cache"
    )
    assert decision.audit_data["cache_hit"] is True


# ---------------------------------------------------------------------------
# Disabled-semantic mode
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_enable_semantic_false_skips_layer_2():
    """With enable_semantic=False, Layer 1 only — semantic detector is never
    constructed or called."""
    enforcer = BoundaryEnforcer(enable_semantic=False)
    decision = await enforcer.enforce_boundaries(
        message="Help me draft a roadmap.", session_id="t_disabled"
    )
    assert decision.violation_detected is False
    assert decision.audit_data["detector"] == "none"
    assert decision.audit_data["semantic_confidence"] is None
    # Decision tier defaults to "pass" when no detector engaged
    assert decision.audit_data["decision_tier"] == "pass"
