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
    assert ok is False and "not FLOOR-disposition" in reason
