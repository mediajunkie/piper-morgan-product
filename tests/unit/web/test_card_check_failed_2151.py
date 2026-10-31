"""#2151 route group 1 (Arch 10-24 09:09): an integration card's Test that couldn't run.

- ``_test_notion``: only 401/403 is an invalid key; a 5xx or rate limit is a check that
  couldn't run (the #2125 shape: it said "API key invalid or expired").
- ``check_integration_connection``: a check that couldn't run answers CHECK_FAILED_MESSAGE
  and records NO failed result, so the card never turns "failed" over it.
(The calendar Test's two cases are in test_integrations.py; config status reading the
keychain with provenance is in test_iss_status_check_failed_2151.py.)
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes import integrations as integ


class _Resp:
    def __init__(self, status):
        self.status = status

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


class _Session:
    def __init__(self, status):
        self._status = status

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    def get(self, *a, **k):
        return _Resp(self._status)


def _notion_with_key():
    service = MagicMock()
    service.get_config = MagicMock(return_value=MagicMock(api_key="fake-notion-key"))
    return patch(
        "services.integrations.notion.config_service.NotionConfigService", return_value=service
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [500, 502, 503, 429])
async def test_notion_a_server_error_is_a_check_that_couldnt_run(status):
    with _notion_with_key(), patch("aiohttp.ClientSession", return_value=_Session(status)):
        out = await integ._test_notion("u1")
    assert out == {
        "success": False,
        "error": integ.CHECK_FAILED_MESSAGE,
        "error_type": "check_failed",
    }


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [401, 403])
async def test_notion_a_rejected_key_is_still_an_invalid_key(status):
    with _notion_with_key(), patch("aiohttp.ClientSession", return_value=_Session(status)):
        out = await integ._test_notion("u1")
    assert out["error_type"] == "api_key_invalid"


@pytest.mark.asyncio
async def test_a_check_that_couldnt_run_records_no_failed_result():
    store = MagicMock()
    with (
        patch.object(integ, "_get_test_result_store", return_value=store),
        patch.object(
            integ,
            "_test_integration",
            new=AsyncMock(
                return_value={
                    "success": False,
                    "error": integ.CHECK_FAILED_MESSAGE,
                    "error_type": "check_failed",
                }
            ),
        ),
    ):
        resp = await integ.check_integration_connection("notion", current_user=MagicMock(sub="u1"))
    assert resp.success is False
    assert resp.message == integ.CHECK_FAILED_MESSAGE
    store.record_test_result.assert_not_called()


# ── Route group 4: the Notion key validator and save ──


def _notion_error(code: str, status: int):
    import httpx
    from notion_client.errors import APIErrorCode, APIResponseError

    response = httpx.Response(status, request=httpx.Request("GET", "https://api.notion.com"))
    return APIResponseError(response, "fake notion error", APIErrorCode(code))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "code,status", [("internal_server_error", 500), ("service_unavailable", 503)]
)
async def test_a_notion_server_error_is_not_an_invalid_key(code, status):
    from web.api.routes.setup import (
        NOTION_CHECK_FAILED_MESSAGE,
        validate_notion_key_and_get_workspace,
    )

    client = MagicMock()
    client.users.me = MagicMock(side_effect=_notion_error(code, status))
    with patch("notion_client.Client", return_value=client):
        ok, workspace, msg = await validate_notion_key_and_get_workspace("fake-notion-key")
    assert (ok, workspace, msg) == (False, None, NOTION_CHECK_FAILED_MESSAGE)
    assert "Invalid" not in msg


@pytest.mark.asyncio
async def test_an_unauthorized_key_is_still_invalid():
    from web.api.routes.setup import validate_notion_key_and_get_workspace

    client = MagicMock()
    client.users.me = MagicMock(side_effect=_notion_error("unauthorized", 401))
    with patch("notion_client.Client", return_value=client):
        ok, _w, msg = await validate_notion_key_and_get_workspace("fake-notion-key")
    assert ok is False and msg.startswith("Invalid API key")


def test_the_save_answers_503_with_the_line_not_400():
    import uuid

    from fastapi.testclient import TestClient

    from services.auth.container import AuthContainer
    from web.api.routes.setup import NOTION_CHECK_FAILED_MESSAGE
    from web.app import app

    c = TestClient(app, follow_redirects=False)
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2151n@example.com", scopes=["user"]
    )
    c.cookies.set("auth_token", token)
    with patch(
        "web.api.routes.setup.validate_notion_key_and_get_workspace",
        new=AsyncMock(return_value=(False, None, NOTION_CHECK_FAILED_MESSAGE)),
    ):
        r = c.post("/api/v1/settings/integrations/notion/save", data={"api_key": "fake-notion-key"})
    assert r.status_code == 503, r.text
    assert r.json()["detail"] == NOTION_CHECK_FAILED_MESSAGE


# ── The calendar card's page: a check that couldn't run renders as that ──


def _sync_fn(body: str, name: str) -> str:
    start = body.index(f"function {name}(")
    i = body.index("{", start)
    depth = 0
    for j in range(i, len(body)):
        if body[j] == "{":
            depth += 1
        elif body[j] == "}":
            depth -= 1
            if depth == 0:
                return body[start : j + 1]
    raise AssertionError(name)


@pytest.mark.skipif(__import__("shutil").which("node") is None, reason="node not on PATH")
def test_the_calendar_card_says_it_couldnt_check():
    import json
    import subprocess
    from pathlib import Path

    from web.api.routes.settings_integrations import CALENDAR_STATUS_CHECK_FAILED_LINE

    body = (Path(__file__).resolve().parents[3] / "templates/settings_calendar.html").read_text()
    script = (
        "const els = {};\n"
        "const document = { getElementById(id) { if (!els[id]) els[id] = { id, className: '',"
        " textContent: '', innerHTML: '', style: {} }; return els[id]; } };\n"
        "let listLoaded = false; function loadCalendarList() { listLoaded = true; }\n"
        + _sync_fn(body, "updateStatusUI")
        + "\nupdateStatusUI(JSON.parse(process.argv[1]));\n"
        "process.stdout.write(JSON.stringify({ title: els['status-title'].textContent,"
        " subtitle: els['status-subtitle'].textContent,"
        " selection: (els['calendar-selection-card'] || {style: {}}).style.display,"
        " listLoaded }));\n"
    )
    data = {
        "check_failed": True,
        "configured": None,
        "valid": None,
        "error": CALENDAR_STATUS_CHECK_FAILED_LINE,
    }
    res = subprocess.run(
        ["node", "-e", script, json.dumps(data)], capture_output=True, text=True, timeout=30
    )
    assert res.returncode == 0, res.stderr
    out = json.loads(res.stdout)
    assert out["title"] == "Couldn't check"
    assert out["subtitle"] == CALENDAR_STATUS_CHECK_FAILED_LINE
    assert out["selection"] == "none" and out["listLoaded"] is False


# ── The GitHub card: no host account on a hosted deploy; a failed lookup is "couldn't check" ──


def _user(sub="u-gh"):
    return MagicMock(sub=sub)


@pytest.mark.asyncio
async def test_hosted_github_card_never_shows_the_host_token():
    from web.api.routes import settings_integrations as si

    config = MagicMock()
    config.get_authentication_token = MagicMock(return_value="fake-host-env-token")
    with (
        patch(
            "services.integrations.integration_status_service.IntegrationStatusService.get_status",
            new=AsyncMock(return_value={"configured": False, "check_failed": False}),
        ),
        patch("services.infrastructure.deployment.is_hosted_deployment", return_value=True),
        patch(
            "services.integrations.github.config_service.GitHubConfigService", return_value=config
        ),
    ):
        out = await si.get_github_settings(current_user=_user())
    assert out == {"configured": False, "valid": False, "username": None, "error": None}
    config.get_authentication_token.assert_not_called()


@pytest.mark.asyncio
async def test_local_github_card_keeps_the_legacy_env_fallback():
    from web.api.routes import settings_integrations as si

    config = MagicMock()
    config.get_authentication_token = MagicMock(return_value="fake-local-env-token")
    with (
        patch(
            "services.integrations.integration_status_service.IntegrationStatusService.get_status",
            new=AsyncMock(return_value={"configured": False, "check_failed": False}),
        ),
        patch("services.infrastructure.deployment.is_hosted_deployment", return_value=False),
        patch(
            "services.integrations.github.config_service.GitHubConfigService", return_value=config
        ),
        patch(
            "services.integrations.github.token_validator.verify_github_token",
            new=AsyncMock(return_value={"authenticated": True, "username": "local-me"}),
        ),
    ):
        out = await si.get_github_settings(current_user=_user())
    assert out["configured"] is True and out["username"] == "local-me"


@pytest.mark.asyncio
@pytest.mark.parametrize("how", ["status_check_failed", "raises"])
async def test_github_card_check_that_couldnt_run(how):
    from web.api.routes import settings_integrations as si

    status = (
        AsyncMock(return_value={"configured": False, "check_failed": True})
        if how == "status_check_failed"
        else AsyncMock(side_effect=RuntimeError("fake"))
    )
    with patch(
        "services.integrations.integration_status_service.IntegrationStatusService.get_status",
        new=status,
    ):
        out = await si.get_github_settings(current_user=_user())
    assert out["check_failed"] is True
    assert out["error"] == si.GITHUB_STATUS_CHECK_FAILED_LINE


# ── Arch 10-24 12:32, gap 1: a Test that raises is a check that couldn't run ──


@pytest.mark.asyncio
async def test_a_connection_failed_test_records_nothing_and_says_couldnt_check():
    store = MagicMock()
    with (
        patch.object(integ, "_get_test_result_store", return_value=store),
        patch.object(
            integ,
            "_test_integration",
            new=AsyncMock(
                return_value={
                    "success": False,
                    "error": "fake: Cannot connect to host",
                    "error_type": "connection_failed",
                }
            ),
        ),
    ):
        resp = await integ.check_integration_connection("notion", current_user=MagicMock(sub="u1"))
    assert resp.message == integ.CHECK_FAILED_MESSAGE
    assert "internet" not in resp.message.lower()
    store.record_test_result.assert_not_called()


@pytest.mark.asyncio
async def test_a_test_that_raises_records_nothing_and_shows_no_exception_text():
    store = MagicMock()
    with (
        patch.object(integ, "_get_test_result_store", return_value=store),
        patch.object(
            integ,
            "_test_integration",
            new=AsyncMock(side_effect=RuntimeError("fake secret-ish detail")),
        ),
    ):
        resp = await integ.check_integration_connection("slack", current_user=MagicMock(sub="u1"))
    assert resp.message == integ.CHECK_FAILED_MESSAGE
    assert "fake secret-ish detail" not in (resp.message + str(resp.error or ""))
    store.record_test_result.assert_not_called()


@pytest.mark.asyncio
async def test_an_unreachable_github_test_records_nothing():
    """Arch 15:29 gap C: a transport degrade is a check that couldn't run."""
    store = MagicMock()
    with (
        patch.object(integ, "_get_test_result_store", return_value=store),
        patch.object(
            integ,
            "_test_integration",
            new=AsyncMock(
                return_value={"success": False, "error": "fake", "error_type": "unreachable"}
            ),
        ),
    ):
        resp = await integ.check_integration_connection("github", current_user=MagicMock(sub="u1"))
    assert resp.message == integ.CHECK_FAILED_MESSAGE
    store.record_test_result.assert_not_called()


@__import__("pytest").fixture(autouse=True)
def _all_connectors_offered_2237(monkeypatch):
    """These tests exercise the Slack/Notion route bodies themselves; #2237's guard
    (pinned in test_offered_connector_guard_2237.py) is stepped aside here."""
    from services.integrations import integration_status_service as svc

    monkeypatch.setattr(
        svc,
        "BETA_OFFERED_CONNECTORS",
        {"github": "GitHub", "slack": "Slack", "calendar": "Google Calendar", "notion": "Notion"},
    )
