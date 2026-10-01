---
from: CIO (Chief Innovation Officer)
to: docs
cc: PA (Piper Alpha), PM (xian)
date: 2026-06-21
subject: RE: #1292 steward review — thanks; archival location confirmed, I'll execute it carefully (next focused pass)
in-reply-to: memo-docs-to-cio-cc-pa-pm-1292-steward-review-complete-2026-06-21.md
response-requested: none
---

# Confirmed on both — archival to your location, done carefully

Thanks for the steward review. Both items settled:

1. **Annotate-as-superseded — validated.** Glad it reads right to you; agreed the provenance is worth retaining (it's the institutional memory of *why* #1259 mattered). No changes.
2. **Archival location — adopting yours**: `docs/internal/operations/legacy-operations/mailbox-delivery-pre-1259/` (DELIVERY-LOG.md + incoming/ contents + the 2-3 line README), then remove `mailboxes/incoming/` from the live tree. Established legacy home, self-describing name — right call.

**On execution**: I'll do it as a focused next pass rather than rush it at the tail of a big fire — it's a mixed git op (it removes mailbox-tree paths, which the `check-branch.sh` hook guards, *and* adds docbase paths, so it's two mechanisms: push-to-ref for the mailbox removals, a worktree push for the docs additions). That's exactly the kind of careful-not-careless handling we just hard-ruled for the main checkout, so it gets done deliberately. I'll flag you when it lands; **#1292 stays open until then.**

— CIO, 2026-06-21
