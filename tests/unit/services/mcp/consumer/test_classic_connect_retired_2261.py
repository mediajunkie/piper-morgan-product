"""Issue 2261 (ADR-081 D3, amended 2026-11-27; Arch's ruling and conditions C1 to C3):
the classic GitHub OAuth connect is retired.

* No handler, in any mode, puts a ``scope`` on the authorize URL. With App mode off there
  is no URL at all: ``GitHubConnectNotConfigured``.
* A ``classic=True`` handler builds no authorize URL and exchanges no code; it revokes,
  exactly as before.
* With App mode off and no ``classic``, the handler loads no client credentials.
* The connect route with App mode off answers CXO's refusal (a marked 503) and stores no
  OAuth state; the callback route refuses and exchanges nothing.
* The startup log says connect is not configured and only a personal token serves.
* Settings, GitHub with App mode off shows no Connect button and no install step, shows
  the personal-token form, and shows CXO's card line in place of the Connect step,
  above the form.

LAYER: the handler and the two routes called directly (Redis, the keychain and GitHub
stubbed; nothing leaves the process); the app's real error handler on a small app for
the refusal's words; the real page route rendered through the app's TestClient (the
Jinja branch that decides what the card shows), plus the page's own status script run
under node over that rendered markup. No browser renders the page.
DENOMINATOR: both handler entry points that start or finish a connect
(``generate_authorization_url``, ``handle_oauth_callback`` / ``_exchange_code_for_tokens``)
in the three handler shapes (App mode, App mode off, ``classic=True``); both routes; one
page in both modes.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import uuid
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from urllib.parse import parse_qs, urlsplit

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.testclient import TestClient

from services.api.errors import UserFacingHTTPException
from services.mcp.consumer import github_app_grant as grant_mod
from services.mcp.consumer import github_oauth_handler as handler_mod
from services.mcp.consumer.github_oauth_handler import (
    GITHUB_CONNECT_NOT_SET_UP_CARD_LINE,
    GITHUB_CONNECT_NOT_SET_UP_LINE,
    GitHubConnectNotConfigured,
    GitHubOAuthHandler,
)

ROOT = Path(__file__).resolve().parents[5]
_OWNER = "11111111-1111-1111-1111-111111111111"
_APP_ENV = (grant_mod.ENV_APP_CLIENT_ID, grant_mod.ENV_APP_CLIENT_SECRET)
_CLASSIC_ENV = ("GITHUB_OAUTH_CLIENT_ID", "GITHUB_OAUTH_CLIENT_SECRET")
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")


@pytest.fixture
def app_on(monkeypatch):
    monkeypatch.setenv(grant_mod.ENV_APP_CLIENT_ID, "test-app-client-id")
    monkeypatch.setenv(grant_mod.ENV_APP_CLIENT_SECRET, "test-app-client-secret")


@pytest.fixture
def app_off(monkeypatch):
    for name in _APP_ENV:
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def classic_env(monkeypatch):
    monkeypatch.setenv("GITHUB_OAUTH_CLIENT_ID", "classic-id")
    monkeypatch.setenv("GITHUB_OAUTH_CLIENT_SECRET", "classic-secret")


@pytest.fixture
def state_redis():
    """#2345: the connect state lives in Redis; Slack's in-memory fake stands in."""
    from contextlib import asynccontextmanager

    from tests.unit.services.integrations.slack.test_oauth_redis_state_1109 import _FakeRedis

    fake = _FakeRedis()

    @asynccontextmanager
    async def _scope():
        yield fake

    with patch("services.cache.redis_factory.RedisFactory.redis_scope", side_effect=_scope):
        yield fake


@pytest.fixture
def no_state_store():
    """The state store's put and take, each failing the test if called."""
    put = AsyncMock(side_effect=AssertionError("no OAuth state may be stored"))
    take = AsyncMock(side_effect=AssertionError("no OAuth state may be read"))
    with patch.object(handler_mod, "put_state", put), patch.object(handler_mod, "take_state", take):
        yield put, take


def _no_network():
    return patch("aiohttp.ClientSession", side_effect=AssertionError("no call to GitHub"))


# ── the words (CXO, 2026-11-27, issue 2261) ──────────────────────────────────────────


class TestTheWords:
    """The one place each line's exact text is pinned; every other test reads the
    constant, so a change of words is a visible diff here."""

    def test_the_refusal(self):
        assert GITHUB_CONNECT_NOT_SET_UP_LINE == (
            "GitHub connect isn't set up on this install. Add a personal access token on "
            "this page, or ask whoever runs this install to set up the Piper GitHub app."
        )

    def test_the_card_line(self):
        assert GITHUB_CONNECT_NOT_SET_UP_CARD_LINE == (
            "This install isn't set up to connect through the Piper GitHub app. "
            "You can add a personal access token below."
        )

    def test_the_refusal_names_the_personal_access_token(self):
        # CXO's pin: the refusal sends a person to the token.
        assert "personal access token" in GITHUB_CONNECT_NOT_SET_UP_LINE

    def test_the_named_error_carries_the_refusal(self):
        assert str(GitHubConnectNotConfigured()) == GITHUB_CONNECT_NOT_SET_UP_LINE

    @pytest.mark.parametrize(
        "line", [GITHUB_CONNECT_NOT_SET_UP_LINE, GITHUB_CONNECT_NOT_SET_UP_CARD_LINE]
    )
    def test_neither_line_names_oauth_a_scope_or_a_client_id(self, line):
        lowered = line.lower()
        assert "oauth" not in lowered and "scope" not in lowered and "client" not in lowered


# ── the handler: point 1, point 2, C1 ────────────────────────────────────────────────


class TestNoScopeInAnyMode:
    async def test_app_mode_url_has_no_scope(self, app_on, state_redis):
        url, state = await GitHubOAuthHandler().generate_authorization_url(_OWNER)
        # HOST's pin: read the BUILT URL's query, not its text: no ``scope`` key at all.
        query = parse_qs(urlsplit(url).query, keep_blank_values=True)
        assert "scope" not in query
        assert set(query) == {"client_id", "redirect_uri", "state"}
        assert query["client_id"] == ["test-app-client-id"] and query["state"] == [state]

    async def test_app_mode_off_makes_no_url_and_stores_no_state(
        self, app_off, classic_env, no_state_store
    ):
        put, _ = no_state_store
        with pytest.raises(GitHubConnectNotConfigured):
            await GitHubOAuthHandler().generate_authorization_url(_OWNER)
        put.assert_not_called()

    @pytest.mark.parametrize("mode", ["app_on", "app_off"])
    async def test_a_classic_handler_makes_no_url(self, request, mode, classic_env, no_state_store):
        request.getfixturevalue(mode)
        put, _ = no_state_store
        with pytest.raises(GitHubConnectNotConfigured):
            await GitHubOAuthHandler(classic=True).generate_authorization_url(_OWNER)
        put.assert_not_called()


class TestAClassicHandlerOnlyRevokes:
    @pytest.mark.parametrize("mode", ["app_on", "app_off"])
    async def test_it_refuses_to_finish_a_callback(
        self, request, mode, classic_env, no_state_store
    ):
        request.getfixturevalue(mode)
        _, take = no_state_store
        handler = GitHubOAuthHandler(classic=True)
        with _no_network(), pytest.raises(GitHubConnectNotConfigured):
            await handler.handle_oauth_callback("code", "state", session_user_id=_OWNER)
        take.assert_not_called()

    @pytest.mark.parametrize("mode", ["app_on", "app_off"])
    async def test_it_refuses_to_exchange_a_code(self, request, mode, classic_env):
        request.getfixturevalue(mode)
        with _no_network(), pytest.raises(GitHubConnectNotConfigured):
            await GitHubOAuthHandler(classic=True)._exchange_code_for_tokens("code")

    async def test_app_mode_off_refuses_the_exchange_too(self, app_off):
        with _no_network(), pytest.raises(GitHubConnectNotConfigured):
            await GitHubOAuthHandler()._exchange_code_for_tokens("code")
        with _no_network(), pytest.raises(GitHubConnectNotConfigured):
            await GitHubOAuthHandler().handle_oauth_callback("c", "s", session_user_id=_OWNER)

    @pytest.mark.parametrize("mode", ["app_on", "app_off"])
    async def test_its_revoke_still_uses_the_classic_client(self, request, mode, classic_env):
        """Point 3: ``classic=True`` stays for the revoke. Same stub shape as the #2178
        revoke tests: DELETE answers 204."""
        request.getfixturevalue(mode)
        seen: dict = {}

        class _Resp:
            status = 204

            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                return False

        class _Session:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                return False

            def delete(self, url, auth=None, headers=None, json=None):
                seen.update(url=url, auth=auth, json=json)
                return _Resp()

        handler = GitHubOAuthHandler(classic=True)
        assert (handler.client_id, handler.client_secret) == ("classic-id", "classic-secret")
        with patch("aiohttp.ClientSession", lambda: _Session()):
            assert await handler.revoke_grant("classic-bearer-value") is True
        assert seen["url"] == "https://api.github.com/applications/classic-id/grant"
        assert seen["auth"].login == "classic-id" and seen["auth"].password == "classic-secret"
        assert seen["json"] == {"access_token": "classic-bearer-value"}


class TestADisconnectWithNoClassicValuesNeverReportsSuccess:
    """HOST's pin (accepted by Arch as a test of today's behaviour, which C3 keeps): a
    Disconnect of a stored CLASSIC grant on an install with no classic client values
    (env unset, nothing in the store) makes no call to GitHub, reports the revoke as
    failed, and the person reads CXO's revoke-failed line, never a bare "disconnected".
    The real handler and the real ``revoke_grant`` run; the stores around them are
    stubbed as in the #2178 tests."""

    @pytest.mark.parametrize("mode", ["app_on", "app_off"])
    async def test_end_to_end(self, request, mode, monkeypatch):
        from services.connectors import disconnect as d
        from services.connectors.disconnect_words import revoke_failed_line
        from services.mcp.consumer.connector import DegradationReason
        from web.api.routes.settings_integrations import _disconnected_message

        request.getfixturevalue(mode)
        for name in _CLASSIC_ENV:
            monkeypatch.delenv(name, raising=False)

        scope = MagicMock()
        scope.__aenter__ = AsyncMock(return_value=MagicMock())
        scope.__aexit__ = AsyncMock(return_value=False)
        factory = MagicMock()
        factory.session_scope.return_value = scope
        store = MagicMock()
        store.get_strict = AsyncMock(return_value="classic-bearer-value")  # a bare token
        store.delete = AsyncMock(return_value=True)
        repo = MagicMock()
        repo.set_status = AsyncMock()
        keychain = MagicMock()
        keychain.return_value.get_api_key.return_value = None  # nothing in the store
        built = []
        real_init = GitHubOAuthHandler.__init__

        def _init(self, **kw):
            real_init(self, **kw)
            built.append((kw, self.client_id, self.client_secret))

        # A MagicMock, not a raiser: revoke_grant swallows exceptions, so only a call
        # count proves no request was made.
        http = MagicMock(name="aiohttp.ClientSession")
        with (
            patch("aiohttp.ClientSession", http),
            patch("services.database.session_factory.AsyncSessionFactory", factory),
            patch(
                "services.mcp.consumer.connector_grant_store.ConnectorGrantStore",
                return_value=store,
            ),
            patch(
                "services.connectors.binding_repository.ConnectorBindingRepository",
                return_value=repo,
            ),
            patch("services.infrastructure.keychain_service.KeychainService", keychain),
            patch.object(GitHubOAuthHandler, "__init__", _init),
            patch.object(d, "_clear_github_personal_token", AsyncMock(return_value=[])),
            patch.object(d, "_keychain_copy_gone", AsyncMock(return_value=True)),
            patch(
                "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.resolve_credential",
                AsyncMock(
                    return_value=MagicMock(leg=None, reason=DegradationReason.CONNECT_REQUIRED)
                ),
            ),
            patch("services.integrations.github.config_service.GitHubConfigService"),
        ):
            result = await d.disconnect_connector(_OWNER, "github")

        http.assert_not_called()  # no request to GitHub at all
        assert built == [({"classic": True}, "", "")]  # classic handler, empty credentials
        assert result.cleared and result.provider_revoke_failed is True
        message = _disconnected_message("GitHub", result)
        assert message == "GitHub disconnected. " + revoke_failed_line("GitHub")
        assert message != "GitHub disconnected"


# ── C3: credentials ──────────────────────────────────────────────────────────────────


class TestNoCredentialsWithoutAppModeOrClassic:
    def test_app_mode_off_reads_no_client_credentials(self, app_off, classic_env):
        keychain = MagicMock(side_effect=AssertionError("the store must not be consulted"))
        load = MagicMock(side_effect=AssertionError("no classic credentials may be loaded"))
        read_env = []
        real_getenv = handler_mod.os.getenv

        def _getenv(name, *a):
            read_env.append(name)
            return real_getenv(name, *a)

        with (
            patch("services.infrastructure.keychain_service.KeychainService", keychain),
            patch.object(GitHubOAuthHandler, "_load_credentials", load),
            patch.object(handler_mod.os, "getenv", _getenv),
        ):
            handler = GitHubOAuthHandler()
        assert handler.app_mode is False
        assert handler.client_id == "" and handler.client_secret == ""
        assert not set(_CLASSIC_ENV) & set(read_env)
        keychain.assert_not_called()
        load.assert_not_called()

    def test_only_a_classic_handler_reads_them(self, app_off, classic_env):
        handler = GitHubOAuthHandler(classic=True)
        assert (handler.client_id, handler.client_secret) == ("classic-id", "classic-secret")

    def test_app_mode_reads_the_app_client_only(self, app_on, classic_env):
        load = MagicMock(side_effect=AssertionError("no classic credentials may be loaded"))
        with patch.object(GitHubOAuthHandler, "_load_credentials", load):
            handler = GitHubOAuthHandler()
        assert (handler.client_id, handler.client_secret) == (
            "test-app-client-id",
            "test-app-client-secret",
        )


# ── the routes ───────────────────────────────────────────────────────────────────────


def _claims():
    claims = MagicMock()
    claims.sub = _OWNER
    return claims


def _through_the_real_handler(exc):
    from web.app import app as real_app

    small = FastAPI()
    small.add_exception_handler(HTTPException, real_app.exception_handlers[HTTPException])

    @small.get("/call")
    async def _call():
        raise exc

    return TestClient(small).get("/call")


class TestConnectRoute:
    async def test_app_mode_off_refuses_with_cxos_line_and_stores_no_state(
        self, app_off, classic_env, no_state_store
    ):
        from web.api.routes import settings_integrations as si

        put, _ = no_state_store
        with pytest.raises(UserFacingHTTPException) as e:
            await si.connect_github(current_user=_claims(), request=None)
        assert e.value.status_code == 503
        assert e.value.detail == GITHUB_CONNECT_NOT_SET_UP_LINE
        put.assert_not_called()

    def test_the_refusal_reaches_the_client_as_written(self):
        reply = _through_the_real_handler(
            UserFacingHTTPException(status_code=503, detail=GITHUB_CONNECT_NOT_SET_UP_LINE)
        )
        assert reply.status_code == 503
        assert reply.json()["detail"] == GITHUB_CONNECT_NOT_SET_UP_LINE

    def test_the_route_raises_it_marked(self):
        import ast

        tree = ast.parse((ROOT / "web/api/routes/settings_integrations.py").read_text())
        details = [
            {k.arg: k.value for k in node.keywords}.get("detail")
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "UserFacingHTTPException"
        ]
        names = [d.id for d in details if isinstance(d, ast.Name)]
        assert names.count("GITHUB_CONNECT_NOT_SET_UP_LINE") == 1

    async def test_app_mode_still_starts(self, app_on, state_redis):
        from web.api.routes import settings_integrations as si

        reply = await si.connect_github(current_user=_claims(), request=None)
        assert (
            "scope=" not in reply["auth_url"]
            and "client_id=test-app-client-id" in reply["auth_url"]
        )


class TestCallbackRoute:
    async def test_app_mode_off_refuses_and_exchanges_nothing(
        self, app_off, classic_env, no_state_store
    ):
        from web.api.routes import settings_integrations as si

        _, take = no_state_store
        callback = AsyncMock(side_effect=AssertionError("no callback may be handled"))
        exchange = AsyncMock(side_effect=AssertionError("no code may be exchanged"))
        with (
            _no_network(),
            patch.object(GitHubOAuthHandler, "handle_oauth_callback", callback),
            patch.object(GitHubOAuthHandler, "_exchange_code_for_tokens", exchange),
        ):
            reply = await si.handle_github_callback(
                code="code", state="state", error=None, browser_session=_claims()
            )
        assert isinstance(reply, RedirectResponse)
        assert reply.headers["location"] == "/settings/integrations/github"
        callback.assert_not_called()
        exchange.assert_not_called()
        take.assert_not_called()

    async def test_app_mode_off_stores_nothing_and_claims_no_success(
        self, app_off, classic_env, no_state_store
    ):
        """Arch's condition on the redirect (2026-11-27): no grant stored, no binding
        marked, and nothing in the redirect the page reads as a connect. The Integrations
        page reads ``github_success=true`` (and ``github_login``) for its success toast."""
        from services.connectors.binding_repository import ConnectorBindingRepository
        from services.mcp.consumer.connector_grant_store import ConnectorGrantStore
        from web.api.routes import settings_integrations as si

        def _never(what):
            return AsyncMock(side_effect=AssertionError(f"{what} must not be called"))

        from services.security.user_api_key_service import UserAPIKeyService

        persist = _never("persist_github_connection")
        store, store_app = _never("ConnectorGrantStore.store"), _never("store_app_grant")
        # HOST's pin: the credential store itself, under the grant store: no row, no token.
        key_write = _never("UserAPIKeyService.store_user_key")
        upsert, set_status = _never("binding upsert"), _never("binding set_status")
        with (
            _no_network(),
            patch.object(handler_mod, "persist_github_connection", persist),
            patch.object(ConnectorGrantStore, "store", store),
            patch.object(ConnectorGrantStore, "store_app_grant", store_app),
            patch.object(UserAPIKeyService, "store_user_key", key_write),
            patch.object(ConnectorBindingRepository, "upsert", upsert),
            patch.object(ConnectorBindingRepository, "set_status", set_status),
        ):
            reply = await si.handle_github_callback(
                code="code", state="state", error=None, browser_session=_claims()
            )
        for writer in (persist, store, store_app, key_write, upsert, set_status):
            writer.assert_not_called()
        location = urlsplit(reply.headers["location"])
        query = parse_qs(location.query, keep_blank_values=True)
        assert location.path == "/settings/integrations/github"
        assert "github_success" not in query and "github_login" not in query
        assert "connected" not in reply.headers["location"].lower()
        page = (ROOT / "templates/integrations.html").read_text()
        assert "params.get('github_success') === 'true'" in page  # the marker we checked


# ── the startup line (C3) ────────────────────────────────────────────────────────────


class TestStartupLine:
    def test_app_mode_off_says_not_configured_and_personal_token_only(self, app_off):
        line = grant_mod.connect_mode_log_line()
        assert line == grant_mod.CONNECT_MODE_NOT_CONFIGURED_LOG_LINE
        assert line == (
            "GitHub connect mode: not configured (no GitHub App values); "
            "only a personal access token serves"
        )

    def test_app_mode_says_github_app(self, app_on):
        assert grant_mod.connect_mode_log_line() == "GitHub connect mode: GitHub App"

    def test_the_app_logs_that_line_and_names_no_classic_app(self):
        source = (ROOT / "web/app.py").read_text()
        assert "logger.info(connect_mode_log_line())" in source
        assert "classic OAuth App" not in source

    def test_the_half_set_warning_no_longer_says_the_classic_app_serves(self, app_off, monkeypatch):
        monkeypatch.setenv(grant_mod.ENV_APP_CLIENT_ID, "test-app-client-id")
        warning = grant_mod.app_mode_config_warning()
        assert warning and "classic OAuth App" not in warning


# ── source guard (point 1) ───────────────────────────────────────────────────────────


class TestSourceGuard:
    def test_no_scope_constant_remains_in_the_handler(self):
        source = (ROOT / "services/mcp/consumer/github_oauth_handler.py").read_text()
        assert "_DEFAULT_SCOPES" not in source
        assert not re.search(r"""\[\s*["']repo["']\s*\]""", source)
        assert not re.search(r"""["']scope["']\s*\]\s*=""", source)  # no params["scope"] = ...

    def test_confirm_minimal_set_appears_nowhere_under_services(self):
        hits = [
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "services").rglob("*.py")
            if "confirm minimal set" in path.read_text(encoding="utf-8")
        ]
        assert hits == []


# ── the page (C2) ────────────────────────────────────────────────────────────────────


@pytest.fixture(scope="module")
def client():
    from services.auth.container import AuthContainer
    from web.app import app

    if getattr(app.state, "templates", None) is None:
        from fastapi.templating import Jinja2Templates

        app.state.templates = Jinja2Templates(directory=str(ROOT / "templates"))
    test_client = TestClient(app, follow_redirects=False)
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2261@example.com", scopes=["user"]
    )
    test_client.cookies.set("auth_token", token)
    yield test_client
    test_client.cookies.delete("auth_token")


def _page(client) -> tuple[str, str]:
    """(markup, text) of the rendered page: the markup is everything before the page's
    inline scripts; the text is that markup with entities decoded."""
    reply = client.get("/settings/integrations/github")
    assert reply.status_code == 200
    markup = reply.text.split('<script src="/static/js/api-error-parser.js">', 1)[0]
    return markup, html.unescape(markup)


class TestTheCardWithAppModeOff:
    def test_no_connect_button_and_no_install_step(self, client, app_off):
        markup, text = _page(client)
        assert 'id="oauth-connect-btn"' not in markup
        assert "connectGitHubOAuth()" not in markup
        assert "Connect with GitHub" not in text
        assert 'id="oauth-approval-note"' not in markup
        assert "github-app-install-link" not in markup and "Install on GitHub" not in text

    def test_the_personal_token_form_is_shown(self, client, app_off):
        markup, text = _page(client)
        assert 'id="pat-form-section"' in markup and 'id="token"' in markup
        # CXO, 2026-11-27, after the browser render: no "Or" with nothing before it.
        assert "Connect with a personal access token:" in text
        assert "Or connect with a personal access token:" not in text

    def test_the_card_line_stands_in_place_of_connect_above_the_form(self, client, app_off):
        markup, text = _page(client)
        assert text.count(GITHUB_CONNECT_NOT_SET_UP_CARD_LINE) == 1
        group = markup.index('id="oauth-connect-group"')
        line = markup.index('id="github-connect-not-set-up"')
        form = markup.index('id="pat-form-section"')
        assert group < line < form  # in the Connect step's place, above the form "below"
        between = html.unescape(markup[line:form])
        assert GITHUB_CONNECT_NOT_SET_UP_CARD_LINE in between
        assert "<button" not in markup[group:form]


class TestTheCardWithAppMode:
    def test_the_connect_step_is_offered_and_the_line_is_not(self, client, app_on):
        markup, text = _page(client)
        assert 'id="oauth-connect-btn"' in markup
        assert GITHUB_CONNECT_NOT_SET_UP_CARD_LINE not in text
        assert 'id="github-connect-not-set-up"' not in markup


_STATUS_HARNESS = r"""
const els = {};
function el(id) {
  if (!els[id]) els[id] = { id, innerHTML: '', textContent: '', className: '', style: {} };
  return els[id];
}
el('oauth-connect-group').innerHTML = GROUP;
const document = { getElementById: (id) => (id === 'oauth-connect-btn' || id === 'oauth-connect-hint')
  ? (GROUP.includes('id="' + id + '"') ? el(id) : null) : el(id) };
let githubOAuthData = null;
function applyTokenFormState() {}
async function fetch(url) { return { ok: true, json: async () => STATUS }; }
"""


@needs_node
class TestThePageScriptKeepsTheLine:
    """The page's own status script, run under node over the rendered group, never puts a
    Connect button back in that state (a stale binding keeps the group as it is)."""

    @pytest.mark.parametrize(
        "status",
        [
            {"connected": False, "stale": True, "serving": None},
            {"connected": False, "stale": False, "serving": None},
        ],
    )
    def test_the_status_script_adds_no_button(self, client, app_off, status):
        markup, _ = _page(client)
        start = markup.index('<div class="form-group" id="oauth-connect-group">')
        group = markup[start : markup.index("</div>", start)].split(">", 1)[1]
        page = (ROOT / "templates/settings_github.html").read_text()
        i = page.index("      let githubOAuthGrant = false;")
        block = page[i : page.index("      async function saveGitHubToken", i)]
        js = (
            f"const GROUP = {json.dumps(group)};\nconst STATUS = {json.dumps(status)};\n"
            + _STATUS_HARNESS
            + block
            + "\n(async () => { await checkGitHubOAuthStatus();"
            " process.stdout.write(JSON.stringify(el('oauth-connect-group').innerHTML)); })();"
        )
        out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True)
        after = json.loads(out.stdout)
        assert "oauth-connect-btn" not in after and "<button" not in after
        assert 'id="github-connect-not-set-up"' in after


# ── the connect-required hint follows the same predicate (Arch 2026-11-27) ───────────


class TestTheConnectRequiredHint:
    """A connect-required degrade points at the connect route only in App mode; with App
    mode off it points at Settings, GitHub (the card line and the token form), never at
    a route that only refuses."""

    async def _degrade(self):
        from services.mcp.consumer.connector import DegradationReason
        from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

        return await GitHubMCPSpatialAdapter().degrade(DegradationReason.CONNECT_REQUIRED)

    async def test_app_mode_points_at_the_connect_route(self, app_on):
        from services.mcp.consumer import github_adapter as adapter_mod

        degraded = await self._degrade()
        assert degraded.action_hint == adapter_mod._CONNECT_URL
        assert degraded.action_hint == "/api/v1/settings/integrations/github/connect"
        assert degraded.user_message == "Connect GitHub to continue."

    async def test_app_mode_off_points_at_the_settings_page(self, app_off):
        from services.mcp.consumer import github_adapter as adapter_mod

        degraded = await self._degrade()
        assert degraded.action_hint == adapter_mod._GITHUB_SETTINGS_URL
        assert degraded.action_hint == "/settings/integrations/github"
        assert degraded.user_message == adapter_mod.GITHUB_CONNECT_REQUIRED_NO_APP_LINE

    def test_the_words(self):
        from services.mcp.consumer import github_adapter as adapter_mod

        # CXO, 2026-11-27 (issue 2261); this pin makes a change of words a diff.
        assert adapter_mod.GITHUB_CONNECT_REQUIRED_NO_APP_LINE == (
            "Add a GitHub personal access token in Settings, under Integrations, to continue."
        )

    def test_the_test_results_words(self):
        from services.mcp.consumer import github_adapter as adapter_mod

        # CXO, 2026-11-27 (issue 2261): the Settings Test result's own line.
        assert adapter_mod.GITHUB_CONNECT_REQUIRED_NO_APP_TEST_LINE == (
            "Add a GitHub personal access token on the GitHub settings page to continue."
        )

    async def test_the_test_result_with_app_mode_off_uses_its_own_line(self, app_off):
        from services.mcp.consumer import github_adapter as adapter_mod
        from web.api.routes.integrations import _github_failure

        result = _github_failure(await self._degrade())
        assert result["success"] is False
        assert result["error"] == adapter_mod.GITHUB_CONNECT_REQUIRED_NO_APP_TEST_LINE
        assert result["error_type"] == "connect_required"

    async def test_the_test_result_in_app_mode_keeps_todays_line(self, app_on):
        from web.api.routes.integrations import _github_failure

        result = _github_failure(await self._degrade())
        assert result["error"] == "Connect GitHub to continue."

    async def test_the_test_result_for_another_reason_is_untouched(self, app_off):
        from services.mcp.consumer.connector import DegradationReason
        from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter
        from web.api.routes.integrations import _github_failure

        degraded = await GitHubMCPSpatialAdapter().degrade(DegradationReason.UNREACHABLE)
        assert _github_failure(degraded)["error"] == degraded.user_message

    def test_the_test_toasts_fix_line_with_app_mode_off(self, app_off):
        """Found by the App-off browser render (Lead, 2026-11-27): the Integrations
        page's Test toast prints the guidance row's message and fix, never ``error``.
        Its fix said "Connect with GitHub", which that install does not offer."""
        from services.mcp.consumer import github_adapter as adapter_mod
        from web.api.routes.integrations import _get_error_guidance

        message, fix = _get_error_guidance("github", "connect_required")
        assert message == "GitHub isn't connected for your account."
        assert fix == adapter_mod.GITHUB_CONNECT_REQUIRED_NO_APP_FIX_LINE
        # CXO, 2026-11-27 (issue 2261); this pin makes a change of words a diff.
        assert fix == "In Settings → Integrations → GitHub, add a personal access token."
        assert "Connect with GitHub" not in f"{message} {fix}"

    def test_the_test_toasts_fix_line_in_app_mode_is_unchanged(self, app_on):
        from web.api.routes.integrations import INTEGRATION_REGISTRY, _get_error_guidance

        message, fix = _get_error_guidance("github", "connect_required")
        assert fix == "In Settings → Integrations → GitHub, Connect with GitHub"
        # The table row is never rewritten: the branch is at read time.
        row = INTEGRATION_REGISTRY["github"]["errors"]["connect_required"]
        assert row["fix"] == fix

    def test_the_table_row_survives_an_app_off_read(self, app_off):
        from web.api.routes.integrations import INTEGRATION_REGISTRY, _get_error_guidance

        _get_error_guidance("github", "connect_required")
        row = INTEGRATION_REGISTRY["github"]["errors"]["connect_required"]
        assert row["fix"] == "In Settings → Integrations → GitHub, Connect with GitHub"

    def test_other_github_rows_and_other_integrations_are_untouched(self, app_off):
        from web.api.routes.integrations import _get_error_guidance

        assert _get_error_guidance("github", "stale_token")[1] == (
            "In Settings → Integrations → GitHub, Reconnect with GitHub"
        )
        assert _get_error_guidance("github", "unreachable")[1] == "Try again in a few minutes"

    async def test_other_reasons_carry_no_hint_in_either_mode(self, app_off):
        from services.mcp.consumer.connector import DegradationReason
        from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

        degraded = await GitHubMCPSpatialAdapter().degrade(DegradationReason.UNREACHABLE)
        assert degraded.action_hint is None


# ── the personal-token hint (Arch 2026-11-27) ────────────────────────────────────────


class TestThePersonalTokenHint:
    """The token form asks for a fine-grained token with ADR-081 D3's permissions, links
    GitHub's fine-grained token page, and names no classic ``repo`` scope, in either
    mode. The input's placeholder is shape-neutral."""

    def test_the_words(self):
        from services.integrations.github import token_validator as tv

        # CXO, 2026-11-27 (issue 2261); this pin makes a change of words a diff.
        assert tv.GITHUB_PERSONAL_TOKEN_HINT == (
            "Create a fine-grained token at github.com/settings/personal-access-tokens/new. "
            "Choose the repositories you want Piper to reach, and give it these repository "
            "permissions: Contents: read; Issues: read and write; Pull requests: read and "
            "write."
        )
        assert tv.GITHUB_FINE_GRAINED_TOKEN_PAGE_URL == (
            "https://github.com/settings/personal-access-tokens/new"
        )

    @staticmethod
    def _hint(reply_text):
        start = reply_text.index('<p class="form-hint" id="pat-token-hint">')
        return reply_text[start : reply_text.index("</p>", start)]

    @pytest.mark.parametrize("mode", ["app_on", "app_off"])
    def test_the_rendered_hint(self, request, client, mode):
        from services.integrations.github import token_validator as tv

        request.getfixturevalue(mode)
        reply = client.get("/settings/integrations/github")
        assert reply.status_code == 200
        hint_html = self._hint(reply.text)
        hint_text = html.unescape(re.sub(r"<[^>]+>", "", hint_html))
        assert hint_text == tv.GITHUB_PERSONAL_TOKEN_HINT  # the one sentence, as written
        assert "fine-grained token" in hint_text
        assert (
            f'<a href="{tv.GITHUB_FINE_GRAINED_TOKEN_PAGE_URL}" target="_blank" '
            f'rel="noopener">{tv.GITHUB_FINE_GRAINED_TOKEN_PAGE_TEXT}</a>'
        ) in hint_html
        # HOST's pin: Contents is read only.
        assert "Contents: read" in hint_text
        assert "Contents: read and write" not in hint_text and "Contents: write" not in hint_text
        assert "full repository access" not in hint_text.lower()
        plain = html.unescape(re.sub(r"<[^>]+>", "", reply.text))
        assert "repo scope" not in plain and "`repo` scope" not in plain
        assert "<code>repo</code>" not in reply.text
        assert "settings/tokens/new" not in reply.text  # the classic token page is gone
        assert reply.text.index('id="pat-form-section"') < reply.text.index('id="pat-token-hint"')

    @pytest.mark.parametrize("mode", ["app_on", "app_off"])
    def test_the_placeholder_no_longer_shows_a_classic_token_shape(self, request, client, mode):
        request.getfixturevalue(mode)
        reply = client.get("/settings/integrations/github")
        tag = re.search(r'<input\b[^>]*\bid="token"[^>]*>', reply.text, flags=re.S).group(0)
        assert 'placeholder="Paste your token"' in tag and "ghp_" not in tag
        assert "const PAT_TOKEN_PLACEHOLDER = 'Paste your token';" in reply.text

    def test_the_form_heading_drops_or_with_app_mode_off(self, client, app_off):
        _, text = _page(client)
        assert "Connect with a personal access token:" in text
        assert "Or connect with a personal access token:" not in text

    def test_the_form_heading_keeps_or_in_app_mode(self, client, app_on):
        _, text = _page(client)
        assert "Or connect with a personal access token:" in text
