# Comms carry-forward

*Rewritten at the 2026-08-03 STOP fire (21:42 PDT). Ephemeral session state only — durable owed/queued items live in `comms-standing-items.md`; the canonical record is the session log.*

## Cron

- Job `e37fa867` · `12 6,9,12,15,18,21 * * *` · verified live at every fire on Aug 3. **Auto-expires ~2026-08-09** — re-arm before then.
- Registry row in `dev/active/duty-cycle-registry.tsv` matches.

## The one dated thing

**Tomorrow (Tue Aug 4) publishes "The List That Lies."** At last check: **1,901 words** (target 800–1,300, `template-audit` flags >1,600), **never voice-passed**, **no art** (frontmatter `image`/`alt`/`caption` all empty), and **one open `[PM: …]` bracket at line 39**. All four need PM. Named cut candidate if PM wants one: the three-agent collaboration paragraph — it's lovely and it's a separate story.

**Wed Aug 5 publishes Weekly Ship #054 "Clear Is Not a Measurement"** (Exec-drafted). Not yet audited by me — **its pre-pass is due tomorrow**, after the Aug 4 post is handled.

## Open PM questions — 4 across 3 posts, best answered in one pass

| post | pubDate | question |
|---|---|---|
| *The List That Lies* | **Aug 4** | Was the Jun 29 gate removal on the live server PM's own? |
| *Drained on Paper* | Aug 6 | Who declared the backlog drained? Does the dishes/baby line land as written? |
| *No Undo* | Sep 12 | Is the babysitter/baby analogy PM's own framing? |

Surfaced only because `template-audit` check #5 was blind to `[PM: …]` until Aug 3. **No bracket ever reached a reader** — verified against the live page.

## Owed by me, with a named trigger

⚠️ **The PreToolUse exit-0 observation, promised to HOST + CIO.** `pre-commit-reconcile-drafts.sh` prints to stderr on exit 0 on *every* commit touching `docs/public/comms/drafts/`. **Trigger: my next such commit** — i.e. tomorrow's voice-pass/art commit. Report whether the line surfaces to the agent. **A null result IS the finding; report seeing nothing if I see nothing.** Do not stage a synthetic probe, and do not infer from the three PostToolUse exit-0 hooks — that cross-event inference is what caused the original defect.

## Waiting on others

- **HOST/CIO** — two hook items I deliberately did not touch: (1) staging-warn behaviour still blocks vs. stated intent; (2) `pre-commit-reconcile-drafts.sh` **header** still teaches the inverted model, incl. the backwards "promote to exit 1 (hard-block)" instruction.
- **Docs** — nothing owed; archival closed (23 files), validator shipped, calendar 0 dangling.
- **PM** — Beats 24–28 steer (**the only item with a real date**: narrative queue runs dry after Aug 18); voice-pass + art on Beats 21–23 (Aug 11/13/18); `/hooks` open or restart for HOST's memory counterweight; compose-UI restore-banner check.
- **Web/PM** — era split + featuring the current post on the blog index. My POV is in `docs/internal/planning/comms/upcoming-beats-plan.html`.

## Verified today, don't re-derive

- Beta target **2026-08-08 (Saturday, deliberate)** — `decisions.log:303`, PM Time Lord prerogative. HOST's "zero occurrences" memo was **retracted same day** (grepped `Aug 8`, missed the ISO rendering). Ship #054 line 77 carries it and is **correct — do not soften it**. Noted on the calendar row.
- Footer-tease chain across the next 10 posts: **clean**. Ships sit outside the chain (6/6 carry no tease; 7/8 narratives tease past them) — now encoded in `template-audit` v1.4.
