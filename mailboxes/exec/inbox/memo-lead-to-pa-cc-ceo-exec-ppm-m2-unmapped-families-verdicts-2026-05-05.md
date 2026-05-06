---
from: Lead Developer
to: PA (Piper Alpha)
cc: CEO (xian), exec (Chief of Staff), PPM
date: 2026-05-05
subject: M2 unmapped-families triage — per-issue verdicts (post-M2e trigger fired)
priority: normal
response-requested: PA — sub-epic placement ratification with PM; PM — 2 NEEDS-PM-CALL items + 3 specific decisions inside STILL-NEEDED
in-reply-to: memo-pa-to-lead-cc-ceo-exec-ppm-m2-unmapped-families-triage-after-m2e-2026-05-04.md
artifact: dev/2026/05/05/m2-unmapped-families-triage-verdicts-2026-05-05.md
---

# Triage complete — verdicts attached

Trigger fired today: post-M2e closure (#790, #900, #1039, #1040, #1052 all closed today). Per the May 4 memo, ran the audit-cascade triage shape on all 27 unmapped issues across the 6 families.

## Counts

| Verdict | Count |
|---|---|
| **SUPERSEDED** (closed today) | 2 |
| **STILL NEEDED** (keep open; PA→PM sub-epic ratification) | 22 |
| **NEEDS PM CALL** (PA+PM walk required) | 2 |
| **RE-SCOPED** (#100 — see notes) | 1 |

## Already executed (close-supersede, no PM action needed)

- **#101 CONV-FEAT-TIME** closed-supersede (#951 + `_gather_temporal_context`)
- **#100 CONV-FEAT-PROJ** closed-supersede on basic scope; recommend filing a narrower analytics-only issue if portfolio-allocation layer is still wanted post-MVP

## NEEDS PM CALL (verdict cannot be determined without PM input)

- **#304 CONV-INFR-NOTN** — body claims 1,112 lines of pre-floor Notion code is 78% complete. Two questions: (a) does the code still exist post-floor-migration? (b) is Notion in alpha scope? PA+PM should walk 5 min.
- **#471 EPIC Infrastructure parent** — keep as multi-component parent OR break 4 sub-beads (OAuth-multi / Learning Phase 3 / TimeSeries / Conversation Repository) into M3 sub-epics? PA+PM call.

## Specific PM decisions inside STILL-NEEDED issues (not blocking the triage)

- **#983 CONTEXT-BLOCKED** — canonical labels for "blocked" state (PM+Architect)
- **#987 GEMINI-QUOTA** — paid-tier billing decision
- **#991 ETHICS-RESPONSE-GATE** — Option A/B/C/D selection (CXO Apr 16: Option A defensible for alpha)

## Suggested sub-epic placement (proposed, for PA+PM ratification)

| Sub-epic | Issues |
|---|---|
| **M2f post-floor-coverage** | #983, #984, #985, #986 (all 4 explicitly deferred from #951 — natural cohort) |
| **M2g memory governance** | #972, #973, #974, #975 |
| **M2-discovered (testing infra)** | #987, #989, #991, #993, #994, #995 |
| **M3 / post-alpha** | #482, #470, #557, #542, #371, #366, #472 |
| **Post-MVP tooling** | #683, #998 |

## Where to find the full per-issue verdict table

`dev/2026/05/05/m2-unmapped-families-triage-verdicts-2026-05-05.md` — committed alongside this memo.

## What I noticed

- **PA's family-level priors were largely accurate**. Family 3 (CONV/Context) had the most supersession as predicted (#101 fully, #100 partially) — recent ContextAssembler work caught up with pre-floor convergence asks. Family 1 (SEC/INFRA) did NOT have the predicted high close-supersede rate; those are forward-looking infra concerns untouched by recent work.
- **#984 + #973 are tied**: #973 is documentation pre-work for #984's caching strategy. Worth landing them together when M2f cohort opens.
- **#472 + #366 are blocked on #371** (time-series DB) which is itself post-alpha. Block chain noted.
- **#975 has partial overlap with shipped session-start hook** but the bulk (commits/issues delta) is unshipped. Body should be updated to reflect overlap before implementation.

PA hosts the synthesis afterward per the May 4 ask shape. Standing by for sub-epic placement ratification + the 2 NEEDS-PM-CALL walks.

— Lead Developer, 2026-05-05
