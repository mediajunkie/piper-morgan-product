"""#1839 — the SERVED /health carries deploy identity (environment/version/git SHA).

The first #1839 landing put these fields only on staging_health.py's router — which
no app mounted — and the gap was found by CURLING the freshly-deployed droplet during
the v0.8.13.0 release verification, not by reading code: the described surface was not
the running one (m-49). This test pins the fields to the route infrastructure actually
polls (web/api/routes/admin.py's /health, the fly.toml + Dockerfile + compose
healthcheck target), through a real ASGI client.

staging_health.py itself was deleted 2026-09-23 (#1499 Class 2 — its router was dead,
mounted by no app); `deploy_identity()` moved to `services/api/health/deploy_identity.py`
first so both live call sites (this route and `/api/v1/version`) keep one shared source.

LAYER (m-43): route, real TestClient — the same HTTP surface the droplet serves.
DENOMINATOR: the one ungated /health route; `/api/v1/version` shares the same
`deploy_identity()` call and is covered separately (test_version_route_1499.py), so the
two cannot drift.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from web.api.routes.admin import router as admin_router


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(admin_router)
    return TestClient(app)


class TestServedHealthCarriesDeployIdentity:
    def test_health_reports_version_environment_and_sha(self, monkeypatch):
        monkeypatch.setenv("PIPER_GIT_SHA", "abc1234")
        monkeypatch.setenv("PIPER_ENVIRONMENT", "development")

        body = _client().get("/health").json()

        assert body["git_sha"] == "abc1234"
        assert body["environment"] == "development"
        # Version comes from the shipped VERSION file — a real value, never a literal.
        assert body["version"] not in ("", "unknown", "staging", "PM-038-staging")

    def test_unset_identity_reports_unknown_never_a_hardcoded_literal(self, monkeypatch):
        """The pre-#1839 defect was a POPULATED wrong value ("staging") — worse than
        absent, because a populated field reads as a working surface. Unset must say
        unknown, honestly."""
        monkeypatch.delenv("PIPER_GIT_SHA", raising=False)
        monkeypatch.delenv("PIPER_ENVIRONMENT", raising=False)

        body = _client().get("/health").json()

        assert body["git_sha"] == "unknown"
        assert body["environment"] == "unknown"

    def test_health_stays_ungated(self):
        """#1598's named exception: infrastructure polls this with no credentials."""
        assert _client().get("/health").status_code == 200
