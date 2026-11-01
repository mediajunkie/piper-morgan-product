"""scripts/router_batch.py two-stage subcommands (#2149 step 3): render-stage1 mirrors the
live stage-1 request; render-stage2 renders one request per stage-1 pick (per planned
group for a plan; nothing for NONE/CLARIFY/REFUSED); parse-two-stage reconstructs each
decision through the REAL route() under the flag, from a replay of both batches."""

import importlib.util
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
_spec = importlib.util.spec_from_file_location("router_batch", ROOT / "scripts" / "router_batch.py")
rb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rb)


def _results(path: Path, texts: dict, usage: dict | None = None) -> None:
    with open(path, "w") as f:
        for cid, text in texts.items():
            rec = {"custom_id": cid, "type": "succeeded", "text": text, "model": "claude-haiku-4-5"}
            if usage and cid in usage:
                rec["usage"] = usage[cid]
            f.write(json.dumps(rec) + "\n")


def test_render_stage1_builds_the_live_stage1_request(tmp_path):
    from services.intent_service.inversion_router import _STAGE1_SYSTEM_PROMPT, build_stage1_prompt

    out = tmp_path / "s1.jsonl"
    rb._render_stage1(
        SimpleNamespace(label="ts", samples=2, phrase=["show my todos"], corpus=False, out=str(out))
    )
    rows = [json.loads(line) for line in out.read_text().splitlines()]
    assert [r["custom_id"] for r in rows] == ["ts-0-1", "ts-0-2"]
    assert rows[0]["stage"] == 1
    assert rows[0]["tree"] and rows[0]["tree"] != "unknown", "the rendering tree is recorded"
    p = rows[0]["params"]
    assert p["system"] == _STAGE1_SYSTEM_PROMPT
    assert p["messages"] == [{"role": "user", "content": build_stage1_prompt("show my todos")}]
    assert p["model"].startswith("claude-") and p["max_tokens"] > 0


def test_render_stage2_renders_one_request_per_pick_by_build_stage2_prompt_unaltered(tmp_path):
    from services.intent_service.inversion_router import (
        _STAGE2_SYSTEM_PROMPT,
        build_stage2_prompt,
        derive_routing_grammar,
    )
    from services.shared_types import RouteGroup

    grammar = derive_routing_grammar()
    s1_reqs = tmp_path / "s1.jsonl"
    with open(s1_reqs, "w") as f:
        for i, phrase in enumerate(
            ["add a todo", "hello there", "list issues and my week", "garbage"]
        ):
            f.write(
                json.dumps(
                    {
                        "custom_id": f"ts-{i}-1",
                        "phrase": phrase,
                        "stage": 1,
                        "tree": rb._tree_sha(),
                        "params": {},
                    }
                )
                + "\n"
            )
    s1_res = tmp_path / "s1-res.jsonl"
    _results(
        s1_res,
        {
            "ts-0-1": '{"group": "todos_and_reminders", "confidence": 0.9}',
            "ts-1-1": '{"group": "NONE", "confidence": 0.8}',
            "ts-2-1": '{"outcome": "plan", "groups": [{"group": "issues", "text": "list issues"}, {"group": "calendar_and_time", "text": "my week"}]}',
            "ts-3-1": "not json at all",
        },
    )
    out = tmp_path / "s2.jsonl"
    rb._render_stage2(SimpleNamespace(requests=str(s1_reqs), results=str(s1_res), out=str(out)))
    rows = [json.loads(line) for line in out.read_text().splitlines()]
    assert [r["custom_id"] for r in rows] == ["ts-0-1-s2-0", "ts-2-1-s2-0", "ts-2-1-s2-1"]
    assert rows[0]["group"] == "todos_and_reminders" and rows[0]["part_text"] is None
    assert rows[0]["params"]["system"] == _STAGE2_SYSTEM_PROMPT
    assert rows[0]["params"]["messages"][0]["content"] == build_stage2_prompt(
        "add a todo", grammar, RouteGroup.TODOS_AND_REMINDERS, None, None
    )
    assert (rows[1]["group"], rows[1]["part_text"]) == ("issues", "list issues")
    assert (rows[2]["group"], rows[2]["part_text"]) == ("calendar_and_time", "my week")
    assert rows[2]["params"]["messages"][0]["content"] == build_stage2_prompt(
        "list issues and my week", grammar, RouteGroup.CALENDAR_AND_TIME, None, "my week"
    )


def test_parse_two_stage_reconstructs_decisions_through_route(tmp_path, monkeypatch):
    monkeypatch.delenv("PIPER_INVERSION_TWO_STAGE", raising=False)
    s1_reqs = tmp_path / "s1.jsonl"
    phrases = ["add a todo", "hello there", "list issues and my week", "garbage", "close it"]
    with open(s1_reqs, "w") as f:
        for i, phrase in enumerate(phrases):
            f.write(
                json.dumps(
                    {
                        "custom_id": f"ts-{i}-1",
                        "phrase": phrase,
                        "stage": 1,
                        "tree": rb._tree_sha(),
                        "params": {},
                    }
                )
                + "\n"
            )
    s1_res = tmp_path / "s1-res.jsonl"
    _results(
        s1_res,
        {
            "ts-0-1": '{"group": "todos_and_reminders", "confidence": 0.9}',
            "ts-1-1": '{"group": "NONE", "confidence": 0.8}',
            "ts-2-1": '{"outcome": "plan", "groups": [{"group": "issues", "text": "list issues"}, {"group": "calendar_and_time", "text": "my week"}]}',
            "ts-3-1": "not json at all",
            "ts-4-1": '{"group": "issues", "confidence": 0.7}',
        },
    )
    s2_reqs = tmp_path / "s2.jsonl"
    rb._render_stage2(SimpleNamespace(requests=str(s1_reqs), results=str(s1_res), out=str(s2_reqs)))
    s2_res = tmp_path / "s2-res.jsonl"
    _results(
        s2_res,
        {
            "ts-0-1-s2-0": '{"operation": "create_todo", "args": {}, "confidence": 0.9, "rationale": "r"}',
            "ts-2-1-s2-0": '{"operation": "list_issues", "args": {}, "confidence": 0.9, "rationale": "r"}',
            "ts-2-1-s2-1": '{"operation": "week_calendar", "args": {}, "confidence": 0.9, "rationale": "r"}',
            "ts-4-1-s2-0": '{"operation": "OTHER_GROUP", "rationale": "belongs elsewhere"}',
        },
        usage={
            "ts-0-1-s2-0": {"input_tokens": 500, "output_tokens": 30},
            "ts-2-1-s2-0": {"input_tokens": 400, "output_tokens": 20},
            "ts-2-1-s2-1": {"input_tokens": 450, "output_tokens": 25},
        },
    )
    expected = tmp_path / "expected.yaml"
    expected.write_text(
        "corpus:\n"
        "  - phrase: add a todo\n    expected: action:create_todo\n"
        "  - phrase: hello there\n    expected: action:greeting\n"
        "  - phrase: close it\n    expected: action:close_issue\n"
        "  - phrase: garbage\n    expected: REVIEW\n"
    )
    out = tmp_path / "report.md"
    rb._parse_two_stage(
        SimpleNamespace(
            s1_requests=str(s1_reqs),
            s1_results=str(s1_res),
            s2_requests=str(s2_reqs),
            s2_results=str(s2_res),
            expected=str(expected),
            out=str(out),
        )
    )
    assert "PIPER_INVERSION_TWO_STAGE" not in os.environ, "the flag is restored after the parse"
    report = out.read_text()
    assert "| add a todo | `create_todo` ×1 | `todos_and_reminders` ×1 | 2 |" in report
    assert "| hello there | `NONE` ×1 | `NONE` ×1 | 1 |" in report
    assert "| list issues and my week | `PLAN[list_issues→week_calendar]` ×1 |" in report
    assert "| garbage | `REFUSED` ×1 |" in report
    assert "| close it | `CLARIFY` ×1 | `issues` ×1 | 2 |" in report
    assert "Stage 2: OTHER_GROUP 1 · CLARIFY 0" in report
    # Arch 09:13: token counts come from the batch results' own usage, never estimated;
    # stage 1 carried none here (0), stage 2 sums the three results that did.
    assert "stage 1 in 0 / out 0 · stage 2 in 1350 / out 75" in report
    assert "2 REFUSED" in report or "1 REFUSED" in report
    assert "## Group confusion" in report
    # Arch 09:21: the report says which tree rendered each stage of this arm.
    assert "Rendered from: stage 1 tree `" in report and "· stage 2 tree `" in report
    assert "trees differ" not in report
    assert "| todos_and_reminders | todos_and_reminders | 1 |" in report
    assert "| assistant_and_conversation | NONE | 1 |" in report
    assert "| issues | issues | 1 |" in report
    assert "| n/a | REFUSED/ERROR | 1 |" in report  # a REVIEW row is unscored, never a group


def test_render_stage2_arm_prefix_keeps_ids_distinct_for_a_shared_stage1(tmp_path):
    """Stage 1 names no op, so its prompts are identical across arms; the arms share one
    stage-1 result set and --arm keeps their stage-2 ids distinct in one batch."""
    s1_reqs = tmp_path / "s1.jsonl"
    s1_reqs.write_text(
        json.dumps(
            {"custom_id": "main-0-1", "phrase": "add a todo", "stage": 1, "tree": "t", "params": {}}
        )
        + "\n"
    )
    s1_res = tmp_path / "s1-res.jsonl"
    _results(s1_res, {"main-0-1": '{"group": "todos_and_reminders", "confidence": 0.9}'})
    out_a = tmp_path / "a.jsonl"
    out_b = tmp_path / "b.jsonl"
    rb._render_stage2(
        SimpleNamespace(requests=str(s1_reqs), results=str(s1_res), arm="d1", out=str(out_a))
    )
    rb._render_stage2(
        SimpleNamespace(requests=str(s1_reqs), results=str(s1_res), arm=None, out=str(out_b))
    )
    a = json.loads(out_a.read_text())
    b = json.loads(out_b.read_text())
    assert a["custom_id"] == "d1__main-0-1-s2-0" and a["arm"] == "d1" and a["parent"] == "main-0-1"
    import re

    assert re.fullmatch(r"[A-Za-z0-9_-]{1,64}", a["custom_id"]), "a batch custom_id's allowed set"
    assert b["custom_id"] == "main-0-1-s2-0" and b["arm"] is None
    assert a["params"] == b["params"], "the arm prefix changes the id only"


def test_corpus_replay_answers_route_by_phrase_for_one_arm(tmp_path, monkeypatch):
    """The scorer's seam: one replay over a whole two-phase batch, keyed by phrase; the
    arm selects which stage-2 requests answer. route() under the flag then reconstructs
    the decision exactly as parse-two-stage does."""
    import asyncio

    from services.intent_service import inversion_router as ir

    s1_reqs = tmp_path / "s1.jsonl"
    s1_reqs.write_text(
        json.dumps(
            {"custom_id": "main-0-1", "phrase": "add a todo", "stage": 1, "tree": "t", "params": {}}
        )
        + "\n"
    )
    s1_res = tmp_path / "s1-res.jsonl"
    _results(s1_res, {"main-0-1": '{"group": "todos_and_reminders", "confidence": 0.9}'})
    s2_reqs = tmp_path / "s2.jsonl"
    with open(s2_reqs, "w") as f:
        for arm, cid in ((None, "main-0-1-s2-0"), ("d1", "d1__main-0-1-s2-0")):
            f.write(
                json.dumps(
                    {
                        "custom_id": cid,
                        "phrase": "add a todo",
                        "stage": 2,
                        "tree": "t",
                        "parent": "main-0-1",
                        "group": "todos_and_reminders",
                        "part_text": None,
                        "arm": arm,
                        "params": {},
                    }
                )
                + "\n"
            )
    s2_res = tmp_path / "s2-res.jsonl"
    _results(
        s2_res,
        {
            "main-0-1-s2-0": '{"operation": "create_todo", "args": {}, "confidence": 0.9, "rationale": "r"}',
            "d1__main-0-1-s2-0": '{"operation": "create_reminder", "args": {}, "confidence": 0.9, "rationale": "r"}',
        },
    )
    monkeypatch.setenv("PIPER_INVERSION_TWO_STAGE", "1")
    main_arm = rb.TwoStageCorpusReplayLLM(
        str(s1_reqs), str(s1_res), str(s2_reqs), str(s2_res), arm=None
    )
    d1_arm = rb.TwoStageCorpusReplayLLM(
        str(s1_reqs), str(s1_res), str(s2_reqs), str(s2_res), arm="d1"
    )
    assert (
        asyncio.run(ir.route("add a todo", None, llm_service=main_arm, user_id=None)).operation
        == "create_todo"
    )
    assert (
        asyncio.run(ir.route("add a todo", None, llm_service=d1_arm, user_id=None)).operation
        == "create_reminder"
    )
    with pytest.raises(RuntimeError):
        asyncio.run(
            main_arm.complete(
                task_type="t",
                prompt="User message: 'unknown phrase'",
                system=ir._STAGE1_SYSTEM_PROMPT,
            )
        )


def test_replay_matches_stage2_by_group_and_part_never_by_the_users_words():
    from services.intent_service.inversion_router import (
        _STAGE1_SYSTEM_PROMPT,
        _STAGE2_SYSTEM_PROMPT,
    )

    s1 = {"type": "succeeded", "text": "S1", "model": "m"}
    s2 = {("issues", None): {"type": "succeeded", "text": "S2-issues", "model": "m"}}
    replay = rb.TwoStageReplayLLM(s1, s2)
    import asyncio

    served: dict = {}
    assert (
        asyncio.run(
            replay.complete(
                task_type="t", prompt="anything", system=_STAGE1_SYSTEM_PROMPT, served=served
            )
        )
        == "S1"
    )
    assert served["model"] == "m"
    prompt = "Operations in the issues group (choose exactly one):\n- close_issue: x\n\nUser message: 'close it'"
    assert (
        asyncio.run(replay.complete(task_type="t", prompt=prompt, system=_STAGE2_SYSTEM_PROMPT))
        == "S2-issues"
    )
    with pytest.raises(RuntimeError):
        asyncio.run(
            replay.complete(
                task_type="t",
                prompt=prompt.replace("issues", "repo_activity"),
                system=_STAGE2_SYSTEM_PROMPT,
            )
        )
