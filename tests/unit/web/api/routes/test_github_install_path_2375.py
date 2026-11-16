"""#2375 (xian 2026-11-15; words CXO, mechanism Arch): the way to the GitHub install step.

The install step lives on the GitHub repository page, and the only way there was a grey
"Settings" link on the Integrations card. Now the card's link names what it leads to
("Install the GitHub app" when the App is installed nowhere, "Choose repositories" when
it is installed, "Repositories" when that isn't known), it lands on the repository
section, and the Settings index has its own link to the same place.

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

    def test_installed_somewhere_says_choose_repositories(self):
        r = _label({"state": "some"})
        assert r["text"] == "Choose repositories" and r["cls"] == "action-btn configure-btn"

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


class TestThePagesSource:
    def test_the_connected_github_card_has_no_bare_settings_link(self):
        start = CARDS.index("${integration.name === 'github' ? `")
        branch = CARDS[start : CARDS.index("` : `", start)]
        assert 'id="github-repositories-link"' in branch
        assert 'href="${GITHUB_REPOSITORIES_URL}"' in branch
        assert "${GITHUB_LINK_LABELS.unknown}" in branch and "Settings" not in branch

    def test_the_list_is_rendered_before_the_label_is_asked_for(self):
        render = CARDS.index("      renderIntegrations(data.integrations);")
        label = CARDS.index("      labelGitHubRepositoriesLink();", render)
        assert label > render and "await labelGitHubRepositoriesLink" not in CARDS

    def test_the_settings_index_links_to_the_repository_section(self):
        assert (
            '<a href="/settings/integrations/github#repositories" '
            'id="index-github-repositories">GitHub repositories</a>'
        ) in INDEX
        # A card is itself a link; the new link is not nested inside one.
        before = INDEX[: INDEX.index('<a href="/settings/integrations/github#repositories"')]
        assert before.count('<a href="/settings') == before.count("</a>")

    def test_the_anchor_is_on_the_repository_section_and_is_scrolled_to_once(self):
        assert '<h3 id="repositories">' in GITHUB_PAGE
        card = GITHUB_PAGE.index('id="repository-selection-card"')
        assert GITHUB_PAGE.index('<h3 id="repositories">') > card
        assert GITHUB_PAGE.count("repoCardEl.scrollIntoView(") == 1
        assert "window.location.hash === '#repositories' && !scrolledToRepositories" in GITHUB_PAGE
