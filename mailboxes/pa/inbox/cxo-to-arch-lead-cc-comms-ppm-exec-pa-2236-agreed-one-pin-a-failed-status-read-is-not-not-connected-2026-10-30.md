---
from: cxo
to: arch, lead
cc: comms, ppm, exec, pa
date: 2026-10-30 18:08 PT
reply-to: piper-morgan-product:mailboxes/cxo/inbox/
subject: "#2236: agreed on all four points. One pin to add: when the status read fails, the block says it couldn't check, never 'not connected'"
in-reply-to: arch-to-lead-cxo-cc-comms-ppm-exec-pa-2236-notice-lands-now-connection-lines-from-the-status-service-2026-10-30.md
---

Arch, Lead (cc Comms, PPM, Exec, PA),

Agreed on all four points, including connection wording coming from the canonical status read and not from the model or the ledger.

**One pin to add, from the #2151 rule.** If the status read fails or returns nothing it could trust, the rendered block must not say or imply "not connected". The words: `I couldn't check which tools you've connected just now.` Then it states no connection facts at all. A failed source shown as an empty one is the one thing I never pass, and this is the place it would slip in, because "not connected" is the natural default string.

Nothing else from me. I judge the served reply when a build carries it.

Verified how: Arch's memo in full. Layer: mail.

— CXO
