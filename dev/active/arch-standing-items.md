# Architect Standing Items — Task List

**Purpose**: Architect's task queue per duty cycle v0.7 (worktree-as-cycle-default; cron-shape-experiments registry Row 1 = 3hr-interval bursty-lane).

**Convention**: tasks listed roughly by priority/cadence. Mark `[x]` when complete; `[⏸]` when blocked on external (per recurring-failure memory on deferred-AC). Move to "Closed" section at end-of-week.

**Last refreshed**: 2026-06-12 07:30 PT (Fire 33 maintenance-on-touch; closing F4 + WS-047 + PA+CIO-clean-test as obsolete-or-shipped; adding #1193 watch + m-42 watch + Pattern-073 sub-shape #3).

---

## Active

- [x] **methodology-40 (layer-then-migrate) v0.1 FILED + COSIGNED + INDEXED** — Architect-authored 2026-06-09 morning; CIO cosigned + slot 40 confirmed + INDEX.md brought current (CIO caught INDEX.md staleness bug along the way — was at m-35 Last Updated May 24; now current with m-36/37/38/39/40). Status Emerging; Proven gated on cross-author invocations. **Cross-author Proven-bar watch is now the standing item**: track if/when HOST/PPM/CXO/CIO/Docs/PA invoke m-40 by name in their own lane.
- [x] **ADR cross-reference back-pass** — Fire 14: ADR-060 amendment + ADR-065 + ADR-066 §Cross-references gained `methodology-40 (Layer-Then-Migrate, Emerging, CIO-confirmed 2026-06-09)`. Methodology-corpus back-refs left to CIO's opportunistic-touch lane per CIO judgment.
- [x] **Day-7 findings F4 reframe — RESOLVED by CIO Gap-C empirical investigation 2026-06-11** (`cc-memo-cio-to-pm-cron-halt-investigation-2026-06-11.md`). Gap-C session-dormancy is dominant; durable=true no-op was correct as it stood. The `4c166d42` 2.5-day "survival" was probabilistic per-resume, not a feature. What CHANGED: 2026-06-08 weekly-usage-limit + 2026-06-10/11 DinP migration = two cohort-wide session-restart events surfaced the gap. Cure: Routines watchdog $70/mo (PM-gated funding). My Fire 25 "two surfaces" framing superseded.
- [x] **Workstream-047 Architect lens FILED 2026-06-12 ~07:00 PT Fire 32** — paced to source-set state per PM 6/9 [Anchor on source-set state] correction (NOT Tue Jun 16 backstop); 6 load-bearing arcs; 2 spine candidates (preferred: "naming what we already do — the catalog grows discipline before crisis"; alt: "composition-not-greenfield"). PM/Exec own altitude call.
- [ ] **#1193 session_scope() audit watch** (NEW 2026-06-12) — Lead-Dev-owned audit fan-out greenlit Fire 32; 149 callers classified into (a) read-only / (b) writes+commits / (c) writes-no-commit-trap. Architect-on-call for fix-shape ratification when audit lands. **Strong-lean Option A** (make session_scope commit on clean exit, match docstring) gated on 0 no-commit-dependent callers; if ≥1 surfaces → **layer-then-migrate (m-40)** with `session_scope_readonly()`. Guard mandatory (AST ratchet). Lead Dev's m-40 invocation as fallback = first cross-author cross-architectural-arc m-40 instance from a different lane (boundary-discipline, not dispatcher).
- [ ] **#973 MEM-CACHE-AUDIT Phase 1 audit** — PM-ratified ship-now-as-prep May 19; ~1-2 hr Architect drive + ~2-3 hr Lead Dev support. STABLE/DYNAMIC labeling + pipeline reorder + per-method TTL suggestions, no behavioral change. Needs Lead Dev coordination — focused session, not fire-driven. **Status check 2026-06-12**: Lead Dev now ALSO in #1193 audit + #1194 Recently home + #1124 Phase 4 + #952 + #355; #973 further deferred until queue clears.
- [ ] **BYO-colleague ADR-068 prep** (M4 trigger) — braintrust convergence complete 6/9; Exec synthesis filed; PPM roadmap-altitude ruled ADR-068-only / no PDR-006; ADR-068 drafts at M4 timing per PPM sequencing. **Architect inputs to carry to drafting**: 6 D-sections (skill-as-broker; needs_signal package_type Pattern-072 9th app; capability-discovery inverted-handshake; staged-context store as ADR-065 D2 conformant package; multi-actor attribution actor_chain extending ADR-063; freshness-window discipline). **NEW from Exec synthesis Fire 21 read**: resource-consent as 4th consent dimension (HOST-surfaced; the user's LLM key/limit is a spendable resource; load-bearing post-6/9 usage-wall). Hold for ADR-068 D5 (consent architecture) at M4 drafting. **NO Architect action until M4 trigger.**
- [x] **duty-cycle-tick skill v1.5 dual-surface ADOPTED** — in active use since 2026-06-10; Step-0 self-heal triggered cleanly Fire 24 (June 10 close-out) + Fire 31 (June 12 START); dual-surface session-log/cycle-log composition holding across 20+ fires; m-31 amendment in CLAUDE.md supports.

## Blocked / waiting on external

- [⏸] **CIO P-073 spec-layer note** — CIO-owned per 6/8 disposition; CIO will action in a follow-up fire (still pending as of Fire 16 evening)
- [⏸] **CIO m-30 Emerging-with-progress edit** — CIO-owned per 6/8 correction; reflects 2-of-3 hold; m-30 instance #3 6/9 (#371 event-shape trace) was a different subsystem but still Lead-Dev-applied (cross-author not yet satisfied)
- [⏸] **HOST mail-vs-GH signaling-channel cohort-norm codification** — HOST-owned per 6/7 disposition; HOST drafting
- [⏸] **Docs #1182 link-rewrite execution** — Docs-owned per Architect's FLATTEN ruling 2026-06-09; Docs needs Verify-First README.md name-conflict check before move
- [x] **PA+CIO clean test for durable=true — OBSOLETE per CIO Gap-C resolution 2026-06-11**. No clean test needed; mechanism characterized empirically (durable=true is no-op; session-dormancy is the failure mode). Cure is external watchdog, not in-memory durability codification.
- [⏸] **Reviewer engagement on ADR-065 + ADR-066 + ADR-060 amendment + m-40** — cohort (PPM/Lead Dev/CIO/CEO) can engage when ready; not Architect-driven
- [⏸] **ADR-067 candidate for #952 Artifact** — Lead Dev's call per 6/8 ratification (Lead Dev's authorship + my ratification is natural shape, but Lead Dev may prefer to just ship)
- [⏸] **#1166 Type-2 Dreaming spike kickoff** — post-M3; structurally gated on persistence; convergence complete (Architect + PPM + CXO lenses all in 2026-06-08); awaiting M3 ship + spike-launch decision (PPM owns PDR)
- [⏸] **BYO-colleague Exec synthesis** — Exec is synthesizer; HOST + PPM lenses still pending; Exec drafts when source set complete (per source-set-anchor discipline)
- [⏸] **Lead-lane detector hook for session-log displacement** — Lead-lane build; CIO + Docs concur on commit-count keying ("no session-log growth across N substantive same-day commits"); composition with PreCompact-signoff-warning
- [⏸] **Docs `cleanup-dev-active` omnibus-coverage guard** — Docs filing per 6/9 evening exchange; protects already-displaced June 3-8 days from cleanup before omnibus coverage; load-bearing durability net

## Watch surfaces (not work; observation only)

- **methodology-40 Proven-bar progress** — 9 architectural instances + **first cross-author cross-arc Lead-Dev-invoked instance Fire 32 (2026-06-12)**: Lead Dev's #1193 confirmed plan invokes m-40 by name as the fallback path if no-commit-dependent caller surfaces. This is the first time a non-Architect role has independently selected m-40 as the migration shape in their own lane (boundary-discipline, distinct from the dispatcher cluster). Cross-author signal strengthening; Proven-bar gating now needs second non-Architect-lane invocation.
- **methodology-41 (Mechanism Displaces Unreferenced Discipline) Proven-bar** — CIO filed Emerging 6/9 evening on Docs's audit data (founding instance: session-log displacement). Gated Proven on second-different-(mechanism, discipline)-pair instance. Watch for: linter displacing manual checklist; test suite displacing manual QA; the AST guard for #1193 session_scope() would qualify if it ships.
- **methodology-42 (Reflexive Verification — we self-exempt from our own rigor under pressure) Proven-bar** (NEW 2026-06-11) — CIO filed Emerging from my Fire 26 recognition + 5-instance articulation. Watch surface: self-catch-rate-up evidence post-naming → Proven; if not → escalate to m-36 structural guard ("claims-of-mechanism require a cited check"). Today's #1193 disposition included an explicit lens-check ("is my Option A blind?" → answered "audit-gated, not blind") — a small self-application instance.
- **methodology-30 Proven-bar progress** — current 3 instances (Phase 3 coverage 6/7 AM; Phase 4 audit-cascade 6/7 PM; #371 event-shape 6/9 AM). All Lead-Dev-applied. CIO 6/8 correction said hold-Emerging + record-progress; the 3rd instance partially addresses arc-diversity + temporal-spread; cross-author still pending.
- **Pattern-072 application count** — at 8 applications post-ADR-066 (verb-enum 6th; capability primitive ADR-065 D3 7th; capability map ADR-066 D1 8th). 9th candidate at `resource_type` enum if BYO-colleague ADR-068 lands. Pattern-072 9th + #952 `ArtifactSourceType` + adversarial-perturbation registry (Type-2 spike) all pending.
- **Pattern-073 spec-layer extension** — 3 instances cataloged with new sub-shape (Phase 3 coverage spec; source_type-in-slots-vs-context spec; **#1193 `session_scope()` docstring-asserted behavior drift 2026-06-12 — docstring promised "Automatic commit and cleanup," implementation has no commit; surfaced via silent write-loss in InsightJournal**). The docstring-vs-implementation sub-shape is distinct from the route-conventions cluster — same Pattern-073 frame, different surface layer (in-code spec vs. external doc spec). CIO-owned catalog edit; flag the sub-shape.
- **External-alignment-Evolution-amendment pattern** — HOST May 24 generalization of Klatch-pause framing landed as Pattern-064 convention (Architect-applied 2026-06-06 in ADR-065 §Evolution). Watch for second non-Klatch external-dependency-uncertainty case to file as separate instance.
- **Duty-cycle gap-class catalog** — 6 classes surfaced 2026-06-06 → 2026-06-09 (worktree-sync-lag; signaling-channel; cron-death; weekly-usage-limit + account-switch; stale-prompt firing; rate-limit-mid-fire). HOST PM-as-catch disposition holds at "addressed-at-sub-mech + dashboard generalization."
- **Same-fire-coherence-across-related-work** — Day-5 findings Finding 5 working hypothesis (PPM refined to "bundle-shaped producing work; not reactive-mail lanes"); CIO folded into adaptive-interval cron-shape synthesis. Holds across producing AND reactive modes per Fire 10 evidence. Fire 15 (BYO-colleague lens FULL DEPTH same fire as receipt) is another instance. Cross-role validation needed before catalog promotion.
- **Four-layer-defense pattern** (session-log displacement source-fix shape) — emerged Fire 16: skill v1.5 dual-surface (source-catch) + cleanup-guard (durability-net) + detector hook (reactive-net) + m-31/m-41/CLAUDE.md (framing). Each layer at a different altitude; m-40 layer-then-migrate composability principle applies. Worth watching for second instance to potentially catalog as a sub-pattern of m-40 or m-41.
- **CIO m-41 Emerging-bar holding pattern as cohort default** — m-40 + m-41 both Emerging-at-founding-instance + Proven-on-generalization-evidence. Conservative-bar discipline operating as default disposition.
- **Conservative-bar Proven-gating at 5 catalog entries (2026-06-12 watch)** — m-30 / m-40 / m-41 / m-42 + ship-routine-keep-loop corollary all filed Emerging carrying the same gating discipline. Watch for 6th entry; if it lands, the catalog's-own-discipline-shape becomes cohort-canonical default worth a meta-catalog note.
- **Meta-pattern "entry-catches-its-authors-at-authoring-time" at 2 instances** — m-41 (CIO filing FROM the displacement audit that displaced itself) + m-42 (CIO filing FROM my self-application failure on session-log displacement at the same hour I argued for the rule). Quiet watch; 3rd instance → CIO-edit-lane catalog entry.

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

## Recently closed (2026-06-10 → 2026-06-12)

- [x] **F4 cron-durability RESOLVED** — CIO empirical investigation 2026-06-11 16:12 PT closed the loop; Gap-C session-dormancy is the dominant mechanism; durable=true no-op; cure is Routines watchdog (PM-gated funding); my Fire 25 "two surfaces" framing superseded; supplied second instance feeding m-42.
- [x] **methodology-42 (Reflexive Verification) Emerging filed** — CIO authored 2026-06-11 16:12 PT from my Fire 26 recognition memo + 5-instance articulation; entry-catches-its-authors meta-pattern at 2 instances.
- [x] **Workstream-047 Architect lens FILED** — 2026-06-12 ~07:00 PT Fire 32; paced to source-set state per PM 6/9 anchor correction; 6 arcs, 2 spine candidates.
- [x] **#1193 session_scope() disposition shipped to Lead Dev** — 2026-06-12 Fire 32; audit greenlit, strong-lean Option A, layer-then-migrate fallback, guard mandatory; Lead Dev ack returned same-hour with plan confirmed + sequencing behind #1194 Recently home.

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
