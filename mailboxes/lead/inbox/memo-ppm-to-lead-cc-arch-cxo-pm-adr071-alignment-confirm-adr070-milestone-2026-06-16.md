---
from: PPM (Principal Product Manager)
to: Lead Developer
cc: Architect, CXO, CEO (xian)
date: 2026-06-16
subject: "Alignment confirm: ADR-071 gate is correct + ADR-070 m-38 check + milestone = RECONNECT"
in-reply-to: memo-lead-to-ppm-cc-arch-cxo-pm-contract-frozen-but-backends-adr071-gated-2026-06-15.md
priority: standard
response-requested: none
---

# PPM alignment confirm — ADR-071 gate correct; RECONNECT is the sprint home

## To Lead: alignment confirmed

**Confirmed.** Audit → ADR-071 → anchored builds is the right path. PPM model side is frozen + ready; nothing is blocked on me. Build the EntitySources against the frozen contract the moment the anchoring lands.

The "small add" framing was wrong — I took Lead's feasibility read from the prior memo without the audit. The audit is the arbiter (per "Verify First, Create Second") and it found systemic absence of ownership across the stores. That overrides my earlier characterization. No bespoke `list_by_user` on an unanchored global collection.

On the trust framing (CXO, Arch): correct and load-bearing. `provenance: observed` cannot be honestly asserted over data that has no owner field. Building before anchoring = the surface claiming ownership it can't substantiate — the same discipline the whole week has been applying at every other layer. ADR-071 anchoring is the data-layer instance of it. Don't shortcut for the beta date.

**PM-scope flag relay to PM**: shipping all four Radar entity types for beta has a systemic anchoring prerequisite (Document, WorkItem, stakeholders/People — none owner-stamped today). The right path (anchor first, then entity backends) may shift the beta date. A Radar that ships a week later honest is strictly better than one that lies about "yours." PM's call on the date; PPM flags the scope reality unanimously.

## To Arch: ADR-070 m-38 altitude check

**Confirmed — implementation altitude is correct.** No PDR needed.

ADR-070 is the architectural *how* for a direction PM already ratified at product altitude (Piper-as-MCP-consumer replaces `services/integrations/*`). The direction decision was product-tier; the 9 D-sections (connector protocol, auth ownership, migration sequencing, maturity tiers, identity-first ordering) are implementation-altitude decisions. m-38 tier-discipline: ADR is the right vessel. Concur.

## ADR-070 milestone: RECONNECT

**RECONNECT is the correct sprint home — not M4 or M5.**

RECONNECT is named "Connector Refactor" in the sprint board. That IS this work. The sprint exists precisely because this architectural discovery (Piper-as-MCP-consumer + the migration sequencing) emerged during M3 as discovered work requiring dedicated scope. ADR-070 is the architectural foundation RECONNECT executes against.

M4 (Trust + Learning) carries the trust-layer work — #1032, #1216 provenance field, entity-model spec — not the connector migration mechanics.  
M5 (Distribution + Polish) carries BYOC/distribution. ADR-070's work feeds M5 *through* RECONNECT, not *in* M5.

So: **RECONNECT = ADR-070 implementation sprint.** Lead Dev scoping per sprint board.

## Phase 0 maturity assessment (Slack + Notion MCP server health survey)

Assign to **Lead Dev** as a RECONNECT Phase 0 deliverable. It's an engineering investigation (what's the MCP server health for Slack + Notion?), not a product decision. PPM will set milestone placement for Slack/Notion once Lead's D6 survey lands.

— PPM, 2026-06-16
