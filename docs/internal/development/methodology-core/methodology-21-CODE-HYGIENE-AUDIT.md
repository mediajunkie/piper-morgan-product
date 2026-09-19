---
type: methodology
title: Code Hygiene Audit Methodology
valid_from: "2025-12-02"
last_updated: "2025-12-02"
---

# Code Hygiene Audit Methodology

## Overview

The **Code Hygiene Audit Methodology** is a systematic approach to identifying and resolving technical debt in existing code files. Unlike feature development, hygiene audits focus on improving code quality without changing external behavior - pure refactoring that reduces bug risk and improves maintainability.

This methodology was formalized during the Setup Wizard Hygiene Audit (#438, December 2025) and is designed to work with the [gameplan-template](../../../../knowledge/gameplan-template.md) and [agent-prompt-template](../../../../knowledge/agent-prompt-template.md).

## When to Use This Methodology

**Good candidates for hygiene audits:**
- Files with multiple small issues discovered during other work
- Critical-path code that will be extended soon
- Files with shadowing bugs, bare exceptions, or code duplication
- Modules blocking confident future development

**Not appropriate for:**
- Files requiring behavior changes (use feature issues instead)
- Entire system refactors (use architectural epics)
- Quick one-off fixes (use bug issues)

## Core Principles

### 1. Audit Before Implementing

Before proposing fixes, systematically inventory all issues:

```bash
# Use Serena for symbolic analysis
mcp__serena__get_symbols_overview("path/to/file.py")

# Find specific patterns
mcp__serena__search_for_pattern("import os", relative_path="path/to/file.py")
mcp__serena__search_for_pattern("except Exception", relative_path="path/to/file.py")
```

**Key insight**: The audit phase often reveals more issues than initially suspected. In #438, we expected ~20 bare exceptions and found 19 - but also discovered 3 redundant imports that weren't in the original assessment.

### 2. Categorize by Risk/Priority

Not all hygiene issues are equal. Categorize by:

| Category | Risk | Priority | Example |
|----------|------|----------|---------|
| **Bugs** | High | P1 | Variable shadowing, import conflicts |
| **Error Handling** | Medium | P2 | Bare exceptions hiding real errors |
| **Duplication** | Low | P3 | Repeated code blocks |
| **Size/Complexity** | Low | P3 | Large functions, missing extraction |

**Decision rule**: Fix high-risk issues first. Low-risk issues can be deferred to follow-up issues if the audit scope grows.

### 3. Phase Structure (Inchworm Protocol)

Structure work in discrete, testable phases:

```
Phase -1: Scope Assessment (before gameplan approval)
Phase 0:  Infrastructure Verification
Phase 1:  Quick Wins (imports, constants, obvious fixes)
Phase 2:  Medium Effort (exception handling, targeted refactors)
Phase 3:  Higher Risk (function extraction, DRY consolidation)
Phase 4:  Validation (full test suite, manual testing)
Phase Z:  Closure (evidence, completion matrix, handoff)
```

**Cathedral Doctrine**: Complete each phase 100% before starting the next. No "80% done" phases.

### 4. Evidence-Based Completion

Every phase completion requires evidence:

```markdown
| Component | Status | Evidence |
|-----------|--------|----------|
| Phase 1: Import cleanup | ✅ | [commit abc1234](link) |
| Phase 2: Exception handling | ✅ | [commit def5678](link) |
| Phase 3: Function extraction | ⏸️ | Deferred - #439 |
```

## Practical Workflow

### Step 1: Create Audit Issue

Use the [feature template](../../../../.github/issue_template/feature.md) with hygiene-specific sections:

```markdown
## Problem Statement
`path/to/file.py` has accumulated code hygiene issues:
- [X] redundant imports causing [specific problem]
- [Y] bare `except Exception` blocks
- [Z] lines of duplicate code

## What Already Exists
- File: `path/to/file.py` (N lines, M functions)
- Tests: `pytest tests/path/` (passing baseline)
- External API: [list public functions/classes]
```

### Step 2: Symbolic Analysis

Use Serena to understand the file structure without reading entire contents:

```python
# Get function overview
mcp__serena__get_symbols_overview("scripts/setup_wizard.py")

# Find specific issues
mcp__serena__search_for_pattern(
    "^import \\w+$",  # Module-level imports
    relative_path="scripts/setup_wizard.py",
    context_lines_before=0,
    context_lines_after=0
)

# Find bare exceptions
mcp__serena__search_for_pattern(
    "except Exception",
    relative_path="scripts/setup_wizard.py",
    context_lines_before=2,
    context_lines_after=2
)
```

### Step 3: Write Gameplan

Use the gameplan template with these hygiene-specific elements:

1. **Completion Matrix**: Every phase gets a row
2. **Acceptance Criteria**: Measurable outcomes ("No bare exceptions in subprocess handlers")
3. **STOP Conditions**: When to escalate (tests fail, scope grows unexpectedly)
4. **Deferral Protocol**: How to handle lower-priority items

### Step 4: Execute Phases

**Phase 1 (Quick Wins)**:
- Fix imports first (highest bug risk)
- Add constants (reduces magic strings)
- Run tests after each change

**Phase 2 (Medium Effort)**:
- Target specific exception categories (e.g., subprocess only)
- Use "targeted" approach if full replacement is risky
- Document what's deferred and why

**Phase 3 (Higher Risk)** - Often deferred:
- Function extraction carries refactoring risk
- Create follow-up issue if scope is too large
- Get PM approval before deferring

### Step 5: Validate and Close

```bash
# Run full test suite
pytest tests/ -v

# Run smoke tests
pytest tests/ -m smoke

# Verify external API unchanged
python -c "from scripts.setup_wizard import is_setup_complete, run_setup_wizard; print('OK')"
```

Update issue with:
- All tasks checked
- Evidence links for each phase
- `@PM-approval-needed` tags for deferrals
- Status: "Ready for PM Review"

## Case Study: Setup Wizard Hygiene Audit (#438)

**Date**: December 1, 2025
**File**: `scripts/setup_wizard.py` (1,159 lines, 21 functions)
**Gameplan**: `/Users/xian/.claude/plans/optimized-exploring-cerf.md`

### Initial Assessment

```
Issues Found:
- 3 redundant imports (os at lines 71, 138; platform in function)
- 19 bare `except Exception` handlers
- 225 lines duplicate code (API key collection 3x)
- 243-line function (run_setup_wizard)
```

### Execution Summary

| Phase | Planned | Actual | Notes |
|-------|---------|--------|-------|
| Phase 1 | 8 constants | 11 constants | Exceeded target |
| Phase 2 | 20 handlers | 7 handlers | Targeted subprocess only |
| Phase 3 | Function extraction | Deferred | Created #439 |
| Phase 4 | Full validation | Complete | 33 tests passed |

### Key Decisions

1. **Phase 2 Scope Reduction**: Found 19 handlers but chose "targeted" approach (7 subprocess handlers) to manage risk. Remaining handlers are lower risk and documented for future.

2. **Phase 3 Deferral**: Function extraction requires more testing infrastructure. Created follow-up issue #439 rather than expanding scope.

3. **Evidence Requirements**: Every completion claim linked to commit hash.

### Lessons Learned

- Symbolic analysis (Serena) is faster than grep for structured queries
- "Targeted" approaches are valid when full replacement is risky
- Deferrals require explicit PM approval and follow-up issues
- Completion matrix prevents "works on my machine" claims

## Templates and References

- **Gameplan Template**: [knowledge/gameplan-template.md](../../../../knowledge/gameplan-template.md)
- **Agent Prompt Template**: [knowledge/agent-prompt-template.md](../../../../knowledge/agent-prompt-template.md)
- **Feature Issue Template**: [.github/issue_template/feature.md](../../../../.github/issue_template/feature.md)
- **STOP Conditions**: [methodology-16-STOP-CONDITIONS.md](methodology-16-STOP-CONDITIONS.md)

## Anti-Patterns

### 1. Scope Creep
**Problem**: "While I'm here, I'll also refactor X..."
**Solution**: File separate issues for discovered work. Audit scope is fixed at gameplan approval.

### 2. Completion Without Evidence
**Problem**: "Tests pass" without terminal output
**Solution**: Every completion claim needs a link (commit, screenshot, terminal output)

### 3. Rationalized Deferrals
**Problem**: "Phase 3 is optional" without PM approval
**Solution**: Use `@PM-approval-needed` tag. PM decides what's optional.

### 4. All-or-Nothing Thinking
**Problem**: "Can't fix 19 handlers so won't fix any"
**Solution**: "Targeted" approaches are valid. 7/19 is progress.

---

**Last Updated**: December 1, 2025
**Formalized From**: Issue #438 (Setup Wizard Hygiene Audit)
**Reference Gameplan**: `/Users/xian/.claude/plans/optimized-exploring-cerf.md`
