"""Tests for the dev-only composting trigger (Issue #1143).

Mirrors test_dev_trust.py: verifies the production 404 gate and the trigger's
behavior against a mocked running composting subsystem on app.state.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.mux.composting_scheduler import CompostingRunResult
from web.routers.dev_composting import router


def _make_app(*, job=None, compost_bin=None) -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    if job is not None:
        app.state.composting_scheduler_job = job
    if compost_bin is not None:
        app.state.compost_bin = compost_bin
    return app


def _make_job(result: CompostingRunResult, *, running=True):
    job = MagicMock()
    job.is_running.return_value = running
    job.scheduler.run = AsyncMock(return_value=result)
    return job


def _make_bin(pending_count):
    b = MagicMock()
    b.pending = list(range(pending_count))
    return b


@pytest.fixture(autouse=True)
def _dev_env(monkeypatch):
    """Default to development so the dev-env gate is open unless a test overrides."""
    monkeypatch.delenv("PIPER_ENVIRONMENT", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)


class TestProductionGate:
    @pytest.mark.parametrize("var", ["PIPER_ENVIRONMENT", "ENVIRONMENT"])
    def test_trigger_404s_in_production(self, monkeypatch, var):
        monkeypatch.setenv(var, "production")
        client = TestClient(_make_app(job=_make_job(CompostingRunResult(processed_count=0))))
        resp = client.post("/api/v1/admin/composting/trigger")
        assert resp.status_code == 404

    def test_status_available_in_development(self):
        client = TestClient(
            _make_app(
                job=_make_job(CompostingRunResult(processed_count=0)), compost_bin=_make_bin(0)
            )
        )
        resp = client.get("/api/v1/admin/composting")
        assert resp.status_code == 200
        assert resp.json()["available"] is True


class TestTrigger:
    def test_trigger_force_runs_and_reports_counts(self):
        result = CompostingRunResult(
            processed_count=2, object_ids=["a", "b"], learnings_extracted=3
        )
        job = _make_job(result)
        client = TestClient(_make_app(job=job, compost_bin=_make_bin(2)))

        resp = client.post("/api/v1/admin/composting/trigger?user_id=u-123")
        assert resp.status_code == 200
        body = resp.json()
        assert body["triggered"] is True
        assert body["processed_count"] == 2
        assert body["learnings_extracted"] == 3
        assert body["object_ids"] == ["a", "b"]
        assert body["bin_pending_before"] == 2
        # force=True is the whole point — bypasses quiet-hours/min-pending gates.
        job.scheduler.run.assert_awaited_once_with(force=True, user_id="u-123")

    def test_empty_bin_reports_honestly(self):
        job = _make_job(CompostingRunResult(processed_count=0))
        client = TestClient(_make_app(job=job, compost_bin=_make_bin(0)))
        resp = client.post("/api/v1/admin/composting/trigger")
        assert resp.status_code == 200
        body = resp.json()
        assert body["processed_count"] == 0
        assert body["bin_pending_before"] == 0
        assert "empty" in body["message"].lower()

    def test_503_when_scheduler_not_running(self):
        client = TestClient(_make_app())  # no composting_scheduler_job on app.state
        resp = client.post("/api/v1/admin/composting/trigger")
        assert resp.status_code == 503

    def test_status_503_when_scheduler_not_running(self):
        client = TestClient(_make_app())
        resp = client.get("/api/v1/admin/composting")
        assert resp.status_code == 503
        assert resp.json()["available"] is False
