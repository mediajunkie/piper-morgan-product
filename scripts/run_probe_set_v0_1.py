#!/usr/bin/env python3
"""
#1004 Step 8 Phase C — Live probe-set calibration runner.

Wires the Phase B probe runner harness to the live SemanticBoundaryDetector
(via LLMClient -> Anthropic per the boundary_detection task config) and
runs all 20 probes from CXO's probe set v0.1. Output is the markdown
divergence table + summary stats CXO consumes for the v0.2 prompt
iteration round.

Usage:
    python scripts/run_probe_set_v0_1.py [output_path]

Default output path:
    dev/{YYYY}/{MM}/{DD}/1004-probe-set-v0-1-run-{N}.md
where N is the next available run ordinal in that directory.

Cost / time profile per the contract Anthropic-only MVP scoping:
    20 LLM calls * ~400 tokens output = ~$0.10-1 depending on tier
    ~30-90s wall clock total
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

# Make the project root importable when invoked directly.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from services.ethics.semantic_boundary_detector import (  # noqa: E402
    SEMANTIC_DETECTOR_PROMPT_V0_1,
    SemanticBoundaryDetector,
)
from tests.ethics.probe_set.probe_definitions import ALL_PROBES  # noqa: E402
from tests.ethics.probe_set.probe_runner import (  # noqa: E402
    ProbeRunResult,
    format_divergence_table,
    run_probe_set,
    summarize_results,
)


def _next_run_path(base_dir: Path) -> Path:
    """Pick the next available 1004-probe-set-v0-1-run-N.md slot."""
    base_dir.mkdir(parents=True, exist_ok=True)
    n = 1
    while True:
        candidate = base_dir / f"1004-probe-set-v0-1-run-{n}.md"
        if not candidate.exists():
            return candidate
        n += 1


def _format_full_results_table(results: List[ProbeRunResult]) -> str:
    rows = [
        "| probe_id | expected (cat / conf) | actual (cat / conf) | violation? | diff_types | latency_ms |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        expected = (
            f"{r.expected_category} / "
            f"[{r.expected_confidence_range[0]:.2f}, "
            f"{r.expected_confidence_range[1]:.2f}]"
        )
        actual = f"{r.actual_output.category} / {r.actual_output.confidence:.2f}"
        violation_match = (
            "✓"
            if r.expected_violation == r.actual_output.violation_detected
            else "✗"
        )
        diffs = ", ".join(r.diff_types) if r.diff_types else "—"
        rows.append(
            f"| {r.probe_id} | {expected} | {actual} | {violation_match} | "
            f"{diffs} | {r.latency_ms:.0f} |"
        )
    return "\n".join(rows)


def _format_hint_assertion_failures(results: List[ProbeRunResult]) -> str:
    """Detail of any hint_shape_violation findings."""
    rows = []
    for r in results:
        if not r.hint_assertion_failures:
            continue
        rows.append(f"\n### {r.probe_id}")
        rows.append(
            f"\n**Detector hint**: {r.actual_output.redirect_hint!r}"
        )
        rows.append(f"\n**Failures**:\n")
        for f in r.hint_assertion_failures:
            rows.append(f"- `{f.rule}` — matched: `{f.matched_text!r}` ({f.detail})")
    return "\n".join(rows) if rows else "_No hint_shape_violation findings._"


def _format_per_probe_detail(results: List[ProbeRunResult]) -> str:
    """Per-probe full detail block — input + actual reasoning + hint."""
    rows = []
    for r in results:
        rows.append(f"\n### {r.probe_id}")
        rows.append(f"\n**Input**: {r.probe_input!r}")
        rows.append(
            f"\n**Expected**: violation={r.expected_violation}, "
            f"category={r.expected_category}, "
            f"confidence∈[{r.expected_confidence_range[0]:.2f}, "
            f"{r.expected_confidence_range[1]:.2f}]"
        )
        rows.append(
            f"\n**Actual**: violation={r.actual_output.violation_detected}, "
            f"category={r.actual_output.category}, "
            f"confidence={r.actual_output.confidence:.3f}"
        )
        rows.append(f"\n**Reasoning**: {r.actual_output.reasoning!r}")
        rows.append(f"\n**Hint**: {r.actual_output.redirect_hint!r}")
        rows.append(f"\n**Latency**: {r.latency_ms:.0f}ms")
        if r.diff_types:
            rows.append(f"\n**Diffs**: {', '.join(r.diff_types)}")
        if r.hint_assertion_failures:
            rows.append("\n**Hint assertion failures**:")
            for f in r.hint_assertion_failures:
                rows.append(
                    f"- `{f.rule}`: matched `{f.matched_text!r}` ({f.detail})"
                )
    return "\n".join(rows)


def _render_report(
    results: List[ProbeRunResult],
    timestamp: datetime,
    prompt_version: str,
) -> str:
    summary = summarize_results(results)
    diff_table = format_divergence_table(results)
    full_table = _format_full_results_table(results)
    per_probe = _format_per_probe_detail(results)
    hint_detail = _format_hint_assertion_failures(results)

    return f"""# #1004 Probe Set v0.1 — Run Report

**Run timestamp**: {timestamp.isoformat()}
**Prompt version**: {prompt_version}
**Probe set**: v0.1 (CXO 2026-04-27, 20 probes)
**Detector**: live `SemanticBoundaryDetector` via `LLMClient` (Anthropic-only MVP per contract)
**Runner**: `scripts/run_probe_set_v0_1.py` (Step 8 Phase C)

## Summary

| Stat | Value |
|---|---|
| Total probes | {summary['total']} |
| Passed (no diffs) | {summary['passed']} |
| Failed (>=1 diff) | {summary['failed']} |
| Latency p_min | {summary.get('latency_ms_min', 0):.0f}ms |
| Latency p_avg | {summary.get('latency_ms_avg', 0):.0f}ms |
| Latency p_max | {summary.get('latency_ms_max', 0):.0f}ms |

### Diff-type counts

{json.dumps(summary['diff_type_counts'], indent=2)}

## Divergence table (failures only)

{diff_table}

## Full results table

{full_table}

## Hint assertion failure detail

{hint_detail}

## Per-probe full detail

{per_probe}

---

_Generated by `scripts/run_probe_set_v0_1.py`._
"""


async def main_async(output_path: Optional[Path] = None) -> Path:
    print("[run_probe_set_v0_1] Initializing live SemanticBoundaryDetector...")
    detector = SemanticBoundaryDetector(prompt=SEMANTIC_DETECTOR_PROMPT_V0_1)

    print(f"[run_probe_set_v0_1] Running {len(ALL_PROBES)} probes...")
    timestamp = datetime.now(timezone.utc)
    results = await run_probe_set(ALL_PROBES, detector)

    if output_path is None:
        ts = timestamp.astimezone()
        base_dir = (
            PROJECT_ROOT
            / "dev"
            / f"{ts.year:04d}"
            / f"{ts.month:02d}"
            / f"{ts.day:02d}"
        )
        output_path = _next_run_path(base_dir)

    report = _render_report(
        results,
        timestamp=timestamp,
        prompt_version="SEMANTIC_DETECTOR_PROMPT_V0_1",
    )
    output_path.write_text(report)

    summary = summarize_results(results)
    print(
        f"\n[run_probe_set_v0_1] Done. {summary['passed']}/{summary['total']} "
        f"passed. Diffs: {summary['diff_type_counts']}"
    )
    print(f"[run_probe_set_v0_1] Report: {output_path}")
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output_path",
        nargs="?",
        type=Path,
        default=None,
        help=(
            "Optional output path. Default: "
            "dev/YYYY/MM/DD/1004-probe-set-v0-1-run-N.md"
        ),
    )
    args = parser.parse_args()
    asyncio.run(main_async(output_path=args.output_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
