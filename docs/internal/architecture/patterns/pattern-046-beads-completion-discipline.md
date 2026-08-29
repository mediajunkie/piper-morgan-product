# Pattern-046: Beads Completion Discipline

**Status**: Established
**Category**: Development & Process
**First Documented**: December 27, 2025 (Pattern Sweep 2.0)
**First Observed**: November 13-14, 2025
**Ratified**: December 27, 2025 (Chief Architect)

---

## Problem Statement

Work gets 75-90% complete then abandoned. Agents rationalize incomplete work as "optional" or "nice-to-have" to avoid the tedious last mile of completion. Issues close without meeting all acceptance criteria.

## Solution

A systematic completion discipline enforcing 100% acceptance criteria fulfillment before issue closure, using `bd` CLI tooling and explicit anti-rationalization rules.

## Pattern Components

### 1. Session Start Protocol
```bash
bd ready --json    # Find work with no blockers
bd list            # Orient to current state
bd status          # Beads database health check
```

### 2. Proactive Issue Creation
- Discover work mid-task → `bd create` immediately
- Link discovered work: `bd dep add <new> <parent> --type discovered-from`
- Don't defer tracking because "it's small"
- PM decides priority, not agent

### 3. Completion Criteria Enforcement
Before closing ANY issue:
1. Read acceptance criteria from gameplan
2. Every criterion met? → Can close
3. Criterion not met? → Complete it OR add `@PM-approval-needed: <reason>`
4. No criteria listed? → STOP, escalate: "Missing completion matrix"

### 4. No Expedience Rationalization
- "Optional" is a PM decision, not agent decision
- If work is in the gameplan → it's required
- If you think it's skippable → ask PM with evidence
- Never close with rationalization like "core works" or "post-MVP"

### 5. Session End Protocol ("Landing the Plane")
Execute in order before ending ANY session:
1. File all remaining work as issues
2. Run quality gates (if code changed)
3. Close completed issues only (use `bd-safe` wrapper)
4. Sync database: `bd sync && git status`
5. Verify no open children: `bd list | grep <your-epic>`

## Key Principle

The discomfort of open issues is working as designed:
- Feel pressure to close? That's correct pressure
- Want to call something done? Meet criteria first
- Want to move on? File remaining work, don't hide it

## When to Apply

- Every session start and end
- Before closing any issue
- When discovering work mid-task
- When tempted to defer or skip work

## Related Patterns

- Pattern-009: GitHub Issue Tracking (formal tracking)
- Pattern-045: Green Tests, Red User (anti-pattern this prevents)
- Pattern-047: Time Lord Alert (uncertainty escape hatch)
- Pattern-021: Development Session Management (session structure)

**Part of the Completion Discipline Triad**: Patterns 045, 046, and 047 form a reinforcing system for preventing premature closure and ensuring quality completion.

## Evidence

- 104 files mention "Beads", "bd-safe", "issue closure discipline"
- 148 files mention "Landing the Plane"
- Integrated into CLAUDE.md "BEADS COMPLETION DISCIPLINE" section
- Memory file: `.serena/memories/beads-discovered-work-discipline.md`

---

*Identified through Pattern Sweep 2.0 (#524) as TRUE EMERGENCE*
*Ratified by Chief Architect: December 27, 2025*
