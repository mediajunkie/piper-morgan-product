"""Pre-claim shadow probe — the measurement backbone for the pre-classifier
narrowing schedule (PM-ratified 2026-08-29; decisions.log same date).

Pinned here (the delegation's pin list, verbatim):

1. DEFAULT-OFF BYTE-IDENTICAL (explosive-shadow idiom) — flag unset means no
   task, the router is never touched (explosive double), and the claim the
   pre-classifier makes is byte-identical to the pre-threading claim.
2. SAMPLED-ON — the shadow is consulted EXACTLY ONCE per claimed turn, with
   zero effect on the response (spy + transcript-identical against a
   flag-off run).
3. FAIL-OPEN — a shadow exception is error-logged and swallowed; the claim
   is unaffected.
4. PATTERN-LIST IDENTITY threads correctly for at least 3 different claiming
   lists, on BOTH surface-1 entry surfaces.
5. REPORT HELPER output shape (per-list counts, agreement rates,
   precision-vs-bar readout, m-44 denominators).

LLM-free throughout: the router's ``route`` is a scripted or explosive
double; ``derive_routing_grammar`` is the real registry read (no LLM).

#1595 Phase 3, ninth deletion (2026-10-03): this file's canonical
DISCOVERY-claimed fixture phrase was "what can you do?" (matched the now-
deleted ``\\bwhat can you do\\b`` literal). Swapped throughout to "I need
help understanding something" — the one load-bearing DISCOVERY_PATTERNS
survivor (``\\bneed\\s*help\\b``) still claims it as DISCOVERY/get_capabilities
via ``pre_classify``/``pre_classify_with_pattern_list``, confirmed live this
session, so every test here that depends on surface 1 claiming
deterministically (the explosive-router pins especially) is unaffected by
the deletion.
"""

from __future__ import annotations

import pytest

from services.intent_service import preclaim_shadow
from services.intent_service.classifier import IntentClassifier
from services.intent_service.inversion_router import RoutingDecision, derive_routing_grammar
from services.intent_service.pre_classifier import PreClassifier
from services.intent_service.preclaim_shadow import (
    AGREEMENT_EVENT,
    DISAGREEMENT_EVENT,
    FAILURE_EVENT,
    INCOMPARABLE_EVENT,
    aggregate_preclaim_events,
    compare_claim,
    maybe_schedule_preclaim_shadow,
    render_preclaim_report,
)

# ---------------------------------------------------------------------------
# Doubles (the #1668 test idioms)
# ---------------------------------------------------------------------------


class _RecordingLogger:
    """Captures (event, fields) for info/warning/error."""

    def __init__(self):
        self.info_events = []
        self.error_events = []

    def info(self, event, **fields):
        self.info_events.append((event, fields))

    def warning(self, event, **fields):
        self.info_events.append((event, fields))

    def error(self, event, **fields):
        self.error_events.append((event, fields))

    def debug(self, event, **fields):
        pass

    @property
    def events(self):
        return [e for e, _ in self.info_events]

    def fields_for(self, event):
        return next(f for e, f in self.info_events if e == event)


@pytest.fixture
def log_rec(monkeypatch):
    rec = _RecordingLogger()
    monkeypatch.setattr(preclaim_shadow, "logger", rec)
    return rec


@pytest.fixture
def probe_on(monkeypatch):
    monkeypatch.setenv("PIPER_PRECLAIM_SHADOW", "1")
    monkeypatch.setenv("PIPER_PRECLAIM_SHADOW_SAMPLE", "1.0")


@pytest.fixture
def explosive_router(monkeypatch):
    """Any router call with the flag OFF is the default-off pin's defect."""
    from services.intent_service import inversion_router as ir

    async def _boom(*a, **k):
        raise AssertionError("inversion router consulted while PIPER_PRECLAIM_SHADOW is off")

    monkeypatch.setattr(ir, "route", _boom)


def _scripted_router(monkeypatch, operation="get_capabilities", outcome="operation"):
    """Install a counting scripted route; returns the call list."""
    from services.intent_service import inversion_router as ir

    calls = []

    async def _route(message, session_state, *, llm_service=None, grammar=None, user_id=None):
        calls.append(message)
        return RoutingDecision(
            outcome=outcome,
            operation=operation if outcome == "operation" else None,
            confidence=0.9,
            llm_calls=1,
        )

    monkeypatch.setattr(ir, "route", _route)
    return calls


# ---------------------------------------------------------------------------
# Pin 1 — default-off byte-identical
# ---------------------------------------------------------------------------


class TestDefaultOff:
    async def test_flag_off_schedules_nothing_and_never_touches_router(
        self, monkeypatch, explosive_router
    ):
        monkeypatch.delenv("PIPER_PRECLAIM_SHADOW", raising=False)
        task = maybe_schedule_preclaim_shadow(
            "I need help understanding something",
            claimed_category="discovery",
            claimed_action="get_capabilities",
            pattern_list="DISCOVERY_PATTERNS",
            entry_surface="pre_classify",
        )
        assert task is None

    async def test_flag_off_classify_claim_is_byte_identical(self, monkeypatch, explosive_router):
        """The classifier's surface-1 claim with the probe OFF equals the
        legacy pre_classify claim field-for-field (and the explosive router
        proves no consult happened on the way)."""
        monkeypatch.delenv("PIPER_PRECLAIM_SHADOW", raising=False)
        clf = IntentClassifier(llm_service=None)
        got = await clf.classify("I need help understanding something", use_cache=False)
        legacy = PreClassifier.pre_classify("I need help understanding something")
        assert (got.category, got.action, got.confidence) == (
            legacy.category,
            legacy.action,
            legacy.confidence,
        )
        assert got.context.get("original_message") == legacy.context.get("original_message")

    def test_threading_sibling_returns_identical_claims(self):
        """pre_classify IS the sibling minus the name — spot-checked across
        claim shapes (the delegator pin)."""
        for msg in (
            "I need help understanding something",
            "remind me to hydrate",
            "who are you?",
            "what time is it?",
            "totally unclaimed gibberish qwertyuiop",
        ):
            via_sibling, _name = PreClassifier.pre_classify_with_pattern_list(msg)
            legacy = PreClassifier.pre_classify(msg)
            if legacy is None:
                assert via_sibling is None
            else:
                assert (via_sibling.category, via_sibling.action) == (
                    legacy.category,
                    legacy.action,
                )

    async def test_sample_zero_schedules_nothing(self, monkeypatch, explosive_router):
        monkeypatch.setenv("PIPER_PRECLAIM_SHADOW", "1")
        monkeypatch.setenv("PIPER_PRECLAIM_SHADOW_SAMPLE", "0.0")
        task = maybe_schedule_preclaim_shadow(
            "I need help understanding something",
            claimed_category="discovery",
            claimed_action="get_capabilities",
            pattern_list="DISCOVERY_PATTERNS",
            entry_surface="pre_classify",
        )
        assert task is None


# ---------------------------------------------------------------------------
# Pin 2 — sampled-on: exactly one consult, zero effect on the response
# ---------------------------------------------------------------------------


class TestSampledOn:
    async def test_one_consult_per_claimed_turn_transcript_identical(
        self, monkeypatch, probe_on, log_rec
    ):
        calls = _scripted_router(monkeypatch, operation="get_capabilities")

        clf_on = IntentClassifier(llm_service=None)
        got_on = await clf_on.classify("I need help understanding something", use_cache=False)
        # Drain the fire-and-forget task deterministically.
        assert len(preclaim_shadow._INFLIGHT) == 1
        await next(iter(preclaim_shadow._INFLIGHT))

        assert calls == ["I need help understanding something"], "shadow consulted exactly once"
        assert AGREEMENT_EVENT in log_rec.events

        # Transcript-identical: the flag-off run returns the same claim.
        monkeypatch.delenv("PIPER_PRECLAIM_SHADOW", raising=False)
        clf_off = IntentClassifier(llm_service=None)
        got_off = await clf_off.classify("I need help understanding something", use_cache=False)
        assert (got_on.category, got_on.action, got_on.confidence) == (
            got_off.category,
            got_off.action,
            got_off.confidence,
        )

    async def test_multi_intent_surface_schedules_with_all_lists(
        self, monkeypatch, probe_on, log_rec
    ):
        # #1595 Phase 3 third deletion (2026-10-01): CALENDAR_QUERY_PATTERNS
        # is deleted — "hi piper! what's on my agenda?" no longer produces a
        # second (calendar) claim (TEMPORAL_PATTERNS has no "agenda"
        # vocabulary, confirmed empirically, so this is now a single-intent
        # greeting-only message, not a 2-intent shape). Swapped to "hi
        # piper! what's blocking the milestone?" (GREETING_PATTERNS +
        # ANALYSIS_PATTERNS), unaffected by the deletion and already used
        # elsewhere in this file for the same "3+ distinct claiming lists"
        # substitution (test_identity_reaches_telemetry_for_three_lists) —
        # preserves this test's actual point (one shadow consult per
        # claimed turn, even multi-intent) intact.
        calls = _scripted_router(monkeypatch, operation="analyze_blockers")
        clf = IntentClassifier(llm_service=None)
        result = await clf.classify_multiple("hi piper! what's blocking the milestone?")
        assert len(result.intents) == 2  # greeting + analysis
        assert len(preclaim_shadow._INFLIGHT) == 1
        await next(iter(preclaim_shadow._INFLIGHT))

        assert len(calls) == 1, "one consult per claimed turn, even multi-intent"
        event = next(e for e in log_rec.events if e.startswith("preclaim_shadow_"))
        fields = log_rec.fields_for(event)
        assert fields["entry_surface"] == "detect_multiple_intents"
        # Primary intent is the substantive one (analyze_blockers from ANALYSIS).
        assert fields["pre_action"] == "analyze_blockers"
        assert fields["pattern_list"] == "ANALYSIS_PATTERNS"
        assert set(fields["all_pattern_lists"]) == {
            "GREETING_PATTERNS",
            "ANALYSIS_PATTERNS",
        }


# ---------------------------------------------------------------------------
# Pin 3 — fail-open
# ---------------------------------------------------------------------------


class TestFailOpen:
    async def test_router_exception_is_swallowed_and_error_logged(
        self, monkeypatch, probe_on, log_rec
    ):
        from services.intent_service import inversion_router as ir

        async def _boom(*a, **k):
            raise RuntimeError("router transport down")

        monkeypatch.setattr(ir, "route", _boom)
        task = maybe_schedule_preclaim_shadow(
            "I need help understanding something",
            claimed_category="discovery",
            claimed_action="get_capabilities",
            pattern_list="DISCOVERY_PATTERNS",
            entry_surface="pre_classify",
        )
        assert task is not None
        await task  # must not raise
        assert [e for e, _ in log_rec.error_events] == [FAILURE_EVENT]
        failure = next(f for e, f in log_rec.error_events if e == FAILURE_EVENT)
        assert failure["pattern_list"] == "DISCOVERY_PATTERNS"

    async def test_claim_unaffected_when_probe_explodes(self, monkeypatch, probe_on, log_rec):
        from services.intent_service import inversion_router as ir

        async def _boom(*a, **k):
            raise RuntimeError("router transport down")

        monkeypatch.setattr(ir, "route", _boom)
        clf = IntentClassifier(llm_service=None)
        got = await clf.classify("I need help understanding something", use_cache=False)
        assert got.action == "get_capabilities"
        for task in list(preclaim_shadow._INFLIGHT):
            await task


# ---------------------------------------------------------------------------
# Pin 4 — pattern-list identity threading (≥3 lists, both entry surfaces)
# ---------------------------------------------------------------------------


class TestPatternIdentityThreading:
    @pytest.mark.parametrize(
        "message,want_list,want_action",
        [
            ("I need help understanding something", "DISCOVERY_PATTERNS", "get_capabilities"),
            ("what's blocking the milestone?", "ANALYSIS_PATTERNS", "analyze_blockers"),
            ("who are you?", "IDENTITY_PATTERNS", "get_identity"),
            # the two claim sites WITHOUT a class-level list resolve to their
            # documented synthetic/underlying names
            (
                "what's the next milestone?",
                "MILESTONE_STATUS_INLINE_PATTERNS",
                "get_project_status",
            ),
            ("connect my github", "INTEGRATION_CONNECT_PATTERNS", "get_contextual_guidance"),
        ],
    )
    def test_pre_classify_surface_names_its_list(self, message, want_list, want_action):
        intent, name = PreClassifier.pre_classify_with_pattern_list(message)
        assert intent is not None and intent.action == want_action
        assert name == want_list

    @pytest.mark.parametrize(
        "message",
        ["remind me to hydrate", "what reminders do I have?"],
    )
    def test_deleted_phase3_lists_name_no_list(self, message):
        """#1595 Phase 3 (2026-09-27): REMINDER_PATTERNS and
        REMINDER_QUERY_PATTERNS were emptied — these two parametrize rows
        used to prove the threading names a specific claiming list; now the
        honest fact is that NO list claims (the two entries above,
        DISCOVERY_PATTERNS/need-help and ANALYSIS_PATTERNS/whats-
        blocking, substitute for the "3+ distinct claiming lists" coverage
        this class's docstring pin (#4) requires)."""
        assert PreClassifier.pre_classify_with_pattern_list(message) == (None, None)

    def test_no_claim_is_none_none(self):
        assert PreClassifier.pre_classify_with_pattern_list("qqq zzz vvv") == (None, None)

    def test_multi_surface_pattern_lists_align_with_intents(self):
        # #1595 Phase 3 third deletion (2026-10-01): CALENDAR_QUERY_PATTERNS
        # is deleted — "hi piper! what's on my agenda?" no longer produces a
        # second (calendar) claim (TEMPORAL_PATTERNS has no "agenda"
        # vocabulary — confirmed empirically). Swapped to "hi piper! what's
        # blocking the milestone?" (GREETING_PATTERNS + ANALYSIS_PATTERNS),
        # unaffected by the deletion, same substitution as
        # TestSampledOn.test_multi_intent_surface_schedules_with_all_lists.
        result = PreClassifier.detect_multiple_intents("hi piper! what's blocking the milestone?")
        assert len(result.pattern_lists) == len(result.intents)
        by_action = dict(zip((i.action for i in result.intents), result.pattern_lists))
        assert by_action["greeting"] == "GREETING_PATTERNS"
        assert by_action["analyze_blockers"] == "ANALYSIS_PATTERNS"

    def test_multi_surface_connect_substitution_named(self):
        result = PreClassifier.detect_multiple_intents("hi piper, connect my calendar")
        by_action = dict(zip((i.action for i in result.intents), result.pattern_lists))
        assert by_action["get_contextual_guidance"] == "INTEGRATION_CONNECT_PATTERNS"

    async def test_identity_reaches_telemetry_for_three_lists(self, monkeypatch, probe_on, log_rec):
        # #1595 Phase 3 (2026-09-27): "remind me to hydrate" no longer names
        # REMINDER_PATTERNS (deleted, empty) — swapped for
        # "what's blocking the milestone?" / ANALYSIS_PATTERNS, keeping this
        # test's actual point (3 DISTINCT claiming lists thread through
        # telemetry) intact.
        _scripted_router(monkeypatch, operation="get_current_time")
        for message in (
            "I need help understanding something",
            "what's blocking the milestone?",
            "who are you?",
        ):
            intent, name = PreClassifier.pre_classify_with_pattern_list(message)
            task = maybe_schedule_preclaim_shadow(
                message,
                claimed_category=intent.category.value,
                claimed_action=intent.action,
                pattern_list=name,
                entry_surface="pre_classify",
            )
            await task
        seen = [f["pattern_list"] for _, f in log_rec.info_events]
        assert seen == ["DISCOVERY_PATTERNS", "ANALYSIS_PATTERNS", "IDENTITY_PATTERNS"]
        # And every line carries the layer statement (m-43).
        assert all("STATELESS" in f["layer_note"] for _, f in log_rec.info_events)


# ---------------------------------------------------------------------------
# Comparison semantics (alias-aware, m-44 incomparable buckets)
# ---------------------------------------------------------------------------


class TestCompareClaim:
    @pytest.fixture(scope="class")
    def grammar(self):
        return derive_routing_grammar()

    def _decision(self, outcome="operation", operation=None):
        return RoutingDecision(outcome=outcome, operation=operation, confidence=0.9)

    def test_exact_agreement(self, grammar):
        agreement, reason = compare_claim(
            "get_capabilities", self._decision(operation="get_capabilities"), grammar
        )
        assert (agreement, reason) == (True, None)

    def test_alias_agreement(self, grammar):
        # set_reminder IS create_reminder (the Phase-0 scoring correction) —
        # only meaningful if the alias map still says so; assert the premise.
        assert grammar.alias_to_canonical.get("set_reminder") == "create_reminder"
        agreement, reason = compare_claim(
            "create_reminder", self._decision(operation="set_reminder"), grammar
        )
        assert (agreement, reason) == (True, None)

    def test_disagreement(self, grammar):
        agreement, reason = compare_claim(
            "get_capabilities", self._decision(operation="get_current_time"), grammar
        )
        assert (agreement, reason) == (False, None)

    def test_router_none_against_concrete_claim_is_disagreement(self, grammar):
        agreement, reason = compare_claim("get_capabilities", self._decision("none"), grammar)
        assert (agreement, reason) == (False, None)

    def test_refused_and_error_are_incomparable(self, grammar):
        for outcome in ("refused", "error"):
            agreement, reason = compare_claim("get_capabilities", self._decision(outcome), grammar)
            assert agreement is None and reason == f"router_{outcome}"

    def test_out_of_grammar_claim_is_its_own_bucket(self, grammar):
        assert "not_a_real_action_xyz" not in grammar.names()
        agreement, reason = compare_claim(
            "not_a_real_action_xyz", self._decision(operation="get_capabilities"), grammar
        )
        assert agreement is None and reason == "claimed_action_outside_grammar"

    def test_no_claimed_action(self, grammar):
        agreement, reason = compare_claim(None, self._decision(operation="x"), grammar)
        assert agreement is None and reason == "no_claimed_action"


# ---------------------------------------------------------------------------
# Pin 5 — report helper output shape
# ---------------------------------------------------------------------------


def _event(event, pattern_list):
    return {"event": event, "pattern_list": pattern_list}


class TestReportHelper:
    def test_aggregate_shape_and_precision_math(self):
        events = [
            _event(AGREEMENT_EVENT, "DISCOVERY_PATTERNS"),
            _event(AGREEMENT_EVENT, "DISCOVERY_PATTERNS"),
            _event(DISAGREEMENT_EVENT, "TEMPORAL_PATTERNS"),
            _event(AGREEMENT_EVENT, "TEMPORAL_PATTERNS"),
            _event(INCOMPARABLE_EVENT, "GREETING_PATTERNS"),
            {"event": "unrelated_event", "pattern_list": "X"},  # ignored
        ]
        agg = aggregate_preclaim_events(events)
        per = agg["per_pattern_list"]
        assert per["DISCOVERY_PATTERNS"] == {
            "claims": 2,
            "agree": 2,
            "disagree": 0,
            "incomparable": 0,
            "comparable": 2,
            "precision": 1.0,
        }
        assert per["TEMPORAL_PATTERNS"]["precision"] == 0.5
        # m-44: only-incomparable is measured-at-nothing, never 1.0/0.0.
        assert per["GREETING_PATTERNS"]["precision"] is None
        assert agg["totals"]["claims"] == 5
        assert agg["totals"]["comparable"] == 4
        assert agg["totals"]["precision"] == 0.75

    def test_render_readout_vs_bar(self):
        agg = aggregate_preclaim_events(
            [
                _event(AGREEMENT_EVENT, "DISCOVERY_PATTERNS"),
                _event(DISAGREEMENT_EVENT, "TEMPORAL_PATTERNS"),
                _event(INCOMPARABLE_EVENT, "GREETING_PATTERNS"),
            ]
        )
        text = render_preclaim_report(agg, bar=1.0)
        assert "MEETS BAR" in text and "BELOW BAR" in text
        assert "NO COMPARABLE DATA" in text
        # Denominator discipline is stated on the artifact itself.
        assert "agree/(agree+disagree)" in text
        for name in ("DISCOVERY_PATTERNS", "TEMPORAL_PATTERNS", "GREETING_PATTERNS"):
            assert name in text

    def test_script_parses_json_and_console_lines(self):
        import importlib.util
        from pathlib import Path

        spec = importlib.util.spec_from_file_location(
            "preclaim_shadow_report",
            Path(__file__).resolve().parents[4] / "scripts" / "preclaim_shadow_report.py",
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        lines = [
            '{"event": "preclaim_shadow_agreement", "pattern_list": "DISCOVERY_PATTERNS"}',
            "2026-09-02 10:00:00 [info] preclaim_shadow_disagreement "
            "pattern_list=TEMPORAL_PATTERNS shadow_route=get_current_time",
            "2026-09-02 10:00:01 [info] some_other_event pattern_list=IGNORED",
        ]
        events = list(mod.parse_probe_events(lines))
        assert events == [
            {"event": AGREEMENT_EVENT, "pattern_list": "DISCOVERY_PATTERNS"},
            {"event": DISAGREEMENT_EVENT, "pattern_list": "TEMPORAL_PATTERNS"},
        ]
