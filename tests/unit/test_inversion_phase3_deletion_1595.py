"""#1595 Phase 3 — pinning tests for the deletion-ratchet INSTRUMENT
(scripts/inversion_phase3_deletion_gate.py).

Epic-0's own conditions on the endpoint (dev/2026/09/25/inversion-epic0-
remaining-scope-2026-09-25.md, unit 5; issue #1595 body): "Deletion ratchet
asserts corpus non-regression ALONGSIDE shrink" and "pattern-to-corpus-case
conversion is a STEP IN the deletion procedure, not an intention." This
suite pins the census mechanics (real corpus, real pre-classifier, real
router reports, NO LLM calls anywhere here) and the non-regression checker
that a future deletion commit's ratchet test will lean on.

Nothing is deleted by this suite. ``DELETED_PATTERN_LISTS`` is empty today —
tests (b)/(c) below prove the non-regression MECHANISM works (via a
synthetic entry, never the real ledger) and that the real, empty ledger is
vacuously clean, not that any list has actually been removed.
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
        assert claimed + unclaimed == 116, (
            "the corpus was 116 rows as of the 2026-09-25 09:0x deposit "
            "(intent-routing-stack.md Pre-claim shadow probe entry); if this "
            "drifts, the corpus grew/shrank — update the pinned number in "
            "the same commit as the corpus change, don't just widen this test"
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
    def test_real_ledger_is_empty_today(self):
        """No `*_PATTERNS` list has actually been deleted yet (2026-09-27) —
        this Phase-3 unit built the INSTRUMENT, not a deletion. Vacuously
        clean is the honest state of an empty ledger, not evidence the
        mechanism works; TestNonRegressionMechanism proves the mechanism."""
        entries = gate.load_deleted_pattern_lists()
        assert entries == [], (
            "DELETED_PATTERN_LISTS is non-empty — a list was deleted since "
            "this test was written; that's fine, but this assertion needs "
            "updating in the SAME commit as the deletion (it exists to make "
            "an undocumented deletion loud, not to forbid deletion)"
        )

    def test_empty_ledger_is_vacuously_non_regressing(self):
        """Every entry in the (currently empty) real ledger passes
        non-regression — with zero entries this is a vacuous pass, which is
        the correct state, not a placebo: the loop below is REAL code that
        will fail the moment a real entry is appended without also holding."""
        entries = gate.load_deleted_pattern_lists()
        for entry in entries:
            ok, problems = gate.check_deleted_entry_non_regression(entry)
            assert ok, f"{entry.get('list')}: {problems}"


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
        # TEMPORAL_PATTERNS genuinely claims "when is my next meeting?"
        # today (verified by the census). Naming that SAME list as the
        # "deleted" one in a synthetic entry must fail loud — the list
        # obviously was not deleted (it still claims), so a real deletion
        # commit that forgot to actually remove the list would be caught
        # here.
        entry = {
            "list": "TEMPORAL_PATTERNS",
            "rows_claimed_at_deletion": ["when is my next meeting?"],
        }
        ok, problems = gate.check_deleted_entry_non_regression(entry)
        assert not ok
        assert any("claimed again by TEMPORAL_PATTERNS" in p for p in problems)

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


# ── (c) TEMPORAL_PATTERNS against the 09-25 re-score — print it, don't pin
#        GO/NO-GO as a fact of the world ────────────────────────────────────


class TestTemporalPatternsVerdictIsReported:
    def test_returns_a_verdict_with_named_rows(self, capsys):
        """Runs the real census (real corpus, real pre-classifier, the real
        09-25 report + temporal-rescore report — no LLM call anywhere) and
        asserts only that TEMPORAL_PATTERNS gets a verdict backed by named
        rows. Whether that verdict is GO or NO-GO is data, printed for the
        test log, never asserted as a fixed fact — the router reports (and
        therefore the verdict) can change out from under this test on a
        future re-score, and pinning GO/NO-GO here would silently start
        lying the day that happens."""
        _records, by_list = gate.build_census(cats=None)
        lv = by_list.get("TEMPORAL_PATTERNS")
        assert lv is not None, "TEMPORAL_PATTERNS must appear in the census"
        assert len(lv.rows) > 0, "TEMPORAL_PATTERNS must claim at least one corpus row"

        verdict = "GO" if lv.deletable else "NO-GO"
        print(f"\nTEMPORAL_PATTERNS verdict (2026-09-25 report + temporal-rescore): {verdict}")
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
