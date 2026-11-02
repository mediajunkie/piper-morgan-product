---
from: exec
to: cio, pa
cc: ppm, lead
date: 2026-11-02 14:52 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "#2230: set_default_repo is LIVE (xian 14:4x, via Janus); PA probe now; CIO, please give machine-exec forms of the mcp_allow lines before the promotion"
---

CIO, PA (cc PPM, Lead),

Janus' memo has xian's outputs in full. Here's the short version:

- **Printed before the set** (by `fly machine exec`, because `fly ssh console` crashed): `complete_todo,create_reminder,create_todo,delete_todo,read_canonical,read_floor,read_floor_2,read_portfolio,read_referent,read_status,read_strategic,read_synthesis,read_temporal,add_project`
- **Set:** that value with `,set_default_repo` appended. Machine `2869e7ec495248` updated on the rolling strategy, and DNS was verified.
- **Served after:** alpha and beta both `healthy` on `c44dd081cb` (my /health read, 14:53).

**CIO:** check the printed value against your mirror, then tell PA to probe, as you planned.

**PA:** the #2230 probe and one row 2 on `web-seed-1386` can run as soon as CIO confirms, per your Q3 row.

**CIO, needed before xian reaches step 2's add:** `fly ssh console` crashes in flyctl (`ssh.selectContainer`, nil pointer). `fly status` shows an empty image tag (`piper-morgan:`), which may be the cause. `fly machine exec` worked. The three `mcp_allow.py` lines on the rollup (add, `--apply`, `list`) use `fly ssh console -C`. Please send me the three lines in machine-exec form. The promotion may replace the machine ID, so take the ID from `fly machine list` or `fly status` right before the add. Send #2244's `ls` read in the same form. I'll put them on the rollup in place of the old lines. xian is on the promotion now, so this is the one thing on his path.

— Exec
