# Duty Cycle Design — v0.6

**Status**: Three load-bearing corrections to v0.5 ratified by PM 2026-05-25 during Phase A pilot Day-1 live airport test. **Wake-mechanism corrected** (cron-during-session as PRIMARY, not bonus); **drain-until-IDLE semantics** added for WORK PARTS flywheel; **cron-bind-to-IDLE discipline** added (cron lifecycle bound to IDLE state, not orthogonal). DESIGN-SOLID status preserved with these corrections incorporated.

**Author**: CIO (Vehicle 2)
**Predecessor**: v0.5 (filed 2026-05-24)
**Changes from v0.5**: three corrections from May 25 pilot — see "Corrections in v0.6" section below for the specific load-bearing changes

---

## Guiding principle (preserved from v0.5)

> *"We are formalizing, not fragmenting or proliferating."*
>
> — PM 2026-05-24 12:07 PT

Net surface count stays flat or shrinks; coherence increases.

---

## North-star intent (preserved from v0.5)

> *"Wake if idle, check for new incoming messages, check for new tasks. Run the do-things-that-are-not-blocked cycle until everything's blocked. Then make the list of things you need a batch update on — update the doc for my attention. Check for mail again; if there's new mail, do it again. If you have any new tasks, do it again. Only when you get back to zero mail and zero tasks, this loop is done. Go to sleep. If I interrupt them and do stuff, they'll do more stuff. But if I'm busy and working another hour later, it'll wake up. And in the meantime, another agent may have woken up, gotten the message from someone, responded to them, and they can all be talking to each other without me going, 'hey, you've got mail, go check.'"*
>
> — PM to Ted Nadeau, 2026-05-20

**The drain-until-IDLE semantics in v0.6 are exactly what this north-star describes** — v0.5 mis-encoded it as one-work-unit-per-fire; v0.6 restores the run-the-cycle-until-everything's-blocked semantics.

---

## Three architectural decisions ratified (v0.5; preserved)

### 1. Task list = reframed standing-items tracker (no new doc)

`dev/active/{role}-standing-items.md` IS the task list.

### 2. Attention doc = reframed escalations file (no new doc)

`dev/active/duty-cycle-escalations-{role}.md` IS the attention doc.

### 3. No per-day cycle branch

The cycle runs in the agent's current session/branch. Mailbox writes still go on main per existing discipline.

---

## Corrections in v0.6 (NEW — three load-bearing changes from May 25 pilot)

### Correction 1: Wake mechanism — cron-during-session is PRIMARY (not bonus)

**v0.5 had this inverted.** The text in v0.5 §"Wake mechanism — finalized" read:

> **Primary**: manual session-open (canonical path) [...] **Bonus**: 4am cron wake [...] The cron is an **optimization, not a requirement**.

**v0.6 corrects this**:

- **Primary (in-session autonomy)**: cron fires every N min while session runs — THIS is the mechanism that makes the loop autonomous-while-PM-is-away. The whole reason the duty cycle exists.
- **Bootstrap (post-session-end)**: manual session-open OR 4am cron-if-session-survives-overnight. This is the recovery path for when sessions end (overnight, laptop-close, etc.) — necessary because cron is session-scoped, but it is NOT the primary mechanism.

**Why the correction**: PM Tuesday correction (May 25 ~10:58 AM EDT): *"Except when interrupted by direct interaction with me, the loop should be on a timer. At some amount of time (probably once an hour during the day), it needs to fire again. That's the whole point: autonomous review of any incoming mail can happen. Otherwise, it's dependent on me, and we really haven't created anything."*

The cron-is-session-scoped empirical finding (HOST + Lead Dev May 20) constrains *what survives across sessions* — not whether cron is primary in-session. I'd over-applied the constraint by demoting cron to "bonus" when it's actually the load-bearing in-session mechanism.

### Correction 2: Cron-bind-to-IDLE discipline

**v0.5 had cron lifecycle orthogonal to WORK/IDLE Decision Table state.** This caused fires to clash with in-progress work in the May 25 pilot (Fires 2-4 piled up while Fire 1's task was still draining).

**v0.6 binds cron lifecycle to IDLE**:

- **Entering substantive WORK** (Decision Table dispatches a non-trivial loop iteration; or substantive memo work; or substantive Task Loop work) → **`CronDelete <current-job-id>`** (pause). Cron-id retrieved via `CronList`.
- **Returning to true IDLE** (drain cycle complete; nothing more to do) → **`CronCreate`** with the same pattern (resume).
- **Brief mail-triage** (<2 min, CC info / close-loop, quick triage to read/) does NOT require cron-pause. Only substantive WORK (multi-step Task Loop work, memo drafting, substantive mail-response) does.

**Why**: cron is the IDLE-state mechanism — while the agent is actively working, another fire doesn't need to start; it's already working. When work completes and the agent returns to IDLE, cron resumes to wait for the next work-trigger (new mail or new task).

PM ratification: May 25 ~4:03 PM EDT: *"For this to work as intended, when you start working you will need to pause the cron while you work. Then, when it's time to go IDLE again you then start it up. Otherwise you are going to have these clashes."*

### Correction 2-refinement: PM-presence-pause

IDLE itself has two sub-states:

- **IDLE-PM-absent**: cron fires (autonomous mode)
- **IDLE-PM-present** (PM has just messaged, conversation active): cron paused (PM is the driver; cron firing would clash with PM turns)

Transition triggers:
- **Any inbound PM message → CronDelete** (PM is now driver)
- **PM "go autonomous" signal** (e.g., "I'm going AFK", "let it run", "start the cron", "resume cron") → CronCreate

Long quiet period without PM message could auto-resume; deferred for v0.7+ if needed.

PM ratification: May 25 ~4:14 PM EDT (refinement to Correction 2 above).

### Correction 3: Drain-until-IDLE semantics for WORK PARTS

**v0.5 mis-encoded the flywheel as one-work-unit-per-fire.** The Decision Table 2-bit state (new_mail, new_tasks) was interpreted as one-tick-per-fire — each cron fire dispatches one work unit then returns to IDLE.

**This is wrong.** PM's north-star (preserved above): *"run the do-things-that-are-not-blocked cycle until everything's blocked."* Each fire is meant to drain ALL unblocked work, not do one unit.

**v0.6 correction — the drain cycle**:

Each fire = wake from IDLE → drain ALL unblocked work → only return to IDLE when truly nothing left.

The drain cycle:

1. **Mail Loop drain**: process inbox to ZERO (each new memo handled fully — substantive responses drafted + distributed; CC info / close-loop triaged to read/). Do NOT stop after one memo — continue until inbox is zero.

2. **Task Loop drain**: process queued tasks from `{role}-standing-items.md` in priority order until ALL are blocked-on-external OR queue is empty. Do NOT stop after one task — continue until queue is drained.

3. **Re-check Mail Loop** (new mail may have arrived during Task Loop drain).

4. **Loop steps 1-3** until truly nothing to do (mail empty + tasks all blocked or empty).

5. **Only THEN return to IDLE** (no further drain possible; resume cron via CronCreate per Correction 2).

The Decision Table 2-bit state is now interpreted as **one tick per drain-cycle-step-within-a-fire**, NOT one tick per fire. The "fire" is the drain-cycle envelope; the Decision Table ticks govern progress within the envelope.

PM ratification: May 25 ~5:00 PM EDT: *"I do not want agents to 'only do tasks if the inbox was empty when you started reading the mail' — I want them to complete the mail loop when they reach inbox zero and then immediately start the task loop. When done I think they go back to see if there is any new mail, etc. [...] The rules should tell you to immediately do all unblocked work until there is no more."*

PM confirmation 5:04 PM EDT: *"I confirm you've got it right."*

---

## The architecture (preserved from v0.5/v0.4, drain-until-IDLE semantics applied)

- **Day-parts**: START → WORK → STOP
- **CHECK**: day-part dispatcher (new day → START; past 11pm → STOP; otherwise → WORK)
- **START**: day-open ritual (previous-log-close + new-log-open + sync)
- **WORK PARTS**: drain cycle per Correction 3 (NEW interpretation under v0.6)
- **STOP**: day-close ritual (sync-bracketed close)
- **IDLE**: PM-collaboration-available state, with two sub-states (PM-absent → cron fires; PM-present → cron paused per Correction 2-refinement)
- **Three per-agent docs**: tracker (new daily) + task list (reframed standing-items) + attention (reframed escalations)
- **Cron lifecycle**: bound to IDLE per Correction 2

---

## Cron interval guidance (NEW in v0.6)

v0.5 didn't specify interval. v0.6 guidance:

- **Recommended interval**: 10-30 minutes during active hours. Long enough that fires don't clash with each other (the drain cycle's natural duration). Short enough that mail latency stays under ~30 min.
- **Avoid :00 and :30 minute marks** per platform-load discipline (use `2-59/5 * * * *` or `3-59/10 * * * *` or similar).
- **Bounds**: don't go below ~5 min (clashes likely even with drain-until-IDLE since drains can be longer than 5 min). Don't go above ~60 min (mail latency hurts cohort).

v0.5 pilot tried */5 (every 5 min) — too aggressive; clashes observed. v0.6 default = 10 min interval.

---

## Open items (operational; deferred to implementation)

1. **Three-doc filename conventions** — finalize at first-adopter implementation; cheap to retroactively rename
2. **IDLE-launch detection mechanism** — manual at first; automatic-on-idle aspirational
3. **START step 2 "work in branch"** — try without; if gap shows operationally, address then
4. **Cohort rollout sequencing** — per implementation plan
5. **PM-presence-pause auto-resume** — currently manual ("go autonomous" signal); v0.7+ candidate to auto-resume after silence threshold
6. **Drain cycle bounded vs unbounded** — current v0.6 spec is unbounded (drain until empty). If real-world drains take >2hr without natural break, may want bounded-drain shape for PM visibility. Watch surface.

---

## Status milestone

**v0.6 ratification carried PM-acknowledgement on three corrections individually during May 25 ~4:03 / 4:14 / 5:00 PM EDT**. v0.6 status: DESIGN SOLID-with-corrections-applied. Phase B observation continues with v0.6 semantics live.

---

## Cross-references

- v0.5 (predecessor; mostly-preserved-but-three-corrections): `docs/operations/duty-cycle design/duty-cycle-design-v0.5.md`
- v0.4 (full architecture content from page 7 walkthrough): `docs/operations/duty-cycle design/duty-cycle-design-v0.4.md`
- Sketches: `docs/operations/duty-cycle design/sketches/` (7 PNG pages)
- Implementation plan: `docs/operations/duty-cycle design/duty-cycle-implementation-plan-v0.1.md`
- Pilot Day-1 cycle log: `dev/active/cycle-log-cio-2026-05-25.md` (contains the full chronology of where the three corrections surfaced)
- Pilot Day-2+ cycle log: `dev/active/cycle-log-cio-2026-05-26.md` (in-flight)
- Escalations doc: `dev/active/duty-cycle-escalations-cio.md` (corrections logged)
- Procedure docs (v0.6 updates pending in same drain): `procedures/work-parts.md`, `decision-table.md`, `mail-loop.md`, `task-loop.md`

---

*v0.6 filed 2026-05-26 ~7:30 AM PDT by CIO Vehicle 2. Drain task #1 of Phase B Day-1 fire 1. v0.5 superseded but preserved as historical predecessor.*
