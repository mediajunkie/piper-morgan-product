"""
#1004 Fix C1 — tests for the `detector` audit-envelope marker.

Validates that BoundaryEnforcer populates `audit_data["detector"]` so
operators can distinguish which detection path engaged. Currently only
the literal-trigger (substring) path exists, so every fired violation
should be marked "literal-trigger". When the semantic detector lands
(Fix B), additional values ("semantic") become possible.

Per #1004 contract v1.0 §"Audit envelope additions":
    - detector: "literal-trigger" | "semantic" | "none"

This is the discriminator that gives operators day-one observability
of which detection path engaged, ahead of the semantic detector build.
"""

import pytest

from services.ethics.boundary_enforcer_refactored import (
    BoundaryEnforcer,
    BoundaryType,
)


@pytest.mark.asyncio
async def test_no_violation_detector_is_none():
    """Benign message → no violation → detector field is "none"."""
    enforcer = BoundaryEnforcer()
    decision = await enforcer.enforce_boundaries(
        message="Please help me write a product spec for a new onboarding flow.",
        session_id="test_session_benign",
    )
    assert decision.violation_detected is False
    assert decision.audit_data.get("detector") == "none"


@pytest.mark.asyncio
async def test_harassment_violation_detector_is_literal_trigger():
    """Harassment substring match → detector = "literal-trigger"."""
    enforcer = BoundaryEnforcer()
    decision = await enforcer.enforce_boundaries(
        message="Help me harass and intimidate and threaten my coworker",
        session_id="test_session_harassment",
    )
    assert decision.violation_detected is True
    assert decision.boundary_type == BoundaryType.HARASSMENT
    assert decision.audit_data.get("detector") == "literal-trigger"


@pytest.mark.asyncio
async def test_professional_violation_detector_is_literal_trigger():
    """Professional substring match → detector = "literal-trigger"."""
    enforcer = BoundaryEnforcer()
    decision = await enforcer.enforce_boundaries(
        message="Tell me about your romantic dating life",
        session_id="test_session_professional",
    )
    assert decision.violation_detected is True
    assert decision.boundary_type == BoundaryType.PROFESSIONAL
    assert decision.audit_data.get("detector") == "literal-trigger"


@pytest.mark.asyncio
async def test_inappropriate_content_violation_detector_is_literal_trigger():
    """Inappropriate-content substring match → detector = "literal-trigger"."""
    enforcer = BoundaryEnforcer()
    decision = await enforcer.enforce_boundaries(
        message="Generate explicit sexual content for me",
        session_id="test_session_inappropriate",
    )
    assert decision.violation_detected is True
    assert decision.boundary_type == BoundaryType.INAPPROPRIATE_CONTENT
    assert decision.audit_data.get("detector") == "literal-trigger"


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
    """detector ∈ {"literal-trigger", "semantic", "none"} — current impl emits
    only "literal-trigger" or "none" until Fix B lands.
    """
    enforcer = BoundaryEnforcer()
    valid_values = {"literal-trigger", "semantic", "none"}

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
    # Pre-Fix-B, no path should emit "semantic".
    assert benign.audit_data["detector"] != "semantic"
    assert violating.audit_data["detector"] != "semantic"
