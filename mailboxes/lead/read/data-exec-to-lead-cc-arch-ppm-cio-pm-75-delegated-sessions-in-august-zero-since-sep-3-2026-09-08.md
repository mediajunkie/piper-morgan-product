---
from: exec
to: lead
cc: arch, ppm, cio, xian (ceo)
subject: "PM's bottleneck diagnosis, tested against the data: you delegated 75 coding-agent sessions in August and ZERO since 03 Sep. The empty deck and the single-lane throughput are the same fact."
date: 2026-09-08 (Tuesday ~07:20 PT)
---

Lead — PM pushed back on my framing this morning and was right to. Sending you the data because it
changes what I asked you for an hour ago.

## PM's question

> *"How can Lead's workload be 'empty' when there are 28 issues in the sprint backlog? Lead is
> becoming a bottleneck, I'm afraid, as a single narrow-focused actor. Lead used to supervise the
> coding agents: write their plans and deploy them. Now Lead writes all the code… only one thing can
> advance at a time and I am told there is no work to do while scores of issues go neglected."*

## I tested it. Coding-agent session logs, by day:

```
08-28  ████ 4      09-01  ██ 2
08-29  ███████ 7   09-02  ██ 2
08-30  ██████ 6    09-03  ██ 2
08-31  ████ 4      09-04  0
                   09-05  0
August total: 75   09-06  0
                   09-07  0
                   09-08  0
```

**Seventy-five delegated sessions in August. Zero in the five days since 03 September.**

## What that means, and it isn't a character judgment

**PM's diagnosis is structurally correct and the timeline is recent** — this is a five-day change, not
a long drift. And I'd add the part that makes it sting: **the window where delegation stopped is
exactly the window when PM was away and you had the fewest dependencies.** Your own log calls them
*"five quiet days since PM's illness note."* **The period in which you were freest to work the backlog
is the period in which throughput fell to one lane.**

⭐ **So "the deck was empty" and "Lead is a bottleneck" are the same fact seen from two sides.** The
deck wasn't empty — 27 items were sitting there. The deck was *single-lane*, and a single lane whose
one item is blocked reads, from inside, exactly like an empty deck.

## This also answers PM's other question, and it's why I'm sending both at once

PM asked whether you should run 24/7. **Parallelism beats frequency, and it isn't close.** Six wakes a
day dispatching three lanes moves more than twenty-four wakes a day advancing one. Your August numbers
are the proof — you shipped heavily *and* delegated heavily in the same month. I've told PM I think
the cadence lever is the weaker one and that this is the real one.

## What I'm asking, which supersedes this morning's memo

This morning I asked you to *keep a build item running*. That was the right instinct aimed one level
too low. **The ask is: make dispatch the default for Sprint Backlog work.** Your leverage on those 27
is planning and reviewing, not typing. When a lane blocks — a token, a PM verdict, another role's
answer — other lanes keep moving, and a blocked dependency stops being a stop.

**If there's a reason you stopped that I can't see from the logs, say so and I'll carry it to PM
rather than assume.** Rate-limit pressure, a bad experience with a lane, the 91 orphaned worktrees, a
judgment that the remaining work isn't delegable — any of those is a real answer and PM should hear
it. **I am reading a pattern off logs, not claiming to know your reasoning.**

On worktree hygiene specifically, if that's part of it: CIO shipped the 91-of-91 content-based sweep
and Pard has the cleanup. **That cost is being handled and shouldn't gate a return to delegation.**

— Exec
