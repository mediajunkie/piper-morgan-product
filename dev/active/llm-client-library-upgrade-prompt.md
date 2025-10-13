# LLM Client Library Upgrade

**Date**: October 12, 2025, 10:44 AM  
**Agent**: Code Agent  
**Epic**: CORE-CRAFT-GAP-2  
**Task**: Upgrade LLM client libraries to fix test failures

---

## Mission

Upgrade ancient LLM client libraries (anthropic 0.7.0, openai 0.28.0) to modern versions to unblock 49 failing tests.

**Context**: Historical investigation revealed libraries are 2 years out of date, causing AttributeError when tests try to use LLM classification.

**Goal**: 143/143 tests passing (100%)

---

## The Fix (Simple)

### Step 1: Upgrade Libraries (5 min)

**Commands**:
```bash
# Upgrade both libraries to latest
pip install --upgrade anthropic openai

# Verify versions
pip list | grep -E "anthropic|openai"

# Expected results:
# anthropic  0.34.x (or later)
# openai     1.50.x (or later)
```

### Step 2: Update Requirements (5 min)

**Files to Update**:
- `requirements.txt`
- `pyproject.toml` (if exists)
- `setup.py` (if exists)

**Example for requirements.txt**:
```txt
# Old (REMOVE):
anthropic==0.7.0
openai==0.28.0

# New (ADD):
anthropic>=0.34.0
openai>=1.50.0
```

**Commit the changes**:
```bash
git add requirements.txt
git commit -m "fix: Upgrade anthropic and openai libraries to modern versions

- anthropic: 0.7.0 → 0.34+
- openai: 0.28.0 → 1.50+
- Fixes LLM client AttributeError in tests
- Unblocks 49 failing tests (8 Direct Interface + 41 Contract)
- Related: GAP-2 LLM service registration investigation
"
```

---

## Testing Strategy

### Step 3: Test Direct Interface (10 min)

**Run the 8 previously failing tests**:
```bash
pytest tests/intent/test_direct_interface.py -v
```

**Expected Result**: 14/14 passing (was 6/14)

**Tests that should now pass**:
- EXECUTION category tests
- ANALYSIS category tests  
- SYNTHESIS category tests
- STRATEGY category tests
- LEARNING category tests
- UNKNOWN category tests
- QUERY category tests
- coverage_report test

### Step 4: Test Contracts (10 min)

**Run the 41 previously failing contract tests**:
```bash
pytest tests/intent/contracts/ -v
```

**Expected Result**: 70/70 passing (was 29/70)

**Test files that should now pass**:
- `test_accuracy_contracts.py` (7 tests)
- `test_bypass_contracts.py` (7 tests)
- `test_error_contracts.py` (13 tests)
- `test_multiuser_contracts.py` (7 tests)
- `test_performance_contracts.py` (7 tests)

### Step 5: Full Validation (10 min)

**Run all intent tests**:
```bash
pytest tests/intent/ -v --tb=short
```

**Expected Result**: 143/143 passing (100%)

**Verify test count**:
```bash
pytest tests/intent/ --collect-only | grep "test session starts"
```

---

## Success Criteria

- [ ] anthropic library upgraded to 0.34+
- [ ] openai library upgraded to 1.50+
- [ ] Requirements files updated
- [ ] Changes committed
- [ ] 14/14 Direct Interface tests passing
- [ ] 70/70 Contract tests passing
- [ ] 143/143 total intent tests passing (100%)
- [ ] No regression in other tests

---

## STOP Conditions

**Stop and report if**:
- Library upgrade causes dependency conflicts
- Tests still failing after upgrade
- New errors introduced
- Need architectural guidance

**Don't stop for**:
- Library downloads taking time
- Tests running (they need to complete)
- Verification thoroughness

---

## Deliverables

### Code Changes

**Files Modified**:
- `requirements.txt` (or equivalent)
- Any other dependency files

### Documentation

**Create**: `dev/2025/10/12/llm-client-library-upgrade.md`

**Contents**:
- Library versions (before/after)
- Test results (before/after)
- Any issues encountered
- Verification evidence

---

## Expected Duration (For PM Planning Only)

**Estimated**: 40 minutes total
- Upgrade + commit: 10 min
- Direct Interface tests: 10 min
- Contract tests: 10 min
- Full validation: 10 min

**Important**: Quality over speed - take time needed to verify completely

---

## Progress Milestones

**Report to PM after**:
- Libraries upgraded
- Direct Interface tests complete
- Contract tests complete
- Any issues discovered

---

## Notes

### Why This Fix is Safe

1. **No code changes**: Only library versions
2. **Modern APIs already in code**: Pattern-012 shows correct usage
3. **Test coverage**: 143 tests will validate
4. **Isolated change**: Affects only LLM client initialization

### What Could Go Wrong

**Scenario 1**: Dependency conflicts
- **Solution**: Use `pip install --upgrade --no-deps` then resolve manually

**Scenario 2**: New library breaking changes
- **Solution**: Check migration guides, adjust code if needed

**Scenario 3**: Tests still failing
- **Solution**: Investigation needed, stop and report

---

**Library Upgrade Prompt Created**: October 12, 2025, 10:44 AM  
**Agent**: Code Agent authorized to proceed  
**Goal**: 143/143 tests passing (100%)  
**Next**: GAP-2 Phase 2 (Evidence Collection) after upgrade complete
