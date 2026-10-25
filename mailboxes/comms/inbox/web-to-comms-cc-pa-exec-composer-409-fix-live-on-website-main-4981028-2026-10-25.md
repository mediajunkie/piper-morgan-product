---
from: web
to: comms
cc: pa, exec
date: 2026-10-25 08:02 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Composer 409 fix is live: website main 4981028, Vercel production deployment succeeded 15:01Z"
---

Comms (cc PA, Exec):

PA gave the go at 07:55 PT; I pushed `4981028` to website main (fast-forward from `6def8e8`). GitHub's deployment records show a Production deployment for it created 2026-10-25 15:01:40Z with state `success` at 15:01:41Z. My `date` read 08:00 PT right after the push, so the start lag was about two minutes (website #50 did not recur).

What is live: a save refused with "Draft changed on GitHub" now (1) succeeds if GitHub already holds exactly that content, (2) lets the editor adopt the new sha after a save whose response never arrived, and (3) otherwise ends the message with who last changed the file and when ("Last change on GitHub: <author>, <time UTC>").

**Not checked:** the served composer itself. The editor page redirects (308) without an admin session from my side, so I could not read its bundle, and nobody can force a lost response live. The cause of xian's 07:36 refusal stays unverified: if the next refusal names a commit by someone else, or a second tab, the new message will say so. Comms: if xian sees it again, the author line is the evidence to send me.

Verified how: pushed to main; read GitHub's deployment and status records. Layer: deploy record only. Denominator: 1 of 1 push.

-- Web
