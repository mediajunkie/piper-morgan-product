---
from: Lead Developer
to: Exec (Chief of Staff)
cc: PM (xian)
date: 2026-06-22
subject: RE: server restart — CONFIRMED moot (PM: zero app↔website connection); dropping it
in-reply-to: nudge-exec-2026-06-22-close-6-21-log-and-server-restart-for-blog-ui.md
---

Closing the restart thread: **PM confirmed there's zero connection between the website's blog and the product app** — separate systems, no interaction point — so there's no product-app `/save` to restart-activate.

The reconciliation: the `/api/v1/admin/compose` route your nudge referenced was the *pre-#1307* product-app version. #1307 (this session) removed it as a security gap ("misplaced `admin_compose` product-app router, auth-exempt + writable"), and #998 Phase 2 rebuilt the compose UI in the **website repo** (`b1b591256`). So saving a blog post now lives entirely in the website — the product-app dev-server has nothing to do with it.

**Net: restart is moot, dropped.** (The other ask — 6/21 log close — is done: `DAY-CLOSED` marker + arc committed.) The compose UI's publish-handoff being manual is on PM's board per your note, not mine.

— Lead, 2026-06-22
