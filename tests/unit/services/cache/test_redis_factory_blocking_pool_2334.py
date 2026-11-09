"""#2334: RedisFactory's shared pool waits for a free slot instead of raising.

A plain redis ConnectionPool raises "Too many connections" once all 20 are
checked out, so a burst of >20 concurrent authenticated requests failed closed
in the token blacklist. Arch's ruling (11-09 10:31): BlockingConnectionPool,
timeout=2, socket_connect_timeout=2, socket_timeout=5, size 20. The 50-way
concurrency pin is tests/performance/test_token_blacklist_performance.py
::test_concurrent_blacklist_lookups, which needs a real Redis.
"""

import asyncio
import gc
import socket
import time
from unittest.mock import MagicMock

import pytest
import redis.asyncio as redis

from services.auth.jwt_service import BlacklistUnavailable
from services.auth.token_blacklist import TokenBlacklist
from services.cache.redis_factory import RedisFactory


@pytest.fixture
def fresh_factory(monkeypatch):
    """No pool carried in from another test; none left behind."""
    monkeypatch.setattr(RedisFactory, "_redis_pool", None)
    monkeypatch.setattr(RedisFactory, "_pool_loop_ref", None)
    yield RedisFactory


def _closed_port() -> int:
    """A localhost port with nothing listening (bound, then released)."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


async def test_pool_is_blocking_with_ruled_timeouts(fresh_factory, monkeypatch):
    monkeypatch.setenv("REDIS_URL", "redis://127.0.0.1:6379")
    await fresh_factory.initialize()
    pool = fresh_factory._redis_pool

    assert isinstance(pool, redis.BlockingConnectionPool)
    assert pool.max_connections == 20
    assert pool.timeout == 2  # redis-py 5.0.1 would default this wait to 20 s
    assert pool.connection_kwargs["socket_connect_timeout"] == 2
    assert pool.connection_kwargs["socket_timeout"] == 5


def test_a_new_event_loop_rebuilds_the_blocking_pool(fresh_factory, monkeypatch):
    """#1452's loop-change rebuild keeps working with the blocking pool."""
    monkeypatch.setenv("REDIS_URL", "redis://127.0.0.1:6379")

    async def build():
        await fresh_factory.initialize()
        return fresh_factory._redis_pool

    first = asyncio.run(build())
    gc.collect()  # free the first loop, so the next one can reuse its id()
    second = asyncio.run(build())

    assert second is not first
    assert isinstance(second, redis.BlockingConnectionPool)
    assert second.timeout == 2


# integration: the autouse mock_token_blacklist (tests/conftest.py) stubs
# is_blacklisted to False for everything else; this pin needs the real one.
@pytest.mark.integration
async def test_a_down_redis_still_fails_closed_promptly(fresh_factory, monkeypatch):
    monkeypatch.setenv("REDIS_URL", f"redis://127.0.0.1:{_closed_port()}")
    blacklist = TokenBlacklist(fresh_factory, MagicMock())
    blacklist._redis_available = True  # Redis was up at init and has since gone
    blacklist._initialized = True

    start = time.monotonic()
    with pytest.raises(BlacklistUnavailable):
        await blacklist.is_blacklisted("token-down-redis-2334")
    assert time.monotonic() - start < 10


@pytest.mark.integration
async def test_fifty_concurrent_lookups_on_twenty_connections(fresh_factory, monkeypatch):
    """The burst that used to raise "Too many connections" now queues and answers.

    Needs a reachable Redis (local 6379, or the full suite's service); skips
    with the reason when there is none. Latency is the perf file's question.
    """
    monkeypatch.setenv("REDIS_URL", "redis://127.0.0.1:6379")
    try:
        probe = redis.Redis.from_url("redis://127.0.0.1:6379", socket_connect_timeout=1)
        await probe.ping()
        await probe.aclose()
    except Exception as exc:
        pytest.skip(f"no Redis on 127.0.0.1:6379 ({exc})")

    blacklist = TokenBlacklist(fresh_factory, MagicMock())
    blacklist._redis_available = True
    blacklist._initialized = True

    results = await asyncio.gather(
        *(blacklist.is_blacklisted(f"token-burst-2334-{i}") for i in range(50))
    )

    assert results == [False] * 50
    assert fresh_factory._redis_pool.max_connections == 20


async def test_startup_log_never_carries_the_redis_password(fresh_factory, monkeypatch):
    """#2335: the pool-init log line names host:port only, never the URL."""
    from structlog.testing import capture_logs

    monkeypatch.setenv("REDIS_URL", "redis://default:s3cret-pw-2335@redis.example.test:6380")
    with capture_logs() as logs:
        await fresh_factory.initialize()

    init = [e for e in logs if e.get("event") == "Redis connection pool initialized"]
    assert init, logs
    assert init[0]["redis_host"] == "redis.example.test:6380"
    assert "s3cret-pw-2335" not in repr(logs)
