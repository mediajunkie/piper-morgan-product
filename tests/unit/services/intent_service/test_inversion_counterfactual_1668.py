"""#1668 — the shadow observer's LEGACY-COUNTERFACTUAL mode.

Before this, a turn routed LIVE by the inversion that was also sampled by the
shadow got its utterance re-routed through the SAME constrained router: a
second LLM call whose finding was self-agreement, which is not signal. The
shadow is repurposed there — on an inversion-routed turn it computes what the
LEGACY chain would have done and logs the comparison, which during a flip wave
is exactly the question the wave is asking.

Pinned here:

1. BRANCHING — the mode is chosen from the turn's routing provenance, passed
   in explicitly; an inversion-routed turn takes the counterfactual, a
   legacy-routed turn takes the router shadow UNCHANGED (the router is
   explosive on the counterfactual path, so a re-route would be loud).
2. LEG HONESTY (m-43) — the log line names which legacy legs actually ran and
   which were deliberately skipped; the LLM leg fires only when both
   deterministic legs decline.
3. COST — the counterfactual makes at most ONE LLM call (0 when a
   deterministic leg claims), against the 1 the re-route always spent.
4. AGREEMENT — agree / disagree / incomparable each get their own event name,
   alias-resolved so ``set_reminder`` scores as ``create_reminder``.
5. SAFETY — a leg that explodes never fails the task; both flags off does zero
   work; provenance is one-shot so it cannot leak into a later turn.

LLM-free throughout: explosive router, scripted classifier doubles.
"""

from __future__ import annotations

import pytest

from services.intent_service import inversion_live, inversion_shadow
from services.intent_service.inversion_live import (
    LiveRouteProvenance,
    consume_live_route_provenance,
)
from services.shared_types import IntentCategory


# ---------------------------------------------------------------------------
# Doubles
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


class _ClassifierDouble:
    """Counts classify() calls; returns a scripted Intent (or raises)."""

    def __init__(self, action="list_issues", category=IntentCategory.QUERY, boom=None):
        self.calls = []
        self._action = action
        self._category = category
        self._boom = boom

    async def classify(self, message, **kwargs):
        self.calls.append((message, kwargs))
        if self._boom is not None:
            raise self._boom
        from services.domain.models import Intent

        return Intent(
            original_message=message,
            category=self._category,
            action=self._action,
            confidence=0.9,
        )


class _ExplosiveClassifier:
    def __getattr__(self, name):
        raise AssertionError(f"classifier touched ({name}) — no LLM leg allowed here")


@pytest.fixture
def log_rec(monkeypatch):
    rec = _RecordingLogger()
    monkeypatch.setattr(inversion_shadow, "logger", rec)
    return rec


@pytest.fixture
def shadow_on(monkeypatch):
    monkeypatch.setenv("PIPER_INVERSION_SHADOW", "1")
    monkeypatch.setenv("PIPER_INVERSION_SHADOW_SAMPLE", "1.0")


@pytest.fixture
def explosive_router(monkeypatch):
    """Any router call on the counterfactual path is the #1668 defect itself."""
    from services.intent_service import inversion_router as ir

    async def _boom(*a, **k):
        raise AssertionError(
            "inversion router re-routed an inversion-routed turn — #1668 regression"
        )

    monkeypatch.setattr(ir, "route", _boom)


def _live(**kw):
    base = dict(
        routed_live=True,
        operation="list_issues",
        canonical="list_issues",
        category="QUERY",
        live_match="group",
        confidence=0.93,
    )
    base.update(kw)
    return LiveRouteProvenance(**base)


# ---------------------------------------------------------------------------
# 1. Mode branching
# ---------------------------------------------------------------------------


class TestModeBranching:
    async def test_inversion_routed_turn_runs_counterfactual_not_reroute(
        self, shadow_on, log_rec, explosive_router
    ):
        task = inversion_shadow.maybe_schedule_shadow_check(
            "show my issues",
            "query:list_issues",
            session_id="s1",
            user_id="u1",
            live_route=_live(),
            classifier=_ExplosiveClassifier(),
        )
        assert task is not None
        assert (await task) is None
        assert log_rec.events == ["shadow_legacy_counterfactual_agreement"]
        # Distinct event family — the router-shadow names must NOT appear.
        assert not any(e.startswith("shadow_route_") for e in log_rec.events)
        assert log_rec.error_events == []

    async def test_legacy_routed_turn_keeps_router_shadow_unchanged(
        self, shadow_on, log_rec, monkeypatch
    ):
        """routed_live False ⇒ the original path, router call and all."""
        from services.intent_service.inversion_router import RoutingDecision

        async def _scripted(utterance, snapshot=None, **kw):
            return RoutingDecision(
                outcome="operation", operation="create_reminder", confidence=0.9
            )

        monkeypatch.setattr(
            "services.intent_service.inversion_router.route", _scripted
        )
        task = inversion_shadow.maybe_schedule_shadow_check(
            "remind me at 9am",
            "execution:set_reminder",
            session_id="s1",
            live_route=LiveRouteProvenance(routed_live=False, reason="sub_threshold"),
        )
        await task
        assert log_rec.events == ["shadow_route_agreement"]

    async def test_no_provenance_at_all_keeps_router_shadow(
        self, shadow_on, log_rec, monkeypatch
    ):
        """The pre-#1668 call shape (no live_route kwarg) is unchanged."""
        from services.intent_service.inversion_router import RoutingDecision

        async def _scripted(utterance, snapshot=None, **kw):
            return RoutingDecision(outcome="operation", operation="list_issues")

        monkeypatch.setattr(
            "services.intent_service.inversion_router.route", _scripted
        )
        task = inversion_shadow.maybe_schedule_shadow_check(
            "show my prs", "query:list_prs_query", session_id="s1"
        )
        await task
        assert log_rec.events == ["shadow_route_disagreement"]

    async def test_both_flags_off_does_zero_work(self, monkeypatch, log_rec):
        monkeypatch.delenv("PIPER_INVERSION_SHADOW", raising=False)

        def _fail():
            raise AssertionError("flag-off path must never reach the event loop")

        monkeypatch.setattr(inversion_shadow.asyncio, "get_running_loop", _fail)
        task = inversion_shadow.maybe_schedule_shadow_check(
            "show my issues",
            "query:list_issues",
            live_route=_live(),
            classifier=_ExplosiveClassifier(),
        )
        assert task is None
        assert log_rec.info_events == [] and log_rec.error_events == []


# ---------------------------------------------------------------------------
# 2. Leg honesty (m-43) + 3. cost
# ---------------------------------------------------------------------------


class TestLegsAndCost:
    async def test_deterministic_claim_spends_no_llm_call(
        self, shadow_on, log_rec, explosive_router
    ):
        """A turn the deterministic surface claims: zero LLM calls, and the
        line says which leg decided it."""
        classifier = _ClassifierDouble()
        task = inversion_shadow.maybe_schedule_shadow_check(
            "show my issues",
            "query:list_issues",
            live_route=_live(),
            classifier=classifier,
        )
        await task
        _, fields = log_rec.info_events[0]
        assert fields["legacy_llm_calls"] == 0
        assert classifier.calls == []  # the LLM leg never ran
        assert fields["legacy_decided_by"] in ("multi_intent_rules", "pre_classifier")
        assert "llm_classifier" not in fields["legacy_legs_run"]

    async def test_llm_leg_runs_only_when_deterministic_legs_decline(
        self, shadow_on, log_rec, explosive_router
    ):
        classifier = _ClassifierDouble(action="list_issues")
        task = inversion_shadow.maybe_schedule_shadow_check(
            "zzq unclaimable phrase for every deterministic surface",
            "query:list_issues",
            live_route=_live(),
            classifier=classifier,
        )
        await task
        _, fields = log_rec.info_events[0]
        assert fields["legacy_legs_run"] == [
            "multi_intent_rules",
            "pre_classifier",
            "llm_classifier",
        ]
        assert fields["legacy_decided_by"] == "llm_classifier"
        # EXACTLY one call, and it is unscoped + uncached (the layer claim).
        assert len(classifier.calls) == 1
        assert fields["legacy_llm_calls"] == 1
        _msg, kwargs = classifier.calls[0]
        assert kwargs == {"use_cache": False}

    async def test_line_names_the_layer_it_measured(
        self, shadow_on, log_rec, explosive_router
    ):
        task = inversion_shadow.maybe_schedule_shadow_check(
            "show my issues",
            "query:list_issues",
            live_route=_live(),
            classifier=_ClassifierDouble(),
        )
        await task
        _, fields = log_rec.info_events[0]
        assert fields["mode"] == "legacy_counterfactual"
        assert "UNSCOPED, UNCACHED, SINGLE-INTENT" in fields["layer_note"]
        # The skipped legs are NAMED, not implied by absence.
        assert "b3_referent_resolution" in fields["legacy_legs_not_run"]
        assert "classifier_cache" in fields["legacy_legs_not_run"]
        assert fields["legacy_legs_run"]  # and what DID run is on the line too

    async def test_never_more_llm_calls_than_the_reroute_it_replaced(
        self, shadow_on, log_rec, explosive_router
    ):
        """The cost pin, stated as a test: whichever legs run, the ceiling is
        1 — the single router call this mode replaced."""
        for utterance in (
            "show my issues",
            "hi Piper",
            "zzq unclaimable phrase for every deterministic surface",
        ):
            log_rec.info_events.clear()
            classifier = _ClassifierDouble()
            task = inversion_shadow.maybe_schedule_shadow_check(
                utterance,
                "query:list_issues",
                live_route=_live(),
                classifier=classifier,
            )
            await task
            _, fields = log_rec.info_events[0]
            assert fields["legacy_llm_calls"] <= 1
            assert len(classifier.calls) <= 1


# ---------------------------------------------------------------------------
# 4. Agreement scoring
# ---------------------------------------------------------------------------


class TestAgreementScoring:
    async def test_disagreement_is_its_own_event(
        self, shadow_on, log_rec, explosive_router
    ):
        classifier = _ClassifierDouble(action="search_documents")
        task = inversion_shadow.maybe_schedule_shadow_check(
            "zzq unclaimable phrase for every deterministic surface",
            "query:list_issues",
            live_route=_live(operation="list_issues", canonical="list_issues"),
            classifier=classifier,
        )
        await task
        event, fields = log_rec.info_events[0]
        assert event == "shadow_legacy_counterfactual_disagreement"
        assert fields["agreement"] is False
        assert fields["live_route"] == "list_issues"
        assert fields["legacy_action"] == "search_documents"

    async def test_alias_resolution_scores_as_agreement(
        self, shadow_on, log_rec, explosive_router
    ):
        """set_reminder IS create_reminder — exact-name comparison would
        under-credit (the Phase-0 scoring correction)."""
        from services.intent_service.inversion_router import derive_routing_grammar

        canon = derive_routing_grammar().alias_to_canonical
        alias = next(
            (a for a, c in canon.items() if a != c and c and a),
            None,
        )
        if alias is None:
            pytest.skip("no alias in the derived grammar to exercise")
        classifier = _ClassifierDouble(action=alias)
        task = inversion_shadow.maybe_schedule_shadow_check(
            "zzq unclaimable phrase for every deterministic surface",
            "query:x",
            live_route=_live(operation=canon[alias], canonical=canon[alias]),
            classifier=classifier,
        )
        await task
        event, fields = log_rec.info_events[0]
        assert event == "shadow_legacy_counterfactual_agreement"
        assert fields["agreement"] is True

    async def test_no_legacy_answer_is_incomparable_not_disagreement(
        self, shadow_on, log_rec, explosive_router
    ):
        """No classifier available and no deterministic claim ⇒ we do not
        KNOW what legacy would have done. That is incomparable, and it must
        not be scored as a disagreement (m-44: absence is not a measurement)."""
        task = inversion_shadow.maybe_schedule_shadow_check(
            "zzq unclaimable phrase for every deterministic surface",
            "query:list_issues",
            live_route=_live(),
            classifier=None,
        )
        await task
        event, fields = log_rec.info_events[0]
        assert event == "shadow_legacy_counterfactual_incomparable"
        assert fields["agreement"] is None
        assert fields["legacy_llm_calls"] == 0


# ---------------------------------------------------------------------------
# 5. Safety
# ---------------------------------------------------------------------------


class TestCounterfactualSafety:
    async def test_exploding_llm_leg_cannot_fail_the_task(
        self, shadow_on, log_rec, explosive_router
    ):
        classifier = _ClassifierDouble(boom=RuntimeError("classifier exploded"))
        task = inversion_shadow.maybe_schedule_shadow_check(
            "zzq unclaimable phrase for every deterministic surface",
            "query:list_issues",
            live_route=_live(),
            classifier=classifier,
        )
        assert (await task) is None
        assert task.exception() is None
        event, fields = log_rec.info_events[0]
        assert event == "shadow_legacy_counterfactual_incomparable"
        # The failure is VISIBLE on the line, not swallowed into a clean-looking
        # "incomparable" (m-44), and the call it may have spent is still counted.
        assert "classifier exploded" in fields["legacy_leg_errors"]["llm_classifier"]
        assert fields["legacy_llm_calls"] == 1

    async def test_exploding_deterministic_leg_cannot_fail_the_task(
        self, shadow_on, log_rec, explosive_router, monkeypatch
    ):
        from services.intent_service.pre_classifier import PreClassifier

        def _boom(message):
            raise RuntimeError("pre-classifier exploded")

        monkeypatch.setattr(
            PreClassifier, "detect_multiple_intents", staticmethod(_boom)
        )
        monkeypatch.setattr(PreClassifier, "pre_classify", staticmethod(_boom))
        task = inversion_shadow.maybe_schedule_shadow_check(
            "show my issues",
            "query:list_issues",
            live_route=_live(),
            classifier=None,
        )
        assert (await task) is None
        assert task.exception() is None
        _, fields = log_rec.info_events[0]
        assert set(fields["legacy_leg_errors"]) == {
            "multi_intent_rules",
            "pre_classifier",
        }

    async def test_sampled_out_creates_no_counterfactual_task(
        self, monkeypatch, log_rec
    ):
        monkeypatch.setenv("PIPER_INVERSION_SHADOW", "1")
        monkeypatch.setenv("PIPER_INVERSION_SHADOW_SAMPLE", "0.0")
        task = inversion_shadow.maybe_schedule_shadow_check(
            "show my issues",
            "query:list_issues",
            live_route=_live(),
            classifier=_ExplosiveClassifier(),
        )
        assert task is None


# ---------------------------------------------------------------------------
# Provenance threading (the consult publishes; nothing re-derives)
# ---------------------------------------------------------------------------


class TestRoutingProvenance:
    def test_absent_by_default(self):
        inversion_live._LIVE_ROUTE.set(None)
        assert consume_live_route_provenance() is None

    def test_consume_is_one_shot(self):
        inversion_live._LIVE_ROUTE.set(_live())
        first = consume_live_route_provenance()
        assert first is not None and first.routed_live is True
        assert consume_live_route_provenance() is None

    async def test_default_empty_consult_clears_stale_provenance(self, monkeypatch):
        """A turn that never reaches a routing decision must not inherit the
        previous turn's record when both share one Task."""
        monkeypatch.delenv("PIPER_INVERSION_LIVE_CATEGORIES", raising=False)
        inversion_live._LIVE_ROUTE.set(_live())
        out = await inversion_live.consult_inversion_live(
            "anything", session_id="s", user_id="u", intent_service=object()
        )
        assert out is None
        assert consume_live_route_provenance() is None

    async def test_dispatching_consult_publishes_routed_live(self, monkeypatch):
        """The record comes from the consult's OWN decision."""
        from services.intent_service.inversion_router import RoutingDecision
        from services.intent_service.workflow_dispatcher import get_action_workflows

        op = next(
            (
                name
                for name, entry in get_action_workflows().items()
                if entry.flip_group
            ),
            None,
        )
        if op is None:
            pytest.skip("no flip-grouped rail operation to exercise")
        group = get_action_workflows()[op].flip_group
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", group)

        async def _snapshot(*a, **k):
            from services.intent_service.session_snapshot import SessionSnapshot

            return SessionSnapshot()

        monkeypatch.setattr(
            "services.intent_service.snapshot_assembly.assemble_session_snapshot",
            _snapshot,
        )

        async def _route(*a, **k):
            return RoutingDecision(outcome="operation", operation=op, confidence=0.99)

        monkeypatch.setattr("services.intent_service.inversion_router.route", _route)
        intent = await inversion_live.consult_inversion_live(
            "does not matter",
            session_id="s",
            user_id="u",
            intent_service=object(),
        )
        assert intent is not None and intent.action == op
        record = consume_live_route_provenance()
        assert record is not None
        assert record.routed_live is True
        assert record.operation == op
        assert record.live_match == "group"
        assert record.confidence == 0.99

    async def test_fall_through_consult_publishes_not_routed_live(self, monkeypatch):
        from services.intent_service.inversion_router import RoutingDecision

        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")

        async def _snapshot(*a, **k):
            from services.intent_service.session_snapshot import SessionSnapshot

            return SessionSnapshot()

        monkeypatch.setattr(
            "services.intent_service.snapshot_assembly.assemble_session_snapshot",
            _snapshot,
        )

        async def _route(*a, **k):
            return RoutingDecision(outcome="none")

        monkeypatch.setattr("services.intent_service.inversion_router.route", _route)
        intent = await inversion_live.consult_inversion_live(
            "does not matter",
            session_id="s",
            user_id="u",
            intent_service=object(),
        )
        assert intent is None
        record = consume_live_route_provenance()
        assert record is not None
        assert record.routed_live is False
        assert record.reason == "router_none"
