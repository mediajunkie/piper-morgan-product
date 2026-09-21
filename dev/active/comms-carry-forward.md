# Comms carry-forward

*Rewritten 2026-09-20 21:42 (day close). Ephemeral session state only — durable owed/queued items
live in `comms-standing-items.md`; the canonical record is the session log
(`dev/2026/09/20/2026-09-20-0642-comms-code-log.md`).*

## Cron

`1b05adf6` — re-armed at 21:42 STOP via delete-then-create (d904b1d9 → 1b05adf6, same cadence),
CronList-verified exactly one job survives. Registry row updated to match. Next fire: 2026-09-21
06:12.

## Notable: comms' cron survived the 2026-09-20 Amber reboot — n=2 fleet finding, unresolved

Exec pre-emptively parked comms's registry row ahead of a coordinated reboot (Pard's runsheet B3),
reasoning "a reboot kills every cron." Self-verified before acting (CronList, twice) rather than
trusting the alert: found `d904b1d9` unchanged from before the reboot. Un-parked per the B9 clearing
condition (only the owning session, only after self-verifying). Reported to Pard/Janus (cc PM/Exec/
CIO) as a **second** confirming data point — Exec found the identical shape on their own seat
independently. **n=2, not resolved fleet-wide, not claimed to generalize.** Risk flagged: if this
does generalize, seats that blindly re-arm per B9's original instruction could duplicate-stack a
second job on the same expression. **Watch for Pard/Janus's ruling on this** — it may change the
reboot-recovery procedure for future reboots.

## Closed today

- **"Assume It Was You"** (pubDate 09-19) — published + distributed by Docs same-day. Nothing owed.
- **"From Abstraction to Example"** (pubDate 09-20) — published by Docs this morning (06:33 PDT,
  confirmed via commit timestamps after I initially and incorrectly logged it as "overnight" — PM
  caught the imprecision). Nothing owed.
- **"The Near-Miss and the Missing Key"** (pubDate 09-22, Tuesday) — PM requested review via chat
  (not a duty-cycle fire). Full audit 16/16, fact-checked harder than usual since it's self-
  implicating (verified the exact "572 words" claim against the real git commit, confirmed the
  compose-editor root-cause matches Web's actual website#35 fix). Calendar → `ready-for-docs`,
  publish-ready memo sent. PM then renamed the image (raw UUID → `bridge-out`, uploaded via phone) —
  propagated to frontmatter + calendar `cartoon` field, sent Docs a follow-up since my first memo had
  quoted the old filename by name. **Docs has since logged their own proofread + durable publish
  plan for 09-22** (seen via sync) — fully closed, nothing owed.
- **Calendar mechanism: new `planned` status + pre-seeded Ship slots #061–#073** (one quarter,
  PM's ask via Exec) — validated same-day when Exec's own tooling hit the #061 placeholder as
  designed; verifying their edit caught a real defect (`draftPath` pointed at `dev/active/` instead
  of `docs/public/comms/drafts/`, same class as a documented Ship #058 mistake), fixed. Known minor
  gap, not fixed: HTML calendar view has no `planned` CSS case (falls back to `drafted` styling).
- **#1406** (calendar `canonicalSite` legacy stale values) — investigated, found already resolved,
  closed with evidence.
- **#1834 build-item 1** (HOST's ruling: agents are never "person"/"people," any register) — picked
  up same-day. `template-audit` v1.15 now catches singular "person." Issue left open for build-item 2
  (Exec's/CIO's — PM-facing internal reports).
- **Drafts-queue count corrected cohort-wide**: my own tracked "9-10" figure was low by 2 (missed
  insight-theme drafts outside the building-narrative artifact's scope). Queried the calendar
  directly, found the true count (12 pre-review; now down as posts publish), corrected via reply-all
  on Exec's sprint-plan share.
- **workDate accuracy — the one flagged row resolved.** "Integration Reveals All"'s workDate
  (June 27, exact match to pubDate) is CONFIRMED CORRECT against PM's own archive — Web self-
  corrected after nearly proposing a fallback that would have destroyed the correct value. The
  broader audit (checking other rows against PM's archive) is still blocked on PM naming where the
  archive lives — not supplied yet.

## Open — no PM-gate currently, just queue depth

- **Drafts awaiting PM's voice-pass**: verify current count fresh at next real need — don't trust a
  carried-forward number without re-querying (see the "9-10 was wrong" lesson above). Full list as of
  09-20 pre-review: The Alarm That Had Been Working All Along, Three Seats Stay Dark Longer, What
  Piper Morgan Actually Is, The Contract Tested the Day It Was Born, Three Silent Failures Became One
  Law, Distribution Is a Product Decision, No Undo, Giving It Away, The Message That Deleted Itself,
  The Feature That Was Never Real, The Board That Stopped Matching Reality (The Near-Miss item closed
  today, removed from this list).
- **ChicagoCamps talk (Sept 17) outcome still unconfirmed.** No session-log mention it happened
  anywhere 09-17 through 09-20. Ask PM directly.
- **`template-audit` gap, 2 data points**: no check for "claims a named person is already public."
  Third instance = file it properly.
- **Cross-doc title inconsistency** — DIRECTORY.md "Communications Chief" vs. ROSTER.md
  "Communications Director." Not mine to reconcile.
- **Series structure (era split + blog-index featuring)** — structural display question open,
  PM/Web's call. Eras sorting (not pubDate) is the intended sequencing mechanism per PM's 09-17 note.
- **No stated GitHub-criteria line yet** (duty-cycle-tick v1.33's third work-queue source) — gap
  named 09-19, still unfilled, nothing blocked on it.
- **Language-governance mechanism, part 2**: HOST named Comms for eventual reconciliation against
  the existing public-prose convention once Exec/CIO build the internal-reports check (#1834 item
  2). Nothing to do until that lands.
- **Attention-rollup gap**: flagged to Exec that my drafts-queue item wasn't visible in a rollup
  snapshot despite being in this file (a canonical source). Watch the next regen.

## Waiting on others

- **PM** — voice-pass + art on the queued drafts (verify count fresh); ChicagoCamps outcome;
  archive location for the workDate audit; editorial calendar planning session (stated next step,
  no scope given yet).
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Pard/Janus** — ruling on the cron-survives-reboot finding (see above).
- **Someone (unclear who)** — #1636 (filed 08-15, OPEN as of 09-19); #1647 (filed 08-18, OPEN as of
  09-19).
