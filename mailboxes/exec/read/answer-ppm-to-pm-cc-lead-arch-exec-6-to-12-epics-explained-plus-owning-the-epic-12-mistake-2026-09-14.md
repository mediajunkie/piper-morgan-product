---
from: ppm
to: xian (ceo)
cc: lead, arch, exec
subject: "Answering directly: why 6 became 12 (now 11), and owning the one call in there that was actually wrong."
in-reply-to: 2026-09-14-1732-lead-PM-ASKS-why-12-epics-when-they-last-heard-6-please-explain-directly.md
date: 2026-09-14
---

xian —

Two things, and I want to keep them separate: the epic-12 mistake (already fixed, reopened epic 2
per your ruling), and the honest answer to why the count grew at all.

## First, the mistake — fixed, not defended

You were right to overrule epic 12. I created a successor epic instead of reopening epic 2, and my
own reasoning was exactly the thing your ruling names: I was protecting "epic 2 is closed" as a
fact on the page, when the truer fact was "epic 2 wasn't actually complete." Those aren't the same
claim, and I optimized for the one that felt better rather than the one that was true. Lead
proposed the successor-epic shape, but I approved it — that's mine to own, not something I can let
Lead carry alone. Epic 2 is reopened now, all six new items folded back in, epic 12 retired. Fixed
in the order doc, pushed.

## Second, the count — the honest structural answer

You asked whether there are really 12 distinct tracks, or scope creep in the epic design. Here's
what actually happened, as plainly as I can put it:

**The 37 items didn't grow.** Arch factored the original Sprint Backlog into 8 cause-groups plus 7
honest singletons on 09-09, at your own directive ("factor the backlog over Arch's six cousins").
I built the ordered epic list from that factoring — same 37 items, organized by cause instead of
symptom.

**Three of the count went from 8 to 11 because of your own 09-12 ruling**, not because I invented
new tracks: you said every MVP item needs an epic home, no exceptions, no ungrouped pile. Three
genuinely new findings this week (a try/except pattern that hides broken features, the chat
composer needing to grow instead of scroll, a schema-validation workflow finding missing domain
converters) didn't fit any of the 8 existing groups. Rather than force them in somewhere they
didn't belong, or leave them in an unsorted list your own ruling had just retired, I gave each its
own epic. That's 11.

**The 12th was the mistake**, now corrected back to 11 — see above.

**So the honest framing**: the growth from "6 or 8" to 11 is mostly your own two rulings compounding
(factor by cause, then give every orphan a home) plus real new discoveries, not epic-count
inflation from me freelancing. The one place I actually got it wrong was epic 12, and that's fixed.

## The question underneath your question, which Lead flagged and I think is the real one

Is an epic a *track of work* or a *bucket for things that don't fit elsewhere*? Three of the 11
(epics 9, 10, 11) carry 1-3 items each. I can defend each individually — none of them share real
membership with anything else, so forcing them into a bigger group would have been the same
"looks-tidy, isn't-true" mistake as epic 12. But I'd rather give you the actual choice than assume
my definition is the right one:

- **Keep them as epics.** Each is a real, if small, unit of work Lead can pick up and close on its
  own terms, and the epic-relative view stays complete — nothing sits outside it.
- **Or: revert to a short named list** ("other MVP work — not grouped, not urgent") for anything
  under some size threshold, and reserve "epic" for genuinely multi-item tracks. This is simpler
  and probably closer to what "epic" means colloquially. The cost is exactly the thing your 09-12
  ruling was trying to avoid — an unsorted pile, even a small one — so I'd want your explicit call
  on trading that back in for simplicity, not do it on my own read.

I lean toward keeping them as-is (mostly because the alternative reintroduces the exact structural
gap your ruling closed nine days ago), but this is genuinely your call on how the roster should
read to you, not a technical question I should decide alone. Tell me which you want and I'll make
the file match immediately either way.

— PPM
