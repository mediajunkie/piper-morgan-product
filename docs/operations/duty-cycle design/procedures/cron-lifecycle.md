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

### Transition triggers (updated — keep-armed-default, PM-ratified 2026-06-06)

- **Inbound PM message / active conversation** → **keep the cron ARMED** (do NOT CronDelete). Idle-suppression + a presence-aware fire (quick "PM still here, hold" + re-arm) keep it from clashing with PM turns.
- **My own substantive multi-step work (>2min)** → `CronDelete` FIRST (this is **Rule 1**, unchanged — the inter-tool-call REPL clash), `CronCreate` same expr back at IDLE.
- **A question I've asked PM that's pending** → **does NOT delete the cron and does NOT block other work** (see refinement below).

### Refinement (PM-ratified 2026-06-06): keep-armed-default; a pending PM question never blocks autonomous work

**Supersedes the 2026-06-03 "CronDelete-when-question-pending" refinement.** That earlier refinement (positive-CronDelete during active exchange with a pending question) turned out to *create* brittleness: it left the cron deleted whenever the agent had asked PM something, so a **silent PM walk-away → no autonomous resumption and no overnight self-wake** (CIO hit exactly this 2026-06-05→06: cron deleted after a pending question, PM got busy, manual reopen required the next morning).

PM's directive (2026-06-06, verbatim sense): *"I have to leave some questions unanswered until I can focus, and we shouldn't let that block you from doing other work until there is no way to advance without my response."*

**The rule now:**
1. **Keep the cron armed during conversation by default.** Rely on idle-suppression + presence-aware hold. A silent PM walk-away then **self-heals** — the next idle tick resumes autonomous work (and overnight continuity) with zero PM action. (PM should NOT have to remember to signal "I'm stepping away," nor press anything — the system absorbs the unknown.)
2. **A pending PM question is NOT a blocker.** Keep advancing any *other* unblocked work (mail drain, task loop, low-pri per v0.6.3). Only genuinely stop / hold on the *specific thread* that has no way to advance without PM's answer — never let it freeze the whole cycle.
3. **The only positive CronDelete is Rule 1** (my own substantive multi-step work), to avoid a re-fire landing mid-sequence. Re-arm at IDLE.

**On the Comms finding (2026-06-03):** the observation was real — a fire *can* slip in while awaiting a PM reply. The disposition is now reversed: that fire is **acceptable** (a presence-aware fire does a quick hold and re-arms; minor cost) and is **far preferable** to the delete-and-forget brittleness. Suppression-imperfection is tolerated; silent-walk-away-self-heal is the priority invariant.

**Note (`/loop` Esc):** Claude Code's `/loop` has an interactive Esc-to-stop; that is `/loop`-specific and does NOT apply to our `CronCreate`-based cycle. PM does not need (and should not rely on) any keypress to pause us — keep-armed-default makes manual pausing unnecessary.

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

**Gap B — sessions abandoned mid-conversation never reached STOP at all (still open).** Agents that were PM-engaged (Rule-2 cron-paused) when PM stopped responding just *trailed off* — they never detected "PM left, resume autonomous cycle" so they never drained-to-IDLE or ran STOP. Hit PA, Web, HOST, CXO, Arch (per Docs's 6/2 omnibus analysis); the evening migration-successor sessions (HOST, CXO) set up but never fired a cycle, and paused/PM-engaged sessions ended on "Surface to PM." This is the long-deferred "auto-resume by silence." **RESOLVED (PM go-ahead 2026-06-03) — and the PoC found no new runtime mechanism is needed: "always-armed" IS the silence-fallback.** A cron left armed fires on its next *idle* tick after PM goes quiet (runtime idle-suppression absorbs fires *during* conversation), so an armed cron auto-resumes autonomy with no separate timer. Gap B was simply that the cron wasn't armed. The three rules that make "always-armed" hold:

1. **Launch registers the cron immediately** — at launch (Rule 0), register the cron and keep it armed *through* PM conversation (Rule-2-Model-A: idle-suppression makes armed-during-conversation safe). Do NOT defer registration because PM is engaging you — that was the HOST/CXO **successor-session failure** (set up substrate, never armed, PM left, never cycled).
2. **Re-arm before yielding to PM** — if you CronDelete-FIRST for substantive work (Rule 1) and then must wait on PM input, CronCreate again *before* going quiet, so you're never PM-waiting with a deleted cron (the PA/Web/Arch **trailing-off failure**).
3. **STOP re-arms** (Gap A, above).

Net: the cron is *always armed*; its next idle fire after PM-silence is the auto-resume. No silence-timer to build. (CIO dogfooding live 2026-06-03: cron `f36e2cf2` stays armed through PM conversation; will auto-resume on the next idle tick when PM goes quiet.)

### Synthesis: "quiet-hold overnight" is the general pattern (HOST finding, 2026-06-03)

HOST's low-freq experiment (`37 */3 * * *`) self-woke overnight→morning **without needing the `2,4-23` re-arm fix** — its 00:37/03:37 fires were *quiet holds* (no-op, PM-absent, cron never deleted), and 06:37 routed to START. The insight: **Gap A is specifically the hazard of the one path that hard-deletes the cron on a quiet tick (STOP-runs-CronDelete-and-not-re-arm).** Shapes that treat overnight as *quiet-holds* (cron keeps ticking, dispatcher routes each tick, CronDelete only for genuinely-substantive Rule-1 work) never open the gap. So the corrected general principle, across all shapes: **STOP is a day-close *ritual*, not a cron-teardown — the cron quiet-holds across the day boundary.** Both shapes are the same family (CIO `2,4-23`: silent-overnight + one watch + STOP-leaves-armed; HOST `*/3`: quiet-hold ticks). The re-arm-at-STOP rule (Gap-A fix) is the *safety net* for the hard-STOP path; quiet-hold is the *primary* mechanism. Fewer moving parts — credit HOST.

### Gap C — compaction silently kills session-scoped crons (PA finding, verified 2026-06-07)

**The biggest stallout vector, and the one neither Gap A nor B addresses.** A session-scoped cron (`durable: false` — what we all run) lives only in the running session's memory, and **a context *compaction/resume* does not carry it across.** PA's cron silently vanished overnight (`CronList` → "No scheduled jobs") — **not** laptop-sleep (caffeine was on; other agents ran fine), but because *that session compacted* (SessionStart:resume events) while others didn't. No error, no fire, no signal — the cycle just stops.

- **Compaction is routine and unpredictable**, so this is a *live, recurring* stallout vector — worse than laptop-sleep because it hits a single agent silently mid-run, not the whole cohort visibly overnight. It reframes the "session-alive premise": the ceiling isn't only session-*death*, it's session-*compaction*.
- **`durable: true` is a no-op in this environment** (PA verified 2026-06-07): `CronCreate(durable:true)` returns the same "Session-only … dies when Claude exits" message and writes no `scheduled_tasks.json`. So the documented durable escape hatch is NOT available — we cannot flag our way out.

**Therefore monitoring is the necessary fix, not a flag.** Three directions (CIO synthesis for the stallout-monitoring effort, PM-directed 2026-06-07):
1. **Liveness/heartbeat monitor** (external) — detect "an agent that should be cycling hasn't fired/committed in N hours" → alert. This is exactly the **Routines watchdog (roadmap item 1)** — Gap C makes it concrete + urgent (it's the only thing that catches a silent compaction-loss, since the dead cron can't self-report).
2. **Agent-side re-arm (partial mitigation — reduces the dead-window, does NOT cure it; PA refinement 2026-06-07).** On any turn the session gets, `CronList`-check and re-arm a vanished duty cron. **Two honest limits PA surfaced:** (a) **the SessionStart hook can't actuate** — it's a *shell script*; `CronCreate`/`CronList` are agent/MCP tools, not shell commands. So the hook can only **emit a reminder** ("duty cron not detected — re-arm it") into session-start context; the **agent** must run `CronList`+`CronCreate` in response. The hook is a *prompt-to-the-agent*, not the actuator (same philosophy as the thin cron prompt itself) — designing it as an actuator would be a no-op like `durable:true` was. (b) **It only fires if the session gets a turn at all** — a fully-dead cron has no trigger, and a bare resume doesn't auto-take a turn, so agent-side re-arm heals on the *next turn the session happens to get* (a human prompt, or a surviving fire). That **shrinks** the silent dead-window; it does not make the cycle self-sustaining across compaction. (PA's 6/7 self-heal worked but was *human-prompted*, not automatic — proven action, unproven automation.) Implemented as the duty-cycle-tick **Step-1 self-heal** (skill v1.3) + PA piloting a session-start-routine version; cohort hook version (reminder-only) is Lead/infra.
3. **Registry cross-check** — "agents expected cycling" vs "crons actually live" surfaces the gap (derived-view; pairs with cohort-cycle-status.sh).

**Net**: the duty-cycle infrastructure is sound, but a routine compaction can silently sever it with no trace and the durable hatch doesn't work → **external liveness monitoring (Routines watchdog) is now load-bearing, not optional.** (This also closes the thin-prompt PoC's "fresh-session-post-compaction" open item: the risk isn't skill-load, it's cron-survival — mitigated by SessionStart-re-arm + the watchdog.)

**Empirical update (PA pilot 6/7 + CIO survival 6/8):**
- **Gap C is *probabilistic*, not deterministic.** PA's cron vanished **~2×** across 6/7's session events; **CIO's cron SURVIVED** the 6/7→8 overnight compaction (CronList showed it live on resume). Same mechanism class, different outcomes — so an agent cannot *assume* either survival or death; it must **check** (CronList) on every turn. This strengthens the watchdog case: with probabilistic loss, only an external monitor reliably catches the cases that *do* die.
- **PA empirical confirmation of the reframe**: both of PA's 6/7 re-arms were **turn-triggered** (AM = PM-prompted; PM = the sign-off-checklist's CronList step caught the vanish *unprompted-by-human, but still required the session to be taking a turn*). The 14:48 re-arm then survived and fired at 16:12 → **re-arm is durable *within* a live session; the failure mode is the session-event, not the arming.** Neither was a *no-turn* recovery → agent-side genuinely only shrinks the dark-window.
- **Refinement → re-arm on *every turn-type*, not just session-start (PA):** the agent-side detection net is widest when the CronList-check-and-re-arm runs at **session-start (hook-reminder) + each cron fire (skill v1.3 Step-1) + sign-off/STOP**. The sign-off checklist is a *second* unprompted detection point beyond session-start. Maximizes the partial mitigation; still cannot cover the no-turn case (the watchdog's job).
- **The clean confirmation still pending**: a fully *unprompted, no-turn* compaction (session compacts, gets no turn, no human, no sign-off) — by the logic it should NOT autonomously recover. PA reports when one is caught in the wild.
- **The variance is *activity-correlated*, not random (PA 6/8)**: both CIO's and PA's crons survived the *quiet* overnight (low activity, ~no compaction); PA's two deaths were both during the *heavy active work day* (many turns + compactions). So Gap-C loss ≈ probabilistic-per-compaction × (compactions cluster during active work) → **"dies on busy days, survives quiet nights."** This *sharpens* the watchdog case: the silent-dark risk **peaks exactly when the agent is busiest and most valuable**, not when idle. (Caveat: small-n; a cohort-wide "deaths vs session-activity" tally — pairs with the registry cross-check — would test it.)
- **RESOLVED (durable:true is a no-op) — Arch withdrew F4, 2026-06-08**: the contradiction is settled. Arch ran the cheap test (check #1): **no `.claude/scheduled_tasks.json` exists** for a `durable:true` cron — the parameter is silently dropped (the CronCreate output literally says "Session-only … dies when Claude exits"). Arch's Mon 07:03 fire was the predicted confound — the *session* was alive across the boundary, not the cron persisting. **PA's "durable=no-op" finding is ground truth.** Consequences: (a) durable is NOT a cheaper Gap-C floor → **the watchdog hold is CLEARED; the Routines watchdog is the Gap-C cure** (agent-side re-arm reduces the dark-window, watchdog cures the silent-stop — durable adds nothing). (b) Any "prefer durable=true" norm-call is **moot** until the durable mechanism actually works (a future tooling/env fix would re-open it). (c) Nice methodology footnote (Arch's own): the F4 error was itself a claim-vs-reality drift — claiming "durable validates" without consumer-tracing the disk-write — i.e., the exact shape m-30 catches; *drift-produced-not-caught*, so not an m-30 Proven instance, but it reinforces the discipline's value.

---

## Cron-mechanism migration — the orphaned-predecessor gap (CIO, 2026-07-10)

**Distinct from Gaps A/B/C above** — those are about overnight *survival*; this is about *migrating between mechanisms* (e.g. ephemeral `CronCreate` → persistent `scheduled-tasks`, or the reverse). Diagnosed with PM as a `methodology-35` (Asymmetric Discipline) instance: the creation-half of a migration is always performed (the new job visibly exists), but nothing ever specifies deleting the predecessor — and unlike Gap A (where the *same* session can self-heal at STOP), here it usually can't, because the two mechanisms don't share visibility.

**The originating instance**: Docs moved their first-fire from `17 10,22` (ephemeral cron) to `17 5,17` (a `scheduled-tasks` entry) to satisfy a PM schedule-change request. The new scheduled-task was created; the old ephemeral cron (`f33227b7`) was never torn down. Both then ran independently — two full duty-cycle sessions doing overlapping work daily, discovered when Docs noticed two session logs covering the same day's work (see "Detecting it after the fact" below).

**Why this is architecturally harder than Gap A**: `CronList`/`CronDelete` only ever see jobs the *calling session itself* created (confirmed empirically 2026-07-10 — CIO could not see or delete `f33227b7` from a different session; same result testing against Arch's cron the same day). `scheduled-tasks` is a genuinely different, disk-persistent subsystem with its own list — a session on one mechanism cannot see, let alone delete, a job on the other. Once the session that performed the migration moves on, **no other session, and no other mechanism, can ever reach back and delete the orphaned predecessor.** This is a structural tool-surface limit, not a discipline gap alone — no amount of "try harder" fixes it after the fact.

**The discipline (the only fix that actually works, since it has to happen before the visibility window closes)**: when migrating your own cron from one mechanism to another, **self-delete the old mechanism's job as an explicit, named step of the same migration** — before or immediately after creating the new one, in the same session/turn that does the creating. Do not defer it, do not assume "I'll clean it up later" — later, it may be permanently unreachable. Verify both surfaces before considering the migration complete: `CronList` for ephemeral jobs, `mcp__scheduled-tasks__list_scheduled_tasks` for persistent ones (the latter is genuinely cross-session-visible, unlike `CronList` — useful for confirming the new job registered correctly, though it still can't see the old ephemeral job if that's what's being retired).

**Detecting it after the fact** (the backstop, for when the discipline above was missed and the window has closed): you can't inspect another session's cron state directly, but you *can* notice the symptom — two session logs (or two sets of commits) for the same role covering overlapping work in the same day, the way Docs's own read of their day surfaced this instance. Once noticed, `mcp__ccd_session_mgmt__list_sessions` can identify which session owns the stray job (it's cross-visible, unlike cron state itself), and `mcp__ccd_session_mgmt__send_message` can ask that session to self-clean — both used successfully for this exact case 2026-07-10. This is detection-and-nudge, not a direct fix; only the session that created the job can actually delete it.

**Cross-reference**: `methodology-35-ASYMMETRIC-DISCIPLINE-CREATION-WITHOUT-PAIRED-CLEANUP.md` — this instance, paired with the same-mechanism STOP-re-arm fix (this doc's Gap-A family, `duty-cycle-tick/SKILL.md` fixed 2026-07-10), meets the methodology's stated ≥2-instances promotion criterion; promoted Emerging → Proven same day.

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
