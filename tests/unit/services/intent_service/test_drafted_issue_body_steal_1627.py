"""#1627 — draft-flow body composition is stealable mid-compose (PM live
2026-08-15, round 2; #1623 family, member 2).

PM's transcript: the compose flow rendered a draft and asked "What should the
body say…?"; PM's long prose answer contained "delete …" and "(a destructive
action)". The turn fell through the drafted-issue seam as off-intent
(abandoning the draft), and surface 1's greedy portfolio pattern (#1527
family, ``\\bdelete\\s+…(.+)``) claimed it — Piper replied "I couldn't find a
project called '(a destructive action)…'" instead of accepting the body.
The draft flow is floor-composed prose, not a registered gathering process,
so the #1623 mid-interview hold could not cover it.

The fix (sanctioned under the routing moratorium — handler-side at the
pending-offer pop seam, which runs ABOVE the whole 4-surface chain; no new
pre-classifier patterns): while the drafted_issue offer is armed, a prose
turn binds to the draft (appended to its body, offer re-armed) before any
classification surface can see it. Explicit commands, file phrases,
declines, and bare exits keep their exact prior routing — the hold is for
prose that answers the open question, not a turn lock.

Layer honesty (m-43): the end-to-end classes drive the REAL
``IntentService.process_intent`` with an explosive LLM — the prose turn must
resolve deterministically at the offer seam, before classification. The
theft-shape proof pins that the #1527 pattern DOES claim PM's prose (so the
regression is against a real thief, not a strawman).
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.drafted_issue import (
    DRAFTED_ISSUE_KIND,
    is_body_prose_answer,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory

GATE = "services.intent_service.collaboration_gate"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
RESOLVER = "services.integrations.github.repo_resolver.get_user_default_repo"

COMPOSE_ASK = "help me write a ticket about the project deletion flow"

# PM's transcript shape: a long prose body answer carrying both an
# action-like substring ("(a destructive action)") and the word that trips
# the #1527 portfolio pattern ("delete the …").
PM_BODY_PROSE = (
    "The problem: deleting a project (a destructive action) happens "
    "immediately — if you delete the wrong one there's no confirmation "
    "step, no undo, and no summary of what will be lost. The body should "
    "ask for a confirmation dialog before any deletion, and suggest "
    "archiving as the safer default."
)

_USER = "3f7b8a52-1627-4b00-9e00-000000001627"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. The bound
    prose turn must resolve at the pending-offer seam, before classification
    — the live theft happened because nothing held it there."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1627 mid-compose prose must "
            "resolve deterministically at the offer seam"
        )


def _compose_intent(message=COMPOSE_ASK, action="create_ticket"):
    return Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        confidence=0.95,
        original_message=message,
        context={},
    )


@pytest.fixture
def svc():
    register_default_workflows()
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


async def _arm_draft(svc, sid):
    """Turn 1 (the compose/draft turn) at the handler seam — arms the binding."""
    intent = _compose_intent()
    with (
        patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
        patch(f"{ROUTER}.initialize", new=AsyncMock()),
        patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        patch(f"{ROUTER}.create_issue", new=AsyncMock()),
    ):
        return await svc._handle_create_issue(intent, "wf-1", sid, user_id=_USER)


# ---------------------------------------------------------------------------
# 0. Theft-shape proof: the thief is real
# ---------------------------------------------------------------------------


class TestTheftShapeIsReal:
    def test_pm_prose_is_claimed_by_the_1527_portfolio_pattern(self):
        """PM's prose DOES match the greedy portfolio delete pattern — the
        regression below is pinned against a real thief. If this ever fails,
        #1527 was narrowed; the hold is still correct (any surface in the
        chain could claim floor-composed prose), but revisit the fixture."""
        from services.intent_service.pre_classifier import PreClassifier

        assert PreClassifier._matches_patterns(
            PM_BODY_PROSE.lower(), PreClassifier.PORTFOLIO_PATTERNS
        )


# ---------------------------------------------------------------------------
# 1. The discriminator (deterministic, pure)
# ---------------------------------------------------------------------------


class TestIsBodyProseAnswer:
    @pytest.mark.parametrize(
        "message",
        [
            PM_BODY_PROSE,  # the live stolen answer
            "It should explain the missing confirmation step and the impact",
            "Steps to reproduce:\n1. Open a project\n2. Click delete",  # multi-line
            # Long prose that OPENS with an imperative verb — the length
            # override is what protects it from the anchored execute check:
            "Add a guard so that deleting a project (a destructive action) "
            "asks for confirmation first, shows what will be lost, and "
            "offers archiving instead — right now one click removes "
            "everything permanently with no way back.",
            # Long prose opening with a word the unanchored accept row claims:
            "Please note that when a user deletes a project there is no "
            "confirmation of any kind, no undo path, and no record of what "
            "was removed — the body should spell out all three gaps and "
            "propose a confirmation dialog as the fix.",
        ],
    )
    def test_prose_answers_bind(self, message):
        assert is_body_prose_answer(message) is True

    @pytest.mark.parametrize(
        "message",
        [
            "close issue #108",  # explicit command (supplement verb family)
            "delete my reminders",  # the #1527 phrase AS a command
            "list my projects",
            "cancel",  # bare exit → honest decline path
            "stop",
            "forget it",
            "no thanks",  # short decline — the generic seam's business
            "yes",  # short accept — files via the generic seam
            "yes please",
            "file an issue about flaky tests",  # anchored imperative (new ask)
            "update the title of issue #12 to something clearer",
            "remind me at 3pm to check the deploy",
            "",
        ],
    )
    def test_exits_and_commands_do_not_bind(self, message):
        assert is_body_prose_answer(message) is False


# ---------------------------------------------------------------------------
# 2. End-to-end: PM's stolen-turn transcript, through the REAL process_intent
# ---------------------------------------------------------------------------


class TestStolenTurnRegression:
    pytestmark = pytest.mark.asyncio

    async def test_pm_prose_binds_to_draft_nothing_filed_nothing_looked_up(self, svc):
        """PM's exact transcript shape: draft armed → long prose body answer
        containing project-like/action-like substrings. The turn binds to
        the draft: no project lookup, no filing, no LLM (explosive), and the
        draft — now carrying the body — is still armed."""
        sid = "e2e-1627-steal"
        await _arm_draft(svc, sid)

        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            r = await svc.process_intent(message=PM_BODY_PROSE, session_id=sid, user_id=_USER)

        # Nothing filed, nothing looked up:
        w.assert_not_awaited()
        assert "couldn't find a project" not in r.message
        assert "manage_portfolio" != r.intent_data.get("action")
        # The turn bound to the draft and says so honestly:
        assert "nothing is filed yet" in r.message.lower()
        assert "(a destructive action)" in r.message  # the body, echoed back
        assert r.intent_data.get("drafted_issue_pending") is True
        assert r.intent_data.get("drafted_issue_body_bound") is True
        # The draft is STILL armed, with the body captured verbatim:
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == DRAFTED_ISSUE_KIND
        assert stored["pending_action"]["draft"]["body"] == PM_BODY_PROSE

    async def test_bound_body_is_what_actually_files(self, svc):
        """The binding is real, not cosmetic: after the prose turn, "file it
        as is" files in ONE confirmation and the created issue's body IS the
        bound prose."""
        sid = "e2e-1627-file"
        await _arm_draft(svc, sid)

        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()),
        ):
            await svc.process_intent(message=PM_BODY_PROSE, session_id=sid, user_id=_USER)

        created = {"number": 456, "html_url": "https://x/456", "title": "t"}
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
            patch(RESOLVER, new=AsyncMock(return_value="acme/widgets")),
        ):
            r = await svc.process_intent(message="file it as is", session_id=sid, user_id=_USER)

        w.assert_awaited_once()
        _, kwargs = w.await_args
        assert kwargs.get("body") == PM_BODY_PROSE
        assert "#456" in r.message
        assert _pending_offers(svc) == {}

    async def test_successive_prose_turns_append(self, svc):
        """Two prose turns compose: the second appends to the bound body."""
        sid = "e2e-1627-append"
        await _arm_draft(svc, sid)
        second = (
            "Impact: PM nearly lost a real project to this last week — "
            "one stray click and the whole thing was gone with no recovery "
            "path, which is exactly the kind of loss the confirmation "
            "dialog exists to prevent."
        )
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()),
        ):
            await svc.process_intent(message=PM_BODY_PROSE, session_id=sid, user_id=_USER)
            await svc.process_intent(message=second, session_id=sid, user_id=_USER)

        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["draft"]["body"] == (f"{PM_BODY_PROSE}\n\n{second}")

    async def test_cancel_mid_compose_drops_the_draft_honestly(self, svc):
        """Explicit commands still work mid-compose: "cancel" is the #1529
        exit tier — honest decline, draft dropped, nothing filed."""
        sid = "e2e-1627-cancel"
        await _arm_draft(svc, sid)
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            r = await svc.process_intent(message="cancel", session_id=sid, user_id=_USER)
        w.assert_not_awaited()
        assert "Nothing was filed" in r.message
        assert _pending_offers(svc) == {}

    async def test_explicit_unrelated_command_still_routes_normally(self, svc):
        """The hold is not a turn lock: "close issue #108" mid-compose
        abandons the draft (the carrier's documented off-intent rule) and
        routes to its own deterministic surface — the #1190 close
        confirmation claims the turn."""
        sid = "e2e-1627-offintent"
        await _arm_draft(svc, sid)
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            r = await svc.process_intent(message="close issue #108", session_id=sid, user_id=_USER)
        w.assert_not_awaited()
        assert "(yes/no)" in r.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"].get("kind") != DRAFTED_ISSUE_KIND
