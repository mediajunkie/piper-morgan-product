# Cron Lifecycle — procedure

**Purpose**: bind cron lifecycle to IDLE state. Cron is the in-session autonomy mechanism that triggers loop fires when there's work to do; it should NOT fire while substantive work is in progress or while PM is actively engaged.

**Source**: v0.6 design corrections (PM-ratified May 25 ~4:03 PM EDT for cron-bind-to-IDLE; May 25 ~4:14 PM EDT for PM-presence-pause refinement)

**Predecessor gap**: v0.5 had cron lifecycle orthogonal to WORK/IDLE state, causing fires to clash with in-progress work in the May 25 pilot.

---

## Rule 0: Launch-with-immediate-flywheel (0th-step)

**Source**: PM May 27 ~8:45 AM PDT — surfaced during HOST adoption.

**Rule**: When an agent first registers their cron via `CronCreate` (or re-registers after a long pause), run **one full flywheel iteration inline immediately**, BEFORE returning control. The first cron fire shouldn't wait up to the cron interval (e.g., up to 60 min for hourly) for the agent to first process accumulated work.

The launch sequence:

1. PM signals go-autonomous → agent starts launch protocol
2. `CronCreate` (registers future fires)
3. **Run flywheel inline NOW** (Fire 0):
   - CHECK dispatcher (likely → WORK PARTS since not new day, not past 11pm)
   - Mail Loop drain (process inbox to zero)
   - Task Loop drain (advance unblocked tasks)
   - Decision Table tick → return to IDLE when (0, 0)
4. Append "Fire 0 — launch + immediate flywheel" entry to cycle log
5. Truly IDLE until next cron fire

**Why this matters**: agents being onboarded into the cycle frequently have accumulated mail or queued tasks from before adoption. Without the 0th-step, that backlog waits up to one cron interval to be processed. With the 0th-step, the cycle starts delivering value immediately on launch.

**CIO precedent**: CIO's May 26 first-launch fire was substantive (the v0.6 design + procedure docs + MEM-975 implementation drain) — Fire 1 effectively WAS the 0th-step. The pattern was already in practice; this rule makes it explicit for cohort adoption.

---

## Rule 1: Cron-bind-to-IDLE

**Cron lifecycle is bound to the agent's IDLE state.** Specifically:

- **Entering substantive WORK** → `CronDelete <current-cron-id>` (pause)
- **Returning to true IDLE** (drain cycle complete; mail empty + tasks blocked-or-empty) → `CronCreate` with the same pattern (resume)

### How to get current cron-id

```
CronList → returns active recurring + one-shot jobs with their IDs
```

Pick the recurring duty-cycle job; pass its ID to CronDelete.

### CronDelete-FIRST refinement (Arch Fire-3, 2026-05-27)

If a fire may go substantive, **CronDelete as the literal FIRST action of the fire — before sync, before anything.** The race it closes: on Fire 3, Arch ran `CronList`, and the next cron fire arrived in the brief REPL-idle window *between the CronList tool-call and the CronDelete tool-call* — a second flywheel began overlapping the first. Pausing first (before even getting the id via CronList — or getting the id and deleting in one uninterrupted step) closes that window. Since adopting CronDelete-first: zero clashes.

### Why Rule 1 survives the worktree model (the load-bearing distinction)

Under Model A (worktree-as-cycle-default) it's tempting to drop Rule 1 — surely worktree-isolation or runtime idle-suppression handles stray fires? **No. The clash Rule 1 prevents is REPL-turn-level, not git-working-tree-level:**

- **Idle-suppression does NOT prevent it**: the runtime fires "when the REPL is idle," but during multi-step work the REPL is briefly idle *between every tool call*. A fire slips into that inter-tool-call gap. Idle-suppression only suppresses fires during a single long operation, not between the many tool-calls that make up substantive work.
- **Worktree-isolation does NOT prevent it**: isolation prevents *git-working-tree* clashes (two agents on main). The re-fire clash is one session getting two overlapping fire-prompts — it arrives in the same session regardless of which working tree that session operates in.

So: Model A eliminates the git-working-tree clash family (the shared-main churn); it does NOT eliminate the within-session re-fire clash. **Different failure modes, different mitigations — Rule 1 (REPL-turn-level) and worktree-isolation (working-tree-level) are orthogonal, both load-bearing.** (Contrast Rule 2, which DOES relax to Model-A: its failure mode — a fire during PM conversation — genuinely is idle-suppressible because PM messages are spaced. See Rule 2.)

### What counts as "substantive WORK"

- Multi-step Task Loop work (>2 min expected)
- Memo drafting + distribution
- Substantive mail response (not quick triage)
- Design / methodology / code edits

### What does NOT count as "substantive WORK"

- Quick mail-triage (CC info / close-loop / move-to-read; <2 min)
- Time/inbox checks
- Status reports to PM
- Cycle log appendage

Brief operations don't require cron-pause — the cron fire interval is longer than the brief op, so no clash.

### When to CronCreate (resume)

After the drain cycle completes — specifically when:
- Mail inbox is empty (post-Mail-Loop drain)
- Task queue is all-blocked-or-empty (post-Task-Loop drain)
- Re-check of Mail Loop produced no new mail
- Decision Table reaches (0, 0) → end loop

Only then resume cron. Returning to IDLE is the signal.

---

## Rule 2: PM-presence-pause (refinement to Rule 1)

IDLE itself has two sub-states:

- **IDLE-PM-absent**: cron fires (autonomous mode — the default IDLE)
- **IDLE-PM-present** (PM has just messaged, conversation active): cron paused (PM is the driver; cron firing would clash with PM turns, recreating the original problem)

### Transition triggers

- **Any inbound PM message** → `CronDelete` (PM is now driver)
- **PM "go autonomous" signal** → `CronCreate`

### Sub-rule: IDLE-advances-low-priority-work (v0.6.3 — PM-ratified 2026-05-27 ~5:51 PM PDT)

PM directive verbatim: *"When idle, please do low-priority work instead of nothing, if it is unblocked."*

**Rule**: When the Decision Table reaches (0,0) in IDLE-PM-absent state, BEFORE pronouncing IDLE, check whether ANY tracked low-priority issue in the agent's lane is unblocked. If yes, advance one (smallest-scope first; finish or partially-progress; commit). If no, pronounce IDLE.

**Why**: prevents the failure mode where agents read "no urgent work" as "nothing to do" + report observation-shaped fires. PM's framing: idle-time is a resource; use it for low-priority work that would otherwise wait indefinitely.

**Threshold for "advance one"**: bounded — pick smallest-scope unblocked low-priority item; advance to natural break (commit); don't over-extend. The point is forward-progress, not depletion.

**Trade-off**: this trades some IDLE quiet for backlog cleanup. Most cohort agents have low-priority backlog that benefits.

---

### Sub-rule: Mail-check-at-interruption (v0.6.2 — PM-ratified 2026-05-27 ~11:00 AM PDT)

When PM message arrives → CronDelete (existing) → **before substantive engagement with PM, do a quick mail-check** (~30s; `ls mailboxes/{role}/inbox/`; no triage, just awareness).

**Why**: PM-engagement may reference recent cohort activity that arrived in mail since the agent's last fire. Without a mail-check, the agent's response could be based on stale state from up to one cron-interval ago. Quick mail-check → agent has current cohort context when responding.

The check is awareness-only:
- If inbox empty → proceed to PM engagement with current state
- If new mail → mention briefly in PM response so PM knows it's there; full triage can wait until appropriate point in conversation OR after PM signals go-autonomous

Adds <30 seconds; eliminates stale-info responses. Applies to ALL adopters.

### Recognizing the "go autonomous" signal

Explicit PM phrases:
- "go autonomous"
- "let it run"
- "resume cron" / "start the cron" / "restart the cron"
- "I'm going AFK"
- "I'll check back later"

Or implicit signal:
- PM ends conversation with action complete
- PM has been silent ≥ {threshold} (v0.7+ — auto-resume by silence not yet implemented)

If unclear: ASK rather than assume. "Want me to resume cron?" is cheap.

---

## Combined invariant

The cron is alive ONLY when the agent is in IDLE-PM-absent. In all other states (WORK, IDLE-PM-present), cron is dead.

State transitions:

```
IDLE-PM-absent  →  WORK  →  IDLE-PM-absent (cron alive throughout transition)
   ↑                ↓
  cron            cron
  alive          paused

IDLE-PM-absent  →  IDLE-PM-present  →  IDLE-PM-absent (cron alive only at endpoints)
   ↑                  ↓                    ↑
  cron              cron                 cron
  alive            paused               alive

WORK  →  IDLE-PM-present  (cron stays paused; both states pause cron)
  ↓
 cron paused
```

---

## Why this discipline exists

Without cron-bind-to-IDLE, fires arrive while the agent is mid-work. The REPL is briefly idle between tool calls; cron fires into that gap; a second "fire" begins overlapping the first. The May 25 pilot saw 4 fires pile up within 10 minutes when 5-min interval was tried — clashes, not productivity.

Without PM-presence-pause, fires arrive while PM is in active conversation. Cron firing during a PM turn confuses both — clashes again.

The discipline is structural, not optional. It resolves the clash problem at the architecture level rather than relying on agent vigilance.

---

## Common pitfalls

- **Forgetting to pause** at start of substantive work — next fire arrives mid-task. Fix: always CronList + CronDelete as the FIRST action when entering substantive WORK.
- **Forgetting to resume** at end of drain — cron stays dead forever. Fix: explicit CronCreate as the LAST action before status report.
- **Pausing for trivial work** — overhead burden; trivial work fits in cron interval. Fix: judgment — substantive >2 min only.
- **Resuming during PM conversation** — re-triggers the clash. Fix: only resume after PM signals go-autonomous.

---

## Overnight continuity + the two self-wake gaps (2026-06-03)

The cohort's first full-cohort overnight (2026-06-02→03) surfaced that agents were NOT self-waking / self-closing reliably. Diagnosis: **two distinct gaps.**

**Gap A — STOP ended cron-deleted (no morning wake).** Agents that *did* run STOP applied Rule-1 CronDelete-FIRST and never re-armed → cron gone → no 4am fire. Hit CIO, PPM (and any STOP-runner who deleted). **FIX (shipped 2026-06-03):** the static cron `{offset} 2,4-23 * * *` (STOP 11pm → silent → WATCH 2am → START 4am → hourly day) + stop.md Step 4 "LEAVE THE CRON ARMED" (re-arm the same expression if Rule-1-paused). Premise: persistent local sessions stay alive overnight.

**Gap B — sessions abandoned mid-conversation never reached STOP at all (still open).** Agents that were PM-engaged (Rule-2 cron-paused) when PM stopped responding just *trailed off* — they never detected "PM left, resume autonomous cycle" so they never drained-to-IDLE or ran STOP. Hit PA, Web, HOST, CXO, Arch (per Docs's 6/2 omnibus analysis); the evening migration-successor sessions (HOST, CXO) set up but never fired a cycle, and paused/PM-engaged sessions ended on "Surface to PM." This is the **unimplemented "auto-resume by silence"** (see "Recognizing the go autonomous signal" below — the `v0.7+ not yet implemented` line). **PROPOSED FIX (PoC, PM go pending):** (1) **launch-registers-cron** — Rule 0 launch should register the cron promptly so the cycle is live even if PM walks away (successor sessions must not "set up but never arm"); (2) **silence-fallback** — when the cron is Rule-2-paused and PM goes silent ≥ threshold, the live session re-arms the cron (auto go-autonomous), which then naturally reaches STOP. Gap B is why ~half the cohort didn't self-close 6/2.

---

## Cron-shape is now experiment-authorized (PM 2026-06-02)

The fixed hourly interval is the *default*, not a mandate. Agents are authorized to experiment with their cron-shape (interval, event-driven, long-interval-when-drained, low-frequency mail-awareness) to fit their lane's work-shape, and to **report results** in `cron-shape-experiments.md`. Bursty/intermittent lanes (Arch, Web) need not run hourly. The Rules above (0/1/2) still govern whatever shape you pick — they're about clash-avoidance, orthogonal to cadence.

---

## Cross-references

- `cron-shape-experiments.md` — work-shape-aware cadence experiments + reporting (PM-authorized 2026-06-02)
- `work-parts.md` — what triggers cron-pause (substantive WORK)
- `decision-table.md` — what triggers cron-resume ((0, 0) state = return to IDLE)
- `mail-loop.md` + `task-loop.md` — inner-loop work that constitutes "substantive WORK"
- v0.6 design: `docs/operations/duty-cycle design/duty-cycle-design-v0.6.md` (§ Corrections 1 + 2 + 2-refinement)
- Pilot cycle log Day-1: `dev/active/cycle-log-cio-2026-05-25.md` (where the clash + PM correction surfaced)

---

*Filed 2026-05-26 ~7:35 AM PDT by CIO Vehicle 2. Procedure derived from May 25 pilot corrections.*
