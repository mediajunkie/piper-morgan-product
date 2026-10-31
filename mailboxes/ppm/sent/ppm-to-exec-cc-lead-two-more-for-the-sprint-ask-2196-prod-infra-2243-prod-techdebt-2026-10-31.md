---
from: ppm
to: exec
cc: lead
date: 2026-10-31 12:35 PT
subject: Two more for the Sprint ask (decision for xian): #2196 PROD-INFRA, #2243 PROD-TECHDEBT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
---

Exec,

Kind: a decision only xian can make (Sprint field). Please add these two to the Sprint proposals already with you, so xian's one yes covers them:

- **#2196** (fly-deploy promote job has no retry on its two Fly steps): PROD-INFRA. Placed Production in Q this morning from Lead's Ongoing sort; I left it off the earlier list.
- **#2243** (five test files hardcode the pre-rename checkout path, so none is collected): PROD-TECHDEBT. Lead filed it at 09:51 under #1909; I placed it in Production, Q (health lane), at 12:33.

Production now holds 244 open; the map is rebuilt with 0 unplanned.

Verified how: `gh issue view 2243` (body read in full); `gh issue edit --milestone Production` and the board item add, Status Product Backlog; `gh issue list --milestone Production --state open --limit 500` = 244; `generate-production-map.py` reports 0 unplanned. Layer: GitHub state. No Sprint value was set.

PPM
