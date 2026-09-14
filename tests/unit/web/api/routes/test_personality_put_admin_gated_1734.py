"""1734: PUT /api/v1/personality/profile is admin-only until the store is
per-user.

The route LOOKED user-scoped ({user_id} in the path) but
PiperConfigParser.save_personality_config ignores user_id and rewrites the
GLOBAL config/PIPER.user.md — any authed hosted-beta user's save clobbers the
whole instance's overlay. Fix shape chosen: gate the PUT with require_admin
(the #1508/#1598 idiom) rather than rewire the store under time pressure.

RETARGETED 2026-09-13 by #1751, which removed the `{user_id}` path segment
(and the GET's total lack of an auth dependency) so the principal comes from
the session. The addresses under test moved from `/profile/{user_id}` to
`/profile`; every pin below is preserved, none relaxed. Two tests changed
meaning rather than just address, and say so at their own docstrings:
`test_a_user_id_in_the_path_is_not_a_bypass` and
`test_get_carries_no_ADMIN_dependency`.

What this file pins, per the 1734 acceptance shape:
  1. Authenticated non-admin PUT → 403, and the overlay file is PROVABLY
     untouched (before/after content hash — a 403 that still wrote the file
     would satisfy a status-only check while doing exactly the harm).
  2. Admin PUT still works (200) and actually persists — the gate must not
     break the route for the people it admits.
  3. GET carries no ADMIN gate — any authenticated user still reads (read-only
     is harmless). It DOES require authentication as of #1751; 1734's claim was
     always about admin authority, never about anonymity.
  4. The 403 carries no payload echo (#1598 no-leak idiom).
  5. Unauthenticated PUT → 401 before any admin DB lookup, file untouched.

Mechanism (same as test_admin_readonly_routes_gated_1598.py): patch
`_user_is_admin` and override `get_current_user`, so require_admin's own
refuse/allow logic runs for real. Bare app carrying only this router → the
status is attributable to the ROUTE dependency alone (m-43 layer note).

File-system layer: PiperConfigParser resolves config/PIPER.user.md relative to
CWD, so each test chdirs into tmp_path and seeds a sentinel overlay there —
the repo's real overlay (legitimately absent, ADR-075 D4) is never in play.
"""

import hashlib

import pytest
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from services.api.errors import APIError
from services.auth import auth_middleware
from services.auth.auth_middleware import get_current_user, require_admin
from web.api.routes import personality as personality_module
from web.personality_integration import PiperConfigParser

SENTINEL_OVERLAY = """# Piper Morgan User Configuration

```yaml
personality:
  warmth_level: 0.31
  confidence_style: numeric
  action_orientation: low
  technical_depth: detailed
```

## Hands off

If a non-admin PUT rewrites this file, 1734's gate has failed.
"""

# A payload distinct from both the sentinel and the code's defaults, so
# presence/absence in file or response body is unambiguous.
ATTACK_PAYLOAD = {
    "warmth_level": 0.93,
    "confidence_style": "descriptive",
    "action_orientation": "medium",
    "technical_depth": "simplified",
}


def _sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class _FakeClaims:
    """Stands in for JWTClaims; require_admin touches only .user_id."""

    user_id = "11111111-1111-1111-1111-111111111111"
    username = "not-an-admin"


@pytest.fixture
def overlay(tmp_path, monkeypatch):
    """Chdir into an isolated tree seeded with a sentinel global overlay."""
    monkeypatch.chdir(tmp_path)
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    overlay_path = config_dir / "PIPER.user.md"
    overlay_path.write_text(SENTINEL_OVERLAY)
    return overlay_path


@pytest.fixture
def app(overlay):
    app = FastAPI()
    app.include_router(personality_module.router)
    # The route pulls the parser from app.state (WebComponentsInitializationPhase
    # does this in the real app).
    app.state.config_parser = PiperConfigParser()

    @app.exception_handler(APIError)
    async def _api_error_handler(request, exc):  # pragma: no cover - trivial
        return JSONResponse(status_code=exc.status_code, content={"error": exc.error_code})

    return app


@pytest.fixture
def client(app):
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


class TestNonAdminPutRefused:
    def test_403_and_overlay_provably_untouched(self, client, as_non_admin, overlay):
        before = _sha256(overlay)
        response = client.put("/api/v1/personality/profile", json=ATTACK_PAYLOAD)
        assert response.status_code == 403, (
            f"authenticated non-admin PUT got {response.status_code}, expected 403. "
            f"body={response.text[:200]}"
        )
        assert _sha256(overlay) == before, (
            "the global overlay file changed on a refused PUT — the 403 is "
            "cosmetic and the cross-user write 1734 exists to stop still happened"
        )
        assert overlay.read_text() == SENTINEL_OVERLAY

    def test_403_leaks_no_payload(self, client, as_non_admin, overlay):
        """#1598 idiom: the refusal must not echo config data — neither the
        attacker's submitted values nor the stored overlay's."""
        body = client.put("/api/v1/personality/profile", json=ATTACK_PAYLOAD).text
        for leaked in ("warmth_level", "0.93", "0.31", "descriptive", "numeric"):
            assert leaked not in body, f"403 body still carries {leaked!r}"

    def test_a_user_id_in_the_path_is_not_a_bypass(self, client, as_non_admin, overlay):
        """Originally: a path segment matching the caller's OWN user_id must not
        admit, because the store is global regardless of what the path claims.
        #1751 made that unreachable by construction — there is no `{user_id}`
        address left — so the pin now asserts the stronger property: no
        id-bearing path exists to aim at all (404), own id or anyone else's,
        and nothing is written either way."""
        before = _sha256(overlay)
        for claimed in (_FakeClaims.user_id, "default", "22222222-2222-4222-8222-222222222222"):
            response = client.put(f"/api/v1/personality/profile/{claimed}", json=ATTACK_PAYLOAD)
            assert response.status_code == 404, (
                f"/profile/{claimed} answered {response.status_code}; the "
                "client-supplied-principal address must not exist (#1751)"
            )
            assert _sha256(overlay) == before


class TestAdminPutStillWorks:
    def test_admin_put_200_and_persists(self, client, as_admin, overlay):
        response = client.put("/api/v1/personality/profile", json=ATTACK_PAYLOAD)
        assert response.status_code == 200, (
            f"admin PUT got {response.status_code} — the gate broke the route for "
            f"the people it is supposed to admit. body={response.text[:200]}"
        )
        assert response.json()["status"] == "success"
        assert response.json()["data"]["warmth_level"] == 0.93
        # Not vacuous: the write must actually have landed.
        assert "0.93" in overlay.read_text(), "admin save reported success but did not persist"


class TestGetUnchangedForAllUsers:
    def test_non_admin_get_still_200(self, client, as_non_admin, overlay):
        """GET is read-only and carries no ADMIN gate — an authenticated
        non-admin still reads. (#1751 added an authentication dependency to the
        GET; 1734's claim was always about admin authority, not authentication.)
        """
        response = client.get("/api/v1/personality/profile")
        assert (
            response.status_code == 200
        ), f"non-admin GET got {response.status_code} — 1734 gates the PUT only"
        # Serves the (sentinel) global config, proving the read path is intact.
        assert response.json()["data"]["warmth_level"] == 0.31

    def test_get_carries_no_ADMIN_dependency(self):
        """Wiring layer, stated as such: the GET's dependency tree must not
        contain require_admin anywhere. Was 'no dependency at all' until #1751
        gave the GET its session principal via get_current_user — which is the
        dependency that makes the read authenticated, not admin-gated."""

        def _callables(dependant):
            for sub in dependant.dependencies:
                yield sub.call
                yield from _callables(sub)

        for route in personality_module.router.routes:
            if route.path == "/api/v1/personality/profile" and "GET" in route.methods:
                calls = set(_callables(route.dependant))
                assert (
                    require_admin not in calls
                ), "require_admin crept onto the GET; 1734 scoped the gate to the PUT"
                assert get_current_user in calls, (
                    "the GET lost its authentication dependency — #1751's principal "
                    "source is gone and the route is anonymous again"
                )
                break
        else:  # pragma: no cover
            pytest.fail("GET /api/v1/personality/profile route not found")


class TestUnauthenticatedPut:
    def test_401_before_admin_lookup_and_file_untouched(self, app, overlay, monkeypatch):
        """No token → 401 from require_admin's get_current_user sub-dependency;
        the admin DB read must not even run, and the file must not change."""
        called = []

        async def _should_not_run(user_id):  # pragma: no cover - asserted absent
            called.append(user_id)
            return True

        monkeypatch.setattr(auth_middleware, "_user_is_admin", _should_not_run)
        before = _sha256(overlay)
        with TestClient(app) as c:
            response = c.put("/api/v1/personality/profile", json=ATTACK_PAYLOAD)
        assert (
            response.status_code == 401
        ), f"unauthenticated PUT got {response.status_code}, expected 401"
        assert not called, "admin DB read ran for an unauthenticated caller"
        assert _sha256(overlay) == before
