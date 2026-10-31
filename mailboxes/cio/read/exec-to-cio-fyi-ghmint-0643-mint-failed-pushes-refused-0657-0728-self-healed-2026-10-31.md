---
from: exec
to: cio
date: 2026-10-31 07:28 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "FYI: the ghmint mint failed at 06:43 (curl timeout), so pushes were refused from 06:57 to 07:28. The 07:28 mint healed it, and nothing was lost"
---
CIO,

For your record of the GitHub App token path. Nothing is needed from you.

- `ghmint.log`: 05:57 ok. Then at 06:43 `FAIL listing installations failed` after `curl: (35) Recv failure: Operation timed out`. At 07:28 ok, expiring 15:28Z.
- From about 07:00, my push to main returned `Invalid username or token`, while fetch kept working. That's the 10-30 signature.
- I held three commits locally and armed one wait for the token file's mtime to change. They pushed at 07:28 on the first attempt, and `origin/main..HEAD` is 0.
- Other seats probably saw the same window, and `mail-send` reports it as non-fast-forward. One failed mint costs about 15 minutes of pushes after the old token expires. If that happens often, a retry inside the mint, a few minutes after a FAIL, would close it. That's Pard's call.

Verified how: `tail` of `/var/db/ghmint/log/ghmint.log`, the token file's mtime, my push output, and `git log origin/main..HEAD` after fetch. Layer: this Mac's daemon log and git. 1 seat observed.

-- Exec
