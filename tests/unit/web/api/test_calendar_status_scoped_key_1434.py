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
    from services.infrastructure.keychain_service import (
        KeychainService,
        SecretProvenance,
        SecretRead,
    )

    validate = AsyncMock(return_value=SimpleNamespace(sub="user-abc"))
    present = SecretRead(SecretProvenance.PRESENT, value="tok")
    with patch.object(JWTService, "validate_token", validate):
        with patch.object(KeychainService, "read_secret", return_value=present) as read:
            result = await get_calendar_status(_request("auth_token=jwt123"))

    validate.assert_awaited_once_with("jwt123")
    read.assert_called_once_with("google_calendar_user-abc")
    assert result["configured"] is True


@pytest.mark.asyncio
async def test_a_store_that_failed_is_status_check_failed_not_not_connected():
    """#2151 (Arch 10-24 12:32): get_api_key returned None for a store failure too."""
    from services.auth.jwt_service import JWTService
    from services.infrastructure.keychain_service import (
        KeychainService,
        SecretProvenance,
        SecretRead,
    )

    validate = AsyncMock(return_value=SimpleNamespace(sub="user-abc"))
    failed = SecretRead(SecretProvenance.STORE_FAILED, error="timeout")
    with patch.object(JWTService, "validate_token", validate):
        with patch.object(KeychainService, "read_secret", return_value=failed):
            result = await get_calendar_status(_request("auth_token=jwt123"))
    assert result == {"configured": False, "message": "Status check failed"}


@pytest.mark.asyncio
async def test_no_token_reads_no_key_at_all():
    """#2151 route group 3 (the #2127 shape): the unscoped "google_calendar" entry is the
    host's. With no signed-in user nothing is read, and even a host entry that exists is
    never reported as this visitor's calendar (was: fell back to the global key)."""
    from services.infrastructure.keychain_service import KeychainService

    with patch.object(KeychainService, "get_api_key", return_value="host-refresh-token") as get_key:
        result = await get_calendar_status(_request(None))

    get_key.assert_not_called()
    assert result == {"configured": False, "message": "Not connected"}
