---
from: host
to: arch
cc: lead, xian (ceo)
subject: "Usage-cap trust-lens — expose Retry-After yes; per-session interpretation confirmed; promote to ADR-076"
in-reply-to: memo-arch-to-host-lead-cc-pm-usage-cap-enforcement-design-2026-07-06.md
date: 2026-07-06
---

Arch — design reads clean. Trust-lens on the OQ and the interpretation flag:

## OQ — transparency of the cap: YES, expose Retry-After

**Expose Retry-After + a friendly reason. Yes. Arch's lean is correct.**

The transparency-when-gated principle (ADR-072 D5): when a user is blocked from access, silence is not neutral — it's trust-eroding. A rate-limited user who gets a bare 429 with no context cannot self-regulate. A concurrency-capped user who gets a silent hang doesn't know to try again in a moment.

What to expose, and how much:
- **Rate-limit (429)**: expose `Retry-After` (seconds until the window resets) + the friendly reason (`"Rate limit: 100 req/min. Retry in Ns."`). Do NOT expose remaining-quota-within-the-window — that's more precise than the user needs, and the information leaks internal window state without corresponding user benefit. `Retry-After` is enough to self-regulate.
- **Concurrency cap (429 or 503)**: expose the full picture — `"Instance at capacity (10/10 active sessions). Try again shortly."` — because the user needs to understand it's a *global* cap (not their own session's fault) and that it will resolve without their action. The number (10/10) here is welfare-protective, not a state leak: it tells the user this is a shared constraint.

The "not silent" spirit is satisfied by both. My one addition: the body should be machine-parseable (not just human-readable) — a JSON `{"error": "rate_limited", "retry_after_seconds": N}` pattern so future client integrations can handle it automatically. Same shape as ADR-070 D5's honest-failure body.

## Per-session interpretation: confirmed

Arch's read is correct: **per-session 100/min, NOT global.** The welfare rationale — one misconfigured session must not exhaust shared resources and silently degrade others — is served by per-session limiting. A global 100/min ceiling would give one bad session 100% of the budget; per-session caps means the worst case is one bad session consuming 10×1 = its own share. Combined with ≤10 concurrent, the implied instance ceiling of 1000/min is the right level for alpha.

## ADR-076: promote it

Yes, please promote to ADR-076. This has lasting architectural implications:
- The fail-closed posture (Redis outage → deny) has welfare and trust consequences that should be documented
- The per-session-vs-global interpretation question will come up again when concurrent-session semantics change
- The exempt-list family (auth-exempt → rate-exempt?) needs a durable record of what the exemption criteria are

The design memo + decisions.log can carry the immediate implementation; the ADR makes the reasoning available to future engineers who hit the same question.

Trust-lens: PASS. Lead, go when the ADR is ratified.

— HOST
