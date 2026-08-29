# ADR-035: The Inchworm Protocol

**Status**: Accepted
**Date**: September 20, 2025
**Deciders**: Christian Crumlish (PM), Chief Architect

## Context

Our architectural review on September 19, 2025, revealed a systemic pattern of incomplete implementations:
- QueryRouter: 75% complete, disabled
- OrchestrationEngine: Never initialized
- Multiple refactors started but not finished
- Dual implementation patterns coexisting
- Configuration validation broken despite ADR documenting it
- 80% of MVP features blocked by incomplete foundations

The root cause: **Starting new work before finishing existing work**. This created cascading failures where each incomplete layer made the next layer impossible to complete properly.

Historical evidence shows this pattern repeatedly:
- PM-034: QueryRouter implementation stopped at 75%
- ADR-005: Dual repositories supposedly eliminated, but both still exist
- ADR-032: Intent classification declared universal, but bypasses remain
- Excellence Flywheel: Methodology documented but not universally applied

## Decision

**Adopt the Inchworm Protocol**: A sequential execution methodology where each epic must be 100% complete before the next begins. NO EXCEPTIONS.

### The Protocol

Each epic follows this rigid pattern:
1. **Fix** the broken system
2. **Test** comprehensively
3. **Lock** with tests that prevent regression
4. **Document** what was done and why
5. **Verify** with core user story (GitHub issue creation)

### Completion Definition

An epic is only complete when:
- All acceptance criteria met
- All tests passing
- Lock mechanisms in place
- Documentation updated
- Core user story validated
- No TODO comments remain
- No workarounds present

## Consequences

### Positive

1. **Guaranteed Completeness**: Each foundation is solid before building on it
2. **No Technical Debt Accumulation**: Problems are fixed, not worked around
3. **Clear Progress Tracking**: Binary state - either done or not done
4. **Reduced Cognitive Load**: Focus on one epic at a time
5. **Prevents Cascade Failures**: No building on broken foundations
6. **Testable Validation**: Each epic has clear success criteria

### Negative

1. **Slower Initial Progress**: Can't parallelize work
2. **No Quick Wins**: Must fix foundations before features
3. **Sequential Dependencies**: Blocked if current epic hits obstacle
4. **Requires Discipline**: Temptation to start next epic early
5. **All-or-Nothing**: Can't ship partial improvements

### Neutral

1. **Cultural Shift**: From "starting" culture to "finishing" culture
2. **Planning Changes**: Must sequence work carefully
3. **Communication**: Progress appears slower but is more real

## Implementation

### The Great Refactor Sequence

Applying Inchworm Protocol to fix our foundations:

1. **CORE-GREAT-1**: Orchestration Core (2 weeks)
   - Complete QueryRouter, initialize OrchestrationEngine
   - Lock: Integration tests for GitHub issue flow

2. **CORE-GREAT-2**: Integration Cleanup (1 week)
   - Eliminate dual patterns, fix configuration
   - Lock: Old patterns physically removed

3. **CORE-GREAT-3**: Plugin Architecture (2 weeks)
   - Extract integrations to plugins
   - Lock: Core isolation tests

4. **CORE-GREAT-4**: Intent Universalization (1 week)
   - No bypass of intent classification
   - Lock: 100% coverage tests

5. **CORE-GREAT-5**: Validation & Quality (1 week)
   - Comprehensive test suite and monitoring
   - Lock: CI gates prevent regression

**Total**: 7 weeks to architectural stability

### Enforcement Mechanisms

1. **GitHub Issues**: Each epic is a single issue with checkboxes
2. **Acceptance Criteria**: Binary checklist - all must be checked
3. **Lock Tests**: Specific tests that prevent regression
4. **CI Gates**: Automated enforcement of quality standards
5. **Review Gates**: Cannot start next epic until current is reviewed

### Daily Checklist

Before starting work each day:
1. Which REFACTOR epic am I on?
2. What's the next unchecked box?
3. Will this help the core user story work?
4. Am I finishing or starting?

If starting when not finished: **STOP**.

## Alternatives Considered

### Alternative 1: Parallel Refactors
**Description**: Work on multiple refactors simultaneously
**Rejected Because**: This is how we got into the current mess

### Alternative 2: Feature-First with Patches
**Description**: Ship features with workarounds, fix foundations later
**Rejected Because**: Workarounds become permanent, foundations never get fixed

### Alternative 3: Big Bang Rewrite
**Description**: Throw everything away and start over
**Rejected Because**: Loses valuable existing work, repeats same mistakes

## Philosophical Foundation

The inchworm moves slowly but inevitably forward. Each movement is complete before the next begins. It cannot move backwards. It leaves a clear trail of where it has been.

This is the opposite of the butterfly approach - flitting from flower to flower, touching everything but completing nothing.

## Success Metrics

- **Epic Completion Rate**: 100% (not 75%)
- **Regression Rate**: 0% (locked by tests)
- **Technical Debt**: Decreasing, not accumulating
- **Developer Confusion**: Eliminated (one focus at a time)
- **Architecture Stability**: Increasing with each epic

## Quotes from the Journey

> "It's better to verify infrastructure than waste hours on wrong approach"

> "Multiple unfinished refactors created confusion and broken systems"

> "We're not building new things. We're finishing what we started."

> "The dream lives on indeed! 🐛"

## Related Decisions

- **ADR-036**: QueryRouter Resurrection (how to complete PM-034)
- **ADR-037**: Test-Driven Locking (preventing regression)
- **DECISION-002**: MVP Scope Reduction (focus on refactor first)

## References

- Great Refactor Roadmap (September 19, 2025)
- Current State Documentation (September 19, 2025)
- PM Quote: "I've been living it for the past week or so and it's kept me from losing it completely"

---

## The Inchworm Pledge

*We commit to:*
- **Finish what we start**
- **Test what we build**
- **Lock what we fix**
- **Document what we do**
- **Verify what we claim**

*We will NOT:*
- Start new work with unfinished work behind us
- Build features on broken foundations
- Create workarounds instead of fixes
- Ship code without tests
- Claim completion without verification

**The inchworm way is the only way forward.** 🐛

---

*"Sequential completion ensures each foundation is solid before building on it."*
