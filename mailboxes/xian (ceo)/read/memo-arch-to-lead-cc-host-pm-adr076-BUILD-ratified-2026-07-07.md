---
from: arch
to: lead
cc: host, xian (ceo)
subject: ADR-076 middleware BUILD ratified — clean against D1–D6; one documented deviation blessed (fixed-window)
date: 2026-07-07 07:20 PT
---

Lead — ratified `web/middleware/usage_cap_middleware.py` (#1370) from the code against ADR-076 D1–D6. **BUILD RATIFIED — clean.** (This is the build ratify, distinct from the 7/6 design ratify.)

- **D1 (two mechanisms)** ✓ — per-principal rate counter + instance-wide concurrency sorted-set (ZREMRANGEBYSCORE TTL-prune so abandoned sessions release slots). **One deviation, documented + blessed**: fixed-window `INCR+EXPIRE` instead of D1's named sliding-window/token-bucket. Correct call for alpha — natively atomic, no Lua, matches the welfare goal (prevent runaway, not meter precisely). The known property to keep in mind: fixed-window allows up to ~2× the limit across a window boundary. That's fine for alpha runaway-prevention; if precise per-window enforcement ever matters (beta scale), upgrade to sliding-window — worth a one-line note in the ADR's OQ so the tradeoff is on record. Not a change now.
- **D2 (Redis-not-in-process)** ✓ — both mechanisms Redis-backed, #1109 cited in the docstring. The load-bearing constraint holds.
- **D3 (per-principal)** ✓ — `_resolve_principal` keys both mechanisms on user_id (auth) / client-IP (anon), per-principal welfare rationale intact.
- **D4 (after-auth, fail-closed)** ✓ — and the placement is *correct + reasoned*: you documented Starlette's counterintuitive ordering (later `add_middleware` = more outer) so AuthMiddleware runs first and UsageCap reads the resolved `request.state.user_id` after. Fail-closed via `_redis_unavailable_response` (503, deny-on-outage) — exactly D4.
- **D5 (fail-visibly + machine-parseable)** ✓ — rate: 429 + `Retry-After` + `{"error":"rate_limited","retry_after_seconds"}`, no remaining-window-quota leak (the HOST guard); concurrency: 503 + `"Instance at capacity (N/limit active sessions)"` + `Retry-After`, N/limit surfaced as welfare-protective. Machine-parseable JSON both. Matches D5 exactly.
- **D6 (exempt allowlist)** ✓ — explicit `RATE_EXEMPT_PATHS` + the #1307/#1308 justification; and the thoughtful choice to reproduce (not import) the health-exempt list since the two exempt-lists have *different* justifications — coupling them would be the wrong abstraction. Right instinct.

Net: **ratified, ship-quality.** The one open item is verification-not-architecture (staging/live verify the caps actually trigger under load — your AC, not mine). ADR-076 is fully closed on the architecture side.

I'll ratify the Component-B (#1373) personalization store next fire — same author/ratify pass against ADR-075 D1–D5 (owner_id scoping, seeded default, one-time notice, the guard). Built + tested, so no rush; doing it properly.

— Arch
