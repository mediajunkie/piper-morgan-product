"""
Performance Tests for Agent Scalability - PM-033d Testing Infrastructure
Tests multi-agent system performance under load and scaling scenarios
"""

import asyncio
import statistics
import time
from typing import Any, Dict, List

import pytest

from tests.mocks.mock_agents import MockCoordinatorAgent, create_mock_agent_pool
from tests.utils.performance_monitor import PerformanceMonitor, PerformanceTargetExceededError


class TestAgentScalability:
    """Test multi-agent system performance under load"""

    @pytest.fixture
    def performance_monitor(self):
        """Create performance monitor for scalability testing"""
        return PerformanceMonitor(target_latency_ms=200)  # Overall workflow target

    @pytest.fixture
    def coordinator_agent(self):
        """Create coordinator agent for scalability testing"""
        return MockCoordinatorAgent()

    @pytest.mark.asyncio
    async def test_concurrent_agent_workflows(self, performance_monitor, coordinator_agent):
        """Test multiple workflows with different agents"""
        performance_monitor.start_session()

        # Create agent pools of different sizes
        agent_pool_sizes = [3, 5, 8, 10]
        workflow_results = {}

        for pool_size in agent_pool_sizes:
            agents = create_mock_agent_pool(
                ["code"] * (pool_size // 2) + ["architect"] * (pool_size // 2)
            )

            # Test concurrent workflow execution
            workflow_tasks = []
            for i in range(3):  # 3 concurrent workflows
                workflow_id = f"concurrent_workflow_{pool_size}_{i}"
                task = coordinator_agent.coordinate_workflow(workflow_id, agents)
                workflow_tasks.append(task)

            # Execute workflows concurrently
            start_time = time.time()
            results = await asyncio.gather(*workflow_tasks)
            end_time = time.time()

            total_time = (end_time - start_time) * 1000
            workflow_results[pool_size] = {
                "total_time_ms": total_time,
                "avg_time_per_workflow": total_time / 3,
                "success_rate": sum(1 for r in results if r.success) / len(results),
                "results": results,
            }

            # Validate performance targets
            assert total_time <= 200 * 3, f"Concurrent workflows exceeded target: {total_time}ms"

        performance_monitor.end_session()

        # Validate scalability characteristics
        for pool_size, results in workflow_results.items():
            assert (
                results["success_rate"] == 1.0
            ), f"Workflow success rate < 100% for {pool_size} agents"
            assert (
                results["avg_time_per_workflow"] <= 200
            ), f"Average workflow time exceeded target for {pool_size} agents"

    @pytest.mark.asyncio
    async def test_agent_pool_expansion(self, performance_monitor, coordinator_agent):
        """Test performance scaling with agent count"""
        performance_monitor.start_session()

        # Test with increasing agent pool sizes
        agent_counts = [2, 4, 6, 8, 10]
        scaling_results = {}

        for agent_count in agent_counts:
            # Create balanced agent pool
            code_agents = agent_count // 2
            architect_agents = agent_count // 2
            analysis_agents = agent_count - code_agents - architect_agents

            agent_types = (
                ["code"] * code_agents
                + ["architect"] * architect_agents
                + ["analysis"] * analysis_agents
            )
            agents = create_mock_agent_pool(agent_types)

            # Measure coordination performance
            start_time = time.time()
            result = await coordinator_agent.coordinate_workflow(
                f"scaling_test_{agent_count}", agents
            )
            end_time = time.time()

            coordination_time = (end_time - start_time) * 1000
            scaling_results[agent_count] = {
                "coordination_time_ms": coordination_time,
                "agents_coordinated": agent_count,
                "success": result.success,
                "workflow_ready": result.output_data["workflow_ready"],
            }

            # Validate basic performance requirements
            assert result.success is True
            assert result.output_data["workflow_ready"] is True
            assert (
                coordination_time <= 200
            ), f"Coordination exceeded target for {agent_count} agents: {coordination_time}ms"

        performance_monitor.end_session()

        # Analyze scaling characteristics
        coordination_times = [
            results["coordination_time_ms"] for results in scaling_results.values()
        ]

        # Validate linear scaling (within reasonable bounds)
        # Coordination time should not grow exponentially
        for i in range(1, len(coordination_times)):
            growth_factor = coordination_times[i] / coordination_times[i - 1]
            assert growth_factor <= 2.0, f"Exponential scaling detected: {growth_factor}x growth"

    @pytest.mark.asyncio
    async def test_communication_channel_capacity(self, performance_monitor, coordinator_agent):
        """Test agent communication under high load"""
        performance_monitor.start_session()

        # Create large agent pool
        large_agent_pool = create_mock_agent_pool(
            ["code"] * 5 + ["architect"] * 5 + ["analysis"] * 5
        )

        # Test high-frequency communication
        communication_tasks = []
        message_count = 20

        for i in range(message_count):
            # Simulate high-frequency status updates
            task = coordinator_agent.synchronize_agent_states(f"high_freq_sync_{i}")
            communication_tasks.append(task)

        # Execute high-frequency communication
        start_time = time.time()
        results = await asyncio.gather(*communication_tasks)
        end_time = time.time()

        total_time = (end_time - start_time) * 1000
        avg_time_per_message = total_time / message_count

        # Validate communication capacity
        assert total_time <= 200, f"High-frequency communication exceeded target: {total_time}ms"
        assert (
            avg_time_per_message <= 25
        ), f"Average message time exceeded target: {avg_time_per_message}ms"

        # Validate all communications successful
        success_count = sum(1 for r in results if r.success)
        assert (
            success_count == message_count
        ), f"Communication success rate: {success_count}/{message_count}"

        performance_monitor.end_session()

    @pytest.mark.asyncio
    async def test_memory_usage_scaling(self, performance_monitor):
        """Test memory usage scaling with agent count"""
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Test memory usage with different agent pool sizes
        memory_usage = {}

        for agent_count in [5, 10, 15, 20]:
            # Create agent pool
            agents = create_mock_agent_pool(["code"] * agent_count)

            # Measure memory usage
            current_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = current_memory - initial_memory

            memory_usage[agent_count] = {
                "total_memory_mb": current_memory,
                "increase_mb": memory_increase,
                "increase_per_agent_mb": memory_increase / agent_count,
            }

            # Validate reasonable memory usage
            assert (
                memory_increase <= agent_count * 10
            ), f"Excessive memory usage: {memory_increase}MB for {agent_count} agents"

        # Validate linear memory scaling
        memory_increases = [data["increase_mb"] for data in memory_usage.values()]
        for i in range(1, len(memory_increases)):
            # #1452: a 0MB step (psutil granularity) is flat growth, not a
            # divisor — the original ZeroDivisionError'd on quiet runs.
            if memory_increases[i - 1] <= 0:
                continue
            growth_factor = memory_increases[i] / memory_increases[i - 1]
            assert growth_factor <= 3.0, f"Exponential memory growth detected: {growth_factor}x"

    @pytest.mark.asyncio
    async def test_cpu_usage_under_load(self, performance_monitor):
        """Test CPU usage under high agent load"""
        import os

        import psutil

        process = psutil.Process(os.getpid())

        # Baseline CPU usage
        baseline_cpu = process.cpu_percent(interval=0.1)

        # Create high-load scenario
        large_agent_pool = create_mock_agent_pool(["code"] * 10 + ["architect"] * 10)
        coordinator = MockCoordinatorAgent()

        # Execute intensive coordination tasks
        start_time = time.time()

        # High-frequency coordination
        coordination_tasks = []
        for i in range(15):
            task = coordinator.coordinate_workflow(f"cpu_test_{i}", large_agent_pool)
            coordination_tasks.append(task)

        # Monitor CPU during execution
        cpu_samples = []
        for _ in range(10):
            cpu_samples.append(process.cpu_percent(interval=0.05))

        # Execute tasks
        results = await asyncio.gather(*coordination_tasks)
        end_time = time.time()

        execution_time = (end_time - start_time) * 1000

        # Validate performance and resource usage
        assert execution_time <= 200, f"CPU-intensive tasks exceeded target: {execution_time}ms"

        # Validate CPU usage is reasonable
        max_cpu = max(cpu_samples)
        assert max_cpu <= 80, f"Excessive CPU usage detected: {max_cpu}%"

        # Validate all tasks completed
        success_count = sum(1 for r in results if r.success)
        assert success_count == 15, f"Task success rate: {success_count}/15"

    @pytest.mark.asyncio
    async def test_concurrent_workflow_throughput(self, performance_monitor, coordinator_agent):
        """Test system throughput with multiple concurrent workflows"""
        performance_monitor.start_session()

        # Test different concurrency levels
        concurrency_levels = [2, 4, 6, 8]
        throughput_results = {}

        for concurrency in concurrency_levels:
            # Create agent pool
            agents = create_mock_agent_pool(["code"] * 3 + ["architect"] * 3 + ["analysis"] * 3)

            # Execute concurrent workflows
            workflow_tasks = []
            for i in range(concurrency):
                workflow_id = f"throughput_test_{concurrency}_{i}"
                task = coordinator_agent.coordinate_workflow(workflow_id, agents)
                workflow_tasks.append(task)

            # Measure throughput
            start_time = time.time()
            results = await asyncio.gather(*workflow_tasks)
            end_time = time.time()

            total_time = (end_time - start_time) * 1000
            throughput = concurrency / (total_time / 1000)  # workflows per second

            throughput_results[concurrency] = {
                "concurrency": concurrency,
                "total_time_ms": total_time,
                "throughput_wfps": throughput,
                "avg_time_per_workflow": total_time / concurrency,
                "success_rate": sum(1 for r in results if r.success) / len(results),
            }

            # Validate throughput requirements
            assert (
                total_time <= 200 * concurrency
            ), f"Throughput target exceeded for {concurrency} concurrent workflows"
            assert throughput >= 1.0, f"Insufficient throughput: {throughput} workflows/second"

        performance_monitor.end_session()

        # Validate throughput scaling
        throughputs = [data["throughput_wfps"] for data in throughput_results.values()]
        for i in range(1, len(throughputs)):
            # Throughput should not decrease significantly with increased concurrency
            throughput_ratio = throughputs[i] / throughputs[i - 1]
            assert throughput_ratio >= 0.5, f"Throughput degradation: {throughput_ratio}x"


class TestPerformanceRegression:
    """Test for performance regression in agent coordination"""

    @pytest.mark.asyncio
    async def test_baseline_performance_consistency(self):
        """Test that baseline performance remains consistent"""
        coordinator = MockCoordinatorAgent()
        agents = create_mock_agent_pool(["code", "architect", "analysis"])

        # Run baseline test multiple times
        baseline_times = []
        for i in range(10):
            start_time = time.time()
            result = await coordinator.coordinate_workflow(f"baseline_{i}", agents)
            end_time = time.time()

            assert result.success is True
            baseline_times.append((end_time - start_time) * 1000)

        # Validate consistency (low variance)
        mean_time = statistics.mean(baseline_times)
        std_dev = statistics.stdev(baseline_times)
        coefficient_of_variation = std_dev / mean_time

        assert (
            coefficient_of_variation <= 0.3
        ), f"High performance variance: {coefficient_of_variation}"
        assert mean_time <= 200, f"Baseline performance exceeded target: {mean_time}ms"

    @pytest.mark.asyncio
    async def test_performance_under_stress(self):
        """Test performance under stress conditions"""
        coordinator = MockCoordinatorAgent()

        # Create stress scenario with many agents
        stress_agents = create_mock_agent_pool(["code"] * 15 + ["architect"] * 15)

        # Execute multiple coordination tasks under stress
        start_time = time.time()

        stress_tasks = []
        for i in range(20):
            task = coordinator.coordinate_workflow(f"stress_test_{i}", stress_agents)
            stress_tasks.append(task)

        results = await asyncio.gather(*stress_tasks)
        end_time = time.time()

        total_time = (end_time - start_time) * 1000

        # Validate stress performance
        assert total_time <= 200 * 20, f"Stress test exceeded target: {total_time}ms"

        # Validate all tasks completed successfully
        success_count = sum(1 for r in results if r.success)
        assert success_count == 20, f"Stress test success rate: {success_count}/20"


# Performance test execution helpers
def run_scalability_tests():
    """Run all scalability performance tests"""
    pytest.main([__file__, "-v", "--tb=short", "--durations=10"])


if __name__ == "__main__":
    run_scalability_tests()
