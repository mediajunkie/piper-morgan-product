# Comms carry-forward

*Rewritten 2026-09-21 21:40 (day close). Ephemeral session state only — durable owed/queued items
live in `comms-standing-items.md`; the canonical record is the session log
(`dev/2026/09/21/2026-09-21-0621-comms-code-log.md`).*

## Cron

`2db6101f` — re-armed at 21:40 STOP via delete-then-create (1b05adf6 → 2db6101f, same cadence),
CronList-verified exactly one job survives. Registry row updated to match. Next fire: 2026-09-22
06:12.

## Notable: cron-survives-reboot finding — n=4, still no Pard/Janus ruling (2 days now)

Comms's cron survived the 2026-09-20 Amber reboot unchanged; Exec/Comms/Web/CIO all independently
confirmed the identical shape on their own seats (n=4), plus CIO's sub-finding that delivery jitter
didn't reroll across the reboot either. **Checked again today (both morning and STOP) — still no
ruling from Pard/Janus.** Nothing for Comms to do here beyond continuing to watch; not chasing it.

## Yesterday's heartbeat lesson, applied again today

09-21's START heartbeat genuinely failed to push (busy `main`, post-reboot traffic) — took 3
fetch/merge/retry cycles, confirmed via a direct `git show origin/main:...` file read rather than
trusting an empty `origin/main..HEAD` diff (which can read clean mid-race). Applied the same
direct-verification habit again at 18:12's heartbeat today (which wrote for real after several
suppressed quiet fires) — worth keeping as standing practice whenever a heartbeat writes, not just
when one visibly fails.

## Closed (carried from 09-19/09-20, still true)

- **"Assume It Was You"** and **"From Abstraction to Example"** — both published + distributed.
  Nothing owed.
- **"The Near-Miss and the Missing Key"** (pubDate 09-22, tomorrow) — `ready-for-docs`, full audit
  16/16, image renamed to `bridge-out`. **Docs independently reproduced the same audit result
  (16/16, same fact-check) and pre-wrote the Tuesday publish plan into their own carry-forward** —
  confirmed via sync 09-21 morning. Fully closed; publishes tomorrow via Docs' own plan, no action
  needed from Comms unless something changes.
- **Calendar mechanism: `planned` status + pre-seeded Ship slots #061–#073** — shipped and validated.
  Known minor gap, not fixed: HTML calendar view has no `planned` CSS case.
- **#1406** and **#1834 build-item 1** — both closed with evidence.
- **Drafts-queue count corrected cohort-wide** (was low by 2, true count established 09-20).
- **workDate accuracy** — the one flagged row ("Integration Reveals All") confirmed correct against
  PM's archive. Broader audit still blocked on PM naming the archive location — not supplied yet.

## Open — no PM-gate currently, just queue depth

- **Drafts awaiting PM's voice-pass**: re-query fresh before quoting a count — don't trust a carried
  number (see the "9-10 was wrong" lesson). No new drafts entered the queue 09-21 as far as I saw.
- **ChicagoCamps talk (Sept 17) outcome still unconfirmed.** No session-log mention it happened
  anywhere 09-17 through 09-21. Ask PM directly.
- **`template-audit` gap, 2 data points**: no check for "claims a named person is already public."
  Third instance = file it properly.
- **Cross-doc title inconsistency** — DIRECTORY.md "Communications Chief" vs. ROSTER.md
  "Communications Director." Not mine to reconcile.
- **Series structure (era split + blog-index featuring)** — structural display question open,
  PM/Web's call. Eras sorting (not pubDate) is the intended sequencing mechanism per PM's 09-17 note.
- **No stated GitHub-criteria line yet** (duty-cycle-tick v1.33's third work-queue source) — gap
  named 09-19, three days unfilled now, nothing blocked on it.
- **Language-governance mechanism, part 2**: HOST named Comms for eventual reconciliation against
  the existing public-prose convention once Exec/CIO build the internal-reports check (#1834 item
  2). Nothing to do until that lands.
- **Attention-rollup gap**: flagged to Exec 09-20 that my drafts-queue item wasn't visible in a
  rollup snapshot despite being in this file. Not re-checked since; watch the next regen.

## Waiting on others

- **PM** — voice-pass + art on the queued drafts (verify count fresh); ChicagoCamps outcome;
  archive location for the workDate audit; editorial calendar planning session (stated next step
  after 09-19's two posts, no scope given yet — two days now with no follow-up on this).
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Pard/Janus** — ruling on the cron-survives-reboot finding, 2 days unruled.
- **Someone (unclear who)** — #1636 (filed 08-15, OPEN as of 09-21); #1647 (filed 08-18, OPEN as of
  09-21).
