---
type: methodology
title: STOP Conditions for Agent Deployment
valid_from: "2025-09-21"
last_updated: "2025-09-21"
---

# STOP Conditions for Agent Deployment
**Version**: 1.0
**Date**: September 4, 2025
**Purpose**: Prevent assumption-based failures and coordination drift

---

## Core Principle
Agents must STOP and request guidance rather than making assumptions that could cascade into failures.

---

## Universal STOP Conditions

### 1. Configuration Uncertainty
**STOP if**: Configuration values, endpoints, or settings are unclear
**Example**: "The API endpoint might be..." → STOP
**Instead**: Verify exact configuration with grep/cat commands

### 2. Method/Function Assumptions
**STOP if**: Assuming a method exists without verification
**Example**: "There's probably a method called..." → STOP
**Instead**: `grep -r "method_name" --include="*.py"`

### 3. Enum/Type Uncertainty
**STOP if**: Creating enums or types without checking shared_types.py
**Example**: "I'll create a CategoryType enum..." → STOP
**Instead**: `cat services/shared_types.py | grep -A 10 "Enum"`

### 4. Pattern Duplication Risk
**STOP if**: Pattern might already exist (60-80% usually does)
**Example**: "I'll implement this new pattern..." → STOP
**Instead**: Search pattern-catalog.md and grep codebase first

### 5. Test Failure Acceptance
**STOP if**: Tests fail but claiming "acceptable" or "expected"
**Example**: "Tests fail but that's okay because..." → STOP
**Instead**: All tests must pass with evidence

### 6. GitHub Metadata Issues
**STOP if**: GitHub labels don't exist when trying to apply
**Example**: "Label 'enhancement' not found..." → STOP
**Instead**: Ask permission to create label or use existing

### 7. Architectural Uncertainty
**STOP if**: Implementation approach affects architecture
**Example**: "Should this be a service or utility?" → STOP
**Instead**: Consult Chief Architect through Lead Developer

---

## Agent-Specific STOP Conditions

### Claude Code
- STOP if multiple quick fixes suggest architectural issue
- STOP if subagent deployment strategy unclear
- STOP if investigation reveals unexpected complexity

### Cursor
- STOP if file paths uncertain (no wildcards!)
- STOP if import paths not verified
- STOP if doing work assigned to Code

---

## STOP Response Protocol

When hitting a STOP condition:

1. **Document the uncertainty**
   ```
   STOP CONDITION: [Type of uncertainty]
   Context: [What you were trying to do]
   Specific question: [What needs clarification]
   ```

2. **Show what you checked**
   ```
   Verification attempted:
   - Ran: [command]
   - Found: [result]
   - Uncertainty: [what's still unclear]
   ```

3. **Propose alternatives**
   ```
   Option A: [approach if X]
   Option B: [approach if Y]
   Recommendation: [your best guess with reasoning]
   ```

---

## Anti-Patterns to Avoid

❌ "I'll assume..." → Always triggers STOP
❌ "It probably..." → Verify or STOP
❌ "Should work..." → Must work with evidence
❌ "Close enough..." → Exact match required
❌ "I think..." → Know or STOP

---

## Success Patterns

✅ "Verified with grep that..."
✅ "Checked shared_types.py and found..."
✅ "Confirmed pattern exists in..."
✅ "Terminal output shows..."
✅ "GitHub issue PM-XXX confirms..."

---

## Remember

**It's always better to STOP and ask than to assume and fail.**

Every assumption creates potential for:
- Cascade failures across agents
- Hours of debugging mysterious issues
- Architectural drift from intended design
- Erosion of systematic methodology

When in doubt, STOP and verify.
