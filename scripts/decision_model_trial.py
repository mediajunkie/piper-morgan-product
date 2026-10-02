#!/usr/bin/env python3
"""Decision-model trial (research hub Q1, standing item 8f) — Laya vs the Phase-1 Haiku router.

RESEARCH HARNESS, READ-ONLY. PM cleared it 2026-10-01 to run CIO-side "if it does not distract or
divert Lead's critical path": it imports the router's grammar and the shadow scorer's matching rules,
never edits them, and touches nothing in services/. Write-up:
docs/internal/research/decision-models-vs-llms-first-read-2026-09-28.md (trial log).

What it measures (m-43, name the layer): operation selection ONLY, context-free, on exactly the rows
the recorded Haiku run scored with a confidence (Lead's 2026-10-01 shadow-score report). Laya returns
no args and no plans, so this compares the one decision both systems make. Scoring reuses
scripts/inversion_phase1_shadow_score.py::router_matches unchanged, so MATCH means the same thing as
in Lead's reports (alias-aware, FLOOR-disposition-aware).

Arms:
  shortlist — laya.predict_shortlist (the vendor's high-cardinality path: embed-rank to k, then choose)
  flat      — one 64-way choice with head_max_len raised (the report says whether any options were truncated)

Run (outside the repo's venv; an isolated env with requirements.txt + `pip install laya`):
  ~/.cache/piper-morgan/trial-env/bin/python scripts/decision_model_trial.py --arm shortlist --out PATH
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

BASELINE = (
    ROOT
    / "docs/internal/architecture/current/inversion-phase1-shadow-score-2026-10-01-delete-desc-after.md"
)
INSTRUCTIONS = "Which operation does the user's message ask Piper (a PM assistant) to perform?"


def baseline_rows() -> list[dict]:
    """The recorded Haiku run's asserted rows that carry a confidence (the comparison set)."""
    lines = BASELINE.read_text().split("\n")
    i = lines.index("## Row detail (asserted rows)")
    out = []
    for line in lines[i + 4 :]:
        if not line.startswith("|"):
            break
        c = [x.strip() for x in line.strip("|").split("|")]
        m = re.search(r"@\s*([0-9.]+)", c[3])
        if m:
            out.append(
                {
                    "phrase": c[0].replace("\\|", "|"),
                    "category": c[1],
                    "expected": c[2],
                    "haiku_match": c[4] == "MATCH",
                    "haiku_conf": float(m.group(1)),
                }
            )
    return out


def criteria() -> dict[str, str]:
    from services.intent_service.inversion_router import derive_routing_grammar

    crit = {}
    for op in derive_routing_grammar().operations:
        desc = (op.description or op.name.replace("_", " ")).strip()
        crit[op.name] = desc[:160]  # bounded per-label text; full descriptions overflow the head
    return crit


def auroc(pos: list[float], neg: list[float]) -> float:
    if not pos or not neg:
        return float("nan")
    return sum((a > b) + 0.5 * (a == b) for a in pos for b in neg) / (len(pos) * len(neg))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", choices=("shortlist", "flat"), required=True)
    ap.add_argument("--k", type=int, default=12)
    ap.add_argument("--head-max-len", type=int, default=448)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()

    import laya
    from inversion_phase1_shadow_score import _op_category_map, router_matches

    rows = baseline_rows()
    if a.limit:
        rows = rows[: a.limit]
    crit = criteria()
    opcat = _op_category_map()
    agent = laya.load("convaiinnovations/laya")
    q = {"op": {"type": "choice", "instructions": INSTRUCTIONS, "criteria": crit}}
    embed = laya.embed_fn_from_agent(agent) if a.arm == "shortlist" else None

    results = []
    for r in rows:
        if a.arm == "shortlist":
            res = laya.predict_shortlist(agent, r["phrase"], q, embed, k=a.k)
        else:
            res = agent.predict(r["phrase"], q, head_max_len=a.head_max_len)
        ans = res["answers"]["op"]
        dec = SimpleNamespace(
            outcome="operation", operation=ans["choice"], route_label=ans["choice"]
        )
        ok, note = router_matches(r["expected"], dec, opcat)
        results.append(
            {
                **r,
                "laya_choice": ans["choice"],
                "laya_conf": ans.get("confidence"),
                "laya_answer_conf": ans.get("answer_confidence"),
                "laya_match": bool(ok),
                "note": note,
                "truncated": bool(res.get("usage", {}).get("truncated_questions")),
            }
        )

    n = len(results)
    lm = sum(x["laya_match"] for x in results)
    hm = sum(x["haiku_match"] for x in results)
    summ = {
        "arm": a.arm,
        "k": a.k if a.arm == "shortlist" else None,
        "head_max_len": a.head_max_len if a.arm == "flat" else None,
        "rows": n,
        "laya_top1": f"{lm}/{n}",
        "haiku_top1_same_rows": f"{hm}/{n}",
        "rows_with_truncated_options": sum(x["truncated"] for x in results),
        "auroc_laya_confidence": round(
            auroc(
                [x["laya_conf"] for x in results if x["laya_match"]],
                [x["laya_conf"] for x in results if not x["laya_match"]],
            ),
            3,
        ),
        "auroc_laya_answer_confidence": round(
            auroc(
                [x["laya_answer_conf"] for x in results if x["laya_match"]],
                [x["laya_answer_conf"] for x in results if not x["laya_match"]],
            ),
            3,
        ),
        "auroc_haiku_self_conf": round(
            auroc(
                [x["haiku_conf"] for x in results if x["haiku_match"]],
                [x["haiku_conf"] for x in results if not x["haiku_match"]],
            ),
            3,
        ),
    }
    a.out.write_text(json.dumps({"summary": summ, "rows": results}, indent=1))
    print(json.dumps(summ, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
