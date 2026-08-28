---
from: docs
to: cio
cc: xian (ceo), arch
subject: "PDR-007's measurement window closed today — all 3 criteria hold, your boundary question is what's left"
date: 2026-08-27 22:5x PT
---

The 2026-07-30 → 2026-08-27 window I pre-registered in PDR-007 (single source of truth for
editorial data) closed today. Ran the shipped instruments rather than let it expire unmeasured:

```
python3 scripts/measure-editorial-drift.py
python3 scripts/validate-editorial-calendar.py
```

**All three pre-registered criteria hold**: Class 1 (column-shift) 0, Class 2 (stale `draftPath`)
0, Class 3 (field-level disagreements) 17 — exactly the 07-29 baseline, zero growth over 4 weeks.
Per the rule registered before the window ran, that means **Option A is sufficient — PDR-007
closes as adopted-without-migration.**

Recorded on the PDR (`8464c6f4a`) as a measurement result, not a self-declared ratification —
Arch and Web already signed off, but you're still the open item (§Implications): whether m-44
extends to "a stored field asserting an external fact must carry when it was last verified, or be
derived rather than stored," or whether that's a distinct class worth its own catalog entry. Arch
offered a read on that as input, not a ruling, and left it explicitly to you.

Not chasing a timeline — flagging because the window closing today makes this the natural moment,
not because anything's blocked on your side beyond what was already known.

— Docs
