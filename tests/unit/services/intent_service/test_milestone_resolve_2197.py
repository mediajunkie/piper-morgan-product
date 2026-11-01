"""#2197 — the op-local milestone resolver (Arch 2026-11-01 10:48 (2), 11:01, 11:14, 11:28).

The model says WHICH read milestone by index; code keeps only indices inside the read
(one → picked, two or more → tie, none → none / named_absent); "next" is code's.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List

import pytest

from services.intent_service import milestone_resolve as mres
from services.llm.request_key import UnboundLLMKeyError, UserLLMKeyRequiredError

CANDIDATES: List[Dict[str, Any]] = [
    {
        "title": "MVP",
        "state": "open",
        "due_on": "2026-11-20T00:00:00Z",
        "open_issues": 4,
        "closed_issues": 6,
    },
    {
        "title": "Production",
        "state": "open",
        "due_on": "2026-12-15T00:00:00Z",
        "open_issues": 9,
        "closed_issues": 1,
    },
    {"title": "Fast Follow", "state": "open", "due_on": None, "open_issues": 2, "closed_issues": 0},
]


class FakeLLM:
    def __init__(self, reply: Any = None, *, usage: Dict[str, int] | None = None, raises=None):
        self.reply = reply
        self.usage = usage
        self.raises = raises
        self.calls: List[Dict[str, Any]] = []

    async def complete(self, **kwargs):
        self.calls.append(kwargs)
        if self.raises is not None:
            raise self.raises
        served = kwargs.get("served")
        if served is not None and self.usage is not None:
            served["usage"] = dict(self.usage)
        return self.reply


async def _resolve(
    reply, candidates=CANDIDATES, message="what's the progress on the MVP milestone?", **kw
):
    llm = FakeLLM(reply, **kw)
    res = await mres.resolve_milestone(message, candidates, llm_service=llm, user_id="u1")
    return res, llm


class TestIndicesShape_Arch1128:
    @pytest.mark.asyncio
    async def test_one_in_range_index_is_picked(self):
        res, llm = await _resolve('{"indices": [0]}')
        assert res.outcome == "picked" and res.index == 0
        assert llm.calls[0]["task_type"] == "milestone_resolution"
        assert llm.calls[0]["user_id"] == "u1"

    @pytest.mark.asyncio
    async def test_out_of_range_index_is_dropped_and_the_in_range_one_picked(self):
        res, _ = await _resolve('{"indices": [1, 7]}')
        assert res.outcome == "picked" and res.index == 1

    @pytest.mark.asyncio
    async def test_two_in_range_indices_are_a_tie(self):
        res, _ = await _resolve('{"indices": [0, 2]}')
        assert res.outcome == "tie" and res.index is None

    @pytest.mark.asyncio
    async def test_empty_indices_is_none(self):
        res, _ = await _resolve('{"indices": []}')
        assert res.outcome == "none" and res.index is None

    @pytest.mark.asyncio
    async def test_non_list_indices_fails(self):
        res, _ = await _resolve('{"indices": 1}')
        assert res.outcome == "failed" and res.index is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "reply",
        [
            '{"indices": [7]}',
            '{"indices": [-1]}',
            '{"indices": ["0"]}',
            '{"indices": [true]}',
            '{"indices": [1.0]}',
        ],
    )
    async def test_out_of_range_or_non_int_binds_nothing(self, reply):
        res, _ = await _resolve(reply)
        assert res.index is None and res.outcome == "none"

    @pytest.mark.asyncio
    async def test_bare_index_is_read_leniently_as_one_element_list(self):
        res, _ = await _resolve('{"index": 1}')
        assert res.outcome == "picked" and res.index == 1
        res, _ = await _resolve('{"index": "1"}')
        assert res.outcome == "failed"

    @pytest.mark.asyncio
    async def test_named_absent_and_null(self):
        res, _ = await _resolve('{"index": null, "named_absent": true}')
        assert res.outcome == "named_absent" and res.named_absent is True and res.index is None
        res, _ = await _resolve('{"index": null}')
        assert res.outcome == "none"

    @pytest.mark.asyncio
    async def test_fenced_json_is_accepted(self):
        res, _ = await _resolve('```json\n{"indices": [2]}\n```')
        assert res.outcome == "picked" and res.index == 2

    @pytest.mark.asyncio
    @pytest.mark.parametrize("reply", ["MVP", "", "[0]", '{"indices": [0]} trailing', None])
    async def test_unparseable_fails(self, reply):
        res, _ = await _resolve(reply)
        assert res.outcome == "failed" and res.index is None


class TestNextIsCodes_Arch1101:
    @pytest.mark.asyncio
    async def test_next_ignores_any_index_the_model_returns(self):
        res, _ = await _resolve(
            '{"selector": "next", "indices": [1], "index": 1}', message="what's the next milestone?"
        )
        assert res.outcome == "next" and res.selector == "next" and res.index is None

    def test_code_picks_earliest_due_among_open(self):
        assert mres.pick_next_index(CANDIDATES) == 0
        cands = [dict(CANDIDATES[0], state="closed"), CANDIDATES[1], CANDIDATES[2]]
        assert mres.pick_next_index(cands) == 1

    def test_undated_or_tied_earliest_is_a_tie(self):
        assert mres.pick_next_index([CANDIDATES[2]]) is None
        tied = [CANDIDATES[0], dict(CANDIDATES[1], due_on="2026-11-20T08:00:00Z")]
        assert mres.pick_next_index(tied) is None


class TestFailuresAndSkips:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "exc",
        [
            UnboundLLMKeyError("x"),
            UserLLMKeyRequiredError("x"),
            asyncio.TimeoutError(),
            RuntimeError("All configured LLM providers failed"),
            ValueError("x"),
        ],
    )
    async def test_errors_are_failed(self, exc):
        res, _ = await _resolve(None, raises=exc)
        assert res.outcome == "failed" and res.index is None

    @pytest.mark.asyncio
    async def test_empty_candidates_or_blank_message_make_no_call(self):
        res, llm = await _resolve('{"indices": [0]}', candidates=[])
        assert res.outcome == "skipped" and llm.calls == []
        res, llm = await _resolve('{"indices": [0]}', message="   ")
        assert res.outcome == "skipped" and llm.calls == []


class TestPromptAndUsage:
    @pytest.mark.asyncio
    async def test_prompt_carries_every_title_and_the_message(self):
        _, llm = await _resolve('{"indices": [0]}')
        prompt = llm.calls[0]["prompt"]
        for m in CANDIDATES:
            assert m["title"] in prompt
        assert "what's the progress on the MVP milestone?" in prompt
        assert "2026-11-20" in prompt and "T00:00:00Z" not in prompt
        assert llm.calls[0]["system"] == mres.MILESTONE_RESOLVER_SYSTEM_PROMPT
        assert '"indices"' in mres.MILESTONE_RESOLVER_SYSTEM_PROMPT
        assert '"tie"' not in mres.MILESTONE_RESOLVER_SYSTEM_PROMPT  # Arch 11:28: dropped

    @pytest.mark.asyncio
    async def test_usage_comes_from_served_usage_only(self):
        res, _ = await _resolve('{"indices": [0]}', usage={"input_tokens": 412, "output_tokens": 7})
        assert (res.input_tokens, res.output_tokens) == (412, 7)
        assert isinstance(res.latency_ms, int)
        res, _ = await _resolve('{"indices": [0]}')  # provider reported nothing → never estimated
        assert res.input_tokens is None and res.output_tokens is None

    def test_task_type_has_its_own_light_tier_config(self):
        from services.llm.config import MODEL_CONFIGS

        assert MODEL_CONFIGS["milestone_resolution"]["model_tier"] == "light"
