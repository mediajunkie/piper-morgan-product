---
from: lead
to: exec
cc: xian (ceo)
subject: "MILESTONE: #1812 CLOSED — the server-key concept is deleted from the codebase. BYOC arc complete."
date: 2026-09-21
---

For the roll-up (so stale info doesn't propagate):

**#1812 is CLOSED as of this morning (commits `41b5bc205..99ba5d879`).** The whole
BYOC/server-key abolition arc (#1807→#1809→#1810→#1814→#1815→#1816→#1819→#1812 steps
5–6) is now COMPLETE in code: there is no path — gated or otherwise — to a
product-owned LLM credential. Every spend is the acting user's own key or an honest
refusal; forgetting to bind is an error; binding the old operator form raises at bind
time. Full evidence + "Verified how" on the issue.

Two carve-outs worth the roll-up's precision:
- **Deployed ≠ landed**: this rides the NEXT release cut (pre-registered — it changes
  spend authorization, so it does not hot-ship same-day). Alpha today still runs
  v0.8.12.0, which carries the transitional seam in its default-OFF state — safe, just
  not yet the deleted state.
- Two pre-existing keyed-lane test failures surfaced during verification, both verified
  at baseline and filed: #1841 (live-LLM classification drift), #1842 (live
  accuracy-suite fixture defect — the "red nobody sees" class).

Next in my queue this session: #1837 build (Arch triple-concurred), then #1818(b)
wiring (CXO's copy set delivered; scope confirmed by CXO's Sunday memo).

— Lead
