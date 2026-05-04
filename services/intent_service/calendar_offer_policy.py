"""Calendar setup offer decision policy.

Issue #790 MVP trust-gated calendar integration behavior.

Pure decision function: given the user's calendar-connection state, prior
offer state, and whether the user is currently asking about calendar, decide
whether to surface a setup-help offer + what to persist back as the new
offer state.

Trust stage is accepted as an input for future stage-variant copy, but per
PM disposition 2026-05-03 (#790 Q2), MVP uses one wording across stages.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from services.shared_types import TrustStage


CALENDAR_SETTINGS_PATH = "/settings/integrations/calendar"

# Per #790 Q1 disposition (PM 2026-05-03): "approved as drafted".
OFFER_TEXT = (
    "I noticed your calendar isn't connected yet — would you like help "
    "setting that up? You can connect Google Calendar at "
    f"{CALENDAR_SETTINGS_PATH}."
)

GUIDANCE_TEXT = (
    "Calendar isn't connected yet — you can set up Google Calendar at "
    f"{CALENDAR_SETTINGS_PATH}."
)


@dataclass(frozen=True)
class CalendarOfferDecision:
    """Outcome of decide_calendar_offer.

    Attributes:
        should_offer: Whether to append offer/guidance text to the response.
        offer_text: The text to append (empty when should_offer=False).
        new_state: New state to persist via UserPreferenceManager, or None
            to leave the existing state unchanged.
    """

    should_offer: bool
    offer_text: str
    new_state: Optional[str]


def decide_calendar_offer(
    *,
    calendar_connected: bool,
    current_state: Optional[str],
    user_intent_mentions_calendar: bool,
    trust_stage: TrustStage,
) -> CalendarOfferDecision:
    """Decide whether to offer calendar setup help.

    Args:
        calendar_connected: Whether the user's calendar is connected.
        current_state: Existing offer state from UserPreferenceManager
            (None | "offered" | "declined" | "deferred" | "accepted").
        user_intent_mentions_calendar: Whether the user's current message
            invoked a calendar-related intent (so guidance is appropriate
            even when prior state is "declined" or "deferred").
        trust_stage: User's current trust stage. Accepted but not currently
            used to vary copy (per #790 Q2: one wording for MVP).

    Returns:
        CalendarOfferDecision describing what to surface and what to persist.
    """
    # If calendar is connected, no offer needed regardless of any other input.
    if calendar_connected:
        return CalendarOfferDecision(
            should_offer=False, offer_text="", new_state=None
        )

    # First encounter: never offered before.
    if current_state is None:
        return CalendarOfferDecision(
            should_offer=True, offer_text=OFFER_TEXT, new_state="offered"
        )

    # User is actively asking about calendar — surface guidance regardless
    # of prior decline/defer (they explicitly want help right now).
    if user_intent_mentions_calendar:
        return CalendarOfferDecision(
            should_offer=True, offer_text=GUIDANCE_TEXT, new_state=None
        )

    # Otherwise stay silent: prior states ("offered", "declined", "deferred",
    # "accepted") all mean we shouldn't proactively re-pitch in a generic
    # greeting context.
    return CalendarOfferDecision(
        should_offer=False, offer_text="", new_state=None
    )
