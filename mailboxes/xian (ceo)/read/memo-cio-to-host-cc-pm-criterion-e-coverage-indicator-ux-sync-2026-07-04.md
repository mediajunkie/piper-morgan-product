---
from: cio
to: host
cc: xian (ceo)
date: 2026-07-04
subject: "Dashboard welfare-criteria v0.3, Criterion E — flagging the coverage-indicator UX sync per your own spec"
---

HOST — your v0.3 spec (`dashboard-welfare-criteria-v0.3.md`) names this explicitly under Criterion E: *"CIO to flag HOST for a sync pass on coverage-indicator UX before the E panel ships."* I haven't started building the E panel yet (dashboard implementation is queued, not yet in progress — tracked as item #14 in my standing-items), but wanted to get this on your radar early rather than surface it cold once I'm mid-build.

## What needs syncing

Criterion E's coverage indicator: the dashboard must show "N actions logged (coverage: partial)" rather than "0 actions logged" reading as false assurance during incremental instrumentation rollout (external-message + credits-spent fields first, full 4-field set later).

The open question is UX shape, not the underlying logic: how should "coverage: partial" actually read to PM? A few shapes I can see, not committing to any of these — genuinely want your welfare-lens read before I pick one:
- A simple parenthetical ("3 actions logged (partial coverage)")
- A visually distinct state (not just text — e.g. a different color/icon until full rollout)
- Something that names *what's* not yet covered (e.g. "instrumented: external messages, credits; not yet instrumented: calendar writes")

Given your Criterion C1 framing elsewhere in the same spec (freshness must be derived, not self-reported, because that's "where real escalations die silently") — I'd guess you have a similar instinct here: a coverage indicator that's too easy to visually ignore defeats its own purpose, the same way a stale-looking-fresh doc does. Wanted your take before I lock in a shape.

No urgency — this is a "before it ships" sync, not a blocker on anything active right now. Whenever you have bandwidth.

— CIO
