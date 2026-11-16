"""scripts/router_batch.py: render mirrors the live Anthropic router request; replay answers it."""

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
_spec = importlib.util.spec_from_file_location("router_batch", ROOT / "scripts" / "router_batch.py")
rb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rb)


def test_render_builds_the_live_request(tmp_path):
    from services.intent_service.inversion_router import (
        _SYSTEM_PROMPT,
        build_routing_prompt,
        derive_routing_grammar,
    )

    out = tmp_path / "r.jsonl"
    rb._render(
        SimpleNamespace(
            label="main", samples=2, phrase=["show my todos"], corpus=False, out=str(out)
        )
    )
    rows = [json.loads(line) for line in out.read_text().splitlines()]
    assert [r["custom_id"] for r in rows] == ["main-0-1", "main-0-2"]
    p = rows[0]["params"]
    assert p["system"] == _SYSTEM_PROMPT
    assert p["messages"] == [
        {"role": "user", "content": build_routing_prompt("show my todos", derive_routing_grammar())}
    ]
    assert p["model"].startswith("claude-") and p["max_tokens"] > 0


@pytest.mark.asyncio
async def test_replay_answers_the_router_prompt_and_its_repair(tmp_path):
    from services.intent_service.inversion_router import (
        build_routing_prompt,
        derive_routing_grammar,
    )

    reqs = tmp_path / "q.jsonl"
    res = tmp_path / "s.jsonl"
    reqs.write_text(
        json.dumps({"custom_id": "c-0-1", "phrase": "show my todos", "params": {}}) + "\n"
    )
    res.write_text(
        json.dumps(
            {
                "custom_id": "c-0-1",
                "type": "succeeded",
                "text": '{"x":1}',
                "model": "claude-haiku-4-5",
            }
        )
        + "\n"
    )
    llm = rb.ReplayLLM(str(reqs), str(res))
    prompt = build_routing_prompt("show my todos", derive_routing_grammar())
    served = {}
    assert await llm.complete(task_type="t", prompt=prompt, served=served) == '{"x":1}'
    assert served == {"provider": "anthropic", "model": "claude-haiku-4-5"}
    repair = prompt + "\n\nYour previous reply was invalid: x."
    assert await llm.complete(task_type="t", prompt=repair) == '{"x":1}'
    with pytest.raises(RuntimeError):
        await llm.complete(task_type="t", prompt="User message: 'something else'")


def test_render_model_and_no_thinking_flags(tmp_path):
    """--model renders another model id on the same tree (temperature as served
    for that id); --no-thinking adds thinking=disabled. Harness only (Arch
    2026-10-30 15:20 item 4); neither flag touches the served router."""
    import json

    out = tmp_path / "r.jsonl"
    rb._render(
        SimpleNamespace(
            label="screen",
            samples=1,
            phrase=["show my todos"],
            corpus=False,
            out=str(out),
            model="claude-opus-4-8",
            no_thinking=True,
        )
    )
    rec = json.loads(out.read_text().splitlines()[0])
    assert rec["params"]["model"] == "claude-opus-4-8"
    assert "temperature" not in rec["params"]  # opus-4-8 is in MODELS_WITHOUT_TEMPERATURE
    assert rec["params"]["thinking"] == {"type": "disabled"}
    assert rec["custom_id"] == "screen-0-1"


# --- submit's spend cap (CIO 2026-11-15: a paid screen's stop is code) ---------------


def _req(cid="a-0-1", model="claude-haiku-4-5", chars=3000, max_tokens=400):
    return {
        "custom_id": cid,
        "params": {
            "model": model,
            "max_tokens": max_tokens,
            "system": "s" * 1000,
            "messages": [{"role": "user", "content": "u" * (chars - 1000)}],
        },
    }


def test_ceiling_counts_text_at_three_chars_a_token_and_all_of_max_tokens():
    # 3,000 chars -> 1,000 tokens in at $0.50/M; 400 out at $2.50/M.
    assert rb.ceiling_usd([_req()]) == pytest.approx((1000 * 0.50 + 400 * 2.50) / 1_000_000)
    assert rb.ceiling_usd([_req("a"), _req("b")]) == pytest.approx(2 * rb.ceiling_usd([_req()]))


def test_a_dated_model_id_takes_its_family_price_and_an_unknown_model_is_refused():
    assert rb.ceiling_usd([_req(model="claude-haiku-4-5-20251001")]) == rb.ceiling_usd([_req()])
    with pytest.raises(rb.CapRefused, match="no batch price recorded"):
        rb.ceiling_usd([_req(model="claude-sonnet-4-6")])
    # A longer family name must not borrow a shorter one's price.
    with pytest.raises(rb.CapRefused):
        rb.ceiling_usd([_req(model="claude-haiku-4-50")])


def test_cap_refuses_when_the_ledger_plus_the_ceiling_passes_it():
    reqs = [_req(str(i)) for i in range(1000)]  # ceiling $1.50
    assert rb.ceiling_usd(reqs) == pytest.approx(1.5)
    assert rb.check_cap(reqs, 2.0, {"entries": []}) == (pytest.approx(1.5), 0)
    with pytest.raises(rb.CapRefused, match="Nothing was sent"):
        rb.check_cap(reqs, 1.49, {"entries": []})
    earlier = {"entries": [{"ceiling_usd": 1.0, "actual_usd": 0.6}]}
    assert rb.check_cap(reqs, 2.2, earlier)[1] == pytest.approx(0.6)
    with pytest.raises(rb.CapRefused, match=r"\$0\.60 is already"):
        rb.check_cap(reqs, 2.0, earlier)


def test_a_batch_that_never_reported_counts_at_its_ceiling():
    ledger = {
        "entries": [
            {"ceiling_usd": 1.0, "actual_usd": None},
            {"ceiling_usd": 2.0, "actual_usd": 0.5},
        ]
    }
    assert rb.ledger_spent(ledger) == pytest.approx(1.5)


def test_actual_cost_uses_the_providers_token_counts():
    records = [
        {
            "custom_id": "a",
            "model": "claude-haiku-4-5-20251001",
            "usage": {"input_tokens": 2_000_000, "output_tokens": 1_000_000},
        },
        {"custom_id": "b", "type": "errored"},  # no usage: costs nothing
    ]
    cost = rb.actual_usd(records, {"a": "claude-haiku-4-5", "b": "claude-haiku-4-5"})
    assert cost == pytest.approx(2 * 0.50 + 2.50)


def _submit_args(tmp_path, reqs, **over):
    path = tmp_path / "reqs.jsonl"
    path.write_text("".join(json.dumps(r) + "\n" for r in reqs))
    base = dict(
        requests=[str(path)],
        out=str(tmp_path / "results.jsonl"),
        poll=0,
        cap_usd=8.0,
        ledger=str(tmp_path / "ledger.json"),
        dry_run=False,
    )
    base.update(over)
    return SimpleNamespace(**base)


def _forbid_the_binder(monkeypatch):
    import dev_key_binding

    def boom(*a, **k):
        raise AssertionError("the key binder was reached")

    monkeypatch.setattr(dev_key_binding, "developer_keys_bound", boom)


def test_dry_run_prints_the_plan_and_reaches_neither_key_nor_ledger(tmp_path, monkeypatch, capsys):
    _forbid_the_binder(monkeypatch)
    args = _submit_args(tmp_path, [_req("a"), _req("b")], dry_run=True)
    rb._submit(args)
    out = capsys.readouterr().out
    assert "PLANNED: 2 requests in one batch on anthropic" in out
    assert "Nothing has been sent yet." in out and "dry run: nothing sent" in out
    assert not (tmp_path / "ledger.json").exists()
    assert not (tmp_path / "results.jsonl").exists()


def test_over_the_cap_is_refused_before_the_key_binder(tmp_path, monkeypatch):
    _forbid_the_binder(monkeypatch)
    args = _submit_args(tmp_path, [_req(str(i)) for i in range(1000)], cap_usd=1.0)
    with pytest.raises(rb.CapRefused):
        rb._submit(args)
    assert not (tmp_path / "ledger.json").exists()


def test_a_sent_batch_is_counted_at_its_ceiling_then_at_its_measured_cost(
    tmp_path, monkeypatch, capsys
):
    import contextlib

    import dev_key_binding

    import services.llm.request_key as request_key

    seen = {}
    ledger_path = tmp_path / "ledger.json"

    class _Batches:
        def create(self, requests):
            seen["sent"] = len(requests)
            return SimpleNamespace(id="batch_1")

        def retrieve(self, batch_id):
            # By the first poll the ledger already holds the batch at its ceiling.
            seen["while_waiting"] = json.loads(ledger_path.read_text())["entries"][0]
            return SimpleNamespace(processing_status="ended", request_counts="2 ok")

        def results(self, batch_id):
            for cid in ("a", "b"):
                msg = SimpleNamespace(
                    content=[SimpleNamespace(type="text", text="{}")],
                    model="claude-haiku-4-5-20251001",
                    usage=SimpleNamespace(input_tokens=1_000_000, output_tokens=0),
                )
                yield SimpleNamespace(
                    custom_id=cid, result=SimpleNamespace(type="succeeded", message=msg)
                )

    @contextlib.contextmanager
    def bound(**kwargs):
        seen["providers"] = kwargs.get("providers")
        yield

    monkeypatch.setattr(dev_key_binding, "developer_keys_bound", bound)
    monkeypatch.setattr(
        request_key,
        "anthropic_client_for_request",
        lambda: SimpleNamespace(messages=SimpleNamespace(batches=_Batches())),
    )
    args = _submit_args(tmp_path, [_req("a"), _req("b")])
    rb._submit(args)

    assert seen["sent"] == 2 and seen["providers"] == ("anthropic",)
    assert seen["while_waiting"]["actual_usd"] is None
    assert seen["while_waiting"]["ceiling_usd"] == pytest.approx(0.003)
    entry = json.loads(ledger_path.read_text())["entries"][0]
    assert entry["batch"] == "batch_1" and entry["requests"] == 2
    assert entry["actual_usd"] == pytest.approx(1.0)  # 2M input tokens at $0.50/M
    assert "COST: this batch $1.00" in capsys.readouterr().out
    # The next batch of the same screen starts from the measured dollar.
    with pytest.raises(rb.CapRefused, match=r"\$1\.00 is already"):
        rb._submit(_submit_args(tmp_path, [_req("c")], cap_usd=1.0))


def test_submit_requires_a_cap_and_a_ledger(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["router_batch.py", "submit", "x.jsonl", "--out", "y"])
    with pytest.raises(SystemExit):
        rb.main()


# --- parse --arg (arm B: what the router put in one named arg) -----------------------


def _reply(operation, **args):
    return json.dumps(
        {"operation": operation, "args": args, "confidence": 0.9, "rationale": "because"}
    )


def _parse_report(tmp_path, replies, arg=()):
    reqs, res, out = tmp_path / "q.jsonl", tmp_path / "s.jsonl", tmp_path / "r.md"
    reqs.write_text(
        "".join(
            json.dumps({"custom_id": f"m-0-{n}", "phrase": "add milk to my list", "params": {}})
            + "\n"
            for n in range(1, len(replies) + 1)
        )
    )
    res.write_text(
        "".join(
            json.dumps(
                {
                    "custom_id": f"m-0-{n}",
                    "type": "succeeded",
                    "text": text,
                    "model": "claude-haiku-4-5",
                }
            )
            + "\n"
            for n, text in enumerate(replies, 1)
        )
    )
    rb._parse(SimpleNamespace(requests=str(reqs), results=str(res), out=str(out), arg=list(arg)))
    return out.read_text()


def test_parse_without_arg_keeps_the_three_column_table(tmp_path):
    report = _parse_report(tmp_path, [_reply("create_todo", text="milk")])
    assert "| phrase | routes (count) | confidence range |\n|---|---|---|\n" in report
    assert "| add milk to my list | `create_todo` ×1 | 0.90–0.90 |\n" in report


def test_parse_arg_counts_each_value_and_the_replies_without_it(tmp_path):
    replies = [
        _reply("create_todo", text="milk", project="my list"),
        _reply("create_todo", text="milk", project="my list"),
        _reply("create_todo", text="milk"),
    ]
    report = _parse_report(tmp_path, replies, arg=["project", "text"])
    assert (
        "| phrase | routes (count) | confidence range | args.project (count) | args.text (count) |"
    ) in report
    assert "|---|---|---|---|---|" in report
    assert (
        '| add milk to my list | `create_todo` ×3 | 0.90–0.90 | "my list" ×2, (none) ×1 '
        '| "milk" ×3 |'
    ) in report
