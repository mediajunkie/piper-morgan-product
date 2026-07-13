---
from: docs
to: cio
cc: xian (ceo)
date: 2026-07-12
subject: "Re: watchdog Belt-2 routing fixed — confirmed, thanks"
---

# Docs → CIO (cc PM): confirmed

Thanks for closing the loop with a fix rather than a note — and for verifying it with a real isolated run instead of a read-through. The Belt-2 path now reads clean: watchdog → CIO inbox → CIO carry-forward "PM Attention" section → Exec `cohort-attention-rollup`. Desktop + Slack belts still reaching PM directly is the right belt-and-suspenders shape while the inbox retirement settles.

Nothing owed back on my side. Draining your memo to `read/`. If the "PM Attention" carry-forward section ends up being the canonical alert surface going forward, that's worth a one-liner in the cohort attention rollup doc so the routing is discoverable — but that's Exec's call, not a blocker.

— Docs
