# Gameplan: CORE-GREAT-5 - Essential Validation & Quality Gates

**Date**: October 7, 2025
**Epic**: CORE-GREAT-5 (Final GREAT epic)
**Context**: Lock in all refactors with regression testing and performance gates
**Effort**: Small-Medium (2-3 days)

## Mission

Establish essential quality gates to prevent regression and maintain the excellent performance achieved in GREAT-1 through GREAT-4. Alpha-appropriate scope without over-engineering.

## Background

Recent discoveries from GREAT-4:
- Permissive test patterns (`[200, 404]`) hide failures
- Missing import validation allowed broken code
- Missing endpoints went undetected
- Performance is excellent (600K req/sec) - must preserve
- 142+ tests exist for intent system alone

## Phase 0: Current State Assessment
**Lead Developer WITH PM - 30 minutes**

### Verify Baselines
```bash
# Current test count and coverage
pytest --collect-only tests/ | grep "test session starts" -A 5
pytest --cov=services --cov-report=term-missing tests/

# Performance baseline from GREAT-4E
grep -r "req/sec\|response.*ms" dev/2025/10/

# Find remaining permissive patterns
grep -r "status_code in \[" tests/
grep -r "assert.*or.*True" tests/
grep -r "except.*pass" tests/

# Check CI/CD current state
cat .github/workflows/ci.yml | grep -A 5 -B 5 "pytest"
```

### Document Starting Point
Record current metrics before improvements

## Phase 1: Zero-Tolerance Regression Suite
**Code Agent - Medium effort**

### Create Regression Test Suite
`tests/regression/test_critical_no_mocks.py`:

Based on GREAT-4E-2 investigation findings:
```python
class TestCriticalImports:
    """All critical imports must work - no mocks"""

    def test_all_services_importable(self):
        """Verify all service modules import successfully"""
        critical_modules = [
            "web.app",
            "services.intent_service",
            "services.orchestration.engine",
            "services.github_service",
            "services.standup_service",
            # ... all critical services
        ]
        for module in critical_modules:
            importlib.import_module(module)  # Hard fail if broken

class TestCriticalEndpoints:
    """All critical endpoints must exist and return correct status"""

    def test_health_returns_200_always(self):
        """NEVER accept 404 for health checks"""
        response = client.get("/health")
        assert response.status_code == 200  # STRICT - no [200, 404]

class TestNoBypassRoutes:
    """Verify intent enforcement from GREAT-4B"""

    def test_no_direct_service_access(self):
        """All routes must go through intent layer"""
        # Implementation from GREAT-4B validation
```

### Fix Remaining Permissive Tests
Find and fix all `[200, 404]` patterns discovered

## Phase 2: Performance Benchmarks
**Cursor Agent - Medium effort**

### Create Performance Benchmark Suite
`scripts/benchmark_performance.py`:

Lock in current excellent performance:
```python
class PerformanceBenchmarks:
    # Baselines from GREAT-4E
    INTENT_CANONICAL_TARGET = 1  # ms
    INTENT_WORKFLOW_TARGET = 3000  # ms
    API_RESPONSE_TARGET = 500  # ms
    THROUGHPUT_TARGET = 500000  # req/sec

    def benchmark_intent_performance(self):
        """Verify intent classification meets targets"""
        # Test canonical path (~1ms)
        # Test workflow path (~3000ms)

    def benchmark_api_performance(self):
        """Verify API responses within targets"""

    def benchmark_throughput(self):
        """Verify system can handle load"""
        # Not full load test, just verify basics
```

### Add Performance Gates to CI
Fail builds if performance degrades >20%

## Phase 3: Integration Tests for Critical Flows
**Code Agent - Medium effort**

### Critical User Flows Only
`tests/integration/test_critical_flows.py`:

Focus on most important paths:
1. **Intent Classification Flow**
   - User input → Intent → Handler → Response
   - All 13 categories tested

2. **GitHub Issue Creation**
   - Intent → Orchestration → GitHub API → Success

3. **Multi-User Context**
   - User A and User B isolation verified

4. **Error Recovery**
   - Failed request → Retry → Success
   - Graceful degradation

## Phase 4: CI/CD Quality Gates
**Cursor Agent - Small effort**

### Update CI Pipeline
`.github/workflows/ci.yml`:

```yaml
name: Quality Gates

on: [push, pull_request]

jobs:
  regression-tests:
    name: Zero Tolerance Tests
    steps:
      - name: Run Regression Suite
        run: |
          PYTHONPATH=. pytest tests/regression/ -v --tb=short
          # MUST pass 100% - no skips allowed

  performance-gates:
    name: Performance Benchmarks
    steps:
      - name: Check Performance
        run: |
          python scripts/benchmark_performance.py
          # Fail if >20% degradation

  coverage-gates:
    name: Maintain Coverage
    steps:
      - name: Check Coverage
        run: |
          pytest --cov=services --cov-fail-under=80

  bypass-detection:
    name: Intent Enforcement
    steps:
      - name: Check for Bypasses
        run: |
          python scripts/check_intent_bypasses.py
          # From GREAT-4B
```

## Phase 5: Basic Monitoring Setup
**Both Agents - Small effort**

### Leverage What We Have
From GREAT-4E-2:
- `/api/admin/intent-monitoring` endpoint exists
- `/health` endpoint operational
- Intent metrics already collected

### Add Simple Additions
1. **Log aggregation script**
   ```bash
   # scripts/aggregate_logs.sh
   tail -f logs/*.log | grep -E "ERROR|WARNING|intent"
   ```

2. **Basic error tracking**
   ```python
   # scripts/track_errors.py
   # Parse logs for error patterns
   # Generate simple report
   ```

3. **Performance tracking**
   - Use existing metrics endpoints
   - Simple HTML dashboard (like GREAT-4E-2)

## Phase Z: Validation & Documentation
**Both Agents**

### Verify All Gates Working
```bash
# Push a commit with broken test
# Should fail CI

# Push a commit with performance regression
# Should fail CI

# Push a commit with bypass route
# Should fail CI

# All gates enforcing ✓
```

### Update Documentation
- Document regression suite purpose
- Document performance baselines
- Document monitoring approach
- Create troubleshooting guide

## Success Criteria

- [ ] Zero-tolerance regression suite created and passing
- [ ] Performance benchmarks established and enforced
- [ ] CI/CD gates blocking bad commits
- [ ] Critical flows have integration tests
- [ ] No permissive test patterns remain
- [ ] Basic monitoring operational
- [ ] Documentation updated

## Agent Division

**Code Agent** - Phases 1, 3
- Regression test suite
- Integration tests
- Test fixes

**Cursor Agent** - Phases 2, 4
- Performance benchmarks
- CI/CD gates
- Performance tracking

**Both** - Phases 0, 5, Z
- Assessment
- Monitoring
- Validation

## STOP Conditions

- If current coverage already >90% (might not need more tests)
- If performance benchmarks show regression from GREAT-4
- If CI/CD configuration blocked by permissions
- If integration tests reveal broken flows

## Critical Notes

- Focus on regression PREVENTION not feature addition
- Lock in the 600K req/sec performance from GREAT-4E
- Zero tolerance for permissive patterns
- Keep it simple - this is alpha, not enterprise

---

*Ready to lock in the Great Refactor achievements!*
