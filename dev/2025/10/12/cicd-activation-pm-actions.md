# CI/CD Activation - PM Action Items
**Date**: October 12, 2025, 1:15 PM
**Status**: Ready for PM Review
**Time Required**: ~30 minutes total

---

## What We Found

✅ CI/CD infrastructure EXISTS and is RUNNING
❌ Every workflow is FAILING (but no one was checking)
✅ Fixed 2 issues, need PM actions to complete activation

**The Gap**: Not "we're not using it" but "we're not watching it"

---

## What We Fixed (Just Now)

### 1. ✅ ci.yml Python Version
- **Changed**: Python 3.9 → 3.11
- **File**: `.github/workflows/ci.yml`
- **Impact**: Consistent Python version across all workflows

###2. ✅ Created dependency-health.yml
- **New File**: `.github/workflows/dependency-health.yml`
- **What It Does**:
  - Runs every Monday at 9 AM
  - Checks for outdated packages
  - **Creates GitHub issue if critical libraries are too old**
  - Would have caught the 2-year-old anthropic/openai libraries

### 3. ✅ Investigation Report
- **File**: `dev/2025/10/12/cicd-investigation-report.md`
- **Contains**: Full analysis of what exists, what's failing, recommendations

---

## Your Action Items (In Priority Order)

### 1. Verify GitHub Secrets ⏱️ 5 minutes

**Why**: Workflows need API keys to run LLM tests

**Steps**:
1. Go to GitHub repository
2. Click: Settings → Secrets and variables → Actions
3. **Check these secrets exist**:
   - `ANTHROPIC_API_KEY`
   - `OPENAI_API_KEY`

**If Missing**:
```bash
# Get keys from keychain locally
security find-generic-password -s "anthropic" -w
security find-generic-password -s "openai" -w

# Add to GitHub:
# Settings → Secrets → New repository secret
# Name: ANTHROPIC_API_KEY, Value: [paste key]
# Name: OPENAI_API_KEY, Value: [paste key]
```

**How to Tell If Done**: Secrets page shows 2 secrets listed

---

### 2. Enable Branch Protection ⏱️ 10 minutes

**Why**: Prevent merging code when tests fail

**Steps**:
1. Go to: Settings → Branches
2. Click: "Add rule" for branch `main`
3. **Configure**:
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Select these required checks:
     - Tests
     - Code Quality
     - Architecture Enforcement
     - Router Pattern Enforcement
   - ✅ Include administrators (even you must pass tests!)
4. Click: "Create" or "Save changes"

**How to Tell If Done**:
- Try to merge a PR with failing tests → Blocked
- Main branch shows "Protected" badge
- Can't force push to main

---

### 3. Set Up Failure Notifications ⏱️ 15 minutes

**Why**: Get alerted when workflows fail (don't rely on checking manually)

**Option A: Email** (Simplest - 2 min)
1. Your GitHub Settings → Notifications
2. ✅ Enable "Actions" notifications
3. ✅ Choose email delivery

**Option B: Slack** (Best - 15 min)
1. Go to: Repository Settings → Integrations
2. Add Slack integration
3. Configure channel: #engineering or #ci-alerts
4. Select events: "Workflow run failures"

**Option C: GitHub Mobile** (Fastest - 5 min)
1. Install GitHub mobile app
2. Enable push notifications
3. Enable "Actions" notifications
4. Get instant alerts on your phone

**Recommendation**: Do Option A (email) immediately, Option B (Slack) when you have time

**How to Tell If Done**:
- Manually trigger a failing workflow
- Receive notification within 1 minute

---

### 4. Review Current Failures ⏱️ 30 minutes

**Why**: Understand what's broken right now

**Steps**:
1. Go to: Actions tab on GitHub
2. Click: "Tests" workflow
3. Click: Most recent run (should be from today)
4. **Review each failed step**:
   - Red ❌ means failure
   - Click to expand and see error
5. **For each failure, decide**:
   - Fix now (simple) OR
   - Create GitHub issue (complex) OR
   - Known issue (document)

**Common Failures to Expect** (based on investigation):
- Missing secrets → Fixed by Action #1
- Old library issues → Already fixed locally (need to push)
- Timeout issues → May need test parallelization

**How to Tell If Done**:
- You have a list of known failures
- Each has either: fix in progress, issue created, or documented as known

---

### 5. Commit and Push Workflow Fixes ⏱️ 2 minutes

**What**: Push the fixes we just made

**Steps**:
```bash
# Check what changed
git status

# Should show:
# modified:   .github/workflows/ci.yml
# new file:   .github/workflows/dependency-health.yml
# new file:   dev/2025/10/12/cicd-investigation-report.md
# new file:   dev/2025/10/12/cicd-activation-pm-actions.md

# Commit
git add .github/workflows/ci.yml .github/workflows/dependency-health.yml
git add dev/2025/10/12/cicd-*.md
git commit -m "ci: Fix Python version and add dependency health checks

- Update ci.yml to use Python 3.11 (was 3.9)
- Add weekly dependency-health.yml workflow
- Creates GitHub issue if critical libraries outdated
- Would have caught 2-year-old anthropic/openai libs

Investigation: dev/2025/10/12/cicd-investigation-report.md
"

# Push
git push origin main
```

**How to Tell If Done**:
- GitHub Actions tab shows new workflow run
- dependency-health workflow appears in workflows list

---

## Ongoing Process (After Activation)

### Daily: Quick CI Health Check ⏱️ 1 minute

**Every morning or after pushing code**:

1. Go to GitHub → Actions tab
2. Quick scan: See any red ❌?
3. **If YES**: Click, read error, decide:
   - Fix immediately (< 5 min fix) OR
   - Create issue (assign, prioritize) OR
   - Known/acceptable (document)
4. **If NO**: ✅ All good, continue with day

**Goal**: Never let failures sit ignored

---

### Weekly: Dependency Health Review ⏱️ 5 minutes

**Every Monday** (after dependency-health workflow runs):

1. Check email/Slack for dependency health report
2. **If issue created** ("🚨 Critical Dependencies Outdated"):
   - Review which libraries are outdated
   - Schedule upgrade (that week)
   - Update requirements.txt
3. **If warnings only** (non-critical outdated):
   - Review list
   - Decide: Upgrade now or later?
   - Create issue if many outdated

**Goal**: Never get 2 years behind on libraries again

---

### Monthly: CI/CD Metrics Review ⏱️ 15 minutes

**First Monday of each month**:

1. Review workflow success rate:
   - Actions → Select workflow → "View all runs"
   - Count: Green vs Red over last month
   - **Goal**: >90% success rate
2. Review workflow runtime trends:
   - Are tests getting slower?
   - Need parallelization?
3. Review persistent failures:
   - Same test failing repeatedly? → Flaky test, fix or skip
   - Same workflow failing? → Infrastructure issue

**Goal**: Proactive improvement, not reactive firefighting

---

## Success Criteria (How to Know It's Working)

### ✅ Immediate (This Week)
- [ ] GitHub Secrets configured (Action #1)
- [ ] Branch protection enabled (Action #2)
- [ ] Notifications set up (Action #3)
- [ ] Current failures reviewed (Action #4)
- [ ] Workflow fixes pushed (Action #5)

### ✅ Short-term (Next 2 Weeks)
- [ ] All workflows passing (green ✅ in Actions tab)
- [ ] No failed workflows go unreviewed
- [ ] First dependency health report received (next Monday)
- [ ] Branch protection prevents bad merge (test it!)

### ✅ Long-term (Ongoing)
- [ ] >90% workflow success rate
- [ ] Dependencies never >6 months old
- [ ] Failures fixed within 24 hours
- [ ] No "surprise" bugs in production (caught in CI)

---

## FAQs

### Q: What if a workflow fails after I enable branch protection?

**A**: Good! That's the system working. You can't merge until tests pass. Options:
1. Fix the code
2. Fix the test (if test is wrong)
3. Temporarily disable protection (NOT RECOMMENDED)
4. Push fix to same branch (retriggers checks)

### Q: What if I need to merge urgently despite failing tests?

**A**: Two options:
1. **Recommended**: Fix tests first (usually faster than you think)
2. **Emergency only**: Admin override (you have admin access)

**BUT**: If you override, create issue immediately to fix tests

### Q: Will this slow down development?

**A**: Initially maybe 5-10 minutes per PR (waiting for tests). But:
- Catches bugs before production
- Prevents "oh no, we broke main" moments
- Actually speeds up development (less debugging)

**Balance**: Fast tests (< 5 min) for common workflows, slower comprehensive tests nightly

### Q: What if tests are flaky (fail randomly)?

**A**: That's a test quality issue. Options:
1. Fix flaky test (best)
2. Mark as "allowed to fail" temporarily
3. Skip flaky test (with issue to fix)

**Never**: Disable all checks because one test is flaky

### Q: How do I manually trigger a workflow?

**A**:
1. Go to Actions tab
2. Select workflow (e.g., "Dependency Health Check")
3. Click "Run workflow" button (if `workflow_dispatch` enabled)
4. Select branch, click "Run"

---

## What Happens Next

### Today (October 12)
1. You review this document ✅
2. You complete Actions #1-5 (30 min total) ⏱️
3. Workflows start passing ✅
4. Branch protection prevents bad merges ✅

### Monday (October 14)
1. First dependency health check runs (9 AM UTC)
2. You receive report
3. Confirms all libraries current (they are, we just upgraded!)

### Ongoing
1. Daily CI health check (1 min/day)
2. Weekly dependency review (5 min/week)
3. Monthly metrics review (15 min/month)

**Total time investment**: ~10-15 min/week to prevent 2-month gaps

---

## Bottom Line

**The Answer to Your Question**:
> "We have built all this sweet CI/CD infrastructure and we're not using it?"

**We ARE using it** - it's running on every commit.
**We WEREN'T watching it** - all failures ignored for 2 months.

**The Fix**: Not more code, but **visibility + process**:
1. Check Actions tab (you'll see red or green)
2. Fix reds immediately (or create issues)
3. Enable branch protection (can't merge on red)
4. Add notifications (get alerted, don't manually check)
5. Weekly dependency health (prevent library staleness)

**Impact**: The issues we found today (2-year-old libraries, LEARNING bug) would have been caught **2 months ago** with these 5 actions done.

---

**Created**: October 12, 2025, 1:15 PM
**Estimated Time to Complete**: 30 minutes
**Long-term Time**: 10-15 minutes/week
**Next Step**: Complete Actions #1-5 above

**Questions?** Review the full investigation report: `dev/2025/10/12/cicd-investigation-report.md`
