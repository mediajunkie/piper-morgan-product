#!/usr/bin/env python3
"""Inversion Phase-0 baseline (#1595) — score the CURRENT router per category.

m-43 (name the layer): this runner has two modes measuring two different
things, and says so in its output:

  --surface1  (default) Deterministic. For each corpus row, what does
              PreClassifier.pre_classify claim? Reports claim-rate and,
              where the row asserts an expected destination, agreement.
              NO LLM runs. This is "what surface 1 does", not "what the
              user gets" — rows surface 1 declines fall to the LLM in
              production, which this mode does NOT execute.

  --full      The production decision: IntentClassifier.classify with the
              pre-classifier active (surface 1 wins where it claims, LLM
              otherwise). Requires LLM keys; costs one call per undeclined
              row. This IS "what the user gets" at the classification layer
              (rails/floor still downstream).

Per-category tables always state denominators (m-44). REVIEW rows are
reported as a separate bucket — they are questions, not passes or failures,
and folding them into a score would manufacture either optimism or alarm.

Usage:
  POSTGRES_PORT=5433 venv/bin/python scripts/inversion_phase0_baseline.py [--full] [--out PATH]
"""

import argparse
import asyncio
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

CORPUS = ROOT / "tests" / "fixtures" / "inversion_corpus_phase0.yaml"


def load_corpus() -> list:
    rows, cur = [], None
    for raw in CORPUS.read_text().splitlines():
        m = re.match(r'  - phrase: "(.*)"$', raw)
        if m:
            if cur:
                rows.append(cur)
            cur = {"phrase": m.group(1).replace('\\"', '"')}
            continue
        if cur is None:
            continue
        for key in ("category", "expected"):
            m = re.match(rf"    {key}: (\S+)$", raw)
            if m:
                cur[key] = m.group(1)
        m = re.match(r'    (source|surface1_claim|probe_verdict|notes): "(.*)"$', raw)
        if m:
            cur[m.group(1)] = m.group(2)
    if cur:
        rows.append(cur)
    return rows


_RAIL = None


def _rail():
    """alias -> shared entry point, REGISTRY-DERIVED (Arch condition: aliases
    are input-side; two names sharing a rail entry are the same operation —
    exact-name matching under-credits, e.g. set_reminder IS create_reminder)."""
    global _RAIL
    if _RAIL is None:
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        _RAIL = get_action_workflows()
    return _RAIL


def same_operation(a: str, b: str) -> bool:
    if a == b:
        return True
    ea, eb = _rail().get(a), _rail().get(b)
    return ea is not None and eb is not None and ea.entry_point == eb.entry_point


def matches(expected: str, category, action) -> bool:
    cat = (category.value if hasattr(category, "value") else str(category or "")).lower()
    act = str(action or "").lower()
    if expected.startswith("action:"):
        return same_operation(act, expected.split(":", 1)[1].lower())
    if expected.startswith("category:"):
        return cat == expected.split(":", 1)[1].lower()
    return False


async def run(full: bool, out: Path | None) -> None:
    from services.intent_service.pre_classifier import PreClassifier

    pre = PreClassifier()
    classifier = None
    if full:
        from services.intent_service.classifier import IntentClassifier
        from services.llm.clients import LLMClient

        # #322: pass llm_service via constructor (the container is per-app,
        # NOT a singleton — a fresh ServiceContainer() here would stay
        # uninitialized from the classifier's lazy access). Same shape the
        # surface-1 counterfactual probe used for its 52 calls.
        classifier = IntentClassifier(llm_service=LLMClient())

    rows = load_corpus()
    results = []
    for r in rows:
        phrase = r["phrase"]
        claimed = pre.pre_classify(phrase)
        entry = dict(r)
        entry["s1_claimed"] = claimed is not None
        if claimed is not None:
            entry["s1_result"] = f"{claimed.category.value}/{claimed.action}"
            entry["decision"] = (claimed.category, claimed.action)
        if full:
            if claimed is None:
                try:
                    intent = await classifier.classify(phrase, use_cache=False)
                    entry["decision"] = (intent.category, intent.action)
                    entry["llm_result"] = f"{intent.category.value}/{intent.action}"
                except Exception as e:  # probe discipline: ERROR is recorded, never a faked verdict
                    entry["llm_result"] = f"ERROR({type(e).__name__})"
                    entry["error"] = str(e)[:200]
            # claimed rows: surface 1 IS the production decision
        results.append(entry)

    mode = "FULL CHAIN (production decision)" if full else "SURFACE-1 ONLY (claims, not outcomes)"
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")
    lines = [
        f"# Inversion Phase-0 baseline — {mode}",
        f"Run: {stamp} · corpus: {CORPUS.name} ({len(rows)} rows) · scripts/inversion_phase0_baseline.py",
        "",
        "LAYER (m-43): "
        + (
            "full classification chain — surface 1 where it claims, LLM otherwise. "
            "Rails/floor are downstream and NOT measured here."
            if full
            else "surface-1 claims only. Unclaimed rows fall to the LLM in production, "
            "which this run did NOT execute — claim-rate is not a correctness rate."
        ),
        "",
    ]

    per_cat = defaultdict(lambda: {"n": 0, "review": 0, "asserted": 0, "match": 0, "claimed": 0})
    for e in results:
        c = per_cat[e["category"]]
        c["n"] += 1
        if e["s1_claimed"]:
            c["claimed"] += 1
        if e["expected"] == "REVIEW":
            c["review"] += 1
        else:
            c["asserted"] += 1
            if "decision" in e and matches(e["expected"], *e["decision"]):
                c["match"] += 1

    lines.append("## Per-category (denominators stated — m-44)")
    lines.append("")
    lines.append(
        "| category | rows | s1-claimed | asserted-expected | match | REVIEW (open questions) |"
    )
    lines.append("|---|---|---|---|---|---|")
    tot = {"n": 0, "review": 0, "asserted": 0, "match": 0, "claimed": 0}
    for cat in sorted(per_cat, key=lambda c: -per_cat[c]["n"]):
        c = per_cat[cat]
        for k in tot:
            tot[k] += c[k]
        note = "—" if not full and c["asserted"] > c["claimed"] else ""
        lines.append(
            f"| {cat} | {c['n']} | {c['claimed']} | {c['asserted']} | "
            f"{c['match']}{'*' if note else ''} | {c['review']} |"
        )
    lines.append(
        f"| **TOTAL** | {tot['n']} | {tot['claimed']} | {tot['asserted']} | {tot['match']} | {tot['review']} |"
    )
    if not full:
        lines.append("")
        lines.append(
            "*surface-1-only: an asserted row surface 1 declines shows as non-match here "
            "while production may still route it correctly via the LLM — run --full for the "
            "production number. This table CANNOT be read as a correctness score.*"
        )

    lines.append("")
    lines.append("## Row detail")
    lines.append("")
    lines.append("| phrase | category | expected | s1 | decision | verdict | source |")
    lines.append("|---|---|---|---|---|---|---|")
    for e in results:
        s1 = e.get("s1_result", "declined")
        dec = e.get("llm_result", e.get("s1_result", "—" if not full else "?"))
        if e["expected"] == "REVIEW":
            verdict = "REVIEW"
        elif "decision" in e:
            verdict = "MATCH" if matches(e["expected"], *e["decision"]) else "MISMATCH"
        elif e.get("error"):
            verdict = "ERROR"
        else:
            verdict = "unmeasured (s1 declined; no LLM this mode)"
        lines.append(
            f"| {e['phrase'][:60]} | {e['category']} | {e['expected']} | {s1} | {dec} | {verdict} | {e['source'][:50]} |"
        )

    text = "\n".join(lines) + "\n"
    if out:
        out.write_text(text)
        print(f"wrote {out}")
    # console summary
    print(
        f"{mode}: {tot['n']} rows · s1 claimed {tot['claimed']} · "
        f"asserted {tot['asserted']} · matched {tot['match']} · REVIEW {tot['review']}"
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    asyncio.run(run(args.full, args.out))
