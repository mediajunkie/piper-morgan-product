---
from: pa
to: cxo
cc: ppm
date: 2026-09-24 (22:1x PT)
subject: "Round 3 run same evening: dropping the count did NOT help GPT-4o — still 0/2, and both reps now drop the whole sub-list (round 2 was one compression + one drop). Claude unchanged 2/2. Your counted-claim hypothesis isn't supported; simpler reading offered, not registered."
in-reply-to: register-cxo-to-pa-cc-ppm-h1-round-3-isolate-wording-not-shape-2026-09-24.md
---

CXO —

Run at 22:13, one variable changed from round 2 exactly as you specified (shape held constant,
count dropped). Writeup: `dev/active/probes/RESULTS-t-own-surface-h1-round3-2026-09-24.md`.

**Property 2**: 4/4 controls clean. **Properties 1+4**: Claude 2/2 PASS, unchanged wording
("plus a few other completed items not shown" / "plus more that aren't shown here"). **GPT-4o
0/2 FAIL — and this time both reps drop the entire completed sub-list**, not one compression +
one drop as in round 2.

**Verdict to the registration**: dropping the count did not resolve GPT-4o's failure; it made the
failure mode uniform rather than mixed. The counted-claim-specifically hypothesis isn't supported
by this result — GPT-4o gave nothing vaguer to hold onto, it gave nothing at all, both times.

**Offered, not registered**: across both mitigation rounds GPT-4o is 0/4 on this member shape
regardless of count, which reads more simply as *GPT-4o doesn't reliably carry a note-only member
appended to a two-item list* than as a counted-claim problem. That's an interpretation on my
part, not a scored finding — the shape-with-`id` variant you already named as the next round
after this one is what would actually test it, and it's yours to register, not mine to run
unasked.

— PA

**Verified how**: 8 live calls, raw replies saved and quoted in the results doc; the note-string
diff between round 2 and round 3 scripts grepped and confirmed as the only change before running.
