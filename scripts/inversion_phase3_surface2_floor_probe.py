#!/usr/bin/env python3
"""Inversion Phase 3 — SURFACE-2 FLOOR PROBE (#1595, epic-0 unit 5).

The deletion gate measures surface 1 (the pre-classifier) against the served
router, and marks a row FAIL when the pattern is the live path and the router
does not own the phrase. For a row whose destination is reached BY CATEGORY —
a FLOOR-disposition action (get_project_status, get_top_priority, …) or a
category ``CanonicalHandlers`` dispatches whole (GUIDANCE, …) — that verdict
is honest but incomplete: deleting the pattern hands the phrase to SURFACE 2,
the LLM classifier, and if surface 2 lands it in the same category the user
reaches the same destination. This script measures exactly that, so the gate
can read a frozen artifact instead of assuming.

Layer (m-43): ``IntentClassifier._classify_with_reasoning`` ONLY — surface 1
bypassed by construction, no session context, the dev keychain key via
``dev_key_binding``. N samples per phrase (default 5 — Arch's condition 2,
2026-10-02); the gate credits a phrase only when EVERY sample's category
equals the expected action's registry category.

Arch's condition 1 (2026-10-02): the SERVED model is recorded per call (via
#1620's ``served=`` capture on the client, injected by a wrapper because the
classifier does not pass it) and printed in the report header; the gate
REFUSES a report that carries no served line — the gpt-4o-mini/Haiku catch,
one layer down.

Usage:
    env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \
      -u ANTHROPIC_CUSTOM_HEADERS venv/bin/python \
      scripts/inversion_phase3_surface2_floor_probe.py \
      --phrase "show today's progress" [--phrase ...] [--samples 5] --out PATH
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

HEADER = "| phrase | sample | surface-2 category | surface-2 action | confidence | served |"
SERVED_LINE_PREFIX = "served (#1620, resolved per call): "


async def _probe(phrases: list[str], samples: int, provider: Optional[str] = None) -> list[dict]:
    from services.intent_service.classifier import IntentClassifier
    from services.llm.clients import LLMClient

    client = LLMClient()
    if provider:
        # Same seam the Phase-1 scorer uses: the dev selection defaults to
        # openai; alpha serves each user on THEIR stored key, so the served
        # population spans both providers. Run the probe once per provider
        # the testers actually hold; the report's served line says which.
        client._config_service.get_default_provider = lambda user_id=None: provider  # type: ignore[method-assign]
    served_seen: list[str] = []
    real_complete = client.complete

    async def _complete(*args, **kwargs):
        capture: dict = {}
        kwargs["served"] = capture
        out = await real_complete(*args, **kwargs)
        served_seen.append(f"{capture.get('provider', '?')}:{capture.get('model', '?')}")
        return out

    client.complete = _complete  # type: ignore[method-assign]
    classifier = IntentClassifier(llm_service=client)
    rows: list[dict] = []
    for phrase in phrases:
        for n in range(1, samples + 1):
            before = len(served_seen)
            intent, _reasoning = await classifier._classify_with_reasoning(phrase)
            category = getattr(getattr(intent, "category", None), "value", None)
            served = served_seen[-1] if len(served_seen) > before else "unrecorded"
            rows.append(
                {
                    "phrase": phrase,
                    "sample": n,
                    "category": (category or "").upper(),
                    "action": getattr(intent, "action", None) or "",
                    "confidence": getattr(intent, "confidence", None),
                    "served": served,
                }
            )
            print(
                f"[{phrase!r} #{n}] {rows[-1]['category']}/{rows[-1]['action']} "
                f"@{rows[-1]['confidence']} served={served}"
            )
    return rows


def write_report(rows: list[dict], out: Path, samples: int) -> None:
    served = ", ".join(sorted({r.get("served", "unrecorded") for r in rows})) or "unrecorded"
    lines = [
        "# Inversion Phase 3 — surface-2 floor probe",
        "",
        f"Run {datetime.now(timezone.utc):%Y-%m-%d %H:%MZ} · {samples} sample(s) per phrase · "
        "LAYER (m-43): `IntentClassifier._classify_with_reasoning` only (surface 1 bypassed, "
        "no session context, dev keychain key). Read by "
        "`scripts/inversion_phase3_deletion_gate.py` (SURFACE2_FLOOR_PROBES) to credit a "
        "category-reached row whose pattern the router does not replace: the row is OK to lose "
        "its pattern when EVERY sample lands in the expected action's own category.",
        "",
        # The gate refuses a report without this line (Arch condition 1).
        SERVED_LINE_PREFIX + served,
        "",
        HEADER,
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['phrase']} | {r['sample']} | {r['category']} | `{r['action']}` | "
            f"{r['confidence']} | {r.get('served', 'unrecorded')} |"
        )
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")


def report_served(path: Path) -> Optional[str]:
    """The report's served-model line, or None when absent (a pre-condition-1
    report, or a hand-written file) — the gate treats None as REFUSE."""
    if not path.exists():
        return None
    for line in path.read_text().splitlines():
        if line.startswith(SERVED_LINE_PREFIX):
            value = line[len(SERVED_LINE_PREFIX) :].strip()
            return value if value and value != "unrecorded" else None
    return None


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
                "served": cells[5] if len(cells) > 5 else "unrecorded",
            }
        )
    return by_phrase


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--phrase", action="append", required=True)
    ap.add_argument("--samples", type=int, default=5)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument(
        "--provider", default=None, help="force the classifier's provider (anthropic | openai)"
    )
    args = ap.parse_args()
    from dev_key_binding import developer_keys_bound

    with developer_keys_bound(require=True):
        result = asyncio.run(_probe(args.phrase, args.samples, args.provider))
    write_report(result, args.out, args.samples)
