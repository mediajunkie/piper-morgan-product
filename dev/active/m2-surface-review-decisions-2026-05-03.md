# M2 Surface Review — Decision Tracker (Sun May 3 PM session)

**Started**: 2026-05-03 ~3:30 PM
**Walked by**: PM (xian) + PA (Piper Alpha)
**Purpose**: Capture decisions from M2 surface review walk so PM can apply GitHub milestone/label metadata after the walk completes.

---

## Topic 1 — Fold M2-adjacent discovered work into the M2 ledger? ✅ DECIDED

**PM decision**: Endorse all four recommendations.

| Item | Action | Target placement | Notes |
|---|---|---|---|
| **#992 ETHICS-ACTIVATE arc (Phases A–F)** | FOLD into M2 ledger | M2 (sub-epic placement TBD — likely M2c-extension or its own M2-ethics line) | Includes ADR-061 v1.0 (paperwork still pending May 3); roadmap v15.0 named "Floor-First Ethics Verification" as pre-sprint action that became this arc |
| **#1018 audit_transparency + cluster #1006 / #1007 / #1008** | FOLD into M2 ledger | M2 (likely under same line as #992, since durability gates Phase F flag-flip operational meaning) | All shipped May 2 (commit `fc79de31`); cluster regressions closed in same merge |
| **#1034 STANDUP-STRUCTURED-WORKITEMS** | FOLD into M2d | M2d (MUX Lifecycle) | Shipped this weekend; functional MUX-Lifecycle work; not in pre-restructure M2d table |
| **#1035 MUX-COMPOSTING-ACTIVATION** | FOLD into M2d | M2d (MUX Lifecycle) | Shipped this weekend; same shape as #1034 |
| **Calibration window observation** (Phase F follow-on) | DO NOT FOLD | Operational discipline; not in M2 ledger | Ongoing observation, not discrete shipment; resulting fix issues get M2-vs-elsewhere placement at filing time if any |

**Pattern**: fold substance that shipped during M2; don't fold ongoing operational disciplines.

**Metadata actions for PM after walk**:
- Add M2 milestone (or appropriate sub-epic milestone) to: #992, #1018, #1006, #1007, #1008, #1034, #1035
- Update m2-structure.md M2d table to add #1034 and #1035
- Decide whether #992 arc gets its own M2 line (e.g., "M2-ethics") or folds under existing M2c (Conversational Depth) or M2-discovered

---

## Topic 2 — Conceptual-integrity gate: verification shape? ✅ DECIDED

**PM decisions** (both confirmed):

1. **Verification shape**: **(C) Combined** — audit-cascade re-run at ship-by-ship moments during M2d (Lead Dev's lane) + CXO designated-reviewer sign-off at the gate moment. Belt-and-suspenders; (A) alone is too mechanical, (B) alone too judgment-dependent.
2. **Gate scope**: **Apply at M2 super-epic closure**, not just M2d. Conceptual-flattening risk extends to M2e (integration-handler UX touches the same object-model semantics). Forward-applies to M3+ as a normalized pattern.

**Adaptation at M2 super-epic level**: audit-cascade target shifts from *issue bodies vs. discovery decisions* (M2d shape) to *shipped surface vs. canonical object-model docs* (`objects-catalog.md`, `views-objects-roadmap.md`). Same skill, different anchor. CIO bless the adapted shape.

**Metadata actions for PM after walk**:
- Update m2-structure.md M2d gate clause to reference verification shape (C) explicitly
- Add M2 super-epic gate criterion: "Conceptual integrity preserved on shipped surface (CXO sign-off + audit-cascade against objects-catalog.md + views-objects-roadmap.md)"
- Route adapted-shape framing to CIO for blessing

---

## Topic 3 — WIRE-* triage (#690–695): when and who? ⏳ PENDING

(Walk-through pending)

---

## Topic 4+ — Stray issues (PM pulls unmilestoned list) ⏳ PENDING

(Walk-through pending)
