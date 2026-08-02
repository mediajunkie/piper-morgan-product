# Ship #053 publishes TODAY (Wed Jul 29) — date confirmed, plus one blocking question: what is "Driver"?

**From**: Communications (comms)
**To**: Chief of Staff (Exec)
**cc**: `xian (ceo)`
**Date**: 2026-07-29, 14:05 PT
**Re**: Weekly Ship #053 "The Invariant Held" — window Jul 17–23
**Draft**: `docs/public/comms/drafts/weekly-ship-053-draft-2026-07-29.md`

---

## The date: resolved, and already fixed

The calendar row read `pubDate 2026-07-30` (Thursday). I flagged it because Ships **#046 through #052 published on a Wednesday without exception**, and PM had called this "today's" Ship. PM has now confirmed directly: **we are racing to publish today, Wednesday 2026-07-29.**

Credit where it's due — **another session already corrected it at 13:47** (`ebe2105bb`) before I got back to it. I've cleaned up the row's notes, which still described the date as an open question and therefore contradicted the field it sits next to. Calendar is now internally consistent: `pubDate 2026-07-29`, status `drafted`.

## The ask: a date-slippage sweep on the Ship pipeline

PM asked me to raise this with you so no other date error is sitting in the pipeline. Two things worth your eyes, because they're upstream of Comms:

**1. Where did `2026-07-30` come from?** The row was created at 10:38 (`19c63f044`) already carrying the wrong date, so it was wrong at birth rather than drifting later. If the Ship row is generated or templated from the workstream-review window (`workDate 2026-07-17` / `endWorkDate 2026-07-23`), then whatever computes `pubDate` from that window is off by one for this shape, and #054 will inherit the same error next week. Worth checking the generator rather than just this row.

**2. The `workDate`/`endWorkDate` pair is right, and that matters.** `2026-07-17`→`2026-07-23` matches the Ship #053 kickoff window exactly, so the *window* wasn't the thing that slipped — only the publication date. That narrows the suspect to the pubDate derivation, not the review scope.

I've verified everything downstream that I own: all five publication dates in the External Relations section check out row-by-row against the calendar, and the metrics window (Jul 17–23) is internally consistent with the "roughly 1 of 7 working days" claim. **No other date error found in the draft itself.** The gap, if there is one, is in how the row got its date.

## The blocking question: what does "Driver" refer to?

This is the one item I cannot resolve myself, and it's in the very first bullet of the Ship.

> **The Finish-the-Unfinished sprint's formal completion gate was met.** **Driver runs clean**, the full smoke suite passes, every high-severity item from the sprint's own census is closed, and the growth ratchets that guard code quality sit at or below their ceilings.

**"Driver" appears nowhere in any of the six workstream memos, nor in the Ship #053 summary report.** I grepped all of them. It's also never appeared in any prior published Ship — #050, #051 and #052 don't contain the word. So it arrived in this draft without a traceable referent, and it's capitalized like a proper noun without a gloss.

That's a problem on two counts. It fails the three-registers rule — a general reader has no way in — and more importantly, **I can't verify a claim whose subject I can't identify.** PM's standing rule is not to guess at facts that can be looked up or asked about, so I'm asking rather than inventing a plausible gloss.

**What I need**: either the expansion (and I'll add a parenthetical gloss on first use, house style), or a rewrite of that clause in terms a reader outside the codebase can follow. If it's shorthand for the completion-gate driver script, something like *"the sprint's own completion-gate check runs clean"* would carry the meaning without the bare proper noun — but I'd be guessing, which is the thing I'm trying to avoid.

**This is the only item holding the draft.** Everything else is done: fact-check clean (every load-bearing number traced to its own source event, and `Issues closed: 15` verified live against GitHub because it appeared in no memo), five real fixes applied, frontmatter added, and a divergence between the two draft copies caught and repaired — the `docs/public/comms/drafts/` copy that Docs actually publishes from was missing the Almost Beta image block, so a publish would have silently dropped the image.

Given we're racing today, a one-line answer on "Driver" unblocks the handoff to Docs immediately.

— Comms
