"""#1508: the four /api/admin cache-mutation routes said "admin only" in their
docstrings and checked nothing — any authenticated user could clear ALL users'
cached context. Fix: #1485's require_admin dependency applied to each. These
pins assert the dependency is actually WIRED (a docstring is not a gate), the
same never-vacuous shape as the #1466 binding guard: derive the route→dependency
mapping from the router itself, not from re-reading the source strings.
"""

from fastapi.params import Depends as DependsParam

from services.auth.auth_middleware import require_admin
from web.api.routes import admin as admin_module

GATED = {
    "/api/admin/intent-cache-clear",
    "/api/admin/piper-config-cache-clear",
    "/api/admin/user-context-cache-clear",
    "/api/admin/user-context-cache-invalidate/{session_id}",
}

UNGATED_READONLY = {
    "/health",
    "/health/config",
    "/api/admin/intent-monitoring",
    "/api/admin/intent-cache-metrics",
    "/api/admin/piper-config-cache-metrics",
    "/api/admin/user-context-cache-metrics",
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
    def test_all_four_mutating_routes_require_admin(self):
        deps = _route_dependencies()
        # Denominator first: every expected route actually exists on the router
        missing = GATED - set(deps)
        assert not missing, f"expected admin routes not found: {missing}"
        ungated = {p for p in GATED if require_admin not in deps[p]}
        assert not ungated, f"mutating admin routes WITHOUT require_admin: {ungated}"

    def test_readonly_routes_unchanged(self):
        """The metrics/health reads deliberately stay ungated (middleware-authed
        for /api/*; /health is exempt by convention) — pin so the 1508 fix
        can't silently widen into breaking monitoring."""
        deps = _route_dependencies()
        missing = UNGATED_READONLY - set(deps)
        assert not missing, f"expected readonly routes not found: {missing}"
        wrongly_gated = {p for p in UNGATED_READONLY if require_admin in deps[p]}
        assert not wrongly_gated, f"readonly routes unexpectedly admin-gated: {wrongly_gated}"

    def test_router_route_count_denominator(self):
        """m-44: the two sets above must cover the whole router, or a new
        mutating route could land ungated and unexamined."""
        deps = _route_dependencies()
        uncovered = set(deps) - GATED - UNGATED_READONLY
        assert not uncovered, (
            f"admin routes outside both audited sets — classify them: {uncovered}"
        )
