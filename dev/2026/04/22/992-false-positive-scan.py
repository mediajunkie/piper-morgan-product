#!/usr/bin/env python3
"""
#992 ETHICS-ACTIVATE — Phase D false-positive scan.

Runs the CANONICAL_QUERIES corpus from dev/2026/04/11/canonical-retest-m1.py
through BoundaryEnforcer.enforce_boundaries() with the feature flag enabled.
Counts how many non-violating canonical queries incorrectly trigger a boundary
decision (false positives).

Gate (per gameplan Phase D): <2-3% false-positive rate. If exceeded, STOP and
escalate — pattern tuning required before activation.

Usage:
    ./venv/bin/python dev/2026/04/22/992-false-positive-scan.py

Outputs:
    dev/2026/04/22/992-false-positive-results.md

Notes:
    - Every query in CANONICAL_QUERIES is a legitimate PM-style request —
      NONE should trigger the ethics gate. Any trigger is a false positive.
    - We set ENABLE_ETHICS_ENFORCEMENT=true so the enforcer's adaptive-learning
      path is exercised; the enforcer always returns a BoundaryDecision regardless
      of the flag, but this mirrors production behavior.
    - No LLM calls; pattern matching only. Safe to run offline.
"""

import asyncio
import importlib.util
import os
import sys
from pathlib import Path

# Load canonical corpus from the Apr 11 retest script without executing its
# top-level server calls. We only need CANONICAL_QUERIES.
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

CANONICAL_PATH = PROJECT_ROOT / "dev" / "2026" / "04" / "11" / "canonical-retest-m1.py"

# Activate the flag before importing the enforcer so any flag-gated init paths
# behave as they will in production.
os.environ["ENABLE_ETHICS_ENFORCEMENT"] = "true"


def _load_canonical_queries():
    """Import the M1 retest module and pull CANONICAL_QUERIES out of it.

    The retest script defines constants at top-level that try to reach a
    local server; importing it would fail. We sidestep by reading the source
    and executing only the list literal.
    """
    source = CANONICAL_PATH.read_text()
    # Carve out just the CANONICAL_QUERIES = [...] assignment.
    start = source.index("CANONICAL_QUERIES = [")
    # Find matching closing bracket at top-level indent (first line that starts with "]")
    rest = source[start:]
    end_rel = rest.index("\n]") + 2
    snippet = rest[:end_rel]
    namespace: dict = {}
    exec(snippet, namespace)  # noqa: S102 - trusted local source
    return namespace["CANONICAL_QUERIES"]


async def main():
    from services.ethics.boundary_enforcer_refactored import (
        boundary_enforcer_refactored,
    )

    queries = _load_canonical_queries()
    total = len(queries)
    triggers: list[dict] = []

    for q in queries:
        qnum, qtext, category, expected_routing, known_issue = q
        decision = await boundary_enforcer_refactored.enforce_boundaries(
            message=qtext,
            session_id=f"fp-scan-{qnum}",
            context={"source": "false_positive_scan"},
        )
        if decision.violation_detected:
            triggers.append(
                {
                    "qnum": qnum,
                    "query": qtext,
                    "category": category,
                    "boundary_type": str(decision.boundary_type),
                    "explanation": decision.explanation,
                    "redirect_context": decision.redirect_context,
                }
            )

    fp_rate = (len(triggers) / total) * 100 if total else 0.0
    threshold = 3.0  # upper bound from gameplan ("<2-3%")

    # Build report
    lines = []
    lines.append("# #992 Phase D — False-Positive Scan Results")
    lines.append("")
    lines.append(f"**Date**: 2026-04-22")
    lines.append(f"**Branch**: `claude/992-ethics-activate`")
    lines.append(f"**Flag**: `ENABLE_ETHICS_ENFORCEMENT=true`")
    lines.append(f"**Corpus**: `dev/2026/04/11/canonical-retest-m1.py::CANONICAL_QUERIES` ({total} queries)")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total queries scanned: **{total}**")
    lines.append(f"- False positives (violations triggered): **{len(triggers)}**")
    lines.append(f"- False-positive rate: **{fp_rate:.2f}%**")
    lines.append(f"- Threshold (gameplan Phase D): **< {threshold:.1f}%**")
    gate_status = "✅ PASS" if fp_rate < threshold else "❌ FAIL — STOP and escalate"
    lines.append(f"- Gate: **{gate_status}**")
    lines.append("")

    if triggers:
        lines.append("## Triggered Queries")
        lines.append("")
        lines.append("| # | Category | Query | Boundary Type | Explanation |")
        lines.append("|---|----------|-------|---------------|-------------|")
        for t in triggers:
            q_escaped = t["query"].replace("|", "\\|")
            exp_escaped = t["explanation"].replace("|", "\\|")
            lines.append(
                f"| {t['qnum']} | {t['category']} | {q_escaped} | {t['boundary_type']} | {exp_escaped} |"
            )
        lines.append("")
    else:
        lines.append("## Triggered Queries")
        lines.append("")
        lines.append("None. All canonical queries passed through the enforcer without triggering a boundary.")
        lines.append("")

    lines.append("## Known Pattern Risks — corpus sanity check")
    lines.append("")
    lines.append("From the Phase 1 audit, these substrings were flagged as potential false-positive risks. Checking whether they appear anywhere in the canonical corpus at all, so a zero FP rate is explained rather than lucky:")
    lines.append("")
    lines.append("| Substring | Pattern list | Hits in corpus |")
    lines.append("|-----------|--------------|----------------|")
    risk_check = [
        ("uncomfortable", "harassment"),
        ("family", "professional"),
        ("personal", "professional"),
        ("private", "professional"),
    ]
    for substring, listname in risk_check:
        hits = sum(1 for q in queries if substring in q[1].lower())
        lines.append(f"| `{substring}` | {listname} | {hits} |")
    lines.append("")
    lines.append("**Interpretation**: the canonical corpus does not exercise the known-risk substrings, so a zero FP rate on this corpus does not yet clear those specific patterns. The Colleague-Test scenarios in Phase E are a separate instrument and do not cover this gap either. Consider a follow-up targeted probe set if CXO wants higher confidence on the known-risk tokens before flag flip.")
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append("Each query was passed to `boundary_enforcer_refactored.enforce_boundaries(message=query, session_id=f'fp-scan-{qnum}', context={'source': 'false_positive_scan'})`. A violation is any `BoundaryDecision` with `violation_detected=True`. No LLM calls; pattern matching only.")
    lines.append("")
    lines.append("## Conclusion")
    lines.append("")
    if fp_rate < threshold:
        lines.append(f"Phase D gate passes: {fp_rate:.2f}% false-positive rate is below the {threshold:.1f}% threshold. Safe to advance to Phase E (Colleague Test) pending PM approval.")
    else:
        lines.append(f"Phase D gate fails: {fp_rate:.2f}% false-positive rate exceeds the {threshold:.1f}% threshold. Pattern tuning required before activation. File a sub-issue and escalate to PM.")
    lines.append("")

    output_path = Path(__file__).parent / "992-false-positive-results.md"
    output_path.write_text("\n".join(lines))

    print(f"Scanned {total} queries. {len(triggers)} triggers. Rate: {fp_rate:.2f}% (threshold < {threshold:.1f}%).")
    print(f"Report: {output_path}")
    if triggers:
        print("Triggered:")
        for t in triggers:
            print(f"  #{t['qnum']} [{t['category']}] {t['query']!r} → {t['boundary_type']}")

    return 0 if fp_rate < threshold else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
