"""#2401 (CXO 2026-11-17, from the card-state file): a failed Test on a sign-in GitHub
card gives the failure its own line; a card whose credential lookup failed offers Test
only.

Layers: the route's card builders called directly; the page's own script under node
through ``scripts/card_state_file.py`` (skipped without ``node``). Not a browser.
"""

import shutil
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from services.integrations.principal_test_results import PrincipalTestResultStore
from services.mcp.consumer.github_adapter import GitHubCredential
from web.api.routes import integrations as routes

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

import card_state_file as cards  # noqa: E402

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")
_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"
USER = "user-2401"
META = {"display_name": "GitHub", "configure_url": "/settings/integrations/github"}
QUESTION = "Not the right account?"


async def _github_card(result, login="octo-example"):
    store = PrincipalTestResultStore()
    if result is not None:
        store.record_test_result(USER, "github", ok=result, error="The check said no")
    credential = GitHubCredential(owner_id="u", mcp_server_ref="github", token=None, leg="oauth")
    read_login = AsyncMock(return_value=login) if login else AsyncMock(side_effect=RuntimeError())
    with (
        patch(f"{_ADAPTER}.resolve_credential", new=AsyncMock(return_value=credential)),
        patch(f"{_ADAPTER}.account_login", new=read_login),
        patch.object(routes, "_get_test_result_store", lambda: store),
    ):
        return await routes._github_card(META, USER)


@pytest.mark.asyncio
async def test_a_failed_test_names_the_account_and_gives_the_failure_its_own_line():
    card = await _github_card(False)
    assert card.status == "failed"
    assert card.status_message == "Connected as octo-example."
    assert card.error_line == "The check said no" and card.error == "The check said no"
    assert QUESTION not in card.status_message


@pytest.mark.asyncio
async def test_a_failed_test_with_no_login_still_gets_the_line():
    card = await _github_card(False, login=None)
    assert card.status_message == "Connected." and card.error_line == "The check said no"


@pytest.mark.asyncio
@pytest.mark.parametrize("result", (True, None))
async def test_passed_and_never_tested_keep_the_question_and_have_no_error_line(result):
    card = await _github_card(result)
    assert QUESTION in card.status_message
    assert card.error_line is None and card.error is None


@pytest.mark.asyncio
@pytest.mark.parametrize("name", ("github", "notion", "slack", "calendar"))
@pytest.mark.parametrize("how", ("lookup_says_unknown", "lookup_raises"))
async def test_a_failed_credential_lookup_is_test_only(name, how):
    meta = {"display_name": name.title(), "configure_url": f"/settings/integrations/{name}"}
    lookup = (
        AsyncMock(return_value="unknown")
        if how == "lookup_says_unknown"
        else AsyncMock(side_effect=RuntimeError("down"))
    )
    with (
        patch.object(routes, "_get_integration_config_status", lookup),
        patch.object(routes, "_github_card", AsyncMock(side_effect=RuntimeError("down"))),
    ):
        card = await routes._check_integration_health(name, meta, user_id=USER)
    assert card.status == "unknown" and card.status_message == routes.CHECK_FAILED_MESSAGE
    assert card.action == "test_only" and card.can_test is True and card.show_test is True


@pytest.mark.asyncio
async def test_not_configured_and_connected_cards_are_not_test_only():
    meta = {"display_name": "Slack", "configure_url": "/settings/integrations/slack"}
    for answer in ("not_configured", "configured"):
        with (
            patch.object(routes, "_get_integration_config_status", AsyncMock(return_value=answer)),
            patch.object(routes, "_get_test_result_store", PrincipalTestResultStore),
        ):
            card = await routes._check_integration_health("slack", meta, user_id=USER)
        assert card.action is None, answer


# --- the page's own script, under node ------------------------------------------------


@pytest.fixture(scope="module")
def drawn():
    user_id = cards._setup()
    return {
        s.key: cards.draw(cards.health_payload(user_id, s), s)
        for s in cards.scenarios()
        if s.key in ("check-failed", "github-app-failed", "github-app-healthy", "failed")
    }


# The ids are not the bare card names: tests/conftest.py skips any test with the keyword
# "github" when no GitHub token is set, and a bare id is a keyword.
@needs_node
@pytest.mark.parametrize("name", cards.CARDS, ids=[f"card-{n}" for n in cards.CARDS])
def test_a_check_failed_card_draws_test_and_nothing_else(drawn, name):
    card = cards.read_card(drawn["check-failed"], name)
    assert [c["label"] for c in card["controls"]] == ["Test"]
    assert card["controls"][0]["disabled"] == ""
    assert "Couldn't check this just now. Press Test to try again." in card["lines"]


@needs_node
def test_the_failed_github_card_draws_two_lines_and_keeps_its_controls(drawn):
    card = cards.read_card(drawn["github-app-failed"], "github")
    assert card["lines"][-2:] == [
        "Connected as octo-example.",
        f"{cards.SAMPLE_ERROR}. Checked just now. [error style]",
    ]
    assert [c["label"] for c in card["controls"]] == ["Test", "Disconnect", "Manage repositories"]


@needs_node
def test_the_passed_github_card_and_the_other_failed_cards_are_unchanged(drawn):
    passed = cards.read_card(drawn["github-app-healthy"], "github")
    assert passed["lines"][-1] == (
        "Connected as octo-example. Not the right account? Disconnect, then connect again. "
        "Checked just now."
    )
    for name in ("notion", "slack", "calendar"):
        card = cards.read_card(drawn["failed"], name)
        assert card["lines"][-1] == f"{cards.SAMPLE_ERROR}. Checked just now. [error style]"
