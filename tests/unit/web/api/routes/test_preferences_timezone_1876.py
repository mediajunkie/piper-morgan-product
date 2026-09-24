"""#1876 — GET/PUT /api/v1/preferences/timezone.

UserPreferenceManager.set_reminder_timezone (#1574's store) had ZERO callers
before this issue — no Settings page, no API route, no chat action — so every
clock face (#1576) rendered on DEFAULT_USER_TIMEZONE for everyone. These are
the two new routes: GET reads the caller's stored zone (or the honest
default + is_default=True); PUT sets it, with the store's own ValueError
becoming an honest 400 (no silent fallback).

LAYER (m-43): real TestClient over the real preferences router with ONLY the
auth dependency overridden (the `test_preferences_routes_claims_field.py`
idiom already used for this router) — the real Pydantic models, the real
route bodies, the real UserPreferenceManager singleton the router module
constructs at import time (`preference_manager` in
web/api/routes/preferences.py), and its real in-memory + best-effort-DB
write path (degrades to in-memory-only without a real Postgres row, per
tests/unit/services/domain/test_preference_persistence_1574.py — no crash).
DENOMINATOR: GET (default + set value), PUT (valid + invalid), and principal
isolation (two different callers never see each other's zone) — through this
router only. Does NOT cover the auth middleware itself (see
test_personality_principal_from_session_1751.py for that pattern against a
different router) or DB persistence across process restarts (#1574 already
covers that at the UserPreferenceManager layer).
"""

from __future__ import annotations

from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from web.api.routes.preferences import router

TIMEZONE_PATH = "/api/v1/preferences/timezone"


def _claims(user_id: UUID) -> JWTClaims:
    return JWTClaims(
        iss="piper-morgan",
        aud="piper-morgan-api",
        sub=str(user_id),
        exp=9999999999,
        iat=1000000000,
        jti=str(uuid4()),
        user_id=user_id,
        user_email=f"{user_id}@test.local",
        username="tz-1876",
        scopes=["user"],
        token_type="access",
        session_id=None,
    )


def _client_as(user_id: UUID) -> TestClient:
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = lambda: _claims(user_id)
    return TestClient(app)


@pytest.fixture
def user_a():
    return uuid4()


@pytest.fixture
def user_b():
    return uuid4()


class TestGetTimezoneDefault:
    def test_unset_user_reads_the_default_and_says_so(self, user_a):
        r = _client_as(user_a).get(TIMEZONE_PATH)
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["timezone"] == "America/Los_Angeles"
        assert body["is_default"] is True


class TestPutTimezoneValid:
    def test_set_then_get_round_trips(self, user_a):
        client = _client_as(user_a)
        r = client.put(TIMEZONE_PATH, json={"timezone": "Europe/Helsinki"})
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["timezone"] == "Europe/Helsinki"
        assert body["is_default"] is False

        r2 = client.get(TIMEZONE_PATH)
        assert r2.status_code == 200, r2.text
        body2 = r2.json()
        assert body2["timezone"] == "Europe/Helsinki"
        assert body2["is_default"] is False

    def test_setting_back_to_the_default_zone_reports_is_default_true(self, user_a):
        client = _client_as(user_a)
        client.put(TIMEZONE_PATH, json={"timezone": "Asia/Tokyo"})
        r = client.put(TIMEZONE_PATH, json={"timezone": "America/Los_Angeles"})
        assert r.status_code == 200, r.text
        assert r.json() == {"timezone": "America/Los_Angeles", "is_default": True}


class TestPutTimezoneInvalid:
    def test_unknown_zone_name_is_an_honest_400_not_a_silent_fallback(self, user_a):
        client = _client_as(user_a)
        r = client.put(TIMEZONE_PATH, json={"timezone": "Mars/Olympus_Mons"})
        assert r.status_code == 400, r.text
        assert "Mars/Olympus_Mons" in r.json()["detail"]

        # The bad PUT must not have silently written anything.
        after = client.get(TIMEZONE_PATH).json()
        assert after == {"timezone": "America/Los_Angeles", "is_default": True}

    def test_empty_string_is_400(self, user_a):
        r = _client_as(user_a).put(TIMEZONE_PATH, json={"timezone": ""})
        assert r.status_code == 400, r.text

    def test_missing_field_is_422(self, user_a):
        r = _client_as(user_a).put(TIMEZONE_PATH, json={})
        assert r.status_code == 422


class TestPrincipalIsolation:
    """Two users' timezones must never cross — the #1252 P6 principal-from-
    session guarantee, exercised at this router the same way #1751 exercises
    it at the personality router."""

    def test_two_users_do_not_see_each_others_timezone(self, user_a, user_b):
        client_a = _client_as(user_a)
        client_b = _client_as(user_b)

        client_a.put(TIMEZONE_PATH, json={"timezone": "Europe/Helsinki"})
        client_b.put(TIMEZONE_PATH, json={"timezone": "Australia/Sydney"})

        assert client_a.get(TIMEZONE_PATH).json()["timezone"] == "Europe/Helsinki"
        assert client_b.get(TIMEZONE_PATH).json()["timezone"] == "Australia/Sydney"

    def test_unauthenticated_request_runs_the_real_auth_dependency(self):
        """Both routes are wired to `Depends(get_current_user)`, not a bare
        `Any` param — a bare FastAPI app (this router only, no exception
        handlers) surfaces that as the dependency's own APIError rather than
        a translated HTTP status (the translation is the full app's
        exception-handler wiring, out of this file's layer per its docstring
        DENOMINATOR). Proving the dependency RUNS — and runs before the
        handler body — is what this test pins."""
        from services.api.errors import APIError

        app = FastAPI()
        app.include_router(router)
        client = TestClient(app, raise_server_exceptions=True)
        with pytest.raises(APIError):
            client.get(TIMEZONE_PATH)
        with pytest.raises(APIError):
            client.put(TIMEZONE_PATH, json={"timezone": "UTC"})
