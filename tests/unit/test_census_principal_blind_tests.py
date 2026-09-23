"""Tests for scripts/census_principal_blind_tests.py (#1533 batch 4).

Pins the shapes the census script recognizes as REAL (non-None) principal
threading, and the shapes it deliberately does NOT scan/count. Batch 4 added
three recognized shapes on top of the batch-1/2 baseline (positional
user_id for get_or_create_context/clear_context, current_user= for the
process_intent route wrapper, and the by-design marker) plus one exclusion
(tests/archive/) — this file pins the OLD baseline shape still working
alongside each NEW shape, so a future edit can't silently regress one while
fixing another.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "census_principal_blind_tests.py"
_spec = importlib.util.spec_from_file_location("census_principal_blind_tests", _SCRIPT)
census_mod = importlib.util.module_from_spec(_spec)
sys.modules["census_principal_blind_tests"] = census_mod
_spec.loader.exec_module(census_mod)


def _real(call: str, func_name: str) -> bool:
    return census_mod._has_real_user_id(call, func_name)


# ---------------------------------------------------------------------------
# Baseline shape (batch 1/2) — must still work unchanged.
# ---------------------------------------------------------------------------


class TestBaselineKwargShapeStillDetected:
    def test_real_uuid_kwarg_is_real(self):
        assert _real("(message, session_id=session_id, user_id=str(uuid4()))", "process_intent")

    def test_literal_none_kwarg_is_blind(self):
        assert not _real("(message, session_id=session_id, user_id=None)", "process_intent")

    def test_no_user_id_at_all_is_blind(self):
        assert not _real('("hello", session_id="test")', "process_intent")

    def test_real_variable_kwarg_is_real_false_live_caveat_documented(self):
        """A user_id=some_var kwarg reads as real even if the variable is
        None at runtime — the known false-live blind spot, unchanged by
        batch 4 (static text scan can't resolve variable values)."""
        assert _real("(message, session_id=session_id, user_id=user_a)", "process_intent")


# ---------------------------------------------------------------------------
# New shape 1 (batch 4): positional user_id for get_or_create_context /
# clear_context — evidenced in test_floor_entry_context_1570.py's
# clear_context(session_id, user_id) cleanup calls.
# ---------------------------------------------------------------------------


class TestPositionalUserIdRecognized:
    @pytest.mark.parametrize("func_name", ["get_or_create_context", "clear_context"])
    def test_positional_real_user_id_is_real(self, func_name):
        assert _real("(session_id, user_id)", func_name)

    @pytest.mark.parametrize("func_name", ["get_or_create_context", "clear_context"])
    def test_positional_literal_none_is_blind(self, func_name):
        assert not _real("(session_id, None)", func_name)

    @pytest.mark.parametrize("func_name", ["get_or_create_context", "clear_context"])
    def test_kwarg_user_id_none_in_second_position_is_still_blind(self, func_name):
        """Regression pin for the bug caught during batch 4 authoring: a
        `user_id=None` KWARG landing at the positional index must not be
        misread as a positional value equal to the literal string
        'user_id=None' (which is never 'None' after a naive strcmp)."""
        assert not _real("(session_id, user_id=None)", func_name)

    @pytest.mark.parametrize("func_name", ["get_or_create_context", "clear_context"])
    def test_kwarg_user_id_real_in_second_position_is_real(self, func_name):
        assert _real("(session_id, user_id=user_a)", func_name)

    def test_positional_not_recognized_for_process_intent(self):
        """Deliberately NOT extended to process_intent/should_offer/
        record_offer — no evidenced instance in batch 4's ten files; stays a
        documented open blind spot rather than a speculative fix."""
        assert not _real("(message, session_id, user_a)", "process_intent")

    def test_session_id_only_call_has_no_second_arg(self):
        assert not _real("(session_id)", "clear_context")

    def test_out_of_order_kwarg_at_the_position_is_not_trusted(self):
        """If some OTHER kwarg (not user_id) happens to land at the assumed
        positional index, don't infer user_id from it."""
        assert not _real("(session_id, some_other_kwarg=real_value)", "get_or_create_context")


# ---------------------------------------------------------------------------
# New shape 2 (batch 4): current_user= for the process_intent ROUTE wrapper
# (web.api.routes.intent.process_intent) — evidenced in
# test_intent_conversation_ownership_1532.py.
# ---------------------------------------------------------------------------


class TestCurrentUserKwargRecognizedForProcessIntent:
    def test_real_current_user_is_real(self):
        assert _real("(req, current_user=_claims(USER_B))", "process_intent")

    def test_current_user_none_is_blind(self):
        assert not _real("(req, current_user=None)", "process_intent")

    def test_current_user_not_recognized_for_other_functions(self):
        """current_user is only ever a route-level process_intent kwarg —
        confirm the signal isn't (mis)applied to the other keyed names."""
        assert not _real("(session_id, current_user=_claims(USER_B))", "get_or_create_context")


# ---------------------------------------------------------------------------
# Integration-level: tests/archive/ exclusion, by-design marker bucketing,
# and the four-number denominator, run against a synthetic tests/ tree.
# ---------------------------------------------------------------------------


@pytest.fixture
def synthetic_tests_root(tmp_path, monkeypatch):
    root = tmp_path / "tests"
    root.mkdir()
    monkeypatch.setattr(census_mod, "TESTS", root)
    monkeypatch.setattr(census_mod, "ROOT", tmp_path)
    return root


class TestArchiveExclusion:
    def test_archive_file_is_not_scanned_or_counted(self, synthetic_tests_root):
        (synthetic_tests_root / "archive" / "load").mkdir(parents=True)
        (synthetic_tests_root / "archive" / "load" / "test_old.py").write_text(
            "def test_x():\n    process_intent(message, session_id='s', user_id=None)\n"
        )
        c = census_mod.census()
        assert c["scanned"] == 0
        assert c["keyed"] == 0
        assert c["blind"] == 0
        assert c["blind_rows"] == []

    def test_nested_archive_subdir_also_excluded(self, synthetic_tests_root):
        (synthetic_tests_root / "unit" / "archive").mkdir(parents=True)
        (synthetic_tests_root / "unit" / "archive" / "test_old2.py").write_text(
            "def test_x():\n    process_intent(message, session_id='s', user_id=None)\n"
        )
        c = census_mod.census()
        assert c["scanned"] == 0
        assert c["keyed"] == 0

    def test_non_archive_file_still_scanned(self, synthetic_tests_root):
        (synthetic_tests_root / "unit").mkdir()
        (synthetic_tests_root / "unit" / "test_live.py").write_text(
            "def test_x():\n    process_intent(message, session_id='s', user_id=None)\n"
        )
        c = census_mod.census()
        assert c["scanned"] == 1
        assert c["keyed"] == 1
        assert c["blind"] == 1


class TestByDesignMarker:
    def test_marked_blind_file_moves_to_by_design(self, synthetic_tests_root):
        (synthetic_tests_root / "unit").mkdir()
        (synthetic_tests_root / "unit" / "test_gate.py").write_text(
            "# principal-blind-by-design: testing the anonymous gate itself\n"
            "def test_x():\n"
            "    process_intent(req, current_user=None)\n"
        )
        c = census_mod.census()
        # Still scanned and keyed — the denominator stays honest.
        assert c["scanned"] == 1
        assert c["keyed"] == 1
        # But excluded from BLIND and listed separately with its reason.
        assert c["blind"] == 0
        assert c["by_design"] == 1
        assert c["by_design_rows"][0]["file"].endswith("test_gate.py")
        assert c["by_design_rows"][0]["by_design_reason"] == "testing the anonymous gate itself"

    def test_unmarked_blind_file_is_not_by_design(self, synthetic_tests_root):
        (synthetic_tests_root / "unit").mkdir()
        (synthetic_tests_root / "unit" / "test_plain.py").write_text(
            "def test_x():\n    process_intent(req, current_user=None)\n"
        )
        c = census_mod.census()
        assert c["blind"] == 1
        assert c["by_design"] == 0

    def test_marker_on_a_file_with_a_real_user_id_is_inert(self, synthetic_tests_root):
        """A marker on a file that ALSO has a real user_id call is neither
        BLIND nor BY-DESIGN — it's just keyed with real coverage; the marker
        has nothing to exclude."""
        (synthetic_tests_root / "unit").mkdir()
        (synthetic_tests_root / "unit" / "test_mixed.py").write_text(
            "# principal-blind-by-design: stale marker, file now has real coverage\n"
            "def test_x():\n"
            "    process_intent(req, current_user=_claims(USER_B))\n"
        )
        c = census_mod.census()
        assert c["blind"] == 0
        assert c["by_design"] == 0


class TestCountFlagUnaffectedInMeaning:
    def test_count_reflects_true_blind_only(self, synthetic_tests_root):
        """--count (the ratchet-shaped output) must keep meaning 'true
        BLIND' — a by-design file must not inflate it."""
        (synthetic_tests_root / "unit").mkdir()
        (synthetic_tests_root / "unit" / "test_gate.py").write_text(
            "# principal-blind-by-design: anonymous gate\n"
            "def test_x():\n"
            "    process_intent(req, current_user=None)\n"
        )
        (synthetic_tests_root / "unit" / "test_plain.py").write_text(
            "def test_x():\n    process_intent(req, current_user=None)\n"
        )
        c = census_mod.census()
        assert c["blind"] == 1  # only test_plain.py
        assert c["by_design"] == 1  # test_gate.py, separately
