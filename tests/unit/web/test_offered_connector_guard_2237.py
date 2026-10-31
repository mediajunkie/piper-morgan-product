"""#2237 (server half): every connect / OAuth-start / credential-save route for a
connector outside ``BETA_OFFERED_CONNECTORS`` refuses with one honest 409 and does no
work: no OAuth start, no key validation, no write. GitHub and Calendar are untouched.
"""

from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from services.integrations import integration_status_service as svc
from web.api.routes.setup import require_setup_incomplete
from web.app import app

SETTINGS = "/api/v1/settings/integrations"
SETUP = "/api/v1/setup"
SLACK_MSG = "Slack isn't available in this beta yet."
NOTION_MSG = "Notion isn't available in this beta yet."


@pytest.fixture(scope="module")
def client():
    app.dependency_overrides[require_setup_incomplete] = lambda: None
    c = TestClient(app, follow_redirects=False)
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2237@example.com", scopes=["user"]
    )
    c.cookies.set("auth_token", token)
    yield c
    app.dependency_overrides.pop(require_setup_incomplete, None)


# (method, path, kwargs, connector). Slack/Notion are not offered; each must refuse.
GUARDED = [
    ("get", f"{SETTINGS}/slack/connect", {}, "slack"),
    ("get", f"{SETTINGS}/slack/authorize", {}, "slack"),
    ("post", f"{SETTINGS}/notion/save", {"data": {"api_key": "ntn_x"}}, "notion"),
    ("get", f"{SETUP}/slack/oauth/start", {}, "slack"),
    ("get", f"{SETTINGS}/slack/callback", {"params": {"code": "c", "state": "s"}}, "slack"),
    ("get", f"{SETUP}/slack/oauth/callback", {"params": {"code": "c", "state": "s"}}, "slack"),
    (
        "post",
        f"{SETUP}/slack-credentials",
        {"json": {"client_id": "a", "client_secret": "b"}},
        "slack",
    ),
    (
        "post",
        f"{SETUP}/validate-key",
        {"json": {"provider": "notion", "api_key": "ntn_x"}},
        "notion",
    ),
]
MESSAGES = {"slack": SLACK_MSG, "notion": NOTION_MSG}

# Everything a guarded route could reach if it ran.
SIDE_EFFECTS = [
    "services.integrations.slack.oauth_handler.SlackOAuthHandler",
    "services.integrations.slack.oauth_handler.RedisFactory",
    "web.api.routes.setup.validate_notion_key_and_get_workspace",
    "services.integrations.integration_config_service.IntegrationConfigService",
    "services.security.user_api_key_service.UserAPIKeyService",
    "services.infrastructure.keychain_service.KeychainService",
]


@pytest.mark.parametrize("method,path,kwargs,name", GUARDED)
def test_not_offered_connector_is_refused_with_no_work(client, method, path, kwargs, name):
    patches = [patch(t, new=MagicMock(side_effect=AssertionError(t))) for t in SIDE_EFFECTS]
    for p in patches:
        p.start()
    try:
        r = getattr(client, method)(path, **kwargs)
    finally:
        for p in patches:
            p.stop()
    assert r.status_code == 409, (path, r.status_code, r.text)
    assert r.json()["detail"] == MESSAGES[name]
    assert r.json()["message"] == MESSAGES[name]  # clients render it as an info toast
    assert "location" not in r.headers  # no OAuth redirect


def test_validator_not_called_for_notion_save_and_validate_key(client):
    with patch("web.api.routes.setup.validate_notion_key_and_get_workspace", new=AsyncMock()) as v:
        client.post(f"{SETTINGS}/notion/save", data={"api_key": "ntn_x"})
        client.post(f"{SETUP}/validate-key", json={"provider": "notion", "api_key": "ntn_x"})
    v.assert_not_called()


def test_slack_oauth_start_not_called(client):
    with patch("services.integrations.slack.oauth_handler.SlackOAuthHandler") as h:
        client.get(f"{SETTINGS}/slack/connect")
        client.get(f"{SETUP}/slack/oauth/start")
    h.assert_not_called()


def _route_src(path: str) -> str:
    import inspect

    path = path.split("?")[0]
    for route in app.routes:
        if getattr(route, "path", "") == path and hasattr(route, "endpoint"):
            return inspect.getsource(route.endpoint)
    raise AssertionError(path)


def test_calendar_and_github_routes_carry_no_guard():
    seen = 0
    for route in app.routes:
        path = getattr(route, "path", "")
        if hasattr(route, "endpoint") and ("/calendar" in path or "/github" in path):
            seen += 1
            assert "refuse_unless_offered" not in _route_src(path), path
    assert seen > 0


def test_calendar_connect_is_not_refused_by_the_guard(client):
    r = client.get(f"{SETTINGS}/calendar/connect")
    assert "isn't available in this beta" not in r.text


def test_admin_app_credential_routes_are_unguarded():
    # CXO: the admin card is unchanged.
    for path in (f"{SETTINGS}/slack/app-credentials", f"{SETTINGS}/slack/app-token"):
        assert "refuse_unless_offered" not in _route_src(path), path


def test_every_guarded_route_calls_the_guard():
    for _, path, _, _ in GUARDED:
        if "validate-key" in path:
            continue
        assert "refuse_unless_offered" in _route_src(path), path


def test_validate_key_for_other_providers_is_not_guarded(client):
    r = client.post(f"{SETUP}/validate-key", json={"provider": "github", "api_key": "x"})
    assert r.status_code != 409


def test_guard_follows_the_constant(client, monkeypatch):
    monkeypatch.setattr(svc, "BETA_OFFERED_CONNECTORS", {"github": "GitHub"})
    r = client.get(f"{SETTINGS}/slack/connect")
    assert r.status_code == 409
    monkeypatch.setattr(svc, "BETA_OFFERED_CONNECTORS", {"github": "GitHub", "slack": "Slack"})
    r = client.get(f"{SETTINGS}/slack/connect")
    assert r.status_code != 409  # offered again: the guard steps aside


def test_disconnect_routes_stay_allowed(client):
    for path in (f"{SETTINGS}/slack/disconnect", f"{SETTINGS}/notion/disconnect"):
        r = client.post(path)
        assert r.status_code != 409, path


def test_setup_complete_does_not_store_a_notion_key():
    src = open("web/api/routes/setup.py").read()
    assert 'if req.notion_key and connector_offered("notion"):' in src


def test_slack_connect_writes_no_oauth_state(client):
    # Arch: the check runs before any OAuth state is stored. The handler's Redis is
    # patched (not the app-wide one, which auth uses) and must not be touched.
    with patch("services.integrations.slack.oauth_handler.RedisFactory") as redis:
        r = client.get(f"{SETTINGS}/slack/connect")
        client.get(f"{SETUP}/slack/oauth/start")
    assert r.status_code == 409
    redis.redis_scope.assert_not_called()


def test_slack_callbacks_refuse_and_store_nothing(client):
    with patch("services.integrations.slack.oauth_handler.SlackOAuthHandler") as handler:
        for path in (f"{SETTINGS}/slack/callback", f"{SETUP}/slack/oauth/callback"):
            r = client.get(path, params={"code": "c", "state": "s"})
            assert r.status_code == 409, path
            assert r.json()["detail"] == SLACK_MSG
    handler.assert_not_called()


def test_one_predicate_is_the_authority():
    assert svc.connector_offered("github") and svc.connector_offered("calendar")
    assert not svc.connector_offered("slack") and not svc.connector_offered("notion")
