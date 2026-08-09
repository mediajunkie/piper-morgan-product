# Comms carry-forward

*Rewritten at the 2026-08-03 STOP fire (21:42 PDT). Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

- ⚠️ **ROTATED at the 2026-08-05 STOP.** New job **`c635f4d1`**, same expression `12 6,9,12,15,18,21 * * *`, fresh 7-day clock — **expires ~2026-08-12**. Old `e37fa867` deleted. Registry row updated.
- **Done CREATE-THEN-DELETE, inverting the skill's documented delete-then-create.** A failed *create* leaves you silently dark until a human notices; a failed *delete* leaves duplicates that Step 1 detects and heals on the next fire. **Prefer the failure mode that announces itself.**

## The one dated thing

**Sun Aug 9 publishes *Over-Checking Has Dividends*** — pre-passed Thu, **1,507 words, ZERO open `[PM:]` questions**, mechanically clean incl. check #15. **Needs PM's voice pass + art only.** ⚠️ **When cleared, the step-3 publish-ready memo goes to Docs FROM ME** regardless of who else offers to tell them.

🔴 **BETA MOVED BACK A MONTH** (PM, `decisions.log` 2026-08-08 ~10:10): *"We clearly have a lot more work still to do than anyone ever reported to me."*
- **Ship #054 (published Aug 5) carries "new target: Aug 8" — now superseded twice.** PM ruled Aug 6: **no retroactive edit, no correction notice**; the honest form is a future Ship saying it moved.
- **Told Exec #055 MUST carry it** even though the move falls outside the Jul 31–Aug 6 window, and **must not soften PM's reason** — *"the timeline was adjusted to accommodate additional scope"* is the exact dishonesty the Ship exists not to commit.
- ✅ **Swept the scheduled queue: ZERO forward-looking beta claims.** Nothing drafted needs changing.

**Narrative queue**: Beats 21–23 hold Aug 11/13/18. **Seven open Tue/Thu slots from Aug 20.** Eight candidate beats (24–28 + new 29–31) recorded in `upcoming-beats-plan.html` — PM reviewing.

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
