# Audit: Issue #992 against `.github/ISSUE_TEMPLATE/feature.md`

**Audit phase**: Issue → Gameplan (gate 1 of 3)
**Date**: 2026-04-22
**Auditor**: Lead Developer (Claude Opus)

---

## Audit Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Title with label/short-name | ✅ | "ETHICS-ACTIVATE: Turn on ENABLE_ETHICS_ENFORCEMENT with validation + CXO voice" |
| Priority | ✅ | P1 |
| Related issues / ADRs | ✅ | Parent #964; PDR-004 referenced; code paths cited |
| Problem Statement: Current State | ✅ | Flag defaults false; BoundaryEnforcer never fires in prod |
| Problem Statement: Impact | ⚠️ | Implicit ("worst state" noted in Priority). Not broken out as Blocks/User/TechDebt. Not blocking — gameplan can carry. |
| Strategic Context | ✅ | Ties to PDR-004 Principle 4 (ethical boundary mode) |
| Goal / Primary Objective | ✅ | Turn on flag after validation + voice-shape refactor |
| Example User Experience | ⚠️ | No concrete before/after scripted. Should add 1-2 denial scenarios to gameplan as "happy path voice." |
| Not In Scope | ✅ | Gap 2 (post-gen check), re-architecting, new mechanisms — all excluded |
| What Already Exists | ✅ | Enforcer wired; pattern lists enumerated |
| What's Missing | ✅ | Structured return, voice pipeline, audit routing, gates |
| Requirements: Phases | ❌ | Issue lists AC but doesn't structure phases. **This is what the gameplan supplies** — not a blocker for issue audit, just a reminder the gameplan must do this work. |
| Acceptance Criteria: Functionality | ✅ | Structured return, voice pipeline, audit logging all enumerated |
| Acceptance Criteria: Testing | ⚠️ | Colleague-Test and false-positive gates present but no explicit unit/integration test enumeration. **Gameplan must add this.** |
| Acceptance Criteria: Quality | ⚠️ | False-positive threshold = quality gate; but no explicit "no regressions" callout. Add to gameplan. |
| Acceptance Criteria: Documentation | ⚠️ | Closing-comment evidence required, but `docs/internal/architecture/current/ethics-architecture.md` update not called out. **Add to gameplan.** |
| Completion Matrix | ❌ | Not populated in issue. Template allows this to be filled during work. Gameplan should include one. |
| Testing Strategy: Unit | ⚠️ | Implied by refactor; not explicit. Gameplan must specify (enforcer structured return, pattern matching, category mapping). |
| Testing Strategy: Integration | ⚠️ | Denial floor pipeline end-to-end implied by Colleague-Test; make explicit in gameplan. |
| Testing Strategy: Manual | ⚠️ | Colleague-Test scenarios ARE the manual harness. Make that explicit. |
| Success Metrics: Quantitative | ✅ | FP rate <2-3%; Colleague Test ≥7; Tone=0 auto-fail |
| Success Metrics: Qualitative | ✅ | PDR-004 Principle 4 Mode 2 voice via Colleague Test T dimension |
| STOP Conditions | ⚠️ | Not listed explicitly in issue. Default gameplan STOPs apply (tests fail, pattern exists, completion bias). Add issue-specific ones in gameplan: FP rate >3%, Colleague <7, existing enforcer tests regress. |
| Effort Estimate | ❌ | Not provided. Gameplan should classify size per phase. |
| Dependencies | ✅ | Lists: CXO input (received), pattern tuning possible |
| Related Documentation | ✅ | PDR-004, parent #964, code paths |

---

## Triage

**Not blocking the gameplan** (issue description is complete in substance):
- Impact section (⚠️) — strategic context carries it
- Example UX (⚠️) — will be supplied via Colleague-Test denial scenarios in gameplan
- Completion Matrix (❌) — filled during implementation, not at issue authoring
- Effort estimate (❌) — gameplan will phase-size

**Must be added by the gameplan** (these are the audit-cascade items the next phase must resolve):
1. Explicit phase breakdown with estimates
2. Unit/integration/manual test strategy enumeration
3. Documentation updates (ethics-architecture.md, PDR-004 cross-ref, operations env-vars.md)
4. Completion matrix scaffold
5. Issue-specific STOP conditions (FP rate >3%, any Colleague <7, enforcer regression)
6. 1-2 concrete denial-scenario user-experience scripts
7. "No regression" callout against existing boundary_enforcer tests

---

## Audit Verdict

**PROCEED to gameplan drafting**, carrying the 7 "must add" items forward as gameplan requirements. No issue-description edits required — all ⚠️/❌ items are either carried by adjacent fields (Strategic Context carrying Impact, Success Metrics carrying quality) or are phase-level work that the gameplan is the right artifact to supply.

## Post-Audit: Update Issue?

No. Issue description is substantively complete. The gameplan is the document that fills the structural gaps, and that's the correct next artifact. Re-opening #992 to add boilerplate phase/metric headers would be paperwork without signal.
