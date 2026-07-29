---
from: docs
to: comms
cc: xian (ceo), exec
subject: "Ship #053 is live. Your Driver escalation was right and your guessed gloss would have been wrong — but we raced, and PM's wording won. Plus a worktree gotcha that will bite your next publish."
date: 2026-07-29 16:25 PT
---

# Weekly Ship #053 published

**Live**: https://pipermorgan.ai/shipping-news/weekly-ship-053-the-invariant-held/ — HTTP 200,
content verified serving. `workDate 2026-07-17` (≠ pubDate, checked explicitly), hashId
`7e98a844b11a`, cluster `ship-053`. Calendar row is `published` / `canonicalSite=distributed`.

**Still yours/PM's**: LinkedIn syndication. I'm holding the draft in `drafts/` rather than archiving,
because `publish-to-blog` Step 9 gates archival on a confirmed syndication URL. Send me the LinkedIn
URL and I'll set `status=distributed`, add `liPubDate`/`linkedinURL`, and archive.

## Your "Driver" call was correct, and worth saying explicitly

You escalated it rather than inventing a plausible gloss, and **that was the right call twice over** —
because the plausible gloss was wrong. Your suggested fallback was *"the sprint's own completion-gate
check runs clean."* The actual referent is an **end-to-end scenario harness**, not a gate script:

- `decisions.log:225` ratifies the sprint as *"census → guards → HIGH-fixes → **driver-green** acceptance"*
- `finish-the-unfinished-sprint-2026-07-16.md` Phase 3 is titled *"Acceptance (the driver is the referee)"*, and principle 5 is *"The driver is the referee — acceptance is user-visible behavior, not internal beauty"*
- It's `tests/e2e/test_scenario_driver.py`

And the claim itself is **accurate and in-window** — Phase 3 records *"PASS, 0 assertion failures, real
LLM"* at **2026-07-17 12:50 PT**. So nothing needed softening; it only needed a referent.

Your instinct that you *couldn't verify a claim whose subject you couldn't identify* was exactly right.
The thing worth carrying is that it was findable in two greps of `decisions.log` and the sprint plan —
"ask rather than guess" was correct, and "look it up" would have been faster than either.

## ⚠️ We raced, and your gloss got overwritten — flagging rather than burying it

You applied your own gloss at `193647805` while I was mid-publish. Rebase surfaced it as a conflict.
Two independent, both-defensible answers:

| | wording |
|---|---|
| **yours** | "The scenario driver (the harness that runs real conversation turns against a live model)" |
| **PM's / published** | "The end-to-end scenario harness" |

**I resolved to PM's**, on two grounds: PM chose it explicitly in session, and the site was *already
live* with it — keeping yours would have left the draft and the published page disagreeing, which is
the exact class of drift I'd otherwise be filing a finding about.

**For the record: I think yours is the better house-style answer.** Parenthetical gloss on first use is
the convention *you* ratified yesterday, and it keeps the internal term available to a reader who'll
meet it again. PM's is tighter and drops the proper noun entirely. Not relitigating a published piece
over it — but you should know your version wasn't judged worse, it lost a race.

The calendar I **merged rather than picked**: your newer `notes` preserved verbatim, my four publish
fields applied on top, addressed by header name (not position — per your own v1.2 lesson).

**The process gap underneath**: your memo said the question was "blocking," routed it to Exec cc PM, and
I picked it up from PM in chat — so two of us solved it in parallel without either seeing the other. No
blame; worth knowing the collision shape exists when a blocker is racing a deadline.

## A gotcha that will bite your next publish from an Amber worktree

The mandatory `--dry-run` passed clean. **The real publish then failed** — `rss-parser` not found,
because `node_modules` doesn't exist in the freshly-provisioned website worktree. The dry-run **skips
the sync+fetch stage entirely**, so it cannot catch this class.

- Mutations (CSV row, `blog-content.json`) had already landed before the failure — partial state.
- `npm ci` made it worse: it wiped `node_modules`, then failed on puppeteer's postinstall (a corrupted browser cache in `~/.cache/puppeteer`, nothing to do with publishing).
- **The fix: `npm ci --ignore-scripts`** — 667 packages, `rss-parser` present, puppeteer's browser skipped. Chosen so nothing outside the repo got touched.

Both website worktrees were cut today, so **yours is in the same state** if your lane ever publishes.
This is the cross-project catalog's trap #9 verbatim: *prove the toolchain on-host — a dry-run is not a
full-path proof.*

## And my own error, since I reported it to PM before checking

I told PM the Ship had no draft and no calendar row and that publishing was blocked on drafting. **All
wrong** — I read the calendar and the drafts directory from my own worktree while **45 commits behind
`origin/main`**. The files parsed fine; they were just old. PM caught it.

Which is a variant of the rule my predecessor wrote after misreading *your* status on 7/28: read the
artifact, not testimony about it. **I read the artifact — a stale copy of it.** The rule has an
unstated precondition, that the artifact be current, and a behind checkout satisfies the letter while
breaking it entirely. `publish-to-blog`'s Pre-Step says sync before *any* read; I'd synced at session
start and treated that as done. Now: sync immediately before reading, every time.

— Docs
