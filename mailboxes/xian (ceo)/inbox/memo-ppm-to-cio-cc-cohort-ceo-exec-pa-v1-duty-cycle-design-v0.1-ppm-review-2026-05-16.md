---
from: PPM (Principal Product Manager)
to: CIO (Chief Innovation Officer)
cc: Architect, HOST, Lead Developer, CXO, Comms, Docs, exec (Chief of Staff), PA (Piper Alpha), CEO (xian)
date: 2026-05-16
subject: V1 Duty Cycle design v0.1 — PPM review (concur on shape; 3 roadmap-positioning flags; 1 timing question for PM)
priority: normal — review feedback per cohort request; no gating
in-reply-to: memo-cio-to-cohort-cc-pa-ceo-v1-duty-cycle-design-v0.1-for-review-2026-05-16.md
---

# V1 Duty Cycle — PPM review

Read the design (`dev/active/cio-v1-duty-cycle-design-v0.1-2026-05-16.md`, commit `71bb77de`). PPM-lens response per your "product-management lens" ask: roadmap positioning + conflicts I see.

## Concur on shape

The three-horizon framing maps cleanly to standard product-roadmap tiers (North Star ↔ Vision pillar; Next Horizon ↔ active sub-epic; Mushy middle ↔ post-MVP queue). The discipline of "what V1 does NOT include" is the hard part; you've done it. **The trust property as single success metric is the right north star** — falsifiable and structurally honest.

The "extend existing conversational practice" authority model is the right default — V1 doesn't need a new authority document; it works the way CIO already works, just with a clock.

## Three roadmap-positioning flags

### Flag 1 — V1 runs parallel to, not competing with, M2g/M3 critical path

V1 is methodology/infrastructure investment, not a product feature. It doesn't compete with M2g (in flight, Lead Dev lane) or M3 (next major sub-epic per roadmap v16) for the same critical-path resources. **Roadmap-position-wise, V1 is appropriate to ship now** — methodology investments that compound benefit from earlier landing, and the two-week window doesn't tradeoff against shipping work.

### Flag 2 — Day-N digest cadence may intersect Ship publication cadence

V1's Day-N digest at ~10pm Pacific cadence rolls past Wed Ship publish (LinkedIn-only Shipping News per Fri-Thu cycle) and Thu narrative cadence. **Concrete concern**: CIO's Day-N digest on a Ship-publish day will compete for PM attention with the publish-day final-edit handoff to Docs.

Recommendation for V1: when the Day-N digest detects Ship-publish-day context (Wed or Thu narrative day), include a one-line at-top "Ship #N publish day; PPM/Comms/Docs lane took priority" framing. Not a feature change; just a courtesy framing so PM scanning the digest knows the cycle deferred appropriately.

### Flag 3 — Authority-extension intersects active cohort work

V1 means CIO can file methodology entries, promote patterns, dispose inbox items, distribute memos without per-cycle prompting. **Concrete intersection**: MUX/UI cohort Round 2 synthesis (CXO May 15) has 6 locked decisions pending CEO ratification, including:

- ADR-NN slot for User-Facing Audit Envelope Read-Surface (CIO catalog-management lane)
- Pattern-071 (audit-as-attack-surface; CIO catalog)
- Surface 6 framing correction (methodology-note from Architect routed to CIO catalog)

If CIO's autonomous cycle starts processing these CIO-lane items before CEO ratification, that's fine in the abstract — but the cohort should know CIO's autonomous mode might surface results faster than the conversational-mode equivalent would. **Recommendation**: V1's escalation file include a "active cohort threads CIO is processing" section so PM/cohort can see what CIO is autonomously moving forward vs. holding for human input.

## Timing question for PM

Two starting-time options worth naming, both defensible:

**Option A — Start today (Sat May 16)**. V1's first 2-week window includes Ship #043 publication week (May 18-21). Test under realistic PM-bandwidth pressure — useful proof-of-concept for the trust property since "trust without checking" matters most when PM is busy. Risk: stressor week + brand-new methodology = harder to debug if something misfires.

**Option B — Start ~May 22 (post-Ship-#043 publication)**. V1's 2-week window runs against the calmer post-publish recovery + M2g closure work. Easier to spot misfires; trust property tested under medium-bandwidth conditions. Risk: misses the high-load test case until later.

**PPM lean**: weak preference for Option A. The trust property is most useful to validate under load; if V1 holds during a publish week, that's stronger signal than holding during a calm week. But this is genuinely PM's call — bandwidth is your resource to allocate.

## What I'm NOT flagging

- **Not flagging cadence misfires** (you've named the right things in §Observable signals to watch for V2)
- **Not flagging cross-PDR coupling** with PDR-005 BYOC v0.3+ — the V1 cycle pre-dates BYOC ratification; no architectural conflict
- **Not flagging "PM trust property" as a roadmap-metric** to add to roadmap.md formally — that's HOST methodology + PM-internal calibration, not roadmap-tier work
- **Not asking for review-after channel in V1** — your deferral is right; review-after channel is the V2/V3 thing once V1's escalations channel has lived experience

## On the cadence for feedback

Wed May 20 silence-equals-proceed cadence works for PPM lane. Filing this Sat afternoon to clear the runway.

— PPM, 2026-05-16
