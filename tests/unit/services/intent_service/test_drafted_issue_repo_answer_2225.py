"""#2225 — the answer to "Which repository should I create this in?" on the
draft path files the draft the user already said "yes" to (Arch 2026-10-30).

Two seams, no draft flag:
1. ``handle_drafted_issue_turn`` re-arms the draft after an unverified dispatch
   ONLY when the offer store is empty; an inner arm (the #1567 repo question)
   is kept and its reply passed through.
2. ``handle_repo_question_turn`` re-asks (stored question, same words) for a
   ``persist_default`` carrier when the reply names no repository, instead of
   dropping the held write to the off-intent flow.

LAYER: the served three-turn class drives the real ``process_intent`` with an
explosive LLM, the real ``ConnectorConfigService`` on in-memory SQLite, and the
GitHub router patched at its seam. The unit classes stub the store.
"""

from __future__ import annotations

import contextlib
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors.config_service import ConnectorConfigService  # noqa: E402
from services.database.models import ConnectorConfig  # noqa: E402
from services.database.session_factory import AsyncSessionFactory  # noqa: E402
from services.domain.models import Intent  # noqa: E402
from services.intent.intent_service import (  # noqa: E402
    WRITE_TARGET_CREATE_QUESTION,
    IntentService,
)
from services.intent_service.classifier import IntentClassifier  # noqa: E402
from services.intent_service.drafted_issue import (  # noqa: E402
    _DRAFT_RETAINED_LINE,
    DRAFTED_ISSUE_KIND,
    handle_drafted_issue_turn,
)
from services.intent_service.repo_clarification import (  # noqa: E402
    REPO_QUESTION_KIND,
    handle_repo_question_turn,
)
from services.intent_service.workflow_entries import register_default_workflows  # noqa: E402
from services.shared_types import IntentCategory  # noqa: E402

pytestmark = pytest.mark.asyncio

_USER = "11111111-2225-2225-2225-111111111111"
CHOSEN = "dinp-machine/piper-test-activity"
GATE = "services.intent_service.collaboration_gate"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
WORKFLOW = "services.intent_service.workflow_entries.run_confirm_pending_action_workflow"
TITLE = "Re-check forward 1503"
BODY = "Steps: open the page, click save, nothing happens."


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@pytest_asyncio.fixture
async def store(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorConfig.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s
            await s.commit()

    monkeypatch.setattr(AsyncSessionFactory, "session_scope", staticmethod(_scope))
    yield maker
    await engine.dispose()


@pytest.fixture
def svc():
    register_default_workflows()
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _offers(service):
    return service.workflow_offer_service._pending_offers


def _stored(service):
    (offer,) = _offers(service).values()
    return offer


def _router_patches(create):
    return [
        patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
        patch(
            "services.configuration.piper_config_loader.piper_config_loader.load_github_config",
            return_value=MagicMock(default_labels=[]),
        ),
        patch(f"{ROUTER}.initialize", new=AsyncMock()),
        patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        patch(f"{ROUTER}.find_open_issue_by_title", new=AsyncMock(return_value=None)),
        patch(f"{ROUTER}.create_issue", new=create),
    ]


async def _draft(svc, sid):
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="create_ticket",
        confidence=0.95,
        original_message=f"Let's track this. Create a GitHub issue: '{TITLE}'",
        context={"title": TITLE, "description": BODY, "user_id": _USER},
    )
    with contextlib.ExitStack() as st:
        for p in _router_patches(AsyncMock()):
            st.enter_context(p)
        return await svc._handle_create_issue(intent, "wf-1", sid, user_id=_USER)


# ---------------------------------------------------------------------------
# Served: draft -> "yes" (no user default) -> owner/name
# ---------------------------------------------------------------------------


class TestDraftYesThenRepo:
    async def test_yes_leaves_the_repo_question_not_the_draft(self, store, svc):
        sid = f"s-2225-{uuid.uuid4()}"
        await _draft(svc, sid)
        assert _stored(svc)["pending_action"]["kind"] == DRAFTED_ISSUE_KIND
        with contextlib.ExitStack() as st:
            for p in _router_patches(AsyncMock()):
                st.enter_context(p)
            r = await svc.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert _stored(svc)["pending_action"]["kind"] == REPO_QUESTION_KIND
        assert WRITE_TARGET_CREATE_QUESTION in r.message
        assert _DRAFT_RETAINED_LINE not in r.message

    async def test_owner_name_files_the_draft_there_and_keeps_the_default(self, store, svc):
        sid = f"s-2225-{uuid.uuid4()}"
        await _draft(svc, sid)
        create = AsyncMock(
            return_value={
                "number": 35,
                "title": TITLE,
                "html_url": f"https://github.com/{CHOSEN}/issues/35",
            }
        )
        with contextlib.ExitStack() as st:
            for p in _router_patches(create):
                st.enter_context(p)
            await svc.process_intent(message="yes", session_id=sid, user_id=_USER)
            r = await svc.process_intent(message=CHOSEN, session_id=sid, user_id=_USER)
        create.assert_awaited_once()
        kw = create.await_args.kwargs
        assert (kw["owner"], kw["repo_name"]) == tuple(CHOSEN.split("/"))
        assert kw["title"] == TITLE  # a bare owner/name must not slot-fill a new title
        assert kw["body"] == BODY
        assert "Created issue #35" in r.message
        assert f"in {CHOSEN}" in r.message
        assert _offers(svc) == {}  # no second confirm armed
        async with store() as s:
            cfg = await ConnectorConfigService(s).get_config(_USER, "github")
        assert cfg["default_repository"] == CHOSEN
        assert cfg["default_repository_source"] == "user"

    async def test_prose_naming_no_repo_reasks_the_exact_question(self, store, svc):
        sid = f"s-2225-{uuid.uuid4()}"
        await _draft(svc, sid)
        create = AsyncMock()
        with contextlib.ExitStack() as st:
            for p in _router_patches(create):
                st.enter_context(p)
            await svc.process_intent(message="yes", session_id=sid, user_id=_USER)
            r = await svc.process_intent(
                message="the one where we keep the activity experiments, you know",
                session_id=sid,
                user_id=_USER,
            )
        create.assert_not_awaited()
        assert r.message == WRITE_TARGET_CREATE_QUESTION
        stored = _stored(svc)
        assert stored["pending_action"]["kind"] == REPO_QUESTION_KIND
        assert stored["question"] == WRITE_TARGET_CREATE_QUESTION

    async def test_no_principal_on_the_answer_binds_nothing(self, store, svc):
        sid = f"s-2225-{uuid.uuid4()}"
        await _draft(svc, sid)
        create = AsyncMock()
        with contextlib.ExitStack() as st:
            for p in _router_patches(create):
                st.enter_context(p)
            await svc.process_intent(message="yes", session_id=sid, user_id=_USER)
            offer = _stored(svc)
            out = await handle_repo_question_turn(
                offer, CHOSEN, session_id=sid, user_id=None, intent_service=svc
            )
        assert out is None
        create.assert_not_awaited()
        async with store() as s:
            assert not await ConnectorConfigService(s).get_config(_USER, "github")


# ---------------------------------------------------------------------------
# Unit: the carrier's re-ask guards, and the draft seam without an inner arm
# ---------------------------------------------------------------------------


def _carrier_offer(question=WRITE_TARGET_CREATE_QUESTION, persist=True):
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="create_issue",
        confidence=1.0,
        context={"title": TITLE},
        original_message="x",
    )
    payload = {
        "kind": REPO_QUESTION_KIND,
        "action": "create_issue",
        "intent": intent,
        "user_id": _USER,
    }
    if persist:
        payload["persist_default"] = True
    return {
        "kind": REPO_QUESTION_KIND,
        "workflow_type": "confirm_pending_action",
        "pending_action": payload,
        "question": question,
    }


class TestCarrierReask:
    async def test_outside_the_family_imperative_still_routes(self):
        svc = MagicMock()
        out = await handle_repo_question_turn(
            _carrier_offer(),
            "list my projects",
            session_id="s",
            user_id=_USER,
            intent_service=svc,
        )
        assert out is None
        svc.workflow_offer_service.set_pending_offer.assert_not_called()

    async def test_decline_still_drops(self):
        out = await handle_repo_question_turn(
            _carrier_offer(), "no", session_id="s", user_id=_USER, intent_service=MagicMock()
        )
        assert out is None

    async def test_carrier_without_persist_default_keeps_the_off_intent_rule(self):
        svc = MagicMock()
        out = await handle_repo_question_turn(
            _carrier_offer(persist=False),
            "hmm, let me think about which one",
            session_id="s",
            user_id=_USER,
            intent_service=svc,
        )
        assert out is None
        svc.workflow_offer_service.set_pending_offer.assert_not_called()

    async def test_persist_default_carrier_reasks_with_stored_question(self):
        svc = MagicMock()
        offer = _carrier_offer()
        out = await handle_repo_question_turn(
            offer,
            "hmm, let me think about which one",
            session_id="s",
            user_id=_USER,
            intent_service=svc,
        )
        assert out["message"] == WRITE_TARGET_CREATE_QUESTION
        assert out["requires_clarification"] is True
        svc.workflow_offer_service.set_pending_offer.assert_called_once()


def _draft_offer():
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="create_issue",
        confidence=1.0,
        context={"title": TITLE, "body": BODY},
        original_message="x",
    )
    return {
        "kind": DRAFTED_ISSUE_KIND,
        "pending_action": {
            "kind": DRAFTED_ISSUE_KIND,
            "action": "create_issue",
            "intent": intent,
            "user_id": _USER,
        },
        "question": "q",
    }


class TestDraftSeamInnerArm:
    async def test_no_inner_arm_still_retains_the_draft(self):
        svc = MagicMock()
        svc.workflow_offer_service.peek_pending_offer.return_value = None
        rail = {"message": "GitHub is not connected.", "intent_data": {}}
        with patch(WORKFLOW, new=AsyncMock(return_value=rail)):
            out = await handle_drafted_issue_turn(
                _draft_offer(), "file it", session_id="s", user_id=_USER, intent_service=svc
            )
        assert _DRAFT_RETAINED_LINE in out["message"]
        svc.workflow_offer_service.set_pending_offer.assert_called_once()

    async def test_inner_arm_passes_through_without_rearm_or_tail(self):
        svc = MagicMock()
        svc.workflow_offer_service.peek_pending_offer.return_value = {
            "pending_action": {"kind": REPO_QUESTION_KIND}
        }
        rail = {
            "message": WRITE_TARGET_CREATE_QUESTION,
            "intent_data": {"issue_repo_question_pending": True},
        }
        with patch(WORKFLOW, new=AsyncMock(return_value=rail)):
            out = await handle_drafted_issue_turn(
                _draft_offer(), "file it", session_id="s", user_id=_USER, intent_service=svc
            )
        assert out["message"] == WRITE_TARGET_CREATE_QUESTION
        svc.workflow_offer_service.set_pending_offer.assert_not_called()

    async def test_body_prose_still_binds_when_no_inner_arm(self):
        svc = MagicMock()
        prose = (
            "The problem is that deleting a project happens immediately, with no "
            "confirmation step and no undo, so the body should ask for a dialog."
        )
        with patch(WORKFLOW, new=AsyncMock()) as wf:
            out = await handle_drafted_issue_turn(
                _draft_offer(), prose, session_id="s", user_id=_USER, intent_service=svc
            )
        wf.assert_not_awaited()
        assert "deleting a project" in out["message"]
