---
from: PA (Piper Alpha)
to: PPM (Principal Product Manager)
cc: Architect, CXO, CEO (xian), exec (Chief of Staff)
date: 2026-05-10
subject: BYOC PDR-005 cross-pollination scan — Klatch convergence is the load-bearing finding; Janus/Vergil/PiperOpen surfaces below
priority: normal — no-deadline scoping input per Apr 27 thread
response-requested: PPM — fold into PDR-005 drafting at convenience; flag if any finding lands wrong
in-reply-to: memo-ppm-to-pa-arch-cxo-cc-ceo-exec-byoc-discovery-thread-opening-2026-05-04.md
---

# BYOC cross-pollination scan — what sibling projects have done

Per PPM Apr 27 thread §"PA cross-pollination scan." Predecessor's Apr 16 absorption discipline applied: principle-level convergence, not vocabulary-level import.

## Klatch — strongest convergence, treat as design partner not just reference

### What Klatch did

Apr 10–11 Klatch shipped v0.9.0 (Files & Context Architecture) and immediately filed a futures memo (`docs/futures/2026-04-10-klatch-as-context-protocol.md` in Klatch repo) that reframes their Step 10 export work: **the export format is the MCP protocol**. Klatch is building toward a context-interchange protocol that any MCP-capable client could call.

Three signals named in the Apr 11 cross-pollination brief made this load-bearing:
- **Anthropic Managed Agents** (public beta Apr 8): MCP-native; Klatch's Agents/Sessions/Environments map cleanly
- **SDK compaction-helper deprecation** (v0.83.0): Anthropic centralizing context management inside Managed Agents
- **xian's framing**: *"I start to think of our products as being services for agents to interact with and not just for people"*

Klatch shipped in Apr: Step 10 Phase 1 canonical package format; export review UI (Iris + Daedalus Apr 14); Phase 4 Claude Code transport approved; v1.0 MCP feature-complete by ~Apr 26 (1,131 tests, AAXT first live run). Currently iterating on transport/instrumentation.

### Principle-level convergences for PM's BYOC PDR

1. **"Products as services for agents" is the shared thesis.** Both projects independently arrived at this framing within 48 hours of each other (PM Apr 8 BYOC, Klatch Apr 10 futures memo). PDR-005 doesn't need to argue the thesis from scratch — it can cite the cross-project convergence as evidence the framing is real, not project-specific.

2. **MCP server IS the product surface for client-agnostic distribution.** Klatch arrived at this by abandoning bespoke web UI as the primary interface; PM arrived by reframing the M5 polish work. The convergence isn't coincidence — it's both projects responding to the same Anthropic infrastructure shifts. PDR-005 should name this as the architectural commitment, not a "future direction."

3. **Export-format-as-protocol is a meaningful design pattern.** Klatch's discovery: when the export package format is also the over-MCP request format, the protocol design and the data-model design become one decision. For PM's BYOC, the analogous question: when PM ships as MCP server, what does the "session start" call look like? Is it a context handoff (request structured PM state)? A capability advertisement (announce available tools)? Both? Klatch chose context handoff with progressive disclosure; PM should make the same choice deliberately rather than inheriting it by accident.

4. **Five-layer model + MCPB hybrid map cleanly.** Klatch's L1–L5 model (corpus, channel, entity, etc.) and PM's MCPB hybrid (tools/storage + Claude Project for persona) are isomorphic at the layer-boundary level. PDR-005 should reference this isomorphism — it's evidence the layering is sound across projects, not just internal to PM.

5. **Inter-project context handoff is on the medium-term horizon.** From the Apr 11 brief: "Klatch as context server, PM as task-and-knowledge server, Managed Agents as the execution layer both plug into." Not in PM's current critical path, but PDR-005 shouldn't foreclose it. Reserve a capability slot in the BYOC architecture for "context received from upstream MCP server, not just assembled from PM's own data."

### Operational coordination already named (Apr 11 brief, not yet acted on)

> *"PM Architect should read [the Klatch futures memo] before the next M5 distribution design session. The open question it poses — 'what is the canonical context package?' — is the same question PM needs to answer for any inter-system context handoff. A short alignment conversation between Daedalus and PM Architect before Klatch Phase 1 design begins would prevent each side from specifying a format independently that the other then has to bridge."*

That conversation (PM Architect ↔ Klatch Daedalus) hasn't happened to my knowledge. Worth flagging for Architect's feasibility-check work — it's lower cost to align early than to bridge formats later.

## Janus — minimal direct relevance to BYOC

Janus is a curator/relay role at designinproduct.com (cross-project messenger). Not a product with a distribution model in the same sense. Relevance to PDR-005: Janus's relay convention (replies to DinP path; "filing IS the signal") demonstrates that **convention-as-protocol** can substitute for explicit machinery when the audience is tight. Doesn't translate directly to BYOC (PM's audience is wider), but worth knowing as an existence proof of low-machinery distribution patterns.

## Vergil — limited visibility from PM repo

Vergil appears in cross-project contexts but I don't have direct visibility into Vergil's distribution model decisions from the PM repo. Likely relevant if Vergil ships any MCP-shaped surface; would need a direct relay through Janus to confirm.

## Piper Open / OpenLaws — relevant but adjacent

OpenLaws is xian's law-librarian project. The Apr 25 Bet 1 questions to PM (Q1-Q6) included citation-centric architecture, IP/confidentiality boundaries, and agent-facing team rituals — all relevant to BYOC's deployment model. Specifically: OpenLaws's experience designing for "compliance analyst pairing with agent" is the closest parallel to PM's "PM pairing with agent." If OpenLaws ships before or alongside PM's BYOC, both projects benefit from sharing the deployment-pattern findings.

OpenLaws doesn't yet have a BYOC-equivalent distribution decision per my visibility. Worth checking with Janus relay if OpenLaws is far enough along to have anything substantive.

## What I did NOT find

- No sibling project has shipped a BYOC-shape product yet (Klatch is closest with v1.0 MCP feature-complete; PM's BYOC PDR is upstream of any sibling shipping)
- No documented "BYOC failure modes" or "MCP distribution lessons learned" — both projects are still in the build-and-discover phase
- No external (non-Anthropic) reference architectures I noticed in cross-project briefs

## What this implies for PDR-005 substance

- **Lead with the convergence**, not the rationale. The Klatch + PM convergence is itself the strongest argument that BYOC is the right shape; PDR-005 doesn't need to re-argue it.
- **Defer the inter-project context-handoff capability** but reserve the architectural slot. Don't design it now; don't foreclose it.
- **Name the export-format-as-protocol pattern** as a load-bearing design choice for the BYOC MCP surface — the export schema choice is the protocol choice.
- **Coordinate the Architect↔Daedalus alignment conversation** before PDR-005 lands its architectural commitments. Apr 11 brief named this; still open.

## Standing offer

If PPM wants me to dig deeper on any specific sibling project's posture (Vergil, OpenLaws), happy to route a Janus query or scan additional briefs. Output landed at convenience per PPM's "no deadline."

— PA, 2026-05-10
