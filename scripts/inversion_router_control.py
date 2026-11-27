#!/usr/bin/env python3
"""Router ×N control — route a few phrases N times each through the SAME
router + grammar the Phase-1 scorer uses, and tabulate the spread.

The refined rule 7 (Arch, 2026-10-10) screens a catalog-description candidate
on its moved rows plus a sentinel set BEFORE the one full ~577-call run that
only the landing candidate owes. Until 2026-10-11 every lane wrote its own
throwaway ``control7.py``; this is that script, kept.

Usage (env-stripped per CLAUDE.md; PIPER_CREDENTIAL_STORE=db, a key named after the
env -u flags, and --provider, #2340):
    env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN \\
      PIPER_CREDENTIAL_STORE=db ANTHROPIC_API_KEY=… \\
      venv/bin/python scripts/inversion_router_control.py --provider anthropic --max-usd N \\
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
import time
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


async def _project_consult(
    phrases: list[str], samples: int, provider: Optional[str], project_names: list[str]
) -> list[dict]:
    """Issue 2425 screen: per sample, the main route; then, on CLARIFY, the live path's
    own ``consult_projects_on_clarify`` with ``project_names`` as the stored projects.

    Same functions as the live path: ``route``, the consult, its fact line, its accept
    rule and its ceiling. Differences from live, stated: the main call has no session
    block (the script has no session), the project read is a stub returning the given
    names (no DB), and both router calls go out with ``user_id=None`` (a measurement
    call, as the main control above).

    Timing (monotonic): ``main_s`` is around the awaited main ``route()``; ``consult_s``
    is around the awaited ``consult_projects_on_clarify`` call, which includes the
    stubbed read, the fact-line build and the ceiling's ``wait_for`` around the second
    ``route()``, the same wrapper live uses. ``ceiling_hit`` is True when that wait_for
    cancelled the second call."""
    from types import SimpleNamespace

    from services.intent_service.inversion_router import (
        SessionSnapshot,
        derive_routing_grammar,
        route,
    )
    from services.intent_service.project_consult import consult_projects_on_clarify
    from services.llm.clients import LLMClient

    grammar = derive_routing_grammar()
    llm = LLMClient()
    if provider:
        llm._config_service.get_default_provider = lambda user_id=None: provider  # type: ignore[method-assign]
    projects = [
        SimpleNamespace(id=f"screen-{i}", name=n, created_at=None)
        for i, n in enumerate(project_names)
    ]

    async def read(_user_id):
        return projects

    rows: list[dict] = []
    for phrase in phrases:
        for n in range(1, samples + 1):
            row: dict = {
                "phrase": phrase,
                "sample": n,
                "main": "ERROR",
                "main_s": None,
                "fired": False,
                "consult_route": "-",
                "consult_args": {},
                "accepted": False,
                "final": "ERROR",
                "final_args": {},
                "consult_s": None,
                "ceiling_hit": False,
                "error": None,
            }
            seen: dict = {}

            async def recorded_route(message, session_state=None, **kw):
                seen["fired"] = True
                seen["block"] = getattr(session_state, "state_block", None)
                kw["user_id"] = None
                try:
                    d = await route(message, session_state, **kw)
                except asyncio.CancelledError:
                    seen["cancelled"] = True
                    raise
                seen["decision"] = d
                return d

            try:
                t0 = time.monotonic()
                main = await route(phrase, None, llm_service=llm, grammar=grammar, user_id=None)
                row["main_s"] = time.monotonic() - t0
                row["main"] = main.route_label
                final = main
                if main.outcome == "clarify":
                    t1 = time.monotonic()
                    final = await consult_projects_on_clarify(
                        phrase,
                        main,
                        "",
                        route=recorded_route,
                        router_snapshot=SessionSnapshot,
                        llm_service=llm,
                        grammar=grammar,
                        user_id="screen",
                        read_projects=read,
                    )
                    if seen.get("fired"):
                        row["consult_s"] = time.monotonic() - t1
                row["fired"] = bool(seen.get("fired"))
                row["ceiling_hit"] = bool(seen.get("cancelled"))
                second = seen.get("decision")
                if second is not None:
                    row["consult_route"] = second.route_label
                    row["consult_args"] = dict(second.args or {})
                row["accepted"] = final is not main
                row["final"] = final.route_label
                row["final_args"] = dict(final.args or {})
            except Exception as e:  # probe discipline: recorded, never aborts
                row["error"] = f"{type(e).__name__}: {e}"
            rows.append(row)
            print(
                f"[{phrase!r} #{n}] main={row['main']} fired={row['fired']} "
                f"consult={row['consult_route']} accepted={row['accepted']} final={row['final']}"
                + (f" consult_s={row['consult_s']:.3f}" if row["consult_s"] is not None else "")
                + (" CEILING" if row["ceiling_hit"] else "")
                + (f" ERR {row['error']}" if row["error"] else "")
            )
    return rows


def _secs(v: Optional[float]) -> str:
    return f"{v:.3f}" if isinstance(v, (int, float)) else "-"


def write_project_consult_report(
    rows: list[dict], out: Path, samples: int, label: str, project_names: list[str]
) -> None:
    from statistics import median

    from services.intent_service.list_consult import D5_CONSULT_CEILING_S
    from services.intent_service.project_consult import project_fact_line

    by_phrase: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_phrase[r["phrase"]].append(r)
    fact = project_fact_line(
        [type("P", (), {"name": n, "id": str(i)})() for i, n in enumerate(project_names)]
    )
    lines = [
        f"# Project consult (2425) screen ×{samples} — {label}",
        "",
        f"Run {datetime.now(timezone.utc):%Y-%m-%d %H:%MZ} · {samples} sample(s) per phrase · "
        f"ceiling {D5_CONSULT_CEILING_S} s · consult fact line: `{fact}`",
        "",
        "| phrase | main routes | consults fired | accepted | final routes | consult s min / median / max | timeouts |",
        "|---|---|---|---|---|---|---|",
    ]
    for phrase, rs in by_phrase.items():
        mains = Counter(r["main"] for r in rs)
        finals = Counter(r["final"] for r in rs)
        fired = [r for r in rs if r["fired"]]
        secs = [r["consult_s"] for r in fired if isinstance(r["consult_s"], (int, float))]
        stats = f"{min(secs):.3f} / {median(secs):.3f} / {max(secs):.3f}" if secs else "-"
        lines.append(
            f"| {phrase} | "
            + ", ".join(f"`{k}` ×{v}" for k, v in mains.most_common())
            + f" | {len(fired)} | {sum(1 for r in rs if r['accepted'])} | "
            + ", ".join(f"`{k}` ×{v}" for k, v in finals.most_common())
            + f" | {stats} | {sum(1 for r in rs if r['ceiling_hit'])} |"
        )
    lines += [
        "",
        "## Samples",
        "",
        "| phrase | # | main | main s | fired | consult route | consult args | accepted | final | final args | consult s | ceiling hit | error |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['phrase']} | {r['sample']} | `{r['main']}` | {_secs(r['main_s'])} | {r['fired']} | "
            f"`{r['consult_route']}` | {_fmt_args(r['consult_args'])} | {r['accepted']} | `{r['final']}` | "
            f"{_fmt_args(r['final_args'])} | {_secs(r['consult_s'])} | {r['ceiling_hit']} | {r['error'] or ''} |"
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote {out}")


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
    ap.add_argument(
        "--max-usd",
        type=float,
        default=None,
        help="the most this run may spend, in dollars; required for a run that makes calls (#2383)",
    )
    ap.add_argument(
        "--approved-by",
        default=None,
        help="for a cap above $10: the mail id of Exec's relay of xian's approval (ADR-084 D2)",
    )
    ap.add_argument(
        "--projects",
        default=None,
        help=(
            "issue 2425 screen: comma-separated stored project names; each sample runs the "
            "main route and, on CLARIFY, the live project consult with these names"
        ),
    )
    args = ap.parse_args()
    sys.path.insert(0, str(ROOT / "scripts"))
    from dev_key_binding import developer_keys_bound, providers_from_flag

    project_names = (
        [n.strip() for n in args.projects.split(",") if n.strip()] if args.projects else None
    )
    _providers = providers_from_flag(args.provider)
    with developer_keys_bound(
        providers=_providers,
        max_usd=args.max_usd,
        approved_by=args.approved_by,
        # 2425: up to two router calls per sample (the main call and the consult).
        planned_calls=len(args.phrase) * args.samples * (2 if project_names else 1),
        require=True,
    ):
        if project_names:
            rows = asyncio.run(
                _project_consult(args.phrase, args.samples, args.provider, project_names)
            )
        else:
            rows = asyncio.run(_control(args.phrase, args.samples, args.provider))
    if project_names:
        write_project_consult_report(rows, args.out, args.samples, args.label, project_names)
    else:
        write_report(rows, args.out, args.samples, args.label)
    return 1 if any(r["error"] for r in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
