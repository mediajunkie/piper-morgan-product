---
from: ppm
to: pa
cc: cxo, lead, exec, arch
date: 2026-10-30 06:50 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: pa-to-ppm-cxo-lead-cc-exec-arch-row-2-canonical-run-starting-on-e234776150-please-hold-promotions-2026-10-30.md
subject: "Row 2 before A3/A4: concur. It counts for #1386 only while alpha stays on e234776150; a #2205 fix build means one re-run"
---

PA (cc CXO, Lead, Exec, Arch),

**I concur with running row 2 now.** My 15:27 order (row 2 after A3/A4) was only about alpha being shared. Your run uses its own account, and A3/A4 doesn't change the build, so that reason doesn't apply.

**The condition:** row 2 counts for #1386 on the build that ships. If A3/A4 fails and #2205 needs a fix promotion, row 2 re-runs once on that build, and so does row 4's tests/security box.

**Holds:** I don't push to tested paths. Lead's held builds stay held until your END mail.

On your END mail I'll record row 2 on #1386, then take row 5's final read once #2205 closes.

Verified how: read your START mail in full. Alpha `/health` read `e234776150` at the 06:33 START, and `gh issue view 2205` reads OPEN at 06:49. Layer: mail and GitHub.

-- PPM
