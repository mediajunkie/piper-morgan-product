---
type: methodology
title: Working Method - Piper Morgan Development
valid_from: "2025-09-21"
last_updated: "2025-09-21"
---

# Working Method - Piper Morgan Development

This document outlines the step-by-step methodology for development work on Piper Morgan.

## Step-by-Step Execution

### Core Pattern: VERIFY → UNDERSTAND → IMPLEMENT → VALIDATE

- **CRITICAL:** One actionable step at a time - provide single command, wait for result, then next command
- Always request current `models.py` first when starting implementation work
- Follow the verification pattern religiously

### Cursor Agent (CA) Supervision Format

When providing instructions for implementation, use this strict format:

```
Step X: [Clear Task Name]

VERIFY FIRST (run these commands):
1. [specific grep/ls/cat commands]
2. [verification of current state]

OBJECTIVE:
[Single, clear goal for this step]

IMPLEMENTATION:
[Specific instructions]

DO NOT:
- [Common mistakes to avoid]
- [Assumptions not to make]

VERIFY AFTER:
[Commands to confirm success]

EXPECTED RESULT:
[What should happen]
```

### CA Supervision Protocol

If CA starts implementing without verification:
- STOP immediately
- Require REPORT of findings first
- Architect decides approach after review

## TDD Discipline

1. **Write test first** - See it fail for the right reason
2. **Implement minimal code** - Just enough to pass
3. **Refactor if needed** - But keep it simple
4. **Verify each step** - Don't assume, check

### TDD Workflow Example

```bash
# 1. Write test first
PYTHONPATH=. python -m pytest tests/test_new_feature.py::test_feature_works -v

# 2. Watch it fail (red)
# 3. Implement minimal code
# 4. Run test again (green)
# 5. Refactor if needed
# 6. Verify all tests still pass
```

## Session Management

### Immediate Actions
- **Create session log immediately** - Track decisions and discoveries
- **Document architectural insights** - Not just code changes
- **Update logs frequently** - Every significant discovery or decision
- **Prepare handoffs early** - Don't wait for capacity warnings

### Pre-Session Checklist

Before starting ANY implementation:
1. **Create session log immediately** - "PM-XXX Session Log - [Date]"
2. **Request current models.py** - Domain models drive all decisions
3. **Review architecture docs** - Especially architecture.md and pattern-catalog.md
4. **Check for existing patterns** - grep before creating new approaches
5. **Verify layer boundaries** - Confirm you're in the right architectural layer

### Session Log Requirements

Every session must:
- Follow naming convention: `YYYY-MM-DD-log.md` (or `YYYY-MM-DDa-log.md`)
- Document key decisions made
- Track architectural insights
- Record files modified
- Note next steps for handoff

## Reference Documents

Always consult these before implementing:
- **Session management**: See `chat-protocols.md`
- **Technical verification**: See `architectural-checklist.md`
- **Approved patterns**: See `pattern-catalog.md`
- **Current status**: Check session log artifact

## Remember

- Every interaction should advance both the codebase and the developer's understanding
- Building Piper Morgan is as much about learning architecture as it is about creating product
- **Never assume - always verify:** Use `find`, `grep`, `ls` before suggesting code
- Check actual method signatures, import paths, and existing patterns
- Ask to see specific files or line ranges when uncertain
---
*Last Updated: July 09, 2025*

## Revision Log
- **July 09, 2025**: Added vertical resize feature to chat window for improved usability
