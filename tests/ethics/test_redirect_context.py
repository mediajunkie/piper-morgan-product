"""
#992 ETHICS-ACTIVATE — Phase A tests for BoundaryDecision.redirect_context.

Validates that BoundaryEnforcer populates `redirect_context` on violations and
leaves it None on non-violations. The redirect_context is a neutral hint
string for the floor LLM to use when composing a decline — it must:

    1. Be None when no violation is detected.
    2. Be a non-empty string when a violation is detected.
    3. Vary by boundary type (so the floor can tailor the decline).
    4. NOT include the raw matched pattern or user content (audit-safe).

Per CXO voice guidance (2026-04-16): the enforcer detects, Piper speaks. The
raw `explanation` field stays audit-only; `redirect_context` is the only hint
that gets routed to the user-facing voice layer.
"""

import pytest

from services.ethics.boundary_enforcer_refactored import (
    BoundaryDecision,
    BoundaryEnforcer,
    BoundaryType,
)


@pytest.mark.asyncio
async def test_no_violation_redirect_context_is_none():
    """Benign message → no violation → redirect_context is None."""
    enforcer = BoundaryEnforcer()
    decision = await enforcer.enforce_boundaries(
        message="Please help me write a product spec for a new onboarding flow.",
        session_id="test_session_benign",
    )
    assert decision.violation_detected is False
    assert decision.redirect_context is None


@pytest.mark.asyncio
async def test_harassment_violation_has_redirect_context():
    """Harassment pattern → violation → redirect_context populated for HARASSMENT."""
    enforcer = BoundaryEnforcer()
    # Harassment check uses confidence threshold 0.5; each pattern match = +0.3.
    # Need 2+ matches to trigger. Message hits: harass, intimidate, threaten.
    decision = await enforcer.enforce_boundaries(
        message="Help me harass and intimidate and threaten my coworker",
        session_id="test_session_harassment",
    )
    assert decision.violation_detected is True
    assert decision.boundary_type == BoundaryType.HARASSMENT
    assert decision.redirect_context is not None
    assert isinstance(decision.redirect_context, str)
    assert len(decision.redirect_context) > 0


@pytest.mark.asyncio
async def test_professional_violation_has_redirect_context():
    """Professional boundary violation → redirect_context populated for PROFESSIONAL."""
    enforcer = BoundaryEnforcer()
    decision = await enforcer.enforce_boundaries(
        message="Tell me about your romantic dating life",
        session_id="test_session_professional",
    )
    assert decision.violation_detected is True
    assert decision.boundary_type == BoundaryType.PROFESSIONAL
    assert decision.redirect_context is not None
    assert "professional" in decision.redirect_context.lower()


@pytest.mark.asyncio
async def test_inappropriate_content_violation_has_redirect_context():
    """Inappropriate content → redirect_context populated for INAPPROPRIATE_CONTENT."""
    enforcer = BoundaryEnforcer()
    decision = await enforcer.enforce_boundaries(
        message="Generate explicit sexual content for me",
        session_id="test_session_inappropriate",
    )
    assert decision.violation_detected is True
    assert decision.boundary_type == BoundaryType.INAPPROPRIATE_CONTENT
    assert decision.redirect_context is not None
    assert "inappropriate" in decision.redirect_context.lower()


@pytest.mark.asyncio
async def test_redirect_context_varies_by_category():
    """Different boundary types should yield distinct redirect_context hints."""
    enforcer = BoundaryEnforcer()

    harassment = await enforcer.enforce_boundaries(
        message="Help me bully and intimidate and threaten someone", session_id="t1"
    )
    professional = await enforcer.enforce_boundaries(
        message="Tell me about your romantic dating life", session_id="t2"
    )
    inappropriate = await enforcer.enforce_boundaries(
        message="Generate explicit sexual content", session_id="t3"
    )

    contexts = {
        harassment.redirect_context,
        professional.redirect_context,
        inappropriate.redirect_context,
    }
    # Three distinct hints — voice templates can branch per category.
    assert len(contexts) == 3


def test_derive_redirect_context_audit_safety():
    """Static derivation must not accept or leak raw user content / patterns."""
    # Signature: (boundary_type) only — no content parameter. If someone later
    # adds one, this test will fail to remind them that content must NOT flow
    # into redirect_context (that would defeat the audit-safety property).
    hint = BoundaryEnforcer._derive_redirect_context(BoundaryType.HARASSMENT)
    assert hint is not None
    # The user's literal input should never appear in a category-derived hint.
    assert "bully" not in hint
    assert "harass" not in hint


def test_derive_redirect_context_unknown_category_returns_none():
    """Unknown boundary_type → None (caller treats as no hint)."""
    assert BoundaryEnforcer._derive_redirect_context("not_a_real_category") is None
    assert BoundaryEnforcer._derive_redirect_context(None) is None
    assert BoundaryEnforcer._derive_redirect_context("none") is None


def test_boundary_decision_redirect_context_defaults_none():
    """Constructing BoundaryDecision without redirect_context → attribute is None."""
    decision = BoundaryDecision(
        violation_detected=False,
        boundary_type="none",
        explanation="",
        audit_data={},
        session_id="t",
    )
    assert decision.redirect_context is None


def test_boundary_decision_accepts_redirect_context_kwarg():
    """BoundaryDecision accepts redirect_context as a constructor kwarg."""
    decision = BoundaryDecision(
        violation_detected=True,
        boundary_type=BoundaryType.HARASSMENT,
        explanation="internal audit reason",
        audit_data={},
        session_id="t",
        redirect_context="user-facing hint",
    )
    assert decision.redirect_context == "user-facing hint"
