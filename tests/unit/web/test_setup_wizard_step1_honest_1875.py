"""#1875 — the setup wizard's Step 1 no longer dead-ends every new user on alpha.

Three stacked causes, each pinned at its own layer (m-43):
1. ROUTE — `/api/v1/setup/check-system` is a read and is not behind the #1504
   write lockout (the classification test in test_setup_lockout_1504.py moved it).
2. APP HANDLER — a 403 raised WITH a specific detail keeps that detail in the
   JSON body; only a bare "Forbidden" gets the generic copy.
3. RENDER (JS) — the wizard checks `response.ok` before reading check-system
   fields, and its failure copy no longer asserts a Docker cause on a hosted
   instance. The message is JS-rendered, so the pin reads the shipped source.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from web.api.routes import setup as setup_routes

REPO_ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.smoke
def test_check_system_answers_even_when_setup_is_complete():
    app = FastAPI()
    app.include_router(setup_routes.router)
    ok = AsyncMock(return_value=True)
    with (
        patch.object(setup_routes, "_completed_setup_exists", new=AsyncMock(return_value=True)),
        patch.object(setup_routes, "check_docker", new=ok),
        patch.object(setup_routes, "check_database", new=ok),
        patch.object(setup_routes, "check_redis", new=ok),
        patch.object(setup_routes, "check_chromadb", new=ok),
        patch.object(setup_routes, "check_temporal", new=AsyncMock(return_value=False)),
    ):
        r = TestClient(app).post("/api/v1/setup/check-system")
    assert r.status_code == 200, r.text
    assert r.json()["all_required_ready"] is True


def _app_with_handlers():
    from web.app import app as real_app  # the handler is registered on the module-level app

    handler = real_app.exception_handlers[HTTPException]
    app = FastAPI()
    app.add_exception_handler(HTTPException, handler)

    @app.get("/specific")
    async def specific():
        raise HTTPException(
            status_code=403, detail="Setup is already complete on this server. Sign in instead."
        )

    @app.get("/bare")
    async def bare():
        raise HTTPException(status_code=403, detail="Forbidden")

    return TestClient(app, raise_server_exceptions=False)


@pytest.mark.smoke
def test_specific_403_detail_survives_the_app_handler():
    c = _app_with_handlers()
    body = c.get("/specific").json()
    assert "already complete" in (body.get("message") or body.get("detail") or "")


def test_bare_403_still_gets_the_generic_copy():
    c = _app_with_handlers()
    body = c.get("/bare").json()
    assert "permission" in (body.get("message") or "").lower()


@pytest.mark.smoke
def test_wizard_js_checks_response_ok_before_reading_the_check_result():
    js = (REPO_ROOT / "web/static/js/setup.js").read_text()
    handler = js[js.index("check-system-btn") : js.index("next-1")]
    fetch_at = handler.index("fetch('/api/v1/setup/check-system'")
    ok_at = handler.index("if (!response.ok)")
    read_at = handler.index("data.docker_available")
    assert (
        fetch_at < ok_at < read_at
    ), "response.ok must be checked before the result fields are read"
    assert (
        "Run: docker compose up -d" not in handler
    ), "a failed check must not assert a Docker cause"
    assert re.search(
        r"data\.message \|\| data\.detail", handler
    ), "the server's own sentence is shown when present"
