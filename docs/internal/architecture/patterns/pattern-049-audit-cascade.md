# Pattern-049: Audit Cascade

## Status

**Proven** - Validated through sustained velocity improvement (Jan 9-11, 2026: 23+ issues in 3 days)

## Context

LLMs, like their human trainers, struggle to adhere to checklists during creation. However, they excel at auditing work against checklists and making corrections. This asymmetry—poor at following templates while creating, excellent at verifying against templates after creating—is a fundamental characteristic that this pattern exploits.

The word "audit" appears to be a powerful trigger that activates careful, systematic verification behavior in ways that "check" or "review" do not.

### The Problem

Multi-step work (issues → gameplans → prompts → execution) accumulates drift at each handoff:
- Issue written without consulting template → gaps
- Gameplan based on incomplete issue → inherited gaps + new gaps
- Prompts based on flawed gameplan → compounded errors
- Execution based on flawed prompts → failure

Each step compounds errors from previous steps. By execution time, the accumulated drift can be substantial.

### The Discovery

January 10, 2026 saw exceptional velocity: 7 issues completed cleanly in 12 hours. Analysis revealed the differentiating factor was **mandatory audit gates between every phase**, not just at the end.

## Pattern Description

**Audit Cascade**: Insert explicit audit-and-correct steps between every phase of multi-step work. Each audit uses the relevant template as a checklist matrix.

```
┌─────────┐     ┌─────────┐     ┌──────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  Write  │────▶│  Audit  │────▶│  Write   │────▶│  Audit  │────▶│  Write  │────▶│  Audit  │────▶ Execute
│  Issue  │     │  Issue  │     │ Gameplan │     │Gameplan │     │ Prompts │     │ Prompts │
└─────────┘     └─────────┘     └──────────┘     └─────────┘     └─────────┘     └─────────┘
                    │                                │                                │
                    ▼                                ▼                                ▼
              Fix against                      Fix against                      Fix against
              issue template                   gameplan template                prompt template
```

### The Six Steps

1. **Write issue** (if doesn't exist yet)
2. **Audit issue** against template → fix gaps (there are always gaps, even when template was consulted)
3. **Write gameplan** based on audited issue; discuss any open questions
4. **Audit gameplan** against template → fix gaps
5. **Write prompts** for subagents based on audited gameplan
6. **Audit prompts** against template → fix gaps
7. **Execute** with cross-checking agents

### Key Insight: One Audit Is Usually Sufficient

A second audit pass is almost always redundant because the first audit with a checklist matrix is thorough. The power is in the *systematic comparison against template*, not in repetition.

## Implementation

### Templates Required

Each audit step requires a corresponding template:

| Phase | Template | Location |
|-------|----------|----------|
| Issue | Issue template (bug/feature/epic) | `.github/ISSUE_TEMPLATE/` |
| Gameplan | `gameplan-template.md` | Knowledge base |
| Prompts | `agent-prompt-template.md` | Knowledge base |

### Audit Process

For each audit step:

1. Open the relevant template
2. Create a checklist matrix (template section → current document)
3. Mark each requirement as ✅ present, ⚠️ partial, or ❌ missing
4. Fix all ⚠️ and ❌ items before proceeding
5. Document any intentional deviations with rationale

### Example Audit Matrix

```markdown
## Gameplan Audit: Issue #583

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Issue number referenced | ✅ | #583 |
| Problem statement | ✅ | Chat not persisting on refresh |
| Five-whys analysis | ⚠️ | Only 3 whys - need deeper |
| Success criteria | ✅ | 3 criteria defined |
| Test strategy | ❌ | Missing - add TDD approach |
| Phases with estimates | ✅ | 4 phases, 2-3 hours |
| Rollback plan | ❌ | Missing - add |

**Action**: Fix five-whys, add test strategy, add rollback plan before proceeding.
```

## Complementary Practices

### Bug-to-Feature Escalation

If a bug fix does not terminate quickly (rule of thumb: >30 minutes of investigation), reframe it as unfinished feature work and subject it to full discipline:
- DDD review (is the domain model correct?)
- TDD process (write failing test first)
- Independent subagent verification

This prevents "quick fix" thinking from creating technical debt.

### Five Whys for Root Cause

Before accepting any fix, apply five whys to look for:
- Categorical issues (does this affect a class of things?)
- Patterns (have we seen this before?)
- Systemic issues (is something structurally wrong?)

Don't be satisfied with the first surface patch idea. The goal is to find the root cause, not just silence the symptom.

### Independent Agent Verification

Use separate agents for:
- Planning (gameplan creation)
- Implementation (code writing)
- Verification (testing and review)

This prevents single-point-of-failure assumptions and catches issues that a single agent might miss due to consistency bias.

## Benefits

- **Prevents compounding errors**: Each gate catches drift before it propagates
- **Exploits LLM strengths**: Auditing against templates is where LLMs excel
- **Creates documentation trail**: Audit matrices document what was checked
- **Enables parallelization**: Clear handoff artifacts allow agent switching
- **Improves velocity**: Counterintuitively, more gates = faster completion (less rework)

## Trade-offs

- **Overhead per step**: Each audit adds ~5-10 minutes
- **Template maintenance**: Templates must be kept current
- **Discipline required**: Easy to skip "just this once" (don't)

## Evidence

### January 10, 2026 Velocity Sprint
- **Issues completed**: 7 in 12 hours
- **Method**: Full audit cascade on each issue
- **Comparison**: Previous attempts without cascade: 2-3 issues/day with more rework

### January 9-11, 2026 Sustained Velocity
- **Total**: 23+ issues in 3 days
- **Quality**: Minimal rework required
- **Factor**: Consistent methodology enforcement

## Anti-Patterns

### Skipping Audits Under Time Pressure
"I'll skip the gameplan audit since I understand the issue well."
→ This is exactly when drift occurs. The audit catches assumptions you don't know you're making.

### Auditing Without Templates
"I'll just review this carefully."
→ Without a checklist, you'll miss the same things you missed when writing. The template externalizes the requirements.

### Multiple Redundant Audits
"I'll audit three times to be sure."
→ One thorough audit against template is sufficient. Multiple passes have diminishing returns.

## Related Patterns

### Completion Theater Family
- [Pattern-045: Green Tests, Red User](pattern-045-green-tests-red-user.md) - Audit cascade prevents this
- [Pattern-046: Beads Completion Discipline](pattern-046-beads-completion-discipline.md) - Cascade ensures 100% before moving on
- [Pattern-047: Time Lord Alert](pattern-047-time-lord-alert.md) - Cascade resists time pressure shortcuts

### Methodology
- [methodology-00-EXCELLENCE-FLYWHEEL.md](../../development/methodology-core/methodology-00-EXCELLENCE-FLYWHEEL.md) - Cascade implements flywheel discipline
- [methodology-07-VERIFICATION-FIRST.md](../../development/methodology-core/methodology-07-VERIFICATION-FIRST.md) - Cascade is verification-first in practice
- [methodology-17-CROSS-VALIDATION-PROTOCOL.md](../../development/methodology-core/methodology-17-CROSS-VALIDATION-PROTOCOL.md) - Independent agent verification

### Templates
- `gameplan-template.md` - Gameplan audit checklist
- `agent-prompt-template.md` - Prompt audit checklist
- Issue templates - Issue audit checklists

## Summary

**The Audit Cascade is institutionalized skepticism at every handoff.**

It exploits a key asymmetry: LLMs struggle to follow templates while creating but excel at auditing against templates afterward. By inserting mandatory audit gates between every phase, errors are caught and corrected before they compound.

The word "audit" matters—it triggers systematic, thorough verification behavior.

---

*Pattern created: January 13, 2026*
*Evidence: January 9-11, 2026 velocity sprint (23+ issues, 3 days)*
*Status: Proven*
