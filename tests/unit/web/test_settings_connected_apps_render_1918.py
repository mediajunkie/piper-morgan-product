"""#1918 — the /settings/connected-apps page actually renders, auth-gated,
with the card/page markers the CXO design spec names, and the Settings index
links to it. This is the render-layer pin (m-43: a curl 200 is not a render
test) for the UI half of #1918 — the backend list/revoke routes are already
covered by tests/unit/web/api/routes/test_mcp_connections_1918.py.

LAYER (m-43): every test drives the REAL ASGI app (`from web.app import
app`) through a real TestClient — real AuthMiddleware, real JWT crypto, the
real `/settings/connected-apps` and `/settings` routes, and the real
`templates/` directory on disk. Mirrors
tests/unit/web/test_settings_preferences_render_1876.py's idiom exactly
(same named-stub-templates fixture, same auth-cookie helper).

DENOMINATOR: this file covers the page's auth gate, its rendered markers for
each spec §2c state container, and the Settings index card link. It does
NOT cover the page's client-side JS fetch/revoke behavior (would need a real
browser) or the backend routes themselves (separate file, above).
"""

from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from web.app import app

PAGE_PATH = "/settings/connected-apps"
INDEX_PATH = "/settings"


@pytest.fixture(scope="module")
def client():
    if getattr(app.state, "templates", None) is None:
        from pathlib import Path

        from fastapi.templating import Jinja2Templates

        repo_root = Path(__file__).resolve().parents[3]
        app.state.templates = Jinja2Templates(directory=str(repo_root / "templates"))
    return TestClient(app, follow_redirects=False)


def _auth_cookie() -> str:
    """A real token signed by the SAME JWTService instance the app's
    AuthMiddleware validates with (AuthContainer is a singleton provider)."""
    return AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(),
        user_email="u1918@example.com",
        scopes=["user"],
    )


class TestPageIsAuthGated:
    def test_unauthenticated_get_is_401(self, client):
        r = client.get(PAGE_PATH)
        assert r.status_code == 401, f"{PAGE_PATH} returned {r.status_code} unauthenticated"


class TestPageRendersTheStatesAndCopy:
    def test_authenticated_get_renders_200_with_state_containers(self, client):
        client.cookies.set("auth_token", _auth_cookie())
        try:
            r = client.get(PAGE_PATH)
        finally:
            client.cookies.delete("auth_token")
        assert r.status_code == 200, f"{PAGE_PATH} returned {r.status_code}: {r.text[:300]}"
        body = r.text
        assert "Connected apps" in body
        # Spec §2c's three states must all be present as containers the
        # page's own JS toggles (loading / empty / populated).
        assert 'id="connected-apps-loading"' in body
        assert "Loading your connected apps" in body
        assert 'id="connected-apps-empty"' in body
        assert "No apps connected yet." in body
        assert 'id="connected-apps-content"' in body
        assert 'id="active-connections-list"' in body
        assert 'id="revoked-disclosure"' in body
        assert 'id="manual-tokens-section"' in body

    def test_page_calls_the_real_backend_endpoints(self, client):
        client.cookies.set("auth_token", _auth_cookie())
        try:
            body = client.get(PAGE_PATH).text
        finally:
            client.cookies.delete("auth_token")
        assert (
            "/api/v1/settings/mcp-connections" in body
        ), "the rendered page does not call the #1918 list endpoint"
        assert "/revoke" in body, "the rendered page has no revoke call wired up"

    def test_intro_copy_names_how_a_connection_gets_here(self, client):
        """Spec §2b: the first-view-alarm fix — name the mechanism."""
        client.cookies.set("auth_token", _auth_cookie())
        try:
            body = client.get(PAGE_PATH).text
        finally:
            client.cookies.delete("auth_token")
        normalized = " ".join(body.split())
        assert "once you approve them on their consent screen" in normalized


class TestSettingsIndexLinksToIt:
    def test_index_page_has_a_connected_apps_card(self, client):
        client.cookies.set("auth_token", _auth_cookie())
        try:
            r = client.get(INDEX_PATH)
        finally:
            client.cookies.delete("auth_token")
        assert r.status_code == 200, f"{INDEX_PATH} returned {r.status_code}"
        body = r.text
        assert (
            'href="/settings/connected-apps"' in body
        ), "the Settings index has no link to the new Connected apps page"
        assert "Connected apps" in body
