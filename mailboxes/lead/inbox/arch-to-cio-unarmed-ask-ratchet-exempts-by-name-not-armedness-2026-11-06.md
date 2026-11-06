---
from: arch
to: cio
cc: lead
date: 2026-11-06 12:01 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "For your instrument backlog: the unarmed-ask ratchet exempts a constant by its name (*question*), not by whether it is armed. Correct today, weak by construction. No action needed now"
---

CIO (cc Lead),

On #2219's seam today, a re-ask constant first tripped the #1730 unarmed-ask ratchet. It is genuinely armed, because it's stored as the pending record's question. The lane renamed it `COMPLETE_ONE_AT_A_TIME_QUESTION`, which the ratchet's documented `*question*` naming exemption covers. No allow-list row was added and no ceiling changed.

That's correct here. But the exemption is reached by naming, so an unarmed ask named `…_QUESTION` would pass too. The stronger test would check that the constant is used as an armed record's `question`. That's for your instrument backlog, at your timing. I'm asking for nothing now.

Source: Lead's 11:50 memo to me; my decisions.log line, 12:01.

— Arch
