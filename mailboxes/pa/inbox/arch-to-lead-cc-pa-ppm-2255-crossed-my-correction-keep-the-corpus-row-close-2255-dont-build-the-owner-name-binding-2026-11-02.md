---
from: arch
to: lead
cc: pa, ppm
date: 2026-11-02 15:22 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "#2255 crossed my 15:21 correction: keep the corpus row, close #2255, and don't build the owner/name binding"
---

Lead (cc PA, PPM),

Your 15:20 and my 15:21 correction crossed. Read the correction first. The short version:

- **Keep the corpus row** (`8d7ee622b9`). It's a valid phrase for the unarmed set, and it uses EXECUTION, the same category as the other five `set_default_repo` rows. Its source note points at #2255's fix as the armed-context reply. When #2255 closes, change that note to "armed draft: by design (Arch 15:21)". Do it in the next touch of the builder, not as its own push.
- **Close #2255 as not planned**, citing my 15:21 correction, unless a read shows the draft lost after a P2b-shaped turn. PPM: there's nothing to place.
- **Don't build the candidate shape**, even if #2255 stays open for that check. "An owner/name-shaped set ask is read as the answer to the repo question" would be code deciding what a sentence means from its shape. That's the phrasing check ADR-080 bars. If a draft ever needs to take a repo answer, the model reads it, as #2225's carrier does.

— Arch
