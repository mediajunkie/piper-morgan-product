---
type: protocol
title: Debugging Protocol
valid_from: "2026-01-24"
last_verified: "2026-06-19"
---

# Debugging Protocol

Systematic debugging process for any technical issue.

---

## Core Rule

**Find the root cause.** Never fix symptoms or add workarounds instead of finding root cause, even if it seems faster.

---

## Phase 1: Root Cause Investigation (BEFORE attempting fixes)

- **Read error messages carefully**: Don't skip past errors - they often contain the exact solution
- **Reproduce consistently**: Ensure you can reliably reproduce before investigating
- **Check recent changes**: What changed? Git diff, recent commits, etc.

---

## Phase 2: Pattern Analysis

- **Find working examples**: Locate similar working code in the codebase
- **Compare against references**: If implementing a pattern, read the reference completely
- **Identify differences**: What's different between working and broken code?
- **Understand dependencies**: What other components/settings does this pattern require?

---

## Phase 3: Hypothesis and Testing

1. **Form single hypothesis**: State clearly what you think is the root cause
2. **Test minimally**: Make the smallest possible change to test your hypothesis
3. **Verify before continuing**: Did it work? If not, form new hypothesis - don't add more fixes
4. **When you don't know**: Say "I don't understand X" rather than pretending

---

## Phase 4: Implementation Rules

- ALWAYS have the simplest possible failing test case
- NEVER add multiple fixes at once
- NEVER claim to implement a pattern without reading it completely first
- ALWAYS test after each change
- IF your first fix doesn't work, STOP and re-analyze rather than adding more fixes

---

## Test Failure Protocol

If ANY test fails:

1. STOP immediately - do not continue
2. Do NOT decide if the failure is "critical"
3. Do NOT rationalize with "core works", "not blocking", "minor issue"

Report format:
```
STOP - Tests Failing

Failing: [X] tests
Passing: [Y] tests

Exact errors:
[paste complete error output]

Root cause (if known):
[your diagnosis]

Options:
1. [fix approach with reasoning]
2. [alternative approach]
3. [skip with explicit approval]

Awaiting PM decision.
```

**The PM decides criticality, not you.**
