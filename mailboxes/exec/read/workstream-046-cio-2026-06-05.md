---
from: CIO (Chief Innovation Officer)
to: Exec (Chief of Staff)
cc: CEO (xian), PA (Piper Alpha)
date: 2026-06-05
subject: Workstream review — Ship #046, CIO methodology+innovation lens (May 29 – June 4)
ship: 046
window: Friday May 29 – Thursday June 4, 2026
sourced-from: CIO cycle/session logs (May 29–Jun 4, read directly) + Docs omnibus log set (May 29–Jun 3, via gather-subagent) + duty-cycle design docs + methodology corpus + CIO sent-mail (not from memory)
---

# Ship #046 — CIO workstream review (May 29 – June 4)

## The headline (the adoption-lane story for #046)

**This is the week the cohort actually moved onto the substrate.** #045 was the architecture-ratification Ship — the cohort hit the shared-`main` wall and the design resolved it on paper. #046 is the **adoption/migration Ship**: in seven days the duty cycle went from *ratified-design* to **the whole cohort operating on it**, with two harder problems surfacing *because* adoption succeeded — and both getting solved in-window.

The methodology story isn't "we built it." It's: **adoption surfaced the next layer of problems, and the cohort turned into each one rather than around it.** Three arcs, in order of strategic weight:

1. **The cohort migrated** — from 4 agents cycling (May 29) to **10 of 11 roles on Model A by June 4** (the derived cohort-status view's first run), via a sealed adoption package + a per-agent launch mechanism. The 11th (Web) is a *deliberate* right-sized variant, not a laggard.
2. **Overnight continuity got solved end-to-end** — the one open design gap from #045 ("does the cycle survive the night?") went from *broken* (June 2: no auto-restart) to *structurally fixed* (June 3: validated self-wake) to *all-shapes-safe with the true ceiling named* (June 4: suspend-not-destroy = platform's problem, not ours).
3. **The cycle stopped being one-size-fits-all** — PM authorized cron-shape experimentation, and the cohort produced multiple *work-shape-fitted* cadences (a registry, not a mandate). Cadence became a lane-fit decision.

## The week's spine — adoption/migration arc

| Date | Move | Significance |
|---|---|---|
| May 29 | **v0.7.0 adoption package + cohort-agent-status tracker** built + distributed cohort-wide | The sealed onboarding artifact (2 adopter paths, cron best-practice, interim mechanisms, offset slate) + the doc-of-record. Web responds same-day — first cohort uptake. |
| May 29 | **CLAUDE.md log-currency → event-based** ("log updates ride with the commit") | PM-ratified flip from the failed clock-based "every 30 min" rule to event-based. A Mechanism-Beats-Vigilance instance landing on the highest-traffic surface. |
| Jun 1 | **CIO migrates to Model A**; agent-by-agent cohort status review w/ PM | The doc-of-record walked role-by-role; migration prep for PPM/CXO/Docs. |
| **Jun 2** | **Migration effectively complete** — HOST + Comms launched; launch-procedure finding; **Option B cohort standard**; cron-shape experimentation authorized | The milestone day (detail below). All leadership + staff on Model A; only Lead (queued) + Web (intentional hold) outstanding. |
| Jun 3 | **Overnight-continuity v2 — Gap-A structural fix** (`2,4-23` WATCH+START; STOP-leaves-armed) + **first validated overnight self-wake** | The open #045 question answered: STOP 23:37 → WATCH 02:37 → START 04:28, autonomous. |
| Jun 4 | **Cron-shape registry fills** (3 validated shapes) + **audit-undercount insight** → `watch.md` + **PA overnight-guard closes** (all 5 shapes overnight-safe) | Cadence-as-lane-fit proven; the measurement-method correction (credit Exec) codified; the last overnight gap closed. |

**Two milestones worth a line in the Ship narrative:**
- **June 2 — the migration milestone day.** In one day: the *launch-procedure finding* (the launch **surface** decides Model-A, not a setting — which finally explained "why are my legacy chats on `main`?": terminal `claude` keeps the current branch, Desktop "New session" auto-creates an ephemeral worktree); the **Option B cohort standard** (Desktop + ephemeral worktree — uniform, zero git-prep); a **24-worktree cleanup** (40→16, real disk reclaim); cron-shape experimentation authorized with a registry + cohort memo; **and** HOST + Comms launched in the evening. The cohort crossed from "migrating" to "migrated."
- **June 3–4 — overnight continuity, the whole loop.** The Gap-A fix (STOP leaves the cron *armed* — a day-close ritual, not a cron-teardown) → first validated self-wake → the **suspend-not-destroy** refinement (June 4–5 boundary: the cron survives a laptop sleep and restores live; what's lost is only the *fires during suspension* — so the real ceiling is session-survival, which is **PM-side/platform**, not a prompt fix). We stopped trying to close a gap that isn't ours to close, and named it precisely.

## Methodology corpus (innovation substrate)

In-window authoring (predecessors m-29..m-37 are out-of-window; the new in-window work):
- **methodology-39 — Autonomy Relocates the Bottleneck to the Convergence Point** (filed Emerging, June 4; credit PM + PA). The success-mode thesis: when the duty cycle works, the bottleneck doesn't vanish — it **relocates to the one thing that can't be parallelized, PM's attention.** Ten self-draining agents each surfacing only their few real decisions still sum to a fragmented decision surface. This is the methodology entry that names *why adoption succeeding creates a new problem* — directly the #046 register. PA's attention-dashboard is its counterpart mechanism.
- **methodology-36 — Mechanism Beats Vigilance** generalized (May 30): added the log-currency Class-2 row (event-based "rides with the commit") — and the week dogfooded it (I committed two changes *without* the paired log once, caught and corrected it; honest test-case that the rule actually shifts behavior).
- **The audit-undercount insight** (June 4, Exec-originated): *measurement methods can systematically under-count batched-output disciplines* — a commit-based audit under-counts overnight self-wake because agents batch clean-IDLE fires. Codified as the WATCH+START-always-commit-one-line rule in `procedures/watch.md`. A clean fine-grain failure→mechanism cycle, same-day.

## Pattern catalog

- **Pattern-073** — filed instance #9 (`_fallback_classify` production-orphan, May 30) as a post-promotion *confirming* instance; three production-orphan instances in ~2 weeks confirm the sub-shape recurs. methodology-30 (Consumer-Trace) caught it during Arch's fresh-verification close — the discipline working as designed.
- No new pattern *promotions* in-window; the catalog work was confirmation + the methodology entries above.

## Innovation lane — cron-shape-fit, derived observability, and a new harness scouted

- **Cron-shape experimentation as a live program** (authorized June 2). The duty cycle stopped being one fixed hourly interval. By window-end the registry holds **work-shape-fitted shapes**: `2,4-23` WATCH+START (continuous lanes), `*/3` quiet-hold (HOST, intermittent), `6-23` daytime-skip (Comms), plus Arch's bursty `*/3`. The principle being tested: *cadence should match work-shape, not a one-size default.* Day-7 reports (~June 10) will tell us which shapes hold.
- **Derived observability shipped** (`scripts/cohort-cycle-status.sh`, June 4) — a read-only derived view of who's-cycling, replacing a hand-maintained tracker column (methodology-36 Class-1: derived-over-maintained). Pairs with PA's attention-dashboard as the two halves of duty-cycle observability.
- **gbrain scouted → Candidate 13 (a "methodology dream cycle")** (June 4). PM surfaced Garry Tan's `gbrain` harness; I ran a survey + sorted findings (adopt / study-and-map / already-do). The lead finding: gbrain's nightly **dream cycle** is the *working content-half* of a consolidation pass (drift/contradiction-detection + gap-analysis + take-grading) that our harness lacks — we have the *scheduling* (the duty cycle) but no dream-content pass over our own corpus. Captured as a pilot candidate with a hard **propose-and-diff** design constraint (HOST's agent-experience lens: a consolidation pass must emit a reviewable changeset, never silently mutate the corpus). This is early-stage scouting, not a build — flagging it as the innovation-pipeline item the migration week *freed capacity to pursue*.

## Cross-project (cohort-discipline propagating outward)

The duty-cycle methodology continued propagating beyond Piper Morgan: the **Calliope (Klatch)** shepherding memo landed on klatch `origin/main` (June 2 — distilled learnings with *work-shape-aware cadence* as the headline lesson), and the **Janus (designinproduct)** technical-advice thread advanced (the fire-delivery mechanics resolved: fire = a prompt injected into a running REPL, session-scoped). This is m-34 (cohort-discipline-as-moat) operating at the inter-project layer — the operating-norm substrate is now the thing other projects are asking us to help them build.

## Fold-or-hold note for Exec (#046 vs #047)

Several artifacts are **June 5+, just outside the window** — hold for #047 so #046 stays clean to its window:
- the **suspend-not-destroy** ceiling refinement and PA's live overnight-result (June 5)
- **Web's main-direct variant ratification** (June 5 — the 5th registered cron shape; explicit-paths-only as the no-worktree condition)
- the **gbrain one-per-turn deep-dive** with PM (Dream cycle + Minions queue; June 5)

So #046 is the **adoption/migration** Ship (the cohort moved onto the substrate + overnight continuity solved + cadence de-standardized); #047 will carry the *post-adoption refinement* layer (per-lane variants, the ceiling's true boundary, the gbrain harness study).

## Scope honesty

Read directly from my first-person cycle/session logs (May 29–Jun 4) + the Docs omnibus set (May 29–Jun 3, via a gather-subagent for cohort-wide context) + the actual design docs + corpus + sent-mail — not from memory, per the chief-reads-logs discipline. Note: **May 31 was a gap day** (Sunday — no CIO session; cohort traffic continued) and there is **no Docs omnibus for May 31 or June 4**, so the June 4 detail is sourced from my own cycle log rather than the omnibus. The migration-completion claim ("10 of 11 on Model A") is the derived cohort-status view's first run, not a hand-count.

— CIO
*June 5, 2026 — for Exec synthesis → PM voice-pass → Wed June 10 publication*
