"""#2092 — a failed calendar read is said as a failed read, never as "no meetings".

xian, alpha e801b1a309, 2026-10-19 13:45: "Do I have any meetings this week?" → "I didn't find
any events in the calendar for the next 7 days." The log held Google's 403 "Request had
insufficient authentication scopes" for the same call; the adapter had swallowed it into [].
The Settings Test read "Healthy" because it only refreshed the token.

LAYER: the classifier and adapter directly (a service stub that raises), the two chat handlers
through their methods with the router replaced at its seam, and the Settings Test coroutine
with the probe replaced at its seam. DENOMINATOR: four error classes, two handlers, the Test's
three outcomes.
"""

import logging
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import (
    CALENDAR_READ_FAILED_LINES,
    IntentService,
    calendar_read_failed_line,
)
from services.mcp.consumer.google_calendar_adapter import classify_calendar_read_error
from services.shared_types import IntentCategory

ROUTER = "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
GOOGLE_403 = (
    "<HttpError 403 when requesting https://www.googleapis.com/calendar/v3/calendars/primary/events"
    ' returned "Request had insufficient authentication scopes.". Details: "[{\'message\': '
    "'Insufficient Permission', 'domain': 'global', 'reason': 'insufficientPermissions'}]\">"
)


def _secret_read(value):
    """#2151: the provenance read the calendar Test makes (``aread_secret``), mirroring a
    mocked ``get_api_key`` value: present when set, verified absent when None."""
    from services.infrastructure.keychain_service import SecretProvenance, SecretRead

    if value:
        return SecretRead(SecretProvenance.PRESENT, value=value)
    return SecretRead(SecretProvenance.VERIFIED_ABSENT)


class TestClassifier:
    def test_the_alpha_403_is_insufficient_scope(self):
        assert classify_calendar_read_error(RuntimeError(GOOGLE_403)) == "insufficient_scope"

    @pytest.mark.parametrize(
        "text,klass",
        [
            ("HttpError 401 invalid credentials", "unauthorized"),
            ("invalid_grant: Token has been expired or revoked", "unauthorized"),
            ("HttpError 404 Not Found", "not_found"),
            ("connection reset by peer", "error"),
        ],
    )
    def test_other_classes(self, text, klass):
        assert classify_calendar_read_error(RuntimeError(text)) == klass

    def test_every_class_has_a_line_and_none_names_a_url(self):
        for klass in ("insufficient_scope", "unauthorized", "not_found", "error"):
            line = calendar_read_failed_line(klass)
            assert line.startswith("I couldn't read your calendar")
            assert "http" not in line and "googleapis" not in line
        assert calendar_read_failed_line(None) == CALENDAR_READ_FAILED_LINES["error"]


def _service() -> IntentService:
    svc = IntentService.__new__(IntentService)
    svc.logger = MagicMock(spec=logging.Logger)
    return svc


def _intent(message: str, action: str) -> Intent:
    return Intent(
        original_message=message,
        category=IntentCategory.QUERY,
        action=action,
        confidence=0.9,
        context={"original_message": message},
    )


def _router(events, last_read_error):
    router = MagicMock()
    router.authenticate = AsyncMock(return_value=True)
    router.get_events_in_range = AsyncMock(return_value=events)
    router.last_read_error = last_read_error
    return router


class TestHandlersTellFailedFromEmpty:
    @pytest.mark.asyncio
    async def test_meeting_time_failed_read_is_not_no_meetings(self):
        with patch(ROUTER, return_value=_router([], "insufficient_scope")):
            out = await _service()._handle_meeting_time_query(
                _intent("what's my agenda today?", "meeting_time"), "wf"
            )
        assert out.message == CALENDAR_READ_FAILED_LINES["insufficient_scope"]
        assert "no meetings" not in out.message.lower()
        assert out.intent_data["calendar_read_error"] == "insufficient_scope"
        assert out.implemented is False

    @pytest.mark.asyncio
    async def test_meeting_time_true_empty_still_says_no_meetings(self):
        with patch(ROUTER, return_value=_router([], None)):
            out = await _service()._handle_meeting_time_query(
                _intent("what's my agenda today?", "meeting_time"), "wf"
            )
        assert out.message == "You have no meetings scheduled for today."

    @pytest.mark.asyncio
    async def test_week_failed_read_is_not_no_events(self):
        with patch(ROUTER, return_value=_router([], "unauthorized")):
            out = await _service()._handle_week_calendar_query(
                _intent("do I have any meetings this week?", "week_calendar"), "wf"
            )
        assert out.message == CALENDAR_READ_FAILED_LINES["unauthorized"]
        assert "didn't find any events" not in out.message


class TestSettingsTestReadsForReal:
    @pytest.mark.asyncio
    async def test_a_scope_refusal_is_a_failed_check(self):
        from web.api.routes import integrations as routes

        keychain = MagicMock()
        keychain.get_api_key.return_value = "refresh-token"
        keychain.aread_secret = AsyncMock(return_value=_secret_read("refresh-token"))
        tokens = MagicMock(access_token="access-token")
        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService", return_value=keychain
            ),
            patch(
                "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler.refresh_access_token",
                new=AsyncMock(return_value=tokens),
            ),
            patch(
                "services.integrations.calendar.oauth_handler.probe_calendar_read",
                new=AsyncMock(return_value="insufficient_scope"),
            ),
        ):
            out = await routes._test_calendar(user_id="u1")
        assert out["success"] is False
        assert out["error_type"] == "insufficient_scope"
        assert "calendar access" in out["error"]

    @pytest.mark.asyncio
    async def test_a_readable_calendar_is_healthy(self):
        from web.api.routes import integrations as routes

        keychain = MagicMock()
        keychain.get_api_key.return_value = "refresh-token"
        keychain.aread_secret = AsyncMock(return_value=_secret_read("refresh-token"))
        tokens = MagicMock(access_token="access-token")
        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService", return_value=keychain
            ),
            patch(
                "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler.refresh_access_token",
                new=AsyncMock(return_value=tokens),
            ),
            patch(
                "services.integrations.calendar.oauth_handler.probe_calendar_read",
                new=AsyncMock(return_value=None),
            ),
        ):
            out = await routes._test_calendar(user_id="u1")
        assert out == {"success": True}
