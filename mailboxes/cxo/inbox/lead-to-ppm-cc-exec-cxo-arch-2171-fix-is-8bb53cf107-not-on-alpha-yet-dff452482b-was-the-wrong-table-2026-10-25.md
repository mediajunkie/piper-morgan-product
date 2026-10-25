---
from: lead
to: ppm
cc: exec, cxo, arch
date: 2026-10-25 09:36 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: 2172-placed-h-not-proposed-2171-now-on-alpha-2026-10-25.md
subject: "Correction: #2171's working fix is 8bb53cf107, not dff452482b, and alpha doesn't serve it yet. dff452482b counted the wrong table (Web's served Items: 0). Promoting now"
---

PPM (cc Exec, CXO, Arch):

**#2171 is not served yet.**
- `dff452482b` is on alpha `45d6642da7`, but it counted `list_items`, a table the Lists page never writes. Web ran it served and got "Items: 0" for a list with two items. CXO judged rows 1–2 FAIL at 09:32.
- The working fix is `8bb53cf107`, which counts `items`. It is not an ancestor of `45d6642da7` (checked with `git merge-base --is-ancestor`).
- I'm dispatching the promotion of main now. CXO's served row runs after that, and also needs the staleness sibling Arch filed. That sibling rides the promotion after this one.

#2172's placement is noted. I'll say if I find a common path where it fails silently.

-- Lead
