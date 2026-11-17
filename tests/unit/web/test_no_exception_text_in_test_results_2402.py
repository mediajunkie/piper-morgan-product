"""#2402 (Arch and CXO, 2026-11-17): an exception's text never reaches a Test's result,
a stored record, a response field or a card. It can quote a URL, a header or a remote
service's reply; here it holds a made-up token shape so a leak is easy to see.

Layer: the route functions called directly, each made to raise at its first outside
call. Nothing here is served and nothing calls a provider.
"""

import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from services.integrations.principal_test_results import PrincipalTestResultStore
from tests.utils.made_up_credentials import github_pat, joined
from web.api.routes import integrations as integ

SECRET = github_pat("a token an exception might quote")
BOOM = RuntimeError(f"GET https://example.invalid/x?token={SECRET} failed: <b>remote reply</b>")
USER = SimpleNamespace(sub="user-2402")
WRITTEN = {
    "success": False,
    "error": integ.CHECK_FAILED_MESSAGE,
    "error_type": "connection_failed",
}


def _raises_at_first_call(name):
    """A patch that makes ``_test_<name>`` raise BOOM at its first outside call."""
    if name == "notion":
        service = MagicMock()
        service.aget_config = AsyncMock(side_effect=BOOM)
        return patch(
            "services.integrations.notion.config_service.NotionConfigService",
            return_value=service,
        )
    if name == "slack":
        service = MagicMock()
        service.get_config = MagicMock(side_effect=BOOM)
        return patch(
            "services.integrations.slack.config_service.SlackConfigService", return_value=service
        )
    if name == "github":
        return patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.resolve_credential",
            new=AsyncMock(side_effect=BOOM),
        )
    keychain = MagicMock()
    keychain.aread_secret = AsyncMock(side_effect=BOOM)
    return patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain)


NAMES = ("notion", "slack", "github", "calendar")
# Not the bare names: tests/conftest.py skips a test whose keyword is "github" when no
# GitHub token is set, and a bare parametrize id is a keyword.
IDS = [f"test-{n}" for n in NAMES]


@pytest.mark.asyncio
@pytest.mark.parametrize("name", NAMES, ids=IDS)
async def test_a_test_function_that_raises_returns_the_written_line_only(name):
    with _raises_at_first_call(name):
        out = await getattr(integ, f"_test_{name}")("u1")
    assert out == WRITTEN
    assert SECRET not in json.dumps(out)


@pytest.mark.asyncio
async def test_the_dispatcher_that_raises_returns_the_written_line_only():
    with patch.object(integ, "_test_notion", AsyncMock(side_effect=BOOM)):
        out = await integ._test_integration("notion", user_id="u1")
    assert out == WRITTEN


@pytest.mark.asyncio
@pytest.mark.parametrize("name", NAMES, ids=IDS)
async def test_nothing_of_the_exception_is_stored_returned_or_drawn(name):
    """Through the Test route, then the card the health route builds after it."""
    store = PrincipalTestResultStore()
    with (
        _raises_at_first_call(name),
        patch.object(integ, "_get_test_result_store", lambda: store),
    ):
        reply = await integ.check_integration_connection(name, current_user=USER)
        record = store.get_test_result(USER.sub, name)
        with (
            patch.object(
                integ, "_get_integration_config_status", AsyncMock(return_value="configured")
            ),
            patch.object(integ, "_github_card", AsyncMock(return_value=None)),
        ):
            card = await integ._check_integration_health(
                name, integ.INTEGRATION_REGISTRY[name], user_id=USER.sub
            )
    assert reply.success is False and reply.message == integ.CHECK_FAILED_MESSAGE
    assert reply.error is None
    assert record is None  # a check that couldn't run is not a failed Test (#2151)
    for text in (reply.model_dump_json(), card.model_dump_json()):
        assert SECRET not in text and "remote reply" not in text and "example.invalid" not in text


@pytest.mark.asyncio
async def test_test_all_says_the_written_line_when_a_single_test_raises():
    with patch.object(integ, "check_integration_connection", AsyncMock(side_effect=BOOM)):
        replies = await integ.check_all_connections(current_user=USER)
    assert len(replies) == len(integ.INTEGRATION_REGISTRY)
    for reply in replies:
        assert reply.message == integ.CHECK_FAILED_MESSAGE and reply.error is None
        assert SECRET not in reply.model_dump_json()


@pytest.mark.asyncio
async def test_the_health_routes_error_names_no_cause():
    with patch.object(integ, "_check_integration_health", AsyncMock(side_effect=BOOM)):
        with pytest.raises(HTTPException) as raised:
            await integ.get_integrations_health(current_user=USER)
    assert raised.value.status_code == 500 and raised.value.detail == "Health check failed"


class _SlackSession:
    """Slack's auth.test answering ok=false with its own error word."""

    def __init__(self, word):
        self._word = word

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    def get(self, *a, **k):
        return self

    async def json(self):
        return {"ok": False, "error": self._word}


@pytest.mark.asyncio
async def test_slacks_own_error_word_is_not_stored_or_returned():
    """Slack's reply is a remote service's text: logged, never the card's line."""
    service = MagicMock()
    service.get_config = MagicMock(
        return_value=MagicMock(bot_token=joined("xo", "xb-", "made-up-for-2402"))
    )
    word = f"invalid_auth <b>{SECRET}</b>"
    with (
        patch(
            "services.integrations.slack.config_service.SlackConfigService", return_value=service
        ),
        patch("aiohttp.ClientSession", return_value=_SlackSession(word)),
    ):
        out = await integ._test_slack("u1")
    assert out == {
        "success": False,
        "error": "Token invalid or expired",
        "error_type": "token_invalid",
    }


@pytest.mark.asyncio
async def test_github_with_no_account_does_not_say_token():
    out = await integ._test_github(None)
    assert out["error_type"] == "not_configured"
    assert out["error"] == (
        "GitHub isn't connected. Open Settings, under Integrations, to connect it."
    )


def test_the_only_exception_text_in_the_file_goes_to_a_log_call():
    source = Path(integ.__file__).read_text(encoding="utf-8").splitlines()
    uses = [line.strip() for line in source if "str(e)" in line or "str(error)" in line]
    assert uses and all(line.startswith(("logger.", "error=str(error)")) for line in uses), uses
