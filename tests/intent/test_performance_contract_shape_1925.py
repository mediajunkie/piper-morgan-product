"""#1925 (b) — the performance contract reports latency and asserts only a hang ceiling.

Arch's ruling (2026-10-05): "(b) report, don't assert, with a hang ceiling."
The 2026-10-05 live run had 23 of 26 ``tests/intent`` failures reading
``Response time Nms exceeds threshold 4000ms`` for round-trips of 5–16 s —
a budget from the deterministic era measuring the LLM era. These tests pin
the new shape deterministically (no LLM, no keys):

  * a 7.7 s sample (yesterday's median) is RECORDED and does NOT fail
  * a sample above the ceiling still fails, with the ceiling named
  * the coverage report carries n / p50 / p95 / max
"""

from __future__ import annotations

import pytest

from tests.intent.base_validation_test import BaseValidationTest
from tests.intent.coverage_tracker import CoverageStats, coverage
from tests.intent.test_constants import PERFORMANCE_THRESHOLDS


@pytest.fixture
def clean_ledger():
    saved = list(coverage.latencies_ms)
    coverage.latencies_ms.clear()
    try:
        yield coverage
    finally:
        coverage.latencies_ms[:] = saved


def test_the_old_budget_is_gone_and_the_ceiling_is_generous():
    assert "max_response_time_ms" not in PERFORMANCE_THRESHOLDS
    assert PERFORMANCE_THRESHOLDS["hang_ceiling_ms"] >= 30_000


def test_a_router_era_round_trip_is_recorded_not_failed(clean_ledger):
    BaseValidationTest().assert_performance(7_700.0)  # 2026-10-05's median
    BaseValidationTest().assert_performance(15_600.0)  # 2026-10-05's max
    assert clean_ledger.latencies_ms == [7_700.0, 15_600.0]


def test_a_hang_still_fails_and_names_the_ceiling(clean_ledger):
    ceiling = PERFORMANCE_THRESHOLDS["hang_ceiling_ms"]
    with pytest.raises(AssertionError) as exc:
        BaseValidationTest().assert_performance(ceiling + 1)
    assert f"hang ceiling {ceiling}ms" in str(exc.value)
    # the sample is still recorded — a hang is a data point too
    assert clean_ledger.latencies_ms == [float(ceiling + 1)]


def test_report_carries_percentiles():
    stats = CoverageStats(
        categories_tested=set(),
        interfaces_tested=set(),
        interface_tests_passed=0,
        contract_tests_passed=0,
        latencies_ms=[5200.0, 6000.0, 7700.0, 8100.0, 15600.0],
    )
    assert stats.latency_percentile(50) == 7700.0
    assert stats.latency_percentile(95) == 15600.0
    line = stats.latency_line()
    assert (
        "n=5" in line and "p50=7700ms" in line and "p95=15600ms" in line and "max=15600ms" in line
    )
    assert line in stats.report()


def test_report_with_no_samples_says_so():
    stats = CoverageStats(set(), set(), 0, 0)
    assert stats.latency_percentile(50) is None
    assert "no samples recorded" in stats.report()
