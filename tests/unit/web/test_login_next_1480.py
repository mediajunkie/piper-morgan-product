"""#1480 — client side of the login round trip must PRESERVE next, safely.

Server side (middleware builds /login?next=… correctly, open-redirect guard)
is pinned in tests/unit/services/auth/test_login_next_redirect_1480.py.
This file pins the surfaces that were DROPPING next:

1. auth.js redirected to '/' unconditionally on successful login — the
   #1466 Slack deep-link (slack_user_id/slack_team_id) died right there.
   It must now read next from the login page's query string, apply the same
   relative-path-only guard as the server (no https://…, no //…, no \\),
   and re-attach the login page's own fragment (fragments survive the 302
   chain in the browser but never reach the server).
2. chat.js's #1520/#840 expiry redirects went to bare "/login" — they must
   carry next so the re-login lands back where the session died.
3. ui.py login_page's already-authenticated redirect went to '/' — it must
   honor a sanitized next.

House discipline: JS has no pytest runtime, so the guard is pinned by source
shape (the exact predicates must exist); the Python route is exercised
directly.
"""

from unittest.mock import MagicMock

import pytest

AUTH_JS = "web/static/js/auth.js"
CHAT_JS = "web/static/js/chat.js"


def _read(path: str) -> str:
    with open(path) as f:
        return f.read()


class TestAuthJsPreservesNext:
    def test_no_unconditional_home_redirect_on_success(self):
        """The #1480 drop point: success handler hardcoded '/'."""
        js = _read(AUTH_JS)
        assert "window.location.href = '/';" not in js, (
            "auth.js still redirects to '/' unconditionally after login — "
            "the deep-link next param is dropped"
        )

    def test_reads_next_from_login_page_query(self):
        js = _read(AUTH_JS)
        assert ".get('next')" in js

    def test_open_redirect_guard_present(self):
        """Relative-path-only guard, mirroring sanitize_next_path:
        https://evil.example fails startsWith('/'); //evil.example is
        protocol-relative; backslash is browser-normalized to slash."""
        js = _read(AUTH_JS)
        assert ".startsWith('/')" in js, "must require a relative path"
        assert ".startsWith('//')" in js, "must refuse protocol-relative URLs"
        assert "\\\\" in js, "must refuse backslash smuggling"

    def test_fragment_reattached_for_deep_link_anchor(self):
        """#link-slack never reaches the server; the login page's own hash
        (carried by the browser across the 302) must ride the final redirect."""
        js = _read(AUTH_JS)
        assert "window.location.hash" in js


class TestChatJsExpiryRedirectsCarryNext:
    def test_no_bare_login_redirects_remain(self):
        js = _read(CHAT_JS)
        assert 'window.location.href = "/login";' not in js, (
            "#1520/#840 expiry redirect still drops the current page"
        )

    def test_expiry_redirect_carries_current_location(self):
        js = _read(CHAT_JS)
        assert '"/login?next=" + encodeURIComponent(' in js


class TestLoginPageHonorsNext:
    """ui.py login_page: already-authenticated visitors with a next param
    must land on next (sanitized), not '/'."""

    def _request(self, next_url=None, user_id="u-42"):
        req = MagicMock()
        req.query_params = {"next": next_url} if next_url is not None else {}
        req.state = MagicMock()
        req.state.user_id = user_id
        return req

    @pytest.mark.asyncio
    async def test_authenticated_with_deep_link_next_lands_on_target(self):
        from web.api.routes.ui import login_page

        target = "/settings/integrations/slack?slack_user_id=U1&slack_team_id=T1"
        response = await login_page(self._request(next_url=target))

        assert response.status_code == 302
        assert response.headers["location"] == target

    @pytest.mark.asyncio
    async def test_authenticated_with_evil_next_lands_home(self):
        from web.api.routes.ui import login_page

        response = await login_page(self._request(next_url="https://evil.example"))

        assert response.status_code == 302
        assert response.headers["location"] == "/"

    @pytest.mark.asyncio
    async def test_authenticated_without_next_lands_home(self):
        from web.api.routes.ui import login_page

        response = await login_page(self._request())

        assert response.status_code == 302
        assert response.headers["location"] == "/"
