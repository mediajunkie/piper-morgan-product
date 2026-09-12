"""#1733 — stale, unauthenticated duplicate of the personality-preferences page.

`web/assets/personality-preferences.html` was a pre-auth-model (2026-02-05,
33e22edae) copy of the personality-preferences UI, publicly served verbatim at
`/assets/personality-preferences.html` because the whole `/assets` StaticFiles
mount (web/app.py) rides the `EXEMPT_STATIC_ASSET_PATHS` auth exemption — an
exemption whose own comment says "CSS/JS/images don't have user-bound
responses." The HTML twin rode along on that rationale while hardcoding
`user_id: "default"` in its fetch calls. Fix: the file is deleted; the real
route `/personality-preferences` (auth-gated, linked from Settings) is the
only surface.

LAYER (m-43, named honestly): every test here drives the REAL ASGI app
(`from web.app import app`) through a real TestClient — the real StaticFiles
mount answering for `/assets/*`, the real AuthMiddleware (real JWT crypto via
the same AuthContainer JWTService instance the app registered) answering for
`/personality-preferences`. No route-table introspection standing in for
requests, no on-disk existence check standing in for the mount's answer.
Stubbed boundaries: exactly one — the app's startup lifespan does not run
under a bare TestClient, so the fixture below seeds `app.state.templates`
with the same real Jinja2Templates(templates/) that web/startup.py:251-252
builds (startup wiring, outside the layer under test; the render itself is
the real template through the real route). Repo-level conftest fixtures
apply as for every real-app test.

Denominator (m-44): this file covers the personality-preferences twin named
by #1733 only. The sibling stale twin `web/assets/standup.html` is the same
exposure class and is tracked separately (#1499 sweep item 6 / follow-up
issue filed from the #1733 session).
"""

import uuid

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from web.app import app

STALE_PATH = "/assets/personality-preferences.html"
CANONICAL_PATH = "/personality-preferences"
LIVE_ASSET_GUARD = "/assets/bot-message-renderer.js"


@pytest.fixture(scope="module")
def client():
    # Bare TestClient (no `with`) skips the startup lifespan, so seed the one
    # piece of startup wiring the canonical route needs — the SAME construction
    # web/startup.py:251-252 performs against the real templates/ directory.
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
        user_email="u1733@example.com",
        scopes=["user"],
    )


class TestStaleStaticTwinIsGone:
    def test_stale_static_page_404s(self, client):
        """The stale public twin no longer exists: the auth-exempt /assets
        mount answers 404, not the pre-auth-model page (was 200)."""
        r = client.get(STALE_PATH)
        assert r.status_code == 404, (
            f"{STALE_PATH} returned {r.status_code}; the stale unauthenticated "
            "twin must be gone from the public /assets mount (#1733)"
        )

    def test_assets_mount_itself_still_serves(self, client):
        """Guard: the fix removed one file, not the /assets mount — live JS
        assets (loaded by shipped templates) must keep serving."""
        r = client.get(LIVE_ASSET_GUARD)
        assert r.status_code == 200, (
            f"{LIVE_ASSET_GUARD} returned {r.status_code}; the /assets mount "
            "must survive the stale-page removal"
        )


class TestCanonicalSurfaceIntact:
    def test_canonical_route_still_mounted_and_gated(self, client):
        """Unauthenticated GET of the real route is 401 — which pins BOTH
        halves: the route is still mounted (an unmounted route would 404)
        and it is still auth-gated (the stale twin's whole defect)."""
        r = client.get(CANONICAL_PATH)
        assert r.status_code == 401, (
            f"{CANONICAL_PATH} returned {r.status_code} unauthenticated; "
            "expected 401 (mounted + gated)"
        )

    def test_canonical_route_serves_authenticated(self, client):
        """With a real auth cookie the canonical page actually renders the
        feature the stale twin served — content-level parity anchor
        (the four preference sections' flagship control)."""
        client.cookies.set("auth_token", _auth_cookie())
        try:
            r = client.get(CANONICAL_PATH)
        finally:
            client.cookies.delete("auth_token")
        assert (
            r.status_code == 200
        ), f"{CANONICAL_PATH} returned {r.status_code} with a valid cookie"
        body = r.text
        for anchor in (
            "Warmth Level",
            "Confidence Display Style",
            "Action Orientation",
            "Technical Depth",
        ):
            assert anchor in body, (
                f"canonical page no longer renders section {anchor!r} — "
                "parity with the removed twin broken"
            )
