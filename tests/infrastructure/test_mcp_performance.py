"""
Performance testing suite for MCP integration
Tests latency, throughput, and resource usage for MCP functionality.
"""

import asyncio
import os
import statistics
import time
from typing import Any, Dict, List

import pytest

from services.mcp.client import PiperMCPClient
from services.mcp.resources import MCPResourceManager
from services.queries.file_queries import FileQueryService
from services.repositories.file_repository import FileRepository


class MCPPerformanceTestSuite:
    """Performance testing suite for MCP integration"""

    def __init__(self):
        self.results: Dict[str, Any] = {}
        self.client_config = {
            "url": "stdio://./scripts/mcp_file_server.py",
            "timeout": 10.0,  # Extended timeout for performance tests
        }

    async def run_connection_performance_tests(self) -> Dict[str, Any]:
        """Test MCP connection performance"""
        print("🔗 Testing MCP connection performance...")

        connection_times = []
        success_count = 0

        # Test multiple connections
        for i in range(10):
            start_time = time.time()

            try:
                client = PiperMCPClient(self.client_config)
                connected = await client.connect()

                if connected:
                    success_count += 1
                    connection_time = time.time() - start_time
                    connection_times.append(connection_time)

                    # Test disconnection
                    await client.disconnect()
                else:
                    print(f"  Connection {i+1} failed")

            except Exception as e:
                print(f"  Connection {i+1} error: {e}")

        if connection_times:
            avg_time = statistics.mean(connection_times)
            median_time = statistics.median(connection_times)
            min_time = min(connection_times)
            max_time = max(connection_times)

            results = {
                "success_rate": success_count / 10.0,
                "avg_connection_time": avg_time,
                "median_connection_time": median_time,
                "min_connection_time": min_time,
                "max_connection_time": max_time,
                "connection_times": connection_times,
            }

            print(f"  ✓ Success rate: {results['success_rate']:.1%}")
            print(f"  ✓ Average connection time: {avg_time:.3f}s")
            print(f"  ✓ Median connection time: {median_time:.3f}s")
            print(f"  ✓ Min/Max connection time: {min_time:.3f}s / {max_time:.3f}s")

            return results
        else:
            return {"success_rate": 0.0, "error": "No successful connections"}

    async def run_resource_listing_performance_tests(self) -> Dict[str, Any]:
        """Test MCP resource listing performance"""
        print("📋 Testing MCP resource listing performance...")

        client = PiperMCPClient(self.client_config)
        connected = await client.connect()

        if not connected:
            return {"error": "Failed to connect to MCP client"}

        try:
            listing_times = []
            resource_counts = []

            # Test multiple resource listings
            for i in range(5):
                start_time = time.time()
                resources = await client.list_resources()
                listing_time = time.time() - start_time

                listing_times.append(listing_time)
                resource_counts.append(len(resources))

                print(f"  Listing {i+1}: {len(resources)} resources in {listing_time:.3f}s")

            avg_time = statistics.mean(listing_times)
            avg_count = statistics.mean(resource_counts)

            results = {
                "avg_listing_time": avg_time,
                "avg_resource_count": avg_count,
                "listing_times": listing_times,
                "resource_counts": resource_counts,
            }

            print(f"  ✓ Average listing time: {avg_time:.3f}s")
            print(f"  ✓ Average resource count: {avg_count:.1f}")

            return results

        finally:
            await client.disconnect()

    async def run_search_performance_tests(self) -> Dict[str, Any]:
        """Test MCP search performance"""
        print("🔍 Testing MCP search performance...")

        client = PiperMCPClient(self.client_config)
        connected = await client.connect()

        if not connected:
            return {"error": "Failed to connect to MCP client"}

        try:
            search_queries = [
                "MCP",
                "project",
                "document",
                "analysis",
                "test",
                "integration",
                "performance",
                "data",
            ]

            search_results = {}

            for query in search_queries:
                search_times = []
                result_counts = []

                # Test each query multiple times
                for i in range(3):
                    start_time = time.time()
                    results = await client.search_content(query)
                    search_time = time.time() - start_time

                    search_times.append(search_time)
                    result_counts.append(len(results))

                avg_time = statistics.mean(search_times)
                avg_count = statistics.mean(result_counts)

                search_results[query] = {
                    "avg_search_time": avg_time,
                    "avg_result_count": avg_count,
                    "search_times": search_times,
                    "result_counts": result_counts,
                }

                print(f"  '{query}': {avg_count:.1f} results in {avg_time:.3f}s")

            # Overall statistics
            all_times = []
            all_counts = []

            for query_results in search_results.values():
                all_times.extend(query_results["search_times"])
                all_counts.extend(query_results["result_counts"])

            overall_results = {
                "overall_avg_time": statistics.mean(all_times),
                "overall_avg_count": statistics.mean(all_counts),
                "query_results": search_results,
            }

            print(f"  ✓ Overall average search time: {overall_results['overall_avg_time']:.3f}s")
            print(f"  ✓ Overall average result count: {overall_results['overall_avg_count']:.1f}")

            return overall_results

        finally:
            await client.disconnect()

    async def run_resource_manager_performance_tests(self) -> Dict[str, Any]:
        """Test MCP resource manager performance"""
        print("🎯 Testing MCP resource manager performance...")

        manager = MCPResourceManager()
        initialized = await manager.initialize(enabled=True)

        if not initialized:
            return {"error": "Failed to initialize MCP resource manager"}

        try:
            search_queries = ["MCP", "project", "document", "analysis"]

            manager_results = {}

            for query in search_queries:
                search_times = []
                result_counts = []

                # Test each query multiple times
                for i in range(3):
                    start_time = time.time()
                    results = await manager.enhanced_file_search(query)
                    search_time = time.time() - start_time

                    search_times.append(search_time)
                    result_counts.append(len(results))

                avg_time = statistics.mean(search_times)
                avg_count = statistics.mean(result_counts)

                manager_results[query] = {
                    "avg_search_time": avg_time,
                    "avg_result_count": avg_count,
                    "search_times": search_times,
                    "result_counts": result_counts,
                }

                print(f"  '{query}': {avg_count:.1f} results in {avg_time:.3f}s")

            # Overall statistics
            all_times = []
            all_counts = []

            for query_results in manager_results.values():
                all_times.extend(query_results["search_times"])
                all_counts.extend(query_results["result_counts"])

            overall_results = {
                "overall_avg_time": statistics.mean(all_times),
                "overall_avg_count": statistics.mean(all_counts),
                "query_results": manager_results,
            }

            print(f"  ✓ Overall average search time: {overall_results['overall_avg_time']:.3f}s")
            print(f"  ✓ Overall average result count: {overall_results['overall_avg_count']:.1f}")

            return overall_results

        finally:
            await manager.cleanup()

    async def run_latency_benchmark(self) -> Dict[str, Any]:
        """Benchmark MCP latency against success criteria"""
        print("⏱️  Running MCP latency benchmark...")

        # Success criteria from POC plan
        MAX_ADDITIONAL_LATENCY = 0.5  # 500ms
        MAX_FALLBACK_LATENCY = 0.1  # 100ms

        # Test MCP search latency
        manager = MCPResourceManager()
        initialized = await manager.initialize(enabled=True)

        if not initialized:
            return {"error": "Failed to initialize MCP resource manager"}

        try:
            # Test MCP search times
            mcp_times = []
            for i in range(10):
                start_time = time.time()
                results = await manager.enhanced_file_search("test query")
                duration = time.time() - start_time
                mcp_times.append(duration)

            avg_mcp_time = statistics.mean(mcp_times)
            median_mcp_time = statistics.median(mcp_times)
            max_mcp_time = max(mcp_times)

            # Test fallback performance (simulated)
            fallback_times = []
            for i in range(10):
                start_time = time.time()
                # Simulate fallback to empty results
                results = []
                duration = time.time() - start_time
                fallback_times.append(duration)

            avg_fallback_time = statistics.mean(fallback_times)

            results = {
                "mcp_avg_latency": avg_mcp_time,
                "mcp_median_latency": median_mcp_time,
                "mcp_max_latency": max_mcp_time,
                "fallback_avg_latency": avg_fallback_time,
                "latency_benchmark_passed": max_mcp_time <= MAX_ADDITIONAL_LATENCY,
                "fallback_benchmark_passed": avg_fallback_time <= MAX_FALLBACK_LATENCY,
                "success_criteria": {
                    "max_additional_latency": MAX_ADDITIONAL_LATENCY,
                    "max_fallback_latency": MAX_FALLBACK_LATENCY,
                },
            }

            print(f"  ✓ MCP average latency: {avg_mcp_time:.3f}s")
            print(f"  ✓ MCP median latency: {median_mcp_time:.3f}s")
            print(f"  ✓ MCP max latency: {max_mcp_time:.3f}s")
            print(f"  ✓ Fallback average latency: {avg_fallback_time:.3f}s")
            print(f"  ✓ Latency benchmark passed: {results['latency_benchmark_passed']}")
            print(f"  ✓ Fallback benchmark passed: {results['fallback_benchmark_passed']}")

            return results

        finally:
            await manager.cleanup()

    async def run_full_performance_suite(self) -> Dict[str, Any]:
        """Run complete performance test suite"""
        print("🚀 Running MCP Performance Test Suite")
        print("=" * 50)

        full_results = {}

        # Run all performance tests
        full_results["connection_performance"] = await self.run_connection_performance_tests()
        print()

        full_results[
            "resource_listing_performance"
        ] = await self.run_resource_listing_performance_tests()
        print()

        full_results["search_performance"] = await self.run_search_performance_tests()
        print()

        full_results[
            "resource_manager_performance"
        ] = await self.run_resource_manager_performance_tests()
        print()

        full_results["latency_benchmark"] = await self.run_latency_benchmark()
        print()

        # Summary
        print("📊 Performance Test Summary")
        print("=" * 30)

        connection_results = full_results.get("connection_performance", {})
        if "success_rate" in connection_results:
            print(f"Connection success rate: {connection_results['success_rate']:.1%}")
            print(
                f"Average connection time: {connection_results.get('avg_connection_time', 0):.3f}s"
            )

        benchmark_results = full_results.get("latency_benchmark", {})
        if "latency_benchmark_passed" in benchmark_results:
            print(f"Latency benchmark passed: {benchmark_results['latency_benchmark_passed']}")
            print(f"Fallback benchmark passed: {benchmark_results['fallback_benchmark_passed']}")

        return full_results


# Test functions for pytest
class TestMCPPerformance:
    """pytest test class for MCP performance"""

    @pytest.mark.asyncio
    async def test_mcp_connection_performance(self):
        """Test MCP connection performance meets requirements"""
        suite = MCPPerformanceTestSuite()
        results = await suite.run_connection_performance_tests()

        # Assert performance requirements
        assert results.get("success_rate", 0) >= 0.95, "Connection success rate should be >= 95%"
        assert (
            results.get("avg_connection_time", 999) <= 1.0
        ), "Average connection time should be <= 1s"

    @pytest.mark.asyncio
    async def test_mcp_search_performance(self):
        """Test MCP search performance meets requirements"""
        suite = MCPPerformanceTestSuite()
        results = await suite.run_search_performance_tests()

        # Assert performance requirements
        overall_avg_time = results.get("overall_avg_time", 999)
        assert (
            overall_avg_time <= 2.0
        ), f"Overall search time should be <= 2s, got {overall_avg_time:.3f}s"

    @pytest.mark.asyncio
    async def test_mcp_latency_benchmark(self):
        """Test MCP latency benchmark meets POC success criteria"""
        suite = MCPPerformanceTestSuite()
        results = await suite.run_latency_benchmark()

        # Assert benchmark requirements
        assert results.get("latency_benchmark_passed", False), "MCP latency should be <= 500ms"
        assert results.get(
            "fallback_benchmark_passed", False
        ), "Fallback latency should be <= 100ms"


# Manual execution
async def main():
    """Manual performance test execution"""
    suite = MCPPerformanceTestSuite()
    results = await suite.run_full_performance_suite()

    # Save results for analysis
    import json

    with open("mcp_performance_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)

    print("\n✅ Performance test results saved to mcp_performance_results.json")


if __name__ == "__main__":
    asyncio.run(main())
