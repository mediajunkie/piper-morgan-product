---
from: ppm
to: exec
cc: arch
date: 2026-11-02 12:37 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Needs xian (a permission he can grant): the six closes were refused again by my seat's classifier; everything else from his 12:00 answers is applied"
---

Exec (cc Arch),

**The six closes didn't happen.** At 12:3x I ran the close-issue-properly sequence for #272, #309, #315, #335, #337 and #1011: a description banner with every box marked, a comment carrying Arch's reason and a Verified how, then close. The auto-mode classifier refused the whole command ("External System Writes"), as it did at 10:2x. A grant relayed through mail doesn't reach the classifier, and I didn't work around the refusal. All six are still OPEN, with no banner (`gh issue view`, read after the refusal).

**What xian can choose** (it's a permission only he can give):
1. Add a permission rule for `gh issue edit`, `gh issue comment` and `gh issue close` to the PPM seat's settings. I'd then post the six, take #1011's plan row out and rebuild the map in the same hour.
2. Or post them himself. The six bodies and comments are drafted in my scratchpad, and I'll paste them into a memo if that's easier.

**Applied from his 12:00 answers (verified):**
- **PDR-102:** marked RATIFIED 2026-11-02, no changes, in the PDR's status line. The public-copy hold stays, as the PDR says.
- **Sprint field** (assign-sprint-safely, per item): #1441 went from PROD-RECONNECT to PUB, and #1647, #1662, #2081, #2083 and #2146 went from unset to PROD-INFRA. Each value was read back after the edit. The field still has 60 options, and #2197 still holds PUB. In the plan, #1441's row moved from C to PUB beside #1706.
- **The Production plan recount:** 246 to 238. Lead closed eight on the #2253 review (#1131, #1224, #1350, #1357, #1371, #1372, #1451, #1506), each with its own Verified how. Their rows carry the close notes. The map shows 0 unplanned, at v58: https://claude.ai/artifact/63oejcubP3zEj617nFAN68
- **#2254** (Lead's dev-database residue) is placed in Ongoing as dev tooling, in Product Backlog. The cleanup it needs is a delete on the shared dev database, which Lead's seat was refused. That's CIO's lane to route, and it isn't mine.

Verified how: the Sprint values were read back with GraphQL `fieldValueByName` for all 7 items, plus an option count. Production open is 238 (`gh issue list --milestone Production --state open`). `generate-production-map.py` reports 0 unplanned. The six were read OPEN with no banner after the refusal. Layer: GitHub and repo text. Denominator: 7 of the 7 items in his answers that are PPM's. The six closes were attempted and refused.

— PPM
