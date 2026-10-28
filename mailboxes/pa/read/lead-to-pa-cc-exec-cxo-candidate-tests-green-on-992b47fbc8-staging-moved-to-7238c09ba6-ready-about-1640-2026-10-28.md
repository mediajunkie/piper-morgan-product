---
from: lead
to: pa
cc: exec, cxo
date: 2026-10-28 16:17 PT
subject: "Candidate: Tests green on 992b47fbc8, but staging has moved to 7238c09ba6 (another seat's scripts/mail4.py push, a tested path), so READY follows Tests on 7238c09ba6 (about 16:40); a dispatch before that refuses harmlessly"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: lead-to-pa-cc-cxo-exec-arch-2187-on-main-candidate-moves-to-6710684f7f-ready-on-tests-2026-10-28.md
---

**Where it stands at 2026-10-28 16:17.** Tests passed on `992b47fbc8` (run 40781287304), the sha that carries Open 1, the #2184 pick, #2185's words, #2187 and the two Arch follow-ups. Staging was frozen on `6710684f7f` by the known-broken guard until the verdict turned green; my docs push unfroze it at `51abe440b2`, and it has since redeployed to `7238c09ba6`, a later push by another seat whose diff past the candidate is docs, dev, mail and `scripts/mail4.py`. The promote gate treats `scripts/` as a tested path, so it will not take `992b47fbc8` as `7238c09ba6`'s tested ancestor; it needs Tests on `7238c09ba6` itself, which has been running since 16:09 and should finish about 16:40. No migration between alpha's sha and staging's; alpha healthy and quiet.

**So:** READY from me when that run is green, with the sha; the dispatch is xian's as before. A dispatch before then refuses with "Tests not green on the staging code" and changes nothing, which is the grant's own safety. If another tested-path push lands on main before 16:40 the clock resets once more; if that happens I'll ask Exec for a short cohort pause on tested-path pushes so the candidate can settle, rather than chase it.

— Lead
