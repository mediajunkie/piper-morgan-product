# Web Routes Conventions

**Status**: Active convention reference
**Owner**: Architecture
**Last updated**: 2026-09-23 (#1499 Class 2 — disposal executed; previously #1499 drift
correction same day; before that 2026-05-16 / #1075)
**Companion**: CLAUDE.md → "API Conventions" section

> ⚠️ **Read the exception list below with its disposal status.** The 2026-08-07 route audit
> (#1499) found that **all three** "deliberate exceptions" this doc described as live route
> surfaces were mounted by no app. Arch ruled GO on disposal the same day (#1499 Class 2,
> `mailboxes/lead/read/rule-arch-to-lead-cc-pm-1863-1499-both-GO-verified-2026-09-23.md`) and
> the dead routers named below were `git rm`'d. The rows are kept struck-through rather than
> removed — deleting them would erase the rationale along with the drift — and each now says
> what happened to it. Full accounting:
> `docs/internal/architecture/design-records/disposal-record-1499-class-2-dark-routers-2026-09-23.md`.
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

Three route surfaces were codified here as intentional exceptions sitting outside `/api/v1/`, so future authors don't trip the rule when reading the code. **As of the 2026-08-07 audit (#1499), none of the three was mounted**, and two of the three were disposed of on 2026-09-23 (#1499 Class 2). The rationales below are kept struck-through — they remain the right rationales *if* a surface like this comes back, and the history is worth more than a silent deletion.

### 1. ~~`web/api/routes/loading_demo.py` — `/loading`~~

> 🔴 **DELETED 2026-09-23 (#1499 Class 2, Arch Rule-0 GO).** Was 8 route definitions, mounted by no app and referenced by no UI, confirmed still-dark at cut time. Disposal record:
> `docs/internal/architecture/design-records/disposal-record-1499-class-2-dark-routers-2026-09-23.md`.

**Purpose (historical)**: Pedagogical demo of loading-state UX patterns. Not part of the product surface; served a demo page that demonstrated spinner/skeleton/progress patterns for design-system reference.

**Why not `/api/v1/` (historical rationale)**: It's a static demo page, not an API endpoint. Putting it under `/api/v1/` would imply API versioning semantics (deprecation, backward-compat guarantees) that don't apply — still the right call if this kind of surface returns.

### 2. ~~`web/api/routes/conversation_context_demo.py` — `/conversation`~~

> 🔴 **DELETED 2026-09-23 (#1499 Class 2, Arch Rule-0 GO).** Was 6 route definitions, mounted by no app and referenced by no UI, confirmed still-dark at cut time. Same disposal record as loading_demo above.

**Purpose (historical)**: Pedagogical demo of conversation-context UX patterns. Served a demo page showing how Piper presents conversation state visually. Sibling to the loading_demo case above.

**Why not `/api/v1/` (historical rationale)**: Same rationale — it's a UX demo, not an API endpoint. The `/conversation` path was chosen for legibility in the demo URL, not for API versioning.

### 3. The root-level `/health` surface

> 🔴 **`staging_health.py` DELETED 2026-09-23 (#1499 Class 2, Arch Rule-0 GO).** This
> section previously named `services/api/health/staging_health.py` as the live `/health` —
> wrong: **that module was mounted by no app** (11 route definitions, all dead), so anything
> probing `/health/liveness` or `/health/readiness` got a 404, and always had.
>
> **The `/health` that actually serves is `web/api/routes/admin.py:56`** (mounted at
> `web/app.py:308`) — the path fly.toml's `[[http_service.checks]]`, the Dockerfile
> `HEALTHCHECK`, `docker-compose.staging.yml` and `scripts/restart-server.sh` all poll. It is
> deliberately ungated; see its docstring before touching it, because gating it is an outage
> rather than a hardening.
>
> `staging_health.py`'s router was the unmounted, deleted part. Its `deploy_identity()`
> helper was NOT dead — it is the single source for the version / git SHA / environment
> fields on both the served `/health` and (since #1499) `/api/v1/version` — so it was
> extracted first, into `services/api/health/deploy_identity.py`, before the shell around it
> was removed. Disposal record:
> `docs/internal/architecture/design-records/disposal-record-1499-class-2-dark-routers-2026-09-23.md`.
>
> The exception itself — root-level `/health`, outside `/api/v1/` — **remains correct and
> live**. Only the file attribution was wrong.

**Purpose**: Operational tooling — ops-team-facing health and monitoring surface for staging deployment validation. Serves uptime checks, audit-log spot checks, and component-status reads consumed by monitoring infrastructure (Datadog / external health checks / staging smoke scripts).

**Why not `/api/v1/`**: Ops-team-facing health endpoints are conventionally root-level (`/health`, `/healthz`, `/ready`) across the industry. Monitoring tooling expects this convention; embedding under `/api/v1/health` would break external monitoring contracts without providing user-facing value. This is the strongest exception — the convention exists *because* operational tooling treats `/health` as a namespace separate from product API.

**Tradeoff**: None really. This is the canonical industry pattern; changing it would create friction with every ops tool that expects `/health` at root.

## Other #1499 Class 2 disposal-batch items (2026-09-23)

Two more dark routers were in the same audit and ruling but weren't documented here as
"deliberate exceptions" — noted for completeness, full accounting in the disposal record:
`docs/internal/architecture/design-records/disposal-record-1499-class-2-dark-routers-2026-09-23.md`.

- ~~`services/api/feedback_api.py`~~ — 🔴 **DELETED.** 6 routes on `/api/v1/feedback`,
  mounted by no app. **Landmine for anyone reading this later**: this router sat on the
  *exact same prefix* as the router that IS mounted — `web/api/routes/feedback.py`
  (`web/app.py:286`) — a same-path collision-in-waiting between a live and a dead router.
- ~~`services/api/slack_monitoring.py`~~ — already deleted **2026-08-30**, in an earlier
  disposal batch (`6729d39521`), before this six-week-old audit's cut date. The fresh sweep
  this ruling required found it already gone; nothing to do.
- `services/integrations/slack/webhook_router.py` (`SlackWebhookRouter`) — **NOT deleted.**
  The audit's own framing ("HTTP surface dead, handlers live via Socket Mode, #1496") turned
  out to be load-bearing, not just color: `SlackWebhookRouter` is instantiated live by
  `services/integrations/slack/socket_mode_runner.py:124-126` to process `/piper`, `/standup`
  and `/link` slash commands, and `tests/test_slack_identity_binding_guard.py` pins this file
  as the sanctioned caller-home for the #1466 identity-binding security invariant. Only the
  class's `APIRouter` mount (`self.router`, `_register_routes`, `get_router`,
  `get_webhook_urls`) is actually dead; the class and its business-logic methods are not.
  Full-file deletion would have broken live Slack slash commands. Left untouched; see the
  disposal record for the recommended scoped follow-up.

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
