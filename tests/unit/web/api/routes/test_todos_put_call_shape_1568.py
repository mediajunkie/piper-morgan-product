"""#1568 — the /todos page's PUT call shape must match the real route.

The page's inline-edit flow (templates/todos.html, pinned in
tests/unit/templates/test_todos_edit_priority_dates_1568.py) sends::

    PUT /api/v1/todos/{id}?title=...        (query param, no body)

because the real route declares ``title`` as a query parameter — there is
no Pydantic body model on PUT. This suite drives the REAL router through
FastAPI's parameter resolution (TestClient), with the repository autospec'd
against the REAL TodoRepository (#1548's discipline: the mock enforces the
real signatures, so an imagined repo call fails here as in production).

It proves both halves of the contract:
- the query-param shape the page sends lands in the route and reaches the
  repo with the real ``update_todo(todo_id, updates, owner_id=...)`` shape;
- the tempting OTHER shape (JSON body {"title": ...}) is silently DROPPED
  by this route — updates arrives empty — which is exactly why the page
  must never use it (success toast, nothing changed: the #1541 lie).

Layer: HTTP request → FastAPI param resolution → route function, repo
autospec'd (no DB). The repo's own behavior is covered by
tests/unit/services/repositories/ and integration suites.
"""

from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import create_autospec
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.repositories.todo_repository import TodoRepository
from web.api.dependencies import get_todo_repository
from web.api.routes.todos import router

CLAIMS = JWTClaims(
    iss="piper-morgan",
    aud="piper-morgan-api",
    sub="user-abc",
    exp=9999999999,
    iat=1234567890,
    jti="test-jti-1568",
    user_id=UUID("00000000-0000-0000-0000-000000000001"),
    user_email="xian@example.com",
    username="xian",
    scopes=["read", "write"],
    token_type="access",
)


def _stored_todo(**overrides):
    base = dict(
        id="t1",
        title="Ship it",
        description="",
        status="pending",
        priority="medium",
        owner_id="user-abc",
        created_at=datetime(2026, 8, 9, 12, 0, tzinfo=timezone.utc),
        updated_at=datetime(2026, 8, 9, 12, 30, tzinfo=timezone.utc),
        due_date=None,
    )
    base.update(overrides)
    return SimpleNamespace(**base)


@pytest.fixture
def repo():
    """A repo double that enforces TodoRepository's REAL method signatures."""
    return create_autospec(TodoRepository, instance=True)


@pytest.fixture
def client(repo):
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = lambda: CLAIMS
    app.dependency_overrides[get_todo_repository] = lambda: repo
    return TestClient(app)


def test_pages_query_param_shape_reaches_the_real_repo_signature(client, repo):
    """PUT ?title=... — the exact shape the page's saveTodoTitle() sends —
    resolves into the route and hits the repo with the real signature."""
    repo.get_todo_by_id.return_value = _stored_todo()
    repo.update_todo.return_value = _stored_todo(title="Renamed")

    resp = client.put("/api/v1/todos/t1", params={"title": "Renamed"})

    assert resp.status_code == 200
    # Domain model stores the title in `text`; the repo routes `text` to the
    # parent ItemDB table — the updates dict must speak the repo's field names.
    repo.update_todo.assert_awaited_once_with("t1", {"text": "Renamed"}, owner_id="user-abc")
    assert resp.json()["title"] == "Renamed"


def test_query_param_shape_survives_titles_needing_url_encoding(client, repo):
    """The page encodeURIComponent()s the title; FastAPI must decode it back
    verbatim (spaces, &, unicode)."""
    tricky = "Fix A & B — café ½"
    repo.get_todo_by_id.return_value = _stored_todo()
    repo.update_todo.return_value = _stored_todo(title=tricky)

    resp = client.put("/api/v1/todos/t1", params={"title": tricky})

    assert resp.status_code == 200
    repo.update_todo.assert_awaited_once_with("t1", {"text": tricky}, owner_id="user-abc")


def test_json_body_title_is_silently_dropped_so_the_page_must_not_send_it(client, repo):
    """Documents the trap this route's shape creates: a JSON body {"title"}
    is ignored by FastAPI (no body model), the updates dict arrives EMPTY,
    and the response still says 200 — a client using this shape would toast
    success while changing nothing (#1541's lie). The template test asserts
    the page uses the query-param shape instead."""
    repo.get_todo_by_id.return_value = _stored_todo()
    repo.update_todo.return_value = _stored_todo()  # unchanged

    resp = client.put("/api/v1/todos/t1", json={"title": "Renamed"})

    assert resp.status_code == 200
    repo.update_todo.assert_awaited_once_with("t1", {}, owner_id="user-abc")
    assert resp.json()["title"] == "Ship it", "title must be unchanged — the body was never read"


def test_refused_update_surfaces_as_500_through_http_layer(client, repo):
    """The page's honest-error path depends on !response.ok arriving — a repo
    refusal must produce a real error status, not a fabricated success."""
    repo.get_todo_by_id.return_value = _stored_todo()
    repo.update_todo.return_value = None

    resp = client.put("/api/v1/todos/t1", params={"title": "Renamed"})

    assert resp.status_code == 500
