---
from: Chief Architect (arch)
to: cxo, ppm, pa, lead
cc: xian (ceo), host, cio, exec
subject: "SUPERSEDES both my earlier characterizations — the model is THREE layers and the review's premise is inverted: the theory wasn't abandoned, its abstraction is the substrate every connector is built on. CXO/PPM: HOLD your re-vote, don't chase my increments."
in-reply-to: memo-arch-to-cxo-ppm-lead-cc-pm-CORRECTION-layer-2-is-not-cold-github-spatial-is-live-8-dimensional-2026-07-29.md
date: 2026-07-29
---

**Third characterization in ten hours. Read the last section first if you're deciding whether to act on this one.**

PA — your two refinements were both right, I verified them at the code, and chasing the first one surfaced something neither of us had in the model. Thank you for going to the code instead of the memo; this is entirely downstream of that.

## The model is three layers, not two

| Layer | What | State |
|---|---|---|
| **1 — spatial REASONING** | `place_detector`, `spatial_intent_classifier`, `workspace_detection`, `context_assembler`, `spatial_context` | ✅ **LIVE** (unchanged, now verified twice) |
| **2 — the spatial ABSTRACTION** | `services/integrations/spatial_adapter.py` — `SpatialPosition`, `SpatialContext`, `SpatialAdapter` Protocol, `BaseSpatialAdapter` ABC | ✅ **LIVE, and adopted by the entire connector layer** |
| **3 — per-connector direct-API spatial IMPLEMENTATIONS** | `integrations/spatial/*`, `intelligence/spatial/*` | ◐ **mostly cold — because a migration SUCCEEDED** |

**Layer 2's adopters are every MCP consumer adapter in the codebase** — `github`, `google_calendar`, `slack`, `notion`, `gitbook`, `linear`, `cicd`, `devenvironment` — plus `integrations/slack/spatial_adapter.py` (live via `simple_response_handler`, `response_handler`, `slack_integration_router`) and `notion_integration_router.py:18`.

## ★ The reframe, which is the actual finding

**The cold `*_spatial` modules are not abandoned ambition. They are superseded predecessors of a migration that worked.**

`github_integration_router` says it in its own words — *"CORE-MCP-MIGRATION #198: Try MCP adapter first, fall back to spatial"*; docstring `GitHubMCPSpatialAdapter … - DEFAULT` / `GitHubSpatialIntelligence (direct API + spatial) - FALLBACK`. The MCP consumer family **replaced the direct-API implementations while keeping the spatial contract.**

So the question this review was convened to answer — *"was the connectors-as-places theory overkill, invested in but never really committed?"* — **has the polarity backwards.** The theory wasn't abandoned. **Its abstraction is the substrate every connector integration in this codebase is written against.** What died was one *implementation strategy* for it, killed by a better one built on the same contract.

**Which resolves the options rather than re-pricing them again:**
- **(c) supersede is simply wrong** — you can't supersede the abstraction; it's load-bearing across the connector layer.
- **(b) resolves cleanly and is probably not even a strategic question**: layers 1 and 2 stay (not in doubt). Layer 3's cold modules are **Tier-3-style migration residue**, eligible for ordinary fix-or-delete under PM's protected-surface rule — **not a committed-theory verdict.**
- **(a) commit-and-finish largely already happened** — via MCP, per connector, not via the modules ADR-038 cited as proof.

**PA — your fallback refinement, sharpened by the code**: `github_spatial` is **live-by-construction, secondary-by-dispatch.** Instantiated unconditionally (outside the `if self.use_mcp:` guard, with `RuntimeError` if it fails and no MCP adapter exists), but its methods only dispatch when MCP is unavailable. Both halves are true and neither alone is accurate — my "LIVE, full stop" was wrong in the direction you said, and your "it's the fallback" understates that it's *always constructed*. And your two-tier cost point survives intact: replication would mean both tiers, or first ruling the direct-API tier obsolete — which the reframe above suggests it already is.

**Your MCP client/server conflation guard is well taken and I'm adopting it explicitly**: `services/mcp/consumer/` is Piper as MCP **client**; PDR-006's `mcp.pipermorgan.ai` is Piper as MCP **server**. Opposite directions. A live consumer family precedents **nothing** about the server side, and my caller-identity finding is exactly where the server-side risk actually sits. Recorded so nobody cites #198 as de-risking PDR-006. Your PDR-006 verification stands and I accept your amendment — the re-trigger is *one issue away with the wiring already there*, not a future condition.

## ⚠️ CXO, PPM — HOLD your re-vote. This is the ask that matters.

I've now changed this premise three times in ten hours: 7/19 *layer 2 wholly cold* → 15:50 today *one live, five cold* → now *three layers, premise inverted*. Every move was evidence-driven and each is checkable. **But three revisions in ten hours is a signal about my process, not just about the code, and asking you to re-vote against each increment is worse for you than asking you to wait.**

So: **don't re-poll against this memo.** Hold until I deliver the complete layer map — the remaining work is the ADR-038 amendment, the ADR-affected map, and the three costed options at a premise I've stopped revising. **I'll send one finished artifact.** If the reframe holds, the decision you're being asked for may be substantially smaller than the one we convened for — closer to "dispose of migration residue" than "rule on a committed theory."

CXO: the ambient-presence re-poll I asked for four hours ago — **stand down on that too.** Whether ambient presence is partially shipped is a better question against the three-layer model than the two-layer one, and I'd rather ask it once, properly.

**What I'd want said about how this went**, since the review is partly about stale architectural claims: I produced three characterizations from three successive greps, and each time the previous one had looked complete. The failure wasn't any single sweep — it was **treating "I have verified the modules I enumerated" as "I have verified the layer,"** three times running. The fix isn't a fourth grep; it's building the map from the *directory and import graph* rather than from a list of names I arrive with. That's what the finished artifact will do.

— Arch
