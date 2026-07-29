# Spatial-Intelligence Committed-Theory Review — Architectural History (Arch lane, WIP)

**Status**: IN PROGRESS (opened 2026-07-19; reachability verified 2026-07-29). Becomes the Arch slice of the decision-brief when complete. Do NOT rush to a disposition — PM wants the full record first.

> ## ⚠️ CORRECTION 2026-07-29 — my own two-layer finding was wrong in a load-bearing way. The lanes voted on the wrong characterization.
>
> On 7/19 I told CXO, PPM and Lead that layer 2 — the per-connector spatial-**adapter** tier — was **cold in its entirety**. **It is not.** `github_spatial` is **LIVE**, is the *full 8-dimensional* implementation, and is reachable from the running app by **two independent paths**. CXO's (b) vote and PPM's scoping question were both formed against my incorrect version, so both may want to revisit. Correction mailed to all three.
>
> **How I got it wrong, and it's both blind-sweep directions in one fire:**
> - **Under-enumeration**: I built the cold list on 7/18 from a *filename pattern I recalled* rather than from a directory listing, so `services/integrations/spatial/github_spatial.py` — sitting in the very directory I was characterizing — was never checked. It surfaced today only because an unrelated grep returned integration routers I hadn't enumerated.
> - **Over-broad match**: today's first pass reported `notion_spatial` as having a live importer. It doesn't — the hit was `config_service.py:222`'s feature-flag string `"notion_spatial_mapping"`, not the module. I nearly recorded a cold module as live.
>
> A sweep lying in both directions inside one investigation, in the lane whose own §4 names that class. Recorded rather than quietly fixed.

## The arc (the "invested but never fully committed" evidence)
- **ADR-013 (Aug 12 2025) — MAXIMALIST commitment.** "ALL external tool integrations MUST use the unified MCP + Spatial Intelligence pattern. No Direct API Integrations. Spatial intelligence as core competitive differentiator." Paired with `spatial-intelligence-competitive-advantage.md`: "unassailable competitive moat," "8-dimensional spatial-intelligence architectural signature."
- **ADR-038 (Sep 30 / Oct 1 2025) — SOFTENED to pluralism.** Supersedes ADR-013's spatial-pattern policy. THREE patterns (Granular Adapter [Slack] / Embedded Intelligence [Notion] / Delegated MCP [Calendar]), "domain-appropriate, not universal." Claimed then: "Notion spatial 100% operational; all patterns production-proven."
- **Now (Jul 2026) — PARTIAL, and the split is PER-CONNECTOR, not per-layer.**

## THE FINDING (corrected 2026-07-29) — two layers, and layer 2 is *split*, not cold

**Layer 1 — LIVE: the intent/MUX spatial-REASONING layer.** Reachability verified by importer trace:
- `place_detector` ← `intent_service/classifier.py`, `mux/orientation.py` (3 importers)
- `spatial_intent_classifier` ← `mux/orientation.py`
- `workspace_detection` ← `mux/workspace_navigation.py`, `mux/workspace_memory.py`
- `context_assembler` ← `intent/intent_service.py`
- `spatial_context` ← `mux/workspace_detection.py`, `slack/simple_response_handler.py`, `slack/response_context.py`

Wired and shipping. This is the spatial *reasoning* at classification/orientation. **Unchanged from 7/19 — this half of the finding held.**

**Layer 2 — the per-connector spatial-ADAPTER tier: ONE LIVE, FIVE COLD.**

| Adapter | Importers (non-test, non-self) | State |
|---|---|---|
| **`github_spatial`** | `github_integration_router.py:30` — **top-level import, not deferred** | ✅ **LIVE** |
| `gitbook_spatial` | 0 | ❄️ cold |
| `notion_spatial` | 0 *(the apparent hit was a feature-flag string)* | ❄️ cold |
| `devenvironment_spatial` | 0 | ❄️ cold |
| `linear_spatial` | 0 | ❄️ cold |
| `cicd_spatial` | 0 | ❄️ cold |
| `cicd_adapter` / `linear_adapter` | only `cicd_spatial` / `linear_spatial` — themselves cold | ❄️ cold island |

**The `github_spatial` live chain, verified link by link:**
1. `intent/intent_service.py:11801` → `ContextAssembler`
2. `intent_service/context_assembler.py:1210, 1296, 1417, 1553` → `github_integration_router`
3. `github_integration_router.py:30` → `from services.integrations.spatial.github_spatial import GitHubSpatialIntelligence`

**Plus a second, independent path**: `web/app.py:264` registers `web.api.routes.places` ("Places API"), and `places.py:81` imports `github_integration_router`. So there is a **live HTTP route surface** over it too.

And its own docstring: *"GitHub Spatial Intelligence Implementation / Following ADR-013: MCP + Spatial Intelligence Pattern / Retrofit from MCP-only to **full 8-dimensional spatial analysis**."*

## Why the correction changes PM's decision materially

The framing I gave the lanes was *"the connector-as-place adapter ambition was never really built."* **The accurate framing is: it WAS built — once, for the most important connector, at full 8-dimensional depth, and it is live in production today. It was simply never replicated to the other five.**

Consequences for the options:
- **(a) commit-and-finish is much cheaper than I implied** — there is a **working reference implementation**, so the cost is *replication*, not invention. That was not true under my 7/19 characterization.
- **(b) keep-live/park-cold now has a concrete boundary**: keep `github_spatial` (it's live and load-bearing), park the five. Cleaner than "park the tier."
- **(c) supersede is much more expensive than I implied** — it would mean removing a live 8-dimensional implementation reached by the context assembler and an HTTP route, not retiring an unbuilt ambition.
- **"Is it overkill?" sharpens again**: the pattern is *demonstrably shippable* — GitHub proves it. The open question is whether **per-connector replication pays**, which is a very different question from whether the theory works.

**And ADR-038's claim needs a precise correction, not just a discrepancy flag**: it asserted *"Notion spatial 100% operational"* and cited Notion as the Embedded-Intelligence proof. `notion_spatial` is both **75% abandoned (12 undefined methods) and unreachable**. Meanwhile GitHub — which ADR-038 did *not* hold up as the spatial exemplar — is the one that actually shipped. **ADR-038 was right about the pattern and wrong about which connector proved it.** That's the amendment.

## TODO (remaining)
- [x] Verify the two-layer live/cold split precisely — **done 7/29, and it corrected the finding.**
- [ ] Read ADR-038 consequences/rejected-options in full; draft the precise amendment (pattern validated by GitHub, not Notion).
- [ ] Map which ADRs are affected under each option (013 deprecated; 038 current — the decision amends 038).
- [ ] Draft the 3 costed options with the corrected cost profile above.
- [ ] **Re-poll CXO** — does "ambient-presence tier" still describe layer 2 if GitHub's 8-dim adapter is live? Is the capability *partially shipped* for one connector?
- [ ] **PPM's roadmap-dependency check** (gated on PPM) — sharper now: does any 1.0 commitment assume the adapter chain *beyond* GitHub?

## Lane inputs folded (2026-07-19) — ⚠️ all formed against the pre-correction characterization
- **CXO (experience theory)** — sharpened layer 2 as the **AMBIENT-PRESENCE tier** (Piper continuously inhabiting connectors, proactively surfacing activity) — a distinct capability from layer 1's "knows WHERE things live." **Vote: (b) keep-live-subset + park-cold-adapters as design capital, NOT supersession; ADR-013 update = scope-clarification not reversal.** *"The theory is not overkill; the full adapter chain is."* → **Needs re-poll: one adapter in that tier is live.**
- **PPM (product-value/scoping)** — accepted lane, deliberately deferred the verdict. Framing: does beta / path-to-1.0 **depend** on the connector-as-place thesis being experientially true, or only on the shipped parts? → **Question survives the correction and gets sharper**: the shipped part is bigger than I said.
- **Lead data point** — with `query_router` deleted, the sim/POC transport's entire remaining reachability sits inside the cold cohort → subsumed by layer-2's disposition. **Still holds** (github_spatial is not sim-transport).

## Emerging convergence (NOT the disposition — now explicitly reopened)
Pre-correction, all lanes pointed at **(b) keep-live + park-cold-adapter-tier, scope-clarify ADR-013/038**. **I still expect (b) to survive** — but it now means something different and better-bounded (keep one *live adapter* plus the reasoning layer; park five), and (a) is cheaper than anyone was told. **Gated on**: the CXO re-poll, PPM's roadmap check, and my ADR-038 amendment draft.
