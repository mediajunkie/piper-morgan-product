---
workstream: "048"
role-slug: ppm
window: "2026-06-12 to 2026-06-18"
filed: 2026-06-20
to: exec
cc: pa, xian (ceo)
---

# Ship #048 Workstream Review — PPM lane (Jun 12–18)

**Filed**: 2026-06-20 · **Window**: Jun 12 (Fri) – Jun 18 (Thu)

---

## TL;DR

- **Entity-model spec delivered and frozen** — the shape contract that unblocks Lead's four-type Radar build is on main
- **Roadmap v18.1 fold** — M2/M3 closed, RECONNECT + D1 added, Jul 4 MVP beta target made explicit
- **Critical gap caught before build** — People entity type has no population mechanism; deferred post-beta (#1281) rather than shipped with broken provenance
- **Taxonomy drift caught** — ArtifactSourceType (code) vs. ProvenanceSource (spec) would have diverged; reconcile map delivered
- **ADR-071 gate confirmed** — anchor-first is correct for entity backends; PPM endorsed the gate rather than routing around it

---

## What landed

**Roadmap v18.1 fold (6/15)**  
M2 ✅ and M3 ✅ closures recorded. Two new sprints added: RECONNECT (connector infrastructure + WS-9) and D1 (current beta design quality sprint). Jul 4 MVP 0.9.0 beta target made explicit in the roadmap body. Source: `docs/internal/planning/roadmap/roadmap.md`. #1166 CLOSED.

**Radar Layer-2 entity-model spec (6/15)**  
Delivered `docs/internal/product/pdr/ppm-spec-radar-layer2-entity-model-2026-06-15.md` — the contract shape Lead and CXO build against. Covers all four entity types (WorkItem, Document, Conversation, People), lifecycle states per type, ProvenanceSource provenance field, trust-gated surfacing behavior, M4 scope table, and 12 open questions for subsequent refinement. This unblocked Lead's entity-source backend work.

**RadarEntity model side frozen (6/15)**  
Per-type lifecycle states and People entity model (inspectable/editable, consent-tiering provenance, personhood type + relationship edges) delivered to Lead cc CXO. Model is frozen as of 6/15 — the gate is Lead's implementation against this contract.

**ADR-071 alignment confirm (6/16)**  
Confirmed the anchor-first position to Lead cc Arch, CXO, PM: `list_by_user` on an unanchored global collection is architecturally wrong. Document/WorkItem/People backends are correctly gated behind ADR-071's anchoring pass. Retracted an earlier "small add" framing I'd offered; Lead's gate reading is sound.

**#1270 Document source-facet model (6/17)**  
Responded to Lead's object-model question. Beta scope: uploaded docs ✅ (already built), generated docs ⚠️ conditional (asked Lead to confirm #355 exists — confirmed yes), federated docs ❌ post-Beta (RECONNECT dependency, per ADR-070 milestone call). ProvenanceSource enum extended to include `generated` and `federated` variants.

**ArtifactSourceType / ProvenanceSource reconcile (6/18)**  
Lead surfaced that code uses `ArtifactSourceType` enum while the spec uses `ProvenanceSource`. Would have diverged on first build. Delivered a mapping table to Lead + CXO: `GENERATED` → `generated`, `FEDERATED` → `federated`, etc. — sync-point confirmed before the backends touched it.

**Trust-model sweep (6/18)**  
Entity-type boundary table delivered: Piper-initiated vs. user-requested access control boundary applies consistently across all four entity types. Confirmed that trust-gating in current code was inadvertently hiding users' *own* content — flag routed to Lead; #1237 scope unaffected but important context for D1 sprint.

**People entity-model decision (6/18)**  
#1240 Phase-0 STOP: no clean People entity source exists at MVP scope. Evaluated all four options:
- GitHub-derived: spec taxonomy deviation
- Session extraction: new infrastructure (no M5 slot)
- Introduce-person intent: new intent flow (no M5 slot)
- Defer post-beta: no model debt

Chose Option 4. PM confirmed. #1237 confirmed 3-of-4 (WorkItem + Document + Conversation) for M5 beta. #1281 filed (People entity source, post-beta, under Dot Releases milestone) with full source-mechanism spec and open questions. CXO asked about empty-door teaser → chose silent omission (3 clean facets, no placeholder).

**#1269 standup data model (6/18)**  
PPM data model delivered to Lead + CXO: the morning standup card is built FROM a per-user snapshot of WorkItem.status changes, recently-active Document references, and Conversation threads from the last 24h — not from live API calls at render time. This unblocks CXO's experience design and Lead's implementation once #1237 is callable.

**#1048 Insight Journal trust-gradient (6/16)**  
Concurred with CXO: Insight Journal is pull (browse-on-demand), not push — stage-specific trust-gradient visual earns its complexity only in push contexts. No build. Told Lead to close.

---

## What surfaced

Three structural problems caught before they hit implementation — worth naming as a pattern:

1. **People provenance gap**: there's no mechanism to reliably populate the People entity with `user_confirmed` / `session_extracted` / `inferred` status. Flagged before #1237 was built; deferred rather than shipped as a broken model.
2. **Taxonomy drift (ArtifactSourceType vs. ProvenanceSource)**: caught mid-thread, reconciled before backends diverged. These catch-before-build moments are exactly what the entity-model ownership lane is for.
3. **ADR-071 gate scope**: the gate is correct, and I endorsed it rather than looking for a bypass. Document/WorkItem/People backends all need anchoring; the right call is to wait for the anchoring pass, not ship an unanchored workaround.

---

## What's still open

- **#1237 3-of-4 Radar build**: awaiting Lead (post ADR-071 anchoring pass)
- **#1269 standup skill**: PM milestone call needed before Lead builds (depends on #1237 callable)
- **Roadmap v18.1/v19 fold**: PPM milestone input owed once PM weighs in on sprint sequencing beyond M5
- **People onboarding (1.0)**: PA flagged the need for a holistic onboarding design spanning the full Piper distribution surface (Skills / MCP plugin / hosted server / Cowork+Code). No urgency; PM and PA have my attention when CXO and I are needed for the design pass
- **#683 interface-verification DoD**: ACs 1–3 complete; Lead Dev operational-check recipe still pending (the last refinement before close)

---

## Cross-role threads worth naming

- **CXO**: frozen on the model side (6/15); three responses from CXO this week all shaped PPM calls (#1270 IA, #1048 keep-generic, People silent-omission B)
- **Lead**: highest-volume exchange this week; every PPM deliverable either unblocked a Lead build or prevented a model error from reaching one
- **Arch**: ADR-071 trust-layer framing was the load-bearing architectural context for all entity-backend decisions this week; the three-altitude motivation memo (6/15) was well-timed

---

*PPM · Ship #048 workstream review · Jun 12–18 window · Filed 2026-06-20*
