"""#1792 — an unreachable revocation store must say "couldn't verify", not "revoked".

THE DEFECT. `TokenBlacklist.is_blacklisted` failed closed by returning `True` on any
exception. `JWTService.validate_token` could not tell that `True` apart from a real
blacklist hit, so it raised `TokenRevoked`, and every handler turned that into
**401 "Token has been revoked"**. A Redis or database blip therefore told every active
user that a security action had been taken against their session. It had not. As an
incident-response signal it is exactly backwards: the responder reads a mass-revocation
event that never happened, while the actual fault (the store is down) goes unnamed.

FAIL-CLOSED IS NOT THE BUG, AND IS NOT CHANGED HERE. `return True` meant "refuse", and
`raise BlacklistUnavailable` also means "refuse". Nothing is granted on a store error
before or after this fix; the security posture is identical. What changes is only the
claim attached to the refusal. Both halves are pinned below on purpose — the honest
message AND the continued refusal — because a fix that made the message nicer by
letting the request through would be far worse than the bug.

PRECEDENT. Status code and copy are not invented. `require_admin`
(services/auth/auth_middleware.py, #1485/#1598) already faced the same situation — a
live authorization lookup that might fail — and answers **503 "Couldn't verify admin
permissions right now — nothing was changed. Try again in a moment."** This is that
sentence with "your session" in place of "admin permissions".

TWO STORE SITES, NOT ONE (m-44). The issue cited `is_blacklisted`'s outer handler
(token_blacklist.py). The live reproduction that found the bug actually ran through
`_check_database`'s SEPARATE `return True` handler, because `_redis_available` was
False and the asyncpg session was bound to a dead event loop. Both sites are exercised
below; a suite covering only the cited one would have passed over the reproduced path.

LAYER (m-43). The store RAISES for real — `redis_factory.create_client` and
`db_session_factory.session_scope` are given real exceptions, and the real `except`
branches in `services/auth/token_blacklist.py` run. `is_blacklisted` is never stubbed
to return a value, so these tests fail if the production error handling is wrong, not
merely if a mock was configured differently. Real `JWTService` (real HS256 sign +
verify), real `AuthMiddleware`, real `get_current_user`.

DENOMINATOR. Two refusal surfaces are covered: the ASGI `AuthMiddleware.dispatch`
path (wire-level status + body) and the `get_current_user` FastAPI dependency
(APIError status_code + detail). Two further call sites take the same new branch and
are NOT covered here: `web/api/routes/standup.py` and the refresh route in
`web/api/routes/auth.py`. `MCPAuthAdapter.validate_mcp_token` deliberately does not
catch the new exception at all.

`@pytest.mark.integration` carries no database or Redis requirement in this file. It
is the established marker (tests/conftest.py:244) for opting OUT of the autouse mock
that pins `TokenBlacklist.is_blacklisted` to `False` — the very method under test.
"""

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.api.errors import APIError
from services.auth.auth_middleware import AuthMiddleware, get_current_user
from services.auth.container import AuthContainer
from services.auth.jwt_service import JWTService
from services.auth.token_blacklist import TokenBlacklist

PROBE_PATH = "/api/v1/probe-1792"
SECRET = "test-secret-1792-not-a-real-key"

# The exact false claim this issue is about. If any assertion below ever sees this
# string in a store-outage response, the bug is back.
REVOKED_CLAIM = "Token has been revoked"


# ---------------------------------------------------------------------------
# Blacklist stores: each one makes the REAL code path raise or answer for real.
# ---------------------------------------------------------------------------


def _blacklist_redis_raises() -> TokenBlacklist:
    """Redis branch, store unreachable — exercises is_blacklisted's own handler."""
    redis_factory = MagicMock()
    redis_factory.create_client = AsyncMock(side_effect=ConnectionError("Redis is down"))
    bl = TokenBlacklist(redis_factory, MagicMock())
    bl._redis_available = True
    return bl


def _blacklist_database_raises() -> TokenBlacklist:
    """Database fallback branch, store unreachable — exercises _check_database's
    SEPARATE handler. This is the site the live #1792 reproduction actually hit.

    #1802: `_check_database` now opens its session via `session_scope_fresh()`
    (a per-call engine bound to the currently-running loop, #442's documented
    opt-in) instead of `session_scope()` (the global `db` singleton, whose
    engine is bound to whichever loop first initialized it — the very thing
    that made a bare TestClient's request 2+ hit a dead loop). Both are
    stubbed to fail here so this test stays correct regardless of which one
    the production code calls.
    """
    failing_scope = MagicMock()
    failing_scope.__aenter__ = AsyncMock(
        side_effect=RuntimeError("Task ... attached to a different loop")
    )
    failing_scope.__aexit__ = AsyncMock(return_value=False)
    db_factory = MagicMock()
    db_factory.session_scope = MagicMock(return_value=failing_scope)
    db_factory.session_scope_fresh = MagicMock(return_value=failing_scope)

    bl = TokenBlacklist(MagicMock(), db_factory)
    bl._redis_available = False
    return bl


def _blacklist_says_revoked() -> TokenBlacklist:
    """Store is UP and reports a genuine hit. The security property must survive."""
    redis_client = AsyncMock()
    redis_client.exists = AsyncMock(return_value=1)
    redis_factory = MagicMock()
    redis_factory.create_client = AsyncMock(return_value=redis_client)
    bl = TokenBlacklist(redis_factory, MagicMock())
    bl._redis_available = True
    return bl


def _blacklist_says_clean() -> TokenBlacklist:
    """Store is UP and reports no hit — the ordinary happy path."""
    redis_client = AsyncMock()
    redis_client.exists = AsyncMock(return_value=0)
    redis_factory = MagicMock()
    redis_factory.create_client = AsyncMock(return_value=redis_client)
    bl = TokenBlacklist(redis_factory, MagicMock())
    bl._redis_available = True
    return bl


# ---------------------------------------------------------------------------
# Harnesses
# ---------------------------------------------------------------------------


def _jwt_service(blacklist: TokenBlacklist) -> JWTService:
    return JWTService(secret_key=SECRET, blacklist=blacklist)


def _fresh_token(jwt_service: JWTService) -> str:
    """A freshly minted, valid, never-revoked token — brand-new `jti` every call."""
    user_id = uuid.uuid4()
    return jwt_service.generate_access_token(
        user_id=user_id,
        user_email=f"{user_id}@example.com",
        scopes=["user"],
    )


def _middleware_client(blacklist: TokenBlacklist) -> tuple[TestClient, JWTService]:
    """Real AuthMiddleware in front of a trivial protected route."""
    jwt_service = _jwt_service(blacklist)
    app = FastAPI()

    @app.get(PROBE_PATH)
    async def probe():  # pragma: no cover - reached only when auth ALLOWS
        return {"reached_the_route": True}

    app.add_middleware(AuthMiddleware, jwt_service=jwt_service)
    return TestClient(app, raise_server_exceptions=False), jwt_service


async def _call_dependency(blacklist: TokenBlacklist):
    """Invoke the real `get_current_user` with a fresh valid token.

    `get_current_user` resolves its JWTService through the AuthContainer singleton,
    so the container is pointed at this test's instrumented service — the SAME
    instance that mints the token, so the signature is real on both ends. APIError
    is a plain Exception with no handler on a bare app, so the dependency is called
    directly and the raised APIError inspected, following the #1485 idiom
    (`exc.value.status_code == 503`).
    """
    jwt_service = _jwt_service(blacklist)
    request = MagicMock()
    request.cookies = {}
    credentials = MagicMock()
    credentials.credentials = _fresh_token(jwt_service)

    with patch.object(AuthContainer, "_jwt_service", jwt_service):
        return await get_current_user(request=request, credentials=credentials)


# ---------------------------------------------------------------------------
# The honest-degrade property
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestStoreOutageIsReportedHonestly:
    """An unreachable store produces "couldn't verify", never "revoked"."""

    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "make_blacklist",
        [_blacklist_redis_raises, _blacklist_database_raises],
        ids=["redis_branch", "database_branch"],
    )
    def test_store_error_reports_unavailable_not_revoked(self, make_blacklist):
        """503 + "couldn't verify", for BOTH fail-closed sites in token_blacklist.py.

        Pre-fix this was 401 "Token has been revoked" for a token minted seconds
        earlier with a `jti` that has never been written to any blacklist.
        """
        client, jwt_service = _middleware_client(make_blacklist())
        token = _fresh_token(jwt_service)

        response = client.get(PROBE_PATH, headers={"Authorization": f"Bearer {token}"})

        assert (
            response.status_code == 503
        ), f"a store outage must report 503, got {response.status_code}: {response.text}"
        body = response.json()
        assert (
            REVOKED_CLAIM not in response.text
        ), "the response still claims a revocation that never happened"
        assert "verify" in body["message"].lower()
        assert "nothing was changed" in body["message"].lower()

    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "make_blacklist",
        [_blacklist_redis_raises, _blacklist_database_raises],
        ids=["redis_branch", "database_branch"],
    )
    def test_store_error_still_refuses_the_request(self, make_blacklist):
        """The SECURITY half: honest does not mean permissive.

        A store outage must not become fail-open. The protected route must not run
        and no success status may be returned.
        """
        client, jwt_service = _middleware_client(make_blacklist())
        token = _fresh_token(jwt_service)

        response = client.get(PROBE_PATH, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code >= 400, "a store outage must never allow the request"
        assert "reached_the_route" not in response.text

    @pytest.mark.smoke
    @pytest.mark.asyncio
    async def test_dependency_surface_reports_unavailable_not_revoked(self):
        """Same property at the `get_current_user` dependency (503 APIError)."""
        with pytest.raises(APIError) as exc:
            await _call_dependency(_blacklist_redis_raises())

        assert exc.value.status_code == 503
        assert exc.value.error_code == "REVOCATION_CHECK_UNAVAILABLE"
        assert REVOKED_CLAIM not in exc.value.details["detail"]
        assert "nothing was changed" in exc.value.details["detail"].lower()


# ---------------------------------------------------------------------------
# The security property that must not regress
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestGenuineRevocationStillReportsRevoked:
    """A real blacklist hit must still get the revoked answer, unchanged."""

    @pytest.mark.smoke
    def test_revoked_token_still_gets_401_revoked(self):
        """Store is UP and says "blacklisted" — 401 "Token has been revoked".

        This is the regression guard on the fix: making outages honest must not
        soften, delay, or reword a real revocation.
        """
        client, jwt_service = _middleware_client(_blacklist_says_revoked())
        token = _fresh_token(jwt_service)

        response = client.get(PROBE_PATH, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 401
        assert response.json()["message"] == REVOKED_CLAIM

    @pytest.mark.smoke
    @pytest.mark.asyncio
    async def test_revoked_token_still_gets_401_at_dependency(self):
        """Same, at the `get_current_user` dependency."""
        with pytest.raises(APIError) as exc:
            await _call_dependency(_blacklist_says_revoked())

        assert exc.value.status_code == 401
        assert exc.value.error_code == "TOKEN_REVOKED"
        assert exc.value.details["detail"] == REVOKED_CLAIM

    @pytest.mark.smoke
    def test_clean_token_still_passes(self):
        """Control: a healthy store reporting no hit still lets the request through.

        Without this, every assertion above is satisfiable by a harness that refuses
        everything for unrelated reasons.
        """
        client, jwt_service = _middleware_client(_blacklist_says_clean())
        token = _fresh_token(jwt_service)

        response = client.get(PROBE_PATH, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert response.json() == {"reached_the_route": True}
