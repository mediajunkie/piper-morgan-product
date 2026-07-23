import pytest

pytestmark = pytest.mark.llm  # #1452: live-pipeline load test — keyed llm lane

"""
GREAT-4E Phase 4: Memory Stability Test - REAL SYSTEM ONLY
Benchmark 4/5: Detect memory leaks with NO MOCKING
"""

import asyncio
import os
import sys
import time
from pathlib import Path

import psutil

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.intent.intent_service import IntentService


async def test_memory_stability():
    """
    Benchmark 4/5: Memory leak detection
    Run for 5 minutes with real requests
    Target: <50MB growth
    NO MOCKING - uses real IntentService with real LLM calls
    """
    print("\n" + "=" * 80)
    print("🚀 BENCHMARK 4/5: Memory Stability (5 minutes)")
    print("=" * 80)
    print("⚠️  TESTING REAL SYSTEM PERFORMANCE (NO MOCKS)")
    print("📊 Expected: Each request takes 2-3 seconds")
    print("🎯 Goal: Detect memory leaks over sustained load")

    # REAL IntentService - NO MOCKING
    intent_service = IntentService()
    process = psutil.Process(os.getpid())

    initial_memory_mb = process.memory_info().rss / 1024 / 1024
    print(f"\n📊 Initial memory: {initial_memory_mb:.1f}MB")

    memory_samples = [initial_memory_mb]
    start_time = time.time()

    # Run for 5 minutes
    duration_seconds = 300  # 5 minutes
    request_count = 0

    print(f"\n⏳ Executing sustained load for {duration_seconds//60} minutes...")
    print("   Each request will take 2-3 seconds - this is expected")
    print("   Memory will be sampled every 10 requests")

    # Variety of queries to test different code paths
    queries = [
        "What's on my calendar?",
        "What am I working on?",
        "What's my priority?",
        "Who are you?",
        "What should I focus on?",
        "Show me my projects",
        "Hello there",
    ]

    while (time.time() - start_time) < duration_seconds:
        query = queries[request_count % len(queries)]

        req_start = time.time()

        # REAL request to REAL system
        result = await intent_service.process_intent(
            f"{query} {request_count}", session_id=f"mem_test_{request_count % 100}"
        )

        req_duration_ms = (time.time() - req_start) * 1000
        request_count += 1

        # Sample memory every 10 requests
        if request_count % 10 == 0:
            current_memory_mb = process.memory_info().rss / 1024 / 1024
            memory_samples.append(current_memory_mb)

            elapsed = time.time() - start_time
            increase = current_memory_mb - initial_memory_mb

            print(
                f"  📊 {elapsed:.0f}s: {current_memory_mb:.1f}MB (+{increase:+.1f}MB) | "
                f"{request_count} requests | Last: {req_duration_ms:.0f}ms"
            )

            # Progress update every minute
            if int(elapsed) % 60 == 0 and elapsed > 0:
                minutes = int(elapsed / 60)
                rate = request_count / elapsed
                print(f"     🕐 {minutes} minute(s) complete - Rate: {rate:.3f} req/sec")

    final_memory_mb = process.memory_info().rss / 1024 / 1024
    memory_increase_mb = final_memory_mb - initial_memory_mb
    total_time = time.time() - start_time

    # Calculate memory trend
    if len(memory_samples) > 2:
        avg_increase_per_sample = sum(
            memory_samples[i] - memory_samples[i - 1] for i in range(1, len(memory_samples))
        ) / (len(memory_samples) - 1)
    else:
        avg_increase_per_sample = 0

    print(f"\n📊 MEMORY STABILITY RESULTS:")
    print(f"  Test duration: {total_time/60:.1f} minutes")
    print(f"  Total requests: {request_count}")
    print(f"  Request rate: {request_count/total_time:.3f} req/sec")
    print(f"  Initial memory: {initial_memory_mb:.1f}MB")
    print(f"  Final memory: {final_memory_mb:.1f}MB")
    print(
        f"  Memory increase: {memory_increase_mb:+.1f}MB ({(memory_increase_mb/initial_memory_mb)*100:+.1f}%)"
    )
    print(f"  Avg increase/sample: {avg_increase_per_sample:+.2f}MB")
    print(f"  Memory samples: {len(memory_samples)}")

    # Verify no major leak
    threshold_mb = 50
    success = memory_increase_mb < threshold_mb

    if success:
        print(f"\n✅ BENCHMARK 4/5 PASSED")
        print(f"   🎯 No memory leak detected")
        print(f"   ✅ Memory increase {memory_increase_mb:+.1f}MB < {threshold_mb}MB threshold")
        print(f"   ✅ Performance validated as REAL ({request_count/total_time:.3f} req/sec)")
    else:
        print(f"\n❌ BENCHMARK 4/5 FAILED")
        print(f"   ❌ Memory increase {memory_increase_mb:+.1f}MB >= {threshold_mb}MB threshold")
        print(f"   ⚠️  Potential memory leak detected")

    assert success, f"Memory increased {memory_increase_mb:.1f}MB (potential leak)"

    return {
        "benchmark": "memory_stability",
        "duration_minutes": total_time / 60,
        "total_requests": request_count,
        "request_rate_rps": request_count / total_time,
        "initial_memory_mb": initial_memory_mb,
        "final_memory_mb": final_memory_mb,
        "memory_increase_mb": memory_increase_mb,
        "memory_increase_pct": (memory_increase_mb / initial_memory_mb) * 100,
        "threshold_mb": threshold_mb,
        "validated_real": True,
    }


if __name__ == "__main__":
    asyncio.run(test_memory_stability())
