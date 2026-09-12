"""#1740 — the divergent renderer twin `web/bot-message-renderer.js` is gone.

Two copies of the bot message renderer existed and had diverged:
`web/assets/bot-message-renderer.js` (LIVE — served at /assets/, loaded by
app_shell since #1732; carries the #1123 link renderer + the Phase 3/4
suggestions UI with the #1741 escaping) and a legacy CommonJS twin at
`web/bot-message-renderer.js` that no mount served (web/app.py mounts only
web/assets and web/static). The twin was a drift trap: #1732 had to patch and
pin BOTH copies to keep the sanitizer from diverging. Fix: the twin is
deleted; this file pins its absence so it cannot silently come back.

LAYER (m-43, named honestly): the serving tests drive the REAL ASGI app
(`from web.app import app`) through a real TestClient — the real StaticFiles
mounts answering for /assets/* and /static/*, the real AuthMiddleware (real
JWT crypto via the same AuthContainer JWTService instance the app registered)
answering for the unmounted root path. Observed reality pinned as observed:
the root path unauthenticated is 401 (AuthMiddleware fires before routing —
proving only that nothing serves it PUBLICLY), so the absence claim proper is
made with a real authenticated cookie, where the answer is 404 (no route, no
mount). One on-disk pin rides along as the anti-resurrection guard — named
for what it is: a filesystem check, not a serving check.

Denominator (m-44): this file covers the #1740 renderer twin only. The
sanitizer behaviour of the surviving copy is pinned elsewhere
(tests/frontend/unit/chat-render-xss-1732.test.js — jsdom exploit suite;
tests/unit/templates/test_chat_render_assets_1732.py — source + template
pins).
"""

import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from web.app import app

REPO = Path(__file__).resolve().parents[3]

TWIN_ROOT_PATH = "/bot-message-renderer.js"
TWIN_ALIAS_PATHS = [
    "/static/bot-message-renderer.js",
    "/static/js/bot-message-renderer.js",
]
LIVE_ASSET_PATH = "/assets/bot-message-renderer.js"


@pytest.fixture(scope="module")
def client():
    return TestClient(app, follow_redirects=False)


def _auth_cookie() -> str:
    """A real token signed by the SAME JWTService instance the app's
    AuthMiddleware validates with (AuthContainer is a singleton provider) —
    real crypto, not a mocked request.state (the #1480/#1640 lesson)."""
    return AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(),
        user_email="u1740@example.com",
        scopes=["user"],
    )


class TestTwinIsNotServed:
    def test_root_path_404s_even_authenticated(self, client):
        """THE absence pin: with a valid auth cookie (so AuthMiddleware's 401
        can't mask routing) the root path has no route and no mount — 404."""
        client.cookies.set("auth_token", _auth_cookie())
        try:
            r = client.get(TWIN_ROOT_PATH)
        finally:
            client.cookies.delete("auth_token")
        assert r.status_code == 404, (
            f"{TWIN_ROOT_PATH} returned {r.status_code} authenticated; "
            "nothing may serve the deleted renderer twin (#1740)"
        )

    def test_root_path_not_public(self, client):
        """Unauthenticated, AuthMiddleware answers 401 before routing — pinned
        as observed so a future auth-exemption of this path (which would
        change this to the mount's answer) surfaces here."""
        r = client.get(TWIN_ROOT_PATH)
        assert r.status_code == 401, (
            f"{TWIN_ROOT_PATH} returned {r.status_code} unauthenticated; "
            "expected 401 (not auth-exempt, and certainly not the file)"
        )

    @pytest.mark.parametrize("alias", TWIN_ALIAS_PATHS)
    def test_static_aliases_404(self, client, alias):
        """The auth-exempt /static mount never held the renderer — the
        plausible alias paths answer 404, not a resurrected copy."""
        r = client.get(alias)
        assert r.status_code == 404, (
            f"{alias} returned {r.status_code}; no static alias may serve "
            "the deleted renderer twin (#1740)"
        )

    def test_twin_file_gone_from_disk(self):
        """Anti-resurrection guard (filesystem layer, named honestly): the
        twin path must not exist in the repo — a re-added copy would drift
        from the served one exactly as before (#1740's whole defect)."""
        assert not (REPO / "web" / "bot-message-renderer.js").exists(), (
            "web/bot-message-renderer.js exists again — the #1740 drift trap "
            "is back; the ONLY renderer copy is web/assets/"
        )


class TestLiveRendererStillServes:
    def test_assets_copy_serves_with_sanitizer(self, client):
        """Guard: the fix removed the twin, not the live renderer — the
        /assets copy (loaded by app_shell) still serves and still carries the
        #1732 sanitizer chokepoint."""
        r = client.get(LIVE_ASSET_PATH)
        assert r.status_code == 200, (
            f"{LIVE_ASSET_PATH} returned {r.status_code}; the live renderer "
            "must survive the twin removal"
        )
        assert (
            "_sanitizeRenderedHtml" in r.text
        ), "served renderer no longer carries the #1732 sanitizer chokepoint"
