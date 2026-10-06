"""Track test coverage for GREAT-4E validation"""

from dataclasses import dataclass, field
from typing import List, Optional, Set

from tests.intent.test_constants import (
    CATEGORY_COUNT,
    CONTRACT_TESTS,
    INTERFACE_COUNT,
    INTERFACE_TESTS,
)


@dataclass
class CoverageStats:
    categories_tested: Set[str]
    interfaces_tested: Set[str]
    interface_tests_passed: int
    contract_tests_passed: int
    # #1925 (b): every assert_performance() sample, in ms, for the p50/p95 line.
    latencies_ms: List[float] = field(default_factory=list)

    def latency_percentile(self, pct: float) -> Optional[float]:
        """Nearest-rank percentile of the recorded samples (None when empty)."""
        if not self.latencies_ms:
            return None
        ordered = sorted(self.latencies_ms)
        rank = max(1, int(round(pct / 100.0 * len(ordered) + 0.5)))
        return ordered[min(rank, len(ordered)) - 1]

    def latency_line(self) -> str:
        n = len(self.latencies_ms)
        if n == 0:
            return "Latency:       no samples recorded"
        p50 = self.latency_percentile(50)
        p95 = self.latency_percentile(95)
        return (
            f"Latency:       n={n}  p50={p50:.0f}ms  p95={p95:.0f}ms  "
            f"max={max(self.latencies_ms):.0f}ms  (reported, not asserted — #1925)"
        )

    @property
    def category_coverage(self) -> float:
        return len(self.categories_tested) / CATEGORY_COUNT

    @property
    def interface_coverage(self) -> float:
        return len(self.interfaces_tested) / INTERFACE_COUNT

    @property
    def interface_test_coverage(self) -> float:
        return self.interface_tests_passed / INTERFACE_TESTS

    @property
    def contract_test_coverage(self) -> float:
        return self.contract_tests_passed / CONTRACT_TESTS

    @property
    def total_coverage(self) -> float:
        total_possible = INTERFACE_TESTS + CONTRACT_TESTS
        total_passed = self.interface_tests_passed + self.contract_tests_passed
        return total_passed / total_possible

    def report(self) -> str:
        """Generate coverage report."""
        return f"""
GREAT-4E Coverage Report
========================
Categories:    {len(self.categories_tested)}/{CATEGORY_COUNT} ({self.category_coverage:.0%})
Interfaces:    {len(self.interfaces_tested)}/{INTERFACE_COUNT} ({self.interface_coverage:.0%})
Interface Tests: {self.interface_tests_passed}/{INTERFACE_TESTS} ({self.interface_test_coverage:.0%})
Contract Tests:  {self.contract_tests_passed}/{CONTRACT_TESTS} ({self.contract_test_coverage:.0%})
TOTAL:         {self.interface_tests_passed + self.contract_tests_passed}/{INTERFACE_TESTS + CONTRACT_TESTS} ({self.total_coverage:.0%})
{self.latency_line()}
"""


# Global tracker instance
coverage = CoverageStats(
    categories_tested=set(),
    interfaces_tested=set(),
    interface_tests_passed=0,
    contract_tests_passed=0,
)
