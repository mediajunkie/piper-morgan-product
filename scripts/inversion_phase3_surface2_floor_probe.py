#!/usr/bin/env python3
"""Inversion Phase 3 — SURFACE-2 FLOOR PROBE (#1595, epic-0 unit 5).

The deletion gate measures surface 1 (the pre-classifier) against the served
router, and marks a row FAIL when the pattern is the live path and the router
does not own the phrase. For a row whose destination is a FLOOR-disposition
action (get_project_status, get_top_priority, …) that verdict is honest but
incomplete: deleting the pattern hands the phrase to SURFACE 2 — the LLM
classifier — and if surface 2 lands it in the same category, the user reaches
the same floor. This script measures exactly that, so the gate can read a
frozen artifact instead of assuming.

Layer (m-43): ``IntentClassifier._classify_with_reasoning`` ONLY — surface 1
bypassed by construction, no session context, the dev keychain key via
``dev_key_binding``. N samples per phrase (default 2); the gate credits a
phrase only when EVERY sample's category equals the expected action's registry
category.

Usage:
    env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \
      -u ANTHROPIC_CUSTOM_HEADERS venv/bin/python \
      scripts/inversion_phase3_surface2_floor_probe.py \
      --phrase "show today's progress" [--phrase ...] [--samples 2] --out PATH
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

HEADER = "| phrase | sample | surface-2 category | surface-2 action | confidence |"


async def _probe(phrases: list[str], samples: int) -> list[dict]:
    from services.intent_service.classifier import IntentClassifier
    from services.llm.clients import LLMClient

    classifier = IntentClassifier(llm_service=LLMClient())
    rows: list[dict] = []
    for phrase in phrases:
        for n in range(1, samples + 1):
            intent, _reasoning = await classifier._classify_with_reasoning(phrase)
            category = getattr(getattr(intent, "category", None), "value", None)
            rows.append(
                {
                    "phrase": phrase,
                    "sample": n,
                    "category": (category or "").upper(),
                    "action": getattr(intent, "action", None) or "",
                    "confidence": getattr(intent, "confidence", None),
                }
            )
            print(
                f"[{phrase!r} #{n}] {rows[-1]['category']}/{rows[-1]['action']} @{rows[-1]['confidence']}"
            )
    return rows


def write_report(rows: list[dict], out: Path, samples: int) -> None:
    lines = [
        "# Inversion Phase 3 — surface-2 floor probe",
        "",
        f"Run {datetime.now(timezone.utc):%Y-%m-%d %H:%MZ} · {samples} sample(s) per phrase · "
        "LAYER (m-43): `IntentClassifier._classify_with_reasoning` only (surface 1 bypassed, "
        "no session context, dev keychain key). Read by "
        "`scripts/inversion_phase3_deletion_gate.py` (SURFACE2_FLOOR_PROBES) to credit a "
        "FLOOR-destination row whose pattern the router does not replace: the row is OK to lose "
        "its pattern when EVERY sample lands in the expected action's own category.",
        "",
        HEADER,
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['phrase']} | {r['sample']} | {r['category']} | `{r['action']}` | {r['confidence']} |"
        )
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")


def parse_report(path: Path) -> dict[str, list[dict]]:
    """phrase → list of sample rows. Markdown-table parsing of this script's own output."""
    by_phrase: dict[str, list[dict]] = {}
    if not path.exists():
        return by_phrase
    for line in path.read_text().splitlines():
        if not line.startswith("| ") or line.startswith("| phrase") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        phrase, sample, category, action, confidence = cells[:5]
        by_phrase.setdefault(phrase, []).append(
            {
                "sample": int(sample) if sample.isdigit() else sample,
                "category": category.upper(),
                "action": action.strip("`"),
                "confidence": confidence,
            }
        )
    return by_phrase


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--phrase", action="append", required=True)
    ap.add_argument("--samples", type=int, default=2)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    from dev_key_binding import developer_keys_bound

    with developer_keys_bound(require=True):
        result = asyncio.run(_probe(args.phrase, args.samples))
    write_report(result, args.out, args.samples)
