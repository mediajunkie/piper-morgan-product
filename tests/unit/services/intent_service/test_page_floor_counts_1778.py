"""#1778 / #1781 / #1782 — a count taken from a FULL API page is a FLOOR, not a total.

The #1776 class at the sites its census didn't reach: the GitHub list endpoints
return ONE page (per_page=100, unpaginated at our call sites), and the handlers
presented ``len(page)`` as the user-facing total. On any repo past 100 of a
thing, the user was told a number that is the cap, not the count. CXO §5b-i
decision 3 (already encoded in ``compose_capped_list.source_total_display``):
*a cap rendered as an exact number is a fabricated denominator — if the source
says 1000+, we say 1000+.* The family rule shipped here: full page → "N+",
short page → exact "N". Zero extra API calls.

LAYER (m-43): unit — the helper pure; the handlers through the real
IntentService with the LLM boundary explosive and the router mocked at the
gather seam; the assembler computes with the router mocked; the render lines
by direct call. DENOMINATOR: labels/branches/milestones/releases handlers, the
PR native-census branch (+ its OAuth control), the three assembler counts, the
first-contact block — every site the three issues name.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.list_remainder import GITHUB_LIST_PAGE_CAP, page_floor


class TestPageFloorHelper:
    def test_under_the_cap_is_exact(self):
        assert page_floor(37) == ("37", False)
        assert page_floor(0) == ("0", False)
        assert page_floor(99) == ("99", False)

    def test_at_and_over_the_cap_is_a_floor(self):
        assert page_floor(100) == ("100+", True)
        assert page_floor(150, page_cap=100) == ("150+", True)

    def test_cap_default_matches_the_github_page_size(self):
        assert GITHUB_LIST_PAGE_CAP == 100


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


def _label(n):
    return {"name": f"label-{n:03d}", "description": ""}


@pytest.fixture
def live_service():
    from services.intent.intent_service import IntentService
    from services.intent_service.classifier import IntentClassifier
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _intent(action):
    from services.domain.models import Intent
    from services.shared_types import IntentCategory

    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        confidence=1.0,
        context={"user_id": "5a2c9d10-1778-4b00-9e00-000000001778"},
    )


@pytest.mark.asyncio
class TestLabelsHandlerFloor:
    async def test_a_full_page_renders_the_floor_form(self, live_service):
        """THE #1781 pin: 100 labels back from an unpaginated per_page=100 read
        is the CAP — the headline must say 100+, not assert exactly 100."""
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter.list_labels_via_mcp",
            AsyncMock(return_value=[_label(i) for i in range(100)]),
        ):
            result = await live_service._handle_list_labels_query(
                _intent("list_labels_query"), "wf-1781"
            )

        assert "**100+ labels**" in result.message
        assert "**100 labels**" not in result.message

    async def test_a_short_page_stays_exact(self, live_service):
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter.list_labels_via_mcp",
            AsyncMock(return_value=[_label(i) for i in range(37)]),
        ):
            result = await live_service._handle_list_labels_query(
                _intent("list_labels_query"), "wf-1781b"
            )

        assert "**37 labels**" in result.message
        assert "37+" not in result.message


@pytest.mark.asyncio
class TestPrCensusFloor:
    async def test_full_issues_page_makes_the_pr_count_a_floor(self, live_service):
        """THE #1782 pin: pr_count filtered from a FULL open-issues page is
        'PRs among the first 100 open issues' — a floor, said as one."""
        from services.mcp.consumer.connector import DegradationReason, DegradationResponse
        from services.mcp.consumer.github_adapter import GitHubIssuesResult

        page = [{"number": i, "title": f"i{i}", "pull_request": (i % 4 == 0)} for i in range(100)]
        degraded = GitHubIssuesResult(
            degradation=DegradationResponse(
                reason=DegradationReason.CONNECT_REQUIRED, user_message="connect"
            ),
        )
        with (
            patch(
                "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_prs",
                AsyncMock(return_value=degraded),
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter.initialize",
                AsyncMock(),
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter.is_available",
                AsyncMock(return_value=True),
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter.get_open_issues",
                AsyncMock(return_value=page),
            ),
        ):
            result = await live_service._handle_list_prs_query(_intent("list_prs_query"), "wf-1782")

        assert "**25+ open PRs**" in result.message
        assert "first 100 open issues" in result.message

    async def test_short_issues_page_stays_exact(self, live_service):
        from services.mcp.consumer.connector import DegradationReason, DegradationResponse
        from services.mcp.consumer.github_adapter import GitHubIssuesResult

        page = [{"number": i, "title": f"i{i}", "pull_request": (i % 4 == 0)} for i in range(40)]
        degraded = GitHubIssuesResult(
            degradation=DegradationResponse(
                reason=DegradationReason.CONNECT_REQUIRED, user_message="connect"
            ),
        )
        with (
            patch(
                "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_prs",
                AsyncMock(return_value=degraded),
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter.initialize",
                AsyncMock(),
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter.is_available",
                AsyncMock(return_value=True),
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter.get_open_issues",
                AsyncMock(return_value=page),
            ),
        ):
            result = await live_service._handle_list_prs_query(
                _intent("list_prs_query"), "wf-1782b"
            )

        assert "**10 open PRs**" in result.message
        assert "10+" not in result.message
        assert "first 100" not in result.message


@pytest.mark.asyncio
class TestAssemblerFloorFlags:
    """#1778: the three context counts carry a capped flag the floor renders."""

    async def _assembler(self):
        from services.intent_service.context_assembler import ContextAssembler

        return ContextAssembler.__new__(ContextAssembler)

    async def test_high_priority_full_page_sets_the_flag(self):
        asm = await self._assembler()
        page = [{"number": i, "title": f"i{i}", "labels": [], "updated_at": ""} for i in range(100)]
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter.initialize",
                AsyncMock(),
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter.get_open_issues",
                AsyncMock(return_value=page),
            ),
        ):
            out = await asm._compute_high_priority_issues("u-1778")

        assert out["open_issue_count"] == 100
        assert out["open_issue_count_capped"] is True

    async def test_high_priority_short_page_does_not(self):
        asm = await self._assembler()
        page = [{"number": i, "title": f"i{i}", "labels": [], "updated_at": ""} for i in range(12)]
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter.initialize",
                AsyncMock(),
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter.get_open_issues",
                AsyncMock(return_value=page),
            ),
        ):
            out = await asm._compute_high_priority_issues("u-1778")

        assert out["open_issue_count_capped"] is False


class TestFloorRenderHonorsTheFlag:
    def test_domain_context_lines_render_the_plus(self):
        from services.intent_service.conversational_floor import ConversationalFloor

        floor = ConversationalFloor(llm_client=MagicMock())
        rendered = floor._format_domain_context(
            {
                "blocked_items": [{"number": 1, "title": "t"}],
                "blocked_count": 41,
                "blocked_count_capped": True,
                "high_priority_issues": [{"number": 2, "title": "u", "labels": []}],
                "open_issue_count": 100,
                "open_issue_count_capped": True,
            }
        )
        assert "41+" in rendered
        assert "100+" in rendered

    def test_unflagged_counts_stay_exact(self):
        from services.intent_service.conversational_floor import ConversationalFloor

        floor = ConversationalFloor(llm_client=MagicMock())
        rendered = floor._format_domain_context(
            {
                "blocked_items": [{"number": 1, "title": "t"}],
                "blocked_count": 4,
            }
        )
        assert "(4 open issues" in rendered
        assert "4+" not in rendered


class TestFirstContactFloor:
    def test_render_block_says_floor_on_a_full_page(self):
        from services.intent_service.first_contact import render_first_contact_block

        payload = {
            "connector": "github",
            "repo": "o/r",
            "items": [{"number": 1, "title": "t", "type": "issue", "recency": "today", "url": ""}],
            "open_count": 100,
            "open_count_capped": True,
        }
        block = render_first_contact_block(payload)
        assert "100+" in block

    def test_render_block_exact_when_not_capped(self):
        from services.intent_service.first_contact import render_first_contact_block

        payload = {
            "connector": "github",
            "repo": "o/r",
            "items": [{"number": 1, "title": "t", "type": "issue", "recency": "today", "url": ""}],
            "open_count": 7,
            "open_count_capped": False,
        }
        block = render_first_contact_block(payload)
        assert "7 open items" in block
        assert "7+" not in block
