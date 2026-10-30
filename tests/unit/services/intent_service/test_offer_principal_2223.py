"""#2223 — an armed offer is acted on only under the principal that armed it.

Arch's ruling (decisions.log 2026-10-30 10:36 PT). The #846 store is
session-keyed and ``/api/v1/intent`` takes optional auth, so an anonymous turn
(or another user's) could pop an authenticated user's offer; the generic accept
then dispatched ``confirm_pending_action``, which re-dispatched the STORED
Intent carrying the arming user. Arch's probe on d59c5a2fc4: an anonymous "yes"
on the #1567 closed default question dispatched ``update_issue`` with the
arming user in its context.

These pins drive the REAL ``process_intent`` (model boundary explosive, GitHub
patched at the router) and spy on ``dispatch_workflow``:

- anonymous "yes" on an armed repo question → nothing dispatched, offer gone;
- anonymous "yes" on an armed destructive close confirm → nothing dispatched;
- a DIFFERENT authenticated user's "yes" → offer dropped silently, nothing
  dispatched, no handler of the offer's kind called (Arch 11:14 (1));
- the SAME user's "yes" → the existing accept path, unchanged;
- an anonymously armed record (names no principal) whose workflow declares a
  non-READ effect → acted on only by an anonymous turn; a signed-in turn drops
  it (Arch 11:14 (2)); a READ or undeclared one is unchanged. The shrink-only
  exception list is pinned by size.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingError, IntentService
from services.intent_service import offer_principal as op
from services.intent_service.classifier import IntentClassifier
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
    build_confirmation_offer,
)
from services.intent_service.repo_clarification import RepoNameResolution
from services.shared_types import IntentCategory

ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
RESOLVER = "services.integrations.github.repo_resolver"
REPO_CLAR = "services.intent_service.repo_clarification"
DISPATCH = "services.intent_service.workflow_dispatcher.dispatch_workflow"

_USER = "3f7b8a52-2223-4b00-9e00-000000002223"
_OTHER = "3f7b8a52-2223-4b00-9e00-0000000000bb"

# What an accepted offer of these kinds dispatches; none may run off a
# dropped offer.
_HELD = {CONFIRM_PENDING_ACTION_WORKFLOW, "update_issue", "close_issue"}


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@pytest.fixture
def service():
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            clf = IntentClassifier(llm_service=_ExplosiveLLM())
            return IntentService(intent_classifier=clf)


def _pending(service, sid):
    return service.workflow_offer_service._pending_offers.get(sid)


async def _arm_repo_question(service, sid):
    """The #1567 closed default question ('say yes to use your default'),
    armed by the REAL update handler for _USER, with a held title update."""
    ask = "change the title of issue 108 to Testing in the test-Piper-Morgan repository"
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="update_issue",
        original_message=ask,
        confidence=1.0,
        context={"original_message": ask, "user_id": _USER},
    )
    with (
        patch(f"{ROUTER}.initialize", new=AsyncMock()),
        patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        patch(
            f"{RESOLVER}.get_user_default_repo",
            new=AsyncMock(return_value="mediajunkie/piper-thing"),
        ),
        patch(
            f"{REPO_CLAR}.resolve_repo_name",
            new=AsyncMock(return_value=RepoNameResolution(status="not_found")),
        ),
    ):
        await service._handle_update_issue(intent, "wf-2223", session_id=sid, user_id=_USER)
    offer = _pending(service, sid)
    assert offer is not None and offer["pending_action"]["kind"] == "issue_repo_question"


def _arm_close_confirm(service, sid, user_id=_USER):
    """The #1190 destructive close confirm, built by the REAL builder from a
    close intent stamped (as the host boundary stamps it) with ``user_id``."""
    ctx = {"original_message": "close issue #108"}
    if user_id:
        ctx["user_id"] = user_id
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="close_issue",
        original_message="close issue #108",
        confidence=1.0,
        context=ctx,
    )
    confirmation = build_confirmation_offer(intent)
    service.workflow_offer_service.set_pending_offer(sid, confirmation.offer, user_id=user_id)
    assert _pending(service, sid) is not None


async def _say(service, sid, message, user_id):
    """One turn through process_intent with dispatch spied and the GitHub
    write explosive unless ``write`` is given. A dropped offer routes the turn
    normally, which may reach the explosive model boundary: that is proof no
    offer seam claimed it, and is tolerated."""
    from services.intent_service import workflow_dispatcher as wd

    real = wd.dispatch_workflow
    spy = AsyncMock(side_effect=real)
    closed = {"number": 108, "title": "t", "state": "closed", "html_url": ""}
    write = AsyncMock(return_value=closed)
    result = None
    with (
        patch(DISPATCH, new=spy),
        patch(f"{ROUTER}.initialize", new=AsyncMock()),
        patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        patch(f"{ROUTER}.update_issue", new=write),
    ):
        try:
            result = await service.process_intent(message=message, session_id=sid, user_id=user_id)
        except IntentProcessingError as exc:
            assert "LLM boundary touched" in str(exc) or "INTENT_CLASSIFICATION_FAILED" in str(
                exc
            ), str(exc)
    dispatched = [c.kwargs.get("workflow_type") for c in spy.await_args_list]
    return result, dispatched, write


class TestAnonymousYesDispatchesNothing:
    pytestmark = pytest.mark.asyncio

    async def test_anonymous_yes_on_repo_question(self, service):
        sid = "sess-2223-anon-repo"
        await _arm_repo_question(service, sid)
        with patch(f"{REPO_CLAR}.handle_repo_question_turn", new=AsyncMock()) as handler:
            result, dispatched, write = await _say(service, sid, "yes", None)
        handler.assert_not_awaited()
        assert not _HELD & set(dispatched), dispatched
        write.assert_not_awaited()
        assert _pending(service, sid) is None  # dropped, not re-armed
        if result is not None:
            assert "Updated issue" not in (result.message or "")

    async def test_anonymous_yes_on_close_confirm(self, service):
        sid = "sess-2223-anon-close"
        _arm_close_confirm(service, sid)
        result, dispatched, write = await _say(service, sid, "yes", None)
        assert not _HELD & set(dispatched), dispatched
        write.assert_not_awaited()
        assert _pending(service, sid) is None

    async def test_drop_is_logged_with_both_principals(self, service):
        from structlog.testing import capture_logs

        sid = "sess-2223-anon-log"
        _arm_close_confirm(service, sid)
        with capture_logs() as events:
            await _say(service, sid, "yes", None)
        drops = [e for e in events if e["event"] == "pending_offer_dropped_principal_mismatch"]
        assert len(drops) == 1
        assert drops[0]["reason"] == "recorded_principal_mismatch"
        assert drops[0]["offer_user"] == [_USER]
        assert drops[0]["turn_user"] is None
        assert drops[0]["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW


class TestDifferentUserYesDispatchesNothing:
    pytestmark = pytest.mark.asyncio

    async def test_other_user_yes_on_close_confirm(self, service):
        sid = "sess-2223-other-close"
        _arm_close_confirm(service, sid)
        result, dispatched, write = await _say(service, sid, "yes", _OTHER)
        assert not _HELD & set(dispatched), dispatched
        write.assert_not_awaited()
        assert _pending(service, sid) is None

    async def test_other_user_yes_on_repo_question_drops_silently(self, service):
        """Arch 11:14 (1): no handler of the offer's kind runs on a foreign
        principal's turn and nothing is rendered for the drop; the turn routes
        normally (here, toward the explosive model boundary)."""
        sid = "sess-2223-other-repo"
        await _arm_repo_question(service, sid)
        with patch(f"{REPO_CLAR}.handle_repo_question_turn", new=AsyncMock()) as handler:
            result, dispatched, write = await _say(service, sid, "yes", _OTHER)
        handler.assert_not_awaited()
        assert not _HELD & set(dispatched), dispatched
        write.assert_not_awaited()
        if result is not None:
            assert "hold off" not in (result.message or "")
            assert not (result.intent_data or {}).get("principal_mismatch")
        assert _pending(service, sid) is None


class TestSameUserYesUnchanged:
    pytestmark = pytest.mark.asyncio

    async def test_same_user_yes_on_close_confirm_runs_the_held_close(self, service):
        sid = "sess-2223-same-close"
        _arm_close_confirm(service, sid)
        result, dispatched, write = await _say(service, sid, "yes", _USER)
        # The existing accept path: the carrier re-dispatches the held close,
        # whose handler runs (here it reaches the #2205 repository ask, as the
        # unit environment has no default repository).
        assert dispatched[:2] == [CONFIRM_PENDING_ACTION_WORKFLOW, "close_issue"], dispatched
        assert result is not None and "#108" in result.message

    async def test_same_user_yes_on_repo_question_fires_the_held_update(self, service):
        sid = "sess-2223-same-repo"
        await _arm_repo_question(service, sid)
        result, dispatched, write = await _say(service, sid, "yes", _USER)
        # The kind handler binds the default and re-dispatches the held update.
        assert dispatched == ["update_issue"], dispatched
        assert write.await_count == 1
        assert write.await_args.kwargs["owner"] == "mediajunkie"


class TestUnrecordedPrincipalBehavesAsBefore:
    @pytest.mark.asyncio
    async def test_anonymous_armed_confirm_accepted_anonymously_as_today(self, service):
        """A record that names no principal (armed on an anonymous turn) is not
        touched by the check: the accept path runs exactly as before."""
        sid = "sess-2223-unrecorded"
        _arm_close_confirm(service, sid, user_id=None)
        assert op.recorded_offer_principals(_pending(service, sid)) == frozenset()
        result, dispatched, write = await _say(service, sid, "yes", None)
        assert dispatched[:2] == [CONFIRM_PENDING_ACTION_WORKFLOW, "close_issue"], dispatched

    @pytest.mark.asyncio
    async def test_anonymous_armed_write_offer_signed_in_yes_drops(self, service):
        """Arch 11:14 (2): an anonymously armed confirm (declared DESTRUCTIVE)
        is not acted on by a signed-in turn."""
        from structlog.testing import capture_logs

        sid = "sess-2223-anon-armed-signed-in"
        _arm_close_confirm(service, sid, user_id=None)
        with capture_logs() as events:
            result, dispatched, write = await _say(service, sid, "yes", _USER)
        assert not _HELD & set(dispatched), dispatched
        write.assert_not_awaited()
        assert _pending(service, sid) is None
        drops = [e for e in events if e["event"] == "pending_offer_dropped_principal_mismatch"]
        assert [d["reason"] for d in drops] == ["anonymous_write_offer_signed_in_turn"]
        assert drops[0]["offer_user"] == [] and drops[0]["turn_user"] == _USER

    @pytest.mark.asyncio
    async def test_anonymous_armed_read_offer_signed_in_yes_unchanged(self, service):
        """The soft ``meeting`` offer (declared READ) names no principal; a
        signed-in "yes" accepts it exactly as before."""
        from structlog.testing import capture_logs

        sid = "sess-2223-anon-meeting"
        service.workflow_offer_service.set_pending_offer(
            sid,
            {
                "workflow_type": "meeting",
                "offer_message": "Want me to help set up a meeting?",
                "question": "Want me to help set up a meeting?",
                "decline_message": "No worries.",
            },
            user_id=None,
        )
        with capture_logs() as events:
            result, dispatched, write = await _say(service, sid, "yes", _USER)
        assert dispatched[:1] == ["meeting"], dispatched
        assert not [e for e in events if e["event"] == "pending_offer_dropped_principal_mismatch"]

    def test_action_required_offer_is_undeclared_and_unchanged(self):
        """The canonical ``action_required`` offers name no principal and their
        workflows are unregistered (no declared effect): never dropped."""
        for wf in ("priority_check", "project_setup", "setup"):
            rec = {"workflow_type": wf, "action_required": wf}
            assert op.principal_drop_reason(rec, _USER) is None
            assert op.principal_drop_reason(rec, None) is None

    def test_exception_list_is_shrink_only(self):
        """SHRINK-ONLY: the write-effect offer kinds that cannot record their
        principal. Lower this number when one leaves; never raise it."""
        assert len(op.UNRECORDED_PRINCIPAL_WRITE_OFFER_KINDS) <= 0


class TestRecordedPrincipal:
    def _intent(self, user_id=None):
        ctx = {"user_id": user_id} if user_id else {}
        return Intent(
            category=IntentCategory.EXECUTION,
            action="close_issue",
            original_message="close issue #1",
            confidence=1.0,
            context=ctx,
        )

    def test_payload_user_and_intent_user_both_count(self):
        rec = {"pending_action": {"user_id": "a", "intent": self._intent("a")}}
        assert op.recorded_offer_principals(rec) == {"a"}
        assert op.offer_principal_mismatch(rec, "a") is False
        assert op.offer_principal_mismatch(rec, None) is True
        assert op.offer_principal_mismatch(rec, "b") is True

    def test_disagreeing_records_never_match(self):
        rec = {"pending_action": {"user_id": "a", "intent": self._intent("b")}}
        assert op.offer_principal_mismatch(rec, "a") is True
        assert op.offer_principal_mismatch(rec, "b") is True

    def test_no_principal_read_or_undeclared_never_mismatches(self):
        for rec in (
            {"workflow_type": "meeting"},
            {"pending_action": {"kind": "x", "user_id": None}},
            {"pending_action": {"intent": self._intent()}},
        ):
            assert op.offer_principal_mismatch(rec, None) is False
            assert op.offer_principal_mismatch(rec, "b") is False

    def test_no_principal_write_offer_acts_only_for_anonymous_turns(self):
        rec = {
            "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
            "pending_action": {"intent": self._intent()},
        }
        assert op.principal_drop_reason(rec, None) is None
        assert op.principal_drop_reason(rec, "b") == "anonymous_write_offer_signed_in_turn"

    def test_floor_bound_offer_records_its_principal(self):
        from services.intent_service.unarmed_offer import build_floor_bound_offer_record

        rec = build_floor_bound_offer_record(
            command="add a project called X",
            question="Want me to?",
            action="add_project",
            user_id=_USER,
        )
        assert op.recorded_offer_principals(rec) == {_USER}
        anon = build_floor_bound_offer_record(
            command="add a project called X", question="Want me to?", action="add_project"
        )
        assert "user_id" not in anon["pending_action"]


class TestStoreStampsTheArmingPrincipal:
    """The store records the arming principal on any record carrying a
    ``pending_action`` that names none, whatever arm site built it, so a
    signed-in arm is never mistaken for an anonymous one at the pop seam."""

    def _svc(self):
        from services.intent_service.soft_invocation import WorkflowOfferService

        return WorkflowOfferService()

    def test_signed_in_arm_stamps_a_record_naming_no_principal(self):
        svc = self._svc()
        original = {
            "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
            "pending_action": {"kind": "k"},
        }
        svc.set_pending_offer("s-stamp", original, user_id=_USER)
        stored = svc._pending_offers["s-stamp"]
        assert stored is original  # stamped in place: the arm site's record
        assert stored["pending_action"]["user_id"] == _USER

    def test_existing_principal_and_anonymous_arms_are_untouched(self):
        svc = self._svc()
        named = {"workflow_type": "x", "pending_action": {"kind": "k", "user_id": _OTHER}}
        svc.set_pending_offer("s-named", named, user_id=_USER)
        assert svc._pending_offers["s-named"] is named
        anon = {"workflow_type": "x", "pending_action": {"kind": "k"}}
        svc.set_pending_offer("s-anon", anon, user_id=None)
        assert svc._pending_offers["s-anon"] is anon

    def test_records_without_pending_action_are_untouched(self):
        svc = self._svc()
        soft = {"workflow_type": "meeting", "question": "Want me to?"}
        svc.set_pending_offer("s-soft", soft, user_id=_USER)
        assert svc._pending_offers["s-soft"] is soft
