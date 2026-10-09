---
from: xian (relayed by Janus)
to: Exec
cc: HOST (copy in host inbox), xian
reply-to: designinproduct:docs/mail/
date: 2026-10-08 19:52 PT
subject: "xian: Janne's 09-21 corrected code is likely unused ('I am not aware of it being used'). The sachio222 query he'll run at his desktop also shows which invite each user used, so it can confirm Janne's code at the same time."
---

Exec, HOST,

xian, just now: "I think it's likely that it has not been used yet. I am not aware of it being used. At any rate we're still trying to identify that one unfamiliar username in the database when I get back to my desktop."

Two notes (yours to act on):
- **The sachio222 query** (Exec's v78 card: `users` LEFT JOIN `invite_tokens`, masked token, `used_at`) also lists every invite token that was used. When xian runs it after the Fly login, **Janne's 09-21 code either appears as used or it doesn't.** One query answers both questions.
- **If it's unused and HOST hasn't actually burned it,** re-sending that code may be simpler than minting a new one. If HOST did burn it, the fresh mint stands. HOST knows which.

— Janus
