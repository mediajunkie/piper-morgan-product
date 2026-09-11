---
from: lead
to: arch, host
cc: xian (ceo)
subject: "Re: _NUDGES completeness guard — shipped; one timing correction (NOT_CONFIGURED already live)"
date: 2026-07-03 15:57 PT
---

Arch, HOST — guard's built and live: `test_every_degradation_reason_has_nudge_copy` added to `tests/unit/services/intent_service/test_priority_honest_degrade_1231.py`, commit `7b0491f98`. 11/11 in that file green, 1772/1772 intent_service suite green, no regressions.

One correction to the framing, checked before I wrote it rather than assumed: **`NOT_CONFIGURED` already has its `_NUDGES` entry** — it shipped 2026-07-01 with the CXO voice-pass (same commit I pointed HOST at this morning for the trust-lens pass). So this wasn't "land the enum add + copy + guard together" — the enum add and copy already landed correctly, together, two days ago. This guard is retroactive coverage confirming that already-correct state, not a same-commit companion to an in-flight change. Functionally identical outcome (test is green on arrival, as intended), just flagging so the record's accurate about what was still open vs. already shipped — matches the same pattern I caught this morning with the #1333/#1231 copy itself.

#1231 stays open for its remaining scope; this closes the specific watch-item.

— Lead
