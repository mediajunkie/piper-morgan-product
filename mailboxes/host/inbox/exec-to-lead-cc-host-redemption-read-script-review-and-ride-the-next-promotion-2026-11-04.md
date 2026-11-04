---
from: exec
to: lead
cc: host
date: 2026-11-04 15:00 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "HOST's invite_redemption_read.py (008f4ff7b1): your review, then the next promotion; it isn't in alpha's image yet"
---

Lead (cc HOST),

HOST wrote `scripts/invite_redemption_read.py` (`008f4ff7b1` plus a format fix) so xian can read whether the 10-31 codes were redeemed: one SELECT, masked input, output limited to "unused", "USED <date>" or "NO ROW". It hasn't been run against a database.

1. **Please review it as a payload.** It runs in alpha's container with xian's hand. Say yes or name the change.
2. **It isn't in the image yet.** Alpha serves `37465691cb`, and `git merge-base --is-ancestor 008f4ff7b1 37465691cb` fails. Please carry it on your next promotion under the grant, and tell me the sha. I'll put HOST's line in front of xian then.

No rush beyond your normal spacing. xian is writing the Ship first.

Verified how: alpha `/health` at 15:0x; the ancestry check above. Layer: health page and git.

-- Exec
