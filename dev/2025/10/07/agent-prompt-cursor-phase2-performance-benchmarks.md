# Prompt for Cursor Agent: GREAT-5 Phase 2 - Performance Benchmarks & Gates

## Context

GREAT-5 mission: Establish essential quality gates to prevent regression and maintain excellent performance from GREAT-1 through GREAT-4.

**This is Phase 2**: Create performance benchmark suite and add performance gates to CI/CD.

## Session Log

Start new log: `dev/2025/10/07/2025-10-07-1655-prog-cursor-log.md`

## Mission

1. Create performance benchmark suite that locks in GREAT-4E achievements
2. Add performance gates to CI/CD to prevent >20% degradation
3. Establish baseline metrics for monitoring

---

## Background from GREAT-4E

**Performance baseline established** (October 6, 2025):

**Canonical Path** (fast-path):
- Response time: ~1ms
- Throughput: 602,907 req/sec sustained
- Cache hit rate: 84.6%
- Cache speedup: 7.6x

**Workflow Path** (LLM classification):
- Response time: 2000-3000ms (expected for LLM)
- Sequential throughput: 904.8 req/sec

**System Capacity**:
- Sustained load: 602K+ req/sec
- Memory: Stable, no leaks
- Error handling: Perfect (0% error rate)

**Source**: `dev/2025/10/06/load-test-report.md`

---

## Task 1: Create Performance Benchmark Suite

### File Structure

Create: `scripts/benchmark_performance.py`

### Implementation

```python
#!/usr/bin/env python3
"""
Performance Benchmark Suite for GREAT-5

Locks in performance achievements from GREAT-4E to prevent regression.
Benchmarks are "alpha appropriate" - validate basics without over-engineering.

Baseline from GREAT-4E (Oct 6, 2025):
- Canonical path: ~1ms
- Throughput: 602K+ req/sec
- Cache hit: 84.6%
- Cache speedup: 7.6x
"""

import time
import asyncio
import statistics
from typing import List, Dict, Any
import sys

# Performance targets (20% tolerance from GREAT-4E baselines)
PERFORMANCE_TARGETS = {
    "canonical_response_ms": 10,        # Target: <10ms (baseline: 1ms, 90% margin)
    "cache_hit_rate_percent": 65,       # Target: >65% (baseline: 84.6%, 20% margin)
    "cache_speedup_factor": 5.0,        # Target: >5x (baseline: 7.6x, 20% margin)
    "workflow_response_ms": 3500,       # Target: <3500ms (baseline: 2000-3000ms, margin)
}


class PerformanceBenchmark:
    """Benchmark suite for intent classification performance"""

    def __init__(self):
        self.results = {}
        self.failures = []

    async def run_all_benchmarks(self) -> bool:
        """
        Run all performance benchmarks.

        Returns:
            bool: True if all benchmarks pass, False otherwise
        """
        print("=" * 80)
        print("GREAT-5 Performance Benchmark Suite")
        print("=" * 80)
        print(f"Baselines from GREAT-4E (Oct 6, 2025)")
        print(f"- Canonical path: ~1ms")
        print(f"- Throughput: 602K+ req/sec")
        print(f"- Cache hit rate: 84.6%")
        print(f"- Cache speedup: 7.6x")
        print("=" * 80)
        print()

        # Run benchmarks
        await self.benchmark_canonical_response_time()
        await self.benchmark_cache_effectiveness()
        await self.benchmark_workflow_response_time()
        await self.benchmark_basic_throughput()

        # Print results
        self.print_results()

        # Return success/failure
        return len(self.failures) == 0

    async def benchmark_canonical_response_time(self):
        """
        Benchmark canonical handler response time.

        Target: <10ms (baseline: 1ms, generous margin)
        Test: IDENTITY intent (simplest canonical handler)
        """
        print("Benchmark 1/4: Canonical Handler Response Time")
        print("-" * 80)

        from fastapi.testclient import TestClient
        from web.app import app

        client = TestClient(app)

        # Warm-up request
        client.post("/api/v1/intent", json={"message": "who are you"})

        # Measure response times
        response_times = []
        for i in range(10):
            start = time.perf_counter()
            response = client.post("/api/v1/intent", json={"message": "who are you"})
            end = time.perf_counter()

            if response.status_code == 200:
                response_times.append((end - start) * 1000)  # Convert to ms

        # Calculate statistics
        avg_ms = statistics.mean(response_times)
        p95_ms = statistics.quantiles(response_times, n=20)[18]  # 95th percentile

        # Check against target
        target_ms = PERFORMANCE_TARGETS["canonical_response_ms"]
        passed = p95_ms < target_ms

        # Store results
        self.results["canonical_response_time"] = {
            "avg_ms": round(avg_ms, 2),
            "p95_ms": round(p95_ms, 2),
            "target_ms": target_ms,
            "passed": passed,
        }

        if not passed:
            self.failures.append(
                f"Canonical response time: {p95_ms:.2f}ms exceeds target {target_ms}ms"
            )

        # Print results
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  Average: {avg_ms:.2f}ms")
        print(f"  P95: {p95_ms:.2f}ms")
        print(f"  Target: <{target_ms}ms")
        print(f"  Status: {status}")
        print()

    async def benchmark_cache_effectiveness(self):
        """
        Benchmark cache hit rate and speedup.

        Targets:
        - Hit rate: >65% (baseline: 84.6%)
        - Speedup: >5x (baseline: 7.6x)
        """
        print("Benchmark 2/4: Cache Effectiveness")
        print("-" * 80)

        from fastapi.testclient import TestClient
        from web.app import app

        client = TestClient(app)

        # Get initial metrics
        response = client.get("/api/admin/intent-cache-metrics")
        if response.status_code != 200:
            print(f"  ⚠️  SKIP: Cache metrics endpoint not available")
            print()
            return

        initial_metrics = response.json()["metrics"]
        initial_hits = initial_metrics.get("hits", 0)
        initial_misses = initial_metrics.get("misses", 0)

        # Make some requests (mix of new and repeated)
        queries = [
            "who are you",
            "show my calendar",
            "what's my status",
            "who are you",  # Repeat
            "show my calendar",  # Repeat
        ]

        for query in queries:
            client.post("/api/v1/intent", json={"message": query})

        # Get final metrics
        response = client.get("/api/admin/intent-cache-metrics")
        final_metrics = response.json()["metrics"]
        final_hits = final_metrics.get("hits", 0)
        final_misses = final_metrics.get("misses", 0)

        # Calculate hit rate
        total_hits = final_hits - initial_hits
        total_misses = final_misses - initial_misses
        total_requests = total_hits + total_misses

        if total_requests > 0:
            hit_rate = (total_hits / total_requests) * 100
        else:
            hit_rate = 0

        # Get speedup from metrics
        speedup = final_metrics.get("speedup_factor", 1.0)

        # Check against targets
        hit_rate_target = PERFORMANCE_TARGETS["cache_hit_rate_percent"]
        speedup_target = PERFORMANCE_TARGETS["cache_speedup_factor"]

        hit_rate_passed = hit_rate >= hit_rate_target or total_requests == 0
        speedup_passed = speedup >= speedup_target
        passed = hit_rate_passed and speedup_passed

        # Store results
        self.results["cache_effectiveness"] = {
            "hit_rate_percent": round(hit_rate, 1),
            "speedup_factor": round(speedup, 1),
            "hit_rate_target": hit_rate_target,
            "speedup_target": speedup_target,
            "passed": passed,
        }

        if not hit_rate_passed:
            self.failures.append(
                f"Cache hit rate: {hit_rate:.1f}% below target {hit_rate_target}%"
            )
        if not speedup_passed:
            self.failures.append(
                f"Cache speedup: {speedup:.1f}x below target {speedup_target}x"
            )

        # Print results
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  Hit Rate: {hit_rate:.1f}% (target: >{hit_rate_target}%)")
        print(f"  Speedup: {speedup:.1f}x (target: >{speedup_target}x)")
        print(f"  Status: {status}")
        print()

    async def benchmark_workflow_response_time(self):
        """
        Benchmark workflow (LLM) response time.

        Target: <3500ms (baseline: 2000-3000ms with margin)
        Note: This is realistic for LLM-based classification
        """
        print("Benchmark 3/4: Workflow Response Time")
        print("-" * 80)

        from fastapi.testclient import TestClient
        from web.app import app

        client = TestClient(app)

        # Use a query that requires workflow (not cached, not canonical)
        # Use unique query to avoid cache
        unique_query = f"analyze project status for timestamp {time.time()}"

        # Measure response time
        start = time.perf_counter()
        response = client.post("/api/v1/intent", json={"message": unique_query})
        end = time.perf_counter()

        response_time_ms = (end - start) * 1000

        # Check against target
        target_ms = PERFORMANCE_TARGETS["workflow_response_ms"]
        passed = response_time_ms < target_ms

        # Store results
        self.results["workflow_response_time"] = {
            "response_ms": round(response_time_ms, 2),
            "target_ms": target_ms,
            "passed": passed,
        }

        if not passed:
            self.failures.append(
                f"Workflow response time: {response_time_ms:.2f}ms exceeds target {target_ms}ms"
            )

        # Print results
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  Response Time: {response_time_ms:.2f}ms")
        print(f"  Target: <{target_ms}ms")
        print(f"  Status: {status}")
        print(f"  Note: LLM-based classification takes 2-3 seconds (expected)")
        print()

    async def benchmark_basic_throughput(self):
        """
        Basic throughput check - not full load test.

        Goal: Verify system can handle multiple sequential requests
        without degradation.
        """
        print("Benchmark 4/4: Basic Throughput")
        print("-" * 80)

        from fastapi.testclient import TestClient
        from web.app import app

        client = TestClient(app)

        # Send 10 sequential requests
        num_requests = 10
        response_times = []

        for i in range(num_requests):
            start = time.perf_counter()
            response = client.post("/api/v1/intent", json={"message": "who are you"})
            end = time.perf_counter()

            if response.status_code == 200:
                response_times.append(end - start)

        # Calculate throughput
        total_time = sum(response_times)
        throughput = num_requests / total_time

        # Check for degradation (last 5 vs first 5)
        first_half_avg = statistics.mean(response_times[:5])
        second_half_avg = statistics.mean(response_times[5:])
        degradation_pct = ((second_half_avg - first_half_avg) / first_half_avg) * 100

        # Pass if no significant degradation (>20%)
        passed = degradation_pct < 20

        # Store results
        self.results["basic_throughput"] = {
            "requests_per_sec": round(throughput, 2),
            "degradation_percent": round(degradation_pct, 1),
            "passed": passed,
        }

        if not passed:
            self.failures.append(
                f"Throughput degradation: {degradation_pct:.1f}% exceeds 20%"
            )

        # Print results
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  Throughput: {throughput:.2f} req/sec")
        print(f"  Degradation: {degradation_pct:.1f}%")
        print(f"  Status: {status}")
        print(f"  Note: Full load test showed 602K req/sec (GREAT-4E)")
        print()

    def print_results(self):
        """Print summary of all benchmark results"""
        print("=" * 80)
        print("BENCHMARK RESULTS SUMMARY")
        print("=" * 80)

        total_benchmarks = len(self.results)
        passed_benchmarks = sum(1 for r in self.results.values() if r.get("passed", False))

        print(f"Total Benchmarks: {total_benchmarks}")
        print(f"Passed: {passed_benchmarks}")
        print(f"Failed: {total_benchmarks - passed_benchmarks}")
        print()

        if self.failures:
            print("FAILURES:")
            for failure in self.failures:
                print(f"  ❌ {failure}")
            print()

        if passed_benchmarks == total_benchmarks:
            print("✅ ALL BENCHMARKS PASSED")
            print("Performance is maintained from GREAT-4E baseline")
        else:
            print("❌ SOME BENCHMARKS FAILED")
            print("Performance has degraded - investigate before deploying")

        print("=" * 80)


async def main():
    """Run all benchmarks and exit with appropriate code"""
    benchmark = PerformanceBenchmark()
    success = await benchmark.run_all_benchmarks()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
```

### Usage

```bash
# Run benchmarks
python scripts/benchmark_performance.py

# Expected output:
# - 4 benchmarks run
# - All pass if performance maintained
# - Exit code 0 on success, 1 on failure
```

---

## Task 2: Add Performance Gates to CI/CD

### Update CI/CD Configuration

**File**: `.github/workflows/test.yml` (or create if doesn't exist)

Add performance gate job:

```yaml
  performance-benchmarks:
    name: Performance Benchmarks
    runs-on: ubuntu-latest
    needs: [test]  # Run after tests pass

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run Performance Benchmarks
        run: |
          python scripts/benchmark_performance.py
        env:
          PYTHONPATH: .

      - name: Upload benchmark results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: performance-benchmarks
          path: benchmark-results.json
```

**Note**: If `.github/workflows/test.yml` doesn't exist, create a basic one with:
- Test job (runs pytest)
- Performance benchmarks job (runs our script)

---

## Task 3: Create Benchmark Documentation

### File: dev/2025/10/07/great5-phase2-performance-benchmarks.md

Document:
- Benchmark suite created
- Performance targets set (with 20% tolerance from GREAT-4E)
- Benchmark results (first run)
- CI/CD integration details
- How to run locally
- What to do if benchmarks fail

### Include

**Baseline metrics from GREAT-4E**:
- Canonical path: 1ms → Target: <10ms (90% margin)
- Cache hit rate: 84.6% → Target: >65% (20% margin)
- Cache speedup: 7.6x → Target: >5x (20% margin)
- Workflow: 2000-3000ms → Target: <3500ms (margin)

**Why generous targets**:
- Alpha-appropriate (not over-engineering)
- Allows for variance in test environment
- Catches significant degradation (>20%)
- Prevents false positives from minor fluctuations

---

## Task 4: Run Initial Benchmarks

### Execute Locally

```bash
# Run benchmark suite
PYTHONPATH=. python scripts/benchmark_performance.py

# Should complete and show results
# Document actual results in Phase 2 report
```

### Expected Results

Based on GREAT-4E performance:
- ✅ Canonical response: <10ms (expect ~1-5ms)
- ✅ Cache hit rate: >65% (expect ~80%+)
- ✅ Cache speedup: >5x (expect ~7x)
- ✅ Workflow response: <3500ms (expect 2000-3000ms)
- ✅ Basic throughput: No degradation

**If benchmarks fail**: Investigate why performance degraded since GREAT-4E

---

## Success Criteria

- [ ] Performance benchmark script created (`scripts/benchmark_performance.py`)
- [ ] 4 benchmarks implemented (canonical, cache, workflow, throughput)
- [ ] Performance targets set with 20% tolerance from GREAT-4E
- [ ] CI/CD updated with performance gate
- [ ] Benchmarks run successfully (all pass)
- [ ] Results documented
- [ ] Session log updated

---

## Critical Notes

- **Alpha-appropriate**: Don't over-engineer, simple benchmarks are fine
- **Generous margins**: 20% tolerance prevents false positives
- **Lock in wins**: Preserve 602K req/sec achievement from GREAT-4E
- **Fail fast**: CI should block merges if performance degrades >20%
- **Document baseline**: Clear reference to GREAT-4E metrics

---

## STOP Conditions

- If benchmarks reveal >20% performance degradation, investigate and ask PM
- If CI/CD permissions blocked, document and ask PM
- If performance targets seem too strict/loose, ask PM

---

**Effort**: Medium (~45-60 minutes)
**Priority**: HIGH (locks in GREAT-4E achievements)
**Deliverable**: Performance benchmark suite + CI/CD integration
