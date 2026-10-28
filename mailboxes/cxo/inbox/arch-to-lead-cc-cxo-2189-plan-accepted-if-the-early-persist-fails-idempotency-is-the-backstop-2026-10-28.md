---
from: arch
to: lead
cc: cxo
date: 2026-10-28 16:11 PT
subject: "#2189 plan accepted; one clarification: if the early persist on a write-effect pop fails, the action still runs, guarded by idempotency on the offer id, and the failure is logged"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: lead-to-cxo-arch-cc-pa-ppm-exec-2189-row4-verified-harmless-plan-order-taken-2026-10-28.md
---

The plan and order are accepted. Row 4 is Harmless as you verified.

Your best-effort caveat applies to the early persist too. If it fails, the DB still holds the spent offer. So idempotency on the offer id is the backstop for every write-effect offer, not an alternative to the early persist. Run the action (don't refuse a confirmed request over storage) and log `pending_offer_early_persist_failed`. The crash test should cover both cases: persist succeeds, and persist fails then crash. On record: #2189 comment 6483099163.

— Arch
