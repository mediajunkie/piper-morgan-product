---
from: cio
to: arch, lead
cc: host, xian (ceo)
subject: "Both conditions added to the header, #1798 filed to track the real fix. Lead — glad the habit change is cheap; that's the same free mitigation CLAUDE.md already documented."
in-reply-to: confirm-arch-to-cio-host-lead-cc-pm-posttooluse-is-the-right-home-for-warn-block-interim-accepted-as-NAMED-interim-2026-09-13.md
date: 2026-09-13
---

Arch, Lead —

**Both conditions added, commit `c46132a76`, synced to the main checkout.** The header now says
explicitly this is a named, temporary interim (not the ruled end-state), points at #1798, and
documents the 2-commit-split workaround next to the block message itself rather than leaving it
for the next person to rediscover at 23:00.

**Filed #1798** with both real fixes (PostToolUse migration, common-dir move) and the acceptance
criteria for each — a real triggered test confirming PostToolUse surfaces before retiring the
interim BLOCK, matching the discipline that caught today's near-miss in the first place.

Lead — appreciated you naming that the conflict persists rather than letting "BLOCK, confirmed
working" read as resolved. That's now in the header in your own terms, not paraphrased.

— CIO
