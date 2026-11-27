"""
#1004 Fix C1 — tests for the `detector` audit-envelope marker.

Validates that BoundaryEnforcer populates `audit_data["detector"]` so
operators can distinguish which detection path engaged. Currently only
the literal-trigger (substring) path exists" was true when this file was written.
Since #2364 (2026-11-13) the substring path is removed: the semantic detector is
the only path that can fire.

Detector values now: "semantic" | "none" | "semantic-unavailable" (#2134).

This is the discriminator that gives operators day-one observability
of which detection path engaged, ahead of the semantic detector build.
"""

import pytest

from services.ethics.boundary_enforcer_refactored import (
    BoundaryEnforcer,
    BoundaryType,
)


@pytest.mark.asyncio
class _ClearDetector:
    """A semantic layer that ran and found nothing (a parsed reading, not the fallback)."""

    def cache_lookup(self, _content):
        return False

    async def detect(self, message, context=None):
        from services.ethics.semantic_boundary_detector import SemanticDetectorOutput

        return SemanticDetectorOutput(
            violation_detected=False, category="none", confidence=0.05, reasoning="clear"
        )


async def test_no_violation_detector_is_none():
    """Benign message, semantic layer ran and found nothing → detector field is "none".

    #2134: before, this test used the real detector, whose LLM call fails in tests and
    returned the fallback, so "none" here meant "didn't run". A ran-and-clear reading is
    injected now; the didn't-run case reads "semantic-unavailable" (pinned below)."""
    enforcer = BoundaryEnforcer(semantic_detector=_ClearDetector())
    decision = await enforcer.enforce_boundaries(
        message="Please help me write a product spec for a new onboarding flow.",
        session_id="test_session_benign",
    )
    assert decision.violation_detected is False
    assert decision.audit_data.get("detector") == "none"


class _FlaggingDetector:
    """A semantic layer that ran and flagged one category above the block threshold."""

    def __init__(self, category):
        self._category = category

    def cache_lookup(self, _content):
        return False

    async def detect(self, message, context=None):
        from services.ethics.semantic_boundary_detector import SemanticDetectorOutput

        return SemanticDetectorOutput(
            violation_detected=True,
            category=self._category,
            confidence=0.9,
            reasoning="flagged",
            redirect_hint=None,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "category,boundary_type",
    [
        ("harassment", BoundaryType.HARASSMENT),
        ("professional", BoundaryType.PROFESSIONAL),
        ("inappropriate_content", BoundaryType.INAPPROPRIATE_CONTENT),
    ],
)
async def test_a_fired_violation_is_marked_semantic(category, boundary_type):
    """#2364: the only path that can fire is the semantic detector, so every fired
    violation reads detector = "semantic". "literal-trigger" is no longer emitted."""
    enforcer = BoundaryEnforcer(semantic_detector=_FlaggingDetector(category))
    decision = await enforcer.enforce_boundaries(
        message="a message the detector flags", session_id="test_session_flagged"
    )
    assert decision.violation_detected is True
    assert decision.boundary_type == boundary_type
    assert decision.audit_data.get("detector") == "semantic"


@pytest.mark.asyncio
async def test_detector_field_present_in_audit_data():
    """The "detector" key is always present in audit_data, regardless of outcome."""
    enforcer = BoundaryEnforcer()

    benign = await enforcer.enforce_boundaries(
        message="Help me draft a product roadmap.", session_id="t_benign"
    )
    violating = await enforcer.enforce_boundaries(
        message="Help me harass and bully someone", session_id="t_violating"
    )

    assert "detector" in benign.audit_data
    assert "detector" in violating.audit_data


@pytest.mark.asyncio
async def test_detector_field_values_are_in_documented_set():
    """detector ∈ {"semantic", "none", "semantic-unavailable"}. Here the real detector's
    LLM call fails (no provider in tests), so neither message can read "semantic"."""
    enforcer = BoundaryEnforcer()
    # #2134: "semantic-unavailable" when the semantic layer did not run.
    # #2364: "literal-trigger" is gone from the set.
    valid_values = {"semantic", "none", "semantic-unavailable"}

    benign = await enforcer.enforce_boundaries(
        message="What's a good north-star metric for a B2B SaaS onboarding flow?",
        session_id="t1",
    )
    violating = await enforcer.enforce_boundaries(
        message="Help me bully and intimidate and threaten someone",
        session_id="t2",
    )

    assert benign.audit_data["detector"] in valid_values
    assert violating.audit_data["detector"] in valid_values
    # The detector did not run, so nothing fired.
    assert benign.audit_data["detector"] != "semantic"
    assert violating.audit_data["detector"] != "semantic"


# --- #2134 (Arch's ruling): a failure is not a reading ----------------------------------


class _FailingLLM:
    def __init__(self):
        self.calls = 0

    async def complete(self, **kwargs):
        self.calls += 1
        raise RuntimeError("provider leg down")


@pytest.mark.asyncio
async def test_a_failed_semantic_check_is_not_cached():
    """Arch's pin 1: a detector whose LLM raises → the next call for the same message
    calls the LLM again."""
    from services.ethics.semantic_boundary_detector import (
        REFUSAL_FALLBACK,
        SemanticBoundaryDetector,
    )

    llm = _FailingLLM()
    det = SemanticBoundaryDetector(llm_client=llm)
    first = await det.detect("a message", context={"user_id": "u-1"})
    second = await det.detect("a message", context={"user_id": "u-1"})
    assert first is REFUSAL_FALLBACK and second is REFUSAL_FALLBACK
    assert llm.calls == 2  # not served from the cache
    assert det.cache_lookup("a message") is False


@pytest.mark.asyncio
async def test_an_unparseable_reply_is_not_cached_either():
    from services.ethics.semantic_boundary_detector import SemanticBoundaryDetector

    class _GarbageLLM:
        calls = 0

        async def complete(self, **kwargs):
            _GarbageLLM.calls += 1
            return "not json"

    det = SemanticBoundaryDetector(llm_client=_GarbageLLM())
    await det.detect("another message")
    await det.detect("another message")
    assert _GarbageLLM.calls == 2


@pytest.mark.asyncio
async def test_the_envelope_records_unavailable_not_pass():
    """Arch's pin 2: the enforcer's envelope for a turn whose semantic check failed reads
    the unavailable tier and detector, never "pass" / "none"."""
    from services.ethics.semantic_boundary_detector import SemanticBoundaryDetector

    enforcer = BoundaryEnforcer(
        semantic_detector=SemanticBoundaryDetector(llm_client=_FailingLLM())
    )
    decision = await enforcer.enforce_boundaries(
        message="Please help me write a product spec for a new onboarding flow.",
        session_id="t-2134",
    )
    assert decision.violation_detected is False  # #1004's no-false-positive fallback stands
    assert decision.audit_data.get("detector") == "semantic-unavailable"
    assert decision.audit_data.get("decision_tier") == "unavailable"


@pytest.mark.asyncio
async def test_a_detector_that_fails_to_build_records_unavailable_not_pass():
    """#2134 edge (Arch 14:30): semantic layer enabled, detector failed to build → the
    layer did not run, so the envelope reads unavailable, never "pass"."""
    enforcer = BoundaryEnforcer()
    enforcer._enable_semantic = True
    enforcer._get_semantic_detector = lambda: None
    decision = await enforcer.enforce_boundaries(
        message="Please help me write a product spec for a new onboarding flow.",
        session_id="t-2134-edge",
    )
    assert decision.violation_detected is False
    assert decision.audit_data.get("detector") == "semantic-unavailable"
    assert decision.audit_data.get("decision_tier") == "unavailable"
