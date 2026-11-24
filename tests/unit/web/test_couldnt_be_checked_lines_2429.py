"""Issue 2429: the three "couldn't be checked" 503 lines reach a person, in CXO's words.

CXO's words (mail 01M8785ZVZ); Arch's ruling on where the class and constants live
(decisions.log 2026-11-24 09:16): ``UserFacingHTTPException`` and the three constants sit
in ``services/api/errors.py`` so a ``services/`` gate raises them without importing
``web/``.

LAYER: each raising site is driven at the layer that produces the reply.
- The four ``UserFacingHTTPException`` sites (the refresh route, ``get_current_user``,
  standup's ``get_current_user_optional``, ``require_admin``, ``require_ops_reader``)
  run inside a small app that carries the app's REAL ``HTTPException`` handler, taken
  from ``web.app``; the client's JSON is read.
- The middleware's own 503 (``AuthMiddleware.dispatch``) is read from the middleware's
  response; it never passes the handler.
"NOTHING WAS CHANGED": for every site that says it (lines 1 and 2), a test shows the
refusal comes before any write on that path: the route body never runs, and for the
refresh route no database call, no audit row, no new token and no cookie.
DENOMINATOR: every site of the three lines under ``services/`` and ``web/`` (six raises;
the source pins below fail if a seventh appears with an old sentence or a copy).
"""

import ast
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient

from services.api import errors
from services.api.errors import (
    ADMIN_PERMISSIONS_COULD_NOT_BE_CHECKED_MESSAGE,
    PERMISSIONS_COULD_NOT_BE_CHECKED_MESSAGE,
    SESSION_COULD_NOT_BE_CHECKED_MESSAGE,
)
from services.auth import auth_middleware
from services.auth.auth_middleware import (
    AuthMiddleware,
    get_current_user,
    require_admin,
    require_ops_reader,
)
from services.auth.container import AuthContainer
from services.auth.jwt_service import BlacklistUnavailable, JWTClaims, JWTService

ROOT = Path(__file__).resolve().parents[3]
SECRET = "test-secret-2429-not-a-real-key"

CXO_SESSION = (
    "Your session couldn't be checked just now. Nothing was changed. Try again in a "
    "moment; if it keeps failing, tell us."
)
CXO_ADMIN = (
    "Admin permissions couldn't be checked just now. Nothing was changed. Try again in a "
    "moment; if it keeps failing, tell us."
)
CXO_PERMISSIONS = (
    "Permissions couldn't be checked just now. Try again in a moment; if it keeps "
    "failing, tell us."
)
OLD_SENTENCES = (
    "Couldn't verify your session",
    "Couldn't verify admin permissions",
    "Couldn't verify permissions",
)


def _real_handler():
    from web.app import app as real_app  # the handler is registered on the module-level app

    return real_app.exception_handlers[HTTPException]


def _app():
    app = FastAPI()
    app.add_exception_handler(HTTPException, _real_handler())
    return app


def _claims() -> JWTClaims:
    return JWTClaims(
        iss="piper",
        aud="piper",
        sub="u-2429",
        exp=0,
        iat=0,
        jti="j-2429",
        user_id="00000000-0000-0000-0000-000000002429",
        user_email="t2429@example.invalid",
        username="t2429",
        scopes=["read"],
        token_type="access",
    )


def _jwt_service_with_store_down() -> JWTService:
    """A real JWTService whose revocation store raises: ``validate_token`` runs for real
    (real HS256 decode) and meets ``BlacklistUnavailable`` at its blacklist check."""
    blacklist = MagicMock()
    blacklist.is_blacklisted = AsyncMock(side_effect=BlacklistUnavailable("store down"))
    return JWTService(secret_key=SECRET, blacklist=blacklist)


def _token(jwt_service: JWTService, refresh: bool = False) -> str:
    make = jwt_service.generate_refresh_token if refresh else jwt_service.generate_access_token
    kwargs = {"user_id": "00000000-0000-0000-0000-000000002429"}
    kwargs["user_email"] = "t2429@example.invalid"
    if not refresh:
        kwargs["scopes"] = ["read"]
    return make(**kwargs)


class TestTheWords:
    def test_the_constants_carry_cxos_words(self):
        assert SESSION_COULD_NOT_BE_CHECKED_MESSAGE == CXO_SESSION
        assert ADMIN_PERMISSIONS_COULD_NOT_BE_CHECKED_MESSAGE == CXO_ADMIN
        assert PERMISSIONS_COULD_NOT_BE_CHECKED_MESSAGE == CXO_PERMISSIONS

    @staticmethod
    def _strings_under_services_and_web():
        for folder in ("services", "web"):
            for path in sorted((ROOT / folder).rglob("*.py")):
                tree = ast.parse(path.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    if isinstance(node, ast.Constant) and isinstance(node.value, str):
                        yield path.relative_to(ROOT).as_posix(), node.value

    def test_each_sentence_is_written_exactly_once_as_its_constant(self):
        """The session line had five copies at four kinds of site; now one. ``ast`` joins
        implicitly concatenated literals, so a copy split over lines is still seen."""
        found = {CXO_SESSION: [], CXO_ADMIN: [], CXO_PERMISSIONS: []}
        old = []
        for path, value in self._strings_under_services_and_web():
            for line in found:
                if line in value:
                    found[line].append(path)
            if any(s.lower() in value.lower() for s in OLD_SENTENCES):
                old.append(path)
        for line, paths in found.items():
            assert paths == ["services/api/errors.py"], (line[:30], paths)
        assert old == [], old


class TestTheRefreshRoute:
    """``POST /api/v1/auth/refresh`` with the revocation store down."""

    def _run(self):
        from web.api.routes import auth as auth_routes

        jwt_service = _jwt_service_with_store_down()
        refresh_token = _token(jwt_service, refresh=True)
        session = MagicMock()
        session.execute = AsyncMock()
        session.commit = AsyncMock()
        session.flush = AsyncMock()
        scope = MagicMock()
        scope.__aenter__ = AsyncMock(return_value=session)
        scope.__aexit__ = AsyncMock(return_value=False)

        app = _app()
        app.include_router(auth_routes.router)
        app.dependency_overrides[auth_routes.get_jwt_service] = lambda: jwt_service
        audit = AsyncMock()
        with (
            patch.object(
                auth_routes.AsyncSessionFactory, "session_scope_fresh", return_value=scope
            ),
            patch("services.auth.jwt_service.audit_logger.log_auth_event", audit),
            patch.object(JWTService, "generate_access_token") as mint,
        ):
            client = TestClient(app)
            client.cookies.set("refresh_token", refresh_token)
            reply = client.post("/api/v1/auth/refresh")
        return reply, session, audit, mint

    def test_the_client_receives_the_session_line(self):
        reply, *_ = self._run()
        assert reply.status_code == 503
        assert reply.json() == {"message": CXO_SESSION, "detail": CXO_SESSION}

    def test_the_refusal_comes_before_any_write(self):
        """No database call, no audit row, no new token, no cookie set or cleared."""
        reply, session, audit, mint = self._run()
        assert reply.status_code == 503
        session.execute.assert_not_called()
        session.commit.assert_not_called()
        session.flush.assert_not_called()
        session.add.assert_not_called()
        audit.assert_not_called()
        mint.assert_not_called()
        assert "set-cookie" not in {k.lower() for k in reply.headers.keys()}


class TestTheMiddlewaresOwnResponse:
    """``AuthMiddleware.dispatch``: its 503 is built by the middleware, not the handler."""

    def _run(self):
        jwt_service = _jwt_service_with_store_down()
        ran = []
        app = FastAPI()

        @app.post("/api/v1/probe-2429")
        async def probe():  # pragma: no cover - reached only if the middleware lets it
            ran.append(True)
            return {"ran": True}

        app.add_middleware(AuthMiddleware, jwt_service=jwt_service)
        client = TestClient(app, raise_server_exceptions=False)
        reply = client.post(
            "/api/v1/probe-2429", headers={"Authorization": f"Bearer {_token(jwt_service)}"}
        )
        return reply, ran

    def test_the_client_receives_the_session_line(self):
        reply, _ = self._run()
        assert reply.status_code == 503
        assert reply.json()["message"] == CXO_SESSION
        assert reply.headers["Retry-After"] == "5"

    def test_the_refusal_comes_before_the_route_runs(self):
        reply, ran = self._run()
        assert reply.status_code == 503
        assert ran == []


class TestTheDependencies:
    """The two session dependencies and the two permission gates, each in front of a
    route whose body records that it ran, through the app's real handler."""

    def _client(self, dependency, ran):
        app = _app()

        @app.post("/write")
        async def write(_user=Depends(dependency)):
            ran.append(True)
            return {"wrote": True}

        return app, TestClient(app)

    def test_get_current_user_says_the_session_line_before_the_route_runs(self):
        jwt_service = _jwt_service_with_store_down()
        ran = []
        _, client = self._client(get_current_user, ran)
        with patch.object(AuthContainer, "_jwt_service", jwt_service):
            reply = client.post(
                "/write", headers={"Authorization": f"Bearer {_token(jwt_service)}"}
            )
        assert reply.status_code == 503
        assert reply.json() == {"message": CXO_SESSION, "detail": CXO_SESSION}
        assert ran == []

    def test_standups_dependency_says_the_session_line_before_the_route_runs(self):
        from web.api.routes import standup

        jwt_service = _jwt_service_with_store_down()
        ran = []
        _, client = self._client(standup.get_current_user_optional, ran)
        with (
            patch.object(standup, "REQUIRE_AUTH", True),
            patch.object(standup, "JWTService", lambda: jwt_service),
        ):
            reply = client.post(
                "/write", headers={"Authorization": f"Bearer {_token(jwt_service)}"}
            )
        assert reply.status_code == 503
        assert reply.json() == {"message": CXO_SESSION, "detail": CXO_SESSION}
        assert ran == []

    def test_require_admin_says_the_admin_line_before_the_route_runs(self):
        ran = []
        app, client = self._client(require_admin, ran)
        app.dependency_overrides[get_current_user] = _claims
        with patch.object(
            auth_middleware, "_user_is_admin", AsyncMock(side_effect=OSError("db down"))
        ):
            reply = client.post("/write")
        assert reply.status_code == 503
        assert reply.json() == {"message": CXO_ADMIN, "detail": CXO_ADMIN}
        assert ran == []

    def test_require_ops_reader_says_the_permissions_line(self):
        ran = []
        app, client = self._client(require_ops_reader, ran)
        app.dependency_overrides[get_current_user] = _claims
        with patch.object(
            auth_middleware, "_user_can_read_ops", AsyncMock(side_effect=OSError("db down"))
        ):
            reply = client.post("/write")
        assert reply.status_code == 503
        assert reply.json() == {"message": CXO_PERMISSIONS, "detail": CXO_PERMISSIONS}
        assert "db down" not in reply.text
        assert ran == []

    @pytest.mark.parametrize(
        "gate, lookup",
        [(require_admin, "_user_is_admin"), (require_ops_reader, "_user_can_read_ops")],
    )
    def test_the_403s_are_unchanged(self, gate, lookup):
        ran = []
        app, client = self._client(gate, ran)
        app.dependency_overrides[get_current_user] = _claims
        with patch.object(auth_middleware, lookup, AsyncMock(return_value=False)):
            reply = client.post("/write")
        assert reply.status_code == 403
        expected = (
            # Issue 2432 (CXO): reworded (no em dash), marked; still refused before the route.
            "This changes app-wide configuration, so it needs an admin account. Nothing "
            "was changed."
            if gate is require_admin
            else "This page is for operations readers."
        )
        assert reply.json()["message"] == expected


def test_the_web_module_re_exports_the_same_class():
    from web.api.exceptions import UserFacingHTTPException as from_web

    assert from_web is errors.UserFacingHTTPException
