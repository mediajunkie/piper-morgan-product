"""#1504: the auth-exempt /api/v1/setup write routes had no setup-complete
lockout — unauthenticated global LLM-key overwrite (F1), global Slack creds
(F2), project rows with attacker-chosen owner_id (F3), and an alembic-upgrade
trigger (F4), all callable forever on a live server. Lockout: once any user has
setup_complete=true, the four write routes refuse 403 with honest copy.

Pins are router-derived (the dependency must be WIRED, not merely defined) plus
behavioral checks of the dependency itself. First-run is protected in both
directions: no-completed-user → allowed; completed-user → refused; DB failure →
refuse (503), never allow.
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from web.api.routes import setup as setup_routes
from web.api.routes.setup import require_setup_incomplete

GATED = {
    "/api/v1/setup/check-system",
    "/api/v1/setup/slack-credentials",
    "/api/v1/setup/complete",
    "/api/v1/setup/projects",
}

# Deliberately ungated: reads, store=False validators, invite-gated create-user,
# and OAuth routes that self-enforce auth (audit not-findings, 2026-08-07).
UNGATED_OK = {
    "/api/v1/setup/status",
    "/api/v1/setup/validate-key",
    "/api/v1/setup/check-keychain/{provider}",
    "/api/v1/setup/use-keychain",
    "/api/v1/setup/create-user",
    "/api/v1/setup/slack/oauth/start",
    "/api/v1/setup/slack/oauth/callback",
    "/api/v1/setup/slack/status",
    "/api/v1/setup/calendar/oauth/start",
    "/api/v1/setup/calendar/oauth/callback",
    "/api/v1/setup/calendar/status",
}


def _route_dependency_map():
    deps = {}
    for route in setup_routes.router.routes:
        calls = {d.call for d in route.dependant.dependencies if d.call is not None}
        deps[route.path] = calls
    return deps


class TestLockoutWiring:
    def test_all_four_write_routes_carry_the_lockout(self):
        deps = _route_dependency_map()
        missing = GATED - set(deps)
        assert not missing, f"expected setup routes not found: {missing}"
        unwired = {p for p in GATED if require_setup_incomplete not in deps[p]}
        assert not unwired, f"write routes WITHOUT the #1504 lockout: {unwired}"

    def test_first_run_routes_stay_open(self):
        """The wizard must still work on a fresh server — reads, validators,
        and the invite-gated create-user stay lockout-free."""
        deps = _route_dependency_map()
        wrongly_gated = {p for p in UNGATED_OK if p in deps and require_setup_incomplete in deps[p]}
        assert not wrongly_gated, f"first-run routes unexpectedly locked: {wrongly_gated}"

    def test_denominator_every_route_classified(self):
        """m-44: any setup route outside both sets is unexamined surface."""
        deps = _route_dependency_map()
        uncovered = set(deps) - GATED - UNGATED_OK
        assert not uncovered, f"setup routes needing classification: {uncovered}"


class TestLockoutBehavior:
    @pytest.mark.asyncio
    async def test_refuses_once_any_user_completed_setup(self):
        with patch.object(
            setup_routes, "_completed_setup_exists", new=AsyncMock(return_value=True)
        ):
            with pytest.raises(HTTPException) as exc:
                await require_setup_incomplete()
            assert exc.value.status_code == 403
            assert "Settings" in exc.value.detail  # honest copy points somewhere real

    @pytest.mark.asyncio
    async def test_allows_on_fresh_server(self):
        with patch.object(
            setup_routes, "_completed_setup_exists", new=AsyncMock(return_value=False)
        ):
            assert await require_setup_incomplete() is None

    @pytest.mark.asyncio
    async def test_db_failure_refuses_never_allows(self):
        """Fail-closed: an unreachable DB must not reopen the wizard."""
        with patch.object(
            setup_routes,
            "_completed_setup_exists",
            new=AsyncMock(side_effect=RuntimeError("db down")),
        ):
            with pytest.raises(HTTPException) as exc:
                await require_setup_incomplete()
            assert exc.value.status_code == 503


class TestPredicateAgainstRealDatabase:
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_predicate_runs_real_sql(self):
        """The count query must be valid against the actual schema (guards the
        column name against drift; value depends on dev-DB state so only the
        type is asserted)."""
        result = await setup_routes._completed_setup_exists()
        assert isinstance(result, bool)
