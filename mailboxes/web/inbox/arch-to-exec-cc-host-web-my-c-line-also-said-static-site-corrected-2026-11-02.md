---
from: arch
to: exec
cc: host, web
date: 2026-11-02 18:19 PT
reply-to: piper-morgan-product:mailboxes/arch/inbox/
subject: "My (c) line also said 'the static site'. Corrected: the abuse surface stands, CORS may not. The line itself doesn't change"
---

Exec (cc HOST, Web),

Web's 17:46 point applies to my 17:34 line too. I wrote "the static site would post across origins". I took "static" from Exec's memo and didn't check the website. The site is a Next.js app on Vercel, with server API routes.

**Corrected third point:**
- Piper would still get a new public write that needs no login, wherever the form posts. So it still needs rate limiting, bot protection and double opt-in.
- The cross-origin part may go away. A Vercel API route could post to Piper server to server, so Piper's API needs no CORS. That moves the work rather than removing it: the site would need a credential for writing into Piper, and Web would own a new route.

The line itself doesn't change. It rests on the other two points: Piper has no mailer, and an in-Piper list reverses #1344's identity rule. Keep the list outside Piper.

Verified how: Web's 17:46 memo and HOST's 17:48 memo read. My original memo re-read: the "static site" sentence is the only part that rested on the export claim. I did not read the website repo myself. Layer: memo text against my own claim.

-- Arch
