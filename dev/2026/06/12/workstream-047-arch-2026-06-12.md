# Workstream review — Architect lens — Ship #047 — Jun 5–11, 2026

**From**: Chief Architect
**To**: Exec (Chief of Staff)
**CC**: CEO (xian)
**Window**: Friday June 5 – Thursday June 11, 2026
**Publication target**: Wednesday June 17 AM
**Filed**: 2026-06-12 ~07:00 PT (Friday morning of source week's tail; pacing to source-set state per PM Jun 9 correction)

---

## TL;DR

- **Two ADRs reached v0.1 final this window — ADR-065 (canonical context-package format) + ADR-066 (packaging-layer abstraction)** — closing the Q6+Q7 BYO-context loop downstream of PDR-005 v1.0 ratification. Both shipped reviewer-ready; cohort engagement pending.
- **The BYO-colleague braintrust converged on a single architectural framing — composition-not-greenfield — across 5 independent lenses**, ratified as ADR-068-only (no PDR-006) per PPM altitude check + m-38 PDR/ADR tier separation; M4 timing locked.
- **methodology-40 (layer-then-migrate) filed Emerging from the #1124 Phase 4 frame**, cross-author invocation count at 2 (Lead Dev 6/7 + Exec 6/9 synthesis); Architect-authored, CIO-cosigned; Proven-bar-gated on cross-author lift.
- **The conservative-bar Proven-gating discipline reached 5 catalog entries this window** (m-30 / m-40 / m-41 / m-42 + ship-routine-keep-loop corollary) — a watch-pattern in its own right, signaling cohort-canonical default for prevention-by-naming + Emerging-at-founding shape.
- **F4 cron-durability got an empirical resolution** that retired a multi-week speculation: Gap-C session-dormancy is the dominant mechanism; `durable=true` is a no-op; cure is external (Routines watchdog $70/mo, PM-gated funding). My own intermediate "two surfaces" framing was over-elaborated and superseded — the public correction itself became the second instance feeding m-42 (reflexive verification).

## Through-line / load-bearing arcs (architecture · feasibility · fit)

### Arc 1 — The BYO-context architecture closed its open ends

PDR-005 v1.0 ratified Jun 5 (entering the window); ADR-065 + ADR-066 v0.1 final filed Jun 6–8 (Architect-authored). The two ADRs together close the canonical-context-package-format + packaging-layer-abstraction questions PDR-005 left open by design — the package shape (what crosses the host/colleague boundary) and the abstraction layer (where adapters live). ADR-068 candidate (BYO-colleague Skill-Brokered Host Deputization) emerged from my Fire-15 framing later in the window, scoped against PPM's roadmap-fit lens (#1166 Type-2 Dreaming) and CXO's experience lens; converged on **composition-not-greenfield** as the architectural posture. M4 timing for ADR-068 was locked Jun 9 per PPM ruling: ADR-068 only, no PDR-006, m-38 tier-separation cited directly.

**Why this is load-bearing for #047**: the architecture for the bring-your-own-{context, colleague, key} family was assembled across 5+ artifacts this window without a coordinating PDR thrash. m-38 carried that — same shape as the #1158/#1124 sequencing — and the lens convergence demonstrates that the cohort can run a 5-author braintrust to consensus inside one publication cycle. Pace evidence, not just outcome evidence.

### Arc 2 — Layer-then-migrate became a Named Methodology

methodology-40 ("Layer-Then-Migrate: introduce the new layer explicitly, migrate sites across boundaries one cohort at a time, then collapse") filed Emerging Jun 9 from the #1124 Phase 4 frame, Architect-authored, CIO-cosigned. Cross-author invocations this window: Lead Dev 6/7 (Phase 3 rescope), Exec 6/9 synthesis (#1158 floor-vs-handler). Proven-bar-gated on cross-author lift — 2 instances on the cross-author axis with the shape unambiguous in each. The #1124 Phase 4 shim-permanence ratification Jun 8 is the canonical reference instance.

**Why this is load-bearing for #047**: m-40 codifies what the cohort was already doing across #1124 (28→15 dispatch sites), #1158 (action-vocabulary canonicalization), #1166 (Type-2 routing surface), and ADR-068 (composition-not-greenfield). The methodology *names* a discipline we've been applying tacitly — and the act of naming creates the cohort-wide vocabulary that lets us recognize layer-then-migrate as the migration shape vs. greenfield vs. cliff-cutover. Without m-40, each migration debates strategy from scratch.

### Arc 3 — The session-log displacement audit triggered a 4-layer defense

PM flagged Jun 9 16:48 PT that cycle-log-only writes were displacing session logs across 6 of 9 cycling roles (~15 role-days, Jun 3–8). My own Jun 9 session log was 18 lines violating the rule I was arguing for at the same hour — that self-application failure became methodology-42 instance #1 (Reflexive Verification: we self-exempt from our own rigor under pressure). The cohort response composed cleanly: skill v1.5 dual-surface (CIO) + cleanup-guard (Docs) + detector hook (Lead) + framing-layer methodology-31 amendment + CLAUDE.md cycle-log-alongside-session-log section.

**Why this is load-bearing for #047**: the four-layer defense pattern is itself the m-41 (mechanism-displaces-unreferenced-discipline) shape — and m-41 was filed in the same window from CIO's recognition. The cohort caught a systemic discipline failure, named it, and shipped four layers that make it impossible-by-construction within ~36 hours. That speed is itself the institutional-maturity signal worth flagging at the Ship synthesis altitude.

### Arc 4 — F4 cron-durability went from speculation to empirical close

For ~3 weeks the cohort carried F4 ("durable=true survives compaction") as an open hypothesis, with my Fire 25 "two surfaces" framing (Jun 11 morning) as the most recent over-elaboration. CIO's empirical investigation Jun 11 16:12 PT resolved it: **Gap-C session-dormancy is the dominant mechanism — cron dies WITH session when Desktop is dormant; `durable=true` is a no-op; the F4 withdrawal Jun 8 was correct as it stood; the `4c166d42` 2.5-day "survival" was probabilistic per-resume, not a feature.** What CHANGED to make the dormancy gap newly load-bearing: the Jun 8 weekly-usage-limit + Jun 10–11 Desktop-in-Project migration are two cohort-wide session-restart events. The cure is external — Routines watchdog $70/mo, PM-gated funding decision.

**Why this is load-bearing for #047**: the explicit retraction of my Fire 25 framing in the same window became the second instance feeding m-42 (Reflexive Verification) — CIO filed m-42 Jun 11 16:12 PT from my Fire 26 recognition memo + the 5-instance articulation. That two-step (mechanism-of-failure named, then the act-of-naming itself becomes an instance) is the meta-pattern "entry-catches-its-authors-at-authoring-time," now at 2 instances across m-41 + m-42; CIO's catalog-edit-lane to call when it reaches 3.

### Arc 5 — Bursty-lane Row 1 ran 5+ days; 3hr cadence operationalized

My duty-cycle shape `52 */3 * * *` (3hr-interval bursty-lane Row 1) ran Day-5 through Day-7+ this window. Findings: cadence-fit-to-Architect-lane confirmed (synthesis work is bursty by nature — 3hr is too tight for some, too loose for none; no actual under-coverage observed); STOP-leaves-armed convention proved through 6 overnight transitions; cron-loss incidents traced to Gap-C dormancy (above), not the shape itself. The single Day-7 finding worth flagging to cohort: **continuous shapes (PA's 30min Row 2 etc.) have different overnight-WATCH branches than bursty shapes**; the v1.5 skill carries that explicitly now (overnight window guard checked FIRST in the dispatcher).

### Arc 6 — Conservative-bar Proven-gating reached 5 catalog entries

m-30 / m-40 / m-41 / m-42 + the ship-routine-keep-loop corollary all filed under Emerging during this window with explicit cross-author cohort-uptake gates. That's a watch-pattern in its own right — when 5 entries land in 2 weeks all carrying the same gating discipline, the discipline itself is becoming cohort-canonical default. Worth a sentence in the synthesis about *what kind of catalog* we're now operating: prevention-by-naming + Emerging-at-founding + cross-author Proven-gating.

## What surfaced — cross-role + meta-shape

- **The meta-pattern "entry-catches-its-authors-at-authoring-time"** reached 2 instances this window (m-41 + m-42). Candidate for catalog entry at the 3rd instance; CIO's edit-lane. The shape itself is interesting: methodologies whose first application is to their own filing process — m-41 (mechanism-displaces-discipline) was filed *as* the mechanism that replaced the displaced discipline; m-42 (reflexive verification) was filed *from* a self-application failure in the same hour the audit landed.
- **Pattern-073 (documentation-asserted behavior drift) extended at the spec layer** — beyond the route-conventions cluster, a third sub-shape emerged: docstring-asserted behavior drift, surfaced Jun 12 morning via Lead Dev's #1193 `session_scope()` find (just outside the window but worth flagging as the Pattern-073 spec-layer evidence continues to accumulate). CIO-owned catalog edit.
- **methodology-38 (PDR/ADR Tier Separation) became operationally load-bearing** this window — PPM cited it directly in the ADR-068-only ruling; m-38 went from Emerging to actively-shaping-decisions inside 4 days. That's the fastest Emerging→reference-grade arc the catalog has tracked.
- **#1192 (BYO-key build-order) crossed Architect adjacency** — the credential-chain shape composes with ADR-066 packaging-layer abstraction (where does the key live? per-package or per-session?). Not blocking, but the BYO-context + BYO-colleague + BYO-key composition will need a coordinating framing at M4 if all three land in the same milestone.

## What's still open

- **ADR-068 (BYO-colleague Skill-Brokered Host Deputization) at M4 ratification gate** — framework + pilot pending; composition-not-greenfield converged but the implementation seam (skill brokerage + host deputization) needs the pilot data before PM ratification. ETA M4 trigger.
- **methodology-40 Proven-bar promotion gated on cross-author lift** — 2 cross-author invocations so far (Lead Dev + Exec); needs a third instance with the shape unambiguous to clear. Watch surface.
- **methodology-42 Proven-bar gated on self-catch-rate-up evidence** — if reflexive verification catches future at-authoring instances at higher rate post-naming, that's the m-29 mechanism. If not, escalate to m-36 structural guard ("claims-of-mechanism require a cited check").
- **Routines watchdog $70/mo funding decision** — PM-gated; the cure for Gap-C session-dormancy. Architecture-feasibility-fit lens: this is the right cure shape (external watchdog, OS-level, can re-launch session); $70/mo is a real cost; cohort-wide value scales with cron-shape population (currently 9+ shapes across roles).
- **Conservative-bar 6th-entry watch** — if a 6th Emerging methodology lands with the same Proven-gating discipline, that's clear cohort-canonical default and worth a meta-catalog note on the catalog's own discipline shape.

## Cross-role threads worth naming

- **Lead Dev + Architect on #1124 Phase 4 + #1158 + #1192 + #1193 (just outside window)** — the dispatcher-rail layer-then-migrate plus the credential-chain plus the silent-no-commit trap form a coherent "boundary-discipline" cluster. Lead Dev is doing most of the implementation work; Architect lens is on the layering shape across the cluster. m-40 is the connective methodology.
- **CIO + Architect on m-40 + m-41 + m-42** — three Emerging methodologies in 4 days, each cosigned across the pair, each capturing a different sub-shape of "mechanism-over-vigilance." The catalog growth itself is the cross-role thread; the *speed* of catalog growth is what's worth flagging.
- **PPM + Architect on ADR-068 + m-38 + #1166** — PPM's altitude-check + tier-separation discipline is now operating cleanly for architectural decisions; Architect provides the framework + technical-shape; PPM gates the doc-tier (PDR vs ADR vs methodology). m-38 going operationally load-bearing this window is the proof-point.
- **Exec + Architect + cohort on bursty-lane operationalization** — the 3hr shape worked in real conditions; cohort can confidently choose between bursty (3hr, Row 1) and continuous (30min, Row 2) lanes based on synthesis-vs-watch role-fit. cron-shape-experiments registry now has lived data, not just predictions.
- **HOST + Architect on signaling-channel cohort-norm codification** — HOST drafting (mail-vs-GH); Architect-adjacent on the decision-trace dimension (which surface carries the canonical decision). Not closed this window; M4-adjacent.

## For PM/Exec consideration — spine nomination for Ship #047

**Spine candidate**: *Naming what we already do — the catalog grows discipline before crisis.* Five Emerging methodologies + one operationally-load-bearing m-38 + one Pattern-073 spec-layer extension + one F4 empirical close in a single window — all carrying the same shape: identify the discipline, name it, gate Proven on cross-author lift, build the mechanism that displaces the vigilance. The cohort moved from "we keep getting bitten by X" to "X is named, mechanism is in place, watch surface defined" inside 7 days, multiple times. The methodology catalog itself is the load-bearing institutional artifact this week — not any single ADR or fix.

**Alternative spine**: *Composition-not-greenfield as the architectural posture.* If the synthesis altitude prefers a single concrete arc, the BYO-context + BYO-colleague + BYO-key composition shape is the cleanest unifier — three independent BYO-{} workstreams converging on the same architectural framing (skill brokerage + host deputization + package abstraction + key chain) without anyone having coordinated it.

I lean toward the first; the second is the easier read for an external audience. PM/Exec call which altitude serves Ship #047.

— Architect, 2026-06-12 ~07:00 PT
