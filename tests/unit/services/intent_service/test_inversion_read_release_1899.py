"""#1899 — the reads-only release for armed-carrier off-intent
discriminators.

Two armed-offer carriers (``todo_handlers.handle_reminder_task_turn`` /
#1654, ``first_contact.handle_ftux_interview_turn`` / #1688) decide "is this
turn an unrelated product command, or the answer to my question?" via
``PreClassifier.pre_classify`` (surface 1) FIRST. #1595 Phase 3 keeps
shrinking what surface 1 can still claim, and ``consult_inversion_live``
cannot backfill the gap on its own — it stands down on ANY turn that popped
a pending offer (#1190's ``turn_had_pending_offer`` guard), which is exactly
every carrier turn. ``inversion_live.read_op_claims_turn`` is the second,
narrower oracle both carriers now consult when surface 1 declines: it calls
the Inversion router DIRECTLY (never through ``consult_inversion_live``) and
releases ONLY on a live-flagged, high-confidence READ verdict — CXO's ruling
(#1899, 2026-09-27): a READ can never sensibly complete "remind me to ___"
or stand in for an FTUX answer, so gating on READ-effect alone is safe in a
way gating on "any router confidence" would not be.

These are unit tests of the HELPER ITSELF — the wiring at both carrier call
sites is pinned separately (test_task_clarify_1654.py::TestTaskTurnHandlerSeam,
test_ftux_interview_1688.py::TestHandleFtuxInterviewTurn).

Deterministic layer only: the router is stubbed (the shared
``_inversion_pin_helper.py`` idiom, ``stub_router_operation`` /
``assert_inversion_routes``'s sibling pattern) — NO live LLM call anywhere,
ever. The threshold-boundary tests below exercise the GATE's own boundary
behavior against a scripted router reply; they are not a claim about what
the real router would return for the phrasing used — that is UNMEASURED
here and would need a live pass (PM budget).
"""

from types import SimpleNamespace

import pytest

from services.intent_service import inversion_live
from services.intent_service.inversion_router import RoutingDecision
from services.intent_service.workflow_entries import register_default_workflows

pytestmark = pytest.mark.asyncio


def _svc():
    register_default_workflows()
    return SimpleNamespace(intent_classifier=None)


def _stub_route(monkeypatch, *, outcome="operation", operation=None, confidence=0.95):
    from services.intent_service import inversion_router as ir

    async def _route(message, session_state=None, **kwargs):
        return RoutingDecision(
            outcome=outcome,
            operation=operation if outcome == "operation" else None,
            confidence=confidence,
        )

    monkeypatch.setattr(ir, "route", _route)


class TestReadOpClaimsTurnGates:
    """The four gates, one at a time — each must be able to hold ALONE and
    force a bind (``None``)."""

    async def test_read_op_at_or_above_threshold_releases(self, monkeypatch):
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status")
        _stub_route(monkeypatch, operation="list_reminders_query", confidence=0.8)
        result = await inversion_live.read_op_claims_turn(
            "list my reminders", session_id="s1", user_id="u1", intent_service=_svc()
        )
        assert result == "list_reminders_query"

    async def test_read_op_below_threshold_binds(self, monkeypatch):
        """Gate 2."""
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status")
        _stub_route(monkeypatch, operation="list_reminders_query", confidence=0.5)
        result = await inversion_live.read_op_claims_turn(
            "list my reminders", session_id="s1", user_id="u1", intent_service=_svc()
        )
        assert result is None

    async def test_write_op_high_confidence_binds(self, monkeypatch):
        """Gate 3 — READ-verdict-only, no exception for an allowlisted
        write: ``create_todo`` is on ``FLIP_WRITE_ALLOWLIST`` (so it CAN
        dispatch live via ``consult_inversion_live``) but must still never
        release a carrier turn, even at confidence 1.0."""
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "create_todo")
        _stub_route(monkeypatch, operation="create_todo", confidence=1.0)
        result = await inversion_live.read_op_claims_turn(
            "buy milk", session_id="s1", user_id="u1", intent_service=_svc()
        )
        assert result is None

    async def test_read_op_not_live_flagged_binds(self, monkeypatch):
        """Gate 4 — the router itself would answer READ at high confidence,
        but nothing named this operation live (a DIFFERENT group is
        flagged): a deployment must behave exactly as today for any
        operation nobody has reviewed and flipped."""
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_synthesis")
        _stub_route(monkeypatch, operation="list_reminders_query", confidence=0.95)
        result = await inversion_live.read_op_claims_turn(
            "list my reminders", session_id="s1", user_id="u1", intent_service=_svc()
        )
        assert result is None

    @pytest.mark.parametrize("outcome", ["none", "clarify", "refused", "error"])
    async def test_non_operation_outcomes_bind(self, monkeypatch, outcome):
        """Gate 1."""
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status")
        _stub_route(monkeypatch, outcome=outcome, confidence=0.95)
        result = await inversion_live.read_op_claims_turn(
            "whatever", session_id="s1", user_id="u1", intent_service=_svc()
        )
        assert result is None

    async def test_non_rail_operation_binds(self, monkeypatch):
        """A router reply naming an operation with no rail entry at all —
        can't be dispatched, so it can't be a READ either; bind."""
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status")
        _stub_route(monkeypatch, operation="not_a_real_operation", confidence=0.95)
        result = await inversion_live.read_op_claims_turn(
            "whatever", session_id="s1", user_id="u1", intent_service=_svc()
        )
        assert result is None

    async def test_flag_off_binds_and_router_not_called(self, monkeypatch):
        """DEFAULT-EMPTY pin, same discipline as ``consult_inversion_live``:
        an unset/empty flag must behave exactly as today, and cheaply — the
        router must not even be called."""
        monkeypatch.delenv(inversion_live.LIVE_CATEGORIES_ENV, raising=False)
        from services.intent_service import inversion_router as ir

        calls = []

        async def _route(message, session_state=None, **kwargs):
            calls.append(message)
            return RoutingDecision(
                outcome="operation", operation="list_reminders_query", confidence=0.95
            )

        monkeypatch.setattr(ir, "route", _route)
        result = await inversion_live.read_op_claims_turn(
            "list my reminders", session_id="s1", user_id="u1", intent_service=_svc()
        )
        assert result is None
        assert calls == []

    async def test_router_exception_binds_and_never_raises(self, monkeypatch):
        """#1423 discipline: a carrier turn must never fail because the
        oracle hiccupped — a transport error binds, logged, and the
        exception never escapes this function."""
        from services.intent_service import inversion_router as ir

        async def _boom(message, session_state=None, **kwargs):
            raise RuntimeError("transport down")

        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status")
        monkeypatch.setattr(ir, "route", _boom)
        result = await inversion_live.read_op_claims_turn(
            "list my reminders", session_id="s1", user_id="u1", intent_service=_svc()
        )
        assert result is None

    async def test_empty_message_binds(self, monkeypatch):
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status")
        result = await inversion_live.read_op_claims_turn(
            "", session_id="s1", user_id="u1", intent_service=_svc()
        )
        assert result is None


class TestAdversarialThresholdBoundary:
    """CXO's ruling (#1899) asked for a pass at the READ-threshold boundary
    on a genuinely task-shaped utterance that happens to be phrased as a
    question — e.g. "what's for dinner" as a literal intended reminder
    subject vs. a read query about dinner plans.

    This is a DETERMINISTIC exercise of the GATE's own boundary behavior
    (release at >= threshold, bind at <) against a SCRIPTED router reply —
    it is NOT a claim about what the real router would return for this
    phrasing. That is UNMEASURED here and would need a live pass (PM
    budget) to characterize. The actual defense against over-release on an
    ambiguous, question-shaped task subject is NOT the confidence
    threshold alone — it is (a) gate 3, the READ-effect requirement itself
    (a genuinely task-shaped answer the router mis-scores as a read still
    needs the router to pick a REAL read operation, at REAL confidence, for
    a REAL live-flagged group — three independent things that all have to
    align for a false release), plus (b) the carrier's own pre-existing
    acceptance-contract STATE_QUESTION path (a genuine state-question
    re-arms the carrier's own question silently rather than either binding
    or releasing — a third disposition this helper never sees or competes
    with). The threshold is not asked to carry that weight by itself.
    """

    async def test_boundary_releases_at_exactly_the_threshold(self, monkeypatch):
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status")
        assert inversion_live.live_min_confidence() == pytest.approx(0.8)
        _stub_route(monkeypatch, operation="list_reminders_query", confidence=0.8)
        result = await inversion_live.read_op_claims_turn(
            "what's for dinner", session_id="s1", user_id="u1", intent_service=_svc()
        )
        assert result == "list_reminders_query"

    async def test_boundary_binds_just_under_the_threshold(self, monkeypatch):
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status")
        _stub_route(monkeypatch, operation="list_reminders_query", confidence=0.79)
        result = await inversion_live.read_op_claims_turn(
            "what's for dinner", session_id="s1", user_id="u1", intent_service=_svc()
        )
        assert result is None
