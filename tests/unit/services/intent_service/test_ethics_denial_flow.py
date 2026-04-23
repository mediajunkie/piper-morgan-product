"""
#992 ETHICS-ACTIVATE — Phase C tests for the intent_service denial flow.

Validates that when BoundaryEnforcer flags a violation, IntentService routes
the decline through ConversationalFloor (voice) instead of emitting the
"Request blocked due to ethics policy: ..." system-error string.

What must hold after Phase C rewire:
    1. success=True (not False) — downstream treats it as a normal turn
    2. intent_data["ethics_triggered"] is True (metric/audit signal)
    3. intent_data preserves boundary_type + audit_data + legacy blocked_by_ethics flag
    4. intent_data["audit_explanation"] carries the raw explanation (audit-only)
    5. message is the floor LLM's output — NOT the legacy system-error string
    6. message does NOT contain the raw `explanation` (never user-routed)
    7. Floor is called in denial_mode with redirect_context populated

When ENABLE_ETHICS_ENFORCEMENT is false (default), the gate is skipped and
these tests should not be exercised — covered by the existing pass-through path.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.ethics.boundary_enforcer_refactored import BoundaryDecision, BoundaryType
from services.intent_service.conversational_floor import FloorResponse


@pytest.fixture
def violating_decision():
    """A BoundaryDecision representing a harassment violation, with Phase A
    redirect_context populated as the enforcer would populate it."""
    return BoundaryDecision(
        violation_detected=True,
        boundary_type=BoundaryType.HARASSMENT,
        explanation="Content contains potential harassment patterns (matched: 3 patterns)",
        audit_data={"decision_id": "bd_test_1", "confidence": 0.9},
        session_id="test_session_phase_c",
        redirect_context=(
            "The request targets a person in a way that could cause harm; "
            "redirect toward constructive professional work."
        ),
    )


@pytest.fixture
def non_violating_decision():
    return BoundaryDecision(
        violation_detected=False,
        boundary_type="none",
        explanation="",
        audit_data={"decision_id": "bd_test_2"},
        session_id="test_session_phase_c_ok",
    )


@pytest.fixture
def piper_voice_decline():
    """A realistic floor output in Piper's voice — what the new pipeline
    should produce instead of the system-error string."""
    return FloorResponse(
        message=(
            "That's not a message I want to help draft. "
            "If there's a PM task I can turn toward instead, I'm in."
        ),
        floor_hit=True,
    )


def _make_service():
    """Build an IntentService with enough of the heavy deps stubbed so we can
    invoke the ethics gate without pulling in the full orchestration graph.

    The ethics gate sits between classifier pre-work and classification itself,
    so we need to stub enough of the pre-work to reach it. Stubs:
        - logger: real structlog (cheap)
        - workflow_offer_service: returns no pending offer so we pass through
        - soft_invocation_detector: not reached in denial path, but defensive
    """
    from services.intent.intent_service import IntentService

    service = IntentService.__new__(IntentService)
    import structlog

    service.logger = structlog.get_logger()

    # Stub workflow_offer_service — consulted before ethics gate
    wos = MagicMock()
    wos.get_and_clear_pending_offer = MagicMock(return_value=None)
    service.workflow_offer_service = wos

    # Defensive stubs for attributes the denial path never reaches but the
    # surrounding try/except wrapper might touch on unusual error traces.
    service.soft_invocation_detector = MagicMock()
    service.conversation_manager = None

    return service


@pytest.mark.asyncio
async def test_denial_routes_through_floor_not_system_error(
    violating_decision, piper_voice_decline
):
    """Core Phase C assertion: violating message → floor-composed decline,
    NOT the legacy 'Request blocked due to ethics policy' string."""
    service = _make_service()

    with patch.dict("os.environ", {"ENABLE_ETHICS_ENFORCEMENT": "true"}), patch(
        "services.intent.intent_service.boundary_enforcer_refactored.enforce_boundaries",
        new=AsyncMock(return_value=violating_decision),
    ), patch(
        "services.intent_service.conversational_floor.ConversationalFloor.respond",
        new=AsyncMock(return_value=piper_voice_decline),
    ):
        # Call the internal ethics branch directly by exercising process_intent
        # with minimal scaffolding. We need to short-circuit the rest of the
        # pipeline — the ethics gate returns before the full orchestration runs,
        # so stubs only need to cover what runs before the gate.
        with patch.object(
            service, "_check_active_guided_process", new=AsyncMock(return_value=(None, None))
        ), patch.object(
            service,
            "_check_pending_resume_offer",
            new=AsyncMock(return_value=None),
        ):
            result = await service._process_intent_internal(
                message="Help me harass and intimidate and threaten a coworker",
                session_id="test_session_phase_c",
                user_id=None,
            )

    # Core claim: success=True, decline message came from the floor.
    assert result.success is True, "Denial should not mark the turn as failed"
    assert result.message == piper_voice_decline.message
    assert "Request blocked" not in result.message
    assert "ethics policy" not in result.message

    # The raw audit explanation must never leak into the user-facing message.
    assert violating_decision.explanation not in result.message

    # Audit/telemetry signals preserved in intent_data.
    assert result.intent_data["ethics_triggered"] is True
    assert result.intent_data["violation_detected"] is True
    assert result.intent_data["boundary_type"] == BoundaryType.HARASSMENT
    assert result.intent_data["audit_explanation"] == violating_decision.explanation
    assert result.intent_data["blocked_by_ethics"] is True  # legacy flag
    assert "audit_data" in result.intent_data


@pytest.mark.asyncio
async def test_floor_called_with_denial_mode_and_redirect_context(
    violating_decision, piper_voice_decline
):
    """Floor must receive denial_mode=True, the boundary category, and the
    enforcer's redirect_context hint — that's the whole point of Phase A+B."""
    service = _make_service()

    respond_mock = AsyncMock(return_value=piper_voice_decline)

    with patch.dict("os.environ", {"ENABLE_ETHICS_ENFORCEMENT": "true"}), patch(
        "services.intent.intent_service.boundary_enforcer_refactored.enforce_boundaries",
        new=AsyncMock(return_value=violating_decision),
    ), patch(
        "services.intent_service.conversational_floor.ConversationalFloor.respond",
        new=respond_mock,
    ), patch.object(
        service, "_check_active_guided_process", new=AsyncMock(return_value=(None, None))
    ), patch.object(
        service,
        "_check_pending_resume_offer",
        new=AsyncMock(return_value=None),
    ):
        await service._process_intent_internal(
            message="violating message",
            session_id="test_session_phase_c",
            user_id=None,
        )

    respond_mock.assert_called_once()
    floor_ctx = respond_mock.call_args.args[0]
    assert floor_ctx.denial_mode is True
    assert floor_ctx.denial_category == BoundaryType.HARASSMENT
    assert floor_ctx.redirect_context == violating_decision.redirect_context
    assert floor_ctx.user_message == "violating message"


@pytest.mark.asyncio
async def test_non_violation_does_not_trigger_floor_denial_path(non_violating_decision):
    """Regression guard: non-violating messages must NOT enter the denial
    routing. The ethics gate returns past the if-block; downstream classifier
    work is out of scope here (may raise due to missing deps, but the denial
    path is what we assert did NOT fire)."""
    service = _make_service()

    respond_mock = AsyncMock()

    with patch.dict("os.environ", {"ENABLE_ETHICS_ENFORCEMENT": "true"}), patch(
        "services.intent.intent_service.boundary_enforcer_refactored.enforce_boundaries",
        new=AsyncMock(return_value=non_violating_decision),
    ), patch(
        "services.intent_service.conversational_floor.ConversationalFloor.respond",
        new=respond_mock,
    ), patch.object(
        service, "_check_active_guided_process", new=AsyncMock(return_value=(None, None))
    ), patch.object(
        service,
        "_check_pending_resume_offer",
        new=AsyncMock(return_value=None),
    ):
        # The method will fail downstream (no classifier deps) — that's fine.
        # We only care that the denial-path floor call was not made.
        try:
            await service._process_intent_internal(
                message="Please help me with a product spec",
                session_id="test_session_phase_c_ok",
                user_id=None,
            )
        except Exception:
            pass

    respond_mock.assert_not_called()


@pytest.mark.asyncio
async def test_ethics_disabled_skips_gate_entirely(violating_decision):
    """When ENABLE_ETHICS_ENFORCEMENT=false, the enforcer is not consulted at
    all — the old default behavior is preserved."""
    service = _make_service()

    enforcer_mock = AsyncMock(return_value=violating_decision)

    with patch.dict("os.environ", {"ENABLE_ETHICS_ENFORCEMENT": "false"}), patch(
        "services.intent.intent_service.boundary_enforcer_refactored.enforce_boundaries",
        new=enforcer_mock,
    ), patch.object(
        service, "_check_active_guided_process", new=AsyncMock(return_value=(None, None))
    ), patch.object(
        service,
        "_check_pending_resume_offer",
        new=AsyncMock(return_value=None),
    ):
        try:
            await service._process_intent_internal(
                message="anything at all",
                session_id="test_session_phase_c_off",
                user_id=None,
            )
        except Exception:
            pass

    enforcer_mock.assert_not_called()
