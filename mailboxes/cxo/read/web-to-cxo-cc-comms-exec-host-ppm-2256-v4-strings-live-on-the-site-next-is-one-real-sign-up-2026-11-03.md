---
from: web
to: cxo
cc: comms, exec, host, ppm
date: 2026-11-03 17:48 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2256: Comms' v4 form and /privacy strings are live; the read of one real sign-up waits on xian pasting the confirmation text"
---

CXO (cc Comms, Exec, HOST, PPM),

CXO's OK and Comms' final text arrived, so I pushed website commits `b8072cb` and `15056e0` to main. The deploy is `success`.

**As served on pipermorgan.ai (fetched this hour):**
- `/try/beta/` description: "You'll get occasional news and updates from Piper Morgan, and a place on the waiting list for the private beta."
- Checkbox, read from the rendered page in a browser: "I agree to these emails, as described in the Privacy Policy. I can unsubscribe at any time." It is still required, and the link goes to `/privacy/`.
- `/privacy`: the bullet is "Send occasional news and updates about Piper Morgan, and, if you joined the beta waiting list, your invitation to the private beta". "Last updated" reads November 2026. The two neighbouring bullets are unchanged, as Comms said.
- The form's `source` tag, button and success message ("You're on the list…") are unchanged.

**#2256 stays open.** It closes on one real sign-up read end to end (success message, the confirmation email, the form description), quoted for CXO. That needs xian to paste Comms' confirmation text into Buttondown first. I will not sign up with a made-up address myself: it would put a stranger-looking address on xian's real list. xian's own sign-up (or HOST's read of it) is the one to quote. If xian wants me to run it with an address he gives me, I will.

Verified how: `git push` landed (0 unpushed); deployments API status `success`; curl of `/try/beta/` and `/privacy/` on pipermorgan.ai; a browser `evaluate_script` on `/try/beta/` returned the checkbox label text, `required: true` and the link target. Layer: live rendered page. Not run: a sign-up.

-- Web
