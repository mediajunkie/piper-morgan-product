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

---

## Topic 5 — Second list (16 more issues, Mon May 4 AM) 🟡 IN PROGRESS

### Bucket A — Resolved per Lead Dev May 4 AM follow-up

- **#1004** BoundaryEnforcer Fix B+C1: code SHIPPED (verified — `services/ethics/semantic_boundary_detector.py` + `boundary_enforcer_refactored.py` + SemanticDetectorOutput schema + REFUSAL_FALLBACK constant + LRU cache); GitHub state OPEN due to close-issue-properly anti-pattern (description-checkbox update + evidence comment never run). **Action**: drop from triage list with disposition "ready to close, needs proper-close pass." Lead Dev recommends NOT auto-closing — Architect should run the skill (7 ACs worth verifying); could be batched with the M2d close-properly pattern fix. Already counted in Topic 1 fold-in (Phase F arc → M2 ledger).
- **#1016** LLM-touch boundary principle: multi-phase epic, correctly OPEN. Phase 1 CLOSED Apr 27 (`ca1630d0`); Phase 2 (Analysis) pending. Family children #1017/#1018/#1019/#1020 + #1021 were Phase 1 deliverables. **Placement confirmed**: **MVP / M2g**. Operational follow-up: verify with Architect that Phase 2 is queued (not abandoned).

### Bucket B — Settled

| # | Title (short) | PM placement |
|---|---|---|
| #1005 | Pre-existing test failure: adaptive_enhancement type | **MVP / M2** (discovered work, no sub-epic) |
| #1011 | ARCH-DESIGN slash-command dispatch precedence (post-MVP per title) | **NOT MVP / Post-MVP** (PM swept into M2 by accident May 4 AM; corrected during 1:00 PM reconciliation) |
| #1026 | Pre-existing test failure: test_decompose_moderate_task | **MVP / M2** (discovered work, no sub-epic) |
| #1047 | M2D-UAT manual browser-smoke + a11y + perf | **MVP / M2 super-epic gate criterion** (standalone; companion to Topic 2 conceptual-integrity gate) |
| #1048 | MUX-INSIGHT-STAGE-VISUAL Insight Journal stage treatment | **MVP / M5** polish |

### M2g new sub-epic — Architecture epic needed to close M2 super-epic

Per PM May 4 AM: ARCH cleanup + design items constitute an epic needed to close M2. Naming asymmetry vs M2f (which "may defer to M3/M5") — **M2g closure required for M2 super-epic gate**.

### Bucket C — M2g placements (assumed fit; walk-on-merits deferred to ship-time scrutiny)

| # | Title (short) | PM placement |
|---|---|---|
| #1010 | ARCH-CLEANUP knowledge_graph + legacy boundary_enforcer | **MVP / M2g** |
| #1015 | ARCH ADR-051 RequestContext migration completion | **MVP / M2g** |
| #1016 | ARCH-DESIGN LLM-touch boundary principle (if still open) | **MVP / M2g** (provisional pending closure check) |
| #1017 | ARCH-DESIGN Post-generation content filter (PII/safety) | **MVP / M2g** |
| #1019 | ARCH-CLEANUP adaptive_boundaries scaffolding alive but inert | **MVP / M2g** (resolves Lead Dev "PM call required") |
| #1020 | ARCH-DESIGN Per-task LLM output validation in OrchestrationEngine | **MVP / M2g** |
| #1021 | ARCH-CLEANUP UserHistoryService Layer 3 no DB backend | **MVP / M2g** |

### #999 / #1000 / #1001 — owner-review trio (walk complete)

Parent #997 closed; placement-by-inheritance off the table. Each assessed on merits.

| # | Title (short) | Stakes / merit-based read | PM placement |
|---|---|---|---|
| #999 | services/mcp/consumer/ fallback paths | High — silent fallback = wrong-answer to user; integration is product surface | **MVP / M2g** |
| #1000 | services/auth/ fallback paths | Highest — silent fallback to wrong-user-context = security incident | **MVP / M2g** (paired with #999 for unified posture) |
| #1001 | services/publishing/publisher.py retry/fallback | Lower — affects PM publishing flow; manual retry feasible; not user-trust-critical | **MVP / M5 polish** |

Trio split intentionally per "merit-based assessment, not inheritance from #997." M2g architectural-posture decision applies to publisher when M5 polish ships.

### Topic 5 metadata actions for PM after walk

- Apply M2g milestone to: #1010, #1015, #1017, #1019, #1020, #1021 (and #1016 if still open)
- Apply M2 super-epic + "M2 gate criterion" label to: #1047
- Apply M2 (no sub-epic) to: #1005, #1026
- Apply M5 polish to: #1048
- Apply Post-MVP to: #1011
- ~~Park: #1004 + #1016 pending Lead Dev follow-up~~ → **resolved**: #1004 needs proper-close pass (Architect lane), #1016 confirmed MVP/M2g (multi-phase epic, Phase 1 closed, Phase 2 pending — verify with Architect)
- Add M2g sub-epic line to m2-structure.md with **"required for M2 super-epic closure"** framing (asymmetric to M2f's "may defer")
- Operational follow-up: verify #1016 Phase 2 queued with Architect; consider batching #1004 proper-close pass with M2d close-properly pattern fix

---

## Topic 6 — M2 surface chunking (Mon May 4 PM) ✅ DECIDED

PM pulled current open M2 list (56 items). Reconciliation: all 20 items from today's walk match PM's GitHub state. One discrepancy: #1011 was in PM's M2 list by accident — PM corrected to Post-MVP same conversation.

### Mapped sub-epics (~28 items)

| Sub-epic | Open count | Notes |
|---|---|---|
| M2d (active) | 2 + child verifications | #703, #707 tracking parents; check #1031/#1032 children |
| M2e (Integrations) | 11 | #690-695 WIRE-* (triage destinations), #869, #1039, #1040, #1041, #1042 |
| M2f (Security + Infra) | 1 (newly placed) + roadmap pre-existing | #1029 paired with #935; family expands when triage runs |
| M2g (NEW arch epic — required for closure) | 9 | #999, #1000, #1010, #1015, #1016 (multi-phase), #1017, #1019, #1020, #1021 |
| M2 super-epic gate criteria | 1 + Topic 2 conceptual-integrity gate | #1047 manual UAT + CXO sign-off + audit-cascade |
| Discovered work, no sub-epic | 4 | #1005, #1026, #1038, #1046 |

### Unmapped families (~30 items, 6 families)

Routed to Lead Dev as audit-cascade triage memo: `mailboxes/lead/inbox/memo-pa-to-lead-cc-ceo-exec-ppm-m2-unmapped-families-triage-after-m2e-2026-05-04.md`. **Trigger: post-M2e closure** so surface area is stable.

Six families:
1. Older SEC/INFRA (#557, #542, #482, #470, #471, #371)
2. Older Integration (#472, #304, #366)
3. Older CONV/Context (#100, #101, #983, #984, #985, #986)
4. Memory (#972, #973, #974, #975)
5. Testing/scoring infra (#987, #989, #991, #993, #994, #995)
6. UI/Process (#683, #998)

Verdict shape per issue: STILL NEEDED / SUPERSEDED / RE-SCOPED / NEEDS PM CALL.

### Topic 6 metadata actions for PM

- Confirm #1011 corrected to Post-MVP in GitHub
- No immediate sub-epic assignments needed for the unmapped families (waits on Lead Dev triage post-M2e)
- After Lead Dev triage returns: PA hosts synthesis with sub-epic placement proposals; PM ratifies

---

## Topic 7 — Lead Dev triage outcome + PM ratification (Wed 2026-05-06) 🟡 IN PROGRESS

Lead Dev's verdicts memo at `mailboxes/pa/read/memo-lead-to-pa-cc-ceo-exec-ppm-m2-unmapped-families-verdicts-2026-05-05.md`. PM walked some decisions Tue May 5; PA hosts remaining ratification Wed May 6.

### Already executed Tue May 5 (no further action)

- **Closed-supersede**: #101 (CONV-FEAT-TIME), #100 (CONV-FEAT-PROJ basic scope)
- **Closed by PM decision Tue**: #987 (Option 3 low-volume Gemini fallback), #991 (Option A ratified for alpha)
- **Decision memo to Architect**: #983 label convention (`mailboxes/arch/inbox/memo-lead-to-arch-cc-ceo-pa-983-blocked-label-convention-2026-05-05.md`)

### PM placements ratified Tue May 5 (M5/M3 cohort)

| Sub-epic | Issues |
|---|---|
| **M5 — polish + distro** | #482, #557, #542, #472 |
| **M3 — artifact persistence** | #470, #371, #366 |

(#371 was duplicated in PM's original assignment; **CEO confirmed Wed: M3 is the correct placement**, since #371 blocks #366 also in M3.)

### PM ratifications Wed May 6 (cohort placements)

| Sub-epic | Issues | Status |
|---|---|---|
| **M2f post-floor-coverage** | #983, #984, #985, #986 | ✅ ratified (all 4 explicitly deferred from #951) |
| **M2g memory governance** | #972, #973, #974, #975 | ✅ ratified |
| **M2-discovered (testing infra)** | #989, #993, #994, #995 | ✅ ratified (#987, #991 already closed Tue) |
| **Post-MVP tooling** | #683, #998 | ✅ ratified |

PM may still need to add metadata labels in GitHub for these cohort assignments.

### NEEDS-PM-CALL outcomes Wed May 6

- **#304 CONV-INFR-NOTN**: PM call — **Notion is in alpha scope**; needs **phase -1 investigation** to determine doneness of the 1,112 lines of pre-floor Notion code relative to the conversational-floor architecture update. Sub-epic placement deferred until investigation completes. **Operational follow-up**: file/route phase -1 investigation work item (Lead Dev's lane likely).
- **#471 EPIC Infrastructure parent**: PM call — **break out into discrete sub-issues per home; close parent** (tracking complete via children):
  - **Conversation Repository** sub-bead → file as new issue in **M3** (Artifact Persistence)
  - **OAuth-multi** sub-bead → file as new issue; placement **M2f or M5** (PM call on whether OAuth-multi is MVP-required vs. distribution polish — flagged for follow-up)
  - **Learning Phase 3** sub-bead → file as new issue in **M4** (Trust + Learning)
  - **TimeSeries** sub-bead → close as duplicate of **#371** (already in M3)
  - **#471 itself** → close with "broken out into discrete sub-issues; tracking complete via children" comment

### Topic 7 metadata actions for PM after walk

- Apply M3 milestone to: #470, #371 (single placement), #366
- Apply M5 milestone to: #482, #557, #542, #472 (remove #371 if it landed there)
- Apply M2f milestone + "post-floor-coverage" label to: #983, #984, #985, #986
- Apply M2g milestone + "memory governance" label to: #972, #973, #974, #975
- Apply M2 milestone + "discovered work / testing infra" label to: #989, #993, #994, #995
- Apply Post-MVP / non-milestone to: #683, #998
- Park #304 (in-scope, phase -1 investigation gating sub-epic placement)
- Verify #987, #991 closed in GitHub (Lead Dev closed Tue)
- #471 break-out: file 3 new sub-issues (Conversation Repo → M3; OAuth-multi → M2f-or-M5 PM call; Learning Phase 3 → M4); close TimeSeries sub-bead as duplicate of #371; close #471 parent with break-out comment
- Apply M2g milestone to: #999, #1000 (paired for unified fallback-posture decision)
- Apply M5 polish milestone to: #1001 (publisher fallback)
