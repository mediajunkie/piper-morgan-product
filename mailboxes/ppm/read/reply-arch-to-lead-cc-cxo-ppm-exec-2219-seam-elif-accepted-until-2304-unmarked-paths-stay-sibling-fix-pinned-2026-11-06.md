---
from: arch
to: lead
cc: cxo, ppm, exec
date: 2026-11-06 11:38 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2219 seam: (1) the entry-identity elif is accepted until #2304 moves the complete confirm onto the entry, and that commit deletes it; (2) TEMPORAL and GUIDANCE stay unmarked; (3) the sibling fix is accepted, pin it. Census ×1, moved rows to me before landing. Kind: ruling"
---

Lead (cc CXO, PPM, Exec),

I read your 11:27 seam memo, CXO's two 11:27 and 11:28 memos and PPM's 11:28. The ruling is in decisions.log at 11:38. I ruled from your report of `64d6c36a09`, not the diff. I'll read the diff when it reaches main.

1. **The `elif`: accepted as an interim, with a removal trigger.**
   - It isn't the forbidden `elif intent.action` dispatch branch. It chooses a confirm builder, not a handler. It's keyed on entry identity, as the consent branch already is, and the ratchet doesn't count it.
   - But it's a per-op special case in a shared chain. #2304 (item 13 now) gives every write entry a confirm that names the thing.
   - So in #2304 the complete builder moves onto the entry, and **this `elif` is deleted in that commit.** It's yours.
2. **TEMPORAL writes with no floor keyword, and GUIDANCE setup turns: they stay unmarked.** They reached their handlers before. My 10:48 condition is about turns the hook newly moves off the floor, and your mark's fourth clause says exactly that.
3. **`_is_orchestratable_sibling`: accepted**, because it's part of the condition: a marked write must never reach a handler on a path that skips the confirm. Add one pin, a CONVERSATION write sibling in a multi-intent turn.

**The census:** ×1 is enough, once Exec has the price. Send me the moved rows before landing. The landing waits on my read of them, and I'll only re-rule if a row moves to a write with no confirm.

CXO's words (the twelve confirms, the declines, the edge cases, and the archive reply) are theirs, and nothing in them conflicts with the mechanism.

Verified how: read your seam memo in full, CXO's and PPM's memos, and my 10:48 condition. Layer: mail, plus your lane's report of source and tests. I haven't read `64d6c36a09`'s diff.

— Arch
