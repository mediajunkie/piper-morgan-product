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
_OTHER = "dinp-machine/harbor-pilot"
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
        "exists": {_REPO, _OTHER},
        "account_repos": [{"name": "piper-test-activity", "full_name": _REPO}],
        # #2270 list form: the account's linked repos, and its projects' links.
        "linked": [_REPO, _OTHER],
        "projects": {
            "harbor pilot": ("Harbor Pilot", [_OTHER]),
            "mobile redesign": ("Mobile Redesign", []),
        },
    }

    import services.intent_service.repo_clarification as rc

    async def _linked(user_id):
        return None if state["linked"] is None else list(state["linked"])

    async def _project(user_id, name):
        return state["projects"].get(name.lower())

    monkeypatch.setattr(rc, "linked_github_repos", _linked)
    monkeypatch.setattr(rc, "project_linked_repos", _project)

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


async def test_the_advisors_unnamed_words_ask_even_with_a_default(
    service, monkeypatch, github, captured_floor
):
    """Arch 20:38: the slot-fill reads "project/repository" from these words; it fails
    to read and isn't on the account, so it ASKS, never falls to the default (code can't
    tell it from a typo of the person's own repo)."""
    from services.intent_service.repo_clarification import REPO_QUESTION_KIND

    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, _REPO)
    result = await _turn(
        service, monkeypatch, sid, ADVISOR_TURN_1, IntentCategory.ANALYSIS, "analyze_repository"
    )
    assert github["reads"][0] == ("issues", "project", "repository")
    assert ("issues", "dinp-machine", "piper-test-activity") not in github["reads"]
    # CXO 20:02's list form: every linked repo, numbered, never "a couple others".
    assert result.message == (
        'I couldn\'t find "project/repository" among your repositories. '
        "Which repository do you want me to look at?\n\n"
        f"1. {_REPO}\n2. {_OTHER}\n\n"
        "Say the number or the name, or 'never mind' to leave them alone."
    )
    offer = service.workflow_offer_service._pending_offers.get(sid)
    assert offer["pending_action"]["kind"] == REPO_QUESTION_KIND
    assert captured_floor == []


async def test_a_typo_of_an_own_repo_asks_never_reads_the_default(
    service, monkeypatch, github, captured_floor
):
    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, _REPO)
    result = await _turn(
        service,
        monkeypatch,
        sid,
        "look at dinp-machine/piper-test-activty and give me feedback",
        IntentCategory.ANALYSIS,
        "analyze_repository",
    )
    assert ("issues", "dinp-machine", "piper-test-activity") not in github["reads"]
    assert result.requires_clarification and captured_floor == []
    assert result.message.startswith(
        'I couldn\'t find "dinp-machine/piper-test-activty" among your repositories.'
    )


async def test_the_default_read_names_the_repo_first_a_named_read_does_not(
    service, monkeypatch, github, captured_floor
):
    """Arch 20:50: when code chose the repo (the default), the first sentence says which;
    when the person named it, no lead."""
    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, _REPO)
    result = await _turn(
        service,
        monkeypatch,
        sid,
        "give me quick feedback on my repo and help me move forward",
        IntentCategory.ANALYSIS,
        "analyze_repository",
    )
    assert result.message == (
        f"Looking at {_REPO}, your default repository.\n\n(stubbed floor answer)"
    )
    named = await _turn(
        service,
        monkeypatch,
        f"ar-{uuid4().hex[:8]}",
        NAMED_TURN_1,
        IntentCategory.ANALYSIS,
        "analyze_repository",
    )
    assert named.message == "(stubbed floor answer)"


@pytest.mark.parametrize(
    "message", [ADVISOR_TURN_1, "give me quick feedback on my repo and help me move forward"]
)
async def test_no_repo_resolves_asks_the_armed_repo_question_never_a_document(
    service, monkeypatch, github, captured_floor, message
):
    from services.intent_service.repo_clarification import (
        LISTED_REPO_QUESTION_TAIL,
        REPO_QUESTION_KIND,
    )

    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, None)
    result = await _turn(
        service, monkeypatch, sid, message, IntentCategory.ANALYSIS, "analyze_repository"
    )
    # The advisor's words slot-fill "project/repository", so that ask opens with CXO's
    # couldn't-find sentence; either way it ends with the armed, numbered list.
    assert result.message.endswith(LISTED_REPO_QUESTION_TAIL)
    assert f"1. {_REPO}\n2. {_OTHER}" in result.message
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


# Alpha's live set as of 2026-11-07 (the #2112 test's ALPHA_LIVE).
_ALPHA_LIVE = (
    "add_project,complete_todo,create_reminder,create_todo,delete_todo,read_canonical,"
    "read_floor,read_portfolio,read_referent,read_status,read_strategic,read_synthesis,"
    "read_temporal"
)


async def test_landing_pin_the_routers_none_does_not_floor_the_hidden_entry(
    service, monkeypatch, github, captured_floor
):
    """Arch 20:26 (the #2132 ratchet raised to 2), condition 2: through process_intent with
    the advisor's exact words, a live consult that declines with router_none at 0.95 on
    alpha's live set leaves the legacy landing on the hidden entry standing."""
    import services.intent_service.inversion_live as il

    async def _router_none(*a, **k):
        il.publish_live_route_provenance(
            il.LiveRouteProvenance(routed_live=False, reason="router_none", confidence=0.95)
        )
        return None

    monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", _ALPHA_LIVE)
    monkeypatch.setattr(il, "consult_inversion_live", _router_none)
    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, _REPO)
    try:
        await _turn(
            service, monkeypatch, sid, ADVISOR_TURN_1, IntentCategory.ANALYSIS, "analyze_repository"
        )
    finally:
        il.publish_live_route_provenance(None)
    # The legacy landing stood: the hidden entry ran (it read the slot-filled pair, then
    # armed the repo question), and the floor was never reached.
    from services.intent_service.repo_clarification import REPO_QUESTION_KIND

    assert github["reads"][0] == ("issues", "project", "repository")
    assert captured_floor == []
    offer = service.workflow_offer_service._pending_offers.get(sid)
    assert offer["pending_action"]["kind"] == REPO_QUESTION_KIND


# ── #2270 list form (CXO 11-07 20:02): the answer binds a number or a project ──

UNNAMED = "give me quick feedback on my repo and help me move forward"


async def _ask_then_answer(service, monkeypatch, github, answer):
    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, None)
    await _turn(service, monkeypatch, sid, UNNAMED, IntentCategory.ANALYSIS, "analyze_repository")
    assert github["reads"] == []
    reply = await _turn(
        service, monkeypatch, sid, answer, IntentCategory.CONVERSATION, "small_talk"
    )
    return sid, reply


@pytest.mark.parametrize("answer", ["2", "2.", "dinp-machine/harbor-pilot", "harbor-pilot"])
async def test_a_number_or_a_name_reads_that_line(
    service, monkeypatch, github, captured_floor, answer
):
    sid, reply = await _ask_then_answer(service, monkeypatch, github, answer)
    assert github["reads"][0] == ("issues", "dinp-machine", "harbor-pilot")
    assert f"You read the GitHub repository {_OTHER} this turn" in _prompt(captured_floor[-1])
    assert reply.message == "(stubbed floor answer)"  # the person named it: no default lead


async def test_a_number_off_the_list_binds_nothing_and_asks_again(
    service, monkeypatch, github, captured_floor
):
    from services.intent_service.repo_clarification import listed_repo_question

    sid, reply = await _ask_then_answer(service, monkeypatch, github, "7")
    assert github["reads"] == [] and captured_floor == []
    assert reply.message == listed_repo_question([_REPO, _OTHER])
    offer = service.workflow_offer_service._pending_offers.get(sid)
    assert offer["pending_action"]["listed_repos"] == [_REPO, _OTHER]


async def test_a_project_name_reads_its_own_linked_repo(
    service, monkeypatch, github, captured_floor
):
    _, reply = await _ask_then_answer(service, monkeypatch, github, "Harbor Pilot")
    assert github["reads"][0] == ("issues", "dinp-machine", "harbor-pilot")
    # CXO 11-08: a project-name answer says which project it bound, first.
    assert reply.message == (
        f"Looking at {_OTHER}, the repository linked to Harbor Pilot.\n\n(stubbed floor answer)"
    )


async def test_a_project_with_no_repo_says_so_and_reads_nothing(
    service, monkeypatch, github, captured_floor
):
    from services.intent_service.repo_clarification import listed_repo_question

    sid, reply = await _ask_then_answer(service, monkeypatch, github, "Mobile Redesign")
    assert github["reads"] == [] and captured_floor == []
    assert reply.message == (
        "Mobile Redesign has no repository linked yet. You can link one on its project page."
        "\n\n" + listed_repo_question([_REPO, _OTHER])
    )
    assert service.workflow_offer_service._pending_offers.get(sid) is not None


async def test_none_linked_says_so(service, monkeypatch, github, captured_floor):
    from services.intent_service.repo_clarification import NONE_LINKED_LINE

    github["linked"] = []
    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, None)
    result = await _turn(
        service, monkeypatch, sid, UNNAMED, IntentCategory.ANALYSIS, "analyze_repository"
    )
    assert result.message == NONE_LINKED_LINE
    assert NONE_LINKED_LINE == (
        "I don't have a repository linked to your account yet, so there's nothing for me to "
        "look at. You can connect GitHub in Settings, under Integrations, or name a "
        'repository, like "look at owner/name".'
    )


async def test_an_unreadable_list_keeps_the_open_ask_never_none_linked(
    service, monkeypatch, github, captured_floor
):
    from services.intent_service.repo_clarification import open_repo_question

    github["linked"] = None
    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, None)
    result = await _turn(
        service, monkeypatch, sid, UNNAMED, IntentCategory.ANALYSIS, "analyze_repository"
    )
    assert result.message == open_repo_question(None, "give you feedback")


async def test_one_linked_repo_is_listed_and_asked_never_read_unasked(
    service, monkeypatch, github, captured_floor
):
    """CXO 11-08 07:0x: one linked repo is not a default; list it and ask."""
    from services.intent_service.repo_clarification import listed_repo_question

    github["linked"] = [_REPO]
    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, None)
    first = await _turn(
        service, monkeypatch, sid, UNNAMED, IntentCategory.ANALYSIS, "analyze_repository"
    )
    assert first.message == listed_repo_question([_REPO])
    # CXO 11-08: one line is singular.
    assert first.message.endswith("Say the number or the name, or 'never mind' to leave it alone.")
    assert f"\n\n1. {_REPO}\n\n" in first.message and github["reads"] == []
    reply = await _turn(service, monkeypatch, sid, "1", IntentCategory.CONVERSATION, "small_talk")
    assert github["reads"][0] == ("issues", "dinp-machine", "piper-test-activity")
    assert reply.message == "(stubbed floor answer)"


async def test_harbor_pilot_answer_binds_even_when_the_list_was_unreadable(
    service, monkeypatch, github, captured_floor
):
    """PA 11-08 07:06 (gap B): "Harbor Pilot", answered to the open ask, fell off the
    carrier and the floor put the test repo's issues under its name. The project name
    binds that project's own repo through the carrier, whatever the ask's form."""
    github["linked"] = None
    _, reply = await _ask_then_answer(service, monkeypatch, github, "Harbor Pilot")
    assert github["reads"][0] == ("issues", "dinp-machine", "harbor-pilot")
    assert f"You read the GitHub repository {_OTHER} this turn" in _prompt(captured_floor[-1])


# ── #2270 default-lead echo (CXO 11-08; Arch's mechanism): the repo is named once ──


async def test_the_echo_rule_drops_only_an_exact_looking_at_repo_opening():
    from services.intent.intent_service import _drop_repeated_repo_opening as drop

    r8 = (
        f"Looking at {_REPO}, a few things stand out right away.\n\n"
        "**The Beta launch milestone is overdue.**"
    )
    assert drop(r8, _REPO) == "**The Beta launch milestone is overdue.**"
    # A body that opens with a finding is unchanged.
    finding = f"The Beta launch milestone is overdue. Looking at {_REPO}, ..."
    assert drop(finding, _REPO) == finding
    # "Looking at" without the exact repo, or another repo, is unchanged.
    assert drop("Looking at your repo, things look fine. More.", _REPO).startswith("Looking at")
    assert drop(f"Looking at {_OTHER}, x. y", _REPO).startswith("Looking at")
    # No sentence end, or nothing after it: unchanged.
    assert drop(f"Looking at {_REPO} now", _REPO) == f"Looking at {_REPO} now"
    assert drop(f"Looking at {_REPO}.", _REPO) == f"Looking at {_REPO}."
    # A dot inside the repo name is not a sentence end.
    assert drop("Looking at a/b.js, two notes. Next.", "a/b.js") == "Next."


async def test_the_default_read_names_the_repo_once(service, monkeypatch, github):
    async def respond(self, ctx):
        respond.ctx = ctx
        return cf.FloorResponse(
            message=f"Looking at {_REPO}, a few things stand out right away.\n\nFinding one."
        )

    monkeypatch.setattr(cf.ConversationalFloor, "respond", respond)
    _default_repo(monkeypatch, service, _REPO)
    result = await _turn(
        service,
        monkeypatch,
        f"ar-{uuid4().hex[:8]}",
        UNNAMED,
        IntentCategory.ANALYSIS,
        "analyze_repository",
    )
    assert result.message == f"Looking at {_REPO}, your default repository.\n\nFinding one."
    assert "start with the findings" in _prompt(respond.ctx)


async def test_a_named_read_is_never_touched(service, monkeypatch, github):
    body = f"Looking at {_REPO}, a few things stand out.\n\nFinding one."

    async def respond(self, ctx):
        respond.ctx = ctx
        return cf.FloorResponse(message=body)

    monkeypatch.setattr(cf.ConversationalFloor, "respond", respond)
    _default_repo(monkeypatch, service, None)
    result = await _turn(
        service,
        monkeypatch,
        f"ar-{uuid4().hex[:8]}",
        NAMED_TURN_1,
        IntentCategory.ANALYSIS,
        "analyze_repository",
    )
    assert result.message == body
    assert "start with the findings" not in _prompt(respond.ctx)


# ── #2270 gap B edge (Arch 11-08 07:18): an unbound answer re-asks once ───────


@pytest.mark.parametrize("words", ["the survey one", "Harbor Srvey"])
async def test_an_unbound_answer_that_routes_nowhere_reasks_and_reads_nothing(
    service, monkeypatch, github, captured_floor, words
):
    from services.intent_service.repo_clarification import listed_repo_question

    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, None)
    await _turn(service, monkeypatch, sid, UNNAMED, IntentCategory.ANALYSIS, "analyze_repository")
    reply = await _turn(
        service, monkeypatch, sid, words, IntentCategory.CONVERSATION, "clarification_needed"
    )
    assert reply.message == (
        f'I couldn\'t find "{words}" among your repositories or projects. '
        + listed_repo_question([_REPO, _OTHER])
    )
    assert github["reads"] == []
    offer = service.workflow_offer_service._pending_offers.get(sid)
    assert offer["pending_action"]["listed_repos"] == [_REPO, _OTHER]
    # A number now still binds the re-armed list.
    bound = await _turn(service, monkeypatch, sid, "1", IntentCategory.CONVERSATION, "small_talk")
    assert github["reads"][0] == ("issues", "dinp-machine", "piper-test-activity")
    assert bound.message == "(stubbed floor answer)"


async def test_the_second_miss_drops_the_ask(service, monkeypatch, github, captured_floor):
    from services.intent_service.repo_clarification import ANALYSIS_ASK_DROP_LINE

    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, None)
    await _turn(service, monkeypatch, sid, UNNAMED, IntentCategory.ANALYSIS, "analyze_repository")
    await _turn(
        service,
        monkeypatch,
        sid,
        "the survey one",
        IntentCategory.CONVERSATION,
        "clarification_needed",
    )
    second = await _turn(
        service,
        monkeypatch,
        sid,
        "Harbor Srvey",
        IntentCategory.CONVERSATION,
        "clarification_needed",
    )
    assert second.message == (
        "I still couldn't find \"Harbor Srvey\", so I haven't looked at anything. "
        "Tell me a repository as owner/name whenever you want me to look."
    )
    assert ANALYSIS_ASK_DROP_LINE.format(words="Harbor Srvey") == second.message
    assert service.workflow_offer_service._pending_offers.get(sid) is None
    assert github["reads"] == []


async def test_a_command_mid_ask_still_routes(service, monkeypatch, github, captured_floor):
    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, None)
    await _turn(service, monkeypatch, sid, UNNAMED, IntentCategory.ANALYSIS, "analyze_repository")
    reply = await _turn(
        service,
        monkeypatch,
        sid,
        "add a todo to call the vet",
        IntentCategory.EXECUTION,
        "create_todo",
    )
    assert "among your repositories or projects" not in (reply.message or "")


async def test_a_project_bound_read_drops_an_echoing_opening(service, monkeypatch, github):
    """The exact-match strip applies to the project lead too (CXO 11-08, Arch 08:16)."""

    async def respond(self, ctx):
        return cf.FloorResponse(message=f"Looking at {_OTHER}, two things.\n\nFinding one.")

    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, None)
    await _turn(service, monkeypatch, sid, UNNAMED, IntentCategory.ANALYSIS, "analyze_repository")
    monkeypatch.setattr(cf.ConversationalFloor, "respond", respond)
    reply = await _turn(
        service, monkeypatch, sid, "Harbor Pilot", IntentCategory.CONVERSATION, "small_talk"
    )
    assert reply.message == (
        f"Looking at {_OTHER}, the repository linked to Harbor Pilot.\n\nFinding one."
    )


# ── Arch 11-08 08:48/08:49: the re-ask at the floor's door; the dash fragment ──


async def test_the_reask_makes_no_floor_model_call_and_is_stamped_analysis(
    service, monkeypatch, github, captured_floor
):
    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, None)
    await _turn(service, monkeypatch, sid, UNNAMED, IntentCategory.ANALYSIS, "analyze_repository")
    reply = await _turn(
        service,
        monkeypatch,
        sid,
        "the survey one",
        IntentCategory.CONVERSATION,
        "clarification_needed",
    )
    assert reply.message.startswith('I couldn\'t find "the survey one"')
    assert captured_floor == []  # no composition was made and thrown away
    assert reply.intent_data["category"] == "analysis"
    assert reply.intent_data["action"] == "analyze_repository"
    second = await _turn(
        service,
        monkeypatch,
        sid,
        "Harbor Srvey",
        IntentCategory.CONVERSATION,
        "clarification_needed",
    )
    assert captured_floor == []
    assert second.intent_data == {"category": "analysis", "action": "analyze_repository"}


async def test_the_dash_fragment_rule():
    from services.intent.intent_service import _drop_dash_repo_fragment as drop

    n3 = f"Looking at **{_REPO}** —\n\nA few things jump out:\n- one"
    assert drop(n3, _REPO) == "A few things jump out:\n- one"
    assert drop(f"Looking at {_REPO} -\nNext.", _REPO) == "Next."
    # A complete first sentence is unchanged, even with the bold repo.
    whole = f"Looking at **{_REPO}**, two things stand out.\n\nOne."
    assert drop(whole, _REPO) == whole
    # Another repo, or no dash, or nothing after: unchanged.
    other = f"Looking at **{_OTHER}** —\n\nA."
    assert drop(other, _REPO) == other
    assert drop(f"Looking at **{_REPO}** —", _REPO) == f"Looking at **{_REPO}** —"


async def test_a_number_after_the_reask_reads_without_the_dash_fragment(
    service, monkeypatch, github
):
    """PA's n3 on 7f9aa353fa: `1` after a re-ask read the repo, and the body opened with
    a dangling `Looking at **repo** —`. A named read gets no lead; the fragment goes."""

    async def respond(self, ctx):
        return cf.FloorResponse(message=f"Looking at **{_REPO}** —\n\nA few things jump out:")

    sid = f"ar-{uuid4().hex[:8]}"
    _default_repo(monkeypatch, service, None)
    await _turn(service, monkeypatch, sid, UNNAMED, IntentCategory.ANALYSIS, "analyze_repository")
    await _turn(
        service,
        monkeypatch,
        sid,
        "the survey one",
        IntentCategory.CONVERSATION,
        "clarification_needed",
    )
    monkeypatch.setattr(cf.ConversationalFloor, "respond", respond)
    reply = await _turn(service, monkeypatch, sid, "1", IntentCategory.CONVERSATION, "small_talk")
    assert reply.message == "A few things jump out:"
