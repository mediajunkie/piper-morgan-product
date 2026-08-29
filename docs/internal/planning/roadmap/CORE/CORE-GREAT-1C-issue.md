# CORE-GREAT-1C: Testing, Locking & Documentation

## Context
Part 3 of CORE-GREAT-1 epic. After QueryRouter is working and connected (GREAT-1A, 1B), we need comprehensive tests, locks to prevent regression, and documentation updates to reflect the working state.

## The Lock Principle
Following the Inchworm Protocol, work isn't complete until it's locked against regression. This issue ensures QueryRouter can never be accidentally disabled again.

## Acceptance Criteria

### Testing Phase
- [ ] Unit tests for QueryRouter initialization
- [ ] Integration tests for orchestration pipeline
- [ ] Performance tests validating <500ms requirement
- [ ] Error scenario tests with meaningful messages
- [ ] End-to-end test: GitHub issue creation through chat

### Locking Phase
- [ ] CI/CD pipeline fails if QueryRouter disabled
- [ ] Initialization test prevents commented-out code
- [ ] Performance regression test alerts on degradation
- [ ] Required test coverage for orchestration module
- [ ] Pre-commit hooks catch disabled components

### Documentation Phase
- [ ] Update architecture.md with current flow
- [ ] Remove or update misleading TODO comments
- [ ] Document initialization sequence
- [ ] Update ADR-032 implementation status
- [ ] Add troubleshooting guide for common issues

### Verification Phase
- [ ] Fresh clone and setup works without issues
- [ ] New developer can understand orchestration flow
- [ ] All tests pass in CI/CD pipeline
- [ ] No remaining TODO comments without issue numbers
- [ ] Performance benchmarks documented

## Evidence Required
- Test suite output showing all passing
- CI/CD configuration preventing regression
- Coverage report for orchestration module
- Performance benchmark results
- Documentation diffs showing updates

## Lock Mechanisms to Implement
1. **Test Lock**: Test that fails if QueryRouter is None
2. **Import Lock**: Test that fails if initialization commented
3. **Performance Lock**: Test that fails if >500ms
4. **Coverage Lock**: Minimum 80% coverage required
5. **TODO Lock**: Pre-commit hook for TODO format

## STOP Conditions
- If comprehensive testing reveals architectural flaws
- If performance cannot be maintained with tests
- If locking mechanisms conflict with development flow

## Definition of Done
- All tests passing with >80% coverage
- Regression impossible without test failure
- Documentation reflects actual implementation
- Performance benchmarks established
- New developer can understand system from docs
- North Star test (GitHub issue creation) in test suite

## Notes on Preventing Future 75% Pattern
- Tests make incomplete work visible
- Locks prevent "temporary" disabling
- Documentation prevents confusion
- This becomes template for future component completion

## Related
- Parent: CORE-GREAT-1 (#180)
- Depends on: CORE-GREAT-1B completion
- Prevents: Future 75% pattern occurrences
- Establishes: Testing pattern for CORE-GREAT-2 through 5
