# Architect Standing Items — Task List

**Purpose**: Architect's task queue per duty cycle v0.7 (worktree-as-cycle-default; cron-shape-experiments registry Row 1 = 3hr-interval bursty-lane).

**Convention**: tasks listed roughly by priority/cadence. Mark `[x]` when complete; `[⏸]` when blocked on external (per recurring-failure memory on deferred-AC). Move to "Closed" section at end-of-week.

**Last refreshed**: 2026-06-09 19:25 PT (post-Fire-16 maintenance; previous refresh Fire 13 13:10 PT — same-day refresh because day produced many load-bearing changes).

---

## Active

- [x] **methodology-40 (layer-then-migrate) v0.1 FILED + COSIGNED + INDEXED** — Architect-authored 2026-06-09 morning; CIO cosigned + slot 40 confirmed + INDEX.md brought current (CIO caught INDEX.md staleness bug along the way — was at m-35 Last Updated May 24; now current with m-36/37/38/39/40). Status Emerging; Proven gated on cross-author invocations. **Cross-author Proven-bar watch is now the standing item**: track if/when HOST/PPM/CXO/CIO/Docs/PA invoke m-40 by name in their own lane.
- [x] **ADR cross-reference back-pass** — Fire 14: ADR-060 amendment + ADR-065 + ADR-066 §Cross-references gained `methodology-40 (Layer-Then-Migrate, Emerging, CIO-confirmed 2026-06-09)`. Methodology-corpus back-refs left to CIO's opportunistic-touch lane per CIO judgment.
- [ ] **Day-7 findings memo F4 reframe** — F4 was withdrawn 2026-06-08 morning (durable=true is no-op per disk check + PA verified finding); then 2026-06-08 evening cron-durability discovery revealed `4c166d42` from June 6 evening survived 2.5 days across session deaths + account-switch, contradicting the withdrawn-as-no-op narrative. Need PA+CIO clean test characterizing the actual in-memory durability surface before any mechanism recommendation. Holding the reframe until the clean test runs.
- [ ] **Workstream-047 Architect lens** — sprint week Jun 5-11 closes Thu Jun 11 EOD / Fri Jun 12 AM; per `[Anchor on source-set state, not publish date — two halves]` memory: start drafting moment source set in hand (cycle/session logs for the week + cohort omnibus traffic), NOT waiting for Exec kickoff. Source-set-state is the substantive trigger.
- [ ] **#973 MEM-CACHE-AUDIT Phase 1 audit** — PM-ratified ship-now-as-prep May 19; ~1-2 hr Architect drive + ~2-3 hr Lead Dev support. STABLE/DYNAMIC labeling + pipeline reorder + per-method TTL suggestions, no behavioral change. Needs Lead Dev coordination — focused session, not fire-driven. **Status check**: Lead Dev currently deep in #1124 Phase 4 build + #952 Artifact build + #355 implementation; may be ready for #973 session after those settle.
- [ ] **BYO-colleague braintrust thread** — Architect lens filed Fire 15 (composition-not-greenfield finding; 4 risks surfaced including actor_chain + enumeration privacy; ADR-068 candidate post-convergence). CXO refined Fire 16 with 3-tier consent model (enumerate/gather/act) affirming actor_chain. HOST + PPM lenses still pending. Exec synthesizes when source set complete. **NO Architect action until convergence**; then potential ADR-068 + possibly PDR-006 companion per methodology-38 (PPM roadmap call).
- [ ] **Pick up duty-cycle-tick skill v1.5 dual-surface** — CIO shipped 2026-06-09 evening; until I pick it up, manually maintaining per-fire session-log + cycle-log accretion. First v1.5-mechanism use should come on next fire after PM-conversation ends.

## Blocked / waiting on external

- [⏸] **CIO P-073 spec-layer note** — CIO-owned per 6/8 disposition; CIO will action in a follow-up fire (still pending as of Fire 16 evening)
- [⏸] **CIO m-30 Emerging-with-progress edit** — CIO-owned per 6/8 correction; reflects 2-of-3 hold; m-30 instance #3 6/9 (#371 event-shape trace) was a different subsystem but still Lead-Dev-applied (cross-author not yet satisfied)
- [⏸] **HOST mail-vs-GH signaling-channel cohort-norm codification** — HOST-owned per 6/7 disposition; HOST drafting
- [⏸] **Docs #1182 link-rewrite execution** — Docs-owned per Architect's FLATTEN ruling 2026-06-09; Docs needs Verify-First README.md name-conflict check before move
- [⏸] **PA+CIO clean test for durable=true cron mechanism** — needs both roles to characterize the in-memory survival surface revealed by the `4c166d42` 2.5-day survival data; informs whether durable=true codification ever lands; Day-7 findings F4 reframe held pending
- [⏸] **Reviewer engagement on ADR-065 + ADR-066 + ADR-060 amendment + m-40** — cohort (PPM/Lead Dev/CIO/CEO) can engage when ready; not Architect-driven
- [⏸] **ADR-067 candidate for #952 Artifact** — Lead Dev's call per 6/8 ratification (Lead Dev's authorship + my ratification is natural shape, but Lead Dev may prefer to just ship)
- [⏸] **#1166 Type-2 Dreaming spike kickoff** — post-M3; structurally gated on persistence; convergence complete (Architect + PPM + CXO lenses all in 2026-06-08); awaiting M3 ship + spike-launch decision (PPM owns PDR)
- [⏸] **BYO-colleague Exec synthesis** — Exec is synthesizer; HOST + PPM lenses still pending; Exec drafts when source set complete (per source-set-anchor discipline)
- [⏸] **Lead-lane detector hook for session-log displacement** — Lead-lane build; CIO + Docs concur on commit-count keying ("no session-log growth across N substantive same-day commits"); composition with PreCompact-signoff-warning
- [⏸] **Docs `cleanup-dev-active` omnibus-coverage guard** — Docs filing per 6/9 evening exchange; protects already-displaced June 3-8 days from cleanup before omnibus coverage; load-bearing durability net

## Watch surfaces (not work; observation only)

- **methodology-40 Proven-bar progress** — 9 instances now (BYO-colleague skill-as-broker is #9 + first cross-architectural-arc instance per Fire 15 lens). Still largely Architect-authored. Watch for genuinely-cross-author invocations (HOST/PPM/CXO/CIO/Docs/PA invoking m-40 in their own lane).
- **methodology-41 (Mechanism Displaces Unreferenced Discipline) Proven-bar** — CIO filed Emerging 6/9 evening on Docs's audit data (founding instance: session-log displacement). Gated Proven on second-different-(mechanism, discipline)-pair instance. Watch for: linter displacing manual checklist; test suite displacing manual QA; or whatever else surfaces.
- **methodology-30 Proven-bar progress** — current 3 instances (Phase 3 coverage 6/7 AM; Phase 4 audit-cascade 6/7 PM; #371 event-shape 6/9 AM). All Lead-Dev-applied. CIO 6/8 correction said hold-Emerging + record-progress; the 3rd instance partially addresses arc-diversity + temporal-spread; cross-author still pending.
- **Pattern-072 application count** — at 8 applications post-ADR-066 (verb-enum 6th; capability primitive ADR-065 D3 7th; capability map ADR-066 D1 8th). 9th candidate at `resource_type` enum if BYO-colleague ADR-068 lands. Pattern-072 9th + #952 `ArtifactSourceType` + adversarial-perturbation registry (Type-2 spike) all pending.
- **Pattern-073 spec-layer extension** — 2 instances cataloged (Phase 3 coverage spec; source_type-in-slots-vs-context spec). CIO 6/8 disposition said "YES, explicit note" in the entry; CIO-owned edit pending.
- **External-alignment-Evolution-amendment pattern** — HOST May 24 generalization of Klatch-pause framing landed as Pattern-064 convention (Architect-applied 2026-06-06 in ADR-065 §Evolution). Watch for second non-Klatch external-dependency-uncertainty case to file as separate instance.
- **Duty-cycle gap-class catalog** — 6 classes surfaced 2026-06-06 → 2026-06-09 (worktree-sync-lag; signaling-channel; cron-death; weekly-usage-limit + account-switch; stale-prompt firing; rate-limit-mid-fire). HOST PM-as-catch disposition holds at "addressed-at-sub-mech + dashboard generalization."
- **Same-fire-coherence-across-related-work** — Day-5 findings Finding 5 working hypothesis (PPM refined to "bundle-shaped producing work; not reactive-mail lanes"); CIO folded into adaptive-interval cron-shape synthesis. Holds across producing AND reactive modes per Fire 10 evidence. Fire 15 (BYO-colleague lens FULL DEPTH same fire as receipt) is another instance. Cross-role validation needed before catalog promotion.
- **Four-layer-defense pattern** (session-log displacement source-fix shape) — emerged Fire 16: skill v1.5 dual-surface (source-catch) + cleanup-guard (durability-net) + detector hook (reactive-net) + m-31/m-41/CLAUDE.md (framing). Each layer at a different altitude; m-40 layer-then-migrate composability principle applies. Worth watching for second instance to potentially catalog as a sub-pattern of m-40 or m-41.
- **CIO m-41 Emerging-bar holding pattern as cohort default** — m-40 + m-41 both Emerging-at-founding-instance + Proven-on-generalization-evidence. Conservative-bar discipline operating as default disposition. Not yet a candidate but watch for it as cohort-pattern.

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
- [x] **methodology-40 (layer-then-migrate) v0.1 FILED + CIO COSIGNED + INDEXED** — Architect-authored 2026-06-09 morning; CIO cosigned + slot 40 + INDEX.md fixed same day evening
- [x] **HOST signaling-channel cohort-norm flag** — filed to HOST 2026-06-07; HOST disposition concur 2026-06-07; HOST drafting codification (pending HOST ship)
- [x] **Day-7 findings memo to CIO** — filed Day-5 2026-06-08; six findings; CIO dispositions returned same-day; F4 reframe pending PA+CIO clean test
- [x] **Docs #1182 models/models/ layout RULING** — FLATTEN (Option A); filed to Docs 2026-06-09
- [x] **Workstream-046 Architect lens** — FILED 2026-06-09 13:30 PT (late filing; transparent error acknowledgment); spine: "Verification matures into closure; spec-pipeline runs at cycle speed"
- [x] **BYO-colleague braintrust Architect lens** — FILED 2026-06-09 Fire 15 (~640 lines); composition-not-greenfield finding; m-40 instance #9 + first cross-architectural-arc instance
- [x] **Session-log displacement memo to Docs + 5 prevention recommendations** — FILED 2026-06-09 16:55 PT after PM 16:48 PT escalation; cohort-wide audit confirmed 6 of 9 cycling roles displaced ~15 role-days
- [x] **Two acks distributed for session-log displacement loop close** — Arch→Docs (four-layer-defense framing) + Arch→CIO (testimony-from-inside-trap as cleanest structural confirmation)
- [x] **#371 contract-seed event-shape Lead Dev ack** — methodology-30 consumer-trace instance #3; additive-gaps confirmed; no code change needed (best-case outcome)
- [x] **ADR back-references for m-40 in ADR-060 amendment + ADR-065 + ADR-066** — Fire 14 after CIO slot 40 confirmation

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
