# ADR-076 — Usage-Cap Enforcement (Alpha Load Backstop)

**Status**: ACCEPTED (v0.1, 2026-07-06) — Arch-authored; HOST trust-lens PASS folded; **implemented** (#1370, `01c28848b`, 2026-07-06) — `web/middleware/usage_cap_middleware.py`, 12 unit tests, staging/live verification not yet done.
**Author**: Chief Architect (arch)
**Reviewers**: HOST (trust-lens — PASS, 2026-07-06), Lead Dev (builder), PM (thresholds ratified 2026-07-04 via HOST).
**Related**: ADR-070 D5 (honest-failure body), ADR-072 D5 (transparency-when-gated), ADR-075 D4 (honest-degradation), #1162/#1307 (gate-removal — this realizes its rate-limit recommendation), #1109 (in-process-vs-Redis shared-state lesson), #1344 (invite-gate — the *who-registers* boundary; this is the *how-much-load* boundary).

---

## Context

The June-29 Caddy perimeter removal (#1162/#1307) meant the alpha droplet lost its coarse external throttle. My gate-removal read named the replacement: rate-limiting must move to the app layer, fail-closed, Redis-backed. With the invite-gate (#1344) closing *who* can register, the remaining exposure is *how much load* the droplet absorbs — an unbounded or misbehaving caller can degrade the shared alpha instance for every tester. PM ratified alpha-appropriate thresholds (2026-07-04): **≤10 concurrent sessions, ≤100 req/min**. This ADR records the enforcement architecture so future engineers hitting the same "per-session vs global / fail-open vs fail-closed" questions have the reasoning, not just the code.

This is a **distinct concern from the invite-code (#1344)** and must not be conflated: invite-code = identity/authorization boundary (*who may register*); usage-cap = availability boundary (*how much total load*). Different failure modes, different layers.

## Decisions

**D1 — Two distinct mechanisms, not one.** Rate (≤100 req/min) and concurrency (≤10 sessions) are different limits with different state:
- **Rate limit** — a **per-principal, Redis-backed sliding-window / token-bucket** counter keyed on the resolved principal. Per-principal (see D3), NOT a single global counter.
- **Concurrency cap** — an **instance-wide Redis gauge of distinct active sessions**, TTL-expired so a dead/abandoned session releases its slot automatically (no leaked slots).

**D2 — Redis-backed shared state, never in-process.** Both counters live in Redis, incremented/checked atomically. This is the load-bearing constraint and the #1109 lesson: in-process per-worker counters don't see each other, so a per-worker cap of N silently becomes N×workers — the cap doesn't hold. A guarantee that isn't atomic across workers isn't a guarantee.

**D3 — Rate limit is PER-SESSION (per-principal), not global.** Welfare rationale: one misconfigured/runaway session must not exhaust a shared global budget and silently starve every other tester. Per-session 100/min means the worst case is one bad session consuming its own share, not everyone's. Combined with ≤10 concurrent, the implied instance ceiling is ~1000/min — the right level for closed alpha. (HOST confirmed this interpretation.)

**D4 — Placement: ASGI middleware after AuthMiddleware, fail-closed.** The limiter runs after auth (it needs the resolved principal to key the per-session counter) and before the handlers. **Fail-closed**: if Redis is unavailable, DENY (return the capacity error), do not fail-open to unbounded access. The welfare + trust cost of a silent fail-open (the cap silently stops existing) exceeds the availability cost of a brief conservative deny during a Redis outage.

**D5 — Fail VISIBLY (honest-degradation at the transport layer; HOST trust-lens).** Never a silent hang or a bare 429. Same principle as ADR-072 D5 / ADR-070 D5, applied at transport:
- **Rate-limit → HTTP 429** with `Retry-After: <seconds>` + a friendly reason (`"Rate limit: 100 req/min. Retry in Ns."`). Expose `Retry-After` (enough to self-regulate); do **not** expose remaining-quota-within-window — that leaks internal window state without user benefit (HOST).
- **Concurrency cap → 429 or 503** with the full picture (`"Instance at capacity (10/10 active sessions). Try again shortly."`). Here the `N/10` IS surfaced deliberately — it's welfare-protective, not a state leak: it tells the user this is a *global* shared constraint that resolves without their action, not their own fault.
- **Machine-parseable body** (HOST): a JSON `{"error": "rate_limited"|"at_capacity", "retry_after_seconds": N}` shape — same as ADR-070 D5's honest-failure body — so future client integrations (the MCPB, web UI) can handle it automatically, not just render a string.

**D6 — Exemptions are an explicit, justified allowlist (same discipline as #1308).** If any route is rate-exempt (e.g. health checks), it goes on an explicit justified allowlist, not an implicit skip — the auth-exempt-list lesson (#1307/#1308) applies to rate-exempt too: an exemption that isn't recorded is an attack/abuse surface. (No exemptions required at v0.1; naming the discipline forward, m-36.)

## Consequences

- Realizes the app-layer rate-limit the #1162/#1307 gate-removal read required; the perimeter-removal is now fully compensated at the app layer.
- Reuse candidate: `session_persistence.active_sessions` for the concurrency gauge (verified to exist) — Lead's call whether to extend it or add a dedicated Redis gauge.
- Thresholds are config (not hardcoded) so PM/HOST can retune for beta without a code change; the *shape* (per-session / Redis / fail-closed / fail-visible) is the durable architecture, the *numbers* are product.
- Fail-closed means a Redis outage degrades to "conservative deny with an honest message," not "unbounded access" — a deliberate availability-for-safety trade, documented here so it isn't mistaken for a bug.

## Open questions

None blocking. Beta will revisit thresholds + whether concurrency semantics change (per-user vs per-instance) when the shared-instance model evolves — that's the durable-record reason D3 exists.

---

*ADR-076 v0.1, Arch-authored 2026-07-06, HOST trust-lens PASS folded. Third in the alpha-security-boundary set with #1343 (billing) + #1344 (registration): billing-exposure closed, open-registration closed, now load-exposure capped — all app-layer, none load-bearing on the removed Caddy perimeter.*
