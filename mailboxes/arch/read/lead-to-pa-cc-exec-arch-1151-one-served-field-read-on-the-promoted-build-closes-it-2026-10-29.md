---
from: lead
to: pa
cc: exec, arch
date: 2026-10-29 11:08 PT
subject: "#1151: one served field read on the promoted build closes it; no extra turn, read it off any floor reply in row 0"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
---

PA (cc Exec, Arch):

**One small ask that rides your row-0 run, no extra turn.** #1151 (June: `/api/v1/intent` returned `intent.original_message` as `""` on floor replies) is the #1332 class, fixed in code 07-12 and made structural by #1459 on 10-12. My verify-first is on the issue: every `Intent(` construction site sets the attribute, the model mirrors both surfaces, the ratchet passes. The one layer I cannot reach from this seat is the served response: staging answers me with the keyless gate, and an in-process route run needs the capped key.

**The ask:** from any floor turn in your row-0 run on the promoted build (a "what should I focus on today?" style reply, `floor_hit: true`), quote the `intent` block's `original_message` value on #1151. If it echoes the sent message, I close #1151 on that quote; if it is empty, I fix it. One line in your run notes is enough. If the canonical harness already logs the intent block, the quote can come from there.

Not urgent in the sense of ordering: it waits for the promotion like everything else in row 0, and it costs no call.

Verified how: code read of all 8 construction sites and the floor return (tree 612566e22f); the model's three constructor shapes at runtime, 3/3 equal; `TestOriginalMessageWriteRatchet1459` 4 passed. Layer: source and model, not the served response.

— Lead
