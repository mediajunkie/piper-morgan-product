# Audit: #950 against .github/ISSUE_TEMPLATE/feature.md

**Date**: 2026-04-16
**Auditor**: Lead Dev (code-opus)
**Phase**: Issue → Gameplan (first audit gate)

## Matrix

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Priority / Labels / Milestone / Epic header | ❌ | Not present in #950 body |
| Problem Statement > Current State | ⚠️ | Implicit in "Context" paragraph; not called out |
| Problem Statement > Impact (Blocks/User/Tech Debt) | ❌ | Missing |
| Problem Statement > Strategic Context | ⚠️ | Referenced via "MUX analysis", not explicit |
| Goal > Primary Objective (one sentence) | ⚠️ | Implicit in "Summary" |
| Goal > Example User Experience (before/after) | ❌ | Missing — critical for prompt-engineering work |
| Goal > Not In Scope | ❌ | Missing |
| What Already Exists | ❌ | Missing — I know the answer now; should capture |
| Requirements > Phases | ❌ | None described — will live in gameplan |
| Acceptance Criteria > Functionality | ✅ | Present (6 items) |
| Acceptance Criteria > Testing | ⚠️ | References Colleague Test + AAXT but no specific verification plan |
| Acceptance Criteria > Quality | ❌ | Missing |
| Acceptance Criteria > Documentation | ❌ | Missing |
| Completion Matrix | ❌ | Missing |
| Testing Strategy | ⚠️ | Implicit ("pass Colleague Test") — need specifics |
| Success Metrics (quant + qual) | ❌ | Missing |
| STOP Conditions | ❌ | Missing |
| Effort Estimate | ❌ | Missing |
| Dependencies | ❌ | Missing |
| Related Documentation | ⚠️ | Vision V2.2 referenced, but CXO gave many more canonical sources |
| Evidence Section | ❌ | Intentional — filled after implementation |
| Completion Checklist | ❌ | Intentional — filled at wrap-up |

## Fix Plan

Before writing the gameplan, update #950 to fill the gaps that matter *at planning time*:

- **Add** Priority/Labels/Epic header
- **Add** Problem Statement > Current State (explicit), Impact, Strategic Context
- **Add** Goal > Example User Experience (before/after dialog sample — essential for prompt work)
- **Add** Goal > Not In Scope (avoid scope creep into context assembler rewrite, personality service, etc.)
- **Add** What Already Exists (the working prohibitions, the warmth calibration, the #960 fabrication guard, the domain_context plumbing)
- **Add** Acceptance Criteria > Testing, Quality, Documentation
- **Add** Testing Strategy (canonical retest as evidence bar, Colleague Test as rubric, AAXT scenarios for multi-turn verification)
- **Add** Success Metrics (quant: Identity tone ≥ PASS on retest; qual: CXO sign-off on draft)
- **Add** Effort Estimate
- **Add** Dependencies (none strict; CXO direction memo is the enabling input)
- **Expand** Related Documentation to include everything CXO cited

Items deferred as intentional (filled during/after work, not at planning):
- Evidence Section
- Completion Checklist
- Completion Matrix

Items not applicable with PM approval marker needed:
- STOP Conditions: template says "Infrastructure doesn't match assumptions", "Tests fail", etc. These apply universally to all work — I'll include a generic STOP section rather than skip it. *Not marking as N/A.*

## Decision

Proceed with updating #950 body, then gameplan. Fresh #950 body drafted in `950-issue-body-updated.md` (next artifact).
