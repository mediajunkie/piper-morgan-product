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

Lead review (2026-10-08) on the FIRST version of this gate (commit
81bc120df1, did NOT land): it read via ``GitHubIntegrationRouter.get_issue``
— the wrong path for alpha's OAuth-connected users, and a read whose
``None`` return collapses 401/403/404/network-error, so "clean None ⇒
not-found" could fire confidently on an auth/rate-limit failure. Fixed by
switching the existence check to ``GitHubMCPSpatialAdapter
.probe_issue_connector`` — a tri-state ("found"/"not_found"/"unknown") probe
(pinned directly, with a real in-memory MCP round-trip, in
``tests/unit/services/mcp/consumer/test_probe_issue_connector_1959.py``).
This file pins the GATE's consumption of that tri-state contract.

Layer honesty (m-43): unit-level tests drive ``build_close_reopen_confirmation``
directly with the PROBE mocked at the ``GitHubMCPSpatialAdapter`` boundary
(the probe's own classification logic is pinned separately, against a real
transport, in the sibling file named above — this file only pins what the
gate DOES with each of the three states). One end-to-end test drives the
REAL ``IntentService.process_intent`` rail to pin the exact user-visible
fix for the transcript above: one turn, no yes/no, the existing not-found
reply.
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

PROBE = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.probe_issue_connector"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"

_USER = "3f7b8a52-1959-4b00-9e00-000000001959"  # valid UUID: survives principal parsing
_REPO = "mediajunkie/test-piper-morgan"

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
        # user_id stamped in context: _principal_from_intent reads ONLY
        # this key (the process_intent host-boundary contract) — an
        # unstamped intent reads as "no principal" and the gate now
        # honestly falls back on that (AC #7), which would otherwise mask
        # every mocked-probe assertion below under the fallback path.
        context={"original_message": message, "user_id": _USER},
    )


@pytest.fixture
def service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            clf = IntentClassifier(llm_service=_ExplosiveLLM())
            return IntentService(intent_classifier=clf)


def _mock_probe(monkeypatch, *, status=None, item=None, resolved_repo=_REPO, side_effect=None):
    """Patch GitHubMCPSpatialAdapter.probe_issue_connector — the ONLY
    GitHub-read boundary the gate touches post-Lead-review. ``status`` is
    one of "found"/"not_found"/"unknown" (the tri-state contract; its
    classification logic is pinned separately against a real transport in
    test_probe_issue_connector_1959.py — this helper mocks its RETURN, not
    its internals)."""
    if side_effect is not None:
        mock = AsyncMock(side_effect=side_effect)
    else:
        mock = AsyncMock(return_value=(status, item, resolved_repo))
    monkeypatch.setattr(PROBE, mock)
    return mock


def _explosive_probe(monkeypatch):
    """The probe must NOT be called — used for legs where the gate bails
    before ever reaching the existence check (no number, repo
    unresolvable)."""

    async def _explode(self, *a, **k):
        raise AssertionError("probe_issue_connector called unexpectedly")

    monkeypatch.setattr(PROBE, _explode)


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

    async def test_no_issue_number_passes_through(self, service, monkeypatch):
        """No parseable number: both legs None — the handler's own 'which
        issue?' ask owns this turn, same invariant build_confirmation_offer
        already honors. The probe must never be reached."""
        _explosive_probe(monkeypatch)
        intent = _intent("close an issue please")
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate == CloseReopenGate()
        assert gate.offer is None
        assert gate.passthrough_result is None

    async def test_no_principal_falls_back_to_generic_confirm(self, service, monkeypatch):
        """AC #7: reads must use the acting user's OWN GitHub connection,
        never a shared/default token. An intent with no stamped user_id has
        no principal to scope the probe to — honest fallback, probe never
        reached."""
        _explosive_probe(monkeypatch)
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue_query",
            confidence=1.0,
            original_message="close issue 108 in mediajunkie/test-piper-morgan",
            context={"original_message": "close issue 108 in mediajunkie/test-piper-morgan"},
        )
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.passthrough_result is None
        assert gate.offer is not None
        assert "#108" in gate.offer.question

    async def test_not_found_returns_existing_reply_unarmed(self, service, monkeypatch):
        """The repo resolves (named explicitly); the probe reports
        not_found — the EXACT existing #1858 not-found reply, nothing
        armed."""
        _mock_probe(monkeypatch, status="not_found", item=None)
        intent = _intent("close issue 99999 in mediajunkie/test-piper-morgan")
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.offer is None
        assert gate.passthrough_result is not None
        assert gate.passthrough_result["message"] == _NOT_FOUND_REPLY
        assert gate.passthrough_result["requires_clarification"] is False

    async def test_reopen_not_found_mirrors_close(self, service, monkeypatch):
        _mock_probe(monkeypatch, status="not_found", item=None)
        intent = _intent(
            "reopen issue 99999 in mediajunkie/test-piper-morgan", action="reopen_issue_query"
        )
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.offer is None
        assert gate.passthrough_result["message"] == _NOT_FOUND_REPLY

    async def test_found_arms_confirm_with_real_title(self, service, monkeypatch):
        """Issue exists, open: arm the #1190 confirm, enriched with the real
        title fetched at resolve time — never a bare number-only question."""
        _mock_probe(monkeypatch, status="found", item={"title": "Login bug", "state": "open"})
        intent = _intent("close issue 108 in mediajunkie/test-piper-morgan")
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.passthrough_result is None
        assert gate.offer is not None
        assert "#108" in gate.offer.question
        assert "Login bug" in gate.offer.question
        assert "(yes/no)" in gate.offer.question
        assert gate.offer.offer["pending_action"]["action"] == "close_issue_query"

    async def test_reopen_found_arms_confirm_with_real_title(self, service, monkeypatch):
        _mock_probe(monkeypatch, status="found", item={"title": "Old bug", "state": "closed"})
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
        _mock_probe(monkeypatch, status="found", item={"title": "Login bug", "state": "closed"})
        intent = _intent("close issue 108 in mediajunkie/test-piper-morgan")
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.offer is None
        assert gate.passthrough_result["message"] == "Issue #108: Login bug is already closed."
        assert gate.passthrough_result["requires_clarification"] is False

    async def test_already_open_passes_through_unarmed(self, service, monkeypatch):
        _mock_probe(monkeypatch, status="found", item={"title": "Login bug", "state": "open"})
        intent = _intent(
            "reopen issue 108 in mediajunkie/test-piper-morgan", action="reopen_issue_query"
        )
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.offer is None
        assert gate.passthrough_result["message"] == "Issue #108: Login bug is already open."

    async def test_probe_unknown_falls_back_to_generic_confirm(self, service, monkeypatch):
        """(a)/(d) Lead's pins, consumed at the gate: the probe reports
        unknown (an auth/rate-limit/network failure on the read, OR a
        degradation like CONNECT_REQUIRED/STALE_TOKEN — the probe's own
        test file pins each cause separately) — never a block on the user,
        never a false not-found claim. Fall back to EXACTLY today's
        generic (unenriched) confirm."""
        _mock_probe(monkeypatch, status="unknown", item=None, resolved_repo=None)
        intent = _intent("close issue 108 in mediajunkie/test-piper-morgan")
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.passthrough_result is None
        assert gate.offer is not None
        assert "#108" in gate.offer.question
        assert "(yes/no)" in gate.offer.question
        # Unenriched: no title was ever fetched, so none can appear.
        assert "Login bug" not in gate.offer.question
        assert "There's no issue" not in gate.offer.question

    async def test_probe_raising_unexpectedly_falls_back(self, service, monkeypatch):
        """Defense in depth: even if the probe itself raised instead of
        returning its tri-state tuple (it shouldn't — it catches
        internally), the gate's own outer handler still falls back rather
        than propagating or guessing."""
        _mock_probe(monkeypatch, side_effect=RuntimeError("unexpected"))
        intent = _intent("close issue 108 in mediajunkie/test-piper-morgan")
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.passthrough_result is None
        assert gate.offer is not None
        assert "#108" in gate.offer.question

    async def test_repo_unresolvable_falls_back_to_generic_confirm(self, service, monkeypatch):
        """No repo named, and the quiet default-repo consult comes back
        empty: repo unresolvable, not not-found — the probe is never
        reached."""
        _explosive_probe(monkeypatch)
        monkeypatch.setattr(service, "_resolve_default_repository", AsyncMock(return_value=None))
        intent = _intent("close issue 108")  # no repo named at all
        gate = await build_close_reopen_confirmation(intent, service, "wf-1")
        assert gate.passthrough_result is None
        assert gate.offer is not None
        assert "#108" in gate.offer.question

    async def test_degenerate_found_result_falls_back_to_generic_confirm(
        self, service, monkeypatch
    ):
        """status=="found" but neither title nor state came back — honest-
        ambiguous, not definitive either way."""
        _mock_probe(monkeypatch, status="found", item={"number": 108})
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
        _mock_probe(monkeypatch, status="not_found", item=None)

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
