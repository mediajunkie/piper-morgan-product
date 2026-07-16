"""#1434: /setup calendar-status must actually authenticate before key selection.

Regression: ``jwt_service.validate_token(token)`` is async and was called without
``await`` — the truthy coroutine made ``claims.sub`` raise, the broad except
swallowed it, and EVERY request (authenticated or not) silently fell back to the
non-scoped ``google_calendar`` key (census B1, sprint #1424; #1419 family — the
fallback is a global credential).

These tests call the route function directly with a fake Request and pin both
branches: a valid token selects the user-scoped key; no token keeps the
anonymous global fallback.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from starlette.requests import Request

from web.api.routes.setup import get_calendar_status


def _request(cookie: str | None) -> Request:
    headers = [(b"cookie", cookie.encode())] if cookie else []
    return Request({"type": "http", "headers": headers, "method": "GET", "path": "/"})


@pytest.mark.asyncio
async def test_valid_token_selects_user_scoped_key():
    from services.auth.jwt_service import JWTService
    from services.infrastructure.keychain_service import KeychainService

    validate = AsyncMock(return_value=SimpleNamespace(sub="user-abc"))
    with patch.object(JWTService, "validate_token", validate):
        with patch.object(KeychainService, "get_api_key", return_value="tok") as get_key:
            result = await get_calendar_status(_request("auth_token=jwt123"))

    validate.assert_awaited_once_with("jwt123")
    get_key.assert_called_once_with("google_calendar_user-abc")
    assert result["configured"] is True


@pytest.mark.asyncio
async def test_no_token_falls_back_to_global_key():
    from services.infrastructure.keychain_service import KeychainService

    with patch.object(KeychainService, "get_api_key", return_value=None) as get_key:
        result = await get_calendar_status(_request(None))

    get_key.assert_called_once_with("google_calendar")
    assert result["configured"] is False
