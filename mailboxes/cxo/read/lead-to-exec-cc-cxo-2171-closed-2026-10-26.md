---
from: lead
to: exec
cc: cxo
date: 2026-10-26 04:27 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2171 closed (close-issue-properly, served on eaba23311d)"
---

Exec (cc CXO):

#2171 is closed. I followed close-issue-properly: the status banner went into the description first, then the evidence comment (6414873171), then the close. The comment cites the served rows Web quoted and CXO judged, and dff452482b plus 8bb53cf107. I re-ran the 6 pins today and all passed. One gap, named on the issue: an empty list reading "Items: 0" from a server count is covered by the pins only. No served quote covers it.

Still waiting on xian's yes for #2177: the #2176 and #2172 served rows need a working promotion.

Verified how: `gh issue view 2171 --json state` reads CLOSED; pytest on `tests/unit/web/test_list_item_count_2171.py`, 6 passed. Layer: GitHub and unit. Denominator: 1 issue, 6 pins.

-- Lead
