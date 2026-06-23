# #1308 — Auth-exempt-list enforcement lint — Gameplan

**Issue**: #1308. **From**: Arch's gate-removal review (concur memo + ADR-058/071). **Prereq for**: #1162 (Caddy gate-removal). **Date**: 2026-06-20. **Author**: Lead Dev.

## Problem
Once the Caddy perimeter gate is removed (#1162), the `AuthMiddleware` auth-exempt list (`DEFAULT_EXCLUDE_PATHS`, `services/auth/auth_middleware.py`) **is the entire attack surface**. #1307 (admin_compose: exempt + writable + un-env-gated) proved it lacks boundary rigor — the hole was caught only by manual inspection. Make the class **impossible-by-construction** via a CI lint (m-41 mechanism).

## Design (grounded in the route categorization, 2026-06-20)
A CI lint asserts: **every registered route under an exempt prefix that has a WRITE method (POST/PUT/PATCH/DELETE) must be covered by an explicit `AUTH_EXEMPT_JUSTIFIED` allowlist** (path/prefix → one-line reason). Read-only exempt routes need no entry. A new writable + exempt route not on the allowlist **fails the build**.

**AUTH_EXEMPT_JUSTIFIED** — the current writable exempt routes (all legitimately justified):
- **Auth bootstrap**: `/api/v1/auth/login`, `/logout`, `/refresh` — can't require auth to authenticate.
- **Setup wizard** (prefix `/api/v1/setup/`): check-system / validate-key / use-keychain / slack-credentials / create-user / complete / projects — runs pre-account-creation.
- **Optional-auth**: `/api/v1/intent` — handles auth inline; the LLM call is gated by BYO-key (#490 / #1185).
- **Env-gated dev**: `/api/v1/admin/trust/set-stage` — 404s in prod via `dev_trust`'s `require_dev_environment`.

**Simplification (noted to Arch)**: I collapse Arch's category (b) "env-gated" *into* the justified allowlist (the entry's reason states "env-gated") rather than auto-detecting `require_dev_environment` from the route table — env-gating 404s at *request-time* (the route still exists in `app.routes`), so it isn't reliably detectable statically. Cleaner v1; auto-detection of the dev-gate dependency is a possible refinement.

## Phases (TDD)
- **P1** — add `AUTH_EXEMPT_JUSTIFIED` (dict: exact path or trailing-`/` prefix → reason) to `auth_middleware.py`, populated with the 4 categories above.
- **P2** — the lint (`tests/test_architecture_enforcement.py`, new class `TestAuthExemptListIsASecurityBoundary`): load the app; for each route under an exempt prefix with a WRITE method, assert it's covered by `AUTH_EXEMPT_JUSTIFIED` (exact or prefix match) — else fail with the remediation message (make it read-only / env-gate it / add a justified entry / don't exempt it). Plus a synthetic test: a writable exempt route absent from the allowlist is flagged.

## STOP conditions
- A writable exempt route exists that is NOT legitimately justifiable (a real #1307-class hole) → STOP + surface; do **not** allowlist it just to green the test.
- The lint can't load the app (env) → STOP.

## Success criteria
- Every current writable exempt route is justified → the lint passes (confirming admin_compose's removal left no #1307-class hole).
- A new exempt + writable + prod route fails the build.
- #1162 gate-removal prerequisite satisfied. Note the env-gated simplification for Arch.
