# Architect Standing Items — Task List

**Purpose**: Architect's task queue per duty cycle v0.7 (worktree-as-cycle-default; cron-shape-experiments registry Row 1 = 3hr-interval bursty-lane).

**Convention**: tasks listed roughly by priority/cadence. Mark `[x]` when complete; `[⏸]` when blocked on external (per recurring-failure memory on deferred-AC). Move to "Closed" section at end-of-week.

**Last refreshed**: 2026-06-09 13:10 PT (post-m-40-filing maintenance; 12 days stale before this refresh — see lesson note at end).

---

## Active

- [ ] **methodology-40 (layer-then-migrate) v0.1 → Proven** — FILED 2026-06-09 morning at `docs/internal/development/methodology-core/methodology-40-LAYER-THEN-MIGRATE.md`; CIO ping memo distributed; awaiting CIO cosign + slot 40 allocation + cross-reference indexing. Promotion-to-Proven gated on cross-author invocations as future retirement decisions surface across cohort. **NOT** adding back-references from adjacent methodology/pattern entries until CIO catalog-confirms (catalog-edit-lane is CIO-owned).
- [ ] **ADR cross-reference back-pass** — once CIO confirms m-40 slot, add `methodology-40 (layer-then-migrate)` to ADR-060 amendment §Cross-references + ADR-065 §Cross-references + ADR-066 §Cross-references. Bounded mechanical work; ~5-10 min. **Gated on CIO slot confirmation** (sequencing risk if slot changes).
- [ ] **Day-7 findings memo F4 reframe** — F4 was withdrawn 2026-06-08 morning (durable=true is no-op per disk check + PA verified finding); then 2026-06-08 evening cron-durability discovery revealed `4c166d42` from June 6 evening survived 2.5 days across session deaths + account-switch, contradicting the withdrawn-as-no-op narrative. Need PA+CIO clean test characterizing the actual in-memory durability surface before any mechanism recommendation. Holding the reframe until the clean test runs.
- [ ] **Workstream-046 Architect lens** — sprint week Jun 5-11 closes Thu Jun 12; PM 6/6 directive "no need to work on workstream reviews before the sprint week is done"; draft ~Jun 12 (deferred per PM directive, NOT delayed).
- [ ] **#973 MEM-CACHE-AUDIT Phase 1 audit** — PM-ratified ship-now-as-prep May 19; ~1-2 hr Architect drive + ~2-3 hr Lead Dev support. STABLE/DYNAMIC labeling + pipeline reorder + per-method TTL suggestions, no behavioral change. Needs Lead Dev coordination — focused session, not fire-driven. **Status check**: Lead Dev currently deep in #1124 Phase 4 build + #952 Artifact build + #355 implementation; may be ready for #973 session after those settle.

## Blocked / waiting on external

- [⏸] **CIO m-40 cosign** — CIO-owned catalog-edit lane; CIO ping memo 2026-06-09 morning
- [⏸] **CIO P-073 spec-layer note** — CIO-owned per 6/8 disposition; CIO will action in a follow-up fire
- [⏸] **CIO m-30 Emerging-with-progress edit** — CIO-owned per 6/8 correction; reflects 2-of-3 hold; m-30 instance #3 today (2026-06-09 #371 event-shape trace) was a different subsystem but still Lead-Dev-applied (cross-author not yet satisfied)
- [⏸] **HOST mail-vs-GH signaling-channel cohort-norm codification** — HOST-owned per 6/7 disposition; HOST drafting
- [⏸] **Docs #1182 link-rewrite execution** — Docs-owned per Architect's FLATTEN ruling 2026-06-09; Docs needs Verify-First README.md name-conflict check before move
- [⏸] **PA+CIO clean test for durable=true cron mechanism** — needs both roles to characterize the in-memory survival surface revealed by the `4c166d42` 2.5-day survival data; informs whether durable=true codification ever lands
- [⏸] **Reviewer engagement on ADR-065 + ADR-066 + ADR-060 amendment + m-40** — cohort (PPM/Lead Dev/CIO/CEO) can engage when ready; not Architect-driven
- [⏸] **ADR-067 candidate for #952 Artifact** — Lead Dev's call per 6/8 ratification (Lead Dev's authorship + my ratification is natural shape, but Lead Dev may prefer to just ship)
- [⏸] **#1166 Type-2 Dreaming spike kickoff** — post-M3; structurally gated on persistence; convergence complete (Architect + PPM + CXO lenses all in 2026-06-08); awaiting M3 ship + spike-launch decision (PPM owns PDR)

## Watch surfaces (not work; observation only)

- **methodology-40 Proven-bar progress** — current 8 instances within one architectural arc + largely Architect-authored. Watch for genuinely-cross-author invocations (HOST/PPM/CXO/CIO/Docs/PA invoking m-40 in their own lane). Each such instance is Proven-bar gate-clearing material.
- **methodology-30 Proven-bar progress** — current 3 instances (Phase 3 coverage 6/7 AM; Phase 4 audit-cascade 6/7 PM; #371 event-shape 6/9 AM). All Lead-Dev-applied. CIO 6/8 correction said hold-Emerging + record-progress; the 3rd instance partially addresses arc-diversity + temporal-spread; cross-author still pending.
- **Pattern-072 application count** — at 8 applications post-ADR-066 (verb-enum 6th; capability primitive ADR-065 D3 7th; capability map ADR-066 D1 8th). Potential 9th if `ArtifactSourceType` (per #952) adopts the discipline; potential at adversarial-perturbation registry if Type-2 spike lands. CIO catalog-aware.
- **Pattern-073 spec-layer extension** — 2 instances cataloged (Phase 3 coverage spec; source_type-in-slots-vs-context spec). CIO 6/8 disposition said "YES, explicit note" in the entry; CIO-owned edit pending.
- **External-alignment-Evolution-amendment pattern** — HOST May 24 generalization of Klatch-pause framing landed as Pattern-064 convention (Architect-applied 2026-06-06 in ADR-065 §Evolution). Watch for second non-Klatch external-dependency-uncertainty case to file as separate instance.
- **Duty-cycle gap-class catalog** — 6 classes surfaced 2026-06-06 → 2026-06-09: (1) worktree-sync-lag; (2) signaling-channel; (3) cron-death; (4) weekly-usage-limit + account-switch; (5) stale-prompt firing in cron-survived-across-cycles; (6) rate-limit-mid-fire. HOST PM-as-catch watch-item disposition holds at "addressed-at-sub-mech + dashboard generalization" but matrix expanded.
- **Same-fire-coherence-across-related-work** — Day-5 findings Finding 5 working hypothesis (PPM refined to "bundle-shaped producing work; not reactive-mail lanes"); CIO folded into adaptive-interval cron-shape synthesis. Holds across producing AND reactive modes per Fire 10 evidence. Needs cross-role instances before catalog promotion.

## Mutual-assessment exchange commitments

- [x] Day-1 "what surprised me" memo to CIO + HOST after first 4-6 fires — SUPERSEDED by Day-7 findings memo (filed Day-5 2026-06-08)
- [x] Day-3/4 comparative observations (cross-role) — folded into Day-5 findings
- [x] Day-7 synthesis to PM — FILED Day-5 2026-06-08 as comprehensive 6-findings memo to CIO + broad cohort CC

## Recently closed (this past cycle 2026-06-06 → 2026-06-09)

- [x] **ADR-065 (canonical context-package format) v0.1 FILED** — Q6 ADR arc complete (2026-06-06 skeleton → 2026-06-07 Decision content → 2026-06-08 polish + final)
- [x] **ADR-066 (packaging-layer abstraction) v0.1 FILED** — Q7 ADR arc complete (2026-06-06 skeleton → 2026-06-07 D1-D6 content → 2026-06-08 polish + final)
- [x] **ADR-060 amendment Phase 3 refinement** — landed 2026-06-07 with Lead Dev's coverage-finding rescope
- [x] **ADR-060 amendment Phase 4 plan ratification** — landed 2026-06-07 PM (Q1 source_type → intent.context + Q2 hybrid prompt-big-bang + shim-then-migrate consumers)
- [x] **ADR-060 amendment Step-4 refinement** — landed 2026-06-08 evening with Lead Dev's shim-as-permanent-ACL finding
- [x] **#952 Artifact model RATIFIED** — unifying-lens with lossless round-trip; round-trip-now + incremental-unification-later
- [x] **#371 spatial-persistence postpone + event-shape seed** — concur on postpone; seed event-shape contract NOW; methodology-30 consumer-trace confirmed gaps are additive (no code change)
- [x] **#1166 Type-2 Dreaming 3-way convergence** — Architect lens + Arch-spike-question seeds; concur with PPM + CXO dispositions; CXO completes 3-way 6/8
- [x] **methodology-40 (layer-then-migrate) v0.1 FILED** — Architect-authored 2026-06-09; awaiting CIO cosign
- [x] **HOST signaling-channel cohort-norm flag** — filed to HOST 2026-06-07; HOST disposition concur 2026-06-07; HOST drafting codification
- [x] **Day-7 findings memo to CIO** — filed Day-5 2026-06-08; six findings; CIO dispositions returned same-day
- [x] **Docs #1182 models/models/ layout RULING** — FLATTEN (Option A); filed to Docs 2026-06-09

## Closed older (pre 2026-06-06)

- [x] **worktree-as-cycle-default v0.7 concur/dissent** — DONE 2026-05-28 Fire 1
- [x] **#1016 LLM-touch boundary boundary-map closing document + verification pass** — DONE 2026-05-28
- [x] **Pattern-070 Evolution-section entry** — DONE 2026-05-28 Fire 1 (External validation via Anthropic Dreams API)
- [x] **Dreams API spec read** — DONE 2026-05-27 Fire 2
- [x] **GitHub Actions operational refactor sanity-check** — DONE 2026-05-27 Fire 1
- [x] **v0.6 duty cycle Day-1 adoption** — substrate up + v0.7 worktree-default adopted; cron experiment validated across 12+ fires Jun 6-9

---

## Refresh discipline note (added 2026-06-09 maintenance pass)

This doc was 12 days stale before today's refresh (last touch 2026-05-28). The PR-discipline failure: standing-items maintenance should ride with the cycle, not wait for a periodic refresh. Going forward, refresh as part of any cycle-fire where the queue meaningfully changes (new ratification shipped; new methodology entry filed; new external blocker surfaces). The "Last refreshed" date is the trip-wire: anything older than 7 days = refresh-on-touch.

This refresh itself was Fire 13's primary work after CronDelete (substantive maintenance work; honored "don't shrink work" by doing the full 12-day fold-in, not a cosmetic touch-up).
