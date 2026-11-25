"""Issue 2399: said-instead replies record that nothing was performed.

Arch's ruling (decisions.log, 2026-11-24 07:10 PT): three shared reply paths answered
``success=True`` when the reply said nothing was done. Each now answers ``success=False``
with the 2188 not-performed marker, and no reply text changes.

1. ``IntentService._rail_write_ask_reply`` keys on ``ask.armed``, never on the text. Armed:
   a clarification (``success`` True, ``requires_clarification``, no marker). Unarmed:
   ``success=False`` with the kind the builder set (2379's App line, DEGRADED) or else
   REFUSED_BEFORE_WRITE.
2. The close/reopen passthrough: not found NOT_FOUND, already closed/open ALREADY_IN_STATE,
   the App refusal DEGRADED. The builder sets the kind on its own branch.
3. The ``GitHubWriteRefused`` branch of ``_unverified_write_result``: REFUSED_BEFORE_WRITE.

Condition (consumers): a reader that changes the text on ``success=False`` reads the marker
first. Pinned here: the soft offer and the unanswered-half question
(``_apply_soft_offer``), and the Slack events path (``_process_through_orchestration``).

Texts are pinned from their constants (or from the builder's own output) wherever one
exists, never retyped.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.conversation_context import get_or_create_context
from services.intent_service.destructive_confirm import build_close_reopen_confirmation
from services.intent_service.not_performed import (
    NOT_PERFORMED_KEY,
    NOT_PERFORMED_KINDS,
    SAID_INSTEAD_KINDS,
    NotPerformed,
    mark_not_performed,
    was_not_performed,
    was_said_instead,
)
from services.intent_service.write_confirm_words import (
    ADD_PROJECT_NAME_QUESTION,
    NOT_SURE_STATEMENT,
    NOT_SURE_UPDATE_DOCUMENT,
    WriteAsk,
    WriteAskRequest,
    resolve_write_ask,
    update_document_write_ask,
)
from services.shared_types import IntentCategory

PROBE = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.probe_issue_connector"
APP_LINE = "services.mcp.consumer.github_adapter.github_app_write_refusal_line"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"

_USER = "3f7b8a52-2399-4b00-9e00-000000002399"
_REPO = "mediajunkie/test-piper-morgan"


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name}): 2399 turns are deterministic")


@pytest.fixture
def service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _intent(message, action="close_issue_query"):
    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        confidence=1.0,
        original_message=message,
        context={"original_message": message, "user_id": _USER},
    )


def _kind(result):
    return (result.intent_data or {}).get(NOT_PERFORMED_KEY)


class TestTheNewKind:
    def test_already_in_state_is_a_kind(self):
        assert NotPerformed.ALREADY_IN_STATE in NOT_PERFORMED_KINDS
        data = mark_not_performed(None, NotPerformed.ALREADY_IN_STATE)
        assert was_not_performed(SimpleNamespace(intent_data=data))

    def test_said_instead_kinds_are_the_two_only_these_paths_set(self):
        assert SAID_INSTEAD_KINDS == {
            NotPerformed.REFUSED_BEFORE_WRITE,
            NotPerformed.ALREADY_IN_STATE,
        }
        for kind in (NotPerformed.DEGRADED, NotPerformed.NOT_FOUND, NotPerformed.NOT_CONNECTED):
            assert not was_said_instead(SimpleNamespace(intent_data={NOT_PERFORMED_KEY: kind}))


# ── Path 1: the write ask's reply ──────────────────────────────────────────────


def _reply(ask, floor_write=False):
    intent = _intent("change it", action="update_document")
    return IntentService._rail_write_ask_reply(intent, ask, floor_write, None, None)


class TestWriteAskReply:
    pytestmark = pytest.mark.asyncio

    async def test_the_not_sure_statement_is_not_performed(self):
        """An entry that names nothing: resolve_write_ask's default statement."""
        entry = SimpleNamespace(write_ask=None)
        ask = await resolve_write_ask(entry, WriteAskRequest(intent=_intent("x"), message="x"))
        outcome = _reply(ask)
        result = outcome.result
        assert result.message == NOT_SURE_STATEMENT
        assert result.success is False
        assert _kind(result) == NotPerformed.REFUSED_BEFORE_WRITE
        assert result.requires_clarification is False
        assert outcome.armed is False

    async def test_a_statement_builder_is_not_performed(self):
        ask = await update_document_write_ask(
            WriteAskRequest(intent=_intent("x", action="update_document"), message="x")
        )
        result = _reply(ask, floor_write=True).result
        assert result.message == NOT_SURE_UPDATE_DOCUMENT
        assert result.success is False
        assert _kind(result) == NotPerformed.REFUSED_BEFORE_WRITE
        assert result.intent_data["floor_category_write"] is True

    async def test_the_app_line_keeps_its_degraded_kind(self):
        """2379's builder carries DEGRADED; the reply keeps it, not REFUSED_BEFORE_WRITE."""
        from services.intent_service.write_confirm_words import _app_not_on_repository
        from services.mcp.consumer.github_adapter import GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY

        with patch(APP_LINE, new=AsyncMock(return_value=GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY)):
            ask = await _app_not_on_repository(
                WriteAskRequest(intent=_intent("x"), message="x", user_id=_USER), _REPO
            )
        result = _reply(ask).result
        assert result.message == GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY
        assert result.success is False
        assert _kind(result) == NotPerformed.DEGRADED
        assert result.intent_data["repository"] == _REPO

    async def test_an_armed_question_is_a_clarification_with_no_marker(self):
        """add_project's name question, armed on its own carrier."""
        ask = WriteAsk(
            reply=ADD_PROJECT_NAME_QUESTION,
            armed=True,
            intent_data={"add_project_name_question_pending": True},
        )
        outcome = _reply(ask)
        result = outcome.result
        assert result.message == ADD_PROJECT_NAME_QUESTION
        assert result.success is True
        assert result.requires_clarification is True
        assert NOT_PERFORMED_KEY not in result.intent_data
        assert not was_not_performed(result)
        assert outcome.armed is True

    async def test_the_split_reads_armed_not_the_text(self):
        """The same words, armed or not, split only on ``armed``."""
        armed = _reply(WriteAsk(reply=NOT_SURE_STATEMENT, armed=True)).result
        unarmed = _reply(WriteAsk(reply=ADD_PROJECT_NAME_QUESTION)).result
        assert armed.success is True and not was_not_performed(armed)
        assert unarmed.success is False and _kind(unarmed) == NotPerformed.REFUSED_BEFORE_WRITE


# ── Path 2: the close/reopen passthrough ──────────────────────────────────────


def _mock_probe(monkeypatch, status, item=None):
    monkeypatch.setattr(PROBE, AsyncMock(return_value=(status, item, _REPO)))


def _no_app_refusal(monkeypatch):
    monkeypatch.setattr(APP_LINE, AsyncMock(return_value=None))


class TestCloseReopenBuilderSetsTheKind:
    pytestmark = pytest.mark.asyncio

    async def test_not_found_leg(self, service, monkeypatch):
        from services.integrations.github.github_integration_router import GitHubIssueNotFound

        _no_app_refusal(monkeypatch)
        _mock_probe(monkeypatch, "not_found")
        intent = _intent(f"close issue 99999 in {_REPO}")
        gate = await build_close_reopen_confirmation(intent, service, "wf")
        owner, name = _REPO.split("/")
        before = service._unverified_write_result(
            GitHubIssueNotFound(issue_number=99999, owner=owner, repo=name), intent, "wf"
        )
        assert gate.passthrough_result["message"] == before.message
        assert gate.passthrough_result["intent_data"] == {NOT_PERFORMED_KEY: NotPerformed.NOT_FOUND}

    @pytest.mark.parametrize(
        "action,state,word",
        [("close_issue_query", "closed", "closed"), ("reopen_issue_query", "open", "open")],
    )
    async def test_already_leg(self, service, monkeypatch, action, state, word):
        _no_app_refusal(monkeypatch)
        _mock_probe(monkeypatch, "found", {"title": "Login bug", "state": state})
        verb = "close" if action.startswith("close") else "reopen"
        gate = await build_close_reopen_confirmation(
            _intent(f"{verb} issue 108 in {_REPO}", action=action), service, "wf"
        )
        assert gate.passthrough_result["message"] == f"Issue #108: Login bug is already {word}."
        assert gate.passthrough_result["intent_data"] == {
            NOT_PERFORMED_KEY: NotPerformed.ALREADY_IN_STATE
        }

    async def test_found_and_mutable_still_arms(self, service, monkeypatch):
        _no_app_refusal(monkeypatch)
        _mock_probe(monkeypatch, "found", {"title": "Login bug", "state": "open"})
        gate = await build_close_reopen_confirmation(
            _intent(f"close issue 108 in {_REPO}"), service, "wf"
        )
        assert gate.passthrough_result is None
        assert gate.offer is not None


class TestCloseReopenPassthroughThroughTheRail:
    """Drives the real ``process_intent`` rail; the probe and the App check are mocked."""

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
            raise AssertionError("update_issue fired on a passthrough turn")

        monkeypatch.setattr(service.intent_classifier, "classify", _classify)
        monkeypatch.setattr(ROUTER + ".update_issue", _explosive_update)

    async def _turn(self, service, message):
        sid = f"e2e-2399-{uuid4()}"
        result = await service.process_intent(message=message, session_id=sid, user_id=_USER)
        assert service.workflow_offer_service._pending_offers.get(sid) is None
        return result

    async def test_not_found(self, service, monkeypatch):
        from services.integrations.github.github_integration_router import GitHubIssueNotFound

        _no_app_refusal(monkeypatch)
        _mock_probe(monkeypatch, "not_found")
        message = f"close issue 99999 in {_REPO}"
        owner, name = _REPO.split("/")
        expected = service._unverified_write_result(
            GitHubIssueNotFound(issue_number=99999, owner=owner, repo=name),
            _intent(message),
            "wf",
        ).message
        result = await self._turn(service, message)
        assert result.message == expected
        assert result.success is False
        assert _kind(result) == NotPerformed.NOT_FOUND
        assert result.requires_clarification is False

    async def test_already_closed(self, service, monkeypatch):
        _no_app_refusal(monkeypatch)
        _mock_probe(monkeypatch, "found", {"title": "Login bug", "state": "closed"})
        result = await self._turn(service, f"close issue 108 in {_REPO}")
        assert result.message == "Issue #108: Login bug is already closed."
        assert result.success is False
        assert _kind(result) == NotPerformed.ALREADY_IN_STATE

    async def test_already_open(self, service, monkeypatch):
        _no_app_refusal(monkeypatch)
        _mock_probe(monkeypatch, "found", {"title": "Login bug", "state": "open"})
        result = await self._turn(service, f"reopen issue 108 in {_REPO}")
        assert result.message == "Issue #108: Login bug is already open."
        assert result.success is False
        assert _kind(result) == NotPerformed.ALREADY_IN_STATE

    async def test_app_refusal(self, service, monkeypatch):
        from services.mcp.consumer.github_adapter import GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY

        monkeypatch.setattr(
            APP_LINE, AsyncMock(return_value=GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY)
        )
        monkeypatch.setattr(PROBE, AsyncMock(side_effect=AssertionError("probe ran")))
        result = await self._turn(service, f"close issue 108 in {_REPO}")
        assert result.message == GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY
        assert result.success is False
        assert _kind(result) == NotPerformed.DEGRADED


# ── Path 3: the refused-write handler ─────────────────────────────────────────


class TestGitHubWriteRefused:
    def _render(self, service, degradation):
        from services.integrations.github.github_integration_router import GitHubWriteRefused

        e = GitHubWriteRefused(
            user_message=degradation.user_message, action_hint=degradation.action_hint
        )
        return service._unverified_write_result(e, _intent("x", action="create_issue"), "wf")

    def test_unknown_tool_refusal(self, service):
        """2106: the server does not offer the tool. The text is the adapter's own words."""
        from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

        deg = GitHubMCPSpatialAdapter._unknown_tool_refusal("issue_write").degradation
        result = self._render(service, deg)
        assert result.message == f"{deg.user_message} {deg.action_hint}"
        assert result.success is False
        assert _kind(result) == NotPerformed.REFUSED_BEFORE_WRITE
        assert result.intent_data["write_refused"] is True
        assert result.requires_clarification is False
        assert result.error is None

    def test_app_not_on_repository_choke_point(self, service):
        """2379's choke point: no hint, the App line itself."""
        from services.mcp.consumer.github_adapter import GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY

        deg = SimpleNamespace(
            user_message=GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY, action_hint=None
        )
        result = self._render(service, deg)
        assert result.message == GITHUB_APP_NOT_ON_REPOSITORY_WRITE_REPLY
        assert result.success is False
        assert _kind(result) == NotPerformed.REFUSED_BEFORE_WRITE


# ── Consumers (Arch's condition) ──────────────────────────────────────────────


class TestSoftOfferAndUnansweredHalfReadTheMarker:
    """``_apply_soft_offer`` returned early on ``success=False`` and the unanswered-half
    question was dropped on it; a said-instead reply gets both exactly as before."""

    LINE = 'I haven\'t done "tell me a joke" yet. Want me to?'

    def _result(self, kind):
        return IntentProcessingResult(
            success=False,
            message="Nothing was written.",
            intent_data={"action": "create_issue", NOT_PERFORMED_KEY: kind},
        )

    def _open_soft_offer(self, service):
        from services.intent_service.soft_invocation import SoftInvocationResult, WorkflowOffer

        service.soft_invocation_detector.detect = MagicMock(
            return_value=SoftInvocationResult(
                has_offer=True,
                offer=WorkflowOffer(
                    workflow_type="project_setup",
                    offer_message="I could help set up a project. Want that?",
                    decline_message="No worries.",
                    confidence=0.9,
                ),
            )
        )
        service.workflow_offer_service.should_offer = MagicMock(return_value=(True, "open"))

    def test_refused_before_write_keeps_the_soft_offer(self, service):
        self._open_soft_offer(service)
        out = service._apply_soft_offer(
            self._result(NotPerformed.REFUSED_BEFORE_WRITE), "hi", str(uuid4()), user_id=_USER
        )
        assert "I could help set up a project. Want that?" in out.message
        assert out.success is False and was_not_performed(out)

    def test_other_kinds_keep_no_soft_offer(self, service):
        self._open_soft_offer(service)
        out = service._apply_soft_offer(
            self._result(NotPerformed.DEGRADED), "hi", str(uuid4()), user_id=_USER
        )
        assert out.message == "Nothing was written."
        service.soft_invocation_detector.detect.assert_not_called()

    def test_refused_before_write_keeps_the_unanswered_half_question(self, service):
        service.workflow_offer_service.should_offer = MagicMock(return_value=(False, "shut"))
        sid = str(uuid4())
        out = service._apply_soft_offer(
            self._result(NotPerformed.REFUSED_BEFORE_WRITE),
            "hi",
            sid,
            user_id=_USER,
            unanswered_half_suffix=self.LINE,
            unanswered_half_clause="tell me a joke",
        )
        assert out.message == f"Nothing was written.\n\n{self.LINE}"
        assert get_or_create_context(sid, user_id=_USER).last_offer.continuation_hint == (
            "tell me a joke"
        )

    def test_degraded_still_drops_the_question(self, service):
        sid = str(uuid4())
        out = service._apply_soft_offer(
            self._result(NotPerformed.DEGRADED),
            "hi",
            sid,
            user_id=_USER,
            unanswered_half_suffix=self.LINE,
            unanswered_half_clause="tell me a joke",
        )
        assert out.message.endswith('I haven\'t done "tell me a joke" yet.')
        assert get_or_create_context(sid, user_id=_USER).last_offer is None


class TestSlackKeepsAMarkedReply:
    """The Slack events path dropped any ``success=False`` result (no reply at all)."""

    pytestmark = pytest.mark.asyncio

    def _handler(self, result):
        from services.integrations.slack.response_handler import SlackResponseHandler

        handler = SlackResponseHandler(
            spatial_adapter=MagicMock(),
            intent_classifier=MagicMock(),
            slack_client=MagicMock(),
            intent_service=MagicMock(),
        )
        handler.intent_service.process_intent = AsyncMock(return_value=result)
        return handler

    async def _run(self, result):
        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_issue",
            original_message="file a bug about the header",
            confidence=0.95,
        )
        return await self._handler(result)._process_through_orchestration(
            intent, {"user_id": str(uuid4()), "workspace_id": "T1", "channel_id": "C1"}
        )

    async def test_marked_reply_is_sent_with_its_text(self):
        result = IntentProcessingResult(
            success=False,
            message=NOT_SURE_STATEMENT,
            intent_data={NOT_PERFORMED_KEY: NotPerformed.REFUSED_BEFORE_WRITE},
        )
        out = await self._run(result)
        assert out is not None and out["type"] == "workflow_result"
        assert out["result"]["message"] == NOT_SURE_STATEMENT

    async def test_unmarked_failure_is_still_dropped(self):
        out = await self._run(IntentProcessingResult(success=False, message="boom", intent_data={}))
        assert out is None
