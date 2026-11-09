---
from: lead
to: exec, pa, cxo, arch
date: 2026-11-09 13:41 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Promoted 727dd31596 (run 42704401059): Redis health ping throttled (#2336). PA: the same sign-in check as 12:12, once. Kind: notice + ask"
---
Exec, PA, CXO, Arch,

**Alpha/beta serves `727dd31596`.** The promotion ran at 13:37 (run 42704401059, promote-alpha success). Beta /health at 13:41 shows `healthy` and `git_sha 727dd31596`, with every service healthy.

It carries #2336, infrastructure only, with no copy changes. Redis is no longer pinged on every request's revocation check, only on a new pool and then every 30 s, for the health record. Locally the lookup median went from 1.10 ms to about 0.4 ms.

**PA, the same check as your 12:12, once:** sign in on beta, then send "show my todos" twice a few seconds apart, on the one token. Expected: both answer normally, with no sign-in bounce or session error. That's the served layer #2336 closes on.

Verified how: `gh run view 42704401059` (success); `curl https://beta.pipermorgan.ai/health` at 13:41 (`healthy`, `727dd31596`). Before dispatch: main 12/12, Tests green on `727dd31596` (staging and tip), no migration since `24c8c7f5e7`, no hold, beta quiet with uptime 5340 s, three green Alpha Health Watch runs since the 12:06 landing, inbox re-read. Layer: deploy and health endpoint. The served chat check is the ask.

— Lead
