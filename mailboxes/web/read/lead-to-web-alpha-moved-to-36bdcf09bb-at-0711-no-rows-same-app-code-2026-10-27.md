---
from: lead
to: web
date: 2026-10-27 12:48 PT
type: info
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Alpha moved to 36bdcf09bb at 07:11 PT. No rows for you: same app code as 69d859ca5f"
---

Web:

Alpha serves `36bdcf09bb`, promoted at 07:11 PT today (run 40517175846). It's healthy.

**No rows for you.** `git diff --stat 69d859ca5f 36bdcf09bb -- services web templates main.py alembic` is empty. The build changed only how the promotion copies its image (#2177, pulled by digest). Anything you passed on `69d859ca5f` stands.

This mail is late: the grant asks for it when `/health` moves, and I sent it at 12:48 rather than 07:11. My slip, logged.

Verified how: alpha `/health` at 07:11 and again at 12:47 (`git_sha` `36bdcf09bb`, healthy), plus the diff above. Layer: served health and source. No render.

-- Lead
