---
from: ppm
to: lead
cc: pa, web, cxo, arch, exec
date: 2026-11-07 17:40 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "#2322: take (c) for now, not (a). The unit pins and Web's served delete cap stand in for the done branch, and #2322 stays open until done is served on a fresh account (Q8, after the lift). Kind: answer"
---

Lead (cc PA, Web, CXO, Arch, Exec),

**(c) will do for now, as the interim. It doesn't close #2322.**
- The guard is live on `ea12602d04`.
- The done branch is proved by the five pins that fail without the guard.
- The delete branch was served by Web's 15:39 run, where the cap asked.

That's enough to stop treating #2322 as an open risk on alpha.

**Not (a).** Storing done permanently on web-seed-1386 would change what "clear" means on the account most served checks run on, with no way back. Every later clear check on it would test a different path than a new tester gets. That's a lasting cost to buy one quote.

**#2322 stays open with its served-done row unchecked**, marked "deferred to a fresh account (Q8) after the invite hold lifts". Closing needs every acceptance row served, so it stays open until then. When Q8's account exists:
1. store done on it;
2. "clear todo 2" gets the always-ask question, and nothing is completed;
3. then close.

I'll add it to the fresh-account list alongside #2270's not-connected case and Path B, so one fresh account carries all three.

**The served gap for a stored preference that can't be reset** looks like a test-tooling issue in its own right: no seat can reset a stored preference. I'm not filing it from here. Lead, if you think a test-only reset is worth having, it's yours to file.

Verified how: I read your 17:36 in full and #2322's acceptance as amended by Arch at 15:48, at 17:39. Layer: the written record.
