"""#1595 Phase 1 — the constrained inversion router + shadow observer.

Covers the Phase-1 acceptance surface:
- grammar derivation TRACKS the live registry (a registry mutation changes the
  next derivation — the derive-at-call-time condition, PDR-006);
- alias collapse (aliases are input-side; the catalog carries canonical names
  only — Arch's material correction);
- structured-output enforcement: malformed output → ONE repair retry →
  REFUSED recorded honestly, never a guessed route; transport failure →
  ERROR recorded, never faked;
- flag OFF ⇒ NO shadow task is created (asserted on task creation, not just
  absence of effect);
- a shadow-task explosion cannot fail the turn (failure is logged, swallowed);
- scorer: per-category output shape + ERROR discipline on a poisoned row.

The no-execution IMPORT boundary lives in
tests/test_architecture_enforcement.py::TestInversionShadowNoExecutionBoundary.

All tests here are LLM-free (explosive/scripted fakes) except the one
@pytest.mark.llm smoke, which needs real keys.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from services.intent_service import inversion_shadow
from services.intent_service.inversion_router import (
    CLARIFY_ROUTE,
    NONE_ROUTE,
    RoutingDecision,
    build_routing_prompt,
    derive_routing_grammar,
    route,
)
from services.intent_service.workflow_dispatcher import (
    WORKFLOW_REGISTRY,
    WorkflowEntry,
    register_workflow,
)
from services.shared_types import EffectClass


class ScriptedLLM:
    """LLM double: returns queued replies; records every call."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []

    async def complete(self, **kwargs):
        self.calls.append(kwargs)
        if not self.replies:
            raise AssertionError("ScriptedLLM exhausted — unexpected extra call")
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply


class ExplosiveLLM:
    """No-execution guarantee double: ANY call is a test failure."""

    async def complete(self, **kwargs):  # pragma: no cover — reaching it IS the failure
        raise AssertionError("LLM was called on a path that must not call it")


# ---------------------------------------------------------------------------
# Grammar derivation
# ---------------------------------------------------------------------------


class TestGrammarDerivation:
    def test_grammar_collapses_aliases_to_canonical_operations(self):
        grammar = derive_routing_grammar()
        names = grammar.names()
        # canonical present, aliases absent from the catalog
        assert "create_reminder" in names
        assert "set_reminder" not in names
        assert "add_reminder" not in names
        # ...but aliases resolve input-side
        assert grammar.alias_to_canonical["set_reminder"] == "create_reminder"
        assert grammar.alias_to_canonical["add_reminder"] == "create_reminder"
        # registry-only canonicals (no rail key) are in the catalog — the
        # corpus asserts several of these as expected actions
        for op in ("get_identity", "manage_portfolio", "get_contextual_guidance"):
            assert op in names
        # catalog is a set of distinct operations, far smaller than the alias
        # key space, and duplicates-free
        assert len(names) == len(set(names))
        assert len(grammar.alias_to_canonical) > len(names)

    def test_create_reminder_stays_distinct_from_todo_reads(self):
        """entry_point collapse would merge WRITE create_reminder with the
        todo READ keys (shared delegation entry point); object-identity
        collapse must keep them distinct operations."""
        grammar = derive_routing_grammar()
        names = grammar.names()
        assert "create_reminder" in names
        assert "list_todos_query" in names
        assert grammar.alias_to_canonical["list_completed_todos"] == "list_todos_query"

    def test_grammar_tracks_a_registry_mutation(self):
        """The derive-from-registry-at-call-time condition (PDR-006 cond. 2):
        registering a new operation changes the NEXT derivation with no code
        change; removing it removes it. A hand-written list cannot pass this."""
        key = "test_inversion_grammar_probe_op"
        alias = "test_inversion_grammar_probe_alias"
        assert key not in derive_routing_grammar().names()

        async def _noop(session_id, user_id=None, context=None):  # pragma: no cover
            return None

        entry = WorkflowEntry(
            entry_point=_noop,
            effect=EffectClass.READ,
            description="grammar-tracking probe (#1595 test)",
            action_triggered=True,
        )
        try:
            register_workflow(key, entry)
            register_workflow(alias, entry)
            grammar = derive_routing_grammar()
            assert key in grammar.names()
            assert alias not in grammar.names()  # alias collapsed input-side
            assert grammar.alias_to_canonical[alias] == key
            # and the prompt catalog the model sees carries it too
            assert key in build_routing_prompt("hello", grammar)
        finally:
            WORKFLOW_REGISTRY.pop(key, None)
            WORKFLOW_REGISTRY.pop(alias, None)
        assert key not in derive_routing_grammar().names()

    def test_registry_descriptions_enrich_the_grammar(self):
        """#1595 Phase 1b (Family 1): ACTION_DESCRIPTIONS is the derivation
        SOURCE for registry-only canonicals — the enriched text must appear
        verbatim in the grammar and in the prompt catalog the model sees.
        The two Family-1 targets carry the specific claims the shadow run
        showed the router was never told."""
        grammar = derive_routing_grammar()
        by_name = {op.name: op for op in grammar.operations}
        # manage_portfolio must say it covers archive/restore/list of projects
        mp = by_name["manage_portfolio"].description
        for word in ("archive", "restore", "list"):
            assert word in mp.lower(), f"manage_portfolio description lacks {word!r}"
        # get_contextual_guidance must say it's the how-do-I / connect-my-
        # integrations destination
        gcg = by_name["get_contextual_guidance"].description
        assert "connect" in gcg.lower()
        assert "how-do-i" in gcg.lower().replace(" ", "-") or "how-do-I" in gcg
        # the enrichment flows into the prompt catalog
        prompt = build_routing_prompt("hello", grammar)
        assert mp in prompt
        assert gcg in prompt

    def test_all_registry_only_operations_are_described(self):
        """Coverage ratchet: no registry-derived operation still carries the
        uninformative '<category> action (<disposition>-handled)' fallback —
        a new ACTION_REGISTRY entry without an ACTION_DESCRIPTIONS line fails
        here rather than silently shipping an undescribed catalog line."""
        grammar = derive_routing_grammar()
        undescribed = [
            op.name
            for op in grammar.operations
            if op.source == "action_registry" and "-handled)" in op.description
        ]
        assert undescribed == [], (
            f"registry-only operations lacking an ACTION_DESCRIPTIONS entry: "
            f"{undescribed} — add a one-liner grounded in the handler's own "
            "code (never an invented capability claim)"
        )

    def test_registry_entry_without_description_gets_honest_fallback(self):
        """An ACTION_REGISTRY entry with NO ACTION_DESCRIPTIONS line derives
        the honest disposition fallback — the catalog never invents."""
        from services.intent_service.action_registry import (
            ACTION_REGISTRY,
            ActionDisposition,
        )

        key = ("QUERY", "test_inversion_undescribed_probe_op")
        assert key not in ACTION_REGISTRY
        try:
            ACTION_REGISTRY[key] = ActionDisposition.FLOOR
            grammar = derive_routing_grammar()
            by_name = {op.name: op for op in grammar.operations}
            probe = by_name["test_inversion_undescribed_probe_op"]
            assert probe.description == "query action (floor-handled)"
        finally:
            ACTION_REGISTRY.pop(key, None)
        assert "test_inversion_undescribed_probe_op" not in derive_routing_grammar().names()

    def test_action_descriptions_keys_are_registry_keys(self):
        """No orphan metadata: every ACTION_DESCRIPTIONS key must be a live
        ACTION_REGISTRY key (a description for a nonexistent operation is
        drift waiting to mislead the next derivation change)."""
        from services.intent_service.action_registry import (
            ACTION_DESCRIPTIONS,
            ACTION_REGISTRY,
        )

        orphans = [k for k in ACTION_DESCRIPTIONS if k not in ACTION_REGISTRY]
        assert orphans == []

    def test_offer_only_entries_are_not_operations(self):
        """action_triggered=False entries (confirm_pending_action &c.) are
        offer-seam plumbing, not selectable operations."""
        names = derive_routing_grammar().names()
        for offer_only in ("confirm_pending_action", "verify_inference", "meeting"):
            assert offer_only not in names


# ---------------------------------------------------------------------------
# Structured-output enforcement (route)
# ---------------------------------------------------------------------------


class TestRouteEnforcement:
    async def test_valid_first_reply_routes_in_one_call(self):
        llm = ScriptedLLM(
            [
                '{"operation": "create_reminder", "args": {"when": "9am"}, '
                '"confidence": 0.92, "rationale": "reminder request"}'
            ]
        )
        d = await route("remind me at 9am", llm_service=llm)
        assert d.outcome == "operation"
        assert d.operation == "create_reminder"
        assert d.args == {"when": "9am"}
        assert d.confidence == 0.92
        assert d.llm_calls == 1
        assert d.repair_attempted is False

    async def test_alias_emission_is_rejected_then_repaired(self):
        """The catalog is canonical-only: an alias emission is INVALID output
        (aliases resolve after selection on the rail, not in the router), and
        the repair retry carries the validation error."""
        llm = ScriptedLLM(
            [
                '{"operation": "set_reminder", "confidence": 0.9, "rationale": "x"}',
                '{"operation": "create_reminder", "confidence": 0.9, "rationale": "x"}',
            ]
        )
        d = await route("remind me at 9am", llm_service=llm)
        assert d.outcome == "operation"
        assert d.operation == "create_reminder"
        assert d.llm_calls == 2
        assert d.repair_attempted is True
        assert "set_reminder" in llm.calls[1]["prompt"]  # error fed back

    async def test_malformed_twice_is_refused_never_guessed(self):
        llm = ScriptedLLM(["I think you want a reminder!", "still not json"])
        d = await route("remind me at 9am", llm_service=llm)
        assert d.outcome == "refused"
        assert d.operation is None  # NEVER a guessed route
        assert d.llm_calls == 2
        assert d.repair_attempted is True
        assert d.error

    async def test_llm_failure_is_error_recorded_not_faked(self):
        llm = ScriptedLLM([RuntimeError("connection down")])
        d = await route("what time is it?", llm_service=llm)
        assert d.outcome == "error"
        assert d.operation is None
        assert "connection down" in (d.error or "")

    async def test_none_and_clarify_are_valid_routes(self):
        llm = ScriptedLLM(
            [f'{{"operation": "{NONE_ROUTE}", "confidence": 0.8, "rationale": "chat"}}']
        )
        d = await route("nice weather today", llm_service=llm)
        assert d.outcome == "none" and d.operation is None
        llm = ScriptedLLM(
            [f'{{"operation": "{CLARIFY_ROUTE}", "confidence": 0.5, "rationale": "??"}}']
        )
        d = await route("do the thing", llm_service=llm)
        assert d.outcome == "clarify" and d.operation is None

    # -------------------------------------------------------------------
    # #1595 unit 4b — the additive "plan" outcome
    # -------------------------------------------------------------------

    async def test_valid_plan_reply_is_accepted(self):
        """A genuine two-op plan parses in one call, elements in order,
        operation/args/confidence/rationale left at their single-op
        defaults (never both populated)."""
        llm = ScriptedLLM(
            [
                '{"outcome": "plan", "operations": ['
                '{"operation": "list_todos_query", "args": {}, '
                '"confidence": 0.9, "rationale": "read the list"}, '
                '{"operation": "delete_todo", "args": {"target": "hydrate"}, '
                '"confidence": 0.85, "rationale": "remove one"}]}'
            ]
        )
        d = await route("what are my todos and delete my hydrate reminder", llm_service=llm)
        assert d.outcome == "plan"
        assert d.operation is None
        assert d.args == {}
        assert [op["operation"] for op in d.operations] == [
            "list_todos_query",
            "delete_todo",
        ]
        assert d.operations[1]["args"] == {"target": "hydrate"}
        assert d.operations[0]["confidence"] == 0.9
        assert d.llm_calls == 1
        assert d.repair_attempted is False
        assert d.route_label == "PLAN[list_todos_query→delete_todo]"

    async def test_plan_with_nested_args_parses_past_the_old_one_level_regex(self):
        """Each plan element's own 'args' object is a THIRD brace level
        (plan → operations[i] → args) — the pre-4b single-level regex could
        not represent this shape at all; this is the property that made the
        balanced-brace scanner necessary, not just tidier."""
        llm = ScriptedLLM(
            [
                '{"outcome": "plan", "operations": ['
                '{"operation": "list_todos_query", '
                '"args": {"owner": "me", "nested": {"deep": "ok"}}, '
                '"confidence": 0.9, "rationale": "x"}, '
                '{"operation": "delete_todo", "args": {}, '
                '"confidence": 0.9, "rationale": "y"}]}'
            ]
        )
        d = await route("two things", llm_service=llm)
        assert d.outcome == "plan"
        assert d.operations[0]["args"]["nested"] == {"deep": "ok"}

    async def test_plan_of_fewer_than_two_elements_is_refused_never_partial(self):
        llm = ScriptedLLM(
            [
                '{"outcome": "plan", "operations": '
                '[{"operation": "list_todos_query", "confidence": 0.9, "rationale": "x"}]}',
                '{"outcome": "plan", "operations": '
                '[{"operation": "list_todos_query", "confidence": 0.9, "rationale": "x"}]}',
            ]
        )
        d = await route("one thing", llm_service=llm)
        assert d.outcome == "refused"
        assert d.operations == []
        assert d.llm_calls == 2
        assert d.repair_attempted is True

    async def test_plan_naming_an_invented_operation_is_refused_never_partial(self):
        """One bad element invalidates the WHOLE plan — never a partial
        accept of the valid elements."""
        llm = ScriptedLLM(
            [
                '{"outcome": "plan", "operations": ['
                '{"operation": "list_todos_query", "confidence": 0.9, "rationale": "x"}, '
                '{"operation": "made_up_operation_xyz", "confidence": 0.9, "rationale": "y"}]}',
                '{"outcome": "plan", "operations": ['
                '{"operation": "list_todos_query", "confidence": 0.9, "rationale": "x"}, '
                '{"operation": "made_up_operation_xyz", "confidence": 0.9, "rationale": "y"}]}',
            ]
        )
        d = await route("two things", llm_service=llm)
        assert d.outcome == "refused"
        assert d.operations == []
        assert "made_up_operation_xyz" in (d.error or "")

    async def test_plan_with_a_malformed_element_is_refused_never_partial(self):
        """A structurally-bad element (missing 'operation') invalidates the
        whole plan, same as an invented name does."""
        llm = ScriptedLLM(
            [
                '{"outcome": "plan", "operations": ['
                '{"operation": "list_todos_query", "confidence": 0.9, "rationale": "x"}, '
                '{"confidence": 0.9, "rationale": "no operation key"}]}',
                '{"outcome": "plan", "operations": ['
                '{"operation": "list_todos_query", "confidence": 0.9, "rationale": "x"}, '
                '{"confidence": 0.9, "rationale": "no operation key"}]}',
            ]
        )
        d = await route("two things", llm_service=llm)
        assert d.outcome == "refused"
        assert "operations[1]" in (d.error or "")

    async def test_plan_of_identical_operations_collapses_and_is_refused(self):
        """A plan whose elements are all the same operation is not a plan —
        it must name at least 2 DISTINCT operations."""
        llm = ScriptedLLM(
            [
                '{"outcome": "plan", "operations": ['
                '{"operation": "delete_todo", "args": {"target": "a"}, '
                '"confidence": 0.9, "rationale": "x"}, '
                '{"operation": "delete_todo", "args": {"target": "b"}, '
                '"confidence": 0.9, "rationale": "y"}]}',
                '{"outcome": "plan", "operations": ['
                '{"operation": "delete_todo", "args": {"target": "a"}, '
                '"confidence": 0.9, "rationale": "x"}, '
                '{"operation": "delete_todo", "args": {"target": "b"}, '
                '"confidence": 0.9, "rationale": "y"}]}',
            ]
        )
        d = await route("delete two things", llm_service=llm)
        assert d.outcome == "refused"
        assert "DISTINCT" in (d.error or "")

    async def test_plan_element_naming_none_or_clarify_is_refused(self):
        """NONE/CLARIFY are sentinels, not operations — they cannot appear
        as a plan element even though the grammar's is_valid_route accepts
        them for the single-op case."""
        llm = ScriptedLLM(
            [
                '{"outcome": "plan", "operations": ['
                '{"operation": "list_todos_query", "confidence": 0.9, "rationale": "x"}, '
                f'{{"operation": "{NONE_ROUTE}", "confidence": 0.9, "rationale": "y"}}]}}',
                '{"outcome": "plan", "operations": ['
                '{"operation": "list_todos_query", "confidence": 0.9, "rationale": "x"}, '
                f'{{"operation": "{NONE_ROUTE}", "confidence": 0.9, "rationale": "y"}}]}}',
            ]
        )
        d = await route("todos and something vague", llm_service=llm)
        assert d.outcome == "refused"
        assert NONE_ROUTE in (d.error or "")

    async def test_first_attempt_malformed_plan_is_repaired_and_accepted(self):
        """The repair path for a plan: attempt 1 is malformed (a single
        stray element), attempt 2 is a valid 2-op plan — the repaired PLAN
        is accepted, not collapsed to a single op."""
        llm = ScriptedLLM(
            [
                "not json at all",
                '{"outcome": "plan", "operations": ['
                '{"operation": "list_todos_query", "confidence": 0.9, "rationale": "x"}, '
                '{"operation": "delete_todo", "confidence": 0.9, "rationale": "y"}]}',
            ]
        )
        d = await route("what are my todos and delete my hydrate reminder", llm_service=llm)
        assert d.outcome == "plan"
        assert [op["operation"] for op in d.operations] == [
            "list_todos_query",
            "delete_todo",
        ]
        assert d.llm_calls == 2
        assert d.repair_attempted is True
        # The shape-aware repair prompt restates BOTH shapes.
        repair_prompt = llm.calls[1]["prompt"]
        assert '"operation": "<name>"' in repair_prompt
        assert '"outcome": "plan"' in repair_prompt

    async def test_repaired_single_object_still_accepted(self):
        """The other half of shape-awareness: attempt 1 malformed, attempt 2
        a valid SINGLE object — unaffected by the plan addition."""
        llm = ScriptedLLM(
            [
                "garbage",
                '{"operation": "create_reminder", "confidence": 0.9, "rationale": "x"}',
            ]
        )
        d = await route("remind me at 9am", llm_service=llm)
        assert d.outcome == "operation"
        assert d.operation == "create_reminder"
        assert d.operations == []
        assert d.llm_calls == 2
        assert d.repair_attempted is True

    def test_plan_rule_in_prompt_is_the_exception_not_the_default(self):
        """The single-op shape stays first/default in both the system
        prompt and the catalog header; the plan shape is introduced as the
        exception clause — matching Arch's explicit ruling wording."""
        grammar = derive_routing_grammar()
        prompt = build_routing_prompt("hello", grammar)
        assert "choose exactly one" in prompt.lower()
        assert "plan form" in prompt.lower()
        # The catalog header must NOT re-open the choice ("or, for a multi-op
        # request...") — measured 2026-09-28: a plural framing anywhere before
        # the catalog primed step-decomposition of single asks ("delete my
        # reminders" → a listing "first", 6/6 vs 0/6 with the singular framing).

        from services.intent_service.inversion_router import _SYSTEM_PROMPT

        assert "single operation" in _SYSTEM_PROMPT
        assert "which operation(s)" not in _SYSTEM_PROMPT

        # The default single-object JSON form is stated before the plan form.
        single_idx = _SYSTEM_PROMPT.index('{"operation": "<name>"')
        plan_idx = _SYSTEM_PROMPT.index('"outcome": "plan"')
        assert single_idx < plan_idx

    async def test_router_uses_inversion_routing_task_type(self):
        """Model selection rides the app config path (light tier / Haiku)."""
        llm = ScriptedLLM(['{"operation": "NONE", "confidence": 1, "rationale": "x"}'])
        await route("hi", llm_service=llm)
        assert llm.calls[0]["task_type"] == "inversion_routing"
        assert llm.calls[0]["response_format"] == {"type": "json_object"}

    @pytest.mark.llm
    async def test_real_call_routes_within_grammar(self):
        """One real Haiku-class call: whatever it answers must be a valid
        grammar route (the enforcement property, live)."""
        from services.llm.clients import LLMClient

        grammar = derive_routing_grammar()
        d = await route("what time is it?", llm_service=LLMClient(), grammar=grammar)
        assert d.outcome in ("operation", "none", "clarify")
        if d.outcome == "operation":
            assert d.operation in grammar.names()


# ---------------------------------------------------------------------------
# Shadow scheduling (flag gate + turn safety)
# ---------------------------------------------------------------------------


class TestShadowScheduling:
    async def test_flag_off_creates_no_task(self, monkeypatch):
        monkeypatch.delenv("PIPER_INVERSION_SHADOW", raising=False)
        loop_touches = []

        def _fail_if_touched():
            loop_touches.append("get_running_loop")
            raise AssertionError("flag-off path must never reach the event loop")

        monkeypatch.setattr(inversion_shadow.asyncio, "get_running_loop", _fail_if_touched)
        task = inversion_shadow.maybe_schedule_shadow_check(
            "hello", "conversation:greeting", llm_service=ExplosiveLLM()
        )
        assert task is None
        assert loop_touches == []  # no task CREATED, not merely no effect

    async def test_flag_on_creates_task_and_failure_cannot_fail_turn(self, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_SHADOW", "1")
        monkeypatch.setenv("PIPER_INVERSION_SHADOW_SAMPLE", "1.0")

        async def _exploding_route(*a, **k):
            raise RuntimeError("router exploded")

        monkeypatch.setattr("services.intent_service.inversion_router.route", _exploding_route)
        task = inversion_shadow.maybe_schedule_shadow_check(
            "hello", "conversation:greeting", session_id="s1", user_id="u1"
        )
        assert task is not None  # the flag-on path DID create a task
        result = await task  # the turn's await of this task must not raise
        assert result is None
        assert task.exception() is None

    async def test_sampled_out_creates_no_task(self, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_SHADOW", "1")
        monkeypatch.setenv("PIPER_INVERSION_SHADOW_SAMPLE", "0.0")
        task = inversion_shadow.maybe_schedule_shadow_check(
            "hello", "conversation:greeting", llm_service=ExplosiveLLM()
        )
        assert task is None

    async def test_shadow_logs_comparison_without_executing_anything(self, monkeypatch):
        """Flag on, scripted router: the task completes, logs, and returns
        None — there is no decision object for a caller to consume."""
        monkeypatch.setenv("PIPER_INVERSION_SHADOW", "1")
        monkeypatch.setenv("PIPER_INVERSION_SHADOW_SAMPLE", "1.0")
        events = []

        async def _scripted_route(utterance, snapshot=None, **kw):
            return RoutingDecision(outcome="operation", operation="create_reminder", confidence=0.9)

        monkeypatch.setattr("services.intent_service.inversion_router.route", _scripted_route)
        monkeypatch.setattr(
            inversion_shadow.logger,
            "info",
            lambda event, **fields: events.append((event, fields)),
        )
        task = inversion_shadow.maybe_schedule_shadow_check(
            "remind me at 9am",
            "execution:set_reminder",  # alias of create_reminder → agreement
            session_id="s1",
            user_id="u1",
        )
        assert (await task) is None
        assert [e for e, _ in events] == ["shadow_route_agreement"]
        fields = events[0][1]
        assert fields["shadow_operation"] == "create_reminder"
        assert fields["production_intent"] == "execution:set_reminder"
        assert fields["utterance_sha256"]

    async def test_disagreement_event_name(self, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_SHADOW", "1")
        monkeypatch.setenv("PIPER_INVERSION_SHADOW_SAMPLE", "1.0")
        events = []

        async def _scripted_route(utterance, snapshot=None, **kw):
            return RoutingDecision(outcome="operation", operation="list_issues")

        monkeypatch.setattr("services.intent_service.inversion_router.route", _scripted_route)
        monkeypatch.setattr(
            inversion_shadow.logger,
            "info",
            lambda event, **fields: events.append(event),
        )
        task = inversion_shadow.maybe_schedule_shadow_check(
            "show my prs", "query:list_prs_query", session_id="s1"
        )
        await task
        assert events == ["shadow_route_disagreement"]


# ---------------------------------------------------------------------------
# Scorer (script) — output shape + ERROR discipline
# ---------------------------------------------------------------------------


def _load_scorer():
    root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(root / "scripts"))
    import inversion_phase1_shadow_score as scorer

    return scorer


class TestShadowScorer:
    async def test_poisoned_row_records_error_never_fakes(self):
        scorer = _load_scorer()
        rows = [
            {
                "phrase": "good row",
                "category": "QUERY",
                "expected": "action:list_issues_query",
                "source": "t",
            },
            {
                "phrase": "poisoned row",
                "category": "QUERY",
                "expected": "action:list_prs_query",
                "source": "t",
            },
            {"phrase": "review row", "category": "TRUST", "expected": "REVIEW", "source": "t"},
        ]

        async def router_fn(phrase):
            if phrase == "poisoned row":
                raise RuntimeError("boom")
            return RoutingDecision(outcome="operation", operation="list_issues")

        decisions = await scorer.route_all(rows, router_fn, progress=False)
        scored = scorer.score(rows, decisions)
        by_phrase = {rr["row"]["phrase"]: rr for rr in scored["rows"]}
        assert by_phrase["poisoned row"]["verdict"] == "ERROR"
        assert by_phrase["good row"]["verdict"] == "MATCH"  # alias-aware
        assert by_phrase["review row"]["verdict"] == "REVIEW"
        # per-category shape: stated denominators, REVIEW outside the score
        q = scored["per_cat"]["QUERY"]
        assert (q["n"], q["asserted"], q["match"], q["errors"]) == (2, 2, 1, 1)
        t = scored["per_cat"]["TRUST"]
        assert (t["asserted"], t["review"]) == (0, 1)

    async def test_category_expectation_scored_via_registry_category(self):
        scorer = _load_scorer()
        rows = [
            {
                "phrase": "who am I?",
                "category": "IDENTITY",
                "expected": "category:IDENTITY",
                "source": "t",
            },
        ]

        async def router_fn(phrase):
            return RoutingDecision(outcome="operation", operation="get_identity")

        decisions = await scorer.route_all(rows, router_fn, progress=False)
        scored = scorer.score(rows, decisions)
        assert scored["rows"][0]["verdict"] == "MATCH"

    async def test_refused_scores_as_mismatch_annotated(self):
        scorer = _load_scorer()
        rows = [
            {
                "phrase": "x",
                "category": "QUERY",
                "expected": "action:list_issues_query",
                "source": "t",
            },
        ]

        async def router_fn(phrase):
            return RoutingDecision(outcome="refused", error="bad json twice")

        scored = scorer.score(rows, await scorer.route_all(rows, router_fn, progress=False))
        rr = scored["rows"][0]
        assert rr["verdict"] == "MISMATCH" and rr["note"] == "REFUSED"
