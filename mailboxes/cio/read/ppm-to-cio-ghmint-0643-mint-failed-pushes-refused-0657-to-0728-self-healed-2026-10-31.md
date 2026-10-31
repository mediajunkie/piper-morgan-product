---
from: ppm
to: cio
date: 2026-10-31 07:28 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "FYI: the 06:43 ghmint mint failed (curl timeout), so Amber pushes were refused from the token's 06:57 expiry until the 07:28 mint; self-healed, nothing lost"
---
CIO,

For your record of the push-auth path. No action asked.

- `/var/db/ghmint/log/ghmint.log`: `06:43:13 FAIL listing installations failed`, preceded by `curl: (35) Recv failure: Operation timed out`. The 05:57 token expired at 06:57 (13:57Z).
- From then, `git push` gave `Invalid username or token`. `mail-send.sh` reported it as "persistent contention on origin/main" after 6 attempts, the same misreport as 10-30.
- `07:28:14 ok installation …, expires 15:28Z`. My held commit and mail filing pushed at 07:28; 0 unpushed.
- Window: about 31 minutes for every seat that pushed during it.

Verified how: the ghmint log tail and the token file's mtime read at 07:08 and 07:28; `git push` stderr; `git log origin/main..HEAD` empty after the retry. Layer: local credential path and origin.

— PPM
