---
name: audit-cascade
description: Perform systematic audit-and-correct between phases of multi-step work. Use when PM says "audit cascade", before transitioning from issue to gameplan, gameplan to agent prompts, or prompts to execution. Catches drift before it accumulates.
scope: cross-role
version: 1.1
created: 2026-01-23
---

# audit-cascade

Perform systematic audit-and-correct steps between phases of multi-step work, using templates as checklists.

**Reference**: [Pattern-049: Audit Cascade](../../../docs/internal/architecture/current/patterns/pattern-049-audit-cascade.md)

## When to Use

Use this skill when:
- Writing or reviewing a GitHub issue before creating a gameplan
- Writing or reviewing a gameplan before creating agent prompts
- Writing or reviewing agent prompts before execution
- Any multi-step work where drift could accumulate

**Critical rule**: You have **ZERO AUTHORIZATION** to mark any template requirement as "optional", "N/A", or "not applicable" without explicit PM approval. If a requirement seems inapplicable, STOP and ask.

---

## The Cascade (3 Phases, 3 Audit Gates)

```
Write Issue → AUDIT → Write Gameplan → AUDIT → Write Prompts → AUDIT → Execute
```

**3 audit gates** catch drift before it compounds into the next phase. Each phase has a write step followed by an audit step.

---

## Procedure

### Step 0 (preamble): Confirm your worktree

Audit-cascade work is substantive by definition (Phase 0 audit + gameplan + audit + execute + audit),
so the standing worktree-default applies. On Amber (Model A): confirm you're in your stable per-agent
worktree (`~/Development/piper-morgan-worktrees/{role}`), not the shared checkout. On Desktop
(Model B): confirm the session's ephemeral auto-worktree is active. Skip only if the audit work is
short enough to qualify as an exception (single-file Phase 0 audit + immediate disposition, no
implementation).

*(Added 2026-08-23, closing a ~3-month-old disposition — `mailboxes/cio/sent/memo-cio-to-host-cc-ppm-docs-arch-ceo-audit-cascade-worktree-preamble-disposition-2026-05-15.md`. Original wording assumed the pre-Amber ephemeral-worktree-per-session model; reworded here for Model A's stable-worktree-reuse reality rather than landing three-month-stale text unchecked against current architecture.)*

### Step 1: Identify the Phase

What are you auditing?

| Phase | Template Location |
|-------|-------------------|
| Issue | `.github/ISSUE_TEMPLATE/` (feature.md, bug_report_alpha.md, e2e-bug.md) |
| Gameplan | `knowledge/gameplan-template.md` |
| Agent Prompts | `knowledge/agent-prompt-template.md` |

### Step 2: Create Audit Matrix

Create a markdown table comparing the template requirements against the document:

```markdown
## Audit: [Document Name] against [Template Name]

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| [Requirement 1] | ✅ / ⚠️ / ❌ | [Details] |
| [Requirement 2] | ✅ / ⚠️ / ❌ | [Details] |
...
```

**Status legend**:
- ✅ **Present**: Requirement fully satisfied
- ⚠️ **Partial**: Requirement addressed but incomplete or unclear
- ❌ **Missing**: Requirement not addressed

### Step 3: Fix ALL Issues

Before proceeding to the next phase:
- Fix every ⚠️ (partial) item
- Fix every ❌ (missing) item
- Do NOT proceed with unfixed items

**If a requirement seems inapplicable**: STOP and ask PM. You cannot decide this yourself.

### Step 4: Document the Audit

Save the audit matrix as a working document:
- Location: `dev/YYYY/MM/DD/`
- Naming: `{issue-number}-{phase}-audit.md`
- Example: `583-gameplan-audit.md`

### Step 5: Proceed to Next Phase

Only after all items are ✅, proceed to:
- Issue audit complete → Write gameplan
- Gameplan audit complete → Write prompts
- Prompts audit complete → Execute

---

## Example Audit Matrix

```markdown
## Audit: #583 Gameplan against gameplan-template.md

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Issue number referenced | ✅ | #583 in header |
| Problem statement | ✅ | "Chat not persisting on refresh" |
| Five-whys analysis | ⚠️ | Only 3 whys - need 2 more |
| Success criteria | ✅ | 3 measurable criteria |
| Test strategy | ❌ | Missing entirely |
| Phases with estimates | ✅ | 4 phases, 2-3 hours |
| Rollback plan | ❌ | Missing |
| Dependencies listed | ✅ | None identified |

### Action Required
Before proceeding to prompts:
1. Complete five-whys to root cause
2. Add test strategy section
3. Add rollback plan
```

---

## Anti-Patterns

| Don't Do This | Why | Do This Instead |
|---------------|-----|-----------------|
| Skip audit under time pressure | This is exactly when drift occurs | Audit takes 5-10 min; rework takes hours |
| Mark requirements as "N/A" yourself | You may be wrong about applicability | Ask PM if requirement seems inapplicable |
| Audit without the template open | You'll miss requirements | Always have template visible |
| Audit multiple times | One thorough audit is sufficient | Do it once, do it right |
| Proceed with ⚠️ or ❌ items | Drift compounds at each phase | Fix everything before proceeding |

---

## Quality Checklist

After completing an audit:
- [ ] Template was open during entire audit
- [ ] Every template requirement has a row in the matrix
- [ ] No ⚠️ or ❌ items remain unfixed
- [ ] No requirements marked "N/A" without PM approval
- [ ] Audit matrix saved to `dev/YYYY/MM/DD/`
- [ ] Ready to proceed to next phase

---

## Key Insight

**LLMs struggle to follow templates while creating but excel at auditing against templates afterward.**

This asymmetry is why audit cascade works: instead of trying harder to follow templates during creation (which doesn't work), we accept imperfect creation and systematically audit afterward (which does work).

The word "audit" triggers systematic verification behavior. Use it.

---

## Pattern Families

This skill is part of the **Completion Theater Family** (045/046/047/049):

- **Pattern-045**: Diagnoses the gap (tests pass, users fail)
- **Pattern-046**: Enforces 100% completion (no expedience rationalization)
- **Pattern-047**: Enables pause when uncertain (Time Lord Alert)
- **Pattern-049**: Audits at every phase boundary — **this skill operationalizes 049**

These patterns form a reinforcing system. Audit cascade (049) is the operational mechanism that catches drift before it compounds. Apply the full family for multi-phase work.

See [PATTERN-FAMILIES.md](../../../docs/internal/architecture/current/patterns/PATTERN-FAMILIES.md) for full family index.

---

## Related

- [Pattern-049: Audit Cascade](../../../docs/internal/architecture/current/patterns/pattern-049-audit-cascade.md) - Full pattern documentation
- [Pattern-046: Beads Completion Discipline](../../../docs/internal/architecture/current/patterns/pattern-046-beads-completion-discipline.md) - No expedience rationalization
- [create-session-log](../create-session-log/SKILL.md) - Session documentation
- [close-issue-properly](../close-issue-properly/SKILL.md) - Issue closure with evidence

---

*Skill version: 1.0*
*Created: 2026-01-23*
*Scope: Cross-role*
