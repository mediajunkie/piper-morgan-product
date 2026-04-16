#!/usr/bin/env python3
"""
PM-033d Phase 4 - Complete Integration Test Suite

Comprehensive validation of all Phase 4 components working together:
1. Database Scenario Testing
2. Performance Measurement
3. Chain-of-Draft Implementation
4. Kind Communication Wrapper
5. Excellence Flywheel Integration
"""

import asyncio
import sys
import time
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.domain.models import Intent
from services.orchestration.chain_of_draft import ChainOfDraftExperiment
from services.orchestration.excellence_flywheel_integration import ExcellenceFlywheelIntegrator
from services.orchestration.kind_communication import KindCommunicationWrapper
from services.orchestration.multi_agent_coordinator import MultiAgentCoordinator
from services.shared_types import IntentCategory


async def run_phase4_integration_test():
    """Run complete Phase 4 integration test"""

    print("🚀 PM-033d PHASE 4 - COMPLETE INTEGRATION TEST")
    print("=" * 60)
    print(f'Start Time: {datetime.now().strftime("%H:%M:%S")}')
    print("Testing all 5 Phase 4 components in integrated workflow...\n")

    integration_start = time.time()

    # Initialize all components
    print("🔧 COMPONENT INITIALIZATION")
    print("-" * 30)

    coordinator = MultiAgentCoordinator()
    chain_experiment = ChainOfDraftExperiment()
    kind_wrapper = KindCommunicationWrapper()
    flywheel_integrator = ExcellenceFlywheelIntegrator()

    print("✅ MultiAgentCoordinator initialized")
    print("✅ ChainOfDraftExperiment initialized")
    print("✅ KindCommunicationWrapper initialized")
    print("✅ ExcellenceFlywheelIntegrator initialized")

    # Create test intent for end-to-end workflow
    test_intent = Intent(
        category=IntentCategory.EXECUTION,
        action="implement_microservice_architecture",
        original_message="Implement complete microservice architecture with API gateway, service discovery, database layer, monitoring, and comprehensive testing",
        confidence=0.98,
    )

    print(f"\n🎯 TEST INTENT: {test_intent.action}")
    print(f"Complexity: High | Confidence: {test_intent.confidence}")

    results = {}

    # Phase 4.1: Database Scenario Testing (Performance baseline)
    print(f"\n📊 PHASE 4.1: Database Scenario Testing")
    print("-" * 40)

    db_start = time.time()
    coordination_result = await coordinator.coordinate_task(test_intent)
    db_time_ms = int((time.time() - db_start) * 1000)

    print(f"✅ Database scenario coordination: {coordination_result.status.value}")
    print(f"   Duration: {db_time_ms}ms")
    print(f"   Subtasks: {len(coordination_result.subtasks)}")
    print(f"   Success Rate: {coordination_result.success_rate}")

    results["database_testing"] = {
        "status": coordination_result.status.value,
        "duration_ms": db_time_ms,
        "subtasks": len(coordination_result.subtasks),
        "success_rate": coordination_result.success_rate,
    }

    # Phase 4.2: Performance Measurement (Benchmark coordination)
    print(f"\n⚡ PHASE 4.2: Performance Measurement")
    print("-" * 40)

    performance_runs = []
    for run in range(5):
        perf_start = time.time()
        perf_result = await coordinator.coordinate_task(test_intent)
        perf_time_ms = int((time.time() - perf_start) * 1000)
        performance_runs.append(perf_time_ms)
        print(f"   Run {run+1}: {perf_time_ms}ms")

    avg_performance = sum(performance_runs) / len(performance_runs)
    max_performance = max(performance_runs)
    min_performance = min(performance_runs)

    print(f"✅ Performance benchmark completed")
    print(f"   Average: {avg_performance:.1f}ms")
    print(f"   Range: {min_performance}ms - {max_performance}ms")
    print(f'   Target (<1000ms): {"✅ PASSED" if avg_performance < 1000 else "❌ FAILED"}')

    results["performance_testing"] = {
        "avg_duration_ms": avg_performance,
        "min_duration_ms": min_performance,
        "max_duration_ms": max_performance,
        "target_met": avg_performance < 1000,
        "runs": performance_runs,
    }

    # Phase 4.3: Chain-of-Draft Implementation
    print(f"\n🔄 PHASE 4.3: Chain-of-Draft Implementation")
    print("-" * 45)

    draft_start = time.time()
    draft_result = await chain_experiment.run_draft_experiment(test_intent)
    draft_time_ms = int((time.time() - draft_start) * 1000)

    print(f'✅ Chain-of-Draft experiment: {"SUCCESSFUL" if draft_result.success else "FAILED"}')
    print(f"   Drafts: {len(draft_result.drafts)}")
    print(f"   Best Quality: {draft_result.best_draft.quality_score:.2f}")
    if draft_result.draft_comparison:
        print(f"   Improvement: {draft_result.draft_comparison.improvement_percentage:.1f}%")
        print(f"   Learning Insights: {len(draft_result.draft_comparison.learning_insights)}")
    print(f"   Total Time: {draft_time_ms}ms")

    results["chain_of_draft"] = {
        "success": draft_result.success,
        "draft_count": len(draft_result.drafts),
        "best_quality": draft_result.best_draft.quality_score,
        "improvement_percentage": (
            draft_result.draft_comparison.improvement_percentage
            if draft_result.draft_comparison
            else 0.0
        ),
        "duration_ms": draft_time_ms,
    }

    # Phase 4.4: Kind Communication Wrapper
    print(f"\n💬 PHASE 4.4: Kind Communication Wrapper")
    print("-" * 42)

    comm_start = time.time()
    kind_message = await kind_wrapper.wrap_coordination_result(coordination_result, test_intent)
    formatted_message = await kind_wrapper.format_message_for_display(kind_message)
    comm_time_ms = int((time.time() - comm_start) * 1000)

    print(f"✅ Kind communication generated")
    print(f"   Message Type: {kind_message.message_type.value}")
    print(f"   Tone: {kind_message.tone.value}")
    print(f"   Details Count: {len(kind_message.details)}")
    print(f"   Action Items: {len(kind_message.action_items)}")
    print(f"   Has Encouragement: {kind_message.encouragement is not None}")
    print(f"   Generation Time: {comm_time_ms}ms")

    # Show sample of formatted message
    print(f"\n   📝 Sample Output (first 100 chars):")
    print(f'   "{formatted_message[:100]}..."')

    results["kind_communication"] = {
        "message_type": kind_message.message_type.value,
        "tone": kind_message.tone.value,
        "details_count": len(kind_message.details),
        "action_items_count": len(kind_message.action_items),
        "has_encouragement": kind_message.encouragement is not None,
        "generation_time_ms": comm_time_ms,
    }

    # Phase 4.5: Excellence Flywheel Integration
    print(f"\n🔄 PHASE 4.5: Excellence Flywheel Integration")
    print("-" * 47)

    flywheel_start = time.time()
    (
        flywheel_coord_result,
        flywheel_tracking,
    ) = await flywheel_integrator.coordinate_with_excellence_flywheel(test_intent)
    flywheel_time_ms = int((time.time() - flywheel_start) * 1000)

    print(f"✅ Excellence Flywheel coordination: {flywheel_coord_result.status.value}")
    print(f"   Systematic Verified: {flywheel_tracking.systematic_verified}")
    print(f"   Verification Checks: {len(flywheel_tracking.verification_checks)}")

    passed_checks = len(
        [c for c in flywheel_tracking.verification_checks if c.result.value == "passed"]
    )
    print(f"   Checks Passed: {passed_checks}/{len(flywheel_tracking.verification_checks)}")
    print(f"   Learning Insights: {len(flywheel_tracking.learning_insights)}")
    print(f"   Patterns Detected: {len(flywheel_tracking.patterns_detected)}")
    print(f"   Flywheel Time: {flywheel_time_ms}ms")

    results["excellence_flywheel"] = {
        "coordination_status": flywheel_coord_result.status.value,
        "systematic_verified": flywheel_tracking.systematic_verified,
        "total_checks": len(flywheel_tracking.verification_checks),
        "passed_checks": passed_checks,
        "learning_insights_count": len(flywheel_tracking.learning_insights),
        "patterns_detected_count": len(flywheel_tracking.patterns_detected),
        "duration_ms": flywheel_time_ms,
    }

    # Integration Test Summary
    total_integration_time = int((time.time() - integration_start) * 1000)

    print(f"\n" + "=" * 60)
    print("🏆 PHASE 4 INTEGRATION TEST SUMMARY")
    print("=" * 60)

    # Overall performance metrics
    print(f"📊 OVERALL PERFORMANCE:")
    print(f"   Total Integration Time: {total_integration_time}ms")
    print(f"   Average Component Time: {total_integration_time/5:.1f}ms per component")

    # Component-by-component success validation
    print(f"\n✅ COMPONENT VALIDATION:")

    validation_results = {
        "Database Testing": results["database_testing"]["success_rate"] == 1.0,
        "Performance Testing": results["performance_testing"]["target_met"],
        "Chain-of-Draft": results["chain_of_draft"]["success"],
        "Kind Communication": results["kind_communication"]["details_count"] > 0,
        "Excellence Flywheel": results["excellence_flywheel"]["systematic_verified"],
    }

    for component, passed in validation_results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {component}: {status}")

    # Integration quality metrics
    print(f"\n📈 INTEGRATION QUALITY METRICS:")

    # Performance consistency
    performance_consistency = (
        results["performance_testing"]["max_duration_ms"]
        - results["performance_testing"]["min_duration_ms"]
    ) <= 100
    print(
        f'   Performance Consistency (<100ms variance): {"✅" if performance_consistency else "❌"}'
    )

    # Component speed (all under 1000ms)
    all_fast = all(
        [
            results["database_testing"]["duration_ms"] < 1000,
            results["performance_testing"]["avg_duration_ms"] < 1000,
            results["chain_of_draft"]["duration_ms"] < 5000,  # Chain-of-Draft has higher threshold
            results["kind_communication"]["generation_time_ms"] < 1000,
            results["excellence_flywheel"]["duration_ms"] < 1000,
        ]
    )
    print(f'   All Components Fast: {"✅" if all_fast else "❌"}')

    # Quality threshold
    high_quality = all(
        [
            results["chain_of_draft"]["best_quality"] >= 0.8,
            results["excellence_flywheel"]["passed_checks"] >= 7,
            results["kind_communication"]["has_encouragement"],
        ]
    )
    print(f'   High Quality Outputs: {"✅" if high_quality else "❌"}')

    # Overall integration success
    overall_success = (
        all(validation_results.values()) and performance_consistency and all_fast and high_quality
    )

    print(f'\n🎯 OVERALL PHASE 4 INTEGRATION: {"✅ SUCCESS" if overall_success else "❌ FAILED"}')

    if overall_success:
        print(f"\n🎉 PHASE 4 INTEGRATION TESTING COMPLETE!")
        print(f"   ✨ All 5 components working seamlessly together")
        print(f"   ⚡ Performance targets met across all scenarios")
        print(f"   🔄 Excellence Flywheel systematic verification operational")
        print(f"   💬 Human-friendly communication system active")
        print(f"   🧪 Chain-of-Draft experimentation validated")
        print(f"   📊 Database integration with fallback resilience confirmed")

    print(f'\nEnd Time: {datetime.now().strftime("%H:%M:%S")}')
    print(f"Total Duration: {total_integration_time/1000:.1f} seconds")

    return {
        "overall_success": overall_success,
        "total_duration_ms": total_integration_time,
        "component_results": results,
        "validation_results": validation_results,
        "quality_metrics": {
            "performance_consistency": performance_consistency,
            "all_components_fast": all_fast,
            "high_quality_outputs": high_quality,
        },
    }


if __name__ == "__main__":
    # Run Phase 4 integration test
    result = asyncio.run(run_phase4_integration_test())

    if result["overall_success"]:
        print(f"\n🏆 PM-033d Phase 4 Integration Test: SUCCESS")
        exit(0)
    else:
        print(f"\n❌ PM-033d Phase 4 Integration Test: FAILED")
        exit(1)
