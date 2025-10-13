# Prompt for Cursor Agent: GREAT-4E Phase 4 - Load Testing

## Context

Phase 3 complete: All 126 tests passing (100% coverage)

**This is Phase 4**: Load testing to verify performance under realistic traffic

## Session Log

Continue: `dev/2025/10/06/2025-10-06-0752-prog-cursor-log.md`

## Mission

Create load tests to validate system performance under varying loads:
1. 100 req/sec: Maintain <100ms response time
2. 500 req/sec: Maintain <200ms response time
3. 1000 req/sec: Maintain <500ms response time
4. Cache effectiveness: >80% hit rate
5. Memory stability: No leaks over 10-minute test

---

## Phase 4: Load Testing (5 Benchmarks)

### Tool Selection

Check what's available:

```bash
# Check for locust
pip list | grep locust

# Check for k6
which k6

# Check for pytest-benchmark
pip list | grep pytest-benchmark

# If none available, use asyncio for simple load test
```

**Recommended**: Use Python asyncio for simple load testing since we already have the test infrastructure.

### Benchmark 1: Low Load (100 req/sec)

Create: `tests/load/test_load_100rps.py`

```python
"""Load test: 100 requests/second"""
import asyncio
import time
import statistics
from services.intent.intent_service import IntentService
from services.intent_service.classifier import Intent, IntentCategory


async def single_request(intent_service: IntentService, request_num: int):
    """Execute a single intent request."""
    intent = Intent(
        text="What's on my calendar?",
        original_message="What's on my calendar?",
        category=IntentCategory.TEMPORAL,
        action="calendar_query",
        confidence=0.95,
        context={}
    )

    start = time.time()
    result = await intent_service.process(intent, session_id=f"load_test_{request_num}")
    duration_ms = (time.time() - start) * 1000

    return duration_ms, result.success


async def test_load_100rps():
    """
    Benchmark 1/5: 100 requests/second for 10 seconds
    Expected: <100ms response time for all requests
    """
    intent_service = IntentService()

    total_requests = 1000  # 100 req/sec * 10 sec
    target_rps = 100
    interval = 1.0 / target_rps  # Time between requests

    print(f"\nStarting load test: {target_rps} req/sec for 10 seconds")
    print(f"Total requests: {total_requests}")
    print(f"Request interval: {interval*1000:.1f}ms")

    results = []
    start_time = time.time()

    for i in range(total_requests):
        # Execute request
        duration_ms, success = await single_request(intent_service, i)
        results.append(duration_ms)

        # Maintain target rate
        elapsed = time.time() - start_time
        expected_time = (i + 1) * interval
        sleep_time = expected_time - elapsed

        if sleep_time > 0:
            await asyncio.sleep(sleep_time)

        # Progress indicator
        if (i + 1) % 100 == 0:
            print(f"  Completed {i+1}/{total_requests} requests")

    # Analyze results
    total_time = time.time() - start_time
    actual_rps = total_requests / total_time

    avg_ms = statistics.mean(results)
    p50_ms = statistics.median(results)
    p95_ms = sorted(results)[int(len(results) * 0.95)]
    p99_ms = sorted(results)[int(len(results) * 0.99)]
    max_ms = max(results)

    print(f"\nResults:")
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Actual RPS: {actual_rps:.1f}")
    print(f"  Average: {avg_ms:.1f}ms")
    print(f"  P50: {p50_ms:.1f}ms")
    print(f"  P95: {p95_ms:.1f}ms")
    print(f"  P99: {p99_ms:.1f}ms")
    print(f"  Max: {max_ms:.1f}ms")

    # Verify benchmark
    assert p95_ms < 100, f"P95 {p95_ms:.1f}ms exceeds 100ms threshold"
    print(f"\n✅ Benchmark 1/5 PASSED: 100 req/sec maintained <100ms")


if __name__ == "__main__":
    asyncio.run(test_load_100rps())
```

### Benchmark 2: Medium Load (500 req/sec)

Create: `tests/load/test_load_500rps.py`

```python
"""Load test: 500 requests/second"""
# Similar structure to 100rps test
# Target: 500 req/sec
# Total: 5000 requests over 10 seconds
# Threshold: <200ms for P95
```

### Benchmark 3: High Load (1000 req/sec)

Create: `tests/load/test_load_1000rps.py`

```python
"""Load test: 1000 requests/second"""
# Similar structure to 100rps test
# Target: 1000 req/sec
# Total: 10000 requests over 10 seconds
# Threshold: <500ms for P95
```

### Benchmark 4: Cache Effectiveness

Create: `tests/load/test_cache_effectiveness.py`

```python
"""Cache effectiveness test"""
import asyncio
import time
from services.intent.intent_service import IntentService
from services.intent_service.classifier import Intent, IntentCategory


async def test_cache_effectiveness():
    """
    Benchmark 4/5: Cache hit rate >80%
    Test repeated requests to verify caching works
    """
    intent_service = IntentService()

    # Test query (should be cached after first call)
    test_query = "What's on my calendar today?"

    print("\nTesting cache effectiveness...")

    # First request (cache miss)
    print("First request (cache miss):")
    intent = Intent(
        text=test_query,
        original_message=test_query,
        category=IntentCategory.TEMPORAL,
        action="calendar_query",
        confidence=0.95,
        context={}
    )

    start = time.time()
    result1 = await intent_service.process(intent, session_id="cache_test")
    first_duration_ms = (time.time() - start) * 1000
    print(f"  Duration: {first_duration_ms:.1f}ms")

    # Subsequent requests (should hit cache)
    print("\nSubsequent requests (should hit cache):")
    cached_durations = []

    for i in range(10):
        start = time.time()
        result = await intent_service.process(intent, session_id="cache_test")
        duration_ms = (time.time() - start) * 1000
        cached_durations.append(duration_ms)
        print(f"  Request {i+1}: {duration_ms:.1f}ms")

    avg_cached_ms = sum(cached_durations) / len(cached_durations)

    # Calculate speedup
    speedup = first_duration_ms / avg_cached_ms

    print(f"\nResults:")
    print(f"  First request: {first_duration_ms:.1f}ms")
    print(f"  Cached average: {avg_cached_ms:.1f}ms")
    print(f"  Speedup: {speedup:.1f}x")

    # Verify cache effectiveness
    # Cached requests should be at least 10x faster
    assert speedup >= 10, f"Cache speedup {speedup:.1f}x below 10x threshold"

    print(f"\n✅ Benchmark 4/5 PASSED: Cache effectiveness verified")


if __name__ == "__main__":
    asyncio.run(test_cache_effectiveness())
```

### Benchmark 5: Memory Stability

Create: `tests/load/test_memory_stability.py`

```python
"""Memory stability test"""
import asyncio
import time
import psutil
import os
from services.intent.intent_service import IntentService
from services.intent_service.classifier import Intent, IntentCategory


async def test_memory_stability():
    """
    Benchmark 5/5: No memory leaks over 10 minutes
    Execute sustained load and monitor memory
    """
    intent_service = IntentService()
    process = psutil.Process(os.getpid())

    print("\nTesting memory stability (10 minute test)...")
    print("Executing 6000 requests (10 req/sec for 10 minutes)")

    # Record initial memory
    initial_memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Initial memory: {initial_memory_mb:.1f}MB")

    memory_samples = [initial_memory_mb]
    start_time = time.time()

    # Run for 10 minutes
    duration_seconds = 600  # 10 minutes
    requests_per_sec = 10
    total_requests = duration_seconds * requests_per_sec

    for i in range(total_requests):
        # Execute request
        intent = Intent(
            text=f"Request {i}",
            original_message=f"Request {i}",
            category=IntentCategory.QUERY,
            action="general_query",
            confidence=0.95,
            context={}
        )

        await intent_service.process(intent, session_id=f"mem_test_{i % 100}")

        # Sample memory every 60 seconds
        elapsed = time.time() - start_time
        if i % 600 == 0 and i > 0:
            current_memory_mb = process.memory_info().rss / 1024 / 1024
            memory_samples.append(current_memory_mb)
            minutes = int(elapsed / 60)
            print(f"  {minutes} min: {current_memory_mb:.1f}MB (+{current_memory_mb - initial_memory_mb:.1f}MB)")

        # Maintain rate
        expected_time = (i + 1) / requests_per_sec
        sleep_time = expected_time - elapsed
        if sleep_time > 0:
            await asyncio.sleep(sleep_time)

    # Final memory check
    final_memory_mb = process.memory_info().rss / 1024 / 1024
    memory_increase_mb = final_memory_mb - initial_memory_mb
    memory_increase_pct = (memory_increase_mb / initial_memory_mb) * 100

    print(f"\nResults:")
    print(f"  Initial memory: {initial_memory_mb:.1f}MB")
    print(f"  Final memory: {final_memory_mb:.1f}MB")
    print(f"  Increase: {memory_increase_mb:.1f}MB ({memory_increase_pct:.1f}%)")
    print(f"  Total requests: {total_requests}")

    # Verify no significant memory leak
    # Allow up to 50MB increase over 10 minutes
    assert memory_increase_mb < 50, \
        f"Memory increased {memory_increase_mb:.1f}MB (potential leak)"

    print(f"\n✅ Benchmark 5/5 PASSED: No memory leaks detected")


if __name__ == "__main__":
    asyncio.run(test_memory_stability())
```

---

## Running the Load Tests

```bash
# Install dependencies if needed
pip install psutil --break-system-packages

# Run each benchmark
PYTHONPATH=. python3 tests/load/test_load_100rps.py
PYTHONPATH=. python3 tests/load/test_load_500rps.py
PYTHONPATH=. python3 tests/load/test_load_1000rps.py
PYTHONPATH=. python3 tests/load/test_cache_effectiveness.py
PYTHONPATH=. python3 tests/load/test_memory_stability.py

# Should see:
# ✅ Benchmark 1/5 PASSED
# ✅ Benchmark 2/5 PASSED
# ✅ Benchmark 3/5 PASSED
# ✅ Benchmark 4/5 PASSED
# ✅ Benchmark 5/5 PASSED
```

---

## Load Test Report

Create: `dev/2025/10/06/load-test-report.md`

```markdown
# GREAT-4E Load Test Report

**Date**: October 6, 2025
**Duration**: ~15 minutes total

## Benchmark Results

### 1. Low Load (100 req/sec)
- Target: <100ms for P95
- Actual: Xms
- Status: PASS/FAIL

### 2. Medium Load (500 req/sec)
- Target: <200ms for P95
- Actual: Xms
- Status: PASS/FAIL

### 3. High Load (1000 req/sec)
- Target: <500ms for P95
- Actual: Xms
- Status: PASS/FAIL

### 4. Cache Effectiveness
- Target: 10x speedup for cached requests
- Actual: Xx speedup
- Status: PASS/FAIL

### 5. Memory Stability
- Target: <50MB increase over 10 minutes
- Actual: XMB increase
- Status: PASS/FAIL

## Summary

Benchmarks passed: X/5
System ready for production load: YES/NO

## Recommendations

[Any performance tuning recommendations]
```

---

## Success Criteria

- [ ] All 5 benchmarks implemented
- [ ] All 5 benchmarks passing
- [ ] Load test report created
- [ ] Session log updated

---

## Critical Notes

- Run benchmarks sequentially (not in parallel)
- Memory test takes 10 minutes - don't interrupt
- If any benchmark fails, investigate before proceeding
- Document actual performance numbers

---

**Effort**: Medium (~1 hour including 10-min memory test)
**Priority**: HIGH (validates production readiness)
**Deliverables**: 5 load tests + report
