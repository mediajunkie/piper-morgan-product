#!/usr/bin/env python3
"""#2327: tally the floored action names that are outside every vocabulary.

Input: the JSON of ``GET /api/v1/admin/floored-actions`` (admin only), from a file
or stdin. A seat reads that endpoint through a signed-in admin browser profile and
saves the JSON; nothing here calls a host, a log service or a database.

The served check counts a name against the IMPORTABLE vocabulary only, so it can
over-report a name the pre-classifier emits. This script applies the full
derivation (``scripts/routing_vocabulary_full.py``, the 1283 lint's own) and
drops those. What is left is a handler-gap candidate (the 2270 class): triage each
as a corpus row, a rail alias under Arch's standing rule, or "the floor is right".

It always prints the window it was given, because absence must not read as clear:
"no names" is only ever said beside the day range and the row count.

Usage:
    python scripts/floored_action_tally.py counts.json
    python scripts/floored_action_tally.py < counts.json

Concept: docs/internal/architecture/current/intent-routing-stack.md
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

WITHHELD = "(withheld)"


def tally(payload: Dict[str, Any], vocabulary: Iterable[str]) -> Dict[str, Any]:
    """Pure: group the payload's rows by name, dropping names the full vocabulary
    knows. Returns the window as given, the kept names (count, sites, days), the
    withheld total, and the names dropped as known."""
    known = set(vocabulary)
    rows = payload.get("rows") or []
    kept: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {"count": 0, "sites": defaultdict(int), "days": set()}
    )
    dropped: Dict[str, int] = defaultdict(int)
    withheld = 0
    for row in rows:
        name, site, day, count = row["name"], row["site"], row["day"], int(row["count"])
        if name == WITHHELD:
            withheld += count
            kept_row = kept[WITHHELD]
        elif name in known:
            dropped[name] += count
            continue
        else:
            kept_row = kept[name]
        kept_row["count"] += count
        kept_row["sites"][site] += count
        kept_row["days"].add(day)
    names: List[Tuple[str, Dict[str, Any]]] = sorted(
        kept.items(), key=lambda item: (-item[1]["count"], item[0])
    )
    return {
        "window": payload.get("window") or {},
        "first_day": payload.get("first_day"),
        "last_day": payload.get("last_day"),
        "row_count": len(rows),
        "names": [
            {
                "name": name,
                "count": info["count"],
                "sites": dict(sorted(info["sites"].items())),
                "first_day": min(info["days"]),
                "last_day": max(info["days"]),
            }
            for name, info in names
        ],
        "withheld": withheld,
        "dropped_as_known": dict(sorted(dropped.items())),
    }


def render(result: Dict[str, Any]) -> str:
    window = result["window"]
    lines = [
        "Floored action names outside every vocabulary (#2327)",
        f"Window asked for: {window.get('since', '?')} to {window.get('through', '?')} "
        f"({window.get('days', '?')} days, UTC)",
        f"Days holding rows: {result['first_day'] or 'none'} to {result['last_day'] or 'none'}; "
        f"rows read: {result['row_count']}",
    ]
    candidates = [n for n in result["names"] if n["name"] != WITHHELD]
    if not candidates:
        lines.append("No out-of-vocabulary names in this window.")
    else:
        lines.append(f"{len(candidates)} name(s) to triage:")
        for entry in candidates:
            sites = ", ".join(f"{site} x{count}" for site, count in entry["sites"].items())
            lines.append(
                f"  {entry['name']}: {entry['count']} "
                f"({entry['first_day']} to {entry['last_day']}; {sites})"
            )
    if result["withheld"]:
        lines.append(
            f"Withheld (a name that was not a short identifier): {result['withheld']} sighting(s)."
        )
    if result["dropped_as_known"]:
        known = ", ".join(f"{name} x{count}" for name, count in result["dropped_as_known"].items())
        lines.append(f"Dropped as known to the full vocabulary (pre-classifier names): {known}")
    return "\n".join(lines)


def main(argv: List[str]) -> int:
    text = Path(argv[1]).read_text() if len(argv) > 1 else sys.stdin.read()
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Not JSON: {e}", file=sys.stderr)
        return 2
    if not isinstance(payload, dict) or "rows" not in payload or "window" not in payload:
        print("Expected the floored-actions endpoint's JSON (window, rows).", file=sys.stderr)
        return 2
    sys.path.insert(0, str(ROOT / "scripts"))
    from routing_vocabulary_full import full_vocabulary

    print(render(tally(payload, full_vocabulary())))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
