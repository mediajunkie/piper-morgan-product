"""#1630 — the UNARMED draft opening is still stealable (#1627's sibling,
found during #1627; agent lane B, 2026-08-15).

The #1627 hold covers the ARMED case only — a draft offer bound with a
subject. "help me write a ticket" with NO extractable subject armed nothing
(no subject = no draft yet, by design), so the user's answer to
"What's it about?" was a bare prose turn fully stealable by the #1527
pattern family — the exact theft shape PM hit live, one turn earlier in
the flow.

The fix (Lead's stated lean on the issue — small, reuses the #1627
discriminator): the collaborate turn arms a minimal SUBJECTLESS draft
carrier at the ask, so the existing #1627 hold covers the first answer
too. The FIRST bound prose answer NAMES the draft
(``derive_subject_from_prose`` → title, mirrored into
``intent.context["title"]`` so the create rail actually files it — the
subjectless original message slot-fills nothing) and seeds the body per
the existing append semantics. Explicit commands, declines, and bare
exits keep their exact prior routing — same discriminator, same seam,
same exits.

Layer honesty (m-43): the end-to-end classes drive the REAL
``IntentService.process_intent`` with an explosive LLM — the first-answer
turn must resolve deterministically at the offer seam, before
classification. The theft-shape proof pins that the #1527 pattern DOES
claim the fixture prose (a real thief, not a strawman): pre-fix, with no
offer armed, that turn fell straight through to surface 1.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.drafted_issue import (
    DRAFTED_ISSUE_KIND,
    build_drafted_issue_offer,
    derive_subject_from_prose,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory

GATE = "services.intent_service.collaboration_gate"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
RESOLVER = "services.integrations.github.repo_resolver.get_user_default_repo"

# PM's shape, pinned: the subjectless opening…
SUBJECTLESS_ASK = "help me write a ticket"

# …and the first answer: long prose carrying 'delete …' substrings — the
# pre-fix steal shape (the #1527 portfolio pattern's food).
FIRST_ANSWER_PROSE = (
    "Deleting a project is instant and unrecoverable — if you delete the "
    "wrong one there's no confirmation step, no undo, and no summary of "
    "what will be lost. The ticket should ask for a confirmation dialog "
    "before any deletion, and suggest archiving as the safer default."
)

_USER = "3f7b8a52-1630-4b00-9e00-000000001630"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. The first
    answer must resolve deterministically at the offer seam, before
    classification — pre-fix, nothing held it there."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1630 first-answer turns must "
            "resolve deterministically at the offer seam"
        )


def _compose_intent(message=SUBJECTLESS_ASK, action="create_ticket"):
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


async def _arm_subjectless(svc, sid):
    """Turn 1 (the subjectless ask) at the handler seam — arms the minimal
    carrier and asks "What's it about?"."""
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
    def test_first_answer_prose_is_claimed_by_the_1527_portfolio_pattern(self):
        """The fixture DOES match the greedy portfolio delete pattern — the
        regression below is pinned against a real thief. Pre-fix, with no
        offer armed, this turn reached surface 1 and was stolen. If this
        ever fails, #1527 was narrowed; the subjectless arm is still
        correct (any surface in the chain could claim a bare prose turn),
        but revisit the fixture."""
        from services.intent_service.pre_classifier import PreClassifier

        assert PreClassifier._matches_patterns(
            FIRST_ANSWER_PROSE.lower(), PreClassifier.PORTFOLIO_PATTERNS
        )


# ---------------------------------------------------------------------------
# 1. The subject derivation and the subjectless carrier (deterministic, pure)
# ---------------------------------------------------------------------------


class TestDeriveSubjectFromProse:
    def test_short_single_sentence_becomes_the_title(self):
        assert (
            derive_subject_from_prose("The login page crashes on Safari.")
            == "The login page crashes on Safari"
        )

    def test_first_sentence_of_long_prose_capped_at_word_boundary(self):
        title = derive_subject_from_prose(FIRST_ANSWER_PROSE)
        assert title.startswith("Deleting a project is instant and unrecoverable")
        assert len(title) <= 81  # cap + ellipsis
        assert title.endswith("…")

    def test_multiline_prose_titles_from_first_nonempty_line(self):
        prose = "\n\nSafari SSO loop\nSteps:\n1. Log in\n2. Watch it loop"
        assert derive_subject_from_prose(prose) == "Safari SSO loop"

    def test_quotes_and_terminal_punctuation_are_stripped(self):
        assert derive_subject_from_prose('"Flaky deploy checks!" ') == (
            "Flaky deploy checks"
        )


class TestSubjectlessOffer:
    def test_subject_none_builds_the_minimal_carrier(self):
        intent = _compose_intent()
        offer = build_drafted_issue_offer(intent, subject=None)
        pa = offer["pending_action"]
        assert pa["kind"] == DRAFTED_ISSUE_KIND
        assert pa["draft"] == {"title": None, "repository": None}
        assert pa["summary"] == "file the drafted issue"
        assert "Nothing was filed" in offer["decline_message"]


# ---------------------------------------------------------------------------
# 2. End-to-end: PM's shape, through the REAL process_intent
# ---------------------------------------------------------------------------


class TestSubjectlessOpeningEndToEnd:
    pytestmark = pytest.mark.asyncio

    async def test_first_answer_binds_nothing_stolen_nothing_filed(self, svc):
        """PM's shape, pinned: 'help me write a ticket' (no subject) → the
        next long prose turn (with 'delete …' substrings — the pre-fix
        steal shape) binds as the draft's subject/body. No project lookup,
        no filing, no LLM (explosive), and the draft — now named — is
        still armed."""
        sid = "e2e-1630-steal"
        r0 = await _arm_subjectless(svc, sid)
        assert "What's it about?" in r0.message

        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            r = await svc.process_intent(
                message=FIRST_ANSWER_PROSE, session_id=sid, user_id=_USER
            )

        # Nothing filed, nothing looked up (the pre-fix theft reply):
        w.assert_not_awaited()
        assert "couldn't find a project" not in r.message
        assert r.intent_data.get("action") != "manage_portfolio"
        # The turn STARTED the draft and says so honestly:
        assert "started the draft" in r.message.lower()
        assert "nothing is filed yet" in r.message.lower()
        assert r.intent_data.get("drafted_issue_pending") is True
        assert r.intent_data.get("drafted_issue_body_bound") is True
        # The draft is STILL armed, named from the answer, body verbatim:
        stored = next(iter(_pending_offers(svc).values()))
        pa = stored["pending_action"]
        assert pa["kind"] == DRAFTED_ISSUE_KIND
        assert pa["draft"]["title"].startswith("Deleting a project is instant")
        assert pa["draft"]["body"] == FIRST_ANSWER_PROSE
        # The naming is real, not cosmetic — it rides the filing intent:
        assert pa["intent"].context["title"] == pa["draft"]["title"]
        assert pa["intent"].context["description"] == FIRST_ANSWER_PROSE
        # …and the reply now teaches the file phrase (content exists):
        assert "file it as is" in r.message

    async def test_file_it_as_is_files_with_one_confirmation(self, svc):
        """'file it as is' after the first answer files in ONE confirmation:
        the created issue's title is the derived subject and its body is
        the bound prose — never the #1490 'What should the issue be about?'
        re-ask (the subjectless original message slot-fills nothing)."""
        sid = "e2e-1630-file"
        await _arm_subjectless(svc, sid)

        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()),
        ):
            await svc.process_intent(
                message=FIRST_ANSWER_PROSE, session_id=sid, user_id=_USER
            )

        created = {"number": 630, "html_url": "https://x/630", "title": "t"}
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
            patch(RESOLVER, new=AsyncMock(return_value="acme/widgets")),
        ):
            r = await svc.process_intent(
                message="file it as is", session_id=sid, user_id=_USER
            )

        w.assert_awaited_once()
        _, kwargs = w.await_args
        assert kwargs.get("title").startswith("Deleting a project is instant")
        assert kwargs.get("body") == FIRST_ANSWER_PROSE
        assert "#630" in r.message
        assert "What should the issue be about" not in r.message
        assert "(yes/no)" not in r.message
        assert _pending_offers(svc) == {}

    async def test_second_prose_turn_appends_and_keeps_the_first_title(self, svc):
        """The first answer names the draft; later prose only appends — the
        title never silently re-derives out from under the user."""
        sid = "e2e-1630-append"
        await _arm_subjectless(svc, sid)
        second = (
            "Impact: PM nearly lost a real project to this last week — one "
            "stray click and the whole thing was gone with no recovery path, "
            "which is exactly the loss a confirmation dialog exists to prevent."
        )
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()),
        ):
            await svc.process_intent(
                message=FIRST_ANSWER_PROSE, session_id=sid, user_id=_USER
            )
            r2 = await svc.process_intent(message=second, session_id=sid, user_id=_USER)

        assert "added to the draft" in r2.message.lower()
        stored = next(iter(_pending_offers(svc).values()))
        pa = stored["pending_action"]
        assert pa["draft"]["title"].startswith("Deleting a project is instant")
        assert pa["draft"]["body"] == f"{FIRST_ANSWER_PROSE}\n\n{second}"
        assert pa["intent"].context["description"] == pa["draft"]["body"]

    async def test_short_first_answer_also_binds(self, svc):
        """'A sentence on the problem is plenty' — the copy's own promise.
        A short single-sentence answer binds and names the draft (the
        discriminator's bind-default, inherited from #1627 unchanged)."""
        sid = "e2e-1630-short"
        await _arm_subjectless(svc, sid)
        answer = "The login page crashes on Safari when SSO is enabled."
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            r = await svc.process_intent(message=answer, session_id=sid, user_id=_USER)
        w.assert_not_awaited()
        assert r.intent_data.get("drafted_issue_body_bound") is True
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["draft"]["title"] == (
            "The login page crashes on Safari when SSO is enabled"
        )

    async def test_cancel_after_the_ask_drops_the_draft_honestly(self, svc):
        """Bare exits keep their exact prior routing — 'cancel' right after
        'What's it about?' drops the empty carrier, nothing filed."""
        sid = "e2e-1630-cancel"
        await _arm_subjectless(svc, sid)
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            r = await svc.process_intent(message="cancel", session_id=sid, user_id=_USER)
        w.assert_not_awaited()
        assert "Nothing was filed" in r.message
        assert _pending_offers(svc) == {}

    async def test_explicit_command_after_the_ask_still_routes_normally(self, svc):
        """The hold is not a turn lock, on the subjectless face too: an
        explicit command mid-compose abandons the empty carrier (the
        carrier's documented off-intent rule) and routes to its own
        deterministic surface — the #1190 close confirmation claims it."""
        sid = "e2e-1630-offintent"
        await _arm_subjectless(svc, sid)
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            r = await svc.process_intent(
                message="close issue #108", session_id=sid, user_id=_USER
            )
        w.assert_not_awaited()
        assert "(yes/no)" in r.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"].get("kind") != DRAFTED_ISSUE_KIND
