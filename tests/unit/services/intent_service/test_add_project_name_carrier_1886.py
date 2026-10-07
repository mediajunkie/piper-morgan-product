"""#1886 — the add-project name-clarify carrier replaces the onboarding-
session bookkeeping ``_handle_add_project`` used to do.

Architect's ruling (2026-10-06, binding): ``_handle_add_project`` gets a
DURABLE PER-TURN CARRIER (the #846/#1190 pending-offer idiom), NOT a
re-registered ``OnboardingProcessAdapter``. The defect (#1867 finding 1):
the no-name ask used to create a ``PortfolioOnboardingManager`` session and
read it back next turn via a private helper gated on the next turn's text
containing an "add"/"create"/"new project" token — a bare-name reply
("Klatch") carried none of those tokens, so it never re-entered the handler
and the ask silently orphaned.

These tests mirror ``tests/unit/services/intent_service/
test_reminder_question_acceptance_1654.py`` / ``test_task_clarify_1654.py``'s
style: a ``SimpleNamespace`` fake service standing in for ``IntentService``,
driving ``_handle_add_project`` (the arm half) and
``add_project_clarify.handle_add_project_name_turn`` (the consume half)
directly at the seam.

Layer honesty (m-43): the arm half goes through the REAL
``CanonicalHandlers._handle_add_project``; the consume half's create path
goes through the REAL ``CanonicalHandlers._create_or_report_project`` with
the DB mocked (mirrors test_add_project_initiation_args_1856.py's
``_Recorder`` pattern) — never a stubbed create, so the carrier's hand-off
to the real write path is actually exercised, not assumed.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent_service.add_project_clarify import (
    _NAME_REASK_TAIL,
    ADD_PROJECT_NAME_QUESTION_KIND,
    CLARIFY_ADD_PROJECT_NAME_WORKFLOW,
    build_add_project_name_offer,
    handle_add_project_name_turn,
)
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.soft_invocation import WorkflowOfferService

_USER = "3f7b8a52-1886-4b00-9e00-000000001886"

_ADD_PROJECT_ASK = CanonicalHandlers._ADD_PROJECT_ASK


class _FakeScope:
    """Minimal async-context-manager double for AsyncSessionFactory.session_scope()."""

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False


class _Recorder:
    """Captures what _create_or_report_project actually wrote (mirrors
    test_add_project_initiation_args_1856.py's _Recorder exactly)."""

    def __init__(self, existing_project=None):
        self.created = []
        self.existing_project = existing_project

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
            return self.existing_project

        return [
            patch.object(AsyncSessionFactory, "session_scope", staticmethod(lambda: _FakeScope())),
            patch.object(ProjectRepository, "create", _create),
            patch.object(ProjectRepository, "find_by_name", _find_by_name),
        ]


def _fake_service():
    """Minimal seam double: an offer store + a REAL CanonicalHandlers (so
    the create path is exercised for real, DB mocked by the caller)."""
    return SimpleNamespace(
        workflow_offer_service=WorkflowOfferService(),
        canonical_handlers=CanonicalHandlers(),
    )


def _offer(original_message="add a project", question=_ADD_PROJECT_ASK):
    return build_add_project_name_offer(original_message, _USER, question=question)


def _patches(rec):
    """ExitStack context manager installing a _Recorder's DB patches."""
    import contextlib

    stack = contextlib.ExitStack()
    for p in rec.install():
        stack.enter_context(p)
    return stack


# ---------------------------------------------------------------------------
# 1. The arm half — _handle_add_project's no-name ask.
# ---------------------------------------------------------------------------


class TestArmHalf:
    pytestmark = pytest.mark.asyncio

    async def test_no_name_ask_arms_the_offer_directly_when_intent_service_given(self):
        """The rail path (run_add_project_workflow) always has intent_service
        in context — the no-name ask must arm DIRECTLY, with no embedded key
        needed."""
        fake = _fake_service()
        result = await fake.canonical_handlers._handle_add_project(
            original_message="add a project",
            session_id="s-1886-arm",
            user_id=_USER,
            intent_service=fake,
        )
        assert result["message"] == _ADD_PROJECT_ASK
        assert "add_project_name_offer" not in result, "armed directly — no embedded key needed"

        stored = fake.workflow_offer_service.peek_pending_offer("s-1886-arm")
        assert stored is not None
        assert stored["workflow_type"] == CLARIFY_ADD_PROJECT_NAME_WORKFLOW
        assert stored["question"] == result["message"] == _ADD_PROJECT_ASK  # #1665
        assert stored["decline_message"]
        assert stored["pending_action"]["kind"] == ADD_PROJECT_NAME_QUESTION_KIND
        assert stored["pending_action"]["original_message"] == "add a project"

    async def test_no_name_ask_embeds_the_offer_when_intent_service_absent(self):
        """The legacy canonical dispatch path (_handle_portfolio_query) has
        no offer-store access — mirrors the #1688 FTUX pattern: the UNARMED
        offer is embedded for the intent_service canonical seam to arm."""
        handler = CanonicalHandlers()
        result = await handler._handle_add_project(
            original_message="add a project",
            session_id="s-1886-embed",
            user_id=_USER,
        )
        assert result["message"] == _ADD_PROJECT_ASK
        embedded = result.get("add_project_name_offer")
        assert embedded is not None
        assert embedded["workflow_type"] == CLARIFY_ADD_PROJECT_NAME_WORKFLOW
        assert embedded["question"] == _ADD_PROJECT_ASK

    async def test_handle_add_project_never_touches_onboarding_components(self):
        """#1886: the dead chain is gone from this handler's own code path —
        patch _get_onboarding_components to raise and confirm neither branch
        calls it."""
        with patch(
            "services.conversation.conversation_handler._get_onboarding_components",
            side_effect=AssertionError("onboarding bookkeeping must not be touched"),
        ):
            handler = CanonicalHandlers()
            # No-name branch.
            result = await handler._handle_add_project(
                original_message="add a project",
                session_id="s-1886-no-onboarding-ask",
                user_id=_USER,
            )
            assert result["message"] == _ADD_PROJECT_ASK

            # Name-present branch.
            rec = _Recorder()
            with _patches(rec):
                result = await handler._handle_add_project(
                    original_message="add project Klatch",
                    session_id="s-1886-no-onboarding-create",
                    user_id=_USER,
                )
            assert "Klatch" in result["message"]


# ---------------------------------------------------------------------------
# 2. The consume half — add_project_clarify.handle_add_project_name_turn.
# ---------------------------------------------------------------------------


class TestConsumeHalf:
    pytestmark = pytest.mark.asyncio

    async def test_bare_name_answer_creates_the_project(self):
        """The ask's whole point: a bare name answer ("Klatch") binds and
        creates — through the REAL create path, DB mocked."""
        fake = _fake_service()
        rec = _Recorder()
        with _patches(rec):
            result = await handle_add_project_name_turn(
                _offer(),
                "Klatch",
                session_id="s-1886-bind",
                user_id=_USER,
                intent_service=fake,
            )
        assert result is not None
        assert len(rec.created) == 1
        assert rec.created[0]["name"] == "Klatch"
        assert "Added Klatch to your portfolio" in result["message"]
        assert result["requires_clarification"] is False

    async def test_implausible_answer_gets_branch_3_copy_and_does_not_rearm(self):
        fake = _fake_service()
        result = await handle_add_project_name_turn(
            _offer(),
            "this is not the name of the new project at all",
            session_id="s-1886-implausible",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is not None
        assert "sorry for the loop" in result["message"].lower()
        assert "have not created anything" in result["message"].lower()
        assert result["intent_data"]["action"] == "add_project_abandoned"
        assert result["intent_data"]["context"]["user_corrected"] is True
        assert fake.workflow_offer_service.peek_pending_offer("s-1886-implausible") is None

    async def test_bare_restatement_gets_branch_3_copy_without_releasing(self):
        """The second no-name 'add' turn (#1867 finding 1) — a BARE
        restatement ("add project" again, no name) must NOT release back to
        _handle_add_project (which would render the identical first ask
        again); it is answered here directly."""
        fake = _fake_service()
        result = await handle_add_project_name_turn(
            _offer(),
            "add a project",
            session_id="s-1886-bare-restate",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is not None
        assert result["message"] != _ADD_PROJECT_ASK
        assert "have not created anything" in result["message"].lower()
        assert fake.workflow_offer_service.peek_pending_offer("s-1886-bare-restate") is None

    async def test_restatement_with_a_name_releases(self):
        """A full restatement that CARRIES its own name ("add project
        Klatch") abandons via the pop and routes normally — the ordinary
        add-project path re-extracts and creates it."""
        fake = _fake_service()
        result = await handle_add_project_name_turn(
            _offer(),
            "add project Klatch",
            session_id="s-1886-restate-named",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is None

    async def test_decline_falls_through(self):
        fake = _fake_service()
        result = await handle_add_project_name_turn(
            _offer(),
            "no",
            session_id="s-1886-decline",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is None

    async def test_principal_mismatch_holds_off(self):
        fake = _fake_service()
        result = await handle_add_project_name_turn(
            _offer(),
            "Klatch",
            session_id="s-1886-principal",
            user_id=str(uuid4()),  # a DIFFERENT principal
            intent_service=fake,
        )
        assert result is not None
        assert "nothing has been created" in result["message"].lower()
        assert result["intent_data"].get("principal_mismatch") is True

    async def test_bare_accept_reasks_and_rearms(self):
        """A bare 'yes' doesn't name a project — honest re-ask, never a
        silent abandon, mirroring handle_reminder_task_turn's ACCEPT branch."""
        fake = _fake_service()
        result = await handle_add_project_name_turn(
            _offer(),
            "yes",
            session_id="s-1886-accept",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is not None
        assert _NAME_REASK_TAIL in result["message"]
        stored = fake.workflow_offer_service.peek_pending_offer("s-1886-accept")
        assert stored["pending_action"]["kind"] == ADD_PROJECT_NAME_QUESTION_KIND

    async def test_state_question_falls_through(self):
        fake = _fake_service()
        result = await handle_add_project_name_turn(
            _offer(),
            "what do you mean?",
            session_id="s-1886-state-q",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is None

    async def test_empty_turn_falls_through(self):
        fake = _fake_service()
        result = await handle_add_project_name_turn(
            _offer(),
            "   ",
            session_id="s-1886-empty",
            user_id=_USER,
            intent_service=fake,
        )
        assert result is None
