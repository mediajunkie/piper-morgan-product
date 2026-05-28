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

## Cross-references

- `work-parts.md` — what triggers cron-pause (substantive WORK)
- `decision-table.md` — what triggers cron-resume ((0, 0) state = return to IDLE)
- `mail-loop.md` + `task-loop.md` — inner-loop work that constitutes "substantive WORK"
- v0.6 design: `docs/operations/duty-cycle design/duty-cycle-design-v0.6.md` (§ Corrections 1 + 2 + 2-refinement)
- Pilot cycle log Day-1: `dev/active/cycle-log-cio-2026-05-25.md` (where the clash + PM correction surfaced)

---

*Filed 2026-05-26 ~7:35 AM PDT by CIO Vehicle 2. Procedure derived from May 25 pilot corrections.*
