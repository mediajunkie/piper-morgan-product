"""#1502 — `request.state.is_admin` is SET by the auth middleware, from `users.is_admin`.

Before: `web/api/routes/files.py` (download + preview) and the template user
context read `request.state.is_admin`, and nothing ever assigned it — every
admin branch behind it was unreachable while `templates/files.html` and
`account.html` already rendered admin affordances on the same flag. After: the
middleware resolves it per authenticated request through the same live DB
read `require_admin` uses (`_user_is_admin`), failing CLOSED to False.

LAYER (m-43): the real `AuthMiddleware.dispatch` with a real JWT in front of a
probe route that echoes `request.state`; only the DB read is patched at its
one-line boundary. DENOMINATOR (m-44): both middleware branches that populate
`request.state.user_id` (the protected path and the optional-auth "/" path),
and the three outcomes of the read (True / False / raises).
"""

from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from services.auth.auth_middleware import AuthMiddleware
from services.auth.jwt_service import JWTService
from services.auth.token_blacklist import TokenBlacklist

SECRET = "test-secret-1502-" + "x" * 32
PROBE_PATH = "/api/v1/probe-1502"


def _blacklist_clean() -> TokenBlacklist:
    bl = TokenBlacklist.__new__(TokenBlacklist)
    redis_client = MagicMock()
    redis_client.exists = AsyncMock(return_value=0)
    redis_factory = MagicMock()
    redis_factory.create_client = AsyncMock(return_value=redis_client)
    bl._redis_factory = redis_factory
    bl._redis = None
    bl._db_factory = None
    bl._seeded = True
    bl._local = set()
    return bl


def _client() -> tuple[TestClient, JWTService, str]:
    jwt_service = JWTService(secret_key=SECRET, blacklist=_blacklist_clean())
    app = FastAPI()

    @app.get(PROBE_PATH)
    async def probe(request: Request):
        return {
            "user_id": getattr(request.state, "user_id", None),
            "is_admin": getattr(request.state, "is_admin", "UNSET"),
        }

    @app.get("/")
    async def home(request: Request):
        return {"is_admin": getattr(request.state, "is_admin", "UNSET")}

    app.add_middleware(AuthMiddleware, jwt_service=jwt_service)
    user_id = uuid.uuid4()
    token = jwt_service.generate_access_token(
        user_id=user_id, user_email=f"{user_id}@example.com", scopes=["user"]
    )
    return TestClient(app, raise_server_exceptions=False), jwt_service, token


@pytest.mark.parametrize("db_says", [True, False])
def test_protected_path_sets_is_admin_from_the_db(db_says):
    client, _, token = _client()
    with patch(
        "services.auth.auth_middleware._user_is_admin", AsyncMock(return_value=db_says)
    ) as read:
        r = client.get(PROBE_PATH, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    assert r.json()["is_admin"] is db_says
    read.assert_awaited_once()


def test_optional_auth_home_path_sets_is_admin_too():
    """'/' authenticates from the cookie without 401ing; the flag must ride along."""
    client, _, token = _client()
    with patch("services.auth.auth_middleware._user_is_admin", AsyncMock(return_value=True)):
        r = client.get("/", cookies={"auth_token": token})
    assert r.status_code == 200, r.text
    assert r.json()["is_admin"] is True


def test_db_failure_fails_closed_to_non_admin_and_request_proceeds():
    client, _, token = _client()
    with patch(
        "services.auth.auth_middleware._user_is_admin",
        AsyncMock(side_effect=RuntimeError("db down")),
    ):
        r = client.get(PROBE_PATH, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    assert r.json()["is_admin"] is False


def test_template_user_context_reads_the_wired_flag():
    """`_extract_user_context` reports what the middleware resolved — not JWT claims."""
    from web.api.routes.ui import _extract_user_context

    request = MagicMock()
    request.state.user_id = "u-1502"
    request.state.user_claims = None
    request.state.is_admin = True
    assert _extract_user_context(request)["is_admin"] is True

    request.state.is_admin = False
    request.state.user_claims = {"is_admin": True}  # a claim must NOT grant
    assert _extract_user_context(request)["is_admin"] is False
