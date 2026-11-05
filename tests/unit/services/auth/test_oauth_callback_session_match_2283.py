"""#2283 (Arch 2026-11-04 21:11; P0 tenancy) and #2281: an OAuth callback stores a provider
grant only for the browser signed in as the account the ``state`` names.

Two accounts, A and B. For each connector: A's state with B's session stores nothing; with
A's session it proceeds to the exchange; with no session it stores nothing. In every refused
case the state is consumed and the code is never exchanged, so CXO's "Nothing was connected
yet" is true by construction. The routes turn a refusal into an HTML page, never JSON; the
login page says CXO's sentence.
"""

from __future__ import annotations

import re
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from services.auth.oauth_callback_guard import (
    SIGN_IN_TO_FINISH_LINE,
    OAuthCallbackSessionMismatch,
    refusal_redirect_url,
    require_session_matches_state,
    sign_in_to_finish_line,
)

ROOT = Path(__file__).resolve().parents[4]
A, B = "aaaaaaaa-2283-4000-8000-00000000000a", "bbbbbbbb-2283-4000-8000-00000000000b"


class TestTheGuard:
    def test_same_user_passes(self):
        require_session_matches_state(A, A)

    def test_another_account_is_refused_as_signed_in(self):
        with pytest.raises(OAuthCallbackSessionMismatch) as e:
            require_session_matches_state(A, B)
        assert e.value.signed_in is True

    @pytest.mark.parametrize("session", [None, ""])
    def test_no_session_is_refused_as_signed_out(self, session):
        with pytest.raises(OAuthCallbackSessionMismatch) as e:
            require_session_matches_state(A, session)
        assert e.value.signed_in is False

    def test_where_a_refusal_goes(self):
        out, wrong = OAuthCallbackSessionMismatch(False), OAuthCallbackSessionMismatch(True)
        assert (
            refusal_redirect_url("github", out)
            == "/login?connect=github&next=%2Fsettings%2Fintegrations"
        )
        assert (
            refusal_redirect_url("calendar", out, wizard=True)
            == "/login?connect=calendar&next=%2Fsetup"
        )
        assert (
            refusal_redirect_url("slack", wrong)
            == "/settings/integrations?slack_error=wrong_account"
        )
        assert (
            refusal_redirect_url("calendar", wrong, wizard=True)
            == "/setup?calendar_error=wrong_account#step-2"
        )

    def test_cxos_words(self):
        assert sign_in_to_finish_line("github") == (
            "Sign in to finish connecting GitHub. Nothing was connected yet. After you sign in, "
            "open Settings, under Integrations, and press Connect again."
        )
        assert sign_in_to_finish_line("calendar").startswith(
            "Sign in to finish connecting Google Calendar."
        )
        assert sign_in_to_finish_line("slack").startswith("Sign in to finish connecting Slack.")
        assert sign_in_to_finish_line("nonsense") is None and sign_in_to_finish_line(None) is None
        assert "{name}" in SIGN_IN_TO_FINISH_LINE


class TestGitHubHandler:
    def _handler(self):
        from services.mcp.consumer.github_oauth_handler import GitHubOAuthHandler

        h = GitHubOAuthHandler.__new__(GitHubOAuthHandler)
        h.client_id, h.client_secret = "Iv1.c", "s"
        h.redirect_uri, h.scopes = "https://alpha.example/cb", ["repo"]
        return h

    @pytest.mark.asyncio
    @pytest.mark.parametrize("session,signed_in", [(B, True), (None, False)])
    async def test_a_refused_callback_never_exchanges_and_consumes_the_state(
        self, session, signed_in
    ):
        h = self._handler()
        _, state = h.generate_authorization_url(user_id=A)
        exchange = AsyncMock(side_effect=AssertionError("the code must not be exchanged"))
        with patch.object(type(h), "_exchange_code_for_tokens", exchange):
            with pytest.raises(OAuthCallbackSessionMismatch) as e:
                await h.handle_oauth_callback("code", state, session_user_id=session)
        assert e.value.signed_in is signed_in
        assert h.verify_state(state) == (False, None)  # consumed: a replay can't succeed

    @pytest.mark.asyncio
    async def test_the_states_own_account_proceeds(self):
        h = self._handler()
        _, state = h.generate_authorization_url(user_id=A)
        tokens = SimpleNamespace(access_token="gho_x")
        with (
            patch.object(type(h), "_exchange_code_for_tokens", AsyncMock(return_value=tokens)),
            patch.object(type(h), "_get_login", AsyncMock(return_value="alice")),
        ):
            result = await h.handle_oauth_callback("code", state, session_user_id=A)
        assert result["user_id"] == A and result["login"] == "alice"


class TestCalendarHandler:
    def _handler(self, monkeypatch):
        monkeypatch.setenv("GOOGLE_CLIENT_ID", "cid")
        monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "csecret")
        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler

        return GoogleCalendarOAuthHandler()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("session,signed_in", [(B, True), (None, False)])
    async def test_a_refused_callback_never_exchanges(self, monkeypatch, session, signed_in):
        h = self._handler(monkeypatch)
        _, state = h.generate_authorization_url(user_id=A)
        with patch.object(
            type(h),
            "_exchange_code_for_tokens",
            AsyncMock(side_effect=AssertionError("no exchange")),
        ):
            with pytest.raises(OAuthCallbackSessionMismatch) as e:
                await h.handle_oauth_callback("code", state, session_user_id=session)
        assert e.value.signed_in is signed_in
        assert h.verify_state(state)[0] is False  # consumed

    @pytest.mark.asyncio
    async def test_the_states_own_account_proceeds(self, monkeypatch):
        h = self._handler(monkeypatch)
        _, state = h.generate_authorization_url(user_id=A)
        tokens = SimpleNamespace(access_token="ya29", refresh_token="r")
        with (
            patch.object(type(h), "_exchange_code_for_tokens", AsyncMock(return_value=tokens)),
            patch.object(
                type(h), "_get_user_info", AsyncMock(return_value={"email": "a@example.invalid"})
            ),
        ):
            result = await h.handle_oauth_callback("code", state, session_user_id=A)
        assert result["user_id"] == A


class TestSlackHandlerOrdering:
    def test_the_check_runs_after_the_state_is_consumed_and_before_the_exchange(self):
        src = (ROOT / "services/integrations/slack/oauth_handler.py").read_text()
        body = src[src.index("async def handle_oauth_callback(") :]
        body = body[
            : body.index("\n    async def ", 10) if "\n    async def " in body[10:] else len(body)
        ]
        pop = body.index("await self._pop_oauth_state(nonce)")
        check = body.index("require_session_matches_state(user_id, session_user_id)")
        exchange = body.index("_exchange_code")
        assert pop < check < exchange
        assert "if isinstance(e, OAuthCallbackSessionMismatch):" in body  # not wrapped away


class TestEveryCallbackPassesTheSession:
    """All five callbacks (Settings: GitHub, Calendar, Slack; the wizard: Calendar, Slack)."""

    def test_no_handler_call_omits_the_session(self):
        for path in ("web/api/routes/settings_integrations.py", "web/api/routes/setup.py"):
            src = (ROOT / path).read_text()
            calls = src.count(".handle_oauth_callback(")
            with_session = src.count('session_user_id=getattr(session, "sub", None)')
            assert calls and calls == with_session, (path, calls, with_session)

    def test_the_count_is_five(self):
        n = sum(
            (ROOT / p).read_text().count("Depends(get_current_user_or_none),  # #2283")
            for p in ("web/api/routes/settings_integrations.py", "web/api/routes/setup.py")
        )
        assert n == 5

    def test_the_handlers_require_the_argument(self):
        import inspect

        from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler
        from services.integrations.slack.oauth_handler import SlackOAuthHandler
        from services.mcp.consumer.github_oauth_handler import GitHubOAuthHandler

        for cls in (GitHubOAuthHandler, GoogleCalendarOAuthHandler, SlackOAuthHandler):
            p = inspect.signature(cls.handle_oauth_callback).parameters["session_user_id"]
            assert p.kind is inspect.Parameter.KEYWORD_ONLY and p.default is inspect.Parameter.empty


class TestTheRoutesAnswerHTML:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "signed_in,expected",
        [
            (False, "/login?connect=github&next=%2Fsettings%2Fintegrations"),
            (True, "/settings/integrations?github_error=wrong_account"),
        ],
    )
    async def test_github_callback_refusal_redirects_and_stores_nothing(self, signed_in, expected):
        from web.api.routes import settings_integrations as si

        handler = AsyncMock(side_effect=OAuthCallbackSessionMismatch(signed_in))
        persist = AsyncMock(side_effect=AssertionError("nothing may be stored"))
        with (
            patch(
                "services.mcp.consumer.github_oauth_handler.GitHubOAuthHandler.handle_oauth_callback",
                handler,
            ),
            patch(
                "services.mcp.consumer.github_oauth_handler.GitHubOAuthHandler.__init__",
                lambda self: None,
            ),
            patch("services.mcp.consumer.github_oauth_handler.persist_github_connection", persist),
        ):
            resp = await si.handle_github_callback(code="c", state="s", error=None, session=None)
        assert resp.status_code == 302 and resp.headers["location"] == expected

    def test_the_login_page_says_cxos_sentence_for_a_connect_return(self):
        src = (ROOT / "templates/login.html").read_text()
        assert "{% if connect_notice %}" in src and "{{ connect_notice }}" in src
        ui = (ROOT / "web/api/routes/ui.py").read_text()
        assert 'sign_in_to_finish_line(request.query_params.get("connect"))' in ui

    def test_no_callback_page_shows_raw_json_words(self):
        for path in ("services/auth/oauth_callback_guard.py", "templates/login.html"):
            assert "authentication_required" not in (ROOT / path).read_text()


class TestTheExemptList:
    def test_the_three_settings_callbacks_are_exempt_only_with_the_route_check(self):
        from services.auth.auth_middleware import EXEMPT_OAUTH_CALLBACK_PATHS

        assert set(EXEMPT_OAUTH_CALLBACK_PATHS) == {
            "/api/v1/settings/integrations/slack/callback",
            "/api/v1/settings/integrations/calendar/callback",
            "/api/v1/settings/integrations/github/callback",
        }


class TestTheHostSwitch:
    """#2281 (b), required by #2283: a Connect started on another host than the callback's
    is sent to the callback's host first, where the session the callback checks exists."""

    def _req(self, host):
        return SimpleNamespace(url=SimpleNamespace(hostname=host))

    def test_another_host_is_sent_to_the_callbacks_host(self):
        from services.auth.oauth_callback_guard import host_switch_url

        cb = "https://alpha.pipermorgan.ai/api/v1/settings/integrations/github/callback"
        assert (
            host_switch_url(self._req("beta.pipermorgan.ai"), cb, "/settings/integrations/github")
            == "https://alpha.pipermorgan.ai/settings/integrations/github"
        )

    def test_the_same_host_or_an_unreadable_one_does_not_switch(self):
        from services.auth.oauth_callback_guard import host_switch_url

        cb = "https://alpha.pipermorgan.ai/api/v1/settings/integrations/github/callback"
        assert host_switch_url(self._req("alpha.pipermorgan.ai"), cb, "/x") is None
        assert host_switch_url(self._req("ALPHA.pipermorgan.ai"), cb, "/x") is None
        assert host_switch_url(None, cb, "/x") is None
        assert host_switch_url(self._req("alpha.pipermorgan.ai"), None, "/x") is None
        assert host_switch_url(self._req("localhost"), "http://localhost:8001/cb", "/x") is None

    @pytest.mark.asyncio
    async def test_the_github_connect_route_switches_before_minting_a_state(self, monkeypatch):
        from web.api.routes import settings_integrations as si

        monkeypatch.setenv("GITHUB_OAUTH_CLIENT_ID", "Iv1.c")
        monkeypatch.setenv("GITHUB_OAUTH_CLIENT_SECRET", "s")
        monkeypatch.setenv(
            "GITHUB_OAUTH_REDIRECT_URI",
            "https://alpha.pipermorgan.ai/api/v1/settings/integrations/github/callback",
        )
        mint = AssertionError("no state is minted on the wrong host")
        with patch(
            "services.mcp.consumer.github_oauth_handler.GitHubOAuthHandler.generate_authorization_url",
            side_effect=mint,
        ):
            res = await si.connect_github(
                current_user=SimpleNamespace(sub=A), request=self._req("beta.pipermorgan.ai")
            )
        assert res == {
            "switch_host_url": "https://alpha.pipermorgan.ai/settings/integrations/github"
        }

    def test_the_three_pages_follow_the_switch(self):
        for page in ("settings_github.html", "settings_calendar.html", "settings_slack.html"):
            assert "switch_host_url" in (ROOT / "templates" / page).read_text(), page
