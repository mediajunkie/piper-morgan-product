"""The /api/v1/preferences/* routes read the auth claims' USER ID by its real field name.

Found 2026-09-23 while live-verifying #1574: every handler in preferences.py did
``str(current_user.id)`` — but the dependency yields ``JWTClaims``, whose field is ``user_id``
— so every call 500'd ('Error loading preferences') since the auth dependency landed, and
nothing ever exercised the routes end-to-end (the #1793 class at the HTTP layer).

LAYER (m-43): real TestClient over the real router with only the auth dependency overridden —
the same HTTP surface alpha serves. A 500 here IS the bug; a 200/404 means the handler at
least reached its own logic with the right principal. DENOMINATOR: the two GET routes (profile,
stats) — the two POST hint routes share the exact same fixed line and are covered by
construction of the fix, not asserted here (they need a stored hint to reach 200).
"""

from __future__ import annotations

from uuid import uuid4

from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from web.api.routes.preferences import router


def _claims() -> JWTClaims:
    uid = uuid4()
    return JWTClaims(
        iss="piper-morgan",
        aud="piper-morgan-api",
        sub=str(uid),
        exp=9999999999,
        iat=1000000000,
        jti=str(uuid4()),
        user_id=uid,
        user_email="claims-field@test.local",
        username="claims-field",
        scopes=["user"],
        token_type="access",
        session_id=None,
    )


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = _claims
    return TestClient(app)


class TestPreferencesRoutesReadTheRealClaimsField:
    def test_profile_does_not_500_on_the_claims_field(self):
        r = _client().get("/api/v1/preferences/profile")
        assert r.status_code != 500, r.text
        assert "Error loading preferences" not in r.text

    def test_stats_does_not_500_on_the_claims_field(self):
        r = _client().get("/api/v1/preferences/stats")
        assert r.status_code != 500, r.text
