"""#2093 — "Is my calendar connected?" gets one sentence; the general ask lists what is
connected and guides only for what is missing (CXO's words, 2026-10-19).

xian, alpha e801b1a309, 13:45 PT: with all four integrations connected, the question got the
setup opener, the Connected list, a "Popular integrations to connect" block naming the same
four, and setup guidance. Facts come from IntegrationStatusService; the text never decides.

LAYER: the handler through its public method with the status service replaced at its one
seam (`IntegrationStatusService.get_all`). DENOMINATOR: the five single-integration states
and three shapes of the general ask.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers

SEAM = "services.integrations.integration_status_service.IntegrationStatusService.get_all"


def _ok(via="keychain"):
    return {
        "configured": True,
        "via": via,
        "healthy": True,
        "last_check": "2026-10-19T20:46:16Z",
        "last_error": None,
    }


def _untested(via="keychain"):
    return {"configured": True, "via": via, "healthy": None, "last_check": None, "last_error": None}


def _failed(reason="Token expired or revoked. Please reconnect."):
    return {
        "configured": True,
        "via": "keychain",
        "healthy": False,
        "last_check": "2026-10-19T20:46:16Z",
        "last_error": reason,
    }


def _stale():
    return {
        "configured": True,
        "via": "oauth_binding_stale",
        "healthy": False,
        "last_check": None,
        "last_error": None,
    }


def _off():
    return {
        "configured": False,
        "via": None,
        "healthy": None,
        "last_check": None,
        "last_error": None,
    }


ALL_FOUR = {"github": _ok("oauth_binding"), "slack": _ok(), "calendar": _ok(), "notion": _ok()}


@pytest.fixture
def handlers():
    return CanonicalHandlers()


async def _ask(handlers, statuses, message):
    with patch(SEAM, new=AsyncMock(return_value=statuses)):
        return await handlers._format_integration_setup_guidance("u1", original_message=message)


class TestOneIntegrationAsked:
    @pytest.mark.asyncio
    async def test_connected_and_tested_is_one_sentence(self, handlers):
        out = await _ask(handlers, ALL_FOUR, "Is my calendar connected?")
        assert out["message"] == "Yes, Google Calendar is connected."
        assert out["intent"]["context"]["asked_integration"] == "calendar"

    @pytest.mark.asyncio
    async def test_connected_never_tested(self, handlers):
        st = dict(ALL_FOUR, calendar=_untested())
        out = await _ask(handlers, st, "is google calendar connected")
        assert out["message"] == "Yes, Google Calendar is connected (not tested yet)."

    @pytest.mark.asyncio
    async def test_connected_last_check_failed_names_the_reason(self, handlers):
        st = dict(ALL_FOUR, calendar=_failed())
        out = await _ask(handlers, st, "is my calendar connected?")
        assert out["message"].startswith(
            "Google Calendar is connected, but the last check failed: Token expired"
        )
        assert "Press Test in Settings → Integrations to try again." in out["message"]
        assert (
            "reconnect it" not in out["message"].lower()
        )  # no reconnect without an auth rejection

    @pytest.mark.asyncio
    async def test_not_connected(self, handlers):
        st = dict(ALL_FOUR, notion=_off())
        out = await _ask(handlers, st, "is notion connected?")
        # #2237 (CXO): Notion is outside the offered set, so it is not offered as a path.
        assert out["message"] == (
            "Notion isn't available in this beta yet. "
            "You can connect GitHub or Google Calendar in Settings → Integrations."
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "ask", ["how do I connect Google Calendar?", "help me connect google calendar"]
    )
    async def test_a_how_ask_gets_the_offer_without_no(self, handlers, ask):
        # CXO 10-23 21:22: a how-question opening with "No," reads like it answered a
        # different question.
        st = dict(ALL_FOUR, calendar=_off())
        out = await _ask(handlers, st, ask)
        assert out["message"] == (
            "Google Calendar isn't connected yet. Connect it in Settings → Integrations → "
            "Google Calendar."
        )

    @pytest.mark.asyncio
    async def test_rejected_grant_says_reconnect(self, handlers):
        st = dict(ALL_FOUR, github=_stale())
        out = await _ask(handlers, st, "is github connected?")
        assert out["message"].startswith("GitHub is connected, but the grant was rejected")
        assert "Reconnect it in Settings → Integrations → GitHub." in out["message"]

    @pytest.mark.asyncio
    async def test_two_named_is_the_general_ask(self, handlers):
        out = await _ask(handlers, ALL_FOUR, "are github and slack connected?")
        assert out["intent"]["context"]["asked_integration"] is None
        assert "✅ **Connected:**" in out["message"]


class TestGeneralAsk:
    @pytest.mark.asyncio
    async def test_all_four_connected_is_the_list_and_nothing_else(self, handlers):
        out = await _ask(handlers, ALL_FOUR, "what integrations do I have?")
        m = out["message"]
        assert m.startswith("✅ **Connected:**")
        for name in ("GitHub", "Slack", "Google Calendar", "Notion"):
            assert f"  - {name}" in m
        assert "happy to help" not in m
        assert "Popular integrations" not in m
        assert "Not connected" not in m
        assert "setup" not in m.lower()

    @pytest.mark.asyncio
    async def test_one_missing_guides_only_for_it(self, handlers):
        st = dict(ALL_FOUR, notion=_off(), slack=_untested())
        out = await _ask(handlers, st, "what integrations do I have?")
        m = out["message"]
        assert "  - Slack (not tested yet)" in m
        assert "⚪ **Not connected yet:**" in m
        assert "  - Notion — connect it in Settings → Integrations → Notion." in m
        assert "Popular integrations" not in m
        # the guidance names only the missing one
        assert m.count("connect it in Settings → Integrations →") == 1

    @pytest.mark.asyncio
    async def test_status_check_failure_is_said_plainly(self, handlers):
        with patch(SEAM, new=AsyncMock(side_effect=RuntimeError("db down"))):
            out = await handlers._format_integration_setup_guidance(
                "u1", original_message="is my calendar connected?"
            )
        m = out["message"]
        assert m.startswith("I couldn't check your current connection status just now")
        assert "Yes," not in m and "No," not in m
