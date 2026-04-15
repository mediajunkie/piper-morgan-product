# Roadmap Refresh Prep: v14.3 → v14.4

**Author**: Piper Alpha (PA)
**Date**: April 2, 2026
**Status**: Prep notes for PM review — actual roadmap update should happen after M1 gate closes
**Source**: Diff between roadmap.md (Mar 10) and BRIEFING-CURRENT-STATE (Mar 29) + GitHub state

---

## What's Out of Date

### Executive Summary
**Current**: "PM taking deliberate pause before M1"
**Reality**: M1 execution complete. Gate verification phase. All engineering tiers done.

### M1 Status
**Current**: "14/30 done, 47% cherry-picked, 15 remaining"
**Reality**: 30/30 done. Gates 3-4 verified (6,310 tests, 0 failures). Gates 1-2 await PM manual testing (14 scenarios in #926).

### Timeline
**Current**: "M1 sprint begin" as unchecked future item
**Reality**: M1 began Mar 12, execution complete Mar 24, gate verification in progress

### Inchworm Position
**Current**: "M1: Foundation (47% cherry-picked) ← NEXT"
**Reality**: "M1: Foundation — GATE VERIFICATION ← CURRENT"

---

## New Issues to Add (Filed Since Mar 10)

| Issue | Title | Sprint | Status |
|-------|-------|--------|--------|
| #921 | FastAPI/Starlette upgrade | M5 | Open |
| #925 | Floor inversion Phase 3-4 | Post-M1 | Open |
| #926 | M1 Sprint Completion Gate | M1 | Pending (14 scenarios) |
| #927 | E2E: Task lifecycle smoke tests | M2 | Open |
| #928 | E2E: Automated canonical suite | M2 | Open |
| #929 | AAXT: Golden scenarios with DeepEval | M2 | Open |
| #930 | CI: E2E + AAXT nightly | M2 | Open |
| #932 | SEC: HIBP stub false safe | M5 | Open |
| #933 | SEC: API key validation disabled | M5 | Open |
| #934 | INVESTIGATE: orphaned task_management.py | M2 | Open |
| #935 | TECH-DEBT: BudgetManager no persistence | M5 | Open |
| #936 | TECH-DEBT: UserService in-memory | M5 | Open |
| #938 | Q2 Maintenance Sweep | Process | Open |

---

## Major Architectural Changes to Document

1. **ADR-060: Floor-First Routing** — shipped Mar 19. Changes the entire routing architecture. LLM floor is default; handlers activate only for side effects.
2. **ADR-059: Workflow Dispatcher** — shipped Mar 19. Onboarding workflow removed per Gall's Law.
3. **PDR-004: Experience Philosophy** — ratified Mar 22. Four principles including "session belongs to user" and LLM floor guarantee.

---

## New Infrastructure to Note

- Mailbox v3 (10-role, `/deliver-mail` skill)
- Blog pipeline (269/269 posts local, `/publish-to-blog` v0.2→v0.4)
- Omnibus automation (`/create-omnibus` skill)
- Agent 360 (first deployment, 9/9 response)
- Editorial calendar (320 entries)
- Piper Alpha operational (Phase 1)
- Cross-pollination hub (daily briefs between PM and Klatch)
- Shipping News section on website (separate from blog)

---

## Sprint Summary Table Update

**Current (v14.3)**:
```
| M1 | MVP Foundation | 31 | 14 | 17 | 45% | ○ NEXT |
```

**Proposed (v14.4)**:
```
| M1 | MVP Foundation | 30 | 30 | 0 | ~98% | 🎯 GATE VERIFICATION |
```

(~98% because #926 gate closure is the remaining 2%)

---

## Timeline Revision

```
March 2026
- [x] M1 sprint begin (Mar 12)
- [x] M1 Tier 1-3 complete (Mar 22)
- [x] M1 Tier 4 complete (Mar 24)
- [x] Gates 3-4 verified (Mar 24)
- [ ] M1 gate closure (#926 — 14 scenarios, PM manual testing)

April 2026
- [ ] M2 sprint begin (post M1-gate)
- [ ] E2E + AAXT testing track (#927-930)
- [ ] IAC presentation (Apr 17, Philadelphia)
- [ ] M3 sprint begin

May 2026
- [ ] M4-M5 execution
- [ ] FastAPI upgrade (#921)
- [ ] Security hardening (#932-933)

June-July 2026
- [ ] DIST Phase 1 (MCP-native packaging)
- [ ] DIST Phase 2 (Desktop distribution)
- [ ] Beta → v1.0
```

---

## Key Pattern: M1 Discovery Work

M0 expanded from 5 planned → 27 actual issues (5.4x).
M1 appears to have expanded similarly — the original 15 remaining issues led to 17 new issues (#921-937) being filed during execution.

**Lesson for v14.4**: M2-M6 estimates should assume similar expansion. The roadmap should note this pattern explicitly as a planning input.

---

## Recommendation

Wait for M1 gate closure before publishing v14.4. The roadmap refresh should capture:
1. M1 as COMPLETE (not just "gate verification")
2. All 17 new issues with sprint assignments
3. Revised timeline
4. Distribution strategy update (MCPB)
5. PA as operational team member
6. Expansion pattern as planning input

The backlog review (separate document) identifies 6-8 issues for closure and suggests a MVP scope triage pass — those changes should land before or alongside the roadmap refresh.

---

*Prep notes only — actual roadmap.md update is a PM-authorized action.*
