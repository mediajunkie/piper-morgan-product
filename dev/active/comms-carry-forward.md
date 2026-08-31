# Comms carry-forward

*Updated at the 2026-08-31 15:42 PT WORK fire (CIO's standing-items audit — see below). Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

`9aef0b01`, expression `12 6,9,12,15,18,21 * * *`, confirmed single active job — no rotation needed.

## Today

No scheduled pubDate row for 2026-08-31 (Monday isn't in the Tue/Thu narrative, Wed Ship, or Sat/Sun insight cadence) — confirmed against the live calendar. Mail empty at START.

## ESSENCE.md — RATIFIED (ahead of schedule)

Landed 08-30 afternoon as v1.0, well before the Wed 09-02 trifecta deadline I'd been tracking. **Concretely resolves the BYOC-copy milestone question**: PM ruled MCP work stays in the **Production** milestone, front-loaded, and its completion is the public-beta gate — not moving to MVP. Per PPM's own stated preference from 08-30 ("if MCP-path work stays in Production... this listing shouldn't exist yet at all"), **BYOC copy stays held**, not rescoped to a partial slice. Not owed to act — not addressed to me, no new ask — but this closes the loop on what was an open watch item. PM may still want a narrative/insight angle on the review itself; nothing to draft unless/until PM signals it.

## Watch: Tuesday Sep 1 is a busy day for PM

Two things compete for PM's Tuesday-morning writing time: **Ship #058's voice-pass** (Exec confirmed same-day compressed turn — my review + Docs' fact-check both land Tuesday, after PM's pass) and **Beat 4's still-needed voice-pass + art** (also pubDate Sep 1). Flagged this to Exec/Docs/PM as an FYI, not a problem — Beat 4 may just slip a day. No action needed from me until one or the other moves.

## CIO's standing-items audit — cleanup done, one real miss caught and fixed

Cohort-wide audit found my own file's staleness self-admission held up: 9 rows CIO confirmed already-published/resolved, now removed (file cleaned to just the genuinely-active items). One real miss: the "BYOC marketplace narrative" row (75 days old) read as "awaiting PM direction" but that framing was itself stale — I'd corrected it Aug 8 (drafted 3 angles, asked PM to pick or deprioritize, Web endorsed the same one I did) and the ask had been sitting unanswered for 23 days without my own tracker reflecting that the ball was actually in PM's court. Re-surfaced directly to PM (cc Exec/PPM/Web/CIO) this fire with the corrected framing and a note that ESSENCE's Production-milestone ruling likely doesn't block this narrative piece the way it blocks the listing copy.

## Open items — no Comms-side move available right now

- **Beats 4-6** — await PM's voice-pass/art (Sep 1/3/8 slots — Beat 4's Sep 1 may slip, see below).
- **ChicagoCamps talk** — PM reviewing script/slides this week (after an overnight trip); script + slide plan at `dev/2026/08/29/chicagocamps-talk-2026-09-17.md`.
- **BYOC marketplace narrative** — re-surfaced to PM today (pick A/B/C or deprioritize), 23 days silent before this. See `comms-standing-items.md` for the full angles.
- **Dispatch's one remaining syndication leg** ("Drained on Paper," Medium) — Dispatch-PM runs it, Docs fills the calendar's syndication columns per the corrected ownership model (Comms owns editorial columns only, per `.claude/skills/update-calendar/SKILL.md`).
- **website#35** — PM watching for recurrence, not actively pursuing.
- **BYOC listing copy** — held per the ESSENCE ratification. Nothing further needed until PM signals otherwise.

## Waiting on others

- **PM** — ChicagoCamps script/slide review; BYOC marketplace narrative pick; any steer on an ESSENCE narrative angle.
- **Dispatch-PM** — the one remaining syndication leg.
- **HOST** — Agent 360 synthesis, ~4 weeks out.
- **Someone (unclear who)** — #1636 (filed 08-15); #1647 (filed 08-18).

## Durable lessons from 2026-08-30 (for context, not action)

- Calendar column ownership is multi-writer *by column*, not single-writer — Comms owns editorial columns, Docs owns publish/syndication columns. Corrected a real miss same-day; saved as `feedback_reverify_ownership_conventions_before_asserting`.
- Cross-project mail to Dispatch-PM now has a formalized convention in `mailboxes/DIRECTORY.md` (real recipient in `to:`, cc Exec, deliver to `exec/inbox/`) — matches what I'd been improvising all week.
