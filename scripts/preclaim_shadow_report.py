#!/usr/bin/env python
"""Pre-claim shadow probe report — the artifact the narrowing schedule reads.

Aggregates ``preclaim_shadow_*`` telemetry lines (emitted by
``services/intent_service/preclaim_shadow.py`` when ``PIPER_PRECLAIM_SHADOW``
is on) into per-pattern-list claim counts, agreement rates, and the
precision-vs-bar readout (the PM-ratified 2026-08-29 policy: a surface-1
pattern claim must meet ~100% precision by shadow divergence; patterns below
the bar get deleted ON EVIDENCE, each deletion citing its rows here).

No LLM, no server — a log read, in the ``inversion_phase2_gate --audit``
spirit: derive the readout from the recorded evidence, never assert it.

Usage:
    python scripts/preclaim_shadow_report.py /tmp/piper-server.log [more.log ...]
    python scripts/preclaim_shadow_report.py --bar 0.98 server.log
    cat server.log | python scripts/preclaim_shadow_report.py -
    python scripts/preclaim_shadow_report.py --json server.log   # machine shape

Line formats accepted, per line:
  1. JSON object containing an ``event`` field (structlog JSONRenderer) —
     the reliable path; every field is available.
  2. Console-renderer lines (``... [info] preclaim_shadow_agreement
     pattern_list=DISCOVERY_PATTERNS ...``) — best-effort: the aggregate
     needs only ``event`` + ``pattern_list``, both unambiguous single
     tokens in that format.

m-44 discipline is inherited from the aggregation: precision's denominator
is agree+disagree (incomparable shown beside it, never folded in), a list
with zero comparable rows prints NO COMPARABLE DATA rather than clean, and
the footer reminds the reader that MEETS BAR at small n is weak evidence.
The parse itself states its denominator too: the report header prints how
many lines were read and how many probe events were found — a zero-event
run reads as "measured nothing", never as "all clear".
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List

# Repo-root import (scripts/ is not a package) — the idiom the other
# inversion scripts use.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from services.intent_service.preclaim_shadow import (  # noqa: E402
    AGREEMENT_EVENT,
    DISAGREEMENT_EVENT,
    INCOMPARABLE_EVENT,
    aggregate_preclaim_events,
    render_preclaim_report,
)

_PROBE_EVENTS = (AGREEMENT_EVENT, DISAGREEMENT_EVENT, INCOMPARABLE_EVENT)
_PATTERN_LIST_RE = re.compile(r"\bpattern_list=([A-Za-z0-9_]+)")


def parse_probe_events(lines: Iterable[str]) -> Iterator[Dict[str, Any]]:
    """Yield ``{"event": ..., "pattern_list": ..., ...}`` dicts from log lines.

    JSON lines yield their full payload; console lines yield the two fields
    the aggregate needs. Lines mentioning no probe event are skipped cheaply.
    """
    for line in lines:
        event = next((e for e in _PROBE_EVENTS if e in line), None)
        if event is None:
            continue
        stripped = line.strip()
        # JSON path: the whole line, or a trailing JSON object.
        brace = stripped.find("{")
        if brace != -1:
            try:
                payload = json.loads(stripped[brace:])
                if payload.get("event") in _PROBE_EVENTS:
                    yield payload
                    continue
            except (json.JSONDecodeError, AttributeError):
                pass
        # Console path: event token + pattern_list=<token>.
        m = _PATTERN_LIST_RE.search(stripped)
        yield {"event": event, "pattern_list": m.group(1) if m else None}


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("logs", nargs="+", help="log file paths, or '-' for stdin")
    parser.add_argument(
        "--bar",
        type=float,
        default=1.0,
        help="precision bar (default 1.0 — the PM-ratified ~100%% bar)",
    )
    parser.add_argument(
        "--json", action="store_true", help="emit the aggregate as JSON instead of the table"
    )
    args = parser.parse_args(argv)

    events: List[Dict[str, Any]] = []
    lines_read = 0
    for source in args.logs:
        fh = sys.stdin if source == "-" else open(source, encoding="utf-8", errors="replace")
        try:
            for line in fh:
                lines_read += 1
                events.extend(parse_probe_events([line]))
        finally:
            if fh is not sys.stdin:
                fh.close()

    aggregate = aggregate_preclaim_events(events)
    if args.json:
        print(
            json.dumps(
                {"lines_read": lines_read, "events_found": len(events), **aggregate},
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    print(f"parsed {lines_read} log lines · {len(events)} probe events found")
    if not events:
        print(
            "NO PROBE EVENTS — this run measured nothing (is PIPER_PRECLAIM_SHADOW "
            "on? is this the right log?). Not an all-clear (m-44)."
        )
        return 1
    print()
    print(render_preclaim_report(aggregate, bar=args.bar))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
