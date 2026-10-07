#!/usr/bin/env python3
"""Offline re-verdict: re-score RECORDED router decisions against the CURRENT
corpus expectations. Zero LLM calls.

Why (2026-10-06, Arch's re-judge ledger ruling 1 + PM's API-cost pause): when
only corpus EXPECTATIONS change (a re-judge) and the catalog does not, the
router's answer to each phrase is already measured — the newest full-corpus
report holds it. Re-routing 514 phrases to re-learn answers we already have
costs ~$1.70 on PM's key and tells us nothing new. This tool keeps the
recorded decision (route, confidence, the report's served-model line) and
recomputes ONLY the verdict, with the scorer's own ``router_matches`` — the
same function a live run uses, never a re-derivation.

It is NOT a substitute for a live run when the CATALOG changed (a rail entry
added, a description edited): then the decisions themselves may move, and
procedure rule 7 (full corpus, same lane) applies.

Usage:
  python scripts/inversion_offline_reverdict.py \\
      --source docs/internal/architecture/current/<newest-full-report>.md \\
      --out    docs/internal/architecture/current/<name>-offline-reverdict.md \\
      [--only-changed]

``--only-changed`` writes only rows whose expectation differs from the
source report's (the re-judged rows) — the shape the deletion gate's
PHASE3_REPORTS wants for an evidence deposit.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import inversion_phase0_baseline as p0  # noqa: E402
import inversion_phase1_shadow_score as p1  # noqa: E402

_ROUTE_RE = re.compile(r"^`(?P<label>[^`]+)`(?:\s*@(?P<conf>[0-9.]+))?$")


def decision_from_cell(cell: str):
    """Rebuild a RoutingDecision from a report's 'router route @conf' cell.
    Returns None for a cell this tool cannot read (never a guess)."""
    from services.intent_service.inversion_router import RoutingDecision

    m = _ROUTE_RE.match(cell.strip())
    if not m:
        return None
    label = m.group("label")
    conf = float(m.group("conf")) if m.group("conf") else None
    if label == "NONE":
        return RoutingDecision(outcome="none", confidence=conf)
    if label == "CLARIFY":
        return RoutingDecision(outcome="clarify", confidence=conf)
    if label.startswith("PLAN[") and label.endswith("]"):
        ops = [o for o in label[5:-1].split("→") if o]
        return RoutingDecision(
            outcome="plan", confidence=conf, operations=[{"operation": o} for o in ops]
        )
    if label in ("ERROR", "REFUSED"):
        return RoutingDecision(outcome=label.lower(), confidence=conf)
    return RoutingDecision(outcome="operation", operation=label, confidence=conf)


def read_source(path: Path):
    """(served_line, [(phrase, category, expected_then, route_cell)]) from the
    report's '## Row detail (asserted rows)' table."""
    lines = path.read_text().splitlines()
    served = next((ln for ln in lines if ln.startswith("Served ")), None)
    start = next(i for i, ln in enumerate(lines) if ln.strip() == "## Row detail (asserted rows)")
    rows, in_table = [], False
    for ln in lines[start + 1 :]:
        s = ln.strip()
        if s.startswith("| phrase |"):
            in_table = True
            continue
        if not in_table or s.startswith("|---"):
            continue
        if not s.startswith("|"):
            break
        cols = [c.strip() for c in s.strip("|").split("|")]
        rows.append((cols[0], cols[1], cols[2], cols[3]))
    return served, rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--source", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--only-changed", action="store_true")
    args = ap.parse_args()

    served, src_rows = read_source(args.source)
    if not served:
        print(f"REFUSING: {args.source} has no 'Served' line (procedure rule 1)", file=sys.stderr)
        return 2
    corpus = {p1._norm_phrase(r["phrase"]): r for r in p0.load_corpus()}
    op_categories = p1._op_category_map()

    out_rows, changed, unreadable, no_row = [], 0, 0, 0
    for phrase, category, expected_then, cell in src_rows:
        row = corpus.get(p1._norm_phrase(phrase))
        if row is None:
            no_row += 1
            continue
        expected_now = row["expected"]
        if expected_now == "REVIEW":
            continue  # unasserted now: nothing to verdict
        if args.only_changed and expected_now == expected_then:
            continue
        decision = decision_from_cell(cell)
        if decision is None:
            unreadable += 1
            continue
        ok, note = p1.router_matches(expected_now, decision, op_categories)
        changed += expected_now != expected_then
        out_rows.append(
            f"| {phrase} | {category} | {expected_now} | {cell} | "
            f"{'MATCH' if ok else 'MISMATCH'} | {note or ''} |"
        )

    matched = sum(1 for r in out_rows if "| MATCH |" in r)
    body = [
        f"# Offline re-verdict of {args.source.name}",
        "",
        "**No LLM calls.** Router decisions are the RECORDED ones from the source report; only the verdict",
        "is recomputed, against the corpus expectations at this commit, with the scorer's own `router_matches`.",
        "Valid evidence only while the catalog is unchanged since the source run (procedure rule 7).",
        "",
        served + " — recorded in the source report, not re-served",
        f"Source: `{args.source.relative_to(ROOT) if args.source.is_absolute() else args.source}`",
        f"Rows: {len(out_rows)} written · {matched} MATCH · {changed} with a changed expectation · "
        f"{unreadable} unreadable route cells skipped · {no_row} source phrases no longer in the corpus",
        "",
        "## Row detail (asserted rows)",
        "",
        "| phrase | category | expected | router route @conf | verdict | note |",
        "|---|---|---|---|---|---|",
        *out_rows,
        "",
    ]
    args.out.write_text("\n".join(body))
    print(
        f"wrote {args.out}: {len(out_rows)} rows, {matched} MATCH, {changed} changed, "
        f"{unreadable} unreadable, {no_row} not in corpus"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
