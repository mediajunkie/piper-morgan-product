# Prompt for Cursor Agent: GREAT-5 Phase 4 - CI/CD Quality Gates

## Context

GREAT-5 mission: Establish essential quality gates to prevent regression and maintain excellent performance from GREAT-1 through GREAT-4.

**This is Phase 4**: Consolidate and verify all CI/CD quality gates are properly configured.

## Session Log

Continue: `dev/2025/10/07/2025-10-07-1655-prog-cursor-log.md`

## Mission

1. Review and consolidate CI/CD configuration
2. Verify all quality gates are active
3. Ensure proper gate ordering and dependencies
4. Document complete CI/CD pipeline

---

## Background

**Quality gates added during GREAT-5**:
- Phase 1: Zero-tolerance regression tests
- Phase 2: Performance benchmarks
- Phase 3: Integration tests

**Existing gates from GREAT-4E-2**:
- 5 intent quality gates (192 test cases)
- Performance regression detection
- Coverage enforcement
- Bypass detection
- Contract validation

**Goal**: Ensure all gates work together and block bad commits

---

## Task 1: Review Current CI/CD Configuration

### Check Existing Configuration

**File**: `.github/workflows/test.yml` (or similar)

Review:
- What jobs currently exist
- What tests are being run
- What's the job dependency order
- Are all quality gates included

### Inventory Quality Gates

**From GREAT-4E-2**:
```yaml
# Existing gates (verify these exist)
- Intent classification tests
- Performance regression detection
- Coverage enforcement (80%+)
- Bypass detection
- Contract validation
```

**From GREAT-5**:
```yaml
# New gates (added in Phase 1-3)
- Zero-tolerance regression tests
- Performance benchmarks
- Integration tests for critical flows
```

---

## Task 2: Consolidate CI/CD Configuration

### Recommended Pipeline Structure

```yaml
name: Quality Gates

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  # Job 1: Basic validation
  lint-and-format:
    name: Lint and Format Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run linters
        run: |
          # Add if linting configured
          # flake8 . || true
          echo "Linting check placeholder"

  # Job 2: Unit and regression tests
  test-suite:
    name: Test Suite
    runs-on: ubuntu-latest
    needs: [lint-and-format]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run zero-tolerance regression tests
        run: |
          PYTHONPATH=. python -m pytest tests/regression/test_critical_no_mocks.py -v
        # MUST pass 100% - no skips allowed

      - name: Run integration tests
        run: |
          PYTHONPATH=. python -m pytest tests/integration/test_critical_flows.py -v
        # Critical flows must work

      - name: Run all tests with coverage
        run: |
          PYTHONPATH=. python -m pytest tests/ --cov=services --cov-report=term-missing

      - name: Check coverage threshold
        run: |
          PYTHONPATH=. python -m pytest --cov=services --cov-fail-under=80

  # Job 3: Performance benchmarks
  performance-benchmarks:
    name: Performance Benchmarks
    runs-on: ubuntu-latest
    needs: [test-suite]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run performance benchmarks
        run: |
          PYTHONPATH=. python scripts/benchmark_performance.py
        # Fails if >20% performance degradation

  # Job 4: Intent quality gates (from GREAT-4E-2)
  intent-quality:
    name: Intent Quality Gates
    runs-on: ubuntu-latest
    needs: [test-suite]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Intent classification tests
        run: |
          PYTHONPATH=. python -m pytest tests/intent/ -v
      - name: Bypass detection
        run: |
          PYTHONPATH=. python -m pytest tests/intent/test_no_web_bypasses.py -v

  # Job 5: Final validation
  all-gates-passed:
    name: All Quality Gates Passed
    runs-on: ubuntu-latest
    needs: [test-suite, performance-benchmarks, intent-quality]
    steps:
      - run: echo "✅ All quality gates passed!"
```

### Key Principles

1. **Job Dependencies**: Tests run before benchmarks, all complete before final validation
2. **Fast Fail**: Regression tests run early to fail fast
3. **Parallel Where Possible**: Performance and intent tests can run in parallel
4. **Clear Names**: Each job clearly describes what it validates
5. **No Skips**: Zero-tolerance tests must pass 100%

---

## Task 3: Verify Gate Functionality

### Test Each Gate Locally

```bash
# 1. Zero-tolerance regression tests
PYTHONPATH=. python -m pytest tests/regression/test_critical_no_mocks.py -v
# Should: Pass 10/10

# 2. Integration tests
PYTHONPATH=. python -m pytest tests/integration/test_critical_flows.py -v
# Should: Pass 16/16

# 3. Performance benchmarks
PYTHONPATH=. python scripts/benchmark_performance.py
# Should: Pass 4/4

# 4. Intent tests
PYTHONPATH=. python -m pytest tests/intent/ -v
# Should: Pass all intent tests

# 5. Coverage check
PYTHONPATH=. python -m pytest --cov=services --cov-fail-under=80
# Should: Meet 80% threshold
```

### Document Results

For each gate:
- Does it run successfully?
- What does it validate?
- What's the failure condition?
- How long does it take?

---

## Task 4: Create CI/CD Documentation

### File: dev/2025/10/07/great5-phase4-cicd-gates.md

Document:
- Complete CI/CD pipeline structure
- All quality gates (what they test, why they matter)
- Gate execution order and dependencies
- How to run gates locally
- What to do if gates fail
- Performance metrics (gate execution time)

### Include Gate Summary Table

```markdown
| Gate | What It Tests | Failure Means | Run Time | Priority |
|------|---------------|---------------|----------|----------|
| Zero-Tolerance Regression | Critical imports, endpoints | Infrastructure broken | ~5s | CRITICAL |
| Integration Tests | End-to-end flows (13 intents) | User flows broken | ~10s | HIGH |
| Performance Benchmarks | Response time, throughput | Performance degraded >20% | ~30s | HIGH |
| Intent Quality | Classification accuracy | Intent system regression | ~60s | HIGH |
| Coverage | Code coverage >80% | Insufficient test coverage | ~30s | MEDIUM |
```

---

## Task 5: Add Badge/Status Indicators (Optional)

If using GitHub Actions, can add status badge to README:

```markdown
![Quality Gates](https://github.com/your-org/piper-morgan/actions/workflows/test.yml/badge.svg)
```

Shows build status at a glance.

---

## Success Criteria

- [ ] CI/CD configuration reviewed and consolidated
- [ ] All quality gates from GREAT-5 integrated
- [ ] All quality gates from GREAT-4E-2 preserved
- [ ] Gate execution order optimized (fail fast)
- [ ] All gates verified working locally
- [ ] Complete documentation created
- [ ] Session log updated

---

## Critical Notes

- **Preserve existing gates**: Don't remove GREAT-4E-2 gates, add to them
- **Fail fast**: Run quick regression tests before slow benchmarks
- **Parallel execution**: Performance and intent tests can run in parallel
- **Clear failures**: Each gate should have clear failure messages
- **Alpha-appropriate**: Don't over-engineer, simple CI is fine

---

## STOP Conditions

- If existing CI/CD configuration is complex and unclear, document and ask PM
- If gates conflict or have circular dependencies, document and ask PM
- If execution time >5 minutes total, consider optimization and ask PM

---

**Effort**: Small-Medium (~30-45 minutes)
**Priority**: HIGH (completes quality gate infrastructure)
**Deliverable**: Consolidated CI/CD pipeline with all quality gates active
