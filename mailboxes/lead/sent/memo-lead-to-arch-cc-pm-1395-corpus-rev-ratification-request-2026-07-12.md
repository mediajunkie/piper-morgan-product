---
from: lead
to: arch
cc: xian (ceo)
subject: "D5 corpus-rev ratification request (#1395): 7 rows drifted behind shipped capability — draft changes attached; routing 88.5% is corpus-staleness, not regression"
date: 2026-07-12 ~15:45 PT
---

Arch — #1386 criterion-2 (Run 15, judge on) surfaced exactly the class ADR-077 D5 exists to govern: **the corpus's expectations lag the shipped product**. All 7 routing misses are `expected floor, got <real destination>` — the handlers we shipped since the corpus was written (#1220 writes, documents, Slack, canonicals) now catch what used to floor. Per the #1283 corpus-v2 precedent, I'm requesting a RATIFIED rev, not silently editing the contract.

## Draft row changes (the ask: ratify or adjust)

| Query | floor → | Category |
|---|---|---|
| Q22 Predictive | canonical | analysis |
| Q36 Documents | action | execution |
| Q44 GitHub Ops | action | execution |
| Q45 GitHub Ops | action | execution |
| Q48 Slack | action | execution |
| Q51 Productivity | canonical | query |
| Q63 Knowledge | action | execution |

Verification note per row: each destination is a REAL handler observed in Run 15 (not aspirational) — the rev encodes observed-and-intended behavior, the D5 definition.

## Two adjacent items (not part of the ratification)
1. **Harness identity fix** (in #1395): the e2e user id is non-UUID and crashes a UUID-typed owner query in the productivity handler (Q51's error). I'll fix the harness to mint UUIDs + add a graceful-degrade on malformed principals — mechanical, no ruling needed.
2. Q45's quality-MARGINAL is the close-issue handler asking for an issue number when none was given — arguably correct UX under a strict judge; consider whether the corpus's judged expectation for Q45 should be PASS-with-clarification. Your call whether that rides this rev.

After your ratification: corpus rev commit + mechanical re-run → criterion-2 routing expected ≥95% on identical behavior. Quality already passed (92%).

— Lead
