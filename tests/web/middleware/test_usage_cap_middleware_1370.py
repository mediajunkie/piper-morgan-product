"""Tests for UsageCapMiddleware (ADR-076).

Covers both mechanisms independently (rate limit, concurrency gauge), the
fail-closed behavior on Redis errors, exempt-path passthrough, and principal
resolution (authenticated user_id vs IP fallback). Uses an in-memory fake
Redis patched in via ``RedisFactory.redis_scope`` — the same pattern
established in ``test_oauth_redis_state_1109.py`` — extended with the
sorted-set + INCR/EXPIRE/TTL commands this middleware needs.
"""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, Mock, patch

import pytest
from starlette.requests import Request

from web.middleware.usage_cap_middleware import (
    CONCURRENCY_GAUGE_KEY,
    MAX_CONCURRENT_SESSIONS,
    RATE_LIMIT_PER_MINUTE,
    UsageCapMiddleware,
    _resolve_principal,
)


class _FakeRedis:
    """Minimal in-memory stand-in covering exactly the surface this
    middleware uses: INCR/EXPIRE/TTL (rate limit) and
    ZADD/ZSCORE/ZCARD/ZREMRANGEBYSCORE (concurrency gauge)."""

    def __init__(self):
        self.counters: dict[str, int] = {}
        self.ttls: dict[str, int] = {}
        self.zsets: dict[str, dict[str, float]] = {}
        self.closed = False

    async def incr(self, key):
        self.counters[key] = self.counters.get(key, 0) + 1
        return self.counters[key]

    async def expire(self, key, seconds):
        self.ttls[key] = seconds
        return True

    async def ttl(self, key):
        return self.ttls.get(key, -1)

    async def zadd(self, key, mapping):
        self.zsets.setdefault(key, {}).update(mapping)
        return len(mapping)

    async def zscore(self, key, member):
        return self.zsets.get(key, {}).get(member)

    async def zcard(self, key):
        return len(self.zsets.get(key, {}))

    async def zremrangebyscore(self, key, min_score, max_score):
        members = self.zsets.get(key, {})
        # min_score is always "-inf" in this middleware's usage
        removed = [m for m, score in members.items() if score <= max_score]
        for m in removed:
            del members[m]
        return len(removed)

    async def close(self):
        self.closed = True


@pytest.fixture
def fake_redis():
    return _FakeRedis()


@pytest.fixture
def patched_redis(fake_redis):
    @asynccontextmanager
    async def _scope():
        yield fake_redis

    with patch(
        "web.middleware.usage_cap_middleware.RedisFactory.redis_scope",
        side_effect=_scope,
    ):
        yield fake_redis


def _make_request(path="/api/v1/intent", user_id=None, client_ip="1.2.3.4", forwarded_for=None):
    request = Mock(spec=Request)
    request.url.path = path
    request.state = Mock()
    request.state.user_id = user_id
    request.client = Mock()
    request.client.host = client_ip
    headers = {}
    if forwarded_for:
        headers["x-forwarded-for"] = forwarded_for
    request.headers = headers
    return request


@pytest.fixture
def middleware():
    return UsageCapMiddleware(Mock())


class TestPrincipalResolution:
    def test_authenticated_user_keyed_by_user_id(self):
        request = _make_request(user_id="user-42")
        assert _resolve_principal(request) == "user:user-42"

    def test_unauthenticated_falls_back_to_ip(self):
        request = _make_request(user_id=None, client_ip="9.8.7.6")
        assert _resolve_principal(request) == "ip:9.8.7.6"

    def test_unauthenticated_prefers_forwarded_for(self):
        request = _make_request(user_id=None, client_ip="9.8.7.6", forwarded_for="1.1.1.1, 2.2.2.2")
        assert _resolve_principal(request) == "ip:1.1.1.1"


class TestExemptPaths:
    @pytest.mark.asyncio
    async def test_health_check_bypasses_redis_entirely(self, middleware):
        request = _make_request(path="/health")
        call_next = AsyncMock(return_value=Mock())

        # No Redis patch active — if the middleware tried to touch Redis here,
        # it would raise (RedisFactory isn't patched), proving passthrough.
        result = await middleware.dispatch(request, call_next)

        call_next.assert_called_once_with(request)
        assert result is call_next.return_value


class TestRateLimit:
    @pytest.mark.asyncio
    async def test_under_limit_passes_through(self, middleware, patched_redis):
        request = _make_request(user_id="user-1")
        call_next = AsyncMock(return_value=Mock())

        result = await middleware.dispatch(request, call_next)

        call_next.assert_called_once_with(request)
        assert result is call_next.return_value

    @pytest.mark.asyncio
    async def test_exceeding_limit_returns_429_with_retry_after(self, middleware, patched_redis):
        request = _make_request(user_id="user-2")
        call_next = AsyncMock(return_value=Mock())

        # Drive the counter past the threshold directly (avoids RATE_LIMIT_PER_MINUTE
        # sequential awaits in the test).
        patched_redis.counters[f"usage_cap:rate:user:user-2"] = RATE_LIMIT_PER_MINUTE
        patched_redis.ttls[f"usage_cap:rate:user:user-2"] = 45

        result = await middleware.dispatch(request, call_next)

        call_next.assert_not_called()
        assert result.status_code == 429
        assert result.headers["retry-after"] == "45"

    @pytest.mark.asyncio
    async def test_rate_limit_is_per_principal_not_global(self, middleware, patched_redis):
        """Two different principals must not share one counter."""
        patched_redis.counters["usage_cap:rate:user:user-A"] = RATE_LIMIT_PER_MINUTE

        request_a = _make_request(user_id="user-A")
        request_b = _make_request(user_id="user-B")
        call_next = AsyncMock(return_value=Mock())

        result_a = await middleware.dispatch(request_a, call_next)
        result_b = await middleware.dispatch(request_b, call_next)

        assert result_a.status_code == 429
        assert result_b is call_next.return_value  # user-B unaffected by user-A's count


class TestConcurrencyCap:
    @pytest.mark.asyncio
    async def test_new_principal_admitted_under_cap(self, middleware, patched_redis):
        request = _make_request(user_id="user-3")
        call_next = AsyncMock(return_value=Mock())

        result = await middleware.dispatch(request, call_next)

        assert result is call_next.return_value
        assert "user:user-3" in patched_redis.zsets[CONCURRENCY_GAUGE_KEY]

    @pytest.mark.asyncio
    async def test_new_principal_rejected_at_cap(self, middleware, patched_redis):
        # Fill the gauge to the cap with OTHER principals.
        for i in range(MAX_CONCURRENT_SESSIONS):
            patched_redis.zsets.setdefault(CONCURRENCY_GAUGE_KEY, {})[f"user:existing-{i}"] = 1e12

        request = _make_request(user_id="user-new")
        call_next = AsyncMock(return_value=Mock())

        result = await middleware.dispatch(request, call_next)

        call_next.assert_not_called()
        assert result.status_code == 503
        assert result.headers["retry-after"] == "30"

    @pytest.mark.asyncio
    async def test_already_active_principal_not_blocked_at_cap(self, middleware, patched_redis):
        """An existing active session refreshing its own slot must not be
        rejected just because the instance is at capacity — it already
        occupies one of the counted slots."""
        for i in range(MAX_CONCURRENT_SESSIONS):
            patched_redis.zsets.setdefault(CONCURRENCY_GAUGE_KEY, {})[f"user:existing-{i}"] = 1e12
        # user-0 is one of the existing (already-counted) members.
        request = _make_request(user_id="existing-0")
        call_next = AsyncMock(return_value=Mock())

        result = await middleware.dispatch(request, call_next)

        assert result is call_next.return_value

    @pytest.mark.asyncio
    async def test_stale_entries_pruned_before_capacity_check(self, middleware, patched_redis):
        """A session that's gone idle past CONCURRENT_SESSION_IDLE_SECONDS
        must release its slot automatically (no explicit decrement needed)."""
        # One ancient entry (score = epoch 0, guaranteed stale) at the cap.
        for i in range(MAX_CONCURRENT_SESSIONS):
            patched_redis.zsets.setdefault(CONCURRENCY_GAUGE_KEY, {})[f"user:stale-{i}"] = 0.0

        request = _make_request(user_id="user-fresh")
        call_next = AsyncMock(return_value=Mock())

        result = await middleware.dispatch(request, call_next)

        # All stale entries pruned, so the new principal is admitted.
        assert result is call_next.return_value
        assert "user:stale-0" not in patched_redis.zsets[CONCURRENCY_GAUGE_KEY]


class TestFailClosed:
    @pytest.mark.asyncio
    async def test_redis_error_denies_request(self, middleware):
        @asynccontextmanager
        async def _broken_scope():
            raise ConnectionError("redis down")
            yield  # pragma: no cover - unreachable, satisfies generator shape

        with patch(
            "web.middleware.usage_cap_middleware.RedisFactory.redis_scope",
            side_effect=_broken_scope,
        ):
            request = _make_request(user_id="user-4")
            call_next = AsyncMock(return_value=Mock())

            result = await middleware.dispatch(request, call_next)

        call_next.assert_not_called()
        assert result.status_code == 503
        assert result.status_code != 200
