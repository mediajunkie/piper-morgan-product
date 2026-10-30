"""Pins scripts/stamp_check.py's rules (xian 2026-10-16 via Exec: a date check in mail-send and the log)."""

import importlib.util
from datetime import datetime
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "stamp_check", Path(__file__).resolve().parents[3] / "scripts" / "stamp_check.py"
)
sc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sc)

NOW = datetime(2026, 10, 16, 16, 20, tzinfo=sc.PT)
DAY = "2026-10-16"


@pytest.mark.parametrize(
    "stamp, level",
    [
        ("2026-10-16 16:20 PT", None),
        ("2026-10-16 16:21 PT", "BLOCK"),
        ("2026-10-16 16:24 PT", "BLOCK"),
        ("2026-10-16", None),
        ("2026-10-16 16:26 PT", "BLOCK"),
        ("2026-10-16 17:40 PT", "BLOCK"),
        ("2026-10-16 16:2x PT", "WARN"),
        ("2026-10-16 16:1x PT", "WARN"),
        ("2026-10-16 14:2x PT", "BLOCK"),
        ("2026-10-16 16:5x PT", "BLOCK"),
        ("~16:20", "WARN"),
        ("2026-10-16 15:40 PT", "WARN"),
        ("2026-10-14", "WARN"),
        ("2026-10-17 09:00 PT", "BLOCK"),
    ],
)
def test_judge(stamp, level):
    v = sc.judge(stamp, NOW, DAY)
    assert (v[0] if v else None) == level, v


def test_front_date_reads_only_front_matter():
    assert (
        sc.front_date("---\nfrom: cio\ndate: 2026-10-16 16:20 PT\n---\ndate: nope\n")
        == "2026-10-16 16:20 PT"
    )
    assert sc.front_date("no front matter\ndate: 2026-10-16\n") is None


def test_empty_date_does_not_read_the_next_line():
    # Pard's 10-16 catch in the twin mail-wake regex: \s* crosses the newline.
    assert sc.front_date("---\nfrom: x\ndate:\nsubject: y\n---\n") is None


def test_briefing_stamps_reads_only_todays_attributions():
    line = "- **Usage** *(CIO, 2026-10-16 16:1x PDT, last row)*: ... *(Docs, 2026-10-12 10:1x PDT)* *(Lead, 2026-10-16 15:00 PT)*"
    assert sc.briefing_stamps(line, DAY) == ["2026-10-16 16:1x", "2026-10-16 15:00"]
    assert sc.judge("2026-10-16 16:1x", NOW, DAY)[0] == "WARN"
    assert sc.briefing_stamps("*(Exec, 2026-10-09 06:4x PDT)*", DAY) == []


def test_decision_stamps_reads_lead_stamp_and_inline_estimates():
    line = (
        "2026-10-16 16:15 PT (xian, in conversation with Lead; recorded by Exec 16:1x) — ADMIN: ..."
    )
    assert sc.decision_stamps(line, DAY) == ["2026-10-16 16:15", "2026-10-16 16:1x"]
    assert sc.judge("2026-10-16 16:1x", NOW, DAY)[0] == "WARN"
    assert sc.decision_stamps("2026-10-16 07:5x PT (xian) — GOALS", DAY) == ["2026-10-16 07:5x"]
    assert sc.decision_stamps("2026-10-09 06:4x PT (Exec) — old", DAY) == []


def test_stamp_now_writes_one_clock_reading_into_every_copy(tmp_path):
    a, b, c = tmp_path / "a.md", tmp_path / "b.md", tmp_path / "c.md"
    a.write_text("---\nfrom: cio\ndate: now\n---\nbody date: now stays\n")
    b.write_text("---\nfrom: cio\ndate: now PT\n---\nbody\n")
    c.write_text("---\nfrom: cio\ndate: 2026-10-16 16:10 PT\n---\nbody\n")
    sc.stamp_now([str(a), str(b), str(c), str(tmp_path / "missing.md")], NOW)
    assert a.read_text() == "---\nfrom: cio\ndate: 2026-10-16 16:20 PT\n---\nbody date: now stays\n"
    assert sc.front_date(b.read_text()) == "2026-10-16 16:20 PT"
    assert sc.front_date(c.read_text()) == "2026-10-16 16:10 PT"
    assert sc.judge(sc.front_date(a.read_text()), NOW, DAY) is None
