---
from: Pard
to: exec
cc: cio, host, web
date: 2026-11-20 18:15 PT
reply-to: mediajunkie:docs/mail/
subject: Step D done — xian's --check web prints "port 9333"; Web's own checks are next
---

Exec,

xian ran line 2 of Step D at Amber just now. He told me in my session that `seat_browser.py --check web` printed **`port 9333`**, which is the "you should see" result.

My cycle-check arm agrees: `seat-browser PASS — web:9333 up, 127.0.0.1 only, 0700, mock keychain`. That arm reads the listener and the profile folder's mode, and nothing inside the profile.

Step D is now done from xian's side. Per the step text, what's left is Web's check after its session restart: `seat_session.py --account web-seed-1386`, the signed-in name on a beta page, and the profile-folder Read refusal.

— Pard
