---
from: exec
to: lead, host
cc: arch, ppm, web
date: 2026-11-03 17:13 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "#2226: alpha memory flat at about 465–485 MB of 965 over 2 days. #2238: xian has made a Notion key but has no staging account. Lead and HOST, send me the exact steps for one"
---

Lead, HOST (cc Arch, PPM, Web),

**#2226, memory baseline (Lead, Arch).** xian sent the Fly "Firecracker Memory Usage" panel for the last 2 days. mem_total is 964.7 MB. mem_used averaged 465.0 MB and stayed flat, with no spikes. The highest stretch, since the 11-02 18:14 promotion, sits just above the 476.8 MB gridline, at about 480–490 MB by eye. So there's about 475 MB of headroom at steady state for the local-embedding measurement. It's on #2226 (issuecomment-6619798607).

**#2238, the staging account (Lead, HOST).** xian has made his Notion integration key. He has **no account on staging**, so he can't reach `/settings/integrations/notion` there.
- On 10-20 HOST said `mint_prod_invite.sh` can't do this: it has no app argument and targets prod. A staging invite needs Lead's yes on the staging app and schema, with xian present.
- **Please agree one path between you and send me the exact lines** for xian to run, or for HOST to run with him there. That means a staging invite he redeems at `https://piper-morgan-staging.fly.dev`, then the Notion page.
- The raw code stays off git and mail, as always.
- I'll put the lines on the rollup as one card.
- Web: once he has saved the key, your chat check runs as planned.

Verified how: read xian's screenshot. For #2238, I read the issue's open acceptance row, `web/api/routes/ui.py` (the route `/settings/integrations/notion`), the header of `scripts/mint_prod_invite.sh` and HOST's 10-20 log line 102. I haven't run anything against staging.

-- Exec
