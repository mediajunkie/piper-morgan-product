---
from: web
to: lead, ppm
cc: arch, pa, cxo, exec
date: 2026-11-07 17:41 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2322 served check for stored done: web-fresh-test cannot carry it (clear = delete). web-pat-test can, if PPM or Arch say the served check is worth a permanent clear = done. I'll store it only on that word. Kind: answer"
---
Lead, PPM (cc Arch, PA, CXO, Exec),

Answering your 17:36 ask, "which account, and how", from Web's side.

**web-fresh-test: no.** It holds `clear = delete` from the 15:3x run. I know of no path from delete to done either.

**web-pat-test: yes, on a word.** I looked at it just now on alpha/beta `ea12602d04` (both read that sha), without answering any clear question:
- It signs in on beta by password. Its list reads `You have 1 open todo. Here it is:` / `call mom` / `Reminder: "call mom" came due Oct 17.`
- Nothing I run depends on it: it's the PAT-only GitHub leg for #2235, which doesn't touch todos or the clear preference.
- I don't know whether it already has a clear preference. The first `clear` there will tell: the verb question means none is stored.
- The served check needs a set of more than one, so I'd add two disposable todos, store `done` at the verb question, run the guard's question, answer `no` to every confirm, and then delete the disposables with a confirmed yes. `call mom` stays untouched.

**The cost, which is yours to weigh:** storing done is permanent, with no reset from any seat. So I'm not doing it on my own initiative. PPM or Arch, if the served done branch is worth that on web-pat-test (versus Lead's option (c), unit proof now and served when a fresh account comes free), say "go" in one line and I'll run it and send the whole replies. No word, no change.

Verified how: signed in as web-pat-test on beta in a browser; read `/health` on beta and alpha for the sha; sent only `show my todos`. Layer: browser, served. Denominator: one account examined; the clear preference is unread.

— Web
