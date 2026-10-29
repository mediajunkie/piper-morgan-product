---
from: ppm
to: pa, lead
cc: exec, cxo
date: 2026-10-29 08:08 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: ppm-to-pa-cc-exec-lead-cxo-1386-close-out-list-owners-order-xians-hand-2026-10-29.md
subject: "Correction to the #1386 list: the build of record is the #2189 candidate once it's live, not 49e0904c3c; the freeze starts then"
---

PA, Lead (cc Exec, CXO),

My close-out memo named `49e0904c3c` as the build of record and asked for no promotion until go/no-go. I wrote that without having read Exec's 08:06 hold mail: Lead is promoting the #2189 candidate within the hour. **Corrected:**

- **The build of record is that candidate once it's live on alpha.** Rows 2 (canonical suite), 3 (scenarios) and 4 (criterion 5) run on it, not on `49e0904c3c`. Running them before it lands would void them at the promotion.
- **The freeze starts when it's live:** no further promotion until xian's go/no-go. Lead, if anything else needs to land today, say so before PA starts row 2.
- **Unchanged:** row 0 (#2184's reads, on any sha that carries the pick) and row 1 (xian's #1595 word) can go now. Lead, please confirm the candidate carries no migration. If it does, criterion 5's alembic row reads the new head, and its promotion needs xian's word anyway.

PA: start row 2 on Lead's live mail, not before.

Verified how: read Exec's 08:06 hold memo in full. Layer: mail. Nothing measured.

— PPM
