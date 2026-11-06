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
            # "hide project X in my portfolio": the hide literal is deleted
            # (#2271, 2026-11-06), so surface 1 claims nothing to subsume.
        ],
    )
    def test_archive_family_single_intent(self, message):
        result, actions = _intents(message)
        assert not result.is_multi_intent, (
            f"phantom STATUS sibling survives for {message!r}: {actions} "
            f"(#1884 — the archive-verb form of the #1738 defect)"
        )
        assert actions == [(IntentCategory.PORTFOLIO, "manage_portfolio")]

    def test_hide_form_claims_nothing_and_no_status_phantom(self):
        """#2271: with the hide literal deleted, surface 1 claims nothing for the
        hide form, and no STATUS phantom appears on its own."""
        result, actions = _intents("hide project X in my portfolio")
        assert actions == []
        assert not result.is_multi_intent

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
        action name alone.

        #1595 Phase 3, rule-10-licensed deletion (2026-10-09): the
        owner/repo-form "link owner/repo to ..." literal is deleted (one
        of REPO_MANAGEMENT_PATTERNS' 5 of 9 non-survivors). Swapped to
        "link repo to project X in my portfolio" (the surviving bare-
        repo(sitory) literal), confirmed empirically to produce the same
        single-intent manage_repos result — the subsumption property this
        test exists to prove is untouched by which literal claims it."""
        message = "link repo to project X in my portfolio"
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
        # #1595 Phase 3 seventh deletion (2026-10-02, PARTIAL): STATUS_PATTERNS'
        # \bstatus update\b literal is gone (among 52 of 56 deleted) — "give
        # me a status update" no longer generates ANY status claim at all,
        # so it can no longer demonstrate "a genuine status ask survives
        # beside a portfolio write." Swapped for "summarize my current
        # work", which matches \bcurrent work\b, one of STATUS_PATTERNS' 4
        # SURVIVING literals and NOT a member of status_project_noun_overlap
        # — still a genuine, distinct status ask by the same test logic.
        message = "archive project Klatch and summarize my current work"
        result, actions = _intents(message)
        categories = {c for c, _ in actions}
        assert IntentCategory.PORTFOLIO in categories
        assert IntentCategory.STATUS in categories, (
            f"over-suppression: a real status ask beside a portfolio WRITE "
            f"lost its STATUS intent: {actions}"
        )

    def test_archive_plus_project_status_phrase_keeps_both(self):
        """The #1884 issue's own probe phrasing.

        #1595 Phase 3 seventh deletion (2026-10-02, PARTIAL): STATUS_PATTERNS'
        \\bproject status\\b literal is gone — "what's my project status?"
        no longer generates any status claim. Swapped for "summarize my
        current work" (matches the surviving \\bcurrent work\\b literal,
        not in the overlap set) — same point, a genuine status ask distinct
        from the portfolio write's own vocabulary."""
        message = "archive project X and summarize my current work"
        result, actions = _intents(message)
        categories = {c for c, _ in actions}
        assert IntentCategory.PORTFOLIO in categories
        assert IntentCategory.STATUS in categories, f"over-suppression: {actions}"

    def test_two_topic_list_plus_genuine_status_phrase_now_kept(self):
        """The #1884 two-topic control, converted (2026-10-11, #1595 PORTFOLIO
        show/list/view-projects literal deleted).

        History: #1738's blunt literal check wrongly subsumed STATUS here; #1884
        fixed it so a genuine status phrase beside a list claim survives; the
        2026-10-02 swap used "summarize my current work" (surviving \\bcurrent
        work\\b literal) as the second clause.

        Now the list claim is gone, so only STATUS claims. Surface 1 DECLINES
        the whole turn (#1977 step 1: a claim set that leaves an ask-shaped
        unclaimed clause -- here the leading "list my archived projects" --
        does not serve a half), and the corpus row for this exact phrasing is a
        PLAN (list_archived_projects -> get_project_status; ruled by Arch
        2026-10-11, rule 11 / planned_at_deletion). Not deleted, not swapped:
        the two-topic fact is now pinned where it lives."""
        import scripts.inversion_phase0_baseline as p0

        message = "list my archived projects and summarize my current work"
        # Surface 1 declines: no PORTFOLIO claim, and STATUS alone is not served.
        assert PreClassifier.pre_classify(message) is None
        result, actions = _intents(message)
        assert IntentCategory.PORTFOLIO not in {c for c, _ in actions}, actions
        # The corpus carries the row, ruled a plan.
        rows = {r["phrase"]: r for r in p0.load_corpus()}
        assert message in rows, "the #1884 two-topic row must stay in the corpus"
        assert rows[message]["expected"] == "plan"
        assert rows[message]["category"] == "PORTFOLIO"

    @pytest.mark.asyncio
    async def test_two_topic_list_plus_status_plans_both_ops(self, monkeypatch):
        """Stubbed consult (no LLM): a router PLAN of both ops is handed off as
        plan_operations [list_archived_projects, get_project_status]."""
        from types import SimpleNamespace

        from services.intent_service import inversion_live
        from services.intent_service import inversion_router as ir
        from services.intent_service.inversion_router import RoutingDecision
        from services.intent_service.workflow_entries import register_default_workflows

        async def _route(message, session_state=None, **kwargs):
            return RoutingDecision(
                outcome="plan",
                operations=[
                    {
                        "operation": "list_archived_projects",
                        "args": {},
                        "confidence": 0.9,
                        "rationale": "list archived",
                    },
                    {
                        "operation": "get_project_status",
                        "args": {},
                        "confidence": 0.9,
                        "rationale": "summarize current work",
                    },
                ],
            )

        monkeypatch.setattr(ir, "route", _route)
        monkeypatch.setenv(inversion_live.LIVE_CATEGORIES_ENV, "read_status,read_portfolio")
        register_default_workflows()
        out = await inversion_live.consult_inversion_live(
            "list my archived projects and summarize my current work",
            session_id=None,
            user_id=None,
            intent_service=SimpleNamespace(intent_classifier=None),
        )
        assert out is None  # no single Intent represents a plan
        record = inversion_live.consume_live_route_provenance()
        assert record.reason == inversion_live.PLAN_STAND_DOWN
        assert [o["operation"] for o in record.plan_operations] == [
            "list_archived_projects",
            "get_project_status",
        ]


class TestUnaffectedControls:
    def test_pure_status_ask_no_portfolio_claim_keeps_status(self):
        """No PORTFOLIO claim at all -> untouched (outer category-
        membership guard).

        #1595 Phase 3 seventh deletion (2026-10-02, PARTIAL): STATUS_PATTERNS'
        \\bwhat.*working on\\b literal is gone — "What projects are we
        working on?" stopped generating any claim at all. Swapped for
        "can you summarize my current work" (matches the surviving
        \\bcurrent work\\b literal) — same point, a pure STATUS ask with no
        PORTFOLIO claim present."""
        result, actions = _intents("can you summarize my current work")
        assert actions == [(IntentCategory.STATUS, "get_project_status")]

    def test_search_projects_read_verb_single_intent_no_status_to_begin_with(self):
        """#1595 Phase 3, rule-10-licensed deletion (2026-10-09):
        PORTFOLIO_PATTERNS' "search projects for Y" literal is deleted
        (the list's only deletable literal) -- "search projects for X" no
        longer claims anything at all (confirmed empirically: is_multi
        False, actions []). Swapped to "find project X in my portfolio"
        (the surviving find-project literal, confirmed empirically to
        produce the identical single-PORTFOLIO-intent, no-STATUS-phantom
        property this control case exists to prove)."""
        result, actions = _intents("find project X in my portfolio")
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
        #
        # #1595 Phase 3 seventh deletion (2026-10-02, PARTIAL): 7 of the 9
        # original overlap literals were deleted from STATUS_PATTERNS
        # itself (52 of 56 literals went; STATUS_PATTERNS now carries only
        # \bcurrent work\b, \bproject overview\b, \bproject landscape\b,
        # \bnext milestone\b). The production overlap set
        # (`status_project_noun_overlap` in `_apply_subsumption_filter`,
        # pre_classifier.py) was pruned in the SAME commit to match — it is
        # a value copy, not independent vocabulary, so it shrinks when its
        # source shrinks. This candidate set is updated to the new value
        # copy's actual 2 members.
        #
        # 2026-10-11 (#1595): `\\bproject landscape\\b` was deleted from
        # STATUS_PATTERNS (gate GO, partial) and pruned from the overlap set in
        # the same commit; the value copy is now the single member below.
        candidates = {
            r"\bproject overview\b",
        }
        assert candidates.issubset(set(PreClassifier.STATUS_PATTERNS)), (
            "the filter's overlap set contains a literal not present in "
            "STATUS_PATTERNS — it has drifted from a value-copy into new "
            "vocabulary"
        )

    def test_genuine_status_literals_are_not_in_overlap(self):
        # #1595 Phase 3 seventh deletion (2026-10-02, PARTIAL): all 5 of the
        # original "genuine status" literals here (\bstatus update\b,
        # \bproject status\b, \bmy status\b, \bwork status\b, \bstatus
        # report\b) were deleted from STATUS_PATTERNS — none would pass
        # `assert p in PreClassifier.STATUS_PATTERNS` any more. Swapped for
        # STATUS_PATTERNS' 2 surviving literals that are NOT in the overlap
        # set (\bcurrent work\b, \bnext milestone\b) — same point: a
        # "genuine" status ask distinct from the portfolio-noun overlap.
        genuine = {
            r"\bcurrent work\b",
            r"\bnext milestone\b",
        }
        overlap = {
            r"\bproject overview\b",
        }
        assert genuine.isdisjoint(overlap)
        for p in genuine:
            assert p in PreClassifier.STATUS_PATTERNS
