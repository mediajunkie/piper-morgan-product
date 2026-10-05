"""#1458 — per-caller-identity rate limiting on ``/mcp`` (services/mcp/server/rate_limit.py).

No rate limiter existed anywhere under ``services/mcp/server/`` before this file (grep
denominator: ``grep -rliI "rate.?limit\\|throttle\\|429" services/ web/`` returned the
usual web-app surfaces — ``web/middleware/usage_cap_middleware.py`` et al. — but nothing
under ``services/mcp/server/``). This pins the mechanism added to close that gap:
:class:`~services.mcp.server.rate_limit.MCPRateLimitMiddleware`, wired into
``build_asgi_app()`` between :class:`~services.mcp.server.app.MCPPathGate` and FastMCP's
own auth+routing stack.

PA REVIEW CORRECTION (2026-10-05): the first revision of this module assumed Redis was
always the backend and failed fully OPEN on any Redis error. PA ran ``fly secrets list
-a piper-morgan-mcp`` and found no ``REDIS_URL`` on that app — in production every
``INCR`` would have errored and the limiter would have enforced NOTHING, silently, while
every test here (against a local dev Redis / a fake) stayed green. The fix: backend
selection is gated on ``REDIS_URL`` actually being set (:func:`_redis_url_configured`,
NOT "try Redis and catch" — local dev has a real Redis on the hardcoded default, which
would have hidden the exact gap PA found), with an in-memory fixed-window fallback that
is used whenever Redis isn't configured, and ALSO used for a single request if Redis
IS configured but errors at request time (never fails open on that either). See
``rate_limit.py``'s module docstring for the full design and the per-machine caveat on
the in-memory backend.

LAYER (m-43): every enforcement test goes through the real ASGI app
(``services.mcp.server.app.build_asgi_app()``) via Starlette's ``TestClient`` — the same
protocol surface uvicorn serves — exercising the real middleware layering, not a direct
call into ``MCPRateLimitMiddleware`` in isolation. Pure-function tests (token/env
parsing) are unit-level on purpose; they don't need the ASGI stack.

DENOMINATOR: the rate limiter only. Identity correctness (401s, two-caller identity
isolation) is ``test_identity_unit1.py``'s scope; this file assumes a valid bearer
resolves correctly (already pinned there) and tests what happens ONCE identity is
resolved, under repeated requests.

Backend gating in these tests: ``REDIS_URL`` is unset by default (autouse
``_default_no_redis_url`` below) — the SAME gate production uses, not ambient
environment state (this dev box has a real Redis on ``RedisFactory``'s default, which
would otherwise mask exactly the gap PA found). Tests that want the Redis CODE PATH use
``patched_redis``/``broken_redis``, which explicitly set ``REDIS_URL`` (opting in) and
patch ``services.cache.redis_factory.RedisFactory.redis_scope`` (the same idiom
``test_usage_cap_middleware_1370.py`` established — patching it at its definition module
affects every caller). Tests that want the MEMORY path (the production default on
``piper-morgan-mcp`` today) rely on the autouse default and never touch Redis at all.
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
from services.mcp.server import rate_limit as rate_limit_mod  # noqa: E402
from services.mcp.server.app import build_asgi_app  # noqa: E402
from services.mcp.server.rate_limit import (  # noqa: E402
    DEFAULT_LIMIT_PER_MINUTE,
    RATE_KEY_PREFIX,
    _bearer_token,
    _fail_closed,
    _limit_per_minute,
    _redis_url_configured,
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


@pytest.fixture(autouse=True)
def _default_no_redis_url(monkeypatch):
    """Backend selection defaults to MEMORY unless a test explicitly opts
    into the Redis path (``patched_redis``/``broken_redis`` below), matching
    production's actual gate (``_redis_url_configured``) rather than this
    dev box's ambient local Redis. This is the fixture that makes the PA
    review finding reproducible as a test: without it, a test run on a
    machine with a local Redis would silently exercise Redis even though
    ``REDIS_URL`` was never set — exactly the mismatch that hid the gap."""
    monkeypatch.delenv("REDIS_URL", raising=False)
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
def patched_redis(monkeypatch, fake_redis):
    """Opts INTO the Redis code path: sets ``REDIS_URL`` (the real gate,
    ``_redis_url_configured``) AND patches the client to the fake. A test
    using only the fake without setting the env var would silently test
    nothing, now that backend selection checks the env var first."""
    monkeypatch.setenv("REDIS_URL", "redis://test-fake:6379/0")

    @asynccontextmanager
    async def _scope():
        yield fake_redis

    with patch(
        "services.cache.redis_factory.RedisFactory.redis_scope",
        side_effect=_scope,
    ):
        yield fake_redis


@pytest.fixture
def broken_redis(monkeypatch):
    """Opts into the Redis path (``REDIS_URL`` set), but every Redis call
    raises — exercises the fall-back-to-memory-and-still-enforce behavior
    (PA review finding), not the old fail-open behavior."""
    monkeypatch.setenv("REDIS_URL", "redis://test-fake:6379/0")

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


class TestNoRedisUrlUsesMemoryBackend:
    """PA review requirement (a): no REDIS_URL -> memory backend enforces
    the limit, and A != B isolation still holds under it."""

    async def test_memory_backend_enforces_the_limit(self, monkeypatch, token_store) -> None:
        factory, scope = token_store
        raw_token = "mcp_rateLimitMemoryToken"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_token)
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)
        monkeypatch.delenv("REDIS_URL", raising=False)
        monkeypatch.setenv("MCP_RATE_LIMIT_PER_MINUTE", "2")

        assert _redis_url_configured() is False  # sanity: this test IS exercising memory

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
        assert third.json()["error"] == "rate_limited"

    async def test_memory_backend_still_isolates_two_callers(
        self, monkeypatch, token_store
    ) -> None:
        factory, scope = token_store
        raw_a, raw_b = "mcp_rateLimitMemoryCallerA", "mcp_rateLimitMemoryCallerB"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_a, label="A")
        await _seed_token(factory, user_id=USER_B, raw_token=raw_b, label="B")
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)
        monkeypatch.delenv("REDIS_URL", raising=False)
        monkeypatch.setenv("MCP_RATE_LIMIT_PER_MINUTE", "1")

        app = build_asgi_app()
        headers_a = {**_accept_headers(), "Authorization": f"Bearer {raw_a}"}
        headers_b = {**_accept_headers(), "Authorization": f"Bearer {raw_b}"}
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            a_first = client.post(MCP_PATH, json=_initialize_payload(1), headers=headers_a)
            a_second = client.post(MCP_PATH, json=_initialize_payload(2), headers=headers_a)
            b_first = client.post(MCP_PATH, json=_initialize_payload(3), headers=headers_b)

        assert a_first.status_code == 200
        assert (
            a_second.status_code == 429
        ), "A's second request should exceed limit=1 even on memory"
        assert b_first.status_code == 200, "B must be unaffected by A's exhausted memory bucket"


class TestRedisConfiguredButErroringFallsBackToMemory:
    """PA review requirement (b): Redis configured (REDIS_URL set) but every
    call raises -> falls back to the in-memory counter and STILL enforces
    the limit — never fails open. This replaces the old
    test_redis_unavailable_fails_open_by_default, which pinned exactly the
    behavior PA's fly secrets check proved unsafe."""

    async def test_falls_back_to_memory_and_still_enforces(
        self, monkeypatch, broken_redis, token_store
    ) -> None:
        factory, scope = token_store
        raw_token = "mcp_rateLimitRedisErrorsToken"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_token)
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)
        monkeypatch.setenv("MCP_RATE_LIMIT_PER_MINUTE", "2")
        monkeypatch.delenv("MCP_RATE_LIMIT_FAIL_CLOSED", raising=False)

        assert _redis_url_configured() is True  # sanity: Redis IS the configured backend here

        app = build_asgi_app()
        headers = {**_accept_headers(), "Authorization": f"Bearer {raw_token}"}
        statuses = []
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            for i in range(3):
                resp = client.post(MCP_PATH, json=_initialize_payload(i), headers=headers)
                statuses.append(resp)

        # The load-bearing assertion: NOT [200, 200, 200] (the old fail-open
        # behavior) — the third request is still refused, via the memory
        # fallback, despite every Redis call having raised.
        assert [r.status_code for r in statuses] == [200, 200, 429]

    async def test_logs_one_warning_not_one_per_request(
        self, monkeypatch, broken_redis, token_store
    ) -> None:
        factory, scope = token_store
        raw_token = "mcp_rateLimitRedisErrorsWarnOnceToken"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_token)
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)
        monkeypatch.setenv("MCP_RATE_LIMIT_PER_MINUTE", "10")
        warnings: list[tuple] = []
        monkeypatch.setattr(
            rate_limit_mod.logger,
            "warning",
            lambda event, **kw: warnings.append((event, kw)),
        )

        app = build_asgi_app()
        headers = {**_accept_headers(), "Authorization": f"Bearer {raw_token}"}
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            for i in range(3):
                client.post(MCP_PATH, json=_initialize_payload(i), headers=headers)

        fallback_warnings = [
            w for w in warnings if w[0] == "mcp_rate_limit_redis_unavailable_falling_back_to_memory"
        ]
        assert (
            len(fallback_warnings) == 1
        ), f"expected exactly one fallback warning across 3 requests, got {len(fallback_warnings)}"


class TestFailClosedLastResort:
    """MCP_RATE_LIMIT_FAIL_CLOSED now only matters for the TRUE last-resort
    case: the rate-limit check raises despite the memory fallback (which
    should not happen in practice — this forces it via monkeypatch to prove
    the opt-in still works end to end)."""

    async def test_fail_closed_returns_503_when_check_itself_raises(
        self, monkeypatch, token_store
    ) -> None:
        factory, scope = token_store
        raw_token = "mcp_rateLimitHardFailureToken"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_token)
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)
        monkeypatch.delenv("REDIS_URL", raising=False)
        monkeypatch.setenv("MCP_RATE_LIMIT_FAIL_CLOSED", "true")

        def _boom(self, key, window_seconds):
            raise RuntimeError("in-memory counter boom (forced, defensive-only path)")

        monkeypatch.setattr(rate_limit_mod._InMemoryFixedWindow, "increment", _boom)

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

    async def test_default_proceeds_unmetered_when_check_itself_raises(
        self, monkeypatch, token_store
    ) -> None:
        """Without the opt-in, the same forced failure proceeds rather than
        503ing — the documented defensive-only default."""
        factory, scope = token_store
        raw_token = "mcp_rateLimitHardFailureDefaultToken"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_token)
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)
        monkeypatch.delenv("REDIS_URL", raising=False)
        monkeypatch.delenv("MCP_RATE_LIMIT_FAIL_CLOSED", raising=False)

        def _boom(self, key, window_seconds):
            raise RuntimeError("in-memory counter boom (forced, defensive-only path)")

        monkeypatch.setattr(rate_limit_mod._InMemoryFixedWindow, "increment", _boom)

        app = build_asgi_app()
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            resp = client.post(
                MCP_PATH,
                json=_initialize_payload(),
                headers={**_accept_headers(), "Authorization": f"Bearer {raw_token}"},
            )

        assert resp.status_code == 200


class TestActiveBackendLoggedOnce:
    """PA review requirement (3): one line naming the active backend, logged
    once per process (per middleware instance here), not per request."""

    async def test_memory_backend_logged_once_across_multiple_requests(
        self, monkeypatch, token_store
    ) -> None:
        factory, scope = token_store
        raw_token = "mcp_rateLimitBackendLogMemoryToken"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_token)
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)
        monkeypatch.delenv("REDIS_URL", raising=False)
        infos: list[tuple] = []
        monkeypatch.setattr(
            rate_limit_mod.logger, "info", lambda event, **kw: infos.append((event, kw))
        )

        app = build_asgi_app()
        headers = {**_accept_headers(), "Authorization": f"Bearer {raw_token}"}
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            for i in range(3):
                client.post(MCP_PATH, json=_initialize_payload(i), headers=headers)

        backend_logs = [kw for event, kw in infos if event == "mcp_rate_limit_backend_active"]
        assert backend_logs == [{"backend": "memory"}]

    async def test_redis_backend_logged_once(self, monkeypatch, patched_redis, token_store) -> None:
        factory, scope = token_store
        raw_token = "mcp_rateLimitBackendLogRedisToken"
        await _seed_token(factory, user_id=USER_A, raw_token=raw_token)
        monkeypatch.setattr(AsyncSessionFactory, "session_scope", scope)
        infos: list[tuple] = []
        monkeypatch.setattr(
            rate_limit_mod.logger, "info", lambda event, **kw: infos.append((event, kw))
        )

        app = build_asgi_app()
        headers = {**_accept_headers(), "Authorization": f"Bearer {raw_token}"}
        with TestClient(app, base_url=LOCAL_BASE_URL) as client:
            client.post(MCP_PATH, json=_initialize_payload(), headers=headers)

        backend_logs = [kw for event, kw in infos if event == "mcp_rate_limit_backend_active"]
        assert backend_logs == [{"backend": "redis"}]


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
