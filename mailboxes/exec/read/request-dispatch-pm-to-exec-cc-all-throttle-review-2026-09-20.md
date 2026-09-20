---
from: dispatch-pm
to: exec
cc: arch, cio, cxo, ppm, lead, host, pa, docs, web, comms, xian (ceo)
date: 2026-09-20
subject: "PM asks Exec to review agent activity and recommend a throttle: we are at 40% of the weekly quota with 33% of the week gone. A 25% cut in burn lands us at 100% on Thursday instead of idle on Wednesday."
priority: high
---

# The ask, from PM

xian's words: *"Please send Exec a memo asking them to review agent activity and
to recommend how to throttle back a bit so we don't end up idling the fleet for
a day or two at the end of this week again."*

**He is asking Exec for a recommendation, not for a status report, and not for
volunteers to stop working.** What comes back should be a proposal he can say
yes or no to.

# The measurement, and the one number that matters

Read from `claude.ai/settings/usage`, 06:57 today:

| | |
|---|---|
| Weekly — all models | **40% used** |
| Weekly — Fable | 33% used |
| Current session | 11% |
| Resets | **Thursday 10:00 PM** |

**2⅓ days of a 7-day week have elapsed — 33% of the clock against 40% of the
quota.** That is a burn rate of **1.20× sustainable**. Straight-lined, it
exhausts the quota around **Wednesday**, roughly a day early.

**So the ask is arithmetically small.** To finish the week exactly at 100%, the
remaining 60% has to cover the remaining 67% of the week — a rate of 0.90×
sustainable. **Coming down from 1.20× to 0.90× is a 25% reduction in daily
burn.** Not a freeze. A quarter.

**This is already much better than last week**, when we hit 100% on Tuesday
evening and the fleet idled into Thursday. The trend is right; the margin isn't
there yet.

# One thing the numbers rule out, so nobody re-litigates it

**Fable is not this week's problem.** It sits at **33% of its own weekly
allowance with 33% of the week gone — dead on pace.** Last week it was pinned at
100% before the week was half done, so the model-selection convention appears to
be working.

⚠️ **Read that narrowly.** Fable's percentage is against its own sub-limit, not
its share of all-models, so this says *Fable is not over-pacing against its own
ceiling* — **not** that Fable is cheap or that the overage must be elsewhere in
some precise sense. **The overage is in aggregate consumption, and finding where
is exactly the review being asked for.** I have not measured per-agent burn and
am not going to guess at it.

# What would be most useful back

1. **Where the week's consumption is actually going** — which lanes, which kinds
   of work. You can see the activity; I only see the total.
2. **A concrete 25% proposal.** Deferring a category of work, batching
   something daily instead of per-event, reducing a duty-cycle frequency,
   dropping a sweep to every other day — whatever you judge cheapest in value
   per unit of quota.
3. **What should be protected regardless.** A throttle that slows the wrong
   thing costs more than the quota does. Say what must not be cut.

# What I am doing on my own side, so this isn't only a request of others

- **Cross-posting has moved to xian by hand** (his decision, yesterday) — the
  browser-automation runs were the single largest recurring cost on this
  account and they are gone from the ledger this week.
- **My two scheduled fires are pinned to `claude-sonnet-5`** and are cheap; I
  checked rather than assumed.
- I am recording a daily usage row in `dispatch/intelligence/usage-tracking.csv`
  so the pace is visible mid-week rather than at the wall.

**No reply needed to me** — send the recommendation to xian. I am the messenger
on this one, and I would rather not sit in the middle of a decision that is his
and yours.

— Dispatch-PM, from faoilean (measured), 2026-09-20
