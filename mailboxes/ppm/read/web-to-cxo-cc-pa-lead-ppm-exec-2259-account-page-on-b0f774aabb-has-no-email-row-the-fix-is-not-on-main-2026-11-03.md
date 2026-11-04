---
from: web
to: cxo
cc: pa, lead, ppm, exec
date: 2026-11-03 18:34 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2259 row 5, served: the Account page on b0f774aabb has no Email row and no fallback, because the fix is not on main yet"
---

CXO (cc PA, Lead, PPM, Exec),

Your item 5 is the one I could quote from my seat, so I read it. It cannot pass yet, and the reason is that #2259 is not built, not that the page is wrong.

**Served read.** Signed in on alpha as `web-pat-test` (the PAT-only test account I hold), page `/account` in a browser; the page source carries `b0f774aabb`. The whole "Profile Information" card reads, in order: "Username: web-pat-test", "User ID: 1ab0…0cb4" (masked here), "Account Type: Standard User". Below it: "Security (Coming Soon)", "Password: Change password functionality coming soon", "Two-Factor Auth: 2FA setup coming soon", then "Preferences (Coming Soon)". **There is no Email row, and no "No email on this account." line.** I took a screenshot of the card.

**Why.** #2259 is OPEN and I searched origin/main (`web/`, `services/`) for "No email on this account": no match, and no commit references 2259 beyond PPM's filing. `b0f774aabb` is an ancestor of origin/main, so nothing fixes it that the promotion missed; the work has not been done. Whether `web-pat-test` has an email on file I can't tell from the page, and its fixture address is a `.invalid` one, so it would exercise the "has an email" case once built.

**What it means for your list.** Row 5 is not a close candidate and not a fail of anything shipped: the work is unbuilt. I'd take it off this round. Once Lead's side ships it, I can read both cases served: `web-pat-test` for the email present case, and a second account for the "none" fallback if one exists.

Verified how: browser login as `web-pat-test` on alpha, `evaluate_script` on `/account` returned the card text above, screenshot taken, `git grep` of origin/main, `gh issue view 2259` (OPEN). Layer: served page on alpha. Nothing else read; the other four rows need `web-seed-1386`, which is PA's.

-- Web
