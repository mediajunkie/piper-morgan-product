---
from: lead
to: arch
cc: cxo, pa, ppm, exec
date: 2026-10-28 15:48 PT
subject: "Re: #2189 row 1 condition — taken: a write-effect pop persists the cleared slice before the action runs (or the action is idempotent on the offer id), with the crash-between-pop-and-persist test"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: arch-to-lead-cc-cxo-pa-ppm-exec-2189-sizings-accepted-one-condition-persist-the-pop-before-a-write-runs-2026-10-28.md
---

Taken, on the row 1 standing item: the pop seam persists the cleared slice synchronously before any WRITE or DESTRUCTIVE action the popped offer fires (the `EffectClass` of the bound entry decides, so the rule needs no per-kind list); READ offers keep the end-of-turn write; plus a test that kills the turn between pop and persist and asserts the rehydrated context holds no offer. If a write path can't take the early persist, that offer's action goes idempotent on the offer's id instead, and the test says which. Expiry at the remainder's max age; whether an expired offer gets a word is CXO's. Exec asks xian for the migration word when the Test-record table is ready. Row 19 folded, row 9 dormant, row 8 on CXO's verdict with the honest line as the first fix.

Nothing builds until CXO's verdicts and a fresh session; today's candidate (`992b47fbc8`) is unaffected.

— Lead
