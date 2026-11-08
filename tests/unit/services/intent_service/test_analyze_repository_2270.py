"""#2270 (Arch 2026-11-07 20:14; CXO 20:1x): "look at this repository, give me feedback".

Before this, ``analyze_repository`` had no handler and floored over the gathered baseline:
the advisor's exact words got a repo read, a "which repo" or a request to paste a document
(PA's table, 6 runs), a project name got another repo's issues, and nothing recorded the
read, so the TRUST floor next turn doubted it (and once confessed to inventing it).

Driven through the real ``process_intent`` (classification stubbed per turn, the floor's
``respond`` captured, GitHub stubbed at the router): turn 1 resolves, reads exactly one
repo, records it, and floors on that read alone; turn 2's TRUST floor carries the fact.
"""

from types import SimpleNamespace
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent_service import conversational_floor as cf
from services.intent_service.context_assembler import ContextAssembler
from services.shared_types import IntentCategory

_USER = "2270bbbb-0000-4000-8000-000000002270"
_REPO = "dinp-machine/piper-test-activity"
ADVISOR_TURN_1 = (
    "look at this project/repository. Give me quick feedback and then help me to move forward."
)
NAMED_TURN_1 = (
    f"look at the repository {_REPO}. Give me quick feedback and then help me to move forward."
)
TURN_2 = "I thought you had access to the GitHub repository. Did you actually look at it?"


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


def _classify_as(monkeypatch, service, category, action):
    async def _classify_multiple(msg, context=None, user_id=None, session_id=None):
        intent = Intent(
            category=category,
            action=action,
            original_message=msg,
            confidence=0.95,
            context={"original_message": msg},
        )
        return SimpleNamespace(
            intents=[intent],
            is_multi_intent=False,
            has_greeting=False,
            has_substantive_intent=True,
            primary_intent=intent,
            secondary_intents=[],
        )

    monkeypatch.setattr(service.intent_classifier, "classify_multiple", _classify_multiple)


@pytest.fixture
def github(monkeypatch):
    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    state = {
        "issues": [
            {"number": 43, "title": "D3 token check", "labels": ["safe-to-close"]},
            {"number": 38, "title": "search across nav", "labels": [], "milestone": "Beta launch"},
        ],
        "milestones": [
            {
                "title": "Beta launch",
                "due_on": "2026-10-29T00:00:00Z",
                "open_issues": 4,
                "closed_issues": 0,
            }
        ],
        "fail": False,
        "reads": [],
        "exists": {_REPO},
        "account_repos": [{"name": "piper-test-activity", "full_name": _REPO}],
    }

    async def _init(self, *a, **k):
        return None

    async def _issues(self, project=None, limit=10, owner=None, repo=None, *, strict=False):
        state["reads"].append(("issues", owner, repo))
        if state["fail"] or f"{owner}/{repo}" not in state["exists"]:
            raise RuntimeError("github: not found or down")
        return list(state["issues"])

    async def _milestones(self, state_="open", owner=None, repo=None, **k):
        state["reads"].append(("milestones", owner, repo))
        return list(state["milestones"])

    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

    async def _repos(self, user_id):
        return SimpleNamespace(degradation=None, repositories=list(state["account_repos"]))

    monkeypatch.setattr(GitHubMCPSpatialAdapter, "search_user_repositories", _repos)
    monkeypatch.setattr(GitHubIntegrationRouter, "initialize", _init)
    monkeypatch.setattr(GitHubIntegrationRouter, "get_open_issues", _issues)
    monkeypatch.setattr(
        GitHubIntegrationRouter,
        "list_milestones_via_mcp",
        lambda self, state="open", owner=None, repo=None: _milestones(self, state, owner, repo),
    )
    return state


@pytest.fixture
def captured_floor(monkeypatch):
    captured = []

    async def fake_respond(self, ctx):
        captured.append(ctx)
        return cf.FloorResponse(message="(stubbed floor answer)")

    monkeypatch.setattr(cf.ConversationalFloor, "respond", fake_respond)
    return captured


@pytest.fixture
def service(monkeypatch):
    from unittest.mock import patch

    import services.intent_service.context_assembler as ca
    from services.intent.intent_service import IntentService
    from services.intent_service.classifier import IntentClassifier
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()

    async def _clock(user_id):
        return ("", "")

    async def _no_gather(self, user_id=None, *a, **k):
        return {}

    monkeypatch.setattr(ca, "_current_time_and_date_for_user", _clock)
    monkeypatch.setattr(ContextAssembler, "_gather_trust_context", _no_gather)
    monkeypatch.setattr(ContextAssembler, "_gather_status_priority_context", _no_gather)
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            svc = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))
    return svc


def _default_repo(monkeypatch, service, repo):
    async def _resolve(user_id):
        return repo

    monkeypatch.setattr(service, "_resolve_default_repository", _resolve)


def _prompt(fc):
    return cf.ConversationalFloor()._build_prompt(fc)


pytestmark = pytest.mark.asyncio


async def _turn(service, monkeypatch, sid, message, category, action):
    _classify_as(monkeypatch, service, category, action)
    return await service.process_intent(message=message, session_id=sid, user_id=_USER)


async def test_named_repo_reads_records_and_the_trust_floor_states_it(
    service, monkeypatch, github, captured_floor
):
    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, None)
    await _turn(
        service, monkeypatch, sid, NAMED_TURN_1, IntentCategory.ANALYSIS, "analyze_repository"
    )
    assert github["reads"] == [
        ("issues", "dinp-machine", "piper-test-activity"),
        ("milestones", "dinp-machine", "piper-test-activity"),
    ]
    fc1 = captured_floor[-1]
    assert set(fc1.domain_context) <= {"repository_read", "current_time", "current_date"}
    p1 = _prompt(fc1)
    assert f"You read the GitHub repository {_REPO} this turn" in p1
    assert "#43 D3 token check" in p1 and "Beta launch: 4 open, 0 closed, due 2026-10-29" in p1

    await _turn(service, monkeypatch, sid, TURN_2, IntentCategory.TRUST, "explain_trust")
    p2 = _prompt(captured_floor[-1])
    assert (
        f"- Earlier this session you read {_REPO} (its open issues and milestones), just now." in p2
    )


async def test_the_advisors_unnamed_words_read_the_default_repo(
    service, monkeypatch, github, captured_floor
):
    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, _REPO)
    await _turn(
        service, monkeypatch, sid, ADVISOR_TURN_1, IntentCategory.ANALYSIS, "analyze_repository"
    )
    # The slot-fill reads "project/repository" from these words; it isn't a repo (no
    # read, not on the account), so the default stands in.
    assert github["reads"][0] == ("issues", "project", "repository")
    assert ("issues", "dinp-machine", "piper-test-activity") in github["reads"]
    assert captured_floor[-1].domain_context["repository_read"]["repository"] == _REPO


@pytest.mark.parametrize(
    "message", [ADVISOR_TURN_1, "give me quick feedback on my repo and help me move forward"]
)
async def test_no_repo_resolves_asks_the_armed_repo_question_never_a_document(
    service, monkeypatch, github, captured_floor, message
):
    from services.intent_service.repo_clarification import REPO_QUESTION_KIND, open_repo_question

    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, None)
    result = await _turn(
        service, monkeypatch, sid, message, IntentCategory.ANALYSIS, "analyze_repository"
    )
    assert result.message == open_repo_question(None, "give you feedback")
    offer = service.workflow_offer_service._pending_offers.get(sid)
    assert offer["pending_action"]["kind"] == REPO_QUESTION_KIND
    assert captured_floor == []
    assert "paste" not in result.message.lower()


async def test_a_failed_read_says_so_and_records_nothing(
    service, monkeypatch, github, captured_floor
):
    from services.intent.intent_service import ANALYZE_REPOSITORY_READ_FAILED_LINE

    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, None)
    github["fail"] = True
    result = await _turn(
        service, monkeypatch, sid, NAMED_TURN_1, IntentCategory.ANALYSIS, "analyze_repository"
    )
    assert result.message == ANALYZE_REPOSITORY_READ_FAILED_LINE.format(repository=_REPO)
    assert captured_floor == []
    await _turn(service, monkeypatch, sid, TURN_2, IntentCategory.TRUST, "explain_trust")
    assert "Earlier this session you read" not in _prompt(captured_floor[-1])


async def test_sentinel_turn_2_alone_claims_no_read(service, monkeypatch, github, captured_floor):
    sid = f"ar-{uuid4().hex[:8]}"
    await _turn(service, monkeypatch, sid, TURN_2, IntentCategory.TRUST, "explain_trust")
    assert "Earlier this session you read" not in _prompt(captured_floor[-1])
