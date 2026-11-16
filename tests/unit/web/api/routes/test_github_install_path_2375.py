"""#2375 (xian 2026-11-15; words CXO, mechanism Arch): the way to the GitHub install step.

The install step lives on the GitHub repository page, and the only way there was a grey
"Settings" link on the Integrations card. Now the card's link names what it leads to
("Install the GitHub app" when the App is installed nowhere, "Manage repositories" when
it is installed, "Repositories" when that isn't known), it lands on the repository
section, and the Settings index has a card for the same place (CXO 11-15: first
"Choose repositories" and a text link; both changed after xian's screen read).

Arch's conditions: one installation read through ``_installed_or_degrade``; the route
returns a state and nothing else; any failure is ``unknown`` and the neutral label,
never "install".

Layer: unit. The adapter with a fake installation read, the route called directly, the
card's script under node with stubbed browser objects, and the templates' source. No
page is rendered in a browser, and nothing calls GitHub.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from services.mcp.consumer import github_adapter as gh_mod
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import GitHubCredential, GitHubMCPSpatialAdapter
from services.mcp.consumer.github_app_install import (
    DETAIL_APP_INSTALL_LINK_MISSING,
    DETAIL_APP_NOT_INSTALLED,
    InstallationReadFailed,
    InstalledRepositories,
)
from web.api.routes import settings_integrations as si

_USER = "11111111-1111-1111-1111-111111111111"
ROOT = Path(__file__).resolve().parents[5]
CARDS = (ROOT / "templates/integrations.html").read_text()
INDEX = (ROOT / "templates/settings-index.html").read_text()
GITHUB_PAGE = (ROOT / "templates/settings_github.html").read_text()
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")


def _credential(leg="oauth", app_grant=True):
    return GitHubCredential(
        owner_id=_USER, mcp_server_ref="github", token="access-live", leg=leg, app_grant=app_grant
    )


def _degraded(reason, detail=None):
    return DegradationResponse(reason=reason, user_message="x", detail=detail)


def _adapter(monkeypatch, credential, installed=None):
    adapter = GitHubMCPSpatialAdapter()
    adapter.resolve_credential = (
        AsyncMock(side_effect=credential)
        if isinstance(credential, Exception)
        else AsyncMock(return_value=credential)
    )
    read = (
        AsyncMock(side_effect=installed)
        if isinstance(installed, Exception)
        else AsyncMock(return_value=installed)
    )
    monkeypatch.setattr(gh_mod, "list_installed_repositories", read)
    monkeypatch.setenv("GITHUB_APP_SLUG", "piper-example")
    return adapter, read


@pytest.mark.asyncio
class TestTheInstallState:
    async def test_installed_nowhere_is_none(self, monkeypatch):
        adapter, read = _adapter(monkeypatch, _credential(), InstalledRepositories(installations=0))
        assert await adapter.app_install_state(_USER) == "none"
        read.assert_awaited_once_with("access-live")  # one installation read

    async def test_installed_nowhere_with_no_install_link_is_still_none(self, monkeypatch):
        adapter, _ = _adapter(monkeypatch, _credential(), InstalledRepositories(installations=0))
        monkeypatch.delenv("GITHUB_APP_SLUG")
        degraded = await adapter._installed_or_degrade(_credential())
        assert degraded.detail == DETAIL_APP_INSTALL_LINK_MISSING
        assert await adapter.app_install_state(_USER) == "none"

    async def test_installed_somewhere_is_some(self, monkeypatch):
        installed = InstalledRepositories(
            installations=1, repositories=[{"id": 1, "full_name": "octo/a"}]
        )
        adapter, _ = _adapter(monkeypatch, _credential(), installed)
        assert await adapter.app_install_state(_USER) == "some"

    @pytest.mark.parametrize("status", [None, 403, 500, 502])
    async def test_a_read_that_did_not_answer_is_unknown_never_none(self, monkeypatch, status):
        adapter, _ = _adapter(monkeypatch, _credential(), InstallationReadFailed(status))
        assert await adapter.app_install_state(_USER) == "unknown"

    async def test_a_rejected_grant_is_unknown_and_takes_the_stale_path(self, monkeypatch):
        # Arch: the same truthful read the repository list makes, stale marking included.
        adapter, _ = _adapter(monkeypatch, _credential(), InstallationReadFailed(401))
        adapter._rejected_token_was_replaced = AsyncMock(return_value=False)
        adapter._mark_oauth_binding_stale = AsyncMock()
        assert await adapter.app_install_state(_USER) == "unknown"
        adapter._mark_oauth_binding_stale.assert_awaited_once()

    @pytest.mark.parametrize(
        "credential",
        [_credential(leg="pat", app_grant=False), _credential(leg="oauth", app_grant=False)],
        ids=["personal token", "classic grant"],
    )
    async def test_an_account_without_an_app_grant_is_not_app_with_no_read(
        self, monkeypatch, credential
    ):
        adapter, read = _adapter(monkeypatch, credential, AssertionError("no installation read"))
        assert await adapter.app_install_state(_USER) == "not_app"
        read.assert_not_awaited()

    async def test_not_connected_is_not_app(self, monkeypatch):
        adapter, read = _adapter(
            monkeypatch, _degraded(DegradationReason.CONNECT_REQUIRED), AssertionError("no read")
        )
        assert await adapter.app_install_state(_USER) == "not_app"
        read.assert_not_awaited()

    @pytest.mark.parametrize(
        "reason", [DegradationReason.UNREACHABLE, DegradationReason.STALE_TOKEN]
    )
    async def test_a_credential_that_could_not_be_resolved_is_unknown(self, monkeypatch, reason):
        adapter, read = _adapter(monkeypatch, _degraded(reason), AssertionError("no read"))
        assert await adapter.app_install_state(_USER) == "unknown"
        read.assert_not_awaited()

    @pytest.mark.parametrize("where", ["resolve", "read"])
    async def test_anything_raised_is_unknown(self, monkeypatch, where):
        if where == "resolve":
            adapter, _ = _adapter(monkeypatch, RuntimeError("store down"))
        else:
            adapter, _ = _adapter(monkeypatch, _credential(), RuntimeError("boom"))
        assert await adapter.app_install_state(_USER) == "unknown"

    async def test_the_four_states_are_named_constants(self):
        assert {
            gh_mod.INSTALL_STATE_NONE,
            gh_mod.INSTALL_STATE_SOME,
            gh_mod.INSTALL_STATE_UNKNOWN,
            gh_mod.INSTALL_STATE_NOT_APP,
        } == {"none", "some", "unknown", "not_app"}
        assert DETAIL_APP_NOT_INSTALLED == "app_not_installed"


@pytest.mark.asyncio
class TestTheRoute:
    @staticmethod
    def _claims():
        c = MagicMock()
        c.sub = _USER
        return c

    @pytest.mark.parametrize("state", ["none", "some", "unknown", "not_app"])
    async def test_it_returns_the_state_and_nothing_else(self, monkeypatch, state):
        monkeypatch.setattr(
            GitHubMCPSpatialAdapter, "app_install_state", AsyncMock(return_value=state)
        )
        assert await si.github_install_state(current_user=self._claims()) == {"state": state}

    async def test_a_raise_is_unknown(self, monkeypatch):
        monkeypatch.setattr(
            GitHubMCPSpatialAdapter, "app_install_state", AsyncMock(side_effect=RuntimeError("x"))
        )
        assert await si.github_install_state(current_user=self._claims()) == {"state": "unknown"}


# ── the card's script, run under node ───────────────────────────────────────────────

HARNESS = r"""
const link = { textContent: 'Repositories', className: 'action-btn configure-btn' };
const document = { getElementById: (id) => (id === 'github-repositories-link' ? link : null) };
async function fetch(url) {
  calls.push(url);
  if (RESPONSE === 'throws') throw new Error('network');
  if (RESPONSE === 'not_ok') return { ok: false, json: async () => ({}) };
  return { ok: true, json: async () => RESPONSE };
}
const calls = [];
"""


def _label(response) -> dict:
    start = CARDS.index("  const GITHUB_REPOSITORIES_URL")
    block = CARDS[start : CARDS.index("  function renderIntegrations(", start)]
    js = (
        f"const RESPONSE = {json.dumps(response)};\n"
        + HARNESS
        + block
        + """
(async () => {
  await labelGitHubRepositoriesLink();
  process.stdout.write(JSON.stringify({ text: link.textContent, cls: link.className, calls,
    url: GITHUB_REPOSITORIES_URL, first: GITHUB_LINK_LABELS.unknown }));
})();
"""
    )
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


@needs_node
class TestTheCardsLabel:
    def test_installed_nowhere_names_the_step_and_is_the_primary_button(self):
        r = _label({"state": "none"})
        assert r["text"] == "Install the GitHub app"  # CXO
        assert r["cls"] == "action-btn connect-btn"
        assert r["calls"] == ["/api/v1/settings/integrations/github/install-state"]

    def test_installed_somewhere_says_manage_repositories(self):
        # CXO 11-15 19:16: "Choose repositories" read as a one-time choice.
        r = _label({"state": "some"})
        assert r["text"] == "Manage repositories" and r["cls"] == "action-btn configure-btn"
        assert "Choose repositories" not in CARDS

    @pytest.mark.parametrize(
        "response",
        [
            {"state": "unknown"},
            {"state": "not_app"},
            {"state": "installed"},
            {},
            "not_ok",
            "throws",
        ],
    )
    def test_anything_else_keeps_the_neutral_label(self, response):
        # CXO and Arch: never "install" on a guess, a failure, or a word it doesn't know.
        r = _label(response)
        assert r["text"] == "Repositories" and r["cls"] == "action-btn configure-btn"

    def test_the_label_shown_before_the_answer_is_the_neutral_one(self):
        r = _label({"state": "some"})
        assert r["first"] == "Repositories"
        assert r["url"] == "/settings/integrations/github#repositories"


# ── the cards as the page's own script draws them, run under node ───────────────────
#
# The first build put the link in the branch that draws Slack and Calendar. GitHub's card
# is drawn by the API-key branch, so beta served "Settings" (xian's screen, 2026-11-15).
# The pins above read the label function and the source text; neither drew a card. These
# run the page's whole script and read the HTML it writes.

PAGE_STUBS = r"""
const elements = {};
const element = () => ({ innerHTML: '', textContent: '', className: '', style: {}, dataset: {},
  classList: { add() {}, remove() {}, toggle() {}, contains: () => false },
  addEventListener() {}, setAttribute() {}, querySelector: () => null, querySelectorAll: () => [] });
const document = {
  getElementById: (id) => (elements[id] = elements[id] || element()),
  addEventListener() {}, querySelector: () => null, querySelectorAll: () => [],
};
const window = { __OFFERED_CONNECTORS__: OFFERED, location: { search: '', pathname: '/' },
  history: { replaceState() {} }, addEventListener() {} };
async function fetch() { return { ok: false, json: async () => ({}) }; }
"""


def _page_script() -> str:
    start = CARDS.index("<script>\n  // Integration icons mapping") + len("<script>")
    return CARDS[start : CARDS.index("</script>", start)]


def _draw(integrations, offered=("github", "notion", "slack", "calendar")) -> str:
    js = (
        f"const OFFERED = {json.dumps(list(offered))};\n"
        + PAGE_STUBS
        + _page_script()
        + f"""
renderIntegrations({json.dumps(integrations)});
process.stdout.write(document.getElementById('integrations-list').innerHTML);
"""
    )
    return subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout


def _card(name, status="healthy"):
    return {
        "name": name,
        "display_name": name.title(),
        "status": status,
        "status_message": "Connected",
        "configure_url": f"/settings/integrations/{name}",
    }


def _card_html(html: str, name: str) -> str:
    start = html.index(f'id="card-{name}"')
    end = html.find('id="card-', start + 1)
    return html[start:] if end == -1 else html[start:end]


@needs_node
class TestTheDrawnCards:
    def test_the_connected_github_card_carries_the_link_and_no_settings_button(self):
        github = _card_html(_draw([_card("github"), _card("notion")]), "github")
        assert 'id="github-repositories-link"' in github
        assert 'href="/settings/integrations/github#repositories"' in github
        assert "Repositories" in github and "Settings" not in github
        assert "Disconnect" in github

    def test_the_link_is_on_the_page_once(self):
        html = _draw([_card(n) for n in ("github", "notion", "slack", "calendar")])
        assert html.count('id="github-repositories-link"') == 1

    @pytest.mark.parametrize("name", ["notion", "slack", "calendar"])
    def test_the_other_connected_cards_keep_settings(self, name):
        card = _card_html(_draw([_card("github"), _card(name)]), name)
        assert "Settings" in card and "github-repositories-link" not in card
        assert f'href="/settings/integrations/{name}"' in card

    def test_a_github_card_that_is_not_connected_offers_connect_and_no_link(self):
        github = _card_html(_draw([_card("github", status="not_configured")]), "github")
        assert "Connect" in github and "github-repositories-link" not in github

    def test_a_github_card_that_needs_reconnecting_has_no_link(self):
        card = dict(_card("github"), action="reconnect")
        github = _card_html(_draw([card]), "github")
        assert "Reconnect with GitHub" in github and "github-repositories-link" not in github

    def test_github_outside_the_beta_list_has_no_link(self):
        github = _card_html(_draw([_card("github")], offered=("notion",)), "github")
        assert "github-repositories-link" not in github and "Not in this beta" in github


class TestThePagesSource:
    def test_github_is_drawn_by_the_api_key_branch_and_the_link_is_in_it(self):
        assert "const API_KEY_INTEGRATIONS = ['notion', 'github'];" in CARDS
        assert "const OAUTH_INTEGRATIONS = ['slack', 'calendar'];" in CARDS
        start = CARDS.index("} else if (isAPIKey) {")
        branch = CARDS[start : CARDS.index("} else if (integration.configure_url) {", start)]
        assert branch.count('id="github-repositories-link"') == 1
        assert CARDS.count('id="github-repositories-link"') == 1

    def test_the_list_is_rendered_before_the_label_is_asked_for(self):
        render = CARDS.index("      renderIntegrations(data.integrations);")
        label = CARDS.index("      labelGitHubRepositoriesLink();", render)
        assert label > render and "await labelGitHubRepositoriesLink" not in CARDS

    def test_the_settings_index_has_a_card_for_the_repository_section(self):
        # CXO 11-15: a card like its neighbours, not a text link (xian looked for the
        # link and did not find it).
        start = INDEX.index('<a href="/settings/integrations/github#repositories"')
        card = INDEX[start : INDEX.index("</a>", start)]
        assert 'class="settings-card"' in card and 'id="index-github-repositories"' in card
        assert '<h3 class="card-title">GitHub repositories</h3>' in card
        assert "Choose which repositories Piper can read." in card
        assert '<div class="card-icon">' in card
        # In the first group's grid, between two other cards, and not nested in one.
        grid = INDEX.index('<div class="settings-grid">')
        group_end = INDEX.index("</section>", grid)
        assert grid < start < group_end
        before = INDEX[grid:start]
        assert before.count('class="settings-card"') == before.count("</a>") >= 1
        assert INDEX.count('href="/settings/integrations/github#repositories"') == 1
        assert "settings-group-links" not in INDEX

    def test_the_anchor_is_on_the_repository_section_and_is_scrolled_to_once(self):
        assert '<h3 id="repositories">' in GITHUB_PAGE
        card = GITHUB_PAGE.index('id="repository-selection-card"')
        assert GITHUB_PAGE.index('<h3 id="repositories">') > card
        assert GITHUB_PAGE.count("repoCardEl.scrollIntoView(") == 1
        assert "window.location.hash === '#repositories' && !scrolledToRepositories" in GITHUB_PAGE
