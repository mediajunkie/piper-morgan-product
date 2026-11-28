"""Issue 2475 (xian's sitting 2026-11-27; Arch 01M8GD84TF; CXO 01M8GD9B2K and 01M8GDZHWM;
HOST 01M8GDBE55).

1. Test All tested every service in the registry. The page then wrote to a status line
   that a not-in-this-beta card does not have, threw, and showed "Couldn't test" to every
   beta account. Test All now tests ``offered_connectors()`` only, and the page skips a
   result whose card has no status line.
2. The headline counted a leftover connection to a service outside the offered set
   ("Needs attention, 2 of 3" with both beta services passing). It counts offered
   services only.
3. The GitHub card says "Connected as {login}." and nothing more; the wrong-account hint
   is visible text in the Disconnect dialog and the Disconnect button's title.

Layers: the routes called directly; the page's own script under node through
``scripts/card_state_file.py`` (skipped without ``node``). Not a browser.
"""

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from services.integrations import integration_status_service as status_service
from services.integrations.principal_test_results import PrincipalTestResultStore
from services.mcp.consumer.github_adapter import GitHubCredential
from web.api.routes import integrations as routes
from web.api.routes.integrations import IntegrationStatus, summarize_integrations

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

import card_state_file as cards  # noqa: E402

needs_node = pytest.mark.skipif(cards.node_missing_is_a_skip(), reason="node not on PATH")
_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"
USER = SimpleNamespace(sub="user-2475")
HINT = "Not the right account? Disconnect, then connect again."


def _named(name: str, status: str) -> IntegrationStatus:
    return IntegrationStatus(
        name=name, display_name=name.title(), status=status, status_message="", can_test=True
    )


# --- 1. Test All tests what this host offers -----------------------------------------


@pytest.mark.asyncio
async def test_test_all_tests_offered_services_only_and_in_registry_order():
    asked = []

    async def check(name, current_user=None):
        asked.append(name)
        return routes.ConnectionTestResponse(integration=name, success=True, message="ok")

    with patch.object(routes, "check_integration_connection", new=check):
        replies = await routes.check_all_connections(current_user=USER)
    offered = status_service.offered_connectors()
    assert asked == [name for name in routes.INTEGRATION_REGISTRY if name in offered]
    assert [r.integration for r in replies] == asked
    assert set(asked) == {"github", "calendar"}
    assert "notion" not in asked and "slack" not in asked


@pytest.mark.asyncio
async def test_test_all_follows_the_one_offered_set_on_staging(monkeypatch):
    """No second list (Arch): staging's extra connector is tested there and only there."""
    monkeypatch.setenv("FLY_APP_NAME", status_service.STAGING_APP_NAME)
    asked = []

    async def check(name, current_user=None):
        asked.append(name)
        return routes.ConnectionTestResponse(integration=name, success=True, message="ok")

    with patch.object(routes, "check_integration_connection", new=check):
        await routes.check_all_connections(current_user=USER)
    assert set(asked) == set(status_service.offered_connectors())
    assert set(asked) - {"github", "calendar"} == set(
        status_service.STAGING_ONLY_OFFERED_CONNECTORS
    )


def test_the_route_reads_offered_connectors_and_keeps_no_list_of_its_own():
    source = (ROOT / "web/api/routes/integrations.py").read_text()
    body = source[source.index("async def check_all_connections") :]
    body = body[: body.index("\n\n\n")]
    assert "offered_connectors()" in body
    assert "BETA_OFFERED_CONNECTORS" not in source


# --- 2. the headline counts what this host offers ------------------------------------


def test_a_leftover_failed_slack_is_not_an_issue_when_both_beta_services_pass():
    """xian's screen: GitHub and Calendar passing, "Needs attention, 2 of 3"."""
    cards_ = [
        _named("notion", "not_configured"),
        _named("slack", "failed"),
        _named("github", "healthy"),
        _named("calendar", "healthy"),
    ]
    overall, headline, summary, working, connected = summarize_integrations(cards_)
    assert (overall, headline) == ("healthy", "All Systems Healthy")
    assert summary == "2 of 2 connected integrations working"
    assert (working, connected) == (2, 2)


def test_only_a_leftover_connection_is_nothing_connected():
    cards_ = [_named("slack", "failed"), _named("github", "not_configured")]
    assert summarize_integrations(cards_)[:3] == ("none", "Nothing connected yet", "")


def test_an_offered_failure_is_still_counted_and_the_leftover_is_not():
    cards_ = [_named("slack", "failed"), _named("github", "failed"), _named("calendar", "healthy")]
    overall, headline, summary, *_ = summarize_integrations(cards_)
    assert (overall, headline) == ("degraded", "Needs attention")
    assert summary == "1 of 2 checked integrations working"


def test_staging_counts_its_extra_connector(monkeypatch):
    monkeypatch.setenv("FLY_APP_NAME", status_service.STAGING_APP_NAME)
    overall, headline, summary, *_ = summarize_integrations([_named("notion", "failed")])
    assert headline == "Needs attention" and summary == "0 of 1 checked integrations working"


# --- 3. the GitHub card's words -------------------------------------------------------


async def _github_card(login="octo-example", result=True):
    store = PrincipalTestResultStore()
    if result is not None:
        store.record_test_result(USER.sub, "github", ok=result, error="The check said no")
    credential = GitHubCredential(owner_id="u", mcp_server_ref="github", token=None, leg="oauth")
    read_login = AsyncMock(return_value=login) if login else AsyncMock(side_effect=RuntimeError())
    meta = {"display_name": "GitHub", "configure_url": "/settings/integrations/github"}
    with (
        patch(f"{_ADAPTER}.resolve_credential", new=AsyncMock(return_value=credential)),
        patch(f"{_ADAPTER}.account_login", new=read_login),
        patch.object(routes, "_get_test_result_store", lambda: store),
    ):
        return await routes._github_card(meta, USER.sub)


@pytest.mark.asyncio
@pytest.mark.parametrize("result", (True, None, False))
async def test_the_card_names_the_login_whenever_it_is_known(result):
    """HOST's condition 1: the login is what catches a wrong account."""
    card = await _github_card(result=result)
    assert card.status_message == "Connected as octo-example."
    assert HINT not in card.status_message
    assert card.disconnect_hint == HINT


@pytest.mark.asyncio
async def test_the_no_login_card_is_unchanged():
    """HOST's condition 3."""
    card = await _github_card(login=None)
    assert card.status_message == "Connected."


def test_the_hint_is_one_constant_and_cxos_words():
    assert routes.GITHUB_WRONG_ACCOUNT_HINT == HINT
    assert routes._GITHUB_CARD_CONNECTED_AS == "Connected as {login}."
    source = (ROOT / "templates/integrations.html").read_text()
    assert "Not the right account" not in source  # from the card payload, never typed there


# --- the page's own script, under node ------------------------------------------------


@pytest.fixture(scope="module")
def text():
    return cards.build()


def _section(text, key):
    start = text.index(f"State key: `{key}`")
    end = text.find("\n## ", start)
    return text[start:] if end == -1 else text[start:end]


@needs_node
def test_test_all_on_this_betas_page_shows_a_count_never_couldnt_test(text):
    row = _section(text, "test-all-beta-pass")
    assert "- Toast (success): **All Tests Passed**. 2 of 2 connections successful" in row
    assert "- Header after the page redraws it: **All Systems Healthy**. 2 of 2 connected" in row
    assert "Couldn't test" not in row and "Needs attention" not in row
    # The leftover Slack card keeps its own words and is left alone by Test All.
    slack = row[row.index("### slack") : row.index("### calendar")]
    assert "this card has no status line, and Test All leaves it alone" in slack
    assert "You connected Slack earlier." in slack
    nothing = _section(text, "test-all-beta-nothing")
    assert "- Toast (info): **Nothing to test yet**. Connect an integration first." in nothing
    assert "- Header after the page redraws it: **Nothing connected yet**." in nothing
    assert "Couldn't test" not in nothing


@needs_node
def test_the_page_skips_a_result_whose_card_has_no_status_line():
    """The page's own guard, apart from the route's: a reply that names a card drawn
    without a status line (an older server, a cached page) is skipped, the rest are
    drawn, and the toast is the count. Before the fix this threw into "Couldn't test"."""
    user_id = cards._setup()
    scenario = next(s for s in cards.test_all_clicks() if s.key == "test-all-beta-pass")
    tested, payload = cards.run_routes(user_id, scenario, test=cards.TEST_ALL)
    stray = {
        "integration": "notion",
        "success": False,
        "connected": False,
        "check_ran": True,
        "message": "Notion isn't connected for your account.",
    }
    pressed = cards.draw(payload, scenario, test=(cards.TEST_ALL, [stray, *tested]))
    assert [t["title"] for t in pressed["toasts"]] == ["All Tests Passed"]
    assert pressed["lines"]["notion"] is None
    assert pressed["lines"]["calendar"]["line"]


def test_the_guard_is_a_skip_not_a_catch_all():
    """Arch: one result is skipped; the loop is not wrapped in a catch of its own."""
    source = (ROOT / "templates/integrations.html").read_text()
    loop = source[source.index("for (const result of results) {") :]
    loop = loop[: loop.index("// CXO 2026-11-18: a card with nothing connected")]
    assert "if (!dot || !statusEl) continue;" in loop
    assert "catch (" not in loop and "try {" not in loop


@needs_node
def test_the_disconnect_dialog_and_button_carry_the_hint(text):
    """HOST's condition 2: visible text in the dialog; the title repeats it."""
    dialogs = _section(text, "dialogs-github-app")
    github = dialogs[dialogs.index("### Disconnect on github") :]
    github = github[: github.index("### Disconnect on calendar")]
    does = "I'll disconnect GitHub. The Piper GitHub app stays installed"
    assert does in github and f"  > {HINT}" in github
    assert github.index(does) < github.index(HINT)  # under the line that says what it does
    # A saved token has no account to get wrong: no hint there.
    token = _section(text, "dialogs-connected")
    token = token[
        token.index("### Disconnect on github") : token.index("### Disconnect on calendar")
    ]
    assert HINT not in token
    healthy = _section(text, "github-app-healthy")
    assert "- Connected as octo-example. Checked just now." in healthy
    assert f"- Hover text on Disconnect: {HINT}" in healthy
