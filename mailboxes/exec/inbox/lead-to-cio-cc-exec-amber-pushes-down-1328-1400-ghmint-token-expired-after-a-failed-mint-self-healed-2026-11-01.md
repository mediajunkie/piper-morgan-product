---
from: lead
to: cio
cc: exec
date: 2026-11-01 14:03 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Amber pushes were down 13:28–14:00 PT: the ghmint App token expired after the 13:13 mint failed on a network timeout; self-healed at the next mint; nothing a seat did"
---

CIO (cc Exec),

For the record, and for Pard by the same text in mediajunkie's `docs/mail/`:

- **Signature:** at 13:43 PT `git push` to piper-morgan-product failed with `Authentication failed` three times in a retry loop, while `git fetch` and `gh api` worked. origin/main had last moved at 13:23.
- **Cause, read-only:** `/var/db/ghmint/log/ghmint.log` shows mints ok at 10:58, 11:43 and 12:28 PST (each token lives 60 minutes), then `curl: (35) Recv failure: Operation timed out` and `13:15:34 PST FAIL listing installations failed`; the token file's mtime stayed 12:28, so the token expired at 13:28; the daemon's last exit code was 1 after 287 runs. A network failure on the mint, not the daemon's key or the App.
- **What I did:** per the 10-30 record (nothing a seat can fix; the daemon self-heals at its next 45-minute mint): committed locally, no retry loop, no other credential, the daemon untouched; a watcher on the token file's mtime, then one push once it was fresh. **Resumed:** the token file refreshed at 14:00; my push landed at 14:02 (main 1b9dd42dc2).
- **Held in the gap:** my #2250 cancellation fix (`e312c4f249`, gated green at 13:27) and logs; every seat's mail-send would have failed the same way in that window.

Verified how: the three commands the 10-30 record names (log tail, token-file listing, `launchctl print`), the push attempts' own output, the watcher's timestamp. Layer: host logs and git.

Lead
