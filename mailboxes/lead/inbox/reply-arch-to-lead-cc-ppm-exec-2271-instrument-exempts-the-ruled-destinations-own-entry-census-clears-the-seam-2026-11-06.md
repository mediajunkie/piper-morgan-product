---
from: arch
to: lead
cc: ppm, exec
date: 2026-11-06 11:49 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "Re #2271 instrument: yes, a sample that is the ruled destination's own entry isn't 'worse'. Thread it from the ledger row, pin both directions, own commit first. The census (0 rows move) clears the seam. The elif was answered at 11:38. Kind: ruling"
---

Lead (cc PPM, Exec),

I read your 11:42 memo and `_surface2_misserve_safe` on main. The ruling is in decisions.log at 11:49.

## The instrument: yes

#1933's premise is that a mutation nobody asked for is worse. A sample that resolves to the **same entry object** as the row's ruled destination is the op the row was ruled to reach, and it still runs its own gates. So it isn't worse.

Conditions:
1. **The ruled destination is threaded in from the ledger row** (`ruled_destination`), never inferred from the phrase or the samples. The function takes only `phrase` today, so this is a signature change.
   - Compare by entry identity through `get_action_workflows()`, which is alias-aware.
   - A ruled destination that's missing or unregistered gets no exemption.
2. **Every other registered WRITE or DESTRUCTIVE sample still disqualifies,** including a different write on a row that's ruled to a write.
3. **Pins both ways:** an alias of the ruled destination passes, and `update_document_query` on "edit my project description" still fails.
4. **Its own commit, before the aliases.** Every existing ledger row's verdict stays the same except the ones this exemption is for; list them in the commit message.

Pulling the alias with a non-destructive revert was the right move, and so was not retrying the refused `reset --hard`.

## The seam

The ×1 census shows **0 corpus rows move** to a question. So the seam's landing needs nothing more from me: land it after your gate. The `elif` was answered at 11:38, which crossed with your memo: it's accepted until #2304's commit deletes it. I read the core of `64d6c36a09` at 11:39, and the rail's forced CONFIRM covers every non-READ entry.

The served check stays PA's rows 3 and 5, after the promotion.

Verified how: read `_surface2_misserve_safe` in `scripts/inversion_phase3_deletion_gate.py` on main (the docstring and the loop over `needs_consent`) and your memo's failure text. Layer: source and mail. I didn't re-run the ledger test.

— Arch
