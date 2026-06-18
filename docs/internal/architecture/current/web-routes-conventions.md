# Web Routes Conventions

**Status**: Active convention reference
**Owner**: Architecture
**Last updated**: 2026-05-16 (#1075)
**Companion**: CLAUDE.md → "API Conventions" section

## The rule

All API endpoints MUST use the `/api/v1/` prefix.

- Router prefix: `APIRouter(prefix="/api/v1/your-domain")`
- Frontend fetch calls: `fetch("/api/v1/your-endpoint")`
- Exempt-list updates: include in `web/middleware/intent_enforcement.py` if needed

Never use `/api/` without the version prefix. This ensures consistent versioning and prevents silent 404 errors.

## Deliberate exceptions

Three live route surfaces sit outside `/api/v1/`. These are intentional and codified here so future authors don't trip the rule when reading the code.

### 1. `web/api/routes/loading_demo.py` — `/loading`

**Purpose**: Pedagogical demo of loading-state UX patterns. Not part of the product surface; serves the demo page that demonstrates spinner/skeleton/progress patterns for design-system reference.

**Why not `/api/v1/`**: It's a static demo page, not an API endpoint. Putting it under `/api/v1/` would imply API versioning semantics (deprecation, backward-compat guarantees) that don't apply.

**Tradeoff**: If this evolves into a documented design-system surface, reconsider. Today, it's a single-page example.

### 2. `web/api/routes/conversation_context_demo.py` — `/conversation`

**Purpose**: Pedagogical demo of conversation-context UX patterns. Serves the demo page that shows how Piper presents conversation state visually. Sibling to the loading_demo case above.

**Why not `/api/v1/`**: Same rationale — it's a UX demo, not an API endpoint. The `/conversation` path was chosen for legibility in the demo URL, not for API versioning.

**Tradeoff**: Same as loading_demo. If demo content becomes part of a documented design system, reconsider URL space.

### 3. `services/api/health/staging_health.py` — `/health`

**Purpose**: Operational tooling — ops-team-facing health and monitoring surface for staging deployment validation. Serves uptime checks, audit-log spot checks, and component-status reads consumed by monitoring infrastructure (Datadog / external health checks / staging smoke scripts).

**Why not `/api/v1/`**: Ops-team-facing health endpoints are conventionally root-level (`/health`, `/healthz`, `/ready`) across the industry. Monitoring tooling expects this convention; embedding under `/api/v1/health` would break external monitoring contracts without providing user-facing value. This is the strongest exception — the convention exists *because* operational tooling treats `/health` as a namespace separate from product API.

**Tradeoff**: None really. This is the canonical industry pattern; changing it would create friction with every ops tool that expects `/health` at root.

## Migrated for compliance (#1075, 2026-05-16)

Two routers were migrated into compliance with `/api/v1/`:

- `services/api/transparency.py` — `/transparency` → `/api/v1/transparency` (PM-087 user audit-log surface; mounted live as part of this migration since the router had been unwired since #1018 Phase 2)
- `web/routers/admin_compose.py` — `/admin/compose` → `/api/v1/admin/compose` (Issue #998 editorial compose UI; localhost-only scaffold, exempt from auth middleware)

Prior precedent: #1013 (Apr 28, 2026) migrated `/auth` → `/api/v1/auth` and `/setup` → `/api/v1/setup` using the same shape (router prefix + middleware exempt-list + client-side callsite updates + template URL updates).

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
