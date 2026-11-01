"""#2149 build step 2: the two-stage router behind PIPER_INVERSION_TWO_STAGE (default OFF).

Flag off: ``route()`` is the flat one-call path, byte-identical prompt and system.
Flag on: stage 1 picks a RouteGroup (or NONE / CLARIFY / a plan), stage 2 picks an op
inside that group (or CLARIFY / OTHER_GROUP). Code never re-routes OTHER_GROUP.

All tests are LLM-free: a fake ``llm_service`` records every ``complete()`` call and
returns scripted JSON.
"""

from __future__ import annotations

import json

import pytest

from services.intent_service.inversion_router import (
    _STAGE1_SYSTEM_PROMPT,
    _STAGE2_SYSTEM_PROMPT,
    _SYSTEM_PROMPT,
    CLARIFY_ROUTE,
    NONE_ROUTE,
    OTHER_GROUP_ROUTE,
    SessionSnapshot,
    build_routing_prompt,
    build_stage1_prompt,
    build_stage2_prompt,
    derive_routing_grammar,
    route,
    two_stage_enabled,
)
from services.shared_types import ROUTE_GROUP_LINES, RouteGroup
from tests.test_architecture_enforcement import TestRouteGroupRatchet2149

EXPECTED = TestRouteGroupRatchet2149.EXPECTED
FLAG = "PIPER_INVERSION_TWO_STAGE"


class FakeLLM:
    """Records every complete() call; returns the queued replies in order."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []

    async def complete(self, **kwargs):
        self.calls.append(kwargs)
        if not self.replies:
            raise AssertionError("FakeLLM exhausted: unexpected extra call")
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply


def j(**kw) -> str:
    return json.dumps(kw)


def op_reply(name, **args) -> str:
    return j(operation=name, args=args, confidence=0.9, rationale="r")


@pytest.fixture(scope="module")
def grammar():
    return derive_routing_grammar()


@pytest.fixture
def two_stage(monkeypatch):
    monkeypatch.setenv(FLAG, "1")


@pytest.fixture(autouse=True)
def _flag_unset_by_default(monkeypatch):
    monkeypatch.delenv(FLAG, raising=False)


class TestFlag:
    @pytest.mark.parametrize("value", ["1", "true", "TRUE", " on ", "yes"])
    def test_truthy_values_enable(self, monkeypatch, value):
        monkeypatch.setenv(FLAG, value)
        assert two_stage_enabled() is True

    @pytest.mark.parametrize("value", ["", "0", "false", "off", "no", "2"])
    def test_everything_else_is_off(self, monkeypatch, value):
        monkeypatch.setenv(FLAG, value)
        assert two_stage_enabled() is False

    def test_default_is_off(self):
        assert two_stage_enabled() is False

    def test_read_at_call_time(self, monkeypatch):
        assert two_stage_enabled() is False
        monkeypatch.setenv(FLAG, "1")
        assert two_stage_enabled() is True


class TestFlagOffIsFlat:
    @pytest.mark.asyncio
    async def test_one_call_with_byte_identical_prompt_and_system(self, grammar):
        snap = SessionSnapshot(pending_offer_summary="a pending offer", entity_names=["Atlas"])
        llm = FakeLLM([op_reply("list_issues")])
        d = await route("show my issues", snap, llm_service=llm, grammar=grammar, user_id=None)
        assert len(llm.calls) == 1
        assert llm.calls[0]["prompt"] == build_routing_prompt("show my issues", grammar, snap)
        assert llm.calls[0]["system"] == _SYSTEM_PROMPT
        assert llm.calls[0]["response_format"] == {"type": "json_object"}
        assert d.outcome == "operation" and d.operation == "list_issues"
        assert d.llm_calls == 1

    @pytest.mark.asyncio
    async def test_new_fields_stay_none(self, grammar):
        llm = FakeLLM([op_reply("list_issues")])
        d = await route("show my issues", None, llm_service=llm, grammar=grammar, user_id=None)
        assert d.route_group is None and d.stage_metrics is None

    @pytest.mark.asyncio
    async def test_repair_prompt_unchanged_when_off(self, grammar):
        llm = FakeLLM(["not json", op_reply("list_issues")])
        d = await route("x", None, llm_service=llm, grammar=grammar, user_id=None)
        assert len(llm.calls) == 2 and d.llm_calls == 2 and d.repair_attempted
        base = build_routing_prompt("x", grammar, None)
        assert llm.calls[1]["prompt"].startswith(base + "\n\nYour previous reply was invalid: ")
        assert llm.calls[1]["system"] == _SYSTEM_PROMPT


class TestStage1Prompt:
    def test_lists_the_nine_groups_in_enum_order_with_their_lines(self):
        prompt = build_stage1_prompt("hello there", None)
        lines = [ln for ln in prompt.splitlines() if ln.startswith("- ")]
        expected = [f"- {g.value}: {ROUTE_GROUP_LINES[g]}" for g in RouteGroup]
        assert lines[:9] == expected
        assert lines[9:] == [
            f"- {NONE_ROUTE}: no group applies",
            f"- {CLARIFY_ROUTE}: genuinely ambiguous; ask the user",
        ]
        assert len(RouteGroup) == 9

    def test_names_no_op(self, grammar):
        rendered = _STAGE1_SYSTEM_PROMPT + "\n" + build_stage1_prompt("hello there", None)
        for op in grammar.operations:
            if "_" in op.name:
                assert op.name not in rendered, f"stage 1 leaks op {op.name}"
            else:
                assert f"- {op.name}:" not in rendered, f"stage 1 leaks op {op.name}"
            if op.example:
                assert op.example not in rendered
            assert op.description not in rendered

    def test_session_state_block_is_the_same_as_flat(self, grammar):
        snap = SessionSnapshot(active_flow="onboarding", entity_names=["Atlas", "Beacon"])
        flat = build_routing_prompt("hi", grammar, snap)
        tail = flat[flat.index("\nSession state:") :]
        assert build_stage1_prompt("hi", snap).endswith(tail)
        assert build_stage2_prompt("hi", grammar, RouteGroup.ISSUES, snap).endswith(tail)


class TestStage2Prompt:
    @pytest.mark.parametrize("group", list(RouteGroup))
    def test_lists_only_that_groups_ops(self, grammar, group):
        prompt = build_stage2_prompt("hi", grammar, group, None)
        op_lines = [
            ln
            for ln in prompt.splitlines()
            if ln.startswith("- ")
            and not ln.startswith((f"- {CLARIFY_ROUTE}", f"- {OTHER_GROUP_ROUTE}"))
        ]
        assert len(op_lines) == len(EXPECTED[group.value])
        for name in EXPECTED[group.value]:
            assert any(ln.startswith(f"- {name}:") for ln in op_lines)
        others = {n for g, names in EXPECTED.items() if g != group.value for n in names}
        for name in others:
            assert not any(ln.startswith(f"- {name}:") for ln in op_lines)
        assert f"- {CLARIFY_ROUTE}:" in prompt and f"- {OTHER_GROUP_ROUTE}:" in prompt
        assert f"- {NONE_ROUTE}:" not in prompt

    def test_op_line_format_matches_flat(self, grammar):
        flat = build_routing_prompt("hi", grammar, None).splitlines()
        stage2 = build_stage2_prompt("hi", grammar, RouteGroup.ISSUES, None).splitlines()
        issue_lines = [ln for ln in stage2 if ln.split(":")[0][2:] in EXPECTED["issues"]]
        assert issue_lines and all(ln in flat for ln in issue_lines)


class TestFlagOnSingleRoute:
    @pytest.mark.asyncio
    async def test_two_calls_and_validated_op(self, grammar, two_stage):
        llm = FakeLLM([j(group="issues", confidence=0.8), op_reply("close_issue", number="12")])
        d = await route("close issue 12", None, llm_service=llm, grammar=grammar, user_id="u")
        assert len(llm.calls) == 2
        assert llm.calls[0]["system"] == _STAGE1_SYSTEM_PROMPT
        assert llm.calls[0]["prompt"] == build_stage1_prompt("close issue 12", None)
        assert llm.calls[1]["system"] == _STAGE2_SYSTEM_PROMPT
        assert llm.calls[1]["prompt"] == build_stage2_prompt(
            "close issue 12", grammar, RouteGroup.ISSUES, None
        )
        assert all(c["user_id"] == "u" for c in llm.calls)
        assert d.outcome == "operation" and d.operation == "close_issue"
        assert d.args == {"number": "12"} and d.confidence == 0.9
        assert d.route_group == "issues"
        assert d.llm_calls == 2 and not d.repair_attempted

    @pytest.mark.asyncio
    async def test_stage_metrics_present(self, grammar, two_stage):
        llm = FakeLLM([j(group="issues"), op_reply("close_issue")])
        d = await route("close it", None, llm_service=llm, grammar=grammar, user_id=None)
        assert d.stage_metrics is not None and len(d.stage_metrics) == 2
        for stage, m in zip((1, 2), d.stage_metrics):
            assert m["stage"] == stage
            assert set(m) >= {"stage", "latency_ms", "prompt_chars", "response_chars", "llm_calls"}
            assert isinstance(m["latency_ms"], float) and m["latency_ms"] >= 0
            assert m["llm_calls"] == 1 and m["response_chars"] > 0
            assert "tokens" not in m and "input_tokens" not in m
        assert d.stage_metrics[0]["prompt_chars"] == len(_STAGE1_SYSTEM_PROMPT) + len(
            build_stage1_prompt("close it", None)
        )

    @pytest.mark.asyncio
    async def test_llm_calls_counts_both_stages_and_repairs(self, grammar, two_stage):
        llm = FakeLLM(["garbage", j(group="issues"), "garbage", op_reply("close_issue")])
        d = await route("close it", None, llm_service=llm, grammar=grammar, user_id=None)
        assert len(llm.calls) == 4 and d.llm_calls == 4 and d.repair_attempted
        assert [m["llm_calls"] for m in d.stage_metrics] == [2, 2]
        assert d.operation == "close_issue"

    @pytest.mark.asyncio
    async def test_stage2_clarify(self, grammar, two_stage):
        llm = FakeLLM([j(group="issues"), op_reply(CLARIFY_ROUTE)])
        d = await route("do the thing", None, llm_service=llm, grammar=grammar, user_id=None)
        assert d.outcome == "clarify" and d.operation is None and d.llm_calls == 2


class TestStage1Sentinels:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("sentinel,outcome", [(NONE_ROUTE, "none"), (CLARIFY_ROUTE, "clarify")])
    async def test_one_call_and_the_usual_decision(self, grammar, two_stage, sentinel, outcome):
        llm = FakeLLM([j(group=sentinel, confidence=0.7, rationale="because")])
        d = await route("hmm", None, llm_service=llm, grammar=grammar, user_id=None)
        assert len(llm.calls) == 1
        assert d.outcome == outcome and d.operation is None and d.operations == []
        assert d.llm_calls == 1 and d.confidence == 0.7 and d.rationale == "because"
        assert d.route_label == outcome.upper()
        assert d.stage_metrics is not None and len(d.stage_metrics) == 1

    @pytest.mark.asyncio
    async def test_unknown_group_refused_after_one_repair(self, grammar, two_stage):
        llm = FakeLLM([j(group="nonsense"), j(group="nonsense")])
        d = await route("hmm", None, llm_service=llm, grammar=grammar, user_id=None)
        assert d.outcome == "refused" and d.llm_calls == 2 and d.repair_attempted
        assert d.route_group is None and d.stage_metrics is not None

    @pytest.mark.asyncio
    async def test_transport_error_is_an_error_decision(self, grammar, two_stage):
        llm = FakeLLM([RuntimeError("boom")])
        d = await route("hmm", None, llm_service=llm, grammar=grammar, user_id=None)
        assert d.outcome == "error" and "boom" in d.error and d.llm_calls == 1


class TestStage2Validation:
    @pytest.mark.asyncio
    async def test_op_outside_the_group_is_repaired_then_refused(self, grammar, two_stage):
        # create_todo is a valid grammar op but belongs to todos_and_reminders
        llm = FakeLLM([j(group="issues"), op_reply("create_todo"), op_reply("create_todo")])
        d = await route("x", None, llm_service=llm, grammar=grammar, user_id=None)
        assert len(llm.calls) == 3
        assert "Your previous reply was invalid" in llm.calls[2]["prompt"]
        assert "not in the issues group" in llm.calls[2]["prompt"]
        assert d.outcome == "refused" and d.operation is None and d.repair_attempted
        assert d.route_group == "issues" and d.llm_calls == 3

    @pytest.mark.asyncio
    async def test_outside_op_then_valid_repair_is_accepted(self, grammar, two_stage):
        llm = FakeLLM([j(group="issues"), op_reply("create_todo"), op_reply("close_issue")])
        d = await route("x", None, llm_service=llm, grammar=grammar, user_id=None)
        assert d.outcome == "operation" and d.operation == "close_issue" and d.llm_calls == 3

    @pytest.mark.asyncio
    async def test_invented_op_is_refused(self, grammar, two_stage):
        llm = FakeLLM([j(group="issues"), op_reply("not_an_op"), op_reply("not_an_op")])
        d = await route("x", None, llm_service=llm, grammar=grammar, user_id=None)
        assert d.outcome == "refused"

    @pytest.mark.asyncio
    async def test_none_is_not_offered_at_stage_2(self, grammar, two_stage):
        llm = FakeLLM([j(group="issues"), op_reply(NONE_ROUTE), op_reply(NONE_ROUTE)])
        d = await route("x", None, llm_service=llm, grammar=grammar, user_id=None)
        assert d.outcome == "refused"

    @pytest.mark.asyncio
    async def test_other_group_is_clarify_and_never_rerouted(self, grammar, two_stage):
        llm = FakeLLM([j(group="issues"), op_reply(OTHER_GROUP_ROUTE)])
        d = await route("remind me tomorrow", None, llm_service=llm, grammar=grammar, user_id=None)
        assert len(llm.calls) == 2, "no third call: code never re-routes OTHER_GROUP"
        assert d.outcome == "clarify" and d.operation is None
        assert d.route_group == "issues" and d.llm_calls == 2
        assert d.stage_metrics[1]["pick"] == OTHER_GROUP_ROUTE


class TestPlan:
    @pytest.mark.asyncio
    async def test_plan_is_one_stage2_call_per_planned_group(self, grammar, two_stage):
        plan1 = json.dumps(
            {
                "outcome": "plan",
                "groups": [
                    {"group": "issues", "text": "close issue 4"},
                    {"group": "todos_and_reminders", "text": "remind me Friday"},
                ],
            }
        )
        llm = FakeLLM([plan1, op_reply("close_issue", number="4"), op_reply("create_reminder")])
        d = await route(
            "close issue 4 and remind me Friday",
            None,
            llm_service=llm,
            grammar=grammar,
            user_id=None,
        )
        assert len(llm.calls) == 3
        assert llm.calls[1]["prompt"] == build_stage2_prompt(
            "close issue 4 and remind me Friday", grammar, RouteGroup.ISSUES, None, "close issue 4"
        )
        assert "remind me Friday" in llm.calls[2]["prompt"]
        assert d.outcome == "plan" and d.operation is None
        assert [o["operation"] for o in d.operations] == ["close_issue", "create_reminder"]
        assert [o["text"] for o in d.operations] == ["close issue 4", "remind me Friday"]
        assert d.route_group == "issues,todos_and_reminders"
        assert d.route_label == "PLAN[close_issue→create_reminder]"
        assert d.llm_calls == 3
        assert [m["stage"] for m in d.stage_metrics] == [1, 2, 2]
        assert [m.get("group") for m in d.stage_metrics] == [
            None,
            "issues",
            "todos_and_reminders",
        ]

    @pytest.mark.asyncio
    async def test_plan_with_one_group_element_is_invalid(self, grammar, two_stage):
        bad = json.dumps({"outcome": "plan", "groups": [{"group": "issues", "text": "a"}]})
        llm = FakeLLM([bad, bad])
        d = await route("x", None, llm_service=llm, grammar=grammar, user_id=None)
        assert d.outcome == "refused" and len(llm.calls) == 2

    @pytest.mark.asyncio
    async def test_plan_over_the_limit_is_invalid(self, grammar, two_stage):
        els = [{"group": "issues", "text": "t"}] * 4
        bad = json.dumps({"outcome": "plan", "groups": els})
        llm = FakeLLM([bad, bad])
        d = await route("x", None, llm_service=llm, grammar=grammar, user_id=None)
        assert d.outcome == "refused"

    @pytest.mark.asyncio
    async def test_plan_element_other_group_stops_as_clarify(self, grammar, two_stage):
        plan1 = json.dumps(
            {
                "outcome": "plan",
                "groups": [
                    {"group": "issues", "text": "a"},
                    {"group": "todos_and_reminders", "text": "b"},
                ],
            }
        )
        llm = FakeLLM([plan1, op_reply(OTHER_GROUP_ROUTE)])
        d = await route("x", None, llm_service=llm, grammar=grammar, user_id=None)
        assert len(llm.calls) == 2 and d.outcome == "clarify"
