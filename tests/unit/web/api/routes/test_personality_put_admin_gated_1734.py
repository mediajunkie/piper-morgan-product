"""1734/1791: PUT /api/v1/personality/profile is per-user; the admin gate is retired.

Historical (1734): the PUT was admin-only because PiperConfigParser ignored
user_id and rewrote the GLOBAL config/PIPER.user.md — any authenticated user's
save clobbered the whole instance's overlay (including PM's ADR-075 D4
personal overlay, if present). require_admin (#1508/#1598 idiom) held that
blast radius back rather than closing it, and said so explicitly in its own
docstring: "When the store is scoped per-user ... this gate can come off."

RETARGETED 2026-09-24 by #1791, which gave the PUT a real per-user store
(users.preferences["upm"], #1574's store): a save now lands in the CALLER'S
OWN row, never the shared file, so the property require_admin existed to
protect (no cross-user, no instance-wide blast radius) now holds structurally
without the gate. require_admin is REMOVED from the PUT in this same change —
1734's own filing named this as its exit condition. This file is retargeted
rather than deleted, the same discipline #1751 already applied to it once
(see its own history for that precedent): what it pins now is "any
authenticated user, admin or not, can PUT and it lands ONLY in their own row;
the shared instance file is untouched; a different user's read is
unaffected."

What this file pins today:
  1. An authenticated NON-ADMIN PUT now succeeds (200) — the gate is gone —
     and persists to the CALLER'S OWN row only; the shared instance overlay
     file is PROVABLY untouched (before/after content hash).
  2. A different user's GET is unaffected by that PUT (still reads the
     instance default, scope="instance") — the write did not leak.
  3. An admin PUT behaves identically to a non-admin PUT — admin status is
     irrelevant to this route now, not merely "also allowed".
  4. Unauthenticated PUT is still 401, before any admin DB lookup even runs,
     and the overlay is untouched.
  5. `require_admin` is provably absent from the PUT route's dependency tree
     (mirrors `test_get_carries_no_ADMIN_dependency` in the sibling
     test_personality_principal_from_session_1751.py).

Mechanism: same bare-app-with-just-this-router pattern as before 1791.

LAYER (m-43): no live Postgres in this unit suite. UserPreferenceManager's
DB read/write both fail closed and degrade to in-memory-only for the life of
the process (documented on the class itself, and already relied on by
test_preferences_timezone_1876.py for the sibling /api/v1/preferences
router) — so a real-UUID principal's PUT/GET round-trip inside ONE
TestClient/app instance (one PiperConfigParser, one UserPreferenceManager)
works without a live database. Cross-PROCESS persistence needs the DB and is
covered separately by
tests/unit/services/domain/test_preference_persistence_1574.py's pattern
(mirrored for personality by test_personality_preference_persistence_1791.py).

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

If a PUT rewrites this file, #1791's per-user store has regressed to the
shared instance file.
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
    """Stands in for JWTClaims; the route touches only .user_id. A real UUID
    string so PiperConfigParser routes it to the per-user store, not the
    non-UUID/instance-file fallback."""

    user_id = "11111111-1111-1111-1111-111111111111"
    username = "not-an-admin"


class _OtherClaims:
    """A second, distinct principal — used to prove a PUT under _FakeClaims
    does not leak to anyone else."""

    user_id = "22222222-2222-4222-8222-222222222222"
    username = "someone-else"


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
    # does this in the real app). ONE instance, shared across requests within a
    # test — exactly how app.state.config_parser is shared in the real app, and
    # load-bearing here: it's what lets a same-user PUT-then-GET round-trip
    # through the in-memory cache without a live database.
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


class TestNonAdminPutNowSucceeds:
    def test_200_persists_to_own_row_overlay_untouched(self, client, as_non_admin, overlay):
        before = _sha256(overlay)
        response = client.put("/api/v1/personality/profile", json=ATTACK_PAYLOAD)
        assert response.status_code == 200, (
            f"authenticated non-admin PUT got {response.status_code}, expected 200 — "
            f"the admin gate should be gone. body={response.text[:200]}"
        )
        body = response.json()
        assert body["data"]["warmth_level"] == 0.93
        assert (
            body["scope"] == "user"
        ), f"a real per-user principal's write must report scope='user', got {body['scope']!r}"
        assert _sha256(overlay) == before, (
            "the shared instance overlay changed on a per-user PUT — writes must "
            "land in the caller's own row only, never the global file"
        )
        assert overlay.read_text() == SENTINEL_OVERLAY

    def test_written_value_reads_back_for_the_same_user(self, client, as_non_admin, overlay):
        client.put("/api/v1/personality/profile", json=ATTACK_PAYLOAD)
        read_back = client.get("/api/v1/personality/profile").json()
        assert read_back["data"]["warmth_level"] == 0.93
        assert read_back["scope"] == "user"

    def test_a_different_user_is_unaffected(self, app, client, as_non_admin, overlay):
        """The write must not leak to anyone else — a second principal still
        reads the untouched instance default through the SAME app/parser."""
        client.put("/api/v1/personality/profile", json=ATTACK_PAYLOAD)
        app.dependency_overrides[get_current_user] = lambda: _OtherClaims()
        other = client.get("/api/v1/personality/profile").json()
        assert other["data"]["warmth_level"] == 0.31, (
            "a different user's read picked up the first user's PUT — per-user "
            "isolation has failed"
        )
        assert other["scope"] == "instance"


class TestAdminStatusIsNowIrrelevant:
    def test_admin_put_behaves_identically_to_non_admin(self, client, as_admin, overlay):
        before = _sha256(overlay)
        response = client.put("/api/v1/personality/profile", json=ATTACK_PAYLOAD)
        assert response.status_code == 200
        body = response.json()
        assert body["data"]["warmth_level"] == 0.93
        assert body["scope"] == "user"
        assert _sha256(overlay) == before, "even an admin's write must not touch the shared file"


class TestUnauthenticatedPut:
    def test_401_before_any_admin_lookup_and_overlay_untouched(self, app, overlay, monkeypatch):
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
        assert not called, "an admin DB read ran even though require_admin was removed"
        assert _sha256(overlay) == before


class TestRequireAdminIsGoneFromThePut:
    def test_put_carries_no_ADMIN_dependency(self):
        def _callables(dependant):
            for sub in dependant.dependencies:
                yield sub.call
                yield from _callables(sub)

        for route in personality_module.router.routes:
            if route.path == "/api/v1/personality/profile" and "PUT" in route.methods:
                calls = set(_callables(route.dependant))
                assert (
                    require_admin not in calls
                ), "require_admin is still wired onto the PUT; #1791 was to remove it"
                assert (
                    get_current_user in calls
                ), "the PUT lost its authentication dependency entirely"
                break
        else:  # pragma: no cover
            pytest.fail("PUT /api/v1/personality/profile route not found")
