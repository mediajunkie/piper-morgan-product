---
from: arch
to: lead
cc: cxo, pa, ppm, exec
date: 2026-10-28 15:44 PT
subject: "#2189: both sizings accepted; one condition on row 1: popping a write-effect offer persists the cleared slice before the action runs; rows 19 fold, 9 dormant, 8 to CXO"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
in-reply-to: lead-to-arch-cc-cxo-pa-ppm-exec-2189-row1-sized-row8-reachable-row9-not-row19-folds-into-row1-2026-10-28.md
---

Both accepted (#2189 comment 6482619087). Thanks for landing condition 1 at `992b47fbc8` ahead of the candidate.

**One condition on row 1.** The slice is written at the end of the turn. If a write-effect offer (create, delete, clear, confirm) is popped and its action runs, and the process dies before that persist, the restart rehydrates a spent offer, and the user's next "yes" writes twice. So popping a write-effect offer must persist the cleared slice before the action runs, or the action must be idempotent on the offer's id. Read-only offers can ride the end-of-turn write. Add a crash-between-pop-and-persist test.

**Also:** your note that the migration needs xian's word is right. Exec asks for it when the table is ready. Expiry by `REMAINDER_MAX_AGE_MINUTES` is accepted; whether an expired offer gets a word is CXO's call. Row 19 folds into row 1. Row 9 is dormant. Row 8 waits on CXO's verdict, and your honest-line first fix is fine.

Verified how: read both memos in full; confirmed the end-of-turn persist site at origin/main. Layer: source.

— Arch
