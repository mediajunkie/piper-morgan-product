"""Tests for calendar-setup offer state preference helpers (Issue #790)."""

from __future__ import annotations

from uuid import uuid4

import pytest

from services.domain.user_preference_manager import (
    CALENDAR_OFFER_STATES,
    CALENDAR_SETUP_OFFERED,
    UserPreferenceManager,
)


@pytest.fixture
def manager() -> UserPreferenceManager:
    return UserPreferenceManager()


class TestCalendarOfferStateRoundTrip:
    """get_/set_calendar_setup_offer_state round-trip + default behavior."""

    async def test_default_is_none_when_never_set(self, manager):
        user_id = uuid4()
        state = await manager.get_calendar_setup_offer_state(user_id)
        assert state is None

    @pytest.mark.parametrize("state", sorted(CALENDAR_OFFER_STATES))
    async def test_set_then_get_returns_value(self, manager, state):
        user_id = uuid4()
        await manager.set_calendar_setup_offer_state(user_id, state)
        result = await manager.get_calendar_setup_offer_state(user_id)
        assert result == state

    async def test_set_to_none_clears_state(self, manager):
        user_id = uuid4()
        await manager.set_calendar_setup_offer_state(user_id, "offered")
        await manager.set_calendar_setup_offer_state(user_id, None)
        result = await manager.get_calendar_setup_offer_state(user_id)
        assert result is None

    async def test_state_is_per_user(self, manager):
        user_a = uuid4()
        user_b = uuid4()
        await manager.set_calendar_setup_offer_state(user_a, "declined")
        await manager.set_calendar_setup_offer_state(user_b, "accepted")
        assert await manager.get_calendar_setup_offer_state(user_a) == "declined"
        assert await manager.get_calendar_setup_offer_state(user_b) == "accepted"


class TestCalendarOfferStateValidation:
    """Setter rejects values outside the allowed vocabulary."""

    @pytest.mark.parametrize(
        "bad_value",
        ["yes", "OFFERED", "asked_again", "", " offered ", 0, True],
    )
    async def test_rejects_invalid_state(self, manager, bad_value):
        user_id = uuid4()
        with pytest.raises(ValueError):
            await manager.set_calendar_setup_offer_state(user_id, bad_value)


class TestCalendarOfferStateConstants:
    """Smoke checks on the exported constants."""

    def test_preference_key_is_stable_string(self):
        # Renaming this would break persisted user data — guard against drift.
        assert CALENDAR_SETUP_OFFERED == "calendar_setup_offered"

    def test_offer_states_set_matches_design(self):
        # Per gameplan + #790 Q4 disposition.
        assert CALENDAR_OFFER_STATES == frozenset({"offered", "declined", "deferred", "accepted"})
