# Pattern-060: Cascade Investigation

## Status

**Proven** — demonstrated in #745, #771 (promoted 2026-06-17, instances verified)

## Product Relevance

**Portable**

This investigation methodology could become a user-facing capability. When Piper helps users track and manage issues, the cascade audit pattern could guide users to discover related problems — "You fixed this bug; would you like me to check for similar issues in this category?" This preserves the discipline's value while automating the systematic audit prompts.

## Context

Bug fixing typically follows a reactive cycle: find bug, fix bug, move on. This leaves adjacent issues undiscovered until they surface independently — often at worse times. Development teams experience:
- Related bugs appearing in clusters over days or weeks
- The same root cause manifesting in multiple places
- Category-wide issues hiding behind individual symptoms
- Missed opportunities to fix an entire class of problems at once

The Cascade Investigation pattern addresses this by treating every bug fix as a trigger for category-wide audit, turning a single fix into a systematic sweep that surfaces adjacent problems while context is fresh.

## Pattern Description

**Core Concept**: When fixing a bug, audit the entire category before moving to the next task.

1. **Trigger**: Any bug fix or investigation reveals an issue
2. **Category Audit**: Ask "what else in this category might be broken?"
3. **Adjacent Discovery**: Each finding triggers its own category audit
4. **Cascade Tracking**: Document the cascade chain (depth and breadth)
5. **Systematic Resolution**: Fix or file every discovery — nothing is ignored

The key insight: a single bug is rarely alone. The conditions that created it likely created siblings. Fixing one without auditing the category is leaving known unknowns on the table.

**What distinguishes this from related patterns**:
- Pattern-041 (Systematic Fix Planning) is about *planning* how to fix multiple known issues
- Pattern-042 (Investigation-Only Protocol) is about *restraint* — investigating without fixing
- Pattern-060 is about the *cascade itself*: each finding triggering a category-wide audit that surfaces adjacent problems

## Implementation

### Structure

```
Bug Fix
    ↓
┌─────────────────────────┐
│ Category Audit          │ → "What else in this category
│ "Is this a pattern?"    │    might have the same issue?"
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│ Adjacent Discovery      │ → File or fix each finding
│ (0-N new issues)        │
└─────────────────────────┘
    ↓ (for each discovery)
┌─────────────────────────┐
│ Recursive Category      │ → Does THIS finding suggest
│ Audit (if warranted)    │    a broader category?
└─────────────────────────┘
    ↓
Resolution + Evidence Table
```

### Cascade Evidence Table

Each cascade investigation should produce an evidence table documenting depth:

```markdown
| Depth | Discovery | Category Audited | Issues Found | Action |
|-------|-----------|-----------------|--------------|--------|
| 0 | Original bug | — | 1 | Fixed |
| 1 | Category audit | [category] | N | Fixed/Filed |
| 2 | Adjacent category | [category] | N | Fixed/Filed |
| ... | ... | ... | ... | ... |
| **Total** | | | **X issues** | |
```

### Process

```
1. Fix the original bug
2. PAUSE — don't move to next task
3. Ask: "What category does this bug belong to?"
   - Examples: timezone handling, user scoping, auth flow, setup UX
4. Audit: Search codebase for same pattern in that category
   - grep for similar code patterns
   - Check related files/modules
   - Review tests for same assumptions
5. For each discovery:
   a. Fix if quick (<5 min) or file as tracked issue
   b. Ask: "Does this suggest a DIFFERENT category to audit?"
   c. If yes, repeat from step 3 for the new category
6. Document cascade in evidence table
7. Report total discoveries to PM
```

## Usage Guidelines

### When to Use

- After fixing any bug (the trigger is universal)
- When a bug involves a systemic pattern (e.g., wrong import, missing parameter, outdated API)
- When the root cause could plausibly exist in other files or modules
- During dedicated bug-fixing sessions where context-switching cost is low

### When NOT to Use

- Truly isolated bugs with no categorical siblings (rare but possible)
- Time-boxed sessions where the PM has prioritized specific issues
- When the cascade would cross into unfamiliar domains (hand off instead)

### Best Practices

1. **Always ask the category question** — Even if the answer is "no siblings," asking is the discipline
2. **File, don't defer** — Every discovery gets a tracking issue immediately (Pattern-046)
3. **Document cascade depth** — The evidence table proves investigation thoroughness
4. **Know when to stop** — Cascades beyond depth 3 may indicate an architectural issue, not a bug pattern. Escalate rather than continuing
5. **Time-box each depth level** — Audit the category, don't audit the codebase

## Proven Instances

### Instance 1: Todo Bug Cascade (February 1, 2026)

**Trigger**: #745 — Hardcoded `user_id` in todo service

| Depth | Discovery | Category | Issues | Action |
|-------|-----------|----------|--------|--------|
| 0 | #745 hardcoded user_id | — | 1 | Fixed |
| 1 | Audit: other hardcoded user_ids | User scoping | 6 | Fixed (#746-#751) |
| 2 | Timezone warnings surfaced | Datetime handling | 7 | Fixed (#752-#758) |
| 3 | Multi-tenancy audit gaps | Auth context | 2 | Fixed (#758-#759) |
| **Total** | | | **16 issues** | All resolved same day |

### Instance 2: Timezone Migration Cascade (February 1-3, 2026)

**Trigger**: #757 — File scoring uses wrong timezone comparison

| Depth | Discovery | Category | Issues | Action |
|-------|-----------|----------|--------|--------|
| 0 | #757 file scoring timezone | — | 1 | Fixed |
| 1 | Audit: datetime usage | Datetime imports | 3 | Fixed (#768, #769, #770) |
| 2 | Schema drift: 73 columns | DB schema | 1 | Migration #771 |
| 3 | Schema validator false positive | Tooling | 1 | Filed #773 |
| **Total** | | | **6 issues** | 5 fixed, 1 tracking |

### Instance 3: Multi-tenancy Cascade (January 30, 2026)

**Trigger**: #734 — Calendar token leaked across users

| Depth | Discovery | Category | Issues | Action |
|-------|-----------|----------|--------|--------|
| 0 | #734 cross-user token leak | — | 1 | Fixed |
| 1 | Audit: user scoping in repos | Repository pattern | 12 | Fixed (9-phase plan) |
| 2 | Auth context in routes | Route auth | 3 | Fixed |
| **Total** | | | **16 issues** | 94 tests added |

## Related Patterns

### Complements

- [Pattern-041: Systematic Fix Planning](pattern-041-systematic-fix-planning.md) — Use after cascade to plan multi-issue resolution
- [Pattern-042: Investigation-Only Protocol](pattern-042-investigation-only-protocol.md) — Cascade investigation *includes* fixing; Investigation-Only does not
- [Pattern-046: Beads Completion Discipline](pattern-046-beads-completion-discipline.md) — Ensures each cascade discovery gets tracked

### Part of Family

- **Investigation & Root Cause Family** (006, 041, 042, 043, 060)
- Pattern-006 (Verification-First) provides the methodology foundation
- Pattern-043 (Defense-in-Depth) provides the prevention layer after cascade

### See Also

- [Pattern-045: Green Tests, Red User](pattern-045-green-tests-red-user.md) — Cascade investigation often surfaces Pattern-045 instances

## References

### Documentation

- Issue #745: Todo bug (cascade trigger)
- Issue #771: Schema drift (cascade trigger)
- Issue #734: Multi-tenancy (cascade trigger)
- Pattern Sweep 2.0 Results: `docs/internal/development/reports/pattern-sweep-2.0-results-2026-02-03.md`

### Discovery

- First observed: February 1, 2026 (todo bug cascade)
- Additional instances: January 30, 2026 (#734); February 3, 2026 (#771)
- Classified as TRUE EMERGENCE: Pattern Sweep 2.0 (February 3, 2026)
- Approved by CIO: February 4, 2026

---

_Pattern documented: February 5, 2026_
_Approved in Pattern Sweep 2.0 (#777) — CIO response February 4, 2026_
