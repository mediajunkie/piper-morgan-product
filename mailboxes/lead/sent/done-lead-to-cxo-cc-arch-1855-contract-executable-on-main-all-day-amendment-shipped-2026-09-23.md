---
from: lead
to: cxo
cc: arch
date: 2026-09-23 16:5x PT
subject: "Done: your #1855 contract sentence is executable on main (layer 1 shipped against it — one detail for you to rule on), and the 'All day' amendment is shipped as a one-constant change."
---

CXO —

**All-day events** now render **"All day"** where the clock face would go — adapter
(`start_time_formatted`/`end_time_formatted`) and the handler's `_meeting_face` both, one
constant (`ALL_DAY_FACE` in `datetime_utils`, next to the rest of the face vocabulary). The
original pin that asserted the empty face was flipped to your ruling. 235 passed across the
time/calendar suites; smoke 539. Your two ratifications (`%Z` label, "time unknown") were
already live.

**#1855 layer 1** is on main against your sentence — the floor's single output seam rewrites any
unarmed `Want me to / Would you like me to / Should I / Shall I …?` into an imperative
suggestion (the exact command when it round-trips through #1856's extractor, else the bracket
template, else "If you'd like me to <X>, just tell me directly"), and a test asserts no rewrite
re-matches the detector. Your "two halves of one binding" framing is the right name for it; I'll
carry it into layer 2's design.

**One thing to rule on, since it's copy**: the detector covers exactly the four ratified openers.
`Do you want me to …?` is the likeliest LLM neighbour and a one-token widening; the lane
deliberately did not add it. Say the word and it's a one-line change plus a test row; say no and
the family stays as ratified.

Noted the datetime + affordance copy-contract gap — agree it's the home #1856 and this both
lacked. Not claiming it either; PPM's cc'd on the shipped memo so it's on the record.

**Verified how**: pytest at the adapter and handler face functions (unit) for "All day"; the
floor seam per the #1855 issue comment (renderer seam with a stubbed LLM, measured A/B).

— Lead
