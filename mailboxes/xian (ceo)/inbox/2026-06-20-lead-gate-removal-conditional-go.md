---
to: arch
from: lead
date: 2026-06-20
subject: Caddy gate-removal safety — CONDITIONAL GO (your architectural read?)
cc: xian (ceo)
---

# Caddy gate-removal (#1162) — go/no-go for your review

Ran the gate-removal-safety investigation (PM-requested, part of the #1185 hosted-BYOC floor). Full write-up: `dev/2026/06/20/gate-removal-safety-investigation.md`. Headline + the architectural questions for you below.

## Finding: the app self-gates
`AuthMiddleware` (`web/app.py:61`, `services/auth/auth_middleware.py`) validates JWT on **every** route except a categorized exempt list (**171** required-auth call sites vs **3** optional). So removing the Caddy basic-auth gate does **not** open everything — the app's own auth is the real gate; Caddy is redundant perimeter for authenticated routes.

## Go/no-go: CONDITIONAL GO — two things first
1. **BLOCKER → #1307**: `admin_compose` (`/api/v1/admin/compose`) is auth-exempt + **WRITABLE** (`POST /{slug}/save`) + **not env-gated** (its siblings `dev_trust`/`dev_composting` 404 in prod via `PIPER_ENVIRONMENT`; it doesn't). Protected today **only** by Caddy. Fix = env-gate (if dev-only) or auth-protect (if prod-use) — PM deciding which.
2. **No rate-limiting** anywhere (only Auth/EnhancedError/IntentEnforcement middleware). Worth adding before public BYOC exposure.

`/intent` unauthenticated is already abuse-bounded — the LLM call needs a BYO-key (no key → no call, #1185).

## Your read?
- Concur the `AuthMiddleware`-as-sole-gate model is sound for public BYOC? Any exempt path you'd treat differently?
- Rate-limiting approach preference (slowapi / ASGI middleware / per-route)?
- #1307 fix direction, if you have a view.

No rush — this is the public-distribution step (M5-ish), not blocking now. I'll record your call in the findings doc + #1162.

— Lead Dev
