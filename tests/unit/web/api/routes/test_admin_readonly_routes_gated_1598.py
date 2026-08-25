"""1598: the five read-only metrics/health reads on the admin router now require
admin, per PM's 2026-08-25 ruling. #1508 gated only the four mutations, leaving
`/api/admin/` a prefix that half-honored its own name.

The sibling file (test_admin_cache_routes_gated_1508.py) pins the WIRING —
require_admin is attached to the right routes. This file pins the BEHAVIOR,
because those are different layers and only one of them is what a caller
experiences (m-43): an authenticated non-admin must get a clean **403**, not a
404, not a 500, and not a silently-empty 200 payload; an admin must still get
the real data.

Mechanism: `require_admin`'s DB read is isolated in `_user_is_admin` precisely
so a test can swap it while require_admin's own refuse/allow logic runs for
real (its docstring says so). We patch that one function and override
`get_current_user`, so the code under test is the shipped dependency, not a
mock of it.

Layer note: these run against a bare app carrying only this router, so the
result is attributable to the ROUTE dependency alone — no middleware in the
path to mask or manufacture the status. Unauthenticated behavior is the
middleware's job and is pinned separately below against the real app.
"""

import pytest
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from services.api.errors import APIError
from services.auth import auth_middleware
from services.auth.auth_middleware import get_current_user
from web.api.routes import admin as admin_module

# The five reads 1598 gated. /health is deliberately NOT here — see
# test_health_probe_open_to_unauthenticated below.
NEWLY_GATED_READS = [
    "/health/config",
    "/api/admin/intent-monitoring",
    "/api/admin/intent-cache-metrics",
    "/api/admin/piper-config-cache-metrics",
    "/api/admin/user-context-cache-metrics",
]

# The #1508 mutations, re-checked here for the non-admin refusal only (no
# admin-path call: clearing a process-wide cache is a side effect a unit test
# shouldn't inflict on its neighbours).
GATED_MUTATIONS = [
    "/api/admin/intent-cache-clear",
    "/api/admin/piper-config-cache-clear",
    "/api/admin/user-context-cache-clear",
    "/api/admin/user-context-cache-invalidate/some-session",
]


class _FakeClaims:
    """Stands in for JWTClaims; require_admin touches only .user_id."""

    user_id = "11111111-1111-1111-1111-111111111111"
    username = "not-an-admin"


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(admin_module.router)

    # web/app.py installs this handler app-wide; the bare app needs it so an
    # unauthenticated call surfaces as a status code instead of an exception.
    @app.exception_handler(APIError)
    async def _api_error_handler(request, exc):  # pragma: no cover - trivial
        return JSONResponse(status_code=exc.status_code, content={"error": exc.error_code})

    app.dependency_overrides[get_current_user] = lambda: _FakeClaims()
    with TestClient(app) as c:
        yield c


@pytest.fixture
def as_non_admin(monkeypatch):
    async def _not_admin(user_id):
        return False

    monkeypatch.setattr(auth_middleware, "_user_is_admin", _not_admin)


@pytest.fixture
def as_admin(monkeypatch):
    async def _is_admin(user_id):
        return True

    monkeypatch.setattr(auth_middleware, "_user_is_admin", _is_admin)


class TestReadOnlyAdminRoutesRefuseNonAdmins:
    @pytest.mark.parametrize("path", NEWLY_GATED_READS)
    def test_authenticated_non_admin_gets_403(self, client, as_non_admin, path):
        response = client.get(path)
        assert response.status_code == 403, (
            f"{path}: authenticated non-admin got {response.status_code}, expected 403. "
            f"body={response.text[:200]}"
        )

    @pytest.mark.parametrize("path", NEWLY_GATED_READS)
    def test_refusal_leaks_no_payload(self, client, as_non_admin, path):
        """A 403 that still returns the metrics would satisfy a status-code-only
        check while leaking exactly what the gate exists to withhold."""
        body = client.get(path).text
        for leaked in ("cache_enabled", "metrics", "validation", "exempt_paths"):
            assert leaked not in body, f"{path}: 403 body still carries {leaked!r}"

    @pytest.mark.parametrize("path", GATED_MUTATIONS)
    def test_mutations_still_refuse_non_admin(self, client, as_non_admin, path):
        """#1508's gate must survive the 1598 edit — same router, same file."""
        assert client.post(path).status_code == 403


class TestReadOnlyAdminRoutesAllowAdmins:
    @pytest.mark.parametrize("path", NEWLY_GATED_READS)
    def test_admin_still_gets_the_data(self, client, as_admin, path):
        response = client.get(path)
        assert response.status_code == 200, (
            f"{path}: admin got {response.status_code} — the gate broke the route "
            f"for the people it is supposed to admit. body={response.text[:200]}"
        )
        # Not vacuous: a 200 with an empty body would pass the line above.
        assert response.json(), f"{path}: admin got an empty payload"


class TestUnauthenticatedBehaviorUnchanged:
    def test_unauthenticated_is_401_not_403(self, monkeypatch):
        """No token → 401 from require_admin's own get_current_user
        sub-dependency, before any admin lookup. Distinct from the non-admin
        403, and the admin DB read must not even be reached."""
        app = FastAPI()
        app.include_router(admin_module.router)

        @app.exception_handler(APIError)
        async def _api_error_handler(request, exc):  # pragma: no cover - trivial
            return JSONResponse(status_code=exc.status_code, content={"error": exc.error_code})

        called = []

        async def _should_not_run(user_id):  # pragma: no cover - asserted absent
            called.append(user_id)
            return True

        monkeypatch.setattr(auth_middleware, "_user_is_admin", _should_not_run)

        with TestClient(app) as c:
            for path in NEWLY_GATED_READS:
                assert c.get(path).status_code == 401, f"{path} unauthenticated"
        assert not called, "admin DB read ran for an unauthenticated caller"

    def test_health_probe_open_to_unauthenticated(self):
        """⚠️ The named exception. /health carries no gate at all: fly.toml's
        [[http_service.checks]] polls it every 30s with no credentials, as do
        the Dockerfile HEALTHCHECK, docker-compose.staging.yml and
        scripts/restart-server.sh. 200 unauthenticated is the contract."""
        app = FastAPI()
        app.include_router(admin_module.router)
        with TestClient(app) as c:
            response = c.get("/health")
        assert response.status_code == 200, (
            "the liveness probe must answer unauthenticated — a gate here fails "
            "Fly's deploy health gate and restart-loops the machine"
        )
        assert response.json()["status"] in ("healthy", "degraded")
