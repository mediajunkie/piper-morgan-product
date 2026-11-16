"""#2376 (Arch 2026-11-15): the personal-token form on Settings, GitHub.

On an account connected through the GitHub App the page showed "Update Token", "Update"
and a dotted placeholder whether or not a token was on file, and a token saved there
would serve every read, with its own wider reach, whenever the App connection yielded
no token. Now: on an App connection the form is not offered and the route refuses; a
token already on file is shown as stored, with Remove only; the dots appear only when a
token is on file; and the route refuses a value that isn't token-shaped before any call
to GitHub.

Layer: unit. The routes are called directly on an in-memory binding table; the page's
own JavaScript runs under node with stubbed browser objects. No page is rendered in a
browser, and nothing calls GitHub.
"""

from __future__ import annotations

import contextlib
import json
import shutil
import subprocess
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from fastapi import HTTPException

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors import disconnect as disconnect_mod  # noqa: E402
from services.connectors.binding_repository import ConnectorBindingRepository  # noqa: E402
from services.database.models import ConnectorBinding  # noqa: E402
from services.database.session_factory import AsyncSessionFactory  # noqa: E402
from services.integrations.github import token_validator  # noqa: E402
from services.integrations.github.read_failed import GitHubReadFailed  # noqa: E402
from services.mcp.consumer import github_app_grant as grant_mod  # noqa: E402
from services.mcp.consumer.connector import ConnectorStatusState  # noqa: E402
from web.api.routes import settings_integrations as si  # noqa: E402

_USER = "11111111-1111-1111-1111-111111111111"
_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"
ROOT = Path(__file__).resolve().parents[5]
PAGE = (ROOT / "templates/settings_github.html").read_text()
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")


def _claims():
    c = MagicMock()
    c.sub = _USER
    return c


@pytest.fixture
def app_on(monkeypatch):
    monkeypatch.setenv(grant_mod.ENV_APP_CLIENT_ID, "app-client-id")
    monkeypatch.setenv(grant_mod.ENV_APP_CLIENT_SECRET, "app-client-secret")


@pytest.fixture
def app_off(monkeypatch):
    monkeypatch.delenv(grant_mod.ENV_APP_CLIENT_ID, raising=False)
    monkeypatch.delenv(grant_mod.ENV_APP_CLIENT_SECRET, raising=False)


@pytest_asyncio.fixture
async def bindings(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    sm = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with sm() as s:
            yield s
            await s.commit()

    monkeypatch.setattr(AsyncSessionFactory, "session_scope", staticmethod(_scope))
    yield sm
    await engine.dispose()


async def _seed(sm, status):
    async with sm() as s:
        await ConnectorBindingRepository(s).upsert(
            _USER, "github", status=status, mcp_server_ref="github"
        )
        await s.commit()


# ── the token's shape ───────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "value,ok",
    [
        ("ghp_abc", True),
        ("github_pat_abc", True),
        ("  ghp_abc  ", True),
        ("hunter2-my-login-password", False),
        ("gho_an-oauth-token", False),
        ("GHP_abc", False),
        ("", False),
        (None, False),
    ],
)
def test_a_personal_token_starts_with_one_of_two_prefixes(value, ok):
    assert token_validator.looks_like_personal_token(value) is ok


def test_the_page_checks_the_same_prefixes_as_the_route():
    listed = json.dumps(list(token_validator.PERSONAL_TOKEN_PREFIXES)).replace('"', "'")
    assert f"const PAT_PREFIXES = {listed};" in PAGE


# ── the save route ──────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestSaveRefusesBeforeAnyCallToGitHub:
    async def test_a_value_that_is_not_a_token_is_never_sent_to_github(self, bindings):
        verify = AsyncMock(side_effect=AssertionError("no call to GitHub"))
        with patch.object(token_validator, "verify_github_token", verify):
            with pytest.raises(HTTPException) as e:
                await si.save_github_token(
                    token="hunter2-my-login-password", current_user=_claims()
                )
        assert e.value.status_code == 400
        assert e.value.detail == si.GITHUB_TOKEN_SHAPE_REFUSAL
        assert "hunter2" not in str(e.value.detail)  # the refusal never repeats the value
        verify.assert_not_awaited()

    async def test_an_app_connected_account_is_refused_a_personal_token(self, bindings, app_on):
        await _seed(bindings, ConnectorStatusState.BOUND.value)
        verify = AsyncMock(side_effect=AssertionError("no call to GitHub"))
        store = MagicMock(side_effect=AssertionError("nothing stored"))
        with (
            patch.object(token_validator, "verify_github_token", verify),
            patch("services.infrastructure.keychain_service.KeychainService", store),
        ):
            with pytest.raises(HTTPException) as e:
                await si.save_github_token(token="ghp_real-looking", current_user=_claims())
        assert e.value.status_code == 409
        assert e.value.detail == si.GITHUB_TOKEN_APP_CONNECTED_REFUSAL
        verify.assert_not_awaited()
        store.assert_not_called()

    @pytest.mark.parametrize("status", [None, "stale", "unbound"])
    async def test_an_account_not_connected_through_the_app_reaches_the_github_check(
        self, bindings, app_on, status
    ):
        if status:
            await _seed(bindings, status)
        verify = AsyncMock(return_value={"authenticated": False, "error": "Bad credentials"})
        with patch.object(token_validator, "verify_github_token", verify):
            with pytest.raises(HTTPException) as e:
                await si.save_github_token(token=" ghp_typed ", current_user=_claims())
        assert e.value.status_code == 400 and e.value.detail == "Bad credentials"
        verify.assert_awaited_once_with("ghp_typed")  # stripped, and only now sent

    async def test_a_classic_connection_keeps_the_token_form(self, bindings, app_off):
        # App mode off (a self-hosted install with a classic OAuth app): not ruled on.
        await _seed(bindings, ConnectorStatusState.BOUND.value)
        verify = AsyncMock(return_value={"authenticated": False, "error": "Bad credentials"})
        with patch.object(token_validator, "verify_github_token", verify):
            with pytest.raises(HTTPException) as e:
                await si.save_github_token(token="ghp_typed", current_user=_claims())
        assert e.value.status_code == 400
        verify.assert_awaited_once()


# ── what the page is told ───────────────────────────────────────────────────────────


class TestAppConnected:
    @pytest.mark.parametrize(
        "status,expected",
        [("bound", True), ("stale", False), ("unbound", False), (None, False)],
    )
    def test_in_app_mode_only_a_bound_binding_is_app_connected(self, app_on, status, expected):
        assert si._github_app_connected(status) is expected

    def test_with_app_mode_off_nothing_is_app_connected(self, app_off):
        assert si._github_app_connected("bound") is False


@pytest.mark.asyncio
class TestOAuthStatusTellsThePage:
    @pytest.mark.parametrize("stored,expected", [("ghp_on_file", True), (None, False)])
    async def test_pat_on_file_is_a_boolean_never_the_token(
        self, bindings, app_on, stored, expected
    ):
        await _seed(bindings, ConnectorStatusState.BOUND.value)
        with patch(f"{_ADAPTER}.account_pat", new=AsyncMock(return_value=stored)):
            out = await si.github_oauth_status(current_user=_claims())
        assert out["app_connected"] is True
        assert out["pat_on_file"] is expected
        assert "ghp_on_file" not in json.dumps(out)

    async def test_a_failed_store_read_is_unknown_never_none_on_file(self, bindings, app_on):
        failed = AsyncMock(side_effect=GitHubReadFailed("store", None, detail="store_failed"))
        with patch(f"{_ADAPTER}.account_pat", new=failed):
            out = await si.github_oauth_status(current_user=_claims())
        assert out["pat_on_file"] is None


# ── removing the token only ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestRemoveTheTokenOnly:
    @staticmethod
    def _helper(monkeypatch, *, readback):
        gone = AsyncMock(return_value=True)
        deleted = AsyncMock(return_value=True)
        monkeypatch.setattr(disconnect_mod, "_keychain_copy_gone", gone)
        monkeypatch.setattr("services.connectors.github_pat_store.delete_user_pat_at_rest", deleted)
        monkeypatch.setattr("services.infrastructure.keychain_service.KeychainService", MagicMock())
        if isinstance(readback, Exception):
            read = AsyncMock(side_effect=readback)
        else:
            read = AsyncMock(return_value=readback)
        monkeypatch.setattr(f"{_ADAPTER}.account_pat", read)
        return gone, deleted

    async def test_the_three_copies_go_and_the_connection_is_untouched(self, bindings, monkeypatch):
        await _seed(bindings, ConnectorStatusState.BOUND.value)
        gone, deleted = self._helper(monkeypatch, readback=None)
        revoke = AsyncMock(side_effect=AssertionError("nothing is revoked at GitHub"))
        monkeypatch.setattr(disconnect_mod, "_revoke_github_grant_at_github", revoke)
        grant_delete = AsyncMock(side_effect=AssertionError("the grant is not touched"))
        monkeypatch.setattr(
            "services.mcp.consumer.connector_grant_store.ConnectorGrantStore.delete", grant_delete
        )
        remaining = await disconnect_mod.remove_github_personal_token(_USER)
        assert remaining == []
        assert [c.args[1] for c in gone.await_args_list] == ["github_token", "github"]
        assert all(c.args[2] == _USER for c in gone.await_args_list)
        deleted.assert_awaited_once()
        async with bindings() as s:
            row = await ConnectorBindingRepository(s).get(_USER, "github")
        assert row.status == ConnectorStatusState.BOUND.value

    async def test_a_token_the_resolver_still_reads_is_not_gone(self, bindings, monkeypatch):
        self._helper(monkeypatch, readback="ghp_still_here")
        assert await disconnect_mod.remove_github_personal_token(_USER) == ["token_still_readable"]

    async def test_a_failed_read_back_is_unverified_not_gone(self, bindings, monkeypatch):
        self._helper(monkeypatch, readback=GitHubReadFailed("store", None, detail="store_failed"))
        assert await disconnect_mod.remove_github_personal_token(_USER) == ["token_unverified"]

    async def test_the_route_says_removed_only_when_nothing_remains(self, monkeypatch):
        monkeypatch.setattr(
            disconnect_mod, "remove_github_personal_token", AsyncMock(return_value=[])
        )
        out = await si.remove_github_token(current_user=_claims())
        assert out == {"success": True, "message": si.GITHUB_TOKEN_REMOVED_LINE}

    @pytest.mark.parametrize("outcome", [["pat_at_rest"], RuntimeError("boom")])
    async def test_the_route_never_says_removed_on_doubt(self, monkeypatch, outcome):
        helper = (
            AsyncMock(side_effect=outcome)
            if isinstance(outcome, Exception)
            else AsyncMock(return_value=outcome)
        )
        monkeypatch.setattr(disconnect_mod, "remove_github_personal_token", helper)
        out = await si.remove_github_token(current_user=_claims())
        assert out == {"success": False, "message": si.GITHUB_TOKEN_REMOVE_INCOMPLETE_LINE}


# ── the page's own script, run under node ───────────────────────────────────────────

HARNESS = r"""
const els = {};
function el(id) {
  if (!els[id]) {
    els[id] = { id, textContent: '', value: '', placeholder: 'INITIAL', disabled: false,
                style: { display: '' }, addEventListener: () => {} };
  }
  return els[id];
}
const document = { getElementById: (id) => el(id), addEventListener: () => {} };
function loadGitHubStatus() {}
function checkGitHubOAuthStatus() {}
"""


def _state(connected_valid: bool, oauth: dict, typed: str = "") -> dict:
    start = PAGE.index("      // #2376: the personal-token form's state")
    block = PAGE[start : PAGE.index("      async function loadGitHubStatus", start)]
    js = (
        HARNESS
        + block
        + f"""
el('form-title').textContent = 'Connect GitHub';
el('save-btn').textContent = 'Connect';
el('token').value = {json.dumps(typed)};
githubConnectedValid = {json.dumps(connected_valid)};
githubOAuthData = {json.dumps(oauth)};
applyTokenFormState();
process.stdout.write(JSON.stringify({{
  form: el('pat-form-section').style.display,
  stored: el('pat-stored-section').style.display,
  storedLine: el('pat-stored-line').textContent,
  title: el('form-title').textContent,
  button: el('save-btn').textContent,
  buttonShown: el('save-btn').style.display,
  buttonDisabled: el('save-btn').disabled,
  placeholder: el('token').placeholder,
  value: el('token').value,
}}));
"""
    )
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


DOTS = "•" * 32


@needs_node
class TestThePagesTokenForm:
    def test_app_connected_with_no_token_shows_nothing_about_tokens(self):
        s = _state(True, {"connected": True, "app_connected": True, "pat_on_file": False})
        assert s["form"] == "none" and s["buttonShown"] == "none"
        assert s["stored"] == "none" and s["storedLine"] == ""
        assert "Update" not in s["title"] and DOTS not in s["placeholder"]

    def test_app_connected_with_a_token_on_file_names_it_and_offers_remove_only(self):
        s = _state(True, {"connected": True, "app_connected": True, "pat_on_file": True})
        assert s["form"] == "none" and s["buttonShown"] == "none"  # no Update
        assert s["stored"] == "block"
        # CXO 2026-11-15, verbatim.
        assert s["storedLine"] == (
            "A personal token is also stored for this account. Piper uses it instead of "
            "the GitHub app if the app connection stops working, and it can reach more of "
            "your GitHub than the app does."
        )

    def test_app_connected_and_the_store_unreadable_claims_no_stored_token(self):
        s = _state(True, {"connected": True, "app_connected": True, "pat_on_file": None})
        assert s["form"] == "none" and s["stored"] == "none"

    def test_anything_typed_before_the_state_arrived_is_cleared_on_an_app_account(self):
        s = _state(True, {"app_connected": True, "pat_on_file": False}, typed="ghp_typed")
        assert s["value"] == ""

    def test_connected_another_way_with_a_token_on_file_says_update_token(self):
        s = _state(True, {"connected": True, "app_connected": False, "pat_on_file": True})
        assert s["form"] == "block" and s["stored"] == "none"
        assert s["title"] == "Update token" and s["button"] == "Update token"
        assert s["placeholder"] == DOTS
        assert s["buttonDisabled"] is True  # CXO: disabled while the field is empty

    def test_connected_with_no_token_on_file_never_shows_dots_or_update(self):
        # The state xian saw on beta, on any connection that isn't through the app.
        s = _state(True, {"connected": True, "app_connected": False, "pat_on_file": False})
        assert s["title"] == "Add a personal token (optional)" and s["button"] == "Save token"
        assert DOTS not in s["placeholder"] and s["placeholder"].startswith("ghp_")
        assert s["buttonDisabled"] is True

    def test_not_connected_keeps_the_connect_form(self):
        s = _state(False, {"connected": False, "app_connected": False, "pat_on_file": False})
        assert s["form"] == "block" and s["buttonShown"] == ""
        assert s["title"] == "Connect GitHub" and s["button"] == "Connect"

    def test_the_button_is_enabled_once_something_is_typed(self):
        s = _state(True, {"app_connected": False, "pat_on_file": False}, typed="ghp_typed")
        assert s["buttonDisabled"] is False


class TestThePageSource:
    def test_no_branch_sets_update_and_dots_on_every_connected_account(self):
        # Before: the configured-and-valid branch set 'Update Token', 'Update' and the
        # dots whatever was stored.
        assert "'Update Token'" not in PAGE and "textContent = 'Update';" not in PAGE
        assert PAGE.count("tokenEl.placeholder = PAT_STORED_PLACEHOLDER") == 1
        assert PAGE.count(DOTS) == 1  # the constant, used in the on-file branch only

    def test_the_stored_section_starts_hidden_and_has_remove_only(self):
        start = PAGE.index('<div id="pat-stored-section"')
        section = PAGE[start : PAGE.index('<div class="button-group">', start)]
        assert 'style="display: none;"' in section.splitlines()[0]
        assert "removeGitHubToken()" in section and "saveGitHubToken()" not in section

    def test_remove_calls_the_token_route_not_disconnect(self):
        start = PAGE.index("      async function removeGitHubToken()")
        body = PAGE[start : PAGE.index("      async function disconnectGitHub()", start)]
        assert "/api/v1/settings/integrations/github/token/remove" in body
        assert "/github/disconnect" not in body
