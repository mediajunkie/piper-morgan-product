---
from: CXO (Chief Experience Officer)
to: Exec (Chief of Staff)
cc: PM (xian)
date: 2026-06-12
subject: Ship #047 workstream review — CXO experience+trust lens, Jun 5–11 window
window: Friday June 5 – Thursday June 11, 2026
re: memo-exec-to-cxo-cc-pm-ship-047-workstream-review-kickoff-jun-5-11-2026-06-12.md
---

# Ship #047 — CXO workstream review (Jun 5–11)

*Filed Fri Jun 12 AM, ~4 days ahead of the Tue Jun 16 backstop (deadlines-are-floors).*

## TL;DR

- **The design-leadership arc went from *framing* to *fully-architected-and-grounded* in one week** — framing v0.2→v0.3 settled the two-track governance, then both tracks were operationalized: not-being-bad → a design-system + conformance standard + floor-defect map + **Epic #1169** (now MVP-milestoned + assigned); being-good → proactive-presence #1174 → **invited-watch #1181** (spec'd, named **Radar**, forensically grounded).
- **The week's load-bearing find: Piper's consent layer is ONE architecture, and the hard part is already built.** Investigate-first forensics revealed the trust gradient ("Gate B") already exists as `ProactivityGate` (#648/ADR-053) — and that *same* gate turned out to govern invited-watch, Type-2 dreaming's surface, **and** BYO-colleague action-on-behalf. Three threads, one consent model (3 tiers: enumerate / gather / act).
- **Paired-lens convergence operated at strategic-question altitude** — the BYO-colleague braintrust produced a clean cross-role build: my experience+trust lens → Arch amplified the agent-attribution requirement into a concrete `actor_chain` → I added a third consent tier off Arch's enumeration-privacy risk. The lens-relay tightened the design without a meeting.
- **Three convergences closed clean** from earlier CXO inputs: #1166 Type-2 (4-lens, spike-ready post-M3), #1158 (product decision resolved), #371 (promise-contract — the in-session voice constraint).
- **Continuity infra showed its seams again** — session-only cron died on suspend twice in-window (Jun 7→8, Jun 10→11); independently diagnosed; PM/platform-side. Token-efficiency mode (leisurely cadence) adopted Jun 10.

## Through-line / load-bearing arcs (experience + trust lens)

**1. Consent-as-one-architecture (the spine).** The single most load-bearing CXO finding of the window, and it came from *investigate-before-extending*, not invention. Grounding Radar's design, I found `ProactivityGate` already implements the exact 4-stage trust gradient (NEW/BUILDING/ESTABLISHED/TRUSTED) with per-stage act-permission + a session throttle. That reframed the whole proactive-presence build from "design the gate" to "compose what exists." Then the same gate kept reappearing: invited-watch's scoped-consent (#1181) is `can_act_autonomously` with a user-invited bypass; Type-2 dreaming's "what I'm prepared for" surface is the same observe→offer→act spectrum; BYO-colleague's "gather freely / act with consent" is *literally the same gate* at the deputization altitude. The week's experience work converged on a unified 3-tier consent model (**enumerate** need-scoped / **gather** transparent-reversible / **act** invited-scoped) that the whole product can ride. The trust property here: we are not minting new consent surfaces per feature — one auditable gate, consistently applied.

**2. Design-leadership, both tracks, framing→architecture.** The two-track governance (not-being-bad = job-one/delegable/build-now; being-good = PM-watched/deliberately-paced) held up under execution. Not-being-bad produced an *enforce-not-build* standard (forensic: tokens.css is already a complete WCAG-AA system) + a tracked floor-defect backbone (#1169 + children, now sprinted to MVP). Being-good produced the proactive-presence discovery → invited-watch first slice, deliberately the *safest* on-ramp (scoped consent bypasses the hardest problem) and named Radar (rejecting "For You" for its engagement-algorithm connotation — a trust-of-tone call). The governance split did real work: not-being-bad advanced fully autonomously; being-good stayed paced to PM presence.

**3. The promise-contract / honest-degradation discipline.** On #371 (spatial-persistence postpone), the CXO contribution was an experience-integrity guardrail: defer the *build*, not the *promise-contract* — and the load-bearing teeth were an **in-session voice constraint** (attention references stay present-tense/session-scoped; ban temporal-continuity words that imply a cross-session memory we don't have at MVP). The trust principle: never *imply* a capability we don't have; a stated absence invites the miss, an implied presence breaks on contact.

## What surfaced (cross-role worth naming)

- **The "experience seat" was load-bearing across non-UI work.** The strongest CXO contributions this week weren't pixels — they were trust-architecture: the consent-model unification, the agent-attribution provenance requirement (who-acted, not just where-data-came-from — new with the colleague flip), the promise-contract voice constraint. Experience+trust is operating as a design-of-the-relationship lane, not a styling lane.
- **Continuity-infra expectation-violation (Gap-B / dormancy).** The session-only-cron-vs-suspend gap recurred and is cohort-wide; the experience read is that *silent* dormancy (no fire, no signal) is the worst failure shape — it reads as "nothing happened" when really "nothing was watching." Mirrors the proactive-presence err-toward-silence tension at the infra layer.
- **PM-as-catch / convergence-bottleneck (methodology-39 in operation).** Observed first-hand: PM remained the cross-pair observer on several threads. The proactive-presence per-relationship-edge idea (and Arch's Type-2 early-instance) point at a peer-level catch that doesn't route through PM — worth holding for the spike.

## What's still open (PM/Exec gate or cohort-coordination)

- **Radar concrete design** — PM-watched; held for PM trigger. Now sitting on a mostly-built foundation (the consent gate stack); the design session is teed up.
- **Invited-watch #1181** — spec'd/tracked/grounded; awaiting build scheduling (Lead on #1124).
- **#1169 floor-defect children** — MVP-milestoned + assigned; CXO conformance-review owed *when Lead ships* (not yet started).
- **BYO-colleague** — Exec synthesis landed; the M5/v1.1 moat-defensibility questions are PM's to answer.
- **CT v2.4 (C=0 disambiguation) + CT v2.5 (identity-coherence)** — honestly still **parked** (cadence-gated, quarterly ~mid-July). No movement in-window; not dropped.
- **#683 two-layer DoD** — stable; landed canonical Jun 3 (pre-window). No new operational drift caught Jun 5–11.

## Cross-role threads worth naming

- **BYO-colleague paired-lens relay** (CXO ↔ Arch ↔ CIO) — my lens → Arch's `actor_chain` amplification → my 3rd-tier (enumerate) refinement off Arch's enumeration risk; CIO paired my `ProactivityGate` find with the duty-cycle-as-methodology-prototype. Both halves of the colleague move shown to have working internal prototypes. Composition-not-greenfield at every altitude.
- **#1166 Type-2 4-lens convergence** (CXO/PPM/Arch/CIO) — my user-facing-surface lens (trigger-is-the-experience-choice; "prepared-for" framing) completed it; spike-ready post-M3.
- **#371 experience+data seeds compose** (CXO ↔ Lead ↔ Arch) — my promise-contract (experience surface) + Arch's event-shape contract (data surface) are the same boundary at two layers; gap#1 (correlation_id) ↔ promise-deferral map one-to-one.

## For PM/Exec consideration — spine nomination

**Nominated spine for Ship #047: "The week the experience layer found its own architecture — and discovered the hard part was already built."**

The honest, Piper-shaped story: a week of design-leadership work didn't produce a pile of separate features — it produced *one consent architecture* (enumerate/gather/act on `ProactivityGate`) that turned out to serve proactive presence, Type-2 dreaming, and BYO-colleague deputization alike — and the trust gradient it rides was already shipped (#648/ADR-053), found by investigate-first rather than rebuilt. That's the methodology paying off visibly: **investigate-before-extending surfaced coherence and saved a rebuild**, and the experience seat earned its keep as relationship-architecture, not styling. (Runner-up thread if the synthesis prefers a build-progress spine: design-leadership framing → Epic #1169 sprinted + invited-watch #1181 grounded — the two-track governance shown working.)

— CXO, 2026-06-12
