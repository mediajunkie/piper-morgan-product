"""#1646 — the resolved repository REACHES the activity fetch.

#1641 made the ANALYSIS repository slot bindable (explicit > slot-fill >
natural phrasing > #1411 default > the ask) and every response message names
the resolved repo — but the fetch itself was
``get_recent_activity(days=days)``: whatever repo the GitHub agent is
internally configured for, attributed to the repo the user named. #1646
threads ``repository`` through the seam so the copy's claim and the query's
scope are the same repo (m-43: the message must not claim a scope the query
didn't have).

Layer honesty: the handler-level tests drive the REAL handlers with the
domain service patched at the ``_github_agent.get_recent_activity`` seam and
assert the RESOLVED repo arrives there. The e2e drives the answer turn
through the REAL ``process_intent`` with an EXPLOSIVE LLM (the arm is
handler-level — no deterministic classifier surface claims analysis
phrasings, same boundary as the #1641 suite).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.repo_clarification import RepoNameResolution
from services.shared_types import IntentCategory

RESOLVER = "services.integrations.github.repo_resolver"
REPO_CLAR = "services.intent_service.repo_clarification"
ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"
GH_DOMAIN = "services.domain.github_domain_service.GitHubDomainService"

_USER = "3f7b8a52-1646-4b00-9e00-000000001646"  # valid UUID
_FULL = "mediajunkie/test-piper-morgan"

NATURAL_ANSWER = "in the test-Piper-Morgan repository"


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — these turns resolve deterministically"
        )


@pytest.fixture
def service():
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            clf = IntentClassifier(llm_service=_ExplosiveLLM())
            return IntentService(intent_classifier=clf)


def _gh_domain(activity=None):
    activity = activity or {
        "commits": [],
        "prs": [],
        "issues_created": [],
        "issues_closed": [],
    }
    instance = MagicMock()
    instance._github_agent.get_recent_activity = AsyncMock(return_value=activity)
    return instance, patch(GH_DOMAIN, return_value=instance)


def _resolved_name():
    return patch(
        f"{REPO_CLAR}.resolve_repo_name",
        new=AsyncMock(return_value=RepoNameResolution(status="resolved", full_name=_FULL)),
    )


def _resolver_unresolved():
    from services.integrations.github.repo_resolver import UnresolvedRepoError

    return patch(f"{RESOLVER}.resolve_repo", new=AsyncMock(side_effect=UnresolvedRepoError()))


def _no_default():
    return patch(f"{RESOLVER}.get_user_default_repo", new=AsyncMock(return_value=None))


def _repos_result(*full_names):
    return MagicMock(
        degradation=None,
        repositories=[{"name": fn.split("/", 1)[1], "full_name": fn} for fn in full_names],
    )


def _adapter_with(*full_names):
    instance = MagicMock()
    instance.search_user_repositories = AsyncMock(return_value=_repos_result(*full_names))
    return patch(f"{ADAPTER}", return_value=instance)


def _intent(action, message, **extra_ctx):
    ctx = {"original_message": message, "user_id": _USER, **extra_ctx}
    return Intent(
        category=IntentCategory.ANALYSIS,
        action=action,
        original_message=message,
        confidence=1.0,
        context=ctx,
    )


class TestResolvedRepoReachesTheFetch:
    """The pin: whichever way ``repository`` resolves, the SAME value arrives
    at the ``get_recent_activity`` seam — never the bare ``days=`` call."""

    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize(
        "handler_attr,action",
        [
            ("_handle_analyze_commits", "analyze_commits"),
            ("_handle_generate_report", "generate_report"),
            ("_handle_analyze_data", "analyze_data"),
        ],
    )
    async def test_named_repo_reaches_the_activity_fetch(self, service, handler_attr, action):
        instance, gh = _gh_domain()
        with gh, _resolved_name():
            result = await getattr(service, handler_attr)(
                _intent(action, f"{action.replace('_', ' ')} in the test-Piper-Morgan repository"),
                "wf-1646",
            )
        assert result.success is True
        fetch = instance._github_agent.get_recent_activity
        assert fetch.await_count == 1
        assert fetch.await_args.kwargs["repository"] == _FULL
        assert fetch.await_args.kwargs["days"] == 7

    @pytest.mark.parametrize(
        "handler_attr,action",
        [
            ("_handle_analyze_commits", "analyze_commits"),
            ("_handle_generate_report", "generate_report"),
            ("_handle_analyze_data", "analyze_data"),
        ],
    )
    async def test_default_repo_reaches_the_activity_fetch(self, service, handler_attr, action):
        """#1411 default path: the repo nobody typed still scopes the fetch."""
        default = MagicMock(full_name=_FULL)
        instance, gh = _gh_domain()
        with gh, patch(f"{RESOLVER}.resolve_repo", new=AsyncMock(return_value=default)):
            result = await getattr(service, handler_attr)(
                _intent(action, "run the usual analysis for the last week"),
                "wf-1646",
            )
        assert result.success is True
        fetch = instance._github_agent.get_recent_activity
        assert fetch.await_count == 1
        assert fetch.await_args.kwargs["repository"] == _FULL

    async def test_explicit_context_repo_reaches_the_activity_fetch(self, service):
        """Explicit ``repository`` in intent context — the top of the consult
        chain — reaches the seam verbatim, days honored from context."""
        instance, gh = _gh_domain()
        with gh:
            result = await service._handle_analyze_commits(
                _intent("analyze_commits", "analyze commits", repository=_FULL, days=30),
                "wf-1646",
            )
        assert result.success is True
        fetch = instance._github_agent.get_recent_activity
        assert fetch.await_args.kwargs["repository"] == _FULL
        assert fetch.await_args.kwargs["days"] == 30

    async def test_message_names_the_repo_the_fetch_was_scoped_to(self, service):
        """The m-43 pin itself: the copy's named repo and the fetch's
        repository kwarg are the SAME string."""
        instance, gh = _gh_domain()
        with gh, _resolved_name():
            result = await service._handle_analyze_commits(
                _intent("analyze_commits", "analyze commits in the test-Piper-Morgan repository"),
                "wf-1646",
            )
        fetched_repo = instance._github_agent.get_recent_activity.await_args.kwargs["repository"]
        assert fetched_repo in result.message


class TestArmAnswerThreadsTheBoundRepo:
    """e2e through the REAL ``process_intent`` (explosive LLM): the armed
    repo question's ANSWER binds, the original analysis re-dispatches, and
    the BOUND repo reaches the activity fetch."""

    pytestmark = pytest.mark.asyncio

    def _pending(self, service, sid):
        return service.workflow_offer_service._pending_offers.get(sid)

    async def test_bound_answer_repo_reaches_the_activity_fetch(self, service):
        sid = "t-1646-e2e"
        with _resolver_unresolved():
            ask = await service._handle_analyze_commits(
                _intent("analyze_commits", "analyze commits from the last week"),
                "wf-1646",
                session_id=sid,
            )
        assert "Which repository should I use to analyze commits?" in ask.message
        assert self._pending(service, sid) is not None

        instance, gh = _gh_domain()
        with gh, _no_default(), _adapter_with(_FULL):
            result = await service.process_intent(
                message=NATURAL_ANSWER, session_id=sid, user_id=_USER
            )
        assert self._pending(service, sid) is None
        fetch = instance._github_agent.get_recent_activity
        assert fetch.await_count == 1
        assert fetch.await_args.kwargs["repository"] == _FULL
        assert f"No commits found in {_FULL}" in result.message
