"""#1886(b) — the shared, stateless armed-turn router consult
(``armed_turn_consult.classify_armed_reply``).

Arch's binding ruling, 2026-10-07 (mail
``rule-arch-to-lead-cc-cxo-1886-b-router-decides-answer-vs-new-ask-confirm-fallback-one-helper-both-carriers-2026-10-07.md``):
on an armed turn, run the stateless router consult and branch on three
outcomes — RELEASE (an operation at/above the live-consult threshold),
BIND (NONE/CLARIFY), or CONFIRM (below threshold, refused, errored, or
unreachable). ONE helper, used by BOTH the #1886 add-project name carrier
(``add_project_clarify.handle_add_project_name_turn``) and the
reminder-task carrier (``todo_handlers.handle_reminder_task_turn``) — "two
copies of 'release or bind' are how they drift" (Arch).

This file pins:
  1. The HELPER ITSELF (``classify_armed_reply``) — deterministic, router
     stubbed, no live LLM call anywhere.
  2. That BOTH carriers actually consult it and land on the right
     outcome, including Lead's 8 probed phrasings that would otherwise
     have CREATED a project with that literal name
     (ask-lead-to-arch-cc-cxo-1886-carrier-held-...-2026-10-07.md).
  3. That the helper never dispatches anything itself (Arch's structural
     constraint) — release only ever hands the turn back as data.
"""

from __future__ import annotations

import contextlib
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent_service.add_project_clarify import (
    ADD_PROJECT_CONFIRM_KIND,
    build_add_project_confirm_offer,
    build_add_project_name_offer,
    handle_add_project_confirm_turn,
    handle_add_project_name_turn,
)
from services.intent_service.armed_turn_consult import (
    ArmedReplyOutcome,
    classify_armed_reply,
)
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.soft_invocation import WorkflowOfferService
from services.intent_service.todo_handlers import (
    build_reminder_task_offer,
    handle_reminder_task_turn,
)

pytestmark = pytest.mark.asyncio

_USER = "3f7b8a52-1886-4b00-9e00-00000000beef"

_PROBED_PHRASINGS = [
    "show my projects",
    "list my projects",
    "archive the Test project",
    "delete my project Klatch",
    "what's on my calendar today",
    "close issue 108",
    "remind me to call mom at 5",
    "show my todos",
]


def _stub_route(monkeypatch, *, outcome="operation", operation=None, confidence=None, error=None):
    from services.intent_service import inversion_router as ir
    from services.intent_service.inversion_router import RoutingDecision

    async def _route(message, session_state=None, **kwargs):
        return RoutingDecision(
            outcome=outcome,
            operation=operation if outcome == "operation" else None,
            confidence=confidence,
            error=error,
        )

    monkeypatch.setattr(ir, "route", _route)


def _svc():
    return SimpleNamespace(intent_classifier=None)


# ---------------------------------------------------------------------------
# 1. The helper itself.
# ---------------------------------------------------------------------------


class TestClassifyArmedReplyOutcomes:
    @pytest.mark.parametrize("phrase", _PROBED_PHRASINGS)
    async def test_probed_phrasings_release(self, monkeypatch, phrase):
        _stub_route(monkeypatch, outcome="operation", operation="some_op", confidence=0.9)
        decision = await classify_armed_reply(phrase, _USER, session_id="s1", intent_service=_svc())
        assert decision.outcome is ArmedReplyOutcome.RELEASE
        assert decision.operation == "some_op"

    async def test_none_outcome_binds(self, monkeypatch):
        _stub_route(monkeypatch, outcome="none")
        decision = await classify_armed_reply(
            "Klatch", _USER, session_id="s1", intent_service=_svc()
        )
        assert decision.outcome is ArmedReplyOutcome.BIND

    async def test_clarify_outcome_binds(self, monkeypatch):
        _stub_route(monkeypatch, outcome="clarify")
        decision = await classify_armed_reply(
            "Piper Morgan Website", _USER, session_id="s1", intent_service=_svc()
        )
        assert decision.outcome is ArmedReplyOutcome.BIND

    async def test_sub_threshold_operation_confirms(self, monkeypatch):
        _stub_route(monkeypatch, outcome="operation", operation="some_op", confidence=0.6)
        decision = await classify_armed_reply(
            "Klatch", _USER, session_id="s1", intent_service=_svc()
        )
        assert decision.outcome is ArmedReplyOutcome.CONFIRM
        assert decision.operation == "some_op"
        assert decision.confidence == 0.6

    async def test_refused_outcome_confirms(self, monkeypatch):
        _stub_route(monkeypatch, outcome="refused")
        decision = await classify_armed_reply(
            "Klatch", _USER, session_id="s1", intent_service=_svc()
        )
        assert decision.outcome is ArmedReplyOutcome.CONFIRM

    async def test_error_outcome_confirms(self, monkeypatch):
        """Covers the router's OWN handled failure path — no key, quota,
        timeout, or any transport error all surface as outcome="error"
        from ``route()`` itself (it never raises for those)."""
        _stub_route(monkeypatch, outcome="error", error="No LLM key configured")
        decision = await classify_armed_reply(
            "Klatch", _USER, session_id="s1", intent_service=_svc()
        )
        assert decision.outcome is ArmedReplyOutcome.CONFIRM

    async def test_consult_exception_confirms_and_never_raises(self, monkeypatch):
        """Belt: if ``route()`` itself raises (rather than returning its own
        handled "error" outcome), the consult must still CONFIRM, never
        crash the armed turn."""
        from services.intent_service import inversion_router as ir

        async def _boom(message, session_state=None, **kwargs):
            raise RuntimeError("transport down")

        monkeypatch.setattr(ir, "route", _boom)
        decision = await classify_armed_reply(
            "Klatch", _USER, session_id="s1", intent_service=_svc()
        )
        assert decision.outcome is ArmedReplyOutcome.CONFIRM

    async def test_empty_text_binds(self, monkeypatch):
        called = []

        async def _route(message, session_state=None, **kwargs):
            called.append(message)
            from services.intent_service.inversion_router import RoutingDecision

            return RoutingDecision(outcome="operation", operation="some_op", confidence=0.99)

        from services.intent_service import inversion_router as ir

        monkeypatch.setattr(ir, "route", _route)
        decision = await classify_armed_reply("   ", _USER, session_id="s1", intent_service=_svc())
        assert decision.outcome is ArmedReplyOutcome.BIND
        assert called == []  # never even consulted for empty text

    async def test_boundary_releases_at_exactly_the_threshold(self, monkeypatch):
        from services.intent_service import inversion_live

        assert inversion_live.live_min_confidence() == pytest.approx(0.8)
        _stub_route(monkeypatch, outcome="operation", operation="some_op", confidence=0.8)
        decision = await classify_armed_reply(
            "Klatch", _USER, session_id="s1", intent_service=_svc()
        )
        assert decision.outcome is ArmedReplyOutcome.RELEASE

    async def test_boundary_confirms_just_under_the_threshold(self, monkeypatch):
        _stub_route(monkeypatch, outcome="operation", operation="some_op", confidence=0.79)
        decision = await classify_armed_reply(
            "Klatch", _USER, session_id="s1", intent_service=_svc()
        )
        assert decision.outcome is ArmedReplyOutcome.CONFIRM

    async def test_ungated_by_live_categories_flag(self, monkeypatch):
        """Deliberately NO ``PIPER_INVERSION_LIVE_CATEGORIES`` set — unlike
        ``consult_inversion_live``/``read_op_claims_turn``, this consult
        never dispatches, so the dispatch-safety flag doesn't gate it."""
        monkeypatch.delenv("PIPER_INVERSION_LIVE_CATEGORIES", raising=False)
        _stub_route(monkeypatch, outcome="operation", operation="some_op", confidence=0.9)
        decision = await classify_armed_reply(
            "show my projects", _USER, session_id="s1", intent_service=_svc()
        )
        assert decision.outcome is ArmedReplyOutcome.RELEASE

    async def test_never_calls_dispatch_workflow(self, monkeypatch):
        import services.intent_service.workflow_dispatcher as wd

        spy = AsyncMock()
        monkeypatch.setattr(wd, "dispatch_workflow", spy)
        for outcome, operation, confidence in [
            ("operation", "some_op", 0.9),
            ("none", None, None),
            ("operation", "some_op", 0.5),
            ("refused", None, None),
        ]:
            _stub_route(monkeypatch, outcome=outcome, operation=operation, confidence=confidence)
            await classify_armed_reply("Klatch", _USER, session_id="s1", intent_service=_svc())
        spy.assert_not_awaited()


# ---------------------------------------------------------------------------
# 2. Carrier wiring — the #1886 add-project name carrier.
# ---------------------------------------------------------------------------


class _FakeScope:
    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False


class _Recorder:
    def __init__(self):
        self.created = []

    def install(self):
        from services.database.repositories import ProjectRepository
        from services.database.session_factory import AsyncSessionFactory

        created_project = MagicMock()
        created_project.id = "proj-1886"

        async def _create(_self, **kwargs):
            self.created.append(kwargs)
            created_project.name = kwargs.get("name", "Klatch")
            return created_project

        async def _find_by_name(_self, **kwargs):
            return None

        return [
            patch.object(AsyncSessionFactory, "session_scope", staticmethod(lambda: _FakeScope())),
            patch.object(ProjectRepository, "create", _create),
            patch.object(ProjectRepository, "find_by_name", _find_by_name),
        ]


def _patches(rec):
    stack = contextlib.ExitStack()
    for p in rec.install():
        stack.enter_context(p)
    return stack


def _fake_add_project_service():
    return SimpleNamespace(
        workflow_offer_service=WorkflowOfferService(),
        canonical_handlers=CanonicalHandlers(),
    )


def _name_offer(original_message="add a project"):
    return build_add_project_name_offer(
        original_message, _USER, question=CanonicalHandlers._ADD_PROJECT_ASK
    )


class TestAddProjectCarrierUsesTheSharedHelper:
    @pytest.mark.parametrize("phrase", _PROBED_PHRASINGS)
    async def test_probed_phrasings_release_and_create_nothing(self, monkeypatch, phrase):
        _stub_route(monkeypatch, outcome="operation", operation="some_op", confidence=0.9)
        fake = _fake_add_project_service()
        rec = _Recorder()
        with _patches(rec):
            result = await handle_add_project_name_turn(
                _name_offer(),
                phrase,
                session_id=f"s-armed-release-{abs(hash(phrase))}",
                user_id=_USER,
                intent_service=fake,
            )
        assert result is None
        assert rec.created == []

    async def test_plain_name_with_none_binds_and_creates(self, monkeypatch):
        _stub_route(monkeypatch, outcome="none")
        fake = _fake_add_project_service()
        rec = _Recorder()
        with _patches(rec):
            result = await handle_add_project_name_turn(
                _name_offer(),
                "Klatch",
                session_id="s-armed-bind",
                user_id=_USER,
                intent_service=fake,
            )
        assert result is not None
        assert len(rec.created) == 1
        assert rec.created[0]["name"] == "Klatch"

    async def test_second_plain_name_with_none_binds_and_creates(self, monkeypatch):
        """The task's second named example ("Piper Morgan Website") — not
        just "Klatch"."""
        _stub_route(monkeypatch, outcome="none")
        fake = _fake_add_project_service()
        rec = _Recorder()
        with _patches(rec):
            result = await handle_add_project_name_turn(
                _name_offer(),
                "Piper Morgan Website",
                session_id="s-armed-bind-2",
                user_id=_USER,
                intent_service=fake,
            )
        assert result is not None
        assert len(rec.created) == 1
        assert rec.created[0]["name"] == "Piper Morgan Website"

    @pytest.mark.parametrize(
        "outcome,operation,confidence,error",
        [
            ("error", None, None, "No LLM key configured"),
            ("operation", "some_op", 0.6, None),
        ],
        ids=["router_error_no_key", "sub_threshold_operation"],
    )
    async def test_uncertain_meaning_arms_confirm_with_cxos_copy(
        self, monkeypatch, outcome, operation, confidence, error
    ):
        _stub_route(
            monkeypatch, outcome=outcome, operation=operation, confidence=confidence, error=error
        )
        fake = _fake_add_project_service()
        rec = _Recorder()
        with _patches(rec):
            result = await handle_add_project_name_turn(
                _name_offer(),
                "Klatch",
                session_id=f"s-armed-confirm-{outcome}",
                user_id=_USER,
                intent_service=fake,
            )
        assert result is not None
        assert result["message"] == 'Add a project called "Klatch"? (yes/no)'
        assert rec.created == []
        stored = fake.workflow_offer_service.peek_pending_offer(f"s-armed-confirm-{outcome}")
        assert stored["pending_action"]["kind"] == ADD_PROJECT_CONFIRM_KIND
        assert stored["pending_action"]["name"] == "Klatch"

    async def test_confirm_yes_creates(self):
        fake = _fake_add_project_service()
        rec = _Recorder()
        offer = build_add_project_confirm_offer("Klatch", None, _USER, "add a project")
        with _patches(rec):
            result = await handle_add_project_confirm_turn(
                offer, "yes", session_id="s-confirm-yes", user_id=_USER, intent_service=fake
            )
        assert result is not None
        assert len(rec.created) == 1
        assert rec.created[0]["name"] == "Klatch"

    async def test_confirm_no_declines_with_exact_copy_and_no_rearm(self):
        fake = _fake_add_project_service()
        offer = build_add_project_confirm_offer("Klatch", None, _USER, "add a project")
        result = await handle_add_project_confirm_turn(
            offer, "no", session_id="s-confirm-no", user_id=_USER, intent_service=fake
        )
        # Kind-specific handler drops honestly via decline_message (None →
        # generic flow); the exact copy lives on the offer record itself.
        assert result is None
        assert offer["decline_message"] == (
            'Okay — I won\'t add a project called "Klatch". Nothing has been changed.'
        )
        assert fake.workflow_offer_service.peek_pending_offer("s-confirm-no") is None


# ---------------------------------------------------------------------------
# 3. Carrier wiring — the reminder-task carrier uses the SAME helper.
# ---------------------------------------------------------------------------


def _fake_reminder_service():
    todo_service = MagicMock()
    todo_service.create_todo = AsyncMock(return_value=SimpleNamespace(id=uuid4(), text="x"))
    return SimpleNamespace(
        workflow_offer_service=WorkflowOfferService(),
        todo_handlers=SimpleNamespace(todo_service=todo_service),
    )


class TestReminderTaskCarrierUsesTheSharedHelper:
    async def test_release_path(self, monkeypatch):
        """One of Lead's probed phrasings, this time against the
        reminder-task carrier's OWN armed question: the shared helper
        releases it too, and nothing is saved."""
        _stub_route(monkeypatch, outcome="operation", operation="some_op", confidence=0.9)
        fake = _fake_reminder_service()
        offer = build_reminder_task_offer("set a reminder: check the oven", _USER)
        result = await handle_reminder_task_turn(
            offer,
            "show my projects",
            session_id="s-reminder-release",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is None
        fake.todo_handlers.todo_service.create_todo.assert_not_awaited()
