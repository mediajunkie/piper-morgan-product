"""Unit tests for the calendar-offer decision policy (Issue #790)."""

from __future__ import annotations

import pytest

from services.intent_service.calendar_offer_policy import (
    GUIDANCE_TEXT,
    OFFER_TEXT,
    CalendarOfferDecision,
    decide_calendar_offer,
)
from services.shared_types import TrustStage


def _decide(
    *,
    calendar_connected: bool = False,
    current_state=None,
    user_intent_mentions_calendar: bool = False,
    trust_stage: TrustStage = TrustStage.NEW,
) -> CalendarOfferDecision:
    return decide_calendar_offer(
        calendar_connected=calendar_connected,
        current_state=current_state,
        user_intent_mentions_calendar=user_intent_mentions_calendar,
        trust_stage=trust_stage,
    )


class TestCalendarConnected:
    """When the calendar is already connected, no offer ever surfaces."""

    def test_connected_no_prior_state(self):
        d = _decide(calendar_connected=True, current_state=None)
        assert d.should_offer is False
        assert d.offer_text == ""
        assert d.new_state is None

    def test_connected_even_when_user_mentions_calendar(self):
        d = _decide(
            calendar_connected=True,
            current_state="declined",
            user_intent_mentions_calendar=True,
        )
        assert d.should_offer is False
        assert d.new_state is None

    def test_connected_across_all_trust_stages(self):
        for stage in (
            TrustStage.NEW,
            TrustStage.BUILDING,
            TrustStage.ESTABLISHED,
            TrustStage.TRUSTED,
        ):
            d = _decide(calendar_connected=True, trust_stage=stage)
            assert d.should_offer is False, f"stage={stage}"


class TestFirstEncounter:
    """Calendar disconnected and never offered before — surface offer once."""

    def test_first_encounter_greeting_context(self):
        d = _decide(current_state=None, user_intent_mentions_calendar=False)
        assert d.should_offer is True
        assert d.offer_text == OFFER_TEXT
        assert d.new_state == "offered"

    def test_first_encounter_calendar_query_context(self):
        d = _decide(current_state=None, user_intent_mentions_calendar=True)
        assert d.should_offer is True
        assert d.offer_text == OFFER_TEXT
        assert d.new_state == "offered"

    def test_first_encounter_does_not_vary_by_trust_stage_for_mvp(self):
        offers = [
            _decide(current_state=None, trust_stage=stage)
            for stage in (
                TrustStage.NEW,
                TrustStage.BUILDING,
                TrustStage.ESTABLISHED,
                TrustStage.TRUSTED,
            )
        ]
        # All four should produce identical offer text per #790 Q2
        # ("one wording for MVP"). If this test starts failing, it's because
        # stage-variant copy was added — update the test to match the design.
        assert {o.offer_text for o in offers} == {OFFER_TEXT}


class TestDeclinedOrDeferredGreetingContext:
    """User previously declined or deferred — stay silent in greeting context."""

    @pytest.mark.parametrize("state", ["declined", "deferred"])
    def test_silent_when_not_asking(self, state):
        d = _decide(current_state=state, user_intent_mentions_calendar=False)
        assert d.should_offer is False
        assert d.offer_text == ""
        assert d.new_state is None  # Don't change state in silent path


class TestDeclinedOrDeferredCalendarContext:
    """User previously declined/deferred but now actively asking about calendar."""

    @pytest.mark.parametrize("state", ["declined", "deferred"])
    def test_guidance_when_user_asks(self, state):
        d = _decide(current_state=state, user_intent_mentions_calendar=True)
        assert d.should_offer is True
        assert d.offer_text == GUIDANCE_TEXT
        # State stays as-is — user re-asking doesn't reset to "offered"
        assert d.new_state is None


class TestOfferedState:
    """User was offered but hasn't reacted yet."""

    def test_silent_when_not_asking(self):
        d = _decide(current_state="offered", user_intent_mentions_calendar=False)
        assert d.should_offer is False

    def test_guidance_when_user_asks(self):
        d = _decide(current_state="offered", user_intent_mentions_calendar=True)
        assert d.should_offer is True
        assert d.offer_text == GUIDANCE_TEXT
        assert d.new_state is None


class TestAcceptedState:
    """User accepted the offer — they're connecting; don't re-pitch."""

    def test_silent_in_greeting(self):
        d = _decide(current_state="accepted", user_intent_mentions_calendar=False)
        assert d.should_offer is False

    def test_guidance_when_user_asks(self):
        # If they accepted but somehow still aren't connected (e.g., setup
        # incomplete), and they're asking, we should still surface guidance.
        d = _decide(current_state="accepted", user_intent_mentions_calendar=True)
        assert d.should_offer is True
        assert d.offer_text == GUIDANCE_TEXT


class TestOfferTextContent:
    """Smoke checks on the user-visible copy (per PM Q1 disposition)."""

    def test_offer_text_includes_settings_path(self):
        assert "/settings/integrations/calendar" in OFFER_TEXT

    def test_guidance_text_includes_settings_path(self):
        assert "/settings/integrations/calendar" in GUIDANCE_TEXT

    def test_offer_text_does_not_claim_calendar_data(self):
        # Trust violation guard from #789 — must not imply we have data.
        forbidden = ["no meetings", "your meetings", "you have", "I see you"]
        lowered = OFFER_TEXT.lower()
        for phrase in forbidden:
            assert phrase not in lowered, f"OFFER_TEXT must not claim calendar data: {phrase!r}"


class TestDecisionImmutability:
    """CalendarOfferDecision is frozen — defensive against accidental mutation."""

    def test_decision_is_frozen(self):
        d = _decide(current_state=None)
        with pytest.raises(Exception):
            d.should_offer = False  # type: ignore[misc]
