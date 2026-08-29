# E2E Bug Fix Execution Protocol

## Overview

When assigned to fix an E2E bug (Phase 3), agents MUST follow this protocol integrating TDD, DDD, and Excellence Flywheel principles.

---

## Pre-Fix Verification (Excellence Flywheel)

**MANDATORY FIRST STEP**: Before writing any code, verify existing patterns:

```bash
# Find existing patterns
grep -r "pattern_name" services/ --include="*.py" -A 5 -B 5

# Check domain models
cat services/domain/models.py | grep "DomainConcept"

# Check ADRs for architectural decisions
find docs/internal/architecture/adrs -name "*relevant-adr*.md"

# Check pattern library
find docs/internal/architecture/patterns -name "*pattern*.md"
```

**Why**: Understanding existing patterns prevents reinventing solutions and ensures consistency.

---

## Fix Execution Steps

### Step 1: Write Failing Test (TDD)

**MANDATORY**: Write test FIRST that reproduces the bug.

```python
def test_bug_issue_number_description():
    """
    Reproduces bug #[N]: [Brief description]
    """
    # Arrange: Set up scenario that reproduces bug
    # Act: Perform action that triggers bug
    # Assert: Verify expected behavior (this will fail initially)
    assert expected_behavior == actual_behavior
```

**Requirements**:

- Test must fail initially (proving it reproduces bug)
- Test must be minimal (isolate the bug)
- Test must be clear (anyone can understand what's being tested)

**Evidence Required**: Test failure output showing bug reproduced

---

### Step 2: Verify Domain Model (DDD)

**MANDATORY**: Check domain model before implementing fix.

```bash
# Check domain models
cat services/domain/models.py | grep -A 10 "RelevantDomainConcept"
```

**Questions to Answer**:

- Does the bug violate domain invariants?
- What domain rules apply to this scenario?
- Does the fix need to respect domain model constraints?

**If Domain Model Conflict**:

- **STOP** and document the conflict
- Check if domain model needs updating (requires PM decision)
- Do NOT change domain model without explicit approval

**Evidence Required**: Domain model check results, any conflicts identified

---

### Step 3: Find Existing Patterns (Excellence Flywheel)

**MANDATORY**: Search for existing patterns before implementing.

```bash
# Find similar working code
grep -r "similar_functionality" services/ --include="*.py"

# Check pattern library
find docs/internal/architecture/patterns -name "*relevant-pattern*.md"
```

**Questions to Answer**:

- How is this solved elsewhere in the codebase?
- What pattern should be used?
- Are there reference implementations?

**If Pattern Found**:

- Use the existing pattern
- Follow the pattern exactly (don't reinvent)
- Document pattern usage

**If No Pattern Found**:

- Document why new approach is needed
- Consider if pattern should be created (requires PM decision)

**Evidence Required**: Pattern search results, pattern chosen or rationale for new approach

---

### Step 4: Implement Minimal Fix (Inchworm Protocol)

**MANDATORY**: Implement smallest possible fix that solves the problem.

**Principles**:

- Fix root cause, not symptoms
- Minimal change required
- Complete 100% before moving on
- No workarounds

**Implementation Checklist**:

- [ ] Fix addresses root cause identified in investigation
- [ ] Fix respects domain model
- [ ] Fix uses existing patterns where possible
- [ ] Fix is minimal (no unnecessary changes)
- [ ] Fix is complete (no TODOs or partial implementation)

**Evidence Required**: Code changes with explanation of why this fixes root cause

---

### Step 5: Lock with Regression Tests

**MANDATORY**: Add tests that prevent bug from recurring.

**Regression Test Requirements**:

- Test the specific bug scenario
- Test edge cases around the bug
- Test integration points if bug was integration-related
- Test domain invariants if bug violated domain rules

**Test Quality**:

- Tests must be meaningful (test behavior, not implementation)
- Tests must be maintainable (clear, well-named)
- Tests must be fast (no slow integration tests unless necessary)

**Evidence Required**: Regression tests written, all tests passing

---

### Step 6: Document Decision

**MANDATORY**: Document what was done and why.

**Documentation Requirements**:

- Update code comments if fix is non-obvious
- Update relevant documentation files
- If architectural change: Create ADR
- If domain model change: Update domain model documentation

**ADR Required If**:

- Architectural pattern changed
- Integration approach changed
- Significant design decision made

**Evidence Required**: Documentation updates, ADR if required

---

### Step 7: Verify with E2E Test

**MANDATORY**: Verify fix works in original E2E scenario.

**Verification Steps**:

1. Reproduce original bug scenario manually
2. Verify bug no longer occurs
3. Verify no regressions introduced
4. Verify related functionality still works

**Evidence Required**:

- Screenshot/video of fix working
- E2E test results
- Manual verification log

---

## Completion Checklist

Before marking fix complete, verify:

- [ ] Original bug fixed (E2E test passes)
- [ ] Test proves fix works (unit/integration test)
- [ ] Regression tests prevent recurrence
- [ ] Domain model respected (no violations)
- [ ] Documentation updated (code comments, docs, ADR if needed)
- [ ] No workarounds introduced (proper fix, not hack)
- [ ] All tests passing (no regressions)
- [ ] Evidence provided for all claims

**Not Done**: "It should work" / "Tests pass" / "Looks good"
**Done**: "Here's the test proving it works, the regression tests preventing recurrence, and the documentation updates"

---

## Anti-Patterns Prevented

- ❌ Fixing symptoms without root cause
- ❌ Skipping test-first approach
- ❌ Ignoring domain model for convenience
- ❌ Reinventing patterns that already exist
- ❌ Partial fixes ("mostly works")
- ❌ Workarounds instead of proper fixes
- ❌ Skipping regression tests
- ❌ Not documenting decisions

---

## Example Fix Flow

```
1. Write failing test → Test fails ✅
2. Check domain model → No conflicts ✅
3. Find pattern → Pattern X exists ✅
4. Implement fix using Pattern X → Code written ✅
5. Test passes → Bug fixed ✅
6. Add regression tests → Tests written ✅
7. Update docs → Documentation updated ✅
8. Verify E2E → Original scenario works ✅
9. All checks pass → Fix complete ✅
```
