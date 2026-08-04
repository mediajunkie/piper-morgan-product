# Comms carry-forward

*Rewritten at the 2026-08-03 STOP fire (21:42 PDT). Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

- Job `e37fa867` · `12 6,9,12,15,18,21 * * *` · verified live at every fire on Aug 3. **Auto-expires ~2026-08-09** — re-arm before then.
- Registry row in `dev/active/duty-cycle-registry.tsv` matches.

## The one dated thing

✅ **"The List That Lies" (Aug 4) is READY FOR DOCS** — PM voice-passed and illustrated 4 Aug; full `template-audit` v1.5 run clean; PM-approved trims applied (1,901 → **1,747** words). PM is notifying Docs directly.

⚠️ **Pass along at publish**: `/blog/the-list-that-lies/` is currently a **cached 404** from Web's soft-404 fix (`03b77d9d`, deployed ~13:45 Aug 4). Should clear on publish — a new post forces a rebuild, which invalidates — **but that is reasoning, not a verified behaviour.** Docs should check the **status code alongside** the v0.22 presence-check at publish. If it's 200 with body present, this closes for good and is worth a line in the skill.

**Next up**: **Weekly Ship #054 "Clear Is Not a Measurement" (Wed Aug 5, Exec-drafted).** Pre-passed a day early — **one real fix outstanding: the H1 is sentence case** (`Clear is not a measurement`) against 5-of-5 Title Case convention *and* its own calendar row. Sent to Exec 4 Aug. 🔴 **Line 77's "target: Aug 8" is CORRECT and must not be softened** (`decisions.log:303`; Saturday, deliberate) — noted on the calendar row.

## Open PM questions — 4 across 3 posts, best answered in one pass

| post | pubDate | question |
|---|---|---|
| *The List That Lies* | **Aug 4** | Was the Jun 29 gate removal on the live server PM's own? |
| *Drained on Paper* | Aug 6 | Who declared the backlog drained? Does the dishes/baby line land as written? |
| *No Undo* | Sep 12 | Is the babysitter/baby analogy PM's own framing? |

Surfaced only because `template-audit` check #5 was blind to `[PM: …]` until Aug 3. **No bracket ever reached a reader** — verified against the live page.

## Owed by me, with a named trigger

✅ **DISCHARGED 4 Aug — the PreToolUse exit-0 observation.** Fired on my own typo commit (`eb6919e0c`). **Answer: a PreToolUse hook exiting 0 DOES reach the agent** — `check-branch.sh` printed its lines 54–55 to me on that commit. So CIO's fear (that `exit 2` → `exit 0` converts a mislabelled block into a silent no-op) **does not hold for stdout**. Reported to CIO + HOST.

⚠️ **Still open, honestly scoped**: the message arrived on **stdout**. Whether **stderr** survives on exit 0 is **unresolved** — `pre-commit-reconcile-drafts.sh` writes to stderr and I saw nothing, but I could not rule out its gate short-circuiting, and my replication attempt staged nothing (`touch` + `git add` on unchanged content) so it measured an empty index. **That run was INCONCLUSIVE, not a null.** The practical fix needs neither: `exit 0` with the message on **stdout**, exactly as `check-branch.sh` already does.

## Waiting on others

- **HOST/CIO** — two hook items I deliberately did not touch: (1) staging-warn behaviour still blocks vs. stated intent; (2) `pre-commit-reconcile-drafts.sh` **header** still teaches the inverted model, incl. the backwards "promote to exit 1 (hard-block)" instruction.
- **Docs** — nothing owed; archival closed (23 files), validator shipped, calendar 0 dangling.
- **PM** — Beats 24–28 steer (**the only item with a real date**: narrative queue runs dry after Aug 18); voice-pass + art on Beats 21–23 (Aug 11/13/18); `/hooks` open or restart for HOST's memory counterweight; compose-UI restore-banner check.
- **Web/PM** — era split + featuring the current post on the blog index. My POV is in `docs/internal/planning/comms/upcoming-beats-plan.html`.

## Verified today, don't re-derive

- Beta target **2026-08-08 (Saturday, deliberate)** — `decisions.log:303`, PM Time Lord prerogative. HOST's "zero occurrences" memo was **retracted same day** (grepped `Aug 8`, missed the ISO rendering). Ship #054 line 77 carries it and is **correct — do not soften it**. Noted on the calendar row.
- Footer-tease chain across the next 10 posts: **clean**. Ships sit outside the chain (6/6 carry no tease; 7/8 narratives tease past them) — now encoded in `template-audit` v1.4.
