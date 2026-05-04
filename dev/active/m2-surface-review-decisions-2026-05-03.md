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

## Topic 3 — WIRE-* triage (#690–695): when and who? ✅ DECIDED

**PM decision**: **(A) Lead Dev runs the sweep using audit-cascade shape, with PM support.** Ahead of M2e gameplan-prep so the triage outcome shapes the M2e table.

Verdicts per WIRE-* will be: still-needed / superseded-close / re-scoped. Output: Lead Dev memo with verdicts + immediate closures + proposed M2e table updates.

WIRE-* set:
- `#690` WIRE-BOUNDARY (likely affected by Phase F refactored boundary_enforcer)
- `#691` WIRE-CANONICAL (likely affected by #1018 repository-pattern work)
- `#692` WIRE-SLACK
- `#693` WIRE-STANDUP
- `#694` WIRE-GITHUB-LLM
- `#695` WIRE-GITHUB-CMD

**Metadata actions for PM after walk**:
- Route a memo to Lead Dev requesting the WIRE-* triage sweep (audit-cascade shape) ahead of M2e gameplan-prep
- Lead Dev's resulting closures + M2e table updates feed back into m2-structure.md

---

## Topic 4 — Stray issue triage (19 items from PM pull) 🟡 IN PROGRESS

PM provided 19 issues for triage on Sun May 3 evening. PA sorted into 11 high-confidence placements + 7 discussion items.

### High-confidence placements (PM scanned + corrected Mon May 4 AM)

| # | Title (short) | PM placement |
|---|---|---|
| #1030 | MUX-INSIGHT-PULL | M2 / M2d (agreed) |
| #1031 | MUX-INSIGHT-PASSIVE | M2 / M2d (agreed) |
| #1032 | MUX-INSIGHT-PUSH | M2 / M2d (agreed; P3 longer pole) |
| #1033 | MUX-COMPOSTED-EXPERIENCE | M2 / M2d (agreed) |
| #1034 | STANDUP-STRUCTURED-WORKITEMS | M2 / M2d (per Topic 1 fold) |
| #1035 | MUX-COMPOSTING-ACTIVATION | M2 / M2d (per Topic 1 fold) |
| #1037 | MUX-INSIGHT-TOPIC-MAPPING | **Fast Follow milestone** (PM call vs. PA "post-MVP") |
| #1039 | INTENT-COVERAGE-A: milestones + releases | M2 / M2e (agreed) |
| #1040 | INTENT-COVERAGE-B: labels + branches | M2 / M2e (agreed) |
| #1041 | M2-WIRE-TRIAGE | M2 / M2e (agreed; Topic 3 outcome) |
| #1043 | (renamed from POST-MVP) Copy review pass | **MVP / M5** polish sprint (PM kept MVP; sprint = M5, title prefix changed) |
| #1045 | POST-MVP Project Detail Activity tab | **NOT MVP** (post-MVP, agreed) |

### Discussion items (serial walk completed Mon May 4 AM)

| # | Title (short) | PA lean | PM decision |
|---|---|---|---|
| #1027 | Re-point CLAUDE_OPUS enum (Opus 4.7 already exists; title premise unclear) | Park for Lead Dev clarification | **PARKED** — PM to discuss with Lead Dev; placement TBD |
| #1028 | PERPLEXITY broader sweep (4 files; tech debt) | MVP / M5 polish | **MVP / M5** |
| #1029 | Wire APIUsageTracker into LLMClient (sync call sites) | MVP / M2f paired with #935 | **MVP / M2f** |
| #1038 | 1018-TESTS-SQLITE-COMPAT (test infra cleanup from #1018 ship) | MVP / M2 (discovered work) | **MVP / M2** (discovered work, no sub-epic) |
| #1042 | PRE-1039: hardcoded repo default removal | MVP / M2e paired with #1039 | **MVP / M2e** paired with #1039 |
| #1044 | Local-git "what branch are we on?" handler (split from #1040) | Fast Follow | **Fast Follow** |
| #1046 | BUG test_mapping_count drift (26→31) | MVP / M2 (discovered work) | **MVP / M2** (discovered work, no sub-epic) |

### Topic 4 metadata actions for PM after walk

- Apply M2 milestone to: #1029 (M2f), #1038 (M2 super), #1042 (M2e), #1046 (M2 super), plus the high-confidence batch (#1030–#1035 M2d, #1039 M2e, #1040 M2e, #1041 M2e, #1043 M5)
- Apply Fast Follow milestone to: #1037, #1044
- Apply M5 milestone to: #1028 (polish), #1043 (polish; renamed from POST-MVP)
- Apply Post-MVP / non-milestone to: #1045
- Park #1027 for Lead Dev clarification
- Add #1034 + #1035 to m2-structure.md M2d table per Topic 1 fold-in
