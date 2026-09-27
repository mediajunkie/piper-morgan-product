"""Phase C unit 4 — the MCP OAuth 2.1 authorization server (#1462).

═══ WHAT THIS FILE EXISTS TO PROVE ═══

Arch's unit-4 review condition (``mailboxes/lead/read/lean-arch-to-pa-cc-lead-exec-pm-
mcp-oauth-as-lean-lead-builds-it-your-call-2026-09-26.md``), verbatim:

    verify the OAuth flow binds the minted token to the SAME identity that
    authenticated at the authorize step, throughout — the specific failure shape:
    exchange_authorization_code minting a token for a different (or unresolved)
    identity than the one that consented. Explicit test, not an assumed property.

The eight things tested, in the build order the dispatch named:

(1) FULL HAPPY PATH, end to end across BOTH hosts: dynamic client registration →
    authorize as session user A → consent Approve → code → PKCE exchange → the
    minted token presented to the MCP RESOURCE SERVER reads ``piper://me/profile``
    **as A**, asserted via the same per-user read spy unit 2's tests use (the
    user_id the resource read actually received == A's).
(2) NO alpha session at ``/authorize`` → no code issued, redirect to /login, ZERO
    rows written. Plus the provider-level form: ``authorize()`` with no consenting
    identity bound raises and writes nothing.
(3) A code issued to A can NEVER be exchanged into a token that resolves to B —
    three adversarial constructions (B's client presenting A's code; an
    ``AuthorizationCode`` object claiming B while the stored row says A; an
    owner-less row reaching the mint), each refused with NOTHING minted.
(4) PKCE mismatch → refused.
(5) Replayed code → refused AND the access token the first exchange minted is
    REVOKED (OAuth 2.1 §4.1.2.5) — and the revocation is verified to have been
    COMMITTED, since the bug it guards against is a rollback.
(6) Refresh token → a new access token for the same user only; the presented
    refresh token is rotated (single-use).
(7) Metadata discovery resolves end to end from what the RS advertises: RS
    protected-resource metadata → issuer → AS metadata → endpoints that are the
    paths actually mounted.
(8) The RS's existing 401 behavior is unchanged by unit 4 (an unknown bearer still
    reads nothing; the RFC 9728 metadata route is reachable — it was NOT, before
    unit 4 opened it in ``MCPPathGate``).

Bonus, same identity boundary: consent-CSRF (a forged approve POST without a valid
consent token mints nothing) and Deny (no code, ``error=access_denied``).

═══ LAYER (m-43) ═══

The AS is exercised through **alpha's real ASGI app** (``web.app:app``) over
``httpx.ASGITransport`` — so ``AuthMiddleware``, the real mounted routes, and the
real SDK handlers all run. The RS is exercised through a **real MCP client**
(``mcp.client.streamable_http`` + ``ClientSession``) against
``build_mcp_server()`` + ``MCPPathGate``, the unit-1/unit-2 idiom. Nothing here
asserts on a hand-built request object or a direct call into a handler except where
a test explicitly names the provider method it is probing (tests 2b, 3b, 3c).

The two hosts share one monkeypatched ``AsyncSessionFactory.session_scope``, which
is how the token minted on the AS side is findable by the RS's verifier — the same
``mcp_access_tokens`` table, deliberately (one verifier, one boundary).

═══ DENOMINATOR (m-44) ═══

Unit 4's authorization-server surface and the identity binding through it. NOT
covered here: unit 1's refusal conditions (revoked/expired/unknown bearer — see
``test_identity_unit1.py``), unit 2's per-resource payload shapes (see
``test_resources_unit2.py``), and **no live client**: ChatGPT was never exercised.
What is claimed about ChatGPT is only that the metadata a spec-compliant OAuth 2.1
+ DCR + PKCE client needs is present and self-consistent (test 7), which is a
statement about our endpoints, not about ChatGPT's behavior.

DB fixture: in-memory SQLite + ``StaticPool`` + teardown disposal, exactly as
``test_identity_unit1.py`` documents (including WHY StaticPool and WHY disposal is
in a fixture) — no Docker/Postgres dependency.
"""

from __future__ import annotations

import base64
import hashlib
import re
import secrets
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from typing import Any
from urllib.parse import parse_qs, urlsplit

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

import httpx  # noqa: E402
import sse_starlette.sse as _sse_starlette_sse  # noqa: E402
from mcp.client.session import ClientSession  # noqa: E402
from mcp.client.streamable_http import streamable_http_client  # noqa: E402
from mcp.server.auth.provider import AuthorizationParams, AuthorizeError, TokenError  # noqa: E402
from mcp.shared.auth import OAuthClientInformationFull  # noqa: E402
from pydantic import AnyUrl, ValidationError  # noqa: E402
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
from services.mcp.server.app import MCPPathGate, build_mcp_server  # noqa: E402
from services.mcp.server.identity import hash_credential  # noqa: E402
from services.mcp.server.oauth_provider import (  # noqa: E402
    ACCESS_TOKEN_PREFIX,
    OAUTH_LABEL_PREFIX,
    PiperAuthorizationCode,
    PiperMCPOAuthProvider,
    _CodeSnapshot,
    _refuse_code,
    consenting_user,
)
from services.user_context_service import UserContext, user_context_service  # noqa: E402
from web.routers import mcp_oauth  # noqa: E402

pytestmark = pytest.mark.asyncio

MCP_PATH = "/mcp"
# Matches FastMCP's auto-enabled DNS-rebinding allowlist (see test_identity_unit1.py's
# HOST HEADER NOTE) — a request that gets PAST auth is checked against it.
LOCAL_BASE_URL = "http://localhost:8080"
ALPHA_BASE_URL = "http://alpha.test"
PROFILE_URI = "piper://me/profile"

USER_A = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
USER_B = uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")

REDIRECT_URI_A = "https://chatgpt.test/oauth/callback"
REDIRECT_URI_B = "https://attacker.test/oauth/callback"


@pytest.fixture(autouse=True)
def _reset_sse_starlette_loop_singleton():
    """``sse_starlette.sse.AppStatus.should_exit_event`` is a process-global bound to
    the first loop that starts an SSE response; pytest-asyncio gives each test its
    own loop. Reset per test — same fix, same reason, as test_identity_unit1.py."""
    _sse_starlette_sse.AppStatus.should_exit = False
    _sse_starlette_sse.AppStatus.should_exit_event = None
    yield


# ─────────────────────────── fixtures ────────────────────────────────────────


@pytest_asyncio.fixture
async def store():
    """In-memory SQLite holding the four tables this unit touches, disposed on
    teardown regardless of outcome."""
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


@pytest.fixture
def wired(monkeypatch, store):
    """Both hosts pointed at the SAME in-memory store, with alpha's JWT validation
    and admin lookup stubbed.

    The provider the real app mounted at import time resolves its session scope
    LAZILY (``PiperMCPOAuthProvider._scope``), which is what makes patching
    ``AsyncSessionFactory.session_scope`` here effective on an already-constructed
    provider — the alternative (capturing the scope in ``__init__``) would have made
    the real app untestable without re-mounting it.
    """
    factory, scope = store
    monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)

    # The alpha session: a cookie value of str(user_uuid) validates to that user.
    # Patching JWTService.validate_token (not the middleware instance) because the
    # real app built its middleware at import time from the AuthContainer singleton.
    from services.auth.jwt_service import JWTService

    async def _validate(self, token):  # noqa: ARG001
        try:
            uuid.UUID(str(token))
        except ValueError:
            return None
        return SimpleNamespace(user_id=str(token), scopes=[])

    monkeypatch.setattr(JWTService, "validate_token", _validate)
    # `request.state.is_admin` does a live users-table read; irrelevant here and it
    # would try to reach Postgres. (It already fails closed to False — this just
    # keeps the test hermetic and fast.)

    async def _not_admin(user_id):  # noqa: ARG001
        return False

    monkeypatch.setattr(auth_middleware_module, "_admin_state_for", _not_admin)
    return factory, scope


@asynccontextmanager
async def alpha_client(cookie_user: uuid.UUID | None = None):
    """An async HTTP client against alpha's REAL app (``web.app:app``), so
    AuthMiddleware and the real mounted AS routes both run. No lifespan (ASGI
    transport sends none), which these routes don't need."""
    from web.app import app as alpha_app

    cookies = {"auth_token": str(cookie_user)} if cookie_user else {}
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=alpha_app),
        base_url=ALPHA_BASE_URL,
        cookies=cookies,
        follow_redirects=False,
        timeout=httpx.Timeout(30.0),
    ) as client:
        yield client


# ─────────────────────────── flow helpers ────────────────────────────────────


def _pkce() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(48)
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
    )
    return verifier, challenge


async def _register_client(
    client: httpx.AsyncClient, *, redirect_uri: str = REDIRECT_URI_A, name: str = "ChatGPT"
) -> dict[str, Any]:
    resp = await client.post(
        mcp_oauth.REGISTER_PATH,
        json={"redirect_uris": [redirect_uri], "client_name": name},
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


_CONSENT_TOKEN_RE = re.compile(r'name="consent_token" value="([^"]+)"')


async def _get_consent_page(
    client: httpx.AsyncClient, *, client_id: str, challenge: str, redirect_uri: str, state: str
) -> httpx.Response:
    return await client.get(
        mcp_oauth.AUTHORIZE_PATH,
        params={
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "state": state,
            "scope": "resources:read",
            "resource": "https://mcp.pipermorgan.ai/mcp",
        },
        headers={"Accept": "text/html"},
    )


async def _consent(
    client: httpx.AsyncClient,
    *,
    client_id: str,
    challenge: str,
    redirect_uri: str,
    state: str,
    consent_token: str,
    decision: str = "approve",
) -> httpx.Response:
    return await client.post(
        mcp_oauth.AUTHORIZE_PATH,
        data={
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "code_challenge": challenge,
            "code_challenge_method": "S256",
            "state": state,
            "scope": "resources:read",
            "resource": "https://mcp.pipermorgan.ai/mcp",
            "consent": decision,
            "consent_token": consent_token,
        },
    )


def _code_from_redirect(resp: httpx.Response) -> str:
    assert resp.status_code == 302, resp.text
    query = parse_qs(urlsplit(resp.headers["location"]).query)
    assert "code" in query, f"no code in redirect: {resp.headers['location']}"
    return query["code"][0]


async def _authorize_as(
    client: httpx.AsyncClient, *, client_id: str, redirect_uri: str = REDIRECT_URI_A
) -> tuple[str, str]:
    """Full browser half of the flow: consent page → Approve → code. Returns
    (raw_code, code_verifier)."""
    verifier, challenge = _pkce()
    page = await _get_consent_page(
        client,
        client_id=client_id,
        challenge=challenge,
        redirect_uri=redirect_uri,
        state="st-123",
    )
    assert page.status_code == 200, page.text
    match = _CONSENT_TOKEN_RE.search(page.text)
    assert match, "consent page carried no consent_token"
    redirect = await _consent(
        client,
        client_id=client_id,
        challenge=challenge,
        redirect_uri=redirect_uri,
        state="st-123",
        consent_token=match.group(1),
    )
    return _code_from_redirect(redirect), verifier


async def _exchange(
    client: httpx.AsyncClient,
    *,
    registration: dict[str, Any],
    code: str,
    verifier: str,
    redirect_uri: str = REDIRECT_URI_A,
) -> httpx.Response:
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": registration["client_id"],
        "code_verifier": verifier,
    }
    if registration.get("client_secret"):
        data["client_secret"] = registration["client_secret"]
    return await client.post(mcp_oauth.TOKEN_PATH, data=data)


# ─────────────────────────── store assertions ────────────────────────────────


async def _rows(factory, model) -> list[Any]:
    async with factory() as session:
        return list((await session.execute(select(model))).scalars().all())


async def _access_token_rows(factory) -> list[MCPAccessToken]:
    return await _rows(factory, MCPAccessToken)


# ─────────────────────────── the resource server ─────────────────────────────


@asynccontextmanager
async def rs_session(raw_token: str):
    """A real MCP client session against the resource server, authenticating with
    ``raw_token`` — the unit-1/unit-2 idiom (built by hand rather than via
    ``build_asgi_app()`` so the session manager's task group can be entered
    explicitly: ``httpx.ASGITransport`` sends no lifespan events)."""
    mcp = build_mcp_server()
    inner = mcp.streamable_http_app()
    asgi_app = MCPPathGate(inner, mcp_path=mcp.settings.streamable_http_path)
    async with mcp.session_manager.run():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=asgi_app),
            base_url=LOCAL_BASE_URL,
            headers={"Authorization": f"Bearer {raw_token}"},
            timeout=httpx.Timeout(30.0),
        ) as http_client:
            async with streamable_http_client(
                f"{LOCAL_BASE_URL}{MCP_PATH}", http_client=http_client
            ) as (read_stream, write_stream, _sid):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    yield session


# ═════════════════════════════ (1) happy path ════════════════════════════════


class TestFullHappyPathAcrossBothHosts:
    async def test_minted_token_reads_the_resource_as_the_consenting_user(
        self, monkeypatch, wired
    ) -> None:
        """register → authorize as A → consent → PKCE exchange → the token reads
        ``piper://me/profile`` AS A, asserted by the user_id the resource read
        actually received (unit 2's spy shape), not by the payload alone."""
        factory, _scope = wired

        async with alpha_client(cookie_user=USER_A) as client:
            registration = await _register_client(client)
            code, verifier = await _authorize_as(client, client_id=registration["client_id"])
            token_resp = await _exchange(
                client, registration=registration, code=code, verifier=verifier
            )

        assert token_resp.status_code == 200, token_resp.text
        payload = token_resp.json()
        assert payload["token_type"] == "Bearer"
        assert payload["scope"] == "resources:read"
        assert payload["expires_in"] == 3600
        access_token = payload["access_token"]
        assert access_token.startswith(ACCESS_TOKEN_PREFIX)
        assert payload["refresh_token"]

        # The minted row is an mcp_access_tokens row owned by A — unit 1's table,
        # unit 1's verifier, no second credential format.
        rows = await _access_token_rows(factory)
        assert len(rows) == 1
        assert str(rows[0].user_id) == str(USER_A)
        assert rows[0].token_hash == hash_credential(access_token)
        assert str(rows[0].label) == f"{OAUTH_LABEL_PREFIX}{registration['client_id']}"
        assert rows[0].expires_at is not None, "an OAuth-minted token must expire"

        # ── and now the load-bearing half: the RESOURCE SERVER resolves it to A ──
        seen: list[uuid.UUID | None] = []

        async def _stub(session_id=None, user_id=None):
            seen.append(user_id)
            return UserContext(
                user_id=user_id,
                organization="Org A",
                projects=["project-a"],
                priorities=["priority-a"],
                projects_source="database",
            )

        monkeypatch.setattr(user_context_service, "get_user_context", _stub)

        async with rs_session(access_token) as session:
            result = await session.read_resource(AnyUrl(PROFILE_URI))
            text = result.contents[0].text  # type: ignore[union-attr]

        assert "Org A" in text
        # THE assertion Arch's condition reduces to: the identity the resource read
        # was scoped to is the identity that authenticated at /authorize.
        assert seen == [USER_A]
        assert seen != [USER_B]


# ═══════════════════════ (2) no session → no code ════════════════════════════


class TestNoSessionNoCode:
    async def test_authorize_without_alpha_session_writes_nothing_and_bounces_to_login(
        self, wired
    ) -> None:
        factory, _scope = wired
        async with alpha_client(cookie_user=USER_A) as client:
            registration = await _register_client(client)

        _verifier, challenge = _pkce()
        async with alpha_client(cookie_user=None) as anon:
            resp = await _get_consent_page(
                anon,
                client_id=registration["client_id"],
                challenge=challenge,
                redirect_uri=REDIRECT_URI_A,
                state="st",
            )
            # Also try to skip straight to the approve POST.
            forced = await _consent(
                anon,
                client_id=registration["client_id"],
                challenge=challenge,
                redirect_uri=REDIRECT_URI_A,
                state="st",
                consent_token="anything",
            )

        assert resp.status_code == 302
        location = resp.headers["location"]
        assert location.startswith("/login?next="), location
        assert "%2Fmcp%2Foauth%2Fauthorize" in location, "the next param must carry us back"
        # No code was issued, by either route, and nothing was written.
        assert "code=" not in location
        assert forced.status_code in (302, 401), forced.text
        if forced.status_code == 302:
            assert forced.headers["location"].startswith("/login?next=")
        assert await _rows(factory, MCPOAuthCode) == []
        assert await _access_token_rows(factory) == []

    async def test_provider_authorize_refuses_with_no_consenting_identity(self, wired) -> None:
        """The provider-level form of the same property: even called directly, with
        a valid client and valid params, ``authorize()`` refuses when no consenting
        session is bound — there is no default user."""
        factory, scope = wired
        provider = PiperMCPOAuthProvider(session_scope=scope)
        await provider.register_client(
            OAuthClientInformationFull(
                client_id="client-direct",
                client_secret=None,
                redirect_uris=[AnyUrl(REDIRECT_URI_A)],
                token_endpoint_auth_method="none",
            )
        )
        client = await provider.get_client("client-direct")
        assert client is not None
        _verifier, challenge = _pkce()
        params = AuthorizationParams(
            state="st",
            scopes=["resources:read"],
            code_challenge=challenge,
            redirect_uri=AnyUrl(REDIRECT_URI_A),
            redirect_uri_provided_explicitly=True,
        )

        with pytest.raises(AuthorizeError) as caught:
            await provider.authorize(client, params)

        assert caught.value.error == "access_denied"
        assert await _rows(factory, MCPOAuthCode) == []

    async def test_consenting_user_refuses_an_empty_binding(self) -> None:
        """The binding helper itself refuses "consent on behalf of nobody", so an
        empty user id fails at the binding site rather than producing an
        owner-less code downstream."""
        with pytest.raises(ValueError):
            with consenting_user(""):
                pass  # pragma: no cover


# ══════════════════ (3) A's code can never become B's token ══════════════════


class TestCodeCannotCrossIdentities:
    async def test_another_clients_exchange_of_As_code_mints_nothing(self, wired) -> None:
        """B's client presents A's code at /token. Refused, and NOTHING is minted —
        so there is no token that could resolve to anyone at all, let alone B."""
        factory, _scope = wired
        async with alpha_client(cookie_user=USER_A) as client:
            reg_a = await _register_client(client, redirect_uri=REDIRECT_URI_A, name="ChatGPT")
            reg_b = await _register_client(client, redirect_uri=REDIRECT_URI_B, name="Attacker")
            code, verifier = await _authorize_as(client, client_id=reg_a["client_id"])

            stolen = await client.post(
                mcp_oauth.TOKEN_PATH,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": REDIRECT_URI_A,
                    "client_id": reg_b["client_id"],
                    "client_secret": reg_b.get("client_secret") or "",
                    "code_verifier": verifier,
                },
            )

        assert stolen.status_code == 400, stolen.text
        assert stolen.json()["error"] == "invalid_grant"
        assert await _access_token_rows(factory) == []

    async def test_a_code_object_claiming_a_different_owner_is_refused(self, wired) -> None:
        """The exact failure shape Arch named, constructed directly: the SDK handler
        hands ``exchange_authorization_code`` an ``AuthorizationCode`` whose
        ``user_id`` says B while the stored row says A. The row is the authority and
        the disagreement is a refusal — the exchange does not pick a side."""
        factory, scope = wired
        provider = PiperMCPOAuthProvider(session_scope=scope)
        await provider.register_client(
            OAuthClientInformationFull(
                client_id="client-tamper",
                client_secret=None,
                redirect_uris=[AnyUrl(REDIRECT_URI_A)],
                token_endpoint_auth_method="none",
            )
        )
        client = await provider.get_client("client-tamper")
        assert client is not None
        _v, challenge = _pkce()
        with consenting_user(str(USER_A)):
            redirect = await provider.authorize(
                client,
                AuthorizationParams(
                    state=None,
                    scopes=["resources:read"],
                    code_challenge=challenge,
                    redirect_uri=AnyUrl(REDIRECT_URI_A),
                    redirect_uri_provided_explicitly=True,
                ),
            )
        raw_code = parse_qs(urlsplit(redirect).query)["code"][0]

        loaded = await provider.load_authorization_code(client, raw_code)
        assert loaded is not None
        assert loaded.user_id == str(USER_A), "the loaded code must carry the consenting owner"

        tampered = loaded.model_copy(update={"user_id": str(USER_B)})
        with pytest.raises(TokenError) as caught:
            await provider.exchange_authorization_code(client, tampered)

        assert caught.value.error == "invalid_grant"
        assert await _access_token_rows(factory) == [], "nothing may be minted on a mismatch"

    async def test_an_owner_less_code_row_cannot_reach_a_minted_token(self, wired) -> None:
        """The stored owner is NOT NULL, so an owner-less code is unreachable through
        the store — asserted structurally, and the guard is exercised anyway by
        handing the mint an owner-less row. "Structurally impossible" is a claim;
        the refusal is the mechanism."""
        factory, scope = wired
        assert MCPOAuthCode.__table__.c.user_id.nullable is False
        # The SDK model subclass also cannot be constructed without an owner.
        with pytest.raises(ValidationError):
            PiperAuthorizationCode(
                code="mcp_code_x",
                scopes=["resources:read"],
                expires_at=9999999999.0,
                client_id="c",
                code_challenge="ch",
                redirect_uri=AnyUrl(REDIRECT_URI_A),
                redirect_uri_provided_explicitly=True,
            )  # type: ignore[call-arg]

        client = OAuthClientInformationFull(client_id="c", redirect_uris=[AnyUrl(REDIRECT_URI_A)])
        now = datetime.now(timezone.utc)
        owner_less = _CodeSnapshot(
            id=uuid.uuid4(),
            user_id=None,
            client_id="c",
            scopes=["resources:read"],
            expires_at=now + timedelta(minutes=5),
        )
        # The one decision point for "may this code be exchanged?" — a pure
        # function, so this asserts the refusal itself, not a side effect of it.
        assert _refuse_code(client, owner_less, claimed_user_id=None, now=now) is not None
        assert _refuse_code(client, None, claimed_user_id=str(USER_A), now=now) is not None
        # And the positive control: an intact snapshot for A IS exchangeable, so the
        # assertions above are not passing for an unrelated reason.
        intact = _CodeSnapshot(
            id=uuid.uuid4(),
            user_id=str(USER_A),
            client_id="c",
            scopes=["resources:read"],
            expires_at=now + timedelta(minutes=5),
        )
        assert _refuse_code(client, intact, claimed_user_id=str(USER_A), now=now) is None
        assert _refuse_code(client, intact, claimed_user_id=str(USER_B), now=now) is not None
        assert await _access_token_rows(factory) == []


# ═══════════════════════════ (4) PKCE mismatch ═══════════════════════════════


class TestPKCE:
    async def test_wrong_code_verifier_is_refused_and_mints_nothing(self, wired) -> None:
        factory, _scope = wired
        async with alpha_client(cookie_user=USER_A) as client:
            registration = await _register_client(client)
            code, _verifier = await _authorize_as(client, client_id=registration["client_id"])
            resp = await _exchange(
                client,
                registration=registration,
                code=code,
                verifier=secrets.token_urlsafe(48),  # a DIFFERENT verifier
            )

        assert resp.status_code == 400, resp.text
        assert resp.json()["error"] == "invalid_grant"
        assert await _access_token_rows(factory) == []

    async def test_authorize_without_pkce_is_refused(self, wired) -> None:
        factory, _scope = wired
        async with alpha_client(cookie_user=USER_A) as client:
            registration = await _register_client(client)
            resp = await client.get(
                mcp_oauth.AUTHORIZE_PATH,
                params={
                    "client_id": registration["client_id"],
                    "redirect_uri": REDIRECT_URI_A,
                    "response_type": "code",
                },
                headers={"Accept": "text/html"},
            )
        assert resp.status_code == 400
        assert resp.json()["error"] == "invalid_request"
        assert await _rows(factory, MCPOAuthCode) == []


# ══════════════════════════ (5) replay revocation ════════════════════════════


class TestReplayRevokesTheFirstToken:
    async def test_second_exchange_is_refused_and_the_first_token_is_revoked(self, wired) -> None:
        """OAuth 2.1 §4.1.2.5. The revocation must be COMMITTED — the bug this
        guards against is a rollback, so the assertion re-reads the row from the
        store rather than trusting the log line."""
        factory, _scope = wired
        async with alpha_client(cookie_user=USER_A) as client:
            registration = await _register_client(client)
            code, verifier = await _authorize_as(client, client_id=registration["client_id"])
            first = await _exchange(client, registration=registration, code=code, verifier=verifier)
            assert first.status_code == 200, first.text
            replay = await _exchange(
                client, registration=registration, code=code, verifier=verifier
            )

        assert replay.status_code == 400, replay.text
        assert replay.json()["error"] == "invalid_grant"

        rows = await _access_token_rows(factory)
        assert len(rows) == 1, "the replay must not mint a second token"
        assert rows[0].revoked_at is not None, (
            "the token the FIRST exchange minted must be revoked on replay "
            "(OAuth 2.1 §4.1.2.5) — and the revocation must be committed"
        )
        refresh_rows = await _rows(factory, MCPOAuthRefreshToken)
        assert len(refresh_rows) == 1
        assert refresh_rows[0].revoked_at is not None

        # And the revoked token is genuinely dead at the resource server: unit 1's
        # verifier refuses a revoked row, so the replay cost the attacker the
        # credential rather than gaining them one.
        access_token = first.json()["access_token"]
        with pytest.raises(Exception):  # noqa: B017 — any failure is correct
            async with rs_session(access_token) as session:
                await session.read_resource(AnyUrl(PROFILE_URI))


# ═══════════════════════════ (6) refresh grant ═══════════════════════════════


class TestRefreshGrant:
    async def test_refresh_mints_for_the_same_user_only_and_rotates(self, wired) -> None:
        factory, _scope = wired
        async with alpha_client(cookie_user=USER_A) as client:
            registration = await _register_client(client)
            code, verifier = await _authorize_as(client, client_id=registration["client_id"])
            first = await _exchange(client, registration=registration, code=code, verifier=verifier)
            assert first.status_code == 200, first.text
            refresh_token = first.json()["refresh_token"]

            data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": registration["client_id"],
            }
            if registration.get("client_secret"):
                data["client_secret"] = registration["client_secret"]
            refreshed = await client.post(mcp_oauth.TOKEN_PATH, data=data)
            # Single-use: the same refresh token a second time is refused.
            reused = await client.post(mcp_oauth.TOKEN_PATH, data=data)

        assert refreshed.status_code == 200, refreshed.text
        new_access = refreshed.json()["access_token"]
        assert new_access != first.json()["access_token"]
        assert refreshed.json()["refresh_token"] != refresh_token, "refresh must rotate"
        assert reused.status_code == 400, reused.text

        # Both access tokens belong to A and only A.
        rows = await _access_token_rows(factory)
        assert {str(r.user_id) for r in rows} == {str(USER_A)}
        new_row = next(r for r in rows if r.token_hash == hash_credential(new_access))
        assert str(new_row.user_id) == str(USER_A)
        assert str(new_row.user_id) != str(USER_B)


# ═════════════════════════ (7) discovery end to end ══════════════════════════


class TestDiscoveryResolvesEndToEnd:
    async def test_rs_metadata_names_the_issuer_and_the_issuer_serves_its_metadata(
        self, wired
    ) -> None:
        """A client that knows only the MCP URL must be able to reach the AS: RS
        protected-resource metadata → issuer → AS metadata → the endpoints actually
        mounted. Each hop is fetched, not assumed."""
        mcp = build_mcp_server()
        inner = mcp.streamable_http_app()
        rs_app = MCPPathGate(inner, mcp_path=mcp.settings.streamable_http_path)

        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=rs_app),
            base_url=LOCAL_BASE_URL,
            timeout=httpx.Timeout(30.0),
        ) as rs:
            rs_meta_resp = await rs.get("/.well-known/oauth-protected-resource")

        assert rs_meta_resp.status_code == 200, (
            "RFC 9728 discovery must be reachable — MCPPathGate denied this path "
            "before unit 4, which made the issuer undiscoverable"
        )
        rs_meta = rs_meta_resp.json()
        assert rs_meta["resource"].rstrip("/") == "https://mcp.pipermorgan.ai"
        issuers = rs_meta["authorization_servers"]
        assert issuers == ["https://alpha.pipermorgan.ai/mcp/oauth"], issuers

        issuer = issuers[0].rstrip("/")
        parsed = urlsplit(issuer)
        # RFC 8414 §3.1 well-known form for an issuer WITH a path component.
        well_known = f"/.well-known/oauth-authorization-server{parsed.path}"
        async with alpha_client() as alpha:
            as_meta_resp = await alpha.get(well_known)
            # …and the path-appended form some clients try first.
            suffixed_resp = await alpha.get(f"{parsed.path}/.well-known/oauth-authorization-server")

        assert as_meta_resp.status_code == 200, well_known
        assert suffixed_resp.status_code == 200
        as_meta = as_meta_resp.json()
        assert suffixed_resp.json() == as_meta, "both locations must serve the SAME metadata"

        # RFC 8414 §3.3: a client validates that `issuer` matches what it asked for.
        assert as_meta["issuer"].rstrip("/") == issuer
        assert as_meta["code_challenge_methods_supported"] == ["S256"]
        assert as_meta["response_types_supported"] == ["code"]
        assert set(as_meta["grant_types_supported"]) == {"authorization_code", "refresh_token"}
        assert as_meta["scopes_supported"] == ["resources:read"]

        # The advertised endpoints are the paths actually mounted — the property
        # that makes a path-prefixed issuer work at all.
        for advertised, mounted in (
            (as_meta["authorization_endpoint"], mcp_oauth.AUTHORIZE_PATH),
            (as_meta["token_endpoint"], mcp_oauth.TOKEN_PATH),
            (as_meta["registration_endpoint"], mcp_oauth.REGISTER_PATH),
            (as_meta["revocation_endpoint"], mcp_oauth.REVOKE_PATH),
        ):
            assert urlsplit(advertised).path == mounted, f"{advertised} != {mounted}"

        from web.app import app as alpha_app

        live_paths = {getattr(r, "path", None) for r in alpha_app.router.routes}
        for path in mcp_oauth.ALL_AS_PATHS:
            assert path in live_paths, f"{path} advertised/expected but not mounted"


# ═════════════════ (8) the RS's existing behavior is unchanged ════════════════


class TestResourceServerUnchanged:
    async def test_unknown_bearer_still_reads_nothing(self, wired) -> None:
        """Unit 4 added a second way to OBTAIN a token; it must not have added a way
        to skip having one. (Unit 1's full refusal matrix — revoked, expired,
        two-caller isolation — stays in test_identity_unit1.py; this is the
        did-unit-4-break-it check, not a re-proof.)"""
        with pytest.raises(Exception):  # noqa: B017 — any failure is correct
            async with rs_session("mcp_never_minted_by_anyone") as session:
                await session.read_resource(AnyUrl(PROFILE_URI))

    async def test_mcp_path_gate_still_denies_an_ungated_path(self, wired) -> None:
        """Opening the RFC 9728 metadata path must not have turned the gate into
        allow-by-default."""
        mcp = build_mcp_server()
        inner = mcp.streamable_http_app()
        rs_app = MCPPathGate(inner, mcp_path=mcp.settings.streamable_http_path)
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=rs_app),
            base_url=LOCAL_BASE_URL,
            timeout=httpx.Timeout(30.0),
        ) as rs:
            resp = await rs.get("/some/route/nobody/gated")
        assert resp.status_code == 401
        assert resp.json() == {"error": "identity_required"}


# ═════════════════ consent-CSRF and Deny (same boundary) ═════════════════════


class TestConsentIntegrity:
    async def test_forged_approve_without_a_valid_consent_token_mints_nothing(self, wired) -> None:
        """The consent-CSRF case: an approve POST that did not come from a consent
        page this server rendered FOR THIS USER is refused, so a cross-site forged
        POST cannot mint a code against a victim's live session."""
        factory, _scope = wired
        _v, challenge = _pkce()
        async with alpha_client(cookie_user=USER_A) as client:
            registration = await _register_client(client)
            forged = await _consent(
                client,
                client_id=registration["client_id"],
                challenge=challenge,
                redirect_uri=REDIRECT_URI_A,
                state="st",
                consent_token="1799999999.deadbeef",
            )
        assert forged.status_code == 400, forged.text
        assert await _rows(factory, MCPOAuthCode) == []

    async def test_a_consent_token_issued_to_one_user_does_not_work_for_another(
        self, wired
    ) -> None:
        """The token is bound to the user who saw the page: B cannot complete a
        consent that was rendered for A."""
        factory, _scope = wired
        async with alpha_client(cookie_user=USER_A) as client_a:
            registration = await _register_client(client_a)
            _v, challenge = _pkce()
            page = await _get_consent_page(
                client_a,
                client_id=registration["client_id"],
                challenge=challenge,
                redirect_uri=REDIRECT_URI_A,
                state="st",
            )
            token = _CONSENT_TOKEN_RE.search(page.text).group(1)  # type: ignore[union-attr]

        async with alpha_client(cookie_user=USER_B) as client_b:
            resp = await _consent(
                client_b,
                client_id=registration["client_id"],
                challenge=challenge,
                redirect_uri=REDIRECT_URI_A,
                state="st",
                consent_token=token,
            )

        assert resp.status_code == 400, resp.text
        assert await _rows(factory, MCPOAuthCode) == []

    async def test_deny_issues_no_code(self, wired) -> None:
        factory, _scope = wired
        async with alpha_client(cookie_user=USER_A) as client:
            registration = await _register_client(client)
            _v, challenge = _pkce()
            page = await _get_consent_page(
                client,
                client_id=registration["client_id"],
                challenge=challenge,
                redirect_uri=REDIRECT_URI_A,
                state="st-deny",
            )
            token = _CONSENT_TOKEN_RE.search(page.text).group(1)  # type: ignore[union-attr]
            resp = await _consent(
                client,
                client_id=registration["client_id"],
                challenge=challenge,
                redirect_uri=REDIRECT_URI_A,
                state="st-deny",
                consent_token=token,
                decision="deny",
            )

        assert resp.status_code == 302
        query = parse_qs(urlsplit(resp.headers["location"]).query)
        assert query["error"] == ["access_denied"]
        assert query["state"] == ["st-deny"]
        assert "code" not in query
        assert await _rows(factory, MCPOAuthCode) == []

    async def test_consent_page_names_the_three_resources_and_the_signed_in_user(
        self, wired
    ) -> None:
        """The consent screen must say what is being granted — the three resource
        URIs and whose account — or "informed consent" is a word we used."""
        async with alpha_client(cookie_user=USER_A) as client:
            registration = await _register_client(client, name="ChatGPT")
            _v, challenge = _pkce()
            page = await _get_consent_page(
                client,
                client_id=registration["client_id"],
                challenge=challenge,
                redirect_uri=REDIRECT_URI_A,
                state="st",
            )
        assert page.status_code == 200
        body = page.text
        assert "ChatGPT" in body
        assert "read-only" in body
        for uri in (
            "piper://me/profile",
            "piper://me/colleague-model",
            "piper://me/github/issues",
        ):
            assert uri in body, f"the consent page must name {uri}"
        assert str(USER_A) in body


# ═══════════════ the exempt-list boundary this unit depends on ═══════════════


class TestAuthMiddlewareExemptionShape:
    """The "no identity, no code" property is enforced partly by /authorize NOT
    being auth-exempt. That is a one-line edit away from being undone silently, so
    it is pinned here rather than trusted to a comment."""

    async def test_authorize_is_not_auth_exempt(self) -> None:
        from services.auth.auth_middleware import DEFAULT_EXCLUDE_PATHS

        for exempt in DEFAULT_EXCLUDE_PATHS:
            assert not mcp_oauth.AUTHORIZE_PATH.startswith(exempt), (
                f"/mcp/oauth/authorize is auth-exempt via '{exempt}' — a code could "
                f"then be issued with no authenticated identity"
            )

    async def test_machine_to_machine_paths_are_exempt(self) -> None:
        from services.auth.auth_middleware import DEFAULT_EXCLUDE_PATHS

        for path in mcp_oauth.MACHINE_TO_MACHINE_PATHS:
            assert any(
                path.startswith(exempt) for exempt in DEFAULT_EXCLUDE_PATHS
            ), f"{path} is machine-to-machine and must be auth-exempt, or discovery/exchange 401s"

    async def test_writable_exempt_paths_are_justified(self) -> None:
        """#1308: the exempt list is a security boundary; a writable exempt route
        needs a stated reason."""
        from services.auth.auth_middleware import AUTH_EXEMPT_JUSTIFIED

        for path in (mcp_oauth.TOKEN_PATH, mcp_oauth.REGISTER_PATH, mcp_oauth.REVOKE_PATH):
            assert path in AUTH_EXEMPT_JUSTIFIED, path
