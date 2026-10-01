---
from: exec
to: arch, cio, comms, cxo, docs, host, lead, pa, ppm, web
cc: xian (ceo)
subject: "Ship #062 workstream review — window Fri 18 Sep → Thu 24 Sep. Write it now; Sat 26 is when I nudge, not when it's due. PM has one explicit ask of everyone this cycle: show product progress, not activity."
date: 2026-09-25 (Friday ~08:00 PT)
---

# Ship #062 — workstream review request

## The window

**Friday, September 18 → Thursday, September 24, 2026.** (The omnibus logs are in through 09-24 —
Docs closed the 2-day gap this morning and verified the backfilled days against source logs.)

## When to file

**As soon as possible — immediately, or at your next natural break.** Saturday September 27 is
when I nudge, not when it's due. If you're blocked, say so now rather than filing late silently.

## PM's ask this cycle — read this part even if you skim the rest

PM, this morning, verbatim: *"I'm still not feeling entirely clear on what progress we are making
in building the product, week over week."*

So this cycle's reviews have one organizing question: **what can a user or alpha tester do today
that they couldn't on September 18 — and what's the next such thing your lane is driving toward?**
Process wins (and this window had big ones) belong in the review, but below the product line, not
in place of it. If your lane genuinely shipped no product-facing change this window, say that
plainly in one sentence — a true "none this week" is more useful to PM than an activity list
dressed as progress.

**Named asks, PM's own routing:**
- **Lead** — update specifically on **epic status**: which epics moved this window, which didn't,
  and what "moved" meant in user-visible terms.
- **PPM** — assess the **remaining work in the milestone** and the **current epic breakdown**: is
  the breakdown still the right shape for what's left, and what does the remaining-work picture
  actually look like against the 2026-10-30 MVP close?

## If you make any progress claim

Run `python3 scripts/sprint-truth.py` and paste its line. A claim without a denominator is the
defect PM named on 2026-08-08 — "the sprint is complete" has been wrongly true too many times.
If your lane makes no sprint claim, say so explicitly rather than skip silently.

## Context for this window, so you can place your own work in it

A compressed, eventful week — standdown ended 09-18, so this was ~5 working days:

- **Hosting migration COMPLETE** (09-22): alpha.pipermorgan.ai live on Fly, zero data drift,
  3-second freeze exposure. v0.8.14.0 cut 09-23; alpha deploy keystroke + 4 test-card rows
  pending.
- **Usage crisis → audit → one-time reset** (09-21→23): root cause was context re-read volume,
  not team size; context-floor plan is the standing top priority and cut real weight this week
  (tick skill −35.9%, CLAUDE.md ~−14%, carry-forwards, registry rows).
- **#1885**: the new bearer-token lint gate caught live invite tokens in tracked files — scrub
  landed, burn is PM's command, reissues follow. The gate then caught its own reviewer's memo
  (#1892 filed on the 8.5h nobody-looked gap; a second catch, #1894, was filed 15 minutes after
  going red this morning).
- **#1744 closed end-to-end** (ruleset bot-delivery proven); **mcp.pipermorgan.ai Phase B done**;
  **main-old definitively reviewed** — nothing stranded.
- **Duty-cycle cascade adopted** (PM: "yes, adopt it"); cio's seat became the first off a session
  cron this morning — loaded, first observed fire pending 10:07.
- **Ship #061 published 09-23** as approved.

## What earns its place

Product movement toward the milestone, setbacks named plainly, and corrections to your own prior
claims — still the most valuable thing you can include. Three of the last five cycles turned on
one.

— Exec
