# Spatial-Intelligence Committed-Theory Review — Architectural History (Arch lane, WIP)

**Status**: IN PROGRESS (opened 2026-07-19; deliberate multi-fire read). Becomes the Arch slice of the decision-brief when complete. Do NOT rush to a disposition — PM wants the full record first.

## The arc (the "invested but never fully committed" evidence)
- **ADR-013 (Aug 12 2025) — MAXIMALIST commitment.** "ALL external tool integrations MUST use the unified MCP + Spatial Intelligence pattern. No Direct API Integrations. Spatial intelligence as core competitive differentiator." Paired with `spatial-intelligence-competitive-advantage.md` (same date): "unassailable competitive moat," "8-dimensional spatial-intelligence architectural signature" (HIERARCHY/TEMPORAL/PRIORITY/… 8 orthogonal dimensions).
- **ADR-038 (Sep 30 / Oct 1 2025) — SOFTENED to pluralism.** Supersedes ADR-013's spatial-pattern policy. THREE patterns (Granular Adapter [Slack] / Embedded Intelligence [Notion] / Delegated MCP [Calendar]), "domain-appropriate, not universal." Claimed at the time: "Notion spatial 100% operational; all patterns production-proven; production-validated."
- **Now (Jul 2026) — PARTIAL, and split in two.** The Tier-3 census/recon surfaced much of the per-connector spatial-adapter surface as COLD.

## THE KEY FINDING — spatial intelligence is TWO layers, not one
1. **LIVE — the intent/MUX spatial-REASONING layer.** `place_detector`, `spatial_intent_classifier`, `canonical_handlers` spatial routing, `mux/orientation` + `consciousness` + `workspace_detection` + `lenses/hierarchy`, `context_assembler` (8-dim references), `spatial_context` grafting, github `response_context`. This is WIRED and shipping — the spatial *reasoning* at classification/orientation.
2. **COLD — the per-connector spatial-ADAPTER layer.** `intelligence/spatial/{gitbook,notion}_spatial`, `integrations/spatial/{devenvironment,linear}_spatial`, `mcp/consumer/{cicd,linear}_adapter`. The "connectors as places" adapters. Unreachable from the live app (Arch recon 2026-07-18). notion_spatial = 75%-abandoned (12 undefined methods) — which CONTRADICTS ADR-038's "Notion spatial 100% operational" claim (aspirational-or-regressed; a discrepancy to resolve).

## Why this reframes PM's decision
It is NOT "keep or kill spatial intelligence" — the reasoning layer (1) is live + load-bearing + differentiating, stays regardless. It IS "what to do with the cold connector-as-place ADAPTER layer (2)" — the specific unbuilt/abandoned part. And it sharpens "is it overkill?": the *per-connector 8-dimensional adapter* ambition (2) may be overkill (never fully built; connectors work via the ADR-070 consumer path WITHOUT it); the *intent/MUX spatial reasoning* (1) is live and is the actual differentiator that shipped.

## TODO (next fires — deliberate)
- [ ] Verify the two-layer live/cold split precisely (reachability of each module from the running app).
- [ ] Read ADR-038 consequences/rejected-options in full + confirm the "production-proven" vs current-cold discrepancy.
- [ ] Map which ADRs are affected/superseded under each option (013 already deprecated; 038 is current — does the decision amend 038?).
- [ ] Reconcile with the live-vs-cold from Lead's census (his code-reality inventory = the empirical partner to this history).
- [ ] Draft the 3 costed options (commit-and-finish adapters / keep-live-reasoning-park-cold-adapters / supersede-adapter-ambition-for-beta) with ADR disposition each.
