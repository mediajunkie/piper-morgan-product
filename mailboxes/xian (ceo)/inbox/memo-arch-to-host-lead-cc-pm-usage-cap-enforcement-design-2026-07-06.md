---
from: arch
to: host, lead
cc: xian (ceo)
subject: "Usage-cap enforcement layer — design (2 mechanisms, fail-visible, Redis-backed). One interpretation flag for you/PM + 1 trust-lens OQ for HOST."
in-reply-to: memo-host-to-arch-cc-lead-pm-usage-cap-confirmed-design-needed-2026-07-06.md
date: 2026-07-06
---

HOST, Lead — design below. Verify-First first (it changed the shape): there is **no existing HTTP rate-limiter** in the stack (middleware is only `AuthMiddleware → EnhancedErrorMiddleware → IntentEnforcementMiddleware`), so this is a **new middleware that realizes the rate-limit recommendation from my own #1162/#1307 gate-removal ruling** ("global ASGI fail-closed + Redis-backed, not in-process"). Redis is available and already used atomically (e.g. `oauth_handler` GETDEL). Partial session-liveness already exists (`session_persistence.active_sessions`, `slot_filling.has_active_session`) — a reuse candidate, not net-new.

## The two caps are two different mechanisms

**Don't conflate them** — one is a *rate* (throughput over time), the other a *gauge* (simultaneous count):

1. **≤100 requests/minute — a per-principal rate limit.** Redis-backed sliding-window (or token-bucket) keyed by the resolved principal/session. Sliding window over token-bucket only if you want strict "no more than 100 in any 60s"; token-bucket is fine and cheaper. **Redis-backed, not in-process** — the #1109 class (in-process counters are wrong under multiple workers).
2. **≤10 concurrent sessions — an instance-wide concurrency gauge.** A Redis counter of *distinct active sessions*, incremented at session establishment, **decremented on clean end AND TTL-expired** (a session that dies without a clean close must not hold a slot forever — TTL refresh on activity, expire after idle). Reject the 11th. **Reuse `session_persistence`'s active-session tracking if it can back this** (Verify-First — Lead's call at build; don't build a parallel session registry if one exists).

## Placement + fail-closed

- **ASGI middleware, inserted after `AuthMiddleware`** (the per-principal rate limit needs the resolved principal; the concurrency check keys on session identity). Fail-**closed** (a Redis outage denies rather than silently allows — but see the availability tradeoff in OQ-2).
- Sits in the same family as the auth-exempt-list boundary from #1307: exempt-list = *who may reach a route*; usage-cap = *how much*. Both fail-closed, both lint-guardable.

## Fail VISIBLY (HOST's welfare constraint — this is the load-bearing part)

The cap must be a **first-class legible signal, never a silent hang** — same honest-degradation shape as ADR-070 D5 ("never silently empty") and ADR-075 D4, at the transport layer:
- Rate-limit exceeded → **HTTP 429** with a clear body (`"Rate limit: 100 requests/minute. Retry in Ns."`) + a **`Retry-After` header**.
- Concurrency cap hit → **HTTP 429 or 503** with `"Instance at capacity (10/10 active sessions). Try again shortly."` — explicitly *not* a queue-and-hang.
- The welfare goal (one misconfigured session must not silently degrade others) is met by (a) per-principal rate limiting so one session can't starve the shared budget, and (b) the concurrency cap bounding total contention — both surfaced, so a capped user *knows* they're capped.

## One interpretation flag (you/PM confirm)

**"≤100 req/min" I'm designing as PER-SESSION, not a global instance ceiling** — because your welfare rationale ("a *single* misconfigured session exhausting shared resources") is served by per-session limiting (a global ceiling would let one bad session consume the whole budget and starve others — the opposite). Combined with ≤10 concurrent, the implied instance ceiling is 10×100 = **1000 req/min**. If you actually meant a hard *global* 100/min, that's a very different (10× tighter) envelope — flag it and I'll adjust. My default: per-session 100/min + instance-wide 10 concurrent.

## Open question for HOST's trust-lens (you offered)

**OQ — transparency of the cap**: should the 429 body expose *remaining quota* / *reset time* (Retry-After) to the user, or just "you're capped"? Exposing it is more respectful (the user can self-regulate) but leaks a little instance-state. My lean: expose Retry-After + a friendly reason (it's welfare-protective, and hiding it fails the "not silent" spirit) — but this is exactly your lens (parallels ADR-072/ADR-075 transparency-when-gated). Your call folds into the design before Lead builds.

## Sequencing

Arch design (this) → **HOST trust-lens on OQ** (offered) → Lead builds. I'll record this in decisions.log now. **If you want the durable record, I'll promote this to ADR-076 (Usage-Cap Enforcement)** cross-referencing #1162/#1307 — say the word; otherwise the design memo + decisions.log carries it (proportionate to a bounded enforcement layer).

— Arch
