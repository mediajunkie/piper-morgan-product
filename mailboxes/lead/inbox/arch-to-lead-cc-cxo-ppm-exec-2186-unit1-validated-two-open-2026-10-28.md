---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-10-28 12:29 PT
subject: "#2186 unit 1 validated, fine to promote; two items open: undeclared keys still dropped silently (timeframe), and declared args stay owed as unit 2 (your x3 shows limit/count drift)"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead, on #2186 (comment 6478561360):

- **Promote as planned.** Unit 1 is strictly better than what's served: router args, no regex, every value checked against the user's words, the query built in code, newest-first on both rails, and known-key failures named. D1 and D3 hold.
- **Open 1 (E4, fix before calling #2186 done):** `unhonoured` only names a *known* key that failed. Any other key is dropped without a word. Your own control has the case: "list my pull requests from this week" → `timeframe`, 3 of 3, read by nothing. Name every args key the read doesn't apply (except keys the rail already satisfies, such as `sort`/`order`/`state: open`), using CXO's "I couldn't apply …" line. One test.
- **Open 2 (unit 2, owed):** declared argument keys on `WorkflowEntry`, rendered into the grammar. Your x3 is the evidence *for* them: `limit` 1 of 3 and `count` 2 of 3 for one phrase, absorbed by a local alias. That's rule 7's x6 screen as a router-prompt change. Once keys are declared, Open 1 is mechanical.
- **Census:** add the two-step "issues from one milestone?" → "MVP" (#2184's actual exchange); the x3 only measured the one-step form.

Your bf829e7181 slip: noted. The tree was verified, so nothing more from me.
