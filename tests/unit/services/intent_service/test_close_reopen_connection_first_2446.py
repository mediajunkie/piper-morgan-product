"""Issue 2446: close and reopen answer the connection before asking the repository.

Arch's mechanism (on the issue, 2026-11-26): in ``build_close_reopen_confirmation``,
right after the principal is known and before any repository resolution, the one
resolver ``GitHubMCPSpatialAdapter.resolve_credential`` is asked. A
``DegradationResponse`` is answered as a passthrough and arms nothing:
``CONNECT_REQUIRED`` says the never-connected line for the verb, marked NOT_CONNECTED;
any other degrade says ``close_reopen_degrade_line``'s line, marked DEGRADED. A
credential present changes nothing.

The gate tests drive the real ``build_close_reopen_confirmation`` with only the
resolver (and, on the connected legs, the write-target read, the App check and the
probe) stubbed. The rail tests drive the real ``process_intent`` with the classifier
stubbed, and read the pending-offer store for what was armed.
"""

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent.intent_service import WRITE_TARGET_ISSUE_QUESTION, IntentService
from services.intent_service import destructive_confirm as dc_mod
from services.intent_service.classifier import IntentClassifier
from services.intent_service.destructive_confirm import build_close_reopen_confirmation
from services.intent_service.not_performed import (
    NOT_PERFORMED_KEY,
    SAID_INSTEAD_KEY,
    NotPerformed,
)
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import (
    GITHUB_CLOSE_NOT_CONNECTED_REPLY,
    GITHUB_CLOSE_STALE_REPLY,
    GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
    GITHUB_REOPEN_NOT_CONNECTED_REPLY,
    GITHUB_REOPEN_STALE_REPLY,
    GitHubCredential,
)
from services.shared_types import IntentCategory

RESOLVE = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.resolve_credential"
PROBE = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.probe_issue_connector"
APP_LINE = "services.mcp.consumer.github_adapter.github_app_write_refusal_line"
WRITE_TARGET = "services.integrations.github.repo_resolver.get_user_write_target"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"

_USER = "3f7b8a52-2446-4b00-9e00-000000002446"
_REPO = "mediajunkie/test-piper-morgan"

R = DegradationReason
VERBS = [
    pytest.param("close_issue_query", GITHUB_CLOSE_NOT_CONNECTED_REPLY, id="close"),
    pytest.param("reopen_issue_query", GITHUB_REOPEN_NOT_CONNECTED_REPLY, id="reopen"),
]


def _deg(reason, detail=None):
    return DegradationResponse(reason=reason, user_message="(never read)", detail=detail)


_CONNECTED = GitHubCredential(owner_id=_USER, mcp_server_ref="github", token="t", leg="oauth")


def _verb(action):
    return "close" if action.startswith("close") else "reopen"


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@pytest.fixture
def service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _intent(message, action):
    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        confidence=1.0,
        original_message=message,
        context={"original_message": message, "user_id": _USER},
    )


@pytest.fixture
def nothing_past_the_resolver(monkeypatch, service):
    """Every step after the resolver raises, so a degrade that reached one would show."""

    def _boom(name):
        async def _a(*a, **k):
            raise AssertionError(f"{name} reached after a degrade")

        return _a

    monkeypatch.setattr(WRITE_TARGET, _boom("get_user_write_target"))
    monkeypatch.setattr(APP_LINE, _boom("the App check"))
    monkeypatch.setattr(PROBE, _boom("the probe"))
    monkeypatch.setattr(
        dc_mod,
        "_repository_first_offer",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("repository question built")),
    )
    monkeypatch.setattr(
        service,
        "_slotfill_issue_request",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("repository slot-fill ran")),
    )


# ── CXO's words, and one constant per verb ───────────────────────────────────


def test_the_never_connected_lines_are_cxos():
    assert GITHUB_CLOSE_NOT_CONNECTED_REPLY == (
        "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can "
        "close that issue."
    )
    assert GITHUB_REOPEN_NOT_CONNECTED_REPLY == (
        "GitHub isn't connected yet. Connect it in Settings → Integrations, and I can "
        "reopen that issue."
    )


def test_the_gate_carries_no_second_copy_of_the_sentence():
    import inspect

    source = inspect.getsource(build_close_reopen_confirmation)
    assert "isn't connected yet" not in source


# ── Never connected: the line, first turn, nothing armed ─────────────────────


@pytest.mark.asyncio
@pytest.mark.parametrize("action,line", VERBS)
@pytest.mark.parametrize(
    "message",
    [
        pytest.param("{verb} issue 999999", id="no-repository-named"),
        pytest.param("{verb} issue 999999 in " + _REPO, id="repository-named"),
    ],
)
async def test_never_connected_says_so_before_any_repository_question(
    service, monkeypatch, nothing_past_the_resolver, action, line, message
):
    resolver = AsyncMock(return_value=_deg(R.CONNECT_REQUIRED))
    monkeypatch.setattr(RESOLVE, resolver)
    gate = await build_close_reopen_confirmation(
        _intent(message.format(verb=_verb(action)), action), service, "wf"
    )
    assert gate.offer is None
    assert gate.passthrough_result == {
        "message": line,
        "requires_clarification": False,
        "intent_data": {NOT_PERFORMED_KEY: NotPerformed.NOT_CONNECTED},
    }
    assert gate.passthrough_result["message"] is line  # the constant object itself
    assert resolver.await_count == 1
    assert resolver.await_args.args[-1] == _USER


# ── Any other degrade: the existing degrade line, before any question ────────


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "deg,action,line",
    [
        pytest.param(
            _deg(R.STALE_TOKEN), "close_issue_query", GITHUB_CLOSE_STALE_REPLY, id="stale-close"
        ),
        pytest.param(
            _deg(R.STALE_TOKEN), "reopen_issue_query", GITHUB_REOPEN_STALE_REPLY, id="stale-reopen"
        ),
        pytest.param(
            _deg(R.UNREACHABLE),
            "close_issue_query",
            GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
            id="unreachable",
        ),
    ],
)
async def test_another_degrade_says_its_line_before_any_repository_question(
    service, monkeypatch, nothing_past_the_resolver, deg, action, line
):
    resolver = AsyncMock(return_value=deg)
    monkeypatch.setattr(RESOLVE, resolver)
    gate = await build_close_reopen_confirmation(
        _intent(f"{_verb(action)} issue 999999", action), service, "wf"
    )
    assert gate.offer is None
    assert gate.passthrough_result == {
        "message": line,
        "requires_clarification": False,
        "intent_data": {NOT_PERFORMED_KEY: NotPerformed.DEGRADED},
    }
    assert resolver.await_count == 1


# ── Connected: nothing changes ───────────────────────────────────────────────


@pytest.mark.asyncio
@pytest.mark.parametrize("action,_line", VERBS)
async def test_connected_with_no_default_still_asks_the_repository(
    service, monkeypatch, action, _line
):
    order = []

    async def _resolve(self, user_id):
        order.append("resolve")
        return _CONNECTED

    async def _no_default(user_id):
        order.append("write_target")
        return None

    real_offer = dc_mod._repository_first_offer

    def _offer(*a, **k):
        order.append("repository_question")
        return real_offer(*a, **k)

    monkeypatch.setattr(RESOLVE, _resolve)
    monkeypatch.setattr(WRITE_TARGET, _no_default)
    monkeypatch.setattr(dc_mod, "_repository_first_offer", _offer)
    monkeypatch.setattr(PROBE, AsyncMock(side_effect=AssertionError("probe before an answer")))

    gate = await build_close_reopen_confirmation(
        _intent(f"{_verb(action)} issue 999999", action), service, "wf"
    )
    assert gate.passthrough_result is None
    assert gate.offer.question == WRITE_TARGET_ISSUE_QUESTION.format(number=999999)
    assert gate.offer.offer["pending_action"]["then_confirm"] is True
    assert order == ["resolve", "write_target", "repository_question"]


@pytest.mark.asyncio
@pytest.mark.parametrize("action,_line", VERBS)
async def test_connected_with_a_repository_still_runs_the_app_check_and_the_probe(
    service, monkeypatch, action, _line
):
    monkeypatch.setattr(RESOLVE, AsyncMock(return_value=_CONNECTED))
    app = AsyncMock(return_value=None)
    probe = AsyncMock(return_value=("degraded", None, _deg(R.STALE_TOKEN)))
    monkeypatch.setattr(APP_LINE, app)
    monkeypatch.setattr(PROBE, probe)
    gate = await build_close_reopen_confirmation(
        _intent(f"{_verb(action)} issue 108 in {_REPO}", action), service, "wf"
    )
    assert app.await_count == 1
    assert probe.await_count == 1
    # The probe's degrade leg, unchanged (issue 2437): it carries the repository.
    assert gate.passthrough_result["intent_data"] == {
        NOT_PERFORMED_KEY: NotPerformed.DEGRADED,
        "repository": _REPO,
    }


# ── Through the real process_intent rail: one turn, nothing pending ──────────


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
        monkeypatch.setattr(RESOLVE, AsyncMock(return_value=_deg(R.CONNECT_REQUIRED)))

    @pytest.mark.parametrize("action,line", VERBS)
    async def test_never_connected_is_one_turn_with_nothing_pending(
        self, service, nothing_past_the_resolver, action, line
    ):
        sid = f"e2e-2446-{uuid4()}"
        result = await service.process_intent(
            message=f"{_verb(action)} issue 999999", session_id=sid, user_id=_USER
        )
        assert service.workflow_offer_service._pending_offers.get(sid) is None
        assert result.message == line
        assert result.success is False
        assert result.requires_clarification is False
        assert result.intent_data[NOT_PERFORMED_KEY] == NotPerformed.NOT_CONNECTED
        assert result.intent_data[SAID_INSTEAD_KEY] is True
