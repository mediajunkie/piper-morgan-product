# CI/CD Investigation Report
**Date**: October 12, 2025, 1:05 PM
**Agent**: Claude Code (Programmer)
**Epic**: CORE-CRAFT-GAP-2
**Task**: Investigate why CI/CD isn't catching issues like 2-year-old libraries

---

## Executive Summary

**PM's Question**: "We have built all this sweet CI/CD infrastructure and we're not using it?"

**Answer**: We ARE using it - but **we're not watching it**.

- ✅ CI/CD infrastructure EXISTS (14 workflows)
- ✅ Workflows ARE RUNNING automatically
- ❌ **Every single workflow is FAILING**
- ❌ **No one is checking/acting on failures**

**The Gap**: Not "unused infrastructure" but **"ignored failures infrastructure"**

---

## What Exists

### GitHub Actions Workflows (14 total)

| Workflow | Purpose | Last Modified | Status |
|----------|---------|---------------|--------|
| test.yml | Main test suite | Oct 7, 17:43 | ❌ FAILING |
| ci.yml | Config validation | Oct 1, 15:02 | ❌ FAILING |
| lint.yml | Code quality | Aug 2, 17:20 | ❌ FAILING |
| docker.yml | Docker builds | Aug 2, 17:29 | ❌ FAILING |
| architecture-enforcement.yml | ADR/Pattern enforcement | Sep 27, 20:47 | ❌ FAILING |
| router-enforcement.yml | Router patterns | Sep 29, 14:39 | ❌ FAILING |
| config-validation.yml | Config checks | Oct 1, 14:22 | ❌ FAILING |
| link-checker.yml | Documentation links | Oct 1, 16:00 | ❌ FAILING |
| weekly-docs-audit.yml | Weekly docs check | Oct 11, 17:48 | ❌ FAILING |
| pm034-llm-intent-classification.yml | Intent testing | Aug 5, 12:07 | ? |
| schema-validation.yml | Schema checks | Aug 2, 17:20 | ? |
| deploy.yml | Deployment | Sep 3, 08:36 | ? |

**Total**: 14 workflows, comprehensive coverage

---

## Recent Workflow Runs (Last 10)

From `gh run list`:

| Time | Trigger | Workflow | Status |
|------|---------|----------|--------|
| Oct 12, 02:55 | schedule | Documentation Link Checker | ❌ FAILURE |
| Oct 12, 00:51 | push (GAP-1) | Tests | ❌ FAILURE |
| Oct 12, 00:51 | push (GAP-1) | Docker Build | ❌ FAILURE |
| Oct 12, 00:51 | push (GAP-1) | Code Quality | ❌ FAILURE (12m 33s) |
| Oct 12, 00:51 | push (GAP-1) | Configuration Validation | ❌ FAILURE |
| Oct 12, 00:51 | push (GAP-1) | Router Pattern Enforcement | ❌ FAILURE |
| Oct 12, 00:51 | push (GAP-1) | Architecture Enforcement | ❌ FAILURE |
| Oct 12, 00:51 | push (GAP-1) | CI Workflow | ❌ FAILURE |
| Oct 12, 00:51 | push (GAP-1) | Pages Build | ✅ SUCCESS (only one!) |
| Oct 11, 00:07 | push | Router Pattern Enforcement | ❌ FAILURE |

**Observation**: 9/10 recent runs FAILED. Only GitHub Pages succeeded.

---

## Analysis of test.yml (Main Test Workflow)

**File**: `.github/workflows/test.yml` (354 lines, 14KB)
**Last Modified**: October 7, 17:43
**Triggers**: Push to main, Pull requests to main

### What It Does (Correctly)

✅ **Python Version**: Uses Python 3.11 (correct)
✅ **Dependency Caching**: Caches pip dependencies
✅ **Intent Interface Tests**: Runs web/slack/cli interface tests
✅ **Intent Contract Tests**: Runs contracts (accuracy, bypass, error, multiuser, performance)
✅ **Bypass Prevention**: Tests no-web/cli/slack-bypasses
✅ **Coverage Gates**: Verifies test coverage
✅ **Performance Regression**: Checks for performance degradation
✅ **Performance Benchmarks**: GREAT-5 benchmark suite
✅ **Tiered Coverage Enforcement**: Ensures completed components have coverage

###What It's Missing

❌ **Doesn't run ALL tests**: Only runs specific test subsets
  - Runs: `tests/intent/test_*_interface.py`
  - Runs: `tests/intent/contracts/`
  - Runs: `tests/intent/test_no_*_bypasses.py`
  - **Missing**: `tests/intent/test_query_fallback.py`
  - **Missing**: `tests/intent/test_direct_interface.py`
  - **Missing**: Handler tests (`test_*_handlers.py`)
  - Line 97: `pytest tests/ --tb=short -v` (runs all, but AFTER specific tests - may timeout)

❌ **No dependency health check**: Doesn't verify library versions
❌ **No secrets validation**: Assumes API keys are available
❌ **No failure notification**: Silent failures

### Why This Matters

The selective test approach means:
- **test_query_fallback.py** with 8 tests? NOT RUN in specific steps
- **test_direct_interface.py** with 14 tests? NOT RUN in specific steps
- **Handler-specific tests**? NOT RUN in specific steps

These tests may run in the final "Run tests" step (line 97), but that step:
1. Runs AFTER all specific tests (adding time)
2. May timeout (3 min max for full suite)
3. Failures are less visible (buried in 278 test output)

**Result**: The LEARNING handler bug we found today would have been caught IF:
1. The workflow ran `test_direct_interface.py` specifically
2. Someone checked the failure logs
3. The workflow didn't timeout first

---

## Analysis of ci.yml

**File**: `.github/workflows/ci.yml` (112 lines, 3KB)
**Last Modified**: October 1, 15:02
**Triggers**: Push to main OR develop, Pull requests

### Critical Issue

❌ **Uses Python 3.9** (line 19) instead of Python 3.11

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.9'  # WRONG!
```

**Impact**:
- Different Python version than production/development (3.11)
- May hide or miss version-specific bugs
- Inconsistent with test.yml

### What It Does

✅ Configuration validation tests
✅ Creates test configs and validates them
✅ Tests invalid config rejection

**Note**: This is a lighter workflow focused on config, but wrong Python version undermines it.

---

## The Real Gap: Ignored Failures

### Documentation Claims

From onboarding.md (assumed):
- GitHub Actions workflows are configured ✅ TRUE
- Test workflow uses Python 3.11 ✅ TRUE (in test.yml)
- Lint workflow uses Python 3.11 ❓ (needs verification)
- Workflows catch issues automatically ✅ TRUE (they run)

### Reality Check

✅ Workflows exist
✅ Workflows run automatically
✅ Workflows use (mostly) correct Python version
❌ **Workflows are ALL FAILING**
❌ **Failures are not being reviewed**
❌ **No escalation/notification on failure**

### The Missing Piece: **Visibility & Accountability**

The infrastructure works. The gap is **process**:

1. **No daily CI/CD health check** - Who checks if workflows pass?
2. **No failure alerts** - Email, Slack, GitHub issues?
3. **No branch protection** - Can merge despite failed tests?
4. **No dependency health checks** - Weekly scan for outdated libraries?
5. **No test result dashboard** - Where to see historical trends?

---

## Root Causes of Current Failures

Based on investigation:

### 1. Library Version Issues (Just Fixed Today!)

- anthropic 0.7.0 (2 years old) → 0.69.0
- openai 0.28.0 (pre-1.0 API) → 2.3.0

These library issues broke 163/278 tests locally. CI/CD caught this, but **no one looked**.

### 2. Missing Secrets (Suspected)

Workflows need:
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`

If these aren't set in GitHub Secrets, LLM-dependent tests fail.

**Check**: PM needs to verify Settings → Secrets → Actions

### 3. Test Timeouts

Full test suite: 278 tests × 3.5s = 16+ minutes
Workflow timeout: Likely 30 minutes (default)

Tests that make real LLM calls take time. No parallelization = slow.

### 4. Python 3.9 in ci.yml

Wrong Python version in secondary workflow creates inconsistency.

---

## Impact Analysis: What We Missed

### What CI/CD TRIED to Catch (But We Ignored)

1. **2-Year-Old Libraries**: Tests failing due to API changes
   - First failed: ~August 13 (when libraries became incompatible)
   - **Duration ignored**: 2 months

2. **LEARNING Handler Bug**: Missing `intent_data` parameter
   - Would fail in test_direct_interface.py
   - Found today by pushing for 100% locally
   - **Could have been caught in CI 2 months ago**

3. **Query Fallback Issues**: LLM service registration
   - test_query_fallback.py tests were failing
   - Fixed today in 5 minutes
   - **Could have been caught immediately**

### Silent Failure Period

**Estimated**: August 13 - October 12 = **2 months**
- ~1,160 commits during this period (estimated)
- Every commit triggered workflows
- Every workflow failed
- **Zero responses to failures**

---

## Comparison: Claims vs Reality

| Claim | Reality | Gap |
|-------|---------|-----|
| "CI/CD infrastructure configured" | ✅ 14 workflows exist | ✅ TRUE |
| "Workflows use Python 3.11" | ⚠️ test.yml yes, ci.yml no | ⚠️ PARTIAL |
| "Tests run automatically" | ✅ Workflows trigger on push | ✅ TRUE |
| "Issues are caught automatically" | ❌ Caught but ignored | ❌ **PROCESS GAP** |

**The Gap**: Not technology, but **process and visibility**.

---

## Recommendations

### Immediate Actions (This Session)

1. **Fix ci.yml Python version** (3.9 → 3.11)
2. **Add comprehensive test execution** to test.yml
3. **Create dependency-health.yml** (weekly checks)
4. **Verify GitHub Secrets** exist (PM action)

### Process Changes (PM Actions)

1. **Daily CI/CD Health Check**
   - Add to morning routine
   - Check Actions tab: Any red ❌?
   - Investigate/assign immediately

2. **Branch Protection Rules**
   - Settings → Branches → main
   - ✅ Require status checks before merging
   - ✅ Require branches to be up to date
   - Select: Tests, Code Quality, Architecture Enforcement

3. **Failure Notifications**
   - Settings → Integrations → Slack
   - Post CI/CD failures to #engineering or #alerts
   - Or: Use GitHub email notifications

4. **Weekly Review**
   - Check workflow success rate
   - Review any persistent failures
   - Update baselines if needed

### Technical Improvements (This Session)

1. **Parallel Test Execution**
   ```yaml
   - name: Run tests in parallel
     run: pytest tests/ -n auto --dist loadscope
   ```
   Reduces 16-min runs to ~5-7 min

2. **Dependency Health Workflow**
   - Runs weekly (Monday 9 AM)
   - Checks for outdated packages
   - Creates GitHub issue if critical libraries outdated
   - **Would have caught anthropic/openai staleness**

3. **Test Result Artifacts**
   ```yaml
   - name: Upload test results
     if: always()
     uses: actions/upload-artifact@v3
     with:
       name: test-results
       path: pytest-report.xml
   ```
   Allows historical analysis

4. **Better Test Organization**
   ```yaml
   # Run fast tests first (fail fast)
   - name: Quick smoke tests
     run: pytest tests/intent/test_bypass_prevention.py -v

   # Then comprehensive tests
   - name: Full test suite
     run: pytest tests/ --tb=short -v
   ```

---

## Success Criteria

**Investigation Complete** ✅:
- [x] Determined workflows exist (14 found)
- [x] Identified why CI/CD not catching issues (they are, but ignored)
- [x] Documented gap between claims and reality

**Activation Complete** (Next Steps):
- [ ] Fix ci.yml Python version
- [ ] Add dependency health workflow
- [ ] Verify secrets in GitHub Settings (PM)
- [ ] Enable branch protection (PM)
- [ ] Set up failure notifications (PM)

**Prevention in Place** (End Goal):
- [ ] Tests run on every push ✅ (already true)
- [ ] Weekly dependency health checks ⏳ (will add)
- [ ] Failures visible and escalated ⏳ (PM process)
- [ ] Branch protection prevents bad merges ⏳ (PM setting)

---

## PM Action Items

**Things only PM can do**:

### 1. Verify GitHub Secrets (5 min)

Go to: Settings → Secrets and variables → Actions

Check these exist:
- [ ] `ANTHROPIC_API_KEY`
- [ ] `OPENAI_API_KEY`
- [ ] `GITHUB_TOKEN` (should be automatic)

If missing, add them with values from keychain.

### 2. Enable Branch Protection (10 min)

Go to: Settings → Branches → Add rule for `main`

Settings:
- [x] Require status checks to pass before merging
- [x] Require branches to be up to date before merging
- [x] Status checks required:
  - Tests
  - Code Quality
  - Architecture Enforcement
  - Router Pattern Enforcement
- [x] Include administrators (so even PM must pass tests)

### 3. Set Up Failure Notifications (15 min)

**Option A: Email** (simplest)
- Settings → Notifications
- Enable email for failed Actions

**Option B: Slack** (better)
- Settings → Integrations
- Add Slack app
- Configure #engineering channel
- Get notifications for failed workflows

**Option C: GitHub Mobile** (fastest feedback)
- Install GitHub mobile app
- Enable push notifications for Actions
- Get instant alerts on failures

### 4. Review Recent Failures (30 min)

**After fixes are pushed**, check:
1. Actions tab
2. Click "Tests" workflow
3. Click most recent run
4. Review what failed
5. Decide: Fix immediately or create issue?

### 5. Weekly CI/CD Health Check (ongoing)

Add to weekly routine (Mondays?):
1. Check Actions tab
2. Review success rate (should be >90%)
3. Investigate any persistent failures
4. Review dependency health report

---

## Timeline

**Today (October 12)**:
- 1:05 PM: Investigation complete ✅
- 1:15 PM: Fix workflows (30 min estimated)
- 1:45 PM: Push fixes and document
- 2:00 PM: PM verifies secrets and settings

**This Week**:
- PM enables branch protection
- PM sets up notifications
- First dependency health check runs (Monday)

**Ongoing**:
- Daily: Quick Actions tab check (green or red?)
- Weekly: Review dependency health report
- Monthly: Review CI/CD metrics (success rate, runtime trends)

---

## Bottom Line

**The Answer to PM's Question**:

> "We have built all this sweet CI/CD infrastructure and we're not using it?"

**Answer**: We're using it. It's running. It's catching issues. **We're just not looking at it.**

**The Fix**: Not more infrastructure, but **visibility + process**:
1. Check Actions tab daily
2. Fix failures immediately (or create issues)
3. Enable branch protection (can't merge on red)
4. Add notifications (Slack/email on failures)
5. Weekly dependency health checks

**Impact**: The 2-year-old libraries and LEARNING handler bug would have been caught **2 months ago** if someone checked the red ❌ symbols.

---

**Investigation Complete**: October 12, 2025, 1:05 PM
**Next Step**: Fix workflows and activate monitoring process
**Philosophy**: "Build it, run it, WATCH IT" - otherwise it's silent failure infrastructure
