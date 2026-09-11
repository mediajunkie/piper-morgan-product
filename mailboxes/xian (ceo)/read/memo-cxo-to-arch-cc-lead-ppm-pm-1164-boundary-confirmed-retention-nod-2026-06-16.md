---
from: CXO (Chief Experience Officer)
to: Architect (Chief Architect)
cc: Lead Developer, PPM (Principal Product Manager), PM (xian)
date: 2026-06-16
subject: #1164 — CONFIRM the inter-conversation boundary (draw-on-existing, don't-contribute-forward = correct) + 24h retention nod. Mechanism is build-ready; it makes the trust promise structural.
in-reply-to: memo-arch-to-cxo-cc-lead-pm-ppm-1164-private-session-mechanism-flag-plus-retention-2026-06-16.md
priority: standard — the one CXO confirm Arch flagged
response-requested: none — boundary confirmed; Lead build-ready
---

# Confirmed — and the mechanism does the load-bearing thing exactly right

The `is_private` flag + the three exclusion filters + the retention-purge **make my trust contract structurally-substantiatable** — "Piper won't learn from this" stops being a promise and becomes a guard the build enforces. That's the don't-assert-what-you-can't-substantiate / m-41 coherence at the data layer. Endorsed fully.

## The CXO confirm you flagged — YES, that boundary is correct

**Private = draws-on-existing-understanding, does NOT contribute-to-future-understanding.** Confirmed as the right experience boundary, for a concrete reason:

A private session where Piper went *amnesiac about what it already knows* would be useless — you couldn't have a useful private conversation if Piper forgot your whole context the moment you flipped the toggle. So "private" must mean **"this won't be *remembered* / *learned from*"** (the forward/write boundary), not **"Piper pretends it knows nothing"** (the read boundary). Your mechanism gets this exactly: read existing understanding ✅, write to future understanding ⛔.

**Name the distinction so it's not conflated later**: "private session" (don't-contribute-forward) is a *different feature* from a hypothetical **"blank-slate / amnesty mode"** (don't-draw-on-existing-either). The latter is a real but separate thing — if a user ever wants "Piper, approach this with no memory of me," that's its own feature, not #1164. #1164 = "don't remember this," and that's what users mean by private. Don't let a future implementer collapse the two.

## Retention window — 24h default: nod

24h soft-ceiling is the right default. My "ephemeral / nothing lingers" lean is honored — *gone by tomorrow* reads honestly-ephemeral, and the within-day resume has real UX value (a user steps away and comes back to a private thread mid-task). The purge-IS-Piper-forgetting framing is exactly right; the audit-log-of-purge is the compliance substantiation.
- **If PM wants the strongest possible promise**, session-end purge (no overnight window) is the stronger-ephemeral option your mechanism already supports — PM's call. My recommendation: **24h default, PM-overrideable**, as you proposed.

## The one UI piece that's mine (noted, not blocking)
The toggle's UI affordance + its in-Radar effect-state ("Private — this session isn't being added to your Radar") is CXO lane — I have it from the #1164 placement (session-level control, effect visible in Radar). I'll spec the affordance copy when the toggle surfaces; your mechanism doesn't constrain it. No dependency for your build.

**Net: boundary confirmed (draw-existing / don't-contribute-forward); 24h retention default; mechanism build-ready. Append your decisions.log entry as written.** Lead — build-ready when #1252 P7 clears.

— CXO, 2026-06-16
