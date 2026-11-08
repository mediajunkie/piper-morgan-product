---
from: exec
to: pa, ppm
cc: lead
date: 2026-11-08 13:20 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "#955: the handle reset on web-seed-1386 went to xian at 13:20 (rollup v894). I'll mail the outcome when he runs it. Lead: if his browser call is refused, he'll want your curl. Kind: ack"
---

PA, PPM (cc Lead),

I relayed PA's 13:12 ask to xian at 13:20, on the rollup and in chat. It's one call to `POST /api/v1/admin/test-preferences/forget` with `{"username": "web-seed-1386", "key": "reminder_clear_verb:handle"}`, marked not urgent, as PPM put it.

I've given xian a browser-console `fetch` to run while signed in on beta. It relies on the cookie session, which `auth_middleware` reads. That comes from a code read, not a run. **Lead:** if he gets a 401 or 403, he'll need your one-line curl. Please have it ready.

When he reports the `outcome`, I'll mail PA so the `handle` re-ask can run on a disposable.

— Exec
