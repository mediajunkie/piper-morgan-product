# Prompt for Cursor Agent: GREAT-4E-2 Phase 3 - CI/CD Verification

## Context

Phase 2 complete: All documentation created (7/9 items done).

**This is Phase 3**: Verify and enhance CI/CD integration for intent system

## Session Log

Continue: `dev/2025/10/06/2025-10-06-0752-prog-cursor-log.md`

## Mission

Verify that GREAT-4E's 126 tests run in CI/CD pipeline and add intent-specific gates if missing.

---

## Phase 3: CI/CD Verification (1 Item)

### Task 1: Verify Test Coverage in CI

Check if GREAT-4E tests run in existing CI workflows:

```bash
# Check main CI workflow
cat .github/workflows/ci.yml

# Look for intent test execution
grep -n "intent" .github/workflows/ci.yml

# Check test workflow
cat .github/workflows/test.yml

# Check what pytest commands run
grep -n "pytest" .github/workflows/*.yml
```

**Document findings**:
- Do GREAT-4E tests (126 tests) run in CI currently?
- Which workflow file runs them?
- Are all test types included (interface tests, contract tests)?

### Task 2: Add Intent-Specific CI Gates (If Missing)

If GREAT-4E tests don't run in CI, add them to `.github/workflows/ci.yml` or `.github/workflows/test.yml`:

**Option A: If tests already run**
- Document that they're already included
- Verify bypass detection runs
- Mark as complete

**Option B: If tests don't run**
Add to CI workflow:

```yaml
# In .github/workflows/ci.yml or test.yml

- name: Run Intent Interface Tests
  run: |
    pytest tests/intent/test_*_interface.py -v
    # Should show 56/56 passing

- name: Run Intent Contract Tests
  run: |
    pytest tests/intent/contracts/ -v
    # Should show 70/70 passing

- name: Verify Intent Bypass Prevention
  run: |
    pytest tests/intent/contracts/test_bypass_contracts.py -v
    # Must pass - critical security check

- name: Intent System Coverage Gate
  run: |
    echo "Verifying intent test coverage..."
    TEST_COUNT=$(pytest tests/intent/ --collect-only -q | grep "test session" | awk '{print $1}')
    if [ "$TEST_COUNT" -lt 126 ]; then
      echo "Error: Expected 126 intent tests, found $TEST_COUNT"
      exit 1
    fi
    echo "✅ Intent coverage verified: $TEST_COUNT tests"
```

### Task 3: Add Classification Accuracy Gate (Optional Enhancement)

If you want to add a quality gate for classification accuracy:

```yaml
- name: Classification Accuracy Gate
  run: |
    # Run accuracy tests
    pytest tests/intent/contracts/test_accuracy_contracts.py -v

    # Verify >90% accuracy threshold
    echo "✅ Classification accuracy verified"
  continue-on-error: false  # Fail build if accuracy drops
```

### Task 4: Create Verification Report

Create: `dev/2025/10/06/great4e-2-phase3-cursor-ci-verification.md`

```markdown
# GREAT-4E-2 Phase 3: CI/CD Verification Report

**Date**: October 6, 2025
**Agent**: Cursor Agent
**Duration**: [X minutes]

## Current CI/CD State

### Workflow Files Found
- `.github/workflows/ci.yml`: [YES/NO - describe what it does]
- `.github/workflows/test.yml`: [YES/NO - describe what it does]
- `.github/workflows/pm034-llm-intent-classification.yml`: [Describe]

### Intent Tests in CI

**Currently Running**: YES/NO

**Test Commands Found**:
```bash
[List actual pytest commands from workflows]
```

**Coverage**:
- Interface tests (56 tests): [YES/NO - running in CI]
- Contract tests (70 tests): [YES/NO - running in CI]
- Bypass detection: [YES/NO - running in CI]
- Total: [X/126 tests running]

## Changes Made

### Option A: No Changes Needed
[If tests already run comprehensively]

All GREAT-4E tests already run in CI via [workflow-name].
- Interface tests: ✅ Running
- Contract tests: ✅ Running
- Bypass detection: ✅ Running
- Coverage gate: ✅ Present

**Status**: CI/CD integration verified ✅

### Option B: Enhanced CI Pipeline
[If changes were made]

**Changes to** `.github/workflows/[file].yml`:

1. Added intent interface tests
2. Added intent contract tests
3. Added bypass prevention verification
4. Added coverage gate (126 tests minimum)

**Before**:
- Intent tests: [describe previous state]

**After**:
- Intent tests: All 126 tests run in CI
- Coverage gate: Enforces minimum test count
- Bypass detection: Critical security check

**Verification**:
```bash
# Test the changes locally
act -j test  # If using act for local CI testing

# Or check workflow syntax
yamllint .github/workflows/ci.yml
```

## Recommendations

### For Immediate Implementation
- [List any critical missing pieces]

### For Future Enhancement
- Add classification accuracy trending
- Add performance regression detection
- Add automatic rollback on test failures

## Summary

**Status**: [COMPLETE/NEEDS_WORK]
**CI Integration**: [VERIFIED/ENHANCED/PARTIAL]
**Action Items**: [List any followup needed]

---

**Phase 3 Complete**: [YES/NO]
**Blockers**: [List any issues]
```

---

## File Naming Convention

**Save your work as**: `great4e-2-phase3-cursor-ci-verification.md`

This matches the report template name and avoids conflicts.

---

## Success Criteria

- [ ] Current CI state documented
- [ ] GREAT-4E test coverage in CI verified
- [ ] Intent-specific gates added (if missing)
- [ ] Bypass detection verified in CI
- [ ] Verification report created
- [ ] Session log updated

---

## Validation

After completion, verify:

```bash
# Check that workflow file is valid YAML
yamllint .github/workflows/*.yml

# If changes were made, verify they work
# (This would require triggering CI, which may not be possible locally)

# Verify report exists
cat dev/2025/10/06/great4e-2-phase3-cursor-ci-verification.md
```

---

## Critical Notes

- **Don't break existing CI** - be very careful with workflow changes
- **Test syntax** - YAML is whitespace-sensitive
- **If unsure** - document current state and recommend changes rather than making them
- **Bypass detection is critical** - this must run in CI

---

**Effort**: Small (~15 minutes)
**Priority**: HIGH (CI/CD integration is acceptance criteria)
**Deliverable**: CI/CD verification report + any necessary workflow updates
