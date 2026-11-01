"""#2242 (a): who may connect the hosted MCP during the beta.

xian's decision (10-31): an allowlist of his account and the cohort's test
accounts, refused for everyone else with a plain line on the consent page.
Arch's mechanism: ONE predicate (``may_connect_mcp``), ONE list source (a
reserved key in ``users.preferences``), checked at THREE points, failing closed:

1. the consent/authorize step (the route shows the line; the provider refuses
   independently, so a forged POST mints nothing);
2. the refresh grant (``invalid_grant``; refresh tokens last 30 days, so the
   consent page alone would not close access);
3. ``MCPTokenVerifier.verify_token`` (``None``, like a revoked token; this is
   what makes a removal bite on the next request and covers operator-minted
   tokens that never saw consent).

And Arch's three store conditions: the key is stripped before
``user_context_service``'s merge (a listed and an unlisted account get identical
context); only ``scripts/mcp_allow.py`` writes the key (enforcement pin in
``tests/test_architecture_enforcement.py``); a lost update fails closed and
``list`` re-reads after ``add`` (the script's tests below).

LAYER: the predicate with a dict-backed reader (the ``users`` table cannot be
created on the in-memory SQLite these tests use: its ``id`` is a Postgres UUID
column); the verifier, the provider and the consent route against the same
in-memory store the other MCP unit tests use; the context service with its
loader patched. The real read of ``users.preferences`` is pinned on Postgres in
``tests/integration/test_mcp_allowlist_2242.py``. Served checks are PA's.
"""

from __future__ import annotations

import hashlib
import html
import sys
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

import httpx  # noqa: E402
from mcp.server.auth.provider import AuthorizationParams, AuthorizeError, TokenError  # noqa: E402
from mcp.shared.auth import OAuthClientInformationFull  # noqa: E402
from pydantic import AnyUrl  # noqa: E402
from sqlalchemy import select  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool  # noqa: E402

from services.auth import auth_middleware as auth_middleware_module  # noqa: E402
from services.database.models import (  # noqa: E402
    MCPAccessToken,
    MCPOAuthClient,
    MCPOAuthCode,
    MCPOAuthRefreshToken,
)
from services.database.session_factory import AsyncSessionFactory  # noqa: E402
from services.mcp.server import allowlist  # noqa: E402
from services.mcp.server.allowlist import (  # noqa: E402
    MCP_ALLOW_KEY,
    may_connect_mcp,
    strip_reserved_keys,
)
from services.mcp.server.identity import MCPTokenVerifier, hash_credential  # noqa: E402
from services.mcp.server.oauth_provider import (  # noqa: E402
    PiperMCPOAuthProvider,
    PiperRefreshToken,
    consenting_user,
)
from services.user_context_service import UserContextService  # noqa: E402
from web.routers import mcp_oauth  # noqa: E402

pytestmark = pytest.mark.asyncio

LISTED = uuid.UUID("11111111-1111-1111-1111-111111111111")
UNLISTED = uuid.UUID("22222222-2222-2222-2222-222222222222")
REDIRECT_URI = "https://claude.test/oauth/callback"
ALPHA_BASE_URL = "http://alpha.test"
EMPTY_CONFIG_PATCH = "services.configuration.piper_config_loader.piper_config_loader.load_config"


# ─────────────────────────── the list, as a reader ───────────────────────────


def _reader_for(table: dict[uuid.UUID, dict | None]):
    """A dict-backed stand-in for the ``users.preferences`` read. A missing key
    is "no such row" (None); a dict is that row's preferences."""

    async def _read(user_id, **_kwargs):
        return table.get(user_id)

    return _read


@pytest.fixture
def listing(monkeypatch):
    """LISTED is on the list, UNLISTED has a row with other preferences only."""
    table = {LISTED: {MCP_ALLOW_KEY: True}, UNLISTED: {"timezone": "Europe/Helsinki"}}
    monkeypatch.setattr(allowlist, "read_preferences", _reader_for(table))
    return table


# ─────────────────────────── (1) the predicate ───────────────────────────────


class TestPredicate:
    async def test_listed_is_true(self):
        assert await may_connect_mcp(LISTED, reader=_reader_for({LISTED: {MCP_ALLOW_KEY: True}}))

    async def test_row_without_the_key_is_false(self):
        assert not await may_connect_mcp(UNLISTED, reader=_reader_for({UNLISTED: {}}))

    async def test_no_row_is_false(self):
        assert not await may_connect_mcp(UNLISTED, reader=_reader_for({}))

    @pytest.mark.parametrize("value", ["true", "yes", 1, "1", [True], {"on": True}])
    async def test_only_json_true_lists_an_account(self, value):
        """Strict: a stray write of a truthy value from some other path lists
        nobody. Only JSON ``true`` does."""
        assert not await may_connect_mcp(
            LISTED, reader=_reader_for({LISTED: {MCP_ALLOW_KEY: value}})
        )

    async def test_false_is_false(self):
        assert not await may_connect_mcp(
            LISTED, reader=_reader_for({LISTED: {MCP_ALLOW_KEY: False}})
        )

    async def test_a_failed_read_is_false_not_an_error(self):
        """Arch's point 4: if the list cannot be read, the predicate says no."""

        async def _boom(_user_id, **_kwargs):
            raise RuntimeError("database unreachable")

        assert await may_connect_mcp(LISTED, reader=_boom) is False

    @pytest.mark.parametrize("bad", ["not-a-uuid", "", None, 42])
    async def test_an_unparseable_user_id_is_false(self, bad):
        calls = []

        async def _read(user_id, **_kwargs):
            calls.append(user_id)
            return {MCP_ALLOW_KEY: True}

        assert not await may_connect_mcp(bad, reader=_read)
        assert calls == [], "no read is made for an id that is not a UUID"

    async def test_string_and_uuid_forms_of_the_same_id_agree(self):
        reader = _reader_for({LISTED: {MCP_ALLOW_KEY: True}})
        assert await may_connect_mcp(str(LISTED), reader=reader)
        assert await may_connect_mcp(LISTED, reader=reader)

    async def test_the_default_reader_is_the_module_level_read(self, listing):
        """The verifier, the provider and the route call the predicate without a
        reader; it must go through the module attribute the fixtures patch."""
        assert await may_connect_mcp(LISTED)
        assert not await may_connect_mcp(UNLISTED)


class TestStripReservedKeys:
    def test_removes_only_the_key(self):
        assert strip_reserved_keys({MCP_ALLOW_KEY: True, "timezone": "UTC"}) == {"timezone": "UTC"}

    def test_an_account_whose_only_preference_is_the_key_reads_as_none(self):
        assert strip_reserved_keys({MCP_ALLOW_KEY: True}) == {}

    def test_none_and_empty(self):
        assert strip_reserved_keys(None) == {}
        assert strip_reserved_keys({}) == {}

    def test_returns_a_copy(self):
        src = {"a": 1}
        out = strip_reserved_keys(src)
        assert out == src and out is not src


# ─────────────────────────── the in-memory store ─────────────────────────────


@pytest_asyncio.fixture
async def store():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @asynccontextmanager
    async def _scope():
        session = factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async with engine.begin() as conn:
        for model in (MCPAccessToken, MCPOAuthClient, MCPOAuthCode, MCPOAuthRefreshToken):
            await conn.run_sync(
                lambda c, m=model: m.__table__.create(c, checkfirst=True)  # type: ignore[attr-defined]
            )
    yield factory, _scope
    await engine.dispose()


async def _rows(factory, model):
    async with factory() as session:
        return list((await session.execute(select(model))).scalars().all())


async def _seed_access_token(factory, *, user_id: uuid.UUID, raw: str) -> None:
    async with factory() as session:
        session.add(
            MCPAccessToken(
                id=uuid.uuid4(),
                user_id=user_id,
                token_hash=hashlib.sha256(raw.encode()).hexdigest(),
                label="test",
                expires_at=None,
                revoked_at=None,
            )
        )
        await session.commit()


# ─────────────────────────── (3) the verifier ────────────────────────────────


class TestVerifierRefusesUnlistedOwner:
    async def test_valid_token_of_an_unlisted_owner_reads_nothing(self, store, listing):
        factory, scope = store
        await _seed_access_token(factory, user_id=UNLISTED, raw="mcp_unlisted_token")
        assert (
            await MCPTokenVerifier(session_scope=scope).verify_token("mcp_unlisted_token") is None
        )

    async def test_valid_token_of_a_listed_owner_resolves(self, store, listing):
        factory, scope = store
        await _seed_access_token(factory, user_id=LISTED, raw="mcp_listed_token")
        resolved = await MCPTokenVerifier(session_scope=scope).verify_token("mcp_listed_token")
        assert resolved is not None and resolved.client_id == str(LISTED)

    async def test_removal_bites_on_the_next_request(self, store, listing):
        """The same token: resolves while listed, refused the request after the
        account leaves the list. No new token, no consent, no 30-day wait."""
        factory, scope = store
        await _seed_access_token(factory, user_id=LISTED, raw="mcp_once_listed")
        verifier = MCPTokenVerifier(session_scope=scope)
        assert await verifier.verify_token("mcp_once_listed") is not None
        del listing[LISTED][MCP_ALLOW_KEY]
        assert await verifier.verify_token("mcp_once_listed") is None

    async def test_a_failed_list_read_refuses_the_token(self, store, monkeypatch):
        factory, scope = store
        await _seed_access_token(factory, user_id=LISTED, raw="mcp_fault")

        async def _boom(_user_id, **_kwargs):
            raise RuntimeError("list unreadable")

        monkeypatch.setattr(allowlist, "read_preferences", _boom)
        assert await MCPTokenVerifier(session_scope=scope).verify_token("mcp_fault") is None


# ─────────────────────────── (1) the provider's authorize ────────────────────


async def _register(provider, client_id="claude-desktop"):
    await provider.register_client(
        OAuthClientInformationFull(
            client_id=client_id,
            client_secret=None,
            redirect_uris=[AnyUrl(REDIRECT_URI)],
            token_endpoint_auth_method="none",
            client_name="Claude",
        )
    )
    client = await provider.get_client(client_id)
    assert client is not None
    return client


def _params():
    return AuthorizationParams(
        state="st",
        scopes=["resources:read"],
        code_challenge="E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM",
        redirect_uri=AnyUrl(REDIRECT_URI),
        redirect_uri_provided_explicitly=True,
    )


class TestProviderAuthorizeRefusesUnlisted:
    async def test_unlisted_consenting_user_gets_no_code(self, store, listing):
        factory, scope = store
        provider = PiperMCPOAuthProvider(session_scope=scope)
        client = await _register(provider)
        with consenting_user(str(UNLISTED)):
            with pytest.raises(AuthorizeError) as caught:
                await provider.authorize(client, _params())
        assert caught.value.error == "access_denied"
        assert await _rows(factory, MCPOAuthCode) == []

    async def test_listed_consenting_user_gets_a_code(self, store, listing):
        factory, scope = store
        provider = PiperMCPOAuthProvider(session_scope=scope)
        client = await _register(provider)
        with consenting_user(str(LISTED)):
            redirect = await provider.authorize(client, _params())
        assert "code=" in redirect
        rows = await _rows(factory, MCPOAuthCode)
        assert [str(r.user_id) for r in rows] == [str(LISTED)]


# ─────────────────────────── (2) the refresh grant ───────────────────────────


async def _seed_refresh(factory, *, user_id: uuid.UUID, raw: str, client_id: str) -> None:
    async with factory() as session:
        session.add(
            MCPOAuthRefreshToken(
                id=uuid.uuid4(),
                token_hash=hash_credential(raw),
                client_id=client_id,
                user_id=user_id,
                scopes=["resources:read"],
                expires_at=datetime.now(timezone.utc) + timedelta(days=30),
            )
        )
        await session.commit()


class TestRefreshRefusesUnlisted:
    async def test_unlisted_owner_cannot_renew_and_the_presented_token_is_spent(
        self, store, listing
    ):
        factory, scope = store
        provider = PiperMCPOAuthProvider(session_scope=scope)
        client = await _register(provider)
        await _seed_refresh(
            factory, user_id=UNLISTED, raw="mcp_refresh_unlisted", client_id=client.client_id
        )
        presented = PiperRefreshToken(
            token="mcp_refresh_unlisted",
            client_id=client.client_id,
            scopes=["resources:read"],
            expires_at=None,
            user_id=str(UNLISTED),
        )
        with pytest.raises(TokenError) as caught:
            await provider.exchange_refresh_token(client, presented, ["resources:read"])
        assert caught.value.error == "invalid_grant"
        assert await _rows(factory, MCPAccessToken) == [], "nothing minted"
        (row,) = await _rows(factory, MCPOAuthRefreshToken)
        assert row.revoked_at is not None, "the presented refresh token is spent (closed direction)"

    async def test_listed_owner_renews(self, store, listing):
        factory, scope = store
        provider = PiperMCPOAuthProvider(session_scope=scope)
        client = await _register(provider)
        await _seed_refresh(
            factory, user_id=LISTED, raw="mcp_refresh_listed", client_id=client.client_id
        )
        presented = PiperRefreshToken(
            token="mcp_refresh_listed",
            client_id=client.client_id,
            scopes=["resources:read"],
            expires_at=None,
            user_id=str(LISTED),
        )
        minted = await provider.exchange_refresh_token(client, presented, ["resources:read"])
        assert minted.access_token
        rows = await _rows(factory, MCPAccessToken)
        assert [str(r.user_id) for r in rows] == [str(LISTED)]


# ─────────────────────────── (1) the consent route ───────────────────────────


@pytest.fixture
def wired(monkeypatch, store):
    """Alpha's real app against the in-memory store, with the session cookie
    validating to its own value and the admin lookup stubbed (the unit-4 shape)."""
    factory, scope = store
    monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)
    from services.auth.jwt_service import JWTService

    async def _validate(self, token):  # noqa: ARG001
        try:
            uuid.UUID(str(token))
        except ValueError:
            return None
        return SimpleNamespace(user_id=str(token), scopes=[])

    monkeypatch.setattr(JWTService, "validate_token", _validate)

    async def _not_admin(user_id):  # noqa: ARG001
        return False

    monkeypatch.setattr(auth_middleware_module, "_admin_state_for", _not_admin)
    return factory, scope


@asynccontextmanager
async def _alpha(cookie_user: uuid.UUID):
    from web.app import app as alpha_app

    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=alpha_app),
        base_url=ALPHA_BASE_URL,
        cookies={"auth_token": str(cookie_user)},
        follow_redirects=False,
        timeout=httpx.Timeout(30.0),
    ) as client:
        yield client


def _authorize_query(client_id: str, challenge: str) -> dict[str, str]:
    return {
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": "st",
        "scope": "resources:read",
        "resource": "https://mcp.pipermorgan.ai/mcp",
    }


class TestConsentPageRefusesUnlisted:
    CHALLENGE = "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"

    async def test_get_shows_the_line_and_no_form(self, wired, listing):
        factory, scope = wired
        client = await _register(PiperMCPOAuthProvider(session_scope=scope))
        async with _alpha(UNLISTED) as http:
            resp = await http.get(
                mcp_oauth.AUTHORIZE_PATH,
                params=_authorize_query(client.client_id, self.CHALLENGE),
                headers={"Accept": "text/html"},
            )
        assert resp.status_code == 403
        assert (
            html.escape(mcp_oauth.MCP_NOT_OFFERED_LINE) in resp.text
        )  # the page escapes the apostrophe
        assert "consent_token" not in resp.text
        assert 'value="approve"' not in resp.text

    def test_the_words_are_cxos(self):
        """CXO 07:40 (11-01): the heading names what the person tried; the page has
        a way on (Piper in the browser, a relative link, no promised date)."""
        assert (
            mcp_oauth.MCP_NOT_OFFERED_LINE
            == "Connecting Piper to Claude isn't part of this beta yet."
        )
        assert mcp_oauth.MCP_NOT_OFFERED_WAY_ON == "You can keep using Piper in your browser."

    async def test_the_page_has_a_way_on_and_still_no_form(self, wired, listing):
        factory, scope = wired
        client = await _register(PiperMCPOAuthProvider(session_scope=scope))
        async with _alpha(UNLISTED) as http:
            resp = await http.get(
                mcp_oauth.AUTHORIZE_PATH,
                params=_authorize_query(client.client_id, self.CHALLENGE),
                headers={"Accept": "text/html"},
            )
        assert resp.status_code == 403
        assert "You can keep using Piper in your browser." in resp.text
        assert '<a href="/">Open Piper Morgan</a>' in resp.text
        assert "nothing was connected" in resp.text
        assert "<form" not in resp.text
        assert 'type="hidden"' not in resp.text
        assert "code=" not in resp.text

    async def test_a_forged_approve_post_mints_no_code(self, wired, listing):
        """Even with a valid consent token (as if the form had been shown), the
        POST is refused and no code row exists. Two independent refusals: the
        route's, and the provider's own authorize()."""
        factory, scope = wired
        client = await _register(PiperMCPOAuthProvider(session_scope=scope))
        token = mcp_oauth._sign_consent(
            str(UNLISTED), client.client_id, self.CHALLENGE, int(time.time()) + 600
        )
        data = dict(_authorize_query(client.client_id, self.CHALLENGE))
        data.update({"consent": "approve", "consent_token": token})
        async with _alpha(UNLISTED) as http:
            resp = await http.post(mcp_oauth.AUTHORIZE_PATH, data=data)
        assert resp.status_code == 403
        assert (
            html.escape(mcp_oauth.MCP_NOT_OFFERED_LINE) in resp.text
        )  # the page escapes the apostrophe
        assert await _rows(factory, MCPOAuthCode) == []

    async def test_listed_account_sees_the_consent_form(self, wired, listing):
        factory, scope = wired
        client = await _register(PiperMCPOAuthProvider(session_scope=scope))
        async with _alpha(LISTED) as http:
            resp = await http.get(
                mcp_oauth.AUTHORIZE_PATH,
                params=_authorize_query(client.client_id, self.CHALLENGE),
                headers={"Accept": "text/html"},
            )
        assert resp.status_code == 200
        assert 'value="approve"' in resp.text
        assert html.escape(mcp_oauth.MCP_NOT_OFFERED_LINE) not in resp.text


# ─────────────────────────── store condition 1: context unchanged ────────────


class TestListedAccountsContextIsUnchanged:
    """Arch's condition 1 on the store: the flag must not change the user's own
    context. The merge in ``_load_context_from_config`` and its ``elif user_prefs``
    branch would both see the key; stripping it first means a listed account with
    no other preferences reads exactly like an unlisted one."""

    async def _context(self, prefs):
        svc = UserContextService()
        svc._context_cache = {}
        with patch(EMPTY_CONFIG_PATCH, return_value={}):
            with patch.object(svc, "_load_user_preferences_from_db", AsyncMock(return_value=prefs)):
                with patch.object(svc, "_load_projects_from_db", AsyncMock(return_value=[])):
                    return await svc._load_context_from_config("sess", uuid.uuid4())

    async def test_listed_and_unlisted_with_no_other_preferences_are_identical(self):
        listed = await self._context({MCP_ALLOW_KEY: True})
        unlisted = await self._context({})
        for field in ("projects", "projects_source", "priorities", "preferences", "organization"):
            assert getattr(listed, field) == getattr(unlisted, field), field
        assert listed.projects_source == "config"
        assert listed.preferences == {}

    async def test_the_key_never_rides_into_the_context_preferences(self):
        ctx = await self._context({MCP_ALLOW_KEY: True, "timezone": "Europe/Helsinki"})
        assert MCP_ALLOW_KEY not in ctx.preferences
        assert ctx.preferences == {"timezone": "Europe/Helsinki"}


# ─────────────────────────── store conditions 2 and 3: the one writer ────────

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "scripts"))
import mcp_allow  # noqa: E402


class _FakeConn:
    """Records the statements the script runs; answers ``listed`` from ``rows``."""

    def __init__(self, rows):
        self.rows = rows
        self.executed: list[tuple[str, dict]] = []

    def execute(self, stmt, params=None):
        self.executed.append((str(stmt), dict(params or {})))
        rows = self.rows
        return SimpleNamespace(fetchall=lambda: rows, first=lambda: (rows[0] if rows else None))


class TestOperatorScript:
    @pytest.mark.parametrize(
        "args",
        [
            SimpleNamespace(command="add", user_email="a@b.co", user_id=None),
            SimpleNamespace(command="remove", user_email=None, user_id=str(LISTED)),
            SimpleNamespace(command="list"),
        ],
    )
    def test_valid_shapes_pass(self, args):
        mcp_allow._validate(args)

    @pytest.mark.parametrize(
        "args",
        [
            SimpleNamespace(command="add", user_email=None, user_id=None),
            SimpleNamespace(command="add", user_email="a@b.co", user_id=str(LISTED)),
            SimpleNamespace(command="add", user_email="not an email", user_id=None),
            SimpleNamespace(command="remove", user_email=None, user_id="not-a-uuid"),
            SimpleNamespace(command="list", user_email="a@b.co", user_id=None),
            SimpleNamespace(command="grant", user_email="a@b.co", user_id=None),
        ],
    )
    def test_bad_shapes_are_refused_before_any_connection(self, args):
        with pytest.raises(SystemExit):
            mcp_allow._validate(args)

    def test_add_is_an_atomic_jsonb_merge_then_rereads_the_list(self, capsys):
        conn = _FakeConn(rows=[(LISTED, "x@y.z", "x")])
        mcp_allow.add(conn, str(LISTED))
        (write, write_params), (reread, reread_params) = conn.executed
        assert "||" in write and "jsonb_build_object" in write, "merge one key, keep the rest"
        assert "coalesce(preferences" in write
        assert write_params == {"key": MCP_ALLOW_KEY, "user_id": str(LISTED)}
        assert "->> :key = 'true'" in reread, "the re-read is as strict as the predicate"
        assert "listed: 1" in capsys.readouterr().out

    def test_remove_is_an_atomic_key_drop_then_rereads(self, capsys):
        conn = _FakeConn(rows=[])
        mcp_allow.remove(conn, str(LISTED))
        (write, params), (reread, _) = conn.executed
        assert "preferences - :key" in write
        assert params == {"key": MCP_ALLOW_KEY, "user_id": str(LISTED)}
        assert "->> :key" in reread
        assert "listed: 0" in capsys.readouterr().out

    def test_the_script_uses_the_module_key_not_its_own_literal(self):
        src = Path(mcp_allow.__file__).read_text(encoding="utf-8")
        assert "mcp_connect_allowed" not in src
        assert "from services.mcp.server.allowlist import MCP_ALLOW_KEY" in src
