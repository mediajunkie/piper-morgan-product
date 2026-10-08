"""#1959 / ADR-080 D2 — resolve close/reopen against real GitHub data BEFORE
the #1190 confirm, so a missing issue gets the existing "no such issue"
reply directly instead of a blind "Close issue #N? (yes/no)" that only
discovers the issue doesn't exist AFTER the user already said yes.

Found on alpha `99289b6690` (PM test-card re-test, 2026-10-07):

    USER:  close issue 99999 in mediajunkie/test-piper-morgan
    PIPER: Close issue #99999? (yes/no)
    USER:  yes
    PIPER: There's no issue #99999 in mediajunkie/test-piper-morgan —
           nothing was changed. Check the number and try again, or say
           'show open issues' to find it.

The fix under test: a third #1190 resolve-first gate
(``build_close_reopen_confirmation``), mirroring
``build_unlink_repo_confirmation``'s shape — resolve first, arm second,
nothing executes before the arm.

Layer honesty (m-43): unit-level tests drive ``build_close_reopen_confirmation``
directly with the GitHub read mocked at the router boundary (the same
``GitHubIntegrationRouter`` seam ``test_destructive_confirm_1190.py`` mocks).
One end-to-end test drives the REAL ``IntentService.process_intent`` rail to
pin the exact user-visible fix for the transcript above: one turn, no
yes/no, the existing not-found reply.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.destructive_confirm import (
    CloseReopenGate,
    build_close_reopen_confirmation,
    is_close_reopen_action,
)
from services.shared_types import IntentCategory

ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"

_USER = "3f7b8a52-1959-4b00-9e00-000000001959"  # valid UUID: survives principal parsing

_NOT_FOUND_REPLY = (
    "There's no issue #99999 in mediajunkie/test-piper-morgan — nothing was changed. "
    "Check the number and try again, or say 'show open issues' to find it."
)


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1959 turns resolve deterministically"
        )


def _intent(message, action="close_issue_query"):
    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        confidence=1.0,
        original_message=message,
        context={"original_message": message},
    )


@pytest.fixture
def service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            clf = IntentClassifier(llm_service=_ExplosiveLLM())
            return IntentService(intent_classifier=clf)


def _mock_router(monkeypatch, *, available=True, get_issue=None):
    """Patch the GitHubIntegrationRouter boundary the gate reads through —
    the same seam test_destructive_confirm_1190.py's _explosive_router
    patches. ``get_issue`` is an AsyncMock (return_value or side_effect) or
    None to leave it unpatched (so a call would explode on the real network
    boundary, proving it was never reached)."""

    async def _noop_init(self, user_id=None):
        return None

    async def _available(self):
        return available

    monkeypatch.setattr(ROUTER + ".initialize", _noop_init)
    monkeypatch.setattr(ROUTER + ".is_available", _available)
    if get_issue is not None:
        monkeypatch.setattr(ROUTER + ".get_issue", get_issue)
    else:

        async def _explosive_get_issue(self, *a, **k):
            raise AssertionError("github_router.get_issue called unexpectedly")

        monkeypatch.setattr(ROUTER + ".get_issue", _explosive_get_issue)


class TestIsCloseReopenAction:
    def test_close_and_reopen_families_recognized(self):
        for action in ("close_issue", "close_issue_query", "reopen_issue", "reopen_issue_query"):
            assert is_close_reopen_action(action) is True

    def test_other_actions_not_recognized(self):
        assert is_close_reopen_action("delete_todo") is False
        assert is_close_reopen_action("create_issue") is False
        assert is_close_reopen_action(None) is False


class TestResolveBeforeConfirm:
    pytestmark = pytest.mark.asyncio

    async def test_no_issue_number_passes_through(self, service):
        """No parseable number: both legs None — the handler's own 'which
        issue?' ask owns this turn, same invariant build_confirmation_offer
        already honors."""
        intent = _intent("close an issue please")
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate == CloseReopenGate()
        assert gate.offer is None
        assert gate.passthrough_result is None

    async def test_not_found_returns_existing_reply_unarmed(self, service, monkeypatch):
        """The repo resolves (named explicitly); the read comes back clean
        with nothing — the EXACT existing #1858 not-found reply, nothing
        armed."""
        _mock_router(monkeypatch, get_issue=AsyncMock(return_value=None))
        intent = _intent("close issue 99999 in mediajunkie/test-piper-morgan")
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.offer is None
        assert gate.passthrough_result is not None
        assert gate.passthrough_result["message"] == _NOT_FOUND_REPLY
        assert gate.passthrough_result["requires_clarification"] is False

    async def test_reopen_not_found_mirrors_close(self, service, monkeypatch):
        _mock_router(monkeypatch, get_issue=AsyncMock(return_value=None))
        intent = _intent(
            "reopen issue 99999 in mediajunkie/test-piper-morgan", action="reopen_issue_query"
        )
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.offer is None
        assert gate.passthrough_result["message"] == _NOT_FOUND_REPLY

    async def test_found_arms_confirm_with_real_title(self, service, monkeypatch):
        """Issue exists, open: arm the #1190 confirm, enriched with the real
        title fetched at resolve time — never a bare number-only question."""
        _mock_router(
            monkeypatch,
            get_issue=AsyncMock(return_value={"title": "Login bug", "state": "open"}),
        )
        intent = _intent("close issue 108 in mediajunkie/test-piper-morgan")
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.passthrough_result is None
        assert gate.offer is not None
        assert "#108" in gate.offer.question
        assert "Login bug" in gate.offer.question
        assert "(yes/no)" in gate.offer.question
        assert gate.offer.offer["pending_action"]["action"] == "close_issue_query"

    async def test_reopen_found_arms_confirm_with_real_title(self, service, monkeypatch):
        _mock_router(
            monkeypatch,
            get_issue=AsyncMock(return_value={"title": "Old bug", "state": "closed"}),
        )
        intent = _intent(
            "reopen issue 42 in mediajunkie/test-piper-morgan", action="reopen_issue_query"
        )
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.passthrough_result is None
        assert gate.offer is not None
        assert "#42" in gate.offer.question
        assert "Old bug" in gate.offer.question

    async def test_already_closed_passes_through_unarmed(self, service, monkeypatch):
        """The handler's own honest 'is already closed' copy, reused as a
        passthrough — never armed, never a redundant confirm."""
        _mock_router(
            monkeypatch,
            get_issue=AsyncMock(return_value={"title": "Login bug", "state": "closed"}),
        )
        intent = _intent("close issue 108 in mediajunkie/test-piper-morgan")
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.offer is None
        assert gate.passthrough_result["message"] == "Issue #108: Login bug is already closed."
        assert gate.passthrough_result["requires_clarification"] is False

    async def test_already_open_passes_through_unarmed(self, service, monkeypatch):
        _mock_router(
            monkeypatch,
            get_issue=AsyncMock(return_value={"title": "Login bug", "state": "open"}),
        )
        intent = _intent(
            "reopen issue 108 in mediajunkie/test-piper-morgan", action="reopen_issue_query"
        )
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.offer is None
        assert gate.passthrough_result["message"] == "Issue #108: Login bug is already open."

    async def test_read_error_falls_back_to_generic_confirm(self, service, monkeypatch):
        """The read itself errors: never a block on the user, never a false
        not-found claim — fall back to EXACTLY today's generic (unenriched)
        confirm."""
        _mock_router(
            monkeypatch, get_issue=AsyncMock(side_effect=RuntimeError("GitHub API hiccup"))
        )
        intent = _intent("close issue 108 in mediajunkie/test-piper-morgan")
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.passthrough_result is None
        assert gate.offer is not None
        assert "#108" in gate.offer.question
        assert "(yes/no)" in gate.offer.question
        # Unenriched: no title was ever fetched, so none can appear.
        assert "Login bug" not in gate.offer.question

    async def test_github_not_connected_falls_back_to_generic_confirm(self, service, monkeypatch):
        """GitHub not connected: an explicit fallback condition — the read
        is never attempted (get_issue stays unpatched/explosive)."""
        _mock_router(monkeypatch, available=False)
        intent = _intent("close issue 108 in mediajunkie/test-piper-morgan")
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.passthrough_result is None
        assert gate.offer is not None
        assert "#108" in gate.offer.question

    async def test_repo_unresolvable_falls_back_to_generic_confirm(self, service, monkeypatch):
        """No repo named, and the quiet default-repo consult comes back
        empty: repo unresolvable, not not-found — the read is never
        attempted."""
        _mock_router(monkeypatch)  # get_issue stays explosive: must not be called
        monkeypatch.setattr(service, "_resolve_default_repository", AsyncMock(return_value=None))
        intent = _intent("close issue 108")  # no repo named at all
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.passthrough_result is None
        assert gate.offer is not None
        assert "#108" in gate.offer.question

    async def test_degenerate_read_result_falls_back_to_generic_confirm(self, service, monkeypatch):
        """Neither title nor state came back (the legacy spatial-fallback
        degrade shape) — honest-ambiguous, not definitive either way."""
        _mock_router(monkeypatch, get_issue=AsyncMock(return_value={"number": 108}))
        intent = _intent("close issue 108 in mediajunkie/test-piper-morgan")
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.passthrough_result is None
        assert gate.offer is not None


class TestEndToEndNotFoundNeverArms:
    """Pins the exact user-visible fix for the reported transcript: one
    turn, no yes/no, the existing not-found reply — through the REAL rail
    (IntentService.process_intent), not just the unit-level builder."""

    pytestmark = pytest.mark.asyncio

    def _stub_classify(self, monkeypatch, service):
        async def _classify(message, *args, **kwargs):
            clean = message.lower()
            if "close issue" in clean:
                action = "close_issue_query"
            elif "reopen issue" in clean:
                action = "reopen_issue_query"
            else:
                raise AssertionError(
                    "LLM boundary touched — #1959 e2e turn resolves deterministically"
                )
            return Intent(
                category=IntentCategory.QUERY,
                action=action,
                confidence=1.0,
                original_message=message,
                context={"original_message": message},
            )

        monkeypatch.setattr(service.intent_classifier, "classify", _classify)

    async def test_not_found_in_one_turn_nothing_armed(self, service, monkeypatch):
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        _mock_router(monkeypatch, get_issue=AsyncMock(return_value=None))

        async def _explosive_update(self, *a, **k):
            raise AssertionError(
                "github_router.update_issue FIRED — a destructive mutation "
                "executed for an issue that was never confirmed to exist"
            )

        monkeypatch.setattr(ROUTER + ".update_issue", _explosive_update)
        self._stub_classify(monkeypatch, service)

        sid = "e2e-1959-not-found"
        result = await service.process_intent(
            message="close issue 99999 in mediajunkie/test-piper-morgan",
            session_id=sid,
            user_id=_USER,
        )
        assert result.message == _NOT_FOUND_REPLY
        assert "(yes/no)" not in result.message
        assert service.workflow_offer_service._pending_offers.get(sid) is None
