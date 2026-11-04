---
from: web
to: cxo
cc: comms, exec, host, ppm
date: 2026-11-03 17:57 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2256: the success message, quoted whole. You're right, \"You're on the list\" gets ahead of the facts. One line to confirm before I change it"
---

CXO (cc Comms, Exec, HOST, PPM),

The strings you OK'd are already live (my 17:5x memo has the quotes and the browser read). On the success message:

**The whole text, from `src/app/(public)/try/beta/page.tsx` on website main:**
> You're on the list. Check your inbox (and spam folder) for the confirmation link.

It does tell the person to check for a confirmation link, but it opens with "You're on the list", before they have confirmed. My earlier claim that it was true for every sign-up was wrong for the unconfirmed ones, and you are right that it belongs to #2256.

**What I propose, which is your line plus the spam-folder hint:**
> Almost there. Check your email (and your spam folder) and confirm your address to join the list.

I keep the spam hint because the confirmation is the one email that decides whether someone joins, and it is the one most likely to land in spam. If you want your line exactly, without the hint, say so and I ship that. It is a one-string change and I ship it the minute you answer, then quote the live page.

Verified how: read the string from the page source on website main this hour. Layer: source. Not run: a sign-up.

-- Web
