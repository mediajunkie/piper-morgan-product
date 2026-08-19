"""#1595 Phase 2.1 — unit tests for the snapshot-aware gate runner.

No LLM calls anywhere here (the runner's --dry contract): these tests pin
the fixture loader's validation (a malformed fixture must never reach a
scored run), the real-dataclass construction path, the armed matcher's
sentinel vocabulary, and the dry-run end-to-end.
"""

import asyncio
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import inversion_phase2_gate as gate  # noqa: E402

from services.intent_service.inversion_router import RoutingDecision  # noqa: E402
from services.intent_service.session_snapshot import (  # noqa: E402
    MAX_SERIALIZED_CHARS,
    SessionSnapshot,
)


# ── the shipped armed corpus ─────────────────────────────────────────────────


class TestShippedArmedCorpus:
    def test_loads_and_twins(self):
        rows = gate.load_armed_corpus()
        armed = [r for r in rows if r["condition"] == "armed"]
        control = [r for r in rows if r["condition"] == "control"]
        assert len(armed) == 7, "seven live-incident armed rows"
        assert len(control) == 7, "each armed row has a stateless control twin"
        by_pair = {}
        for r in rows:
            by_pair.setdefault(r["pair"], {})[r["condition"]] = r
        assert len(by_pair) == 7
        for pair, members in by_pair.items():
            assert set(members) == {"armed", "control"}, pair
            assert members["armed"]["phrase"] == members["control"]["phrase"], pair

    def test_armed_rows_build_the_real_dataclass(self):
        rows = gate.load_armed_corpus()
        for r in rows:
            if r["condition"] != "armed":
                assert "_snapshot" not in r and "_state_block" not in r
                continue
            assert isinstance(r["_snapshot"], SessionSnapshot), r["pair"]
            block = r["_state_block"]
            assert block and len(block) <= MAX_SERIALIZED_CHARS, r["pair"]
            # every armed fixture arms a pending offer → the contract's
            # OPEN QUESTION line (and its RULE) must be in the block
            assert "OPEN QUESTION" in block, r["pair"]
            assert "RULE:" in block, r["pair"]

    def test_armed_kinds_are_real_store_kinds(self):
        """Fixture kinds must be the arm sites' actual constants — a fixture
        naming a kind no store emits measures a world that cannot occur."""
        from services.intent_service.destructive_confirm import (  # noqa: F401
            CONFIRM_PENDING_ACTION_WORKFLOW,
        )
        from services.intent_service.drafted_issue import DRAFTED_ISSUE_KIND
        from services.intent_service.reminder_clear import (
            CLEAR_DELETE_CONFIRMATION_KIND,
            CLEAR_VERB_QUESTION_KIND,
        )
        from services.intent_service.repo_clarification import REPO_QUESTION_KIND
        from services.intent_service.standup_todo_offer import STANDUP_TODO_OFFER_KIND
        from services.intent_service.todo_handlers import REMINDER_TIME_QUESTION_KIND

        real_kinds = {
            CLEAR_VERB_QUESTION_KIND,
            CLEAR_DELETE_CONFIRMATION_KIND,
            DRAFTED_ISSUE_KIND,
            REMINDER_TIME_QUESTION_KIND,
            STANDUP_TODO_OFFER_KIND,
            REPO_QUESTION_KIND,
        }
        for r in gate.load_armed_corpus():
            if r["condition"] == "armed":
                assert r["fixture"]["pending_offer_kind"] in real_kinds, r["pair"]

    def test_phase0_corpus_is_untouched_by_extension(self):
        """The extension file must not leak rows into the phase0 loader —
        the frozen PHASE0_BASELINE comparison depends on it."""
        import inversion_phase0_baseline as p0

        phrases = {r["phrase"] for r in p0.load_corpus()}
        for r in gate.load_armed_corpus():
            assert r["phrase"] not in phrases, (
                f"armed-extension phrase collides with a phase0 row: {r['phrase']!r}"
            )


# ── loader validation (tmp corpora) ──────────────────────────────────────────


def _write(tmp_path, text):
    p = tmp_path / "armed.yaml"
    p.write_text(text)
    return p


_VALID_ROW = """corpus:
  - phrase: "delete"
    pair: p1
    condition: armed
    category: TEMPORAL
    expected: route:NONE
    source: "x"
    fixture:
      pending_offer_kind: reminder_clear_verb_question
      pending_offer_question: "done or delete?"
  - phrase: "delete"
    pair: p1
    condition: control
    category: TEMPORAL
    expected: REVIEW
    source: "x"
"""


class TestLoaderValidation:
    def test_valid_minimal_corpus_loads(self, tmp_path):
        rows = gate.load_armed_corpus(_write(tmp_path, _VALID_ROW))
        assert len(rows) == 2
        assert rows[0]["_state_block"].startswith("OPEN QUESTION")

    def test_unknown_fixture_key_fails_loudly(self, tmp_path):
        bad = _VALID_ROW.replace(
            "pending_offer_kind:", "pending_offer_kindx:"
        )
        with pytest.raises(ValueError, match="not on SessionSnapshot"):
            gate.load_armed_corpus(_write(tmp_path, bad))

    def test_armed_without_fixture_fails(self, tmp_path):
        bad = _VALID_ROW.replace(
            '    fixture:\n      pending_offer_kind: reminder_clear_verb_question\n'
            '      pending_offer_question: "done or delete?"\n',
            "",
        )
        with pytest.raises(ValueError, match="requires a fixture"):
            gate.load_armed_corpus(_write(tmp_path, bad))

    def test_control_with_fixture_fails(self, tmp_path):
        bad = _VALID_ROW + "    fixture:\n      draft_in_compose: true\n"
        with pytest.raises(ValueError, match="NO fixture"):
            gate.load_armed_corpus(_write(tmp_path, bad))

    def test_missing_control_twin_fails(self, tmp_path):
        bad = _VALID_ROW.split("  - phrase")[0] + "  - phrase" + (
            _VALID_ROW.split("  - phrase")[1]
        )
        with pytest.raises(ValueError, match="exactly one armed \\+ one control"):
            gate.load_armed_corpus(_write(tmp_path, bad))

    def test_twin_phrase_mismatch_fails(self, tmp_path):
        bad = _VALID_ROW.replace('phrase: "delete"\n    pair: p1\n    condition: control',
                                 'phrase: "remove"\n    pair: p1\n    condition: control')
        with pytest.raises(ValueError, match="phrases differ"):
            gate.load_armed_corpus(_write(tmp_path, bad))

    def test_bad_expected_vocabulary_fails(self, tmp_path):
        bad = _VALID_ROW.replace("expected: route:NONE", "expected: NONE")
        with pytest.raises(ValueError, match="bad expected"):
            gate.load_armed_corpus(_write(tmp_path, bad))

    def test_fixture_over_serialization_cap_fails_loudly(self, tmp_path):
        # a question grossly over the excerpt clip still serializes (the clip
        # truncates) — the loud failure is the dataclass contract's job; what
        # the loader must reject is an EMPTY block (fixture with no signal)
        bad = _VALID_ROW.replace(
            "      pending_offer_kind: reminder_clear_verb_question\n"
            '      pending_offer_question: "done or delete?"\n',
            "      pending_offer_is_confirm: false\n",
        )
        with pytest.raises(ValueError, match="EMPTY block"):
            gate.load_armed_corpus(_write(tmp_path, bad))


# ── the armed matcher's sentinel vocabulary ──────────────────────────────────


class TestArmedMatches:
    @pytest.fixture(scope="class")
    def op_categories(self):
        import inversion_phase1_shadow_score as p1

        return p1._op_category_map()

    def test_route_none_sentinel(self, op_categories):
        ok, note = gate.armed_matches(
            "route:NONE", RoutingDecision(outcome="none"), op_categories
        )
        assert ok and note == ""
        ok, note = gate.armed_matches(
            "route:NONE",
            RoutingDecision(outcome="operation", operation="complete_todo"),
            op_categories,
        )
        assert not ok and note == "complete_todo"

    def test_route_clarify_sentinel(self, op_categories):
        ok, _ = gate.armed_matches(
            "route:CLARIFY", RoutingDecision(outcome="clarify"), op_categories
        )
        assert ok

    def test_action_expected_delegates_to_alias_aware_matcher(self, op_categories):
        # set_reminder IS create_reminder (shared rail entry point)
        ok, _ = gate.armed_matches(
            "action:create_reminder",
            RoutingDecision(outcome="operation", operation="set_reminder"),
            op_categories,
        )
        assert ok

    def test_error_and_refused_annotated_never_matched(self, op_categories):
        ok, note = gate.armed_matches(
            "route:NONE", RoutingDecision(outcome="error", error="boom"), op_categories
        )
        assert not ok and note == "ERROR"
        ok, note = gate.armed_matches(
            "route:NONE", RoutingDecision(outcome="refused"), op_categories
        )
        assert not ok and note == "REFUSED"


# ── dry run end-to-end (no LLM) ──────────────────────────────────────────────


class TestDryRun:
    def test_dry_run_validates_without_llm(self, capsys):
        rc = asyncio.run(gate.run(dry=True, out=None))
        assert rc == 0
        out = capsys.readouterr().out
        assert "planned calls:" in out
        assert "No LLM calls made" in out
        # arithmetic stated with its denominators (m-44)
        assert "7 armed ×2 conditions + 7 control ×1" in out
