# Audit: #964 against .github/ISSUE_TEMPLATE/feature.md

**Date**: 2026-04-16
**Auditor**: Lead Dev (code-opus)
**Phase**: Issue → Plan (first audit gate, per audit-cascade skill)
**Nature of #964**: Verification/analysis task — deliverable is a findings memo, not code

## Matrix

| Template Section | Status | Notes |
|-----------------|--------|-------|
| Priority / Labels / Milestone / Epic header | ❌ | Missing from body |
| Problem Statement > Current State | ⚠️ | Stated in "Context" paragraph |
| Problem Statement > Impact | ❌ | Missing — what's the risk if coverage dropped? |
| Problem Statement > Strategic Context | ⚠️ | Partial (ADR-060 context given) |
| Goal > Primary Objective | ⚠️ | Implicit in Summary, not one-sentence |
| Goal > Example User Experience | ✅ N/A | Verification task — no user-facing change to illustrate |
| Goal > Not In Scope | ❌ | Missing — risk of scope creep into re-architecting ethics |
| What Already Exists | ⚠️ | Some references (BoundaryEnforcer, handler layer, #960 fabrication guard) but scattered |
| Requirements > Phases | ⚠️ | The 6 acceptance criteria serve as phase markers but not called "phases" |
| Acceptance Criteria > Functionality | ✅ | Present (6 items) |
| Acceptance Criteria > Testing | ✅ N/A | Verification task, no code added |
| Acceptance Criteria > Quality | ❌ | Missing — memo quality criteria |
| Acceptance Criteria > Documentation | ⚠️ | "Findings memo" mentioned; recipients clear |
| Completion Matrix | ❌ | Intentional — filled during Phase 7 closure |
| Testing Strategy | ✅ N/A | Verification task, no automated tests to define |
| Success Metrics | ❌ | Missing — what makes this a "complete" verification? |
| STOP Conditions | ❌ | Missing — what would force escalation mid-verification? |
| Effort Estimate | ❌ | Missing |
| Dependencies | ⚠️ | #690 referenced, not formalized |
| Related Documentation | ⚠️ | ADR-060 referenced, PDR-004 implied, no explicit list |
| Evidence Section | ❌ | Intentional — filled during/after |

## N/A Rationale (explicit per audit-cascade skill)

| Item | Why N/A |
|------|---------|
| Example User Experience | This issue produces a verification memo; there is no user-facing behavior change to illustrate. Before/after is about internal enforcement coverage, not UX. |
| Acceptance Criteria > Testing | No code is written; no tests to define. Verification is done via cross-reference and memo review. |
| Testing Strategy section | Same as above. |

These align with the template's implicit "When to Apply" — the feature template targets code-change features. A verification task is a legitimate variant.

## Fix Plan (pre-execution)

Update #964 body to add:
1. **Priority/Labels/Milestone** header (P2, `verification`, MVP/M2c)
2. **Impact statement** — what's the risk if a gap slipped through (ethical boundary failure = user trust erosion, potential compliance issue, reputational)
3. **Not In Scope** — re-architecting ethics stack, adding new enforcement, tuning thresholds
4. **What Already Exists** — consolidated list of current known enforcement mechanisms
5. **Success Metrics** — qualitative (comprehensive inventory + clear decision per gap + memo signed off by PM/CXO)
6. **STOP Conditions** — adapted for verification work (gap with no current mitigation + no clear path forward → escalate to PM before deciding)
7. **Effort Estimate** — Medium (2-3 hours for Lead Dev in-context)
8. **Explicit Dependencies** — #690 WIRE-BOUNDARY visibility, ADR-060 read, PDR-004 Principle 4 context
9. **Related Documentation** — explicit links/paths

## Decision

Proceed with Phase 1 inventory after updating #964 body. Updated body saved to `964-issue-body-updated.md`.
