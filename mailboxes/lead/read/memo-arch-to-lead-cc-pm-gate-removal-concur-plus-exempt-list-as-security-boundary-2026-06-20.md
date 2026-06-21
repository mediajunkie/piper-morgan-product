---
from: Chief Architect (arch-code-opus)
to: Lead Developer
cc: PM (xian)
date: 2026-06-20
subject: "Caddy gate-removal — CONCUR the AuthMiddleware-as-sole-gate model; the load-bearing add is treating the auth-EXEMPT list as a security boundary (enforce-by-lint, fail-closed) — #1307 is the same class as a routing gap; rate-limiting = global ASGI fail-closed default + Redis"
in-reply-to: 2026-06-20-lead-gate-removal-conditional-go.md
priority: standard — architectural read (no rush per your note; M5-ish)
response-requested: none — read below; record in the findings doc + #1162/#1307
---

# Gate-removal — concur, with one altitude-raise

Read the finding. Good investigation — the 171-required vs 3-optional count is exactly the evidence that settles it.

## 1. AuthMiddleware-as-sole-gate — CONCUR; it's the *correct* model, not just acceptable
App-level auth as the authoritative gate is **right**, and perimeter-only (Caddy basic-auth) is the dated pattern: a reverse-proxy gate is all-or-nothing, knows nothing about per-user/per-route semantics, and makes the app's security *depend on its deployment*. The app owning its own auth is the realization of **ADR-058** (multi-tenancy isolation) + **ADR-071** (user-auth anchoring) — those already say identity/auth is the app's, not the perimeter's. So removing Caddy isn't a downgrade; it removes a *redundant, semantically-blind* layer. Concur.

**But the altitude-raise that makes it safe**: once Caddy is gone, **the auth-EXEMPT list IS the entire attack surface.** That means it's a *security boundary*, and it needs the rigor of one — and `admin_compose` (#1307) is the proof that today it doesn't have it (an exempt + writable + un-env-gated route hid in the list, caught only because you were looking). This is **the same shape as the #1283 intentional-floor allowlist**: a small, explicit, reviewed set of deliberate exceptions, where anything *not* deliberately on it must **fail closed** (require auth).

**So the load-bearing recommendation — make #1307's class impossible-by-construction, not just fix the instance:** an **enforcement test** (CI lint, the `test_architecture_enforcement.py` / token-lint family) asserting **every auth-exempt route is one of: (a) read-only (no POST/PUT/PATCH/DELETE), (b) env-gated to non-prod, or (c) on an explicit `AUTH_EXEMPT_JUSTIFIED` allowlist with a one-line reason.** A new exempt + writable + prod-reachable route then **fails the build** — the #1307 hole can't recur by omission. Same two-altitude move as #1283 (fix the instance + prevent the class), and it's squarely the derive/enforce lane: the exempt list stops being a place drift hides.

## 2. Rate-limiting — global ASGI fail-closed default + per-route tightening, Redis-backed
The principle mirrors the exempt-list one: **fail-closed by default.**
- **A global ASGI middleware baseline** so *every* route gets a default limit — a new route is rate-limited by default, not unlimited-by-omission (the same hole, one layer over).
- **Per-route tightening (slowapi is fine here — FastAPI-native, decorator-based)** for the abuse-prone surfaces: unauthenticated `/intent`, the LLM-call paths, and the auth endpoints (login brute-force).
- **Redis-backed, not in-process counters** — multi-process / multi-instance safe. In-process counters are the same class as the #1109 Slack class-level-dict (works single-process, silently wrong under scale). We already run Redis.

## 3. #1307 fix direction — fail-closed: env-gate if dev-only, else auth-protect
The principle decides it: **an admin/compose WRITE endpoint must not be reachable in prod without auth, full stop.** So: if `admin_compose` is dev-tooling (its siblings `dev_trust`/`dev_composting` are, and they 404 in prod via `PIPER_ENVIRONMENT`) → **env-gate it to match them** (consistency + the obvious intent). If it has any real prod use → **auth-protect it**. Either closes #1307; PM's call on which based on the use-case. But the durable fix is the enforcement lint above — so the *next* admin/dev endpoint can't ship exempt+writable+prod, regardless of which way #1307 itself goes.

Net: **GO on gate-removal once #1307 is closed + the exempt-list lint lands** (the lint is the thing that lets you remove the perimeter *and trust* the app-gate going forward). Rate-limiting before public exposure as you flagged. Record my call in the findings doc + #1162/#1307.

— Architect (DinP / Opus 4.8), 2026-06-20 ~19:00 PT
