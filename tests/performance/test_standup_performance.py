"""
Issue #556: STANDUP-PERF - Standup Conversation Performance Benchmarks

This module establishes baseline performance metrics for the standup conversation
system and implements regression tests to ensure performance characteristics are maintained.

Benchmarks measure:
- Turn response time (target: <500ms p95)
- Memory usage across multi-turn conversations
- State machine transition performance
- Preference extraction overhead

Epic: #242 (CONV-MCP-STANDUP-INTERACTIVE)
Issue: #556 (STANDUP-PERF)
Phase: 0 - Profiling & Baseline Establishment
"""

import asyncio
import gc
import statistics
import sys
import time
import tracemalloc
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import pytest

from services.domain.models import StandupConversation
from services.shared_types import StandupConversationState
from services.standup.conversation_handler import ConversationResponse, StandupConversationHandler
from services.standup.conversation_manager import StandupConversationManager

# ============================================================================
# Performance Metrics Collector
# ============================================================================


@dataclass
class StandupPerformanceMetrics:
    """Collector for standup system performance metrics."""

    measurements: Dict[str, List[float]] = field(default_factory=dict)
    memory_samples: List[int] = field(default_factory=list)
    peak_memory: int = 0

    def record(self, operation: str, duration_ms: float) -> None:
        """Record a single timing measurement."""
        if operation not in self.measurements:
            self.measurements[operation] = []
        self.measurements[operation].append(duration_ms)

    def record_memory(self, bytes_used: int) -> None:
        """Record a memory sample."""
        self.memory_samples.append(bytes_used)
        self.peak_memory = max(self.peak_memory, bytes_used)

    def get_stats(self, operation: str) -> Dict[str, float]:
        """Get statistics for an operation."""
        if operation not in self.measurements or not self.measurements[operation]:
            return {}

        latencies = self.measurements[operation]
        return {
            "count": len(latencies),
            "min_ms": min(latencies),
            "max_ms": max(latencies),
            "mean_ms": statistics.mean(latencies),
            "median_ms": statistics.median(latencies),
            "stdev_ms": statistics.stdev(latencies) if len(latencies) > 1 else 0.0,
            "p50_ms": self._percentile(latencies, 50),
            "p95_ms": self._percentile(latencies, 95),
            "p99_ms": self._percentile(latencies, 99),
        }

    def _percentile(self, values: List[float], percentile: int) -> float:
        """Calculate percentile value."""
        if not values:
            return 0.0
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]

    def get_memory_stats(self) -> Dict[str, int]:
        """Get memory usage statistics."""
        if not self.memory_samples:
            return {}
        return {
            "samples": len(self.memory_samples),
            "min_bytes": min(self.memory_samples),
            "max_bytes": max(self.memory_samples),
            "mean_bytes": int(statistics.mean(self.memory_samples)),
            "peak_bytes": self.peak_memory,
            "growth_bytes": (
                self.memory_samples[-1] - self.memory_samples[0]
                if len(self.memory_samples) > 1
                else 0
            ),
        }

    def summary(self) -> Dict[str, Any]:
        """Get summary of all metrics."""
        return {
            "timing": {op: self.get_stats(op) for op in self.measurements.keys()},
            "memory": self.get_memory_stats(),
        }


# ============================================================================
# Performance Targets (from Issue #556 acceptance criteria)
# ============================================================================

PERFORMANCE_TARGETS = {
    # Response time targets (milliseconds)
    "turn_response_p95_ms": 500,  # <500ms per turn (p95)
    "turn_response_p50_ms": 200,  # Ideal p50 target
    "state_transition_max_ms": 10,  # State transitions should be fast
    # Memory targets (bytes)
    "memory_growth_max_bytes": 1024 * 1024,  # Max 1MB growth over 20 turns
    "per_turn_memory_max_bytes": 100 * 1024,  # Max 100KB per turn
}


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def metrics() -> StandupPerformanceMetrics:
    """Create a fresh metrics collector."""
    return StandupPerformanceMetrics()


@pytest.fixture
def manager() -> StandupConversationManager:
    """Create a conversation manager."""
    return StandupConversationManager()


@pytest.fixture
def handler(manager: StandupConversationManager) -> StandupConversationHandler:
    """Create a conversation handler without workflow (pure state machine)."""
    return StandupConversationHandler(
        conversation_manager=manager,
        standup_workflow=None,
    )


@pytest.fixture
async def conversation(manager: StandupConversationManager) -> StandupConversation:
    """Create a test conversation. (#1452: create_conversation went async —
    DB-backed persistence — after this suite was written.)"""
    return await manager.create_conversation(
        user_id="perf-test-user",
        session_id="perf-test-session",
    )


# ============================================================================
# Phase 0: Baseline Profiling Tests
# ============================================================================


class TestTurnResponseTimeBaseline:
    """Establish baseline for turn response times."""

    @pytest.mark.asyncio
    async def test_single_turn_response_time(
        self,
        handler: StandupConversationHandler,
        conversation: StandupConversation,
        metrics: StandupPerformanceMetrics,
    ):
        """Measure single turn response time."""
        start = time.perf_counter()
        response = await handler.handle_turn(
            conversation=conversation,
            user_message="Start my standup",
        )
        elapsed_ms = (time.perf_counter() - start) * 1000

        metrics.record("single_turn", elapsed_ms)
        stats = metrics.get_stats("single_turn")

        # Baseline assertion - just establish that it works
        assert response is not None
        assert isinstance(response, ConversationResponse)
        print(f"\nSingle turn response time: {elapsed_ms:.2f}ms")

    @pytest.mark.asyncio
    async def test_multi_turn_response_times(
        self,
        handler: StandupConversationHandler,
        manager: StandupConversationManager,
        metrics: StandupPerformanceMetrics,
    ):
        """Measure response times across multiple conversation turns."""
        # Create a fresh conversation for multi-turn test
        conversation = await manager.create_conversation(
            user_id="multi-turn-user",
            session_id="multi-turn-session",
        )

        # Simulate a realistic conversation flow
        messages = [
            "Start my standup",  # INITIATED -> response
            "focus on GitHub issues",  # GATHERING -> preferences
            "skip documentation updates",  # More preferences
            "that's all my preferences",  # Ready to generate
        ]

        for i, message in enumerate(messages):
            # #1452: refresh per turn — the live caller (process/adapters)
            # re-fetches before every handle_turn; a stale object replays
            # its old state branch and trips same-state transition guards.
            conversation = await manager.get_conversation(conversation.id)
            start = time.perf_counter()
            response = await handler.handle_turn(
                conversation=conversation,
                user_message=message,
            )
            elapsed_ms = (time.perf_counter() - start) * 1000

            metrics.record("multi_turn", elapsed_ms)
            print(f"Turn {i + 1}: {elapsed_ms:.2f}ms - State: {response.state}")

        stats = metrics.get_stats("multi_turn")
        print(f"\nMulti-turn statistics:")
        print(f"  Mean: {stats['mean_ms']:.2f}ms")
        print(f"  P50: {stats['p50_ms']:.2f}ms")
        print(f"  P95: {stats['p95_ms']:.2f}ms")
        print(f"  Max: {stats['max_ms']:.2f}ms")

        # Baseline assertion
        assert stats["count"] == len(messages)

    @pytest.mark.asyncio
    async def test_turn_response_time_under_target(
        self,
        handler: StandupConversationHandler,
        manager: StandupConversationManager,
        metrics: StandupPerformanceMetrics,
    ):
        """Verify turn response time meets p95 target of <500ms."""
        # Run 20 turns to get statistically meaningful sample
        num_iterations = 20

        for i in range(num_iterations):
            conversation = await manager.create_conversation(
                user_id=f"target-user-{i}",
                session_id=f"target-session-{i}",
            )

            start = time.perf_counter()
            await handler.handle_turn(
                conversation=conversation,
                user_message="Start my standup",
            )
            elapsed_ms = (time.perf_counter() - start) * 1000

            metrics.record("target_test", elapsed_ms)

        stats = metrics.get_stats("target_test")
        p95 = stats["p95_ms"]
        target = PERFORMANCE_TARGETS["turn_response_p95_ms"]

        print(f"\n{'='*60}")
        print("TURN RESPONSE TIME BASELINE")
        print(f"{'='*60}")
        print(f"  Iterations: {stats['count']}")
        print(f"  Mean: {stats['mean_ms']:.2f}ms")
        print(f"  P50: {stats['p50_ms']:.2f}ms")
        print(f"  P95: {stats['p95_ms']:.2f}ms (target: <{target}ms)")
        print(f"  P99: {stats['p99_ms']:.2f}ms")
        print(f"  Min: {stats['min_ms']:.2f}ms")
        print(f"  Max: {stats['max_ms']:.2f}ms")
        print(f"{'='*60}")

        # This is baseline - we're establishing the current state
        # After Phase 1, this should become an assertion:
        # assert p95 < target, f"P95 {p95:.2f}ms exceeds target {target}ms"


class TestMemoryUsageBaseline:
    """Establish baseline for memory usage patterns."""

    @pytest.mark.asyncio
    async def test_memory_usage_single_conversation(
        self,
        handler: StandupConversationHandler,
        manager: StandupConversationManager,
        metrics: StandupPerformanceMetrics,
    ):
        """Measure memory usage for a single conversation."""
        gc.collect()
        tracemalloc.start()

        initial_memory = tracemalloc.get_traced_memory()[0]
        metrics.record_memory(initial_memory)

        conversation = await manager.create_conversation(
            user_id="memory-test-user",
            session_id="memory-test-session",
        )

        await handler.handle_turn(
            conversation=conversation,
            user_message="Start my standup",
        )

        current_memory = tracemalloc.get_traced_memory()[0]
        metrics.record_memory(current_memory)

        tracemalloc.stop()

        memory_used = current_memory - initial_memory
        print(f"\nMemory used for single conversation: {memory_used / 1024:.2f}KB")

    @pytest.mark.asyncio
    async def test_memory_usage_multi_turn_conversation(
        self,
        handler: StandupConversationHandler,
        manager: StandupConversationManager,
        metrics: StandupPerformanceMetrics,
    ):
        """Measure memory usage across 20+ turns (acceptance criteria)."""
        gc.collect()
        tracemalloc.start()

        initial_memory = tracemalloc.get_traced_memory()[0]
        metrics.record_memory(initial_memory)

        conversation = await manager.create_conversation(
            user_id="memory-multi-user",
            session_id="memory-multi-session",
        )

        # Simulate 25 turns (exceeds 20-turn requirement)
        messages = [
            "Start my standup",
            "focus on GitHub",
            "skip documentation",
            "include calendar events",
        ] + [f"refinement request {i}" for i in range(21)]

        for i, message in enumerate(messages):
            conversation = await manager.get_conversation(conversation.id)
            await handler.handle_turn(
                conversation=conversation,
                user_message=message,
            )

            current_memory = tracemalloc.get_traced_memory()[0]
            metrics.record_memory(current_memory)

            if i % 5 == 0:
                print(f"Turn {i + 1}: Memory = {current_memory / 1024:.2f}KB")

        tracemalloc.stop()

        memory_stats = metrics.get_memory_stats()
        growth = memory_stats["growth_bytes"]
        max_growth = PERFORMANCE_TARGETS["memory_growth_max_bytes"]

        print(f"\n{'='*60}")
        print("MEMORY USAGE BASELINE (25 turns)")
        print(f"{'='*60}")
        print(f"  Initial: {memory_stats['min_bytes'] / 1024:.2f}KB")
        print(f"  Final: {memory_stats['max_bytes'] / 1024:.2f}KB")
        print(f"  Growth: {growth / 1024:.2f}KB (target: <{max_growth / 1024:.2f}KB)")
        print(f"  Peak: {memory_stats['peak_bytes'] / 1024:.2f}KB")
        print(f"{'='*60}")

        # This is baseline - we're establishing the current state
        # After Phase 2, this should become an assertion:
        # assert growth < max_growth, f"Memory growth {growth}B exceeds target {max_growth}B"


class TestStateTransitionPerformance:
    """Profile state machine transition performance."""

    @pytest.mark.asyncio
    async def test_state_transition_timing(
        self,
        manager: StandupConversationManager,
        metrics: StandupPerformanceMetrics,
    ):
        """Measure state transition performance."""
        conversation = await manager.create_conversation(
            user_id="state-test-user",
            session_id="state-test-session",
        )

        transitions = [
            StandupConversationState.GATHERING_PREFERENCES,
            StandupConversationState.GENERATING,
            StandupConversationState.REFINING,
            StandupConversationState.FINALIZING,
            StandupConversationState.COMPLETE,
        ]

        for new_state in transitions:
            start = time.perf_counter()
            result = await manager.transition_state(conversation.id, new_state)
            elapsed_ms = (time.perf_counter() - start) * 1000

            metrics.record("state_transition", elapsed_ms)
            print(f"Transition to {new_state.name}: {elapsed_ms:.3f}ms")

        stats = metrics.get_stats("state_transition")
        max_target = PERFORMANCE_TARGETS["state_transition_max_ms"]

        print(f"\nState transition statistics:")
        print(f"  Mean: {stats['mean_ms']:.3f}ms")
        print(f"  Max: {stats['max_ms']:.3f}ms (target: <{max_target}ms)")

        # State transitions should be very fast
        assert stats["max_ms"] < max_target


class TestPreferenceExtractionOverhead:
    """Profile preference extraction performance."""

    def test_preference_extraction_timing(
        self,
        handler: StandupConversationHandler,
        metrics: StandupPerformanceMetrics,
    ):
        """Measure preference extraction overhead."""
        test_messages = [
            "focus on GitHub issues",
            "skip documentation and tests",
            "make it brief",
            "include calendar events from this week",
            "don't include PRs that are already merged",
            "prioritize blockers and urgent items",
        ]

        for message in test_messages:
            start = time.perf_counter()
            prefs = handler._extract_preferences(message)
            elapsed_ms = (time.perf_counter() - start) * 1000

            metrics.record("preference_extraction", elapsed_ms)
            print(f"'{message[:30]}...': {elapsed_ms:.3f}ms -> {len(prefs)} prefs")

        stats = metrics.get_stats("preference_extraction")
        print(f"\nPreference extraction statistics:")
        print(f"  Mean: {stats['mean_ms']:.3f}ms")
        print(f"  Max: {stats['max_ms']:.3f}ms")


# ============================================================================
# Baseline Summary Test
# ============================================================================


class TestBaselineSummary:
    """Generate comprehensive baseline summary."""

    @pytest.mark.asyncio
    async def test_comprehensive_baseline(
        self,
        handler: StandupConversationHandler,
        manager: StandupConversationManager,
    ):
        """Generate full baseline metrics for Issue #556."""
        metrics = StandupPerformanceMetrics()

        # 1. Response time baseline
        for i in range(10):
            conversation = await manager.create_conversation(
                user_id=f"baseline-{i}",
                session_id=f"baseline-session-{i}",
            )

            start = time.perf_counter()
            await handler.handle_turn(conversation, "Start my standup")
            elapsed_ms = (time.perf_counter() - start) * 1000
            metrics.record("turn_response", elapsed_ms)

        # 2. Multi-turn memory baseline
        gc.collect()
        tracemalloc.start()

        initial = tracemalloc.get_traced_memory()[0]
        metrics.record_memory(initial)

        conversation = await manager.create_conversation(
            user_id="baseline-multi",
            session_id="baseline-multi-session",
        )

        for i in range(20):
            conversation = await manager.get_conversation(conversation.id)
            await handler.handle_turn(conversation, f"Turn {i}")
            current = tracemalloc.get_traced_memory()[0]
            metrics.record_memory(current)

        tracemalloc.stop()

        # 3. Print comprehensive summary
        summary = metrics.summary()

        print("\n" + "=" * 70)
        print("ISSUE #556 PHASE 0: BASELINE PERFORMANCE METRICS")
        print("=" * 70)

        timing = summary["timing"]
        if "turn_response" in timing:
            t = timing["turn_response"]
            print(f"\nTURN RESPONSE TIME (n={t['count']}):")
            print(
                f"  P50: {t['p50_ms']:.2f}ms (target: <{PERFORMANCE_TARGETS['turn_response_p50_ms']}ms)"
            )
            print(
                f"  P95: {t['p95_ms']:.2f}ms (target: <{PERFORMANCE_TARGETS['turn_response_p95_ms']}ms)"
            )
            print(f"  P99: {t['p99_ms']:.2f}ms")
            print(f"  Mean: {t['mean_ms']:.2f}ms ± {t['stdev_ms']:.2f}ms")

        memory = summary["memory"]
        if memory:
            print(f"\nMEMORY USAGE (20 turns):")
            print(
                f"  Growth: {memory['growth_bytes'] / 1024:.2f}KB (target: <{PERFORMANCE_TARGETS['memory_growth_max_bytes'] / 1024:.2f}KB)"
            )
            print(f"  Peak: {memory['peak_bytes'] / 1024:.2f}KB")

        print("\n" + "=" * 70)
        print("BASELINE ESTABLISHED - Ready for Phase 1 optimization")
        print("=" * 70)


# ============================================================================
# Phase 5: Load Testing (Alpha-Realistic)
# ============================================================================


class TestAlphaRealisticLoad:
    """
    Issue #556 Phase 5: Load testing with alpha-realistic profiles.

    Per PM guidance (2026-01-08): Alpha testers rarely have >1 concurrent user.
    This test validates performance under light concurrency (2-3 users max).
    """

    @pytest.mark.asyncio
    async def test_light_concurrent_conversations(self):
        """Test 2-3 concurrent conversations meet p95 target."""
        import asyncio

        async def run_conversation(user_id: str, num_turns: int = 5) -> List[float]:
            """Run a single conversation and return turn times."""
            manager = StandupConversationManager()
            handler = StandupConversationHandler(
                conversation_manager=manager,
                standup_workflow=None,
            )

            conversation = await manager.create_conversation(
                user_id=user_id,
                session_id=f"concurrent-session-{user_id}",
            )

            times = []
            for i in range(num_turns):
                conversation = await manager.get_conversation(conversation.id)
                start = time.perf_counter()
                await handler.handle_turn(
                    conversation=conversation,
                    user_message=f"Turn {i} from {user_id}",
                )
                elapsed_ms = (time.perf_counter() - start) * 1000
                times.append(elapsed_ms)

            return times

        # Run 3 concurrent conversations (alpha realistic max)
        num_users = 3
        num_turns = 5

        print(f"\nRunning {num_users} concurrent conversations, {num_turns} turns each...")

        results = await asyncio.gather(
            *[run_conversation(f"concurrent-user-{i}") for i in range(num_users)]
        )

        # Flatten all times
        all_times = [t for user_times in results for t in user_times]

        # Calculate statistics
        sorted_times = sorted(all_times)
        p50_idx = len(sorted_times) // 2
        p95_idx = int(len(sorted_times) * 0.95)

        p50 = sorted_times[p50_idx]
        p95 = sorted_times[min(p95_idx, len(sorted_times) - 1)]
        mean = sum(all_times) / len(all_times)
        max_time = max(all_times)

        target = PERFORMANCE_TARGETS["turn_response_p95_ms"]

        print(f"\n{'='*60}")
        print(f"PHASE 5: CONCURRENT LOAD TEST ({num_users} users)")
        print(f"{'='*60}")
        print(f"  Total turns: {len(all_times)}")
        print(f"  Mean: {mean:.2f}ms")
        print(f"  P50: {p50:.2f}ms")
        print(f"  P95: {p95:.2f}ms (target: <{target}ms)")
        print(f"  Max: {max_time:.2f}ms")
        print(f"{'='*60}")

        # Per-user breakdown
        print("\nPer-user breakdown:")
        for i, user_times in enumerate(results):
            user_mean = sum(user_times) / len(user_times)
            user_max = max(user_times)
            print(f"  User {i}: mean={user_mean:.2f}ms, max={user_max:.2f}ms")

        # Assert p95 meets target
        assert p95 < target, f"P95 under concurrent load {p95:.2f}ms exceeds target {target}ms"

    @pytest.mark.asyncio
    async def test_single_user_performance_validation(self):
        """
        Single-user performance validation test.

        This is the primary Phase 5 test: validates that a single user
        completing a 10-turn conversation meets the p95 <500ms target.
        """
        manager = StandupConversationManager()
        handler = StandupConversationHandler(
            conversation_manager=manager,
            standup_workflow=None,
        )

        # Create single conversation
        conversation = await manager.create_conversation(
            user_id="validation-user",
            session_id="validation-session",
        )

        times = []
        for i in range(10):
            conversation = await manager.get_conversation(conversation.id)
            start = time.perf_counter()
            await handler.handle_turn(
                conversation=conversation,
                user_message=f"Turn {i} for validation",
            )
            elapsed_ms = (time.perf_counter() - start) * 1000
            times.append(elapsed_ms)

        # Calculate statistics
        sorted_times = sorted(times)
        p95_idx = int(len(sorted_times) * 0.95)
        p95 = sorted_times[min(p95_idx, len(sorted_times) - 1)]

        target = PERFORMANCE_TARGETS["turn_response_p95_ms"]

        print(f"\n{'='*60}")
        print("PHASE 5: SINGLE-USER PERFORMANCE VALIDATION")
        print(f"{'='*60}")
        print(f"  Turns: {len(times)}")
        print(f"  P95: {p95:.2f}ms (target: <{target}ms)")
        print(f"  Max: {max(times):.2f}ms")
        print(f"  RESULT: {'PASS ✓' if p95 < target else 'FAIL ✗'}")
        print(f"{'='*60}")

        # Assert p95 meets target
        assert p95 < target, f"P95 {p95:.2f}ms exceeds target {target}ms"
