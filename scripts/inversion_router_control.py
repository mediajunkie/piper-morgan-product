#!/usr/bin/env python3
"""Router ×N control — route a few phrases N times each through the SAME
router + grammar the Phase-1 scorer uses, and tabulate the spread.

The refined rule 7 (Arch, 2026-10-10) screens a catalog-description candidate
on its moved rows plus a sentinel set BEFORE the one full ~577-call run that
only the landing candidate owes. Until 2026-10-11 every lane wrote its own
throwaway ``control7.py``; this is that script, kept.

Usage (env-stripped per CLAUDE.md; keys resolve via Keychain):
    env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \\
      venv/bin/python scripts/inversion_router_control.py --provider anthropic \\
      --samples 6 --phrase "show today's tasks" --phrase "what needs my attention?" \\
      --label candidate --out /path/report.md

Run it once on the baseline tree and once on the candidate tree (same
phrases, same N, same provider) and compare the two tables. The report's
``served`` line says which model answered (m-43); a run whose served line is
not the one you meant is not the measurement you meant.
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


async def _control(phrases: list[str], samples: int, provider: Optional[str]) -> list[dict]:
    from services.intent_service.inversion_router import derive_routing_grammar, route
    from services.llm.clients import LLMClient

    grammar = derive_routing_grammar()
    llm = LLMClient()
    if provider:
        llm._config_service.get_default_provider = lambda user_id=None: provider  # type: ignore[method-assign]
    rows: list[dict] = []
    for phrase in phrases:
        for n in range(1, samples + 1):
            try:
                d = await route(phrase, None, llm_service=llm, grammar=grammar, user_id=None)
                label = d.route_label
                conf = d.confidence
                # #2186 (2026-10-28): the args the router emitted, so a screen
                # sees whether a qualifier (milestone, label, count, repo) is
                # already extracted under the wording being measured.
                args_ = dict(d.args or {})
                served = (
                    f"{d.served_provider}:{d.served_model}"
                    if d.served_provider and d.served_model
                    else "unresolved"
                )
                err = d.error
            except Exception as e:  # probe discipline: recorded, never aborts
                label, conf, args_, served, err = (
                    "ERROR",
                    None,
                    {},
                    "unresolved",
                    f"{type(e).__name__}: {e}",
                )
            rows.append(
                {
                    "phrase": phrase,
                    "sample": n,
                    "route": label,
                    "confidence": conf,
                    "args": args_,
                    "served": served,
                    "error": err,
                }
            )
            print(
                f"[{phrase!r} #{n}] {label} @{conf} served={served}"
                + (f" ERR {err}" if err else "")
            )
    return rows


def _fmt_args(args: Optional[dict]) -> str:
    """``key=value`` pairs, sorted, or ``-`` — one cell per sample (#2186)."""
    if not args:
        return "-"
    return "; ".join(f"{k}={v}" for k, v in sorted(args.items()))


def write_report(rows: list[dict], out: Path, samples: int, label: str) -> None:
    by_phrase: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_phrase[r["phrase"]].append(r)
    served = Counter(r["served"] for r in rows)
    errors = sum(1 for r in rows if r["error"])
    lines = [
        f"# Router ×{samples} control — {label}",
        "",
        f"Run {datetime.now(timezone.utc):%Y-%m-%d %H:%MZ} · {samples} sample(s) per phrase · "
        f"{len(rows)} router calls · {errors} ERROR · served: "
        + "; ".join(f"{k} ({v}/{len(rows)})" for k, v in served.most_common()),
        "",
        "| phrase | routes (count) | confidence range |",
        "|---|---|---|",
    ]
    for phrase, rs in by_phrase.items():
        counts = Counter(r["route"] for r in rs)
        spread = ", ".join(f"`{k}` ×{v}" for k, v in counts.most_common())
        confs = [r["confidence"] for r in rs if isinstance(r["confidence"], (int, float))]
        rng = f"{min(confs):.2f}–{max(confs):.2f}" if confs else "-"
        lines.append(f"| {phrase} | {spread} | {rng} |")
    lines += [
        "",
        "## Samples",
        "",
        "| phrase | # | route | conf | args | served | error |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['phrase']} | {r['sample']} | `{r['route']}` | {r['confidence']} | {_fmt_args(r.get('args'))} | {r['served']} | {r['error'] or ''} |"
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out}")


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--phrase", action="append", required=True)
    ap.add_argument("--samples", type=int, default=6)
    ap.add_argument("--provider", default=None, help="anthropic = alpha's Haiku-class router")
    ap.add_argument("--label", default="control", help="baseline / candidate / …")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    sys.path.insert(0, str(ROOT / "scripts"))
    from dev_key_binding import developer_keys_bound

    with developer_keys_bound(require=True):
        rows = asyncio.run(_control(args.phrase, args.samples, args.provider))
    write_report(rows, args.out, args.samples, args.label)
    return 1 if any(r["error"] for r in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
