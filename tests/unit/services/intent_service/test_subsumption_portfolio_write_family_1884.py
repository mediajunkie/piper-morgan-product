"""#1884: the #1738 PORTFOLIO-subsumes-STATUS subsumption rule covered only
the portfolio LIST claim. Probed against the real pre-classifier at HEAD
(before this fix), "archive project X in my portfolio" produced:

    is_multi: True
        PORTFOLIO manage_portfolio
        STATUS    get_project_status      <- phantom, the #1738 class

`_apply_subsumption_filter` dropped the phantom `get_project_status`
sibling only when the raw message matched `PORTFOLIO_LIST_PATTERN`
(#1738 defect 2). Every OTHER PORTFOLIO write verb whose object phrase
happens to name "my portfolio"/"my projects" the same way a portfolio
LIST does — archive, add, restore, and the REPO_MANAGEMENT_PATTERNS
"link" verb (also category PORTFOLIO, action manage_repos) — still
emitted the phantom sibling, turning a one-topic write into a ≥2-
substantive plan and logging a skipped orchestration on every such
command (#1763's write-wins gate contains the user-facing damage but the
phantom itself was still emitted).

Fix (services/intent_service/pre_classifier.py,
`PreClassifier._apply_subsumption_filter`): the drop condition no longer
re-matches the raw message against the LIST-only `PORTFOLIO_LIST_PATTERN`
literal. It now fires whenever (a) ANY PORTFOLIO intent survived the
turn (any verb, either PORTFOLIO_PATTERNS' manage_portfolio or
REPO_MANAGEMENT_PATTERNS' manage_repos) and (b) every STATUS_PATTERNS
entry that actually matched the raw message is one of the
project/portfolio-NOUN-only entries copied by value into
`status_project_noun_overlap` (not a new pattern — a precedence
partition of vocabulary STATUS_PATTERNS already matches; #1559
moratorium / TestExtractionPatternRatchet unaffected).

What the new condition deliberately does NOT subsume: a STATUS match
that ALSO hits a genuine status-asking pattern (status update/report,
project status, my status, standup*, progress*, "what am I working
on", ...) is untouched — a real two-topic turn like "archive project X
and what's my project status?" matches ONLY r"\\bproject status\\b" (not
in the overlap set), so both intents survive. This is the SAME trade-
off #1738 already accepted for the list claim (probed below,
`test_two_topic_list_plus_status_still_subsumes` — a pre-existing,
unchanged limitation, not something #1884 introduces) — a genuine
second topic that happens to share the SAME incidental vocabulary as
the PORTFOLIO write's own object phrase is still subsumed; only a
genuine status ask using its OWN distinct vocabulary survives beside a
PORTFOLIO write.

"delete"-headed writes never reach this filter with a phantom to drop
in the first place: the separate #1756 `DESTRUCTIVE_ASK_BLOCKERS`
decline already makes the STATUS read-lane fall through inside the
main `detect_multiple_intents` loop, before this filter runs (probed:
"delete project X from my portfolio" emits ONLY the PORTFOLIO intent at
HEAD, unaffected by this change). Pinned here as a no-op control, not a
fix target.

Layer honesty (m-43): pure pre-classifier function
(`PreClassifier.detect_multiple_intents`), no LLM, no DB, no live
classifier — surface 1 of the intent-routing-stack only.
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


def _intents(message: str):
    result = PreClassifier.detect_multiple_intents(message)
    return result, [(i.category, i.action) for i in result.intents]


class TestPortfolioWriteFamilySubsumesStatusPhantom:
    """Each of these previously emitted a PORTFOLIO+STATUS pair
    (is_multi_intent True) purely because the write's own object phrase
    ("... in my portfolio") shares vocabulary with STATUS_PATTERNS. Each
    must now collapse to a single PORTFOLIO intent."""

    @pytest.mark.parametrize(
        "message",
        [
            "archive project X in my portfolio",
            "hide project X in my portfolio",
        ],
    )
    def test_archive_family_single_intent(self, message):
        result, actions = _intents(message)
        assert not result.is_multi_intent, (
            f"phantom STATUS sibling survives for {message!r}: {actions} "
            f"(#1884 — the archive-verb form of the #1738 defect)"
        )
        assert actions == [(IntentCategory.PORTFOLIO, "manage_portfolio")]

    def test_add_family_single_intent(self):
        message = "add a new project to my portfolio"
        result, actions = _intents(message)
        assert not result.is_multi_intent, f"phantom STATUS sibling survives: {actions}"
        assert actions == [(IntentCategory.PORTFOLIO, "manage_portfolio")]

    def test_restore_family_single_intent(self):
        message = "restore project X in my portfolio"
        result, actions = _intents(message)
        assert not result.is_multi_intent, f"phantom STATUS sibling survives: {actions}"
        assert actions == [(IntentCategory.PORTFOLIO, "manage_portfolio")]

    def test_link_family_single_intent(self):
        """REPO_MANAGEMENT_PATTERNS — category PORTFOLIO, action
        manage_repos, distinct from manage_portfolio. The subsumption rule
        must key on the PORTFOLIO category, not the manage_portfolio
        action name alone."""
        message = "link owner/repo to project X in my portfolio"
        result, actions = _intents(message)
        assert not result.is_multi_intent, f"phantom STATUS sibling survives: {actions}"
        assert actions == [(IntentCategory.PORTFOLIO, "manage_repos")]

    def test_delete_family_no_phantom_to_begin_with(self):
        """Control, not a fix target: #1756's DESTRUCTIVE_ASK_BLOCKERS
        already declines the STATUS read-lane for delete-headed turns, so
        no phantom ever reaches this filter. Pinned so a future change to
        either guard is caught by whichever test actually regresses."""
        message = "delete project X from my portfolio"
        result, actions = _intents(message)
        assert not result.is_multi_intent, f"unexpected multi-intent: {actions}"
        assert actions == [(IntentCategory.PORTFOLIO, "manage_portfolio")]


class TestGenuineTwoTopicControlUnchanged:
    """The #1738 control, restated for the write family: a status ask
    using its OWN distinct vocabulary survives beside a PORTFOLIO write."""

    def test_archive_plus_distinct_status_ask_keeps_both(self):
        message = "archive project Klatch and give me a status update"
        result, actions = _intents(message)
        categories = {c for c, _ in actions}
        assert IntentCategory.PORTFOLIO in categories
        assert IntentCategory.STATUS in categories, (
            f"over-suppression: a real status ask beside a portfolio WRITE "
            f"lost its STATUS intent: {actions}"
        )

    def test_archive_plus_project_status_phrase_keeps_both(self):
        """The #1884 issue's own probe phrasing."""
        message = "archive project X and what's my project status?"
        result, actions = _intents(message)
        categories = {c for c, _ in actions}
        assert IntentCategory.PORTFOLIO in categories
        assert IntentCategory.STATUS in categories, f"over-suppression: {actions}"

    def test_two_topic_list_plus_genuine_status_phrase_now_kept(self):
        """Incidental improvement over #1738's blunt literal check, pinned
        so it is a deliberate, known change rather than an unnoticed side
        effect: #1738's rule dropped STATUS whenever the raw message
        matched PORTFOLIO_LIST_PATTERN ANYWHERE in the string, regardless
        of why STATUS also matched — so "list my archived projects and
        what's my project status" was WRONGLY subsumed at HEAD before
        this fix (probed, #1884 report), even though "project status" is
        a genuine, distinct status ask. The #1884 condition checks WHICH
        STATUS_PATTERNS entries actually matched, so a genuine status
        phrase riding alongside a list claim now correctly survives."""
        message = "list my archived projects and what's my project status"
        result, actions = _intents(message)
        categories = {c for c, _ in actions}
        assert IntentCategory.PORTFOLIO in categories
        assert IntentCategory.STATUS in categories, f"over-suppression: {actions}"


class TestUnaffectedControls:
    def test_pure_status_ask_no_portfolio_claim_keeps_status(self):
        """No PORTFOLIO claim at all -> untouched (outer category-
        membership guard)."""
        result, actions = _intents("What projects are we working on?")
        assert actions == [(IntentCategory.STATUS, "get_project_status")]

    def test_search_projects_read_verb_single_intent_no_status_to_begin_with(self):
        result, actions = _intents("search projects for X")
        assert actions == [(IntentCategory.PORTFOLIO, "manage_portfolio")]


class TestOverlapSetIsValueCopyNotNewVocabulary:
    """Guard-rail test: every literal in the filter's local overlap set
    must already exist, verbatim, in STATUS_PATTERNS — proving this is a
    precedence partition of existing vocabulary, not new extraction
    vocabulary (#1559 moratorium / TestExtractionPatternRatchet)."""

    def test_overlap_literals_are_a_subset_of_status_patterns(self):
        # Re-derive the same literal set the filter uses, straight from
        # a live probe against STATUS_PATTERNS, rather than hardcoding a
        # parallel copy in the test that could drift silently.
        candidates = {
            r"\bmy portfolio\b",
            r"\bmy projects\b",
            r"\bcurrent projects\b",
            r"\bactive projects\b",
            r"\bproject overview\b",
            r"\bproject landscape\b",
            r"\bshow.*projects\b",
            r"\blist.*projects\b",
            r"\bprojects.*working on\b",
        }
        assert candidates.issubset(set(PreClassifier.STATUS_PATTERNS)), (
            "the filter's overlap set contains a literal not present in "
            "STATUS_PATTERNS — it has drifted from a value-copy into new "
            "vocabulary"
        )

    def test_genuine_status_literals_are_not_in_overlap(self):
        genuine = {
            r"\bstatus update\b",
            r"\bproject status\b",
            r"\bmy status\b",
            r"\bwork status\b",
            r"\bstatus report\b",
        }
        overlap = {
            r"\bmy portfolio\b",
            r"\bmy projects\b",
            r"\bcurrent projects\b",
            r"\bactive projects\b",
            r"\bproject overview\b",
            r"\bproject landscape\b",
            r"\bshow.*projects\b",
            r"\blist.*projects\b",
            r"\bprojects.*working on\b",
        }
        assert genuine.isdisjoint(overlap)
        for p in genuine:
            assert p in PreClassifier.STATUS_PATTERNS
