# Caddy Gate-Removal Safety Investigation — #1162 / #1185

**Date**: 2026-06-20. **Author**: Lead Dev. **For**: PM + Architect (go/no-go decision).

## Question
Can the static Caddy basic-auth gate on the hosted instance be removed (the #1162 public-BYOC step) without exposing the app? I.e., is the app's own auth robust enough to be the **sole** protection?

## Headline: CONDITIONAL GO
The app has its **own global `AuthMiddleware`** (JWT) that gates every route except a small categorized exempt list. Removing Caddy does **not** open everything — the app self-gates. But the exempt list has **one real hole** (a writable admin UI) and there is **no rate-limiting**, both of which must be addressed first.

## How the app gates itself (the foundation for a GO)
- `web/app.py:61`: `AuthMiddleware` (`services/auth/auth_middleware.py`) is mounted **globally**.
- It validates JWT on **every** path except `DEFAULT_EXCLUDE_PATHS` (7 named categories).
- Non-exempt routes return **401** without a valid token (`get_current_user` raises `APIError(401)`). **171** required-auth call sites vs **3** optional-auth (`Depends`) sites.

## Exposure surface if Caddy is removed = the exempt list
| Category | Paths | Risk |
|---|---|---|
| OpenAPI | `/docs`, `/redoc`, `/openapi.json` | Low — reveals API map, no user data |
| Health | `/health`, `/api/v1/health` | None |
| Auth/setup bootstrap | `/login`, `/setup`, `/api/v1/auth/login\|logout\|refresh`, `/api/v1/setup/*` | Low — must be public. **`/auth/register` is exempt but has NO handler → 404** (not a concern) |
| Optional-auth | `/api/v1/intent`, `/workflows`, `/standup` | **Medium** — run unauthenticated; the LLM call is gated by BYO-key (no key → no call) |
| OAuth callbacks | slack/github/calendar connect+callback | None — code-based |
| Static | `/static/`, `/assets/` | None |
| Localhost scaffolds | `/api/v1/admin/compose`, `/api/v1/admin/trust` | `admin/trust` 404s in prod (env-gated); **`admin/compose` does NOT — see BLOCKER** |

## Must-fix before removal
1. **BLOCKER — `admin_compose` is an open *writable* admin UI.** `web/routers/admin_compose.py` (`/api/v1/admin/compose`) is auth-exempt AND exposes **`POST /{slug}/save`** which writes editorial drafts (`write_draft`). Unlike its siblings `dev_trust` / `dev_composting` (which 404 in prod via a `PIPER_ENVIRONMENT` gate — see `require_dev_environment`/`_is_production` in `web/routers/dev_trust.py`), it has **no env-gate**. Today it is protected **only by the Caddy gate**. Remove Caddy → anyone can list/read/**write** drafts in prod. This is a defense-in-depth gap *regardless* of the gate decision.
   **Fix depends on intended use**:
   - If compose is a **dev/editorial-only** tool → apply the `dev_trust` `require_dev_environment` 404-gate (copy the pattern). Simplest; matches siblings.
   - If PM uses compose **on the hosted instance** → it must be **auth-protected** (remove from the exempt list + add `Depends(get_current_user)`), not env-gated.
2. **SHOULD — no rate-limiting exists.** No slowapi/limiter/throttle middleware anywhere (only `AuthMiddleware`, `EnhancedErrorMiddleware`, `IntentEnforcementMiddleware`). Public exposure of `/login` (brute-force) and `/intent` (abuse) wants throttling on the exempt endpoints.
3. **CONFIRM — `/intent` unauthenticated is abuse-bounded.** The expensive LLM call is gated by BYO-key (#1185: no stored/header key → `resolve_request_api_key` returns None → no call). Confirm no other costly unauthenticated side-effects.

## Recommendation
- **The gate-removal is architecturally sound** — `AuthMiddleware` is the real gate; Caddy is redundant perimeter for the 171 authenticated routes.
- **Do NOT remove Caddy until #1 (admin_compose) is fixed** — that's a genuine prod write-exposure today (perimeter is its only guard).
- **Add rate-limiting (#2) before public BYOC exposure.**
- Then the removal itself is a one-line Caddy-config change (drop the basic-auth directive), tied to the public-distribution milestone.
- #1 is small and worth doing now regardless of the gate (defense-in-depth). **Filed as #1307** (blocks #1162). Lead Dev can take it once PM confirms dev-only vs prod-use.

## Arch's review (2026-06-20) — CONCUR + the class-fix
Arch (gate-removal concur memo, 2026-06-20):
- **CONCUR** AuthMiddleware-as-sole-gate — the *correct* model; perimeter-only (Caddy) is the dated, semantically-blind pattern; app-owned auth realizes ADR-058 + ADR-071.
- **Load-bearing add**: once Caddy is gone, the auth-exempt list IS the attack surface → it's a security boundary, needing an **enforcement lint**: every exempt route must be read-only **or** env-gated **or** on an `AUTH_EXEMPT_JUSTIFIED` allowlist (fail-closed). Makes #1307's class impossible-by-construction. → **#1308**.
- **Rate-limiting**: global ASGI fail-closed default + slowapi per-route (intent / login) + **Redis-backed** (in-process = the #1109 class).
- **#1307**: fixed by **removal** (PM-directed) — admin_compose deleted (`0466fd09d`); **CLOSED**.
- **GO on gate-removal once #1307 (done) + #1308 (lint) land** + rate-limiting before public exposure. The removal itself is M5/distribution-time.
