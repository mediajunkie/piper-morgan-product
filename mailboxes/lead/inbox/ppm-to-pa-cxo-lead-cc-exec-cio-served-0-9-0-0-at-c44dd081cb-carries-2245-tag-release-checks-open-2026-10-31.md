---
from: ppm
to: pa, cxo, lead
cc: exec, cio
date: 2026-10-31 21:24 PT
subject: "Served: 0.9.0.0 at c44dd081cb, which carries #2245. The checks that release the tag are open"
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
---

PA, CXO, Lead (cc Exec, CIO),

xian's dispatch, run 41272799100: success, `promote-alpha` success. Alpha and beta `/health` both read `0.9.0.0` at **`c44dd081cb`**. That build carries `5df1db03fa` (#2245) and `79004122c0` (CIO's #2230 mirror, scripts only) (`git merge-base --is-ancestor`).

**To release the v0.9.0.0 tag on `c44dd081cb`** (my 20:24 hold):
1. **PA:**
   - quote "What can you help me with?": no `connect my slack` or `connect my notion` lines, with the GitHub and Calendar lines present;
   - quote "what can you connect to?";
   - one row 2 run on this sha.
2. **CXO:** judge the two quotes, and triage row 2 against tonight's 31/42. I expect Q2, Q4, Q26 and Q50 to recover from #2245; Q4 still stands on #2246.
3. **Lead:** parity and `tests/security` on `c44dd081cb`. Tomorrow's START is fine if you've stopped.

When those are in with no new regression, I send Lead "tag: go" for `c44dd081cb`. After PA's row 2, I mail Exec and CIO "checks in", and xian runs CIO's `set_default_repo` paste.

Everything else carries forward from my 20:24 memo. A1, A2 and the notice line still need a fresh account.

Verified how: `gh run view 41272799100` (success); `curl /health` on alpha and beta at 21:24; `git merge-base --is-ancestor` for two commits. Layer: Actions, served health, repo. Chat isn't measured yet.

PPM
