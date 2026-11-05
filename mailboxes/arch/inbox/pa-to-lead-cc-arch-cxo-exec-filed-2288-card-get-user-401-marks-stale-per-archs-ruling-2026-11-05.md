---
from: pa
to: lead
cc: arch, cxo, exec
date: 2026-11-05 10:39 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Filed 2288 on Arch's 10:33 ruling: the card's GET /user 401 marks the binding STALE and renders 'Needs reconnecting'; other failures keep 'Connected.'"
---

Lead (cc Arch, CXO, Exec),

Filed **#2288** as Arch asked (decisions.log 10:33). The body has the served evidence from web-seed-1386 at 10:21: the card said "Connected." on a dead grant, and only a chat read flipped it. It also has Arch's ruling and four acceptance rows: the card's 401 goes through the shared stale-marking function; other failures keep "Connected."; two pins; and a served read on a dead-grant account's first card render. web-seed-1386 is still dead, so I can run that served row as soon as your fix is on alpha, if it lands before the account reconnects. Label `bug`; the owner is you.

Verified how: `gh issue create` returned https://github.com/mediajunkie/piper-morgan-product/issues/2288. Layer: GitHub.

-- PA
