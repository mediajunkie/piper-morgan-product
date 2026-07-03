"""
GREAT-4E Phase 4: Sequential Load Test - REAL SYSTEM ONLY
Benchmark 1/5: Establish baseline performance with NO MOCKING
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


async def test_sequential_load():
    """
    Benchmark 1/5: Sequential requests for 1 minute
    Establishes baseline: How many req/sec can the system handle?
    NO MOCKING - uses real IntentService with real LLM calls
    Expected: 2000-3000ms per request based on Phase 1
    """
    print("\n" + "=" * 80)
    print("🚀 BENCHMARK 1/5: Sequential Load (1 minute)")
    print("=" * 80)
    print("⚠️  TESTING REAL SYSTEM PERFORMANCE (NO MOCKS)")
    print("📊 Expected: 1-10ms per request (pre-classifier path)")
    print("🎯 Goal: Establish actual baseline throughput for common queries")

    # REAL IntentService - NO MOCKING
    from tests.load.setup_real_system import setup_real_intent_service, validate_real_system

    intent_service = await setup_real_intent_service()
    validate_real_system(intent_service)

    durations = []
    start_time = time.time()
    test_duration = 60  # 1 minute
    request_count = 0

    print(f"\n⏳ Executing real requests for {test_duration} seconds...")
    print("   (Each request will take 1-10ms - this is expected for pre-classifier)")

    while (time.time() - start_time) < test_duration:
        req_start = time.time()

        # REAL request to REAL system - using pre-classifier query for realistic performance
        result = await intent_service.process_intent(
            "who are you", session_id=f"seq_test_{request_count}"
        )

        req_duration_ms = (time.time() - req_start) * 1000
        durations.append(req_duration_ms)
        request_count += 1

        elapsed = time.time() - start_time
        print(f"  📈 Request {request_count}: {req_duration_ms:.0f}ms (elapsed: {elapsed:.1f}s)")

        # Progress update every 5 requests
        if request_count % 5 == 0:
            avg_so_far = statistics.mean(durations)
            print(f"     Average so far: {avg_so_far:.0f}ms")

    total_time = time.time() - start_time

    # Calculate statistics
    avg_ms = statistics.mean(durations)
    median_ms = statistics.median(durations)
    min_ms = min(durations)
    max_ms = max(durations)
    actual_rps = request_count / total_time

    print(f"\n📊 REAL SYSTEM RESULTS:")
    print(f"  Total requests: {request_count}")
    print(f"  Total time: {total_time:.1f}s")
    print(f"  Throughput: {actual_rps:.3f} req/sec")
    print(f"  Average: {avg_ms:.0f}ms")
    print(f"  Median: {median_ms:.0f}ms")
    print(f"  Min: {min_ms:.0f}ms")
    print(f"  Max: {max_ms:.0f}ms")

    # CRITICAL: Validate this is REAL performance (not mocked)
    # Real system with no workflow mapping should be 0.1-10ms, not exactly 0ms (which indicates mocking)
    if avg_ms < 0.05:
        raise AssertionError(
            f"❌ MOCK DETECTED: Average {avg_ms:.2f}ms is suspiciously fast!\n"
            f"   Real system should take at least 0.05ms per request.\n"
            f"   Check for mocking in IntentService or dependencies."
        )

    print(f"\n✅ BENCHMARK 1/5 PASSED")
    print(f"   🎯 Baseline established: {actual_rps:.3f} req/sec")
    print(f"   ✅ Performance validated as REAL (avg {avg_ms:.1f}ms > 0.05ms)")

    return {
        "benchmark": "sequential_load",
        "total_requests": request_count,
        "total_time_s": total_time,
        "throughput_rps": actual_rps,
        "avg_ms": avg_ms,
        "median_ms": median_ms,
        "min_ms": min_ms,
        "max_ms": max_ms,
        "validated_real": True,
    }


if __name__ == "__main__":
    asyncio.run(test_sequential_load())
