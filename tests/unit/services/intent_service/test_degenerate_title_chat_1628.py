"""#1628 — chat-side listings never render degenerate GitHub titles verbatim.

#1622 guarded the Radar entity-derivation seam (``services/radar/sources.py``)
against the literal-``{`` residue class (JSON-fragment issue titles in the bound
repo). #1628 is the follow-up that issue named: chat-side listing surfaces
printed GitHub titles verbatim outside that seam. The guard now lives in
``services/utils/text_sanitation.display_title`` and is applied at every
chat-side render site; these tests pin the shared util plus one representative
handler per surface family (open-issues listing, first-contact demo block,
canonical status/priority formatters).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.first_contact import render_first_contact_block
from services.mcp.consumer.github_adapter import GitHubIssuesResult
from services.shared_types import IntentCategory
from services.utils.text_sanitation import display_title

# ---------------------------------------------------------------------------
# The shared util (lifted verbatim from radar/sources.py — same matrix as #1622)
# ---------------------------------------------------------------------------


class TestDisplayTitle:
    @pytest.mark.parametrize(
        "degenerate",
        ["{", "}", "", "   ", None, "!", "...", "-", "*", "x", "\t\n"],
    )
    def test_degenerate_titles_fall_back(self, degenerate):
        assert display_title(degenerate, "(untitled issue #100)") == "(untitled issue #100)"

    @pytest.mark.parametrize(
        "real",
        ["v2", "Fix login flow", "a1", "#1 fix", "OK"],
    )
    def test_real_short_titles_survive(self, real):
        assert display_title(real, "(untitled)") == real

    def test_whitespace_is_stripped_not_falsified(self):
        assert display_title("  v2  ", "(untitled)") == "v2"


# ---------------------------------------------------------------------------
# "Show my open issues" — _handle_list_issues_query (intent_service.py)
# ---------------------------------------------------------------------------

_CONN = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_issues"
_NATIVE = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _list_issues_intent():
    return Intent(
        category=IntentCategory.QUERY,
        action="list_issues_query",
        context={"original_message": "show my open issues"},
    )


@pytest.mark.asyncio
async def test_open_issues_listing_replaces_brace_title(intent_service):
    issues = [
        {"number": 100, "title": "{", "labels": []},
        {"number": 7, "title": "v2", "labels": []},
    ]
    result = GitHubIssuesResult(issues=issues, total=2)
    with patch(_CONN, new=AsyncMock(return_value=result)):
        with patch(_NATIVE) as native:
            res = await intent_service._handle_list_issues_query(_list_issues_intent(), "wf")
    assert res.success
    assert "(untitled issue #100)" in res.message  # id-carrying placeholder
    assert "{" not in res.message  # the residue class never renders verbatim
    assert "v2" in res.message  # real short titles survive (#1622 matrix)
    native.assert_not_called()


# ---------------------------------------------------------------------------
# First-contact demo block (first_contact.py render_first_contact_block)
# ---------------------------------------------------------------------------


def test_first_contact_block_replaces_brace_title():
    payload = {
        "connector": "github",
        "repo": "acme/rocket",
        "items": [
            {"number": 100, "title": "{", "type": "issue", "recency": "updated today"},
            {"number": 456, "title": "v2", "type": "pr", "recency": "updated 3 days ago"},
        ],
        "open_count": 2,
    }
    block = render_first_contact_block(payload)
    assert '"(untitled issue #100)"' in block
    assert "{" not in block
    assert '"v2"' in block


# ---------------------------------------------------------------------------
# Canonical formatters (canonical_handlers.py) — priority + project-status
# ---------------------------------------------------------------------------


@pytest.fixture
def canonical_handlers():
    return CanonicalHandlers()


def test_standard_priorities_replaces_brace_title(canonical_handlers):
    metadata = {
        "high_priority_issues": [
            {"number": 100, "title": "{", "labels": ["p0"]},
            {"number": 7, "title": "v2", "labels": ["p1"]},
        ]
    }
    out = canonical_handlers._format_standard_priorities(
        ["Ship the beta"], MagicMock(organization=None), metadata
    )
    assert "(untitled issue #100)" in out
    assert "{" not in out
    assert "v2" in out


def test_project_specific_status_replaces_brace_title(canonical_handlers):
    metadata = {
        "has_github": True,
        "repository": "acme/rocket",
        "open_issues_count": 2,
        "issues_preview": [
            {"number": 100, "title": "{"},
            {"number": 7, "title": "v2"},
        ],
    }
    out = canonical_handlers._format_project_specific_status(
        "rocket", metadata, user_context=None, spatial_pattern="GRANULAR"
    )
    assert "(untitled issue #100)" in out
    assert "{" not in out
    assert "v2" in out
