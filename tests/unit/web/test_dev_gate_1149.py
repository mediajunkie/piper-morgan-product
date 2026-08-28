"""#1149 — dev-route gate: /debug-markdown must 404 in production.

The 2026-06-03 #1142 audit flagged /debug-markdown as a dev page reachable in prod.
The global auth middleware already 401s it, but defense-in-depth says a dev test page
should not be *mounted* in prod at all. `web/dev_gate.require_dev_environment` is the
canonical gate; the debug router depends on it. Tested via real request behavior
(TestClient → actual 404 / 200), not just an assertion that the symbol exists.
"""

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from web.dev_gate import is_production, require_dev_environment

# --- the gate logic ---


def test_is_production_true_only_when_explicit(monkeypatch):
    monkeypatch.setenv("PIPER_ENVIRONMENT", "production")
    assert is_production() is True
    monkeypatch.setenv("PIPER_ENVIRONMENT", "development")
    assert is_production() is False
    monkeypatch.delenv("PIPER_ENVIRONMENT", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    assert is_production() is False  # defaults to development (#1087 pattern)


def test_require_dev_environment_404s_in_prod(monkeypatch):
    monkeypatch.setenv("PIPER_ENVIRONMENT", "production")
    with pytest.raises(HTTPException) as exc:
        require_dev_environment()
    assert exc.value.status_code == 404  # 404 (invisible), not 403 (forbidden)


def test_require_dev_environment_noop_in_dev(monkeypatch):
    monkeypatch.setenv("PIPER_ENVIRONMENT", "development")
    assert require_dev_environment() is None


# --- the debug route's real behavior ---


def _debug_client() -> TestClient:
    from web.api.routes.debug import router

    app = FastAPI()
    app.include_router(router)
    return TestClient(app, raise_server_exceptions=False)


def test_debug_markdown_404_in_production(monkeypatch):
    monkeypatch.setenv("PIPER_ENVIRONMENT", "production")
    resp = _debug_client().get("/debug-markdown")
    assert resp.status_code == 404  # invisible in prod


def test_debug_markdown_served_in_dev(monkeypatch):
    monkeypatch.setenv("PIPER_ENVIRONMENT", "development")
    resp = _debug_client().get("/debug-markdown")
    assert resp.status_code == 200
    assert "renderMarkdown" in resp.text  # the dev debug page still works in dev
