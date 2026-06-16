# Audit: #1252 (REFACTOR-AUTH-ANCHORING umbrella) against `.github/ISSUE_TEMPLATE/feature.md`

_Lead Dev · 2026-06-15 · audit-cascade ISSUE gate (Pattern-049). Refactor kickoff per PM "gameplan-first, full audit-cascade." Template open during audit._

| Template Requirement | Status | Notes |
|---|---|---|
| Title `[LABEL]-[SHORT-NAME] - Full Title` | ✅ | `[REFACTOR] … (ADR-071 D2–D6)` + body H1 `REFACTOR-AUTH-ANCHORING` |
| Priority | ✅ | P1 |
| Labels | ✅ | refactor/architecture (note: `refactor` GH-label doesn't exist → `[REFACTOR]` title prefix; not blocking) |
| Milestone | ✅ | MVP 0.9-beta (sprint = PPM/PM call) |
| Epic | ✅ | ADR-071 consolidating refactor (this is the umbrella) |
| Related (issues/patterns/ADRs) | ✅ | ADR-071, #1241, #1238, #1250, #1239, #1248, ADR-058, m-40, m-41 |
| Problem → Current State | ✅ | 3-way inconsistency + (c,3) gaps + (a,3) leak paths + 40+ resolution sites + #1250 instance |
| Problem → Impact (Blocks/User/Debt) | ✅ | all three named |
| Problem → Strategic Context | ✅ | ADR-071 ratified + PM-endorsed refactor; gameplan-first |
| Goal → Primary Objective | ✅ | one canonical enforced anchoring pattern (one sentence) |
| Goal → Example User Experience (if applicable) | ⚠️→✅ | **GAP FIXED**: added a before/after example (#1250 toggle + dev-facing "new content inherits the pattern") |
| Goal → Not In Scope | ✅ | multi-tenancy / entity-model spec / ADR-058 changes |
| What Already Exists → Infrastructure | ✅ | ADR-071, #1241 audit, ratchet-lint precedent, ensure_conversation_exists |
| What Already Exists → What's Missing | ✅ | the canonical convention + threading + fixes + guards |
| Requirements → Phases (Objective/Tasks/Deliverables) | ⚠️→✅ | phases had Objective+Tasks but **lacked explicit per-phase Deliverables/Evidence** → **GAP FIXED**: added a one-line Deliverable to each phase |
| Requirements → Phase Z Completion & Handoff | ✅ | present |
| Acceptance Criteria → Functionality | ✅ | owner_id canonical / (c,3) closed / (a,3) fixed / threading / #1250 works |
| Acceptance Criteria → Testing | ✅ | TDD per phase / D5 guards / regression / #1248 jest CI |
| Acceptance Criteria → Quality | ✅ | no regressions / recurrence closed / ADR updated |
| Acceptance Criteria → Documentation | ✅ | decisions.log / cross-refs / session log |
| Completion Matrix | ✅ | per-phase table with legend + definition-of-complete |

## Gaps found + fixed (before proceeding to gameplan)
1. **Goal → Example User Experience** (⚠️ missing, "if applicable" = applicable here) → added the #1250 before/after + the developer-facing "new content type inherits the pattern" example.
2. **Requirements → per-phase Deliverables** (⚠️ tasks present, deliverables implicit) → added a concise Deliverable line to each phase so the umbrella states each phase's artifact (full DDD/TDD detail still lands in the gameplan, the next gate).

## Result
All template requirements ✅ after the 2 fixes. **ISSUE gate PASSED → proceed to the GAMEPLAN gate** (write gameplan vs `knowledge/gameplan-template.md`, then audit it).
