"""#1595 Phase 1 shadow-score m-44 fix — unit tests for the shared-subset
scorer (Task A: the report's `Δ`/`gate` column previously compared the
router's match count on the CURRENT corpus against the baseline's count on
a DIFFERENT, smaller corpus — two denominators. ``compute_shared_subset``
scores only rows asserted in BOTH sources, matched by phrase.)

No LLM calls anywhere here: this file exercises the pure parsing/matching/
scoring functions against synthetic baseline rows and synthetic scored
``row_results`` — the same shape ``score()`` produces, built by hand.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import inversion_phase1_shadow_score as p1  # noqa: E402


def _rr(phrase: str, category: str, verdict: str) -> dict:
    """Build a synthetic row_results entry (the shape score() produces)."""
    return {"row": {"phrase": phrase, "category": category}, "verdict": verdict}


def _br(phrase: str, category: str, verdict: str) -> dict:
    """Build a synthetic baseline row (the shape parse_baseline_row_detail
    produces)."""
    return {"phrase": phrase, "category": category, "expected": "x", "verdict": verdict}


class TestNormPhrase:
    def test_strips_collapses_casefolds(self):
        assert p1._norm_phrase("  Remind   Me\n") == "remind me"

    def test_case_insensitive_equal(self):
        assert p1._norm_phrase("What's My Week Look Like?") == p1._norm_phrase(
            "what's my week look like?"
        )


class TestPrefixCandidates:
    def test_finds_unambiguous_prefix(self):
        haystack = {"remind me at 9:41 today to check in with the lead devel": object()}
        candidates = p1._prefix_candidates(
            "remind me at 9:41 today to check in with the lead developer",
            haystack.keys(),
        )
        assert candidates == list(haystack.keys())

    def test_rejects_short_prefix_below_threshold(self):
        # both under _MIN_PREFIX_LEN (20) — must not match by accident
        haystack = {"hi there": object()}
        assert p1._prefix_candidates("hi", haystack.keys()) == []

    def test_ambiguous_multi_candidate_is_not_returned_as_single(self):
        haystack = {
            "archive my project called test please and thanks": object(),
            "archive my project called test right now instead": object(),
        }
        candidates = p1._prefix_candidates("archive my project called test", haystack.keys())
        assert len(candidates) == 2  # caller treats >1 as unmatched


class TestComputeSharedSubset:
    def test_shared_only_counts_rows_asserted_on_both_sides(self):
        row_results = [
            _rr("when is my next meeting?", "TEMPORAL", "MATCH"),
            _rr("what time is it?", "TEMPORAL", "MATCH"),
            _rr("hello", "CONVERSATION", "REVIEW"),  # not asserted — excluded
        ]
        baseline_rows = [
            _br("when is my next meeting?", "TEMPORAL", "MATCH"),
            _br("what time is it?", "TEMPORAL", "MATCH"),
            _br("hello", "CONVERSATION", "REVIEW"),  # not asserted — excluded
        ]
        shared = p1.compute_shared_subset(row_results, baseline_rows)
        assert shared["per_cat"]["TEMPORAL"] == {
            "shared": 2,
            "router_match": 2,
            "baseline_match": 2,
        }
        assert shared["dropped"] == {}
        assert shared["added"] == {}
        assert shared["regressed"] == {}

    def test_temporal_reproduces_leads_read(self):
        """Pins the exact 2026-09-25 finding: shared 4, router 3/4,
        baseline 4/4, REGRESSION, naming 'what's on my calendar today?' —
        Lead's read at the bottom of
        inversion-phase1-shadow-score-2026-09-25.md is the spec for this
        test."""
        row_results = [
            _rr("what's on my calendar today?", "TEMPORAL", "MISMATCH"),  # -> week_calendar
            _rr("when is my next meeting?", "TEMPORAL", "MATCH"),
            _rr("what time is it?", "TEMPORAL", "MATCH"),
            _rr(
                "remind me at 9:41 today to check in with the lead developer",
                "TEMPORAL",
                "MATCH",
            ),
        ]
        baseline_rows = [
            _br("what's on my calendar today?", "TEMPORAL", "MATCH"),
            _br("when is my next meeting?", "TEMPORAL", "MATCH"),
            _br("what time is it?", "TEMPORAL", "MATCH"),
            _br(
                "remind me at 9:41 today to check in with the lead developer",
                "TEMPORAL",
                "MATCH",
            ),
        ]
        shared = p1.compute_shared_subset(row_results, baseline_rows)
        temporal = shared["per_cat"]["TEMPORAL"]
        assert temporal == {"shared": 4, "router_match": 3, "baseline_match": 4}
        assert temporal["router_match"] < temporal["baseline_match"]  # REGRESSION, by the gate rule
        assert shared["regressed"]["TEMPORAL"] == ["what's on my calendar today?"]
        assert shared["dropped"] == {}
        assert shared["added"] == {}

    def test_dropped_rows_reported_when_baseline_row_has_no_current_match(self):
        row_results = [_rr("when is my next meeting?", "TEMPORAL", "MATCH")]
        baseline_rows = [
            _br("when is my next meeting?", "TEMPORAL", "MATCH"),
            _br("what projects have I archived?", "PORTFOLIO", "MISMATCH"),
        ]
        shared = p1.compute_shared_subset(row_results, baseline_rows)
        assert shared["dropped"] == {"PORTFOLIO": ["what projects have I archived?"]}
        assert "PORTFOLIO" not in shared["per_cat"]

    def test_added_rows_reported_when_current_row_has_no_baseline_match(self):
        row_results = [
            _rr("when is my next meeting?", "TEMPORAL", "MATCH"),
            _rr("add todo buy oat milk", "EXECUTION", "MATCH"),
        ]
        baseline_rows = [_br("when is my next meeting?", "TEMPORAL", "MATCH")]
        shared = p1.compute_shared_subset(row_results, baseline_rows)
        assert shared["added"] == {"EXECUTION": ["add todo buy oat milk"]}
        assert "EXECUTION" not in shared["per_cat"]

    def test_prefix_fallback_matches_truncated_baseline_phrase(self):
        # baseline row rendered from a table that truncated (no ellipsis) —
        # current corpus has the full phrase
        row_results = [
            _rr(
                "remind me at 9:41 today to check in with the lead developer",
                "TEMPORAL",
                "MATCH",
            )
        ]
        baseline_rows = [
            _br(
                "remind me at 9:41 today to check in with the lead devel",  # truncated
                "TEMPORAL",
                "MATCH",
            )
        ]
        shared = p1.compute_shared_subset(row_results, baseline_rows)
        assert shared["per_cat"]["TEMPORAL"]["shared"] == 1
        assert shared["dropped"] == {}

    def test_review_rows_on_either_side_never_enter_shared(self):
        row_results = [_rr("hello", "CONVERSATION", "REVIEW")]
        baseline_rows = [_br("hello", "CONVERSATION", "REVIEW")]
        shared = p1.compute_shared_subset(row_results, baseline_rows)
        assert shared["per_cat"] == {}
        assert shared["dropped"] == {}
        assert shared["added"] == {}

    def test_error_verdict_scores_as_non_match_not_excluded(self):
        row_results = [_rr("what time is it?", "TEMPORAL", "ERROR")]
        baseline_rows = [_br("what time is it?", "TEMPORAL", "MATCH")]
        shared = p1.compute_shared_subset(row_results, baseline_rows)
        assert shared["per_cat"]["TEMPORAL"] == {
            "shared": 1,
            "router_match": 0,
            "baseline_match": 1,
        }
        assert shared["regressed"]["TEMPORAL"] == ["what time is it?"]


class TestBuildSharedSubsetSection:
    def test_regression_gate_and_named_row_appear_in_rendered_section(self):
        shared = {
            "per_cat": {"TEMPORAL": {"shared": 4, "router_match": 3, "baseline_match": 4}},
            "dropped": {},
            "added": {},
            "regressed": {"TEMPORAL": ["what's on my calendar today?"]},
        }
        text = "\n".join(p1.build_shared_subset_section(shared))
        assert "TEMPORAL | 4 | 3/4 | 4/4 | **REGRESSION**" in text
        assert "what's on my calendar today?" in text

    def test_no_shared_rows_is_stated_not_silently_skipped(self):
        shared = {
            "per_cat": {"CONVERSATION": {"shared": 0, "router_match": 0, "baseline_match": 0}},
            "dropped": {},
            "added": {},
            "regressed": {},
        }
        text = "\n".join(p1.build_shared_subset_section(shared))
        assert "no shared rows" in text


class TestParseBaselineRowDetail:
    def test_parses_real_baseline_doc(self):
        rows = p1.parse_baseline_row_detail(p1.PHASE0_BASELINE_DOC)
        assert len(rows) == 93  # the 08-12 FULL-CHAIN doc's stated corpus size
        asserted = [r for r in rows if r["verdict"] in ("MATCH", "MISMATCH")]
        assert len(asserted) == 39  # matches the doc's own TOTAL asserted column
        temporal_asserted = [r for r in asserted if r["category"] == "TEMPORAL"]
        assert len(temporal_asserted) == 4
        assert all(r["verdict"] == "MATCH" for r in temporal_asserted)
        phrases = {r["phrase"] for r in temporal_asserted}
        assert "what's on my calendar today?" in phrases

    def test_missing_section_raises(self, tmp_path):
        p = tmp_path / "bad.md"
        p.write_text("# no row detail section here\n")
        with pytest.raises(ValueError, match="Row detail"):
            p1.parse_baseline_row_detail(p)

    def test_empty_table_raises(self, tmp_path):
        p = tmp_path / "bad.md"
        p.write_text(
            "## Row detail\n\n| phrase | category | expected | s1 | decision | verdict | source |\n|---|---|---|---|---|---|---|\n"
        )
        with pytest.raises(ValueError, match="parsed zero rows"):
            p1.parse_baseline_row_detail(p)


class TestParsePhase1ReportRowDetail:
    def test_parses_real_2026_09_25_report_if_present(self):
        path = p1._DRY_RUN_REFERENCE_REPORT
        if not path.exists():
            pytest.skip(f"{path} not present in this checkout")
        rows = p1.parse_phase1_report_row_detail(path)
        assert rows  # non-empty
        assert all(r["verdict"] != "REVIEW" for r in rows)  # only asserted rows in this table


class TestRunDryRunIncludesSharedSubset:
    def test_dry_run_still_makes_no_llm_calls_and_exits_zero(self):
        import asyncio

        rc = asyncio.run(p1.run(dry_run=True, out=None))
        assert rc == 0
