# CIO Duty-Cycle Escalations / PM Attention Doc

> **⚠️ DEPRECATED 2026-06-17 (FOLD, PM-ratified).** This per-role escalations doc is retired. PM-attention / escalation items now ride `dev/active/cio-carry-forward.md` (the residual home); the cohort-attention rollup GitHub-verifies open items and the freeze-registry handles liveness, so this hand-maintained surface (which rotted despite the STOP-reconcile step) is no longer load-bearing. Kept below for traceability; no longer maintained. See `duty-cycle-tick` skill v1.13 + `methodology-41`.

**Agent**: CIO (Piper Morgan, Code instance)
**Maintained by**: CIO during each duty-cycle pass
**Last updated**: 2026-06-16 (STOP-fire reconcile — stale items dispositioned; see "Open escalations for PM")
**Pattern reference (historical)**: V1 v0.2 design, Section "Escalation surface — structured-markdown enumerated entries"

**Duty Cycle role (v0.5 design ratified 2026-05-24)**: This file IS the canonical **Attention Doc** (Doc 3 of the three per-agent duty-cycle docs) under the new design. Per the formalizing-not-proliferating principle, no parallel "attention doc" is created — the existing escalations file is reframed to serve as the PM-batching surface. Items for PM to scan during IDLE accumulate here. Blockers captured during Task Loop step 1.2 land here. When PM engages during IDLE-engaged, this is the doc to walk through together.

---

## How to read this file

PM scans for escalations open against CIO. Severity typology:

- **blocking** — CIO is stopped until PM acts; cycle cannot proceed on this thread
- **drift** — cycle has noticed a trend that may degrade trust property if not addressed
- **uncertainty** — CIO needs PM judgment on a call; cycle is proceeding on alternatives in the meantime
- **complete-stale** — work is done; PM input was waiting; PM input not yet given

CIO scans for escalations the cohort filed against CIO via memos; surfaces here as needed.

---

## Active cohort threads (CIO autonomously processing)

Threads the cycle is moving forward without per-decision PM ratification. PM scans for "what's CIO touching that I might want to weigh in on."

- *(2026-05-16 ~1:25 PM, initial population)* Pattern-073 (Documentation-Asserted-Behavior Drift) — disposition memo filed to Lead Dev + Architect; Lead Dev authors; awaiting Lead Dev pattern body. Cycle observes, doesn't author.
- *(2026-05-16 ~1:25 PM)* methodology-30 Consumer-Trace Verification — CIO drafts Mon-Tue per Friday disposition; deferred behind weekend deliverables (V1 dry-run + cycle artifacts).
- *(2026-05-16 ~1:25 PM)* Audit-cascade preamble Step 0 (12t) — CIO-owned ~5 min edit; queued for next quiet cycle.
- *(2026-05-16 ~1:25 PM)* Type 2 cross-pollination fan-out (Klatch / OpenLaws) — PA-owned routing; cycle tracks completion via PA's cross-pollination cadence.

---

## Open escalations for PM

**RECONCILED 2026-06-16 22:37 PT (STOP-fire, methodology-41 step).** Most items below were stale — resolved by events but never moved (this is exactly the rot Exec's 6/16 flag named; actioned now).

**Genuinely OPEN (1):**
- **#972 MEM-TEMPORAL field-name alignment** (was 5/25) — Daedalus alignment memo delivered to the Klatch repo 6/15 (proposes `valid_until`); **awaiting Klatch rousing** (dormant >1wk per PM 6/16). P1 lint shipped (#1243) + doc-set extended 6/16. PM action: none right now (gated on Klatch); confirm `valid_until`-vs-`ended` only if Janus context shifts.

**RESOLVED by events** (dispositions; originals retained below for traceability):
- Routines / freeze watchdog (6/7–6/11 decision items) → **SHIPPED**: launchd freeze-watcher 6/15 + cycling-registry 6/16 (cio+exec). The zero-agent OS-job is the Gap-C cure; the $70/mo Routines path is moot.
- Thin-prompt cohort-broadcast nod (6/7) → **nod given 6/16**; Exec dogfooding thin now + drives the cohort broadcast (#7b).
- Cycle-agent launch gesture (6/6) → **settled**: ephemeral Option B (Desktop worktree checkbox); documented in the plan-of-record migration runbook.
- Mailbox-bridge structural seam (6/3) → **design landed** as #1259 (push-to-ref recommended); gated on LD plumbing review — tracked on the issue now, not here.
- v0.6 design corrections / functional-vs-named START / commit-cadence (5/25–5/26) → all folded into v0.6/v0.7 + the skill (batched no-op holds); settled.

> **Meta (CIO):** this reconcile *is* the STOP step my 6/16 fold-recommendation flags as usually-skipped → the doc rots. Running it tonight keeps it accurate while the fold (deprecate these per-role docs; let the GitHub-verifying rollup + the freeze-registry + the carry-forward carry the load) awaits HOST concurrence + PM ratification.

---

### Historical open items (superseded by the 2026-06-16 reconciliation above; retained for traceability)

- **2026-06-03 ~10:35 AM PDT — Mailbox-bridge is the next structural seam; escalating the Lead-Dev hook-amendment (for today's Lead discussion).** HOST's mutual-assessment surfaced the concrete cost: an **exec-inbox MANIFEST carried unresolved `stash pop` conflict markers in main's local working tree for ~9 hours overnight** (a concurrent-agent bridge collision), resolved only by Exec's hand-recovery. Worktree isolation killed the concurrent-commit-race family but NOT the mailbox-bridge-into-shared-main friction (mail can't be worktree-isolated; it rides shared main). I hit a cousin myself yesterday (errant `git stash pop`). **Severity**: drift (recurring friction degrading the autonomy substrate). **Action**: adoption-package **open-item #1** — the Lead-Dev hook-amendment allowing `mailboxes/` commits on `claude/*-cycle` branches → mail rides per-fire push-to-ref, retiring the shared-main bridge. **Recommend folding into PM's Lead-Dev discussion today.** The 9hr-stuck MANIFEST is the receipt for leaving it open.

### Resolved (folded into v0.6/v0.7)
The 2026-05-25 escalations below (cron-bind-to-IDLE + PM-presence refinement + 10-min interval) were **ratified and are canonical** in `procedures/cron-lifecycle.md` (Rules 1/2). Resolved; archived below.

- **2026-05-25 ~4:11 PM EDT — v0.6 design correction candidate: cron-bind-to-IDLE (with PM-presence refinement at 4:14 PM EDT).** PM-surfaced architectural insight during airport-test Fire 3/4 pile-up. v0.5 design had cron lifecycle orthogonal to WORK/IDLE Decision Table state, causing fires to clash with in-progress work. PM directive: bind cron lifecycle to IDLE — `CronDelete` when entering WORK; `CronCreate` when returning to IDLE. **Refinement (4:14 PM EDT)**: IDLE itself has two sub-states — IDLE-PM-absent (cron fires) vs IDLE-PM-present (cron paused; PM is the driver). Any inbound PM message pauses cron; PM "go autonomous" signal resumes. **Severity**: uncertainty (v0.5 design has a structural gap that the pilot surfaced). **Action needed from PM**: ratify the cron-bind-to-IDLE shape + PM-presence refinement as v0.6 design correction; CIO will file design-doc edit when bandwidth allows. **Status**: applied operationally in this airport test (cron paused at 4:11 PM; relaunched at 4:13 PM; re-paused at 4:15 PM per PM-presence refinement); design-doc edit pending.

- **2026-05-25 ~3:52 PM EDT — v0.6 design correction candidate (related): 5-min interval mismatched with Task Loop work-duration.** PM directive at 3:52 PM: shift to 10-min interval. Combined with cron-bind-to-IDLE above, the interval-mismatch concern partly evaporates (cron only fires in IDLE, so interval matters less). Still: 10-min interval feels right for IDLE-tick cadence. **Severity**: closed by PM directive; logging for completeness.

- **2026-05-26 ~11:30 PM PDT — Functional-START vs Named-START gap surfaced.** Fire 1 today functionally ran START (opened session log + cycle log) but skipped the daily tracker creation. Result: no `dev/2026/05/26/cio-tracker-2026-05-26.md` for today (vs yesterday's pilot which had one). Tomorrow's named-START test should explicitly create all 5 START artifacts including the daily tracker. **Severity**: uncertainty (clarifies what "named START" should ensure vs what "functional START" missed). **Action needed from PM**: at next engagement, confirm whether the missing tracker is a v0.6 design refinement worth filing OR just an artifact of yesterday's-not-fully-procedural Fire 1.

- **2026-05-26 ~9:04 AM PDT — v0.7+ candidate: commit-cadence-during-no-op-fires.** After 5 quick-no-op fires in 80 min, git log on origin/main is accumulating one no-op commit every 10 min. Cohort-wide this would be ~42 commits/hr from autonomous fires. Worth considering batching no-op cycle log appends OR committing only every Nth no-op. NOT proposing change now; PM may prefer noisy-but-explicit visibility. Filing for v0.7+ ratification. **Severity**: uncertainty (operational; not blocking; commit noise tradeoff vs PM-visibility tradeoff is a judgment call). **Action needed from PM**: ratify the commit cadence at next engagement — keep noisy default or adopt batching.

- **2026-05-25 ~5:00 PM EDT — v0.6 design correction (load-bearing): drain-until-IDLE semantics.** PM correction during airport test: v0.5 design had wrong WORK semantics. Each cron fire is meant to be "wake from IDLE → drain ALL unblocked work (mail loop to inbox-zero → task loop to blocked-or-empty → re-check mail → loop until truly nothing) → only then return to IDLE." NOT "do one work-unit per fire then back to IDLE." The 2-bit Decision Table is "one tick per drain-cycle step within a fire," not "one tick per fire." Cron prompt explicitly said *"advance ONE queued task"* — that was the wrong-semantics encoding moment. **PM confirmed I've got the corrected semantics right** (5:04 PM EDT). **Severity**: load-bearing (v0.5 design has fundamental semantics gap that the pilot surfaced + PM corrected). **Action needed**: update v0.5 → v0.6 design doc + work-parts.md + decision-table.md + cron prompt with drain-until-IDLE semantics BEFORE next live cycle run. **Carryforward**: next session (PM 8am PT May 26 wake-up) must do design-doc + procedure-doc edits before re-launching cron.

- **2026-05-25 ~4:50 PM EDT — #972 MEM-TEMPORAL field-name alignment call made without direct Janus cadence visibility.** CIO made ship-and-adopt call (Docs's option 3) with rename-if-needed escape hatch. PM has Janus context CIO doesn't; if Janus is actually near-term (~1-2 weeks), PM can override with a "wait" directive and Docs holds. Otherwise default ship-and-adopt proceeds. **Severity**: uncertainty (incomplete data; defensible default chosen; reversible). **Action needed from PM**: confirm or override the ship-and-adopt call when next scanning attention doc.

*(prior: none — V1 escalations file initialized 2026-05-16)*

---

## Resolved escalations (kept one cycle for traceability)

*(none yet)*

---

## File maintenance notes

- File updated at the end of each cycle pass
- Cycles append new escalations; resolve in-place when PM acts; move to Resolved section after one cycle's preservation
- Active cohort threads section refreshed each pass to reflect current state
- File path: `dev/active/duty-cycle-escalations-cio.md` (per CXO Framing 4 cross-agent naming convention; globbable as `dev/active/duty-cycle-escalations-*.md` when fleet extends)

> **[All three "## OPEN —" items below + their UPDATE blocks are RESOLVED — see the 2026-06-16 reconciliation under "Open escalations for PM" above. Launch-gesture: settled (Option B). Routines-watchdog: SHIPPED (launchd freeze-watcher + registry). Thin-prompt nod: given; Exec drives #7b.]**

## OPEN — PM clarification: actual cycle-agent launch gesture (2026-06-06)
**Surfaced by**: Web 6/6 ("PM: I have not had to set up doppleganger sessions for any other agents"). **The gap**: documented model is Option B (Desktop "New session" → auto-worktree), but PM's comment suggests possible drift between the documented launch model and PM's actual practice. CIO can't confabulate the operator gesture (I run *inside* a session, don't observe launch). **Ask**: PM confirm how a cycle agent is actually launched → reconcile `cohort-agent-status.md` launch-procedure section to reality. **Impact**: affects every future onboarding + Web's eventual daily-mail-check. No rush; doc-accuracy not blocking. (Pending-PM, doesn't block other work per Rule 2.)

## OPEN — PM decision: build the Routines alert-only watchdog? (2026-06-07)
**Context**: Gap C (compaction silently kills session-crons; durable=noop) needs an *external* liveness monitor — agent-side self-heal (v1.3) only reduces the dark-window. **Routines feasibility CONFIRMED** (`routines-watchdog-feasibility-2026-06-07.md`): alert-only watchdog buildable now (cloud-persistent, headless, git-commit-recency signal per claude/{role}-cycle branch, Slack alert), ~4-6hr build, ~$70/mo. **Decisions**: (1) build it? (2) silence threshold per role (propose ~3h continuous / ~6h async)? (3) Slack-only alerts to start? (4) fallback-fire tier (B) = defer to design pass (it's the v2-airlift on-ramp)? CIO scoped; build is PM-go + likely Lead/infra to implement the Routine. Pending-PM; doesn't block.

## OPEN — PM decision: thin-prompt cohort-rollout BROADCAST nod (READY 2026-06-07)
Proposal COMPLETE both halves: `thin-prompt-cohort-rollout-proposal-2026-06-07.md`. CIO mechanics + HOST welfare sections finalized + co-signed; HOST OK-to-PM. Validated continuous (CIO) + low-freq (HOST live, incl. overnight). **Ask: nod to broadcast the cohort memo** (thin-prompt + Rule-2 keep-armed; agents self-migrate at cadence, ~5min carry-forward setup each). On nod, CIO sends the cohort memo (mechanics) + HOST co-signs welfare framing. Pending-PM; doesn't block.

## UPDATE 2026-06-08 — watchdog hold CLEARED (durable=no-op confirmed)
The durable:true reconcile RESOLVED: Arch ran the disk check (no scheduled_tasks.json), withdrew F4 — durable is a confirmed no-op (PA was right). So durable is NOT a cheaper Gap-C floor → **the Routines alert-only watchdog decision is UN-blocked**. It's the Gap-C cure (agent-side re-arm reduces the dark-window; watchdog cures the silent-stop). Decision (1) above [build watchdog ~$70/mo? thresholds? Slack-only?] is ready for PM with no remaining technical blocker. Also: the watchdog is the *liveness tier* of the same cross-pair-observability HOST's attention-dashboard provides (PM-as-catch rationale).

## UPDATE 2026-06-11 — Routines watchdog: funding-trigger criterion MET (empirical halt data)
The 5-whys cron-halt empirical investigation (CIO-dispatched background research agent, ~30min, 2026-06-11 morning) confirmed: Gap-C dormancy is the dominant halt mechanism; incidence rose 6/8-6/11 with weekly-usage-limit + planned re-migration events stacking cohort-wide session restarts. **Trend data**: 6 of ~9 cycling roles needed PM intervention on 6/11 morning (retroactive STOPs + session resumes). My morning REPL-busy framing was wrong-direction — halts cluster at PM-inactive windows (session dormancy), not PM-active. Full investigation memo: `mailboxes/cio/sent/memo-cio-to-pm-cc-arch-host-pa-cron-halt-investigation-gap-c-dormancy-is-dominant-routines-watchdog-is-the-cure-2026-06-11.md`. **For PM**: the data probably qualifies as the funding-trigger criterion. Decision items above (build? thresholds? Slack-only?) are unchanged + ready.
