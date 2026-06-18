# PPM Standing Items — Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-06-18 (Fire 1, 09:52 PDT)
**Purpose**: duty-cycle carry-forward; rewritten each fire to reflect current queue

---

## Entity-model lane (PPM is designated owner, 6/15)

Canonical spec: `docs/internal/product/pdr/ppm-spec-radar-layer2-entity-model-2026-06-15.md`
(addenda 2026-06-17: ProvenanceSource extensions; 2026-06-18: ArtifactSourceType reconcile mapping table)

All 4 entity types modeled. PPM owns the RadarEntity contract shape; Lead implements.

| Item | Status | Gate |
|---|---|---|
| **#1237 4-type Radar (3-of-4 for M5)** | Awaiting Lead build | ADR-071 anchoring path (Lead's call); confirmed 3-of-4 by PM 6/18 |
| **#1240 PeopleEntitySource** | **DEFERRED post-beta** (PM 6/18) | #1281 filed under Dot Releases (Post-MVP); spec complete |
| **#1281 People entity source** | Post-beta; spec ready | Source mechanism TBD (session extraction or introduce-person flow) |
| **#1269 standup skill** | PPM model + CXO experience design both delivered (6/18) | **PM milestone call needed** before Lead builds (depends on #1237 callable) |
| **#1270 ArtifactSourceType reconcile** | Mapping table delivered to Lead (6/18) | Lead to build per ProvenanceSource↔ArtifactSourceType table |
| **Trust-model sweep** | PPM per-entity boundary delivered; CXO ratified (6/18) | Lead implementing (ungate user-content reads; fix stage-definition language) |
| **People UI treatment** | CXO decided: **silent omission** (6/18) | Recorded on #1237 + #1281 GH comments |

---

## Roadmap

| Item | Status | Gate |
|---|---|---|
| **Roadmap v18.1/v19 fold** | Owed (carried from 6/15 session) | PM milestone input needed to fold v18 → v18.1 (sprint board = M4→RECONNECT→D1→M5) |

---

## Ship #048

No Comms kickoff memo yet. Owed on next kickoff cycle.

---

## Blocked / waiting-on-external

| Item | Blocked on |
|---|---|
| **#683** | Lead Dev operational-check recipe + service-type/interface matrix (Lead-gated) |
| **#967** | Edges 1/2/5 still valid defers; no trigger yet |
| **#1185 M5** | Not in sprint yet (floor-blocked) |
| **#5 Multi-Agent** | Lane unclear (PA+CIO or PPM?) |
| **PDR-005** | Docs swap (Docs-owned) |
| **ADR-071 anchoring** | Lead's lane; gates EntitySource production builds (#1237/#1238/#1239) |

---

## Done (since 6/15 migration — for context)

- People entity-model (RadarEntity contract for PeopleEntitySource) → Lead ✅ 6/18
- Trust-model sweep (per-entity boundary table) → Lead + CXO ✅ 6/18
- #1270 ArtifactSourceType reconcile mapping table → Lead ✅ 6/18
- #1269 standup data model (EntitySource consumer architecture) → Lead + CXO ✅ 6/18
- #1240 People deferral decision (Option 4; PM-confirmed) → #1281 filed ✅ 6/18
- CXO empty-door question → silent omission confirmed ✅ 6/18
- All 4 entity-model types: WorkItem ✅, Document ✅, Conversation ✅, People ✅ (6/15–6/18)
- ADR-066 m-38 check ✅ (6/15 — ADR already ratified, no re-check needed)
- History-sidebar-IS-radar Layer 2 resolution ✅ (6/15)

---

*Duty-cycle: drain in priority order until blocked or empty. Rewrite this file each fire.*
