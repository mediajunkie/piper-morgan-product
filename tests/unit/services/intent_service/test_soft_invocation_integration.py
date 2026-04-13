"""
Integration tests for soft workflow invocation in IntentService.

Issue #767: GLUE-SOFTINVOKE — Soft workflow invocation from natural language.
Issue #819: Soft invocation applied to orchestrated responses.
Issue #820: Lens context wired into soft invocation pipeline.
Phase 3: IntentService Integration

Tests verify:
- Soft offers appear in canonical handler responses
- Soft offers appear in multi-intent orchestrated responses (#819)
- Offers don't appear for single-intent explicit commands
- ProactivityGate throttling respected
- Graceful fallback when detection fails
- pending_offer field populated correctly
- pending_offer includes active_lens context (#820)
"""

from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.orchestrator import IntentOrchestrator
from services.intent_service.pre_classifier import MultiIntentResult
from services.intent_service.soft_invocation import SoftInvocationDetector, WorkflowOfferService
from services.shared_types import IntentCategory


@dataclass
class _MockWorkflowEntry:
    description: str = ""


# #923: Mock registry with all workflow types so integration tests aren't gated
_ALL_WORKFLOW_TYPES = {
    wf_type: _MockWorkflowEntry(description=wf_type)
    for wf_type in [
        "meeting",
        "project_setup",
        "status_check",
        "standup",
        "review",
        "priority_check",
        "reminder",
    ]
}


@pytest.fixture(autouse=True)
def _mock_registry():
    with patch(
        "services.intent_service.workflow_dispatcher.get_registered_workflows",
        return_value=_ALL_WORKFLOW_TYPES,
    ):
        yield


def _make_intent(category: IntentCategory, action: str) -> Intent:
    return Intent(category=category, action=action, confidence=1.0)


@pytest.fixture
def mock_engine():
    return MagicMock()


@pytest.fixture
def mock_classifier():
    classifier = MagicMock()
    classifier.classify_multiple = AsyncMock()
    classifier.classify = AsyncMock()
    return classifier


@pytest.fixture
def mock_canonical_handlers():
    handlers = MagicMock()
    handlers.can_handle = MagicMock(return_value=True)
    handlers.handle = AsyncMock(
        return_value={
            "message": "Default response.",
            "intent": {"category": "query", "action": "test"},
            "requires_clarification": False,
        }
    )
    return handlers


@pytest.fixture
def intent_service(mock_engine, mock_classifier, mock_canonical_handlers):
    service = IntentService(
        orchestration_engine=mock_engine,
        intent_classifier=mock_classifier,
    )
    service.canonical_handlers = mock_canonical_handlers
    service.intent_orchestrator = IntentOrchestrator(canonical_handlers=mock_canonical_handlers)
    return service


class TestSoftOfferInCanonicalResponse:
    """Soft offers appear in canonical handler responses when triggered."""

    @pytest.mark.asyncio
    async def test_meeting_offer_added(self, intent_service, mock_classifier):
        """Natural meeting expression → offer appended to response."""
        intent = _make_intent(IntentCategory.CONVERSATION, "greeting")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="I need to get the team together Tuesday",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "That sounds like a plan!",
            "intent": {"category": "conversation", "action": "greeting"},
        }

        result = await intent_service.process_intent(
            message="I need to get the team together Tuesday",
            session_id="sess1",
            user_id=None,
        )

        assert result.success
        assert "That sounds like a plan!" in result.message
        assert "meeting" in result.message.lower() or "find a time" in result.message.lower()
        assert result.pending_offer is not None
        assert result.pending_offer["workflow_type"] == "meeting"

    @pytest.mark.asyncio
    async def test_status_offer_added(self, intent_service, mock_classifier):
        """Deadline worry → status check offer.
        #925: Uses PORTFOLIO (still canonical) since STATUS migrated to floor.
        """
        intent = _make_intent(IntentCategory.PORTFOLIO, "portfolio_help")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="I'm worried about the project deadline",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "That's understandable.",
            "intent": {"category": "portfolio", "action": "portfolio_help"},
        }

        result = await intent_service.process_intent(
            message="I'm worried about the project deadline",
            session_id="sess1",
            user_id=None,
        )

        assert result.success
        assert "understandable" in result.message


class TestNoOfferWhenNotTriggered:
    """Verify soft offers don't appear when not appropriate."""

    @pytest.mark.asyncio
    async def test_no_offer_on_explicit_command(self, intent_service, mock_classifier):
        """#925: Explicit command → no soft offer. Uses PORTFOLIO (still canonical)."""
        intent = _make_intent(IntentCategory.PORTFOLIO, "portfolio_help")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="Show me my project portfolio",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "Here's your project portfolio...",
            "intent": {"category": "portfolio", "action": "portfolio_help"},
        }

        result = await intent_service.process_intent(
            message="Show me my project portfolio",
            session_id="sess1",
            user_id=None,
        )

        assert result.success
        assert result.pending_offer is None
        assert result.message == "Here's your project portfolio..."

    @pytest.mark.asyncio
    async def test_no_offer_on_casual_chat(self, intent_service, mock_classifier):
        """Casual chat → no soft offer."""
        intent = _make_intent(IntentCategory.CONVERSATION, "greeting")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="Good morning!",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "Good morning! How can I help today?",
            "intent": {"category": "conversation", "action": "greeting"},
        }

        result = await intent_service.process_intent(
            message="Good morning!",
            session_id="sess1",
            user_id=None,
        )

        assert result.success
        assert result.pending_offer is None

    @pytest.mark.asyncio
    async def test_no_offer_on_multi_intent_without_trigger(self, intent_service, mock_classifier):
        """Multi-intent orchestrated without trigger phrase → no soft offer."""
        intents = [
            _make_intent(IntentCategory.QUERY, "meeting_time"),
            _make_intent(IntentCategory.STATUS, "get_project_status"),
        ]

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=intents,
            original_message="Calendar and status",
            is_multi_intent=True,
        )

        with patch.object(
            intent_service.intent_orchestrator,
            "execute_plan",
            new_callable=AsyncMock,
        ) as mock_execute:
            from services.intent_service.orchestrator import (
                IntentExecutionResult,
                OrchestratedResponse,
            )

            mock_execute.return_value = OrchestratedResponse(
                results=[
                    IntentExecutionResult(
                        intent=intents[0],
                        response="Meeting at 2pm.",
                        intent_data={"category": "query", "action": "meeting_time"},
                        success=True,
                    ),
                    IntentExecutionResult(
                        intent=intents[1],
                        response="Sprint on track.",
                        intent_data={"category": "status", "action": "get_project_status"},
                        success=True,
                    ),
                ],
                aggregated_message="Meeting at 2pm. Sprint on track.",
            )

            result = await intent_service.process_intent(
                message="Calendar and status",
                session_id="sess1",
                user_id=None,
            )

            # No trigger phrase → no soft offer, even on orchestrated
            assert result.multi_intent_orchestrated
            assert result.pending_offer is None


class TestSoftOfferOnOrchestratedResponses:
    """Issue #819: Soft offers now apply to multi-intent orchestrated responses."""

    @pytest.mark.asyncio
    async def test_orchestrated_with_trigger_gets_offer(self, intent_service, mock_classifier):
        """Orchestrated response with meeting trigger → offer appended."""
        # Both intents must be substantive (non-CONVERSATION) for orchestration path
        intents = [
            _make_intent(IntentCategory.STATUS, "get_project_status"),
            _make_intent(IntentCategory.PRIORITY, "get_priorities"),
        ]

        # Message contains a soft trigger: "get the team together"
        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=intents,
            original_message="Check status and priorities, I need to get the team together",
            is_multi_intent=True,
        )

        with patch.object(
            intent_service.intent_orchestrator,
            "execute_plan",
            new_callable=AsyncMock,
        ) as mock_execute:
            from services.intent_service.orchestrator import (
                IntentExecutionResult,
                OrchestratedResponse,
            )

            mock_execute.return_value = OrchestratedResponse(
                results=[
                    IntentExecutionResult(
                        intent=intents[0],
                        response="Sprint is on track.",
                        intent_data={"category": "status", "action": "get_project_status"},
                        success=True,
                    ),
                    IntentExecutionResult(
                        intent=intents[1],
                        response="Top priority: deploy v2.",
                        intent_data={"category": "priority", "action": "get_priorities"},
                        success=True,
                    ),
                ],
                aggregated_message="Sprint is on track. Top priority: deploy v2.",
            )

            result = await intent_service.process_intent(
                message="Check status and priorities, I need to get the team together",
                session_id="sess_orch_trigger",
                user_id=None,
            )

            assert result.success
            assert result.multi_intent_orchestrated
            assert result.pending_offer is not None
            assert result.pending_offer["workflow_type"] == "meeting"
            # Original orchestrated message should still be present
            assert "Sprint is on track" in result.message


class TestLensContextInSoftOffer:
    """Issue #820: pending_offer includes active lens from conversation context."""

    @pytest.mark.asyncio
    async def test_pending_offer_includes_active_lens(self, intent_service, mock_classifier):
        """Soft offer includes active_lens field from conversation context."""
        intent = _make_intent(IntentCategory.CONVERSATION, "greeting")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="I need to get the team together Tuesday",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "That sounds like a plan!",
            "intent": {"category": "conversation", "action": "greeting"},
        }

        result = await intent_service.process_intent(
            message="I need to get the team together Tuesday",
            session_id="sess_lens",
            user_id=None,
        )

        assert result.pending_offer is not None
        assert "active_lens" in result.pending_offer
        # Lens may be None (no prior turns) or a value — just verify field exists

    @pytest.mark.asyncio
    async def test_no_offer_still_no_lens_field(self, intent_service, mock_classifier):
        """When no soft offer triggers, pending_offer remains None."""
        intent = _make_intent(IntentCategory.STATUS, "get_project_status")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="Check my project status",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "Here's your project status...",
            "intent": {"category": "status", "action": "get_project_status"},
        }

        result = await intent_service.process_intent(
            message="Check my project status",
            session_id="sess_no_lens",
            user_id=None,
        )

        assert result.pending_offer is None


class TestSoftOfferGracefulFallback:
    """Verify graceful degradation when soft invocation fails."""

    @pytest.mark.asyncio
    async def test_detector_error_graceful(self, intent_service, mock_classifier):
        """Detection error → normal response returned without offer."""
        intent = _make_intent(IntentCategory.CONVERSATION, "greeting")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="test message for error",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "Normal response.",
            "intent": {"category": "conversation", "action": "greeting"},
        }

        # Break the detector
        intent_service.soft_invocation_detector.detect = MagicMock(
            side_effect=RuntimeError("Detector broken")
        )

        result = await intent_service.process_intent(
            message="test message for error",
            session_id="sess1",
            user_id=None,
        )

        assert result.success
        assert result.message == "Normal response."
        assert result.pending_offer is None


class TestPendingOfferField:
    """Verify pending_offer field defaults and population."""

    def test_default_none(self):
        result = IntentProcessingResult(success=True, message="test", intent_data={})
        assert result.pending_offer is None

    def test_set_with_offer(self):
        result = IntentProcessingResult(
            success=True,
            message="test",
            intent_data={},
            pending_offer={
                "workflow_type": "meeting",
                "offer_message": "Want me to set up a meeting?",
                "decline_message": "No worries.",
            },
        )
        assert result.pending_offer["workflow_type"] == "meeting"


class TestTrustStageGating:
    """Issue #826: Soft offers gated by real trust stage, not hardcoded BUILDING."""

    @pytest.mark.asyncio
    async def test_new_user_gets_no_offers(self, intent_service, mock_classifier):
        """NEW trust stage → soft offer blocked (can_offer_hints=False)."""
        intent = _make_intent(IntentCategory.CONVERSATION, "greeting")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="I need to get the team together Tuesday",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "That sounds like a plan!",
            "intent": {"category": "conversation", "action": "greeting"},
        }

        # Mock the trust stage resolution to return NEW
        with patch("services.intent.intent_service.AsyncSessionFactory") as mock_factory:
            from services.shared_types import TrustStage

            mock_session = AsyncMock()
            mock_context = AsyncMock()
            mock_context.__aenter__ = AsyncMock(return_value=mock_session)
            mock_context.__aexit__ = AsyncMock(return_value=False)
            mock_factory.session_scope.return_value = mock_context

            # Mock trust repo and service to return NEW
            with (
                patch("services.intent.intent_service.UserTrustProfileRepository") as mock_repo_cls,
                patch("services.intent.intent_service.TrustComputationService") as mock_trust_cls,
            ):
                mock_trust_svc = AsyncMock()
                mock_trust_svc.get_trust_stage.return_value = TrustStage.NEW
                mock_trust_cls.return_value = mock_trust_svc

                result = await intent_service.process_intent(
                    message="I need to get the team together Tuesday",
                    session_id="sess_new_user",
                    user_id="00000000-0000-0000-0000-000000000001",
                )

        assert result.success
        # NEW user should NOT get a soft offer
        assert result.pending_offer is None
        # But should still get the canonical response
        assert "plan" in result.message.lower()

    @pytest.mark.asyncio
    async def test_building_user_gets_offers(self, intent_service, mock_classifier):
        """BUILDING trust stage → soft offers allowed (same as current behavior)."""
        intent = _make_intent(IntentCategory.CONVERSATION, "greeting")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="I need to get the team together Tuesday",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "That sounds like a plan!",
            "intent": {"category": "conversation", "action": "greeting"},
        }

        with patch("services.intent.intent_service.AsyncSessionFactory") as mock_factory:
            from services.shared_types import TrustStage

            mock_session = AsyncMock()
            mock_context = AsyncMock()
            mock_context.__aenter__ = AsyncMock(return_value=mock_session)
            mock_context.__aexit__ = AsyncMock(return_value=False)
            mock_factory.session_scope.return_value = mock_context

            with (
                patch("services.intent.intent_service.UserTrustProfileRepository") as mock_repo_cls,
                patch("services.intent.intent_service.TrustComputationService") as mock_trust_cls,
            ):
                mock_trust_svc = AsyncMock()
                mock_trust_svc.get_trust_stage.return_value = TrustStage.BUILDING
                mock_trust_cls.return_value = mock_trust_svc

                result = await intent_service.process_intent(
                    message="I need to get the team together Tuesday",
                    session_id="sess_building_user",
                    user_id="00000000-0000-0000-0000-000000000002",
                )

        assert result.success
        # BUILDING user SHOULD get a soft offer
        assert result.pending_offer is not None
        assert result.pending_offer["workflow_type"] == "meeting"

    @pytest.mark.asyncio
    async def test_no_user_id_defaults_to_building(self, intent_service, mock_classifier):
        """No user_id → defaults to BUILDING (backward-compatible)."""
        intent = _make_intent(IntentCategory.CONVERSATION, "greeting")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="I need to get the team together Tuesday",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "That sounds like a plan!",
            "intent": {"category": "conversation", "action": "greeting"},
        }

        # No user_id — trust stage lookup should be skipped
        result = await intent_service.process_intent(
            message="I need to get the team together Tuesday",
            session_id="sess_no_user",
            user_id=None,
        )

        assert result.success
        # Should still get offer (BUILDING default allows hints)
        assert result.pending_offer is not None

    @pytest.mark.asyncio
    async def test_trust_lookup_failure_falls_back_to_building(
        self, intent_service, mock_classifier
    ):
        """Trust stage lookup error → graceful fallback to BUILDING."""
        intent = _make_intent(IntentCategory.CONVERSATION, "greeting")

        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[intent],
            original_message="I need to get the team together Tuesday",
            is_multi_intent=False,
        )

        intent_service.canonical_handlers.handle.return_value = {
            "message": "That sounds like a plan!",
            "intent": {"category": "conversation", "action": "greeting"},
        }

        # Mock DB to throw an error
        with patch("services.intent.intent_service.AsyncSessionFactory") as mock_factory:
            mock_factory.session_scope.side_effect = RuntimeError("DB down")

            result = await intent_service.process_intent(
                message="I need to get the team together Tuesday",
                session_id="sess_fallback",
                user_id="00000000-0000-0000-0000-000000000003",
            )

        assert result.success
        # Should still work — falls back to BUILDING default
        assert result.pending_offer is not None
