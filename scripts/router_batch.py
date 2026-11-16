#!/usr/bin/env python3
"""Router screens through the Anthropic Message Batches API (half price; #2145 follow-up).

Rule 7's same-minute control becomes same-batch (Arch, 2026-10-23): main, the
main control and the candidate are rendered from their own trees and sent in
ONE batch, so they share a time window. Three steps:

  # in each tree (main, main again as the control, the candidate):
  venv/bin/python scripts/router_batch.py render --label main --samples 6 \\
      --phrase "..." --phrase "..." --out /tmp/reqs-main.jsonl
  # once, from any tree (a cap and a ledger are required; --dry-run sends nothing):
  venv/bin/python scripts/router_batch.py submit /tmp/reqs-*.jsonl --out /tmp/results.jsonl \\
      --cap-usd 8 --ledger /tmp/screen-ledger.json
  # in each tree again:
  venv/bin/python scripts/router_batch.py parse --requests /tmp/reqs-main.jsonl \\
      --results /tmp/results.jsonl --out report-main.md

``render`` builds exactly the request the live router sends on Anthropic (the
same system prompt, catalog prompt, model, max_tokens and temperature).
``parse`` validates each reply against that tree's own grammar. A reply that
fails validation is recorded as REFUSED: the live router would retry once with
a repair prompt, which a batch can't do, so the report counts them.

``submit`` refuses before anything is sent when the batch could cost more than
what is left under ``--cap-usd`` (CIO, 2026-11-15: a paid screen's stop is code,
not a plan). The ceiling is an upper estimate made without a provider call: each
request's text at 3 characters per token (the router prompt measures nearer 4)
plus its whole ``max_tokens`` as output, at the batch price. The ledger file
holds what the screen's earlier batches cost (the provider's own token counts
once a batch ends, the ceiling until then), so the cap covers the whole screen.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))


def _render(args) -> None:
    from services.intent_service.inversion_router import (
        _SYSTEM_PROMPT,
        TASK_TYPE,
        build_routing_prompt,
        derive_routing_grammar,
    )
    from services.llm.clients import _build_temperature_kwarg
    from services.llm.config import (
        MODEL_CONFIGS,
        LLMProvider,
        resolve_model,
        resolve_model_alias,
    )

    grammar = derive_routing_grammar()
    if args.corpus:
        import yaml

        corpus = yaml.safe_load(
            (ROOT / "tests" / "fixtures" / "inversion_corpus_phase0.yaml").read_text()
        )["corpus"]
        seen: set = set()
        args.phrase = [
            r["phrase"] for r in corpus if not (r["phrase"] in seen or seen.add(r["phrase"]))
        ]
    task = MODEL_CONFIGS.get(TASK_TYPE, MODEL_CONFIGS["reasoning"])
    model = resolve_model(LLMProvider.ANTHROPIC, TASK_TYPE)
    # --model overrides the configured router model for a screen of another
    # model on the same tree (the Haiku 5.5 screen, Arch 2026-10-30 14:54).
    # Harness only: the served router still resolves through config.py.
    model_id = getattr(args, "model", None) or model.value
    no_thinking = bool(getattr(args, "no_thinking", False))
    # ADR-083 arm C (screen harness only): every request carries the slot, rendered by
    # the served serializer from the served snapshot type, so the screened bytes are
    # the bytes the live consult would send with that list recorded.
    session_state = None
    last_list = getattr(args, "last_list", None)
    if last_list:
        from services.intent_service.inversion_router import SessionSnapshot as RouterSnapshot
        from services.intent_service.session_snapshot import (
            SessionSnapshot,
            serialize_for_prompt,
        )

        kind, _, lines = last_list.partition(":")
        block = serialize_for_prompt(
            SessionSnapshot(last_list_kind=kind, last_list_lines=int(lines))
        )
        session_state = RouterSnapshot(state_block=block)
    with open(args.out, "w") as f:
        for i, phrase in enumerate(args.phrase):
            prompt = build_routing_prompt(phrase, grammar, session_state)
            for n in range(1, args.samples + 1):
                params = {
                    "model": resolve_model_alias(model_id),
                    "max_tokens": task["max_tokens"],
                    **_build_temperature_kwarg(model_id, task["temperature"]),
                    **({"thinking": {"type": "disabled"}} if no_thinking else {}),
                    "system": _SYSTEM_PROMPT,
                    "messages": [{"role": "user", "content": prompt}],
                }
                cid = f"{args.label}-{i}-{n}"
                f.write(json.dumps({"custom_id": cid, "phrase": phrase, "params": params}) + "\n")
    print(f"rendered {len(args.phrase) * args.samples} requests -> {args.out}")


# Batch prices in USD per million tokens (input, output): half the standard price.
# claude-haiku-4-5 is $1 / $5 standard (services/llm/config.py). A model with no row
# here is refused: add its row with the source of the price.
_BATCH_USD_PER_MTOK = {"claude-haiku-4-5": (0.50, 2.50)}
# Characters per token used for the ceiling. Lower than the router prompt measures,
# so the ceiling overstates the input side.
_CEILING_CHARS_PER_TOKEN = 3.0


class CapRefused(SystemExit):
    """The batch was not sent: it could cost more than the cap leaves."""


def _batch_price(model: str) -> tuple:
    for name, price in _BATCH_USD_PER_MTOK.items():
        if model == name or model.startswith(name + "-"):
            return price
    raise CapRefused(
        f"REFUSED: no batch price recorded for model {model!r}. Nothing was sent. "
        "Add its row to _BATCH_USD_PER_MTOK with the source of the price."
    )


def _request_chars(params: dict) -> int:
    system = params.get("system") or ""
    chars = len(system) if isinstance(system, str) else len(json.dumps(system))
    for message in params.get("messages", []):
        content = message.get("content", "")
        chars += len(content) if isinstance(content, str) else len(json.dumps(content))
    return chars


def ceiling_usd(reqs: list) -> float:
    """An upper estimate of what these requests cost as one batch. No provider call."""
    total = 0.0
    for r in reqs:
        params = r["params"]
        usd_in, usd_out = _batch_price(params["model"])
        tokens_in = -(-_request_chars(params) // int(_CEILING_CHARS_PER_TOKEN))
        total += (tokens_in * usd_in + params["max_tokens"] * usd_out) / 1_000_000
    return total


def actual_usd(records: list, model_by_id: dict) -> float:
    """What a finished batch cost, from the provider's own token counts."""
    total = 0.0
    for rec in records:
        usage = rec.get("usage") or {}
        usd_in, usd_out = _batch_price(rec.get("model") or model_by_id[rec["custom_id"]])
        total += (
            (usage.get("input_tokens") or 0) * usd_in + (usage.get("output_tokens") or 0) * usd_out
        ) / 1_000_000
    return total


def _read_ledger(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {"entries": []}


def ledger_spent(ledger: dict) -> float:
    """Each earlier batch at its measured cost, or at its ceiling if it never reported."""
    return sum(
        e["actual_usd"] if e.get("actual_usd") is not None else e["ceiling_usd"]
        for e in ledger["entries"]
    )


def check_cap(reqs: list, cap_usd: float, ledger: dict) -> tuple:
    """Return (ceiling, spent) or raise CapRefused. Sends nothing."""
    ceiling = ceiling_usd(reqs)
    spent = ledger_spent(ledger)
    if spent + ceiling > cap_usd:
        raise CapRefused(
            f"REFUSED: this batch could cost up to ${ceiling:.2f}; ${spent:.2f} is already "
            f"counted against the ${cap_usd:.2f} cap. Nothing was sent."
        )
    return ceiling, spent


def _submit(args) -> None:
    from dev_key_binding import developer_keys_bound

    reqs = []
    for path in args.requests:
        for line in Path(path).read_text().splitlines():
            r = json.loads(line)
            reqs.append({"custom_id": r["custom_id"], "params": r["params"]})
    ids = [r["custom_id"] for r in reqs]
    assert len(ids) == len(set(ids)), "custom_id collision: give each tree a distinct --label"
    ledger_path = Path(args.ledger)
    ledger = _read_ledger(ledger_path)
    ceiling, spent = check_cap(reqs, args.cap_usd, ledger)
    print(
        f"PLANNED: {len(reqs)} requests in one batch on anthropic, at most ${ceiling:.2f}; "
        f"${spent:.2f} already counted of the ${args.cap_usd:.2f} cap. "
        "Nothing has been sent yet.",
        flush=True,
    )
    if args.dry_run:
        print("dry run: nothing sent, ledger unchanged")
        return
    model_by_id = {r["custom_id"]: r["params"]["model"] for r in reqs}
    with developer_keys_bound(providers=("anthropic",), require=True):
        from services.llm.request_key import anthropic_client_for_request

        client = anthropic_client_for_request()
        batch = client.messages.batches.create(requests=reqs)
        # Counted at its ceiling from the moment it is sent, so a run that dies while
        # waiting still counts against the cap.
        entry = {
            "batch": batch.id,
            "requests": len(reqs),
            "ceiling_usd": round(ceiling, 4),
            "actual_usd": None,
        }
        ledger["entries"].append(entry)
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")
        print(f"batch {batch.id}: {len(reqs)} requests submitted", flush=True)
        while True:
            b = client.messages.batches.retrieve(batch.id)
            if b.processing_status == "ended":
                break
            time.sleep(args.poll)
        records = []
        with open(args.out, "w") as f:
            for result in client.messages.batches.results(batch.id):
                rec = {"custom_id": result.custom_id, "type": result.result.type}
                if result.result.type == "succeeded":
                    msg = result.result.message
                    # Models that think by default put a thinking block first;
                    # the router reply is the text block (probe 2026-10-30).
                    rec["text"] = next((b.text for b in msg.content if b.type == "text"), "")
                    rec["blocks"] = [b.type for b in msg.content]
                    rec["model"] = msg.model
                    # #2149 step 3 (Arch 09:13): token counts come from the batch
                    # result's own usage, never estimated.
                    usage = getattr(msg, "usage", None)
                    if usage is not None:
                        rec["usage"] = {
                            "input_tokens": getattr(usage, "input_tokens", None),
                            "output_tokens": getattr(usage, "output_tokens", None),
                        }
                else:
                    rec["error"] = str(getattr(result.result, "error", result.result.type))
                records.append(rec)
                f.write(json.dumps(rec) + "\n")
        entry["actual_usd"] = round(actual_usd(records, model_by_id), 4)
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n")
    print(f"batch {batch.id} ended -> {args.out} ({b.request_counts})")
    print(
        f"COST: this batch ${entry['actual_usd']:.2f} from the provider's token counts "
        f"(ceiling was ${ceiling:.2f}); the screen so far ${ledger_spent(ledger):.2f} "
        f"of the ${args.cap_usd:.2f} cap."
    )


def _parse(args) -> None:
    from services.intent_service.inversion_router import (
        CLARIFY_ROUTE,
        NONE_ROUTE,
        _parse_and_validate,
        derive_routing_grammar,
    )

    grammar = derive_routing_grammar()
    reqs = {}
    for line in Path(args.requests).read_text().splitlines():
        r = json.loads(line)
        reqs[r["custom_id"]] = r
    label = next(iter(reqs)).rsplit("-", 2)[0]
    results = {}
    for line in Path(args.results).read_text().splitlines():
        r = json.loads(line)
        if r["custom_id"] in reqs:
            results[r["custom_id"]] = r
    rows = []
    for cid, req in reqs.items():
        res = results.get(cid)
        route, conf, served, err = "ERROR", None, "unresolved", None
        if res is None:
            err = "no result"
        elif res["type"] != "succeeded":
            err = res.get("error", res["type"])
        else:
            served = f"anthropic:{res.get('model')}"
            parsed, perr = _parse_and_validate(res["text"], grammar)
            if parsed is None:
                route, err = "REFUSED", perr
            elif parsed.get("outcome") == "plan":
                route = (
                    "PLAN["
                    + "→".join(str(o.get("operation", "?")) for o in parsed["operations"])
                    + "]"
                )
            else:
                op = parsed["operation"]
                route = "NONE" if op == NONE_ROUTE else "CLARIFY" if op == CLARIFY_ROUTE else op
                conf = parsed.get("confidence")
        rows.append(
            {
                "phrase": req["phrase"],
                "route": route,
                "confidence": conf,
                "served": served,
                "error": err,
            }
        )
    by_phrase: dict = defaultdict(list)
    for r in rows:
        by_phrase[r["phrase"]].append(r)
    served_c = Counter(r["served"] for r in rows)
    lines = [
        f"# Router batch — {label}",
        "",
        f"Parsed {datetime.now(timezone.utc):%Y-%m-%d %H:%MZ} · {len(rows)} requests · "
        f"{sum(1 for r in rows if r['route'] == 'REFUSED')} REFUSED (no repair in a batch) · "
        f"{sum(1 for r in rows if r['route'] == 'ERROR')} ERROR · served: "
        + "; ".join(f"{k} ({v}/{len(rows)})" for k, v in served_c.most_common()),
        "",
        "| phrase | routes (count) | confidence range |",
        "|---|---|---|",
    ]
    for phrase, rs in by_phrase.items():
        counts = Counter(r["route"] for r in rs)
        spread = ", ".join(f"`{k}` ×{v}" for k, v in counts.most_common())
        confs = [r["confidence"] for r in rs if isinstance(r["confidence"], (int, float))]
        rng = f"{min(confs):.2f}–{max(confs):.2f}" if confs else "-"
        lines.append(f"| {phrase} | {spread} | {rng} |")
    Path(args.out).write_text("\n".join(lines) + "\n")
    print(f"wrote {args.out}")


class ReplayLLM:
    """An ``llm_service`` for ``route()`` that answers from a finished batch.

    The scorer's full run uses it (``--replay-requests/--replay-results``), so a
    batched full run is scored by the SAME scorer code as a live one. A repair
    prompt gets the same (invalid) reply again, so it ends REFUSED: a batch
    can't repair.
    """

    def __init__(self, requests_path: str, results_path: str):
        by_id = {}
        for line in Path(results_path).read_text().splitlines():
            r = json.loads(line)
            by_id[r["custom_id"]] = r
        self._by_line: dict = {}
        for line in Path(requests_path).read_text().splitlines():
            req = json.loads(line)
            res = by_id.get(req["custom_id"])
            key = f"User message: {req['phrase']!r}"
            if res is not None and key not in self._by_line:
                self._by_line[key] = res

    async def complete(
        self,
        *,
        task_type,
        prompt,
        system=None,
        response_format=None,
        user_id=None,
        served=None,
        **_,
    ):
        # build_routing_prompt ends the first attempt with `User message: {utterance!r}`;
        # a repair prompt appends after it, so search every line.
        res = None
        for line in prompt.splitlines():
            if line.startswith("User message: "):
                res = self._by_line.get(line)
                break
        if res is None:
            raise RuntimeError("no batch result for this prompt")
        if res.get("type") != "succeeded":
            raise RuntimeError(res.get("error", res.get("type")))
        if served is not None:
            served["provider"] = "anthropic"
            served["model"] = res.get("model")
        return res["text"]


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render")
    r.add_argument("--label", required=True)
    r.add_argument("--samples", type=int, default=6)
    r.add_argument(
        "--model",
        default=None,
        help="model id to render instead of the configured router model (screen harness only)",
    )
    r.add_argument(
        "--no-thinking",
        action="store_true",
        help="send thinking={'type': 'disabled'} (models that think by default)",
    )
    r.add_argument("--phrase", action="append", default=[])
    r.add_argument(
        "--last-list",
        default=None,
        help="ADR-083 arm C: KIND:LINES, e.g. todos:7 (the slot on every request; harness only)",
    )
    r.add_argument(
        "--corpus", action="store_true", help="every phrase of the inversion corpus (a full run)"
    )
    r.add_argument("--out", required=True)
    s = sub.add_parser("submit")
    s.add_argument("requests", nargs="+")
    s.add_argument("--out", required=True)
    s.add_argument("--poll", type=int, default=20)
    s.add_argument(
        "--cap-usd",
        type=float,
        required=True,
        help="the screen's spend cap in USD; a batch that could pass it is refused unsent",
    )
    s.add_argument(
        "--ledger",
        required=True,
        help="JSON file holding what this screen's earlier batches cost (created if absent)",
    )
    s.add_argument(
        "--dry-run", action="store_true", help="print the planned line and stop; needs no key"
    )
    p = sub.add_parser("parse")
    p.add_argument("--requests", required=True)
    p.add_argument("--results", required=True)
    p.add_argument("--out", required=True)
    a = ap.parse_args()
    {
        "render": _render,
        "submit": _submit,
        "parse": _parse,
    }[a.cmd](a)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
