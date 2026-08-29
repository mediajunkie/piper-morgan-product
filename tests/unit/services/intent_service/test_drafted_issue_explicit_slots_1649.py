"""#1649 — the draft flow ignored EXPLICITLY-given subject and description
(teach-then-ignore; PM live 2026-08-18).

PM's exact shape: 'let's open a new issue, with the subject "issue body
test" and description "…"' — both slots given, in quotes. The collaborate
gate asked "What's it about?" anyway (no extraction knew the subject/
description marker words), then derived a truncated title from PM's
follow-up prose; the stated subject was never used.

The fix, at the arm seam:

- ``_slotfill_issue_request`` extracts quoted subject/title/called/named
  and description/body forms — plus the anchored UNQUOTED equivalents —
  from the ORIGINAL ask, before anything is asked.
- Both slots given → the shaped draft presents ready for "file it as is",
  no question; the stated slots ride ``intent.context`` so that is what
  actually files.
- One slot given → ask only for the gap. A body-only draft's first bound
  prose is the TITLE answer (named, not appended into the given body).
- No explicit slots → the #1630 derive-from-prose path, byte-for-byte
  unchanged (its suite pins it).

Extraction is deterministic and anchored to stated marker words — loose
nouns are never scavenged into a title (a wrong confident title is worse
than the question).

Layer honesty (m-43): the end-to-end classes drive the REAL
``IntentService.process_intent`` for the follow-up turns with an explosive
LLM — offer-seam turns must resolve deterministically before any
classification surface. Turn 1 (the ask itself) runs at the handler seam,
mirroring the #1630 suite (classifying the opening ask is not this
issue's layer).
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.collaboration_gate import build_collaboration_response
from services.intent_service.drafted_issue import (
    DRAFTED_ISSUE_KIND,
    build_drafted_issue_offer,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory

GATE = "services.intent_service.collaboration_gate"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
RESOLVER = "services.integrations.github.repo_resolver.get_user_default_repo"

# PM's transcript shape, pinned. The description carries apostrophes on
# purpose — the paired-quote capture must not truncate at "issue's".
EXPLICIT_SUBJECT = "issue body test"
EXPLICIT_DESCRIPTION = (
    "Testing whether an explicitly given description lands in the filed "
    "issue's body verbatim, instead of Piper asking what it's about."
)
EXPLICIT_ASK = (
    f'let\'s open a new issue, with the subject "{EXPLICIT_SUBJECT}" '
    f'and description "{EXPLICIT_DESCRIPTION}"'
)

_USER = "3f7b8a52-1649-4b00-9e00-000000001649"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Offer-seam
    turns must resolve deterministically, before classification."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1649 offer-seam turns must "
            "resolve deterministically"
        )


def _compose_intent(message, action="create_ticket"):
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


def _slotfill():
    return IntentService._slotfill_issue_request


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


async def _arm(svc, sid, message):
    """Turn 1 (the ask) at the handler seam — the gate holds and arms."""
    intent = _compose_intent(message)
    with (
        patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
        patch(f"{ROUTER}.initialize", new=AsyncMock()),
        patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        patch(f"{ROUTER}.create_issue", new=AsyncMock()),
    ):
        return await svc._handle_create_issue(intent, "wf-1", sid, user_id=_USER)


# ---------------------------------------------------------------------------
# 1. Slot extraction (deterministic, pure)
# ---------------------------------------------------------------------------


class TestExplicitSlotExtraction:
    def test_pm_exact_shape_extracts_both_slots(self):
        slots = _slotfill()(EXPLICIT_ASK)
        assert slots.get("title") == EXPLICIT_SUBJECT
        # Verbatim — apostrophes inside the double-quoted span survive.
        assert slots.get("body") == EXPLICIT_DESCRIPTION

    def test_quoted_subject_alone(self):
        slots = _slotfill()('let\'s open a new issue with the subject "flaky login"')
        assert slots.get("title") == "flaky login"
        assert "body" not in slots

    def test_quoted_title_called_and_named_forms(self):
        assert (
            _slotfill()('open an issue called "Login loop on Safari"')["title"]
            == "Login loop on Safari"
        )
        assert _slotfill()('file a ticket named "Retry storm"')["title"] == ("Retry storm")
        assert _slotfill()('the title is "Retry storm"')["title"] == "Retry storm"

    def test_with_the_body_quoted_form(self):
        slots = _slotfill()(
            'create an issue titled "Flaky deploys" with the body "CI fails one ' 'run in five."'
        )
        assert slots["title"] == "Flaky deploys"
        assert slots["body"] == "CI fails one run in five."

    def test_quoted_description_alone(self):
        slots = _slotfill()(
            "let's open a new issue with the description \"Repro: log in twice, "
            'watch the session drop."'
        )
        assert "title" not in slots
        assert slots["body"] == "Repro: log in twice, watch the session drop."

    def test_unquoted_subject_and_description(self):
        slots = _slotfill()(
            "open a ticket with the subject login flakiness and description "
            "users cannot log in reliably"
        )
        assert slots["title"] == "login flakiness"
        assert slots["body"] == "users cannot log in reliably"

    def test_unquoted_subject_strips_trailing_repo_clause(self):
        slots = _slotfill()("open an issue with the subject flaky login in acme/widgets")
        assert slots["title"] == "flaky login"
        assert slots["repository"] == "acme/widgets"

    def test_about_form_is_bounded_by_a_description_clause(self):
        slots = _slotfill()(
            "create an issue about the login timeout and the description is " "users cannot log in"
        )
        assert slots["title"] == "the login timeout"
        assert slots["body"] == "users cannot log in"

    # -- no scavenging: the anchored forms never invent a title ------------

    def test_subjectless_ask_extracts_nothing(self):
        assert "title" not in _slotfill()("help me write a ticket")
        assert "body" not in _slotfill()("help me write a ticket")

    def test_loose_subject_noun_is_not_scavenged(self):
        # "subject" as an ordinary noun (no quoted span, no with-the anchor)
        # must not grow a confident wrong title.
        assert "title" not in _slotfill()("the email subject line is broken, file a ticket")

    def test_noun_phrase_description_does_not_truncate_the_about_title(self):
        # "title and description" as a NOUN PHRASE (no filler/colon/quote
        # after the marker) is content, not slot-giving: the about-form
        # keeps the whole tail and no body is scavenged.
        slots = _slotfill()("create an issue about the title and description fields being swapped")
        assert slots["title"] == "the title and description fields being swapped"
        assert "body" not in slots

    def test_bare_unquoted_description_requires_a_dictated_subject(self):
        # Unmarked ask + bare content after "description" (no filler): a
        # noun phrase like "the description field bug" must not scavenge.
        slots = _slotfill()("create an issue with the description field bug")
        assert "body" not in slots
        assert "title" not in slots

    def test_1543_about_form_unchanged_without_a_description_clause(self):
        slots = _slotfill()(
            "create an issue in mediajunkie/test-piper-morgan about testing regressions"
        )
        assert slots["title"] == "testing regressions"
        assert slots["repository"] == "mediajunkie/test-piper-morgan"


# ---------------------------------------------------------------------------
# 2. The carrier and the copy (pure)
# ---------------------------------------------------------------------------


class TestOfferAndCopy:
    def test_offer_seeds_the_explicit_body(self):
        intent = _compose_intent(EXPLICIT_ASK)
        offer = build_drafted_issue_offer(
            intent, subject=EXPLICIT_SUBJECT, body=EXPLICIT_DESCRIPTION
        )
        draft = offer["pending_action"]["draft"]
        assert draft["title"] == EXPLICIT_SUBJECT
        assert draft["body"] == EXPLICIT_DESCRIPTION

    def test_offer_without_body_keeps_the_1630_minimal_shape(self):
        # The subjectless minimal carrier the #1630 suite pins: no body key.
        intent = _compose_intent("help me write a ticket")
        offer = build_drafted_issue_offer(intent, subject=None)
        assert offer["pending_action"]["draft"] == {
            "title": None,
            "repository": None,
        }

    def test_full_slots_copy_presents_the_draft_and_asks_nothing(self):
        msg = build_collaboration_response(
            subject=EXPLICIT_SUBJECT, body=EXPLICIT_DESCRIPTION, draft_bound=True
        )
        assert f"**Title**: {EXPLICIT_SUBJECT}" in msg
        assert EXPLICIT_DESCRIPTION in msg
        assert "file it as is" in msg
        assert "What's it about?" not in msg
        assert "What should the body say" not in msg

    def test_body_only_copy_asks_only_for_the_title(self):
        msg = build_collaboration_response(body=EXPLICIT_DESCRIPTION, draft_bound=True)
        assert EXPLICIT_DESCRIPTION in msg
        assert "What should the title be?" in msg
        assert "What's it about?" not in msg
        assert "What should the body say" not in msg
        # Never-teach-unbound (#1571): no file phrase before the draft has
        # a title.
        assert "file it as is" not in msg

    def test_subject_only_copy_unchanged(self):
        msg = build_collaboration_response(subject="flaky login", draft_bound=True)
        assert "**Title**: flaky login" in msg
        assert "What should the body say" in msg
        assert "file it as is" in msg

    def test_no_slots_copy_unchanged(self):
        msg = build_collaboration_response()
        assert "What's it about?" in msg


# ---------------------------------------------------------------------------
# 3. End-to-end: PM's transcript, through the REAL process_intent
# ---------------------------------------------------------------------------


class TestExplicitSlotsEndToEnd:
    pytestmark = pytest.mark.asyncio

    async def test_explicit_ask_arms_the_shaped_draft_no_question(self, svc):
        """PM's shape, pinned: both slots given → the reply presents the
        shaped draft (stated title, stated description), teaches "file it
        as is", and asks NO slot question."""
        sid = "e2e-1649-arm"
        r = await _arm(svc, sid, EXPLICIT_ASK)

        assert "What's it about?" not in r.message
        assert "What should the body say" not in r.message
        assert f"**Title**: {EXPLICIT_SUBJECT}" in r.message
        assert EXPLICIT_DESCRIPTION in r.message
        assert "file it as is" in r.message
        assert r.intent_data.get("drafted_issue_pending") is True

        stored = next(iter(_pending_offers(svc).values()))
        pa = stored["pending_action"]
        assert pa["kind"] == DRAFTED_ISSUE_KIND
        assert pa["draft"]["title"] == EXPLICIT_SUBJECT
        assert pa["draft"]["body"] == EXPLICIT_DESCRIPTION
        # The slots are real, not cosmetic — they ride the filing intent:
        assert pa["intent"].context["title"] == EXPLICIT_SUBJECT
        assert pa["intent"].context["description"] == EXPLICIT_DESCRIPTION

    async def test_file_it_as_is_files_with_the_stated_slots(self, svc):
        """'file it as is' files with THAT title and THAT description — the
        create_issue kwargs are the stated strings, verbatim."""
        sid = "e2e-1649-file"
        await _arm(svc, sid, EXPLICIT_ASK)

        created = {"number": 1649, "html_url": "https://x/1649", "title": "t"}
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
        assert kwargs.get("title") == EXPLICIT_SUBJECT
        assert kwargs.get("body") == EXPLICIT_DESCRIPTION
        assert "#1649" in r.message
        assert "What should the issue be about" not in r.message
        assert _pending_offers(svc) == {}

    async def test_subject_only_ask_asks_only_for_the_body(self, svc):
        sid = "e2e-1649-subject-only"
        r = await _arm(svc, sid, 'let\'s open a new issue with the subject "flaky login"')
        assert "What's it about?" not in r.message
        assert "**Title**: flaky login" in r.message
        assert "What should the body say" in r.message

    async def test_body_only_ask_asks_only_for_the_title_then_files(self, svc):
        """Description given, subject missing → asks only for the title; the
        short answer NAMES the draft (it is not appended into the given
        body); 'file it as is' files with the answered title and the stated
        description."""
        sid = "e2e-1649-body-only"
        ask = (
            "let's open a new issue with the description \"Repro: log in "
            'twice, watch the session drop."'
        )
        r0 = await _arm(svc, sid, ask)
        assert "What's it about?" not in r0.message
        assert "What should the body say" not in r0.message
        assert "What should the title be?" in r0.message

        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            r1 = await svc.process_intent(message="issue body test", session_id=sid, user_id=_USER)
        w.assert_not_awaited()
        assert "that's the title" in r1.message.lower()
        stored = next(iter(_pending_offers(svc).values()))
        pa = stored["pending_action"]
        assert pa["draft"]["title"] == "issue body test"
        # The title answer is NOT duplicated into the explicit description:
        assert pa["draft"]["body"] == "Repro: log in twice, watch the session drop."

        created = {"number": 42, "html_url": "https://x/42", "title": "t"}
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
            patch(RESOLVER, new=AsyncMock(return_value="acme/widgets")),
        ):
            r2 = await svc.process_intent(message="file it as is", session_id=sid, user_id=_USER)
        w.assert_awaited_once()
        _, kwargs = w.await_args
        assert kwargs.get("title") == "issue body test"
        assert kwargs.get("body") == "Repro: log in twice, watch the session drop."
        assert "#42" in r2.message

    async def test_no_explicit_slots_path_unchanged(self, svc):
        """The #1630 face is untouched: a subjectless ask still asks
        "What's it about?" and arms the minimal carrier."""
        sid = "e2e-1649-subjectless"
        r = await _arm(svc, sid, "help me write a ticket")
        assert "What's it about?" in r.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["draft"] == {
            "title": None,
            "repository": None,
        }


# ---------------------------------------------------------------------------
# 4. v64 REWORK (PM live round 2026-08-29) — quoted slot values, never raw
#    messages
# ---------------------------------------------------------------------------

# PM's exact first-turn phrasing (single straight quotes), plus the
# smart-quote form a chat client auto-converts it into — the deployed
# titled-pattern knew straight and curly-DOUBLE quotes but not
# curly-single, which is the only mechanism that reproduces PM's observed
# split (description captured, title dropped).
PM_V64_ASK = "draft an issue titled 'Login timeout' with description 'sessions expire after 5 min'"
PM_V64_ASK_CURLY = "draft an issue titled ‘Login timeout’ with description ‘sessions expire after 5 min’"
PM_V64_ASK_DOUBLE = 'draft an issue titled "Login timeout" with description "sessions expire after 5 min"'
# PM's exact correction turn — live, this ENTIRE sentence became the title.
PM_V64_CORRECTION = "title should be 'Login timeout' as I indicated in my initial request"
V64_TITLE = "Login timeout"
V64_DESCRIPTION = "sessions expire after 5 min"
# A body-only ask to reproduce the state PM was actually in when the
# correction turn arrived (title missing, description given, title re-ask
# open).
V64_BODY_ONLY_ASK = "draft an issue with the description 'sessions expire after 5 min'"


class TestV64FirstTurnExtraction:
    """Slot extraction fills the title on the FIRST turn — every quote
    style, including the smart quotes clients type on PM's behalf."""

    def test_pm_exact_straight_single_quotes(self):
        slots = _slotfill()(PM_V64_ASK)
        assert slots.get("title") == V64_TITLE
        assert slots.get("body") == V64_DESCRIPTION

    def test_curly_single_quotes_regression(self):
        slots = _slotfill()(PM_V64_ASK_CURLY)
        assert slots.get("title") == V64_TITLE
        assert slots.get("body") == V64_DESCRIPTION

    def test_double_quotes(self):
        slots = _slotfill()(PM_V64_ASK_DOUBLE)
        assert slots.get("title") == V64_TITLE
        assert slots.get("body") == V64_DESCRIPTION

    def test_curly_double_quotes(self):
        slots = _slotfill()("draft an issue titled “Login timeout” with description “sessions expire after 5 min”")
        assert slots.get("title") == V64_TITLE
        assert slots.get("body") == V64_DESCRIPTION


class TestTitleAnswerExtraction:
    """The pure slot-ANSWER extractor: a dictated/quoted value IS the
    value; metacommentary never enters the slot; bare answers return None
    (the derive path keeps handling them verbatim)."""

    def _extract(self):
        from services.intent_service.drafted_issue import extract_title_answer

        return extract_title_answer

    def test_pm_exact_correction_extracts_the_quoted_value(self):
        assert self._extract()(PM_V64_CORRECTION) == V64_TITLE

    def test_double_quoted_correction(self):
        assert (
            self._extract()('title should be "Login timeout" as I indicated in my initial request')
            == V64_TITLE
        )

    def test_bare_quoted_answer_both_styles(self):
        assert self._extract()("'Login timeout'") == V64_TITLE
        assert self._extract()('"Login timeout"') == V64_TITLE
        assert self._extract()("‘Login timeout’") == V64_TITLE
        assert self._extract()("“Login timeout”") == V64_TITLE

    def test_bare_unquoted_answer_is_none_for_the_derive_path(self):
        assert self._extract()("Login timeout") is None

    def test_unquoted_dictation_strips_metacommentary(self):
        assert self._extract()("the title should be Login timeout as I indicated earlier") == V64_TITLE

    def test_body_prose_with_incidental_quotes_is_never_stolen(self):
        # A quoted span floating inside genuine body prose is content —
        # extracting it would replay the #1627 theft in miniature.
        assert self._extract()("Users see 'session expired' after login and lose work") is None

    def test_prose_about_the_subject_is_not_a_dictation(self):
        assert self._extract()("the subject is being spammed with retries") is None


class TestV64EndToEnd:
    """PM's two failing exchanges, pinned through the REAL process_intent
    for the answer turns."""

    pytestmark = pytest.mark.asyncio

    async def test_pm_first_turn_fills_both_slots_no_reask(self, svc):
        """Exchange 1 fixed: titled + quoted value fills the slot on the
        FIRST turn — the shaped draft presents, nothing re-asks."""
        for sid, ask in (
            ("e2e-v64-arm-straight", PM_V64_ASK),
            ("e2e-v64-arm-curly", PM_V64_ASK_CURLY),
        ):
            r = await _arm(svc, sid, ask)
            assert "What should the title be?" not in r.message
            assert "What's it about?" not in r.message
            assert f"**Title**: {V64_TITLE}" in r.message
            assert V64_DESCRIPTION in r.message
            assert "file it as is" in r.message
            pa = _pending_offers(svc)[sid]["pending_action"]
            assert pa["draft"]["title"] == V64_TITLE
            assert pa["draft"]["body"] == V64_DESCRIPTION

    async def test_pm_correction_turn_titles_the_quoted_value_only(self, svc):
        """Exchange 2 fixed: the correction turn's QUOTED value becomes the
        title — the metacommentary sentence never does."""
        sid = "e2e-v64-correction"
        r0 = await _arm(svc, sid, V64_BODY_ONLY_ASK)
        assert "What should the title be?" in r0.message

        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            r1 = await svc.process_intent(message=PM_V64_CORRECTION, session_id=sid, user_id=_USER)
        w.assert_not_awaited()
        assert "that's the title" in r1.message.lower()
        pa = _pending_offers(svc)[sid]["pending_action"]
        assert pa["draft"]["title"] == V64_TITLE
        assert "as I indicated" not in pa["draft"]["title"]
        # The stated description survives, unpolluted by the correction:
        assert pa["draft"]["body"] == V64_DESCRIPTION
        assert pa["intent"].context["title"] == V64_TITLE

        created = {"number": 64, "html_url": "https://x/64", "title": "t"}
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
            patch(RESOLVER, new=AsyncMock(return_value="acme/widgets")),
        ):
            r2 = await svc.process_intent(message="file it as is", session_id=sid, user_id=_USER)
        w.assert_awaited_once()
        _, kwargs = w.await_args
        assert kwargs.get("title") == V64_TITLE
        assert kwargs.get("body") == V64_DESCRIPTION

    async def test_straight_bare_answer_still_titles_verbatim(self, svc):
        """A bare unquoted answer keeps working exactly as before — the
        extractor only overrides when something is explicitly dictated."""
        sid = "e2e-v64-bare-answer"
        await _arm(svc, sid, V64_BODY_ONLY_ASK)
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            r = await svc.process_intent(message="Login timeout", session_id=sid, user_id=_USER)
        w.assert_not_awaited()
        pa = _pending_offers(svc)[sid]["pending_action"]
        assert pa["draft"]["title"] == V64_TITLE
        assert pa["draft"]["body"] == V64_DESCRIPTION

    async def test_set_aside_path_stays_intact(self, svc):
        """PM's 'no' worked live — pin it so the rework can't cost it."""
        sid = "e2e-v64-set-aside"
        await _arm(svc, sid, V64_BODY_ONLY_ASK)
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            r = await svc.process_intent(message="no", session_id=sid, user_id=_USER)
        w.assert_not_awaited()
        assert "set that draft aside" in r.message
        assert _pending_offers(svc) == {}
