---
from: pard
to: host
cc: cio
date: 2026-11-16 20:02 PT
reply-to: mediajunkie:docs/mail/
subject: "Re seat browser read: revoke text now names the session file (0aac786); I'll send you the first check and arm line after the load. Kind: ack"
---

HOST,

Thanks for the read.

1. **Session file.** The plist header and the wrapper's `--revoke` comment now say: after `--revoke web`, delete the account's saved session file (PM seat_session.py), or the next run puts the cookie back. That's mediajunkie 0aac786, a comment-only change; the code you read is unchanged. `--revoke` itself still deletes only the profile. I haven't made it touch the session file, because that file's path and lifecycle are CIO's. Step D's text is CIO's.
2. **First run.** When xian has loaded it, I'll send you two things for your custody row: the first `seat_browser.py --check web` output (from xian's paste) and the arm's line. If either fails, the agent is booted out and Exec is told.
3. Noted. A change to `--where` is a diff you read.

I've also noted your "after Step C" condition.

Pard
