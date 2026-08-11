# Comms carry-forward

*Rewritten at the 2026-08-03 STOP fire (21:42 PDT). Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

🔴 **PARKED 2026-08-11 — this seat does NOT fire until re-armed by hand.** Session-scoped `CronCreate` job **`f53ad8c5` cancelled** ahead of the Amber macOS 26.6 reboot, per Pard's second stand-down notice. `CronList` verified **"No scheduled jobs."**

**A session-scoped cron dies with the reboot and leaves no trace** — nothing re-arms it automatically, and a dark seat looks identical to a healthy one.

**Restore instructions — expression AND verbatim prompt — are in `docs/handoff-comms-2026-08-11.md` §0.** The cadence alone is insufficient: `CronCreate` requires the prompt, and re-arming with the wrong one produces a cron that fires into nothing.

**Watchdog registry row parked to match**, with a falsifiable clearing condition: **clear it only when `CronList` actually shows an armed job, not when someone intends to re-arm.**

## The one dated thing

**Tue Aug 11 publishes *The Write-Path Chase* (Beat 21).** ✅ Pre-passed Aug 9, two days early. **550 words and that is FINE** — measured, published narratives run 597–2,564 and *Almost Beta* (597) shipped clean. **DO NOT PAD.** Structurally complete: verify-by-read-back rule → five stacked releases → issue #104 confirmed.
⚠️ **One flag for PM**: text says *"five stacked point releases"* but names **three** problems — same three-vs-five miscount class PM cut from Ship #054.
**Needs PM: voice pass + art only.** Zero open brackets. **Publish-ready memo goes to Docs FROM ME.**

⚠️ **OPEN: Aug 8 *Verify at the User Path* is `published` but NOT syndicated** — no Medium, no LinkedIn, while Aug 9 (published later) is fully `distributed`. Filed with Dispatch at `~/Development/dispatch/mail/` (they are NOT on the `mailboxes/` system); Docs tracking. **I own the calendar columns and offered to fill them from URLs.**

🆕 **BYOC task force is LIVE** — convened 8/9 after seven weeks; **PPM and Web both took their lanes within hours.** PPM: the bar isn't a connector *count*, it's #1440's ratified five-point contract. Web: `/try` exists but assumes a **web-first** visitor, not a storefront arrival. **Next move is mine** — the listing copy, once PM/CXO settle *product vs model*.

## Open PM questions — 4 across 3 posts, best answered in one pass

| post | pubDate | question |
|---|---|---|
| *The List That Lies* | **Aug 4** | Was the Jun 29 gate removal on the live server PM's own? |
| *Drained on Paper* | Aug 6 | Who declared the backlog drained? Does the dishes/baby line land as written? |
| *No Undo* | Sep 12 | Is the babysitter/baby analogy PM's own framing? |

Surfaced only because `template-audit` check #5 was blind to `[PM: …]` until Aug 3. **No bracket ever reached a reader** — verified against the live page.

## Owed by me, with a named trigger

✅ **DISCHARGED 4 Aug — the PreToolUse exit-0 observation.** A PreToolUse hook exiting 0 **does** reach the agent (`check-branch.sh` printed to me on commit `eb6919e0c`). CIO's silent-no-op fear doesn't hold for **stdout**. ⚠️ **stderr remains unresolved** — my replication staged nothing and measured an empty index; that run was **inconclusive, not a null**. The practical fix needs neither: `exit 0` with the message on stdout.

🆕 **OWED tomorrow morning — the heartbeat surface check.** I proposed it to CIO as the test that replaces tomorrow's uninformative 06:46 alarm, so I should run it:
```
ls dev/heartbeats/2026-08-05/
for f in dev/heartbeats/2026-08-05/*.tsv; do head -1 "$f"; done
```
**My stated prediction** (so it can be falsified): the surface **fills** — several role files, each with a START row — **and most START timestamps land after 06:46**. That would close "nobody runs it" + "it declines to write" and confirm "it runs too late" with a number.
⚠️ **Weakest link, flagged**: I inferred "the surface will fill" by **reading** that START bypasses `--if-quiet` at `duty-cycle-heartbeat.sh:65`. **I have not watched a START write** — mine today ran before CIO's change. If the surface is still `cio.tsv` only, the promotion didn't take either.

## Waiting on others

- **HOST/CIO** — two hook items I deliberately did not touch: (1) staging-warn behaviour still blocks vs. stated intent; (2) `pre-commit-reconcile-drafts.sh` **header** still teaches the inverted model, incl. the backwards "promote to exit 1 (hard-block)" instruction.
- **Docs** — nothing owed; archival closed (23 files), validator shipped, calendar 0 dangling.
- **PM** — Beats 24–28 steer (**the only item with a real date**: narrative queue runs dry after Aug 18); voice-pass + art on Beats 21–23 (Aug 11/13/18); `/hooks` open or restart for HOST's memory counterweight; compose-UI restore-banner check.
- **Web/PM** — era split + featuring the current post on the blog index. My POV is in `docs/internal/planning/comms/upcoming-beats-plan.html`.

## Verified today, don't re-derive

- Beta target **2026-08-08 (Saturday, deliberate)** — `decisions.log:303`, PM Time Lord prerogative. HOST's "zero occurrences" memo was **retracted same day** (grepped `Aug 8`, missed the ISO rendering). Ship #054 line 77 carries it and is **correct — do not soften it**. Noted on the calendar row.
- Footer-tease chain across the next 10 posts: **clean**. Ships sit outside the chain (6/6 carry no tease; 7/8 narratives tease past them) — now encoded in `template-audit` v1.4.
