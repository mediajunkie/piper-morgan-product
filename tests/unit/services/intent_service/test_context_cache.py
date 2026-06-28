"""
Unit tests for ContextCache (#984).

Covers cache hit, miss, error-on-get, error-on-set, get_or_compute,
invalidate, invalidate_prefix. Redis is mocked; no live Redis required.
"""

import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from services.intent_service.context_cache import ContextCache


@pytest.fixture
def fake_redis_client():
    """Mock Redis client with the methods ContextCache uses."""
    client = MagicMock()
    client.get = AsyncMock()
    client.setex = AsyncMock()
    client.delete = AsyncMock()
    client.scan = AsyncMock()
    return client


@pytest.fixture
def fake_factory(fake_redis_client):
    """Mock RedisFactory.create_client() returning the fake client."""
    factory = MagicMock()
    factory.create_client = AsyncMock(return_value=fake_redis_client)
    return factory


@pytest.fixture
def cache(fake_factory):
    return ContextCache(redis_factory=fake_factory)


class TestGet:
    @pytest.mark.asyncio
    async def test_get_returns_none_on_miss(self, cache, fake_redis_client):
        fake_redis_client.get.return_value = None
        result = await cache.get("context:calendar:user1")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_returns_deserialized_value_on_hit(self, cache, fake_redis_client):
        fake_redis_client.get.return_value = json.dumps(
            {"calendar": {"next_meeting": "10am"}}
        ).encode()
        result = await cache.get("context:calendar:user1")
        assert result == {"calendar": {"next_meeting": "10am"}}

    @pytest.mark.asyncio
    async def test_get_accepts_string_payload(self, cache, fake_redis_client):
        fake_redis_client.get.return_value = json.dumps({"x": 1})
        result = await cache.get("k")
        assert result == {"x": 1}

    @pytest.mark.asyncio
    async def test_get_returns_none_on_redis_error(self, cache, fake_redis_client):
        fake_redis_client.get.side_effect = Exception("connection refused")
        result = await cache.get("context:calendar:user1")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_returns_none_when_factory_fails(self, fake_factory):
        fake_factory.create_client.side_effect = Exception("redis down")
        cache = ContextCache(redis_factory=fake_factory)
        result = await cache.get("context:calendar:user1")
        assert result is None


class TestSet:
    @pytest.mark.asyncio
    async def test_set_calls_setex_with_ttl_and_returns_true(self, cache, fake_redis_client):
        ok = await cache.set("context:calendar:user1", {"foo": "bar"}, ttl_seconds=60)
        assert ok is True
        fake_redis_client.setex.assert_awaited_once()
        args, _ = fake_redis_client.setex.call_args
        assert args[0] == "context:calendar:user1"
        assert args[1] == 60
        assert json.loads(args[2]) == {"foo": "bar"}

    @pytest.mark.asyncio
    async def test_set_returns_false_on_redis_error_no_exception(self, cache, fake_redis_client):
        fake_redis_client.setex.side_effect = Exception("disk full")
        ok = await cache.set("k", {"x": 1}, ttl_seconds=60)
        assert ok is False  # graceful — must not raise

    @pytest.mark.asyncio
    async def test_set_returns_false_on_non_serializable(self, cache, fake_redis_client):
        class NotJSON:
            pass

        ok = await cache.set("k", NotJSON(), ttl_seconds=60)
        assert ok is False
        fake_redis_client.setex.assert_not_awaited()


class TestGetOrCompute:
    @pytest.mark.asyncio
    async def test_returns_cached_on_hit_does_not_call_compute(self, cache, fake_redis_client):
        fake_redis_client.get.return_value = json.dumps({"cached": True}).encode()
        compute = AsyncMock(return_value={"computed": True})
        result = await cache.get_or_compute("k", 60, compute)
        assert result == {"cached": True}
        compute.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_calls_compute_on_miss_and_writes_through(self, cache, fake_redis_client):
        fake_redis_client.get.return_value = None
        compute = AsyncMock(return_value={"computed": True})
        result = await cache.get_or_compute("k", 60, compute)
        assert result == {"computed": True}
        compute.assert_awaited_once()
        fake_redis_client.setex.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_returns_compute_result_on_redis_error_no_cache_write(
        self, cache, fake_redis_client
    ):
        fake_redis_client.get.side_effect = Exception("redis down")
        compute = AsyncMock(return_value={"computed": True})
        result = await cache.get_or_compute("k", 60, compute)
        assert result == {"computed": True}
        compute.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_does_not_cache_none_result(self, cache, fake_redis_client):
        fake_redis_client.get.return_value = None
        compute = AsyncMock(return_value=None)
        result = await cache.get_or_compute("k", 60, compute)
        assert result is None
        fake_redis_client.setex.assert_not_awaited()


class TestInvalidate:
    @pytest.mark.asyncio
    async def test_invalidate_returns_true_when_key_deleted(self, cache, fake_redis_client):
        fake_redis_client.delete.return_value = 1
        ok = await cache.invalidate("context:trust:user1")
        assert ok is True
        fake_redis_client.delete.assert_awaited_once_with("context:trust:user1")

    @pytest.mark.asyncio
    async def test_invalidate_returns_false_when_key_missing(self, cache, fake_redis_client):
        fake_redis_client.delete.return_value = 0
        ok = await cache.invalidate("context:trust:user1")
        assert ok is False

    @pytest.mark.asyncio
    async def test_invalidate_returns_false_on_error_no_exception(self, cache, fake_redis_client):
        fake_redis_client.delete.side_effect = Exception("connection lost")
        ok = await cache.invalidate("context:trust:user1")
        assert ok is False


class TestInvalidatePrefix:
    @pytest.mark.asyncio
    async def test_invalidate_prefix_uses_scan_and_returns_count(self, cache, fake_redis_client):
        # Two SCAN iterations: first returns keys+cursor, second returns empty+cursor=0
        fake_redis_client.scan.side_effect = [
            (123, [b"context:pending_todos:u1", b"context:completed_todos:u1"]),
            (0, []),
        ]
        fake_redis_client.delete.return_value = 2
        count = await cache.invalidate_prefix("context:pending_todos:u1")
        assert count == 2

    @pytest.mark.asyncio
    async def test_invalidate_prefix_returns_zero_on_no_matches(self, cache, fake_redis_client):
        fake_redis_client.scan.return_value = (0, [])
        count = await cache.invalidate_prefix("context:pending_todos:u1")
        assert count == 0
        fake_redis_client.delete.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_invalidate_prefix_returns_zero_on_error(self, cache, fake_redis_client):
        fake_redis_client.scan.side_effect = Exception("redis down")
        count = await cache.invalidate_prefix("context:pending_todos:u1")
        assert count == 0
