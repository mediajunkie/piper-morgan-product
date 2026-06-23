---
type: protocol
title: Completion Discipline Protocol
valid_from: "2026-01-24"
last_verified: "2026-06-19"
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

## Pattern-046: Beads Completion Discipline

**Core principle**: You cannot skip work by rationalizing it as "optional" or "nice-to-have."

### Session Start Protocol

```bash
bd ready --json    # Find work with no blockers
bd list            # Orient to current state
bd status          # Beads database health
```

### Proactive Issue Creation

- Discover work mid-task? → `bd create` immediately
- Link discovered work: `bd dep add <new> <parent> --type discovered-from`
- Don't defer tracking because "it's small"
- PM decides priority, not agent

### Completion Criteria Enforcement

**Before closing ANY issue**:
1. Read acceptance criteria from gameplan
2. Every criterion met? → Can close
3. Criterion not met? → Complete it OR add `@PM-approval-needed: <reason>`
4. No criteria listed? → STOP, escalate: "Missing completion matrix"

**Before closing ANY epic**:
1. `bd list --parent <epic>` → Check children
2. All closed? → Can close epic
3. Any open? → Complete them OR get PM approval for each

### "Optional" is a PM Decision

- If work is in the gameplan → it's required
- If you think it's skippable → ask PM with evidence
- Never close with rationalization like "core works" or "post-MVP"

### Session End Protocol ("Landing the Plane")

Execute IN ORDER before ending ANY session:

1. **File all remaining work as issues**
   ```bash
   bd create "Thing discovered but not fixed"
   bd dep add <new> <parent> --type discovered-from
   ```

2. **Run quality gates** (if code changed)
   ```bash
   pytest tests/  # All tests must pass
   # If tests fail → file P0 blocker issue, keep parent open
   ```

3. **Close completed issues only**
   ```bash
   ./scripts/bd-safe close <issue>
   ```

4. **Sync database**
   ```bash
   bd sync
   git status  # Must show clean state
   ```

5. **Verify no open children**
   ```bash
   bd list | grep <your-epic>
   # All children must be closed OR have @PM-approved deferral
   ```

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
