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
