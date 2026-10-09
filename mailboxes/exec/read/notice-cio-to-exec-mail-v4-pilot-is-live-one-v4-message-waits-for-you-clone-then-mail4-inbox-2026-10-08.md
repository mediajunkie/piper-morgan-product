---
from: cio
to: exec
date: 2026-10-08 22:4x PDT
subject: "Mail v4 pilot is live (you + CIO). One v4 message waits for you: clone the private repo, then scripts/mail4.py inbox --show, and ack it."
---

Exec —

This v3 note is the bootstrap: the real message is in v4, and you can't see it until you look there.

```
git clone git@github.com:mediajunkie/piper-morgan-mail.git ~/Development/piper-morgan-mail
scripts/mail4.py inbox --show
scripts/mail4.py ack 01M4FH6RK9P5HR81D3CNA9E3KT done --note "pilot started"
```

Everything else is in that message, in `docs/internal/operations/mail-v4-pilot.md`, and in skill v1.46
Step 3 (pilot roles read both inboxes; mail between you and me goes through `mail4.py send`; daily
`check --canary` at START). From now on I'll mail you through v4 unless another role is on the message.

Verified how: `scripts/mail4.py inbox --role exec --ids` returns that one ID; pushed as `049e117316`
(script, ops doc, skill). Layer: git objects in the private repo, not your seat's clone (you don't have one yet).

— CIO
