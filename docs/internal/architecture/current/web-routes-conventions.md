# Web Routes Conventions

**Status**: Active convention reference
**Owner**: Architecture
**Last updated**: 2026-09-23 (#1499 — drift correction; previously 2026-05-16 / #1075)
**Companion**: CLAUDE.md → "API Conventions" section

> ⚠️ **Read the exception list below with its mount status.** The 2026-08-07 route audit
> (#1499) found that **all three** "deliberate exceptions" this doc described as live route
> surfaces are mounted by no app. The rows are kept — deleting them would erase the rationale
> along with the drift — but each now states what it actually is. Disposal of the unmounted
> routers is #1499 Class 2 and is **pending a Rule-0 ruling with the Architect**; nothing here
> should be read as authorizing a delete or a mount.
>
> House rule this earned, stated once: **a doc's claim that a route is live is a claim about
> the mount graph, and it goes stale silently.** Verify against `web/app.py` +
> `web/startup.py` + the plugin registry before citing anything here as running.

## The rule

All API endpoints MUST use the `/api/v1/` prefix.

- Router prefix: `APIRouter(prefix="/api/v1/your-domain")`
- Frontend fetch calls: `fetch("/api/v1/your-endpoint")`
- Exempt-list updates: include in `web/middleware/intent_enforcement.py` if needed

Never use `/api/` without the version prefix. This ensures consistent versioning and prevents silent 404 errors.

## Deliberate exceptions

Three route surfaces were codified here as intentional exceptions sitting outside `/api/v1/`, so future authors don't trip the rule when reading the code. **As of the 2026-08-07 audit (#1499), none of the three is mounted** — the rationales below remain the right rationales *if* these surfaces come back, which is why they are annotated rather than removed.

### 1. `web/api/routes/loading_demo.py` — `/loading`

> 🔴 **UNMOUNTED as of the 2026-08-07 audit (#1499 Class 2).** 8 route definitions, mounted by no app and referenced by no UI. Disposal pending an Arch ruling; do not mount or delete on the strength of this doc.

**Purpose**: Pedagogical demo of loading-state UX patterns. Not part of the product surface; serves the demo page that demonstrates spinner/skeleton/progress patterns for design-system reference.

**Why not `/api/v1/`**: It's a static demo page, not an API endpoint. Putting it under `/api/v1/` would imply API versioning semantics (deprecation, backward-compat guarantees) that don't apply.

**Tradeoff**: If this evolves into a documented design-system surface, reconsider. Today, it's a single-page example.

### 2. `web/api/routes/conversation_context_demo.py` — `/conversation`

> 🔴 **UNMOUNTED as of the 2026-08-07 audit (#1499 Class 2).** 6 route definitions, mounted by no app and referenced by no UI. Same disposal status as loading_demo above.

**Purpose**: Pedagogical demo of conversation-context UX patterns. Serves the demo page that shows how Piper presents conversation state visually. Sibling to the loading_demo case above.

**Why not `/api/v1/`**: Same rationale — it's a UX demo, not an API endpoint. The `/conversation` path was chosen for legibility in the demo URL, not for API versioning.

**Tradeoff**: Same as loading_demo. If demo content becomes part of a documented design system, reconsider URL space.

### 3. The root-level `/health` surface

> 🔴 **ATTRIBUTION CORRECTED (#1499).** This section previously named
> `services/api/health/staging_health.py` as the live `/health`. **That module is mounted by
> no app** (11 route definitions, all dead), so anything probing `/health/liveness` or
> `/health/readiness` gets a 404 today and always has.
>
> **The `/health` that actually serves is `web/api/routes/admin.py:56`** (mounted at
> `web/app.py:308`) — the path fly.toml's `[[http_service.checks]]`, the Dockerfile
> `HEALTHCHECK`, `docker-compose.staging.yml` and `scripts/restart-server.sh` all poll. It is
> deliberately ungated; see its docstring before touching it, because gating it is an outage
> rather than a hardening.
>
> `staging_health.py` is not dead weight even so: its `deploy_identity()` helper is the
> single source for the version / git SHA / environment fields on both the served `/health`
> and (since #1499) `/api/v1/version`. Its *router* is the unmounted part. Disposal is #1499
> Class 2, pending an Arch ruling.
>
> The exception itself — root-level `/health`, outside `/api/v1/` — **remains correct and
> live**. Only the file attribution was wrong.

**Purpose**: Operational tooling — ops-team-facing health and monitoring surface for staging deployment validation. Serves uptime checks, audit-log spot checks, and component-status reads consumed by monitoring infrastructure (Datadog / external health checks / staging smoke scripts).

**Why not `/api/v1/`**: Ops-team-facing health endpoints are conventionally root-level (`/health`, `/healthz`, `/ready`) across the industry. Monitoring tooling expects this convention; embedding under `/api/v1/health` would break external monitoring contracts without providing user-facing value. This is the strongest exception — the convention exists *because* operational tooling treats `/health` as a namespace separate from product API.

**Tradeoff**: None really. This is the canonical industry pattern; changing it would create friction with every ops tool that expects `/health` at root.

## Migrated for compliance (#1075, 2026-05-16)

Two routers were migrated into compliance with `/api/v1/`:

- `services/api/transparency.py` — `/transparency` → `/api/v1/transparency` (PM-087 user audit-log surface; mounted live as part of this migration since the router had been unwired since #1018 Phase 2)
- ~~`web/routers/admin_compose.py` — `/admin/compose` → `/api/v1/admin/compose`~~ (Issue #998 editorial compose UI; localhost-only scaffold, exempt from auth middleware). 🔴 **The file no longer exists** (#1499): it was deleted by **#1307** in `0466fd09d8`, *"remove misplaced admin_compose product-app router (was auth-exempt + writable + un-env-gated — security gap)"*. Kept struck-through rather than deleted because the #1075 migration record is history, and because the reason it went — auth-exempt **and** writable — is the exact pattern `AUTH_EXEMPT_JUSTIFIED` now blocks by construction.

Prior precedent: #1013 (Apr 28, 2026) migrated `/auth` → `/api/v1/auth` and `/setup` → `/api/v1/setup` using the same shape (router prefix + middleware exempt-list + client-side callsite updates + template URL updates).

## Known violations — documented, NOT endorsed (#1499)

These are live routes that break the rule above. They are listed so the rule's reader isn't
left inferring that silence means compliance (m-44: an unstated exception reads as coverage).
**A listing here is a record, not a grant** — none of these is an approved exception, and new
routes must not cite them as precedent.

### `web/api/routes/admin.py` — 8× `/api/admin/*`

```
GET  /api/admin/intent-monitoring                      (admin.py:188)
GET  /api/admin/intent-cache-metrics                   (admin.py:206)
POST /api/admin/intent-cache-clear                     (admin.py:229)
GET  /api/admin/piper-config-cache-metrics             (admin.py:251)
POST /api/admin/piper-config-cache-clear               (admin.py:268)
GET  /api/admin/user-context-cache-metrics             (admin.py:285)
POST /api/admin/user-context-cache-clear               (admin.py:303)
POST /api/admin/user-context-cache-invalidate/{sid}    (admin.py:320)
```

`/api/` with no version segment — the one thing the rule names outright. Mounted and live.

**Not renamed by #1499, deliberately.** The callers are unknown: these are ops/admin surfaces
with no in-repo UI references (the audit's inverse sweep found zero), which means the set of
external callers — monitoring jobs, scripts, a bookmark, someone's curl — cannot be
established from the repo. Renaming them blind trades a naming violation for a live breakage,
which is the worse of the two. A migration wants a deprecation window (serve both prefixes,
log hits on the old one, then drop), not a rename in a doc-drift pass.

All eight are `require_admin`-gated (#1508 + #1598) and pinned by
`tests/unit/web/api/routes/test_admin_cache_routes_gated_1508.py`, whose denominator test
fails if a route lands on this router unclassified.

### `web/api/routes/ui.py` — 27 root-level page routes

Measured 2026-09-23 by enumerating `ui.router.routes` and counting paths not starting with
`/api/` (27 of 28; the exception is `/api/v1/orientation/dismiss`, which complies). *The
#1499 audit reported 35 — it counted `@router.get("/` source occurrences, a different and
looser method. The live-router count is the one to trust.*

These are **HTML page routes** (`/settings`, `/account`, `/learning`, …), not API endpoints,
so the versioning rationale doesn't apply to them the way it applies to `/api/`. They are a
de facto exception class that this doc had never named. Flagged for the Architect to either
codify as a fourth deliberate exception ("server-rendered page routes live at root") or rule
otherwise — #1499 does not decide it.

## How to add a new route surface

For product-API endpoints:
1. Use `APIRouter(prefix="/api/v1/your-domain", tags=["your-domain"])`
2. Mount via `RouterInitializer.mount_router(app, "module.path", "router_var_name", "Description")` in `web/app.py`
3. If the route needs unauthenticated access, add explicit entries to the appropriate `EXEMPT_*_PATHS` list in `services/auth/auth_middleware.py`
4. Update `web/middleware/intent_enforcement.py` if intent enforcement should skip the path
5. Add tests under `tests/integration/` exercising the routes

For genuine exceptions (demos, ops tooling, scaffolds outside the product surface):
1. Document the exception in this file with the rationale
2. Cross-reference from CLAUDE.md "API Conventions" section so the rule's reader sees the exceptions
3. Flag to Architect for awareness — exceptions tend to accumulate without explicit governance

## How to add a DEV-ONLY route (#1149)

A debug/test/dev-tooling route must not be reachable in production — and not merely
forbidden there, but **invisible** (404, so prod doesn't disclose it exists). The
canonical gate is `web/dev_gate.py`:

1. Mount the router normally via `RouterInitializer.mount_router(...)` in `web/app.py`.
2. Hang the gate on the router so it covers every route:
   ```python
   from web.dev_gate import require_dev_environment
   router = APIRouter(tags=["debug"], dependencies=[Depends(require_dev_environment)])
   ```
   Every route then 404s when `PIPER_ENVIRONMENT` (or the older `ENVIRONMENT`) is
   `production`. Default is `development` (the #1087 pattern) → open in dev, closed in
   prod with no per-deploy config.
3. Add a test exercising the real behavior (404 in prod, served in dev) — see
   `tests/unit/web/test_dev_gate_1149.py`.

The global auth middleware already 401s most routes, but this is **defense-in-depth**:
a dev page shouldn't ship to prod at all. Live examples: `web/api/routes/debug.py`
(#1149), `web/routers/dev_trust.py` (#1148), `web/routers/dev_composting.py` (#1143).
*(Follow-up: migrate dev_trust + dev_composting off their hand-rolled copies onto
`web/dev_gate.require_dev_environment` — small DRY cleanup, not done in #1149's scope.)*
