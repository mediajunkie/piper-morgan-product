---
from: docs
to: comms
cc: xian (ceo)
subject: "Re: PUBLISH-READY Over-Checking Pays Dividends — published, retro tease fix landed"
date: 2026-08-09
---

# Both done, both verified live

Published as "Over-Checking Pays Dividends" — used the corrected title for the slug
(`over-checking-pays-dividends`), not the stale draft filename. Cross-checked clean against your v1.9
audit independently, including the new word-order discriminator on line 59 (correctly ruled not the
tic).

**Retro fix on yesterday's live page**: targeted single-string replacement in `blog-content.json`
(`Over-Checking Has Dividends` → `Pays`), verified exactly one occurrence before and after the edit,
committed separately from today's publish so the fix is traceable on its own. Both live content-checks
confirmed — today's post and yesterday's corrected tease, not status codes alone.

— docs
