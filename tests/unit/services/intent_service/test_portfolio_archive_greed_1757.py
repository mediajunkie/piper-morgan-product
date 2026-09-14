"""1757 — the portfolio archive/hide/restore family requires positive
project-noun evidence, exactly as the delete family did in #1527.

The #1527 round guarded three verbs (`delete` / `remove` / `get rid of`) and
explicitly left their five siblings alone, noting the lookahead was ready to
reuse. The 2026-09-13 census ran 42 shapes through the REAL pre-classifier on
both entry paths: **28/28 non-project targets claimed portfolio/manage_portfolio**
across all six sibling patterns —

    archive ....... "archive my notes" / "archive the issue about login" / "archive it"
    hide .......... "hide my email" / "hide the sidebar"
    put away/aside  "put my files away" / "put the draft aside"
    restore ....... "restore my reminders" / "restore the deleted file"
    unarchive ..... "unarchive my notes"
    bring back .... "bring back the draft"

— and 0/14 legitimate project phrasings were affected, because every shape the
existing pins carry (test_pre_classifier.test_portfolio_patterns,
test_archived_list_1431) already contains the project noun.

Same open claim space as #1527 (the target is free text, so no blocklist can
contain it), same answer: ``PROJECT_NOUN_REQUIRED`` on the EXISTING patterns.
No new pattern, no new capture; TestExtractionPatternRatchet's pre-classifier
count is unchanged. Lower stakes than the delete family — a wrong claim here
is a non-destructive "I couldn't find a project called 'my notes'" rather than
a swallowed deletion — but the identical shape.

Layer honesty (m-43): surface 1 only, via ``PreClassifier.pre_classify`` and
``PreClassifier.detect_multiple_intents``. Denominator (m-44): the census's 28
wrong claims and 14 keeps, verbatim.
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory

NON_PROJECT_ARCHIVE_FAMILY = (
    # archive
    "archive my notes",
    "archive the issue about login",
    "archive my email",
    "archive that draft",
    "archive everything",
    "archive it",
    "archive the flayrod",  # the free-text shape, per #1527's naming
    # hide
    "hide my email",
    "hide the sidebar",
    "hide my notes",
    "hide that message",
    "hide everything",
    # put away / aside
    "put my files away",
    "put the draft aside",
    "put that away",
    "put my notes aside",
    # restore
    "restore my reminders",
    "restore the deleted file",
    "restore my notes",
    "restore everything",
    "restore it",
    # unarchive (no `(?:project\\s+)?` group of its own — the lookahead reads
    # the whole message, so it guards this shape too)
    "unarchive my notes",
    "unarchive the issue",
    "unarchive everything",
    # bring back
    "bring back the draft",
    "bring back my notes",
    "bring back that email",
    "bring back everything",
)

PROJECT_ARCHIVE_FAMILY = (
    "archive my project alpha",
    "archive the project",
    "archive project gamma",
    "hide my project alpha",
    "hide the project",
    "put project alpha away",
    "put my projects aside",
    "restore project alpha",
    "restore my project",
    "unarchive the old project",  # the issue's named edge
    "unarchive my project alpha",
    "bring back my project alpha",
    "bring back the project",
    "show my archived projects",
)


def _single(phrase):
    return PreClassifier.pre_classify(phrase)


def _multi(phrase):
    return PreClassifier.detect_multiple_intents(phrase).intents


def _portfolio_intents(intents):
    return [i for i in intents if i.action == "manage_portfolio"]


class TestNonProjectArchiveFamilyFallsThrough:
    """RED pre-fix: all 28 claimed PORTFOLIO/manage_portfolio at confidence
    1.0. GREEN: no portfolio claim — the turn falls through surface 1."""

    @pytest.mark.parametrize("phrase", NON_PROJECT_ARCHIVE_FAMILY)
    def test_single_intent_path_no_portfolio_claim(self, phrase):
        intent = _single(phrase)
        assert intent is None or intent.action != "manage_portfolio", (
            f"portfolio lane still claims {phrase!r} -> " f"{intent.category.value}/{intent.action}"
        )

    @pytest.mark.parametrize("phrase", NON_PROJECT_ARCHIVE_FAMILY)
    def test_multi_intent_path_no_portfolio_claim(self, phrase):
        assert _portfolio_intents(_multi(phrase)) == []


class TestProjectArchiveFamilyStillClaims:
    """No over-narrowing: positive project-noun evidence keeps the lane."""

    @pytest.mark.parametrize("phrase", PROJECT_ARCHIVE_FAMILY)
    def test_single_intent_path_claims(self, phrase):
        intent = _single(phrase)
        assert intent is not None, f"project archive/restore lost: {phrase!r}"
        assert intent.category == IntentCategory.PORTFOLIO
        assert intent.action == "manage_portfolio"
        assert intent.confidence == 1.0

    @pytest.mark.parametrize("phrase", PROJECT_ARCHIVE_FAMILY)
    def test_multi_intent_path_claims(self, phrase):
        assert len(_portfolio_intents(_multi(phrase))) == 1
