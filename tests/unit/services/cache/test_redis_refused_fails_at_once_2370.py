"""#2370: a refused Redis connection fails at once, not after the pool's timeout.

redis-py 5.0.1's ``BlockingConnectionPool.get_connection`` held its condition lock
while connecting. On a failed connect the base class called ``release``, which
needs the same lock, so the pool waited on itself until ``async_timeout(timeout)``
fired: our 2 seconds (#2334's setting), on EVERY call. One status turn makes about
ten cache calls, so an unreachable Redis added about 20 seconds to it, and the
revoked-token check paid 2 seconds per request. Arch ruled the fix is the upgrade
(2026-11-14); 5.0.2 and later connect outside the lock. ``requirements.txt`` pins
5.0.8 (CIO's weighing: patch releases only).

These pins fail on 5.0.1 (each call takes the full 2 s) and pass on the fixed
client. They use a localhost port with nothing listening, so the connect is REFUSED;
a blackholed host still costs one ``socket_connect_timeout``, which is correct.

LAYER: the real ``RedisFactory`` pool and the real redis client against a closed
local port. No Redis server is needed.
"""

import socket
import time
from unittest.mock import MagicMock

import pytest
import redis
import redis.asyncio as aioredis

from services.auth.jwt_service import BlacklistUnavailable
from services.auth.token_blacklist import TokenBlacklist
from services.cache.redis_factory import RedisFactory
from services.intent_service.context_cache import ContextCache

# Generous for a slow CI runner; the defect cost 2.0 s per call.
PER_CALL_BUDGET_S = 0.75
CALLS = 10


@pytest.fixture
def refused_redis(monkeypatch):
    """A RedisFactory pointed at a closed local port, with no pool carried in or
    left behind."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    monkeypatch.setattr(RedisFactory, "_redis_pool", None)
    monkeypatch.setattr(RedisFactory, "_pool_loop_ref", None)
    monkeypatch.setattr(RedisFactory, "_last_health_ping", None)
    monkeypatch.setenv("REDIS_URL", f"redis://127.0.0.1:{port}")
    yield RedisFactory


def test_the_pinned_client_has_the_fix():
    """The self-wait was fixed in 5.0.2. A pin below that brings the 2 s per call
    back, so the requirement and the installed client are both checked."""
    installed = tuple(int(p) for p in redis.__version__.split(".")[:3])
    assert installed >= (5, 0, 2), f"redis {redis.__version__} has the blocking-pool self-wait"
    from pathlib import Path

    pins = Path(__file__).resolve().parents[4].joinpath("requirements.txt").read_text()
    line = next(ln for ln in pins.splitlines() if ln.startswith("redis=="))
    pinned = tuple(int(p) for p in line.split("==")[1].split(".")[:3])
    assert pinned >= (5, 0, 2), line


async def test_ten_cache_reads_against_a_refused_redis_take_well_under_a_second_each(
    refused_redis,
):
    """The turn-level shape: ten cache calls. Each is a miss (None), and none waits
    for the pool timeout."""
    cache = ContextCache(redis_factory=refused_redis)
    start = time.monotonic()
    results = [await cache.get(f"k-2370-{i}") for i in range(CALLS)]
    elapsed = time.monotonic() - start
    assert results == [None] * CALLS  # a failed cache is a miss, never an error
    assert elapsed < CALLS * PER_CALL_BUDGET_S, (
        f"{CALLS} cache reads took {elapsed:.1f} s against a refused Redis; "
        "on the defective client each took the pool's 2 s"
    )


async def test_a_direct_call_raises_a_connection_error_at_once(refused_redis):
    client = await refused_redis.create_client()
    start = time.monotonic()
    with pytest.raises(aioredis.ConnectionError):
        await client.get("k-2370-direct")
    assert time.monotonic() - start < PER_CALL_BUDGET_S


# integration: the autouse mock_token_blacklist (tests/conftest.py) stubs
# is_blacklisted for everything else; this pin needs the real one (as #2334's does).
@pytest.mark.integration
async def test_the_revoked_token_check_still_fails_closed_and_now_does_so_quickly(
    refused_redis,
):
    """HOST's line (2026-11-14): faster must still mean CLOSED. With Redis refusing,
    the check raises ``BlacklistUnavailable``; it never answers "not revoked"."""
    blacklist = TokenBlacklist(refused_redis, MagicMock())
    blacklist._redis_available = True  # Redis was up at init and has since gone
    blacklist._initialized = True
    start = time.monotonic()
    for i in range(3):
        with pytest.raises(BlacklistUnavailable):
            await blacklist.is_blacklisted(f"token-2370-{i}")
    assert time.monotonic() - start < 3 * PER_CALL_BUDGET_S
