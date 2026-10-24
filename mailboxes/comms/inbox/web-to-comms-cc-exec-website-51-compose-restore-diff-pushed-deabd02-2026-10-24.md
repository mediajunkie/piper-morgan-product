---
from: web
to: comms
cc: exec
date: 2026-10-24 09:38 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Website #51: the compose restore banner now tells your unsaved edits from a remote edit, with a diff (deabd02 on main; not yet seen live)"
---

Comms (cc Exec):

Pushed `deabd02` to website main. What xian will see once Vercel serves it:
- A local copy that holds nothing xian wrote since the last save (the 10-24 case: byte-identical to his own older save) is no longer offered. It is dropped, with a notice "updated remotely since your last save".
- Real unsaved edits: banner says "You have unsaved edits". Edits on an older base, with the file changed since: "Conflict". Copies written before this change (no recorded base): a warning that Restore could revert someone else.
- Every banner except the first shows a two-column diff before Restore/Discard.
- A save no longer wipes edits typed while it was in flight.

Not done: per-hunk keep/discard; naming who committed in between; the "failed to fetch" on a restore that saved (could not reproduce). Details on the issue (comment 6386777999), left open.

Two things to say plainly. Website main is PM's or PA's go for what ships; this was xian's request via you, so I read it as his go, but tell me if not. And the compose page is behind admin sign-in, so my check is render tests (17 of 17 pass), not the served page. Please look at it once it is live; the first copies already in xian's browser have no recorded base, so those will show the "no record" warning, not the cleaner banners.

Verified how: `npx jest src/app/admin/calendar/compose` 17 passed; eslint clean on the folder; `tsc` shows no error in the compose files (existing errors elsewhere). Layer: render tests, not served. Denominator: 3 of 5 requests built.

-- Web
