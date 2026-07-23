"""
PM-034: Performance benchmarks for LLM Intent Classification

Benchmarks test:
- Classification latency (target: <500ms p95 with LLM, <300ms p50)
- Knowledge Graph enrichment overhead
- Concurrent request handling
- Memory usage patterns
"""

import asyncio
import statistics
import time
from datetime import datetime
from typing import List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import KnowledgeNode
from services.intent_service.llm_classifier_factory import LLMClassifierFactory
from services.shared_types import NodeType


class BenchmarkMetrics:
    """Helper class to collect and analyze benchmark metrics"""

    def __init__(self):
        self.latencies = []
        self.memory_usage = []

    def record_latency(self, latency_ms: float):
        self.latencies.append(latency_ms)

    def get_percentile(self, percentile: int) -> float:
        """Get percentile value (e.g., 95 for p95)"""
        if not self.latencies:
            return 0.0
        sorted_latencies = sorted(self.latencies)
        index = int(len(sorted_latencies) * percentile / 100)
        return sorted_latencies[min(index, len(sorted_latencies) - 1)]

    def get_stats(self) -> dict:
        """Get comprehensive statistics"""
        if not self.latencies:
            return {"error": "No data collected"}

        return {
            "count": len(self.latencies),
            "mean": statistics.mean(self.latencies),
            "median": statistics.median(self.latencies),
            "p50": self.get_percentile(50),
            "p95": self.get_percentile(95),
            "p99": self.get_percentile(99),
            "min": min(self.latencies),
            "max": max(self.latencies),
        }


@pytest.mark.benchmark
class TestLLMClassifierBenchmarks:
    """Performance benchmarks for LLM Intent Classifier"""

    @pytest.fixture
    def mock_llm_responses(self):
        """Generate mock LLM responses for benchmarking"""
        responses = []
        categories = ["query", "execution", "analysis", "synthesis"]
        actions = ["search_documents", "create_task", "analyze_data", "generate_report"]

        for i in range(100):
            responses.append(
                {
                    "category": categories[i % len(categories)],
                    "action": actions[i % len(actions)],
                    "confidence": 0.75 + (i % 25) / 100,  # 0.75 to 0.99
                    "reasoning": f"Benchmark test {i}",
                }
            )

        return responses

    @pytest.fixture
    async def benchmark_classifier(self):
        """Create classifier optimized for benchmarking"""
        # Create with mocked dependencies for consistent performance
        mock_kg = MagicMock()
        mock_kg.create_node = AsyncMock(return_value=KnowledgeNode(id="bench"))
        mock_kg.get_nodes_by_type = AsyncMock(return_value=[])

        mock_semantic = MagicMock()
        mock_semantic.similarity_search = AsyncMock(return_value=[])

        # #1452: since #322 the classifier requires an injected llm_service —
        # the lazy .llm container fallback raises ContainerNotInitializedError
        # in tests. Every test here patches .complete on it anyway.
        mock_llm = MagicMock()
        mock_llm.complete = AsyncMock(return_value="{}")

        return await LLMClassifierFactory.create_for_testing(
            mock_knowledge_graph_service=mock_kg,
            mock_semantic_indexing_service=mock_semantic,
            mock_llm_service=mock_llm,
            confidence_threshold=0.75,
        )

    @pytest.mark.asyncio
    async def test_single_classification_latency(self, benchmark_classifier, mock_llm_responses):
        """Benchmark single classification latency"""
        metrics = BenchmarkMetrics()

        # Mock LLM with realistic delay
        async def mock_llm_complete(**kwargs):
            # Simulate LLM latency (150-250ms)
            await asyncio.sleep(0.15 + (hash(kwargs["prompt"]) % 100) / 1000)
            return str(mock_llm_responses[0])

        with patch.object(benchmark_classifier.llm, "complete", mock_llm_complete):
            # Run 50 classifications
            for i in range(50):
                start = time.perf_counter()

                await benchmark_classifier.classify(f"Find documents about feature {i}")

                latency_ms = (time.perf_counter() - start) * 1000
                metrics.record_latency(latency_ms)

        stats = metrics.get_stats()
        print(f"\nSingle Classification Latency: {stats}")

        # Assert performance targets
        assert stats["p50"] < 300  # p50 target: <300ms
        assert stats["p95"] < 500  # p95 target: <500ms

    @pytest.mark.asyncio
    async def test_knowledge_graph_enrichment_overhead(self, benchmark_classifier):
        """Benchmark overhead of Knowledge Graph context enrichment"""
        metrics_with_kg = BenchmarkMetrics()
        metrics_without_kg = BenchmarkMetrics()

        # Mock instant LLM response
        instant_response = (
            '{"category": "query", "action": "search", "confidence": 0.9, "reasoning": "test"}'
        )

        with patch.object(
            benchmark_classifier.llm, "complete", AsyncMock(return_value=instant_response)
        ):
            # Test WITH Knowledge Graph
            benchmark_classifier.knowledge_graph = MagicMock()
            benchmark_classifier.knowledge_graph.get_nodes_by_type = AsyncMock(
                return_value=[
                    KnowledgeNode(id=f"node_{i}", node_type=NodeType.EVENT) for i in range(10)
                ]
            )
            benchmark_classifier.semantic_indexer = MagicMock()
            benchmark_classifier.semantic_indexer.similarity_search = AsyncMock(
                return_value=[(KnowledgeNode(id="similar"), 0.85)]
            )

            for i in range(30):
                start = time.perf_counter()
                await benchmark_classifier.classify(
                    "Search for documents", session_id="bench_session"
                )
                latency_ms = (time.perf_counter() - start) * 1000
                metrics_with_kg.record_latency(latency_ms)

            # Test WITHOUT Knowledge Graph
            benchmark_classifier.knowledge_graph = None
            benchmark_classifier.semantic_indexer = None

            for i in range(30):
                start = time.perf_counter()
                await benchmark_classifier.classify("Search for documents")
                latency_ms = (time.perf_counter() - start) * 1000
                metrics_without_kg.record_latency(latency_ms)

        stats_with = metrics_with_kg.get_stats()
        stats_without = metrics_without_kg.get_stats()

        overhead_ms = stats_with["mean"] - stats_without["mean"]
        overhead_percent = (overhead_ms / stats_without["mean"]) * 100

        print(f"\nKnowledge Graph Overhead: {overhead_ms:.2f}ms ({overhead_percent:.1f}%)")
        print(f"With KG: {stats_with}")
        print(f"Without KG: {stats_without}")

        # Knowledge Graph should add minimal overhead
        assert overhead_ms < 50  # Less than 50ms overhead

    @pytest.mark.asyncio
    async def test_concurrent_classification_throughput(self, benchmark_classifier):
        """Benchmark concurrent classification handling"""
        metrics = BenchmarkMetrics()

        # Mock fast LLM responses
        async def mock_llm_complete(**kwargs):
            # Simulate some LLM latency
            await asyncio.sleep(0.05)
            return '{"category": "query", "action": "search", "confidence": 0.85, "reasoning": "concurrent"}'

        with patch.object(benchmark_classifier.llm, "complete", mock_llm_complete):
            # Test different concurrency levels
            for concurrent_requests in [1, 5, 10, 20]:
                messages = [f"Query {i}" for i in range(concurrent_requests)]

                start = time.perf_counter()

                # Run concurrent classifications
                results = await asyncio.gather(
                    *[benchmark_classifier.classify(msg) for msg in messages]
                )

                total_time = time.perf_counter() - start
                throughput = concurrent_requests / total_time
                avg_latency_ms = (total_time / concurrent_requests) * 1000

                print(
                    f"\nConcurrency {concurrent_requests}: {throughput:.1f} req/s, "
                    f"avg latency: {avg_latency_ms:.1f}ms"
                )

                # Record individual latencies
                for _ in range(concurrent_requests):
                    metrics.record_latency(avg_latency_ms)

        stats = metrics.get_stats()

        # Should handle concurrent requests efficiently
        assert stats["p95"] < 1000  # Even under load, p95 < 1s

    @pytest.mark.asyncio
    async def test_cache_effectiveness(self, benchmark_classifier):
        """Benchmark cache effectiveness for repeated queries"""
        metrics_first_run = BenchmarkMetrics()
        metrics_cached = BenchmarkMetrics()

        # Mock LLM with caching simulation
        cache = {}

        async def mock_llm_with_cache(**kwargs):
            prompt_hash = hash(kwargs["prompt"])
            if prompt_hash in cache:
                # Cached response - instant
                return cache[prompt_hash]
            else:
                # First time - simulate LLM latency
                await asyncio.sleep(0.15)
                response = '{"category": "query", "action": "search", "confidence": 0.9, "reasoning": "cached"}'
                cache[prompt_hash] = response
                return response

        with patch.object(benchmark_classifier.llm, "complete", mock_llm_with_cache):
            # First run - populate cache
            queries = ["Find project docs", "Show all tasks", "List team members"]

            for query in queries:
                start = time.perf_counter()
                await benchmark_classifier.classify(query)
                latency_ms = (time.perf_counter() - start) * 1000
                metrics_first_run.record_latency(latency_ms)

            # Cached runs
            for _ in range(3):  # Repeat same queries
                for query in queries:
                    start = time.perf_counter()
                    await benchmark_classifier.classify(query)
                    latency_ms = (time.perf_counter() - start) * 1000
                    metrics_cached.record_latency(latency_ms)

        stats_first = metrics_first_run.get_stats()
        stats_cached = metrics_cached.get_stats()

        cache_speedup = stats_first["mean"] / stats_cached["mean"]

        print(f"\nCache Effectiveness:")
        print(f"First run: {stats_first['mean']:.1f}ms")
        print(f"Cached: {stats_cached['mean']:.1f}ms")
        print(f"Speedup: {cache_speedup:.1f}x")

        # Cache should provide significant speedup
        assert cache_speedup > 5  # At least 5x faster with cache

    @pytest.mark.asyncio
    async def test_classification_accuracy_under_load(
        self, benchmark_classifier, mock_llm_responses
    ):
        """Test classification accuracy remains high under load"""
        successful_classifications = 0
        total_attempts = 100

        # Mock LLM with variable response times
        async def mock_llm_variable(**kwargs):
            # Simulate variable latency (50-200ms)
            await asyncio.sleep(0.05 + (hash(kwargs["prompt"]) % 150) / 1000)
            response_idx = hash(kwargs["prompt"]) % len(mock_llm_responses)
            return str(mock_llm_responses[response_idx])

        with patch.object(benchmark_classifier.llm, "complete", mock_llm_variable):
            # Run many classifications concurrently
            tasks = []
            for i in range(total_attempts):
                tasks.append(benchmark_classifier.classify(f"Test query {i}"))

            # Execute with some concurrency
            for i in range(0, total_attempts, 10):
                batch = tasks[i : i + 10]
                results = await asyncio.gather(*batch, return_exceptions=True)

                for result in results:
                    if not isinstance(result, Exception):
                        successful_classifications += 1

        success_rate = successful_classifications / total_attempts
        print(
            f"\nAccuracy under load: {success_rate:.2%} ({successful_classifications}/{total_attempts})"
        )

        # Should maintain high success rate even under load
        assert success_rate > 0.95  # >95% success rate

    @pytest.mark.asyncio
    async def test_memory_usage_pattern(self, benchmark_classifier):
        """Test memory usage doesn't grow unbounded"""
        import gc
        import sys

        # Force garbage collection
        gc.collect()

        # Track object counts
        initial_objects = len(gc.get_objects())

        # Mock instant LLM
        with patch.object(
            benchmark_classifier.llm,
            "complete",
            AsyncMock(
                return_value='{"category": "query", "action": "search", "confidence": 0.9, "reasoning": "memory test"}'
            ),
        ):
            # Run many classifications
            for i in range(100):
                await benchmark_classifier.classify(f"Memory test query {i}")

                # Periodically force GC
                if i % 20 == 0:
                    gc.collect()

        # Final GC
        gc.collect()
        final_objects = len(gc.get_objects())

        object_growth = final_objects - initial_objects
        growth_percent = (object_growth / initial_objects) * 100

        print(f"\nMemory usage:")
        print(f"Initial objects: {initial_objects}")
        print(f"Final objects: {final_objects}")
        print(f"Growth: {object_growth} ({growth_percent:.1f}%)")

        # Should not have significant memory growth
        assert growth_percent < 10  # Less than 10% object growth


@pytest.mark.benchmark
class TestRealWorldScenarios:
    """Benchmark real-world usage patterns"""

    @pytest.fixture
    async def production_classifier(self):
        """Create production-like classifier"""
        # #1452: create() resolves services from the container, which is not
        # initialized in the test process (#322 DI). The test patches the LLM
        # anyway — build via the testing factory with an injected mock.
        mock_llm = MagicMock()
        mock_llm.complete = AsyncMock(return_value="{}")

        return await LLMClassifierFactory.create_for_testing(
            mock_llm_service=mock_llm,
            confidence_threshold=0.75,
        )

    @pytest.mark.asyncio
    async def test_morning_standup_query_sequence(self, production_classifier):
        """Benchmark typical morning standup query sequence"""
        # Typical morning standup queries
        standup_queries = [
            "What did I work on yesterday?",
            "Show my tasks for today",
            "Any blockers reported?",
            "Team velocity this sprint",
            "Upcoming deadlines this week",
        ]

        metrics = BenchmarkMetrics()

        # Mock reasonable LLM responses
        async def mock_standup_llm(**kwargs):
            await asyncio.sleep(0.1)  # 100ms LLM latency
            return '{"category": "query", "action": "search", "confidence": 0.88, "reasoning": "standup query"}'

        with patch.object(production_classifier.llm, "complete", mock_standup_llm):
            for query in standup_queries:
                start = time.perf_counter()

                result = await production_classifier.classify(
                    query,
                    user_context={"time_of_day": "morning", "recurring": True},
                    session_id="standup_session",
                )

                latency_ms = (time.perf_counter() - start) * 1000
                metrics.record_latency(latency_ms)

                print(f"Query: '{query[:30]}...' -> {latency_ms:.1f}ms")

        stats = metrics.get_stats()
        print(f"\nStandup sequence stats: {stats}")

        # Morning standup should be fast
        assert stats["p95"] < 400  # Even p95 should be under 400ms
        assert stats["mean"] < 250  # Average under 250ms
