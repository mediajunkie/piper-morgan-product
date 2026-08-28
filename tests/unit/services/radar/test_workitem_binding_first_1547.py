"""#1547 (audit F4, Radar leg): WorkItemProvider's gate is binding-first.

The previous gate was PAT-only ``router.config_service.is_configured(user_id)`` —
an OAuth-bound-no-PAT user (the normal hosted case post-#1322) read "not
configured" and standup/Radar work items silently blanked to [] while the web
/health page correctly reported GitHub healthy.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.radar.feed_factory import WorkItemProvider

SVC = "services.integrations.integration_status_service.IntegrationStatusService"


def _mock_router(*, pat_configured=False):
    router = MagicMock()
    router.config_service.is_configured.return_value = pat_configured
    router.initialize = AsyncMock()
    router.get_open_issues = AsyncMock(return_value=[])
    router.close = AsyncMock()
    return router


@pytest.mark.asyncio
async def test_oauth_bound_no_pat_user_gets_work_items_fetched():
    """The F4 case: canonical service says configured (OAuth binding) while the
    PAT-only config service says False → the provider must STILL fetch."""
    router = _mock_router(pat_configured=False)
    with (
        patch(f"{SVC}.is_configured", new=AsyncMock(return_value=True)),
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ),
        patch(
            "services.integrations.github.repo_resolver.read_user_github_handle",
            new=AsyncMock(return_value=None),
        ),
    ):
        result = await WorkItemProvider().list_for_user("u1")
    assert result == []
    router.initialize.assert_awaited_once_with(user_id="u1")
    router.get_open_issues.assert_awaited_once()


@pytest.mark.asyncio
async def test_unconfigured_user_short_circuits_before_any_session():
    """The pre-existing no-session fast path stays: not configured → [] with no
    router constructed at all."""
    with (
        patch(f"{SVC}.is_configured", new=AsyncMock(return_value=False)),
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as router_cls,
    ):
        result = await WorkItemProvider().list_for_user("u1")
    assert result == []
    router_cls.assert_not_called()
