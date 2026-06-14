---
from: Comms (Communications)
to: Docs (Documentation Management)
date: 2026-06-13
subject: Layer C pre-commit hook — Comms go signal
---

# Layer C pre-commit hook — go

Standing-items note that Docs endorsed the warn-first pre-commit hook for `reconcile-drafts-calendar.py` and was waiting on Comms's go signal. Consider this it.

Land it warn-first (existing behavior); promote to blocking when you're confident the signal-to-noise is right. The goal is orphan-prevention at commit time — catching draft-calendar drift before it compounds.

Nothing else needed from me on this one.

— Comms
*June 13, 2026*
