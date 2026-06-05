"""Unit tests for the dev-only trust-stage affordance (Issue #1148).

Covers the two parts that don't need a database:
  1. The production gate (AC#3: not exposed in production) — the security-
     critical bit, tested directly so it can't silently regress.
  2. A REAL Jinja render of the picker template (not a raw-string scan), with
     StrictUndefined so any typo'd template variable fails the test.

The DB write path (_force_set_stage) and route wiring are verified live against
the running server (see #1148 closing evidence) since they require Postgres.
"""

from pathlib import Path

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from web.routers.dev_trust import (
    _is_production,
    _stage_choices,
    require_dev_environment,
    router,
)


class TestProductionGate:
    """AC#3 — the affordance must be invisible in production."""

    def test_default_environment_is_not_production(self, monkeypatch):
        monkeypatch.delenv("PIPER_ENVIRONMENT", raising=False)
        monkeypatch.delenv("ENVIRONMENT", raising=False)
        assert _is_production() is False
        # Dependency must NOT raise when not in production.
        assert require_dev_environment() is None

    @pytest.mark.parametrize("var", ["PIPER_ENVIRONMENT", "ENVIRONMENT"])
    def test_production_blocks_with_404(self, monkeypatch, var):
        monkeypatch.delenv("PIPER_ENVIRONMENT", raising=False)
        monkeypatch.delenv("ENVIRONMENT", raising=False)
        monkeypatch.setenv(var, "production")
        assert _is_production() is True
        with pytest.raises(HTTPException) as exc_info:
            require_dev_environment()
        # 404 (not 403) so production does not disclose the route exists.
        assert exc_info.value.status_code == 404

    def test_production_is_case_insensitive(self, monkeypatch):
        monkeypatch.delenv("ENVIRONMENT", raising=False)
        monkeypatch.setenv("PIPER_ENVIRONMENT", "PRODUCTION")
        assert _is_production() is True

    def test_piper_environment_takes_precedence_over_legacy(self, monkeypatch):
        # PIPER_ENVIRONMENT is canonical (#1087); legacy ENVIRONMENT is the fallback.
        monkeypatch.setenv("PIPER_ENVIRONMENT", "development")
        monkeypatch.setenv("ENVIRONMENT", "production")
        assert _is_production() is False

    def test_staging_is_not_production(self, monkeypatch):
        monkeypatch.delenv("ENVIRONMENT", raising=False)
        monkeypatch.setenv("PIPER_ENVIRONMENT", "staging")
        assert _is_production() is False


class TestRouteWiringInProduction:
    """Prove the router-level dependency actually fires on the mounted routes —
    not just the helper in isolation. In production both routes must 404 BEFORE
    the handler runs (so no DB is touched, hence no fixtures needed)."""

    @pytest.fixture
    def prod_client(self, monkeypatch):
        monkeypatch.delenv("ENVIRONMENT", raising=False)
        monkeypatch.setenv("PIPER_ENVIRONMENT", "production")
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    def test_get_form_404s_in_production(self, prod_client):
        assert prod_client.get("/api/v1/admin/trust").status_code == 404

    def test_post_set_stage_404s_in_production(self, prod_client):
        resp = prod_client.post(
            "/api/v1/admin/trust/set-stage",
            data={"user_id": "009afc8c-bbb0-4391-8265-1575c0812949", "stage": "4"},
        )
        assert resp.status_code == 404


class TestStageChoices:
    def test_returns_all_four_stages_ascending(self):
        choices = _stage_choices()
        assert [c["value"] for c in choices] == [1, 2, 3, 4]
        assert [c["name"] for c in choices] == [
            "NEW",
            "BUILDING",
            "ESTABLISHED",
            "TRUSTED",
        ]


class TestTrustStageTemplateRenders:
    """Real Jinja render (StrictUndefined) — catches TemplateNotFound, syntax
    errors, and undefined-variable references that a raw-string scan misses."""

    M1 = "11111111-1111-1111-1111-111111111111"
    ADMIN = "22222222-2222-2222-2222-222222222222"

    @pytest.fixture
    def rendered(self):
        templates_dir = Path("web/templates")
        env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=True,
            undefined=StrictUndefined,
        )
        template = env.get_template("admin/trust_stage.html")
        return template.render(
            {
                "users": [
                    {"username": "m1-test", "user_id": self.M1},
                    {"username": "admin", "user_id": self.ADMIN},
                ],
                "stages": {
                    self.M1: {"value": 1, "name": "NEW"},
                    self.ADMIN: {"value": 4, "name": "TRUSTED"},
                },
                "stage_choices": [
                    {"value": 1, "name": "NEW"},
                    {"value": 2, "name": "BUILDING"},
                    {"value": 3, "name": "ESTABLISHED"},
                    {"value": 4, "name": "TRUSTED"},
                ],
                "message": "Set m1-test to Stage 4 (TRUSTED).",
                "error": None,
            }
        )

    def test_renders_dev_only_banner(self, rendered):
        assert "DEV ONLY" in rendered

    def test_renders_post_form_to_set_stage_endpoint(self, rendered):
        assert 'action="/api/v1/admin/trust/set-stage"' in rendered
        assert 'method="post"' in rendered

    def test_renders_user_options_with_current_stage(self, rendered):
        assert f'value="{self.M1}"' in rendered
        assert "m1-test" in rendered
        assert "current: Stage 1 (NEW)" in rendered
        assert "current: Stage 4 (TRUSTED)" in rendered

    def test_renders_all_stage_choices(self, rendered):
        for label in (
            "Stage 1 — NEW",
            "Stage 2 — BUILDING",
            "Stage 3 — ESTABLISHED",
            "Stage 4 — TRUSTED",
        ):
            assert label in rendered

    def test_stage_4_is_preselected_default(self, rendered):
        assert 'value="4" selected' in rendered

    def test_renders_flash_message(self, rendered):
        assert "Set m1-test to Stage 4 (TRUSTED)." in rendered

    def test_renders_current_stages_table(self, rendered):
        # Reference table shows both users with their stage pills.
        assert "Current stages" in rendered
        assert "1 · NEW" in rendered
        assert "4 · TRUSTED" in rendered
