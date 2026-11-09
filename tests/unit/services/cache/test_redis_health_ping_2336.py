"""#2336: create_client pings for the health record, not on every client.

The ping gated nothing (a failure only logged), so it was one extra round trip
on every Redis read. Now it runs on a new pool's first client and then at most
once per _HEALTH_PING_INTERVAL_S, and still feeds the redis_connection record.
"""

from unittest.mock import AsyncMock, patch

import pytest
import redis.asyncio as redis

from services.cache import redis_factory as rf
from services.cache.redis_factory import RedisFactory


@pytest.fixture
def fresh_factory(monkeypatch):
    monkeypatch.setenv("REDIS_URL", "redis://127.0.0.1:6379")
    monkeypatch.setattr(RedisFactory, "_redis_pool", None)
    monkeypatch.setattr(RedisFactory, "_pool_loop_ref", None)
    monkeypatch.setattr(RedisFactory, "_last_health_ping", None)
    yield RedisFactory


async def test_many_clients_inside_the_interval_ping_once(fresh_factory):
    with patch.object(redis.Redis, "ping", new=AsyncMock(return_value=True)) as ping:
        for _ in range(25):
            await fresh_factory.create_client()
    assert ping.await_count == 1


async def test_the_ping_runs_again_once_the_interval_has_passed(fresh_factory, monkeypatch):
    clock = [1000.0]
    monkeypatch.setattr(rf.time, "monotonic", lambda: clock[0])
    with patch.object(redis.Redis, "ping", new=AsyncMock(return_value=True)) as ping:
        await fresh_factory.create_client()
        clock[0] += rf._HEALTH_PING_INTERVAL_S - 1
        await fresh_factory.create_client()
        clock[0] += 1
        await fresh_factory.create_client()
    assert ping.await_count == 2


async def test_health_still_records_success_and_failure(fresh_factory, monkeypatch):
    clock = [5000.0]
    monkeypatch.setattr(rf.time, "monotonic", lambda: clock[0])
    with (
        patch.object(rf.health_monitor, "record_success") as ok,
        patch.object(rf.health_monitor, "record_failure") as bad,
    ):
        with patch.object(redis.Redis, "ping", new=AsyncMock(return_value=True)):
            await fresh_factory.create_client()
        clock[0] += rf._HEALTH_PING_INTERVAL_S
        with patch.object(redis.Redis, "ping", new=AsyncMock(side_effect=ConnectionError("down"))):
            await fresh_factory.create_client()

    assert ok.call_args[0][0] == "redis_connection"
    assert bad.call_args[0][0] == "redis_connection"
    assert "down" in bad.call_args[0][1]


async def test_a_rebuilt_pool_pings_on_its_first_client(fresh_factory):
    with patch.object(redis.Redis, "ping", new=AsyncMock(return_value=True)) as ping:
        await fresh_factory.create_client()
        fresh_factory._redis_pool = None  # as after a loop change or close_pool
        fresh_factory._pool_loop_ref = None
        await fresh_factory.create_client()
    assert ping.await_count == 2
