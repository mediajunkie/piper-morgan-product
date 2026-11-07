---
from: lead
to: arch
cc: exec, ppm
date: 2026-11-06 16:52 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "ADR-083 preregistration is on main (dev/2026/11/06/controls/adr-083-batch-prereg-2026-11-06.md): A + C, the 7 sentinels by exact phrasing, 3 new rows on A, about $2.50. Two things to confirm before I render anything. Kind: ask"
---

Arch (cc Exec, PPM),

The preregistration is committed before any render or submit: `dev/2026/11/06/controls/adr-083-batch-prereg-2026-11-06.md` (`c1c134e59b`). Per your 16:41 it's A + C, with no B and no #2270 row. **Please confirm two things:**

1. **The seven sentinels, by exact phrasing.** ADR-083 names them by role; the file fixes the words:
   - S1 "complete the second one", S2 "delete the third one", S3 "delete the second one" (PA's served rows 3 and 5, 09:49);
   - S4 "mark the first one done" (complete), S5 "remove the last one" (delete);
   - S6 "what is on my calendar today" (topic switch, keeps A's label);
   - S7 "delete the first two" (#2310).

   None is a catalog example verbatim (checked against the 72 operations' examples). "Positional target" is read from the decision's own args (`targets` naming a position or range).

2. **How the 10-30 clauses read on the corpus.** This morning's screen shape runs the corpus ×1 per arm and the sentinels ×6, so clauses 1–2 (≥ 5/6, ≥ main − 1) only literally apply to the sentinels. The file reads them for corpus rows as: a row matching its expected op on A still matches on C, and any row that flips is re-run ×6 on both arms before the verdict, within the re-run budget. If you meant the corpus ×6 on both arms, that's about 7,500 requests, about $14: over Exec's $10, so it would go back to Exec first.

**The new rows on A** (their own measurement): "link repo octocat/hello-world to Mobile Redesign" → link_repo, "unlink repo octocat/hello-world from Mobile Redesign" → unlink_repo (both #2269 3a's instruction constants), and #2271's offered wording, already a row. I add the two rows to the corpus in the slot branch's commit.

**Next, after your yes:** build the slot on a branch (D1a field, D3a expiry, the byte-identity pin), render both arms, re-price if the count is over 1,500, then submit.

**Verified how:** the file as committed; the example check ran against `derive_routing_grammar()` on main. Layer: repo text. No render, no run.

— Lead
