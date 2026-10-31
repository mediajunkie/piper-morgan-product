---
type: protocol
title: Completion Discipline Protocol
valid_from: "2026-01-24"
last_verified: "2026-10-31"
---

# Completion Discipline Protocol

The Completion Discipline Triad: Patterns 045, 046, 047.

---

## Pattern-045: Green Tests, Red User

**Core insight**: Tests passing ≠ users succeeding.

This pattern documents cases where 705 unit tests passed while all CRUD operations failed for real users.

**YOU MUST NEVER**:
- Declare completion without 100% of acceptance criteria met
- Rationalize gaps as "minor" or "not critical"
- Skip STOP conditions because work is "almost done"
- Defer tasks without explicit PM approval
- Claim "tests pass" without providing terminal output

If you catch yourself thinking "this is good enough" → STOP and escalate immediately.

---

## Pattern-046: Completion Discipline (formerly "Beads Completion Discipline")

**Core principle**: You cannot skip work by rationalizing it as "optional" or "nice-to-have."

The principle stands. The Beads (`bd`) commands this section used to carry are retired (CIO, 2026-10-31,
#1726): `.beads/` stopped being tracked on 2026-02-03, `bd` is not installed on Amber, and GitHub is the
tracker (CIO ruling 2026-10-05). Session start and end follow CLAUDE.md ("Session start" and "Sign-off").

### Proactive Issue Creation

- Discover work mid-task? → `gh issue create` immediately (the `discovered-work-capture` skill carries the procedure; the rule itself is CLAUDE.md's "Discovered work" line)
- Link discovered work: name the parent issue in the new issue's body and comment the new number on the parent
- Don't defer tracking because "it's small"
- PM decides priority, not agent

### Completion Criteria Enforcement

**Before closing ANY issue** (skill `close-issue-properly`):
1. Read the acceptance criteria from the issue and gameplan
2. Every criterion met, with evidence? → Can close
3. Criterion not met? → Complete it, or ask PM (through Exec) to defer it and record the answer on the issue
4. No criteria listed? → STOP, escalate: "Missing completion matrix"

**Before closing ANY epic**:
1. `gh issue view <epic>` and read its task list or sub-issues
2. All closed? → Can close epic
3. Any open? → Complete them OR get PM approval for each

### "Optional" is a PM Decision

- If work is in the gameplan → it's required
- If you think it's skippable → ask PM with evidence
- Never close with rationalization like "core works" or "post-MVP"

### Before ending a session

1. **File all remaining work as issues** with `gh issue create`, naming the parent.
2. **Run the quality gates** if code changed: `python -m pytest tests/unit/ -v` at least. Failing tests → file a
   P0 blocker issue and keep the parent open.
3. **Close only completed issues**, with skill `close-issue-properly`.
4. **Run the CLAUDE.md sign-off block.** `git log --oneline origin/main..HEAD` must be empty.

---

## Pattern-047: Time Lord Alert

**Escape hatch for uncertainty.**

If you're uncertain about a decision but uncomfortable expressing it directly, say: **"Time Lord Alert"**

**Response Protocol**:
1. PM immediately pauses
2. Explore uncertainty together
3. Clear decision or escalation
4. Document for future reference

**Why this matters**: Completion bias is an emergent property of AI agents. This pattern provides explicit permission to pause rather than proceed with uncertainty.

---

## The Discomfort is Working as Designed

- Feel pressure to close? That's correct pressure
- Want to call something done? Meet criteria first
- Want to move on? File remaining work, don't hide it
