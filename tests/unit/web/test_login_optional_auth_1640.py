"""#1640 — /login is OPTIONAL-auth, so the #1480 already-authenticated
next-bounce is actually reachable.

LAYER (m-43 — name the layer, because the wrong layer is this bug's whole
story): these tests drive the REAL AuthMiddleware and the REAL login_page
route wired together through a real ASGI TestClient, with REAL JWT crypto
(a real JWTService signs and validates the cookie). request.state is never
mocked — tests/unit/web/test_login_next_1480.py mocked
`req.state.user_id` directly, which verified the bounce branch's logic
while the middleware exclusion one layer up kept the branch unreachable
for two months (#1597 live finding, 2026-08-16).

Stubbed boundaries (each outside the layer under test):
  - the users-count DB query (session_scope_fresh patched to report one
    user, so the unauthenticated path shows the form, not /setup)
  - nothing else: the login form is the REAL templates/login.html render.

Issues: #1640 (fix), #1480 (bounce surface), #1597 (live finding).
"""

import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from urllib.parse import quote

import pytest
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.testclient import TestClient

from services.auth.auth_middleware import (
    DEFAULT_EXCLUDE_PATHS,
    OPTIONAL_AUTH_UI_PATHS,
    AuthMiddleware,
)
from services.auth.jwt_service import JWTService
from web.api.routes.ui import login_page

REPO_ROOT = Path(__file__).resolve().parents[3]
DEEP_LINK = "/settings/integrations/slack?slack_user_id=U1640&slack_team_id=T1640"

# Real crypto: this service signs the cookie AND is the instance the
# middleware validates with — no mocked validate_token.
_JWT = JWTService(secret_key="unit-test-secret-for-1640-32byte")


def _auth_cookie(jwt_service: JWTService = _JWT) -> str:
    return jwt_service.generate_access_token(
        user_id=uuid.uuid4(),
        user_email="u1640@example.com",
        scopes=["user"],
    )


def _make_app() -> FastAPI:
    app = FastAPI()
    app.add_middleware(AuthMiddleware, jwt_service=_JWT)
    app.add_api_route("/login", login_page, response_class=HTMLResponse)
    # Same template the production startup phase mounts (repo-root templates/).
    app.state.templates = Jinja2Templates(directory=str(REPO_ROOT / "templates"))
    return app


@pytest.fixture
def client(monkeypatch):
    """Real middleware + real route + real template; only the DB stubbed."""
    from services.database.session_factory import AsyncSessionFactory

    @asynccontextmanager
    async def _fake_scope():
        result = MagicMock()
        result.scalar_one.return_value = 1  # users exist → no /setup redirect
        session = MagicMock()
        session.execute = AsyncMock(return_value=result)
        yield session

    monkeypatch.setattr(AsyncSessionFactory, "session_scope_fresh", _fake_scope)
    return TestClient(_make_app(), follow_redirects=False)


HTML = {"accept": "text/html"}


class TestAuthenticatedBounce:
    """The #1480 surface #1640 made reachable."""

    def test_authenticated_next_bounces_to_target(self, client):
        client.cookies.set("auth_token", _auth_cookie())
        resp = client.get(f"/login?next={quote(DEEP_LINK, safe='')}", headers=HTML)
        assert resp.status_code == 302, resp.text[:300]
        assert resp.headers["location"] == DEEP_LINK

    def test_authenticated_without_next_bounces_to_app_default(self, client):
        client.cookies.set("auth_token", _auth_cookie())
        resp = client.get("/login", headers=HTML)
        assert resp.status_code == 302, resp.text[:300]
        assert resp.headers["location"] == "/"


class TestUnauthenticatedUnchanged:
    """/login must never BLOCK — the other half of optional-auth."""

    def test_no_cookie_shows_form_200(self, client):
        resp = client.get(f"/login?next={quote(DEEP_LINK, safe='')}", headers=HTML)
        assert resp.status_code == 200, resp.text[:300]
        assert "login" in resp.text.lower()

    def test_invalid_cookie_shows_form_200_no_error(self, client):
        client.cookies.set("auth_token", "garbage.not.a.jwt")
        resp = client.get("/login", headers=HTML)
        assert resp.status_code == 200, resp.text[:300]
        assert "login" in resp.text.lower()

    def test_expired_cookie_shows_form_200_no_error(self, client):
        # Signed with the SAME key, already expired — the realistic
        # stale-session case, distinct from garbage bytes.
        expired_minter = JWTService(
            secret_key="unit-test-secret-for-1640-32byte",
            access_token_expire_minutes=-5,
        )
        client.cookies.set("auth_token", _auth_cookie(expired_minter))
        resp = client.get("/login", headers=HTML)
        assert resp.status_code == 200, resp.text[:300]
        assert "login" in resp.text.lower()


class TestOpenRedirectGuardOnTheBounce:
    """sanitize_next_path applies to the now-live redirect (pinned at the
    same real layer, not just on the pure function)."""

    @pytest.mark.parametrize(
        "evil",
        [
            "https://evil.example/x",  # absolute external URL
            "//evil.example/x",  # protocol-relative
            "/\\evil",  # backslash smuggling
            "/login",  # auth-flow loop
        ],
    )
    def test_hostile_next_falls_back_to_app_default(self, client, evil):
        client.cookies.set("auth_token", _auth_cookie())
        resp = client.get(f"/login?next={quote(evil, safe='')}", headers=HTML)
        assert resp.status_code == 302, resp.text[:300]
        assert resp.headers["location"] == "/", (
            f"open redirect: next={evil!r} produced " f"Location {resp.headers['location']!r}"
        )


class TestMechanismPins:
    """Structural pins on HOW /login gets its state populated."""

    def test_login_is_optional_auth_not_excluded(self):
        assert "/login" in OPTIONAL_AUTH_UI_PATHS
        assert "/login" not in DEFAULT_EXCLUDE_PATHS, (
            "#1640: /login in the exclude list is exactly what made the "
            "#1480 bounce unreachable (dispatch skipped the cookie parse). "
            "It belongs in OPTIONAL_AUTH_UI_PATHS only."
        )

    def test_optional_auth_wins_even_if_reexcluded(self, monkeypatch):
        """Defense pinned: the optional-auth branch runs BEFORE the exclude
        check, so even a middleware constructed with /login in
        exclude_paths still parses the cookie (the #1640 regression shape
        can't come back via exclude-list drift)."""
        from services.database.session_factory import AsyncSessionFactory

        @asynccontextmanager
        async def _fake_scope():
            result = MagicMock()
            result.scalar_one.return_value = 1
            session = MagicMock()
            session.execute = AsyncMock(return_value=result)
            yield session

        monkeypatch.setattr(AsyncSessionFactory, "session_scope_fresh", _fake_scope)

        app = FastAPI()
        app.add_middleware(
            AuthMiddleware,
            jwt_service=_JWT,
            exclude_paths=["/login", *DEFAULT_EXCLUDE_PATHS],
        )
        app.add_api_route("/login", login_page, response_class=HTMLResponse)
        app.state.templates = Jinja2Templates(directory=str(REPO_ROOT / "templates"))
        client = TestClient(app, follow_redirects=False)

        client.cookies.set("auth_token", _auth_cookie())
        resp = client.get(f"/login?next={quote(DEEP_LINK, safe='')}", headers=HTML)
        assert resp.status_code == 302, resp.text[:300]
        assert resp.headers["location"] == DEEP_LINK
