# CORE-GREAT-1A: QueryRouter Investigation & Fix

## Context
Part 1 of CORE-GREAT-1 epic. The QueryRouter component is 75% complete but has been disabled. This blocks 80% of MVP features. We need to discover WHY it was disabled and fix the root cause.

## The 75% Pattern
QueryRouter exists and is mostly implemented but was disabled with a TODO comment. This is part of our discovered pattern where components reach 75% completion before being abandoned. Following the Inchworm Protocol, we will complete this existing work rather than creating new solutions.

## Acceptance Criteria

### Investigation Phase
- [ ] Locate the disabled QueryRouter code
- [ ] Review git history to understand when/why it was disabled
- [ ] Identify the root cause that led to disabling
- [ ] Document any dependencies or blockers discovered
- [ ] Find all references to QueryRouter in codebase

### Fix Phase
- [ ] Fix the root cause (not symptoms)
- [ ] Re-enable QueryRouter with proper initialization
- [ ] Verify it starts without errors
- [ ] Confirm it doesn't break existing functionality
- [ ] Update or remove TODO comments with issue references

## Evidence Required
- Git history showing when/why disabled
- Grep results showing all QueryRouter references
- Terminal output showing successful initialization
- Test results before and after re-enabling

## Known Information
- QueryRouter exists in `services/orchestration/`
- Referenced in ADR-032 as part of intent universal entry
- OrchestrationEngine exists but never initializes QueryRouter
- A single commented line may be the blocker

## STOP Conditions
- If QueryRouter is missing entirely
- If root cause involves major architectural changes
- If enabling breaks critical existing functionality
- If dependencies are missing or incompatible

## Definition of Done
- QueryRouter is enabled and initializes successfully
- Root cause is fixed (not worked around)
- All tests pass
- Evidence provided for all investigation findings
- No TODO comments without issue numbers

## Related
- Parent: CORE-GREAT-1 (#180)
- Blocks: 80% of MVP features
- Related: Bug #166 (UI hang - may be related)
