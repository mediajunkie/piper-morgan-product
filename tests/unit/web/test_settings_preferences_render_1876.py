"""#1876 — the /settings/preferences page actually renders, auth-gated, with
the timezone control and the Preferences card linking to it from the
Settings index.

Before this issue, UserPreferenceManager.set_reminder_timezone had ZERO
callers: no Settings page existed at all. This is the render-layer pin (m-43:
a curl 200 is not a render test) proving the real page — through the real
route, the real Jinja2Templates, the real auth-gated app — actually contains
the control, not just that the route answers something.

LAYER (m-43): every test drives the REAL ASGI app (`from web.app import
app`) through a real TestClient — real AuthMiddleware, real JWT crypto
(tokens signed by the same AuthContainer JWTService singleton the middleware
validates with), the real `/settings/preferences` and `/settings` routes,
and the real `templates/` directory on disk. Named stub, exactly one (the
same one #1733/#1751 use): the bare TestClient skips the startup lifespan, so
`app.state.templates` is seeded the way `web/startup.py` builds it, only if
not already present.

DENOMINATOR: this file covers `/settings/preferences`'s auth gate + rendered
content, and `/settings`'s Preferences card link. It does NOT cover the
page's client-side JS behavior (fetch/save/nudge) — that would need a real
browser; the JS is inline in the template and reviewed by reading, not
executed here.
"""

from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from web.app import app

PAGE_PATH = "/settings/preferences"
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
    AuthMiddleware validates with (AuthContainer is a singleton provider) —
    real crypto, not a mocked request.state (the #1480/#1640 lesson)."""
    return AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(),
        user_email="u1876@example.com",
        scopes=["user"],
    )


class TestPageIsAuthGated:
    def test_unauthenticated_get_is_401(self, client):
        r = client.get(PAGE_PATH)
        assert r.status_code == 401, f"{PAGE_PATH} returned {r.status_code} unauthenticated"


class TestPageRendersTheControl:
    def test_authenticated_get_renders_timezone_select_and_save(self, client):
        client.cookies.set("auth_token", _auth_cookie())
        try:
            r = client.get(PAGE_PATH)
        finally:
            client.cookies.delete("auth_token")
        assert r.status_code == 200, f"{PAGE_PATH} returned {r.status_code}: {r.text[:300]}"
        body = r.text
        assert 'id="prefs-timezone"' in body, "timezone <select> missing from the rendered page"
        assert 'id="prefs-timezone-save"' in body, "save button missing from the rendered page"
        # The select must actually be populated server-side, not empty.
        assert "America/Los_Angeles" in body
        assert "Europe/Helsinki" in body

    def test_page_calls_the_real_timezone_api(self, client):
        client.cookies.set("auth_token", _auth_cookie())
        try:
            body = client.get(PAGE_PATH).text
        finally:
            client.cookies.delete("auth_token")
        assert "/api/v1/preferences/timezone" in body, (
            "the rendered page does not call the #1876 timezone API — the "
            "select-and-save control would have nothing to save to"
        )

    def test_nudge_is_present_but_hidden_by_default(self, client):
        client.cookies.set("auth_token", _auth_cookie())
        try:
            body = client.get(PAGE_PATH).text
        finally:
            client.cookies.delete("auth_token")
        assert 'id="prefs-nudge"' in body
        assert "prefs-nudge-apply" in body
        assert 'class="prefs-nudge visible"' not in body, (
            "the browser-zone nudge must not render visible by default — it "
            "is shown only client-side when the stored zone is still the "
            "default AND the browser's own zone differs (never auto-applied)"
        )


class TestSettingsIndexLinksToIt:
    def test_index_page_has_a_preferences_card(self, client):
        client.cookies.set("auth_token", _auth_cookie())
        try:
            r = client.get(INDEX_PATH)
        finally:
            client.cookies.delete("auth_token")
        assert r.status_code == 200, f"{INDEX_PATH} returned {r.status_code}"
        body = r.text
        assert (
            'href="/settings/preferences"' in body
        ), "the Settings index has no link to the new Preferences page"
