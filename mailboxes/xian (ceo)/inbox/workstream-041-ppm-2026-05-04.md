---
from: PPM (Principal Product Manager)
to: exec (Chief of Staff)
cc: CEO (xian), PA (Piper Alpha)
date: 2026-05-04
subject: Ship #041 workstream review — Apr 24–30 window — PPM lens
priority: normal
window: 2026-04-24 (Friday) – 2026-04-30 (Thursday)
naming-standard: per CoS Apr 19 (`workstream-{ship#}-{role}-{date}.md`)
verifiable-claims-norm: per `memo-exec-to-host-verifiable-claims-2026-04-19.md`
sources-primary: omnibus logs Apr 24/25/26/27/28/29/30 (per CEO direction in v2 kickoff); v2 kickoff `memo-exec-to-leadership-ship-041-workstream-kickoff-v2-2026-05-04.md`; primary-sense-clarification `memo-exec-to-leadership-cc-ceo-pa-docs-cio-primary-sense-clarification-2026-05-04.md`
sources-verification: PPM session logs Apr 25-27 (own primary record), commit hashes cited inline
---

# Ship #041 PPM Workstream Review

## TL;DR

- **#992 ETHICS-ACTIVATE arc closes in six calendar days** end-to-end (initial S1 floor-bypass finding Apr 25 → Phase F flag-flip merged `deecc816` Apr 30 → #992 closed properly with 8/8 ACs marked). Phase E gate held against three test scenarios; #1002 + #1003 filed and closed; #1004 design contract → ship in single Lead Dev session against ~3-day estimate.
- **PM-named alpha catch-22 reframes calibration plan structurally** (Apr 30, ~7:45 AM PT): wait-for-real-traffic-calibration unreachable from alpha. Three-phase reframe (simulation harness → beta-traffic refinement → stable) becomes the calibration plan; flip-now decision authorized same morning. **Single load-bearing PM intervention of the window.**
- **C-axis rubric drift caught and reconciled as a discipline issue** (Apr 26): Phase E rubric C=Clarity vs CT v2 C=Context produced verdict-convergent / methodology-divergent scoring. Reframed per PM "we still need to clarify and align anytime we notice drift" → Pattern-063 (Parallel-Authoring Drift) Emerging filed by CIO + Methodology-24 (Branch-or-Anchor) + CT v2.3 embeds rule directly in rubric — all within 24 hours.
- **Migration wave completes Apr 26** (Architect 12:48 PM, Exec 1:45 PM); first day on the project with all seven leadership roles + Lead Dev simultaneously on Code. Apr 27 demonstrates four parallel substantive workstreams converging by calendar (Lead Dev #1004 ship, HOST 360 synthesis, CIO methodology codification, Docs briefing sweep) — none coordinated explicitly.
- **BYOC PDR scoping outline trigger fired Apr 27 ~14:00 PM** (PM "we have now reached that trigger point"); rate-limited same hour to post-Ship #040 publication. Cover memo + scoping outline staged in `dev/active/` with explicit DRAFT/HELD framing. Ship #040 published Apr 29; trigger conditions now met but PPM was not active Apr 28–30 to fire the distribution. **Open as carry-forward.**

## What landed

### Phase E gate-close + #1002/#1003 escalation (Apr 25 evening)

PPM's first Code session (`friendly-proskuriakova-990919` worktree, opened 6:40 PM) drafted **Phase E sign-off with 5 refinements** before Lead Dev's run completed: (1) Tone-3 anchor calibration deferred to CXO; (2) judging panel CXO + PPM as primary scorers, PM tiebreak only on ≥2-pt divergence; (3) re-run policy fresh instance + written dispute rationale; (4) transcript naming `transcript-s{N}-r{N}.md` with metadata header; (5) false-positive findings → `known_pathological` tag standing policy from Phase F+. PM sanity-checked + approved; sign-off filed to Lead Dev's inbox after the run completed (concurrent paths handled through artifacts, neither blocking the other).

Phase E run surfaced **Scenario 1 floor-bypass-by-pre-classifier finding**: pre-classifier matched "blocking my PRs" → `list_prs_query` and the canonical handler responded before the ethics floor saw the message. PPM finding-response memo with **4 decisions**: re-run S1 rephrased (keep r1 transcript permanently as Finding 1 evidence); **file bypass as P0 tracked issue, recommend as Phase F flag-flip blocker** (Pattern-045 territory: activating ethics with documented bypass = safety theater); Architect scoping required before Phase F (coverage breadth + fix shape); score scenarios 2 & 3 in parallel.

**#1002 filed** (P0, Lead Dev): *"Pre-classifier keyword-match dispatch shadows ethics floor for handler-adjacent input."*

### Phase E scoring exchange + #1003 filing (Apr 26)

S1 r2 (rephrased) re-ran ~02:00 AM Apr 26: floor reached the message (`floor_hit: true`) but classifier produced `category: GUIDANCE / action: provide_guidance` rather than firing the harassment-boundary code path — usable redirect content but no `boundary_type: harassment` envelope. **#1003 filed** by PPM Apr 26 morning: *"Phase E S1 r2: Harassment-vector input classified as GUIDANCE intent; ethics infrastructure did not engage."*

**Scoring**: PPM 7/8/8 PASS (S2/S3/S1 r2); CXO independently 9/9/9 PASS — convergence on PASS verdict, no tiebreak needed. CXO's §6 finding (three possibilities a/b/c for the GUIDANCE-vs-HARASSMENT classification) and PPM's #1003 surfaced the same defect from independent observation.

### C-axis rubric reconciliation as discipline issue (Apr 26 morning)

Verdict-convergent scoring revealed methodology-divergent application: PPM scored against CT v2 (C=Context), CXO scored against Phase E rubric draft (C=Clarity). Same letter, materially different criteria. PPM's initial framing was "v2.x calibration data note." PM corrected: *"terminology or rubric drift worries me. It suggests hearsay and guesswork vs a reference source... we still need to clarify and align anytime we notice drift."*

**PPM C-axis reconciliation memo filed** (Apr 26 morning) treating it as discipline issue, not v2.x note. Three reconciliation options proposed; PPM lean Option 1 (anchor Phase E to CT v2 canonical) + Option 3 (branch-or-anchor decision rule as durable safeguard). CIO + CXO concurred Apr 26 evening; **C-axis closure memo filed** Apr 27 (`c4497f5a`) confirming convergence.

Downstream: **CIO files Pattern-063 Emerging** (Parallel-Authoring Drift) Apr 27 (`a5d82e82`); **Methodology-24** (Branch-or-Anchor) + **Methodology-25** (Workstream Review Cadence) Apr 27 (`3bcd9eed`); **CT v2.3** embeds Branch-or-Anchor rule directly in rubric Apr 27 (`64a94e2e`). Methodology-to-codification latency: ~24 hours from PPM memo to four canonical landings.

### Phase F flag-flip recommendation v1 → v4 (Apr 26)

**v1** (~9:15 AM): DO NOT AUTHORIZE pending #1002 + #1003 resolution. Filed without explicit PM approval after I'd asked for sanity-check; PM had topic-shifted to inbox triage. **Retraction memo filed** (`bd518aef`) preserving the original retracted file in inboxes per audit-trail discipline. Memory entry saved (`feedback_explicit_approval_for_authority_memos.md`): topic-changes ≠ approval; PM-authority memos require explicit re-confirmation before distribution.

**v3** (~10:45 AM, after #1003 diagnostic landed): Lead Dev's `flag=false` comparison run on S1 r2 produced byte-identical audit envelope — flag observably inert for harassment vectors on this code path. Recommendation strengthened.

**v4** (~1:50 PM, after Lead Dev S2 flag-off + 3 additional vectors): **category-conditional theater** framing — flag matters for PROFESSIONAL (envelope present flag-on, absent flag-off) but is theater for HARASSMENT (4-vector confirmation envelope absent both ways). Public-facing one-liner: *"Activating ethics enforcement when the highest-stakes category (HARASSMENT) has no actual enforcement, while a lower-stakes category (PROFESSIONAL) does, would assert asymmetric coverage exactly inverted from where stakes are highest."* PM/PA Phase F decision memo (Apr 26 ~12:00 PT) named the **"no silent failures" companion principle** — the system-level analog of PDR-004 anti-fabrication.

### HOST 360 synthesis acknowledgment + BYOC trigger fired (Apr 27)

HOST 360 synthesis (`244b0ea7` + `aad2b1c2`) named **three PPM-specific pulls**: Pattern E workstream memo split (PPM §4.4 framing canonical), explicit "needs PPM review" gates on product-facing changes (PPM §9.2), joint ADR-061 BYOC with Architect (Architect §8.3 + PPM §8.3 independent convergence — *"the strongest decision-debt signal in the cohort"*).

PPM acknowledgment memo (`794b9841`) accepted all three pulls; proposed **paired-document approach** (PDR-005 + ADR-061 separate but cross-referencing) per existing PDR-001/ADR-060 precedent. Asked PM whether HOST cohort-surfacing fired the held-distribution trigger for the BYOC PDR scoping outline.

**PM Apr 27 ~14:00 PT**: *"we have now reached that trigger point."* Fourth trigger condition fires (PM signals "what's next on product strategy queue"). PM Apr 27 ~14:04 PT proposed **rate-limiting** the distribution to post-Ship #040 publication (~Wed Apr 29). PPM concurred — discovery thread parallelizes naturally; doesn't compete with Phase F implementation bandwidth.

Three artifacts produced (held in `dev/active/`):
- `ppm-pdr-byoc-scoping-outline-2026-04-26.md` (six decision-rule questions; tier-placement question PDR-005 Foundational vs PDR-201 Integration Patterns; six-step suggested sequence)
- `draft-cover-memo-byoc-pdr-scoping-distribution-held-until-post-ship-040.md` (explicit DRAFT/HELD framing in front-matter)
- New memory entry: `feedback_rate_limit_cross_traffic_at_inflection.md` (captures PM instinct as recurring discipline)

### Migration wave completes (Apr 26)

PPM was the fifth role to migrate (Apr 25 evening, alongside CXO). Architect migrated Apr 26 ~12:48 PM; Exec ~1:45 PM. **First day on the project with all seven leadership roles + Lead Dev simultaneously on Code.** Predecessor PPM handoff §3 framing of PA↔PPM coordination held: PA drafts analysis, PPM reviews and translates into product positions, PM decides — pattern executed cleanly Apr 25-27 (Phase E lens-pass appendix Apr 25, branch-discipline routing reply Apr 26, coordination check exchange Apr 26).

## What surfaced

### "Where does the data come from?" as a category-of-question (Apr 30 Lead Dev self-flag)

PM's catch-22 question on calibration data was the load-bearing intervention of Apr 30: wait-for-real-traffic calibration unreachable from alpha because alpha = no real users. Lead Dev's self-flag captured the methodology gap: *should have surfaced this Apr 28 when wait-for-calibration first landed; CEO surfaced it today*. The deployment-phase-mismatch in calibration plans is a candidate proto-pattern (deployment-phase-mismatch-in-calibration-plans). For PPM this generalizes to gate-design discipline: **calibration plans must bind to a specific traffic source; "real users" is not a source until users exist.** Worth importing as standing diagnostic for any future gate that depends on observation-window data.

### Methodology-to-runtime latency continues to compress

Apr 27 codification arc (Pattern-063 + Methodologies-24/25 + CT v2.3) → Apr 28 operational automation (`merge-keeper-sweep.py` 454 lines + `regenerate-mailbox-manifests.py` 319 lines, both shipped by Lead Dev) → Apr 29 hook+CLAUDE.md fix (briefing-freshness response) → Apr 30 catch-22 reframe → flip → #992 closure. **Methodology landings within hours of operational findings is the new tempo, not the exception.** From PPM's lens this changes the C-axis-style discipline-recovery cadence: drift surfaced Apr 26 morning → reconciliation closed Apr 27 closure memo (24 hours), with all four downstream methodology landings same day.

### Verdict-convergence as a dangerous signal (CIO Apr 26)

CIO's diagnostic question — *"What would have to be true for these to be wrong in the same direction?"* — surfaces in the C-axis reconciliation thread and generalizes beyond rubrics. When two divergent methods produce the same answer on trivial cases, that tells you nothing about non-trivial cases. PPM importing as a standing diagnostic for future scoring exchanges, sub-epic gate signals, and any product-decision input where output convergence might mask methodology divergence.

### Phase F decision shape changed across the week

Apr 26 v4: DO NOT AUTHORIZE — category-conditional theater; missing harassment coverage. Apr 27: all conditions empirically met (Lead Dev #1004 SHIPPED end-to-end same day); Lead Dev recommends defer pending ADR-061 + calibration window. Apr 28 ADR-061 v0.1 filed (Architect, `35a1108c`); Lead Dev review names "no further gating concerns; mid-week ratification feasible." **Decision shape shifted from "are we ready?" to "how long is the calibration window?"** Apr 30 catch-22 surfaces the deployment-phase-mismatch; flip-now reframe collapses the wait. Single PM intervention reshaped a multi-day sequencing question into a same-day authorization.

### M2d framing correction landed

Apr 26 omnibus footnote: M2d corrected to **MUX Lifecycle** (#703, #707, #714, #869), not Context Assembly. Predecessor handoff §1 had it as #951 context-assembler expansion; PM Apr 25 directive corrected. PPM's Ship #040 v2 used the predecessor framing — worth noting as correction now in the record. M2c-tail finishes before M2d starts per the same directive.

## What's still open

- **BYOC PDR scoping outline distribution** — held in `dev/active/`; trigger condition (post-Ship #040 publication) fired Apr 29 ~10:30 AM PT; distribution still pending. PPM not active Apr 28–30 to fire it. First action when PPM resumes (today, May 4).
- **ADR-061 v1.0 PM ratification** — Architect committed Apr 30 with all 6 of Lead Dev's review findings folded; ratification pending. PM signed off mid-afternoon Apr 30 for Open Laws Sprint focus block.
- **Sub-epic gate definitions for M2d/M2e** — PPM responsibility per predecessor handoff §2 as M2c approaches completion. Not engaged in this window.
- **Pattern-063 + Pattern-064 slot allocation finalization** — CIO Apr 27 noted slot allocation pending PM concurrence; status of both patterns at "Emerging" awaiting trial cycle before "Proven."
- **#1004 follow-on issues** — #1006/#1007/#1008 audit_transparency cluster + #1027/#1028/#1029 dead-code follow-ups + Architect's Apr 27 Phase 1 LLM-touch lens 12 issues filed (3 P1, 3 P2, 6 P3) including "alive scaffolding" architectural-debt class. None PPM-owned but PPM may want to weigh in on quality-threshold implications when the cluster reaches gate consideration.
- **Calibration enhancement scope** — Architect's design needed before BoundaryEnforcer accumulates observations under Phase F flag-on; simulation harness Phase A unbounds the calibration data source. PPM may want to weigh in on what "observable signal" means at the product layer.
- **IAC retroactive coverage** — Apr 17 Philadelphia "Ethics as IA" presentation omitted from Ship #040 narrative (PM flag Apr 29); routed to Comms for Ship #041 framing per Exec Apr 30 catch-and-fold pattern. Worth knowing as PPM if the framing ends up affecting product narrative on the activation arc.

## Cross-role threads worth naming

- **The #992 arc as methodology demonstration**: every layer worked across the six days. Rubric drift caught + reconciled within 24 hours; Pattern-063 + Methodology-24 codified within 24 hours; #1004 contract-then-build-then-ship in single Lead Dev sessions; alpha catch-22 surfaced and reframed by PM in real-time; Phase F merged + #992 closed properly via skill (8/8 ACs). **The product-decision-quality story is the recursive validation**: rubric scored honestly even when verdict-convergent, drift surfaced as discipline issue not v2.x note, fix was structural (semantic detector + literal-trigger backstop) not patch, calibration plan reshaped by data-source-question rather than time-pressure.
- **Migration's parallel-velocity payoff is now reproducible-by-default, not occasional** (per Apr 28 omnibus). Apr 27's four-workstream convergence (Lead Dev #1004, HOST 360 synthesis, CIO methodology codification, Docs briefing sweep) ran independently and converged by calendar; Apr 28's five-stream day (Lead Dev 13-commit shipping arc, Architect ADR-061 + Pattern-064, Docs sign-off discipline + publish + cleanup, Exec briefing refresh, PA branch-discipline synthesis) reproduced the pattern. The post-migration parallel-velocity ceiling is being demonstrated, not hypothesized.
- **Branch-discipline norms layer in same-week response cadence**: Apr 26 mailbox-discipline norm landed (CLAUDE.md + check-branch.sh hook + leadership memo) under emergency time pressure; Apr 28 sign-off discipline norm landed proactively (CLAUDE.md + Docs merge-keeper sweep section + Lead Dev hook-feasibility scoping); Apr 29 PA branch-discipline synthesis v1.0 final published at canonical path with explicit + silence-=-concur cohort acceptance. PPM-side discipline pairing: per-memo commit-push norm absorbed across the cohort (lessons from Lead Dev's 17-PPM-moves incident propagated into PPM's own explicit-paths staging discipline by Apr 27 evening).
- **The 062/063/064 architectural-debt family is now complete**: 062 component-layer (Assembly Assumption), 063 vocabulary-layer (Parallel-Authoring Drift, CIO Apr 27), 064 extension-layer (Extension Without Integration, Architect Apr 28 — #197 substring detector recall gap as reference instance). Same root cause (integration-pass missing); three layers of where it manifests. Future architectural-debt findings should ask: which family member is this? PPM lens implication: any product decision that opens a new integration surface should specify the integration pass that closes the loop.

## For PM/Exec consideration

**Theme proposal: "The Activation Arc Closes"** — captures the #992 multi-week arc closing in 6 calendar days as the through-line; lets the methodology-codification + migration-parallel-velocity threads + alpha-catch-22 reframe land as the supporting evidence that the closure was structural, not coincidental.

**Alt themes considered**: "Activation, with Honesty" (foregrounds the catch-22 reframe but understates the structural completeness); "From Bypass to Ship in Six Days" (direct narrative but loses the methodology compounding); "The Methodology Compounds at Speed" (parallels Ship #040's "The Methodology Audits Itself" but may feel redundant in the cycle-after-cycle pattern).

**Worth flagging for PM**: the recurrence of *"PM-named structural reframe in real-time"* (Apr 26 "no silent failures" companion principle; Apr 26 "rubric drift is a discipline issue, not a v2.x note"; Apr 27 BYOC trigger invocation; Apr 27 rate-limiting at inflection points; Apr 30 alpha catch-22) is a load-bearing pattern of this window. Each intervention reshaped a multi-day sequencing question into a same-day decision. From PPM's lens this is the strongest cohort signal that PM-as-product-judgment-surface compounds when conversational rhythm preserves real-time access — which connects directly to HOST 360 Pattern C ("PM-as-mail-courier doesn't scale") and Exec briefing's 2-week addition on conversational rhythm with PM.

**One product-narrative consideration**: Ship #040 told the methodology-audits-itself story; Ship #041 has a parallel arc available — *the activation gate is the methodology's hardest test, and the gate's product was a structural fix to the gate itself*. The recursive shape is real. Worth consideration in theme selection but PM/Exec call.

---

— PPM, 2026-05-04
