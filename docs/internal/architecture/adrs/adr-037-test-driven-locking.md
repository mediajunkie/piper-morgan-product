# ADR-037: Test-Driven Locking Strategy

**Status**: Accepted
**Date**: September 26, 2025
**Deciders**: Christian Crumlish (PM), Claude Opus (Chief Architect)
**Category**: Testing, Quality, Methodology

## Context

The 75% pattern revealed a critical weakness in our development process: completed work can become disabled through "temporary" comments, TODO markers, or partial implementations. During CORE-GREAT-1, we discovered QueryRouter had been 75% complete but disabled with TODO comments for months, blocking 80% of features.

We need a systematic approach to prevent completed work from regressing, being accidentally disabled, or degrading in quality. This approach must balance preventing regression with maintaining development velocity.

## Decision

We will implement a comprehensive Test-Driven Locking Strategy that makes regression impossible without deliberate test modification. Each completed component or epic will have multiple lock mechanisms that prevent various forms of degradation.

### Lock Categories

#### 1. Existence Locks
Tests that verify a component exists and is initialized:
- Component cannot be None/null
- Initialization cannot be commented out
- Required imports must succeed
- Core functionality must be callable

#### 2. Performance Locks
Tests that prevent performance degradation:
- Baseline performance metrics established
- Tolerance threshold defined (typically 20%)
- CI/CD fails if thresholds exceeded
- Realistic targets based on actual performance, not aspirations

#### 3. Coverage Locks
Tiered enforcement based on component status:
- **Completed components**: 80% minimum coverage
- **Active development**: 25% minimum coverage
- **Legacy/baseline**: 15% minimum (prevent further degradation)
- Coverage must increase with each epic

#### 4. Integration Locks
Tests that verify component connections:
- API contracts cannot be broken
- Integration points must remain functional
- Data flow between components verified
- Plugin interfaces maintain compatibility

#### 5. Quality Locks
Automated checks that maintain standards:
- Pre-commit hooks for TODO format compliance
- Link checkers for documentation
- Configuration validation
- Pattern detection (prevent dual implementations)

### Implementation Requirements

#### For Each Epic/Component

1. **During Development**
   - Write tests for new functionality
   - Establish performance baselines
   - Document expected behavior

2. **At Completion**
   - Create regression test suite
   - Set coverage thresholds
   - Configure CI/CD gates
   - Remove old patterns physically

3. **Post-Completion**
   - Monitor for violations
   - Update baselines only with justification
   - Maintain lock tests through refactors

### Lock Lifecycle

#### Creation
- Locks are created when a component reaches "complete" status
- Must be part of epic completion criteria
- Reviewed during Phase Z (completion) of epic

#### Modification
- Requires architectural review
- Must maintain or strengthen protection
- Changes documented in commit messages

#### Removal
- Only when component is being replaced
- Replacement must have equivalent or better locks
- Transition period may have dual locks

### CI/CD Integration

All locks must be enforced in CI/CD pipeline:
```yaml
- name: Run Lock Tests
  run: |
    pytest tests/regression/ -v
    pytest tests/unit/ --cov --cov-fail-under=80
    pytest tests/performance/ --benchmark-fail-if-slower=threshold
```

### Developer Experience

Locks must not significantly impede development:
- Fast feedback (lock tests run quickly)
- Clear error messages explaining violations
- Documentation on how to work with locks
- Escape hatches for legitimate changes (with review)

## Consequences

### Positive

1. **Regression Prevention**: Completed work cannot be accidentally disabled
2. **Quality Maintenance**: Performance and coverage cannot degrade silently
3. **Confidence**: Changes can be made knowing locks will catch breaks
4. **Documentation**: Lock tests serve as executable specifications
5. **75% Pattern Prevention**: Incomplete work becomes immediately visible

### Negative

1. **Initial Overhead**: Time required to create comprehensive locks
2. **Maintenance Burden**: Lock tests must be updated with legitimate changes
3. **False Positives**: Overly strict locks may block valid improvements
4. **Learning Curve**: Developers must understand lock patterns

### Mitigation

- Start with critical locks, add others incrementally
- Use pragmatic thresholds based on reality, not perfection
- Document lock bypass procedures for emergencies
- Provide templates and examples for common lock patterns

## Examples from Implementation

### GREAT-1C QueryRouter Locks
```python
# Existence Lock
def test_queryrouter_must_be_enabled_in_orchestration_engine():
    engine = OrchestrationEngine()
    assert engine.query_router is not None
    assert callable(engine.query_router.route_query)

# Performance Lock
def test_performance_requirement_queryrouter_initialization_under_500ms():
    times = []
    for _ in range(10):
        start = time.time()
        QueryRouter()
        times.append(time.time() - start)
    assert sum(times) / len(times) < 0.5
```

### CI/CD Configuration
```yaml
# Coverage Lock
- run: pytest tests/ --cov=services/orchestration/queryrouter --cov-fail-under=80

# Performance Lock
- run: pytest tests/performance/ --benchmark-fail-threshold=5400ms
```

## Related Decisions

- **ADR-035**: Inchworm Protocol - Sequential completion methodology
- **ADR-036**: QueryRouter Resurrection Strategy - First application of locks
- **ADR-032**: Intent-Based Architecture - Requires lock protection

## Review Schedule

This decision should be reviewed after:
- Completion of CORE-GREAT-5 (full epic sequence)
- First major refactor under lock protection
- Six months of operational experience

## Notes

The test-driven locking strategy emerged from painful experience with the 75% pattern. It represents a shift from trust-based development ("this should work") to evidence-based development ("this is proven to work and cannot be broken without deliberate action").

The key insight: regression tests are not just about detecting breaks, they're about making breaks impossible without conscious override.

---

*"Tests make incomplete work visible. Locks prevent 'temporary' disabling."*
