"""Issue 2437: a degraded probe answers the degrade's line and arms nothing.

Arch's rulings (decisions.log 2026-11-25 08:54, 08:55, 09:04, 09:05, 09:06) with CXO's
words: ``probe_issue_connector`` reports ``"degraded"`` with the ``DegradationResponse``
it holds; the close/reopen gate says ``close_reopen_degrade_line``'s line as a passthrough
marked DEGRADED (the rail adds the said-instead flag), arms no yes/no and writes nothing.
``"unknown"`` (served, no evidence) keeps the generic confirm. The after-yes reply from
``_github_gate_failed`` is marked DEGRADED with ``mark_not_performed`` (not said-instead),
and its stale line for close and reopen is the gate's constant.

The gate tests drive the real ``build_close_reopen_confirmation``; the rail tests drive the
real ``process_intent`` with only the probe, the App check and the classifier mocked.
"""

import ast
import inspect
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.integrations.github.read_failed import GitHubReadFailed
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.destructive_confirm import (
    build_close_reopen_confirmation,
    build_confirmation_offer,
)
from services.intent_service.not_performed import (
    NOT_PERFORMED_KEY,
    SAID_INSTEAD_KEY,
    NotPerformed,
    was_not_performed,
    was_said_instead,
)
from services.mcp.consumer import github_adapter as gh_mod
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import (
    GITHUB_APP_INSTALL_LINK_MISSING_REPLY,
    GITHUB_APP_NOT_INSTALLED_REPLY,
    GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY,
    GITHUB_APP_TOO_MANY_REPOSITORIES_REPLY,
    GITHUB_CLOSE_NOT_CONNECTED_REPLY,
    GITHUB_CLOSE_STALE_REPLY,
    GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
    GITHUB_REOPEN_NOT_CONNECTED_REPLY,
    GITHUB_REOPEN_STALE_REPLY,
    close_reopen_degrade_line,
)
from services.mcp.consumer.github_app_grant import REASON_CUTOVER
from services.mcp.consumer.github_app_install import (
    DETAIL_APP_INSTALL_LINK_MISSING,
    DETAIL_APP_NOT_INSTALLED,
    DETAIL_APP_NOT_ON_REPOSITORY,
    DETAIL_APP_TOO_MANY_REPOSITORIES,
)
from services.shared_types import IntentCategory

PROBE = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.probe_issue_connector"
APP_LINE = "services.mcp.consumer.github_adapter.github_app_write_refusal_line"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"

_USER = "3f7b8a52-2437-4b00-9e00-000000002437"
_REPO = "mediajunkie/test-piper-morgan"


# ── CXO's sentences, pinned once as literals ─────────────────────────────────


def test_the_new_sentences_are_cxos():
    assert GITHUB_CLOSE_STALE_REPLY == (
        "Your GitHub connection isn't working anymore. Reconnect it in Settings → "
        "Integrations, and I can close that issue."
    )
    assert GITHUB_REOPEN_STALE_REPLY == (
        "Your GitHub connection isn't working anymore. Reconnect it in Settings → "
        "Integrations, and I can reopen that issue."
    )
    assert GITHUB_CLOSE_NOT_CONNECTED_REPLY == (
        "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can "
        "close that issue."
    )
    assert GITHUB_REOPEN_NOT_CONNECTED_REPLY == (
        "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can "
        "reopen that issue."
    )
    assert GITHUB_ISSUE_COULD_NOT_CHECK_REPLY == (
        "I couldn't check that issue just now, so I haven't done anything. Try again in a "
        "moment; if it keeps failing, tell us."
    )


# ── The cases: (id, degradation, close line, reopen line) ────────────────────


def _deg(reason, detail=None):
    return DegradationResponse(reason=reason, user_message="(never read)", detail=detail)


R = DegradationReason
CASES = [
    ("stale", _deg(R.STALE_TOKEN), GITHUB_CLOSE_STALE_REPLY, GITHUB_REOPEN_STALE_REPLY),
    (
        "stale-cutover",
        _deg(R.STALE_TOKEN, REASON_CUTOVER),
        GITHUB_CLOSE_STALE_REPLY,
        GITHUB_REOPEN_STALE_REPLY,
    ),
    (
        "app-not-on-repository",
        _deg(R.REPO_UNRESOLVED, DETAIL_APP_NOT_ON_REPOSITORY),
        GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY,
        GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY,
    ),
    (
        "app-not-installed",
        _deg(R.REPO_UNRESOLVED, DETAIL_APP_NOT_INSTALLED),
        GITHUB_APP_NOT_INSTALLED_REPLY,
        GITHUB_APP_NOT_INSTALLED_REPLY,
    ),
    (
        "app-install-link-missing",
        _deg(R.REPO_UNRESOLVED, DETAIL_APP_INSTALL_LINK_MISSING),
        GITHUB_APP_INSTALL_LINK_MISSING_REPLY,
        GITHUB_APP_INSTALL_LINK_MISSING_REPLY,
    ),
    (
        "app-too-many",
        _deg(R.UNREACHABLE, DETAIL_APP_TOO_MANY_REPOSITORIES),
        GITHUB_APP_TOO_MANY_REPOSITORIES_REPLY,
        GITHUB_APP_TOO_MANY_REPOSITORIES_REPLY,
    ),
    (
        "connect-required",
        _deg(R.CONNECT_REQUIRED),
        GITHUB_CLOSE_NOT_CONNECTED_REPLY,
        GITHUB_REOPEN_NOT_CONNECTED_REPLY,
    ),
    (
        "not-configured",
        _deg(R.NOT_CONFIGURED),
        GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
        GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
    ),
    (
        "unreachable",
        _deg(R.UNREACHABLE),
        GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
        GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
    ),
    (
        "misconfigured",
        _deg(R.MISCONFIGURED),
        GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
        GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
    ),
    (
        "repo-unresolved",
        _deg(R.REPO_UNRESOLVED),
        GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
        GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
    ),
    (
        "resource-not-found-after-404-check",
        _deg(R.RESOURCE_NOT_FOUND),
        GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
        GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
    ),
]
VERBED = [
    pytest.param(deg, action, close if action.startswith("close") else reopen, id=f"{cid}-{verb}")
    for cid, deg, close, reopen in CASES
    for verb, action in (("close", "close_issue_query"), ("reopen", "reopen_issue_query"))
]


# ── The chooser ─────────────────────────────────────────────────────────────


@pytest.mark.parametrize("deg,action,line", VERBED)
def test_the_chooser_picks_by_reason_and_detail(deg, action, line):
    verb = "close" if action.startswith("close") else "reopen"
    assert close_reopen_degrade_line(deg, verb) is line


def test_the_chooser_never_reads_the_message():
    for _cid, deg, close, _reopen in CASES:
        other = DegradationResponse(
            reason=deg.reason, user_message="something else", detail=deg.detail
        )
        assert close_reopen_degrade_line(other, "close") is close


def test_the_chooser_refuses_another_verb():
    with pytest.raises(ValueError):
        close_reopen_degrade_line(_deg(R.STALE_TOKEN), "update")


def _chooser_tree():
    return ast.parse(inspect.getsource(gh_mod.close_reopen_degrade_line))


def test_every_return_is_an_upper_case_constant():
    returns = [n for n in ast.walk(_chooser_tree()) if isinstance(n, ast.Return)]
    assert returns
    for node in returns:
        assert isinstance(node.value, ast.Name), ast.dump(node)
        assert node.value.id.isupper(), node.value.id
        assert isinstance(getattr(gh_mod, node.value.id), str)


def test_every_degradation_reason_is_named_in_the_chooser():
    """A new DegradationReason member must be mapped here explicitly."""
    named = {
        n.attr
        for n in ast.walk(_chooser_tree())
        if isinstance(n, ast.Attribute)
        and isinstance(n.value, ast.Name)
        and n.value.id == "DegradationReason"
    }
    assert named == {m.name for m in DegradationReason}


@pytest.mark.parametrize("member", list(DegradationReason), ids=lambda m: m.name)
def test_every_reason_gets_a_constant_line_for_both_verbs(member):
    constants = {v for k, v in vars(gh_mod).items() if k.isupper() and isinstance(v, str)}
    for verb in ("close", "reopen"):
        assert close_reopen_degrade_line(_deg(member), verb) in constants


# ── Through the real gate ────────────────────────────────────────────────────


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@pytest.fixture
def service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _intent(message, action="close_issue_query", **extra):
    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        confidence=1.0,
        original_message=message,
        context={"original_message": message, "user_id": _USER, **extra},
    )


def _verb(action):
    return "close" if action.startswith("close") else "reopen"


@pytest.mark.asyncio
@pytest.mark.parametrize("deg,action,line", VERBED)
async def test_the_gate_answers_the_line_and_arms_nothing(service, monkeypatch, deg, action, line):
    monkeypatch.setattr(APP_LINE, AsyncMock(return_value=None))
    monkeypatch.setattr(PROBE, AsyncMock(return_value=("degraded", None, deg)))
    gate = await build_close_reopen_confirmation(
        _intent(f"{_verb(action)} issue 108 in {_REPO}", action=action), service, "wf"
    )
    assert gate.offer is None
    assert gate.passthrough_result == {
        "message": line,
        "requires_clarification": False,
        "intent_data": {NOT_PERFORMED_KEY: NotPerformed.DEGRADED, "repository": _REPO},
    }


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ["close_issue_query", "reopen_issue_query"])
async def test_unknown_still_arms_the_generic_confirm(service, monkeypatch, action):
    """Served, no evidence either way: the write may still succeed, so the confirm stays."""
    monkeypatch.setattr(APP_LINE, AsyncMock(return_value=None))
    monkeypatch.setattr(PROBE, AsyncMock(return_value=("unknown", None, None)))
    intent = _intent(f"{_verb(action)} issue 108 in {_REPO}", action=action)
    gate = await build_close_reopen_confirmation(intent, service, "wf")
    assert gate.passthrough_result is None
    assert gate.offer == build_confirmation_offer(intent)
    assert gate.offer.question == f"{_verb(action).capitalize()} issue #108 in {_REPO}? (yes/no)"


# ── Through the real process_intent rail ─────────────────────────────────────


class TestTheRail:
    pytestmark = pytest.mark.asyncio

    @pytest.fixture(autouse=True)
    def _rail(self, service, monkeypatch):
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()

        async def _classify(message, *args, **kwargs):
            action = "reopen_issue_query" if "reopen" in message else "close_issue_query"
            return Intent(
                category=IntentCategory.QUERY,
                action=action,
                confidence=1.0,
                original_message=message,
                context={"original_message": message},
            )

        async def _explosive_update(self, *a, **k):
            raise AssertionError("update_issue fired")

        monkeypatch.setattr(service.intent_classifier, "classify", _classify)
        monkeypatch.setattr(ROUTER + ".update_issue", _explosive_update)
        monkeypatch.setattr(APP_LINE, AsyncMock(return_value=None))

    async def _turn(self, service, message):
        sid = f"e2e-2437-{uuid4()}"
        result = await service.process_intent(message=message, session_id=sid, user_id=_USER)
        return result, service.workflow_offer_service._pending_offers.get(sid)

    @pytest.mark.parametrize("deg,action,line", VERBED)
    async def test_every_degrade_is_said_instead_with_nothing_armed(
        self, service, monkeypatch, deg, action, line
    ):
        monkeypatch.setattr(PROBE, AsyncMock(return_value=("degraded", None, deg)))
        result, pending = await self._turn(service, f"{_verb(action)} issue 108 in {_REPO}")
        assert pending is None
        assert result.message == line
        assert result.success is False
        assert result.requires_clarification is False
        assert result.intent_data[NOT_PERFORMED_KEY] == NotPerformed.DEGRADED
        assert result.intent_data[SAID_INSTEAD_KEY] is True
        assert was_said_instead(result)

    @pytest.mark.parametrize("verb", ["close", "reopen"])
    async def test_an_open_or_closed_issue_still_arms_its_question(
        self, service, monkeypatch, verb
    ):
        state = "open" if verb == "close" else "closed"
        monkeypatch.setattr(
            PROBE,
            AsyncMock(return_value=("found", {"title": "Login bug", "state": state}, _REPO)),
        )
        result, pending = await self._turn(service, f"{verb} issue 108 in {_REPO}")
        assert pending is not None
        assert result.message == f"{verb.capitalize()} issue #108 'Login bug' in {_REPO}? (yes/no)"
        assert not was_not_performed(result)

    async def test_not_found_is_unchanged(self, service, monkeypatch):
        monkeypatch.setattr(PROBE, AsyncMock(return_value=("not_found", None, _REPO)))
        result, pending = await self._turn(service, f"close issue 99999 in {_REPO}")
        assert pending is None
        assert result.success is False
        assert result.intent_data[NOT_PERFORMED_KEY] == NotPerformed.NOT_FOUND

    @pytest.mark.parametrize("verb,state", [("close", "closed"), ("reopen", "open")])
    async def test_already_in_state_is_unchanged(self, service, monkeypatch, verb, state):
        monkeypatch.setattr(
            PROBE,
            AsyncMock(return_value=("found", {"title": "Login bug", "state": state}, _REPO)),
        )
        result, pending = await self._turn(service, f"{verb} issue 108 in {_REPO}")
        assert pending is None
        assert result.message == f"Issue #108: Login bug is already {state}."
        assert result.intent_data[NOT_PERFORMED_KEY] == NotPerformed.ALREADY_IN_STATE

    async def test_unknown_still_arms(self, service, monkeypatch):
        monkeypatch.setattr(PROBE, AsyncMock(return_value=("unknown", None, None)))
        result, pending = await self._turn(service, f"close issue 108 in {_REPO}")
        assert pending is not None
        assert result.message == f"Close issue #108 in {_REPO}? (yes/no)"


# ── After a yes: the handler's reply ─────────────────────────────────────────


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "action,reason,expected",
    [
        ("close_issue_query", R.STALE_TOKEN, GITHUB_CLOSE_STALE_REPLY),
        ("reopen_issue_query", R.STALE_TOKEN, GITHUB_REOPEN_STALE_REPLY),
        (
            "close_issue_query",
            R.UNREACHABLE,
            "I couldn't check your GitHub connection just now, so I can't close that issue "
            "yet. Nothing was changed. Try again in a moment; if it keeps failing, tell us.",
        ),
        (
            "reopen_issue_query",
            R.UNREACHABLE,
            "I couldn't check your GitHub connection just now, so I can't reopen that issue "
            "yet. Nothing was changed. Try again in a moment; if it keeps failing, tell us.",
        ),
    ],
)
async def test_after_yes_the_reply_is_marked_degraded_not_said_instead(
    service, action, reason, expected
):
    msg = f"{_verb(action)} issue 108 in {_REPO}"
    intent = _intent(msg, action=action, destructive_confirmed=True, repository=_REPO)
    with (
        patch(f"{ROUTER}.initialize", AsyncMock()),
        patch(
            f"{ROUTER}.is_available",
            AsyncMock(side_effect=GitHubReadFailed("x", reason, detail=reason.value)),
        ),
    ):
        handler = (
            service._handle_close_issue_query
            if action.startswith("close")
            else service._handle_reopen_issue_query
        )
        result = await handler(intent, "wf")
    assert result.message == expected
    assert result.success is False
    assert result.intent_data[NOT_PERFORMED_KEY] == NotPerformed.DEGRADED
    assert was_not_performed(result)
    assert not was_said_instead(result)


def test_the_gate_and_the_after_yes_reply_share_the_stale_constant():
    """One fact, one constant (Arch 09:05)."""
    svc = IntentService.__new__(IntentService)
    svc.logger = MagicMock()
    rf = GitHubReadFailed("x", R.STALE_TOKEN, detail="stale_token")
    close = svc._github_gate_failed(rf, "close_issue", "close that issue").message
    reopen = svc._github_gate_failed(rf, "reopen_issue", "reopen that issue").message
    assert (
        close is GITHUB_CLOSE_STALE_REPLY is close_reopen_degrade_line(_deg(R.STALE_TOKEN), "close")
    )
    assert reopen is GITHUB_REOPEN_STALE_REPLY
    assert reopen is close_reopen_degrade_line(_deg(R.STALE_TOKEN), "reopen")
