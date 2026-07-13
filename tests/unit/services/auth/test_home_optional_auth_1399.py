"""#1399/login-regression — "/" is OPTIONAL-auth, not exempt.

The 2026-07-12 chain: #1399's first cut made "/" fully exempt to fix the
fresh-visitor 401. That skipped token extraction entirely, so a logged-in
user's cookie was never read on "/" → the home route saw no user_id →
redirected them back to /login → "pulse and stay" (found live by PM's
Scenario A login the same evening).

Contract pinned: on "/", a valid cookie POPULATES request.state.user_id
(authenticated user sees the app); a missing/invalid cookie falls through
with NO user_id and NO 401 (fresh visitor reaches the home route's smart
redirect → /login).
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.auth.auth_middleware import AuthMiddleware


def _mw(claims=None, raises=False):
    jwt = MagicMock()
    if raises:
        jwt.validate_token = AsyncMock(side_effect=RuntimeError("bad token"))
    else:
        jwt.validate_token = AsyncMock(return_value=claims)
    return AuthMiddleware(app=MagicMock(), jwt_service=jwt)


def _request(path="/", cookie=None):
    req = MagicMock()
    req.url.path = path
    req.url.scheme = "https"
    req.headers = {}
    req.query_params = {}
    req.cookies = {"auth_token": cookie} if cookie else {}
    req.state = MagicMock()
    req.state.user_id = None
    return req


@pytest.mark.asyncio
async def test_valid_cookie_on_root_populates_user_id():
    claims = MagicMock(user_id="u-42", scopes=["user"])
    mw = _mw(claims=claims)
    req = _request("/", cookie="valid.jwt.token")
    call_next = AsyncMock(return_value="HOME")

    result = await mw.dispatch(req, call_next)

    assert result == "HOME"
    assert req.state.user_id == "u-42"
    call_next.assert_awaited_once_with(req)


@pytest.mark.asyncio
async def test_no_cookie_on_root_falls_through_without_401():
    mw = _mw(claims=None)
    req = _request("/", cookie=None)
    call_next = AsyncMock(return_value="HOME")

    result = await mw.dispatch(req, call_next)

    assert result == "HOME"  # reached the route, NOT a 401 — the #390 redirect runs
    assert req.state.user_id is None
    call_next.assert_awaited_once()


@pytest.mark.asyncio
async def test_invalid_cookie_on_root_treated_as_anonymous_no_401():
    mw = _mw(raises=True)
    req = _request("/", cookie="expired.or.garbage")
    call_next = AsyncMock(return_value="HOME")

    result = await mw.dispatch(req, call_next)

    assert result == "HOME"
    assert req.state.user_id is None
    call_next.assert_awaited_once()
