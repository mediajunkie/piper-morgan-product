"""#1411 slice (PM live 2026-08-13 3:30–3:33 PM) — default-repo resolution +
clarify-first on unmapped status values in the update_issue slot-fill.

PM's transcript isolated two mechanisms this file pins, each with PM's exact
sentences as regression tests:

1. **Default repo never consulted**: "change the status of issue #108 to
   Done" → 'repository not specified' — even saying "in my default
   repository" explicitly. PM HAS a default repo (it powered the
   first-contact demo in the same session). The fix wires the SAME
   ``resolve_repo`` rail first_contact/#1590 already use into the update
   slot-fill, BEFORE the error; the error copy (now firing only when
   resolution also fails) teaches the conversational fix
   ("set my default repo to owner/name" — #1327, deterministically routed).

2. **'status → Done' has no mapping and asked nothing**: with the repo given
   explicitly → 'no fields to update specified'. Per PM's clarify-first
   ruling (decisions.log 2026-08-13 ~14:1x — unmapped verbs/values over
   stateful operations ASK, never map-by-decree), the handler now asks
   "By 'Done' do you mean close issue #108?" via the EXISTING #1190
   pending_action carrier (kind-distinguished); "yes" dispatches close_issue
   through the SAME confirm_pending_action path #1190 uses (PM live-verified
   end-to-end the same afternoon). No synonym table: nothing maps silently —
   every close-shaped value produces the ask, only "yes" acts.

Layer honesty (m-43): handler-level tests drive the REAL
``_handle_update_issue`` with the router and resolver patched at their
seams; end-to-end classes drive the REAL ``process_intent`` with an
EXPLOSIVE LLM (PM's sentence resolves deterministically at Stage 0 — proven
by test_explicit_issue_update_live_entry_1411) and the GitHub router patched
at the API boundary only.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
)
from services.shared_types import IntentCategory

ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
RESOLVER = "services.integrations.github.repo_resolver"

# PM's verbatim transcript sentences (2026-08-13 3:30–3:33 PM).
PM_STATUS_DONE = "change the status of issue #108 to Done"
PM_STATUS_DONE_DEFAULT_REPO = "change the status of issue #108 to Done in my default repository"

_USER = "3f7b8a52-1411-4b00-9e00-000000001411"  # valid UUID (resolve_repo takes UUIDs)


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM (forbidden:
    PM's sentence must resolve deterministically at Stage 0)."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — explicit issue updates resolve at Stage 0"
        )


class _FakeResolved:
    full_name = "mediajunkie/test-piper-morgan"


def _resolver_ok():
    return patch(f"{RESOLVER}.resolve_repo", new=AsyncMock(return_value=_FakeResolved()))


def _resolver_unresolved():
    from services.integrations.github.repo_resolver import UnresolvedRepoError

    return patch(f"{RESOLVER}.resolve_repo", new=AsyncMock(side_effect=UnresolvedRepoError()))


@pytest.fixture
def service():
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            clf = IntentClassifier(llm_service=_ExplosiveLLM())
            return IntentService(intent_classifier=clf)


def _update_intent(message: str) -> Intent:
    return Intent(
        category=IntentCategory.EXECUTION,
        action="update_issue",
        original_message=message,
        confidence=1.0,
        context={"original_message": message, "user_id": _USER},
    )


def _pending(service, sid):
    return service.workflow_offer_service._pending_offers.get(sid)


async def _handler_turn(service, message, sid="sess-1411", resolver=None):
    resolver_cm = resolver or _resolver_ok()
    with (
        patch(f"{ROUTER}.initialize", new=AsyncMock()),
        patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        resolver_cm,
    ):
        return await service._handle_update_issue(
            _update_intent(message), "wf-1411", session_id=sid, user_id=_USER
        )


# ---------------------------------------------------------------------------
# Extraction unit — the status-value detector
# ---------------------------------------------------------------------------


class TestUnmappedStatusValueDetection:
    def test_pm_exact_sentence_extracts_done(self):
        assert IntentService._detect_unmapped_status_value(PM_STATUS_DONE) == "Done"

    def test_trailing_repo_clause_is_not_part_of_the_value(self):
        """PM's 'in my default repository' phrasing — the value is 'Done'."""
        assert IntentService._detect_unmapped_status_value(PM_STATUS_DONE_DEFAULT_REPO) == "Done"

    def test_non_status_updates_do_not_extract(self):
        assert (
            IntentService._detect_unmapped_status_value("change the title of issue #108 to Testing")
            is None
        )

    def test_in_progress_extracts_but_is_not_close_shaped(self):
        value = IntentService._detect_unmapped_status_value(
            "change the status of issue #108 to in progress"
        )
        assert value == "in progress"
        assert value.lower() not in IntentService._CLOSE_SHAPED_STATUS_VALUES


# ---------------------------------------------------------------------------
# Mechanism 1 — default-repo resolution before the error
# ---------------------------------------------------------------------------


class TestDefaultRepoResolution:
    pytestmark = pytest.mark.asyncio

    async def test_pm_sentence_no_longer_dead_ends_on_repository(self, service):
        """PM's exact sentence, no repo in the message, default repo set →
        NOT the 'repository not specified' refusal. (It proceeds to the
        clarify-first ask — mechanism 2.)"""
        result = await _handler_turn(service, PM_STATUS_DONE)
        assert "repository not specified" not in result.message
        assert result.clarification_type != "repository_required"

    async def test_in_my_default_repository_phrasing_resolves(self, service):
        """PM said 'in my default repository' EXPLICITLY and still got the
        refusal. The slot-fill finds no owner/name pair in that phrase; the
        resolver supplies the default."""
        result = await _handler_turn(service, PM_STATUS_DONE_DEFAULT_REPO)
        assert "repository not specified" not in result.message

    async def test_resolution_failure_with_session_asks_instead_of_refusing(self, service):
        """#1567: with a session to bind the answer to, resolution failure is
        no longer a dead-end refusal — the handler ARMS the repo-question
        carrier and asks which repository (the answer slot-fills next turn)."""
        result = await _handler_turn(
            service, PM_STATUS_DONE, sid="sess-repo-ask", resolver=_resolver_unresolved()
        )
        assert result.success is True
        assert result.requires_clarification is True
        assert "Which repository is issue #108 in?" in result.message
        offer = _pending(service, "sess-repo-ask")
        assert offer is not None
        assert offer["pending_action"]["kind"] == "issue_repo_question"

    async def test_resolution_failure_without_session_teaches_the_conversational_fix(self, service):
        """With NO session there is nothing to bind an answer to, so the
        honest refusal stands — and it teaches 'set my default repo to
        owner/name' (#1327, a phrase that routes deterministically; #1571:
        never teach a phrase that doesn't)."""
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            _resolver_unresolved(),
        ):
            result = await service._handle_update_issue(
                _update_intent(PM_STATUS_DONE), "wf-1411", user_id=_USER
            )
        assert result.success is False
        assert result.clarification_type == "repository_required"
        assert "set my default repo to" in result.message

    async def test_explicit_repo_skips_the_resolver(self, service):
        """An explicitly-named repo is never second-guessed by the default."""
        explosive = patch(
            f"{RESOLVER}.resolve_repo",
            new=AsyncMock(side_effect=AssertionError("resolver consulted")),
        )
        updated = {"number": 108, "title": "t", "state": "open"}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.update_issue", new=AsyncMock(return_value=updated)) as w,
            explosive,
        ):
            result = await service._handle_update_issue(
                _update_intent(
                    'change the title of issue #108 to "Testing" in mediajunkie/test-piper-morgan'
                ),
                "wf-1411",
                session_id="sess-explicit",
                user_id=_USER,
            )
        assert result.success is True
        assert w.await_args.kwargs["owner"] == "mediajunkie"


# ---------------------------------------------------------------------------
# Mechanism 2 — clarify-first on the unmapped close-shaped status value
# ---------------------------------------------------------------------------


class TestClarifyFirstOnDoneStatus:
    pytestmark = pytest.mark.asyncio

    async def test_pm_sentence_asks_instead_of_erroring(self, service):
        """The PM-ruled ask, verbatim shape: names the value AND the candidate
        action, one yes/no. Never the 'no fields to update' dead end."""
        result = await _handler_turn(service, PM_STATUS_DONE, sid="sess-ask")
        assert result.success is True
        assert result.message == "By 'Done' do you mean close issue #108? (yes/no)"
        assert result.requires_clarification is True
        assert result.intent_data["unmapped_field_clarification_pending"] is True
        assert "no fields to update" not in result.message

    async def test_ask_rides_the_1190_carrier_with_distinct_kind(self, service):
        """The pending record is #1190's action-agnostic carrier (same
        workflow_type, same acceptance seam), kind-distinguished — no
        parallel offer mechanism."""
        await _handler_turn(service, PM_STATUS_DONE, sid="sess-carrier")
        offer = _pending(service, "sess-carrier")
        assert offer is not None
        assert offer["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        pa = offer["pending_action"]
        assert pa["kind"] == "unmapped_field_value_clarification"
        assert pa["action"] == "close_issue"
        assert pa["intent"].context["original_message"] == PM_STATUS_DONE
        assert pa["intent"].context["user_id"] == _USER  # #1532: principal rides

    async def test_non_close_value_falls_to_the_honest_error(self, service):
        """'in progress' has no plausible close mapping — no fabricated ask;
        the honest no-fields error stands (#1567/#1595 corpus territory)."""
        result = await _handler_turn(
            service,
            "change the status of issue #108 to in progress",
            sid="sess-nonclose",
        )
        assert result.success is False
        assert result.clarification_type == "update_fields_required"
        assert _pending(service, "sess-nonclose") is None

    async def test_no_session_falls_to_the_honest_error(self, service):
        """No session → nothing to bind the answer to → no dangling ask."""
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            _resolver_ok(),
        ):
            result = await service._handle_update_issue(
                _update_intent(PM_STATUS_DONE), "wf-1411", user_id=_USER
            )
        assert result.success is False
        assert result.clarification_type == "update_fields_required"


# ---------------------------------------------------------------------------
# End-to-end — PM's exact turns through the REAL process_intent
# ---------------------------------------------------------------------------


class TestEndToEndThroughRealProcessIntent:
    pytestmark = pytest.mark.asyncio

    async def _pm_turn(self, service, sid):
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            _resolver_ok(),
        ):
            return await service.process_intent(
                message=PM_STATUS_DONE, session_id=sid, user_id=_USER
            )

    async def test_pm_sentence_reaches_the_ask_deterministically(self, service):
        """PM's exact sentence through the live entry: Stage 0 routes it to
        update_issue with the LLM structurally unreachable, and the turn
        returns the clarify-first ask."""
        result = await self._pm_turn(service, "e2e-ask")
        assert "By 'Done' do you mean close issue #108?" in result.message
        assert _pending(service, "e2e-ask") is not None

    async def test_yes_closes_via_the_1190_confirm_path(self, service):
        """'yes' → the SAME confirm_pending_action path #1190 uses dispatches
        close_issue with the ORIGINAL params; the close executes in one turn
        (destructive_confirmed marker) — PM live-verified this exact close
        path end-to-end the same afternoon."""
        sid = "e2e-yes"
        await self._pm_turn(service, sid)
        closed = {
            "number": 108,
            "title": "testing regressions",
            "state": "closed",
            "html_url": "https://github.com/mediajunkie/test-piper-morgan/issues/108",
        }
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.update_issue", new=AsyncMock(return_value=closed)) as w,
        ):
            result = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
        w.assert_awaited_once_with(108, state="closed")
        assert "Closed issue #108" in result.message
        assert _pending(service, sid) is None

    async def test_no_cancels_honestly_and_nothing_fires(self, service):
        sid = "e2e-no"
        await self._pm_turn(service, sid)
        explosive_router = patch(
            f"{ROUTER}.update_issue",
            new=AsyncMock(side_effect=AssertionError("declined ask must never write")),
        )
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            explosive_router,
        ):
            result = await service.process_intent(message="no", session_id=sid, user_id=_USER)
        assert "I haven't changed issue #108" in result.message
        assert _pending(service, sid) is None
