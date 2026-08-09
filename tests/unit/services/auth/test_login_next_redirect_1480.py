"""#1480 — Slack deep-link params must survive the unauthenticated login round trip.

The #1466 Slack-side decline links to
/settings/integrations/slack?slack_user_id=U…&slack_team_id=T…#link-slack.
An unauthenticated visit hits AuthMiddleware, which redirects to
/login?next=… — but the next value was built UNENCODED, so the second query
param (slack_team_id) escaped the next value and became a stray param on
/login, and the client dropped next entirely anyway (auth.js redirected to
'/' unconditionally; pinned in tests/unit/web/test_login_next_1480.py).

Contract pinned here (server side):
1. The middleware's /login redirect percent-encodes the FULL original
   path+query into a single `next` param — both slack params survive.
2. The expired-session variant (#1520: token present but expired) carries
   next identically.
3. sanitize_next_path is the open-redirect guard: relative paths only.
   https://evil.example, protocol-relative //evil.example, backslash and
   scheme smuggling are all refused (fall back to '/').

Fragments (#link-slack) never reach the server — the settings page
auto-scrolls when slack params are present (settings_slack.html
initSlackLink), so path+query fidelity is the whole server-side contract.
"""

from unittest.mock import AsyncMock, MagicMock
from urllib.parse import parse_qs, urlsplit

import pytest

from services.auth.auth_middleware import AuthMiddleware, sanitize_next_path
from services.auth.jwt_service import TokenExpired

DEEP_LINK_PATH = "/settings/integrations/slack"
DEEP_LINK_QUERY = "slack_user_id=U123ABC&slack_team_id=T456DEF"


def _mw(claims=None, side_effect=None):
    jwt = MagicMock()
    if side_effect is not None:
        jwt.validate_token = AsyncMock(side_effect=side_effect)
    else:
        jwt.validate_token = AsyncMock(return_value=claims)
    return AuthMiddleware(app=MagicMock(), jwt_service=jwt)


def _request(path=DEEP_LINK_PATH, query=DEEP_LINK_QUERY, cookie=None):
    req = MagicMock()
    req.url.path = path
    req.url.query = query
    req.url.scheme = "https"
    req.headers = {"accept": "text/html,application/xhtml+xml"}
    req.query_params = {}
    req.cookies = {"auth_token": cookie} if cookie else {}
    req.state = MagicMock()
    req.state.user_id = None
    return req


def _next_param(response) -> str:
    """Extract the parsed `next` value from a redirect's Location header."""
    location = response.headers["location"]
    split = urlsplit(location)
    assert split.path == "/login", f"expected /login redirect, got {location}"
    params = parse_qs(split.query)
    assert list(params.keys()) == ["next"], (
        f"next must be the ONLY query param on /login — leaked params mean the "
        f"original query was not encoded into next: {location}"
    )
    return params["next"][0]


class TestMiddlewareNextCarriesDeepLink:
    @pytest.mark.asyncio
    async def test_unauthenticated_deep_link_visit_encodes_full_url_into_next(self):
        """No token at all → /login redirect whose next holds path AND both
        slack params. Before #1480 the unencoded '&' split slack_team_id out
        of next into a stray /login param (data loss)."""
        mw = _mw()
        req = _request(cookie=None)
        call_next = AsyncMock()

        response = await mw.dispatch(req, call_next)

        assert response.status_code == 302
        assert _next_param(response) == f"{DEEP_LINK_PATH}?{DEEP_LINK_QUERY}"
        call_next.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_expired_session_deep_link_visit_carries_next(self):
        """#1520 companion: token PRESENT but expired → same next contract."""
        mw = _mw(side_effect=TokenExpired("expired"))
        req = _request(cookie="expired.jwt.token")
        call_next = AsyncMock()

        response = await mw.dispatch(req, call_next)

        assert response.status_code == 302
        assert _next_param(response) == f"{DEEP_LINK_PATH}?{DEEP_LINK_QUERY}"
        call_next.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_plain_path_without_query_still_redirects(self):
        mw = _mw()
        req = _request(path="/settings", query="", cookie=None)

        response = await mw.dispatch(req, AsyncMock())

        assert response.status_code == 302
        assert _next_param(response) == "/settings"


class TestSanitizeNextPathOpenRedirectGuard:
    """Relative paths only — everything else falls back to '/'."""

    def test_accepts_deep_link_path_with_query(self):
        url = f"{DEEP_LINK_PATH}?{DEEP_LINK_QUERY}"
        assert sanitize_next_path(url) == url

    def test_refuses_absolute_external_url(self):
        assert sanitize_next_path("https://evil.example") == "/"
        assert sanitize_next_path("https://evil.example/settings") == "/"

    def test_refuses_protocol_relative_url(self):
        assert sanitize_next_path("//evil.example") == "/"
        assert sanitize_next_path("//evil.example/settings") == "/"

    def test_refuses_backslash_smuggling(self):
        # Browsers normalize backslashes to slashes: /\evil.example acts
        # like //evil.example.
        assert sanitize_next_path("/\\evil.example") == "/"
        assert sanitize_next_path("\\\\evil.example") == "/"

    def test_refuses_scheme_urls(self):
        assert sanitize_next_path("javascript:alert(1)") == "/"
        assert sanitize_next_path("http://evil.example") == "/"

    def test_refuses_non_relative_garbage(self):
        assert sanitize_next_path("") == "/"
        assert sanitize_next_path(None) == "/"
        assert sanitize_next_path("settings/integrations") == "/"

    def test_refuses_control_characters(self):
        assert sanitize_next_path("/settings\r\nSet-Cookie: x=y") == "/"

    def test_refuses_auth_flow_loops(self):
        # next pointing back at the auth flow would loop (or dead-end on the
        # route-less GET /logout the SessionTimeout default still points at).
        assert sanitize_next_path("/login") == "/"
        assert sanitize_next_path("/login?next=/x") == "/"
        assert sanitize_next_path("/logout") == "/"

    def test_preserves_nested_query_and_encoded_chars(self):
        url = "/settings/integrations/slack?slack_user_id=U%2B1&slack_team_id=T1"
        assert sanitize_next_path(url) == url
