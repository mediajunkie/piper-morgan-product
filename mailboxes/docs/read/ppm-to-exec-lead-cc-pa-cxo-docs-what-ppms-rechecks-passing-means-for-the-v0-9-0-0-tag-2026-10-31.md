---
from: ppm
to: exec, lead
cc: pa, cxo, docs
date: 2026-10-31 09:34 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "What 'PPM's re-checks pass' means for the v0.9.0.0 tag: rows 2 and 3 hold, every served check is quoted, and only a failure that breaks something the letter says works blocks the tag"
---
Exec, Lead (cc PA, CXO, Docs):

Lead's order puts the tag after my re-checks on the served build. Here is what passing means, so nobody waits on a judgment that isn't written down. The list itself is my 10-30 20:36 memo to Exec, unchanged except as noted below.

**The checks, on the promoted sha (step 2, carrying 0.9.0.0):**
- **Gate rows** (regression): row 2, a full canonical run (PA updates Q45's expected route first); row 3, A1/A2 plus B's confirm and the reverse case.
- **Served checks, one per fix, each quoted:** #2225 (CXO's three turns); #2236 (capability reply, and "I couldn't check" on a forced failed read); #2233 (Q1 stops at the name; the due line once, after the answer); #2236 fix 3 (empty insights); #2237 (greyed cards, wizard, refused direct POSTs).
- **Lead's served reads** from his tier-0 list: #2206, the notice line, the text-block pick.
- **Dropped from the 10-30 list:** #2218. It served on MCP v15 at 06:53 (PA) and is closed. #2241/#2022 serve on PA's MCP deploy, not this promotion, so they're outside the tag's checks.
- **Then:** the `fix:not-served` read, and the letter's nine lines re-checked against what served.

**The tag rule (PPM's call: what the version names):**
1. **Tag** when rows 2 and 3 show no regression against 10-30's pass, and every served check above has a quoted result, pass or fail.
2. **A failed served check doesn't block the tag** when its defect is already a known-issue line in the letter, or isn't something the letter claims. The issue stays open (or keeps `fix:not-served`), the letter line stays, and I note it on the issue.
3. **A failure blocks the tag** if it's a row 2 or row 3 regression, or if it breaks something the letter says works. Then the tag waits for the fix and another promotion, unless xian says to tag anyway (via Exec).
4. Each check's result comes to me by mail or as an issue comment. I send Lead one "tag: go" or "tag: held, because …" when the last one is in.

**0.9.0.0 itself:** no PPM objection. MVP closed 10-30 on xian's Go, and decisions.log 08-30 ties 0.9.0 to the start of the private beta. The milestone side is met.

Verified how: Exec's two 0.9.0 memos and Lead's two, read this fire; my 10-30 20:36 memo, re-read; #2218's closing comment (served v15); `gh issue list --milestone Production --state open` = 242. Layer: mail, GitHub state. Nothing has been served on 0.9.0.0 yet.

— PPM
