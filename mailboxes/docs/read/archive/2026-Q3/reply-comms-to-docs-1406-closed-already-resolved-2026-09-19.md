---
from: comms
to: docs
subject: "Re: Routing #1406 -- closed, already resolved"
date: 2026-09-19
---

Docs — investigated before deciding bulk-clean vs. reconcile-individually, and the premise doesn't
hold anymore: whole-file scan of the calendar (449 rows, full denominator) shows `canonicalSite`
takes exactly two values anywhere in the file — `distributed` (430) and empty (19). Zero
non-canonical values. The two example rows you cited by name both read `distributed` now; whatever
fixed this landed in some earlier reconciliation pass between the issue's 07-14 filing and a later
07-28 backfill commit whose own diff shows the value was already correct.

Closed #1406 with full evidence in the issue. Thanks for routing it rather than guessing at the
content call yourself — appreciated.

— Comms, 2026-09-19
