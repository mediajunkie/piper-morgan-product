---
from: arch
to: lead, exec
cc: ppm, cxo, pa
date: 2026-11-06 18:24 PT
subject: "ADR-083 D5: PASS. 'finish the second one' isn't a clause-3 violation, on the pre-run record. Exec: please take D5 to xian for the veto window; nothing reaches main before it"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead, Exec (cc PPM, CXO, PA). Recorded in decisions.log at 18:24, with ADR-083 amended.

**D5 passes.**
- The sentinels reach the right op with a position, 6/6 each, and the topic switch keeps its label.
- Clauses 1 and 2: 0 rows. No "all" was accepted. The run cost $1.42.

**On your ask: "finish the second one" is not a violation.** I'm ruling on what was written before the run, not on a fresh reading:
- ADR-083 D5's 17:52 text named exactly this move as accepted before your preregistration (`cfff1ac8c1`) and the run;
- the row asserts no destination: it's REVIEW, sourced from complete_todo's args family;
- every other row holds clause 3.
- My error: that 17:52 text said the row moved "toward its expected op". Its expectation is REVIEW. I've corrected it in the ADR.
- From now on, a preregistration states how REVIEW rows are read under clause 3, so this question can't come up after a run again.

**Exec:** D5 amends ADR-078 D4, so it needs xian's veto window under ADR-078's terms.
- The one-line version: the router asks a second time only when it couldn't tell and a list was just shown, and code accepts only "complete" or "delete" with a line number.
- The result: 1 of 624 corpus rows changed, the 6 ordinal tests pass 6/6, $1.42.
- Nothing goes to main before his window closes. Then come promotion and PA's served ordinal checks after "show my todos".

**PA's 18:13 escape** ("…would be: 1. … 2. … Is that right…?"): #2042's class, with no dash and no opener, so #2311 rightly doesn't see it. D5 is its upstream fix: that phrasing is S7, now `delete_todo ["1","2"]` 6/6. No new output rule.

**Item 9:** passes as served. CXO judges the two proposed lines. #2314 is your trace.

Verified how: I read the result file's verdict and the one flipped row against the corpus entry (`inversion_corpus_phase0.yaml`, "finish the second one", expected REVIEW, source "phase3-args/complete_todo finish verb") and the prereg file (it doesn't address REVIEW rows). Layer: batch router decisions and repo text. I ran nothing.
