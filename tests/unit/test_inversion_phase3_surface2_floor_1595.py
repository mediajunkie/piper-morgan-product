"""#1595 Phase 3 — the gate's SURFACE-2 floor rule (2026-10-02).

A row whose destination is a FLOOR-disposition action, whose pattern serves
it right, and whose router answer is declined/sub-threshold is FAIL at
surface 1 — unless a frozen surface-2 probe shows the LLM classifier landing
the phrase in the same category every time, in which case the pattern is not
load-bearing. Synthetic probe files; no LLM calls.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import inversion_phase3_deletion_gate as gate  # noqa: E402
import inversion_phase3_surface2_floor_probe as s2  # noqa: E402

CLAIM = gate.ClaimResult(
    pattern_list="STATUS_PATTERNS",
    action="get_project_status",
    category="STATUS",
    entry_surface="pre_classify",
)
LIVE = gate.CURRENT_LIVE_CATEGORIES


def _probe_file(tmp_path, rows):
    for r in rows:
        r.setdefault("served", "stub:stub-model")  # a served line is required (Arch condition 1)
    out = tmp_path / "probe.md"
    s2.write_report(rows, out, samples=max(r["sample"] for r in rows))
    return out


def _sub_threshold():
    return gate.RouterLookup(
        route="session_activity_query", conf=0.7, verdict="MISMATCH", source_table="synthetic"
    )


def test_parse_report_round_trips(tmp_path):
    rows = [
        {
            "phrase": "show today's progress",
            "sample": 1,
            "category": "STATUS",
            "action": "x",
            "confidence": 0.9,
        },
        {
            "phrase": "show today's progress",
            "sample": 2,
            "category": "STATUS",
            "action": "y",
            "confidence": 0.9,
        },
    ]
    parsed = s2.parse_report(_probe_file(tmp_path, rows))
    assert [r["category"] for r in parsed["show today's progress"]] == ["STATUS", "STATUS"]


def test_floor_row_with_unanimous_probe_is_ok(tmp_path, monkeypatch):
    rows = [
        {
            "phrase": "show today's progress",
            "sample": n,
            "category": "STATUS",
            "action": "a",
            "confidence": 0.9,
        }
        for n in (1, 2, 3)
    ]
    monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [_probe_file(tmp_path, rows)])
    ok, reason = gate.row_disposition(
        CLAIM, _sub_threshold(), "action:get_project_status", LIVE, phrase="show today's progress"
    )
    assert ok is True, reason
    assert "3/3 probe samples" in reason


def test_one_dissenting_sample_is_not_ok(tmp_path, monkeypatch):
    rows = [
        {
            "phrase": "show today's progress",
            "sample": 1,
            "category": "STATUS",
            "action": "a",
            "confidence": 0.9,
        },
        {
            "phrase": "show today's progress",
            "sample": 2,
            "category": "PRIORITY",
            "action": "b",
            "confidence": 0.9,
        },
    ]
    monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [_probe_file(tmp_path, rows)])
    ok, reason = gate.row_disposition(
        CLAIM, _sub_threshold(), "action:get_project_status", LIVE, phrase="show today's progress"
    )
    assert ok is False
    assert "1/2 probe samples" in reason


def test_no_probe_no_phrase_or_rail_destination_gets_no_credit(tmp_path, monkeypatch):
    monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [tmp_path / "absent.md"])
    ok, reason = gate.row_disposition(
        CLAIM, _sub_threshold(), "action:get_project_status", LIVE, phrase="show today's progress"
    )
    assert ok is False and "no surface-2 probe" in reason
    ok, reason = gate.row_disposition(CLAIM, _sub_threshold(), "action:get_project_status", LIVE)
    assert ok is False and "no phrase threaded" in reason
    # A rail-served destination never takes this route, probe or not.
    rows = [
        {
            "phrase": "what are my todos",
            "sample": 1,
            "category": "QUERY",
            "action": "a",
            "confidence": 0.9,
        }
    ]
    monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [_probe_file(tmp_path, rows)])
    rail_claim = gate.ClaimResult(
        pattern_list="X", action="list_todos_query", category="QUERY", entry_surface="pre_classify"
    )
    ok, reason = gate.row_disposition(
        rail_claim, _sub_threshold(), "action:list_todos_query", LIVE, phrase="what are my todos"
    )
    assert ok is False and "names list_todos_query only 0/1" in reason


def test_canonical_category_destination_takes_the_route(tmp_path, monkeypatch):
    assert "GUIDANCE" in gate._CANONICAL_CATEGORIES and "STATUS" not in gate._CANONICAL_CATEGORIES
    rows = [
        {
            "phrase": "what's your advice here",
            "sample": n,
            "category": "GUIDANCE",
            "action": "g",
            "confidence": 0.9,
        }
        for n in (1, 2)
    ]
    monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [_probe_file(tmp_path, rows)])
    claim = gate.ClaimResult(
        pattern_list="GUIDANCE_PATTERNS",
        action="get_contextual_guidance",
        category="GUIDANCE",
        entry_surface="pre_classify",
    )
    declined = gate.RouterLookup(
        route="CLARIFY", conf=0.4, verdict="MISMATCH", source_table="synthetic"
    )
    ok, reason = gate.row_disposition(
        claim, declined, "action:get_contextual_guidance", LIVE, phrase="what's your advice here"
    )
    assert ok is True, reason
    assert "canonical category (GUIDANCE) in 2/2" in reason


def test_a_report_without_a_served_line_is_refused(tmp_path, monkeypatch):
    """Arch condition 1 (2026-10-02): the gpt-4o-mini/Haiku catch one layer
    down — a probe that does not say which model answered gives no credit."""
    out = tmp_path / "unserved.md"
    out.write_text(
        "# probe\n\n| phrase | sample | surface-2 category | surface-2 action | confidence |\n"
        "|---|---|---|---|---|\n| show today's progress | 1 | STATUS | `x` | 0.9 |\n"
    )
    assert s2.report_served(out) is None
    real_reports = list(gate.SURFACE2_FLOOR_PROBES)
    monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [out])
    ok, reason = gate.row_disposition(
        CLAIM, _sub_threshold(), "action:get_project_status", LIVE, phrase="show today's progress"
    )
    assert ok is False and "no surface-2 probe" in reason
    # And the real reports of record both carry one.
    for p in real_reports:
        assert s2.report_served(p), p


def test_match_on_a_non_live_op_needs_the_probe(tmp_path, monkeypatch):
    """2026-10-02 (the GUIDANCE lane's STOP): a MATCH names the ruled op; it
    does not mean the consult SERVES it. On a non-live op the consult stands
    down and deletion hands the phrase to surface 2 — so a MATCH credits the
    row only when the op is live, or when the probe shows the same category."""
    match = gate.RouterLookup(
        route="get_contextual_guidance", conf=0.9, verdict="MATCH", source_table="synthetic"
    )
    claim = gate.ClaimResult(
        pattern_list="GUIDANCE_PATTERNS",
        action="get_contextual_guidance",
        category="GUIDANCE",
        entry_surface="pre_classify",
    )
    monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [tmp_path / "absent.md"])
    ok, reason = gate.row_disposition(
        claim, match, "action:get_contextual_guidance", LIVE, phrase="advise me on this decision"
    )
    assert ok is False and "NON-LIVE" in reason and "no surface-2 probe" in reason
    rows = [
        {
            "phrase": "advise me on this decision",
            "sample": n,
            "category": "GUIDANCE",
            "action": "g",
            "confidence": 0.9,
        }
        for n in range(1, 6)
    ]
    monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [_probe_file(tmp_path, rows)])
    ok, reason = gate.row_disposition(
        claim, match, "action:get_contextual_guidance", LIVE, phrase="advise me on this decision"
    )
    assert ok is True and "MATCH on a non-live op, and" in reason and "5/5" in reason
    # A MATCH on a LIVE op needs no probe — the consult owns it.
    live_match = gate.RouterLookup(
        route="list_todos_query", conf=0.95, verdict="MATCH", source_table="synthetic"
    )
    live_claim = gate.ClaimResult(
        pattern_list="X", action="list_todos_query", category="QUERY", entry_surface="pre_classify"
    )
    monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [tmp_path / "absent.md"])
    ok, reason = gate.row_disposition(
        live_claim, live_match, "action:list_todos_query", LIVE, phrase="what are my todos"
    )
    assert ok is True and reason.startswith("MATCH (expected action")


def test_rail_action_by_name_needs_the_same_action_every_sample(tmp_path, monkeypatch):
    """A rail entry reached by NAME but outside the live flag (a write such as
    close_issue_query): category alone proves nothing — surface 2 must name the
    same operation (alias-aware) in every sample."""
    claim = gate.ClaimResult(
        pattern_list="GITHUB_QUERY_PATTERNS",
        action="close_issue_query",
        category="EXECUTION",
        entry_surface="pre_classify",
    )
    match = gate.RouterLookup(
        route="close_issue", conf=0.95, verdict="MATCH", source_table="synthetic"
    )
    rows = [
        {
            "phrase": "close issue 42",
            "sample": n,
            "category": "EXECUTION",
            "action": "close_issue",
            "confidence": 0.9,
        }
        for n in range(1, 6)
    ]
    monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [_probe_file(tmp_path, rows)])
    ok, reason = gate.row_disposition(
        claim, match, "action:close_issue_query", LIVE, phrase="close issue 42"
    )
    assert ok is True and "names the same rail action" in reason and "5/5" in reason
    rows[2]["action"] = "comment_issue"  # one dissenting sample
    monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [_probe_file(tmp_path, rows)])
    ok, reason = gate.row_disposition(
        claim, match, "action:close_issue_query", LIVE, phrase="close issue 42"
    )
    assert ok is False and "4/5" in reason


def test_category_expectation_is_probed_by_category_and_floor_match_needs_nothing(
    tmp_path, monkeypatch
):
    claim = gate.ClaimResult(
        pattern_list="PRIORITY_PATTERNS",
        action="get_top_priority",
        category="PRIORITY",
        entry_surface="pre_classify",
    )
    match = gate.RouterLookup(
        route="get_top_priority", conf=0.9, verdict="MATCH", source_table="synthetic"
    )
    rows = [
        {
            "phrase": "what are my top priorities?",
            "sample": n,
            "category": "PRIORITY",
            "action": "p",
            "confidence": 0.9,
        }
        for n in range(1, 6)
    ]
    monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [_probe_file(tmp_path, rows)])
    ok, reason = gate.row_disposition(
        claim, match, "category:PRIORITY", LIVE, phrase="what are my top priorities?"
    )
    assert ok is True and "ruled category (PRIORITY)" in reason
    # A ruled `floor` MATCH (router declined) is the whole claim — no probe needed.
    declined = gate.RouterLookup(route="NONE", conf=0.9, verdict="MATCH", source_table="synthetic")
    monkeypatch.setattr(gate, "SURFACE2_FLOOR_PROBES", [tmp_path / "absent.md"])
    ok, reason = gate.row_disposition(
        claim, declined, "floor", LIVE, phrase="book a slot with the team"
    )
    assert ok is True and reason == "MATCH (ruled floor)"


def test_accepted_variance_needs_a_reason_and_an_unclaimed_phrase():
    """A documented surface-2 variance (one leg unanimous, the other split)
    passes the ledger's non-regression check only with a stated reason, and
    only while the phrase stays unclaimed by surface 1."""
    base = {
        "list": "SYNTHETIC",
        "rows_claimed_at_deletion": ["comment on 99"],
        "expected_op_by_phrase": {"comment on 99": "comment_issue_query"},
    }
    with_reason = dict(
        base,
        surface2_variance_accepted={
            "comment on 99": {"reason": "elliptical; clarify is defensible"}
        },
    )
    ok, problems = gate.check_deleted_entry_non_regression(with_reason, cats=LIVE)
    assert ok, problems
    without = dict(base, surface2_variance_accepted={"comment on 99": {"reason": ""}})
    ok, problems = gate.check_deleted_entry_non_regression(without, cats=LIVE)
    assert not ok


def test_load_bearing_literals_resolve_failing_rows_to_the_claiming_literal(monkeypatch):
    """PARTIAL deletion (2026-10-02): the literals the FAILING rows depend on
    survive; everything else goes. Synthetic list on the real matcher."""
    from services.intent_service.pre_classifier import PreClassifier

    monkeypatch.setattr(
        PreClassifier,
        "ZZ_SYNTHETIC_PATTERNS",
        [r"\bset up.*projects?\b", r"\bproject overview\b", r"\bzebra\b"],
        raising=False,
    )

    def rec(phrase, ok):
        return gate.RowRecord(
            phrase=phrase,
            category="X",
            expected="action:x",
            source="s",
            claim=gate.ClaimResult(
                pattern_list="ZZ_SYNTHETIC_PATTERNS",
                action="x",
                category="X",
                entry_surface="pre_classify",
            ),
            router=gate.RouterLookup(route=None, conf=None, verdict="UNSCORED", source_table=None),
            row_ok=ok,
            reason="",
        )

    failing = [rec("I want to set up my projects", False), rec("give me a project overview", False)]
    survivors = gate.load_bearing_literals("ZZ_SYNTHETIC_PATTERNS", failing)
    assert set(survivors) == {r"\bset up.*projects?\b", r"\bproject overview\b"}
    assert survivors[r"\bproject overview\b"] == ["give me a project overview"]
    assert gate.PreClassifier_claims_any(
        "ZZ_SYNTHETIC_PATTERNS", "give me a project overview", survivors
    )
    assert not gate.PreClassifier_claims_any("ZZ_SYNTHETIC_PATTERNS", "a zebra", survivors)
