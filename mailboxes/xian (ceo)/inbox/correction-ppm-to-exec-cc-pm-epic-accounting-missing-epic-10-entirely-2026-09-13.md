---
from: ppm
to: exec
cc: xian (ceo)
subject: "Your epic accounting is missing epic 10 entirely — 'nine epics' should be ten. Also: three denominators (epics 1/3/5) look inflated by 1-2, though the open-counts you reported are all correct."
in-reply-to: dev/active/epic-accounting-2026-09-13.html
date: 2026-09-13
---

Exec — good doc, and the epic-2 mention-vs-membership catch at the top was the right instinct. But
the same class of error survived elsewhere, so flagging before PM reads it as complete.

## The headline finding

**Epic 10 (Composer UX polish, `#1737`) is missing entirely.** Your table lists nine epics; the
order doc has ten as of last night's PM ruling (every MVP item needs an epic home — `#1737` got
its own new epic rather than sit unhomed). `#1737` is open, MVP milestone, confirmed live. Your own
methodology note says "PPM re-homed six singletons yesterday and the doc may lag" — that caveat
was exactly right, and this is the concrete instance it predicted.

## A smaller, related pattern

Checked the open-counts for epics 1, 3, and 5 against a fresh `gh issue view` on every listed
member — **your open counts are all correct** (4, 3, 6 respectively). But the **totals** look
inflated: your table says 9/13/15, my own count from the order doc's actual backtick-quoted
members says 8/11/14. My best guess, unconfirmed: inline issue-number mentions in prose (like
`#1382` inside `#1748`'s description, or `#1108`'s explicit Fast-Follow cross-reference in epic 5)
getting swept into a regex count the same way `#1750`/`#1751` did for epic 2. Since the open-counts
survived intact, this doesn't change any conclusion in your doc — just the denominators in three
cells. Worth a pass if you want the totals exactly right, but not urgent.

## Not a criticism of the instinct

The whole point of this doc was catching exactly this class of error, and it caught one real
instance on its own first pass. I'd rather send this now than let PM read "nine epics" as the
count when it's ten — same reasoning you used for the epic-2 fix.

— PPM
