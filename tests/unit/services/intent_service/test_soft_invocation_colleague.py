"""
Colleague tests for soft workflow invocation.

Issue #767: GLUE-SOFTINVOKE — Soft workflow invocation from natural language.
Phase 4: Colleague Test

Each test asks: "Would a colleague offer help this way?"

Scenarios:
1. Meeting need → offers to set up meeting
2. Project complexity → offers to organize
3. Deadline worry → offers status check
4. Casual chat → no unsolicited offer
5. Decline gracefully → conversation continues naturally
6. Throttled → no repeated offers
"""

from dataclasses import dataclass
from unittest.mock import patch
from uuid import uuid4

import pytest

from services.intent_service.soft_invocation import (
    SoftInvocationDetector,
    WorkflowOfferService,
    detect_offer_response,
)
from services.trust.proactivity_gate import TrustStage


@dataclass
class _MockWorkflowEntry:
    description: str = ""


# #923: Mock registry with all workflow types so colleague tests aren't gated
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


class TestSoftInvocationColleague:
    """Would a colleague respond this way?"""

    def test_scenario_1_meeting_need(self, detector, offer_service):
        """
        User: "I need to get the team together Tuesday"
        Colleague: [response] + "I could help set up a meeting. Want me to find a time?"

        NOT: Auto-scheduling a meeting without asking.
        NOT: Ignoring the implied need.
        """
        detection = detector.detect("I need to get the team together Tuesday")
        assert detection.has_offer
        assert detection.offer.workflow_type == "meeting"

        # Format the offer with a base response
        full_response = offer_service.format_offer(detection.offer, "Sounds like a busy week!")
        assert "Sounds like a busy week!" in full_response
        assert "meeting" in full_response.lower() or "find a time" in full_response.lower()
        # Offer includes a question (soft, not assuming)
        assert "?" in full_response

    def test_scenario_2_project_complexity(self, detector, offer_service):
        """
        User: "This project is getting complicated"
        Colleague: [response] + "I could help organize things. Want to set up some structure?"

        NOT: "I'll reorganize your entire project!"
        NOT: Ignoring the frustration.
        """
        detection = detector.detect("This project is getting complicated")
        assert detection.has_offer
        assert detection.offer.workflow_type == "project_setup"

        full_response = offer_service.format_offer(detection.offer, "That can be frustrating.")
        assert "frustrating" in full_response
        assert "organize" in full_response.lower() or "structure" in full_response.lower()
        assert "?" in full_response

    def test_scenario_3_deadline_worry(self, detector, offer_service):
        """
        User: "I'm worried about the deadline"
        Colleague: [response] + "Want me to pull up the project status?"

        NOT: "Don't worry, everything will be fine!" (dismissive)
        NOT: Auto-running a status report.
        """
        detection = detector.detect("I'm worried about the deadline")
        assert detection.has_offer
        assert detection.offer.workflow_type == "status_check"

        full_response = offer_service.format_offer(detection.offer, "That's understandable.")
        assert "understandable" in full_response
        assert "status" in full_response.lower() or "where things stand" in full_response.lower()
        assert "?" in full_response

    def test_scenario_4_casual_chat_no_offer(self, detector):
        """
        User: "What a nice day outside"
        Colleague: [normal response, no workflow offer]

        NOT: "Want me to schedule some outdoor time?" (annoying)
        """
        detection = detector.detect("What a nice day outside")
        assert not detection.has_offer

        detection = detector.detect("Thanks for the update!")
        assert not detection.has_offer

        detection = detector.detect("Good morning!")
        assert not detection.has_offer

    def test_scenario_5_decline_gracefully(self, detector, offer_service):
        """
        User: "This project is getting complicated"
        Piper: [response] + "I could help organize things. Want to set up some structure?"
        User: "No, just venting"
        Piper: "Got it, no worries. I'm here if you need help later."

        NOT: "Are you sure? I really think you should..."
        NOT: Awkward silence.
        """
        detection = detector.detect("This project is getting complicated")
        assert detection.has_offer

        # User declines
        user_reply = "No, just venting"
        response_type = detect_offer_response(user_reply)
        assert response_type == "decline"

        # Piper acknowledges gracefully
        decline_msg = offer_service.format_decline(detection.offer)
        assert "no worries" in decline_msg.lower() or "got it" in decline_msg.lower()

    def test_scenario_6_throttled_no_repeated_offers(self, detector, offer_service):
        """
        Turn 1: User expresses meeting need → offer made
        Turn 3: User expresses status concern → offer made (within window)
        Turn 4: User expresses priority need → NO offer (window saturated)

        NOT: Bombarding user with offers every message.
        """
        # First offer
        allowed_1, _ = offer_service.should_offer(
            trust_stage=TrustStage.BUILDING,
            session_id="sess1",
            current_turn=1,
            suggestions_this_session=0,
        )
        assert allowed_1
        offer_service.record_offer("sess1", 1)

        # Second offer in window
        allowed_2, _ = offer_service.should_offer(
            trust_stage=TrustStage.BUILDING,
            session_id="sess1",
            current_turn=3,
            suggestions_this_session=1,
        )
        assert allowed_2
        offer_service.record_offer("sess1", 3)

        # Third offer — should be blocked (2 offers in last 5 turns)
        allowed_3, reason = offer_service.should_offer(
            trust_stage=TrustStage.BUILDING,
            session_id="sess1",
            current_turn=4,
            suggestions_this_session=2,  # Hit BUILDING session limit of 2
        )
        assert not allowed_3


class TestSoftInvocationColleagueAuthenticated:
    """#1533 (principal-dropping audit) — every should_offer/record_offer
    call above omits user_id entirely (defaults to None), so this file never
    exercises the #817 user-scoped throttling key. If user_id were ever
    dropped from should_offer/record_offer's WorkflowOfferService._key
    composition, two authenticated users sharing a session_id would throttle
    each other's offers and this file's coverage would not catch it (m-44:
    a probe where the keys coincide is a config check, not a verification).
    """

    def test_two_authenticated_users_sharing_a_session_do_not_throttle_each_other(
        self, offer_service
    ):
        session_id = str(uuid4())
        user_a = str(uuid4())
        user_b = str(uuid4())

        # User A saturates their own offer window (2 offers in the window,
        # mirroring test_scenario_6_throttled_no_repeated_offers above).
        allowed_a1, _ = offer_service.should_offer(
            trust_stage=TrustStage.BUILDING,
            session_id=session_id,
            current_turn=1,
            suggestions_this_session=0,
            user_id=user_a,
        )
        assert allowed_a1
        offer_service.record_offer(session_id, 1, user_id=user_a)

        allowed_a2, _ = offer_service.should_offer(
            trust_stage=TrustStage.BUILDING,
            session_id=session_id,
            current_turn=3,
            suggestions_this_session=1,
            user_id=user_a,
        )
        assert allowed_a2
        offer_service.record_offer(session_id, 3, user_id=user_a)

        allowed_a3, _ = offer_service.should_offer(
            trust_stage=TrustStage.BUILDING,
            session_id=session_id,
            current_turn=4,
            suggestions_this_session=2,
            user_id=user_a,
        )
        assert not allowed_a3, "sanity: user A's own window should now be saturated"

        # The teeth: a DIFFERENT authenticated user sharing the SAME
        # session_id must get their own, independent window. If user_id
        # were dropped from the composite key, B's first offer would be
        # blocked by A's saturation above.
        allowed_b1, reason_b1 = offer_service.should_offer(
            trust_stage=TrustStage.BUILDING,
            session_id=session_id,
            current_turn=4,
            suggestions_this_session=0,
            user_id=user_b,
        )
        assert allowed_b1, (
            f"user B's offer window was throttled by user A's saturation on "
            f"the same session_id — user_id was dropped from the offer "
            f"throttle key ({reason_b1!r})"
        )
