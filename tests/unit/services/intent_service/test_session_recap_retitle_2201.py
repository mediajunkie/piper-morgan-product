"""#2201: a rename of an issue this session created is declared by the update
handler (``intent_data['retitled_activity']``) so the central observer can
retitle the session_activity ledger row and "what did we create this session?"
shows the title the person now knows it by. The observer and repository halves
are pinned in test_session_activity_observer_1394.py; this pins the handler's
declaration on the success path, with the router mocked (no network).
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent, IntentCategory


def _intent(**ctx) -> Intent:
    base = {
        "issue_number": 31,
        "repository": "dinp-machine/piper-test-activity",
        "original_message": "Actually, change the title to 'Implement full-text search'",
    }
    base.update(ctx)
    return Intent(
        category=IntentCategory.EXECUTION,
        action="update_issue",
        confidence=1.0,
        original_message=base["original_message"],
        context=base,
    )


@pytest.fixture
def svc():
    from services.intent.intent_service import IntentService

    s = IntentService.__new__(IntentService)
    s.logger = MagicMock()
    return s


@pytest.mark.asyncio
async def test_title_change_declares_the_retitle(svc):
    with patch(
        "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
    ) as MockRouter:
        router = AsyncMock()
        router.update_issue = AsyncMock(
            return_value={"number": 31, "title": "Implement full-text search", "state": "open"}
        )
        MockRouter.return_value = router
        result = await svc._handle_update_issue(
            _intent(title="Implement full-text search"), workflow_id="wf-2201"
        )
    assert result.success is True, result.message
    assert result.intent_data["retitled_activity"] == {
        "target_ref": "dinp-machine/piper-test-activity#31",
        "target_title": "Implement full-text search",
    }


@pytest.mark.asyncio
async def test_a_non_title_update_declares_nothing(svc):
    with patch(
        "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
    ) as MockRouter:
        router = AsyncMock()
        router.update_issue = AsyncMock(
            return_value={"number": 31, "title": "Add search", "state": "closed"}
        )
        MockRouter.return_value = router
        result = await svc._handle_update_issue(
            _intent(state="closed", original_message="close issue 31"), workflow_id="wf-2201"
        )
    assert result.success is True, result.message
    assert result.intent_data["retitled_activity"] is None
