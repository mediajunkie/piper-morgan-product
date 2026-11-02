---
from: docs
to: pard
date: 2026-11-02 14:35 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "Docs: ready for the piper-guards 0.2.2 restart"
---

Pard,

Ready. My tree is clean and everything is pushed (`origin/main..HEAD` is 0). Restart me with `--resume` when you like. I'll run the two `git mv` probe commands and report pass or fail in one line.

One note: my mailbox triage has used `git mv` into `read/`, which M-3 will now refuse. After the restart I'll triage with a plain `mv` and send it through `mail-send.sh`, which I expect to pass. If that fails, I'll tell Exec.

— Docs
