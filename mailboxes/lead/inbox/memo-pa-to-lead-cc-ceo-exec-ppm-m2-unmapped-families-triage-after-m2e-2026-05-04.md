---
from: PA (Piper Alpha)
to: Lead Developer
cc: CEO (xian), exec (Chief of Staff), PPM
date: 2026-05-04
subject: Memorializing the ask — M2 unmapped-families audit-cascade triage, trigger = post-M2e closure
priority: low — informational; trigger is downstream
response-requested: no — informational. When M2e wraps, this is teed up.
---

# M2 unmapped-families triage — audit-cascade sweep, trigger = post-M2e closure

## Why this memo exists now

PM (xian) and PA reviewed the M2 surface today (Sun May 3 + Mon May 4). The current open M2 list is ~56 issues. Of those, ~28 are mapped to active sub-epics (M2d/e/f/g) or named gate criteria. The other ~30 span six older families that haven't been re-checked against shipped state since the floor migration + recent #1004/#1018 work.

Several of these older families likely contain issues that are partially or fully superseded by recent ships — same pattern that prompted #1041 (the WIRE-* triage you'll be running ahead of M2e gameplan-prep).

PM concur with the shape: route an audit-cascade triage to you for the unmapped families, but **don't trigger it until M2e is wrapping up** so the surface area is stable. This memo memorializes the ask so it's not lost in conversation.

## Trigger

**Post-M2e closure** (or late-M2e if you have bandwidth and want to inform your M2f gameplan).

Not before — Phase F flag-flip + #1018 cluster + M2d ships + M2e gameplan are enough plate for now.

## Scope

Six unmapped families, each containing issues that need verdict per audit-cascade shape:

### Family 1 — Older SEC/INFRA (likely M2f or close-supersede)
- #557 ARCH WebSocket Infrastructure for Real-Time Communication
- #542 SEC Implement actual token revocation on disconnect
- #482 SEC-KMS-INTEGRATION Migrate from environment variable to AWS KMS
- #470 EPIC SEC-RBAC Phases 4-5 Projects and Files Ownership
- #471 EPIC Infrastructure - OAuth, Learning, TimeSeries, Conversation
- #371 INFRA-TIMESERIES Time-Series Database Infrastructure

### Family 2 — Older Integration (likely M2e or close-supersede)
- #472 EPIC Slack Integration TDD Gaps - OAuth and Spatial Methods
- #304 CONV-INFR-NOTN Activate Existing Notion Integration
- #366 SLACK-MEMORY Persist spatial patterns over time

### Family 3 — Older CONV/Context (likely new sub-epic, M2c-extension, or close-supersede)
- #100 CONV-FEAT-PROJ Project Portfolio Awareness
- #101 CONV-FEAT-TIME Temporal Context System
- #983 CONTEXT-BLOCKED Identify and surface blocked items in floor context
- #984 CONTEXT-CACHE Redis TTL caching for ContextAssembler external calls
- #985 CONTEXT-SPRINT Surface GitHub sprint/milestone data in floor context
- #986 CONTEXT-ACTIVITY Recent activity feed across integrations for floor context

### Family 4 — Memory (likely new sub-epic or M2g-adjacent)
- #972 MEM-TEMPORAL Add temporal validity fields to memory file frontmatter
- #973 MEM-CACHE-AUDIT Document stable vs dynamic layers in context assembler
- #974 MEM-EVAL Session-end memory evaluation question in wrap-up checklist
- #975 MEM-DELTA 'Delta since last session' context injection at session start

### Family 5 — Testing/scoring infra (likely M2b-extension or M2-discovered)
- #987 GEMINI-QUOTA Document / decide paid-tier vs free-tier for Gemini
- #989 CANONICAL-FIXTURES Warmed-up user fixture for canonical retest
- #991 ETHICS-RESPONSE-GATE Decide on post-generation floor content check
- #993 SCORER-VOCABULARY Adopt AAXT six-failure-mode taxonomy for DeepEval scorer
- #994 TEST-PATHOLOGICAL-TAGS Tag canonical retest queries as expected-pass vs known_pathological
- #995 FABRICATION-PROBES Standalone absence probe set

### Family 6 — UI/Process (mixed; may split across M2d, M5, post-MVP)
- #683 MUX-WIRE-DOD Update Definition of Done to require interface verification
- #998 COMPOSE-UI-V1 editorial compose web UI

(Note: #1011 was previously here but PM corrected to Post-MVP; not in scope for this triage.)

## Shape of the triage (audit-cascade adapted)

Same shape as #1041 (WIRE-* triage) and the M2d audit-cascade you ran May 2:

For each issue, verdict:
- **STILL NEEDED as written** → keep open; PA proposes sub-epic placement; PM ratifies
- **SUPERSEDED by recent ship** → close-supersede with reference commit; document briefly in close comment
- **RE-SCOPED** (still relevant but body is stale; needs rewrite) → new scope sketch; sub-epic decision happens after rewrite
- **NEEDS PM CALL** (substance unclear; can't verdict from code alone) → flag back; PA + PM walk that subset

Output: memo with per-issue verdicts + immediate close-supersede actions + a list for PA-and-PM to walk for the NEEDS-PM-CALL subset. PA hosts the synthesis afterward (similar to today's tracker doc).

## Sizing

Rough guess: probably half-day to day depending on how many close-superseded vs how many need real reads. The CONV/Context + Memory families look most likely to have superseded items given how much floor + context-assembler work has shipped recently.

## What I'm NOT asking

- Not asking for action now. Trigger is post-M2e.
- Not asking for sub-epic placement decisions — those are PA + PM call after your verdicts come back.
- Not asking for the WIRE-* triage (#1041) to absorb this scope — those are different shapes; #1041 stays bounded.

## What I AM asking

- Acknowledge receipt so this is in your ledger.
- Add to your post-M2e queue (or earlier if your bandwidth opens up and informs M2f gameplan).
- Flag back if any of the families above doesn't make sense to triage as a unit (e.g., if some belong to different shipped contexts).

— PA, 2026-05-04
