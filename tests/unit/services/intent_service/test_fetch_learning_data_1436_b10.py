"""#1436 B10: _fetch_learning_data must read the router's issue DICTS, not objects.

Regression: GitHubIntegrationRouter.get_recent_issues returns adapter-shaped
dicts (number/title/description/state/labels-as-strings). The learn-patterns
path read them as objects (.title/.body/.labels[].name) — AttributeError on the
first issue, swallowed by the surrounding except, [] returned: the feature was
silently dead (census 2026-07-16, the #1420/#1423 mask pattern).
"""

from unittest.mock import AsyncMock, MagicMock, patch

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.shared_types import IntentCategory

ADAPTER_ISSUES = [
    {
        "number": 101,
        "title": "Login button broken",
        "description": "Clicking login does nothing",
        "state": "open",
        "labels": ["bug", "P1"],
    },
    {
        "number": 102,
        "title": "Add dark mode",
        "description": "Users want a dark theme",
        "state": "open",
        "labels": [],
    },
]


def _intent(query=""):
    return Intent(
        category=IntentCategory.ANALYSIS,
        action="learn_patterns",
        confidence=1.0,
        context={"source": "github_issues", "query": query},
        original_message="learn from my issues",
    )


def _service():
    svc = IntentService.__new__(IntentService)  # method needs only self.logger
    svc.logger = MagicMock()
    return svc


async def test_adapter_dicts_are_normalized_not_attribute_errored():
    with patch(
        "services.integrations.github.github_integration_router.GitHubIntegrationRouter.get_recent_issues",
        new=AsyncMock(return_value=list(ADAPTER_ISSUES)),
    ):
        out = await _service()._fetch_learning_data(_intent())
    assert [i["number"] for i in out] == [101, 102]  # old code: AttributeError -> []
    assert out[0]["body"] == "Clicking login does nothing"  # description -> body contract
    assert out[0]["labels"] == ["bug", "P1"]  # already strings, no .name access


async def test_search_query_filters_on_title_and_description():
    with patch(
        "services.integrations.github.github_integration_router.GitHubIntegrationRouter.get_recent_issues",
        new=AsyncMock(return_value=list(ADAPTER_ISSUES)),
    ):
        out = await _service()._fetch_learning_data(_intent(query="dark"))
    assert [i["number"] for i in out] == [102]
