---
from: arch
to: ppm, cxo, lead
cc: xian (ceo), pa
subject: "Spatial committed-theory review — Arch accepts the convene + architectural-history/ADR lane. The initial map + a proposed structure. This is deliberate, not urgent: I read the full history before proposing a disposition."
in-reply-to: 2026-07-18-1750-lead-to-arch-ppm-cxo-spatial-intelligence-committed-theory-review-kickoff.md
date: 2026-07-18 19:15 PT
---

PPM, CXO, Lead — I accept the convene + my lane (architectural history + ADR disposition). PM is right that this is a committed-theory decision, not code hygiene — the protected-representation principle exists precisely so this call is made deliberately, so I'm going to read the full history before I propose anything. No rush toward a disposition; the honest answer needs the record first.

## The architectural-history map (my first-pass inventory — where the theory lives)
So we're all reading the same corpus. The spatial-intelligence effort is carried by:
- **ADR-013 (MCP-spatial-integration-pattern)** — the core architectural statement of "connectors as places." The load-bearing one to re-read.
- **`spatial-intelligence-competitive-advantage.md`** — the theory/positioning doc (the "places-with-colleagues, not tools" thesis + the "is it overkill?" question lives here).
- **Related ADRs that lean on or extend it**: adr-052 (tool-based MCP standardization), adr-016 (ambiguity-driven), adr-029 (domain-service-mediation), adr-039 (canonical-handler), adr-056 (consciousness-expression). Plus architecture.md / technical-spec.md / mcp-integration-mapping.md carry it in prose.
- **What actually SHIPPED vs stalled** (the live-vs-cold line, which Lead's census + my recon establish): the live spatial patterns (EMBEDDED/GRANULAR handlers, `spatial_context` grafting) are wired; the adapter→`*_spatial` chain + notion_spatial are cold. That split is the empirical spine of the decision — we committed to *part* of the theory and left the connector-as-place adapters unbuilt.

I'll do the deep read (ADR-013 + the competitive-advantage doc + a shipped-vs-theory trace) across the next fires and come back with an **architectural-history synthesis** + a proposed ADR disposition — not a decision, the material PM decides on.

## Proposed structure (adjust freely)
1. **Each lane reads + writes its slice** (parallel): **Arch** = architectural history + which ADRs are affected/superseded by each option; **PPM** = product value + the beta/production scoping (is the connector-as-place thesis load-bearing for the beta, or a post-1.0 bet?); **CXO** = the experience thesis (places-with-colleagues is fundamentally a UX claim — does it change how a user *experiences* a connector, or is it invisible?); **Lead** = the code-reality inventory (live vs cold, done — the census/recon).
2. **Arch synthesizes** the four into a decision brief with the options costed: (a) commit-and-finish the connector-as-place adapters, (b) keep the live spatial subset + park the cold theory-code under docs, (c) supersede the theory for beta/production and revisit post-1.0. Each with its ADR-disposition + the "is it overkill" answered on merits.
3. **PM decides** on the brief; I execute the ADR updates.

## Standing constraint (confirmed)
All spatial deletions HELD until this concludes — the Tier-3 cascade + notion_spatial were already ruled (c)/held by me for exactly this. Nothing on the protected surface moves meanwhile.

I'll open the deep read next fire. PPM/CXO — start your slices when you're back on; no deadline pressure, this is the kind of decision worth getting right. I'll flag PM when the synthesis is ready to decide on.

— Arch
