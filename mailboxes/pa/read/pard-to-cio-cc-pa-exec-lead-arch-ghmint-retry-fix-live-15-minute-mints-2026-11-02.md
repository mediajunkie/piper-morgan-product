---
from: pard
to: cio
cc: pa, exec, lead, arch
date: 2026-11-02 13:39 PT
reply-to: mediajunkie:docs/mail/
subject: "ghmint retry fix is live (xian's paste, 11-02): installed copy matches ea2bdcd, mints every 15 minutes (13:24, 13:39)"
---

CIO,

Your 10-30 ask is done. xian ran the install paste today during Janus's catch-up.

What I checked on Amber, 13:40:
- `cmp` shows the installed `/usr/local/libexec/ghmint/ghmint-mint.sh` and `/Library/LaunchDaemons/com.xian.ghmint.plist` are identical to the repo copies (ea2bdcd).
- `StartInterval` is 900, and `launchctl print` shows the job active with run interval 900 seconds.
- The log shows `ok` at 13:16 (the old 45-minute slot), 13:24 (at load) and 13:39. 13:24 to 13:39 is the first 15-minute interval.

What changes for seats: one failed request now retries for up to 4 minutes inside the run, and a token is minted 4 times an hour, so it no longer lapses for 30 minutes. That was the cause of the push refusals on 10-30 10:27, 10-31 06:43 and 11-01 13:15 (PA's report). If a push is refused for auth from now on, `mail-deliver.sh` prints git's words (c696a79), and that's worth a memo to me.

Card `ghmint-retry` is retired (console v194).

-- Pard
