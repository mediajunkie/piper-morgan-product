"""#2327: a floored action name outside every vocabulary is noted, safely.

#2270's gap (the classifier invented ``analyze_repository``, it was floored, and the
floor's reply looked like working behaviour) was found from a live mismatch days
later. The four floor fallthrough sites now share one check. Arch's ruling and HOST's
content bar (2026-11-14): only the importable vocabulary is consulted; the name is
recorded only when it is a short identifier, else withheld and never truncated; the
message's sha256 rides, never its text; no user id; it feeds an evidence line and a
counter; it never fails the person's turn.

LAYER: the audit module with the counter write replaced at its one seam, the evidence
logger captured, source pins on the four call sites, and the tally script's pure
functions. The counter's SQL and the admin endpoint are in the integration test.
DENOMINATOR: known, absent, invented (short, long, off-shape), a failing counter, an
unknown site; every importable name against the shape; the four sites; the tally.
The endpoint's gate and the flag control are in tests/unit/web/api/routes/test_admin_ops_2327.py.
"""

import ast
import io
import json
import logging
import sys
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from services.infrastructure.logging import evidence as ev
from services.intent_service import floored_action_audit as audit
from services.intent_service import routing_vocabulary as vocab
from services.utils.utterance_log import utterance_sha256

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
import floored_action_tally as tally_script  # noqa: E402

MESSAGE = "quick feedback and help me tidy this repository"
SHA = utterance_sha256(MESSAGE)


@pytest.fixture
def lines():
    """The evidence logger's lines for one test, as parsed JSON."""
    log = ev.configure_evidence_logger()
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(handler)
    yield lambda: [json.loads(ln) for ln in stream.getvalue().splitlines() if ln.strip()]
    log.removeHandler(handler)


@pytest.fixture
def counter(monkeypatch):
    mock = AsyncMock()
    monkeypatch.setattr(audit, "_increment", mock)
    return mock


class TestTheShape:
    def test_every_importable_name_fits_the_recorded_shape(self):
        """Arch 11-14: if a real name ever exceeds the cap, this fails, and the cap
        goes to HOST before it changes, rather than real names being withheld."""
        off = sorted(n for n in vocab.importable_vocabulary() if not vocab.fits_recorded_shape(n))
        assert off == []
        assert max(len(n) for n in vocab.importable_vocabulary()) <= 40

    @pytest.mark.parametrize(
        "name,recorded",
        [
            ("analyze_repository", "analyze_repository"),
            ("a" * 40, "a" * 40),
            ("a" * 41, None),
            ("email_jane_about_the_lawsuit_and_the_settlement_terms", None),
            ("Analyze_Repository", None),
            ("analyze repository", None),
            ("1st_action", None),
            ("analyze-repository", None),
        ],
    )
    def test_a_name_is_recorded_whole_or_withheld_never_cut(self, name, recorded):
        assert audit.recorded_name(name) == recorded

    @pytest.mark.parametrize(
        "name", ["a", "a1_b2", "z" * 40, "", "_a", "9a", "a" * 41, "aB", "a b", "a-b", "a.b", "é"]
    )
    def test_the_character_check_is_exactly_the_ruled_pattern(self, name):
        """HOST and Arch ruled the shape as ^[a-z][a-z0-9_]{0,39}$. The module checks
        characters (its package's regex count is a frozen ratchet); this proves the
        two agree, with the pattern living only in this test."""
        import re

        ruled = re.compile(r"^[a-z][a-z0-9_]{0,39}$")
        assert vocab.fits_recorded_shape(name) is bool(ruled.match(name))

    @pytest.mark.parametrize("value", [None, 7, ["a"], b"abc"])
    def test_a_non_string_never_fits(self, value):
        assert vocab.fits_recorded_shape(value) is False


class TestWhatCounts:
    def test_a_known_action_is_not_outside(self):
        assert audit.outside_vocabulary("create_todo") is False
        assert audit.outside_vocabulary("clarification_needed") is False  # category teaching

    @pytest.mark.parametrize("action", [None, "", "   ", 7, ["x"]])
    def test_no_action_is_not_an_invented_name(self, action):
        assert audit.outside_vocabulary(action) is False

    def test_an_invented_name_is_outside(self):
        assert audit.outside_vocabulary("tidy_the_whole_repository") is True

    def test_the_2270_name_is_known_now(self):
        """``analyze_repository`` was the invented name that prompted this; 2270's
        fix made it a real action, so it is no longer reported."""
        assert audit.outside_vocabulary("analyze_repository") is False


class TestTheNote:
    async def test_a_known_action_records_nothing(self, lines, counter):
        await audit.note_floored_action(audit.SITE_QUERY_ACTION, "create_todo", MESSAGE)
        assert lines() == []
        counter.assert_not_awaited()

    async def test_an_invented_short_name_is_recorded_with_site_and_sha_only(self, lines, counter):
        await audit.note_floored_action(
            audit.SITE_ANALYSIS_ACTION, "tidy_the_whole_repository", MESSAGE
        )
        (line,) = lines()
        assert line["event"] == "floored_action_outside_vocabulary"
        assert line["site"] == "analysis_action_routing_to_floor"
        assert line["action"] == "tidy_the_whole_repository"
        assert line["message_sha256"] == SHA
        # HOST's bar: nothing but those, plus the logger's own fields.
        assert set(line) == {
            "event",
            "site",
            "action",
            "message_sha256",
            "logger",
            "level",
            "timestamp",
        }
        assert MESSAGE not in json.dumps(line)
        assert "evidence_event_unlisted" not in line and "evidence_fields_dropped" not in line
        counter.assert_awaited_once_with(
            "tidy_the_whole_repository", "analysis_action_routing_to_floor"
        )

    @pytest.mark.parametrize(
        "action",
        ["email_jane_about_the_lawsuit_and_the_settlement_terms", "Tell Me A Secret", "a" * 41],
    )
    async def test_a_name_off_the_shape_is_withheld_whole(self, lines, counter, action):
        await audit.note_floored_action(audit.SITE_ACTION_GATE, action, MESSAGE)
        (line,) = lines()
        assert line["action_withheld"] is True
        assert "action" not in line
        text = json.dumps(line)
        assert action not in text and action[:20] not in text  # not truncated either
        assert line["message_sha256"] == SHA
        counter.assert_awaited_once_with(audit.WITHHELD, audit.SITE_ACTION_GATE)

    def test_the_withheld_value_can_never_be_a_real_name(self):
        assert not vocab.fits_recorded_shape(audit.WITHHELD)

    async def test_a_failing_counter_never_fails_the_turn_and_the_line_is_still_written(
        self, lines, monkeypatch
    ):
        monkeypatch.setattr(audit, "_increment", AsyncMock(side_effect=RuntimeError("db down")))
        await audit.note_floored_action(
            audit.SITE_QUERY_ACTION, "tidy_the_whole_repository", MESSAGE
        )
        assert len(lines()) == 1

    async def test_a_hung_counter_write_is_bounded_and_the_line_is_still_written_2373(
        self, lines, monkeypatch
    ):
        """#2373: the write is awaited on the person's turn. A write that never returns
        costs the reply the bound and no more; it is cancelled, and nothing raises."""
        import asyncio
        import time

        cancelled = []

        async def hangs(name, site):
            try:
                await asyncio.sleep(60)
            except asyncio.CancelledError:
                cancelled.append(site)
                raise

        monkeypatch.setattr(audit, "_increment", hangs)
        monkeypatch.setattr(audit, "COUNT_WRITE_TIMEOUT_S", 0.2)
        start = time.monotonic()
        await audit.note_floored_action(
            audit.SITE_QUERY_ACTION, "tidy_the_whole_repository", MESSAGE
        )
        assert time.monotonic() - start < 1.5
        assert len(lines()) == 1
        assert cancelled == [audit.SITE_QUERY_ACTION]  # not left running after the turn

    def test_the_shipped_bound_is_about_two_seconds_2373(self):
        assert audit.COUNT_WRITE_TIMEOUT_S == 2.0

    async def test_a_failing_vocabulary_read_never_fails_the_turn(self, counter, monkeypatch):
        monkeypatch.setattr(audit, "importable_vocabulary", lambda: 1 / 0)
        await audit.note_floored_action(
            audit.SITE_QUERY_ACTION, "tidy_the_whole_repository", MESSAGE
        )
        counter.assert_not_awaited()

    async def test_an_unknown_site_records_nothing(self, lines, counter):
        await audit.note_floored_action("some_other_site", "tidy_the_whole_repository", MESSAGE)
        assert lines() == []
        counter.assert_not_awaited()

    async def test_no_message_still_records_a_sha(self, lines, counter):
        await audit.note_floored_action(audit.SITE_QUERY_ACTION, "tidy_the_whole_repository", None)
        assert lines()[0]["message_sha256"] == utterance_sha256("")


class TestTestsDoNotWriteTheCounter:
    def test_the_counter_write_is_a_no_op_under_pytest(self):
        """The autouse fixture in tests/conftest.py replaces the write, so a test that
        floors a made-up action name leaves no row in a shared developer database."""
        assert audit._increment.__name__ == "_no_write"


class TestTheFourSites:
    def test_each_floor_site_calls_the_note_with_its_own_site(self):
        """Each of the four ``*_routing_to_floor`` log calls is followed by the note,
        awaited, with that site's constant, the intent's action and its message."""
        src = (ROOT / "services/intent/intent_service.py").read_text()
        tree = ast.parse(src)
        seen = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Await) and isinstance(node.value, ast.Call):
                call = node.value
                if ast.unparse(call.func) == "_floored_action_audit.note_floored_action":
                    seen.append([ast.unparse(a) for a in call.args])
        assert sorted(a[0] for a in seen) == sorted(
            f"_floored_action_audit.{c}"
            for c in (
                "SITE_ACTION_GATE",
                "SITE_ANALYSIS_ACTION",
                "SITE_CANONICAL_GENERIC",
                "SITE_QUERY_ACTION",
            )
        )
        assert all(a[1:] == ["intent.action", "intent.original_message"] for a in seen)
        for site in audit.SITES:
            assert src.count(f'"{site}"') == 1, f"{site}: its own log line should appear once"

    def test_the_runtime_module_never_reads_the_pre_classifiers_source(self):
        """Arch 11-14: reading pre_classifier.py's text is for tests and scripts."""
        src = (ROOT / "services/intent_service/floored_action_audit.py").read_text()
        assert "pre_classifier_surface" not in src and "full_vocabulary" not in src
        shared = (ROOT / "services/intent_service/routing_vocabulary.py").read_text()
        assert "read_text" not in shared and "\nimport re\n" not in shared


class TestTheTally:
    PAYLOAD = {
        "window": {"days": 30, "since": "2026-10-16", "through": "2026-11-14"},
        "first_day": "2026-11-10",
        "last_day": "2026-11-13",
        "row_count": 5,
        "rows": [
            {
                "name": "tidy_the_whole_repository",
                "site": audit.SITE_ANALYSIS_ACTION,
                "day": "2026-11-10",
                "count": 3,
            },
            {
                "name": "tidy_the_whole_repository",
                "site": audit.SITE_ACTION_GATE,
                "day": "2026-11-13",
                "count": 1,
            },
            {"name": "tidy_up", "site": audit.SITE_QUERY_ACTION, "day": "2026-11-12", "count": 1},
            {"name": "(withheld)", "site": audit.SITE_ACTION_GATE, "day": "2026-11-12", "count": 2},
            {
                "name": "pre_only_name",
                "site": audit.SITE_QUERY_ACTION,
                "day": "2026-11-11",
                "count": 4,
            },
        ],
    }

    def test_names_are_grouped_and_known_names_are_dropped(self):
        result = tally_script.tally(self.PAYLOAD, {"pre_only_name", "create_todo"})
        names = {n["name"]: n for n in result["names"]}
        assert names["tidy_the_whole_repository"]["count"] == 4
        assert names["tidy_the_whole_repository"]["sites"] == {
            audit.SITE_ACTION_GATE: 1,
            audit.SITE_ANALYSIS_ACTION: 3,
        }
        assert names["tidy_the_whole_repository"]["first_day"] == "2026-11-10"
        assert names["tidy_the_whole_repository"]["last_day"] == "2026-11-13"
        assert names["tidy_up"]["count"] == 1
        assert "pre_only_name" not in names
        assert result["dropped_as_known"] == {"pre_only_name": 4}
        assert result["withheld"] == 2

    def test_the_report_always_shows_the_window_it_saw(self):
        text = tally_script.render(tally_script.tally(self.PAYLOAD, {"pre_only_name"}))
        assert "Window asked for: 2026-10-16 to 2026-11-14 (30 days, UTC)" in text
        assert "Days holding rows: 2026-11-10 to 2026-11-13; rows read: 5" in text
        assert "tidy_the_whole_repository: 4" in text
        assert "Withheld" in text and "2 sighting(s)" in text

    def test_no_names_is_only_said_beside_its_window(self):
        empty = {
            "window": {"days": 7, "since": "2026-11-08", "through": "2026-11-14"},
            "first_day": None,
            "last_day": None,
            "row_count": 0,
            "rows": [],
        }
        text = tally_script.render(tally_script.tally(empty, set()))
        assert text.splitlines()[-1] == "No out-of-vocabulary names in this window."
        assert "Window asked for: 2026-11-08 to 2026-11-14 (7 days, UTC)" in text
        assert "Days holding rows: none to none; rows read: 0" in text

    def test_input_that_is_not_the_endpoints_json_is_refused(self, tmp_path, capsys):
        bad = tmp_path / "x.json"
        bad.write_text('{"something": "else"}')
        assert tally_script.main(["tally", str(bad)]) == 2
        bad.write_text("not json")
        assert tally_script.main(["tally", str(bad)]) == 2
