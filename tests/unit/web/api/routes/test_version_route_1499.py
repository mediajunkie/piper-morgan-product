"""#1499 Class 3 — `/api/v1/version` is fetched by two live pages and defined nowhere.

`templates/settings-index.html` and `templates/account.html` both fetch `/api/v1/version`
on load to fill their footer. No router defined the path, so both pages 404'd silently
and showed "unknown" (the catch branch) plus a warning toast — a user-visible defect that
looked like a version-lookup failure rather than a missing route.

The fix reuses `deploy_identity()` (`services/api/health/staging_health.py:62`), the same
helper the SERVED `/health` uses (`web/api/routes/admin.py`), so version/git_sha/
environment cannot drift between the two surfaces — the #1839 lesson, applied again.

LAYER (m-43): two layers, deliberately, because either alone is insufficient here —
  (a) route: real `TestClient` against the real mounted router → the path resolves and
      the payload has the fields;
  (b) template: real `template.render()` → the PAGES ask for that path and read those
      field NAMES. A route that 200s with the wrong key names would still show "unknown"
      in the footer, and (a) alone cannot see that.
DENOMINATOR: the one `/api/v1/version` route and both of its two known callers.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from jinja2 import Environment, FileSystemLoader

from web.api.routes.admin import router as admin_router

VERSION_PATH = "/api/v1/version"


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(admin_router)
    return TestClient(app)


def _render(template_name: str) -> str:
    env = Environment(loader=FileSystemLoader("templates"))
    return env.get_template(template_name).render(request=None, user={"username": "t"})


class TestVersionRouteExists:
    def test_version_path_resolves(self):
        """The whole defect in one assertion: this used to be a 404."""
        assert _client().get(VERSION_PATH).status_code == 200

    def test_reports_version_environment_and_sha(self, monkeypatch):
        monkeypatch.setenv("PIPER_GIT_SHA", "def5678")
        monkeypatch.setenv("PIPER_ENVIRONMENT", "development")

        body = _client().get(VERSION_PATH).json()

        assert body["git_sha"] == "def5678"
        assert body["environment"] == "development"
        # Version comes from the shipped VERSION file — a real value, never a literal.
        assert body["version"] not in ("", "unknown")

    def test_unset_identity_reports_unknown_never_a_hardcoded_literal(self, monkeypatch):
        """Same contract as /health (#1839): absent must say so, not invent a label."""
        monkeypatch.delenv("PIPER_GIT_SHA", raising=False)
        monkeypatch.delenv("PIPER_ENVIRONMENT", raising=False)

        body = _client().get(VERSION_PATH).json()

        assert body["git_sha"] == "unknown"
        assert body["environment"] == "unknown"

    def test_shares_deploy_identity_with_the_served_health(self, monkeypatch):
        """One helper, two surfaces — they cannot report different deploys."""
        monkeypatch.setenv("PIPER_GIT_SHA", "cafe123")
        monkeypatch.setenv("PIPER_ENVIRONMENT", "development")
        client = _client()

        version = client.get(VERSION_PATH).json()
        health = client.get("/health").json()

        for field in ("version", "environment", "git_sha"):
            assert version[field] == health[field]


class TestVersionCallersGetTheFieldsTheyRead:
    """The template half — a 200 with the wrong key names still shows 'unknown'."""

    def test_settings_index_fetches_the_route_and_reads_version_and_environment(self):
        html = _render("settings-index.html")
        assert f"fetch('{VERSION_PATH}'" in html
        assert "data.version" in html
        assert "data.environment" in html

    def test_account_fetches_the_route_and_reads_version_and_environment(self):
        html = _render("account.html")
        assert f"fetch('{VERSION_PATH}'" in html
        assert "data.version" in html
        assert "data.environment" in html

    def test_the_route_actually_serves_those_two_field_names(self):
        """Closes the loop between the two layers above."""
        body = _client().get(VERSION_PATH).json()
        assert "version" in body
        assert "environment" in body
