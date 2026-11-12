"""#2342 (ADR-081 D3): GitHub connect through one published GitHub App.

The unit layer of the build, which needs no registered App: the grant record and how a
stored value is classified, the switch keyed on configuration, the handler's authorize
URL and refresh, and the one resolver's behaviour in App mode. Each class names the
ruling it pins (Arch on issue 2342, 2026-11-11 19:09, 19:11, 19:23 and 2026-11-12 06:51;
CXO's final cutover lines, 2026-11-11 19:38).

Layer: unit. The binding table is real (in-memory SQLite behind a committing
``session_scope``); the grant store and GitHub's token endpoint are fakes. Nothing here
calls GitHub, and no value in this file is shaped like a real token.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import time
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors.binding_repository import ConnectorBindingRepository  # noqa: E402
from services.database.models import ConnectorBinding  # noqa: E402
from services.mcp.consumer import github_adapter as gh_mod  # noqa: E402
from services.mcp.consumer import github_app_grant as grant_mod  # noqa: E402
from services.mcp.consumer import github_app_refresh as refresh_mod  # noqa: E402
from services.mcp.consumer import github_oauth_handler as handler_mod  # noqa: E402
from services.mcp.consumer.connector import (  # noqa: E402
    ConnectorStatusState,
    DegradationReason,
    DegradationResponse,
)
from services.mcp.consumer.github_adapter import (  # noqa: E402
    CREDENTIAL_STORE_FAILED_MESSAGE,
    GITHUB_CUTOVER_STALE_REPLY,
    GITHUB_STALE_TOKEN_REPLY,
    GitHubCredential,
    GitHubMCPSpatialAdapter,
    github_degrade_reply,
)
from services.mcp.consumer.github_app_grant import (  # noqa: E402
    MINTED_BY_APP,
    REASON_CUTOVER,
    REASON_REFRESH_REJECTED,
    GitHubAppGrant,
    GrantRecordDamaged,
    app_mode,
    app_mode_config_warning,
    classify,
)
from services.mcp.consumer.github_oauth_handler import (  # noqa: E402
    GitHubOAuthHandler,
    GitHubOAuthTokens,
    RefreshOutcome,
    persist_github_connection,
)

_OWNER = "11111111-1111-1111-1111-111111111111"
_CLASSIC = "classic-bearer-value"
_APP_ENV = (grant_mod.ENV_APP_CLIENT_ID, grant_mod.ENV_APP_CLIENT_SECRET)


def _grant(tag: str = "one", *, access_in: int = 8 * 3600, refresh_in: int = 180 * 86400):
    now = int(time.time())
    return GitHubAppGrant(
        access_token=f"access-{tag}",
        access_expires_at=now + access_in,
        refresh_token=f"refresh-{tag}",
        refresh_expires_at=now + refresh_in,
    )


@pytest.fixture
def app_on(monkeypatch):
    monkeypatch.setenv(grant_mod.ENV_APP_CLIENT_ID, "app-client-id")
    monkeypatch.setenv(grant_mod.ENV_APP_CLIENT_SECRET, "app-client-secret")
    monkeypatch.delenv("ENCRYPTION_SCOPED_SUBKEYS", raising=False)


@pytest.fixture
def app_off(monkeypatch):
    for name in _APP_ENV:
        monkeypatch.delenv(name, raising=False)


# ── the grant record ────────────────────────────────────────────────────────────────


class TestGrantRecord:
    """Requirement 3 and Arch's parse condition (2026-11-12 06:51)."""

    def test_round_trip_keeps_the_four_fields_and_the_marker(self):
        grant = _grant()
        raw = grant.encode()
        assert json.loads(raw)["minted_by"] == MINTED_BY_APP
        assert classify(raw) == grant

    @pytest.mark.parametrize(
        "raw",
        [_CLASSIC, "", '["a","b"]', "  a-token-with-spaces-around  "],
    )
    def test_a_bare_string_is_a_classic_grant(self, raw):
        assert classify(raw) is None

    @pytest.mark.parametrize(
        "raw",
        [
            '{"access_token":"x"}',  # a parsed object with no marker
            '{"minted_by":"someone_else","access_token":"x"}',  # a wrong marker value
            "{}",
        ],
    )
    def test_a_json_object_without_the_right_marker_is_damage_not_classic(self, raw):
        # Arch 2026-11-12 07:24: no writer has ever stored a classic grant as JSON.
        with pytest.raises(GrantRecordDamaged):
            classify(raw)

    def test_no_value_is_not_a_grant(self):
        assert classify(None) is None

    @pytest.mark.parametrize(
        "raw",
        [
            '{"minted_by":"github_app"',  # starts with { and does not parse
            "{not json at all",
            json.dumps({"minted_by": MINTED_BY_APP, "access_token": "a"}),
            json.dumps(
                {
                    "minted_by": MINTED_BY_APP,
                    "access_token": "a",
                    "refresh_token": "r",
                    "access_expires_at": 1,
                }
            ),
            json.dumps(
                {
                    "minted_by": MINTED_BY_APP,
                    "access_token": "",
                    "refresh_token": "r",
                    "access_expires_at": 1,
                    "refresh_expires_at": 2,
                }
            ),
            json.dumps(
                {
                    "minted_by": MINTED_BY_APP,
                    "access_token": "a",
                    "refresh_token": "r",
                    "access_expires_at": "soon",
                    "refresh_expires_at": 2,
                }
            ),
        ],
    )
    def test_a_damaged_record_is_a_read_failure_never_classic(self, raw):
        with pytest.raises(GrantRecordDamaged):
            classify(raw)

    def test_no_repr_carries_a_token(self):
        grant = _grant("secretpart")
        tokens = GitHubOAuthTokens(access_token="access-secretpart", refresh_token="refresh-x")
        verdict = refresh_mod.AppGrantVerdict(token="access-secretpart")
        for shown in (repr(grant), repr(tokens), repr(verdict), str(grant)):
            assert "secretpart" not in shown and "refresh-x" not in shown

    def test_refresh_is_due_inside_five_minutes_and_expiry_is_separate(self):
        nearly = _grant(access_in=120)
        assert nearly.refresh_due() and not nearly.access_expired()
        gone = _grant(access_in=-5)
        assert gone.refresh_due() and gone.access_expired()
        assert not _grant().refresh_due()


# ── the switch ──────────────────────────────────────────────────────────────────────


class TestAppModeSwitch:
    """Arch's ruling 1 (2026-11-12 06:51): keyed on configuration; one alone is off."""

    def test_both_present_turns_app_mode_on(self, app_on):
        assert app_mode() is True
        assert app_mode_config_warning() is None

    def test_neither_present_is_off_without_a_warning(self, app_off):
        assert app_mode() is False
        assert app_mode_config_warning() is None

    @pytest.mark.parametrize("present,missing", [_APP_ENV, tuple(reversed(_APP_ENV))])
    def test_one_alone_is_off_and_the_warning_names_the_missing_one(
        self, app_off, monkeypatch, present, missing
    ):
        monkeypatch.setenv(present, "set-value")
        assert app_mode() is False
        warning = app_mode_config_warning()
        assert warning and missing in warning and "OFF" in warning
        assert "set-value" not in warning

    def test_install_link_needs_a_slug(self, monkeypatch):
        monkeypatch.delenv(grant_mod.ENV_APP_SLUG, raising=False)
        assert grant_mod.app_install_url() is None
        monkeypatch.setenv(grant_mod.ENV_APP_SLUG, "piper-example")
        assert (
            grant_mod.app_install_url() == "https://github.com/apps/piper-example/installations/new"
        )


# ── the handler ─────────────────────────────────────────────────────────────────────


class _FakeResponse:
    def __init__(self, status, body):
        self.status = status
        self._body = body

    async def json(self, content_type=None):
        if isinstance(self._body, Exception):
            raise self._body
        return self._body

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False


class _FakeHTTP:
    """Stands in for ``aiohttp.ClientSession``: records the POST and answers as scripted."""

    def __init__(self, reply):
        self.reply = reply
        self.posts = []

    def __call__(self, *args, **kwargs):
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    def post(self, url, **kwargs):
        self.posts.append((url, kwargs))
        if isinstance(self.reply, Exception):
            raise self.reply
        return self.reply


def _token_reply(tag="new"):
    return {
        "access_token": f"access-{tag}",
        "expires_in": 28800,
        "refresh_token": f"refresh-{tag}",
        "refresh_token_expires_in": 15897600,
        "token_type": "bearer",
        "scope": "",
    }


class TestHandlerInAppMode:
    """Requirements 1 and 3: no ``scope`` on the authorize URL; four fields stored."""

    def test_authorize_url_sends_no_scope_and_uses_the_app_client(self, app_on):
        url, _ = GitHubOAuthHandler().generate_authorization_url(_OWNER)
        assert "scope=" not in url
        assert "client_id=app-client-id" in url

    def test_classic_mode_still_asks_for_repo(self, app_off, monkeypatch):
        monkeypatch.setenv("GITHUB_OAUTH_CLIENT_ID", "classic-id")
        monkeypatch.setenv("GITHUB_OAUTH_CLIENT_SECRET", "classic-secret")
        handler = GitHubOAuthHandler()
        url, _ = handler.generate_authorization_url(_OWNER)
        assert handler.app_mode is False
        assert "scope=repo" in url and "client_id=classic-id" in url

    def test_classic_flag_forces_the_classic_client_in_app_mode(self, app_on, monkeypatch):
        monkeypatch.setenv("GITHUB_OAUTH_CLIENT_ID", "classic-id")
        monkeypatch.setenv("GITHUB_OAUTH_CLIENT_SECRET", "classic-secret")
        handler = GitHubOAuthHandler(classic=True)
        assert handler.app_mode is False and handler.client_id == "classic-id"

    def test_the_token_reply_becomes_the_four_stored_fields(self):
        before = int(time.time())
        grant = GitHubOAuthHandler._tokens_from_reply(_token_reply()).as_app_grant()
        assert grant.access_token == "access-new" and grant.refresh_token == "refresh-new"
        assert before + 28800 <= grant.access_expires_at <= before + 28805
        assert before + 15897600 <= grant.refresh_expires_at <= before + 15897605

    @pytest.mark.parametrize("drop", ["refresh_token", "expires_in", "refresh_token_expires_in"])
    def test_a_reply_without_the_expiring_pair_is_refused(self, drop):
        reply = _token_reply()
        del reply[drop]
        with pytest.raises(ValueError):
            GitHubOAuthHandler._tokens_from_reply(reply).as_app_grant()


@pytest.mark.asyncio
class TestRefreshOutcomes:
    """Requirement 5 as narrowed (Arch 2026-11-11 19:11): classify on the reply body's
    ``error`` field, never on the status alone."""

    async def _refresh(self, monkeypatch, reply):
        http = _FakeHTTP(reply)
        monkeypatch.setattr(handler_mod.aiohttp, "ClientSession", http)
        outcome = await GitHubOAuthHandler().refresh_grant("refresh-old")
        return outcome, http

    async def test_a_new_pair_comes_back_as_a_grant(self, app_on, monkeypatch):
        outcome, http = await self._refresh(monkeypatch, _FakeResponse(200, _token_reply()))
        assert outcome.refreshed and outcome.grant.refresh_token == "refresh-new"
        sent = http.posts[0][1]["data"]
        assert sent["grant_type"] == "refresh_token" and sent["refresh_token"] == "refresh-old"
        assert sent["client_id"] == "app-client-id" and "scope" not in sent

    async def test_bad_refresh_token_in_a_200_body_is_rejected(self, app_on, monkeypatch):
        body = {"error": "bad_refresh_token", "error_description": "expired or revoked"}
        outcome, _ = await self._refresh(monkeypatch, _FakeResponse(200, body))
        assert outcome.rejected and not outcome.refreshed and not outcome.could_not_complete

    @pytest.mark.parametrize(
        "reply",
        [
            _FakeResponse(502, {"message": "bad gateway"}),
            _FakeResponse(503, ValueError("not json")),
            _FakeResponse(500, {"error": "bad_refresh_token"}),  # a 5xx is never a verdict
            asyncio.TimeoutError(),
            ConnectionResetError(),
            _FakeResponse(200, {}),  # no error field and no token: unclassifiable
            _FakeResponse(200, {"error": "incorrect_client_credentials"}),  # our fault
            _FakeResponse(200, {"access_token": "access-only"}),  # no expiring pair
        ],
    )
    async def test_anything_else_could_not_complete(self, app_on, monkeypatch, reply):
        outcome, _ = await self._refresh(monkeypatch, reply)
        assert outcome.could_not_complete and not outcome.rejected and outcome.grant is None

    async def test_outside_app_mode_no_call_is_made(self, app_off, monkeypatch):
        outcome, http = await self._refresh(monkeypatch, _FakeResponse(200, _token_reply()))
        assert outcome.could_not_complete and http.posts == []


# ── the resolver ────────────────────────────────────────────────────────────────────


class _FakeStore:
    """An in-memory stand-in for ``ConnectorGrantStore`` (one value per owner)."""

    values: dict = {}
    writes: list = []
    read_error: Exception | None = None

    async def get_encrypted_strict(self, session, user_id, connector):
        if _FakeStore.read_error is not None:
            raise _FakeStore.read_error
        return _FakeStore.values.get(str(user_id))

    async def store_app_grant(self, session, user_id, connector, grant):
        _FakeStore.writes.append(grant)
        _FakeStore.values[str(user_id)] = grant.encode()


class _FakeRefresher:
    """Stands in for the handler's ``refresh_grant``: scripted outcomes, call count."""

    def __init__(self, *outcomes, delay: float = 0.0, on_call=None):
        self.outcomes = list(outcomes)
        self.calls = []
        self.delay = delay
        self.on_call = on_call

    async def refresh_grant(self, refresh_token):
        self.calls.append(refresh_token)
        if self.delay:
            await asyncio.sleep(self.delay)
        if self.on_call:
            self.on_call()
        return self.outcomes.pop(0) if len(self.outcomes) > 1 else self.outcomes[0]


@pytest_asyncio.fixture
async def world(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    sm = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with sm() as s:
            yield s
            await s.commit()

    monkeypatch.setattr(gh_mod.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    _FakeStore.values, _FakeStore.writes, _FakeStore.read_error = {}, [], None
    refresh_mod._OWNER_LOCKS.clear()
    monkeypatch.setattr(refresh_mod, "ConnectorGrantStore", _FakeStore)

    async def _oauth_grant(owner_id):
        return await _FakeStore().get_encrypted_strict(None, owner_id, "github")

    monkeypatch.setattr(GitHubMCPSpatialAdapter, "_oauth_grant", staticmethod(_oauth_grant))
    monkeypatch.setattr(
        GitHubMCPSpatialAdapter, "account_pat", staticmethod(AsyncMock(return_value=None))
    )
    yield sm
    await engine.dispose()


async def _seed(sm, status=ConnectorStatusState.BOUND.value, *, reason=None, stored=None):
    async with sm() as s:
        repo = ConnectorBindingRepository(s)
        await repo.upsert(_OWNER, "github", status=status, mcp_server_ref="github")
        if reason is not None:
            await repo.set_status(_OWNER, "github", status, reason=reason)
        await s.commit()
    if stored is not None:
        _FakeStore.values[_OWNER] = stored


async def _row(sm):
    async with sm() as s:
        return await ConnectorBindingRepository(s).get(_OWNER, "github")


def _use(monkeypatch, refresher):
    monkeypatch.setattr(refresh_mod, "_new_handler", lambda: refresher)
    return refresher


@pytest.mark.asyncio
class TestLandingChangesNothingForAClassicGrant:
    """Arch's ruling 1: with App mode off, a classic grant serves exactly as before."""

    async def test_classic_grant_serves_with_app_mode_off(self, world, app_off, monkeypatch):
        await _seed(world, stored=_CLASSIC)
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(rejected=True)))
        credential = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert isinstance(credential, GitHubCredential)
        assert credential.leg == "oauth" and credential.token == _CLASSIC
        assert credential.app_grant is False
        row = await _row(world)
        assert row.status == ConnectorStatusState.BOUND.value and row.status_reason is None
        assert refresher.calls == []

    async def test_a_record_is_never_forwarded_as_a_bearer_even_with_app_mode_off(
        self, world, app_off, monkeypatch
    ):
        # The MCP app holds no client secret, so App mode is off there. A stored record
        # holds the refresh token: its access token serves, the record never does.
        record = _grant("live").encode()
        await _seed(world, stored=record)
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(rejected=True)))
        credential = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert isinstance(credential, GitHubCredential)
        assert credential.token == "access-live" and credential.token != record
        assert credential.app_grant is True  # a fact about the grant, not the config
        assert "refresh-live" not in credential.token
        headers = await GitHubMCPSpatialAdapter()._grant_headers_or_raise(_OWNER)
        assert headers == {"Authorization": "Bearer access-live"}
        assert refresher.calls == [] and _FakeStore.writes == []

    async def test_the_older_store_re_read_never_turns_a_record_into_a_bearer(
        self, world, app_off, monkeypatch
    ):
        # A credential built without a token falls back to a store read (the pre-#2266
        # path, still used by callers that mock the resolver).
        import contextlib

        from services.integrations.github.read_failed import GitHubReadFailed

        record = _grant("live").encode()
        adapter = GitHubMCPSpatialAdapter()
        adapter.resolve_credential = AsyncMock(
            return_value=GitHubCredential(
                owner_id=_OWNER, mcp_server_ref="github", token=None, leg="oauth"
            )
        )

        class _Store:
            value = record

            async def get(self, session, user_id, connector):
                return _Store.value

        monkeypatch.setattr(gh_mod, "ConnectorGrantStore", _Store)
        headers = await adapter._grant_headers_or_raise(_OWNER)
        assert headers == {"Authorization": "Bearer access-live"}
        for bad in (_grant("gone", access_in=-5).encode(), '{"minted_by":"github_app"'):
            _Store.value = bad
            with pytest.raises(GitHubReadFailed) as exc:
                await adapter._grant_headers_or_raise(_OWNER)
            assert exc.value.detail == "grant_missing"
        _Store.value = _CLASSIC  # a classic grant is still read as before
        assert await adapter._grant_headers_or_raise(_OWNER) == {
            "Authorization": f"Bearer {_CLASSIC}"
        }

    async def test_an_expired_record_with_app_mode_off_is_unreachable_never_refreshed(
        self, world, app_off, monkeypatch
    ):
        old = _grant("old", access_in=-10).encode()
        await _seed(world, stored=old)
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(grant=_grant("new"))))
        result = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert result.reason is DegradationReason.UNREACHABLE
        assert refresher.calls == [] and _FakeStore.values[_OWNER] == old
        row = await _row(world)
        assert row.status == ConnectorStatusState.BOUND.value and row.status_reason is None

    async def test_a_damaged_record_with_app_mode_off_is_a_failed_read_not_a_bearer(
        self, world, app_off, monkeypatch
    ):
        await _seed(world, stored='{"minted_by":"github_app","access_token":"a"')
        result = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert result.reason is DegradationReason.UNREACHABLE
        assert (await _row(world)).status == ConnectorStatusState.BOUND.value

    async def test_a_401_on_a_replaced_token_is_not_stale_with_app_mode_off(self, world, app_off):
        await _seed(world, stored=_grant("new").encode())
        held = GitHubCredential(
            owner_id=_OWNER, mcp_server_ref="github", token="access-old", leg="oauth"
        )
        rejection = gh_mod.GitHubToolError(
            "failed to search issues: GET https://api.github.com/search/issues: 401 Bad credentials []"
        )
        result = await GitHubMCPSpatialAdapter()._degrade_for_exc(held, rejection)
        assert result.reason is DegradationReason.UNREACHABLE
        assert (await _row(world)).status == ConnectorStatusState.BOUND.value


@pytest.mark.asyncio
class TestMarkerlessGrantNeverServes:
    """Arch 2026-11-11 19:09 and 2026-11-12 06:51: in App mode a grant without the App
    marker never serves, and the resolver records ``cutover`` when it meets one."""

    async def test_classic_grant_in_app_mode_goes_stale_with_cutover(
        self, world, app_on, monkeypatch
    ):
        await _seed(world, stored=_CLASSIC)
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(grant=_grant("x"))))
        result = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert isinstance(result, DegradationResponse)
        assert result.reason is DegradationReason.STALE_TOKEN
        assert result.detail == REASON_CUTOVER
        assert github_degrade_reply(result) == GITHUB_CUTOVER_STALE_REPLY
        row = await _row(world)
        assert row.status == ConnectorStatusState.STALE.value
        assert row.status_reason == REASON_CUTOVER
        assert refresher.calls == []  # a classic token is never sent anywhere
        assert _FakeStore.values[_OWNER] == _CLASSIC  # the script deletes it, not the resolver

    async def test_the_next_read_keeps_the_cutover_words(self, world, app_on, monkeypatch):
        await _seed(world, stored=_CLASSIC)
        adapter = GitHubMCPSpatialAdapter()
        await adapter.resolve_credential(_OWNER)
        again = await adapter.resolve_credential(_OWNER)  # binding is STALE now
        assert github_degrade_reply(again) == GITHUB_CUTOVER_STALE_REPLY

    async def test_d4_a_personal_token_still_serves_beside_a_cutover_binding(
        self, world, app_on, monkeypatch
    ):
        await _seed(world, stored=_CLASSIC)
        monkeypatch.setattr(
            GitHubMCPSpatialAdapter,
            "account_pat",
            staticmethod(AsyncMock(return_value="personal-token-value")),
        )
        credential = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert isinstance(credential, GitHubCredential) and credential.leg == "pat"
        assert credential.token == "personal-token-value"
        assert credential.stale_oauth_reason is DegradationReason.STALE_TOKEN


@pytest.mark.asyncio
class TestResolverRefresh:
    """Requirement 4 and requirement 5 as narrowed."""

    async def test_a_live_token_serves_without_a_refresh(self, world, app_on, monkeypatch):
        await _seed(world, stored=_grant("live").encode())
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(rejected=True)))
        credential = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert credential.token == "access-live" and refresher.calls == []

    async def test_a_due_token_is_refreshed_and_the_pair_rewritten_in_one_write(
        self, world, app_on, monkeypatch
    ):
        await _seed(world, stored=_grant("old", access_in=60).encode())
        new = _grant("new")
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(grant=new)))
        credential = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert credential.token == "access-new"
        assert refresher.calls == ["refresh-old"]
        assert _FakeStore.writes == [new]  # one write holds both tokens
        assert classify(_FakeStore.values[_OWNER]) == new
        assert (await _row(world)).status == ConnectorStatusState.BOUND.value

    async def test_a_rejected_refresh_is_stale_with_its_reason(self, world, app_on, monkeypatch):
        old = _grant("old", access_in=-10).encode()
        await _seed(world, stored=old)
        _use(monkeypatch, _FakeRefresher(RefreshOutcome(rejected=True, error="bad_refresh_token")))
        result = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert result.reason is DegradationReason.STALE_TOKEN
        assert result.detail is None
        assert github_degrade_reply(result) == GITHUB_STALE_TOKEN_REPLY  # CXO: no new words
        row = await _row(world)
        assert row.status == ConnectorStatusState.STALE.value
        assert row.status_reason == REASON_REFRESH_REJECTED
        assert _FakeStore.values[_OWNER] == old and _FakeStore.writes == []  # dead pair left

    @pytest.mark.parametrize(
        "outcome",
        [RefreshOutcome(error="server_error", status=502), RefreshOutcome(error="TimeoutError")],
    )
    async def test_could_not_complete_with_an_expired_token_is_unreachable_store_unchanged(
        self, world, app_on, monkeypatch, outcome
    ):
        old = _grant("old", access_in=-10).encode()
        await _seed(world, stored=old)
        _use(monkeypatch, _FakeRefresher(outcome))
        result = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert isinstance(result, DegradationResponse)
        assert result.reason is DegradationReason.UNREACHABLE
        assert result.reason is not DegradationReason.CONNECT_REQUIRED
        row = await _row(world)
        assert row.status == ConnectorStatusState.BOUND.value and row.status_reason is None
        assert _FakeStore.values[_OWNER] == old and _FakeStore.writes == []

    async def test_could_not_complete_with_time_left_serves_the_current_token(
        self, world, app_on, monkeypatch
    ):
        await _seed(world, stored=_grant("old", access_in=120).encode())
        _use(monkeypatch, _FakeRefresher(RefreshOutcome(error="server_error", status=503)))
        credential = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert credential.token == "access-old" and _FakeStore.writes == []

    async def test_a_rejected_refresh_after_a_concurrent_rewrite_serves_the_new_pair(
        self, world, app_on, monkeypatch
    ):
        await _seed(world, stored=_grant("old", access_in=-10).encode())
        newer = _grant("newer")

        def _someone_else_wrote():
            _FakeStore.values[_OWNER] = newer.encode()

        _use(
            monkeypatch,
            _FakeRefresher(
                RefreshOutcome(rejected=True, error="bad_refresh_token"),
                on_call=_someone_else_wrote,
            ),
        )
        credential = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert isinstance(credential, GitHubCredential) and credential.token == "access-newer"
        row = await _row(world)
        assert row.status == ConnectorStatusState.BOUND.value and row.status_reason is None

    async def test_two_concurrent_requests_spend_the_refresh_token_once(
        self, world, app_on, monkeypatch
    ):
        await _seed(world, stored=_grant("old", access_in=30).encode())
        refresher = _use(
            monkeypatch, _FakeRefresher(RefreshOutcome(grant=_grant("new")), delay=0.05)
        )
        adapter = GitHubMCPSpatialAdapter()
        first, second = await asyncio.gather(
            adapter.resolve_credential(_OWNER), adapter.resolve_credential(_OWNER)
        )
        assert refresher.calls == ["refresh-old"]  # spent once
        assert first.token == second.token == "access-new"  # the other read the new pair
        assert len(_FakeStore.writes) == 1

    async def test_a_damaged_record_is_a_failed_read_never_cutover(
        self, world, app_on, monkeypatch
    ):
        await _seed(world, stored='{"minted_by":"github_app","access_token":"a"}')
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(rejected=True)))
        result = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert result.reason is DegradationReason.UNREACHABLE
        assert result.user_message == CREDENTIAL_STORE_FAILED_MESSAGE
        row = await _row(world)
        assert row.status == ConnectorStatusState.BOUND.value and row.status_reason is None
        assert refresher.calls == []

    async def test_an_object_that_lost_its_marker_is_a_failed_read_never_cutover(
        self, world, app_on, monkeypatch
    ):
        record = json.loads(_grant("x").encode())
        del record["minted_by"]
        await _seed(world, stored=json.dumps(record))
        result = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert result.reason is DegradationReason.UNREACHABLE
        row = await _row(world)
        assert row.status == ConnectorStatusState.BOUND.value and row.status_reason is None

    async def test_a_failed_write_after_a_refresh_has_its_own_log_event(
        self, world, app_on, monkeypatch
    ):
        await _seed(world, stored=_grant("old", access_in=60).encode())
        _use(monkeypatch, _FakeRefresher(RefreshOutcome(grant=_grant("new"))))

        async def _boom(self, session, user_id, connector, grant):
            raise RuntimeError("disk full")

        monkeypatch.setattr(_FakeStore, "store_app_grant", _boom)
        events = []
        monkeypatch.setattr(
            refresh_mod.logger, "error", lambda event, **kw: events.append((event, kw))
        )
        result = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert result.reason is DegradationReason.UNREACHABLE  # never "reconnect"
        assert [e for e, _ in events] == ["github_app_grant_refreshed_write_failed"]
        assert "new" not in repr(events) and "disk full" not in repr(events)
        assert (await _row(world)).status == ConnectorStatusState.BOUND.value

    async def test_the_bearer_is_the_access_token_never_the_record(
        self, world, app_on, monkeypatch
    ):
        await _seed(world, stored=_grant("live").encode())
        headers = await GitHubMCPSpatialAdapter()._grant_headers_or_raise(_OWNER)
        assert headers == {"Authorization": "Bearer access-live"}


@pytest.mark.asyncio
class TestScopedProcessNeverRefreshes:
    """The MCP app is decrypt-only (#1982): it can't write a new pair, so it never
    spends a refresh token. An expired token there is UNREACHABLE, never stale."""

    async def test_expired_in_a_scoped_process_is_unreachable(self, world, app_on, monkeypatch):
        monkeypatch.setenv("ENCRYPTION_SCOPED_SUBKEYS", "ctx=unused")
        old = _grant("old", access_in=-10).encode()
        await _seed(world, stored=old)
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(grant=_grant("new"))))
        result = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert result.reason is DegradationReason.UNREACHABLE
        assert refresher.calls == [] and _FakeStore.values[_OWNER] == old
        assert (await _row(world)).status == ConnectorStatusState.BOUND.value

    async def test_nearly_expired_in_a_scoped_process_still_serves(
        self, world, app_on, monkeypatch
    ):
        monkeypatch.setenv("ENCRYPTION_SCOPED_SUBKEYS", "ctx=unused")
        await _seed(world, stored=_grant("old", access_in=120).encode())
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(grant=_grant("new"))))
        credential = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert credential.token == "access-old" and refresher.calls == []


@pytest.mark.asyncio
class TestStatusReason:
    """Arch 2026-11-11 19:23: every stale-writing path sets the reason; rebinding clears
    it; the reply is chosen by the stored reason."""

    @pytest.mark.parametrize(
        "reason,reply",
        [
            (REASON_CUTOVER, GITHUB_CUTOVER_STALE_REPLY),
            (REASON_REFRESH_REJECTED, GITHUB_STALE_TOKEN_REPLY),
            (None, GITHUB_STALE_TOKEN_REPLY),  # stale before the column existed
        ],
    )
    async def test_the_reply_is_chosen_by_the_stored_reason(self, world, app_on, reason, reply):
        await _seed(world, ConnectorStatusState.STALE.value, reason=reason)
        result = await GitHubMCPSpatialAdapter().resolve_credential(_OWNER)
        assert result.reason is DegradationReason.STALE_TOKEN
        assert github_degrade_reply(result) == reply

    async def test_rebinding_clears_the_reason(self, world, app_on):
        await _seed(world, ConnectorStatusState.STALE.value, reason=REASON_CUTOVER)
        store = AsyncMock()
        grant = _grant("fresh")
        async with world() as s:
            await persist_github_connection(s, _OWNER, "", grant_store=store, app_grant=grant)
            await s.commit()
        store.store_app_grant.assert_awaited_once()
        assert store.store_app_grant.call_args.args[3] == grant
        store.store.assert_not_awaited()
        row = await _row(world)
        assert row.status == ConnectorStatusState.BOUND.value and row.status_reason is None

    async def test_a_status_change_without_a_reason_clears_the_old_one(self, world):
        await _seed(world, ConnectorStatusState.STALE.value, reason=REASON_REFRESH_REJECTED)
        async with world() as s:
            await ConnectorBindingRepository(s).set_status(
                _OWNER, "github", ConnectorStatusState.UNBOUND.value
            )
            await s.commit()
        assert (await _row(world)).status_reason is None

    async def test_a_401_on_the_grant_marks_stale_without_a_reason(self, world, app_on):
        await _seed(world)
        credential = GitHubCredential(
            owner_id=_OWNER, mcp_server_ref="github", token="access-live", leg="oauth"
        )
        assert await GitHubMCPSpatialAdapter._mark_oauth_binding_stale(credential) is True
        row = await _row(world)
        assert row.status == ConnectorStatusState.STALE.value and row.status_reason is None


class TestCutoverCopy:
    """CXO's FINAL lines (2026-11-11 19:38). "choose which repositories I can see" is the
    App's install choice; "saved settings" are the kept ``connector_configs``."""

    def test_the_chat_line_is_cxos_final_wording(self):
        assert GITHUB_CUTOVER_STALE_REPLY == (
            "GitHub now connects through the Piper GitHub app, so your connection needs to "
            "be set up again. Reconnect GitHub in Settings, under Integrations, and choose "
            "which repositories I can see. Your saved settings are unchanged."
        )


class TestAdvisoryLockKey:
    """Arch's ruling 4: a key namespaced to this use, one per owner."""

    def test_the_key_is_stable_per_owner_and_fits_a_signed_bigint(self):
        key = refresh_mod.advisory_lock_key(_OWNER)
        assert key == refresh_mod.advisory_lock_key(_OWNER)
        assert key != refresh_mod.advisory_lock_key("22222222-2222-2222-2222-222222222222")
        assert -(2**63) <= key < 2**63


# ── the validator bypass is one function wide ───────────────────────────────────────


class TestSecurityCheckBypassIsOneFunctionWide:
    """Arch 2026-11-12 06:53: ``connector_grant_store.py`` is on #1982's closed list for
    ``store_app_grant`` only. The bare-token ``store`` keeps the validator, and nothing
    but a complete ``GitHubAppGrant`` passes through the bypass."""

    @staticmethod
    def _functions():
        import ast
        from pathlib import Path

        import services.mcp.consumer.connector_grant_store as mod

        source = Path(mod.__file__).read_text(encoding="utf-8")
        tree = ast.parse(source)
        found = {}
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                found[node.name] = node
        return found

    @staticmethod
    def _passes_bypass(func) -> bool:
        import ast

        for node in ast.walk(func):
            if isinstance(node, ast.keyword) and node.arg == "security_check":
                if isinstance(node.value, ast.Constant) and node.value.value is False:
                    return True
        return False

    def test_only_store_app_grant_passes_security_check_false(self):
        functions = self._functions()
        passing = sorted(name for name, func in functions.items() if self._passes_bypass(func))
        assert passing == ["store_app_grant"]

    def test_the_bare_token_store_keeps_the_validator_on(self):
        import ast

        store = self._functions()["store"]
        keywords = [n.arg for n in ast.walk(store) if isinstance(n, ast.keyword)]
        assert "security_check" not in keywords  # the default (True) applies
        assert any(
            isinstance(n, ast.Attribute) and n.attr == "store_user_key" for n in ast.walk(store)
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "bad",
        [
            "a-raw-string",
            '{"minted_by":"github_app"}',
            GitHubAppGrant("", 10, "refresh-x", 20),
            GitHubAppGrant("access-x", 10, "  ", 20),
            GitHubAppGrant("access-x", 0, "refresh-x", 20),
            GitHubAppGrant("access-x", 10, "refresh-x", None),
        ],
    )
    async def test_an_incomplete_or_raw_value_is_refused_before_any_write(self, bad):
        from services.mcp.consumer.connector_grant_store import ConnectorGrantStore

        service = AsyncMock()
        with pytest.raises((TypeError, ValueError)):
            await ConnectorGrantStore(service).store_app_grant(None, _OWNER, "github", bad)
        service.store_user_key.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_a_complete_grant_is_written_once_as_one_record(self):
        from services.mcp.consumer.connector_grant_store import ConnectorGrantStore

        service = AsyncMock()
        grant = _grant("whole")
        await ConnectorGrantStore(service).store_app_grant("sess", _OWNER, "github", grant)
        service.store_user_key.assert_awaited_once()
        args, kwargs = service.store_user_key.call_args
        assert args[2] == "github_mcp_oauth" and classify(args[3]) == grant
        assert kwargs == {"validate": False, "security_check": False}


# ── the background pass ─────────────────────────────────────────────────────────────


@pytest.mark.asyncio
class TestBackgroundRefreshPass:
    """Arch 2026-11-12 06:52: only App mode, only App-marked grants on a BOUND binding
    with under two hours left; one log line of counts."""

    async def test_outside_app_mode_the_pass_does_nothing(self, world, app_off, monkeypatch):
        await _seed(world, stored=_grant("old", access_in=60).encode())
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(grant=_grant("new"))))
        counts = await refresh_mod.background_refresh_pass()
        assert set(counts.values()) == {0} and refresher.calls == []

    async def test_a_scoped_process_never_runs_the_pass(self, world, app_on, monkeypatch):
        monkeypatch.setenv("ENCRYPTION_SCOPED_SUBKEYS", "ctx=unused")
        await _seed(world, stored=_grant("old", access_in=60).encode())
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(grant=_grant("new"))))
        counts = await refresh_mod.background_refresh_pass()
        assert set(counts.values()) == {0} and refresher.calls == []

    async def test_a_grant_with_under_two_hours_left_is_refreshed(self, world, app_on, monkeypatch):
        await _seed(world, stored=_grant("old", access_in=3600).encode())  # 1 h left
        new = _grant("new")
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(grant=new)))
        counts = await refresh_mod.background_refresh_pass()
        assert counts == {
            "seen": 1,
            "refreshed": 1,
            "already_fresh": 0,
            "rejected": 0,
            "could_not_complete": 0,
        }
        assert refresher.calls == ["refresh-old"] and classify(_FakeStore.values[_OWNER]) == new

    async def test_a_grant_with_more_than_two_hours_left_is_left_alone(
        self, world, app_on, monkeypatch
    ):
        await _seed(world, stored=_grant("live", access_in=3 * 3600).encode())
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(grant=_grant("new"))))
        counts = await refresh_mod.background_refresh_pass()
        assert counts["seen"] == 1 and counts["already_fresh"] == 1 and refresher.calls == []

    @pytest.mark.parametrize(
        "status", [ConnectorStatusState.STALE.value, ConnectorStatusState.UNBOUND.value]
    )
    async def test_a_binding_that_is_not_bound_is_never_refreshed(
        self, world, app_on, monkeypatch, status
    ):
        await _seed(world, status, stored=_grant("old", access_in=60).encode())
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(grant=_grant("new"))))
        counts = await refresh_mod.background_refresh_pass()
        assert counts["seen"] == 0 and refresher.calls == [] and _FakeStore.writes == []

    async def test_a_classic_grant_is_not_this_passes_business(self, world, app_on, monkeypatch):
        await _seed(world, stored=_CLASSIC)
        refresher = _use(monkeypatch, _FakeRefresher(RefreshOutcome(grant=_grant("new"))))
        counts = await refresh_mod.background_refresh_pass()
        assert counts["seen"] == 0 and refresher.calls == []
        row = await _row(world)  # the pass marks nothing; the resolver and script do
        assert row.status == ConnectorStatusState.BOUND.value and row.status_reason is None

    async def test_a_rejected_refresh_marks_the_binding_stale_with_its_reason(
        self, world, app_on, monkeypatch
    ):
        await _seed(world, stored=_grant("old", access_in=60).encode())
        _use(monkeypatch, _FakeRefresher(RefreshOutcome(rejected=True, error="bad_refresh_token")))
        counts = await refresh_mod.background_refresh_pass()
        assert counts["rejected"] == 1 and counts["refreshed"] == 0
        row = await _row(world)
        assert row.status == ConnectorStatusState.STALE.value
        assert row.status_reason == REASON_REFRESH_REJECTED

    async def test_a_refresh_that_cannot_complete_writes_nothing(self, world, app_on, monkeypatch):
        old = _grant("old", access_in=60).encode()
        await _seed(world, stored=old)
        _use(monkeypatch, _FakeRefresher(RefreshOutcome(error="server_error", status=502)))
        counts = await refresh_mod.background_refresh_pass()
        assert counts["could_not_complete"] == 1
        assert _FakeStore.values[_OWNER] == old and _FakeStore.writes == []
        row = await _row(world)
        assert row.status == ConnectorStatusState.BOUND.value and row.status_reason is None


# ── a 401 on a token a refresh has already replaced ─────────────────────────────────


@pytest.mark.asyncio
class TestRejectedTokenAlreadyReplaced:
    """Arch 2026-11-12 06:52 (#2288's rule): the binding goes stale only if the token
    GitHub rejected is still the stored one."""

    @staticmethod
    def _rejection():
        return gh_mod.GitHubToolError(
            "failed to search repositories: GET https://api.github.com/search/repositories: "
            "401 Bad credentials []"
        )

    async def test_a_replaced_token_is_not_marked_stale(self, world, app_on):
        await _seed(world, stored=_grant("new").encode())
        held = GitHubCredential(
            owner_id=_OWNER, mcp_server_ref="github", token="access-old", leg="oauth"
        )
        result = await GitHubMCPSpatialAdapter()._degrade_for_exc(held, self._rejection())
        assert result.reason is DegradationReason.UNREACHABLE
        row = await _row(world)
        assert row.status == ConnectorStatusState.BOUND.value

    async def test_the_stored_token_rejected_is_stale(self, world, app_on):
        await _seed(world, stored=_grant("same").encode())
        held = GitHubCredential(
            owner_id=_OWNER, mcp_server_ref="github", token="access-same", leg="oauth"
        )
        result = await GitHubMCPSpatialAdapter()._degrade_for_exc(held, self._rejection())
        assert result.reason is DegradationReason.STALE_TOKEN
        assert (await _row(world)).status == ConnectorStatusState.STALE.value

    async def test_classic_mode_keeps_the_existing_rule(self, world, app_off):
        await _seed(world, stored=_CLASSIC)
        held = GitHubCredential(
            owner_id=_OWNER, mcp_server_ref="github", token="some-other-value", leg="oauth"
        )
        result = await GitHubMCPSpatialAdapter()._degrade_for_exc(held, self._rejection())
        assert result.reason is DegradationReason.STALE_TOKEN
        assert (await _row(world)).status == ConnectorStatusState.STALE.value


# ── the connector's own lines ───────────────────────────────────────────────────────


class TestConnectorLines:
    """CXO 2026-11-12 07:19 (Arch 07:08): a person in the Claude connector may never have
    opened the web app. UNREACHABLE reads as a wait and never names Settings; STALE is
    the only state that asks for a reconnect, and says where Settings is."""

    def test_unreachable_is_temporary_and_sends_nobody_to_settings(self):
        line = gh_mod.github_connector_reply(
            DegradationResponse(reason=DegradationReason.UNREACHABLE, user_message="internal")
        )
        assert line == (
            "I couldn't reach GitHub just now. This is temporary, so please try again in a "
            "moment."
        )
        assert "Settings" not in line and "MCP" not in line

    def test_stale_asks_for_a_reconnect_in_the_piper_morgan_app(self):
        line = gh_mod.github_connector_reply(
            DegradationResponse(reason=DegradationReason.STALE_TOKEN, user_message="short")
        )
        assert line == (
            "Your GitHub connection needs re-authorizing. Reconnect GitHub in the Piper "
            "Morgan app, in Settings under Integrations."
        )

    def test_cutover_differs_from_the_web_line_only_by_naming_the_app(self):
        line = gh_mod.github_connector_reply(
            DegradationResponse(
                reason=DegradationReason.STALE_TOKEN, user_message="short", detail=REASON_CUTOVER
            )
        )
        assert line == (
            "GitHub now connects through the Piper GitHub app, so your connection needs to "
            "be set up again. Reconnect GitHub in the Piper Morgan app, in Settings under "
            "Integrations, and choose which repositories I can see. Your saved settings are "
            "unchanged."
        )
        assert line.replace(
            " in the Piper Morgan app, in Settings under", " in Settings, under"
        ) == (GITHUB_CUTOVER_STALE_REPLY)

    def test_a_reason_with_no_connector_line_keeps_its_message(self):
        line = gh_mod.github_connector_reply(
            DegradationResponse(
                reason=DegradationReason.CONNECT_REQUIRED,
                user_message="Connect GitHub to continue.",
            )
        )
        assert line == "Connect GitHub to continue."

    @pytest.mark.asyncio
    async def test_the_mcp_resource_shows_the_connector_line(self, monkeypatch):
        import json as _json

        from services.mcp.server import resources

        degraded = DegradationResponse(
            reason=DegradationReason.UNREACHABLE,
            user_message="GitHub's MCP server is unreachable right now.",
        )

        class _Adapter:
            async def list_open_issues(self, user_id, limit):
                return gh_mod.GitHubIssuesResult(issues=None, degradation=degraded)

        monkeypatch.setattr(resources, "GitHubMCPSpatialAdapter", _Adapter)
        monkeypatch.setattr(resources, "current_user_id", lambda: _OWNER)
        payload = _json.loads(await resources._read_github_issues())
        assert payload["available"] is False and payload["reason"] == "unreachable"
        assert payload["message"] == gh_mod.GITHUB_CONNECTOR_UNREACHABLE_REPLY
