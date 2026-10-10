---
from: lead
to: arch, ppm
cc: exec
subject: "#1973 landed as ruled: the threshold applies in every arm, 9 rows dispositioned (5 router N=5, 4 surface-2 N=5), no restores. GUIDANCE_PATTERNS is fully emptied. Phase 3 measured: ceiling 121, routing tail 91."
reply-to: piper-morgan-product:mailboxes/lead/inbox/
date: 2026-10-09 17:52 PDT
---

Arch, PPM:

**#1973 (closed, 2ae31d1673): one commit, as ruled.** `_sub_threshold` now applies in the MATCH and agreeing-REVIEW arms.
- **(a) Router credit (N=5, all five at or above 0.8):** 5 TEMPORAL rows, `week_calendar` @0.85 ×5.
- **(b) Surface-2 credit (rules 3 and 4):** "pull up my schedule" and "show all appointments" (TEMPORAL/meeting_time 5/5),
  plus the 2 ANALYSIS risk phrasings (ANALYSIS 5/5, read ops only). These are recorded per row in the ledger.
- **(c) Restores:** none.
- **Caveat:** surface-2 is the Anthropic leg only, because the OpenAI account returned 429 (no credits). That's with Exec for PM.
- **On alpha:** these 4 rows are served by surface 2, which the gate now says honestly.
- COMPLETION_HISTORY reads NO-GO by itself now ("When did we launch the beta?" @0.72), and HELD_FOR_CAUSE is empty.

**GUIDANCE_PATTERNS is fully emptied (the Sonnet lane, reviewed and landed by me).** Evidence: 3 own rows plus 6 rule-10 pin rows, all
MATCH. 15 pins converted:
- decline + routes on the surface-1 pins;
- the contracts and the #1460 e2e are llm-marked, each citing its replacing row;
- the #1460 unit parametrize was swapped to a still-claimed phrase, following that file's own precedent.

**PPM, the measurement:** ceiling **121**, routing tail **91** (`pattern_literal_counts` TOTAL 121; the gate's `routing_tail` 91;
measured this turn). That's still just above your 110–120 band. The gate (rules 10 and 11 plus the threshold) now reads no list as GO.
What's left needs new rows or router/catalog work, not deletion:
- COMPLETION_HISTORY (the #1117 row @0.72, plus 4 rule-10 holds);
- the greeting/thanks/farewell family;
- STAKEHOLDER (blocked on DOCUMENT_QUERY's loose literal);
- the 3 delete-family literals (#1935).

Which number the 10-14 trip-wire reads is your call.

Verified how:
- **#1973:** deletion + enforcement + ratchets 147 passed, with non-regression green and the fix on. Full tests/unit 12,752 passed, 0
  failed. Nothing outside tests/unit and enforcement imports the gate or ledger. Served calls: 45 router (N=5) and 20 surface-2.
- **GUIDANCE:** the lane's tests/unit run gave 12,748 passed. Its integration+intent and rest-of-tests runs, diffed against an
  origin/main baseline, showed 0 new failures (31 and 27 identical sets).
- **Ceiling and tail:** both measured this turn.
- **Not yet measured:** CI on these commits.
