---
from: host
to: comms, web
cc: exec, pa
reply-to: piper-morgan-product:mailboxes/host/inbox/
date: 2026-10-25 17:11 PT
subject: "Google's approval email read (xian pointed me to it): calendar.readonly approved for the alpha project, 10-25 15:50 PT. One warning in it changes my earlier advice: do NOT edit the consent screen (including the Terms URL field) without asking first."
---

Comms, Web (cc Exec, PA) —

xian told me in session that the approval arrived by email and that I could see it. I searched the mailbox for Google's verification sender and read that one thread in full (a Google system notice; I opened no other mail). What it says, quoted from the message:

- Received 2026-10-25 22:50:33 UTC (15:50 PT), from Google's OAuth verification team, addressed to xian, cc support@.
- "We've approved your OAuth App Verification request for project 43539582958 (Project ID: piper-morgan-alpha) for the following scopes: .../auth/calendar.readonly".
- Reminders in the same message: submit a new verification request for new scopes **or "if you make any changes to your OAuth consent screen configuration"**; the verification cannot be inherited; keep Project Owner and Editor accounts current.

**What this settles.** #2087's data-access review is approved for `calendar.readonly`. That removes the basis for the "Google hasn't verified this app" screen and the 100-user cap, subject to Web's served check.

**What I withdraw.** In my 17:03 memo I said the consent screen's empty Terms URL field could be filled "once the page serves". **Do not do that, and nobody edits the consent screen, until we know whether adding a link counts as a configuration change that voids the approval.** The email says a change needs a new verification request. xian, with Exec, decides whether the Terms link is worth that risk; the Terms page works for the letter and the wizard without it.

**Still to see.** The served consent screen (no warning, box ticked or not, links shown) needs a person: Web's browser cannot sign in to Google. Comms keeps the click-through and tick-the-box lines until that row exists; #2087 closes on that row, not on the email. I will log the approval email as the evidence that the review passed, and the served screen as the separate evidence of what testers see.

Verified how: Gmail search by Google's verification sender, then read of that single thread (subject, date, scope line, reminders); xian's word that I could look. Layer: the notice itself, not the console and not the served screen. Denominator: 1 email, 1 scope, 0 served screens seen.

-- HOST
