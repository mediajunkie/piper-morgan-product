"""#1508: the four /api/admin cache-mutation routes said "admin only" in their
docstrings and checked nothing — any authenticated user could clear ALL users'
cached context. Fix: #1485's require_admin dependency applied to each. These
pins assert the dependency is actually WIRED (a docstring is not a gate), the
same never-vacuous shape as the #1466 binding guard: derive the route→dependency
mapping from the router itself, not from re-reading the source strings.

1598 (PM ruling 2026-08-25) extends the same gate to the FIVE read-only
metrics/health reads #1508 deliberately left open. `UNGATED_READONLY` below is
consequently down to one member — `/health`, which deployment infrastructure
polls without credentials (fly.toml health check, Dockerfile HEALTHCHECK,
docker-compose.staging.yml, scripts/restart-server.sh). Gating that one would
be an outage, not a hardening; see the route docstring.

Behavioral 403/200 pins for the newly-gated reads live in
test_admin_readonly_routes_gated_1598.py — this file stays a wiring pin.
"""

from fastapi.params import Depends as DependsParam

from services.auth.auth_middleware import require_admin
from web.api.routes import admin as admin_module

GATED = {
    # #1508 — the mutations
    "/api/admin/intent-cache-clear",
    "/api/admin/piper-config-cache-clear",
    "/api/admin/user-context-cache-clear",
    "/api/admin/user-context-cache-invalidate/{session_id}",
    # 1598 — the read-only metrics/health reads
    "/health/config",
    "/api/admin/intent-monitoring",
    "/api/admin/intent-cache-metrics",
    "/api/admin/piper-config-cache-metrics",
    "/api/admin/user-context-cache-metrics",
}

UNGATED_READONLY = {
    "/health",
}


def _route_dependencies():
    """Map route path -> set of dependency callables, derived from the live router."""
    deps = {}
    for route in admin_module.router.routes:
        callables = set()
        for p in route.dependant.dependencies:
            if p.call is not None:
                callables.add(p.call)
        deps[route.path] = callables
    return deps


class TestAdminCacheRoutesGated:
    def test_all_privileged_routes_require_admin(self):
        deps = _route_dependencies()
        # Denominator first: every expected route actually exists on the router
        missing = GATED - set(deps)
        assert not missing, f"expected admin routes not found: {missing}"
        ungated = {p for p in GATED if require_admin not in deps[p]}
        assert not ungated, f"admin routes WITHOUT require_admin: {ungated}"

    def test_health_liveness_probe_stays_open(self):
        """/health must NOT acquire require_admin. Fly's http_service check,
        the Dockerfile HEALTHCHECK and the restart scripts poll it with no
        credentials — a gate here fails the deploy health gate and restart-loops
        the machine. Pinned so a future "gate everything on this router" sweep
        has to argue with a test instead of taking prod down."""
        deps = _route_dependencies()
        missing = UNGATED_READONLY - set(deps)
        assert not missing, f"expected readonly routes not found: {missing}"
        wrongly_gated = {p for p in UNGATED_READONLY if require_admin in deps[p]}
        assert not wrongly_gated, (
            f"liveness probe unexpectedly admin-gated (this is an OUTAGE, not a "
            f"hardening — see fly.toml [[http_service.checks]]): {wrongly_gated}"
        )

    def test_router_route_count_denominator(self):
        """m-44: the two sets above must cover the whole router, or a new
        mutating route could land ungated and unexamined."""
        deps = _route_dependencies()
        uncovered = set(deps) - GATED - UNGATED_READONLY
        assert not uncovered, (
            f"admin routes outside both audited sets — classify them: {uncovered}"
        )
