"""
Tests for SoftInvocationDetector + WorkflowOfferService.

Issue #767: GLUE-SOFTINVOKE — Soft workflow invocation from natural language.
Phase 1: Pattern detection + data model
Phase 2: Offer service + throttling

Tests cover:
- Pattern matching for each workflow type (10+ expressions)
- No false positives on casual conversation
- WorkflowOffer properties
- OfferWindow exchange throttling
- ProactivityGate integration
- Offer formatting
- Accept/decline detection
"""

from dataclasses import dataclass
from unittest.mock import MagicMock, patch

import pytest

from services.intent_service.soft_invocation import (
    EXCHANGE_WINDOW_SIZE,
    MAX_OFFERS_PER_WINDOW,
    PROSE_LENGTH_FLOOR,
    OfferWindow,
    SoftInvocationDetector,
    WorkflowOffer,
    WorkflowOfferService,
    detect_offer_response,
    is_prose_reply,
)
from services.trust.proactivity_gate import ProactivityGate, TrustStage


@dataclass
class _MockWorkflowEntry:
    description: str = ""


# #923: All 7 workflow types registered for pattern-matching tests.
# In production, only registered types are offered. These tests verify
# the regex patterns themselves, so we mock the registry to allow all.
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
    """Mock the dispatcher registry so pattern tests aren't gated."""
    with patch(
        "services.intent_service.soft_invocation.get_registered_workflows",
        return_value=_ALL_WORKFLOW_TYPES,
        create=True,
    ):
        # Also need to patch where it's imported inside detect()
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


# --- Pattern Detection Tests ---


class TestMeetingPatterns:
    """Meeting/scheduling workflow detection."""

    def test_need_to_get_together(self, detector):
        result = detector.detect("I need to get the team together Tuesday")
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"

    def test_should_sync_up(self, detector):
        result = detector.detect("We should sync up about the release")
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"

    def test_lets_catch_up(self, detector):
        result = detector.detect("Let's catch up on the project this week")
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"

    def test_need_to_schedule_meeting(self, detector):
        result = detector.detect("I need to schedule a meeting with the design team")
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"

    def test_should_discuss(self, detector):
        result = detector.detect("We should talk about the roadmap")
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"

    def test_can_we_meet(self, detector):
        result = detector.detect("Can we meet to go over the proposal?")
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"


class TestProjectSetupPatterns:
    """Project organization workflow detection."""

    def test_project_getting_complicated(self, detector):
        result = detector.detect("This project is getting complicated")
        assert result.has_offer
        assert result.offer.workflow_type == "project_setup"

    def test_help_me_organize(self, detector):
        result = detector.detect("Help me organize this project")
        assert result.has_offer
        assert result.offer.workflow_type == "project_setup"

    def test_things_getting_messy(self, detector):
        result = detector.detect("Things are getting messy with all these tasks")
        assert result.has_offer
        assert result.offer.workflow_type == "project_setup"

    def test_dont_know_how_to_structure(self, detector):
        result = detector.detect("I don't know how to structure this")
        assert result.has_offer
        assert result.offer.workflow_type == "project_setup"

    def test_lost_track_of(self, detector):
        """Issue #850: 'lost track of' idiom."""
        result = detector.detect("I've lost track of all the open tasks")
        assert result.has_offer
        assert result.offer.workflow_type == "project_setup"

    def test_lost_sight_of(self, detector):
        """Issue #850: 'lost sight of' idiom."""
        result = detector.detect("I've lost sight of the original plan")
        assert result.has_offer
        assert result.offer.workflow_type == "project_setup"

    def test_fallen_behind_on(self, detector):
        """Issue #850: 'fallen behind on' idiom."""
        result = detector.detect("I've fallen behind on organizing the backlog")
        assert result.has_offer
        assert result.offer.workflow_type == "project_setup"


class TestStatusCheckPatterns:
    """Status/deadline concern detection."""

    def test_worried_about_deadline(self, detector):
        result = detector.detect("I'm worried about the deadline")
        assert result.has_offer
        assert result.offer.workflow_type == "status_check"

    def test_not_sure_where_things_stand(self, detector):
        result = detector.detect("I'm not sure where things stand on the release")
        assert result.has_offer
        assert result.offer.workflow_type == "status_check"

    def test_are_we_on_track(self, detector):
        result = detector.detect("Are we on track for Friday?")
        assert result.has_offer
        assert result.offer.workflow_type == "status_check"

    def test_how_are_things_going(self, detector):
        result = detector.detect("How are things going with the migration?")
        assert result.has_offer
        assert result.offer.workflow_type == "status_check"

    def test_will_we_finish_on_time(self, detector):
        """Issue #850: 'will we finish on time' expression."""
        result = detector.detect("Will we finish on time for the launch?")
        assert result.has_offer
        assert result.offer.workflow_type == "status_check"

    def test_will_we_make_it_by(self, detector):
        """Issue #850: 'will we make it by' expression."""
        result = detector.detect("Will we make it by the Friday deadline?")
        assert result.has_offer
        assert result.offer.workflow_type == "status_check"

    def test_will_we_be_ready_in_time(self, detector):
        """Issue #850: 'will we be ready in time' expression."""
        result = detector.detect("Will we be ready in time for the demo?")
        assert result.has_offer
        assert result.offer.workflow_type == "status_check"


class TestStandupPatterns:
    """Standup/alignment detection."""

    def test_team_needs_alignment(self, detector):
        result = detector.detect("The team needs alignment on the sprint goals")
        assert result.has_offer
        assert result.offer.workflow_type == "standup"

    def test_everyone_out_of_sync(self, detector):
        result = detector.detect("Everyone seems out of sync lately")
        assert result.has_offer
        assert result.offer.workflow_type == "standup"

    def test_should_do_standup(self, detector):
        result = detector.detect("We should do a standup today")
        assert result.has_offer
        assert result.offer.workflow_type == "standup"


class TestPersonalAgencyPatterns:
    """Issue #844: Personal agency expressions for team alignment."""

    def test_need_to_get_team_aligned(self, detector):
        """CXO test case: personal agency + adjective form."""
        result = detector.detect(
            "I really need to get the team aligned on our Q3 planning process."
        )
        assert result.has_offer
        assert result.offer.workflow_type == "standup"

    def test_want_to_make_sure_everyone_on_same_page(self, detector):
        result = detector.detect("I want to make sure everyone is on the same page.")
        assert result.has_offer
        assert result.offer.workflow_type == "standup"

    def test_have_to_get_team_in_sync(self, detector):
        result = detector.detect("I have to get the team in sync on priorities.")
        assert result.has_offer
        assert result.offer.workflow_type == "standup"

    def test_need_to_discuss_with_team(self, detector):
        result = detector.detect("I need to discuss this with the team.")
        assert result.has_offer
        assert result.offer.workflow_type == "meeting"

    def test_no_false_positive_personal_alignment(self, detector):
        """Should NOT match personal goals without team context."""
        result = detector.detect("I need to align my personal goals.")
        assert not result.has_offer


class TestReviewPatterns:
    """Review/feedback detection."""

    def test_need_someone_to_review(self, detector):
        result = detector.detect("Can someone review this PR?")
        assert result.has_offer
        assert result.offer.workflow_type == "review"

    def test_need_feedback(self, detector):
        result = detector.detect("I need feedback on the design doc")
        assert result.has_offer
        assert result.offer.workflow_type == "review"

    def test_another_pair_of_eyes(self, detector):
        """Issue #850: 'another pair of eyes' idiom."""
        result = detector.detect("This needs another pair of eyes before we ship it")
        assert result.has_offer
        assert result.offer.workflow_type == "review"

    def test_could_use_some_feedback(self, detector):
        """Issue #850: 'could use some feedback' expression."""
        result = detector.detect("I could use some feedback on this approach")
        assert result.has_offer
        assert result.offer.workflow_type == "review"

    def test_would_love_feedback(self, detector):
        """Issue #850: 'would love feedback' expression."""
        result = detector.detect("I would love feedback on the new layout")
        assert result.has_offer
        assert result.offer.workflow_type == "review"

    def test_can_this_get_another_look(self, detector):
        """Issue #850: 'can this get another look' expression."""
        result = detector.detect("Can this get another look before we merge?")
        assert result.has_offer
        assert result.offer.workflow_type == "review"

    def test_fresh_pair_of_eyes(self, detector):
        """Issue #850: 'a fresh pair of eyes' variant."""
        result = detector.detect("This could use a fresh pair of eyes")
        assert result.has_offer
        assert result.offer.workflow_type == "review"


class TestPriorityPatterns:
    """Priority/focus detection."""

    def test_dont_know_what_to_focus_on(self, detector):
        result = detector.detect("I don't know what to focus on today")
        assert result.has_offer
        assert result.offer.workflow_type == "priority_check"

    def test_too_many_things(self, detector):
        result = detector.detect("Too many things to do, I'm overwhelmed")
        assert result.has_offer
        assert result.offer.workflow_type == "priority_check"

    def test_what_should_i_work_on(self, detector):
        result = detector.detect("What should I work on first?")
        assert result.has_offer
        assert result.offer.workflow_type == "priority_check"

    def test_im_overwhelmed(self, detector):
        """Issue #850: Emotional overwhelm expression."""
        result = detector.detect("I'm overwhelmed with all these tasks")
        assert result.has_offer
        assert result.offer.workflow_type == "priority_check"

    def test_im_drowning(self, detector):
        """Issue #850: 'drowning' emotional expression."""
        result = detector.detect("I'm drowning in work right now")
        assert result.has_offer
        assert result.offer.workflow_type == "priority_check"

    def test_im_swamped(self, detector):
        """Issue #850: 'swamped' emotional expression."""
        result = detector.detect("I'm swamped this week")
        assert result.has_offer
        assert result.offer.workflow_type == "priority_check"

    def test_im_buried(self, detector):
        """Issue #850: 'buried' emotional expression."""
        result = detector.detect("I'm buried under all these requests")
        assert result.has_offer
        assert result.offer.workflow_type == "priority_check"

    def test_everything_feels_urgent(self, detector):
        """Issue #850: 'everything feels urgent' expression."""
        result = detector.detect("Everything feels urgent right now")
        assert result.has_offer
        assert result.offer.workflow_type == "priority_check"

    def test_everything_seems_pressing(self, detector):
        """Issue #850: 'everything seems pressing' expression."""
        result = detector.detect("Everything seems pressing and I can't decide what to tackle")
        assert result.has_offer
        assert result.offer.workflow_type == "priority_check"


class TestReminderPatterns:
    """Reminder/tracking detection."""

    def test_keep_forgetting(self, detector):
        result = detector.detect("I keep forgetting to update the changelog")
        assert result.has_offer
        assert result.offer.workflow_type == "reminder"

    def test_dont_let_me_forget(self, detector):
        result = detector.detect("I need to remember to follow up with Sarah")
        assert result.has_offer
        assert result.offer.workflow_type == "reminder"


# --- No False Positive Tests ---


class TestNoFalsePositives:
    """Ensure casual conversation doesn't trigger offers."""

    def test_simple_greeting(self, detector):
        result = detector.detect("Good morning!")
        assert not result.has_offer

    def test_casual_chat(self, detector):
        result = detector.detect("What a nice day outside")
        assert not result.has_offer

    def test_short_message(self, detector):
        result = detector.detect("Hey")
        assert not result.has_offer

    def test_empty_message(self, detector):
        result = detector.detect("")
        assert not result.has_offer

    def test_simple_question(self, detector):
        result = detector.detect("What time is it?")
        assert not result.has_offer

    def test_explicit_command(self, detector):
        # Explicit commands should use normal intent classification, not soft invocation
        result = detector.detect("Check my calendar")
        assert not result.has_offer

    def test_thank_you(self, detector):
        result = detector.detect("Thanks for the help!")
        assert not result.has_offer


# --- WorkflowOffer Data Model Tests ---


class TestWorkflowOffer:
    def test_creation(self):
        offer = WorkflowOffer(
            workflow_type="meeting",
            offer_message="Want me to set up a meeting?",
            decline_message="No worries.",
            confidence=0.7,
            trigger_pattern=r"test",
        )
        assert offer.workflow_type == "meeting"
        assert offer.confidence == 0.7

    def test_frozen(self):
        offer = WorkflowOffer(
            workflow_type="meeting",
            offer_message="test",
            decline_message="test",
            confidence=0.7,
        )
        with pytest.raises(AttributeError):
            offer.workflow_type = "standup"  # type: ignore


# --- OfferWindow Tests ---


class TestOfferWindow:
    def test_empty_window(self):
        window = OfferWindow()
        assert window.count_in_window(5) == 0

    def test_count_within_window(self):
        window = OfferWindow()
        window.record_offer(3)
        window.record_offer(5)
        # At turn 7, window covers turns 2-7: both offers are in window
        assert window.count_in_window(7) == 2

    def test_count_outside_window(self):
        window = OfferWindow()
        window.record_offer(1)
        window.record_offer(2)
        # At turn 10, window covers turns 5-10: neither offer is in window
        assert window.count_in_window(10) == 0

    def test_mixed_window(self):
        window = OfferWindow()
        window.record_offer(1)  # Outside window at turn 8
        window.record_offer(5)  # Inside window at turn 8
        assert window.count_in_window(8) == 1


# --- Accept/Decline Detection Tests ---


class TestAcceptDeclineDetection:
    def test_accept_yes(self):
        assert detect_offer_response("Yes") == "accept"

    def test_accept_sure(self):
        assert detect_offer_response("Sure!") == "accept"

    def test_accept_please(self):
        assert detect_offer_response("Please") == "accept"

    def test_accept_go_ahead(self):
        assert detect_offer_response("Go ahead") == "accept"

    def test_accept_sounds_good(self):
        assert detect_offer_response("Sounds good") == "accept"

    def test_accept_yes_please(self):
        assert detect_offer_response("Yes please") == "accept"

    def test_accept_lets_do_it(self):
        assert detect_offer_response("Let's do it") == "accept"

    def test_decline_no(self):
        assert detect_offer_response("No") == "decline"

    def test_decline_not_now(self):
        assert detect_offer_response("Not now") == "decline"

    def test_decline_just_venting(self):
        assert detect_offer_response("Just venting") == "decline"

    def test_decline_im_good(self):
        assert detect_offer_response("I'm good") == "decline"

    def test_decline_maybe_later(self):
        assert detect_offer_response("Maybe later") == "decline"

    def test_decline_no_thanks(self):
        assert detect_offer_response("No thanks") == "decline"

    def test_neither(self):
        assert detect_offer_response("Tell me more about the project") is None

    def test_empty(self):
        assert detect_offer_response("") is None


class TestProseOverride1631:
    """#1631 — a multi-line or >= PROSE_LENGTH_FLOOR-character turn is prose
    by shape, never an offer response. The unanchored accept/decline rows
    ("^please\\s", "\\bnot today\\b") must not claim a substring of a long
    free-text reply to whatever offer is armed."""

    _ACCEPT_GREED_PROSE = (
        "Please note that we should not delete this yet, not today anyway, "
        "because the migration is still running and three boards reference "
        "this item while it stays open — let's revisit after the cutover."
    )
    _DECLINE_GREED_PROSE = (
        "The rollout still has two unresolved dependencies, so not today for "
        "the cutover — we need the backup verified and the DNS change window "
        "approved before anything irreversible happens on this environment."
    )

    def test_fixture_prose_is_actually_long_single_line(self):
        # Guard the fixtures themselves: each must trip the length floor
        # (not the multi-line branch) or the tests below prove nothing.
        for prose in (self._ACCEPT_GREED_PROSE, self._DECLINE_GREED_PROSE):
            assert len(prose) >= PROSE_LENGTH_FLOOR
            assert "\n" not in prose

    def test_long_prose_opening_please_is_not_an_accept(self):
        assert detect_offer_response(self._ACCEPT_GREED_PROSE) is None

    def test_long_prose_containing_not_today_is_not_a_decline(self):
        assert detect_offer_response(self._DECLINE_GREED_PROSE) is None

    def test_multiline_turn_is_not_an_offer_response(self):
        assert (
            detect_offer_response("Yes, here is the plan:\n- step one\n- step two")
            is None
        )

    def test_short_accepts_unchanged(self):
        for message in ("Yes", "Yes please", "Sure, go ahead", "Please do", "Okay"):
            assert detect_offer_response(message) == "accept", message

    def test_short_declines_unchanged(self):
        for message in ("No", "No thanks", "Not now", "Not today", "Maybe later"):
            assert detect_offer_response(message) == "decline", message

    def test_just_below_floor_single_line_still_matches(self):
        message = "Yes, go ahead — " + "x" * (PROSE_LENGTH_FLOOR - 20)
        clean = message.strip()
        assert len(clean) < PROSE_LENGTH_FLOOR
        assert detect_offer_response(message) == "accept"

    def test_trailing_newline_does_not_count_as_multiline(self):
        assert detect_offer_response("Yes please\n") == "accept"

    def test_prose_override_opt_out_preserves_decline_in_prose(self):
        # Sole opt-out consumer: verified_inference's meta-feedback seam,
        # where a decline caught in prose only prevents a store.
        prose = (
            "No, that particular inference is wrong and should not be stored "
            "anywhere — and honestly, stop asking me every time about these "
            "details; I'd rather you trust your inferences going forward."
        )
        assert len(prose) >= PROSE_LENGTH_FLOOR
        assert detect_offer_response(prose) is None
        assert detect_offer_response(prose, prose_override=False) == "decline"

    def test_is_prose_reply_shape(self):
        assert is_prose_reply("a\nb") is True
        assert is_prose_reply("x" * PROSE_LENGTH_FLOOR) is True
        assert is_prose_reply("x" * (PROSE_LENGTH_FLOOR - 1)) is False


# --- WorkflowOfferService Tests ---


class TestOfferServiceThrottling:
    """ProactivityGate + exchange window throttling."""

    def test_new_user_blocked(self, offer_service):
        """NEW trust stage blocks all offers."""
        allowed, reason = offer_service.should_offer(
            trust_stage=TrustStage.NEW,
            session_id="sess1",
            current_turn=1,
            suggestions_this_session=0,
        )
        assert not allowed
        assert "doesn't allow" in reason

    def test_building_user_allowed(self, offer_service):
        """BUILDING trust stage allows hints."""
        allowed, reason = offer_service.should_offer(
            trust_stage=TrustStage.BUILDING,
            session_id="sess1",
            current_turn=1,
            suggestions_this_session=0,
        )
        assert allowed

    def test_established_user_allowed(self, offer_service):
        """ESTABLISHED trust stage allows suggestions."""
        allowed, reason = offer_service.should_offer(
            trust_stage=TrustStage.ESTABLISHED,
            session_id="sess1",
            current_turn=1,
            suggestions_this_session=0,
        )
        assert allowed

    def test_session_limit_reached(self, offer_service):
        """Session-level limit blocks offers."""
        allowed, reason = offer_service.should_offer(
            trust_stage=TrustStage.BUILDING,
            session_id="sess1",
            current_turn=1,
            suggestions_this_session=5,  # Over BUILDING limit of 2
        )
        assert not allowed
        assert "limit" in reason

    def test_exchange_window_saturated(self, offer_service):
        """Exchange window blocks after MAX_OFFERS_PER_WINDOW."""
        # Record 2 offers in recent turns
        offer_service.record_offer("sess1", 3)
        offer_service.record_offer("sess1", 4)

        allowed, reason = offer_service.should_offer(
            trust_stage=TrustStage.ESTABLISHED,
            session_id="sess1",
            current_turn=5,
            suggestions_this_session=2,
        )
        assert not allowed
        assert "window saturated" in reason

    def test_exchange_window_clears(self, offer_service):
        """Old offers fall out of window."""
        offer_service.record_offer("sess1", 1)
        offer_service.record_offer("sess1", 2)

        # At turn 10, both offers are outside the 5-turn window
        allowed, reason = offer_service.should_offer(
            trust_stage=TrustStage.ESTABLISHED,
            session_id="sess1",
            current_turn=10,
            suggestions_this_session=2,
        )
        assert allowed


class TestOfferServiceFormatting:
    """Offer message formatting."""

    def test_format_offer_appends(self, offer_service):
        offer = WorkflowOffer(
            workflow_type="meeting",
            offer_message="Want me to set up a meeting?",
            decline_message="No worries.",
            confidence=0.7,
        )
        result = offer_service.format_offer(offer, "That sounds like a busy day.")
        assert "busy day" in result
        assert "set up a meeting" in result

    def test_format_offer_strips_trailing_whitespace(self, offer_service):
        offer = WorkflowOffer(
            workflow_type="meeting",
            offer_message="Want me to help?",
            decline_message="No worries.",
            confidence=0.7,
        )
        result = offer_service.format_offer(offer, "Response here.  \n")
        assert result.startswith("Response here.")

    def test_format_acceptance_known_type(self, offer_service):
        msg = offer_service.format_acceptance("meeting")
        assert "set that up" in msg

    def test_format_acceptance_unknown_type(self, offer_service):
        msg = offer_service.format_acceptance("unknown_workflow")
        assert "help" in msg

    def test_format_decline(self, offer_service):
        offer = WorkflowOffer(
            workflow_type="meeting",
            offer_message="test",
            decline_message="No worries, just let me know.",
            confidence=0.7,
        )
        msg = offer_service.format_decline(offer)
        assert msg == "No worries, just let me know."


# --- SoftInvocationResult Tests ---


class TestSoftInvocationResult:
    def test_no_offer_result(self, detector):
        result = detector.detect("Good morning!")
        assert not result.has_offer
        assert result.offer is None
        assert result.reason

    def test_offer_result(self, detector):
        result = detector.detect("I need to get the team together")
        assert result.has_offer
        assert result.offer is not None
        assert result.offer.workflow_type == "meeting"
        assert result.offer.offer_message
        assert result.offer.decline_message
        assert result.offer.confidence > 0


# --- Lens-Boosted Confidence Tests (#822) ---


class TestLensBoostedConfidence:
    """Test that active conversational lens boosts soft invocation confidence."""

    def test_calendar_lens_boosts_meeting(self, detector):
        """Calendar lens + meeting pattern → boosted confidence."""
        result = detector.detect("We need to schedule a meeting about this", active_lens="calendar")
        assert result.has_offer
        assert result.offer.confidence > 0.7  # Boosted above baseline

    def test_no_lens_gives_baseline(self, detector):
        """No lens → baseline 0.7 confidence."""
        result = detector.detect("We need to schedule a meeting about this")
        assert result.has_offer
        assert result.offer.confidence == 0.7

    def test_unrelated_lens_no_boost(self, detector):
        """Issues lens + meeting pattern → no boost."""
        result = detector.detect("We need to schedule a meeting about this", active_lens="issues")
        assert result.has_offer
        assert result.offer.confidence == 0.7  # No affinity

    def test_issues_lens_boosts_priority_check(self, detector):
        """Issues lens + priority pattern → boosted confidence."""
        result = detector.detect("I don't know what to focus on first", active_lens="issues")
        assert result.has_offer
        assert result.offer.confidence > 0.7

    def test_people_lens_boosts_standup(self, detector):
        """People lens + standup pattern → boosted confidence."""
        result = detector.detect("We should do a quick standup", active_lens="people")
        assert result.has_offer
        assert result.offer.confidence > 0.7

    def test_confidence_capped_at_095(self, detector):
        """Boosted confidence should not exceed 0.95."""
        result = detector.detect("We need to schedule a meeting", active_lens="calendar")
        assert result.has_offer
        assert result.offer.confidence <= 0.95


# --- User-Scoped Composite Key Tests (#817) ---


class TestCompositeKeys:
    """Test that WorkflowOfferService uses user-scoped composite keys."""

    def test_pending_offers_session_scoped(self, offer_service):
        """Issue #846: Pending offers are session-scoped, not user-scoped.

        Offers are transient (one-turn lifetime). Using session_id alone
        prevents key mismatch when user_id changes between turns (e.g.,
        auth token expiry). Same session = same offer, regardless of user_id.
        """
        offer_alice = {"workflow_type": "meeting"}
        offer_service.set_pending_offer("sess1", offer_alice, user_id="alice")

        # Retrieve with different user_id — still finds the offer (#846 fix)
        retrieved = offer_service.get_and_clear_pending_offer("sess1", user_id="bob")
        assert retrieved["workflow_type"] == "meeting"

    def test_pending_offer_survives_auth_change(self, offer_service):
        """Issue #846: Offer set with user_id is retrievable without user_id."""
        offer_service.set_pending_offer("sess1", {"workflow_type": "standup"}, user_id="alice")

        # Simulate auth loss on next turn — user_id becomes None
        retrieved = offer_service.get_and_clear_pending_offer("sess1", user_id=None)
        assert retrieved is not None
        assert retrieved["workflow_type"] == "standup"

    def test_different_sessions_isolated(self, offer_service):
        """Different sessions still have separate pending offers."""
        offer_service.set_pending_offer("sess1", {"workflow_type": "meeting"})
        offer_service.set_pending_offer("sess2", {"workflow_type": "standup"})

        r1 = offer_service.get_and_clear_pending_offer("sess1")
        r2 = offer_service.get_and_clear_pending_offer("sess2")
        assert r1["workflow_type"] == "meeting"
        assert r2["workflow_type"] == "standup"

    def test_throttling_still_user_scoped(self, offer_service):
        """Throttling uses composite key — different users on same session are isolated."""
        offer_service.record_offer("sess1", turn=1, user_id="alice")
        offer_service.record_offer("sess1", turn=2, user_id="alice")

        key_alice = offer_service._key("sess1", "alice")
        key_bob = offer_service._key("sess1", "bob")
        assert key_alice in offer_service._offer_windows
        assert key_bob not in offer_service._offer_windows

    def test_anonymous_throttling_fallback(self, offer_service):
        """No user_id falls back to 'anonymous' composite key for throttling."""
        key = offer_service._key("sess1")
        assert key == "anonymous:sess1"


# --- #923: Registry Gate Tests ---


class TestRegistryGate:
    """
    #923: Soft invocation only offers workflow types that have registered
    entry points in the dispatcher. Unregistered types are suppressed.
    """

    def test_registered_type_offered(self):
        """Meeting (registered) should produce an offer."""
        only_meeting = {"meeting": _MockWorkflowEntry(description="Meeting scheduling")}
        with patch(
            "services.intent_service.workflow_dispatcher.get_registered_workflows",
            return_value=only_meeting,
        ):
            d = SoftInvocationDetector()
            result = d.detect("I need to get the team together on Tuesday")
            assert result.has_offer
            assert result.offer.workflow_type == "meeting"

    def test_unregistered_type_suppressed(self):
        """Priority check (not registered) should NOT produce an offer."""
        only_meeting = {"meeting": _MockWorkflowEntry(description="Meeting scheduling")}
        with patch(
            "services.intent_service.workflow_dispatcher.get_registered_workflows",
            return_value=only_meeting,
        ):
            d = SoftInvocationDetector()
            result = d.detect("I'm so overwhelmed with too many things to do")
            assert not result.has_offer

    def test_empty_registry_suppresses_all(self):
        """With no registered workflows, no offers should be made."""
        with patch(
            "services.intent_service.workflow_dispatcher.get_registered_workflows",
            return_value={},
        ):
            d = SoftInvocationDetector()
            # meeting pattern
            r1 = d.detect("I need to get the team together on Tuesday")
            assert not r1.has_offer
            # priority pattern
            r2 = d.detect("I'm overwhelmed with too many priorities")
            assert not r2.has_offer

    def test_adding_workflow_enables_offers(self):
        """When a workflow type is added to registry, offers start appearing."""
        registry = {"meeting": _MockWorkflowEntry(), "reminder": _MockWorkflowEntry()}
        with patch(
            "services.intent_service.workflow_dispatcher.get_registered_workflows",
            return_value=registry,
        ):
            d = SoftInvocationDetector()
            result = d.detect("I keep forgetting to follow up on this task")
            assert result.has_offer
            assert result.offer.workflow_type == "reminder"

    def test_removing_workflow_disables_offers(self):
        """When a workflow type is removed from registry, offers stop."""
        # meeting is normally in the default registry, but simulate removal
        no_meeting = {"reminder": _MockWorkflowEntry()}
        with patch(
            "services.intent_service.workflow_dispatcher.get_registered_workflows",
            return_value=no_meeting,
        ):
            d = SoftInvocationDetector()
            result = d.detect("We need to schedule a meeting about this")
            assert not result.has_offer
