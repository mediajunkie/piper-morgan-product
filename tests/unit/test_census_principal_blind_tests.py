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
# New shapes (batch 5): dispatch_workflow and _process_intent_internal —
# both use the SAME generic user_id= kwarg check as the original five (no
# new code path in _has_real_user_id itself), pinned here so a future
# change to that generic check can't silently stop covering them.
# ---------------------------------------------------------------------------


class TestDispatchWorkflowRecognized:
    def test_real_user_id_kwarg_is_real(self):
        assert _real(
            '(workflow_type="create_reminder", session_id="s", user_id="user-1560")',
            "dispatch_workflow",
        )

    def test_literal_none_is_blind(self):
        assert not _real(
            '(workflow_type="shipped_this_week", session_id="test-session", user_id=None)',
            "dispatch_workflow",
        )

    def test_no_user_id_kwarg_at_all_is_blind(self):
        assert not _real('(workflow_type="x", session_id="s")', "dispatch_workflow")


class TestProcessIntentInternalRecognized:
    def test_real_user_id_kwarg_is_real(self):
        assert _real(
            '(dummy_self, message="hi", session_id="default_session", user_id="user-a")',
            "_process_intent_internal",
        )

    def test_literal_none_is_blind(self):
        assert not _real(
            '(dummy_self, message="hi", session_id="s", user_id=None)',
            "_process_intent_internal",
        )

    def test_empty_parens_is_blind(self):
        """Guards the exact false-match shape from test_standup_routing_585.py:
        a docstring referencing `_process_intent_internal()` with no args at
        all (never a real call) must not read as real."""
        assert not _real("()", "_process_intent_internal")


# ---------------------------------------------------------------------------
# New (batch 5): the tokenize-based _scan_text() — replaces a hand-rolled
# comment-only stripper. Pins that COMMENT and STRING tokens (including
# docstrings, multi-line strings, and inline trailing comments) are blanked
# to same-length whitespace, that real code is left untouched, and that
# character positions are preserved (a call AFTER a stripped span is still
# found at its correct offset in the ORIGINAL text).
# ---------------------------------------------------------------------------


class TestScanTextTokenizeBasedStripping:
    def test_whole_line_comment_is_blanked(self):
        src = "# mock intent_service.process_intent (direct dispatch path)\nx = 1\n"
        scanned = census_mod._scan_text(src)
        assert "process_intent" not in scanned
        assert "x = 1" in scanned

    def test_trailing_inline_comment_is_also_blanked(self):
        """Unlike the old line-based stripper (batch 5's FIRST attempt, since
        replaced), a trailing comment on a line of real code is blanked too —
        the tokenizer doesn't distinguish whole-line vs trailing."""
        src = "x = 1  # calls process_intent(user_id=None) eventually\n"
        scanned = census_mod._scan_text(src)
        assert "process_intent" not in scanned
        assert "x = 1" in scanned

    def test_docstring_prose_is_blanked(self):
        src = (
            '"""\n'
            "The rail check in process_intent (`intent.action in get_action_workflows()`)\n"
            'runs BEFORE category routing.\n"""\n'
            "y = 2\n"
        )
        scanned = census_mod._scan_text(src)
        assert "process_intent" not in scanned
        assert "y = 2" in scanned

    def test_string_literal_call_name_is_blanked(self):
        """A call name appearing only inside a string (e.g. a patch() target
        path) is not real code either — general robustness win from
        tokenizing rather than regex-stripping comments only."""
        src = 'patch("services.foo.process_intent")\n'
        scanned = census_mod._scan_text(src)
        assert "process_intent" not in scanned

    def test_real_call_is_untouched(self):
        """The call NAME/shape (code, not string content) survives scanning
        unchanged — string literal VALUES are themselves STRING tokens and
        are blanked too, same as any other string; that's fine, because
        _call_text() always re-reads argument values from the ORIGINAL
        text (pinned by the position-preservation test below), never from
        the scanned text."""
        src = 'result = process_intent(message, session_id="s", user_id="real")\n'
        scanned = census_mod._scan_text(src)
        assert "process_intent(" in scanned
        assert "session_id=" in scanned
        assert "user_id=" in scanned

    def test_positions_preserved_for_call_after_blanked_comment(self):
        """The whole point of blanking (not deleting): _call_text() reads
        against the ORIGINAL text at the offset _CALL found in the SCANNED
        text — this only works if blanking preserves every character's
        position. A real call on the line right after a comment mentioning
        the same name must still be found at its correct offset."""
        src = (
            "# see process_intent(...) docs\n"
            'result = process_intent(message, session_id="s", user_id="real")\n'
        )
        scanned = census_mod._scan_text(src)
        matches = list(census_mod._CALL.finditer(scanned))
        assert len(matches) == 1, "the comment's mention must not also match"
        call_text = census_mod._call_text(src, matches[0].start())
        assert census_mod._has_real_user_id(call_text, "process_intent")

    def test_falls_back_to_original_on_tokenize_failure(self):
        """A handful of test fixture files are intentionally-invalid Python
        fragments (unbalanced brackets, etc.) — _scan_text must not crash
        the census, just skip stripping for that file."""
        broken = "def f(:\n    process_intent(user_id=None\n"
        scanned = census_mod._scan_text(broken)
        assert scanned == broken


# ---------------------------------------------------------------------------
# New (batch 5): the JWT-bearer-route fallback — a file whose ONLY
# KEYED_CALL_NAMES match is a zero-arg stub `process_intent(self, **kwargs)`
# definition can still be recognized as real if the file separately mints a
# real (non-None) user_id via generate_access_token() and uses it as a
# Bearer header. Scoped: must be an ALREADY-keyed file (this fallback only
# flips real from 0 to 1, never creates a KEYED match on its own).
# ---------------------------------------------------------------------------


class TestJwtBearerRouteFallback:
    def test_real_token_used_as_bearer_flips_the_file_to_real(self, synthetic_tests_root):
        (synthetic_tests_root / "unit").mkdir()
        (synthetic_tests_root / "unit" / "test_route.py").write_text(
            "class _Stub:\n"
            "    async def process_intent(self, **kwargs):\n"
            "        return None\n\n"
            "def _token(jwt_service):\n"
            "    user_id = 'a-real-uuid'\n"
            "    return jwt_service.generate_access_token(user_id=user_id, scopes=['user'])\n\n"
            "def test_x():\n"
            '    headers = {"Authorization": f"Bearer {token}"}\n'
        )
        c = census_mod.census()
        assert c["keyed"] == 1
        assert c["blind"] == 0
        assert c["blind_rows"] == []

    def test_token_without_bearer_usage_stays_blind(self, synthetic_tests_root):
        """generate_access_token(user_id=...) alone, with no evidence the
        token is ever sent as a Bearer header, is not enough — the fallback
        requires BOTH signals."""
        (synthetic_tests_root / "unit").mkdir()
        (synthetic_tests_root / "unit" / "test_route.py").write_text(
            "class _Stub:\n"
            "    async def process_intent(self, **kwargs):\n"
            "        return None\n\n"
            "def _token(jwt_service):\n"
            "    user_id = 'a-real-uuid'\n"
            "    return jwt_service.generate_access_token(user_id=user_id)\n"
        )
        c = census_mod.census()
        assert c["blind"] == 1

    def test_none_user_id_token_does_not_flip_even_with_bearer_usage(self, synthetic_tests_root):
        (synthetic_tests_root / "unit").mkdir()
        (synthetic_tests_root / "unit" / "test_route.py").write_text(
            "class _Stub:\n"
            "    async def process_intent(self, **kwargs):\n"
            "        return None\n\n"
            "def _token(jwt_service):\n"
            "    return jwt_service.generate_access_token(user_id=None)\n\n"
            "def test_x():\n"
            '    headers = {"Authorization": f"Bearer {token}"}\n'
        )
        c = census_mod.census()
        assert c["blind"] == 1

    def test_generate_access_token_alone_does_not_inflate_keyed(self, synthetic_tests_root):
        """A file that calls generate_access_token but never touches any
        KEYED_CALL_NAMES surface at all must not appear in KEYED — the
        fallback only PROMOTES an already-keyed file, never adds one."""
        (synthetic_tests_root / "unit").mkdir()
        (synthetic_tests_root / "unit" / "test_pure_auth.py").write_text(
            "def _token(jwt_service):\n"
            "    user_id = 'a-real-uuid'\n"
            "    return jwt_service.generate_access_token(user_id=user_id)\n\n"
            "def test_x():\n"
            '    headers = {"Authorization": f"Bearer {token}"}\n'
        )
        c = census_mod.census()
        assert c["scanned"] == 1
        assert c["keyed"] == 0
        assert c["blind"] == 0


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
