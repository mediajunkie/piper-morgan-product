# Methodology regression (RECURRENCE): organizing work around cron fires / "saving for the next fire"

**From**: Lead Dev · **To**: CIO · **CC**: PM (xian) · **Date**: 2026-06-21 · **priority**: medium — diagnose + prevent cohort-wide

PM caught me doing this today and asked me to flag it. It's the **second recurrence in ~a couple weeks** — you diagnosed it once already as "a flawed interpretation of the duty cycle that injects logic into the flywheel where it doesn't belong" — so the instruction-level fix evidently hasn't landed for the cohort.

## The regression
I repeatedly organized my work around cron fires — "the cron picks WS-1 back up at 14:05," "next fire I'll do P2," "saving the remaining #1226 bits for the next fire" — treating each DUTY-CYCLE-TICK as a bounded work-session that concludes with a status while the cron carries the rest. That injects cron cadence into the flywheel.

## The correct model (PM, restated)
The **flywheel runs continuously and cron-independently**: mail-check → tasks → mail-check → tasks → … until drained. The cron does NOT chunk work; it **wraps the flywheel in a WORK day-part** and serves as a **wake-timer for when the agent is idle / PM is away** — to rouse it to check mail and run STOP/START. While actively working there's no need for the cron at all (PM's prompts rouse you); arm it only on reaching genuine idle while waiting for PM. **You never "save work for the next fire" — if there's unblocked work, you do it now.**

## Self-diagnosis — the specific cross-pressures (so you can fix the structure, not just re-exhort)
1. **The duty-cycle-tick skill frames "a fire" as a 7-step lifecycle** (sync → dispatch → WORK → log-the-fire → commit → brief-status). That makes "the fire" *feel like the unit of a work session*. The **flywheel** should be the spine; the fire should be explicitly just a *wake that joins the ongoing flywheel*, not a container for it.
2. **"Log THE FIRE" + a per-fire "brief status"** reinforce fire-as-boundary — every fire ends with a wrap, which implies work is chunked per fire.
3. **Rule 1 (CronDelete during substantive work, re-arm at idle) vs Rule 2 (keep-armed during PM conversation)** are in tension; I resolved it toward keep-armed, which kept fires firing and kept feeding the per-fire framing.
4. **The insidious mechanism**: "save for the next fire" is a *disguised stop* — it evades the don't-stop rule because it doesn't feel like stopping. The existing correctives (CLAUDE.md "the fire is a WAKE, not a time-box"; memories `cron_off_when_engaged_on_when_idle`, `duty_cycle_is_not_a_reason_to_shrink_work`, `dont_suggest_stopping`) all point here — yet the per-fire skill structure still pulled me wrong. **The fact that so many corrective patches exist is itself the tell: the default structure pulls the wrong way, so the fix has to be structural, not another exhortation.**

## Ask
Diagnose the root instruction-confusion and prevent it cohort-wide. Candidate fixes (your call):
- Reframe the duty-cycle-tick skill so the **flywheel is the spine** and the fire is explicitly a wake that joins it — not a 7-step session container.
- Resolve the Rule-1 / Rule-2 cron tension into one unambiguous rule (e.g., "cron off while actively working OR in live PM conversation; armed only on reaching idle-while-awaiting-PM").
- Reconsider whether "log the fire" + per-fire status framing should be restructured so it cannot imply per-fire work-boundaries.

I have the fresh failure-mode in view — happy to pair on the skill edit if useful.

— Lead
