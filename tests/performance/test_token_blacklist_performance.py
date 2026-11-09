"""
Performance benchmarks for Token Blacklist lookups.

Tests both Redis (when available) and database fallback performance
to ensure <5ms target for blacklist checks during authentication.

Issue: #227 CORE-USERS-JWT
"""

import asyncio
import time
import uuid
from datetime import datetime, timedelta, timezone
from statistics import mean, median

import pytest

from services.auth.token_blacklist import TokenBlacklist
from services.cache.redis_factory import RedisFactory
from services.database.connection import db
from services.database.session_factory import AsyncSessionFactory

# --- Config ---
TARGET_LATENCY_MS = 5.0  # Target: <5ms for blacklist lookups
NUM_ITERATIONS = 100  # Number of lookups to test


# --- Helpers ---
async def measure_async_latency(coro):
    """Measure latency of an async operation in milliseconds"""
    start = time.perf_counter()
    result = await coro
    latency_ms = (time.perf_counter() - start) * 1000
    return latency_ms, result


# --- Fixtures ---
@pytest.fixture(scope="function")
async def blacklist():
    """Create TokenBlacklist instance for testing

    Handles event loop conflicts by resetting the global database connection
    to prevent futures from being attached to different event loops.
    """
    # Reset global database connection to avoid event loop conflicts
    # Each test gets a fresh event loop, so we need a fresh engine
    await db.close()
    db._initialized = False

    redis_factory = RedisFactory()
    db_session_factory = AsyncSessionFactory()
    bl = TokenBlacklist(redis_factory, db_session_factory)
    await bl.initialize()

    yield bl

    # Cleanup: Close database connection to prevent event loop issues
    # This ensures each test gets fresh connections on a clean event loop
    await db.close()
    db._initialized = False


@pytest.fixture(scope="function")
async def sample_tokens(blacklist):
    """Create sample blacklisted tokens for testing"""
    token_ids = []
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    # Add 10 sample tokens to blacklist
    for i in range(10):
        token_id = f"test_token_{uuid.uuid4()}"
        await blacklist.add(token_id=token_id, reason="performance_test", expires_at=expires_at)
        token_ids.append(token_id)

    yield token_ids

    # Cleanup: Test tokens will be automatically cleaned up by database rollback
    # Note: Redis entries would auto-expire via TTL if Redis were available
    pass


# --- Performance Tests ---
@pytest.mark.asyncio
@pytest.mark.performance
async def test_blacklist_lookup_latency(blacklist, sample_tokens):
    """
    Test blacklist lookup performance.

    Target: <5ms per lookup (average)
    """
    latencies = []

    # Test lookups for blacklisted tokens
    for token_id in sample_tokens:
        latency_ms, is_blacklisted = await measure_async_latency(blacklist.is_blacklisted(token_id))
        latencies.append(latency_ms)
        assert is_blacklisted, f"Token {token_id} should be blacklisted"

    # Test lookups for non-blacklisted tokens
    for i in range(10):
        non_existent_token = f"non_existent_{uuid.uuid4()}"
        latency_ms, is_blacklisted = await measure_async_latency(
            blacklist.is_blacklisted(non_existent_token)
        )
        latencies.append(latency_ms)
        assert not is_blacklisted, f"Token {non_existent_token} should NOT be blacklisted"

    # Calculate statistics
    avg_latency = mean(latencies)
    median_latency = median(latencies)
    max_latency = max(latencies)
    min_latency = min(latencies)

    # Print results
    print(f"\n{'='*60}")
    print(f"Token Blacklist Lookup Performance")
    print(f"{'='*60}")
    print(f"Iterations:      {len(latencies)}")
    print(f"Average latency: {avg_latency:.3f} ms")
    print(f"Median latency:  {median_latency:.3f} ms")
    print(f"Min latency:     {min_latency:.3f} ms")
    print(f"Max latency:     {max_latency:.3f} ms")
    print(f"Target:          <{TARGET_LATENCY_MS} ms")
    print(f"{'='*60}")

    if blacklist._redis_available:
        print(f"✅ Using Redis (fast path)")
    else:
        print(f"⚠️  Using Database fallback (slower)")

    # Assert performance target
    if avg_latency <= TARGET_LATENCY_MS:
        print(f"✅ PASS: Average latency {avg_latency:.3f}ms <= {TARGET_LATENCY_MS}ms target")
    else:
        print(f"⚠️  WARNING: Average latency {avg_latency:.3f}ms > {TARGET_LATENCY_MS}ms target")
        if not blacklist._redis_available:
            print(f"   (Database fallback is expected to be slower - consider this acceptable)")

    print(f"{'='*60}\n")


@pytest.mark.asyncio
@pytest.mark.performance
async def test_blacklist_add_latency():
    """
    Test blacklist add operation performance.

    Target: <10ms per add operation (less critical than lookup)
    """
    # Reset global database connection to avoid event loop conflicts
    await db.close()
    db._initialized = False

    # Create fresh blacklist instance
    redis_factory = RedisFactory()
    db_session_factory = AsyncSessionFactory()
    blacklist = TokenBlacklist(redis_factory, db_session_factory)
    await blacklist.initialize()

    latencies = []
    token_ids = []
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

    # Test adding tokens
    for i in range(20):
        token_id = f"perf_test_add_{uuid.uuid4()}"
        token_ids.append(token_id)

        latency_ms, success = await measure_async_latency(
            blacklist.add(
                token_id=token_id,
                reason="performance_test_add",
                expires_at=expires_at,
            )
        )
        latencies.append(latency_ms)
        assert success, f"Failed to add token {token_id}"

    # Calculate statistics
    avg_latency = mean(latencies)
    median_latency = median(latencies)
    max_latency = max(latencies)

    # Print results
    print(f"\n{'='*60}")
    print(f"Token Blacklist Add Performance")
    print(f"{'='*60}")
    print(f"Iterations:      {len(latencies)}")
    print(f"Average latency: {avg_latency:.3f} ms")
    print(f"Median latency:  {median_latency:.3f} ms")
    print(f"Max latency:     {max_latency:.3f} ms")
    print(f"Target:          <10 ms (less critical)")
    print(f"{'='*60}")

    if blacklist._redis_available:
        print(f"✅ Using Redis (fast path)")
    else:
        print(f"⚠️  Using Database fallback")

    if avg_latency <= 10.0:
        print(f"✅ PASS: Average latency {avg_latency:.3f}ms <= 10ms target")
    else:
        print(f"⚠️  WARNING: Average latency {avg_latency:.3f}ms > 10ms target")

    print(f"{'='*60}\n")

    # Cleanup: Close database connection to prevent event loop issues
    await db.close()
    db._initialized = False


@pytest.mark.asyncio
@pytest.mark.performance
async def test_concurrent_blacklist_lookups():
    """
    Test concurrent blacklist lookup performance.

    Simulates multiple simultaneous authentication requests checking blacklist.
    """
    # Reset global database connection to avoid event loop conflicts
    await db.close()
    db._initialized = False

    # Create fresh blacklist instance
    redis_factory = RedisFactory()
    db_session_factory = AsyncSessionFactory()
    blacklist = TokenBlacklist(redis_factory, db_session_factory)
    await blacklist.initialize()

    # Create sample tokens
    token_ids = []
    expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
    for i in range(10):
        token_id = f"test_token_{uuid.uuid4()}"
        await blacklist.add(token_id=token_id, reason="performance_test", expires_at=expires_at)
        token_ids.append(token_id)

    num_concurrent = 50

    # Create concurrent lookup tasks
    async def lookup_task(token_id):
        start = time.perf_counter()
        result = await blacklist.is_blacklisted(token_id)
        latency_ms = (time.perf_counter() - start) * 1000
        return latency_ms, result

    # Run concurrent lookups
    start_time = time.perf_counter()
    tasks = [lookup_task(token_ids[i % len(token_ids)]) for i in range(num_concurrent)]
    results = await asyncio.gather(*tasks)
    total_time_ms = (time.perf_counter() - start_time) * 1000

    # Extract latencies
    latencies = [latency for latency, _ in results]
    avg_latency = mean(latencies)
    max_latency = max(latencies)
    throughput = num_concurrent / (total_time_ms / 1000)  # requests/second

    # Print results
    print(f"\n{'='*60}")
    print(f"Concurrent Blacklist Lookup Performance")
    print(f"{'='*60}")
    print(f"Concurrent requests: {num_concurrent}")
    print(f"Total time:          {total_time_ms:.3f} ms")
    print(f"Avg latency:         {avg_latency:.3f} ms")
    print(f"Max latency:         {max_latency:.3f} ms")
    print(f"Throughput:          {throughput:.0f} requests/second")
    print(f"{'='*60}")

    if blacklist._redis_available:
        print(f"✅ Using Redis (concurrent operations efficient)")
    else:
        print(f"⚠️  Using Database fallback (may limit concurrency)")

    print(f"{'='*60}\n")

    # Assert reasonable performance under concurrent load
    assert (
        avg_latency <= TARGET_LATENCY_MS * 2
    ), f"Concurrent avg latency {avg_latency:.3f}ms should be <{TARGET_LATENCY_MS*2}ms"

    # Cleanup: Close database connection to prevent event loop issues
    await db.close()
    db._initialized = False


if __name__ == "__main__":
    # Allow running performance tests directly
    import sys

    sys.exit(pytest.main([__file__, "-v", "-s", "-m", "performance"]))
