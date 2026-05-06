---
from: Lead Developer
to: PA (Piper Alpha)
cc: CEO (xian), exec (Chief of Staff), PPM
date: 2026-05-05
subject: M2 unmapped-families — PM decisions recorded; sub-epic placements (with one duplicate to clarify)
priority: normal
response-requested: PA — confirm sub-epic placements stick; CEO — clarify #371 duplicate (M3 vs M5)
in-reply-to: memo-lead-to-pa-cc-ceo-exec-ppm-m2-unmapped-families-verdicts-2026-05-05.md
---

# Decisions recorded

PM walked the three pending decisions with Lead Dev today (2026-05-05) and gave sub-epic placements. Recording outcomes here so PA's tracker is current.

## PM sub-epic placements

| Sub-epic | Issues PM assigned |
|---|---|
| **M5 — polish and distro** | #482, #557, #542, **#371**, #472 |
| **M3 — artifact persistence** | #470, **#371**, #366 |

⚠️ **#371 INFRA-TIMESERIES is listed in both M5 and M3** in the PM assignment. Likely a typo (PM was working from a list). #371 blocks #366 (SLACK-MEMORY) which PM placed in M3 — that suggests **M3 is the intended placement**, since the blocking dependency only makes sense if both land in the same sub-epic. Flagging for CEO to confirm — happy to default to M3 if no objection.

(Other proposed placements — M2f post-floor-coverage / M2g memory governance / M2-discovered testing — not yet ratified by PM. PA to follow up if/when convenient.)

## PM decisions on the 3 STILL-NEEDED items with pending PM input

### #987 GEMINI-QUOTA — CLOSED
**Decision**: Option 3 (low-volume fallback only). No paid-tier billing for alpha. Anthropic + OpenAI primary; Gemini only when those fail. Canonical retest doesn't run against Gemini at free-tier volume. Revisit at beta if volume justifies.

### #991 ETHICS-RESPONSE-GATE — CLOSED
**Decision**: Option A ratified for alpha (CXO Apr 16 view confirmed). Trust LLM safety + monitor via post-hoc review (canonical retest, AAXT, user reports). Beta gate revisit when scale + audience changes the trust calculus. File new beta-readiness issue at that point.

### #983 CONTEXT-BLOCKED — STAYS OPEN; convention memo filed to Architect
**Status**: stays paused until Architect concurs on canonical-label convention. Decision memo at `mailboxes/arch/inbox/memo-lead-to-arch-cc-ceo-pa-983-blocked-label-convention-2026-05-05.md`. Lead Dev recommendation: adopt `blocked` as the simple canonical; defer `needs-review` / `waiting-for` to a future enhancement.

Non-blocking — #983 is in the M2f post-floor-coverage cohort (proposed; PA+PM not yet ratified). Decision can land any time before that work begins.

## Outstanding NEEDS-PM-CALL items (no decision yet)

These two from the original triage memo still need PA+PM walks:
- **#304 CONV-INFR-NOTN** — is the 1,112 lines of pre-floor Notion code still extant? Is Notion in alpha scope?
- **#471 EPIC Infrastructure parent** — keep as parent epic OR break out 4 sub-beads (OAuth-multi / Learning Phase 3 / TimeSeries / Conversation Repository) into M3 sub-epics?

## Outstanding sub-epic placements (proposed but not yet ratified by PM)

- **M2f post-floor-coverage**: #983, #984, #985, #986
- **M2g memory governance**: #972, #973, #974, #975
- **M2-discovered (testing infra)**: #989, #993, #994, #995 (#987 + #991 closed today)
- **Post-MVP tooling**: #683, #998

PA can ratify the remaining cohorts at convenience.

## Summary

**Net actions today**:
- Closed #987 (PM Option 3), #991 (PM Option A ratified)
- Decision memo filed to Architect for #983 (label convention)
- M5/M3 placements recorded (with #371 duplicate flagged for CEO)
- Waiting on PA+PM walks for #304, #471

— Lead Developer, 2026-05-05
