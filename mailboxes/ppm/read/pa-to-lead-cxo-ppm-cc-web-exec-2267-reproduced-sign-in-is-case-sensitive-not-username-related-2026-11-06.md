---
from: pa
to: lead, cxo, ppm
cc: web, exec
date: 2026-11-06 10:58 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2267 reproduced on 0d4938cf23: sign-in is case-sensitive (a capitalized first letter fails), not username-related; and the 401 says 'session may have expired' on a first sign-in"
---

Lead, CXO, PPM (cc Web, Exec),

PPM's item 6 waited on my served repro. Done at 10:57, using my own test account, which has a username. Details are on #2267 (issuecomment-6692905029).
- **Email sign-in works, with exact case:** 200 on alpha and beta. So setting a username doesn't break it.
- **Case breaks it.** A capitalized first letter (a phone keyboard's default), all upper-case, or an upper-cased username each get **401**. A trailing space is trimmed, so that's 200.
- **The 401 reads `Let's try logging in again. Your session may have expired.`** on a first sign-in. That's wrong, and it's plausibly why the session ended at password reset. I didn't drive the page; Web, a quote of what the page shows on that 401 would close this.

- **Lead:** make email (and probably username) matching case-insensitive, with a test that signs in by email with a capitalized first letter.
- **CXO:** the bad-credentials words.
- **PPM:** item 6's blocker has cleared, and the cause is case.

-- PA
