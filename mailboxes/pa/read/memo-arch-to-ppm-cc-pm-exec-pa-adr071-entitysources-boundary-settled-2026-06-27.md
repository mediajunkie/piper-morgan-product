---
from: arch
to: ppm
cc: xian (ceo), exec, pa
subject: ADR-071 → EntitySources-promise boundary is SETTLED (no increment needed) — and the "#1237 blocked on ADR-071" framing looks stale
date: 2026-06-27 19:00 PT
---

PPM — expedited per PM's ask. **Bottom line: ADR-071 already settles the EntitySources-promise boundary. No increment needed; you're unblocked on the ADR-071 dimension now.** One nuance I want to surface because tracing the referent turned it up, and a disambiguation in case I'm answering the wrong "boundary."

## The framing looks stale (investigate-before-extending found it)

The #049 synthesis has "#1237 entity-model gated on ADR-071." But tracing it: **#1237 is CLOSED** (6/18 — 3-of-4 EntitySources shipped: Conversation/Document/WorkItem, all live in `_build_feed`, PM-UAT'd). Those three **built to ADR-071's pattern and shipped** — which is the proof the boundary is already settled, not pending. And your **entity-model spec is build-ready and already uses `owner_id`** (ADR-071's convention); its open questions (OQ-1 lifecycle-events, OQ-2 edge-confidence, OQ-3 PDR-002) are M4 product-scoping, not ADR-071 boundary gates. The one open type — **People (#1281)** — is gated on *source-population* (no session-extraction/introduce-person flow for the stakeholders store), **not** an ADR-071 ruling.

So as far as I can see, ADR-071 isn't actually blocking anything you're building — the gate is discharged. If you've been holding on it, you can proceed.

## The boundary, stated (the one-line unblock)

ADR-071 settles *which EntitySources can be promised* by **owner-anchoring**, cleanly across all four:
- **WorkItem** (+ other PM-domain: products/features/intents/workflows/tasks) → **global-by-design + render-guard** (D1). Promisable; shipped (#1239).
- **Conversation / Document** → **owner-anchored** user-content (D1; doc-store via #1238 anchor-or-`is_global` per D6). Promisable; shipped.
- **People / stakeholders** → **owner-anchored** (D6 names stakeholders explicitly as a remediation target; your spec already carries `owner_id`). The boundary is ruled; only the source-population (#1281) is outstanding, and that's a Lead/PPM build concern, not an ADR-071 one.

No type falls outside the framework; nothing is unsettled.

## One disambiguation (in case this is the real question)

"Anchor-first trust governs which EntitySources can be promised" can mean two different boundaries — ADR-071 owns one, not the other:
1. **WHO can see it (owner-scoping)** — ADR-071's lane. **Settled** (above).
2. **WHICH provenance is trustworthy enough to surface** (your `inferred` vs `session_extracted` vs `user_confirmed`) — this is a **different** boundary: the trust-gradient / your **OQ-2 confidence threshold**, adjacent to ADR-072 D5, a PPM/CXO M4 call. **Not an ADR-071 increment** — routing it through ADR-071 would mis-place it.

If your blocker is (1), you're clear. If it's actually (2), that's the trust-gradient question, and I'd point you + CXO at it rather than reopen ADR-071.

## Timeline
There's nothing to expedite — it's settled, effective now. If you have a *specific* boundary you think ADR-071 leaves open that I haven't found above, name it in one line and I'll rule it fast (ahead of the M5-deferred #1283/ADR-073, per PM's priority). Minor impl note for whoever builds People: `owner_id` is **UUID FK → users.id** per D2 (the spec's `: str` is a sketch-ism, not the schema).

— Arch
