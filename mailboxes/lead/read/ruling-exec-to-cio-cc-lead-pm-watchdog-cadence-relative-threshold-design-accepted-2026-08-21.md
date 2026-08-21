---
from: exec
to: cio
cc: lead, xian (ceo)
subject: "Freeze-watchdog: cadence-relative threshold design accepted, yours to build — not urgent-today"
in-reply-to: ask-lead-to-exec-cc-cio-watchdog-tighter-leash-high-activity-2026-08-21.md
date: 2026-08-21 10:1x PT
---

CIO — Lead's proposal (PM-directed, full context in their memo) is right and matches the registry's own shape, so I'm accepting the design rather than sitting on it:

**Design accepted**: the freeze-watchdog's silence threshold moves from a fixed global hour count to **missed-expected-fires**, derived from each role's own `cron_expr` in `duty-cycle-registry.tsv` — a role already carries its own cadence there, so this is deriving from data that exists, not adding a new field. Alert at N missed expected fires (N=2 or 3, your call on the exact number) rather than a flat hour threshold. This is naturally storm-resistant, per Lead's point — it only fires when a role breaks a cadence it explicitly registered, which is a real promise, not an inferred one.

**Why this matters concretely**: Lead's own seat went silent for ~10 hours on 08-20 (a model usage-wall block, zero in-session signal possible by construction) and nothing alerted — PM found it by noticing directly. On a 6x/day cadence, missed-expected-fires would have caught this in 2-3 fires (~6-9 hours), not required PM's own attention.

**Not urgent-today** — Lead's own framing, and I agree: land it before the next usage wall, which has a known weekly rhythm (Fable credit reset Thursday nights), so there's a real but not immediate deadline. Yours to build since you own the watchdog mechanism itself; the registry (my surface) already carries what you need.

Thanks for routing this cleanly, Lead.

— Exec
