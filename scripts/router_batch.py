#!/usr/bin/env python3
"""Router screens through the Anthropic Message Batches API (half price; #2145 follow-up).

Rule 7's same-minute control becomes same-batch (Arch, 2026-10-23): main, the
main control and the candidate are rendered from their own trees and sent in
ONE batch, so they share a time window. Three steps:

  # in each tree (main, main again as the control, the candidate):
  venv/bin/python scripts/router_batch.py render --label main --samples 6 \\
      --phrase "..." --phrase "..." --out /tmp/reqs-main.jsonl
  # once, from any tree:
  venv/bin/python scripts/router_batch.py submit /tmp/reqs-*.jsonl --out /tmp/results.jsonl
  # in each tree again:
  venv/bin/python scripts/router_batch.py parse --requests /tmp/reqs-main.jsonl \\
      --results /tmp/results.jsonl --out report-main.md

``render`` builds exactly the request the live router sends on Anthropic (the
same system prompt, catalog prompt, model, max_tokens and temperature).
``parse`` validates each reply against that tree's own grammar. A reply that
fails validation is recorded as REFUSED: the live router would retry once with
a repair prompt, which a batch can't do, so the report counts them.

Env-strip per CLAUDE.md; keys come from the Keychain (dev_key_binding).

Two-stage runs (#2149 step 3; the router behind ``PIPER_INVERSION_TWO_STAGE``):
a two-stage turn is two dependent calls, so a batch run is two phases:
  venv/bin/python scripts/router_batch.py render-stage1 --label ts --samples 6 --corpus --out /tmp/s1-reqs.jsonl
  venv/bin/python scripts/router_batch.py submit /tmp/s1-reqs.jsonl --out /tmp/s1-res.jsonl
  venv/bin/python scripts/router_batch.py render-stage2 --requests /tmp/s1-reqs.jsonl --results /tmp/s1-res.jsonl --out /tmp/s2-reqs.jsonl
  venv/bin/python scripts/router_batch.py submit /tmp/s2-reqs.jsonl --out /tmp/s2-res.jsonl
  venv/bin/python scripts/router_batch.py parse-two-stage --s1-requests /tmp/s1-reqs.jsonl --s1-results /tmp/s1-res.jsonl \
      --s2-requests /tmp/s2-reqs.jsonl --s2-results /tmp/s2-res.jsonl --out report-ts.md
``parse-two-stage`` reconstructs every decision by running the REAL ``route()``
with the flag on against a replay of both batches (``TwoStageReplayLLM``), so
the parse is the production path, not a re-implementation; a repair prompt
gets the same reply again and ends REFUSED, as in the single-shot replay. The
report adds the stage-1 picks, the OTHER_GROUP and CLARIFY counts, and, with
``--expected``, the group-confusion table (expected group, from each phrase's
expected op through the enum, against the picked group).
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
    with open(args.out, "w") as f:
        for i, phrase in enumerate(args.phrase):
            prompt = build_routing_prompt(phrase, grammar)
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


def _submit(args) -> None:
    from dev_key_binding import developer_keys_bound

    reqs = []
    for path in args.requests:
        for line in Path(path).read_text().splitlines():
            r = json.loads(line)
            reqs.append({"custom_id": r["custom_id"], "params": r["params"]})
    ids = [r["custom_id"] for r in reqs]
    assert len(ids) == len(set(ids)), "custom_id collision: give each tree a distinct --label"
    with developer_keys_bound(require=True):
        from services.llm.request_key import anthropic_client_for_request

        client = anthropic_client_for_request()
        batch = client.messages.batches.create(requests=reqs)
        print(f"batch {batch.id}: {len(reqs)} requests submitted", flush=True)
        while True:
            b = client.messages.batches.retrieve(batch.id)
            if b.processing_status == "ended":
                break
            time.sleep(args.poll)
        with open(args.out, "w") as f:
            for entry in client.messages.batches.results(batch.id):
                rec = {"custom_id": entry.custom_id, "type": entry.result.type}
                if entry.result.type == "succeeded":
                    msg = entry.result.message
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
                    rec["error"] = str(getattr(entry.result, "error", entry.result.type))
                f.write(json.dumps(rec) + "\n")
    print(f"batch {batch.id} ended -> {args.out} ({b.request_counts})")


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


def _phrases(args) -> list:
    """The phrase list for a render: ``--phrase`` repeats, or every distinct corpus phrase."""
    if getattr(args, "corpus", False):
        import yaml

        corpus = yaml.safe_load(
            (ROOT / "tests" / "fixtures" / "inversion_corpus_phase0.yaml").read_text()
        )["corpus"]
        seen: set = set()
        return [r["phrase"] for r in corpus if not (r["phrase"] in seen or seen.add(r["phrase"]))]
    return list(args.phrase)


def _request_params(system: str, prompt: str, model_id: str, no_thinking: bool) -> dict:
    from services.intent_service.inversion_router import TASK_TYPE
    from services.llm.clients import _build_temperature_kwarg
    from services.llm.config import MODEL_CONFIGS, resolve_model_alias

    task = MODEL_CONFIGS.get(TASK_TYPE, MODEL_CONFIGS["reasoning"])
    return {
        "model": resolve_model_alias(model_id),
        "max_tokens": task["max_tokens"],
        **_build_temperature_kwarg(model_id, task["temperature"]),
        **({"thinking": {"type": "disabled"}} if no_thinking else {}),
        "system": system,
        "messages": [{"role": "user", "content": prompt}],
    }


def _tree_sha() -> str:
    """The sha of the tree this render runs in (Arch 2026-11-01 09:21: each arm's stage 1
    AND stage 2 are rendered from the arm's own tree, and the report says which)."""
    import subprocess

    try:
        return subprocess.run(
            ["git", "rev-parse", "--short=10", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (
        Exception
    ):  # silent-ok: a render outside a checkout still renders; the header then says "unknown"
        return "unknown"


def _router_model_id(args) -> str:
    from services.intent_service.inversion_router import TASK_TYPE
    from services.llm.config import LLMProvider, resolve_model

    return getattr(args, "model", None) or resolve_model(LLMProvider.ANTHROPIC, TASK_TYPE).value


def _render_stage1(args) -> None:
    """Phase 1 of a two-stage run: one stage-1 request per phrase per sample."""
    from services.intent_service.inversion_router import _STAGE1_SYSTEM_PROMPT, build_stage1_prompt

    phrases = _phrases(args)
    model_id = _router_model_id(args)
    no_thinking = bool(getattr(args, "no_thinking", False))
    tree = _tree_sha()
    with open(args.out, "w") as f:
        for i, phrase in enumerate(phrases):
            prompt = build_stage1_prompt(phrase)
            for n in range(1, args.samples + 1):
                rec = {
                    "custom_id": f"{args.label}-{i}-{n}",
                    "phrase": phrase,
                    "stage": 1,
                    "tree": tree,
                    "params": _request_params(_STAGE1_SYSTEM_PROMPT, prompt, model_id, no_thinking),
                }
                f.write(json.dumps(rec) + "\n")
    print(f"rendered {len(phrases) * args.samples} stage-1 requests -> {args.out}")


def _render_stage2(args) -> None:
    """Phase 2: one stage-2 request per stage-1 pick (per planned group for a plan).

    A stage-1 reply that fails ``_parse_stage1`` renders nothing (it is REFUSED at
    stage 1 and reported as such by ``parse-two-stage``); NONE and CLARIFY render
    nothing (decided at stage 1)."""
    from services.intent_service.inversion_router import (
        _STAGE2_SYSTEM_PROMPT,
        CLARIFY_ROUTE,
        NONE_ROUTE,
        _parse_stage1,
        build_stage2_prompt,
        derive_routing_grammar,
    )
    from services.shared_types import RouteGroup

    grammar = derive_routing_grammar()
    model_id = _router_model_id(args)
    no_thinking = bool(getattr(args, "no_thinking", False))
    tree = _tree_sha()
    results = {}
    for line in Path(args.results).read_text().splitlines():
        r = json.loads(line)
        results[r["custom_id"]] = r
    count = 0
    with open(args.out, "w") as f:
        for line in Path(args.requests).read_text().splitlines():
            req = json.loads(line)
            res = results.get(req["custom_id"])
            if res is None or res.get("type") != "succeeded":
                continue
            parsed, _err = _parse_stage1(res["text"])
            if parsed is None:
                continue
            if parsed.get("outcome") == "plan":
                parts = [(el["group"], el["text"]) for el in parsed["groups"]]
            elif parsed["group"] in (NONE_ROUTE, CLARIFY_ROUTE):
                continue
            else:
                parts = [(parsed["group"], None)]
            arm = getattr(args, "arm", None)
            for k, (group_name, part_text) in enumerate(parts):
                group = RouteGroup(group_name)
                prompt = build_stage2_prompt(req["phrase"], grammar, group, None, part_text)
                rec = {
                    # --arm prefixes the id so several arms can share one stage-1 result set
                    # (stage 1 names no op, so its prompts are identical across arms) and
                    # still submit in one batch.
                    # Batch custom_ids allow only [A-Za-z0-9_-], so the arm joins with "__".
                    "custom_id": (f"{arm}__" if arm else "") + f"{req['custom_id']}-s2-{k}",
                    "arm": arm,
                    "phrase": req["phrase"],
                    "stage": 2,
                    "tree": tree,
                    "parent": req["custom_id"],
                    "group": group.value,
                    "part_text": part_text,
                    "params": _request_params(_STAGE2_SYSTEM_PROMPT, prompt, model_id, no_thinking),
                }
                f.write(json.dumps(rec) + "\n")
                count += 1
    print(f"rendered {count} stage-2 requests -> {args.out}")


class TwoStageReplayLLM:
    """An ``llm_service`` for ``route()`` under the two-stage flag, answering ONE
    sample of ONE phrase from both finished batches.

    Stage is told by the system prompt object; a stage-2 call is matched by the
    group named on its first line and the plan part (if any) on its last line,
    never by the user's words. A repair prompt gets the same reply again, so an
    invalid reply ends REFUSED, as a batch can't repair."""

    def __init__(self, stage1: dict, stage2_by_key: dict):
        self._s1 = stage1  # a results record
        self._s2 = stage2_by_key  # {(group_value, part_text or None): results record}

    @staticmethod
    def _answer(res: dict, served) -> str:
        if res is None:
            raise RuntimeError("no batch result for this prompt")
        if res.get("type") != "succeeded":
            raise RuntimeError(res.get("error", res.get("type")))
        if served is not None:
            served["provider"] = "anthropic"
            served["model"] = res.get("model")
        return res["text"]

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
        import ast

        from services.intent_service.inversion_router import _STAGE1_SYSTEM_PROMPT

        if system == _STAGE1_SYSTEM_PROMPT:
            return self._answer(self._s1, served)
        group = None
        part = None
        for line in prompt.splitlines():
            if line.startswith("Operations in the ") and group is None:
                group = line[len("Operations in the ") :].split(" group", 1)[0]
            elif line.startswith("Route only this part of the message now: "):
                part = ast.literal_eval(line[len("Route only this part of the message now: ") :])
        return self._answer(self._s2.get((group, part)), served)


def _parse_two_stage(args) -> None:
    """Reconstruct every two-stage decision through the real ``route()`` and report."""
    import asyncio
    import os

    from services.intent_service.inversion_router import derive_routing_grammar, route

    grammar = derive_routing_grammar()
    s1_res = {
        json.loads(l)["custom_id"]: json.loads(l)
        for l in Path(args.s1_results).read_text().splitlines()
    }
    s2_res = {
        json.loads(l)["custom_id"]: json.loads(l)
        for l in Path(args.s2_results).read_text().splitlines()
    }
    s2_by_parent: dict = defaultdict(dict)
    for line in Path(args.s2_requests).read_text().splitlines():
        req = json.loads(line)
        s2_by_parent[req["parent"]][(req["group"], req.get("part_text"))] = s2_res.get(
            req["custom_id"]
        )
    expected: dict = {}
    if getattr(args, "expected", None):
        import yaml

        corpus = yaml.safe_load(Path(args.expected).read_text())
        rows_in = corpus["corpus"] if isinstance(corpus, dict) and "corpus" in corpus else corpus
        for r in rows_in:
            op = next(
                (r[k] for k in ("expected_action", "expected_op", "action", "expected") if k in r),
                None,
            )
            if isinstance(op, str) and r.get("phrase") not in expected:
                # The phase-0 corpus writes `action:<op>`, `floor`, `plan`, `REVIEW` (unscored)
                # or `category:<X>`; the first maps to a group, the rest are their own buckets.
                expected[r["phrase"]] = op[len("action:") :] if op.startswith("action:") else op
    group_of = {
        op.name: (op.route_group.value if op.route_group else None) for op in grammar.operations
    }

    def _usage(res) -> tuple:
        u = (res or {}).get("usage") or {}
        return (u.get("input_tokens") or 0, u.get("output_tokens") or 0)

    s1_trees = Counter(
        json.loads(l).get("tree", "unknown")
        for l in Path(args.s1_requests).read_text().splitlines()
    )
    s2_trees = Counter(
        json.loads(l).get("tree", "unknown")
        for l in Path(args.s2_requests).read_text().splitlines()
    )
    arms = Counter(
        json.loads(l).get("arm") for l in Path(args.s2_requests).read_text().splitlines()
    )

    label = None
    rows = []
    prev = os.environ.get("PIPER_INVERSION_TWO_STAGE")
    os.environ["PIPER_INVERSION_TWO_STAGE"] = "1"
    try:
        for line in Path(args.s1_requests).read_text().splitlines():
            req = json.loads(line)
            label = label or req["custom_id"].rsplit("-", 2)[0]
            replay = TwoStageReplayLLM(
                s1_res.get(req["custom_id"]), s2_by_parent.get(req["custom_id"], {})
            )
            decision = asyncio.run(
                route(req["phrase"], None, llm_service=replay, grammar=grammar, user_id=None)
            )
            served = next((m for m in [decision.served_model] if m), None)
            s1_in, s1_out = _usage(s1_res.get(req["custom_id"]))
            s2_in = sum(_usage(r)[0] for r in s2_by_parent.get(req["custom_id"], {}).values())
            s2_out = sum(_usage(r)[1] for r in s2_by_parent.get(req["custom_id"], {}).values())
            rows.append(
                {
                    "phrase": req["phrase"],
                    "route": decision.route_label,
                    "outcome": decision.outcome,
                    "group": decision.route_group,
                    "llm_calls": decision.llm_calls,
                    "served": f"anthropic:{served}" if served else "unresolved",
                    "error": decision.error,
                    "metrics": decision.stage_metrics or [],
                    "tokens": {"s1_in": s1_in, "s1_out": s1_out, "s2_in": s2_in, "s2_out": s2_out},
                }
            )
    finally:
        if prev is None:
            os.environ.pop("PIPER_INVERSION_TWO_STAGE", None)
        else:
            os.environ["PIPER_INVERSION_TWO_STAGE"] = prev

    by_phrase: dict = defaultdict(list)
    for r in rows:
        by_phrase[r["phrase"]].append(r)
    served_c = Counter(r["served"] for r in rows)
    stage1_picks = Counter((r["group"] or "REFUSED/ERROR") for r in rows)
    other_group = sum(
        1
        for r in rows
        for m in r["metrics"]
        if m.get("stage") == 2 and m.get("pick") == "OTHER_GROUP"
    )
    stage2_clarify = sum(
        1 for r in rows for m in r["metrics"] if m.get("stage") == 2 and m.get("pick") == "CLARIFY"
    )
    refused = sum(1 for r in rows if r["outcome"] == "refused")
    errors = sum(1 for r in rows if r["outcome"] == "error")
    lines = [
        f"# Router batch, two-stage — {label}"
        + (f" · arm {', '.join(str(a) for a in arms if a)}" if any(arms) else ""),
        "",
        f"Parsed {datetime.now(timezone.utc):%Y-%m-%d %H:%MZ} · {len(rows)} decisions · "
        f"{refused} REFUSED (no repair in a batch) · {errors} ERROR · served: "
        + "; ".join(f"{k} ({v}/{len(rows)})" for k, v in served_c.most_common()),
        "",
        "Rendered from: stage 1 tree "
        + ", ".join(f"`{k}` ({v})" for k, v in s1_trees.most_common())
        + " · stage 2 tree "
        + (", ".join(f"`{k}` ({v})" for k, v in s2_trees.most_common()) or "(no stage-2 requests)")
        + (
            ""
            if set(s1_trees) == set(s2_trees) or not s2_trees
            else " · **stage 1 and stage 2 trees differ: not one arm**"
        ),
        "",
        "## Stage 1 picks",
        "",
        "| pick | count |",
        "|---|---|",
    ]
    lines += [f"| {k} | {v} |" for k, v in stage1_picks.most_common()]
    tok = {k: sum(r["tokens"][k] for r in rows) for k in ("s1_in", "s1_out", "s2_in", "s2_out")}
    lines += [
        "",
        f"Tokens (from the batch results' usage; 0 when a result carries none): "
        f"stage 1 in {tok['s1_in']} / out {tok['s1_out']} · stage 2 in {tok['s2_in']} / out {tok['s2_out']} · "
        f"per decision in {(tok['s1_in'] + tok['s2_in']) / max(len(rows), 1):.0f} / "
        f"out {(tok['s1_out'] + tok['s2_out']) / max(len(rows), 1):.0f}",
        "",
        f"Stage 2: OTHER_GROUP {other_group} · CLARIFY {stage2_clarify} "
        f"(stage-1 error rate, OTHER_GROUP over decisions that reached stage 2: "
        f"{other_group}/{sum(1 for r in rows if any(m.get('stage') == 2 for m in r['metrics']))})",
        "",
        "## Decisions",
        "",
        "| phrase | routes (count) | stage-1 group (count) | llm_calls |",
        "|---|---|---|---|",
    ]
    for phrase, rs in by_phrase.items():
        counts = Counter(r["route"] for r in rs)
        groups = Counter(str(r["group"]) for r in rs)
        spread = ", ".join(f"`{k}` ×{v}" for k, v in counts.most_common())
        gspread = ", ".join(f"`{k}` ×{v}" for k, v in groups.most_common())
        calls = ", ".join(str(r["llm_calls"]) for r in rs)
        lines.append(f"| {phrase} | {spread} | {gspread} | {calls} |")
    if expected:
        confusion: Counter = Counter()
        for r in rows:
            exp_op = expected.get(r["phrase"])
            if not exp_op:
                exp_group = "n/a"
            elif exp_op in group_of:
                exp_group = group_of[exp_op]
            elif exp_op in ("NONE", "CLARIFY", "floor", "plan"):
                exp_group = exp_op
            else:
                exp_group = "n/a"  # REVIEW rows and category-only expectations are unscored here
            picked = r["group"] or "REFUSED/ERROR"
            confusion[(str(exp_group), str(picked).split(",")[0])] += 1
        lines += [
            "",
            "## Group confusion (expected group × picked stage-1 group)",
            "",
            "| expected | picked | count |",
            "|---|---|---|",
        ]
        lines += [
            f"| {e} | {p} | {c} |"
            for (e, p), c in sorted(confusion.items(), key=lambda kv: (-kv[1], kv[0]))
        ]
        agree = sum(c for (e, p), c in confusion.items() if e == p)
        lines += ["", f"Agreement: {agree}/{sum(confusion.values())}"]
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
        "--corpus", action="store_true", help="every phrase of the inversion corpus (a full run)"
    )
    r.add_argument("--out", required=True)
    s = sub.add_parser("submit")
    s.add_argument("requests", nargs="+")
    s.add_argument("--out", required=True)
    s.add_argument("--poll", type=int, default=20)
    p = sub.add_parser("parse")
    p.add_argument("--requests", required=True)
    p.add_argument("--results", required=True)
    p.add_argument("--out", required=True)
    s1 = sub.add_parser("render-stage1", help="two-stage phase 1 (#2149 step 3)")
    s1.add_argument("--label", required=True)
    s1.add_argument("--samples", type=int, default=6)
    s1.add_argument("--model", default=None)
    s1.add_argument("--no-thinking", action="store_true")
    s1.add_argument("--phrase", action="append", default=[])
    s1.add_argument("--corpus", action="store_true")
    s1.add_argument("--out", required=True)
    s2 = sub.add_parser("render-stage2", help="two-stage phase 2, from the stage-1 picks")
    s2.add_argument("--requests", required=True, help="the stage-1 requests file")
    s2.add_argument("--results", required=True, help="the stage-1 results file")
    s2.add_argument("--model", default=None)
    s2.add_argument("--no-thinking", action="store_true")
    s2.add_argument(
        "--arm",
        default=None,
        help="prefix for this arm's stage-2 ids when several arms share one stage-1 result set",
    )
    s2.add_argument("--out", required=True)
    pt = sub.add_parser("parse-two-stage", help="reconstruct decisions through route() and report")
    pt.add_argument("--s1-requests", required=True)
    pt.add_argument("--s1-results", required=True)
    pt.add_argument("--s2-requests", required=True)
    pt.add_argument("--s2-results", required=True)
    pt.add_argument("--expected", default=None, help="a corpus YAML for the group-confusion table")
    pt.add_argument("--out", required=True)
    a = ap.parse_args()
    {
        "render": _render,
        "submit": _submit,
        "parse": _parse,
        "render-stage1": _render_stage1,
        "render-stage2": _render_stage2,
        "parse-two-stage": _parse_two_stage,
    }[a.cmd](a)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
