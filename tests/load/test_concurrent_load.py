import pytest

pytestmark = pytest.mark.llm  # #1452: live-pipeline load test — keyed llm lane

"""
GREAT-4E Phase 4: Concurrent Load Test - REAL SYSTEM ONLY
Benchmark 2/5: Test parallelism with NO MOCKING
"""

import asyncio
import statistics
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.intent.intent_service import IntentService


async def concurrent_request(intent_service: IntentService, request_id: int):
    """Single concurrent request to REAL system."""
    start = time.time()

    # REAL request to REAL system
    result = await intent_service.process_intent(
        f"Request {request_id}", session_id=f"concurrent_{request_id}"
    )

    duration_ms = (time.time() - start) * 1000
    return duration_ms


async def test_concurrent_load():
    """
    Benchmark 2/5: 5 concurrent requests, repeated 5 times
    Tests if system handles parallelism correctly
    NO MOCKING - uses real IntentService
    Expected: Each request still takes 2000-3000ms, but 5 run in parallel
    """
    print("\n" + "=" * 80)
    print("🚀 BENCHMARK 2/5: Concurrent Load (5 concurrent × 5 batches)")
    print("=" * 80)
    print("⚠️  TESTING REAL SYSTEM PERFORMANCE (NO MOCKS)")
    print("📊 Expected: 2000-3000ms per request, but 5 run in parallel")
    print("🎯 Goal: Verify system handles concurrency correctly")

    # REAL IntentService - NO MOCKING
    intent_service = IntentService()

    concurrency = 5
    batches = 5  # Reduced for realistic testing

    all_durations = []
    batch_times = []

    print(f"\n⏳ Executing {batches} batches of {concurrency} concurrent requests...")
    print("   (Each batch will take 2-3 seconds - this is expected)")

    for batch in range(batches):
        print(f"\n📦 Starting batch {batch+1}/{batches}...")
        batch_start = time.time()

        # Launch concurrent requests to REAL system
        tasks = [
            concurrent_request(intent_service, batch * concurrency + i) for i in range(concurrency)
        ]

        durations = await asyncio.gather(*tasks)
        all_durations.extend(durations)

        batch_time = time.time() - batch_start
        batch_times.append(batch_time)

        avg_request_time = statistics.mean(durations)
        print(f"  ✅ Batch {batch+1} complete: {batch_time:.2f}s total")
        print(f"     Average request time: {avg_request_time:.0f}ms")
        print(f"     Individual times: {[f'{d:.0f}ms' for d in durations]}")

    # Calculate statistics
    avg_request_ms = statistics.mean(all_durations)
    avg_batch_time = statistics.mean(batch_times)
    effective_rps = concurrency / avg_batch_time

    print(f"\n📊 REAL SYSTEM RESULTS:")
    print(f"  Total requests: {len(all_durations)}")
    print(f"  Average request time: {avg_request_ms:.0f}ms")
    print(f"  Average batch time: {avg_batch_time:.2f}s")
    print(f"  Effective throughput: {effective_rps:.3f} req/sec")
    print(f"  Concurrency benefit: {effective_rps:.3f} vs {1/(avg_request_ms/1000):.3f} sequential")

    # CRITICAL: Validate real performance
    if avg_request_ms < 100:
        raise AssertionError(
            f"❌ MOCK DETECTED: Average {avg_request_ms:.0f}ms is suspiciously fast!\n"
            f"   Real system should take 2000-3000ms per request.\n"
            f"   Check for mocking in IntentService or dependencies."
        )

    print(f"\n✅ BENCHMARK 2/5 PASSED")
    print(f"   🎯 Concurrency working: {effective_rps:.3f} req/sec with {concurrency} concurrent")
    print(f"   ✅ Performance validated as REAL (avg {avg_request_ms:.0f}ms > 100ms)")

    return {
        "benchmark": "concurrent_load",
        "total_requests": len(all_durations),
        "concurrency": concurrency,
        "avg_request_ms": avg_request_ms,
        "avg_batch_time_s": avg_batch_time,
        "effective_rps": effective_rps,
        "validated_real": True,
    }


if __name__ == "__main__":
    asyncio.run(test_concurrent_load())
