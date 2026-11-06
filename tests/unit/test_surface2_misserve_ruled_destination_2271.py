"""#2271 (Arch, decisions.log 2026-11-06 11:49): the deletion gate's #1933 mis-serve
check disqualified any surface-2 sample that resolves to a registered WRITE, even when
that sample is the row's ruled destination's own entry (an alias of the op the row is
ruled to reach). One exemption: the same entry object as the ruled destination, which
comes from the ledger or corpus row, never from the phrase or the samples. Every other
registered WRITE/DESTRUCTIVE sample still disqualifies.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import inversion_phase3_deletion_gate as gate  # noqa: E402


def _samples(monkeypatch, *actions):
    monkeypatch.setattr(
        gate, "_surface2_probe_rows", lambda phrase: [{"action": a} for a in actions]
    )


def test_an_alias_of_the_ruled_destination_is_not_worse(monkeypatch):
    # edit_document is a registered alias of update_document's entry (WRITE).
    _samples(monkeypatch, "edit_document", "edit_document")
    ok, reason = gate._surface2_misserve_safe("edit the plan doc", "action:update_document")
    assert ok, reason


def test_a_different_write_still_disqualifies(monkeypatch):
    # #1933's own case: a write nobody asked for, on a row ruled elsewhere.
    _samples(monkeypatch, "update_document_query")
    ok, reason = gate._surface2_misserve_safe("edit my project description", "action:link_repo")
    assert not ok
    assert "update_document_query" in reason


def test_no_ruled_destination_exempts_nothing(monkeypatch):
    _samples(monkeypatch, "edit_document")
    ok, _ = gate._surface2_misserve_safe("edit the plan doc", None)
    assert not ok


def test_an_unregistered_ruled_destination_exempts_nothing(monkeypatch):
    _samples(monkeypatch, "edit_document")
    ok, _ = gate._surface2_misserve_safe("edit the plan doc", "action:no_such_op")
    assert not ok


@pytest.mark.parametrize("ruled", ["floor", "plan"])
def test_a_non_action_ruling_exempts_nothing(monkeypatch, ruled):
    _samples(monkeypatch, "edit_document")
    ok, _ = gate._surface2_misserve_safe("edit the plan doc", ruled)
    assert not ok
