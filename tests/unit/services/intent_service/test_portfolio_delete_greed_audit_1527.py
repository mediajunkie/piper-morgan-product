"""1527 (audit round) — the portfolio delete-family patterns require positive
project-noun evidence; bare `delete <anything>` no longer lands on
manage_portfolio.

The 2026-09-12 audit ran 57 representative `delete/remove/get rid of <noun>`
shapes through the REAL pre-classifier: 51 claimed portfolio, of which only 6
were legitimate project deletes. The REMINDER_TODO_NOUN_GUARD (commit
4b1a5cdb3) fixed exactly the reminder/todo vocabulary and nothing else — the
greedy `(.+)` still swallowed issues, files, drafts, notes, meetings, calendar
events, credentials, messages, repos, lists, emails, accounts, and every
free-text name ("delete the flayrod" — the shape of PM's 2026-08-18 live hit
"delete the reminder to check the flayrod" minus the reminder word).

A blocklist can never contain that space: the claim set is open (free text),
so the fix flips the discipline from negative vocabulary (block reminder
nouns) to POSITIVE EVIDENCE (require the project noun): the delete-family
patterns claim only when the text after the verb carries `project(s)`
(``PROJECT_NOUN_REQUIRED``, a lookahead guard on the EXISTING patterns — no
new pattern, no new capture; TestExtractionPatternRatchet count unchanged).

NARROWING ONLY, same contract as the reminder guard: a guarded miss is a
fall-through to later surfaces / the LLM lane, never a reroute. The
REMINDER_TODO_NOUN_GUARD stays: "delete the reminder about the alpha project"
carries the project noun but is still a reminder delete.

Layer honesty (m-43): every class here calls ``PreClassifier.pre_classify``
and/or ``PreClassifier.detect_multiple_intents`` directly — the two entry
surfaces that consult PORTFOLIO_PATTERNS. Denominator (m-44): the decline
set below is the audit's 45 wrong claims, thinned to per-domain-per-verb
representatives (32 phrases); the keep set is every project-noun phrasing the
existing suites pin plus the bare-"project" edge.
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory

# Wrong claims found by the 2026-09-12 audit — every domain noun the system
# actually has, plus free-text. RED pre-fix: all of these claimed
# PORTFOLIO/manage_portfolio at confidence 1.0.
NON_PROJECT_DELETES = (
    # issues / tickets
    "delete the issue about login",
    "delete issue 1234",
    "remove my issue about the login bug",
    "delete that ticket",
    # files / uploads / documents
    "delete the file I uploaded",
    "remove the csv I uploaded yesterday",
    "delete the document about onboarding",
    "get rid of the pdf",
    "delete my upload",
    # drafts / notes
    "delete the draft",
    "remove the drafted issue",
    "delete my notes",
    "delete the note about the meeting",
    # meetings / calendar
    "delete my 3pm meeting",
    "remove the calendar event",
    "delete the event on friday",
    # credentials
    "delete my api key",
    "delete the github token",
    "remove my credentials",
    # messages / memory
    "delete my messages",
    "delete that message",
    "delete what you remember about me",
    # account / repo / list / email
    "delete my account",
    "delete the repo",
    "delete my default repo",
    "delete my shopping list",
    "delete the email from john",
    # free text — the open set no blocklist can cover
    "delete the flayrod",
    "delete everything",
    "delete it",
    "remove the thing we talked about",
    "get rid of all of it",
)

# Legitimate project-lane deletes — positive evidence present; the guard must
# not touch these (superset of the pins in test_reminder_delete_misroute_1527
# and test_pre_classifier.test_portfolio_patterns).
PROJECT_DELETES = (
    "delete the alpha project",
    "delete my project alpha",
    "delete my project Gamma",
    "delete project piper morgan",
    "remove the project Delta",
    "remove the old project",
    "get rid of my test project",
    "get rid of the alpha project",
    "delete my project",  # bare — claims, handler asks which
)

# Project noun present BUT reminder/todo vocabulary too — the negative guard
# still out-ranks the positive evidence (a reminder ABOUT a project is a
# reminder delete, not a project delete).
REMINDER_WITH_PROJECT_NOUN = (
    "delete the reminder about the alpha project",
    "remove my todo about the project",
    "delete the task for project alpha",
)


def _single(phrase):
    return PreClassifier.pre_classify(phrase)


def _multi(phrase):
    return PreClassifier.detect_multiple_intents(phrase).intents


def _portfolio_intents(intents):
    return [i for i in intents if i.action == "manage_portfolio"]


class TestNonProjectDeletesFallThrough:
    """RED pre-audit-fix: PORTFOLIO/manage_portfolio claimed every one of
    these. GREEN: no portfolio claim — the turn falls through this surface."""

    @pytest.mark.parametrize("phrase", NON_PROJECT_DELETES)
    def test_single_intent_path_no_portfolio_claim(self, phrase):
        intent = _single(phrase)
        assert intent is None or intent.action != "manage_portfolio", (
            f"portfolio lane still claims {phrase!r} -> " f"{intent.category}/{intent.action}"
        )

    @pytest.mark.parametrize("phrase", NON_PROJECT_DELETES)
    def test_multi_intent_path_no_portfolio_claim(self, phrase):
        assert _portfolio_intents(_multi(phrase)) == []


class TestProjectDeletesStillClaim:
    """No over-narrowing: positive project-noun evidence keeps the lane."""

    @pytest.mark.parametrize("phrase", PROJECT_DELETES)
    def test_single_intent_path_claims(self, phrase):
        intent = _single(phrase)
        assert intent is not None, f"project delete lost: {phrase!r}"
        assert intent.category == IntentCategory.PORTFOLIO
        assert intent.action == "manage_portfolio"
        assert intent.confidence == 1.0

    @pytest.mark.parametrize("phrase", PROJECT_DELETES)
    def test_multi_intent_path_claims(self, phrase):
        assert len(_portfolio_intents(_multi(phrase))) == 1


class TestReminderGuardOutranksProjectNoun:
    """The 4b1a5cdb3 negative guard survives the positive-evidence change."""

    @pytest.mark.parametrize("phrase", REMINDER_WITH_PROJECT_NOUN)
    def test_single_intent_path_declines(self, phrase):
        intent = _single(phrase)
        assert (
            intent is None or intent.action != "manage_portfolio"
        ), f"reminder guard lost to project noun on {phrase!r}"

    @pytest.mark.parametrize("phrase", REMINDER_WITH_PROJECT_NOUN)
    def test_multi_intent_path_declines(self, phrase):
        assert _portfolio_intents(_multi(phrase)) == []
