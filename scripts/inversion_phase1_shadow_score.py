#!/usr/bin/env python3
"""Inversion Phase-1 shadow score (#1595) — score the CONSTRAINED ROUTER
against the Phase-0 corpus, per category, vs the Phase-0 FULL-CHAIN baseline.

m-43 (name the layer): this run measures the INVERSION ROUTER ONLY —
``inversion_router.route`` with an EMPTY session snapshot (the corpus rows are
stored context-free; the 1529 offer/flow rows are context-DEPENDENT and their
router answers here are therefore informational, not the router's Phase-2
shape). The production chain is NOT executed in this run; the baseline column
is the Phase-0 FULL-CHAIN production decision
(docs/internal/architecture/current/inversion-phase0-baseline-full-2026-08-12.md).

Scoring reuses the Phase-0 scorer's idioms unchanged so the numbers are
comparable:
  - registry-alias-aware operation matching via the shared rail entry points
    (``same_operation`` — exact-name matching under-credits;
    set_reminder IS create_reminder);
  - per-category tables with stated denominators (m-44);
  - ERROR recorded, never a faked verdict;
  - REVIEW rows reported as their own bucket — they are the Inversion's
    question book, recorded as data, folded into NO score.

``category:`` expectations (the router emits operations, not categories) are
scored by resolving the router's operation to its ACTION_REGISTRY category
(alias→canonical first); an operation with no registry category scores
NO-MATCH with an annotation rather than a silent pass — a gate that cannot
see a row must say so (m-44).

Usage (env-stripped per CLAUDE.md; keys resolve via Keychain):

    env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \
      -u ANTHROPIC_CUSTOM_HEADERS POSTGRES_PORT=5433 \
      venv/bin/python scripts/inversion_phase1_shadow_score.py \
      [--dry-run] [--out PATH]

Cost: one Haiku-class call per corpus row (93), plus at most one repair retry
per row. --dry-run validates corpus + grammar + row selections, no LLM calls.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Awaitable, Callable, Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import inversion_phase0_baseline as p0  # noqa: E402  (shared corpus + matching idioms)

DEFAULT_OUT = (
    ROOT
    / "docs"
    / "internal"
    / "architecture"
    / "current"
    / f"inversion-phase1-shadow-score-{datetime.now(timezone.utc):%Y-%m-%d}.md"
)

DEMANDED_ROW = "what reminders do I have?"  # Arch's one demand — must be present

# Exhibit-A selection rule: the 8 rows sourced from PM's 2026-08-08 13:19–13:24
# live transcript — corpus sources exhibit-a/* (offer-binding/flow-escape/1530)
# plus issue-1559 (reminder adjacency) and issue-1492 (archive extraction ×3).
_EXHIBIT_SOURCE_TOKENS = ("exhibit-a", "issue-1559", "issue-1492")

# Phase-0 FULL-CHAIN baseline, per category: (asserted, matched). Source:
# inversion-phase0-baseline-full-2026-08-12.md (run 2026-08-12 19:42Z). The
# gate (Arch condition 1 as amended, PPM): NO category regresses — never
# aggregate. Categories with asserted == 0 have REVIEW-only denominators and
# CANNOT be gated (stated, not skipped silently — the M2 lesson).
PHASE0_BASELINE: dict[str, tuple[int, int]] = {
    "QUERY": (12, 12),
    "EXECUTION": (6, 5),
    "PORTFOLIO": (7, 6),
    "TEMPORAL": (4, 4),
    "GUIDANCE": (1, 1),
    "CONVERSATION": (0, 0),
    "STATUS": (2, 1),
    "PRIORITY": (2, 2),
    "IDENTITY": (2, 2),
    "SYNTHESIS": (2, 2),
    "MEMORY": (1, 1),
    "DISCOVERY": (0, 0),
    "PROVENANCE": (0, 0),
    "TRUST": (0, 0),
    "ANALYSIS": (0, 0),
}


def _op_category_map() -> dict[str, str]:
    """action/operation → registry category (alias-resolved), for scoring
    ``category:`` expectations against a router OPERATION."""
    from services.intent_service.action_registry import ACTION_REGISTRY
    from services.intent_service.inversion_router import derive_routing_grammar

    grammar = derive_routing_grammar()
    canon = dict(grammar.alias_to_canonical)
    by_action: dict[str, str] = {}
    for (category, action), _ in ACTION_REGISTRY.items():
        by_action.setdefault(action, category)
        # credit the rail canonical for a registry alias and vice versa
        c = canon.get(action)
        if c:
            by_action.setdefault(c, category)
    return by_action


def router_matches(expected: str, decision, op_categories: dict[str, str]) -> tuple[bool, str]:
    """Score one asserted row. Returns (matched, annotation)."""
    if decision is None or decision.outcome == "error":
        return False, "ERROR"
    if decision.outcome == "refused":
        return False, "REFUSED"
    if decision.outcome in ("none", "clarify"):
        return False, decision.outcome.upper()
    op = decision.operation or ""
    if expected.startswith("action:"):
        return p0.matches(expected, "", op), ""
    if expected.startswith("category:"):
        want = expected.split(":", 1)[1].upper()
        got = op_categories.get(op)
        if got is None:
            return False, "no-registry-category-for-operation"
        return got.upper() == want, ""
    return False, "unknown-expectation-shape"


async def route_all(
    rows: list[dict],
    router_fn: Callable[[str], Awaitable],
    progress: bool = True,
) -> list:
    """Route every row; an exception on a row is recorded as an ERROR decision
    (never faked, never aborts the run)."""
    from services.intent_service.inversion_router import RoutingDecision

    decisions = []
    for i, r in enumerate(rows, 1):
        try:
            d = await router_fn(r["phrase"])
        except Exception as e:  # probe discipline: ERROR recorded, run continues
            d = RoutingDecision(outcome="error", error=f"{type(e).__name__}: {e}")
        decisions.append(d)
        if progress:
            label = d.route_label if hasattr(d, "route_label") else "?"
            print(f"[{i}/{len(rows)}] {label:<28} {r['phrase'][:60]!r}")
    return decisions


def score(rows: list[dict], decisions: list) -> dict:
    """Per-category scoring with stated denominators. Pure — testable."""
    op_categories = _op_category_map()
    per_cat: dict[str, dict] = defaultdict(
        lambda: {"n": 0, "asserted": 0, "match": 0, "review": 0, "errors": 0}
    )
    row_results = []
    for r, d in zip(rows, decisions):
        c = per_cat[r["category"]]
        c["n"] += 1
        verdict, note = "", ""
        if getattr(d, "outcome", "error") == "error":
            c["errors"] += 1
        if r["expected"] == "REVIEW":
            c["review"] += 1
            verdict = "REVIEW"
        else:
            c["asserted"] += 1
            ok, note = router_matches(r["expected"], d, op_categories)
            if ok:
                c["match"] += 1
                verdict = "MATCH"
            else:
                verdict = "ERROR" if note == "ERROR" else "MISMATCH"
        row_results.append({"row": r, "decision": d, "verdict": verdict, "note": note})
    return {"per_cat": dict(per_cat), "rows": row_results}


def select_exhibit_rows(row_results: list[dict]) -> list[dict]:
    return [
        rr
        for rr in row_results
        if any(tok in rr["row"].get("source", "") for tok in _EXHIBIT_SOURCE_TOKENS)
    ]


def served_summary(decisions: list) -> str:
    """#1620: the RESOLVED provider+model that actually answered each routed
    row, after fallback — never the configured/requested one. Cross-run
    same-model comparability (run N vs run N+1) is otherwise inferred, not
    proven (m-43: the served model is part of the measurement's layer)."""
    counts: defaultdict[str, int] = defaultdict(int)
    for d in decisions:
        provider = getattr(d, "served_provider", None)
        model = getattr(d, "served_model", None)
        key = f"{provider}:{model}" if provider and model else "unresolved (no successful call)"
        counts[key] += 1
    if not counts:
        return "no rows routed"
    return "; ".join(
        f"{k} ({v}/{len(decisions)})" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])
    )


def build_report(scored: dict, grammar, llm_note: str, served_note: str) -> str:
    per_cat = scored["per_cat"]
    row_results = scored["rows"]
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")
    n_ops = len(grammar.operations)
    n_aliases = sum(len(op.aliases) for op in grammar.operations)

    lines = [
        "# Inversion Phase-1 shadow score — CONSTRAINED ROUTER vs Phase-0 baseline",
        f"Run: {stamp} · corpus: inversion_corpus_phase0.yaml ({len(row_results)} rows) · "
        "scripts/inversion_phase1_shadow_score.py",
        f"Served (#1620 — resolved, post-fallback, per row): {served_note}",
        "",
        "LAYER (m-43): **router only, context-free** — one constrained "
        f"Haiku-class call per row ({llm_note}), grammar derived from the live "
        f"registry at run time ({n_ops} canonical operations, {n_aliases} "
        "input-side aliases collapsed, + NONE/CLARIFY). The production chain "
        "was NOT executed in this run; the baseline column is Phase-0's "
        "FULL-CHAIN production decision "
        "(inversion-phase0-baseline-full-2026-08-12.md). Context-dependent "
        "rows (the 1529 offer/flow family) ran WITHOUT session state — their "
        "answers are informational for Phase 2, not its measured shape.",
        "",
        "## Per-category vs baseline (denominators stated — m-44)",
        "",
        "| category | rows | asserted | router match | baseline match | Δ | REVIEW | gate |",
        "|---|---|---|---|---|---|---|---|",
    ]
    tot = {"n": 0, "asserted": 0, "match": 0, "review": 0}
    regressions = []
    for cat in sorted(per_cat, key=lambda c: -per_cat[c]["n"]):
        c = per_cat[cat]
        for k in tot:
            tot[k] += c[k]
        base_asserted, base_match = PHASE0_BASELINE.get(cat, (None, None))
        if base_match is None:
            base_cell, delta_cell, gate = "—", "—", "no baseline row"
        elif c["asserted"] == 0:
            base_cell = f"{base_match}/{base_asserted}"
            delta_cell = "—"
            gate = "**UNGATEABLE** (REVIEW-only denominator)"
        else:
            base_cell = f"{base_match}/{base_asserted}"
            delta = c["match"] - base_match
            delta_cell = f"{delta:+d}"
            if delta < 0:
                gate = "**REGRESSION**"
                regressions.append((cat, base_match, c["match"]))
            else:
                gate = "no regression"
        lines.append(
            f"| {cat} | {c['n']} | {c['asserted']} | {c['match']} | "
            f"{base_cell} | {delta_cell} | {c['review']} | {gate} |"
        )
    lines.append(
        f"| **TOTAL** | {tot['n']} | {tot['asserted']} | {tot['match']} | "
        f"36/39 | {tot['match'] - 36:+d} | {tot['review']} | (aggregate is NOT the gate) |"
    )
    lines += [
        "",
        "Gate reading (Arch condition 1 as amended 08-09 08:3x, PPM): **no "
        "category may regress; the aggregate is never the gate** (the M2 "
        "precedent: 72.1% aggregate passed while a category was broken). "
        "CONVERSATION / DISCOVERY / PROVENANCE / TRUST / ANALYSIS have "
        "REVIEW-only denominators in Phase 0 and remain **ungateable** here — "
        "same as Phase 0 stated; growing asserted expectations there is "
        "outstanding Phase-0 work, not a Phase-1 scoring artifact.",
    ]
    if regressions:
        lines += [
            "",
            "🔴 **Per-category regressions vs baseline** (recorded as data — "
            "this run does not tune-until-green): "
            + "; ".join(f"{c}: {b}→{m}" for c, b, m in regressions),
        ]

    # Exhibit A + the demanded row
    exhibit = select_exhibit_rows(row_results)
    lines += [
        "",
        "## Exhibit A (PM 2026-08-08 live transcript) + Arch's demanded row",
        "",
        f"Selection rule: corpus `source` containing one of {_EXHIBIT_SOURCE_TOKENS} "
        f"→ {len(exhibit)} rows (the 8 Exhibit-A failures), plus the demanded "
        'row `"what reminders do I have?"` (probe-row-11, REVIEW — the '
        "sharpest test of the thesis: the LLM classifier misrouted it until "
        "the pre-classifier claimed it).",
        "",
        "| phrase | expected | router route @conf | verdict | source |",
        "|---|---|---|---|---|",
    ]
    demanded = [rr for rr in row_results if rr["row"]["phrase"] == DEMANDED_ROW]
    for rr in exhibit + demanded:
        r, d = rr["row"], rr["decision"]
        conf = getattr(d, "confidence", None)
        route_cell = f"`{d.route_label}`" + (f" @{conf}" if conf is not None else "")
        verdict = rr["verdict"] if rr["verdict"] != "REVIEW" else "REVIEW (informational)"
        lines.append(
            f"| {r['phrase'][:58]} | {r['expected']} | {route_cell} | {verdict} | "
            f"{r.get('source', '')[:48]} |"
        )

    # REVIEW rows — the question book, answered as data
    lines += [
        "",
        "## REVIEW rows — the router's answers as data (informational, unscored)",
        "",
        "These 54 rows are the Inversion's question book (36 probe-DISAGREEs "
        "by construction + PM's live failures). Nothing here is scored; the "
        "router's answer is recorded so the questions accumulate evidence.",
        "",
        "| phrase | category | router route @conf | rationale | source |",
        "|---|---|---|---|---|",
    ]
    for rr in row_results:
        if rr["verdict"] != "REVIEW":
            continue
        r, d = rr["row"], rr["decision"]
        conf = getattr(d, "confidence", None)
        route_cell = f"`{d.route_label}`" + (f" @{conf}" if conf is not None else "")
        rationale = (getattr(d, "rationale", "") or "").replace("|", "/")[:60]
        lines.append(
            f"| {r['phrase'][:55]} | {r['category']} | {route_cell} | {rationale} | "
            f"{r.get('source', '')[:40]} |"
        )

    # Full row detail
    lines += [
        "",
        "## Row detail (asserted rows)",
        "",
        "| phrase | category | expected | router route @conf | verdict | note |",
        "|---|---|---|---|---|---|",
    ]
    for rr in row_results:
        if rr["verdict"] == "REVIEW":
            continue
        r, d = rr["row"], rr["decision"]
        conf = getattr(d, "confidence", None)
        route_cell = f"`{d.route_label}`" + (f" @{conf}" if conf is not None else "")
        lines.append(
            f"| {r['phrase'][:55]} | {r['category']} | {r['expected']} | "
            f"{route_cell} | {rr['verdict']} | {rr['note']} |"
        )
    return "\n".join(lines) + "\n"


async def run(dry_run: bool, out: Optional[Path]) -> int:
    from services.intent_service.inversion_router import derive_routing_grammar, route

    rows = p0.load_corpus()
    assert any(r["phrase"] == DEMANDED_ROW for r in rows), (
        f"Arch's demanded row {DEMANDED_ROW!r} is missing from the corpus — "
        "refusing to score without it"
    )
    grammar = derive_routing_grammar()
    n_aliases = sum(len(op.aliases) for op in grammar.operations)
    print(
        f"corpus: {len(rows)} rows · grammar: {len(grammar.operations)} canonical "
        f"operations (+NONE/CLARIFY), {n_aliases} aliases collapsed input-side"
    )
    exhibit_count = sum(
        1 for r in rows if any(tok in r.get("source", "") for tok in _EXHIBIT_SOURCE_TOKENS)
    )
    print(f"exhibit-A selection: {exhibit_count} rows (expected 8) + demanded row present")

    if dry_run:
        for op in grammar.operations:
            print(f"  {op.name:<28} [{op.source}] aliases={list(op.aliases)}")
        print("dry-run complete: corpus + grammar + selections validated, no LLM calls.")
        return 0

    from services.llm.clients import LLMClient

    llm = LLMClient()  # #322 constructor-injection pattern; keys via app config path

    async def router_fn(phrase: str):
        return await route(phrase, None, llm_service=llm, grammar=grammar)

    decisions = await route_all(rows, router_fn)
    scored = score(rows, decisions)
    calls = sum(getattr(d, "llm_calls", 0) for d in decisions)
    errors = sum(1 for d in decisions if getattr(d, "outcome", "") == "error")
    refused = sum(1 for d in decisions if getattr(d, "outcome", "") == "refused")
    print(f"served (#1620, resolved post-fallback): {served_summary(decisions)}")
    report = build_report(
        scored,
        grammar,
        llm_note=f"{calls} LLM calls incl. repair retries; {errors} ERROR, {refused} REFUSED",
        served_note=served_summary(decisions),
    )
    out = out or DEFAULT_OUT
    out.write_text(report)
    print(f"wrote {out}")
    tot_match = sum(c["match"] for c in scored["per_cat"].values())
    tot_asserted = sum(c["asserted"] for c in scored["per_cat"].values())
    print(
        f"router: {tot_match}/{tot_asserted} asserted matched · "
        f"{calls} LLM calls · {errors} ERROR · {refused} REFUSED"
    )
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()
    sys.exit(asyncio.run(run(args.dry_run, args.out)))
