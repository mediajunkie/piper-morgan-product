"""A Google 403 "accessNotConfigured" (the Calendar API not enabled for the app's
project) is its own class, said as a setup step on our side, and the Settings
probe logs the class (never the text or the token).

2026-10-21: xian's connect on the "Piper Morgan (Alpha)" project passed consent and
the first read came back "Google refused the calendar read (error)", with no server
line to read.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.integrations.calendar.read_errors import classify_calendar_read_error
from services.intent.intent_service import calendar_read_failed_line


def _secret_read(value):
    """#2151: the provenance read the calendar Test makes (``aread_secret``), mirroring a
    mocked ``get_api_key`` value: present when set, verified absent when None."""
    from services.infrastructure.keychain_service import SecretProvenance, SecretRead

    if value:
        return SecretRead(SecretProvenance.PRESENT, value=value)
    return SecretRead(SecretProvenance.VERIFIED_ABSENT)


class _HttpError(Exception):
    pass


ACCESS_NOT_CONFIGURED = _HttpError(
    "<HttpError 403 when requesting https://www.googleapis.com/calendar/v3/calendars/primary/events "
    'returned "Google Calendar API has not been used in project 43539582958 before or it is '
    "disabled. Enable it by visiting https://console.developers.google.com/apis/api/"
    'calendar-json.googleapis.com/overview?project=43539582958 then retry." '
    'Details: [{"reason": "accessNotConfigured"}]>'
)


def test_access_not_configured_is_its_own_class():
    assert classify_calendar_read_error(ACCESS_NOT_CONFIGURED) == "api_not_enabled"


def test_the_other_classes_are_unchanged():
    assert (
        classify_calendar_read_error(
            _HttpError("403 Request had insufficient authentication scopes")
        )
        == "insufficient_scope"
    )
    assert classify_calendar_read_error(_HttpError("401 invalid_grant")) == "unauthorized"
    assert classify_calendar_read_error(_HttpError("404 Not Found")) == "not_found"
    assert classify_calendar_read_error(_HttpError("something else")) == "error"


def test_the_chat_line_names_a_setup_step_on_our_side():
    """CXO's words (10-21 10:21): say only what the class proves, and that
    reconnecting won't fix it (the sentence the old catch-all got wrong)."""
    line = calendar_read_failed_line("api_not_enabled")
    assert line == (
        "I couldn't read your calendar. Google refused the request because the Calendar "
        "service isn't switched on for this app yet. That's a setup step on our side, and "
        "reconnecting won't fix it."
    )
    assert "API" not in line


async def _settings_test_with_read_error(read_error):
    from unittest.mock import AsyncMock, MagicMock, patch

    from web.api.routes.integrations import _test_calendar

    keychain = MagicMock()
    keychain.get_api_key.return_value = "valid_refresh_token"
    keychain.aread_secret = AsyncMock(return_value=_secret_read("valid_refresh_token"))
    handler = MagicMock()
    handler.refresh_access_token = AsyncMock(return_value=MagicMock(access_token="tok"))
    with (
        patch(
            "services.integrations.calendar.oauth_handler.probe_calendar_read",
            new=AsyncMock(return_value=read_error),
        ),
        patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=keychain,
        ),
        patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler",
            return_value=handler,
        ),
    ):
        return await _test_calendar()


@pytest.mark.asyncio
async def test_settings_test_says_the_service_is_off_and_reconnecting_wont_help():
    result = await _settings_test_with_read_error("api_not_enabled")
    assert result["success"] is False
    assert result["error_type"] == "api_not_enabled"
    assert result["error"] == (
        "Google refused the calendar read: the Calendar service isn't switched on "
        "for this app yet. That's a setup step on our side. Reconnecting won't help."
    )


@pytest.mark.asyncio
async def test_settings_test_catch_all_does_not_promise_that_reconnecting_fixes_it():
    """CXO: "(error)" tells the user nothing, and "Reconnect and try again" is a
    promise the product can't back when the cause is ours."""
    result = await _settings_test_with_read_error("error")
    assert result["success"] is False
    assert result["error_type"] == "error"
    assert result["error"] == (
        "Google refused the calendar read, and I couldn't tell why. "
        "Reconnecting may help. If it doesn't, tell us."
    )
    assert "(error)" not in result["error"]
    assert "Reconnect and try again" not in result["error"]


@pytest.mark.asyncio
async def test_settings_test_keeps_the_known_classes_on_their_lines():
    """CXO: only the catch-all and the new class change."""
    result = await _settings_test_with_read_error("unauthorized")
    assert result["error_type"] == "unauthorized"
    assert result["error"] == (
        "Google refused the calendar read (unauthorized). Reconnect and try again."
    )


@pytest.mark.asyncio
async def test_the_settings_probe_logs_the_class_not_the_text():
    """Exec's ask (10-21): the server log for the read. The probe now logs the class
    and the exception type; never the text (ids, URLs) and never the token."""
    from services.integrations.calendar import oauth_handler

    async def _raise(fn, *a, **k):
        raise ACCESS_NOT_CONFIGURED

    with (
        patch.object(oauth_handler, "logger") as log,
        patch("asyncio.to_thread", new=_raise),
    ):
        result = await oauth_handler.probe_calendar_read("ya29.not-a-real-token")
    assert result == "api_not_enabled"
    log.warning.assert_called_once()
    args, kwargs = log.warning.call_args
    assert args[0] == "calendar_read_probe_failed"
    assert kwargs["error_class"] == "api_not_enabled"
    assert kwargs["exception_type"] == "_HttpError"
    assert "ya29" not in str(kwargs) and "43539582958" not in str(kwargs)
