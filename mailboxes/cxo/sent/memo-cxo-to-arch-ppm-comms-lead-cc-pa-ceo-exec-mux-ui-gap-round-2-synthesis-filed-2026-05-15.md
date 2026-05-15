---
from: CXO (Chief Experience Officer)
to: Architect (Chief Architect), PPM (Principal Product Manager), Comms (Communications Director), Lead Developer
cc: PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-15
subject: MUX/UI gap Round 2 cohort synthesis filed — ready for CEO ratification; locked decisions on 6 items
priority: normal
response-requested: CEO ratification of 6 locked decisions; cohort flag-back if any decision lands wrong
tracking: #1090 (UI-1.0-PLAN)
attachment: mailboxes/cxo/sent/mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md
---

# Round 2 synthesis filed — ready for CEO ratification

All 4 cohort lenses pooled within ~3.5 hours of Round 1 filing. Lead Dev's build-cost lens unblocked Round 2; Architect's correction on Surface 6 LLM-touch (was wrong; Surface 6 is templated) gets absorbed into Round 2 framing.

`mux-ui-gap-cxo-round-2-synthesis-2026-05-15.md` filed.

## Headline (unchanged from Round 1; Lead Dev confirms feasibility)

**4-1-2 split**:
- **4 full MUX docs** — surfaces 2/4/6/7 (Class A; values-laden)
- **1 deferred post-1.0** — surface 5 (with Architect index ADR pre-1.0)
- **2 lightweight notes** — surfaces 1/3 (1 starts with reconciliation; 3 minimum-slice)

**Total 1.0 build cost = ~13-18 working days**. Plausible at 3-4 week dedicated sprint. **No 1.0-required call is implausibly expensive.**

## 6 locked decisions for CEO ratification

1. **Surface 4 integration pick**: GitHub + Calendar + Notion; **defer Slack** (12,213 LOC would balloon to 8-10 days alone)
2. **Surface 7 audit-envelope read surface**: paired deliverables — ADR-NN (companion to ADR-061) + Surface 7 MUX doc
3. **Surface 2 privacy granularity**: per-conversation for 1.0; per-message deferred post-1.0
4. **Surface 1 sidebar reconciliation**: assign roles (left = continuation, right = archive), don't merge
5. **Surface 6 framing**: templated voice surface, NOT LLM-touch (Architect correction absorbed; Class A + Class C still apply; no four-element obligations at greeting composition layer)
6. **Total build estimate**: ~13-18 working days plus voice work in parallel; PDR-005 v0.3+ sequencing dependency before Surface 2 + Surface 4 lock

## Three sequencing dependencies for CEO visibility

1. **#1075 route-prefix migration** before Surface 4 OAuth wizard work (in-flight)
2. **PDR-005 v0.3+** sufficient resolution before Surface 2 + Surface 4 commitments lock (PPM cadence; my Round 1 review flags + Architect AC-1/AC-3 + Lead Dev build-cost validation all feed v0.3)
3. **Surface 1 reconciliation** before Surface 2 privacy UI

## Cohort-correction note worth elevating

The Round 2 absorbs an Architect Surface 6 LLM-touch correction (his Round 1 claim was wrong; Lead Dev's pre-read was right; Architect filed correction this morning). This was a Pattern-063-adjacent failure mode at code-trace scale — incomplete consumer-trace assertion that the cohort baked in for ~12 hours before Lead Dev's verification caught it.

Architect proposed a methodology note for CIO routing: *"LLM-touch claims require consumer trace to actual LLM call, not just upstream context-shape inspection."* I endorse the methodology framing. Routing to CIO at Architect's cadence.

The narrower point: **methodology-honest move is to flag the correction explicitly in Round 2**, which I've done. My Round 1 endorsement of the LLM-touch claim was wrong by extension. The cohort-iteration cadence working at high speed both produced and caught the error within hours — that's the system working as designed.

## Post-ratification triggers

CEO ratification → Phase 2 begins:
- **CXO + Comms voice work**: per-surface MUX doc drafting for 2/4/6/7 (voice clusters per Comms framing)
- **Lead Dev Phase 2 build** at PDR-005-sufficient-resolution
- **Architect**: ADR-NN (audit-envelope read-surface) + Surface 5 index ADR pre-1.0
- **CIO**: Pattern-063 frontend instance filing when Surface 1 reconciliation lands; consumer-trace methodology note absorption

## What this synthesis is NOT

- Not committing per-surface MUX doc content
- Not committing build sequencing within the 13-18 day window (Lead Dev determines post-ratification)
- Not committing ADR-NN slot allocation (CIO catalog-management lane)
- Not synthesizing PDR-005 implications beyond Surface 2/4 intersection (parallel CXO work; experience-section deliverable May 25 – Jun 1)
- Not calling a convergence-tension sync — cohort converged cleanly; only PM/CEO ratification needed

— CXO, 2026-05-15 (11:35 PT)
