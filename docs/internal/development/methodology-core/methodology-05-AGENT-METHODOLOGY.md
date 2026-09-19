---
type: methodology
title: Agent Methodology for Piper Morgan
valid_from: "2025-09-21"
last_updated: "2025-09-21"
---

# Agent Methodology for Piper Morgan
*Living document - Last updated: August 18, 2025*

## Core Principle: Executable Documentation

Every `/agent` command is simultaneously:
- A task to be executed
- A specification of our standards
- A learning example for future work
- An architectural guardian

## The Three Laws of Agent Usage

1. **Verification Before Implementation**: Always use `/agent` to discover existing patterns before creating new ones
2. **Bounded Scope**: Every `/agent` task must have clear success criteria and boundaries
3. **Evidence Collection**: All `/agent` outputs become part of our compound learning library

## Standard Agent Patterns

### 🔍 Pattern Discovery (ALWAYS FIRST)

```bash
# Before ANY new feature implementation
/agent Find all existing patterns similar to [feature] in services/ and document:
1. Implementation approaches used
2. Test patterns employed
3. Error handling strategies
4. Related ADRs or documentation

# Before refactoring
/agent Analyze current implementation of [module] and identify:
1. Patterns that match our standards
2. Deviations from architectural guidelines
3. Test coverage gaps
4. Performance bottlenecks
```

### 🏗️ Architecture Enforcement

```bash
# Weekly Architecture Sweep (Every Monday)
/agent Audit services/ for architectural compliance:
1. Verify all enums are in shared_types.py
2. Check repositories contain only data access (no business logic)
3. Ensure AsyncSessionFactory.session_scope() is used consistently
4. Identify any direct database access not using AsyncSessionFactory
Create a PM-* issue for each violation found with remediation steps

# Domain Model Integrity Check
/agent Verify services/domain/models.py alignment:
1. Check all services reference canonical domain models
2. Identify any duplicate model definitions
3. Ensure no service-specific models exist outside domain/
Document findings in architecture-health.md
```

### 🧪 Test Generation & Coverage

```bash
# Test Gap Analysis
/agent Analyze test coverage in [module] and:
1. Identify top 5 uncovered code paths
2. Generate unit tests following existing patterns in tests/unit/
3. Create integration tests for critical workflows
4. Document test strategy in PR description

# Test Pattern Extraction
/agent Extract successful test patterns from tests/ and create:
1. Unit test template for new services
2. Integration test template for orchestration workflows
3. Fixture patterns for common test data
4. Mock patterns for external dependencies
```

### 📚 Knowledge Synthesis

```bash
# Session Log Pattern Mining
/agent Extract reusable patterns from session logs [date range]:
1. Successful implementation approaches
2. Resolved architectural challenges
3. Performance optimizations discovered
4. Anti-patterns to avoid
Format as additions to pattern-catalog.md

# ADR Generation from Implementation
/agent Analyze implementation of [feature] and draft ADR including:
1. Context (what problem was solved)
2. Decision (approach taken)
3. Consequences (trade-offs accepted)
4. Alternatives considered
```

### 🔗 GitHub Integration

```bash
# Issue Lifecycle Management
/agent Review PM-* issues and:
1. Add acceptance criteria based on code patterns
2. Link related test files
3. Generate implementation checklist
4. Create evidence documentation template

# PR Preparation
/agent Prepare PR for [feature] with:
1. Test output evidence
2. Coverage metrics comparison
3. Performance benchmarks
4. Architecture compliance check
```

## Multi-Agent Coordination Patterns

### Sequential Discovery (Preferred)

```bash
Step 1: /agent Find all uses of [pattern] in codebase
Step 2: [Human reviews results]
Step 3: /agent Implement similar pattern for [new feature] based on examples found
Step 4: /agent Generate tests matching patterns from Step 1
```

### Parallel Analysis (Use Judiciously)

Only for truly independent domains:
```bash
Terminal 1: /agent Analyze test patterns in tests/unit/
Terminal 2: /agent Document API endpoints in services/*/router.py
Terminal 3: /agent Review error handling in services/*/service.py
```

## Anti-Patterns to Avoid

### ❌ DON'T

```bash
# Too broad - lacks focus
/agent Fix all issues in services/

# No verification first
/agent Implement user authentication system

# Unbounded refactoring
/agent Refactor entire codebase to match new pattern

# Assuming rather than discovering
/agent Update all files to use new import style
```

### ✅ DO INSTEAD

```bash
# Specific and bounded
/agent Fix AsyncSessionFactory usage in services/queries/service.py

# Verification first
/agent Find existing authentication patterns in codebase, then implement similar approach

# Bounded refactoring
/agent Refactor services/orchestration/workflow.py to match ADR-013

# Discovery before change
/agent Find all import patterns currently used, document frequency, then proceed
```

## Measurement & Optimization

### Track Agent Effectiveness

```bash
# Weekly metrics collection
/agent Generate weekly agent effectiveness report:
1. Time saved vs manual implementation
2. Patterns discovered and reused
3. Test coverage improvement
4. Architecture violations prevented
5. Issues completed with agent assistance
```

### Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Pattern Reuse Rate | >80% | New features using discovered patterns |
| Test Coverage Delta | +5% weekly | Coverage reports |
| Architecture Violations | <2 per audit | Weekly sweep results |
| Issue Completion Velocity | +30% | GitHub metrics |
| Documentation Currency | <1 week lag | Last updated timestamps |

## Command Templates Library

### Daily Development

```bash
# Morning Setup
/agent Check for new PM-* issues and summarize implementation requirements

# Before Feature Work
/agent Find patterns for [feature] and create implementation plan

# End of Day
/agent Document today's discoveries in pattern-catalog.md
```

### Weekly Rituals

```bash
# Monday: Architecture Audit
/agent Run complete architecture compliance check

# Wednesday: Test Coverage
/agent Analyze and improve test coverage for this week's changes

# Friday: Knowledge Synthesis
/agent Extract patterns from week's work for team learning
```

### Release Preparation

```bash
# Pre-Release Audit
/agent Verify all acceptance criteria met for PM-* issues in release

# Documentation Check
/agent Ensure all new patterns are documented

# Performance Validation
/agent Run benchmarks and compare with previous release
```

## Integration with Excellence Flywheel

The `/agent` methodology directly supports each flywheel component:

1. **Systematic Verification** → Pattern Discovery commands
2. **Test-Driven Development** → Test Generation commands
3. **Multi-Agent Coordination** → Sequential/Parallel patterns
4. **GitHub-First Tracking** → Issue Lifecycle commands

## Evolution Protocol

This document evolves through:
1. Weekly retrospectives on agent effectiveness
2. New pattern discoveries get added as templates
3. Failed patterns documented as anti-patterns
4. Success metrics adjusted based on actuals

## Appendix: Economic Impact

With Chain-of-Draft integration, agent operations become economically transformative:

| Operation | Traditional Cost | With CoD | Weekly Savings |
|-----------|-----------------|----------|---------------|
| Architecture Audit | $50 | $2.50 | $237.50 |
| Test Generation | $30 | $1.50 | $142.50 |
| Pattern Discovery | $20 | $1.00 | $95.00 |
| **Total Weekly** | **$500** | **$25** | **$475** |

This makes daily architectural excellence not just feasible but economically optimal.

---
*Next review scheduled: August 25, 2025*
*Owner: Chief of Staff with Chief Architect oversight*
