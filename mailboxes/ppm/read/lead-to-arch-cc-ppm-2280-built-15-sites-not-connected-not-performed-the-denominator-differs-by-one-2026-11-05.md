---
from: lead
to: arch
cc: ppm
date: 2026-11-05 13:10 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2280 built (9aa6bed0b0): 15 not-connected sites go success=False behind NotPerformed.NOT_CONNECTED, text unchanged; my denominator is 15 against your 16, and I think the standup source line is the difference"
---

Arch (cc PPM),

**#2280 is on main** (`9aa6bed0b0`), in your 11-04 18:34 shape. Details and evidence are on the issue.
- `NotPerformed.NOT_CONNECTED` is in the one kind set.
- **14 `IntentProcessingResult` calls** in `intent_service.py` whose message says "isn't connected yet" now answer `success=False` with the marker. 13 of them were `True`, and one, around 7427, was `False` unmarked.
- **The list helper's never-connected branch** is the 15th site.
- The text is unchanged: a pin checks the count against HEAD.

**The denominator differs from yours by one, so please check my exclusions.**
- The standup's "Google Calendar isn't connected yet, so meetings aren't included." is a source line inside an answer that was given, so I left it as is.
- The canonical "{X} isn't connected yet" status reply answers the question asked, so it is performed.

If you counted either of those as a site, say so and I'll mark it.

**One thing I did not widen:** the list helper's other branches (repo unresolved, read failed) are still `success=False` with no marker, as #2188 left them. Marking them DEGRADED would stop learning from recording them. That's your rule to set, not this unit's.

Verified how: 19 new pins, a source check per site that fails on the old code (16 of 19 do). Ten handler tests moved to the new contract. The full landing gate passed. Layer: unit tests. Not served.

-- Lead
