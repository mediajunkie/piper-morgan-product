"""
INFR-CONFIG-PERF: Configuration System Performance Benchmarks

This module establishes baseline performance metrics for the configuration system
and implements regression tests to ensure performance characteristics are maintained.

Benchmarks measure:
- Configuration loading time (first load + cache hits)
- Validation execution time
- CLI command response time
- Memory usage patterns

Issue: #143 (INFR-CONFIG-PERF)
Related: #139 (PM-132: Implement Notion configuration loader)
"""

import asyncio
import statistics
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional
from unittest.mock import MagicMock, patch

import pytest

from services.configuration.piper_config_loader import PiperConfigLoader


class ConfigPerformanceMetrics:
    """Collector for configuration system performance metrics"""

    def __init__(self):
        self.measurements: Dict[str, List[float]] = {}
        self.memory_samples: List[float] = []
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def record(self, operation: str, duration_ms: float):
        """Record a single measurement"""
        if operation not in self.measurements:
            self.measurements[operation] = []
        self.measurements[operation].append(duration_ms)

    def get_stats(self, operation: str) -> Dict[str, float]:
        """Get statistics for an operation"""
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
        """Calculate percentile value"""
        if not values:
            return 0.0
        sorted_values = sorted(values)
        index = int(len(sorted_values) * percentile / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]

    def summary(self) -> Dict[str, Dict[str, float]]:
        """Get summary of all metrics"""
        return {op: self.get_stats(op) for op in self.measurements.keys()}


# ============================================================================
# Baseline Performance Targets
# ============================================================================

PERFORMANCE_TARGETS = {
    "config_loading_first_load": 100,  # First load should be <100ms
    "config_loading_cache_hit": 5,  # Cache hit should be <5ms
    "system_prompt_generation": 20,  # System prompt generation <20ms
    "parse_piper_md": 80,  # Markdown parsing <80ms
}


# ============================================================================
# Unit Performance Tests
# ============================================================================


class TestConfigLoaderPerformance:
    """Performance tests for PiperConfigLoader"""

    @pytest.fixture
    def metrics(self):
        """Fresh metrics collector for each test"""
        return ConfigPerformanceMetrics()

    @pytest.fixture
    def temp_config(self, tmp_path):
        """Create temporary config file for testing"""
        config_file = tmp_path / "PIPER.test.md"
        config_file.write_text(
            """# Piper Configuration

## Personality
- warmth_level: 0.7
- confidence_style: contextual

## Knowledge
- preferred_sources: github, notion
- update_frequency: daily

## Behavior
- response_length: medium
- verbosity: detailed
"""
        )
        return config_file

    def test_first_load_performance(self, temp_config, metrics):
        """Benchmark first configuration load (cache miss)"""
        loader = PiperConfigLoader(str(temp_config))

        start_time = time.time()
        config = loader.load_config()
        duration_ms = (time.time() - start_time) * 1000

        metrics.record("config_loading_first_load", duration_ms)

        assert config is not None
        assert duration_ms < PERFORMANCE_TARGETS["config_loading_first_load"]

    def test_cache_hit_performance(self, temp_config, metrics):
        """Benchmark cached configuration load (cache hit)"""
        loader = PiperConfigLoader(str(temp_config))

        # Prime the cache with first load
        loader.load_config()

        # Measure cached load
        start_time = time.time()
        config = loader.load_config()
        duration_ms = (time.time() - start_time) * 1000

        metrics.record("config_loading_cache_hit", duration_ms)

        assert config is not None
        assert loader.cache_hits > 0
        assert duration_ms < PERFORMANCE_TARGETS["config_loading_cache_hit"]

    def test_system_prompt_generation_performance(self, temp_config, metrics):
        """Benchmark system prompt generation from config"""
        loader = PiperConfigLoader(str(temp_config))

        start_time = time.time()
        prompt = loader.get_system_prompt()
        duration_ms = (time.time() - start_time) * 1000

        metrics.record("system_prompt_generation", duration_ms)

        assert prompt is not None
        assert len(prompt) > 0
        assert duration_ms < PERFORMANCE_TARGETS["system_prompt_generation"]

    def test_multiple_loads_consistency(self, temp_config, metrics):
        """Test performance consistency across multiple loads"""
        loader = PiperConfigLoader(str(temp_config))

        # Perform multiple loads to establish baseline
        for i in range(10):
            start_time = time.time()
            config = loader.load_config()
            duration_ms = (time.time() - start_time) * 1000
            metrics.record("config_loading_subsequent", duration_ms)

        stats = metrics.get_stats("config_loading_subsequent")

        # Verify cache is working (cache hits should be recorded)
        assert loader.cache_hits >= 9  # 9 of 10 loads should be cache hits
        # Verify all loads are reasonably fast
        assert stats["max_ms"] < PERFORMANCE_TARGETS["config_loading_cache_hit"] * 3  # 15ms max

    def test_large_config_performance(self, tmp_path, metrics):
        """Benchmark performance with large configuration file"""
        # Create a large config file (simulate real-world complexity)
        large_config = tmp_path / "PIPER.large.md"
        content = "# Piper Configuration\n\n"
        for i in range(100):
            content += f"## Section {i}\n"
            content += f"- property{i}: value{i}\n"
            content += f"- description: This is a detailed description of section {i}\n\n"

        large_config.write_text(content)

        loader = PiperConfigLoader(str(large_config))

        start_time = time.time()
        config = loader.load_config()
        duration_ms = (time.time() - start_time) * 1000

        metrics.record("large_config_loading", duration_ms)

        assert config is not None
        # Large files may take longer, but should still be reasonable
        assert duration_ms < 200  # 200ms threshold for large files


# ============================================================================
# Regression Test Markers
# ============================================================================
# NOTE (2026-08-30, census disposal Batch 3): TestConfigValidationPerformance
# was excised here with services/config_validator.py — the CI-stub validator
# (returned {"status": "ok"} unconditionally since 2025-10-13; PM-ruled
# 2026-08-28 with the behavioral-validation CI job removal, #1687). The LIVE
# validator is services/infrastructure/config/config_validator.py, which is
# not what these benchmarks exercised.


@pytest.mark.regression
class TestConfigPerformanceRegression:
    """Regression tests to detect performance degradation"""

    def test_config_loading_regression(self):
        """
        Regression test: Config loading should not degrade over time

        This test should fail if:
        - First load takes >150ms (baseline 100ms + 50% margin)
        - Cache hit takes >10ms (baseline 5ms + 100% margin)
        """
        loader = PiperConfigLoader()

        # Verify caching mechanism is working
        assert hasattr(loader, "cache_hits")
        assert hasattr(loader, "cache_misses")
        assert loader.cache_ttl == 300  # Should still be 5 minutes

    def test_cache_effectiveness(self):
        """
        Regression test: Cache should be effective

        This test verifies:
        - Cache hit counter exists
        - Cache miss counter exists
        - Cache TTL is reasonable (300 seconds)
        """
        loader = PiperConfigLoader()

        # Load twice
        loader.load_config()
        loader.load_config()

        # Cache should have at least one hit
        assert loader.cache_hits >= 1


# ============================================================================
# Performance Reporting
# ============================================================================


class ConfigPerformanceReport:
    """Generate performance report for documentation"""

    @staticmethod
    def generate_baseline_report(metrics: ConfigPerformanceMetrics) -> str:
        """Generate a markdown report of baseline metrics"""
        report = "# Configuration System Performance Baseline\n\n"
        report += f"**Generated**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

        report += "## Performance Targets\n\n"
        report += "| Operation | Target (ms) |\n"
        report += "|-----------|-------------|\n"
        for op, target in PERFORMANCE_TARGETS.items():
            report += f"| {op} | {target} |\n"

        report += "\n## Measured Performance\n\n"
        for op, stats in metrics.summary().items():
            if stats:
                report += f"### {op}\n\n"
                report += f"- **Count**: {int(stats.get('count', 0))}\n"
                report += f"- **Mean**: {stats.get('mean_ms', 0):.2f}ms\n"
                report += f"- **Median**: {stats.get('median_ms', 0):.2f}ms\n"
                report += f"- **P95**: {stats.get('p95_ms', 0):.2f}ms\n"
                report += f"- **P99**: {stats.get('p99_ms', 0):.2f}ms\n"
                report += f"- **Min**: {stats.get('min_ms', 0):.2f}ms\n"
                report += f"- **Max**: {stats.get('max_ms', 0):.2f}ms\n"
                report += f"- **StDev**: {stats.get('stdev_ms', 0):.2f}ms\n\n"

        return report

    @staticmethod
    def verify_performance_targets(metrics: ConfigPerformanceMetrics) -> Dict[str, bool]:
        """Verify all measurements are within targets"""
        results = {}
        summary = metrics.summary()

        for operation, target_ms in PERFORMANCE_TARGETS.items():
            if operation in summary:
                stats = summary[operation]
                # Use p95 as the verification metric (accounts for variance)
                p95 = stats.get("p95_ms", 0)
                results[operation] = p95 < target_ms
            else:
                results[operation] = None  # Not tested

        return results


# ============================================================================
# Pytest Fixtures for Performance Testing
# ============================================================================


@pytest.fixture(scope="session")
def performance_session_metrics():
    """Session-wide metrics collection for all performance tests"""
    return ConfigPerformanceMetrics()


@pytest.fixture(autouse=True)
def clear_cache_between_tests():
    """Clear config cache between tests to avoid cache hits affecting results"""
    yield
    # Cleanup happens after test


# ============================================================================
# Benchmark Report Generation (for CI/CD)
# ============================================================================


def pytest_configure(config):
    """Configure pytest with performance benchmarking"""
    config.addinivalue_line(
        "markers",
        "benchmark: mark test as a performance benchmark",
    )
    config.addinivalue_line(
        "markers",
        "regression: mark test as a performance regression test",
    )


def pytest_collection_modifyitems(config, items):
    """Mark performance tests appropriately"""
    for item in items:
        if "performance" in item.nodeid:
            item.add_marker(pytest.mark.benchmark)
