"""#1458 — per-caller-identity rate limiting on ``/mcp`` (services/mcp/server/rate_limit.py).

No rate limiter existed anywhere under ``services/mcp/server/`` before this file (grep
denominator: ``grep -rliI "rate.?limit\\|throttle\\|429" services/ web/`` returned the
usual web-app surfaces — ``web/middleware/usage_cap_middleware.py`` et al. — but nothing
under ``services/mcp/server/``). This pins the mechanism added to close that gap:
:class:`~services.mcp.server.rate_limit.MCPRateLimitMiddleware`, wired into
``build_asgi_app()`` between :class:`~services.mcp.server.app.MCPPathGate` and FastMCP's
own auth+routing stack.

LAYER (m-43): every enforcement test goes through the real ASGI app
(``services.mcp.server.app.build_asgi_app()``) via Starlette's ``TestClient`` — the same
protocol surface uvicorn serves — exercising the real middleware layering, not a direct
call into ``MCPRateLimitMiddleware`` in isolation. Pure-function tests (token/env
parsing) are unit-level on purpose; they don't need the ASGI stack.

DENOMINATOR: the rate limiter only. Identity correctness (401s, two-caller identity
isolation) is ``test_identity_unit1.py``'s scope; this file assumes a valid bearer
resolves correctly (already pinned there) and tests what happens ONCE identity is
resolved, under repeated requests.

Redis is faked per-test via the same idiom ``test_usage_cap_middleware_1370.py``
established: patching ``services.cache.redis_factory.RedisFactory.redis_scope``, which
is the SAME class object ``rate_limit.py`` imports and calls — patching it at its
definition module affects every caller. ``tests/conftest.py``'s autouse
``mock_usage_cap_redis`` fixture already patches this target with a permissive
always-succeeds fake for every test that doesn't override it (which is why the EXISTING
MCP test files, none of which know about rate limiting, keep passing unaffected by this
change) — the fakes defined below take precedence for the duration of each test that
asks for them, the same nesting ``test_usage_cap_middleware_1370.py`` relies on.
"""

from __future__ import annotations

import hashlib
import uuid
from contextlib import asynccontextmanager
from unittest.mock import patch

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

import sse_starlette.sse as _sse_starlette_sse  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool  # noqa: E402

from services.database.models import MCPAccessToken  # noqa: E402
from services.database.session_factory import AsyncSessionFactory  # noqa: E402
from services.mcp.server.app import build_asgi_app  # noqa: E402
from services.mcp.server.rate_limit import (  # noqa: E402
    DEFAULT_LIMIT_PER_MINUTE,
    RATE_KEY_PREFIX,
    _bearer_token,
    _fail_closed,
    _limit_per_minute,
)

MCP_PATH = "/mcp"
LOCAL_BASE_URL = "http://localhost:8080"

USER_A = uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
USER_B = uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")


@pytest.fixture(autouse=True)
def _reset_sse_starlette_loop_singleton():
    """Same fresh-per-test singleton reset as test_identity_unit1.py — see that
    file's module docstring for why this is load-bearing across several tests
    in one file that each reach a real `initialize` response."""
    _sse_starlette_sse.AppStatus.should_exit = False
    _sse_starlette_sse.AppStatus.should_exit_event = None
    yield


def _hash(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _initialize_payload(req_id: int = 1) -> dict:
    return {
        "jsonrpc": "2.0",
        "id": req_id,
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
    """Same in-memory-SQLite token store as test_identity_unit1.py."""
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


async def _seed_token(factory, *, user_id: uuid.UUID, raw_token: str, label: str = "test") -> None:
    async with factory() as session:
        session.add(
            MCPAccessToken(
                id=uuid.uuid4(), user_id=user_id, token_hash=_hash(raw_token), label=label
            )
        )
        await session.commit()


class _FakeFixedWindowRedis:
    """Minimal in-memory stand-in for exactly what MCPRateLimitMiddleware
    uses: INCR (fixed-window counter), EXPIRE, TTL. Deliberately simpler
    than test_usage_cap_middleware_1370.py's ``_FakeRedis`` (no ZSET
    commands — this limiter has no concurrency-gauge mechanism)."""

    def __init__(self) -> None:
        self.counters: dict[str, int] = {}
        self.ttls: dict[str, int] = {}
        self.closed = False

    async def incr(self, key):
        self.counters[key] = self.counters.get(key, 0) + 1
        return self.counters[key]

    async def expire(self, key, seconds):
        self.ttls[key] = seconds
        return True

    async def ttl(self, key):
        return self.ttls.get(key, -1)

    async def close(self):
        self.closed = True


class _BoomRedis:
    """Simulates a Redis backend that cannot answer at all (connection
    refused/timeout) — every command raises."""

    async def incr(self, key):
        raise ConnectionError("redis unreachable (simulated)")

    async def close(self):
        pass


@pytest.fixture
def fake_redis():
    return _FakeFixedWindowRedis()


@pytest.fixture
def patched_redis(fake_redis):
    @asynccontextmanager
    async def _scope():
        yield fake_redis

    with patch(
        "services.cache.redis_factory.RedisFactory.redis_scope",
        side_effect=_scope,
    ):
        yield fake_redis


@pytest.fixture
def broken_redis():
    @asynccontextmanager
    async def _scope():
        yield _BoomRedis()

    with patch(
        "services.cache.redis_factory.RedisFactory.redis_scope",
        side_effect=_scope,
    ):
        yield


# ---- ASGI-layer enforcement, via the real build_asgi_app() ----


class TestUnresolvableTokenNeverRateLimited:
    """Not our refusal to make — see rate_limit.py's module docstring. An
    unresolvable bearer must reach the SAME 401 the real auth stack always
    produced, and must never create a rate-limit bucket (which would let a
    flood of garbage tokens pollute/exhaust Redis keyspace for free)."""

    async def test_missing_authorization_header_still_401_untouched(self, patched_redis) -> None:
        app = build_asgi_app()
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            resp = client.post(MCP_PATH, json=_initialize_payload(), headers=_accept_headers())

        assert resp.status_code == 401
        assert patched_redis.counters == {}

    async def test_garbage_bearer_token_still_401_untouched(
        self, patched_redis, token_store
    ) -> None:
        _factory, scope = token_store
        with patch.object(AsyncSessionFactory, "session_scope", scope):
            app = build_asgi_app()
            with TestClient(app, base_url=LOCAL_BASE_URL) as client:
                resp = client.post(
                    MCP_PATH,
                    json=_initialize_payload(),
                    headers={**_accept_headers(), "Authorization": "Bearer mcp_never_minted"},
                )

        assert resp.status_code == 401
        assert patched_redis.counters == {}


class TestValidIdentityRateLimited:
    async def test_single_request_under_limit_succeeds_and_increments(
        self, monkeypatch, patched_redis, token_store
    ) -> None:
        factory, scope = token_store
        raw_token = "mcp_rateLimitUnderToken"
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
        assert patched_redis.counters == {f"{RATE_KEY_PREFIX}{USER_A}": 1}

    async def test_exceeding_limit_returns_429_with_retry_after(
        self, monkeypatch, patched_redis, token_store
    ) -> None:
        """The load-bearing proof: N+1 requests for the SAME identity within
        the window, limit set to N via env -> the first N succeed, the next
        one is refused with a real HTTP 429 and a Retry-After header, never
        an MCP-protocol-level error (see rate_limit.py's docstring for why
        that distinction is the whole point of this layer)."""
        factory, scope = token_store
        raw_token = "mcp_rateLimitExceedToken"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_token)
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)
        monkeypatch.setenv("MCP_RATE_LIMIT_PER_MINUTE", "2")

        app = build_asgi_app()
        headers = {**_accept_headers(), "Authorization": f"Bearer {raw_token}"}
        statuses = []
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            for i in range(3):
                resp = client.post(MCP_PATH, json=_initialize_payload(i), headers=headers)
                statuses.append(resp)

        assert [r.status_code for r in statuses] == [200, 200, 429]
        third = statuses[2]
        assert "Retry-After" in third.headers
        body = third.json()
        assert body["error"] == "rate_limited"
        assert "retry_after_seconds" in body

    async def test_two_callers_have_independent_limits(
        self, monkeypatch, patched_redis, token_store
    ) -> None:
        """Caller A exhausting its own limit must never limit caller B — the
        explicit AC in the dispatch prompt (\"caller A hitting the limit does
        not limit caller B\"). Proves the bucket is keyed per-identity, not
        shared/process-wide."""
        factory, scope = token_store
        raw_a, raw_b = "mcp_rateLimitCallerA", "mcp_rateLimitCallerB"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_a, label="A")
        await _seed_token(factory, user_id=USER_B, raw_token=raw_b, label="B")
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)
        monkeypatch.setenv("MCP_RATE_LIMIT_PER_MINUTE", "1")

        app = build_asgi_app()
        headers_a = {**_accept_headers(), "Authorization": f"Bearer {raw_a}"}
        headers_b = {**_accept_headers(), "Authorization": f"Bearer {raw_b}"}
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            a_first = client.post(MCP_PATH, json=_initialize_payload(1), headers=headers_a)
            a_second = client.post(MCP_PATH, json=_initialize_payload(2), headers=headers_a)
            # B's FIRST request, sent only after A is already over its own limit.
            b_first = client.post(MCP_PATH, json=_initialize_payload(3), headers=headers_b)

        assert a_first.status_code == 200
        assert a_second.status_code == 429, "A's second request should exceed limit=1"
        assert b_first.status_code == 200, "B must be unaffected by A's exhausted bucket"
        assert patched_redis.counters == {
            f"{RATE_KEY_PREFIX}{USER_A}": 2,
            f"{RATE_KEY_PREFIX}{USER_B}": 1,
        }


class TestRedisBackendFailure:
    async def test_redis_unavailable_fails_open_by_default(
        self, monkeypatch, broken_redis, token_store
    ) -> None:
        """Deliberate asymmetry with identity.py's fail-closed contract — see
        rate_limit.py's module docstring. The rate limiter's OWN backend
        failing must not take down the whole (already-live) read endpoint."""
        factory, scope = token_store
        raw_token = "mcp_rateLimitRedisDownToken"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_token)
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)
        monkeypatch.delenv("MCP_RATE_LIMIT_FAIL_CLOSED", raising=False)

        app = build_asgi_app()
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            resp = client.post(
                MCP_PATH,
                json=_initialize_payload(),
                headers={**_accept_headers(), "Authorization": f"Bearer {raw_token}"},
            )

        assert resp.status_code == 200

    async def test_redis_unavailable_fails_closed_when_opted_in(
        self, monkeypatch, broken_redis, token_store
    ) -> None:
        factory, scope = token_store
        raw_token = "mcp_rateLimitRedisDownClosedToken"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_token)
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)
        monkeypatch.setenv("MCP_RATE_LIMIT_FAIL_CLOSED", "true")

        app = build_asgi_app()
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            resp = client.post(
                MCP_PATH,
                json=_initialize_payload(),
                headers={**_accept_headers(), "Authorization": f"Bearer {raw_token}"},
            )

        assert resp.status_code == 503
        assert "Retry-After" in resp.headers
        assert resp.json()["error"] == "capacity_check_unavailable"


# ---- Pure-function unit tests: no ASGI, no DB, no Redis ----


class TestBearerTokenExtraction:
    def test_extracts_token_from_properly_formed_header(self) -> None:
        scope = {"headers": [(b"authorization", b"Bearer mcp_abc123")]}
        assert _bearer_token(scope) == "mcp_abc123"

    def test_case_insensitive_scheme_and_header_name(self) -> None:
        scope = {"headers": [(b"Authorization", b"bearer mcp_abc123")]}
        assert _bearer_token(scope) == "mcp_abc123"

    def test_missing_header_returns_none(self) -> None:
        assert _bearer_token({"headers": []}) is None
        assert _bearer_token({"headers": None}) is None

    def test_non_bearer_scheme_returns_none(self) -> None:
        scope = {"headers": [(b"authorization", b"Basic dXNlcjpwYXNz")]}
        assert _bearer_token(scope) is None

    def test_empty_bearer_value_returns_none(self) -> None:
        scope = {"headers": [(b"authorization", b"Bearer ")]}
        assert _bearer_token(scope) is None


class TestLimitAndFailClosedEnvParsing:
    def test_default_limit_when_env_unset(self, monkeypatch) -> None:
        monkeypatch.delenv("MCP_RATE_LIMIT_PER_MINUTE", raising=False)
        assert _limit_per_minute() == DEFAULT_LIMIT_PER_MINUTE

    def test_limit_overridden_by_env(self, monkeypatch) -> None:
        monkeypatch.setenv("MCP_RATE_LIMIT_PER_MINUTE", "7")
        assert _limit_per_minute() == 7

    @pytest.mark.parametrize("value", ["1", "true", "True", "yes", "YES"])
    def test_fail_closed_truthy_values(self, monkeypatch, value) -> None:
        monkeypatch.setenv("MCP_RATE_LIMIT_FAIL_CLOSED", value)
        assert _fail_closed() is True

    @pytest.mark.parametrize("value", ["0", "false", "False", "no", ""])
    def test_fail_closed_falsy_values(self, monkeypatch, value) -> None:
        monkeypatch.setenv("MCP_RATE_LIMIT_FAIL_CLOSED", value)
        assert _fail_closed() is False

    def test_fail_closed_defaults_false_when_unset(self, monkeypatch) -> None:
        monkeypatch.delenv("MCP_RATE_LIMIT_FAIL_CLOSED", raising=False)
        assert _fail_closed() is False
