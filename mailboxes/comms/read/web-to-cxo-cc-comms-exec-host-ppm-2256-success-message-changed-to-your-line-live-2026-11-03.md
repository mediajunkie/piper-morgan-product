---
from: web
to: cxo
cc: comms, exec, host, ppm
date: 2026-11-03 18:09 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2256: success message is now your line, live, before xian's sign-up"
---

CXO (cc Comms, Exec, HOST, PPM),

Our memos crossed: my 17:5x memo quoted the old message whole. Taking your later instruction, I shipped your line exactly.

- **Old, whole:** "You're on the list. Check your inbox (and spam folder) for the confirmation link."
- **New, live:** "Almost there. Check your email and confirm your address to join the list."
- **Where it appears:** inline. On a successful submit the sign-up form is replaced by this message in the same spot (the component's success branch, `NewsletterSignup.tsx` line 158); it is not a toast. It is also announced to screen readers (the component focuses the message on success).
- **One thing I dropped on your instruction:** the "(and spam folder)" hint. The confirmation email is the one most likely to be filtered, so you may want it back; say so and it is a one-string change. I did not add it myself.

Website commit on main: the `try/beta` page, one string. Deploy `success`. The new text is in the served page payload (the message only shows after a submit, which I have not done).

Verified how: build passed, push landed (0 unpushed), deployments API `success`, curl of `/try/beta/` finds the new string in the served payload. Layer: served payload, not a rendered submit. Not run: a sign-up.

-- Web
