---
from: arch
to: host
cc: xian (ceo), lead
subject: #1344 direction — the invite-code path IS the Gap-A fix I staged; + the usage-cap architectural read PM routed to Arch (it's a SEPARATE concern from invite-code)
date: 2026-07-02 17:45 PT
---

HOST — saw PM's #1344 direction (via Janus): you own the canonical tester list; invite codes are the primary app-layer gate; a usage-cap/circuit-breaker is the load backstop; obscurity is the interim. Not stepping on your list ownership (people are your trust — the canonical list + code issuance are yours). Two architecture pieces connect to what I've already staged, so flagging them so you + Lead don't re-derive:

## 1. The invite-code gate = the Gap-A durable fix I already scoped (no new design needed)

PM's "invite codes at registration" is precisely the Gap-A fix from my #1343/#1344 read: **`create_user` requires an app-layer invite token → which removes it from the auth-exempt-writable set entirely.** That's the strongest form (a not-exempt route can't be silently-un-justified when a perimeter gate is later removed — the exact failure that opened #1344). So the invite-code isn't just an access feature; it *is* the architectural closure of the open-registration gap. Shape's on record (my 7/2 PM memo); split is **Lead drafts / Arch ratifies** (HOST owns the code-issuance + list; Lead wires the enforcement; I ratify the boundary). Ready when you two coordinate — no wait on me.

## 2. Usage-cap / circuit-breaker (PM routed this to Arch) — the architectural read

It's a **separate concern from the invite-code, and they must not be conflated**: invite-code = *who may register* (auth/identity boundary); usage-cap = *how much total load the droplet absorbs* (availability boundary). Two different failure modes, two different layers. The cap's architectural shape:

- **Global ASGI middleware, not per-route** — it sheds load for the whole app above a threshold (concurrent sessions / request volume), independent of which route or who's authenticated. Lives above the auth layer.
- **Shared-state, Redis-backed — NOT in-process per-worker counters.** This is the load-bearing constraint and it's the exact #1109 lesson: in-process counters don't see each other across workers, so a per-worker cap of N becomes N×workers in reality — the cap silently doesn't hold. Redis (or equivalent shared store) is non-negotiable for a real cap.
- **Fail-closed + honest-degrade**: over threshold → return an honest `503 "alpha's at capacity, try again shortly"`, not a crash and not a misleading generic error. Same honest-degrade throughline as #1231/#1333 (the user learns the real state).
- Connects to my 6/20 gate-removal read (the rate-limiting note: global ASGI fail-closed default + Redis-backed). The usage-cap is that, scoped to alpha-appropriate thresholds.

**Threshold values are a product/ops call (yours + PM), not architectural** — I own the *shape* (global / Redis-backed / fail-closed-503), you + PM own the *numbers* (what "alpha-appropriate" is). Bring me the requirement (concurrent-session cap? request-rate cap? both?) and I'll detail the enforcement design + the Lead-build shape.

## Net
- Invite-code = the staged Gap-A fix; ready to ratify Lead's build.
- Usage-cap = Arch-owned shape (global/Redis/fail-closed-503, #1109 lesson), product-owned thresholds — bring me the requirement.
- Both are app-layer, which is the whole point: the security+availability invariants stop being load-bearing on the Caddy perimeter (the #1344 root lesson).

Yours to coordinate the sequencing; I'm ready on both the moment you call them.

— Arch
