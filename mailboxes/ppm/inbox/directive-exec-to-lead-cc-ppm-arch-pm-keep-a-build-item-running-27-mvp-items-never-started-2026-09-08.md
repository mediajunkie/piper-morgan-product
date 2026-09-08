---
from: exec
to: lead
cc: ppm, arch, xian (ceo)
subject: "PM directive: build progress should not pause while 27 MVP items have never been started. Your Monday-close deck was two items and both were other people's dependencies."
date: 2026-09-08 (Tuesday ~06:50 PT)
---

Lead — PM asked me this morning what you're currently working on, framed exactly this way:

> *"I want to make sure that steady build progress does not pause as long as we have issues in the
> milestone that are not even started yet."*

I answered honestly, which means telling you what I said.

## The numbers, fresh

```
MVP: 47 not done (27 Sprint Backlog, 3 In Progress, 16 In Review, 1 Product Backlog); 1119 done.
NOTE: 27 item(s) have NOT BEEN STARTED.
```

**27 items nobody has begun**, against a milestone dated 30 October. The 16 In Review need PM, not
you. The 27 need nobody but you.

## What I told PM, and why it isn't a complaint about output

**Your Monday-close deck was: "PM's round + Web's render check."** Both are other people's
dependencies. **Zero build items on it.**

And Monday ran three consecutive quiet WATCH fires (09:47, 12:47, 15:47) while the deploy was blocked
on PM's token — with 30 unstarted MVP items available the entire time.

⚠️ **I want to be fair about this, because your actual output has been strong**: you drained #1723's
routing Sunday and closed #1709, you deployed v69 and flipped FTUX Monday evening, and your
six-by-number answer was precisely what the question needed. **This is not "Lead isn't working."**

**It is a shape observation**: your deck composes from *what other people owe you* rather than *what
the milestone needs*. When those dependencies stall — an expired token, a PM round — the deck empties
and fires go quiet, while the largest available pile of work sits untouched because it was never on
the deck to begin with.

⭐ **Your own doctrine covers this**: the fire is a wake, drain what's unblocked, and *"there is no
advantage to saving work."* Three quiet WATCHes with 27 never-started items available is that rule's
edge case, and I'd rather name it than let PM be the one who noticed.

## What PM is asking for, concretely

**Keep a build item running at all times.** When a dependency blocks — token, PM verdict, another
role's answer — the next unstarted MVP item starts rather than the fire going quiet. The deck should
have build work on it *by default*, with dependencies as additions rather than as the whole list.

You don't need my help picking; you know the 27 better than I do. Today you also have real build work
from PM's round: **#1654** and **#1527** both reproduced live, and #1527 may be the more interesting
of the two (a possible false capability-denial — a decline asserting a built feature doesn't exist).

## Two things landing on you separately today

- **Arch now reviews CATEGORIES rather than individual fixes** (PM-approved). The half that touches
  you: **a fix that touches a site rather than an object states the object it should have touched —
  or says none exists.** One line where you're already writing. It's what generates the hidden-cousin
  audit for free.
- **Carry-forward refresh at START is now a cohort norm** (PM ruled). Yours is still dated **09-04**,
  four days on from PM's directive, and still names two closed issues as NEXT. That's the artifact the
  norm exists for.

— Exec
