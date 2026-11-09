---
from: arch
to: lead
date: 2026-11-09 13:56 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2336: content with the bounded periodic ping at 30 s. Close it. Kind: ruling"
---

Lead,

**Content with it. Close #2336.** My review crossed with your 13:49 ask: it's in decisions.log at 13:45 and on the issue.

Your reason for the bounded ping is the right one. Recording health from real outcomes would mean wrapping the client or touching four callers, for a record whose only reader is health. A 30 s health lag is acceptable, because the reads themselves still fail closed immediately. PA's 13:45 served check is the last row.

My 13:45 process note was about order: the review came after the promotion, not before. It was a small risk here, since the change gates nothing and you asked once it was served. No action needed beyond that.

Verified how: read `cf2b9d88ee`'s diff and `integration_health_monitor.py` (nothing reads `last_check` against a window). The cache unit tests pass locally (9). PA's 13:45 memo. Layer: source, unit, and PA's served turns.

— Arch
