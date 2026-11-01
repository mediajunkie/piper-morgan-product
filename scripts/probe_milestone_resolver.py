#!/usr/bin/env python3
"""#2197 cost probe: the op-local milestone resolver, live, on the developer's own key.

PPM's measure (2026-11-01): per call outcome, latency and the provider's own token
counts (``served["usage"]``, never estimated), over the six control phrasings named in
the #2197 brief plus two more "next" asks, against a fixture of the six milestones
``gh api repos/mediajunkie/piper-morgan-product/milestones`` returned on 2026-11-01
(state=open, the API default). Run with the inherited Anthropic env vars stripped.

Usage: python scripts/probe_milestone_resolver.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

# gh api repos/mediajunkie/piper-morgan-product/milestones, read 2026-11-01 11:4x PT.
MILESTONES = [
    {"title": "Ongoing", "state": "open", "due_on": None, "open_issues": 27, "closed_issues": 179},
    {"title": "Icebox", "state": "open", "due_on": None, "open_issues": 8, "closed_issues": 0},
    {
        "title": "Production",
        "state": "open",
        "due_on": "2027-02-02T00:00:00Z",
        "open_issues": 248,
        "closed_issues": 164,
    },
    {
        "title": "Fast Follow",
        "state": "open",
        "due_on": "2027-05-08T00:00:00Z",
        "open_issues": 50,
        "closed_issues": 1,
    },
    {
        "title": "Dot Releases (Post-MVP)",
        "state": "open",
        "due_on": "2027-09-02T00:00:00Z",
        "open_issues": 10,
        "closed_issues": 1,
    },
    {
        "title": "Enterprise",
        "state": "open",
        "due_on": "2028-10-30T00:00:00Z",
        "open_issues": 16,
        "closed_issues": 0,
    },
]

PHRASES = [
    # the six corpus rows of the brief's section 6
    "what's the progress on the MVP milestone?",
    "how is the Production milestone going",
    "status of the Fast Follow milestone",
    "any update on the next milestone",
    "what's the next milestone?",
    "when's the milestone deadline",
    # two more "next" asks
    "which milestone is due next?",
    "what milestone is coming up?",
]


async def run() -> int:
    from services.intent_service.milestone_resolve import pick_next_index, resolve_milestone
    from services.llm.clients import LLMClient

    llm = LLMClient()
    rows = []
    for phrase in PHRASES:
        res = await resolve_milestone(phrase, MILESTONES, llm_service=llm, user_id=None)
        bound = None
        if res.outcome == "picked":
            bound = MILESTONES[res.index]["title"]
        elif res.outcome == "next":
            i = pick_next_index(MILESTONES)
            bound = f"(code) {MILESTONES[i]['title']}" if i is not None else "(code) tie"
        rows.append((phrase, res, bound))
    print("| phrase | outcome | bound to | latency_ms | input_tokens | output_tokens |")
    print("|---|---|---|---|---|---|")
    for phrase, res, bound in rows:
        print(
            f"| {phrase} | {res.outcome} | {bound or '-'} | {res.latency_ms} | "
            f"{res.input_tokens} | {res.output_tokens} |"
        )
    measured = [r for _p, r, _b in rows if r.input_tokens is not None]
    if measured:
        n = len(measured)
        print(
            f"| mean (n={n} with usage) | | | {sum(r.latency_ms or 0 for r in measured) / n:.0f} | "
            f"{sum(r.input_tokens or 0 for r in measured) / n:.1f} | "
            f"{sum(r.output_tokens or 0 for r in measured) / n:.1f} |"
        )
    failed = sum(1 for _p, r, _b in rows if r.outcome == "failed")
    print(f"calls: {len(rows)}, failed: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    from dev_key_binding import developer_keys_bound

    with developer_keys_bound():
        sys.exit(asyncio.run(run()))
