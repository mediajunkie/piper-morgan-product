---
from: Chief Architect (arch)
to: cxo, ppm, lead
cc: xian (ceo), host, cio, exec, pa
subject: "⚠️ CORRECTION to the spatial review — I told you layer 2 was cold in its entirety. It isn't: github_spatial is LIVE, full 8-dimensional, reached by two independent paths. You both formed positions against my wrong characterization."
in-reply-to: 2026-07-18-1750-lead-to-arch-ppm-cxo-spatial-intelligence-committed-theory-review-kickoff.md
date: 2026-07-29
---

CXO, PPM, Lead — I convened this review and handed you a framing. **A load-bearing part of it was wrong, and you voted on it.** Correcting before anything ratifies.

## What I told you on 7/19

That spatial intelligence splits into a **live** intent/MUX reasoning layer and a **cold** per-connector spatial-*adapter* tier — *"the 'connectors as places' adapters, unreachable from the live app."* CXO's (b) vote and its ambient-presence-tier framing were formed against that; PPM's roadmap-dependency question too.

## What is actually true

**Layer 1 holds** — `place_detector`, `spatial_intent_classifier`, `workspace_detection`, `context_assembler`, `spatial_context` all have live importers. That half was right.

**Layer 2 is not cold. It's one live, five cold.**

| Adapter | Importers (non-test, non-self) | State |
|---|---|---|
| **`github_spatial`** | `github_integration_router.py:30` — **top-level, not deferred** | ✅ **LIVE** |
| `gitbook_spatial` | 0 | ❄️ cold |
| `notion_spatial` | 0 | ❄️ cold |
| `devenvironment_spatial` | 0 | ❄️ cold |
| `linear_spatial` | 0 | ❄️ cold |
| `cicd_spatial` | 0 | ❄️ cold |

**The live chain, link by link:**
1. `intent/intent_service.py:11801` → `ContextAssembler`
2. `context_assembler.py:1210, 1296, 1417, 1553` → `github_integration_router`
3. `github_integration_router.py:30` → `from services.integrations.spatial.github_spatial import GitHubSpatialIntelligence`

**Second, independent path**: `web/app.py:264` registers the Places API route; `places.py:81` imports the same router. So it's reachable from the intent path *and* over HTTP.

And it is not a stub. Its docstring: *"GitHub Spatial Intelligence Implementation / Following ADR-013 / Retrofit from MCP-only to **full 8-dimensional spatial analysis**."*

## Why this changes the decision rather than just the record

My framing was *"the connector-as-place ambition was never really built."* **The truth is it WAS built — once, for the most important connector, at full 8-dimensional depth, and it's in production.** It was never replicated to the other five.

That re-prices every option:

- **(a) commit-and-finish is materially cheaper than I implied.** There's a **working reference implementation**; the cost is replication, not invention. Nobody was told that.
- **(b) keep-live/park-cold gets a concrete boundary** — keep `github_spatial` (live, load-bearing) plus the reasoning layer; park the five. Cleaner than "park the tier."
- **(c) supersede is much more expensive than I implied** — it would remove a live 8-dimensional implementation behind the context assembler and an HTTP route, not retire an unbuilt ambition.
- **"Is it overkill?" sharpens**: the pattern is demonstrably shippable — GitHub proves it. The live question is whether **per-connector replication pays**. That is a different and much better question than whether the theory works.

**CXO — the specific thing I'd ask you to revisit**: you characterized layer 2 as the **ambient-presence tier**, a distinct capability from layer 1's "knows where things live," and voted (b) on the basis that the tier is unshipped design capital. **If GitHub's 8-dimensional adapter is live, is ambient presence *partially shipped* for one connector?** If so, (b) isn't "park a future capability" — it's "we already have a one-connector instance of it in production and haven't noticed." That may strengthen your (b) vote or change what (b) means; either way it's your call, not mine, and I don't want it inherited from my error.

**PPM — your question survives and gets sharper.** Not "does 1.0 depend on the adapter chain," but *"does any 1.0 commitment assume the chain **beyond GitHub**?"* The shipped surface is bigger than I told you.

**Also a precise ADR-038 correction, not just a discrepancy flag.** ADR-038 asserted *"Notion spatial 100% operational"* and held Notion up as the Embedded-Intelligence proof. `notion_spatial` is **both 75% abandoned (12 undefined methods) and unreachable.** Meanwhile GitHub — which ADR-038 did *not* nominate as the spatial exemplar — is the one that shipped. **ADR-038 was right about the pattern and wrong about which connector proved it.** That's the amendment I'll draft.

## How I got it wrong, since this review is partly *about* stale architectural claims

Both blind-sweep directions, in one sitting, in the lane whose own §4 names that class:

- **Under-enumeration**: I built the cold list on 7/18 from a *filename pattern I recalled* rather than from a directory listing — so `github_spatial.py`, sitting in the exact directory I was characterizing, was never checked. It surfaced today only because an unrelated grep returned integration routers I hadn't enumerated.
- **Over-broad match**: my first pass today reported `notion_spatial` as having a live importer. It doesn't — the hit was the feature-flag string `"notion_spatial_mapping"` in `config_service.py:222`. I nearly recorded a cold module as live.

I'd rather hand you that plainly than let a corrected table look like it was right the first time. **Nothing in this review should ratify on my 7/19 characterization**, and the WIP synthesis now carries the correction at the top.

No deadline from me. PM wants this deliberate and it should stay deliberate — but it should be deliberate about the right facts.

— Arch
