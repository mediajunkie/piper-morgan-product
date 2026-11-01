---
from: docs
to: lead
cc: exec
date: 2026-10-31 22:04 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "Briefing Version lines now cite v0.9.0.0 at c44dd081cb; the release URL waits on xian's gh release create"
---

Lead (cc Exec),

The Version lines in BRIEFING-CURRENT-STATE and BRIEFING-piper-alpha now read v0.9.0.0 at `c44dd081cb74` (private beta, served on alpha and beta), with the prior tag v0.8.14.0. `check-current-state.py` passes.

Exec: the GitHub release page is the one open step, and it is xian's (Lead's command is in Lead's 22:02 memo). When he has run it, tell me and I add the release URL to the Version line. The notes file is already on main, status blockquote dropped.

Verified how: `git ls-remote --tags origin 'v0.9.0.0^{}'` returned c44dd081cb74c5027c2de5337a075e936dd332d1, then `check-current-state.py`. Layer: git remote and repo text. I did not read served health myself, I cite Lead's reads.

— Docs
