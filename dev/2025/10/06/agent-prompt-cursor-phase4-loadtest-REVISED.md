# Prompt for Cursor Agent: GREAT-4E Phase 4 - Load Testing (REVISED - NO MOCKS)

## Context

Phase 3 complete: All 126 tests passing (100% coverage)

**CRITICAL ISSUE DISCOVERED**: Initial Phase 4 attempt used mocks, producing fake 1ms response times instead of real 2000-3000ms performance from Phase 1.

**This revision**: REQUIRES testing the REAL system with NO mocking

## Session Log

Continue: `dev/2025/10/06/2025-10-06-0752-prog-cursor-log.md`

Add note: "Phase 4 restarted - original attempt used mocks, invalidating results"

## Mission

Create load tests using the ACTUAL system (no mocks) to discover real-world performance capabilities and limits.

---

## CRITICAL: NO MOCKING ALLOWED

**STOP if you see any of these:**
```python
from unittest.mock import Mock, patch, MagicMock  # ❌ FORBIDDEN
@patch('services.intent...')  # ❌ FORBIDDEN
mock_classify = Mock()  # ❌ FORBIDDEN
```

**ONLY use real components:**
```python
from services.intent.intent_service import IntentService  # ✅ REAL
from services.intent_service.classifier import classify  # ✅ REAL
intent_service = IntentService()  # ✅ REAL INSTANCE
result = await intent_service.process(intent, session_id)  # ✅ REAL CALL
```

If you find yourself wanting to mock something, STOP and report to PM that the component needs to be made testable without mocking.

---

## Revised Understanding from Phase 1

**Real performance characteristics:**
- LLM classification: 2000-3000ms per request
- Cached responses: 0.1-0.3ms
- System is **inherently slow** due to LLM calls
- This is EXPECTED and OK

**Original benchmarks were unrealistic** - they assumed <100ms responses, but real system takes 2000-3000ms. We need to adjust benchmarks to reality.

---

## Phase 4: Realistic Load Testing (5 Benchmarks)

### Revised Benchmark Targets

Based on Phase 1 findings (2000-3000ms per request):

1. **Sequential Load**: 1 req at a time, sustained for 1 minute
   - Measures: Throughput, consistency
   - No target RPS (limited by LLM speed)

2. **Concurrent Load**: 5 concurrent requests
   - Measures: System handles parallelism
   - Expected: ~5 req every 2-3 seconds

3. **Cache Effectiveness**: Repeated queries
   - Measures: Cache hit speedup
   - Target: >100x speedup (2000ms → <20ms)

4. **Memory Stability**: Sustained load for 5 minutes
   - Measures: Memory leaks
   - Target: <50MB growth

5. **Error Recovery**: System handles failures gracefully
   - Measures: Error handling under load

### Benchmark 1: Sequential Load (Baseline)

Create: `tests/load/test_sequential_load.py`

```python
"""Sequential load test - establish baseline performance"""
import asyncio
import time
import statistics
from services.intent.intent_service import IntentService
from services.intent_service.classifier import Intent, IntentCategory


async def test_sequential_load():
    """
    Benchmark 1/5: Sequential requests for 1 minute
    Establishes baseline: How many req/sec can the system handle?
    NO MOCKING - uses real IntentService with real LLM calls
    """
    print("\n" + "="*80)
    print("Benchmark 1/5: Sequential Load (1 minute)")
    print("="*80)
    print("Testing REAL system performance (no mocks)")
    print("Expected: 2000-3000ms per request based on Phase 1")

    intent_service = IntentService()

    durations = []
    start_time = time.time()
    test_duration = 60  # 1 minute
    request_count = 0

    print("\nExecuting requests...")

    while (time.time() - start_time) < test_duration:
        intent = Intent(
            text="What's on my calendar?",
            original_message="What's on my calendar?",
            category=IntentCategory.TEMPORAL,
            action="calendar_query",
            confidence=0.95,
            context={}
        )

        req_start = time.time()
        result = await intent_service.process(
            intent,
            session_id=f"seq_test_{request_count}"
        )
        req_duration_ms = (time.time() - req_start) * 1000

        durations.append(req_duration_ms)
        request_count += 1

        if request_count % 5 == 0:
            elapsed = time.time() - start_time
            print(f"  {request_count} requests in {elapsed:.1f}s (avg: {req_duration_ms:.0f}ms)")

    total_time = time.time() - start_time

    # Calculate statistics
    avg_ms = statistics.mean(durations)
    median_ms = statistics.median(durations)
    min_ms = min(durations)
    max_ms = max(durations)
    actual_rps = request_count / total_time

    print(f"\nResults:")
    print(f"  Total requests: {request_count}")
    print(f"  Total time: {total_time:.1f}s")
    print(f"  Throughput: {actual_rps:.2f} req/sec")
    print(f"  Average: {avg_ms:.0f}ms")
    print(f"  Median: {median_ms:.0f}ms")
    print(f"  Min: {min_ms:.0f}ms")
    print(f"  Max: {max_ms:.0f}ms")

    # Validate this is REAL performance (not mocked)
    assert avg_ms > 100, \
        f"Average {avg_ms:.0f}ms is suspiciously fast - check for mocking"

    print(f"\n✅ Benchmark 1/5 PASSED")
    print(f"   Baseline established: {actual_rps:.2f} req/sec")

    return actual_rps


if __name__ == "__main__":
    asyncio.run(test_sequential_load())
```

### Benchmark 2: Concurrent Load

Create: `tests/load/test_concurrent_load.py`

```python
"""Concurrent load test - multiple simultaneous requests"""
import asyncio
import time
import statistics
from services.intent.intent_service import IntentService
from services.intent_service.classifier import Intent, IntentCategory


async def concurrent_request(intent_service: IntentService, request_id: int):
    """Single concurrent request."""
    intent = Intent(
        text=f"Request {request_id}",
        original_message=f"Request {request_id}",
        category=IntentCategory.QUERY,
        action="general_query",
        confidence=0.95,
        context={}
    )

    start = time.time()
    result = await intent_service.process(
        intent,
        session_id=f"concurrent_{request_id}"
    )
    duration_ms = (time.time() - start) * 1000

    return duration_ms


async def test_concurrent_load():
    """
    Benchmark 2/5: 5 concurrent requests, repeated 10 times
    Tests if system handles parallelism correctly
    NO MOCKING - uses real IntentService
    """
    print("\n" + "="*80)
    print("Benchmark 2/5: Concurrent Load (5 concurrent × 10 batches)")
    print("="*80)

    intent_service = IntentService()

    concurrency = 5
    batches = 10

    all_durations = []
    batch_times = []

    print(f"\nExecuting {batches} batches of {concurrency} concurrent requests...")

    for batch in range(batches):
        batch_start = time.time()

        # Launch concurrent requests
        tasks = [
            concurrent_request(intent_service, batch * concurrency + i)
            for i in range(concurrency)
        ]

        durations = await asyncio.gather(*tasks)
        all_durations.extend(durations)

        batch_time = time.time() - batch_start
        batch_times.append(batch_time)

        print(f"  Batch {batch+1}: {batch_time:.2f}s")

    # Calculate statistics
    avg_request_ms = statistics.mean(all_durations)
    avg_batch_time = statistics.mean(batch_times)
    effective_rps = concurrency / avg_batch_time

    print(f"\nResults:")
    print(f"  Total requests: {len(all_durations)}")
    print(f"  Average request time: {avg_request_ms:.0f}ms")
    print(f"  Average batch time: {avg_batch_time:.2f}s")
    print(f"  Effective throughput: {effective_rps:.2f} req/sec")

    # Validate real performance
    assert avg_request_ms > 100, \
        f"Suspiciously fast ({avg_request_ms:.0f}ms) - check for mocking"

    print(f"\n✅ Benchmark 2/5 PASSED")
    print(f"   Concurrency working: {effective_rps:.2f} req/sec with {concurrency} concurrent")


if __name__ == "__main__":
    asyncio.run(test_concurrent_load())
```

### Benchmark 3: Cache Effectiveness (CRITICAL)

Create: `tests/load/test_cache_effectiveness.py`

```python
"""Cache effectiveness test"""
import asyncio
import time
from services.intent.intent_service import IntentService
from services.intent_service.classifier import Intent, IntentCategory


async def test_cache_effectiveness():
    """
    Benchmark 3/5: Cache hit rate and speedup
    First request: slow (2000-3000ms with LLM)
    Cached requests: fast (<20ms)
    Target: >100x speedup
    NO MOCKING
    """
    print("\n" + "="*80)
    print("Benchmark 3/5: Cache Effectiveness")
    print("="*80)

    intent_service = IntentService()
    test_query = "What's on my calendar today?"

    print("\nFirst request (cache miss - will be slow):")

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
    print(f"  Duration: {first_duration_ms:.0f}ms")

    # Validate this was real (not mocked)
    if first_duration_ms < 100:
        raise AssertionError(
            f"First request was {first_duration_ms:.0f}ms - "
            "suspiciously fast, check for mocking"
        )

    print("\nSubsequent requests (should hit cache - will be fast):")

    cached_durations = []
    for i in range(10):
        start = time.time()
        result = await intent_service.process(intent, session_id="cache_test")
        duration_ms = (time.time() - start) * 1000
        cached_durations.append(duration_ms)
        print(f"  Request {i+1}: {duration_ms:.1f}ms")

    avg_cached_ms = sum(cached_durations) / len(cached_durations)
    speedup = first_duration_ms / avg_cached_ms

    print(f"\nResults:")
    print(f"  First (uncached): {first_duration_ms:.0f}ms")
    print(f"  Cached average: {avg_cached_ms:.1f}ms")
    print(f"  Speedup: {speedup:.0f}x")

    # Verify significant cache benefit
    assert speedup >= 100, \
        f"Cache speedup {speedup:.0f}x below 100x threshold"

    print(f"\n✅ Benchmark 3/5 PASSED")
    print(f"   Cache working: {speedup:.0f}x speedup")


if __name__ == "__main__":
    asyncio.run(test_cache_effectiveness())
```

### Benchmark 4: Memory Stability (Shorter Duration)

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
    Benchmark 4/5: Memory leak detection
    Run for 5 minutes with real requests
    Target: <50MB growth
    NO MOCKING
    """
    print("\n" + "="*80)
    print("Benchmark 4/5: Memory Stability (5 minutes)")
    print("="*80)

    intent_service = IntentService()
    process = psutil.Process(os.getpid())

    initial_memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"Initial memory: {initial_memory_mb:.1f}MB")

    memory_samples = [initial_memory_mb]
    start_time = time.time()

    # Run for 5 minutes
    duration_seconds = 300
    request_count = 0

    print("\nExecuting sustained load...")

    while (time.time() - start_time) < duration_seconds:
        intent = Intent(
            text=f"Request {request_count}",
            original_message=f"Request {request_count}",
            category=IntentCategory.QUERY,
            action="general_query",
            confidence=0.95,
            context={}
        )

        await intent_service.process(
            intent,
            session_id=f"mem_test_{request_count % 100}"
        )
        request_count += 1

        # Sample memory every minute
        elapsed = time.time() - start_time
        if request_count % 10 == 0:
            current_memory_mb = process.memory_info().rss / 1024 / 1024
            memory_samples.append(current_memory_mb)

            if int(elapsed) % 60 == 0:
                minutes = int(elapsed / 60)
                increase = current_memory_mb - initial_memory_mb
                print(f"  {minutes} min: {current_memory_mb:.1f}MB (+{increase:.1f}MB), {request_count} requests")

    final_memory_mb = process.memory_info().rss / 1024 / 1024
    memory_increase_mb = final_memory_mb - initial_memory_mb

    print(f"\nResults:")
    print(f"  Initial: {initial_memory_mb:.1f}MB")
    print(f"  Final: {final_memory_mb:.1f}MB")
    print(f"  Increase: {memory_increase_mb:.1f}MB")
    print(f"  Total requests: {request_count}")

    # Verify no major leak
    assert memory_increase_mb < 50, \
        f"Memory increased {memory_increase_mb:.1f}MB (potential leak)"

    print(f"\n✅ Benchmark 4/5 PASSED")
    print(f"   No memory leak detected")


if __name__ == "__main__":
    asyncio.run(test_memory_stability())
```

### Benchmark 5: Error Recovery

Create: `tests/load/test_error_recovery.py`

```python
"""Error recovery under load"""
import asyncio
import time
from services.intent.intent_service import IntentService
from services.intent_service.classifier import Intent, IntentCategory


async def test_error_recovery():
    """
    Benchmark 5/5: System handles errors gracefully
    Mix valid and invalid requests
    Target: No crashes, proper error responses
    NO MOCKING
    """
    print("\n" + "="*80)
    print("Benchmark 5/5: Error Recovery")
    print("="*80)

    intent_service = IntentService()

    # Mix of valid and invalid requests
    test_cases = [
        ("valid", Intent(
            text="What's on my calendar?",
            original_message="What's on my calendar?",
            category=IntentCategory.TEMPORAL,
            action="calendar_query",
            confidence=0.95,
            context={}
        )),
        ("invalid_empty", Intent(
            text="",
            original_message="",
            category=IntentCategory.UNKNOWN,
            action="invalid",
            confidence=0.0,
            context={}
        )),
        ("invalid_action", Intent(
            text="Test",
            original_message="Test",
            category=IntentCategory.QUERY,
            action="nonexistent_action",
            confidence=0.95,
            context={}
        )),
    ]

    print("\nTesting error handling...")

    for test_type, intent in test_cases:
        try:
            start = time.time()
            result = await intent_service.process(
                intent,
                session_id=f"error_test_{test_type}"
            )
            duration_ms = (time.time() - start) * 1000

            # Should not crash
            assert result is not None
            assert hasattr(result, 'message')

            print(f"  {test_type}: handled gracefully ({duration_ms:.0f}ms)")

        except Exception as e:
            raise AssertionError(
                f"System crashed on {test_type}: {e}"
            )

    print(f"\n✅ Benchmark 5/5 PASSED")
    print(f"   Error handling working correctly")


if __name__ == "__main__":
    asyncio.run(test_error_recovery())
```

---

## Load Test Report

Create: `dev/2025/10/06/load-test-report.md`

Document ACTUAL performance findings, not idealized targets.

---

## Success Criteria

- [ ] All 5 benchmarks use REAL system (no mocks)
- [ ] All 5 benchmarks passing
- [ ] Performance numbers realistic (>100ms avg)
- [ ] Load test report with actual findings
- [ ] Session log notes Phase 4 restart reason

---

## If Benchmarks Fail

That's OK! The goal is discovering actual capabilities, not passing arbitrary targets.

If real system can't handle 100 req/sec, that's valuable information. Document actual throughput and recommend optimizations if needed.

---

**Effort**: Medium (~1 hour including 5-min memory test)
**Priority**: CRITICAL (must use real system)
**Deliverables**: 5 realistic load tests + honest report
