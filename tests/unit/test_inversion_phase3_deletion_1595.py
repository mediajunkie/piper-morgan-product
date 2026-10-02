"""#1595 Phase 3 — pinning tests for the deletion-ratchet INSTRUMENT
(scripts/inversion_phase3_deletion_gate.py).

Epic-0's own conditions on the endpoint (dev/2026/09/25/inversion-epic0-
remaining-scope-2026-09-25.md, unit 5; issue #1595 body): "Deletion ratchet
asserts corpus non-regression ALONGSIDE shrink" and "pattern-to-corpus-case
conversion is a STEP IN the deletion procedure, not an intention." This
suite pins the census mechanics (real corpus, real pre-classifier, real
router reports, NO LLM calls anywhere here) and the non-regression checker
that a future deletion commit's ratchet test will lean on.

This suite does not itself delete anything (that happened in
``services/intent_service/pre_classifier.py``, same commit). As of
2026-10-02 ``DELETED_PATTERN_LISTS`` carries SIX real entries
(REMINDER_PATTERNS, REMINDER_QUERY_PATTERNS, TODO_QUERY_PATTERNS,
CALENDAR_QUERY_PATTERNS, TEMPORAL_PATTERNS, GITHUB_QUERY_PATTERNS — all
emptied to ``[]``, kept as tombstones). ``TestNonRegressionMechanism`` still
proves the non-regression MECHANISM against synthetic entries (never the
real ledger); ``TestDeletedPatternListsLedger`` now also proves the real
ledger's six entries actually pass it — including TODO_QUERY_PATTERNS' one
documented ``known_reabsorptions`` exception ("what should I do next"
reclaimed by PRIORITY_PATTERNS, a pre-existing shadowed duplicate literal
that AGREES with the ruled destination), CALENDAR_QUERY_PATTERNS' 19
documented ``known_reabsorptions`` exceptions (TEMPORAL_PATTERNS reclaimed
these as ``get_current_time`` before TEMPORAL_PATTERNS was itself deleted —
reported with ``"agrees": false``, never silenced, and now also marked
``resolved_by`` since the reclaiming list is gone and the phrases are
genuinely unclaimed again), TEMPORAL_PATTERNS' own entry, whose 69 claimed
rows include the same 19 ex-CALENDAR phrases (reabsorbed, all disagreeing)
plus 5 rows passing via a THIRD documented shape, ``misserved_at_deletion``
(the deleted pattern's own claim disagreed with the ruled destination AND
the router independently declined — deletion licensed because removing a
deterministically-wrong fallback cannot regress a row that was already
unserved correctly; see ``check_deleted_entry_non_regression``'s docstring),
and GITHUB_QUERY_PATTERNS' own entry (66 claimed rows, all its own — no
sibling reabsorption existed at deletion time, unlike CALENDAR/TEMPORAL),
whose ONE post-deletion ``known_reabsorptions`` entry ("any update on the
next milestone" reclaimed by STATUS_PATTERNS's pre-existing ``\bnext
milestone\b`` literal) is the SAME agreeing-reclaim shape TODO_QUERY_PATTERNS
first exercised, not a new mechanism. CALENDAR's and TEMPORAL's entries are
the first two to require the live-flag ``cats`` parameter (their
MISMATCH-but-live-route rows need ``read_temporal`` in the live set); the
other four (including GITHUB_QUERY_PATTERNS) never strictly needed it but
are still checked with ``_LIVE_CATS`` for consistency with production's
actual live flag.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import inversion_phase0_baseline as p0  # noqa: E402
import inversion_phase3_deletion_gate as gate  # noqa: E402
import pattern_literal_counts  # noqa: E402

from services.intent_service.pre_classifier import PreClassifier  # noqa: E402

# ── (a) the census runs over the REAL corpus and REAL pre-classifier, and
#        its denominators add up ────────────────────────────────────────────


class TestCensusDenominators:
    def test_claimed_plus_unclaimed_equals_corpus_size(self):
        records, by_list = gate.build_census(cats=None)
        corpus_size = len(p0.load_corpus())
        assert len(records) == corpus_size, "one record per corpus row"

        claimed = sum(1 for r in records if r.claim.pattern_list is not None)
        unclaimed = sum(1 for r in records if r.claim.pattern_list is None)
        assert claimed + unclaimed == len(records)
        assert claimed + unclaimed == 382, (
            "the corpus was 382 rows as of the 2026-10-01 STATUS_PATTERNS "
            "phase3-conversion deposit (#1595 epic-0 unit 5: 336 + 46 new claimed "
            "rows = 382, unclaimed unchanged at 150); if this drifts, the corpus "
            "grew/shrank — update the pinned number in the same commit as the "
            "corpus change, don't just widen this test"
        )

    def test_every_claimed_row_has_a_pattern_list_with_a_literal_count(self):
        """A row claimed by a list that per_list_literal_counts() cannot see
        (a synthetic/non-class-attribute name, e.g. MILESTONE_STATUS_INLINE_
        PATTERNS) is allowed — the gate defaults its literal count to 0 —
        but every OTHER claimed row's list must resolve to a real, counted
        `*PATTERNS` class attribute. This is the vacuity guard the census
        table's per-list literal column depends on."""
        records, by_list = gate.build_census(cats=None)
        literal_counts = pattern_literal_counts.per_list_literal_counts()
        claimed_lists = {r.claim.pattern_list for r in records if r.claim.pattern_list}
        unresolvable = claimed_lists - set(literal_counts) - {"MILESTONE_STATUS_INLINE_PATTERNS"}
        assert not unresolvable, (
            f"claimed pattern-list name(s) with no literal count and no known "
            f"synthetic-name exemption: {unresolvable} — either "
            f"per_list_literal_counts() needs to see this list, or "
            f"pre_classify_with_pattern_list's synthetic-name docstring "
            f"needs updating (and this test's exemption set with it)"
        )

    def test_every_list_in_by_list_carries_its_real_literal_count(self):
        """by_list's literal_count for every REAL (non-synthetic) list must
        equal the extraction ratchet's own count for that list — the same
        number TestExtractionPatternRatchet sums to 567. A mismatch here
        would mean the deletion gate's 'ceiling 567 -> 567-N' arithmetic is
        wrong."""
        _records, by_list = gate.build_census(cats=None)
        literal_counts = pattern_literal_counts.per_list_literal_counts()
        for name, count in literal_counts.items():
            if name in by_list:
                assert by_list[name].literal_count == count, name


# ── (b) DELETED_PATTERN_LISTS — empty today; the non-regression MECHANISM
#        is proven with a synthetic entry, never the real ledger ───────────


class TestDeletedPatternListsLedger:
    # The exact --live categories every Phase-3 deletion gate run has used
    # throughout this epic (2026-10-01: promoted to a shared constant,
    # gate.CURRENT_LIVE_CATEGORIES, when TestChatPointersReachabilityRatchet
    # needed the identical set — see that constant's own docstring). Threaded
    # into check_deleted_entry_non_regression for every entry below —
    # harmless for REMINDER_PATTERNS/REMINDER_QUERY_PATTERNS/
    # TODO_QUERY_PATTERNS (none of their rows ever need a live condition to
    # pass) and REQUIRED for CALENDAR_QUERY_PATTERNS' and TEMPORAL_PATTERNS'
    # MISMATCH-but-live-route rows.
    _LIVE_CATS = gate.CURRENT_LIVE_CATEGORIES

    def test_real_ledger_has_the_first_six_deletions(self):
        """2026-09-27, #1595 Phase 3: REMINDER_PATTERNS (5 literals) and
        REMINDER_QUERY_PATTERNS (4 literals) were emptied first, then
        TODO_QUERY_PATTERNS (10 literals) on 2026-09-28, then
        CALENDAR_QUERY_PATTERNS (52 literals) and TEMPORAL_PATTERNS (56
        literals) on 2026-10-01, then GITHUB_QUERY_PATTERNS (64 literals) on
        2026-10-02 — all emptied to `[]` in
        services/intent_service/pre_classifier.py (kept as tombstones — the
        class attributes and their consumer code paths survive; only the
        literals were deleted). This assertion is pinned to the CURRENT
        ledger contents, per this test's own prior docstring ("this
        assertion needs updating in the SAME commit as the deletion") — a
        future deletion updates it again, in that commit."""
        entries = gate.load_deleted_pattern_lists()
        names = {e["list"] for e in entries}
        assert names == {
            "REMINDER_PATTERNS",
            "REMINDER_QUERY_PATTERNS",
            "TODO_QUERY_PATTERNS",
            "CALENDAR_QUERY_PATTERNS",
            "TEMPORAL_PATTERNS",
            "GITHUB_QUERY_PATTERNS",
        }, (
            f"DELETED_PATTERN_LISTS contents changed — update this pin in the "
            f"same commit as the ledger change. Got: {sorted(names)}"
        )

    def test_real_ledger_entries_pass_non_regression(self):
        """Every entry in the real (now non-empty) ledger passes
        non-regression: neither deleted list's claimed phrases is
        re-claimed by an UNDOCUMENTED surviving surface-1 list, and each is
        still a corpus row scoring MATCH, an agreeing REVIEW, or a
        live-MISMATCH (the router's own route is itself a live op) under
        the SAME --live categories the CALENDAR_QUERY_PATTERNS gate run
        used. This is the real deletion evidence, not the synthetic proof
        (TestNonRegressionMechanism, below) that the mechanism works."""
        entries = gate.load_deleted_pattern_lists()
        assert entries, "expected the six real entries — ledger is empty"
        for entry in entries:
            ok, problems = gate.check_deleted_entry_non_regression(entry, cats=self._LIVE_CATS)
            assert ok, f"{entry.get('list')}: {problems}"

    def test_calendar_entry_fails_non_regression_without_the_live_flag(self):
        """The CALENDAR_QUERY_PATTERNS entry's 3 MISMATCH-but-live-route rows
        (1 unclaimed, 2 reclaimed-but-independently-reproved) genuinely
        NEED read_temporal in the live set — this is not a decorative
        parameter. Proven here so a future refactor that silently drops the
        cats threading is caught: the SAME entry that passes with
        ``_LIVE_CATS`` must fail without it."""
        entries = {e["list"]: e for e in gate.load_deleted_pattern_lists()}
        entry = entries["CALENDAR_QUERY_PATTERNS"]
        ok, problems = gate.check_deleted_entry_non_regression(entry)  # cats=None
        assert not ok
        # Was 3 when written; the mis-serve rule (same morning) resolves the
        # row whose reclaiming TEMPORAL claim disagrees with the ruling
        # without needing the live set. The property pinned is "needs the
        # flag", not the count.
        assert 1 <= len(problems) <= 3, problems
        assert all("live-set-unknown" in p for p in problems), problems

    def test_calendar_entry_known_reabsorptions_are_all_documented_disagreements(self):
        """#1595 Phase 3 third deletion's defining finding: TEMPORAL_PATTERNS
        reabsorbs 19 of CALENDAR_QUERY_PATTERNS' 49 claimed phrases as
        ``get_current_time`` — NONE of them agree with the ruled
        destination. Pinned so a future router/prompt change that makes one
        of these agree (or disagree differently) is visible, not silently
        absorbed into a passing suite."""
        entries = {e["list"]: e for e in gate.load_deleted_pattern_lists()}
        entry = entries["CALENDAR_QUERY_PATTERNS"]
        reabsorptions = entry["known_reabsorptions"]
        assert len(reabsorptions) == 19, sorted(reabsorptions)
        for phrase, info in reabsorptions.items():
            assert info["reclaimed_by"] == "TEMPORAL_PATTERNS", phrase
            assert info["claimed_action"] == "get_current_time", phrase
            assert info["agrees"] is False, phrase


class TestNonRegressionMechanism:
    """Proves check_deleted_entry_non_regression's TWO failure modes fire —
    against SYNTHETIC entries only. Never touches the real (empty) ledger."""

    def test_passes_for_a_phrase_still_matching_and_unclaimed(self):
        # "who am I?" is a real corpus row (IDENTITY, action:get_identity)
        # that scores MATCH in the 09-25 full report — and, measured
        # directly, is NOT claimed by IDENTITY_PATTERNS or any other
        # surface-1 list today (only its sibling "who are you?" is; a real
        # finding of the census, not a fixture artifact). It is therefore a
        # genuinely clean stand-in for "the deleted list's phrase is
        # unclaimed post-deletion and still scores MATCH".
        assert (
            gate.claim_for_phrase(PreClassifier, "who am I?").pattern_list is None
        ), "test fixture assumption broke — pick another unclaimed MATCH row"
        entry = {
            "list": "SYNTHETIC_NEVER_CLAIMED_LIST",
            "rows_claimed_at_deletion": ["who am I?"],
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert ok, problems

    def test_fails_when_phrase_is_claimed_by_a_surviving_list(self):
        # PRIORITY_PATTERNS genuinely claims "what should I do next" today
        # (verified by the census — unaffected by any of the five
        # deletions). Naming that SAME list as the "deleted" one in a
        # synthetic entry must fail loud — the list obviously was not
        # deleted (it still claims), so a real deletion commit that forgot
        # to actually remove the list would be caught here. (Was
        # TEMPORAL_PATTERNS/"when is my next meeting?" before #1595 Phase 3's
        # fourth deletion emptied TEMPORAL_PATTERNS itself, which broke this
        # fixture's own premise.)
        entry = {
            "list": "PRIORITY_PATTERNS",
            "rows_claimed_at_deletion": ["what should I do next"],
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert not ok
        assert any("claimed again by PRIORITY_PATTERNS" in p for p in problems)

    def test_fails_for_a_phrase_that_is_no_longer_a_corpus_row(self):
        entry = {
            "list": "SYNTHETIC_NEVER_CLAIMED_LIST",
            "rows_claimed_at_deletion": ["this phrase does not exist in the corpus, at all, ever"],
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert not ok
        assert any("no longer a corpus row" in p for p in problems)

    def test_fails_for_a_phrase_whose_router_verdict_is_not_match_or_agreeing_review(self):
        # "analyze the file I uploaded" is a real corpus row (QUERY,
        # action:analyze_data), unclaimed by any surface-1 list today, whose
        # router verdict in the 09-25 full report is MISMATCH
        # (analyze_document vs expected analyze_data). A synthetic entry
        # citing it as safely-deleted evidence must fail non-regression.
        assert (
            gate.claim_for_phrase(PreClassifier, "analyze the file I uploaded").pattern_list is None
        ), "test fixture assumption broke — pick another unclaimed MISMATCH row"
        entry = {
            "list": "SYNTHETIC_NEVER_CLAIMED_LIST",
            "rows_claimed_at_deletion": ["analyze the file I uploaded"],
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert not ok
        assert any("no longer MATCH or an agreeing REVIEW" in p for p in problems)

    def test_passes_for_an_unclaimed_floor_expected_phrase_that_matches(self):
        # #1595 Phase 3 third deletion (CALENDAR_QUERY_PATTERNS): a `floor`
        # corpus expectation scores MATCH when the router declines
        # (outcome in none/clarify) — scripts/inversion_phase1_shadow_score
        # .py's router_matches encodes this at SCORE time, so by the time
        # this phrase reaches check_deleted_entry_non_regression it is
        # already a MATCH row like any other; the unclaimed path's unified
        # row_disposition reuse passes it with ZERO need for cats or
        # expected_op_by_phrase (MATCH never consults either). "time spent
        # in meetings is high lately" is a real corpus row (CALENDAR,
        # expected: floor) confirmed unclaimed by any surviving surface-1
        # list post-CALENDAR_QUERY_PATTERNS-deletion.
        assert (
            gate.claim_for_phrase(
                PreClassifier, "time spent in meetings is high lately"
            ).pattern_list
            is None
        ), "test fixture assumption broke — pick another unclaimed floor row"
        entry = {
            "list": "SYNTHETIC_FLOOR_LIST",
            "rows_claimed_at_deletion": ["time spent in meetings is high lately"],
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)  # no cats needed
        assert ok, problems

    def test_passes_for_a_floor_expected_phrase_reclaimed_but_documented_disagreeing(self):
        # The companion shape: a floor row a SURVIVING list now claims
        # (disagreeing — any real action disagrees with "floor" by
        # construction, p0.same_operation(action, "floor") is always
        # False). Documented via known_reabsorptions with explicit
        # "agrees": false, it must still pass IF the row's own frozen
        # router verdict is independently MATCH — exactly PRIORITY_
        # PATTERNS' "list priorities for the team" shape (a PRIORITY-
        # category floor row PRIORITY_PATTERNS claims as get_top_priority;
        # the row itself scores MATCH, so no cats are even needed here).
        # (Was CALENDAR_QUERY_PATTERNS' "check my calendar for conflicts"
        # shape, reclaimed by TEMPORAL_PATTERNS, before #1595 Phase 3's
        # fourth deletion emptied TEMPORAL_PATTERNS itself and left that
        # phrase genuinely unclaimed, breaking this fixture's own premise.)
        phrase = "list priorities for the team"
        claim = gate.claim_for_phrase(PreClassifier, phrase)
        assert claim.pattern_list is not None, "test fixture assumption broke"
        entry = {
            "list": "SYNTHETIC_FLOOR_RECLAIMED_LIST",
            "rows_claimed_at_deletion": [phrase],
            "expected_op_by_phrase": {phrase: "floor"},
            "known_reabsorptions": {
                phrase: {
                    "reclaimed_by": claim.pattern_list,
                    "claimed_action": claim.action,
                    "agrees": False,
                }
            },
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert ok, problems

    def test_fails_for_an_undocumented_reclaim_even_when_independently_safe(self):
        # The SAME floor row as above, WITHOUT a known_reabsorptions entry.
        # The reclaim is a SURPRISE the ledger author never named — must
        # fail loud regardless of whether the underlying router evidence
        # happens to be fine (that is the whole point of requiring
        # documentation: catching the unexpected reclaim itself, not just
        # its eventual safety).
        phrase = "list priorities for the team"
        entry = {
            "list": "SYNTHETIC_UNDOCUMENTED_RECLAIM_LIST",
            "rows_claimed_at_deletion": [phrase],
            "expected_op_by_phrase": {phrase: "floor"},
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert not ok
        assert any("reabsorbed by a surviving pattern" in p for p in problems)

    def test_documented_disagreeing_reclaim_needs_the_live_flag_when_the_row_is_mismatch(self):
        # A MISMATCH-but-live-route row (not a plain MATCH like the floor
        # cases above) genuinely needs cats to pass even when documented —
        # STATUS_PATTERNS' "give me a project status report" shape (a
        # synthetic-expectation corpus row, action:update_issue, that
        # STATUS_PATTERNS claims as get_project_status; the router's own
        # route, generate_report@0.92, is live only via the read_referent
        # group). (Was CALENDAR_QUERY_PATTERNS' "what is on my calendar"
        # shape, reclaimed by TEMPORAL_PATTERNS, before #1595 Phase 3's
        # fourth deletion emptied TEMPORAL_PATTERNS itself and left that
        # phrase genuinely unclaimed, breaking this fixture's own premise.)
        phrase = "give me a project status report"
        claim = gate.claim_for_phrase(PreClassifier, phrase)
        assert claim.pattern_list == "STATUS_PATTERNS", "test fixture assumption broke"
        entry = {
            "list": "SYNTHETIC_MISMATCH_RECLAIM_LIST",
            "rows_claimed_at_deletion": [phrase],
            "expected_op_by_phrase": {phrase: "update_issue"},
            "known_reabsorptions": {
                phrase: {
                    "reclaimed_by": "STATUS_PATTERNS",
                    "claimed_action": "get_project_status",
                    "agrees": False,
                }
            },
        }
        # 2026-10-01 (evening): the router's answer for this row moved on a
        # re-score (generate_report@0.92 → get_project_status@0.95, Haiku
        # variance) and the premise broke a third time. The premise is about
        # the MECHANISM, not this phrase's live verdict — so the router
        # verdict is now a stub: MISMATCH, route generate_report@0.92 (live
        # only via read_referent). The claim side stays real (STATUS_PATTERNS
        # really does claim the phrase as get_project_status).

        class _StubReports:
            def lookup(self, phrase_, category_):
                return gate.RouterLookup(
                    route="generate_report", conf=0.92, verdict="MISMATCH", source_table="stub"
                )

        ok_without, problems_without = gate.check_deleted_entry_non_regression(
            entry, reports=_StubReports()
        )
        assert not ok_without, problems_without

        ok_with, problems_with = gate.check_deleted_entry_non_regression(
            entry, cats=frozenset({"READ_REFERENT"}), reports=_StubReports()
        )
        assert ok_with, problems_with


# ── (c) PRIORITY_PATTERNS against the frozen reports — print it, don't pin
#        GO/NO-GO as a fact of the world ────────────────────────────────────


class TestPriorityPatternsVerdictIsReported:
    """Exercises the SAME verdict-reporting mechanism the four deletion
    sessions each ran by hand before their own list's deletion — originally
    pinned against TEMPORAL_PATTERNS as a stable, many-rows example. #1595
    Phase 3's fourth deletion emptied TEMPORAL_PATTERNS itself (it now
    claims ZERO corpus rows — "NO ROWS" in the `--all` census, not GO/NO-GO),
    which broke this class's own fixture premise. Swapped to
    PRIORITY_PATTERNS (still live, 42 claimed rows as of 2026-10-01) rather
    than deleted — same idiom as every other pin swap in this deletion
    series."""

    def test_returns_a_verdict_with_named_rows(self, capsys):
        """Runs the real census (real corpus, real pre-classifier, the real
        frozen router reports — no LLM call anywhere) and asserts only that
        PRIORITY_PATTERNS gets a verdict backed by named rows. Whether that
        verdict is GO or NO-GO is data, printed for the test log, never
        asserted as a fixed fact — the router reports (and therefore the
        verdict) can change out from under this test on a future re-score,
        and pinning GO/NO-GO here would silently start lying the day that
        happens."""
        _records, by_list = gate.build_census(cats=None)
        lv = by_list.get("PRIORITY_PATTERNS")
        assert lv is not None, "PRIORITY_PATTERNS must appear in the census"
        assert len(lv.rows) > 0, "PRIORITY_PATTERNS must claim at least one corpus row"

        verdict = "GO" if lv.deletable else "NO-GO"
        print(f"\nPRIORITY_PATTERNS verdict (frozen reports): {verdict}")
        print(f"literals: {lv.literal_count}  rows claimed: {len(lv.rows)}")
        for rec in lv.rows:
            mark = "OK" if rec.row_ok else "FAIL"
            print(f"  [{mark}] {rec.phrase!r} -> {rec.reason}")

        # The only pinned facts: every claimed row is NAMED (phrase is
        # non-empty) and carries a reason string (never silently blank) —
        # the verdict itself is read, not asserted.
        for rec in lv.rows:
            assert rec.phrase, "every row backing the verdict must be named"
            assert rec.reason, f"{rec.phrase!r} has no reason recorded"
        assert verdict in ("GO", "NO-GO")

    def test_temporal_patterns_now_claims_zero_rows(self):
        """#1595 Phase 3 fourth deletion: TEMPORAL_PATTERNS is tombstoned —
        pins the post-deletion state directly rather than leaving it as an
        implicit consequence of the ledger entry alone."""
        _records, by_list = gate.build_census(cats=None)
        lv = by_list.get("TEMPORAL_PATTERNS")
        assert (
            lv is not None
        ), "TEMPORAL_PATTERNS must still appear in the census (0 rows, not absent)"
        assert len(lv.rows) == 0
        assert lv.deletable is False, "an empty list reports NO ROWS, not GO"


# ── router-report parsers (route column, REVIEW table) ─────────────────────


class TestReportParsers:
    def test_parse_asserted_rows_retains_route(self):
        rows = gate.parse_asserted_rows(gate.FULL_REPORT)
        assert rows, "must parse at least one asserted row"
        sample = next(r for r in rows if r["phrase"] == "who am I?")
        assert sample["route"] == "get_identity"
        assert sample["conf"] == 1.0
        assert sample["verdict"] == "MATCH"

    def test_parse_review_rows(self):
        rows = gate.parse_review_rows(gate.FULL_REPORT)
        assert rows, "must parse at least one REVIEW row"
        sample = next(r for r in rows if r["phrase"] == "what reminders do I have?")
        assert sample["route"] == "list_reminders_query"
        assert sample["conf"] == 1.0

    def test_temporal_rescore_overrides_full_report_for_temporal_category(self):
        """The documented precedence: 'what's on my calendar today?' is
        MISMATCH in the full 09-25 report (week_calendar vs expected
        meeting_time) but MATCH in the same-day temporal re-score (after the
        registry-description sharpening). The gate's lookup must return the
        re-score's MATCH for this TEMPORAL-category row."""
        reports = gate.RouterReports(gate.FULL_REPORT, gate.TEMPORAL_RESCORE_REPORT)
        full_hit = reports._find(
            gate.p1._norm_phrase("what's on my calendar today?"), reports._full_asserted_by_norm
        )
        assert full_hit is not None and full_hit["verdict"] == "MISMATCH"

        lookup = reports.lookup("what's on my calendar today?", "TEMPORAL")
        assert lookup.verdict == "MATCH", "temporal re-score must override the full run"
        assert lookup.source_table == "temporal-rescore-asserted"

    def test_non_temporal_category_never_consults_temporal_rescore(self):
        reports = gate.RouterReports(gate.FULL_REPORT, gate.TEMPORAL_RESCORE_REPORT)
        lookup = reports.lookup("who am I?", "IDENTITY")
        assert lookup.source_table == "full-asserted"


# ── live-set resolution (condition (c)) ─────────────────────────────────────


class TestLiveSetResolution:
    def test_unknown_when_unset_and_no_override(self, monkeypatch):
        monkeypatch.delenv("PIPER_INVERSION_LIVE_CATEGORIES", raising=False)
        cats, source = gate.live_set(explicit=None)
        assert cats is None
        assert source == "unknown"

    def test_explicit_override_wins(self, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status")
        cats, source = gate.live_set(explicit="create_todo,create_reminder")
        assert cats == {"CREATE_TODO", "CREATE_REMINDER"}
        assert source == "--live"

    def test_condition_c_false_when_live_set_unknown(self):
        ok, reason = gate.expected_action_is_live("action:create_todo", cats=None)
        assert ok is False
        assert reason == "live-set-unknown"

    def test_condition_c_false_for_non_action_expected(self):
        ok, reason = gate.expected_action_is_live("category:STATUS", cats=frozenset({"QUERY"}))
        assert ok is False
        assert reason == "expected-not-action-shaped"

    def test_condition_c_true_when_action_is_live_by_operation_name(self):
        ok, reason = gate.expected_action_is_live(
            "action:create_todo", cats=frozenset({"CREATE_TODO"})
        )
        assert ok is True
        assert "live via" in reason


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))


class TestLiveMeansDispatchable:
    """Arch's 2026-10-01 ruling: the gate's "live" must mean what production
    means — a rail key (WorkflowEntry) that passes the #1677 effect guard AND
    matches the flag. A name that only matches the flag (op / group /
    category) but has no WorkflowEntry can never be served by the live
    consult, so the gate must read NOT-live for it even when the operator
    passes its own name as a token. Latent false GO before this pin."""

    def test_floor_routed_canonical_is_not_live_even_when_named_in_the_flag(self):
        # #1595 Phase 3 (2026-10-01): get_current_time now HAS a rail entry
        # (Arch's ruling, workflow_entries.py get_current_time_entry,
        # flip_group read_temporal) — swapped to explain_suggestion
        # (PROVENANCE, CANONICAL disposition, no WorkflowEntry) per this
        # test's own original instruction: the property pinned is "a
        # floor-routed canonical with no rail entry is not live", not this
        # specific example. explain_suggestion verified still rail-free
        # 2026-10-01 (same session that added get_current_time's entry).
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        assert get_action_workflows().get("explain_suggestion") is None, (
            "explain_suggestion now has a rail entry — pick another floor-routed canonical "
            "for this pin rather than deleting it"
        )
        ok, reason = gate.expected_action_is_live(
            "action:explain_suggestion",
            frozenset({"EXPLAIN_SUGGESTION", "PROVENANCE", "READ_TEMPORAL"}),
        )
        assert ok is False
        assert "no WorkflowEntry" in reason

    def test_rail_key_in_a_live_group_is_live(self):
        ok, reason = gate.expected_action_is_live(
            "action:meeting_time", frozenset({"READ_TEMPORAL"})
        )
        assert ok is True, reason
        assert reason.startswith("live via")


class TestMismatchRowRuleMeasuresTheRouterNotTheDestination:
    """2026-10-01: a MISMATCH row is safe to delete only when the ROUTER's own
    answer is a live operation (the consult already owns the phrase). When the
    router declined (NONE/CLARIFY/REFUSED) the consult stands down and the
    pattern IS the live path, so deletion changes behaviour. The old rule
    checked whether the EXPECTED action was live — the wrong object. Pinned
    on synthetic rows through the factored row_disposition(), so the pin does
    not depend on the census happening to contain a broken row."""

    LIVE = frozenset({"READ_TEMPORAL", "READ_STATUS"})
    CLAIM = gate.ClaimResult(
        pattern_list="CALENDAR_QUERY_PATTERNS",
        action="week_calendar",
        category="QUERY",
        entry_surface="pre_classify",
    )

    def _router(self, route, verdict):
        return gate.RouterLookup(route=route, conf=0.85, verdict=verdict, source_table="synthetic")

    def test_router_declined_mismatch_is_not_ok_even_when_the_expected_action_is_live(self):
        for route in ("NONE", "CLARIFY", "REFUSED"):
            ok, reason = gate.row_disposition(
                self.CLAIM, self._router(route, "MISMATCH"), "action:week_calendar", self.LIVE
            )
            assert ok is False, (route, reason)
            assert "the pattern is the live path" in reason

    def test_router_answered_with_a_live_op_mismatch_is_ok(self):
        ok, reason = gate.row_disposition(
            self.CLAIM, self._router("meeting_time", "MISMATCH"), "action:week_calendar", self.LIVE
        )
        assert ok is True, reason
        assert "the consult owns this phrase" in reason

    def test_router_answered_with_a_live_op_below_dispatch_threshold_is_not_ok(self):
        # 2026-10-01: STATUS score — "show today's assignments" → meeting_time
        # @0.6. meeting_time is live, but production dispatches only at
        # >= live_min_confidence() (0.8); below it the consult stands down and
        # the pattern is still the live path.
        low = gate.RouterLookup(
            route="meeting_time", conf=0.6, verdict="MISMATCH", source_table="synthetic"
        )
        ok, reason = gate.row_disposition(self.CLAIM, low, "action:week_calendar", self.LIVE)
        assert ok is False, reason
        assert "dispatch threshold" in reason
        # And with no confidence recorded at all, the same stand-down applies.
        none_conf = gate.RouterLookup(
            route="meeting_time", conf=None, verdict="MISMATCH", source_table="synthetic"
        )
        ok, reason = gate.row_disposition(self.CLAIM, none_conf, "action:week_calendar", self.LIVE)
        assert ok is False, reason

    def test_router_answered_with_a_not_live_op_mismatch_is_not_ok(self):
        # get_top_priority has no live group in this flag set.
        ok, reason = gate.row_disposition(
            self.CLAIM,
            self._router("get_top_priority", "MISMATCH"),
            "action:week_calendar",
            self.LIVE,
        )
        assert ok is False, reason

    def test_unscored_rows_are_never_ok(self):
        ok, reason = gate.row_disposition(
            self.CLAIM, self._router(None, "UNSCORED"), "action:week_calendar", self.LIVE
        )
        assert ok is False
        assert "UNSCORED" in reason

    def test_match_is_ok(self):
        ok, _ = gate.row_disposition(
            self.CLAIM, self._router("week_calendar", "MATCH"), "action:week_calendar", self.LIVE
        )
        assert ok is True

    def test_router_declined_but_pattern_misserves_the_row_is_ok(self):
        # The pattern claims get_current_time for a row ruled week_calendar:
        # the regex is the live fallback AND it is wrong; deletion cannot
        # make the fallback worse. OK, with the reason naming the mis-serve.
        claim = gate.ClaimResult(
            pattern_list="TEMPORAL_PATTERNS",
            action="get_current_time",
            category="TEMPORAL",
            entry_surface="pre_classify",
        )
        ok, reason = gate.row_disposition(
            claim, self._router("CLARIFY", "MISMATCH"), "action:week_calendar", self.LIVE
        )
        assert ok is True, reason
        assert "mis-serves this row" in reason

    def test_router_declined_and_pattern_serves_the_row_right_is_still_not_ok(self):
        # Same decline, but the claim AGREES with the ruling: the pattern is
        # the live path and correct — keep it.
        ok, reason = gate.row_disposition(
            self.CLAIM, self._router("CLARIFY", "MISMATCH"), "action:week_calendar", self.LIVE
        )
        assert ok is False, reason
