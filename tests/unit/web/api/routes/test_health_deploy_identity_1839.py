"""#1839 — the SERVED /health carries deploy identity (environment/version/git SHA).

The first #1839 landing put these fields only on staging_health's router — which no
app mounts — and the gap was found by CURLING the freshly-deployed droplet during the
v0.8.13.0 release verification, not by reading code: the described surface was not the
running one (m-49). This test pins the fields to the route infrastructure actually
polls (web/api/routes/admin.py's /health, the fly.toml + Dockerfile + compose
healthcheck target), through a real ASGI client.

LAYER (m-43): route, real TestClient — the same HTTP surface the droplet serves.
DENOMINATOR: the one ungated /health route; staging_health's own payload is covered by
its module (and shares `deploy_identity()`, so the two cannot drift).
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
