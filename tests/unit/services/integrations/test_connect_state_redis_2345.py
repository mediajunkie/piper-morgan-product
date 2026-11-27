"""#2345: GitHub and Google Calendar keep the pending Connect state in Redis.

Ruled by Arch (decisions.log 2026-10-28 15:58 for 2189, and 2026-11-12): the state
survives a process restart between the start and the callback, the Slack way: a key per
nonce under a prefix of the connector's own, a TTL of ``STATE_EXPIRATION``, one ``GETDEL``
read. Redis down refuses at the start (no authorize URL) and at the callback.

No real Redis and no network: ``RedisFactory.redis_scope`` yields Slack's in-memory fake
(``test_oauth_redis_state_1109._FakeRedis``) with a controllable clock added here.
"""

from __future__ import annotations

import ast
import json
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import HTTPException

from services.auth import oauth_state_store as store_mod
from services.auth.oauth_state_store import (
    CALENDAR_STATE_KEY_PREFIX,
    GITHUB_STATE_KEY_PREFIX,
    OAuthStateStoreUnavailable,
)
from services.integrations.calendar import oauth_handler as cal_mod
from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler
from services.integrations.slack.oauth_handler import OAUTH_STATE_KEY_PREFIX as SLACK_PREFIX
from services.mcp.consumer import github_app_grant as grant_mod
from services.mcp.consumer import github_oauth_handler as gh_mod
from services.mcp.consumer.github_oauth_handler import GitHubOAuthHandler
from tests.unit.services.integrations.slack.test_oauth_redis_state_1109 import _FakeRedis

ROOT = Path(__file__).resolve().parents[4]
A, B = "aaaaaaaa-2345-4000-8000-00000000000a", "bbbbbbbb-2345-4000-8000-00000000000b"


class _ClockedFakeRedis(_FakeRedis):
    """Slack's fake plus a clock: a key whose TTL has run out reads as absent."""

    def __init__(self):
        super().__init__()
        self.now = 0.0
        self.expires: dict = {}

    async def setex(self, key, ttl_seconds, value):
        self.expires[key] = self.now + int(ttl_seconds)
        return await super().setex(key, ttl_seconds, value)

    def advance(self, seconds: float) -> None:
        self.now += seconds
        for key, at in list(self.expires.items()):
            if self.now >= at:
                self.store.pop(key, None)
                self.ttls.pop(key, None)
                self.expires.pop(key, None)

    async def getdel(self, key):
        self.expires.pop(key, None)
        return await super().getdel(key)


class _DownRedis:
    """Every command fails the way redis-py does when the server can't be reached."""

    async def setex(self, *a, **k):
        from redis.exceptions import ConnectionError as RedisConnectionError

        raise RedisConnectionError("Error 111 connecting to localhost:6379. Connection refused.")

    async def getdel(self, *a, **k):
        from redis.exceptions import ConnectionError as RedisConnectionError

        raise RedisConnectionError("Error 111 connecting to localhost:6379. Connection refused.")

    async def close(self):
        pass


def _patch_redis(client):
    @asynccontextmanager
    async def _scope():
        yield client

    return patch("services.cache.redis_factory.RedisFactory.redis_scope", side_effect=_scope)


@pytest.fixture
def redis_fake():
    fake = _ClockedFakeRedis()
    with _patch_redis(fake):
        yield fake


@pytest.fixture
def redis_down():
    with _patch_redis(_DownRedis()):
        yield


@pytest.fixture(autouse=True)
def _creds(monkeypatch):
    monkeypatch.setenv("GITHUB_OAUTH_CLIENT_ID", "cid")
    monkeypatch.setenv("GITHUB_OAUTH_CLIENT_SECRET", "csecret")
    monkeypatch.setenv("GOOGLE_CLIENT_ID", "gid")
    monkeypatch.setenv("GOOGLE_CLIENT_SECRET", "gsecret")
    # Issue 2261: a GitHub connect runs only in App mode, so the App's (fake) values are
    # set; the classic ones stay beside them and are not read by a connect.
    monkeypatch.setenv(grant_mod.ENV_APP_CLIENT_ID, "test-app-client-id")
    monkeypatch.setenv(grant_mod.ENV_APP_CLIENT_SECRET, "test-app-client-secret")


def _nonce(state: str) -> str:
    padded = state + "=" * (-len(state) % 4)
    import base64

    return json.loads(base64.urlsafe_b64decode(padded))["nonce"]


def _claims(sub=A):
    return SimpleNamespace(sub=sub)


# ── the acceptance row: "survives a process restart between start and callback" ──


class TestSurvivesARestart:
    async def test_github_state_validates_on_a_second_instance(self, redis_fake):
        _, state = await GitHubOAuthHandler().generate_authorization_url(A)
        # A second instance shares nothing with the first but the (fake) Redis.
        assert await GitHubOAuthHandler().verify_state(state) == (True, A)

    async def test_github_callback_on_a_second_instance_reaches_the_exchange(self, redis_fake):
        _, state = await GitHubOAuthHandler().generate_authorization_url(A)
        h2 = GitHubOAuthHandler()
        tokens = SimpleNamespace(access_token="gho_x")
        with (
            patch.object(
                GitHubOAuthHandler, "_exchange_code_for_tokens", AsyncMock(return_value=tokens)
            ),
            patch.object(GitHubOAuthHandler, "_get_login", AsyncMock(return_value="alice")),
        ):
            result = await h2.handle_oauth_callback("code", state, session_user_id=A)
        assert result["user_id"] == A

    async def test_calendar_settings_start_validates_on_a_second_instance(self, redis_fake):
        from web.api.routes import settings_integrations as si

        res = await si.connect_calendar(current_user=_claims(), request=None)
        assert res["auth_url"].startswith(GoogleCalendarOAuthHandler.AUTHORIZATION_URL)
        assert await GoogleCalendarOAuthHandler().verify_state(res["state"]) == (True, A)

    async def test_calendar_setup_start_validates_on_a_second_instance(self, redis_fake):
        from web.api.routes import setup as setup_mod

        res = await setup_mod.start_calendar_oauth(current_user=_claims())
        assert res["auth_url"].startswith(GoogleCalendarOAuthHandler.AUTHORIZATION_URL)
        assert await GoogleCalendarOAuthHandler().verify_state(res["state"]) == (True, A)

    async def test_github_settings_start_validates_on_a_second_instance(self, redis_fake):
        from web.api.routes import settings_integrations as si

        res = await si.connect_github(current_user=_claims(), request=None)
        assert res["auth_url"].startswith(GitHubOAuthHandler.AUTHORIZATION_URL)
        assert await GitHubOAuthHandler().verify_state(res["state"]) == (True, A)


# ── storage shape: prefix, value, TTL ──


@pytest.mark.parametrize(
    "make,prefix",
    [
        (GitHubOAuthHandler, GITHUB_STATE_KEY_PREFIX),
        (GoogleCalendarOAuthHandler, CALENDAR_STATE_KEY_PREFIX),
    ],
)
class TestStoredEntry:
    async def test_key_value_and_ttl(self, redis_fake, make, prefix):
        h = make()
        _, state = await h.generate_authorization_url(A)
        key = f"{prefix}{_nonce(state)}"
        assert list(redis_fake.store) == [key]
        assert redis_fake.ttls[key] == make.STATE_EXPIRATION == 900
        value = json.loads(redis_fake.store[key])
        assert set(value) == {"created_at", "user_id"} and value["user_id"] == A

    async def test_a_replayed_state_is_refused(self, redis_fake, make, prefix):
        h = make()
        _, state = await h.generate_authorization_url(A)
        assert await h.verify_state(state) == (True, A)
        assert redis_fake.store == {}  # GETDEL removed it on the first read
        assert await make().verify_state(state) == (False, None)

    async def test_a_ttl_expired_state_is_refused(self, redis_fake, make, prefix):
        h = make()
        _, state = await h.generate_authorization_url(A)
        redis_fake.advance(make.STATE_EXPIRATION)
        assert redis_fake.store == {}
        assert await h.verify_state(state) == (False, None)

    async def test_an_old_created_at_is_refused_with_the_key_still_present(
        self, redis_fake, make, prefix
    ):
        import time

        h = make()
        _, state = await h.generate_authorization_url(A)
        key = f"{prefix}{_nonce(state)}"
        value = json.loads(redis_fake.store[key])
        value["created_at"] = time.time() - make.STATE_EXPIRATION - 1
        redis_fake.store[key] = json.dumps(value).encode()
        assert await h.verify_state(state) == (False, None)
        assert key not in redis_fake.store  # consumed even when refused

    async def test_a_state_naming_another_user_is_refused(self, redis_fake, make, prefix):
        import base64

        h = make()
        _, state = await h.generate_authorization_url(A)
        forged = (
            base64.urlsafe_b64encode(json.dumps({"user_id": B, "nonce": _nonce(state)}).encode())
            .decode()
            .rstrip("=")
        )
        assert await h.verify_state(forged) == (False, None)


class TestPrefixesKeepConnectorsApart:
    def test_the_three_prefixes_differ(self):
        prefixes = {GITHUB_STATE_KEY_PREFIX, CALENDAR_STATE_KEY_PREFIX, SLACK_PREFIX}
        assert len(prefixes) == 3
        for p in prefixes:
            assert not any(q != p and q.startswith(p) for q in prefixes)

    async def test_a_github_state_does_not_validate_in_calendar(self, redis_fake):
        _, state = await GitHubOAuthHandler().generate_authorization_url(A)
        assert await GoogleCalendarOAuthHandler().verify_state(state) == (False, None)
        assert await GitHubOAuthHandler().verify_state(state) == (True, A)  # untouched

    async def test_a_calendar_state_does_not_validate_in_github(self, redis_fake):
        _, state = await GoogleCalendarOAuthHandler().generate_authorization_url(A)
        assert await GitHubOAuthHandler().verify_state(state) == (False, None)
        assert await GoogleCalendarOAuthHandler().verify_state(state) == (True, A)


# ── Redis down: refuse at the start (no URL) and at the callback ──


class TestRedisDownAtTheStart:
    @pytest.mark.parametrize(
        "make,mod", [(GitHubOAuthHandler, gh_mod), (GoogleCalendarOAuthHandler, cal_mod)]
    )
    async def test_the_handler_raises_and_builds_no_url(self, redis_down, make, mod):
        spy = MagicMock(side_effect=AssertionError("no authorize URL may be built"))
        with patch.object(mod, "urlencode", spy), pytest.raises(OAuthStateStoreUnavailable):
            await make().generate_authorization_url(A)
        spy.assert_not_called()

    async def test_github_settings_start_says_so(self, redis_down):
        from web.api.routes import settings_integrations as si
        from web.api.routes.setup import GITHUB_CONNECT_COULD_NOT_START_MESSAGE

        with pytest.raises(HTTPException) as e:
            await si.connect_github(current_user=_claims(), request=None)
        assert e.value.status_code == 503
        assert e.value.detail == GITHUB_CONNECT_COULD_NOT_START_MESSAGE
        assert e.value.detail == (
            "The GitHub connection couldn't start just now. "
            "Try again in a moment; if it keeps failing, tell us."
        )

    async def test_calendar_settings_start_says_so(self, redis_down):
        from web.api.routes import settings_integrations as si
        from web.api.routes.setup import CALENDAR_CONNECT_COULD_NOT_START_MESSAGE

        with pytest.raises(HTTPException) as e:
            await si.connect_calendar(current_user=_claims(), request=None)
        assert e.value.status_code == 503
        assert e.value.detail == CALENDAR_CONNECT_COULD_NOT_START_MESSAGE

    async def test_calendar_setup_start_says_so(self, redis_down):
        from web.api.routes import setup as setup_mod

        with pytest.raises(HTTPException) as e:
            await setup_mod.start_calendar_oauth(current_user=_claims())
        assert e.value.status_code == 503
        assert e.value.detail == setup_mod.CALENDAR_CONNECT_COULD_NOT_START_MESSAGE

    def test_the_github_page_and_the_wizard_show_the_routes_line(self):
        page = (ROOT / "templates/settings_github.html").read_text()
        body = page[page.index("async function connectGitHubOAuth()") :]
        body = body[: body.index("\n      }\n")]
        assert "parseApiDetail(errBody.detail" in body
        wizard = (ROOT / "web/static/js/setup.js").read_text()
        start = wizard[wizard.index("/api/v1/setup/calendar/oauth/start") :][:1200]
        assert "data.detail" in start


class TestRedisDownAtTheCallback:
    @pytest.mark.parametrize("make", [GitHubOAuthHandler, GoogleCalendarOAuthHandler])
    async def test_verify_refuses(self, redis_fake, make):
        _, state = await make().generate_authorization_url(A)
        with _patch_redis(_DownRedis()):
            assert await make().verify_state(state) == (False, None)

    @pytest.mark.parametrize("make", [GitHubOAuthHandler, GoogleCalendarOAuthHandler])
    async def test_the_callback_refuses_before_any_exchange(self, redis_fake, make):
        _, state = await make().generate_authorization_url(A)
        exchange = AsyncMock(side_effect=AssertionError("no exchange"))
        with (
            _patch_redis(_DownRedis()),
            patch.object(make, "_exchange_code_for_tokens", exchange),
            pytest.raises(ValueError, match="Invalid or expired state token"),
        ):
            await make().handle_oauth_callback("code", state, session_user_id=A)

    async def test_the_settings_routes_redirect_with_the_existing_error(self, redis_fake):
        from web.api.routes import settings_integrations as si

        _, gh_state = await GitHubOAuthHandler().generate_authorization_url(A)
        _, cal_state = await GoogleCalendarOAuthHandler().generate_authorization_url(A)
        with _patch_redis(_DownRedis()):
            gh = await si.handle_github_callback(
                code="c", state=gh_state, error=None, browser_session=_claims()
            )
            cal = await si.handle_calendar_callback(
                code="c", state=cal_state, error=None, browser_session=_claims()
            )
        assert gh.headers["location"] == "/settings/integrations?github_error=callback_failed"
        assert cal.headers["location"] == "/settings/integrations?calendar_error=callback_failed"

    async def test_the_setup_route_redirects_with_the_existing_error(self, redis_fake):
        from web.api.routes import setup as setup_mod

        _, state = await GoogleCalendarOAuthHandler().generate_authorization_url(A)
        with _patch_redis(_DownRedis()):
            res = await setup_mod.handle_calendar_oauth_callback(
                code="c", state=state, error=None, browser_session=_claims()
            )
        assert res.headers["location"] == "/setup?calendar_error=callback_failed#step-2"


# ── no in-process store, and no state or nonce in a log line ──


class TestNoInProcessStore:
    @pytest.mark.parametrize(
        "path",
        [
            "services/mcp/consumer/github_oauth_handler.py",
            "services/integrations/calendar/oauth_handler.py",
            "services/auth/oauth_state_store.py",
        ],
    )
    def test_no_pending_dict_and_no_module_level_mutable_map(self, path):
        src = (ROOT / path).read_text()
        assert "_PENDING_STATES" not in src
        assert "lru_cache" not in src and "functools.cache" not in src
        tree = ast.parse(src)
        mutable_calls = {"dict", "set", "defaultdict", "OrderedDict", "WeakValueDictionary"}
        nodes = list(tree.body)
        for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
            nodes.extend(cls.body)  # class attributes are process-wide too
        for node in nodes:
            value = (
                getattr(node, "value", None)
                if isinstance(node, (ast.Assign, ast.AnnAssign))
                else None
            )
            if value is None:
                continue
            assert not isinstance(value, (ast.Dict, ast.Set, ast.DictComp, ast.SetComp)), (
                path,
                ast.unparse(node),
            )
            if isinstance(value, ast.Call):
                name = getattr(value.func, "id", None) or getattr(value.func, "attr", None)
                assert name not in mutable_calls, (path, ast.unparse(node))


class TestNothingSecretIsLogged:
    async def test_no_log_call_carries_the_state_or_the_nonce(self, redis_fake):
        from web.api.routes import settings_integrations as si
        from web.api.routes import setup as setup_mod

        loggers = {name: MagicMock() for name in ("gh", "cal", "store", "si", "setup")}
        targets = {
            "gh": gh_mod,
            "cal": cal_mod,
            "store": store_mod,
            "si": si,
            "setup": setup_mod,
        }
        seen_states = []
        with (
            patch.object(gh_mod, "logger", loggers["gh"]),
            patch.object(cal_mod, "logger", loggers["cal"]),
            patch.object(store_mod, "logger", loggers["store"]),
            patch.object(si, "logger", loggers["si"]),
            patch.object(setup_mod, "logger", loggers["setup"]),
        ):
            for make in (GitHubOAuthHandler, GoogleCalendarOAuthHandler):
                h = make()
                _, ok_state = await h.generate_authorization_url(A)
                await h.verify_state(ok_state)  # success
                await h.verify_state(ok_state)  # replay
                _, expired = await h.generate_authorization_url(A)
                redis_fake.advance(make.STATE_EXPIRATION)
                await h.verify_state(expired)  # expired
                seen_states += [ok_state, expired]
            seen_states.append(
                (await si.connect_github(current_user=_claims(), request=None))["state"]
            )
            seen_states.append(
                (await si.connect_calendar(current_user=_claims(), request=None))["state"]
            )
            seen_states.append(
                (await setup_mod.start_calendar_oauth(current_user=_claims()))["state"]
            )
            with _patch_redis(_DownRedis()):
                for make in (GitHubOAuthHandler, GoogleCalendarOAuthHandler):
                    await make().verify_state(seen_states[0])
                    with pytest.raises(OAuthStateStoreUnavailable):
                        await make().generate_authorization_url(A)
                for call in (
                    si.connect_github(current_user=_claims(), request=None),
                    si.connect_calendar(current_user=_claims(), request=None),
                    setup_mod.start_calendar_oauth(current_user=_claims()),
                ):
                    with pytest.raises(HTTPException):
                        await call
        secrets_seen = set(seen_states) | {_nonce(s) for s in seen_states}
        logged = []
        for mock in loggers.values():
            for call in mock.mock_calls:
                logged.append(repr(call.args) + repr(call.kwargs))
        assert logged, "the loggers were not exercised"
        for line in logged:
            for secret in secrets_seen:
                assert secret not in line


# ── What the person receives, through the app's real handler (issues 2345 and 2428) ──
#
# The tests above call the route functions, which shows the route builds the line. They do
# not show a person gets it: the app's handler masks every 5xx that is not marked
# user-facing. These go through that handler.


def _through_the_real_handler(route_function):
    """Call a start route's function inside a small app that carries the REAL exception
    handler from ``web.app``, and return what a client would receive."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from web.app import app as real_app

    app = FastAPI()
    app.add_exception_handler(HTTPException, real_app.exception_handlers[HTTPException])

    @app.get("/start")
    async def _start():
        return await route_function()

    return TestClient(app).get("/start")


class TestThePersonGetsTheLine:
    async def _github(self):
        from web.api.routes import settings_integrations as si

        return await si.connect_github(current_user=_claims(), request=None)

    async def _calendar_settings(self):
        from web.api.routes import settings_integrations as si

        return await si.connect_calendar(current_user=_claims(), request=None)

    async def _calendar_setup(self):
        from web.api.routes import setup as setup_mod

        return await setup_mod.start_calendar_oauth(current_user=_claims())

    def test_github_start_with_redis_down(self, redis_down):
        from web.api.routes.setup import GITHUB_CONNECT_COULD_NOT_START_MESSAGE as line

        reply = _through_the_real_handler(self._github)
        assert reply.status_code == 503
        assert reply.json() == {"message": line, "detail": line}

    def test_both_calendar_starts_with_redis_down(self, redis_down):
        from web.api.routes.setup import CALENDAR_CONNECT_COULD_NOT_START_MESSAGE as line

        for start in (self._calendar_settings, self._calendar_setup):
            reply = _through_the_real_handler(start)
            assert reply.status_code == 503
            assert reply.json() == {"message": line, "detail": line}

    def test_setup_calendar_start_with_no_google_client_says_cxos_line(self, monkeypatch):
        """CXO 2026-11-24: never the variable names on a setup page."""
        monkeypatch.delenv("GOOGLE_CLIENT_ID", raising=False)
        monkeypatch.delenv("GOOGLE_CLIENT_SECRET", raising=False)
        reply = _through_the_real_handler(self._calendar_setup)
        assert reply.status_code == 503
        assert reply.json()["detail"] == "Google Calendar sign-in isn't set up on this server."
        assert "GOOGLE_CLIENT" not in reply.text and "OAuth" not in reply.text


class TestThePagesWords:
    """CXO 2026-11-24 (mail 01M873MXMG): no protocol word and no status code on a card."""

    def test_the_github_dialog_title_and_fallback(self):
        from web.api.routes.setup import GITHUB_CONNECT_COULD_NOT_START_MESSAGE

        page = (ROOT / "templates/settings_github.html").read_text(encoding="utf-8")
        assert 'title: "GitHub connection couldn\'t start",' in page
        assert "Could not start GitHub OAuth" not in page
        assert "connect failed: HTTP" not in page
        assert f'"{GITHUB_CONNECT_COULD_NOT_START_MESSAGE}"' in page

    def test_the_wizards_two_fallbacks_are_the_connection_lines(self):
        from web.api.routes import setup as setup_mod

        script = (ROOT / "web/static/js/setup.js").read_text(encoding="utf-8")
        assert "Failed to start OAuth flow" not in script
        assert f'"{setup_mod.SLACK_CONNECT_COULD_NOT_START_MESSAGE}"' in script
        assert f'"{setup_mod.CALENDAR_CONNECT_COULD_NOT_START_MESSAGE}"' in script

    def test_the_slack_step_says_cxos_line_when_slack_is_not_set_up(self):
        """CXO 2026-11-24: Calendar's twin. The raise is marked, the names are logged, and
        the wizard's Slack step shows the route's line when there is one."""
        from web.api.routes import setup as setup_mod

        assert setup_mod.SLACK_SIGN_IN_NOT_SET_UP_MESSAGE == (
            "Slack sign-in isn't set up on this server."
        )
        src = (ROOT / "web/api/routes/setup.py").read_text(encoding="utf-8")
        assert "detail=SLACK_SIGN_IN_NOT_SET_UP_MESSAGE" in src
        assert 'detail="Slack OAuth not configured' not in src
        script = (ROOT / "web/static/js/setup.js").read_text(encoding="utf-8")
        slack = script[script.index("/api/v1/setup/slack/oauth/start") :][:1200]
        assert (
            "showSlackError(typeof data.detail === 'string' && data.detail ? data.detail :" in slack
        )

    def test_the_wording_pending_mark_is_gone(self):
        src = (ROOT / "web/api/routes/setup.py").read_text(encoding="utf-8")
        assert "CXO wording pending" not in src
