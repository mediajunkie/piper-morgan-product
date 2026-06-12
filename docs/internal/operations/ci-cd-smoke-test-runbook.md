# CI/CD Smoke Test Runbook

**Created**: December 9, 2025
**Purpose**: Smoke test suite deployment and operations guide
**Audience**: DevOps, Release Engineers, and Development Team
**Status**: ✅ **Active** - Smoke test suite production deployment

---

## Overview

The smoke test suite is a **critical-path quality gate** that runs on every push to identify failures in the core system quickly (2-3 seconds execution time).

**Primary Purpose**: Fail fast - prevent wasting time on longer test suites when basic functionality is broken.

---

## Smoke Test Suite Specifications

### Execution Profile

- **Test Count**: 616 tests (87.5% of unit test suite)
- **Execution Time**: 2-3 seconds (40-60% faster than 5s target)
- **Pass Rate**: 100% (verified clean)
- **Coverage**: Integration, Service, and UI/API tests
- **Flakiness**: Zero known flaky tests

### Test Categories Included

- **Integration Tests** (162 tests): Slack, GitHub, MCP, Notion integrations
- **Service Tests** (344 tests): Auth, Analysis, Conversation, LLM services
- **UI/API Tests** (96 tests): Responses, Contracts, Messages endpoints

### Test Categories Excluded

- ❌ Tests >500ms execution time
- ❌ Tests with database dependencies
- ❌ Tests with network I/O
- ❌ LLM tests (require API keys)
- ❌ Manual tests

---

## GitHub Actions Workflow Integration

### Trigger Events

Smoke tests run automatically on:

1. **Every push** (all branches) - for rapid developer feedback
2. **Every pull request** (all branches) - to verify code quality before merge
3. **On schedule** (optional) - daily or on-demand testing

### Workflow Status

- **Workflow File**: `.github/workflows/test.yml`
- **Job Name**: `smoke-tests` (first job in sequence)
- **Run Before**: Full test suite, performance benchmarks, coverage analysis
- **Blocking**: Yes - PR cannot merge if smoke tests fail

### GitHub Check Status

- **Check Name**: "Tests / smoke-tests"
- **Visual Indicator**: Green ✅ (pass) or Red ❌ (fail) on PR/commit
- **Auto-blocking**: Prevents PR merge if configured as required check

---

## Running Smoke Tests

### Local Development

Run smoke tests locally during development:

```bash
# Quick smoke check (2-3 seconds)
python -m pytest -m smoke -q

# Verbose output
python -m pytest -m smoke -v

# With specific test matching
python -m pytest -m smoke -k "test_name_pattern" -v

# Single file
python -m pytest tests/unit/test_file.py -m smoke -v
```

### CI/CD Pipeline

Smoke tests run automatically in GitHub Actions:

```bash
# This is what runs in CI/CD (in .github/workflows/test.yml)
python -m pytest -m smoke -q --tb=short
```

---

## Understanding Smoke Test Failures

### When Smoke Tests Fail in CI

1. **PR shows red X** ❌ on commit/PR
2. **GitHub check fails**: "Tests / smoke-tests"
3. **PR cannot merge** (if required check is enabled)

### Investigation Steps

```bash
# 1. Check which tests failed
python -m pytest -m smoke -v

# 2. Run failed test in isolation
python -m pytest tests/path/to/test_file.py::test_name -xvs

# 3. Check recent commits
git log --oneline -10

# 4. Check test timing (might be >500ms now)
python -m pytest -m smoke --durations=10 -q
```

### Common Failure Causes

| Cause | Action |
|-------|--------|
| Recent code change broke test | Fix the code, push again |
| Test execution time >500ms | Remove @pytest.mark.smoke, add to full suite |
| Infrastructure issue (DB down) | Fix infrastructure, retry |
| Flaky test (intermittent fail) | Investigate flakiness, may need fix |

### Responding to Failures

1. **DO NOT skip smoke tests** in CI/CD
2. **DO NOT disable the failing test** without understanding why
3. **DO fix the code** that broke the test
4. **DO commit and push** - CI/CD will re-run automatically

---

## Smoke Test Performance Monitoring

### Expected Performance

- **Total execution**: 2-3 seconds
- **Per-test average**: ~5-10ms
- **Max single test**: 500ms (by design)

### Monitoring for Regressions

Check if smoke tests are slowing down:

```bash
# Measure execution time
time python -m pytest -m smoke -q

# Get detailed breakdown
python -m pytest -m smoke --durations=10 -q
```

If execution time creeps above 5 seconds:
1. Run detailed timing
2. Identify slow tests
3. Either optimize or remove from smoke suite
4. Maintain <5 second execution target

---

## Adding/Removing Tests from Smoke Suite

### Adding New Tests to Smoke

Only add tests that meet these criteria:
- Execution time <500ms (verified)
- No database dependencies (or very minimal)
- No external API calls (except mocked)
- Critical path functionality
- Reliable/non-flaky

```bash
# 1. Add decorator to test function
@pytest.mark.smoke
def test_my_feature():
    # test code

# 2. Verify it runs
python -m pytest tests/path/to/test_file.py::test_my_feature -m smoke -v

# 3. Commit
git add tests/path/to/test_file.py
git commit -m "feat: Add test_my_feature to smoke suite"
```

### Removing Tests from Smoke

If a test is slowing down or becoming unreliable:

```bash
# 1. Remove decorator
# @pytest.mark.smoke  ← Delete or comment out
def test_my_feature():
    # test code

# 2. Verify removal
python -m pytest -m smoke -q | grep test_my_feature  # Should not appear

# 3. Commit
git commit -m "chore: Remove test_my_feature from smoke suite"
```

---

## GitHub Actions Configuration

### Smoke Test Job Definition

In `.github/workflows/test.yml`:

```yaml
  smoke-tests:
    name: Smoke Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run smoke tests (critical path)
        run: |
          echo "🔥 Running smoke test suite (616 tests, <5s target)"
          python -m pytest -m smoke -q --tb=short
          echo "✅ Smoke tests passed"
```

### Setting as Required Check

In GitHub repository settings:

1. Go to **Settings → Branches → Branch protection rules**
2. Edit rule for `main` branch
3. Under "Require status checks to pass": Add **"Tests / smoke-tests"**
4. This prevents PR merge if smoke tests fail

---

## Notification Configuration

### GitHub Native Notifications

Automatic via GitHub Actions:

- **✅ Success**: PR shows green checkmark
- **❌ Failure**: PR shows red X, comment shows failure details
- **⏸️ In Progress**: PR shows loading icon while tests run

### Slack Integration (Optional)

To notify Slack on failures:

1. Create GitHub Action that sends Slack message on failure
2. Or use Slack GitHub App integration (native)

**Recommended**: Use native GitHub notifications first, add Slack if needed.

### Email Notifications

Automatic GitHub email (default):
- Sends on failure
- May be noisy for fast feedback cycles
- Can be customized in GitHub notification settings

---

## Troubleshooting

### Smoke Tests Won't Run

**Symptom**: Tests not collected
**Solution**:
```bash
pytest -m smoke --collect-only | grep "smoke"
# Should show 616 collected tests
```

### Some Tests Marked as Smoke But Slow

**Symptom**: Smoke execution >5 seconds
**Solution**:
```bash
python -m pytest -m smoke --durations=10 -q
# Find slow tests, check if they still <500ms
# If >500ms, remove @pytest.mark.smoke decorator
```

### Flaky Smoke Test

**Symptom**: Test passes locally, fails in CI or vice versa
**Solution**:
1. Run test 10 times locally: `for i in {1..10}; do pytest test_name.py; done`
2. If fails sometimes: test is flaky, needs investigation
3. Consider removing from smoke suite if can't fix
4. File issue to fix flakiness

### Smoke Tests Pass Locally, Fail in CI

**Symptom**: `pytest -m smoke` works locally but fails in GitHub Actions
**Possible Causes**:
- Different Python version in CI (should be 3.11)
- Missing environment variables
- Database not available in CI
- Race conditions from parallel test execution

**Solution**:
```bash
# Check Python version in CI
python --version  # Should be 3.11

# Run tests sequentially (like CI does)
python -m pytest -m smoke -n0 -v

# Check for environment variables
env | grep -i piper
```

---

## Performance Baselines

These are the established performance baselines for smoke tests:

| Metric | Value | Status |
|--------|-------|--------|
| **Total execution time** | 2-3 seconds | ✅ 40-60% under 5s target |
| **Average per-test** | 5-10ms | ✅ Well under 500ms threshold |
| **Slowest test** | ~400-500ms | ✅ At threshold but acceptable |
| **Pass rate** | 100% | ✅ Zero flakes |
| **Test count** | 616 tests | ✅ 87.5% of unit tests |

---

## Decision Log

### December 9, 2025 - Smoke Test Suite Deployment

**Decision**: Deploy smoke test suite as first CI/CD quality gate on every push

**Rationale**:
- Ultra-fast execution (2-3 seconds) = no pipeline delays
- Comprehensive coverage (87.5% of tests) = reliable safety net
- Zero flakes and 100% pass rate = no false failures
- Clear fail-fast strategy = prevents wasting time on longer tests

**Approval**: Automatic for all branches (not just main)

**Notification**: GitHub native checks (red X if fail, prevents merge to main)

---

## Related Documentation

- T2 Sprint Final Report *(proposed; doc TBD)* - Complete test suite analysis
- [Issue #277](https://github.com/mediajunkie/piper-morgan-product/issues/277) - Smoke test discovery (CLOSED)
- [Issue #341](https://github.com/mediajunkie/piper-morgan-product/issues/341) - Test Infrastructure Epic (CLOSED)
- [pytest markers](pytest.ini) - Smoke test marker definition

---

**Last Updated**: December 9, 2025
**Maintained By**: DevOps / Development Team
**Version**: 1.0 - Initial deployment
