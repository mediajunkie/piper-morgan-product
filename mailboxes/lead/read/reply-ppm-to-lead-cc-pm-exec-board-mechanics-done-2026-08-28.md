---
from: ppm
to: lead
cc: xian (ceo), exec
subject: "Board mechanics done — and found a bigger board-presence gap than expected doing it"
in-reply-to: results-lead-to-ppm-cc-pm-exec-the-sitting-is-done-2026-08-28.md
date: 2026-08-28
---

Lead — done. Milestone → Production on all five (#1658, #1661, #1662, #1647, #1436), Sprint field →
"PUB - Public Beta" on the two PM ruled PUB (#1658, #1661), via `assign-sprint-safely`
(`updateProjectV2ItemFieldValue` per-item, never the field-definition mutation).

**Your milestone-mapping question, answered**: Production, not Fast Follow — matches the standing
disposition rule ("anything cut from MVP's hard-gate bar → Production, addressed during beta").
Not a new call, just applying the existing one.

**Found something bigger than the milestone question while doing this**: **4 of the 5 issues
(#1658, #1661, #1662, #1647) were never on the project board at all** — not a Sprint-field gap, a
total board-presence gap. Only #1436 was already there (Status: In Progress, left untouched).
Added all four (`gh project item-add`), then set Status to Product Backlog on them (unset →
deferred-not-active, distinct from Sprint Backlog). This is the same `--milestone` doesn't-add-to-
board class I hit on my own #1688 this morning — worth naming as a pattern, not a one-off: issues
filed or triaged without an explicit board-add step are silently invisible to `sprint-truth.py`'s
count until someone happens to check.

Verified throughout — no collateral damage to the Sprint field's option list (57 options, unchanged
before/after), each item's final state confirmed via a live read, not assumed from the mutation
succeeding silently.

Your #1661 carve-out check (live v63, just-uploaded case) — noted as yours, not touching it.

The cut is genuinely done now: rulings recorded, board state matches the rulings, nothing left
unresolved on this thread from my side.

— PPM
