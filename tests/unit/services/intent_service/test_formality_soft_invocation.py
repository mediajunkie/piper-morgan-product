"""
Tests for formality-aware soft invocation (#838).

Verifies that SoftInvocationDetector and WorkflowOfferService select
the correct message tier based on formality_baseline.
"""

from dataclasses import dataclass
from unittest.mock import patch

import pytest

from services.intent_service.soft_invocation import (
    _SOFT_TRIGGER_PATTERNS,
    SoftInvocationDetector,
    WorkflowOffer,
    WorkflowOfferService,
)


@dataclass
class _MockWorkflowEntry:
    description: str = ""


# #923: Mock registry with all workflow types so pattern tests aren't gated
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


@pytest.fixture
def detector():
    return SoftInvocationDetector()


@pytest.fixture
def offer_service():
    return WorkflowOfferService()


# --- Tier selection via formality_baseline ---


class TestFormalityTierSelection:
    """detect() picks the right message tier based on formality_baseline."""

    def test_warm_tier_with_high_baseline(self, detector):
        """baseline=0.8 -> warm tier (exclamation marks, casual)."""
        result = detector.detect(
            "I need to get the team together Tuesday",
            formality_baseline=0.8,
        )
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"
        # Warm tier uses exclamation mark
        assert "!" in result.offer.offer_message
        assert "!" in result.offer.decline_message

    def test_professional_tier_with_low_baseline(self, detector):
        """baseline=0.2 -> professional tier (concise, formal)."""
        result = detector.detect(
            "I need to get the team together Tuesday",
            formality_baseline=0.2,
        )
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"
        # Professional tier uses "Shall I" phrasing
        assert "Shall I" in result.offer.offer_message
        # Professional decline uses "Understood"
        assert "Understood" in result.offer.decline_message

    def test_balanced_tier_with_mid_baseline(self, detector):
        """baseline=0.5 -> balanced tier (period endings, moderate)."""
        result = detector.detect(
            "I need to get the team together Tuesday",
            formality_baseline=0.5,
        )
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"
        # Balanced tier: same as old behavior (period, not exclamation)
        assert (
            result.offer.offer_message == "I could help set up a meeting. Want me to find a time?"
        )
        assert (
            result.offer.decline_message == "No worries, just let me know if you change your mind."
        )

    def test_none_baseline_defaults_to_balanced(self, detector):
        """baseline=None -> balanced tier (backward compatible)."""
        result = detector.detect(
            "I need to get the team together Tuesday",
            formality_baseline=None,
        )
        assert result.has_offer
        # Should get balanced tier (same as old behavior)
        assert (
            result.offer.offer_message == "I could help set up a meeting. Want me to find a time?"
        )

    def test_omitted_baseline_defaults_to_balanced(self, detector):
        """No formality_baseline argument -> balanced tier (backward compatible)."""
        result = detector.detect("I need to get the team together Tuesday")
        assert result.has_offer
        assert (
            result.offer.offer_message == "I could help set up a meeting. Want me to find a time?"
        )


# --- All workflow types have all three tiers ---


class TestAllWorkflowTypesHaveFormality:
    """Every workflow type in _SOFT_TRIGGER_PATTERNS has warm/balanced/professional tiers."""

    def test_all_patterns_have_three_offer_tiers(self):
        for _patterns, workflow_type, offer_msgs, _decline_msgs in _SOFT_TRIGGER_PATTERNS:
            for tier in ("warm", "balanced", "professional"):
                assert tier in offer_msgs, f"Workflow '{workflow_type}' missing '{tier}' offer tier"
                assert isinstance(offer_msgs[tier], str)
                assert len(offer_msgs[tier]) > 0

    def test_all_patterns_have_three_decline_tiers(self):
        for _patterns, workflow_type, _offer_msgs, decline_msgs in _SOFT_TRIGGER_PATTERNS:
            for tier in ("warm", "balanced", "professional"):
                assert (
                    tier in decline_msgs
                ), f"Workflow '{workflow_type}' missing '{tier}' decline tier"
                assert isinstance(decline_msgs[tier], str)
                assert len(decline_msgs[tier]) > 0


# --- Per-workflow formality spot checks ---


class TestWorkflowFormalityMessages:
    """Spot-check each workflow type resolves correct tier."""

    @pytest.mark.parametrize(
        "message,workflow_type",
        [
            ("I need to get the team together Tuesday", "meeting"),
            ("This project is getting really complicated", "project_setup"),
            ("I'm worried about the deadline", "status_check"),
            ("The team needs better alignment", "standup"),
            ("Can someone review this pull request please", "review"),
            ("I don't know what to focus on anymore", "priority_check"),
            ("I keep forgetting to follow up on that", "reminder"),
        ],
    )
    def test_warm_tier_uses_exclamation(self, detector, message, workflow_type):
        result = detector.detect(message, formality_baseline=0.9)
        assert result.has_offer
        assert result.offer.workflow_type == workflow_type
        assert "!" in result.offer.offer_message

    @pytest.mark.parametrize(
        "message,workflow_type",
        [
            ("I need to get the team together Tuesday", "meeting"),
            ("This project is getting really complicated", "project_setup"),
            ("I'm worried about the deadline", "status_check"),
            ("The team needs better alignment", "standup"),
            ("Can someone review this pull request please", "review"),
            ("I don't know what to focus on anymore", "priority_check"),
            ("I keep forgetting to follow up on that", "reminder"),
        ],
    )
    def test_professional_tier_is_formal(self, detector, message, workflow_type):
        result = detector.detect(message, formality_baseline=0.1)
        assert result.has_offer
        assert result.offer.workflow_type == workflow_type
        # Professional decline messages all start with "Understood"
        assert result.offer.decline_message.startswith("Understood")


# --- WorkflowOfferService.format_acceptance with formality ---


class TestFormatAcceptanceFormality:
    """format_acceptance() selects tier based on formality_baseline."""

    def test_warm_acceptance(self, offer_service):
        msg = offer_service.format_acceptance("meeting", formality_baseline=0.8)
        assert msg == "Great! Let me help set that up."

    def test_professional_acceptance(self, offer_service):
        msg = offer_service.format_acceptance("meeting", formality_baseline=0.1)
        assert msg == "Confirmed. I'll arrange the meeting."

    def test_balanced_acceptance(self, offer_service):
        msg = offer_service.format_acceptance("meeting", formality_baseline=0.5)
        assert msg == "Great! Let me help set that up."

    def test_none_baseline_defaults_balanced(self, offer_service):
        msg = offer_service.format_acceptance("meeting", formality_baseline=None)
        assert msg == "Great! Let me help set that up."

    def test_no_baseline_arg_defaults_balanced(self, offer_service):
        """Backward compatible: no formality_baseline argument."""
        msg = offer_service.format_acceptance("meeting")
        assert msg == "Great! Let me help set that up."

    def test_unknown_workflow_warm(self, offer_service):
        msg = offer_service.format_acceptance("unknown", formality_baseline=0.9)
        assert msg == "Let me help with that!"

    def test_unknown_workflow_professional(self, offer_service):
        msg = offer_service.format_acceptance("unknown", formality_baseline=0.1)
        assert msg == "I'll proceed."

    def test_all_known_workflows_have_professional(self, offer_service):
        """All known workflow types return a professional acceptance."""
        known = [
            "meeting",
            "project_setup",
            "status_check",
            "standup",
            "review",
            "priority_check",
            "reminder",
        ]
        for wf in known:
            msg = offer_service.format_acceptance(wf, formality_baseline=0.1)
            assert (
                isinstance(msg, str) and len(msg) > 0
            ), f"Workflow '{wf}' missing professional acceptance"


# --- format_decline with formality ---


class TestFormatDeclineFormality:
    """format_decline() returns the offer's already-resolved decline_message."""

    def test_decline_returns_offer_message(self, offer_service):
        offer = WorkflowOffer(
            workflow_type="meeting",
            offer_message="test offer",
            decline_message="Understood. Let me know if you'd like to revisit.",
            confidence=0.7,
        )
        msg = offer_service.format_decline(offer, formality_baseline=0.2)
        assert msg == "Understood. Let me know if you'd like to revisit."

    def test_decline_ignores_baseline_uses_offer_message(self, offer_service):
        """formality_baseline is accepted but the offer's pre-resolved message wins."""
        offer = WorkflowOffer(
            workflow_type="meeting",
            offer_message="test",
            decline_message="Custom decline",
            confidence=0.7,
        )
        # Even with warm baseline, returns the offer's decline_message as-is
        msg = offer_service.format_decline(offer, formality_baseline=0.9)
        assert msg == "Custom decline"


# #1863 (2026-09-23, Rule-0 rip, Arch GO): TestFormalityWithLensBoosting
# was deleted here — it exercised the #822 active_lens confidence boost,
# which had no live writer and is removed along with SoftInvocationDetector.
# detect()'s active_lens parameter. Formality-tier selection itself is still
# covered by the classes above; nothing about that behavior depended on lens.
