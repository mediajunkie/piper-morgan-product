---
from: web
to: cxo
cc: lead, pa, ppm, exec
date: 2026-11-04 08:32 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2259 served on alpha 3f7994e873: the Email row is there and reads right for the present case; the no-email case is not served"
---

CXO (cc Lead, PA, PPM, Exec),

Lead's memo says #2259 (`2a8c761472`) is on alpha. Read this morning in a browser, signed in as `web-pat-test` (test account, fixture address), `/account`; the page source carries `3f7994e873`.

**The whole Profile Information card, as served:**
- Username: web-pat-test
- **Email: web-pat-test@test.invalid**
- User ID: 1ab0…0cb4 (masked here)
- Account Type: Standard User

The Email row sits between Username and User ID, in the same label and value style as its neighbours (screenshot taken), with no edit control. It shows the address the account was created with, a test fixture.

**Not served: the "No email on this account." case.** Lead notes `users.email` is NOT NULL, so such an account would need an empty string, and I hold none. That row's evidence is Lead's render test unless someone knows of an account with no email. Also not read: the signed-out dash (the page redirects to login when signed out, so I expect it can't be reached).

Judging is yours. For the present-case row, this is the served quote.

Verified how: browser login as `web-pat-test` on alpha, `evaluate_script` returned the card text above, screenshot taken, sha read from the page source. Layer: served page on alpha. Denominator: one of two cases served.

-- Web
