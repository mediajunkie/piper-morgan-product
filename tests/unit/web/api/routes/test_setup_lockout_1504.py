"""#1504: the auth-exempt /api/v1/setup write routes had no setup-complete
lockout — unauthenticated global LLM-key overwrite (F1), global Slack creds
(F2), project rows with attacker-chosen owner_id (F3), and an alembic-upgrade
trigger (F4), all callable forever on a live server. Lockout: once any user has
setup_complete=true, the instance-wide write route refuses 403 with honest copy
(#2078 moved the two per-user writes onto the session principal instead).

Pins are router-derived (the dependency must be WIRED, not merely defined) plus
behavioral checks of the dependency itself. First-run is protected in both
directions: no-completed-user → allowed; completed-user → refused; DB failure →
refuse (503), never allow.
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from services.auth.auth_middleware import get_current_user
from web.api.routes import setup as setup_routes
from web.api.routes.setup import require_setup_incomplete

GATED = {
    "/api/v1/setup/slack-credentials",
}

# #2078 (Arch, 2026-10-17): the two PER-USER wizard writes take their principal
# from the session instead (create-user signs the new account in). The #1504
# lockout came off them because the principal check is what stops F1 now; on an
# initialized instance the lockout had refused every invited tester's wizard.
PRINCIPAL_GATED = {
    "/api/v1/setup/complete",
    "/api/v1/setup/projects",
}

# Deliberately ungated: reads, store=False validators, invite-gated create-user,
# and OAuth routes that self-enforce auth (audit not-findings, 2026-08-07).
# check-system moved here 2026-09-24 (#1875): it is a READ, and gating it
# 403'd the wizard's Step 1 for every invited user on an initialized instance.
UNGATED_OK = {
    "/api/v1/setup/check-system",
    "/api/v1/setup/check-invite",  # #2088: a READ (checks, never spends)
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
    def test_instance_wide_write_route_carries_the_lockout(self):
        deps = _route_dependency_map()
        missing = GATED - set(deps)
        assert not missing, f"expected setup routes not found: {missing}"
        unwired = {p for p in GATED if require_setup_incomplete not in deps[p]}
        assert not unwired, f"write routes WITHOUT the #1504 lockout: {unwired}"

    def test_per_user_write_routes_carry_the_session_principal_not_the_lockout(self):
        """#2078: /complete and /projects require the signed-in user and must NOT
        carry the instance lockout (which stranded every invited tester)."""
        deps = _route_dependency_map()
        missing = PRINCIPAL_GATED - set(deps)
        assert not missing, f"expected setup routes not found: {missing}"
        no_principal = {p for p in PRINCIPAL_GATED if get_current_user not in deps[p]}
        assert not no_principal, f"per-user writes WITHOUT get_current_user: {no_principal}"
        still_locked = {p for p in PRINCIPAL_GATED if require_setup_incomplete in deps[p]}
        assert not still_locked, f"per-user writes still behind the #1504 lockout: {still_locked}"

    def test_first_run_routes_stay_open(self):
        """The wizard must still work on a fresh server — reads, validators,
        and the invite-gated create-user stay lockout-free."""
        deps = _route_dependency_map()
        wrongly_gated = {p for p in UNGATED_OK if p in deps and require_setup_incomplete in deps[p]}
        assert not wrongly_gated, f"first-run routes unexpectedly locked: {wrongly_gated}"

    def test_denominator_every_route_classified(self):
        """m-44: any setup route outside both sets is unexamined surface."""
        deps = _route_dependency_map()
        uncovered = set(deps) - GATED - PRINCIPAL_GATED - UNGATED_OK
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
