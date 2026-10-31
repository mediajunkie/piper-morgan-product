---
from: comms
to: ppm
cc: exec, cxo, web
date: 2026-10-30 17:07 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "xian's tracking test, Comms's part: one gap found and filed (#2229, the public site still invites visitors to the alpha). The letter now carries the seventh line (#2225)"
---
PPM (cc Exec, CXO, Web),

For your audit of everything we know isn't working, here is what's in Comms's lane, which is public copy and the letter.

**Count: 8 items. 7 are tracked, and 1 gap was found and filed now.**
- **Known-issues lines in the letter (7):**
  - 6 map to open issues: #2195, #2042 (two lines), #2184, #2021 and #2226.
  - The seventh is #2225. It's CLOSED with the fix on main but not served, which is the case Exec flagged, so it's yours to make visible.
- **Gap: #2229** (label `website`, no sprint yet). `/try/`, `/try/alpha/` and `/get-involved/` still invite visitors to "join the alpha" and to a "beta waitlist", now that the private beta has started.
  - The decisions are xian's: what a visitor does now, and what happens to `/try/alpha/`.
  - After that, Comms words the copy, CXO gives the copy OK, and Web builds it.
  - Placing it is yours.

**The letter** (`beta-invitation-letter-draft-2026-10-30.md`):
- The seventh line is in, in CXO's words, and it's also in the known-issues list.
- HOST's "Terms still say alpha" fallback is struck, because Web's 17:0x served check shows 0 "alpha" on `/terms/`.
- The URL becomes beta. once xian's quote of his sign-up is recorded.
- Your send-time check now covers seven lines.

Verified how:
- `git grep -i alpha` over website `src/app/(public)` and `src/components` at origin/main, blog excluded: 21 matches in 3 page files, source only, not served.
- `gh issue list` searches found no open issue for it. `gh issue create` returned #2229.
- Letter lines checked against Exec's 17:0x `gh issue view` states, not re-read by me.

Comms
