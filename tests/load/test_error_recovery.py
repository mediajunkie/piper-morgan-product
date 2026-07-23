import pytest

pytestmark = pytest.mark.llm  # #1452: live-pipeline load test — keyed llm lane

"""
GREAT-4E Phase 4: Error Recovery Test - REAL SYSTEM ONLY
Benchmark 5/5: Test error handling under load with NO MOCKING
"""

import asyncio
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.intent.intent_service import IntentService


async def test_error_recovery():
    """
    Benchmark 5/5: System handles errors gracefully
    Mix valid and invalid requests
    Target: No crashes, proper error responses
    NO MOCKING - uses real IntentService
    """
    print("\n" + "=" * 80)
    print("🚀 BENCHMARK 5/5: Error Recovery")
    print("=" * 80)
    print("⚠️  TESTING REAL SYSTEM PERFORMANCE (NO MOCKS)")
    print("📊 Expected: System handles errors gracefully, no crashes")
    print("🎯 Goal: Verify robust error handling under various conditions")

    # REAL IntentService - NO MOCKING
    intent_service = IntentService()

    # Mix of valid and potentially problematic requests
    test_cases = [
        ("valid_temporal", "What's on my calendar?"),
        ("valid_status", "What am I working on?"),
        ("valid_priority", "What's my top priority?"),
        ("empty_string", ""),
        ("very_long", "x" * 1000),  # Very long input
        ("special_chars", "!@#$%^&*()_+{}|:<>?[]\\;'\",./ ñáéíóú"),
        ("sql_injection_attempt", "'; DROP TABLE users; --"),
        ("unicode_mixed", "Hello 世界 🌍 مرحبا"),
        ("whitespace_only", "   \t\n   "),
        ("numbers_only", "12345678901234567890"),
    ]

    print(f"\n⏳ Testing error handling with {len(test_cases)} different scenarios...")

    results = []

    for i, (test_type, query) in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}/{len(test_cases)}: {test_type}")
        print(f"   Query: {repr(query[:50])}")

        try:
            start = time.time()

            # REAL request to REAL system
            result = await intent_service.process_intent(
                query, session_id=f"error_test_{test_type}"
            )

            duration_ms = (time.time() - start) * 1000

            # Should not crash and should return a result
            assert result is not None, f"Result was None for {test_type}"
            assert hasattr(result, "message"), f"Result missing message for {test_type}"
            assert hasattr(result, "success"), f"Result missing success for {test_type}"

            # Log the result
            success_status = "✅" if result.success else "⚠️"
            print(f"   {success_status} Handled gracefully ({duration_ms:.0f}ms)")
            print(f"   Response: {result.message[:100]}...")

            results.append(
                {
                    "test_type": test_type,
                    "query": query,
                    "duration_ms": duration_ms,
                    "success": result.success,
                    "message": result.message,
                    "crashed": False,
                }
            )

        except Exception as e:
            print(f"   ❌ SYSTEM CRASHED: {str(e)[:100]}...")
            results.append(
                {
                    "test_type": test_type,
                    "query": query,
                    "duration_ms": 0,
                    "success": False,
                    "message": str(e),
                    "crashed": True,
                }
            )

            # This is a failure - system should not crash
            raise AssertionError(
                f"System crashed on {test_type} with query: {repr(query)}\n"
                f"Error: {e}\n"
                f"System must handle all inputs gracefully without crashing."
            )

    # Analyze results
    total_tests = len(results)
    crashed_tests = sum(1 for r in results if r["crashed"])
    successful_responses = sum(1 for r in results if r["success"] and not r["crashed"])
    handled_gracefully = sum(1 for r in results if not r["crashed"])

    avg_duration = sum(r["duration_ms"] for r in results if not r["crashed"]) / max(
        1, handled_gracefully
    )

    print(f"\n📊 ERROR RECOVERY RESULTS:")
    print(f"  Total test cases: {total_tests}")
    print(
        f"  Handled gracefully: {handled_gracefully}/{total_tests} ({(handled_gracefully/total_tests)*100:.1f}%)"
    )
    print(
        f"  Successful responses: {successful_responses}/{total_tests} ({(successful_responses/total_tests)*100:.1f}%)"
    )
    print(f"  System crashes: {crashed_tests}/{total_tests}")
    print(f"  Average response time: {avg_duration:.0f}ms")

    # Verify no crashes occurred
    success = crashed_tests == 0

    if success:
        print(f"\n✅ BENCHMARK 5/5 PASSED")
        print(f"   🎯 Error handling working correctly")
        print(f"   ✅ No system crashes detected")
        print(f"   ✅ All inputs handled gracefully")
        print(f"   ✅ Performance validated as REAL (avg {avg_duration:.0f}ms)")
    else:
        print(f"\n❌ BENCHMARK 5/5 FAILED")
        print(f"   ❌ {crashed_tests} system crashes detected")
        print(f"   ⚠️  System must handle all inputs without crashing")

    return {
        "benchmark": "error_recovery",
        "total_tests": total_tests,
        "handled_gracefully": handled_gracefully,
        "successful_responses": successful_responses,
        "crashed_tests": crashed_tests,
        "avg_duration_ms": avg_duration,
        "success_rate": handled_gracefully / total_tests,
        "validated_real": True,
        "results": results,
    }


if __name__ == "__main__":
    asyncio.run(test_error_recovery())
