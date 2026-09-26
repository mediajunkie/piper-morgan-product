"""Phase C unit 1 — fail-closed caller identity for the MCP server (#1462).

Pins Arch's condition 1 ("no identity, no read; never default to
anonymous") the way the build plan's unit 1 asked for it, proven, not
asserted:

(a) monkeypatched verifier that always returns None -> `initialize` gets 401
(b) a real, valid bearer token -> `initialize` gets 200
(c) a revoked token -> 401
(d) an expired token -> 401
(e) two-caller isolation: two synthetic users A and B, each with their own
    token, and a resource stub that returns `current_user_id()`. A's token
    reads A, B's reads B, A's token can never produce B's id, and a garbage
    token reads nothing.

LAYER (m-43): (a)-(d) go through the real ASGI app
(`services.mcp.server.app.build_asgi_app()`) via Starlette's TestClient —
the same protocol surface uvicorn serves, exercising FastMCP's own
`RequireAuthMiddleware` (wired by `build_mcp_server()`'s `auth=`/
`token_verifier=`), not a call into `MCPTokenVerifier` in isolation. (e)
goes one layer further: a real MCP client (`mcp.client.streamable_http` +
`ClientSession`) round-tripping `initialize` + `resources/read` over an
in-process ASGI transport, so the isolation proof is at the same layer a
real tester's client operates at, not a direct call into the resource
function. A handful of narrower unit-level tests on `MCPTokenVerifier`
itself are included too (not-found/revoked/expired/valid, `last_used_at`
update) since they pin the exact refusal conditions the ASGI-layer tests
only observe from the outside as "some 401".

DENOMINATOR: unit 1's identity boundary only. No resources are registered
by `services.mcp.server.app` yet (unit 2) — the isolation test (e) builds
its OWN minimal FastMCP instance with one stub resource for exactly this
purpose, per the build plan's own instruction ("a resource stub registered
for the test that returns current_user_id()"), not a claim about unit 2's
real resources.

DB fixture: in-memory SQLite (the #1035/#1238 pattern used elsewhere in this
suite — see test_document_model_1238.py), not the real-Postgres `db_session`
conftest fixture other DB-touching tests use, so this file has no Docker/
Postgres dependency. `StaticPool` is load-bearing: an in-memory SQLite
database is per-CONNECTION by default, and both the verifier and this
file's own seeding helper open independent sessions against the same
engine — without `StaticPool` they would each see a different, empty
database. Engine disposal happens in a fixture teardown (not inline at the
end of each test body) so a mid-test assertion failure still disposes the
engine — skipping disposal leaves aiosqlite's non-daemon worker thread
running, which blocks the whole test process from exiting (found live
while writing this file: a failing assertion made the run LOOK hung for
tens of seconds, when the actual failure was instant — the hang was
process-shutdown waiting on that thread, not the test itself).

HOST HEADER NOTE: FastMCP auto-enables DNS-rebinding protection for the
default `host="127.0.0.1"` (`allowed_hosts=["127.0.0.1:*", "localhost:*",
"[::1]:*"]`), enforced INSIDE the streamable-HTTP session manager — i.e.
AFTER `RequireAuthMiddleware` already ran. An unauthenticated/invalid-bearer
request never reaches that check (401 fires first), but a genuinely
authenticated request does, so any test that expects to get PAST auth must
address requests to a host:port matching that allowlist (`localhost:8080`
here) — Starlette TestClient's default `http://testserver` does not match
and would 421 a would-be-200 request.
"""

from __future__ import annotations

import hashlib
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

import httpx  # noqa: E402
import sse_starlette.sse as _sse_starlette_sse  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from mcp.client.session import ClientSession  # noqa: E402
from mcp.client.streamable_http import streamable_http_client  # noqa: E402
from mcp.server.auth.settings import AuthSettings  # noqa: E402
from mcp.server.fastmcp import FastMCP  # noqa: E402
from pydantic import AnyUrl  # noqa: E402
from sqlalchemy import select  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool  # noqa: E402

from services.database.models import MCPAccessToken  # noqa: E402
from services.database.session_factory import AsyncSessionFactory  # noqa: E402
from services.mcp.server.app import build_asgi_app  # noqa: E402
from services.mcp.server.identity import (  # noqa: E402
    RESOURCE_READ_SCOPE,
    MCPTokenVerifier,
    current_user_id,
)

pytestmark = pytest.mark.asyncio


@pytest.fixture(autouse=True)
def _reset_sse_starlette_loop_singleton():
    """``sse_starlette.sse.AppStatus.should_exit_event`` is a process-global
    singleton, lazily created and bound to whichever asyncio loop is running
    the first time an SSE response starts. pytest-asyncio gives each test
    function its own event loop by default; any test here that reaches a
    real `initialize` response goes through ``sse_starlette`` (FastMCP's
    default is `json_response=False`), so a LATER test in this file that
    also does so would bind to a stale singleton from an earlier test's
    already-closed loop and fail with "bound to a different event loop" —
    found live running this file's tests together after every test passed
    individually. Resetting before each test gives every test a fresh
    singleton bound to its own loop."""
    _sse_starlette_sse.AppStatus.should_exit = False
    _sse_starlette_sse.AppStatus.should_exit_event = None
    yield


MCP_PATH = "/mcp"

# Matches FastMCP's auto-enabled DNS-rebinding allowlist for host="127.0.0.1"
# (see module docstring's HOST HEADER NOTE).
LOCAL_BASE_URL = "http://localhost:8080"

USER_A = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
USER_B = uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")


def _hash(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _initialize_payload() -> dict:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "0.0.1"},
        },
    }


def _accept_headers() -> dict:
    return {"Accept": "application/json, text/event-stream"}


@pytest_asyncio.fixture
async def token_store():
    """A fresh in-memory-SQLite (engine, sessionmaker, session_scope) triple
    holding only ``mcp_access_tokens``, disposed on teardown regardless of
    test outcome (see module docstring)."""
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
        await conn.run_sync(lambda c: MCPAccessToken.__table__.create(c, checkfirst=True))

    yield factory, _scope

    await engine.dispose()


async def _seed_token(
    factory,
    *,
    user_id: uuid.UUID,
    raw_token: str,
    label: str = "test",
    expires_at: datetime | None = None,
    revoked_at: datetime | None = None,
) -> None:
    async with factory() as session:
        session.add(
            MCPAccessToken(
                id=uuid.uuid4(),
                user_id=user_id,
                token_hash=_hash(raw_token),
                label=label,
                expires_at=expires_at,
                revoked_at=revoked_at,
            )
        )
        await session.commit()


# ---- (a)-(d): ASGI layer, via services.mcp.server.app.build_asgi_app() ----


class TestASGILayerBearerAuth:
    async def test_unresolvable_identity_is_refused_not_served(self, monkeypatch) -> None:
        """(a) A verifier that NEVER resolves an identity (the monkeypatch
        the build plan asked for) -> initialize is refused, never served
        anonymously. Equivalent in effect to "no such hash" for every
        possible token — there is no code path that falls through to a
        default identity."""

        async def _always_refuse(self, token: str):
            return None

        monkeypatch.setattr(MCPTokenVerifier, "verify_token", _always_refuse)

        app = build_asgi_app()
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            resp = client.post(
                MCP_PATH,
                json=_initialize_payload(),
                headers={**_accept_headers(), "Authorization": "Bearer mcp_anything_at_all"},
            )

        assert resp.status_code == 401

    async def test_valid_bearer_gets_200_on_initialize(self, monkeypatch, token_store) -> None:
        """(b) A real, valid, unexpired, unrevoked token resolves and the
        `initialize` handshake succeeds."""
        factory, scope = token_store
        raw_token = "mcp_validForInitialize"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_token)
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)

        app = build_asgi_app()
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            resp = client.post(
                MCP_PATH,
                json=_initialize_payload(),
                headers={**_accept_headers(), "Authorization": f"Bearer {raw_token}"},
            )

        assert resp.status_code == 200

    async def test_revoked_bearer_is_refused(self, monkeypatch, token_store) -> None:
        """(c) A token that exists but has been revoked is refused
        identically to an unresolvable one — never a distinguishable
        response that would let a caller learn WHY."""
        factory, scope = token_store
        raw_token = "mcp_revokedForInitialize"
        await _seed_token(
            factory,
            user_id=USER_A,
            raw_token=raw_token,
            revoked_at=datetime.now(timezone.utc),
        )
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)

        app = build_asgi_app()
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            resp = client.post(
                MCP_PATH,
                json=_initialize_payload(),
                headers={**_accept_headers(), "Authorization": f"Bearer {raw_token}"},
            )

        assert resp.status_code == 401

    async def test_expired_bearer_is_refused(self, monkeypatch, token_store) -> None:
        """(d) A token past its expires_at is refused, same as revoked/unknown."""
        factory, scope = token_store
        raw_token = "mcp_expiredForInitialize"
        await _seed_token(
            factory,
            user_id=USER_A,
            raw_token=raw_token,
            expires_at=datetime.now(timezone.utc) - timedelta(days=1),
        )
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)

        app = build_asgi_app()
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            resp = client.post(
                MCP_PATH,
                json=_initialize_payload(),
                headers={**_accept_headers(), "Authorization": f"Bearer {raw_token}"},
            )

        assert resp.status_code == 401


# ---- MCPTokenVerifier unit-level: pins the exact refusal conditions the
#      ASGI-layer tests above only observe from the outside as "some 401" ----


class TestMCPTokenVerifierDirect:
    async def test_unknown_token_hash_refused(self, token_store) -> None:
        _factory, scope = token_store
        verifier = MCPTokenVerifier(session_scope=scope)

        result = await verifier.verify_token("mcp_never_minted")

        assert result is None

    async def test_valid_token_resolves_to_the_real_owner(self, token_store) -> None:
        factory, scope = token_store
        raw_token = "mcp_directValid"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_token)
        verifier = MCPTokenVerifier(session_scope=scope)

        result = await verifier.verify_token(raw_token)

        assert result is not None
        assert result.client_id == str(USER_A)
        assert result.scopes == [RESOURCE_READ_SCOPE]

    async def test_revoked_token_refused(self, token_store) -> None:
        factory, scope = token_store
        raw_token = "mcp_directRevoked"
        await _seed_token(
            factory, user_id=USER_A, raw_token=raw_token, revoked_at=datetime.now(timezone.utc)
        )
        verifier = MCPTokenVerifier(session_scope=scope)

        result = await verifier.verify_token(raw_token)

        assert result is None

    async def test_expired_token_refused(self, token_store) -> None:
        factory, scope = token_store
        raw_token = "mcp_directExpired"
        await _seed_token(
            factory,
            user_id=USER_A,
            raw_token=raw_token,
            expires_at=datetime.now(timezone.utc) - timedelta(days=1),
        )
        verifier = MCPTokenVerifier(session_scope=scope)

        result = await verifier.verify_token(raw_token)

        assert result is None

    async def test_valid_verification_updates_last_used_at(self, token_store) -> None:
        factory, scope = token_store
        raw_token = "mcp_directTouch"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_token)
        verifier = MCPTokenVerifier(session_scope=scope)

        assert await verifier.verify_token(raw_token) is not None

        async with factory() as session:
            row = (await session.execute(select(MCPAccessToken))).scalar_one()
            assert row.last_used_at is not None


# ---- (e): two-caller isolation, via a real MCP client round trip ----


def _build_isolation_test_app(session_scope) -> FastMCP:
    """A minimal FastMCP instance with ONE stub resource that echoes
    `current_user_id()` — exactly what the build plan's unit 1 asked for
    ("a resource stub registered for the test that returns
    current_user_id()"). Not a claim about unit 2's real resources, which
    don't exist yet. `host="127.0.0.1"` (the FastMCP default) matches
    `LOCAL_BASE_URL`'s DNS-rebinding allowlist — see module docstring."""
    mcp = FastMCP(
        name="mcp-unit1-isolation-test",
        auth=AuthSettings(
            issuer_url="https://issuer.test.invalid",
            resource_server_url="https://resource.test.invalid",
            required_scopes=[RESOURCE_READ_SCOPE],
        ),
        token_verifier=MCPTokenVerifier(session_scope=session_scope),
    )

    @mcp.resource("piper://test/whoami")
    def whoami() -> str:
        return current_user_id()

    return mcp


async def _read_whoami_over_real_mcp_client(asgi_app, raw_token: str) -> str:
    """A real MCP client (`mcp.client.streamable_http` + `ClientSession`)
    round-tripping `initialize` then `resources/read` over an in-process
    ASGI transport — the same client-side protocol surface a real tester's
    MCP client speaks, not a direct call into the resource function or the
    verifier."""
    headers = {"Authorization": f"Bearer {raw_token}"}
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=asgi_app),
        base_url=LOCAL_BASE_URL,
        headers=headers,
        timeout=httpx.Timeout(30.0),
    ) as http_client:
        async with streamable_http_client(
            f"{LOCAL_BASE_URL}{MCP_PATH}", http_client=http_client
        ) as (read_stream, write_stream, _get_session_id):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                result = await session.read_resource(AnyUrl("piper://test/whoami"))
                return result.contents[0].text  # type: ignore[union-attr]


class TestTwoCallerIsolation:
    """Arch's #1462 condition 1, "tested with two synthetic users even
    though only one real tester exists" (build plan, unit 1)."""

    async def test_each_callers_token_resolves_to_only_that_caller(self, token_store) -> None:
        factory, scope = token_store
        raw_a, raw_b = "mcp_callerAToken", "mcp_callerBToken"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_a, label="caller A")
        await _seed_token(factory, user_id=USER_B, raw_token=raw_b, label="caller B")

        mcp = _build_isolation_test_app(scope)
        app = mcp.streamable_http_app()

        # streamablehttp_client only speaks HTTP over the ASGI transport — it
        # never sends the ASGI "lifespan" protocol messages that would
        # normally start the session manager's task group. Entering
        # session_manager.run() directly is the same thing
        # `streamable_http_app()`'s own `lifespan=` callback does.
        async with mcp.session_manager.run():
            whoami_a = await _read_whoami_over_real_mcp_client(app, raw_a)
            whoami_b = await _read_whoami_over_real_mcp_client(app, raw_b)

        assert whoami_a == str(USER_A)
        assert whoami_b == str(USER_B)
        # The load-bearing assertion: A's token can NEVER produce B's identity,
        # and vice versa.
        assert whoami_a != str(USER_B)
        assert whoami_b != str(USER_A)

    async def test_garbage_token_reads_nothing(self, token_store) -> None:
        _factory, scope = token_store
        mcp = _build_isolation_test_app(scope)
        app = mcp.streamable_http_app()

        async with mcp.session_manager.run():
            with pytest.raises(
                Exception  # noqa: B017 — any failure is correct; there is no success shape
            ):
                await _read_whoami_over_real_mcp_client(app, "mcp_this_was_never_minted")


@pytest.mark.asyncio
async def test_backend_fault_refuses_with_none_not_exception(monkeypatch):
    """A store that cannot answer is a refusal, never an exception (the live
    09-26 probe returned 500 on a garbage bearer when the app had no DATABASE_URL)."""
    from services.mcp.server import identity as mod

    verifier = mod.MCPTokenVerifier()

    async def _boom(self, token):  # noqa: ARG001
        raise PermissionError("[Errno 13] Permission denied: '/root/.postgresql/postgresql.key'")

    monkeypatch.setattr(mod.MCPTokenVerifier, "_verify_token", _boom)
    assert await verifier.verify_token("mcp_XXXX0000XXXX0000") is None
