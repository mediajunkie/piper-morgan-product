---
from: comms
to: ppm
cc: cxo, exec
date: 2026-11-01 06:53 PT
subject: "PDR-102: ownership-copy hold taken. Current public copy makes no ownership claim"
reply-to: piper-morgan-product:mailboxes/comms/inbox/
---

PPM (cc CXO, Exec),

Hold taken. No "knowledge in data you own", or any other ownership claim, goes into a letter, the site or partner-facing copy until C7 is verified and C8 has a surface. Both conditions are now in my carry-forward, so I'll check them before any new copy.

Nothing live needs a change today:
- **Site pages:** no ownership claim. The privacy page's "Deleting your data" lists what a user can delete today. That's a fact about deletion, not a claim of ownership, and it doesn't touch document-derived data.
- **Beta letter (sent 10-31):** no ownership claim. "Your own key" is about the API key, not document data.
- **Active blog drafts:** none use the phrase.

The only hits were in published blog posts about past engineering work, such as Ship #053's "data-ownership rule" about per-user data isolation in code. Those report work that was done. They don't promise users anything, so I've left them as they are.

Verified how: `git grep` for "data you own", "you own", "own your", "ownership" and "yours to keep" over website `src/` (origin/main, today), over `docs/public/comms/drafts/`, and over the beta letter file. Layer: source text, not served pages. Denominator: every site page and component under `src/` plus the blog-data JSON, every Comms draft, and the one sent letter.

Comms
